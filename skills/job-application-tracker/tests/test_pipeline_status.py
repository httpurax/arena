#!/usr/bin/env python3
"""Offline tests for the job-application-tracker skill.

Stdlib-only and network-free: the skill's script reads one local JSON file, so every case
here is a temp file, a fixed reference date, or a pure function call.

Covered:

  * the frontmatter identity (``name`` matches the directory) and the documented schema;
  * the shipped example file: it exists, validates against the schema, and is fictional;
  * ``scripts/pipeline_status.py``: a missing, empty, malformed, or schema-breaking data
    file is reported as one clear message, never a traceback;
  * overdue / due-soon detection against fixed dates, including both window edges and the
    closed statuses that are never nudged;
  * the privacy guard: credential-shaped free text is warned about without its value being
    echoed, and ``data/`` is ignored so real pipeline data cannot be committed.
"""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import re
import tempfile
import unittest
from datetime import date
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = SKILL_ROOT.name
SKILL_MD = SKILL_ROOT / "SKILL.md"
DATA_FORMAT_MD = SKILL_ROOT / "references" / "data-format.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "applications.example.json"
GITIGNORE = SKILL_ROOT / ".gitignore"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "pipeline_status.py"

_spec = importlib.util.spec_from_file_location("pipeline_status", SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
pipeline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pipeline)

TODAY = date(2026, 10, 12)  # every deadline test is written against this fixed date

# A credential-shaped string used only as a canary: the report must warn about it and must
# never print it. Nothing here is a real value.
CANARY_SECRET = "correct-horse-battery"


def make_application(**changes: Any) -> "dict[str, Any]":
    """A valid record; tests override only the field each case is about."""
    record: "dict[str, Any]" = {
        "id": "nimbus-support-agent",
        "company": "Nimbus Cloudworks",
        "role": "Customer Support Agent (Remote)",
        "pay": "$22/hr",
        "source": "job board",
        "date_applied": "2026-10-05",
        "status": "interview",
        "next_step": "Confirm the video interview slot",
        "next_step_deadline": "2026-10-14",
        "notes": "Recruiter: Dana. Panel is 30 minutes.",
    }
    record.update(changes)
    return record


def document(applications: "list[dict[str, Any]]") -> "dict[str, Any]":
    return {"applications": applications}


class TempFileTestCase(unittest.TestCase):
    """Base class giving each test its own throwaway data directory."""

    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary_directory.cleanup)
        self.workspace = Path(self._temporary_directory.name)

    def write_data(self, payload: Any, name: str = "applications.json") -> Path:
        """Write payload (raw text or an object) into the workspace and return the path."""
        path = self.workspace / name
        text = payload if isinstance(payload, str) else json.dumps(payload, indent=2)
        path.write_text(text, encoding="utf-8")
        return path

    def run_command(self, argv: "list[str]") -> "tuple[int, str, str]":
        """Run the script in-process; return (exit code, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = pipeline.main(argv, out=out, err=err)
        return code, out.getvalue(), err.getvalue()


# --------------------------------------------------------------------------------------
# frontmatter and documentation
# --------------------------------------------------------------------------------------

class FrontmatterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = SKILL_MD.read_text(encoding="utf-8")
        block = self.skill_text.split("---", 2)[1]
        self.frontmatter = {}
        for line in block.splitlines():
            if line.strip() and not line.startswith((" ", "\t")) and ":" in line:
                key, _, value = line.partition(":")
                self.frontmatter[key.strip()] = value.strip()

    def test_skill_md_exists(self) -> None:
        self.assertTrue(SKILL_MD.is_file(), f"missing {SKILL_MD}")

    def test_frontmatter_name_matches_the_directory(self) -> None:
        self.assertEqual("job-application-tracker", SKILL_NAME)
        self.assertEqual(SKILL_NAME, self.frontmatter["name"])

    def test_frontmatter_declares_the_documented_identity(self) -> None:
        self.assertEqual("Track job applications, next steps, and deadlines.",
                         self.frontmatter["description"])
        self.assertEqual("1.0.0", self.frontmatter["version"])
        self.assertEqual("MIT", self.frontmatter["license"])
        self.assertEqual("[linux, macos, windows]", self.frontmatter["platforms"])
        self.assertIn("category: productivity", self.skill_text)
        self.assertLess(len(self.frontmatter["description"]), 60)

    def test_behaviors_are_documented(self) -> None:
        for heading in (
            "### 1. Add or update an application",
            "### 2. Pipeline view — group by status",
            "### 3. Nudges for overdue and due-soon next steps",
            "### 4. Weekly review",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.skill_text)
        self.assertIn("Never invent data", self.skill_text)
        self.assertIn("needs attention", self.skill_text)

    def test_commands_are_shown_for_bash_and_powershell(self) -> None:
        self.assertIn("```bash", self.skill_text)
        self.assertIn("```powershell", self.skill_text)
        self.assertIn("python3 scripts/pipeline_status.py", self.skill_text)
        self.assertIn("python scripts/pipeline_status.py", self.skill_text)

    def test_data_format_reference_exists_and_is_linked(self) -> None:
        self.assertTrue(DATA_FORMAT_MD.is_file(), f"missing {DATA_FORMAT_MD}")
        self.assertIn("[`references/data-format.md`](references/data-format.md)", self.skill_text)
        reference = DATA_FORMAT_MD.read_text(encoding="utf-8")
        for status in pipeline.STATUS_ORDER:
            with self.subTest(status=status):
                self.assertIn(f"`{status}`", reference)


# --------------------------------------------------------------------------------------
# the shipped example file
# --------------------------------------------------------------------------------------

class ExampleDataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        self.applications = self.document["applications"]

    def test_example_exists_and_parses(self) -> None:
        self.assertTrue(EXAMPLE_DATA.is_file(), f"missing {EXAMPLE_DATA}")
        self.assertIsInstance(self.document, dict)
        self.assertIn("applications", self.document)

    def test_example_validates_against_the_documented_schema(self) -> None:
        self.assertEqual([], pipeline.applications_errors(self.applications))

    def test_example_is_loadable_by_the_script(self) -> None:
        self.assertEqual(self.applications, pipeline.load_applications(EXAMPLE_DATA))

    def test_example_covers_the_record_shape_without_being_real_data(self) -> None:
        self.assertGreaterEqual(len(self.applications), 3)
        ids = [application["id"] for application in self.applications]
        self.assertEqual(len(ids), len(set(ids)), "example ids must be unique")
        self.assertTrue(all(application["company"].endswith(("Cloudworks", "Data Co", "Logistics",
                                                              "Software", "Localization"))
                            for application in self.applications),
                        "the example must stay visibly fictional")

    def test_example_never_carries_a_credential_shaped_value(self) -> None:
        for application in self.applications:
            for field in ("notes", "next_step"):
                value = application.get(field, "")
                with self.subTest(application=application["id"], field=field):
                    self.assertIsNone(pipeline.CREDENTIAL_HINT_RE.search(value))


# --------------------------------------------------------------------------------------
# privacy guard
# --------------------------------------------------------------------------------------

class PrivacyTests(unittest.TestCase):
    def test_gitignore_excludes_the_private_data_directory(self) -> None:
        self.assertTrue(GITIGNORE.is_file(), f"missing {GITIGNORE}")
        lines = [line.strip() for line in GITIGNORE.read_text(encoding="utf-8").splitlines()]
        self.assertIn("data/", lines)

    def test_skill_documents_the_privacy_rules(self) -> None:
        text = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("data/applications.json", text)
        self.assertIn("never committed", text)
        self.assertIn("fictional", text)
        self.assertIn("## Setup — first run only", text)
        self.assertIn("cp examples/applications.example.json data/applications.json", text)
        self.assertIn("Copy-Item examples/applications.example.json data/applications.json", text)

    def test_credential_shaped_text_is_warned_about_without_echoing_the_value(self) -> None:
        application = make_application(notes=f"portal password = {CANARY_SECRET}")
        hints = pipeline.credential_hints(application)
        self.assertEqual(1, len(hints))
        self.assertIn("notes", hints[0])
        self.assertNotIn(CANARY_SECRET, "\n".join(hints))

        report = "\n".join(pipeline.build_report([application], TODAY, "fixture.json"))
        self.assertIn("privacy warnings (1)", report)
        self.assertNotIn(CANARY_SECRET, report)

    def test_clean_free_text_raises_no_warning(self) -> None:
        self.assertEqual([], pipeline.credential_hints(make_application()))
        report = "\n".join(pipeline.build_report([make_application()], TODAY, "fixture.json"))
        self.assertIn("privacy warnings (0)", report)

    def test_no_shipped_text_file_holds_an_embedded_credential(self) -> None:
        # A deliberately small mirror of the repository linter's rules, so this suite still
        # stands on its own when the skill is installed on its own.
        patterns = (
            re.compile(r"(?i)\b(?:api[_-]?key|passwd|password|pwd|client[_-]?secret|"
                       r"secret[_-]?key|access[_-]?token|auth[_-]?token|bearer[_-]?token)\b"
                       r"\s*[:=]\s*['\"][^'\"]+['\"]"),
            re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
            re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
            re.compile(r"\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s:@]+@"),
        )
        scanned = 0
        for path in sorted(SKILL_ROOT.rglob("*")):
            if not path.is_file() or "data" in path.relative_to(SKILL_ROOT).parts:
                continue
            if path.suffix in {".pyc", ".png", ".jpg"}:
                continue
            scanned += 1
            text = path.read_text(encoding="utf-8", errors="replace")
            for rule in patterns:
                self.assertIsNone(rule.search(text), f"{path.name} carries a credential literal")
        self.assertGreater(scanned, 0)


# --------------------------------------------------------------------------------------
# loading: the failure paths must be messages, not tracebacks
# --------------------------------------------------------------------------------------

class LoadFailureTests(TempFileTestCase):
    def test_missing_file_is_reported_with_the_example_to_copy(self) -> None:
        missing = self.workspace / "nope.json"
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(missing)
        message = str(caught.exception)
        self.assertIn("data file not found", message)
        self.assertIn("applications.example.json", message)

        code, out, err = self.run_command(["--data", str(missing)])
        self.assertEqual(1, code)
        self.assertEqual("", out)
        self.assertIn("ERROR", err)
        self.assertIn("data file not found", err)
        self.assertNotIn("Traceback", err)

    def test_empty_file_is_reported_as_empty_not_as_a_crash(self) -> None:
        empty = self.write_data("")
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(empty)
        self.assertIn("data file is empty", str(caught.exception))

        code, out, err = self.run_command(["--data", str(empty)])
        self.assertEqual(1, code)
        self.assertIn("data file is empty", err)
        self.assertNotIn("Traceback", err)

    def test_whitespace_only_file_is_treated_as_empty(self) -> None:
        blank = self.write_data("\n   \n\t\n")
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(blank)
        self.assertIn("data file is empty", str(caught.exception))

    def test_malformed_json_names_the_line_and_column(self) -> None:
        broken = self.write_data('{"applications": [{"id": "x", }')
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(broken)
        message = str(caught.exception)
        self.assertIn("malformed JSON", message)
        self.assertIn("line 1", message)

        code, out, err = self.run_command(["--data", str(broken)])
        self.assertEqual(1, code)
        self.assertEqual("", out)
        self.assertIn("malformed JSON", err)
        self.assertNotIn("Traceback", err)

    def test_directory_instead_of_a_file_is_reported(self) -> None:
        directory = self.workspace / "data.json"
        directory.mkdir()
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(directory)
        self.assertIn("is a directory", str(caught.exception))

    def test_top_level_must_be_an_object_with_an_applications_list(self) -> None:
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(self.write_data([{"id": "x"}]))
        self.assertIn("'applications' list", str(caught.exception))

        without_key = self.write_data({"pipelines": []})
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(without_key)
        self.assertIn("no 'applications' key", str(caught.exception))

        not_a_list = self.write_data({"applications": {"id": "x"}})
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(not_a_list)
        self.assertIn("applications must be a list", str(caught.exception))

    def test_every_schema_problem_is_listed_with_its_position(self) -> None:
        broken = self.write_data(document([
            make_application(),
            make_application(id="Not A Slug", status="super-interview", notes=42),
        ]))
        with self.assertRaises(pipeline.DataError) as caught:
            pipeline.load_applications(broken)
        message = str(caught.exception)
        self.assertIn("3 schema problems", message)
        self.assertIn("applications[1].id", message)
        self.assertIn("applications[1].status", message)
        self.assertIn("applications[1].notes", message)

    def test_an_empty_pipeline_file_is_valid_and_reports_nothing_to_do(self) -> None:
        path = self.write_data(document([]))
        self.assertEqual([], pipeline.load_applications(path))
        code, out, err = self.run_command(["--data", str(path), "--today", "2026-10-12"])
        self.assertEqual(0, code)
        self.assertEqual("", err)
        self.assertIn("no applications tracked yet", out)
        self.assertIn("needs attention (0)", out)


# --------------------------------------------------------------------------------------
# schema rules
# --------------------------------------------------------------------------------------

class SchemaTests(unittest.TestCase):
    def test_a_documented_record_is_valid(self) -> None:
        self.assertEqual([], pipeline.application_errors(make_application()))

    def test_optional_fields_may_be_missing_or_null(self) -> None:
        minimal = {
            "id": "acme-support",
            "company": "Acme",
            "role": "Support",
            "status": "researching",
            "date_applied": None,
            "next_step_deadline": None,
        }
        self.assertEqual([], pipeline.application_errors(minimal))

    def test_unknown_status_values_are_rejected(self) -> None:
        for status in ("super-interview", "APPLIED", "", "pending", "on hold"):
            with self.subTest(status=status):
                problems = pipeline.application_errors(make_application(status=status))
                self.assertTrue(
                    any(".status" in problem for problem in problems),
                    f"{status!r} must be rejected; got {problems}",
                )
                self.assertTrue(any("not a known status" in p for p in problems))

    def test_every_documented_status_is_accepted(self) -> None:
        for status in pipeline.STATUS_ORDER:
            with self.subTest(status=status):
                self.assertEqual([], pipeline.application_errors(make_application(status=status)))

    def test_required_text_fields_must_be_present_and_non_empty(self) -> None:
        for field in ("id", "company", "role"):
            with self.subTest(field=field):
                record = make_application()
                record[field] = "   "
                problems = pipeline.application_errors(record)
                self.assertIn(f"applications[0].{field} must be non-empty text", problems)

                record.pop(field)
                problems = pipeline.application_errors(record)
                self.assertIn(
                    f"applications[0] is missing the required field '{field}'", problems
                )

    def test_id_must_be_a_slug(self) -> None:
        problems = pipeline.application_errors(make_application(id="Nimbus Support Agent"))
        self.assertTrue(any("is not a short slug" in problem for problem in problems))

    def test_dates_must_be_iso_calendar_dates_or_null(self) -> None:
        for bad in ("12/10/2026", "2026-13-01", "2026-02-30", "20261012", 20261012):
            with self.subTest(value=bad):
                problems = pipeline.application_errors(make_application(date_applied=bad))
                self.assertTrue(any(".date_applied" in problem for problem in problems), problems)

    def test_a_deadline_requires_a_next_step(self) -> None:
        problems = pipeline.application_errors(
            make_application(next_step="", next_step_deadline="2026-10-14")
        )
        self.assertTrue(any("next_step is empty" in problem for problem in problems))

    def test_unknown_fields_are_rejected_rather_than_silently_dropped(self) -> None:
        problems = pipeline.application_errors(make_application(next_step_deadlin="2026-10-14"))
        self.assertTrue(any("unknown field" in problem for problem in problems), problems)

    def test_duplicate_ids_are_rejected(self) -> None:
        problems = pipeline.applications_errors([make_application(), make_application()])
        self.assertTrue(any("duplicates" in problem for problem in problems), problems)

    def test_non_object_records_are_rejected(self) -> None:
        self.assertEqual(
            ["applications[0] must be an object, got str"],
            pipeline.application_errors("nope"),
        )


# --------------------------------------------------------------------------------------
# deadlines: overdue, due soon, and what is never nudged
# --------------------------------------------------------------------------------------

class DeadlineTests(unittest.TestCase):
    def test_overdue_and_due_soon_are_detected(self) -> None:
        cases = {
            "2026-10-05": (True, "overdue by 7 days"),
            "2026-10-11": (True, "overdue by 1 day"),
            "2026-10-12": (True, "due today"),
            "2026-10-13": (True, "due in 1 day"),
            "2026-10-15": (True, "due in 3 days"),
            "2026-10-16": (False, "due in 4 days"),
            "2026-11-30": (False, "due in 49 days"),
        }
        for deadline, (expected, phrase) in cases.items():
            with self.subTest(deadline=deadline):
                application = make_application(next_step_deadline=deadline)
                self.assertIs(expected, pipeline.needs_attention(application, TODAY))
                self.assertEqual(phrase, pipeline.deadline_phrase(date.fromisoformat(deadline), TODAY))

    def test_open_statuses_are_nudged_and_closed_ones_are_not(self) -> None:
        overdue = make_application(next_step_deadline="2026-10-01")
        for status in pipeline.STATUS_ORDER:
            with self.subTest(status=status):
                application = make_application(status=status, next_step_deadline="2026-10-01")
                expected = status not in pipeline.CLOSED_STATUSES
                self.assertIs(expected, pipeline.needs_attention(application, TODAY))
        for status in ("offer", "rejected", "withdrawn"):
            with self.subTest(status=status):
                closed = make_application(status=status, next_step_deadline="2026-10-01")
                self.assertFalse(pipeline.needs_attention(closed, TODAY))
        self.assertEqual({"offer", "rejected", "withdrawn"}, set(pipeline.CLOSED_STATUSES))
        self.assertIs(True, pipeline.needs_attention(overdue, TODAY))

    def test_a_record_without_a_deadline_is_never_flagged(self) -> None:
        for deadline in (None, ""):
            with self.subTest(deadline=deadline):
                application = make_application(next_step_deadline=deadline)
                self.assertFalse(pipeline.needs_attention(application, TODAY))
                self.assertFalse(pipeline.needs_attention(application, TODAY, due_soon_days=3650))

    def test_the_window_is_configurable(self) -> None:
        application = make_application(next_step_deadline="2026-10-13")
        self.assertFalse(pipeline.needs_attention(application, TODAY, due_soon_days=0))
        self.assertTrue(pipeline.needs_attention(application, TODAY, due_soon_days=1))
        self.assertTrue(pipeline.needs_attention(make_application(next_step_deadline="2026-10-12"),
                                                 TODAY, due_soon_days=0))

    def test_deadline_phrase_pluralises_days(self) -> None:
        self.assertEqual("overdue by 2 days", pipeline.deadline_phrase(date(2026, 10, 10), TODAY))
        self.assertEqual("due in 2 days", pipeline.deadline_phrase(date(2026, 10, 14), TODAY))


# --------------------------------------------------------------------------------------
# the report
# --------------------------------------------------------------------------------------

class ReportTests(TempFileTestCase):
    def build(self, applications: "list[dict[str, Any]]", **kwargs: Any) -> str:
        return "\n".join(pipeline.build_report(applications, TODAY, "fixture.json", **kwargs))

    def test_pipeline_view_groups_by_status_in_pipeline_order(self) -> None:
        applications = [
            make_application(id="b-watching", status="watching", next_step="", next_step_deadline=None),
            make_application(id="c-interview", status="interview"),
            make_application(id="a-assessment", status="assessment", next_step_deadline=None),
        ]
        report = self.build(applications)
        self.assertIn("3 applications tracked: 1 assessment, 1 interview, 1 watching", report)
        positions = [report.index(f"{status} (1)") for status in ("assessment", "interview", "watching")]
        self.assertEqual(sorted(positions), positions, "groups must follow pipeline order")
        self.assertLess(report.index("assessment (1)"), report.index("interview (1)"))

    def test_empty_groups_are_omitted(self) -> None:
        report = self.build([make_application(status="offer")])
        self.assertIn("offer (1)", report)
        self.assertNotIn("applied (0)", report)

    def test_needs_attention_lists_overdue_before_due_soon(self) -> None:
        applications = [
            make_application(id="due-soon", next_step_deadline="2026-10-14"),
            make_application(id="overdue", next_step_deadline="2026-10-09"),
        ]
        report = self.build(applications)
        self.assertIn("needs attention (2)", report)
        self.assertIn("[overdue] overdue:", report)
        self.assertIn("[due soon] due-soon:", report)
        self.assertLess(report.index("[overdue]"), report.index("[due soon]"))
        self.assertIn("overdue by 3 days", report)
        self.assertIn("due in 2 days", report)

    def test_a_closed_application_is_not_nudged_even_with_an_overdue_deadline(self) -> None:
        applications = [
            make_application(id="still-open", status="applied", next_step_deadline="2026-10-09"),
            make_application(id="closed-rejected", status="rejected", next_step_deadline="2026-10-01"),
            make_application(id="closed-withdrawn", status="withdrawn", next_step_deadline="2026-10-01"),
        ]
        report = self.build(applications)
        attention = report[report.index("needs attention ("):]
        self.assertIn("needs attention (1)", report)
        self.assertIn("still-open", attention)
        self.assertNotIn("closed-rejected", attention)
        self.assertNotIn("closed-withdrawn", attention)

    def test_a_calm_pipeline_says_so(self) -> None:
        report = self.build([make_application(next_step_deadline="2026-12-01")])
        self.assertIn("needs attention (0)", report)
        self.assertIn("nothing overdue or due within 3 days", report)

    def test_the_report_is_offline_and_ascii(self) -> None:
        report = self.build([make_application()])
        report.encode("ascii")  # never depends on the console's encoding

    def test_command_prints_the_report_and_exits_zero(self) -> None:
        path = self.write_data(document([make_application()]))
        code, out, err = self.run_command(
            ["--data", str(path), "--today", "2026-10-12"]
        )
        self.assertEqual(0, code)
        self.assertEqual("", err)
        self.assertIn(str(path), out)
        self.assertIn("today: 2026-10-12", out)
        self.assertIn("nimbus-support-agent", out)
        self.assertIn("needs attention (1)", out)

    def test_the_default_data_path_is_the_private_file_under_the_skill(self) -> None:
        self.assertEqual(SKILL_ROOT / "data" / "applications.json", pipeline.DEFAULT_DATA_PATH)
        self.assertEqual(
            SKILL_ROOT / "examples" / "applications.example.json", pipeline.EXAMPLE_PATH
        )

    def test_bad_options_are_usage_errors(self) -> None:
        path = self.write_data(document([]))
        for argv in (
            ["--data", str(path), "--today", "12/10/2026"],
            ["--data", str(path), "--due-soon-days", "-1"],
            ["--data", str(path), "--due-soon-days", "soon"],
        ):
            with self.subTest(argv=argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    pipeline.main(argv)
                self.assertEqual(2, caught.exception.code)


if __name__ == "__main__":
    unittest.main()
