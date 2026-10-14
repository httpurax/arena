#!/usr/bin/env python3
"""progress.py - offline chapter-progress tracker for the atm10-quest-companion skill.

Reads one local JSON file (``<skill>/data/progress.json`` by default) mapping every
FTB Quests chapter of All the Mods 10 to a status (``pending`` or ``done``) and prints:

  * the overall completion percentage;
  * one completion line per progression stage (early-game -> tech -> magic -> endgame),
    in progression order;
  * the next unfinished chapters, in quest-book order (the order of the file, which
    mirrors the pack's own chapter grouping and ordering), optionally filtered to one
    stage with ``--stage``;
  * a pack-drift warning section when the file disagrees with the chapter list this
    skill ships (unknown or missing chapter ids, a different or absent pack-version
    stamp). Warnings never fail the run and never change the numbers: the in-game quest
    book stays authoritative.

It can also flip chapter statuses itself, with validation *before* anything is written::

    python3 scripts/progress.py --set mekanism done --set "Mekanism: Reactors" pending

``--set`` accepts a chapter id or an exact chapter title, refuses an unknown one with a
clear message (plus the closest ids it can find) instead of a traceback, rewrites the
file through a temporary file in the same directory (so a crash cannot leave a
half-written progress file behind), and then prints the normal report for the file as it
now stands on disk.

The chapter list itself comes from ``examples/progress.example.json``, which carries the
ATM10 pack-version stamp the list was researched from (``pack_version``, ``8.x``): copy
that file to ``data/progress.json`` once, then flip ``pending`` to ``done`` as chapters
are completed. ``data/`` is gitignored, so real progress never leaves the machine.

The script is stdlib-only, makes no network requests, and never raises a traceback at
the user: a missing file, an empty file, malformed JSON, a chapter that breaks the
documented schema, an unknown chapter id, or an unwritable path is reported as one clear
message, and the exit status is 1.

Usage:
    python3 scripts/progress.py [--data PATH] [--next N] [--stage STAGE_ID]
                                [--set CHAPTER_ID STATUS]...
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, FrozenSet, NamedTuple, Optional, Sequence, Tuple

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
STAGE_ORDER = tuple(stage_id for stage_id, _ in STAGES)

# A chapter status. Exactly two: a chapter is either finished or it is not.
VALID_STATUSES = frozenset({"pending", "done"})

REQUIRED_FIELDS = ("id", "title", "stage", "status")
OPTIONAL_FIELDS = ("group",)
KNOWN_FIELDS = frozenset(REQUIRED_FIELDS + OPTIONAL_FIELDS)
# The order ``--set`` rewrites each chapter in, matching the shipped example file.
CHAPTER_FIELD_ORDER = ("id", "title", "group", "stage", "status")

# Pack-version stamp: which ATM10 version the chapter list was researched from. The
# example file carries it; a progress file copied from the example inherits it, and the
# drift check compares the two. Both keys are optional so an older progress file (written
# before the stamp existed) still loads - it just gets told it is unstamped.
PACK_VERSION_FIELD = "pack_version"
PACK_VERSION_SOURCE_FIELD = "pack_version_source"
TOP_LEVEL_FIELDS = (PACK_VERSION_FIELD, PACK_VERSION_SOURCE_FIELD, "chapters")
STAMP_FIELDS = (PACK_VERSION_FIELD, PACK_VERSION_SOURCE_FIELD)
# A stamp is a pack version such as "8.x", "8.2", or "8.2.1". Anything else still loads
# (the field only has to be a non-empty string) but is reported as drift.
PACK_VERSION_RE = re.compile(r"^\d+(\.\d+)*(\.[xX])?$")
DEFAULT_PACK_VERSION = "8.x"

DEFAULT_NEXT_LIMIT = 10
# How many chapter ids a drift warning spells out before falling back to "(+N more)".
DRIFT_ID_LIMIT = 6


class ProgressError(Exception):
    """One clear, user-facing failure: a bad file, a bad path, or a bad argument."""


class KnownChapters(NamedTuple):
    """The chapter list this skill ships, used as the reference for the drift check.

    A NamedTuple rather than a dataclass on purpose: this module is imported by the skill's
    tests through ``importlib.util.module_from_spec`` without being registered in
    ``sys.modules``, and ``@dataclass`` resolves its string annotations through
    ``sys.modules[cls.__module__]`` - which then does not exist and raises AttributeError
    at import time. ``typing`` collections are not resolved that eagerly.
    """

    ids: FrozenSet[str]
    order: Tuple[str, ...]
    version: str
    path: Path

    @property
    def total(self) -> int:
        """How many chapters the known list holds."""
        return len(self.order)


# --------------------------------------------------------------------------------------
# loading and validation
# --------------------------------------------------------------------------------------

def load_document(path: Path) -> "tuple[list[dict[str, Any]], dict[str, str]]":
    """Read the progress file and return ``(chapters, stamps)``.

    ``stamps`` holds whichever pack-version fields the file carries (possibly none).
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

    stamps = {
        key: data[key] for key in STAMP_FIELDS
        if isinstance(data.get(key), str) and data[key].strip()
    }
    return data["chapters"], stamps


def load_progress(path: Path) -> "list[dict[str, Any]]":
    """Read the progress file and return its validated chapter list (stamps dropped)."""
    return load_document(path)[0]


def load_known_chapters(path: Path = EXAMPLE_DATA) -> "Optional[KnownChapters]":
    """Load the shipped chapter list that ``data/progress.json`` is checked against.

    Returns ``None`` - silently disabling the drift check rather than breaking the
    report - when the example file is missing, unreadable, malformed, or carries no
    usable chapter ids. A progress report is more useful without a drift check than
    without a report.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        return None
    ids = [
        chapter["id"].strip() for chapter in chapters
        if isinstance(chapter, dict) and isinstance(chapter.get("id"), str) and chapter["id"].strip()
    ]
    if not ids:
        return None
    version = data.get(PACK_VERSION_FIELD)
    if not isinstance(version, str) or not version.strip():
        version = DEFAULT_PACK_VERSION
    return KnownChapters(ids=frozenset(ids), order=tuple(ids), version=version.strip(), path=path)


def validate(data: Any) -> "list[str]":
    """Return every schema problem in ``data`` (empty list when it is valid).

    The document is ``{"chapters": [...]}`` plus the optional pack-version stamp keys;
    each chapter needs ``id``, ``title``, ``stage``, and ``status``, may carry ``group``,
    and nothing else. Ids are unique, stages are the four progression stages, statuses
    are pending/done, and both stamp fields are non-empty strings when present.
    """
    problems: "list[str]" = []
    if not isinstance(data, dict):
        return ["the file must contain a JSON object {\"chapters\": [...]}"]
    unknown_top = sorted(set(data) - set(TOP_LEVEL_FIELDS))
    if unknown_top:
        problems.append(
            f"unknown top-level key(s): {', '.join(unknown_top)} "
            f"(expected only {', '.join(repr(field) for field in TOP_LEVEL_FIELDS)})"
        )
    for field in STAMP_FIELDS:
        value = data.get(field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            problems.append(f"'{field}' must be a non-empty string (or absent)")
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


def next_pending(
    chapters: "Sequence[dict[str, Any]]", limit: int, stage: "Optional[str]" = None
) -> "list[dict[str, Any]]":
    """Unfinished chapters in quest-book order (the file order), capped at ``limit``.

    ``stage`` (one of STAGE_IDS) narrows the list to a single progression stage; the
    overall and per-stage numbers are never filtered, only this list.
    """
    pending = [
        chapter for chapter in chapters
        if chapter["status"] != "done" and (stage is None or chapter["stage"] == stage)
    ]
    return pending[:limit]


def pending_count(chapters: "Sequence[dict[str, Any]]", stage: "Optional[str]" = None) -> int:
    return sum(
        1 for chapter in chapters
        if chapter["status"] != "done" and (stage is None or chapter["stage"] == stage)
    )


# --------------------------------------------------------------------------------------
# pack-version drift
# --------------------------------------------------------------------------------------

def _id_listing(ids: "Sequence[str]", limit: int = DRIFT_ID_LIMIT) -> str:
    """A comma-separated id list, shortened with '(+N more)' past ``limit`` entries."""
    head = ", ".join(ids[:limit])
    rest = len(ids) - min(len(ids), limit)
    return f"{head} (+{rest} more)" if rest > 0 else head


def check_drift(
    chapters: "Sequence[dict[str, Any]]",
    known: "Optional[KnownChapters]",
    stamps: "Optional[Dict[str, str]]" = None,
) -> "list[str]":
    """Warning lines for a progress file that disagrees with the shipped chapter list.

    Three kinds of drift, none of them fatal:

      * a pack-version stamp that differs from the known list's, or is missing entirely,
        or does not look like a version;
      * chapter ids present in the file but absent from the known list (the usual sign of
        a pack update, or of a hand-edited file);
      * known chapter ids absent from the file (a chapter dropped or renamed by a pack
        update, or a file built from a partial list).

    Returns an empty list when there is nothing to warn about, or when the known list
    could not be loaded (the check then stays silent rather than guessing).
    """
    if known is None:
        return []
    stamps = stamps or {}
    warnings: "list[str]" = []

    version = stamps.get(PACK_VERSION_FIELD, "").strip()
    if not version:
        warnings.append(
            f'this file carries no "{PACK_VERSION_FIELD}" stamp, so its pack version cannot be '
            f"checked (the known chapter list is pack {known.version}); add the stamp this file "
            f"was copied with, e.g. \"{PACK_VERSION_FIELD}\": \"{known.version}\""
        )
    else:
        if known.version and version != known.version:
            warnings.append(
                f"this file is stamped pack {version}, but the known chapter list is pack "
                f"{known.version} ({known.path.name}) - the chapters may no longer line up"
            )
        if not PACK_VERSION_RE.match(version):
            warnings.append(
                f'the "{PACK_VERSION_FIELD}" stamp {version!r} does not look like a pack version '
                f'(expected a form such as 8.x or 8.2)'
            )

    file_ids = [chapter.get("id") for chapter in chapters if isinstance(chapter.get("id"), str)]
    id_set = set(file_ids)
    extra = [chapter_id for chapter_id in file_ids if chapter_id not in known.ids]
    missing = [chapter_id for chapter_id in known.order if chapter_id not in id_set]
    if extra:
        noun = "id" if len(extra) == 1 else "ids"
        warnings.append(
            f"{len(extra)} chapter {noun} in this file are not in the known pack {known.version} "
            f"list of {known.total} chapters: {_id_listing(extra)}"
        )
        warnings.append(
            "  the in-game quest book is authoritative: if these chapters really exist, the pack "
            "has moved past the list this skill ships, which is worth re-researching; if they do "
            "not, they were added by hand and can be removed"
        )
    if missing:
        noun = "id" if len(missing) == 1 else "ids"
        warnings.append(
            f"{len(missing)} chapter {noun} from the known pack {known.version} list are missing "
            f"from this file: {_id_listing(missing)}"
        )
    return warnings


# --------------------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------------------

def format_report(
    chapters: "Sequence[dict[str, Any]]",
    data_path: Path,
    limit: int,
    stage: "Optional[str]" = None,
    known: "Optional[KnownChapters]" = None,
    stamps: "Optional[Dict[str, str]]" = None,
) -> str:
    """The full human-readable report for a valid chapter list.

    ``stage`` filters only the next-chapters list; ``known`` and ``stamps`` add the
    pack-drift section (both optional, so a bare call still renders the old report).
    """
    overall = overall_summary(chapters)
    stamps = stamps or {}
    lines: "list[str]" = []
    lines.append("atm10 quest companion - chapter progress")
    lines.append(f"data: {data_path}")
    if known is not None or stamps:
        stamp = stamps.get(PACK_VERSION_FIELD, "").strip() or "unstamped"
        if known is not None:
            lines.append(
                f"pack: {stamp}  (known chapter list: pack {known.version}, {known.total} chapters)"
            )
        else:
            lines.append(f"pack: {stamp}")
    lines.append("")
    lines.append(
        f"overall: {overall['done']}/{overall['total']} chapters done ({overall['percent']:.1f}%)"
    )
    lines.append("")

    lines.append("per stage (progression order)")
    id_width = max(len(stage_id) for stage_id, _ in STAGES)
    title_width = max(len(title) for _, title in STAGES)
    for row in stage_summary(chapters):
        marker = "  <==" if stage is not None and row["id"] == stage else ""
        lines.append(
            f"  {row['id']:<{id_width}}  {row['title']:<{title_width}}  "
            f"{row['done']:>3}/{row['total']:<3} done ({row['percent']:>5.1f}%){marker}"
        )
    lines.append("")

    remaining = pending_count(chapters, stage)
    if remaining == 0:
        if stage is not None:
            lines.append(
                f"no unfinished chapters in stage '{stage}' ({STAGE_TITLES[stage]}) - "
                f"the other stages still have {pending_count(chapters)} pending"
            )
        else:
            lines.append("all chapters done - the ATM Star is yours. New pack version? Re-check the quest book.")
    else:
        shown = next_pending(chapters, limit, stage)
        scope = f"stage filter: {stage}, " if stage is not None else ""
        lines.append(f"next unfinished chapters (quest-book order, {scope}showing {len(shown)} of {remaining})")
        for position, chapter in enumerate(shown, 1):
            group = chapter.get("group") or "General"
            lines.append(
                f"  {position:>3}. [{chapter['stage']}] {chapter['title']} "
                f"({chapter['id']}, group: {group})"
            )

    drift = check_drift(chapters, known, stamps)
    if drift:
        lines.append("")
        lines.append(
            f"pack drift (this file vs the known chapter list for pack "
            f"{known.version if known is not None else '?'})"
        )
        for warning in drift:
            # A warning whose text starts with a space is a continuation of the one above.
            if warning.startswith(" "):
                lines.append(f"    {warning.strip()}")
            else:
                lines.append(f"  ! {warning}")

    lines.append("")
    lines.append(
        "the in-game quest book (FTB Quests) and JEI are authoritative for what each"
        " chapter actually requires; this list only tracks completion."
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# writing (--set)
# --------------------------------------------------------------------------------------

def parse_stage(value: str) -> str:
    """Validate a ``--stage`` argument against the four progression stages."""
    key = (value or "").strip().lower()
    if key not in STAGE_IDS:
        raise ProgressError(
            f"--stage '{value}' is not a progression stage; expected one of: "
            + ", ".join(STAGE_ORDER)
        )
    return key


def resolve_chapter(
    chapters: "Sequence[dict[str, Any]]", wanted: str, data_path: Path
) -> "dict[str, Any]":
    """Find the chapter ``--set`` means, or fail with the closest candidates.

    Matches a chapter id exactly, then an exact chapter title (case-insensitively, so
    ``--set "Mekanism: Reactors" done`` works), then gives up with a message naming the
    nearest ids and titles instead of guessing - a silent near-match would mark the wrong
    chapter done.
    """
    key = (wanted or "").strip()
    for chapter in chapters:
        if chapter.get("id") == key:
            return chapter
    for chapter in chapters:
        if isinstance(chapter.get("title"), str) and chapter["title"].strip().lower() == key.lower():
            return chapter

    ids = [chapter.get("id", "") for chapter in chapters]
    title_to_id = {}
    for chapter in chapters:
        title = chapter.get("title")
        if isinstance(title, str) and title.strip():
            title_to_id.setdefault(title.strip().lower(), chapter.get("id", ""))
    close = list(difflib.get_close_matches(key, ids, n=3, cutoff=0.5))
    for match in difflib.get_close_matches(key.lower(), list(title_to_id), n=3, cutoff=0.5):
        candidate = title_to_id[match]
        if candidate and candidate not in close:
            close.append(candidate)
    close = close[:4]
    hints = f"\n  closest chapters in that file: {', '.join(close)}" if close else ""
    raise ProgressError(
        f"unknown chapter '{wanted}' for --set: no chapter id or title in {data_path} matches it"
        f"{hints}\n"
        f"  ids come from examples/progress.example.json ({len(chapters)} chapters in this file);"
        f" an exact chapter title works too, e.g. --set \"Mekanism\" done"
    )


def apply_status_changes(
    chapters: "Sequence[dict[str, Any]]",
    requested: "Sequence[Sequence[str]]",
    data_path: Path,
) -> "tuple[list[str], int]":
    """Flip the requested statuses in place; return ``(report lines, changed count)``.

    Every request is validated first, so one bad ``--set`` cannot leave an earlier one
    applied: an unknown chapter or an invalid status raises ProgressError before any
    chapter is touched, and the caller therefore writes nothing.
    """
    resolved: "list[tuple[dict[str, Any], str]]" = []
    for entry in requested:
        wanted, raw_status = entry[0], entry[1]
        status = (raw_status or "").strip().lower()
        if status not in VALID_STATUSES:
            raise ProgressError(
                f"--set status '{raw_status}' is not one of: {', '.join(sorted(VALID_STATUSES))}"
            )
        resolved.append((resolve_chapter(chapters, wanted, data_path), status))

    lines: "list[str]" = []
    changed = 0
    for chapter, status in resolved:
        previous = chapter["status"]
        if previous == status:
            lines.append(f"set: {chapter['id']} ({chapter['title']}) -> {status}: already {status}, nothing to change")
            continue
        chapter["status"] = status
        changed += 1
        lines.append(f"set: {chapter['id']} ({chapter['title']}) -> {status} (was {previous})")
    return lines, changed


def build_document(
    chapters: "Sequence[dict[str, Any]]", stamps: "Optional[Dict[str, str]]" = None
) -> "dict[str, Any]":
    """Assemble the document to write: stamp keys first, then chapters in canonical order."""
    stamps = stamps or {}
    document: "dict[str, Any]" = {}
    for field in STAMP_FIELDS:
        if field in stamps:
            document[field] = stamps[field]
    document["chapters"] = [
        {field: chapter[field] for field in CHAPTER_FIELD_ORDER if field in chapter}
        for chapter in chapters
    ]
    return document


def write_progress(path: Path, document: "dict[str, Any]") -> None:
    """Validate, then write the progress file atomically.

    The document is re-validated immediately before writing, so a malformed document can
    never reach the disk, and it is written to a temporary file in the same directory
    followed by ``os.replace``, so an interrupted run leaves either the old file or the
    new one - never a half-written progress file.
    """
    problems = validate(document)
    if problems:
        listing = "\n".join(f"  - {problem}" for problem in problems)
        raise ProgressError(
            f"refusing to write {path}: the updated document does not match the schema:\n{listing}"
        )
    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    directory = path.parent if str(path.parent) else Path(".")
    handle = None
    temporary: "Optional[Path]" = None
    try:
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=str(directory),
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        )
        temporary = Path(handle.name)
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
        handle.close()
        handle = None
        os.replace(str(temporary), str(path))
        temporary = None
    except OSError as exc:
        raise ProgressError(f"cannot write the progress file {path}: {exc}") from exc
    finally:
        if handle is not None:
            try:
                handle.close()
            except OSError:
                pass
        if temporary is not None:
            try:
                os.unlink(str(temporary))
            except OSError:
                pass


# --------------------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------------------

def parse_args(argv: "Optional[Sequence[str]]") -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="progress.py",
        description="Report ATM10 quest-chapter progress from a local JSON file, "
                    "and optionally flip chapter statuses.",
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
    parser.add_argument(
        "--stage", default=None, metavar="STAGE_ID",
        help="list only the unfinished chapters of one stage: "
             + ", ".join(STAGE_ORDER),
    )
    parser.add_argument(
        "--set", nargs=2, action="append", default=None, dest="set_status",
        metavar=("CHAPTER_ID", "STATUS"),
        help="mark a chapter done or pending (id or exact title), then report; repeatable, "
             "validated before the file is written",
    )
    return parser.parse_args(argv)


def main(argv: "Optional[Sequence[str]]" = None) -> int:
    """Print the progress report; return 0 on success, 1 on any user-facing problem."""
    try:
        args = parse_args(argv)
        if args.next_limit < 1:
            raise ProgressError(f"--next must be at least 1 (got {args.next_limit})")
        stage = parse_stage(args.stage) if args.stage else None
        data_path = Path(args.data).expanduser()
        known = load_known_chapters()

        if args.set_status:
            chapters, stamps = load_document(data_path)
            lines, changed = apply_status_changes(chapters, args.set_status, data_path)
            for line in lines:
                print(line)
            if changed:
                write_progress(data_path, build_document(chapters, stamps))
                noun = "chapter" if changed == 1 else "chapters"
                print(f"wrote: {data_path} ({changed} {noun} updated)")
            else:
                print(f"unchanged: {data_path} was not written")
            # Report what is on disk now, so the numbers shown are the numbers saved.
            chapters, stamps = load_document(data_path)
            print("")
        else:
            chapters, stamps = load_document(data_path)

        print(format_report(chapters, data_path, args.next_limit,
                            stage=stage, known=known, stamps=stamps))
        return 0
    except ProgressError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:  # an unwritable stdout, a broken pipe - still no traceback
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
