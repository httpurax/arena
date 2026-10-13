#!/usr/bin/env python3
"""Offline tests for the arena-pr-watcher skill.

Stdlib-only and network-free: the watcher's only network path is the `gh` CLI,
which is patched at the JSON level (`pr_watch.gh_json`) with canned payloads.
Everything else is a pure function, a temp state file, or the skill's own
convention files.

Covered:

  * the skill's conventions: frontmatter identity (name == directory, version,
    license, category, description length), the gitignored state directory,
    the shipped (fictional) state example, and the README table + installer
    mapping entries;
  * CI-state buckets from check runs and from the legacy combined status,
    including the vacuous-green guard (no checks at all is not green);
  * state change detection: baseline, opened, green/failing transitions,
    no-notification when nothing changed, failing -> running -> failing
    announced exactly once, and silent pruning of closed PRs;
  * message formatting: number/title/branch/checks/link per PR, one batched
    message for several PRs, empty string for a quiet tick;
  * end-to-end ticks through `run()`: stdout is the Telegram message, the
    state file is written atomically and re-diffed, `--dry-run` changes no
    state, `--json` is read-only, and a `gh` failure exits 1 without touching
    the state file.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List
from unittest import mock

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = SKILL_ROOT.name
SKILL_MD = SKILL_ROOT / "SKILL.md"
GITIGNORE = SKILL_ROOT / ".gitignore"
EXAMPLE_STATE = SKILL_ROOT / "examples" / "pr-state.example.json"
README = SKILL_ROOT.parent.parent / "README.md"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "pr_watch.py"

_spec = importlib.util.spec_from_file_location("pr_watch", SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
pr_watch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pr_watch)

REPO = "httpurax/arena"


def make_pr(number: int, title: str, branch: str, sha: str) -> Dict[str, Any]:
    """A `gh pr list --json` row (raw CLI shape, pre-checks)."""
    return {
        "number": number,
        "title": title,
        "headRefName": branch,
        "headRefOid": sha,
        "url": f"https://github.com/{REPO}/pull/{number}",
        "createdAt": "2026-10-01T00:00:00Z",
    }


def snapshot(pr: Dict[str, Any]) -> Dict[str, Any]:
    """The internal snapshot `fetch_open_prs` produces from a CLI row."""
    return pr_watch.normalize_pr_item(pr, REPO)


def with_checks(pr: Dict[str, Any], checks: str, detail: str) -> Dict[str, Any]:
    out = dict(pr)
    out["checks"] = checks
    out["checks_detail"] = detail
    return out


def check_run(status: str = "completed", conclusion: str = "success") -> Dict[str, Any]:
    return {"status": status, "conclusion": conclusion}


def stored_state(prs: List[Dict[str, Any]], repo: str = REPO) -> Dict[str, Any]:
    """The same shape pr_watch.build_state writes, from checked PRs."""
    return {
        "version": pr_watch.STATE_VERSION,
        "repo": repo,
        "updated_at": "2026-10-13T00:00:00+00:00",
        "prs": {
            str(p["number"]): {
                "title": p["title"],
                "branch": p["branch"],
                "sha": p["sha"],
                "url": p["url"],
                "checks": p["checks"],
            }
            for p in prs
        },
    }


GREEN = "all 12 checks passed"
GREEN_PR = with_checks(snapshot(make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40)),
                       pr_watch.CHECKS_GREEN, GREEN)
FAILING_PR = with_checks(snapshot(make_pr(43, "Update the README", "docs/readme", "b" * 40)),
                         pr_watch.CHECKS_FAILING, "2 of 9 checks failed")
RUNNING_PR = with_checks(snapshot(make_pr(44, "Add rate limiting", "feat/rate-limit", "c" * 40)),
                         pr_watch.CHECKS_RUNNING, "3 of 7 checks in progress")


# ---------------------------------------------------------------------------
# skill conventions
# ---------------------------------------------------------------------------

class TestConventions(unittest.TestCase):
    def read_frontmatter(self) -> Dict[str, str]:
        lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0].strip(), "---", "SKILL.md must open with frontmatter")
        fm: Dict[str, str] = {}
        for line in lines[1:]:
            if line.strip() == "---":
                return fm
            if not line or line.lstrip().startswith("#"):
                continue
            if line[0] in (" ", "\t"):
                continue  # nested keys (metadata.hermes) are checked separately
            key, sep, value = line.partition(":")
            self.assertTrue(sep, f"frontmatter line is not key: value: {line!r}")
            fm[key.strip()] = value.strip()
        raise AssertionError("frontmatter block is not closed")

    def test_frontmatter_identity(self):
        fm = self.read_frontmatter()
        self.assertEqual(fm.get("name"), SKILL_NAME, "name must match the directory")
        self.assertEqual(fm.get("version"), "1.0.0")
        self.assertEqual(fm.get("license"), "MIT")
        description = fm.get("description", "")
        self.assertTrue(description, "description must not be empty")
        self.assertLess(len(description), 60, "description stays under 60 characters")
        platforms = fm.get("platforms", "")
        for platform in ("linux", "macos", "windows"):
            self.assertIn(platform, platforms, f"platforms must include {platform}")

    def test_category_is_productivity(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("category: productivity", text,
                      "the installer maps this skill under the productivity category")

    def test_state_directory_is_gitignored(self):
        text = GITIGNORE.read_text(encoding="utf-8")
        self.assertIn("data/", text, "the state directory must be gitignored")

    def test_example_state_is_valid_and_fictional(self):
        data = json.loads(EXAMPLE_STATE.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], pr_watch.STATE_VERSION)
        self.assertEqual(data["repo"], REPO)
        self.assertIsInstance(data["prs"], dict)
        self.assertTrue(data["prs"], "the example must show at least one PR record")
        for number, record in data["prs"].items():
            self.assertTrue(number.isdigit(), f"PR key {number!r} must be a number")
            for field in ("title", "branch", "sha", "url", "checks"):
                self.assertIn(field, record, f"example record #{number} misses {field}")
            self.assertIn(record["checks"],
                          (pr_watch.CHECKS_GREEN, pr_watch.CHECKS_FAILING, pr_watch.CHECKS_RUNNING))

    def test_readme_table_entry_and_installer_mapping(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn(f"[`{SKILL_NAME}`](skills/{SKILL_NAME}/)", text,
                      "README skills table entry missing")
        self.assertIn(f"<skills root>/productivity/{SKILL_NAME}/", text,
                      "README installer layout mapping missing")

    def test_no_secrets_shipped(self):
        """Nothing that looks like a credential may sit in the skill's text files."""
        import re
        patterns = (
            re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
            re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
            re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
            re.compile(r"(?i)\b(?:api[_-]?key|passwd|password|token)\b\s*[:=]\s*['\"][^'\"]+['\"]"),
        )
        for path in sorted(SKILL_ROOT.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".json", ".py", ".txt"):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for pattern in patterns:
                self.assertIsNone(pattern.search(text),
                                  f"credential-shaped value in {path.relative_to(SKILL_ROOT)}")


# ---------------------------------------------------------------------------
# CLI-row normalization
# ---------------------------------------------------------------------------

class TestNormalizePrItem(unittest.TestCase):
    def test_fields_map_to_snapshot(self):
        item = make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40)
        self.assertEqual(pr_watch.normalize_pr_item(item, REPO),
                         {"number": 42, "title": "Fix the flaky test",
                          "branch": "fix/flaky-test", "sha": "a" * 40,
                          "url": "https://github.com/httpurax/arena/pull/42"})

    def test_missing_optional_fields_degrade_gracefully(self):
        item = {"number": 7}
        self.assertEqual(pr_watch.normalize_pr_item(item, REPO),
                         {"number": 7, "title": "", "branch": "", "sha": "",
                          "url": "https://github.com/httpurax/arena/pull/7"})


# ---------------------------------------------------------------------------
# CI-state buckets
# ---------------------------------------------------------------------------

class TestSummarizeCheckRuns(unittest.TestCase):
    def test_all_green(self):
        runs = [check_run(), check_run(), check_run(conclusion="skipped"),
                check_run(conclusion="neutral")]
        self.assertEqual(pr_watch.summarize_check_runs(runs),
                         {"checks": pr_watch.CHECKS_GREEN, "detail": "all 4 checks passed"})

    def test_failing_on_failure(self):
        runs = [check_run(), check_run(conclusion="failure")]
        self.assertEqual(pr_watch.summarize_check_runs(runs),
                         {"checks": pr_watch.CHECKS_FAILING, "detail": "1 of 2 checks failed"})

    def test_cancelled_and_timed_out_count_as_failing(self):
        runs = [check_run(conclusion="cancelled"), check_run(conclusion="timed_out")]
        self.assertEqual(pr_watch.summarize_check_runs(runs),
                         {"checks": pr_watch.CHECKS_FAILING, "detail": "2 of 2 checks failed"})

    def test_in_progress_and_queued_are_running(self):
        runs = [check_run(), check_run(status="in_progress", conclusion=None),
                check_run(status="queued", conclusion=None)]
        self.assertEqual(pr_watch.summarize_check_runs(runs),
                         {"checks": pr_watch.CHECKS_RUNNING, "detail": "2 of 3 checks in progress"})

    def test_action_required_is_running_not_failing(self):
        runs = [check_run(conclusion="success"), check_run(conclusion="action_required")]
        self.assertEqual(pr_watch.summarize_check_runs(runs),
                         {"checks": pr_watch.CHECKS_RUNNING, "detail": "1 of 2 checks in progress"})

    def test_empty_list_is_none(self):
        self.assertIsNone(pr_watch.summarize_check_runs([]))


class TestSummarizeCombinedStatus(unittest.TestCase):
    def test_success(self):
        self.assertEqual(pr_watch.summarize_combined_status({"state": "success", "statuses": [1, 2]}),
                         {"checks": pr_watch.CHECKS_GREEN, "detail": "all 2 status checks passed"})

    def test_failure(self):
        self.assertEqual(pr_watch.summarize_combined_status({"state": "failure", "statuses": [1]}),
                         {"checks": pr_watch.CHECKS_FAILING, "detail": "status checks failing"})

    def test_pending(self):
        self.assertEqual(pr_watch.summarize_combined_status({"state": "pending", "statuses": [1, 2, 3]}),
                         {"checks": pr_watch.CHECKS_RUNNING, "detail": "3 status checks in progress"})

    def test_no_statuses_is_not_vacuously_green(self):
        """GitHub reports `state: success` for a commit with zero statuses; the
        watcher must not call that green."""
        self.assertEqual(pr_watch.summarize_combined_status({"state": "success", "statuses": []}),
                         {"checks": pr_watch.CHECKS_RUNNING, "detail": "no checks reported yet"})


# ---------------------------------------------------------------------------
# state change detection
# ---------------------------------------------------------------------------

class TestPlanEvents(unittest.TestCase):
    def test_baseline_silently_records_open_prs(self):
        events, state = pr_watch.plan_events([GREEN_PR, RUNNING_PR], None, REPO)
        self.assertEqual(events, [])
        self.assertEqual(set(state["prs"]), {"42", "44"})
        self.assertEqual(state["prs"]["42"]["checks"], pr_watch.CHECKS_GREEN)
        self.assertEqual(state["repo"], REPO)

    def test_new_pr_after_baseline_is_opened(self):
        state = stored_state([RUNNING_PR])
        events, new_state = pr_watch.plan_events([RUNNING_PR, GREEN_PR], state, REPO)
        self.assertEqual([e["number"] for e in events], [42])
        self.assertTrue(events[0]["opened"])
        self.assertEqual(set(new_state["prs"]), {"44", "42"})

    def test_running_to_green_notifies(self):
        state = stored_state([with_checks(GREEN_PR, pr_watch.CHECKS_RUNNING,
                                          "1 of 12 checks in progress")])
        events, _ = pr_watch.plan_events([GREEN_PR], state, REPO)
        self.assertEqual([(e["number"], e["checks"]) for e in events],
                         [(42, pr_watch.CHECKS_GREEN)])
        self.assertFalse(events[0]["opened"])

    def test_running_to_failing_notifies(self):
        state = stored_state([with_checks(FAILING_PR, pr_watch.CHECKS_RUNNING,
                                          "2 of 9 checks in progress")])
        events, _ = pr_watch.plan_events([FAILING_PR], state, REPO)
        self.assertEqual([(e["number"], e["checks"]) for e in events],
                         [(43, pr_watch.CHECKS_FAILING)])

    def test_green_to_failing_notifies(self):
        state = stored_state([GREEN_PR])
        events, _ = pr_watch.plan_events([FAILING_PR], state, REPO)
        self.assertEqual([(e["number"], e["checks"]) for e in events],
                         [(43, pr_watch.CHECKS_FAILING)])

    def test_failing_to_green_notifies(self):
        state = stored_state([FAILING_PR])
        events, _ = pr_watch.plan_events([GREEN_PR], state, REPO)
        self.assertEqual([(e["number"], e["checks"]) for e in events],
                         [(42, pr_watch.CHECKS_GREEN)])

    def test_no_change_no_events(self):
        """The no-notification case: identical PRs, identical CI states."""
        state = stored_state([GREEN_PR, FAILING_PR, RUNNING_PR])
        events, _ = pr_watch.plan_events([GREEN_PR, FAILING_PR, RUNNING_PR], state, REPO)
        self.assertEqual(events, [])

    def test_change_to_running_does_not_notify_but_updates_state(self):
        state = stored_state([FAILING_PR])
        running = with_checks(FAILING_PR, pr_watch.CHECKS_RUNNING, "1 of 9 checks in progress")
        events, new_state = pr_watch.plan_events([running], state, REPO)
        self.assertEqual(events, [])
        self.assertEqual(new_state["prs"]["43"]["checks"], pr_watch.CHECKS_RUNNING)

    def test_flapping_pr_notifies_second_failure_exactly_once(self):
        """failing (announced) -> running (silent) -> failing (announced once)."""
        state = stored_state([FAILING_PR])  # previous tick already announced the failure
        events1, state_after_running = pr_watch.plan_events(
            [with_checks(FAILING_PR, pr_watch.CHECKS_RUNNING, "1 of 9 checks in progress")],
            state, REPO)
        self.assertEqual(events1, [])
        events2, _ = pr_watch.plan_events([FAILING_PR], state_after_running, REPO)
        self.assertEqual([(e["number"], e["checks"]) for e in events2],
                         [(43, pr_watch.CHECKS_FAILING)])
        events3, _ = pr_watch.plan_events([FAILING_PR],
                                          pr_watch.plan_events([FAILING_PR], state_after_running,
                                                               REPO)[1], REPO)
        self.assertEqual(events3, [], "a still-failing PR is not re-announced")

    def test_closed_prs_are_pruned_silently(self):
        """Merged/closed PRs drop out of the state without a message: this skill
        notifies only; a human does the merging."""
        state = stored_state([GREEN_PR, FAILING_PR])
        events, new_state = pr_watch.plan_events([GREEN_PR], state, REPO)
        self.assertEqual(events, [])
        self.assertEqual(set(new_state["prs"]), {"42"})

    def test_state_is_rebuilt_from_current_prs_only(self):
        state = stored_state([FAILING_PR])
        _, new_state = pr_watch.plan_events([GREEN_PR], state, REPO)
        self.assertNotIn("43", new_state["prs"])
        self.assertEqual(new_state["prs"]["42"]["checks"], pr_watch.CHECKS_GREEN)


# ---------------------------------------------------------------------------
# message formatting
# ---------------------------------------------------------------------------

class TestFormatMessage(unittest.TestCase):
    def test_empty_when_no_events(self):
        self.assertEqual(pr_watch.format_message(REPO, []), "")

    def test_single_green_pr_carries_number_title_branch_checks_link(self):
        message = pr_watch.format_message(REPO, [{**GREEN_PR, "opened": False}])
        self.assertEqual(message, (
            f"{REPO}: 1 PR update\n"
            "\n"
            "✅ #42 all checks green — ready to merge\n"
            "   Fix the flaky test\n"
            "   fix/flaky-test\n"
            f"   checks: {GREEN}\n"
            "   https://github.com/httpurax/arena/pull/42"
        ))

    def test_failing_header_and_detail(self):
        message = pr_watch.format_message(REPO, [{**FAILING_PR, "opened": False}])
        self.assertIn("❌ #43 checks failing", message)
        self.assertIn("checks: 2 of 9 checks failed", message)

    def test_opened_headers(self):
        self.assertEqual(pr_watch.event_header({**RUNNING_PR, "opened": True}),
                         "🆕 #44 opened")
        self.assertEqual(pr_watch.event_header({**GREEN_PR, "opened": True}),
                         "🆕 #42 opened — all checks green")
        self.assertEqual(pr_watch.event_header({**FAILING_PR, "opened": True}),
                         "🆕 #43 opened — checks failing")

    def test_several_prs_batch_into_one_message_sorted_by_number(self):
        events = [
            {**FAILING_PR, "opened": False},
            {**GREEN_PR, "opened": False},
            {**RUNNING_PR, "opened": True},
        ]
        message = pr_watch.format_message(REPO, events)
        self.assertEqual(message.count("httpurax/arena: 3 PR updates"), 1)
        # one header block per PR, in PR-number order (42, 43, 44)
        pos_green = message.find("✅ #42")
        pos_fail = message.find("❌ #43")
        pos_open = message.find("🆕 #44 opened")
        self.assertTrue(-1 < pos_green < pos_fail < pos_open)
        for line in ("   Fix the flaky test", "   Update the README", "   Add rate limiting",
                     "   fix/flaky-test", "   docs/readme", "   feat/rate-limit",
                     "   https://github.com/httpurax/arena/pull/42",
                     "   https://github.com/httpurax/arena/pull/43",
                     "   https://github.com/httpurax/arena/pull/44"):
            self.assertIn(line, message)
        # exactly three "checks:" lines — every PR block carries its check state
        self.assertEqual(message.count("checks: "), 3)


# ---------------------------------------------------------------------------
# end-to-end ticks (gh_json patched, temp state file)
# ---------------------------------------------------------------------------

class FakeGitHub:
    """Stands in for `gh` at the JSON level: a PR list plus per-SHA CI data."""

    def __init__(self, prs: List[Dict[str, Any]], checks_by_sha: Dict[str, List[Dict[str, Any]]],
                 status_by_sha: Dict[str, Dict[str, Any]] | None = None):
        self.prs = prs
        self.checks_by_sha = checks_by_sha
        self.status_by_sha = status_by_sha or {}

    def __call__(self, args: List[str], timeout: float) -> Any:
        # Patched at the gh_json level, so return decoded objects like the
        # real gh_json does (it runs json.loads on the CLI output).
        if args and args[0] == "pr":
            return self.prs
        if args and args[0] == "api":
            endpoint = args[1]
            sha = endpoint.split("/commits/")[1].split("/")[0]
            if "/check-runs" in endpoint:
                runs = self.checks_by_sha.get(sha, [])
                return {"total_count": len(runs), "check_runs": runs}
            if endpoint.endswith("/status"):
                return self.status_by_sha.get(
                    sha, {"state": "success", "statuses": []})
        raise AssertionError(f"unexpected gh args in test: {args}")


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="pr-watch-test-")
        self.tmp = Path(self._tmp.name)
        self.state = self.tmp / "pr-state.json"

    def tearDown(self):
        self._tmp.cleanup()

    def run_tick(self, fake: FakeGitHub, *extra: str) -> "tuple[int, str, str]":
        """Run one tick with the fake GitHub; return (exit, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(pr_watch, "gh_json", side_effect=fake):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = pr_watch.run(["--state", str(self.state), *extra])
        return code, out.getvalue(), err.getvalue()

    def test_full_lifecycle(self):
        prs = [make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40),
               make_pr(44, "Add rate limiting", "feat/rate-limit", "c" * 40)]

        # Tick 1: no state file → silent baseline, state written.
        code, out, _ = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run(status="in_progress",
                                                                           conclusion=None)]}))
        self.assertEqual(code, 0)
        self.assertEqual(out, "", "the baseline tick is silent")
        saved = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertEqual(set(saved["prs"]), {"42", "44"})

        # Tick 2: nothing changed → still silent.
        code, out, _ = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run(status="in_progress",
                                                                           conclusion=None)]}))
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

        # Tick 3: PR 42 goes green → exactly one batched message about PR 42.
        code, out, _ = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()] * 12}))
        self.assertEqual(code, 0)
        self.assertIn("✅ #42 all checks green — ready to merge", out)
        self.assertIn("Fix the flaky test", out)
        self.assertIn("fix/flaky-test", out)
        self.assertIn(f"checks: {GREEN}", out)
        self.assertIn("https://github.com/httpurax/arena/pull/42", out)
        self.assertNotIn("#44", out, "an unchanged PR is not re-announced")
        saved = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertEqual(saved["prs"]["42"]["checks"], pr_watch.CHECKS_GREEN)

        # Tick 4: PR 42 still green, PR 44 fails → only PR 44 is announced.
        pr44_failed = [check_run(), check_run(conclusion="failure"), check_run(conclusion="success")]
        code, out, _ = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()] * 12,
                                                      "c" * 40: pr44_failed}))
        self.assertEqual(code, 0)
        self.assertIn("❌ #44 checks failing", out)
        self.assertIn("checks: 1 of 3 checks failed", out)
        self.assertNotIn("✅ #42", out)

        # Tick 5: PR 44 is merged (human's job) and PR 42 is still green → silent,
        # and PR 44 is pruned from the state.
        code, out, _ = self.run_tick(FakeGitHub([prs[0]], {"a" * 40: [check_run()] * 12}))
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        saved = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertEqual(set(saved["prs"]), {"42"})

        # Tick 6: a brand-new PR opens → announced as opened.
        code, out, _ = self.run_tick(FakeGitHub(
            [prs[0], make_pr(45, "Add rate limiting", "feat/rate-limit", "d" * 40)],
            {"a" * 40: [check_run()] * 12}))
        self.assertEqual(code, 0)
        self.assertIn("🆕 #45 opened", out)
        self.assertIn("https://github.com/httpurax/arena/pull/45", out)

    def test_no_notification_when_nothing_changed(self):
        """State exists, PRs and CI states are identical → empty stdout, and the
        stored per-PR state is untouched (only the timestamp moves)."""
        prs = [make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40)]
        self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()]}))
        before = json.loads(self.state.read_text(encoding="utf-8"))["prs"]
        code, out, _ = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()]}))
        self.assertEqual(code, 0)
        self.assertEqual(out, "", "nothing changed, nothing sent")
        after = json.loads(self.state.read_text(encoding="utf-8"))["prs"]
        self.assertEqual(before, after)

    def test_dry_run_changes_no_state(self):
        prs = [make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40)]
        # Baseline for real, with CI still running...
        self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run(status="in_progress",
                                                            conclusion=None)]}))
        saved_before = self.state.read_text(encoding="utf-8")
        # ...then a change that a dry run must not commit.
        code, out, err = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()] * 12}),
                                       "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(out, "", "dry-run keeps stdout empty; cron would deliver it")
        self.assertIn("[dry-run] ✅ #42 all checks green — ready to merge", err)
        self.assertEqual(self.state.read_text(encoding="utf-8"), saved_before,
                         "dry-run must not write the state file")

    def test_json_mode_is_read_only(self):
        prs = [make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40)]
        code, out, _ = self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()]}), "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["repo"], REPO)
        self.assertEqual(len(data["prs"]), 1)
        self.assertEqual(data["prs"][0]["number"], 42)
        self.assertEqual(data["prs"][0]["checks"], pr_watch.CHECKS_GREEN)
        self.assertFalse(self.state.exists(), "--json must not create or write the state file")

    def test_gh_failure_exits_nonzero_and_touches_no_state(self):
        prs = [make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40)]
        self.run_tick(FakeGitHub(prs, {"a" * 40: [check_run()]}))
        saved_before = self.state.read_text(encoding="utf-8")

        def broken(args: List[str], timeout: float) -> Any:
            raise pr_watch.GhError("gh pr list failed (exit 4): HTTP 401: Bad credentials")

        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(pr_watch, "gh_json", side_effect=broken):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = pr_watch.run(["--state", str(self.state)])
        self.assertEqual(code, 1, "a broken watch must exit non-zero (cron alerts on it)")
        self.assertIn("401", err.getvalue())
        self.assertEqual(self.state.read_text(encoding="utf-8"), saved_before)

    def test_legacy_combined_status_fallback(self):
        """A commit with no check runs falls back to the combined status; zero
        statuses is not green."""
        prs = [make_pr(42, "Fix the flaky test", "fix/flaky-test", "a" * 40),
               make_pr(43, "Update the README", "docs/readme", "b" * 40)]
        fake = FakeGitHub(prs, {},
                          status_by_sha={"a" * 40: {"state": "success", "statuses": [1, 2]},
                                         "b" * 40: {"state": "success", "statuses": []}})
        # Baseline: PR 42 green via legacy status, PR 43 running (nothing reported).
        code, out, _ = self.run_tick(fake)
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        saved = json.loads(self.state.read_text(encoding="utf-8"))
        self.assertEqual(saved["prs"]["42"]["checks"], pr_watch.CHECKS_GREEN)
        self.assertEqual(saved["prs"]["43"]["checks"], pr_watch.CHECKS_RUNNING)
        # Then PR 43's legacy status goes failing → announced.
        fake = FakeGitHub(prs, {},
                          status_by_sha={"a" * 40: {"state": "success", "statuses": [1, 2]},
                                         "b" * 40: {"state": "failure", "statuses": [1]}})
        code, out, _ = self.run_tick(fake)
        self.assertEqual(code, 0)
        self.assertIn("❌ #43 checks failing", out)


if __name__ == "__main__":
    unittest.main()
