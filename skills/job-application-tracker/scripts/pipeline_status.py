#!/usr/bin/env python3
"""pipeline_status.py - offline pipeline summary for the job-application-tracker skill.

Reads one local JSON file (``<skill>/data/applications.json`` by default) and prints:

  * a pipeline view: every application grouped by status, in pipeline order;
  * a "needs attention" section: every open application whose next step is overdue or
    due within the due-soon window (3 days by default);
  * a "privacy warnings" section: any free-text field that looks like a pasted
    credential, because the data file is local but the note is the wrong place for it.

The script is stdlib-only, makes no network requests, and writes nothing. It never
raises a traceback at the user: a missing file, an empty file, malformed JSON, or a
record that breaks the documented schema is reported as one clear message, and the
exit status is 1.

Usage:
    python3 scripts/pipeline_status.py [--data PATH] [--today YYYY-MM-DD] [--due-soon-days N]

The data file is ``{"applications": [ ... ]}``; see examples/applications.example.json
for the shape and SKILL.md for the field-by-field schema. ``--today`` makes the report
reproducible (tests use it); without it the system date is used.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Optional, Sequence

# --------------------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------------------

# Pipeline order: the statuses read top to bottom the way a hunt progresses. "watching"
# is a deliberate state, not a rejection: the user is tracking an opening without an
# application in play yet, so it sorts last but is still open.
STATUS_ORDER: "tuple[str, ...]" = (
    "researching",
    "applied",
    "assessment",
    "interview",
    "offer",
    "rejected",
    "withdrawn",
    "watching",
)

# A status that closes an application: no next step is expected, so these are never
# surfaced as needing attention even when a stale deadline is left in the record.
CLOSED_STATUSES = frozenset({"offer", "rejected", "withdrawn"})

DUE_SOON_DAYS = 3

REQUIRED_TEXT_FIELDS = ("id", "company", "role")
OPTIONAL_TEXT_FIELDS = ("pay", "source", "next_step", "notes")
DATE_FIELDS = ("date_applied", "next_step_deadline")
# The order the schema is documented in, so a rejection can be read against references/data-format.md.
KNOWN_FIELDS = ("id", "company", "role", "status") + OPTIONAL_TEXT_FIELDS + DATE_FIELDS

ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Free text is scanned for something that looks like a credential being pasted in. The
# data file is a local, private file, but it is edited in the same editor as the repo and
# a password or an API token in it is exactly the mistake this rule exists to catch.
CREDENTIAL_HINT_RE = re.compile(
    r"(?i)\b(?:password|passwd|passphrase|pwd|api[ _-]?key|secret|token|"
    r"one[ _-]?time[ _-]?code|otp|security[ _-]?answer)\b\s*[:=]\s*\S"
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = SKILL_ROOT / "data" / "applications.json"
EXAMPLE_PATH = SKILL_ROOT / "examples" / "applications.example.json"


class DataError(Exception):
    """A problem with the data file that the user has to fix. Never a traceback."""


# --------------------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------------------

def _is_iso_date(value: Any) -> bool:
    """True when value is a string in the exact YYYY-MM-DD form the schema documents.

    The regex runs first on purpose: ``date.fromisoformat`` accepts more than this format
    on recent Pythons (basic format, ISO week dates), and the data file is meant to hold
    one unambiguous spelling.
    """
    if not isinstance(value, str) or not DATE_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def application_errors(application: Any, index: int = 0) -> "list[str]":
    """Return one message per schema violation in a single application record.

    Messages are prefixed with ``applications[<index>]`` so a file with several bad
    records can be fixed from one report. An empty list means the record is valid.
    """
    where = f"applications[{index}]"
    problems: "list[str]" = []

    if not isinstance(application, dict):
        return [f"{where} must be an object, got {type(application).__name__}"]

    for field in REQUIRED_TEXT_FIELDS:
        if field not in application:
            problems.append(f"{where} is missing the required field '{field}'")
        elif not isinstance(application[field], str) or not application[field].strip():
            problems.append(f"{where}.{field} must be non-empty text")

    identifier = application.get("id")
    if isinstance(identifier, str) and identifier.strip() and not ID_RE.match(identifier):
        problems.append(
            f"{where}.id {identifier!r} is not a short slug "
            "(lowercase letters, digits and single hyphens, e.g. 'nimbus-support-agent')"
        )

    status = application.get("status")
    if "status" not in application:
        problems.append(f"{where} is missing the required field 'status'")
    elif not isinstance(status, str) or status not in STATUS_ORDER:
        problems.append(
            f"{where}.status {status!r} is not a known status "
            f"(expected one of: {', '.join(STATUS_ORDER)})"
        )

    for field in OPTIONAL_TEXT_FIELDS:
        value = application.get(field)
        if value is not None and not isinstance(value, str):
            problems.append(f"{where}.{field} must be text")

    for field in DATE_FIELDS:
        value = application.get(field)
        if value is not None and not _is_iso_date(value):
            problems.append(f"{where}.{field} must be a YYYY-MM-DD date or null, got {value!r}")

    next_step = application.get("next_step")
    if application.get("next_step_deadline") is not None:
        if not isinstance(next_step, str) or not next_step.strip():
            problems.append(
                f"{where}.next_step_deadline is set but {where}.next_step is empty; "
                "a deadline needs a step to belong to"
            )

    for field in application:
        if field not in KNOWN_FIELDS:
            problems.append(
                f"{where} has unknown field {field!r} "
                f"(known fields: {', '.join(KNOWN_FIELDS)})"
            )

    return problems


def applications_errors(applications: Any) -> "list[str]":
    """Return every schema violation in the ``applications`` list, duplicates included."""
    if not isinstance(applications, list):
        return [f"applications must be a list, got {type(applications).__name__}"]

    problems: "list[str]" = []
    seen: "dict[str, int]" = {}
    for index, application in enumerate(applications):
        problems.extend(application_errors(application, index))
        identifier = application.get("id") if isinstance(application, dict) else None
        if isinstance(identifier, str) and identifier.strip():
            if identifier in seen:
                problems.append(
                    f"applications[{index}].id {identifier!r} duplicates "
                    f"applications[{seen[identifier]}]; ids must be unique"
                )
            else:
                seen[identifier] = index
    return problems


def credential_hints(application: "dict[str, Any]") -> "list[str]":
    """Warn when free text in a record looks like a pasted credential.

    Only ``notes`` and ``next_step`` are scanned: they are the free-text fields a user
    actually types into. Company, role, pay and source are short metadata fields, and a
    value there cannot plausibly be a secret.
    """
    hints: "list[str]" = []
    for field in ("next_step", "notes"):
        value = application.get(field)
        if isinstance(value, str) and CREDENTIAL_HINT_RE.search(value):
            hints.append(
                f"{application.get('id', '<no id>')}: {field} looks like it contains a "
                "credential; notes must never hold passwords, tokens or codes"
            )
    return hints


# --------------------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------------------

def load_applications(path: Path) -> "list[dict[str, Any]]":
    """Read and validate the data file, raising DataError with a fixable message.

    Covers the four cases the skill promises to survive: the file is missing, the file is
    empty, the JSON is malformed, and the content does not match the documented schema.
    """
    if not path.exists():
        raise DataError(
            f"data file not found: {path}\n"
            f"       create it from the shipped example, then edit it:\n"
            f"         {EXAMPLE_PATH}"
        )
    if path.is_dir():
        raise DataError(f"{path} is a directory, not the JSON data file")

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise DataError(
            f"{path} is not valid UTF-8 text ({exc.reason} at byte {exc.start}); "
            "the data file must be plain UTF-8 JSON"
        ) from None
    except OSError as exc:
        raise DataError(f"could not read {path}: {exc}") from None

    if not text.strip():
        raise DataError(
            f"data file is empty: {path}\n"
            "       an empty file is not valid JSON. Restore it from the shipped example:\n"
            f"         {EXAMPLE_PATH}\n"
            '       or write {"applications": []} by hand'
        )

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DataError(
            f"malformed JSON in {path}: line {exc.lineno} column {exc.colno}: {exc.msg}\n"
            "       fix the syntax error and run the command again; nothing was changed"
        ) from None

    if not isinstance(document, dict):
        raise DataError(
            f"{path} must hold an object with an 'applications' list, "
            f"got {type(document).__name__} at the top level"
        )
    if "applications" not in document:
        raise DataError(
            f"{path} has no 'applications' key; the file must look like "
            '{"applications": [ ... ]}'
        )

    applications = document["applications"]
    problems = applications_errors(applications)
    if problems:
        count = len(problems)
        noun = "problem" if count == 1 else "problems"
        listing = "\n".join(f"         - {problem}" for problem in problems)
        raise DataError(f"{path} has {count} schema {noun}:\n{listing}")

    return applications  # type: ignore[return-value]


# --------------------------------------------------------------------------------------
# report
# --------------------------------------------------------------------------------------

def deadline_phrase(deadline: date, today: date) -> str:
    """Describe a deadline relative to today: overdue, due today, due in N days."""
    delta = (deadline - today).days
    if delta < 0:
        days = -delta
        return f"overdue by {days} " + ("day" if days == 1 else "days")
    if delta == 0:
        return "due today"
    return f"due in {delta} " + ("day" if delta == 1 else "days")


def needs_attention(
    application: "dict[str, Any]", today: date, due_soon_days: int = DUE_SOON_DAYS
) -> bool:
    """True when an open application's next step is overdue or due within the window.

    Closed statuses (offer, rejected, withdrawn) are excluded on purpose: an offer is a
    decision, not a pending step, and a rejected or withdrawn application cannot be
    nudged into moving. A record with no deadline is never "needing attention" — the
    skill does not invent urgency the user never recorded.
    """
    if application["status"] in CLOSED_STATUSES:
        return False
    deadline = application.get("next_step_deadline")
    if not _is_iso_date(deadline):
        return False
    return date.fromisoformat(deadline) <= today + timedelta(days=due_soon_days)


def _urgency(application: "dict[str, Any]", today: date) -> str:
    deadline = date.fromisoformat(application["next_step_deadline"])
    return "overdue" if deadline < today else "due soon"


def _entry_lines(application: "dict[str, Any]", today: date) -> "list[str]":
    """The one- or two-line rendering of an application used by both sections."""
    pay = application.get("pay")
    heading = f"{application['company']} - {application['role']}"
    if isinstance(pay, str) and pay.strip():
        heading += f" ({pay})"

    lines = [f"{application['id']}: {heading}"]

    details: "list[str]" = []
    applied = application.get("date_applied")
    if isinstance(applied, str) and applied.strip():
        details.append(f"applied {applied}")
    source = application.get("source")
    if isinstance(source, str) and source.strip():
        details.append(f"via {source}")

    next_step = application.get("next_step")
    if isinstance(next_step, str) and next_step.strip():
        step = f"next: {next_step}"
        deadline = application.get("next_step_deadline")
        if _is_iso_date(deadline):
            due = date.fromisoformat(deadline)
            step += f" (deadline {deadline}, {deadline_phrase(due, today)})"
        details.append(step)

    if details:
        lines.append(" | ".join(details))
    return lines


def build_report(
    applications: "list[dict[str, Any]]",
    today: date,
    data_label: str,
    due_soon_days: int = DUE_SOON_DAYS,
) -> "list[str]":
    """Render the whole report as a list of lines, in report order."""
    attention = [
        application
        for application in applications
        if needs_attention(application, today, due_soon_days)
    ]
    attention.sort(key=lambda application: (application["next_step_deadline"], application["id"]))

    lines = [
        "job application pipeline",
        f"data:  {data_label}",
        f"today: {today.isoformat()}",
        "",
    ]

    if not applications:
        lines.append("no applications tracked yet - add the first one to data/applications.json")
        lines.append("")
    else:
        counts = []
        for status in STATUS_ORDER:
            count = sum(1 for application in applications if application["status"] == status)
            if count:
                counts.append(f"{count} {status}")
        plural = "application" if len(applications) == 1 else "applications"
        lines.append(f"{len(applications)} {plural} tracked: {', '.join(counts)}")
        lines.append("")

        for status in STATUS_ORDER:
            group = sorted(
                (application for application in applications if application["status"] == status),
                key=lambda application: (application.get("date_applied") or "", application["id"]),
            )
            if not group:
                continue
            lines.append(f"{status} ({len(group)})")
            for application in group:
                first, *rest = _entry_lines(application, today)
                lines.append(f"  - {first}")
                for detail in rest:
                    lines.append(f"      {detail}")
            lines.append("")

    lines.append(f"needs attention ({len(attention)})")
    if attention:
        for application in attention:
            first, *rest = _entry_lines(application, today)
            lines.append(f"  - [{_urgency(application, today)}] {first}")
            for detail in rest:
                lines.append(f"      {detail}")
    else:
        lines.append(
            f"  nothing overdue or due within {due_soon_days} "
            + ("day" if due_soon_days == 1 else "days")
        )
    lines.append("")

    hints: "list[str]" = []
    for application in applications:
        hints.extend(credential_hints(application))
    lines.append(f"privacy warnings ({len(hints)})")
    if hints:
        for hint in hints:
            lines.append(f"  - {hint}")
    else:
        lines.append("  none: no free-text field looks like a password, token or code")

    return lines


# --------------------------------------------------------------------------------------
# command line
# --------------------------------------------------------------------------------------

def _parse_today(value: str) -> date:
    if not _is_iso_date(value):
        raise argparse.ArgumentTypeError(f"{value!r} is not a YYYY-MM-DD date")
    return date.fromisoformat(value)


def _parse_due_soon_days(value: str) -> int:
    try:
        days = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a whole number of days") from None
    if days < 0:
        raise argparse.ArgumentTypeError("the due-soon window cannot be negative")
    return days


def main(
    argv: "Optional[Sequence[str]]" = None,
    out: "Optional[Any]" = None,
    err: "Optional[Any]" = None,
) -> int:
    """Print the report (exit 0) or the one clear error message (exit 1).

    ``out`` and ``err`` default to the real streams and exist so the test suite can run
    the command in-process with deterministic dates and capture both outputs.
    """
    parser = argparse.ArgumentParser(
        prog="pipeline_status.py",
        description="Print the job application pipeline and what needs attention. Offline, read-only.",
    )
    parser.add_argument(
        "--data", default=str(DEFAULT_DATA_PATH),
        help=f"path to the JSON data file (default: {DEFAULT_DATA_PATH})",
    )
    parser.add_argument(
        "--today", type=_parse_today, default=None,
        help="treat this YYYY-MM-DD date as today (default: the system date)",
    )
    parser.add_argument(
        "--due-soon-days", type=_parse_due_soon_days, default=DUE_SOON_DAYS,
        help=f"how many days ahead counts as due soon (default: {DUE_SOON_DAYS})",
    )
    args = parser.parse_args(argv)

    out_stream = sys.stdout if out is None else out
    err_stream = sys.stderr if err is None else err

    data_path = Path(args.data).expanduser()
    try:
        applications = load_applications(data_path)
    except DataError as exc:
        err_stream.write(f"ERROR  {exc}\n")
        return 1

    report = build_report(
        applications,
        today=args.today or date.today(),
        data_label=str(data_path),
        due_soon_days=args.due_soon_days,
    )
    out_stream.write("\n".join(report) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
