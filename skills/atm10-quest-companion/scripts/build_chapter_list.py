#!/usr/bin/env python3
"""build_chapter_list.py - rebuild the skill's chapter list from a local ATM-10 checkout.

Given a local clone of the official `AllTheMods/ATM-10` pack repository (the user clones
it; this script clones nothing and touches no network), this reads the FTB Quests config
and rewrites ``examples/progress.example.json`` from it:

  * chapter ids and quest counts come from ``config/ftbquests/quests/chapters/*.snbt``
    (the id is the chapter's own ``filename``, matching its SNBT basename);
  * quest-book order comes from each chapter's ``order_index``, laid out as the book
    shows it: standalone chapters first, then the groups in ``chapter_groups.snbt``
    order, chapters within a group by ``order_index``;
  * chapter and group titles come from the ``lang/en_us`` lang SNBT, with Minecraft
    ``&`` formatting codes stripped (an escaped ``\\&`` is a literal ampersand and is
    left alone);
  * the pack version comes from ``config/bcc-common.toml`` (``modpackVersion``); the
    shipped ``pack_version`` stamp tracks the whole major line, so pack ``8.2`` stamps
    ``8.x`` while the exact version goes into ``pack_version_source``;
  * each chapter's progression stage (``early-game``/``tech``/``magic``/``endgame``)
    comes from ``STAGE_ASSIGNMENTS`` below - the quest book has no stage notion; that
    mapping *is* the skill's progression model. A chapter the table does not know
    (a pack update added it) stops the build with a clear error naming the chapter,
    so a human assigns the stage instead of the tool guessing.

Usage (from the skill directory)::

    python3 scripts/build_chapter_list.py /path/to/ATM-10 --commit e5e3d1d83e
    python3 scripts/build_chapter_list.py /path/to/ATM-10 --check

The default action rewrites ``examples/progress.example.json`` (review with
``git diff``, then reconcile the private progress file with
``scripts/progress.py --sync``). ``--check`` writes nothing: it exits 0 when the
output file is already up to date and 1 when it would change, printing what changed.

The script is stdlib-only, never opens a socket, and never raises a traceback at the
user: a missing path, a directory that is not an ATM-10 checkout, a malformed SNBT
file, or a chapter the skill has not placed in a stage yet is one clear message with
exit status 1. The SNBT grammar reader lives in the sibling module ``snbt.py``.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple

try:
    import snbt
except ImportError:  # loaded by the test suite, where scripts/ is not on sys.path
    import importlib.util

    _snbt_path = Path(__file__).resolve().parent / "snbt.py"
    _snbt_spec = importlib.util.spec_from_file_location("snbt", _snbt_path)
    assert _snbt_spec is not None and _snbt_spec.loader is not None
    snbt = importlib.util.module_from_spec(_snbt_spec)
    _snbt_spec.loader.exec_module(snbt)

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = SKILL_ROOT / "examples" / "progress.example.json"

# Inside a checkout of https://github.com/AllTheMods/ATM-10.
QUESTS_REL = Path("config") / "ftbquests" / "quests"
CHAPTERS_REL = QUESTS_REL / "chapters"
CHAPTER_GROUPS_REL = QUESTS_REL / "chapter_groups.snbt"
LANG_CHAPTER_REL = QUESTS_REL / "lang" / "en_us" / "chapter.snbt"
LANG_GROUP_REL = QUESTS_REL / "lang" / "en_us" / "chapter_group.snbt"
BCC_REL = Path("config") / "bcc-common.toml"

CLONE_HINT = (
    "clone it first, e.g.:  git clone https://github.com/AllTheMods/ATM-10\n"
    "then pass the checkout directory (this tool reads local files only, always offline)"
)

# The four progression stages, in the order references/progression.md plays them out.
STAGES = ("early-game", "tech", "magic", "endgame")

# The chapter -> stage mapping. This table is the skill's progression model, not pack
# data: the quest config knows nothing about stages. It covers all 66 chapters of the
# pack-8.x quest book; a build against a checkout whose book has chapters missing
# here fails loudly (that is the pack-update "review" moment), never guesses.
STAGE_ASSIGNMENTS: "dict[str, str]" = {
    # Main Questline: chapter 1 plays before any mod; chapters 2-4 are the endgame spine.
    "welcome": "early-game",
    "bounty_board": "early-game",
    "building_tips": "early-game",
    "tips_and_tricks": "early-game",
    "mainquestline_part_1": "early-game",
    "allthemodium": "endgame",
    "chapter_2_the_star": "endgame",
    "achapter_2r_6the_atm_star": "endgame",
    # Tools and Gear: vanilla-plus kits first; mahou_tsukai is a magic mod on this page.
    "apotheosis_gear": "early-game",
    "artifacts": "early-game",
    "basic_armor": "early-game",
    "basic_tools": "early-game",
    "mahou_tsukai": "magic",
    "relics": "early-game",
    "silent_gear": "early-game",
    # Storage.
    "storage": "early-game",
    "applied_energistics_2": "tech",
    "extended__advanced_ae": "tech",
    "refined_storage": "tech",
    # Logistics.
    "basic_logistics": "early-game",
    "integrated_dynamics": "tech",
    "modular_router": "tech",
    "pylons": "tech",
    # Resources.
    "apotheosis_2": "early-game",
    "food_and_farming": "early-game",
    "hostile_neural_networks": "tech",
    "elmystical_agriculturerr": "tech",
    "productive_bees": "tech",
    "productive_trees": "tech",
    # Tech. Draconic Evolution is an ATM Star component line, so it is endgame.
    "create": "tech",
    "draconic_evolution": "endgame",
    "immersive_engineering": "tech",
    "industrial_foregoing": "tech",
    "justdirethings": "tech",
    "mekanism": "tech",
    "mekanism_reactors": "tech",
    "oritech": "tech",
    "xycraft": "tech",
    "pneumaticcraft": "tech",
    "railcraft": "tech",
    # Modern Industrialization.
    "mi_steam": "tech",
    "mi_electric": "tech",
    "mi_digital": "tech",
    "mi_endgame": "tech",
    # Power.
    "basic_power": "early-game",
    "extreme_reactors": "tech",
    "generators": "tech",
    "powah": "tech",
    # Magic.
    "apothic_enchanting": "magic",
    "ars_nouveau": "magic",
    "evilcraft": "magic",
    "forbidden__arcanus": "magic",
    "iron_spells_and_spellbooks": "magic",
    "natures_aura": "magic",
    "neo_vitae": "magic",
    "occultism": "magic",
    "theurgy": "magic",
    # Exploration: the dimension and boss lines are endgame content.
    "aether": "endgame",
    "bumblezone": "endgame",
    "auroral": "endgame",
    "cataclysm": "endgame",
    "deeper_and_darker": "endgame",
    "eternal_starlight": "endgame",
    "ice__fire": "endgame",
    "twilight_forest": "endgame",
    "undergarden": "endgame",
}

# Minecraft text formatting codes look like &4 or &l; an ampersand that is meant
# literally is escaped as \& (SNBT "\\&") and must survive normalization.
_FORMAT_CODE_RE = re.compile(r"(?<!\\)&[0-9a-fk-orA-FK-OR]")

_VALID_VERSION_RE = re.compile(r"^\d+(\.\d+)*$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# JSON document field order, matching how examples/progress.example.json is written.
CHAPTER_FIELD_ORDER = ("id", "title", "group", "stage", "status")


class BuildError(Exception):
    """One clear, user-facing failure: a bad path, a bad checkout, or bad config."""


class CheckoutLayout(NamedTuple):
    """The files of an ATM-10 checkout this tool reads, existence already verified."""

    root: Path
    chapters_dir: Path
    chapter_groups: Path
    lang_chapter: Path
    lang_group: Path
    bcc_config: Path


class RawChapter(NamedTuple):
    """One parsed chapter file, before ordering and stage assignment."""

    identifier: str
    title: str
    group_id: str  # the FTB group hex id; "" for a standalone chapter
    order_index: int
    quests: int


class DiffSummary(NamedTuple):
    """How a regenerated document differs from the file on disk (if at all)."""

    lines: Tuple[str, ...]
    chapters_changed: bool
    stamp_changed: bool

    @property
    def changed(self) -> bool:
        return self.chapters_changed or self.stamp_changed


# --------------------------------------------------------------------------------------
# titles
# --------------------------------------------------------------------------------------

def normalize_title(raw: str) -> str:
    """Strip Minecraft ``&`` formatting codes; keep escaped ``\\&`` ampersands.

    ``&aChapter 2&r: &6The ATM Star`` becomes ``Chapter 2: The ATM Star``; the pack
    escapes a literal ampersand as ``\\&`` (``Extended \\& Advanced AE``), which is not
    a formatting code and is left untouched. Surrounding whitespace added by code
    removal is trimmed; the book's own inner spacing is preserved.
    """
    return _FORMAT_CODE_RE.sub("", raw).strip()


# --------------------------------------------------------------------------------------
# reading the checkout
# --------------------------------------------------------------------------------------

def find_checkout(path_arg: str) -> CheckoutLayout:
    """Validate that ``path_arg`` is an AllTheMods/ATM-10 checkout; return its layout.

    Every failure is one message telling the user exactly what is missing; a directory
    that merely exists is not mistaken for the pack.
    """
    root = Path(path_arg).expanduser()
    if not root.exists():
        raise BuildError(
            f"no such path: {path_arg}\n"
            f"pass the directory of a local AllTheMods/ATM-10 checkout; {CLONE_HINT}"
        )
    if not root.is_dir():
        raise BuildError(f"not a directory: {path_arg}\npass the ATM-10 checkout directory")

    def under(relative: Path) -> Path:
        return root / relative

    problems: "list[str]" = []
    chapters_dir = under(CHAPTERS_REL)
    if not (root / "config").is_dir():
        problems.append("there is no config/ directory at all")
    if not chapters_dir.is_dir():
        problems.append(f"missing {CHAPTERS_REL.as_posix()}/ (the FTB Quests chapter files)")
    elif not any(chapters_dir.glob("*.snbt")):
        problems.append(f"{CHAPTERS_REL.as_posix()}/ holds no .snbt chapter files")
    for relative in (CHAPTER_GROUPS_REL, LANG_CHAPTER_REL, LANG_GROUP_REL, BCC_REL):
        if not under(relative).is_file():
            problems.append(f"missing {relative.as_posix()}")
    if problems:
        listing = "\n".join(f"  - {problem}" for problem in problems)
        raise BuildError(
            f"{path_arg} does not look like an AllTheMods/ATM-10 checkout:\n{listing}\n"
            f"expected the pack repository (github.com/AllTheMods/ATM-10); {CLONE_HINT}"
        )
    return CheckoutLayout(
        root=root,
        chapters_dir=chapters_dir,
        chapter_groups=under(CHAPTER_GROUPS_REL),
        lang_chapter=under(LANG_CHAPTER_REL),
        lang_group=under(LANG_GROUP_REL),
        bcc_config=under(BCC_REL),
    )


def read_snbt(path: Path) -> Any:
    """Parse one SNBT config file; wrap every failure with the file's name."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise BuildError(f"cannot read {path}: {exc}") from exc
    try:
        return snbt.parse(text)
    except snbt.SnbtError as exc:
        raise BuildError(f"cannot parse the SNBT in {path}: {exc}") from exc


def expect_mapping(data: Any, path: Path) -> "dict[str, Any]":
    if not isinstance(data, dict):
        raise BuildError(f"{path}: expected a top-level compound '{{...}}'")
    return data


def expect_str(mapping: "dict[str, Any]", key: str, path: Path) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise BuildError(f"{path}: key {key!r} must be a non-empty string")
    return value


def expect_int(value: Any, key: str, path: Path, default: "Optional[int]" = None) -> int:
    if value is None and default is not None:
        return default
    if isinstance(value, bool) or not isinstance(value, int):
        raise BuildError(f"{path}: key {key!r} must be an integer (got {value!r})")
    return value


def load_group_order(layout: CheckoutLayout) -> "tuple[list[str], dict[str, str]]":
    """Return the ordered FTB group hex ids and a hex id -> display-title mapping."""
    path = layout.chapter_groups
    data = expect_mapping(read_snbt(path), path)
    entries = data.get("chapter_groups")
    if not isinstance(entries, list) or not entries:
        raise BuildError(f"{path}: expected a non-empty 'chapter_groups' array")
    order: "list[str]" = []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise BuildError(f"{path}: chapter_groups[{index}] must be a compound")
        group_id = expect_str(entry, "id", path)
        if group_id in order:
            raise BuildError(f"{path}: duplicate chapter group id {group_id!r}")
        order.append(group_id)

    lang_path = layout.lang_group
    lang = expect_mapping(read_snbt(lang_path), lang_path)
    titles: "dict[str, str]" = {}
    for group_id in order:
        key = f"chapter_group.{group_id}.title"
        raw = lang.get(key)
        if not isinstance(raw, str) or not raw.strip():
            raise BuildError(
                f"{lang_path}: no title for chapter group id {group_id!r} (key {key!r}); "
                f"is this really an ATM-10 en_us lang file?"
            )
        titles[group_id] = normalize_title(raw)
    return order, titles


def load_chapters(
    layout: CheckoutLayout, known_group_ids: "Sequence[str]"
) -> "list[RawChapter]":
    """Read every chapter SNBT: id, title, group, order, and quest count."""
    lang_path = layout.lang_chapter
    lang = expect_mapping(read_snbt(lang_path), lang_path)
    chapter_paths = sorted(layout.chapters_dir.glob("*.snbt"))
    if not chapter_paths:
        raise BuildError(f"{layout.chapters_dir}: no .snbt chapter files found")

    chapters: "list[RawChapter]" = []
    for path in chapter_paths:
        data = expect_mapping(read_snbt(path), path)
        identifier = data.get("filename")
        if not isinstance(identifier, str) or not identifier.strip():
            identifier = path.stem  # FTB always writes it; a hand-rolled file may not
        else:
            identifier = identifier.strip()

        title: "Optional[str]" = None
        ftb_id = data.get("id")
        if isinstance(ftb_id, str) and ftb_id.strip():
            raw = lang.get(f"chapter.{ftb_id}.title")
            if isinstance(raw, str) and raw.strip():
                title = normalize_title(raw)
        if title is None:  # older FTB Quests keeps the title inside the chapter file
            raw = data.get("title")
            if isinstance(raw, str) and raw.strip():
                title = normalize_title(raw)
        if title is None:
            raise BuildError(
                f"{path}: no title found for chapter {identifier!r} - looked for "
                f"'chapter.{ftb_id}.title' in {lang_path} and a 'title' key in the chapter file"
            )

        group_id = data.get("group", "")
        if not isinstance(group_id, str):
            raise BuildError(f"{path}: key 'group' must be a string")
        group_id = group_id.strip()
        if group_id and group_id not in known_group_ids:
            raise BuildError(
                f"{path}: chapter {identifier!r} is in group id {group_id!r}, which is not "
                f"listed in {layout.chapter_groups} (a removed group? re-check the checkout)"
            )
        order_index = expect_int(data.get("order_index"), "order_index", path, default=0)
        quests_raw = data.get("quests")
        quests = len(quests_raw) if isinstance(quests_raw, list) else 0
        chapters.append(RawChapter(identifier, title, group_id, order_index, quests))

    identifiers = [chapter.identifier for chapter in chapters]
    duplicates = sorted({c for c in identifiers if identifiers.count(c) > 1})
    if duplicates:
        raise BuildError(
            f"{layout.chapters_dir}: duplicate chapter id(s) {', '.join(duplicates)}; "
            f"chapter filenames must be unique"
        )
    return chapters


def detect_pack_version(layout: CheckoutLayout) -> "tuple[str, str]":
    """Return ``(modpackName, modpackVersion)`` from the pack's bcc config.

    bcc-common.toml is a flat key/value file; read the two keys with a line scan rather
    than a TOML dependency so the tool stays stdlib-only on every Python it supports.
    """
    path = layout.bcc_config
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise BuildError(f"cannot read {path}: {exc}") from exc
    values: "dict[str, str]" = {}
    for key in ("modpackName", "modpackVersion"):
        match = re.search(
            rf"^\s*{key}\s*=\s*\"([^\"]*)\"", text, flags=re.MULTILINE
        )
        if match:
            values[key] = match.group(1).strip()
    name = values.get("modpackName", "")
    if name and "all the mods" not in name.lower():
        raise BuildError(
            f"{path} names modpackName {name!r} - this tool only rebuilds from "
            f"AllTheMods/ATM-10 checkouts"
        )
    version = values.get("modpackVersion", "")
    if not _VALID_VERSION_RE.match(version):
        raise BuildError(
            f"{path}: cannot stamp the chapter list - modpackVersion is "
            f"{version or '<missing>'!r}, expected something like \"8.2\""
        )
    return name or "All the Mods 10", version


def pack_stamp(version: str) -> str:
    """The stamp the skill ships for ``version``: the major line, e.g. ``8.2`` -> ``8.x``.

    The skill tracks the chapter list per major pack line (the list barely moves inside
    one); the exact version the list was built from goes into pack_version_source.
    """
    return version.split(".", 1)[0] + ".x"


# --------------------------------------------------------------------------------------
# building the document
# --------------------------------------------------------------------------------------

def order_chapters(
    chapters: "Sequence[RawChapter]",
    group_order: "Sequence[str]",
    group_titles: "Dict[str, str]",
) -> "list[dict[str, Any]]":
    """Lay chapters out the way the quest book shows them: standalone files first,
    then the groups in chapter_groups.snbt order, each group by order_index."""
    unknown = sorted(
        {chapter.identifier for chapter in chapters} - set(STAGE_ASSIGNMENTS)
    )
    if unknown:
        by_id = {chapter.identifier: chapter for chapter in chapters}
        lines = [
            f"  - {identifier} (group: "
            f"{group_titles.get(by_id[identifier].group_id, 'standalone')})"
            for identifier in unknown
        ]
        raise BuildError(
            f"{len(unknown)} chapter(s) are not in the stage table "
            f"(STAGE_ASSIGNMENTS in scripts/build_chapter_list.py):\n"
            + "\n".join(lines)
            + "\nthe stage model is the skill's own (references/progression.md): place each "
            "new chapter in early-game, tech, magic, or endgame there, then re-run"
        )

    def sort_key(chapter: RawChapter) -> "tuple[int, str]":
        return (chapter.order_index, chapter.identifier)

    ordered: "list[dict[str, Any]]" = []
    standalone = sorted(
        (chapter for chapter in chapters if not chapter.group_id), key=sort_key
    )
    grouped: "list[RawChapter]" = []
    for group_id in group_order:
        members = sorted(
            (chapter for chapter in chapters if chapter.group_id == group_id),
            key=sort_key,
        )
        grouped.extend(members)

    def record(chapter: RawChapter, group_title: str) -> "dict[str, Any]":
        return {
            "id": chapter.identifier,
            "title": chapter.title,
            "group": group_title,
            "stage": STAGE_ASSIGNMENTS[chapter.identifier],
            "status": "pending",
        }

    ordered.extend(record(chapter, "") for chapter in standalone)
    ordered.extend(
        record(chapter, group_titles[chapter.group_id]) for chapter in grouped
    )
    return ordered


def build_source_line(
    name: str,
    version: str,
    commit: "Optional[str]",
    date: str,
    chapter_count: int,
    quest_count: int,
) -> str:
    """The provenance sentence stored in pack_version_source."""
    where = f"commit {commit}" if commit else "a local checkout"
    return (
        f"Chapter list rebuilt offline from the official {name} quest config "
        f"(AllTheMods/ATM-10, config/ftbquests/quests: chapter files, "
        f"chapter_groups.snbt, and the en_us lang titles) at pack {version}, {where}, "
        f"{date} - {chapter_count} chapters, {quest_count} quests. The in-game quest "
        f"book is authoritative; re-research this list when the pack moves on."
    )


def build_document(
    chapters: "Sequence[dict[str, Any]]",
    stamp: str,
    source: str,
) -> "dict[str, Any]":
    return {
        "pack_version": stamp,
        "pack_version_source": source,
        "chapters": [
            {field: chapter[field] for field in CHAPTER_FIELD_ORDER}
            for chapter in chapters
        ],
    }


# --------------------------------------------------------------------------------------
# comparing against what is on disk
# --------------------------------------------------------------------------------------

def signature(document: "dict[str, Any]") -> "tuple[Any, ...]":
    """The semantic content of a chapter-list document: stamp + ordered chapter fields.

    ``pack_version_source`` is deliberately excluded: it carries the build date/commit,
    so a same-day content-identical rebuild must not report a difference for it.
    """
    if not isinstance(document, dict):
        return (None,)
    chapters = document.get("chapters")
    rows = tuple(
        tuple(str(chapter.get(field, "")) for field in CHAPTER_FIELD_ORDER)
        for chapter in chapters
    ) if isinstance(chapters, list) and all(isinstance(c, dict) for c in chapters) else ()
    return (document.get("pack_version"), rows)


def diff_documents(
    old: "Optional[dict[str, Any]]", new: "dict[str, Any]", existed: bool = False
) -> DiffSummary:
    """Describe what replacing ``old`` with ``new`` would change, in review terms."""
    if old is None:
        line = (
            "the file does not exist yet - it will be created" if not existed
            else "the file exists but is not a usable chapter-list document - it will be overwritten"
        )
        return DiffSummary((line,), True, True)

    lines: "list[str]" = []
    old_stamp = old.get("pack_version") if isinstance(old, dict) else None
    new_stamp = new.get("pack_version")
    stamp_changed = old_stamp != new_stamp
    if stamp_changed:
        lines.append(f"pack_version: {old_stamp!r} -> {new_stamp!r}")

    old_rows = (
        {row[0]: row for row in signature(old)[1]}
    )
    new_rows = (
        {row[0]: row for row in signature(new)[1]}
    )
    added = [row[0] for row in signature(new)[1] if row[0] not in old_rows]
    removed = [row[0] for row in signature(old)[1] if row[0] not in new_rows]
    if added:
        lines.append(f"new chapters: {', '.join(added)}")
    if removed:
        lines.append(f"removed chapters: {', '.join(removed)}")
    changed_fields: "list[str]" = []
    for identifier, new_row in new_rows.items():
        old_row = old_rows.get(identifier)
        if old_row is None:
            continue
        for index, field in enumerate(CHAPTER_FIELD_ORDER):
            if field == "status":
                continue  # regeneration always ships all-pending; ignore statuses
            if old_row[index] != new_row[index]:
                changed_fields.append(
                    f"{identifier}: {field} {old_row[index]!r} -> {new_row[index]!r}"
                )
    lines.extend(changed_fields)
    old_order = [row[0] for row in signature(old)[1] if row[0] in new_rows]
    new_order = [row[0] for row in signature(new)[1] if row[0] in old_rows]
    order_changed = old_order != new_order
    if order_changed:
        lines.append("quest-book order changed")
    chapters_changed = bool(added or removed or changed_fields or order_changed)

    if not lines:
        old_source = old.get("pack_version_source") if isinstance(old, dict) else None
        if old_source != new.get("pack_version_source"):
            lines.append(
                "only pack_version_source differs (the rebuild stamps today's provenance; "
                "chapter content and pack stamp are identical)"
            )
        else:
            lines.append("no differences")
    return DiffSummary(tuple(lines), chapters_changed, stamp_changed)


def load_existing(path: Path) -> "tuple[bool, Optional[dict[str, Any]]]":
    """``(existed, document)`` for the current output file.

    ``document`` is None when the file is absent, unreadable, or not a JSON object;
    ``existed`` keeps a genuinely missing file distinguishable from a broken one.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False, None
    except (OSError, ValueError):
        return True, None
    return True, data if isinstance(data, dict) else None


# --------------------------------------------------------------------------------------
# writing
# --------------------------------------------------------------------------------------

def write_document(path: Path, document: "dict[str, Any]") -> None:
    """Write the document atomically (temp file in the same directory, then replace)."""
    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    directory = path.parent if str(path.parent) else Path(".")
    handle = None
    temporary: "Optional[Path]" = None
    try:
        directory.mkdir(parents=True, exist_ok=True)
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
        raise BuildError(f"cannot write {path}: {exc}") from exc
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
        prog="build_chapter_list.py",
        description="Rebuild examples/progress.example.json from a local AllTheMods/ATM-10 "
                    "checkout (offline; the checkout is read, never written).",
    )
    parser.add_argument(
        "checkout",
        help="path to a local clone of github.com/AllTheMods/ATM-10",
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUT),
        help=f"chapter list to write (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="write nothing; exit 0 when the output file is already up to date, "
             "1 (with a summary) when it would change",
    )
    parser.add_argument(
        "--commit", default=None, metavar="REV",
        help="pack commit/tag the checkout sits at; recorded in pack_version_source",
    )
    parser.add_argument(
        "--date", default=None, metavar="YYYY-MM-DD",
        help="provenance date for pack_version_source (default: today)",
    )
    return parser.parse_args(argv)


def _parse_date(value: "Optional[str]") -> str:
    if value is None:
        return datetime.date.today().isoformat()
    if not _DATE_RE.match(value):
        raise BuildError(f"--date must be YYYY-MM-DD (got {value!r})")
    try:
        datetime.date(*map(int, value.split("-")))
    except ValueError:
        raise BuildError(f"--date {value!r} is not a real calendar date")
    return value


def rebuild(layout: CheckoutLayout, commit: "Optional[str]", date: str) -> "dict[str, Any]":
    """The full pipeline: checkout -> chapter-list document."""
    group_order, group_titles = load_group_order(layout)
    chapters = load_chapters(layout, group_order)
    name, version = detect_pack_version(layout)
    ordered = order_chapters(chapters, group_order, group_titles)
    quest_count = sum(chapter.quests for chapter in chapters)
    source = build_source_line(name, version, commit, date, len(ordered), quest_count)
    return build_document(ordered, pack_stamp(version), source)


def chapter_total(document: "dict[str, Any]") -> int:
    chapters = document.get("chapters")
    return len(chapters) if isinstance(chapters, list) else 0


def main(argv: "Optional[Sequence[str]]" = None) -> int:
    try:
        try:
            args = parse_args(argv)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1

        if "\x00" in args.checkout or "\x00" in args.out:
            raise BuildError("paths cannot contain a null character")
        date = _parse_date(args.date)
        layout = find_checkout(args.checkout)
        document = rebuild(layout, args.commit, date)
        out_path = Path(args.out).expanduser()

        existed, existing = load_existing(out_path)
        differences = diff_documents(existing, document, existed=existed)
        _, exact_version = detect_pack_version(layout)

        if args.check:
            if differences.changed:
                print(f"check failed: {out_path} would change "
                      f"(checkout is pack {exact_version}):")
                for line in differences.lines:
                    print(f"  - {line}")
                print("run without --check to write the rebuilt list, then review with git diff")
                return 1
            print(f"check ok: {out_path} is up to date with the checkout "
                  f"(pack {exact_version}, {chapter_total(document)} chapters)")
            for line in differences.lines:
                if line != "no differences":
                    print(f"  note: {line}")
            return 0

        if existing is not None and not differences.changed:
            print(f"unchanged: {out_path} already matches the checkout "
                  f"(pack {exact_version}, {chapter_total(document)} chapters); "
                  f"nothing written")
            return 0

        for line in differences.lines:
            print(f"  change: {line}")
        write_document(out_path, document)
        print(f"wrote {out_path}: {chapter_total(document)} chapters, pack {exact_version} "
              f"(stamp {document['pack_version']})")
        print("next: review with  git diff -- examples/progress.example.json")
        print("then reconcile the private progress file:")
        print("  python3 scripts/progress.py --sync          # preview")
        print("  python3 scripts/progress.py --sync --yes    # apply after reviewing")
        return 0
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # never let an odd input escape as a traceback
        detail = str(exc).strip() or exc.__class__.__name__
        print(f"error: cannot rebuild the chapter list: {detail}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
