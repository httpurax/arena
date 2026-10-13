#!/usr/bin/env python3
"""pr_watch.py — watchdog for the open pull requests of httpurax/arena.

Polls the repository's open PRs through the already-authenticated `gh` CLI,
compares each PR's CI state against the last-seen state in a local JSON file,
and prints ONE batched message describing only what changed. When nothing
changed, it prints nothing.

Delivery: Hermes cron's no-agent mode runs this script on a schedule and
delivers its stdout to Telegram verbatim (empty stdout = silent tick), using
the Hermes install's existing Telegram setup. This script never touches
Telegram credentials and never touches GitHub credentials — `gh` uses the
machine's existing authentication. It is read-only with respect to GitHub:
it never merges, closes, edits, or comments on anything.

Stdlib only, Python 3.8+. No third-party packages; the only network access is
through `gh`.

Usage:
    pr_watch.py [--repo OWNER/NAME] [--state PATH] [--timeout SECONDS]
                [--dry-run] [--json] [--verbose]

Exit status: 0 on success (a message, or silence); 1 on a fetch error (in
cron mode a non-zero exit delivers an error alert, so a broken watch cannot
fail silently); 2 on a usage error.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

DEFAULT_REPO = "httpurax/arena"
STATE_VERSION = 1
STATE_FILE_NAME = "pr-state.json"
PR_LIST_LIMIT = 100

CHECKS_GREEN = "green"
CHECKS_FAILING = "failing"
CHECKS_RUNNING = "running"

# Check-run conclusions. In flight: not completed yet, or completed but parked
# on a person (manual approval) — neither green nor failed. Terminal failures
# include cancelled and timed-out runs: a PR in either state is not ready to
# merge. Everything else completed (success, skipped, neutral) counts as
# passing.
IN_FLIGHT_CONCLUSIONS = frozenset({None, "action_required"})
FAILED_CONCLUSIONS = frozenset({"failure", "cancelled", "timed_out"})

CHECK_RUNS_PER_PAGE = 100
MAX_CHECK_RUN_PAGES = 50


class GhError(RuntimeError):
    """A `gh` invocation failed (or returned unusable output)."""


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def default_state_path() -> Path:
    """<parent of scripts/>/data/pr-state.json.

    In a repo checkout that is the skill's own gitignored data/ directory;
    when the script is copied to $HERMES_HOME/scripts/ for the cron job it
    becomes $HERMES_HOME/data/pr-state.json — private either way.
    """
    return Path(__file__).resolve().parent.parent / "data" / STATE_FILE_NAME


# ---------------------------------------------------------------------------
# GitHub, through the machine's `gh` CLI (no tokens handled here)
# ---------------------------------------------------------------------------

def gh(args: Sequence[str], timeout: float) -> str:
    """Run `gh <args>` and return its stdout; raise GhError on any failure."""
    short = " ".join(list(args)[:2])
    try:
        proc = subprocess.run(
            ["gh", *args], capture_output=True, text=True, timeout=timeout,
        )
    except FileNotFoundError:
        raise GhError(
            "`gh` not found on PATH — install the GitHub CLI and authenticate "
            "it with `gh auth login`"
        )
    except subprocess.TimeoutExpired:
        raise GhError(f"gh {short} timed out after {timeout:.0f}s")
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise GhError(f"gh {short} failed (exit {proc.returncode}): {detail[:400]}")
    return proc.stdout


def gh_json(args: Sequence[str], timeout: float) -> Any:
    out = gh(args, timeout)
    try:
        return json.loads(out)
    except json.JSONDecodeError as exc:
        raise GhError(f"gh {' '.join(list(args)[:2])} returned non-JSON output: {exc}")


def normalize_pr_item(item: Dict[str, Any], repo: str) -> Dict[str, Any]:
    """One `gh pr list --json` row (number/title/headRefName/headRefOid/url)
    as the internal snapshot: number, title, branch, sha, url."""
    number = int(item["number"])
    return {
        "number": number,
        "title": item.get("title") or "",
        "branch": item.get("headRefName") or "",
        "sha": item.get("headRefOid") or "",
        "url": item.get("url") or f"https://github.com/{repo}/pull/{number}",
    }


def fetch_open_prs(repo: str, timeout: float) -> List[Dict[str, Any]]:
    """The repo's open PRs: number, title, branch, head SHA, and link."""
    fields = "number,title,headRefName,headRefOid,url,createdAt"
    data = gh_json(
        ["pr", "list", "--repo", repo, "--state", "open",
         "--limit", str(PR_LIST_LIMIT), "--json", fields],
        timeout,
    )
    return [normalize_pr_item(item, repo) for item in data]


def fetch_check_runs(repo: str, sha: str, timeout: float) -> List[Dict[str, Any]]:
    """All check runs for a commit, following pagination."""
    runs: List[Dict[str, Any]] = []
    for page in range(1, MAX_CHECK_RUN_PAGES + 1):
        endpoint = (f"repos/{repo}/commits/{sha}/check-runs"
                    f"?per_page={CHECK_RUNS_PER_PAGE}&page={page}")
        data = gh_json(["api", endpoint], timeout)
        batch = data.get("check_runs") or []
        runs.extend(batch)
        if len(batch) < CHECK_RUNS_PER_PAGE:
            break
    return runs


def fetch_combined_status(repo: str, sha: str, timeout: float) -> Dict[str, Any]:
    """Legacy combined commit status (the pre-check-runs world)."""
    data = gh_json(["api", f"repos/{repo}/commits/{sha}/status"], timeout)
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# CI state: three buckets — green / failing / running
# ---------------------------------------------------------------------------

def summarize_check_runs(runs: Sequence[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    """`{"checks": ..., "detail": ...}` for check runs, or None for an empty
    list (nothing to summarize — the caller falls back to the combined
    commit status)."""
    if not runs:
        return None
    total = len(runs)
    passed = failed = pending = 0
    for run in runs:
        status = run.get("status")
        conclusion = run.get("conclusion")
        if status != "completed" or conclusion in IN_FLIGHT_CONCLUSIONS:
            pending += 1
        elif conclusion in FAILED_CONCLUSIONS:
            failed += 1
        else:
            passed += 1
    if pending:
        return {"checks": CHECKS_RUNNING, "detail": f"{pending} of {total} checks in progress"}
    if failed:
        return {"checks": CHECKS_FAILING, "detail": f"{failed} of {total} checks failed"}
    return {"checks": CHECKS_GREEN, "detail": f"all {total} checks passed"}


def summarize_combined_status(data: Dict[str, Any]) -> Dict[str, str]:
    """Same buckets from the legacy combined status. A commit with no
    statuses at all is NOT vacuously green — nothing has been checked."""
    n = len(data.get("statuses") or [])
    if n == 0:
        return {"checks": CHECKS_RUNNING, "detail": "no checks reported yet"}
    state = data.get("state")
    if state == "success":
        return {"checks": CHECKS_GREEN, "detail": f"all {n} status checks passed"}
    if state == "failure":
        return {"checks": CHECKS_FAILING, "detail": "status checks failing"}
    return {"checks": CHECKS_RUNNING, "detail": f"{n} status checks in progress"}


def check_state_for_pr(repo: str, pr: Dict[str, Any], timeout: float,
                       verbose: bool = False) -> Dict[str, Any]:
    """Fill in `checks` and `checks_detail` for one PR snapshot, in place."""
    runs = fetch_check_runs(repo, pr["sha"], timeout)
    summary = summarize_check_runs(runs)
    if summary is None:
        summary = summarize_combined_status(fetch_combined_status(repo, pr["sha"], timeout))
    pr["checks"] = summary["checks"]
    pr["checks_detail"] = summary["detail"]
    if verbose:
        print(f"pr-watch: #{pr['number']} {pr['title']} → {pr['checks']} ({pr['checks_detail']})",
              file=sys.stderr)
    return pr


# ---------------------------------------------------------------------------
# state file and change detection
# ---------------------------------------------------------------------------

def load_state(path: Path) -> Optional[Dict[str, Any]]:
    """The stored state, or None for a missing/unreadable/malformed file.
    A missing file is the normal first run; a broken one is treated the same
    (baseline fresh) rather than crashing the tick — at worst one transition
    is not announced."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"pr-watch: ignoring unreadable state file {path} ({exc}); baselining fresh",
              file=sys.stderr)
        return None
    if not isinstance(data, dict) or not isinstance(data.get("prs"), dict):
        print(f"pr-watch: ignoring malformed state file {path}; baselining fresh", file=sys.stderr)
        return None
    return data


def write_state(path: Path, state: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".pr-state-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


def build_state(prs: Sequence[Dict[str, Any]], repo: str) -> Dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "repo": repo,
        "updated_at": utc_now(),
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


def plan_events(prs: Sequence[Dict[str, Any]], state: Optional[Dict[str, Any]],
                repo: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Diff the current PR snapshots against the stored state.

    Returns (events, new_state). Rules:

    * missing stored state (first run, or the file was deleted) → baseline:
      every currently open PR is recorded, nothing is announced. The watch
      starts from a quiet state instead of replaying history.
    * a PR number not in the stored state → "opened" event.
    * a stored PR whose CI state changed into green or failing → that event.
      A change into running announces nothing (CI merely started), and the
      state is still stored, so failing → running → failing announces the
      second failing exactly once.
    * a PR no longer open (merged, closed, deleted) → silently dropped from
      the state. This skill notifies only; a human does the merging.
    """
    new_state = build_state(prs, repo)
    if state is None:
        return [], new_state
    stored = state["prs"]
    events: List[Dict[str, Any]] = []
    for pr in prs:
        prev = stored.get(str(pr["number"]))
        if prev is None:
            events.append({**pr, "opened": True})
        elif pr["checks"] in (CHECKS_GREEN, CHECKS_FAILING) and pr["checks"] != prev.get("checks"):
            events.append({**pr, "opened": False})
    return events, new_state


# ---------------------------------------------------------------------------
# the message: one batched Telegram text, or nothing
# ---------------------------------------------------------------------------

def event_header(ev: Dict[str, Any]) -> str:
    n = ev["number"]
    if ev.get("opened"):
        if ev["checks"] == CHECKS_GREEN:
            return f"🆕 #{n} opened — all checks green"
        if ev["checks"] == CHECKS_FAILING:
            return f"🆕 #{n} opened — checks failing"
        return f"🆕 #{n} opened"
    if ev["checks"] == CHECKS_GREEN:
        return f"✅ #{n} all checks green — ready to merge"
    return f"❌ #{n} checks failing"


def format_message(repo: str, events: Sequence[Dict[str, Any]]) -> str:
    """The batched message for this tick; the empty string when nothing
    changed (in cron mode, empty stdout is a silent tick)."""
    if not events:
        return ""
    n = len(events)
    lines = [f"{repo}: {n} PR update" + ("" if n == 1 else "s"), ""]
    for ev in sorted(events, key=lambda e: e["number"]):
        lines.append(event_header(ev))
        lines.append(f"   {ev['title']}")
        lines.append(f"   {ev['branch']}")
        lines.append(f"   checks: {ev['checks_detail']}")
        lines.append(f"   {ev['url']}")
        lines.append("")
    return "\n".join(lines).rstrip("\n")


# ---------------------------------------------------------------------------
# one tick
# ---------------------------------------------------------------------------

def run(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pr_watch.py",
        description="Watch the open PRs of a GitHub repo and print a batched "
                    "message for whatever changed (Hermes cron no-agent mode "
                    "delivers stdout to Telegram). Read-only: never merges or "
                    "modifies anything.",
    )
    parser.add_argument("--repo", default=DEFAULT_REPO,
                        help=f"owner/name to watch (default: {DEFAULT_REPO})")
    parser.add_argument("--state", default=None,
                        help="state file path (default: <skill>/data/pr-state.json, "
                             "gitignored; private, holds public PR metadata only)")
    parser.add_argument("--timeout", type=float, default=60.0,
                        help="per-gh-call timeout in seconds (default: 60)")
    parser.add_argument("--dry-run", action="store_true",
                        help="do not write the state file; the would-be message is "
                             "printed to stderr, stdout stays empty")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="print the fetched snapshot as JSON and write no "
                             "state (read-only diagnostic)")
    parser.add_argument("--verbose", action="store_true",
                        help="log each fetched PR and its CI state to stderr")
    args = parser.parse_args(argv)

    state_path = Path(os.path.expanduser(args.state)) if args.state else default_state_path()

    try:
        prs = fetch_open_prs(args.repo, args.timeout)
        for pr in prs:
            check_state_for_pr(args.repo, pr, args.timeout, verbose=args.verbose)
    except GhError as exc:
        print(f"pr-watch: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps({
            "repo": args.repo,
            "generated_at": utc_now(),
            "state_file": str(state_path),
            "prs": prs,
        }, indent=2, ensure_ascii=False))
        return 0

    state = load_state(state_path)
    if state is None and args.verbose:
        print("pr-watch: no state file — baselining silently (no message)", file=sys.stderr)
    events, new_state = plan_events(prs, state, args.repo)
    message = format_message(args.repo, events)

    if args.dry_run:
        if message:
            for line in message.splitlines():
                print(f"[dry-run] {line}", file=sys.stderr)
        else:
            print("[dry-run] no changes; nothing would be sent", file=sys.stderr)
        return 0

    if message:
        print(message)
    write_state(state_path, new_state)
    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
