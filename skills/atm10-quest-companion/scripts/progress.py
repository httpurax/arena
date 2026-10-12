#!/usr/bin/env python3
"""progress.py - offline chapter-progress report for the atm10-quest-companion skill.

Reads one local JSON file (``<skill>/data/progress.json`` by default) mapping every
FTB Quests chapter of All the Mods 10 to a status (``pending`` or ``done``) and prints:

  * the overall completion percentage;
  * one completion line per progression stage (early-game -> tech -> magic -> endgame),
    in progression order;
  * the next unfinished chapters, in quest-book order (the order of the file, which
    mirrors the pack's own chapter grouping and ordering).

The chapter list itself comes from ``examples/progress.example.json``: copy that file to
``data/progress.json`` once, then flip ``pending`` to ``done`` as chapters are completed.
``data/`` is gitignored, so real progress never leaves the machine.

The script is stdlib-only, makes no network requests, and writes nothing. It never
raises a traceback at the user: a missing file, an empty file, malformed JSON, or a
chapter that breaks the documented schema is reported as one clear message, and the
exit status is 1.

Usage:
    python3 scripts/progress.py [--data PATH] [--next N]

``--next N`` caps how many unfinished chapters are listed (default 10).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional, Sequence

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = SKILL_ROOT / "data" / "progress.json"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# --------------------------------------------------------------------------------------
# schema
# --------------------------------------------------------------------------------------

# The four progression stages, in the order the pack plays out. Every chapter in the
# progress file must carry one of these stage ids; the report lists stages in this order.
STAGES: "tuple[tuple[str, str], ...]" = (
    ("early-game", "Early Game"),
    ("tech", "Tech & Automation"),
    ("magic", "Magic"),
    ("endgame", "Endgame & Exploration"),
)
STAGE_IDS = frozenset(stage_id for stage_id, _ in STAGES)
STAGE_TITLES = dict(STAGES)

# A chapter status. Exactly two: a chapter is either finished or it is not.
VALID_STATUSES = frozenset({"pending", "done"})

REQUIRED_FIELDS = ("id", "title", "stage", "status")
OPTIONAL_FIELDS = ("group",)
KNOWN_FIELDS = frozenset(REQUIRED_FIELDS + OPTIONAL_FIELDS)

DEFAULT_NEXT_LIMIT = 10


class ProgressError(Exception):
    """One clear, user-facing failure: a bad file, a bad path, or a bad argument."""


# --------------------------------------------------------------------------------------
# loading and validation
# --------------------------------------------------------------------------------------

def load_progress(path: Path) -> "list[dict[str, Any]]":
    """Read the progress file and return its validated chapter list.

    Every failure mode - missing, unreadable, empty, malformed JSON, wrong shape, bad
    field values - raises ProgressError with a single actionable message instead of
    letting an exception escape as a traceback.
    """
    if not path.exists():
        raise ProgressError(
            f"no progress file at {path}\n"
            f"create one first (from the skill directory):\n"
            f"  mkdir -p data && cp examples/progress.example.json data/progress.json"
        )
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ProgressError(f"cannot read the progress file {path}: {exc}") from exc

    if not text.strip():
        raise ProgressError(
            f"the progress file {path} is empty\n"
            f"copy examples/progress.example.json into it, then flip statuses to done"
        )

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProgressError(
            f"the progress file {path} is not valid JSON: {exc.msg} (line {exc.lineno}, column {exc.colno})"
        ) from exc

    problems = validate(data)
    if problems:
        listing = "\n".join(f"  - {problem}" for problem in problems)
        raise ProgressError(f"the progress file {path} does not match the schema:\n{listing}")
    return data["chapters"]


def validate(data: Any) -> "list[str]":
    """Return every schema problem in ``data`` (empty list when it is valid).

    The document is ``{"chapters": [...]}``; each chapter needs ``id``, ``title``,
    ``stage``, and ``status``, may carry ``group``, and nothing else. Ids are unique,
    stages are the four progression stages, statuses are pending/done.
    """
    problems: "list[str]" = []
    if not isinstance(data, dict):
        return ["the file must contain a JSON object {\"chapters\": [...]}"]
    unknown_top = sorted(set(data) - {"chapters"})
    if unknown_top:
        problems.append(f"unknown top-level key(s): {', '.join(unknown_top)} (expected only 'chapters')")
    chapters = data.get("chapters")
    if chapters is None:
        problems.append("missing key 'chapters'")
        return problems
    if not isinstance(chapters, list):
        return problems + ["'chapters' must be a list of chapter objects"]
    if not chapters:
        return problems + ["'chapters' is empty - copy examples/progress.example.json and edit statuses"]

    seen_ids: "dict[str, int]" = {}
    for index, chapter in enumerate(chapters, 1):
        where = f"chapters[{index}]"
        if not isinstance(chapter, dict):
            problems.append(f"{where}: expected an object, got {type(chapter).__name__}")
            continue
        chapter_id = chapter.get("id")
        if isinstance(chapter_id, str) and chapter_id.strip():
            where = f"chapters[{index}] ({chapter_id})"
            if chapter_id in seen_ids:
                problems.append(f"{where}: duplicate id (first seen at chapters[{seen_ids[chapter_id]}])")
            else:
                seen_ids[chapter_id] = index
        for field in REQUIRED_FIELDS:
            value = chapter.get(field)
            if value is None:
                problems.append(f"{where}: missing required field '{field}'")
            elif not isinstance(value, str) or not value.strip():
                problems.append(f"{where}: field '{field}' must be a non-empty string")
        unknown = sorted(set(chapter) - KNOWN_FIELDS)
        if unknown:
            problems.append(f"{where}: unknown field(s): {', '.join(unknown)}")
        group = chapter.get("group")
        if group is not None and not isinstance(group, str):
            problems.append(f"{where}: field 'group' must be a string (or absent)")
        stage = chapter.get("stage")
        if isinstance(stage, str) and stage not in STAGE_IDS:
            problems.append(
                f"{where}: stage '{stage}' is not one of: {', '.join(sorted(STAGE_IDS))}"
            )
        status = chapter.get("status")
        if isinstance(status, str) and status not in VALID_STATUSES:
            problems.append(
                f"{where}: status '{status}' is not one of: {', '.join(sorted(VALID_STATUSES))}"
            )
    return problems


# --------------------------------------------------------------------------------------
# report math
# --------------------------------------------------------------------------------------

def stage_summary(chapters: "Sequence[dict[str, Any]]") -> "list[dict[str, Any]]":
    """Per-stage totals, in progression order (a stage with no chapters still appears)."""
    summary = [
        {"id": stage_id, "title": STAGE_TITLES[stage_id], "total": 0, "done": 0}
        for stage_id, _ in STAGES
    ]
    by_id = {row["id"]: row for row in summary}
    for chapter in chapters:
        row = by_id[chapter["stage"]]
        row["total"] += 1
        if chapter["status"] == "done":
            row["done"] += 1
    for row in summary:
        row["percent"] = percentage(row["done"], row["total"])
    return summary


def overall_summary(chapters: "Sequence[dict[str, Any]]") -> "dict[str, Any]":
    """Overall done/total/percent across every chapter."""
    total = len(chapters)
    done = sum(1 for chapter in chapters if chapter["status"] == "done")
    return {"total": total, "done": done, "percent": percentage(done, total)}


def percentage(done: int, total: int) -> float:
    """Completion percentage rounded to one decimal; 0.0 when there is nothing to do."""
    return round(done * 100.0 / total, 1) if total else 0.0


def next_pending(chapters: "Sequence[dict[str, Any]]", limit: int) -> "list[dict[str, Any]]":
    """Unfinished chapters in quest-book order (the file order), capped at ``limit``."""
    pending = [chapter for chapter in chapters if chapter["status"] != "done"]
    return pending[:limit]


def pending_count(chapters: "Sequence[dict[str, Any]]") -> int:
    return sum(1 for chapter in chapters if chapter["status"] != "done")


# --------------------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------------------

def format_report(chapters: "Sequence[dict[str, Any]]", data_path: Path, limit: int) -> str:
    """The full human-readable report for a valid chapter list."""
    overall = overall_summary(chapters)
    lines: "list[str]" = []
    lines.append("atm10 quest companion - chapter progress")
    lines.append(f"data: {data_path}")
    lines.append("")
    lines.append(
        f"overall: {overall['done']}/{overall['total']} chapters done ({overall['percent']:.1f}%)"
    )
    lines.append("")

    lines.append("per stage (progression order)")
    id_width = max(len(stage_id) for stage_id, _ in STAGES)
    title_width = max(len(title) for _, title in STAGES)
    for row in stage_summary(chapters):
        lines.append(
            f"  {row['id']:<{id_width}}  {row['title']:<{title_width}}  "
            f"{row['done']:>3}/{row['total']:<3} done ({row['percent']:>5.1f}%)"
        )
    lines.append("")

    remaining = pending_count(chapters)
    if remaining == 0:
        lines.append("all chapters done - the ATM Star is yours. New pack version? Re-check the quest book.")
    else:
        shown = next_pending(chapters, limit)
        lines.append(f"next unfinished chapters (quest-book order, showing {len(shown)} of {remaining})")
        for position, chapter in enumerate(shown, 1):
            group = chapter.get("group") or "General"
            lines.append(
                f"  {position:>3}. [{chapter['stage']}] {chapter['title']} "
                f"({chapter['id']}, group: {group})"
            )
        lines.append("")
        lines.append(
            "the in-game quest book (FTB Quests) and JEI are authoritative for what each"
            " chapter actually requires; this list only tracks completion."
        )
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------------------

def parse_args(argv: "Optional[Sequence[str]]") -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="progress.py",
        description="Report ATM10 quest-chapter progress from a local JSON file.",
    )
    parser.add_argument(
        "--data", default=str(DEFAULT_DATA),
        help=f"progress file to read (default: {DEFAULT_DATA})",
    )
    parser.add_argument(
        "--next", type=int, default=DEFAULT_NEXT_LIMIT, dest="next_limit",
        metavar="N",
        help=f"how many unfinished chapters to list (default: {DEFAULT_NEXT_LIMIT})",
    )
    return parser.parse_args(argv)


def main(argv: "Optional[Sequence[str]]" = None) -> int:
    """Print the progress report; return 0 on success, 1 on any user-facing problem."""
    try:
        args = parse_args(argv)
        if args.next_limit < 1:
            raise ProgressError(f"--next must be at least 1 (got {args.next_limit})")
        chapters = load_progress(Path(args.data).expanduser())
        print(format_report(chapters, Path(args.data).expanduser(), args.next_limit))
        return 0
    except ProgressError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:  # an unwritable stdout, a broken pipe - still no traceback
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
