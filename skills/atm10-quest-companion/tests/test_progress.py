#!/usr/bin/env python3
"""Offline tests for the atm10-quest-companion skill.

Stdlib-only and network-free: the skill's script reads one local JSON file, so every
case here is a temp file, a fixed chapter list, or a pure function call.

Covered:

  * the frontmatter identity (``name`` matches the directory) and the documented
    research-grounding rule (in-game quest book + JEI authoritative, uncertain details
    flagged as approximate, nothing invented);
  * the shipped example file: it exists, validates against the schema, carries the
    pack-version stamp, every chapter is pending, ids are unique, and the quest-book order
    is preserved (standalone chapters first, then the pack's groups in order, contiguous
    within each group);
  * ``scripts/progress.py``: a missing, empty, malformed, or schema-breaking progress
    file is reported as one clear message with exit status 1, never a traceback;
  * completion math against fixed inputs (per stage and overall, one-decimal rounding,
    empty-stage and all-done edges) and next-chapter ordering (file order across stages,
    ``--next`` cap, done chapters skipped, ``--stage`` filter);
  * ``--set``: validation before write, id *and* title resolution, an unknown id rejected
    with the closest candidates and the file left byte-for-byte untouched, all-or-nothing
    across repeated flags, a no-op that does not rewrite, stamp and order preservation,
    atomic replacement that leaves no temporary file behind, and a refused write when the
    document would break the schema;
  * the pack-version stamp and the drift check: the known list is loaded from the shipped
    example, unknown/missing chapter ids and a differing or absent stamp produce warnings
    on stdout with exit status 0, and a clean file produces no drift section at all;
  * the three endgame reference docs: they exist, are grounded in the named pack
    repository files, carry the same grounding rules as SKILL.md, and list the verified
    Chapter 3 components, the boss lines, and Chapter 4's post-star quests — the multiblock
    automation line, the five star parts, and the eleven creative-tier items behind
    *Fully Automated ATM Star*;
  * the resource-farming guide: it exists, is grounded the same way and at the same pinned
    commit, maps allthemodium / vibranium / unobtainium (plus the smithing templates, the
    Piglich Heart, the three alloy chains, and the farm systems the book points at) to the
    pack's verified quest titles, keeps its hedges and its *(no title in the config)*
    markings, and states no coordinate, ore level, or recipe of its own;
  * offline guarantee: the script imports no network module;
  * privacy: ``.gitignore`` excludes ``data/`` so real progress cannot be committed.
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
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = SKILL_ROOT.name
SKILL_MD = SKILL_ROOT / "SKILL.md"
GITIGNORE = SKILL_ROOT / ".gitignore"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"
PROGRESSION_MD = SKILL_ROOT / "references" / "progression.md"
KEY_MODS_MD = SKILL_ROOT / "references" / "key-mods.md"
GETTING_STARTED_MD = SKILL_ROOT / "references" / "getting-started.md"
STAR_CHECKLIST_MD = SKILL_ROOT / "references" / "atm-star-checklist.md"
BOSS_CHECKLIST_MD = SKILL_ROOT / "references" / "boss-checklist.md"
CREATIVE_CHECKLIST_MD = SKILL_ROOT / "references" / "creative-checklist.md"
RESOURCE_GUIDE_MD = SKILL_ROOT / "references" / "resource-farming-guide.md"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "progress.py"

_spec = importlib.util.spec_from_file_location("progress", SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
progress = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(progress)

# The quest-book group sequence, from the pack's chapter_groups.snbt (standalone
# chapters, group "", render outside the groups and come first in the example file).
EXPECTED_GROUP_SEQUENCE = (
    "",
    "Main Questline",
    "Tools and Gear",
    "Storage",
    "Logistics",
    "Resources",
    "Tech",
    "Modern Industrialization",
    "Power",
    "Magic",
    "Exploration",
)


def make_chapter(**changes: Any) -> "dict[str, Any]":
    """A valid chapter record; tests override only the field each case is about."""
    chapter: "dict[str, Any]" = {
        "id": "welcome",
        "title": "Welcome",
        "group": "",
        "stage": "early-game",
        "status": "pending",
    }
    chapter.update(changes)
    return chapter


def document(chapters: "list[dict[str, Any]]") -> "dict[str, Any]":
    return {"chapters": chapters}


def run_main(argv: "list[str]") -> "tuple[int, str, str]":
    """Call the script's main() in-process; return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = progress.main(argv)
    return code, out.getvalue(), err.getvalue()


class TempFileTestCase(unittest.TestCase):
    """Base class giving each test its own throwaway data file."""

    def setUp(self) -> None:
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary_directory.cleanup)
        self.data_path = Path(self._temporary_directory.name) / "progress.json"

    def write_data(self, payload: Any, raw: "str | None" = None) -> Path:
        text = raw if raw is not None else json.dumps(payload, indent=2)
        self.data_path.write_text(text, encoding="utf-8")
        return self.data_path


# --------------------------------------------------------------------------------------
# SKILL.md and the skill's identity
# --------------------------------------------------------------------------------------

class TestSkillDocs(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SKILL_MD.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", cls.text, re.DOTALL)
        assert match is not None, "SKILL.md must start with a frontmatter block"
        cls.frontmatter = match.group(1)

    def test_skill_md_exists(self) -> None:
        self.assertTrue(SKILL_MD.is_file(), f"missing {SKILL_MD}")

    def test_frontmatter_name_matches_directory(self) -> None:
        match = re.search(r"^name:\s*(\S+)\s*$", self.frontmatter, re.MULTILINE)
        self.assertIsNotNone(match, "frontmatter has no `name` key")
        assert match is not None
        self.assertEqual(match.group(1), SKILL_NAME)
        self.assertEqual(SKILL_NAME, "atm10-quest-companion")

    def test_frontmatter_required_keys(self) -> None:
        for key, pattern in (
            ("description", r"^description:\s*\S+"),
            ("version", r"^version:\s*\d+\.\d+\.\d+\s*$"),
            ("license", r"^license:\s*\S+"),
            ("platforms", r"^platforms:\s*\[linux, macos, windows\]\s*$"),
            ("category", r"^\s+category:\s*gaming\s*$"),
        ):
            self.assertRegex(self.frontmatter, re.compile(pattern, re.MULTILINE),
                             f"frontmatter is missing or malformed: {key}")

    def test_research_grounding_rule_is_documented(self) -> None:
        """SKILL.md must state the grounding rule the whole skill is built on."""
        lowered = self.text.lower()
        self.assertIn("in-game quest book", lowered,
                      "SKILL.md must name the in-game quest book as a source")
        self.assertIn("jei", lowered, "SKILL.md must name JEI alongside the quest book")
        self.assertIn("authoritative", lowered,
                      "SKILL.md must say the quest book and JEI are authoritative")
        self.assertIn("never invent", lowered,
                      "SKILL.md must forbid inventing quest requirements, ids, or recipes")
        self.assertIn("approximate", lowered,
                      "SKILL.md must require flagging uncertain details as approximate")
        # The rule must cover all three invented-detail classes explicitly.
        grounding = re.search(
            r"never invent quest requirements, item ids, counts, or recipes", lowered
        )
        self.assertIsNotNone(
            grounding,
            "SKILL.md must forbid inventing quest requirements, item ids, and recipes",
        )

    def test_privacy_and_setup_documented(self) -> None:
        lowered = self.text.lower()
        self.assertIn("data/progress.json", lowered)
        self.assertIn("gitignore", lowered)
        self.assertIn("examples/progress.example.json", lowered)
        # Windows is a declared platform: commands appear for both shells.
        self.assertIn("python3 scripts/progress.py", self.text)
        self.assertIn("python scripts/progress.py", self.text)

    def test_reference_docs_exist_and_cover_the_stages(self) -> None:
        for path in (PROGRESSION_MD, KEY_MODS_MD, GETTING_STARTED_MD, STAR_CHECKLIST_MD,
                     BOSS_CHECKLIST_MD, CREATIVE_CHECKLIST_MD, RESOURCE_GUIDE_MD):
            self.assertTrue(path.is_file(), f"missing reference doc: {path}")
            self.assertGreater(len(path.read_text(encoding="utf-8").strip()), 400,
                               f"{path.name} looks like a stub")
        progression = PROGRESSION_MD.read_text(encoding="utf-8").lower()
        for stage in ("early game", "tech", "magic", "endgame"):
            self.assertIn(stage, progression,
                          f"progression.md must document the {stage} stage")
        self.assertIn("quest book", progression)
        self.assertIn("jei", progression)
        self.assertIn("approximate", progression)
        # progression.md is the orientation doc; the endgame detail lives in the three
        # endgame docs and the material map in the resource guide, and it must point at them.
        for link in ("atm-star-checklist.md", "boss-checklist.md", "creative-checklist.md",
                     "resource-farming-guide.md"):
            self.assertIn(link, progression, f"progression.md must link {link}")
        self.assertIn("128 quests", progression,
                      "the star chapter's verified quest count (pack 8.2) is 128, not ~160")

    def test_gitignore_excludes_data_directory(self) -> None:
        self.assertTrue(GITIGNORE.is_file(), "the skill must ship a .gitignore")
        lines = [line.strip() for line in GITIGNORE.read_text(encoding="utf-8").splitlines()]
        self.assertIn("data/", lines)


# --------------------------------------------------------------------------------------
# the shipped example file
# --------------------------------------------------------------------------------------

class TestExampleProgressFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = EXAMPLE_DATA.read_text(encoding="utf-8")
        cls.data = json.loads(cls.raw)
        cls.chapters = cls.data["chapters"]

    def test_example_exists_and_is_a_chapters_document(self) -> None:
        self.assertTrue(EXAMPLE_DATA.is_file(), f"missing {EXAMPLE_DATA}")
        self.assertIsInstance(self.data, dict)
        self.assertEqual(set(self.data), {"pack_version", "pack_version_source", "chapters"})
        self.assertIsInstance(self.chapters, list)

    def test_example_carries_the_pack_version_stamp(self) -> None:
        """The shipped list must say which ATM10 version it was researched from."""
        self.assertEqual(self.data["pack_version"], "8.x")
        self.assertTrue(progress.PACK_VERSION_RE.match(self.data["pack_version"]),
                        "the pack_version stamp must look like a pack version (8.x, 8.2, ...)")
        source = self.data["pack_version_source"]
        self.assertIsInstance(source, str)
        lowered = source.lower()
        # Provenance: the pack repository the chapter list was read from, and when.
        self.assertIn("allthemods/atm-10", lowered)
        self.assertIn("config/ftbquests", lowered)
        self.assertRegex(source, r"\b\d{4}-\d{2}-\d{2}\b")
        # The stamp is data, not a licence to invent: it defers to the game.
        self.assertIn("in-game quest book", lowered)

    def test_chapters_are_non_empty(self) -> None:
        self.assertGreater(len(self.chapters), 0)
        # The researched pack-8.x quest book has 66 chapters; guard against a truncated
        # regeneration while allowing the list to grow with the pack.
        self.assertGreaterEqual(len(self.chapters), 60)

    def test_example_validates_against_the_schema(self) -> None:
        self.assertEqual(progress.validate(self.data), [])

    def test_statuses_are_valid_and_all_pending(self) -> None:
        for chapter in self.chapters:
            self.assertIn(chapter["status"], progress.VALID_STATUSES)
        pending = [c for c in self.chapters if c["status"] == "pending"]
        self.assertEqual(len(pending), len(self.chapters),
                         "the shipped example must start with every chapter pending")

    def test_ids_are_unique_and_well_formed(self) -> None:
        ids = [chapter["id"] for chapter in self.chapters]
        self.assertEqual(len(ids), len(set(ids)), "chapter ids must be unique")
        for chapter in self.chapters:
            for field in ("id", "title", "stage"):
                self.assertIsInstance(chapter[field], str)
                self.assertTrue(chapter[field].strip(),
                                f"{field} must be non-empty in {chapter.get('id')}")
            self.assertIn(chapter["stage"], progress.STAGE_IDS)

    def test_main_questline_chapters_are_present_and_ordered(self) -> None:
        ids = [chapter["id"] for chapter in self.chapters]
        spine = ["mainquestline_part_1", "allthemodium", "chapter_2_the_star",
                 "achapter_2r_6the_atm_star"]
        for chapter_id in spine:
            self.assertIn(chapter_id, ids, f"main questline chapter missing: {chapter_id}")
        positions = [ids.index(chapter_id) for chapter_id in spine]
        self.assertEqual(positions, sorted(positions),
                         "the main questline must appear in quest-book order")
        self.assertEqual(ids[0], "welcome", "the Welcome chapter comes first")

    def test_quest_book_order_is_preserved(self) -> None:
        """Groups must appear contiguously, in the pack's chapter-group order."""
        sequence: "list[str]" = []
        for chapter in self.chapters:
            group = chapter.get("group", "")
            if not sequence or sequence[-1] != group:
                sequence.append(group)
        self.assertEqual(sequence, list(EXPECTED_GROUP_SEQUENCE),
                         "example chapters are not in quest-book group order")

    def test_stage_assignment_covers_every_chapter(self) -> None:
        counts = {stage_id: 0 for stage_id, _ in progress.STAGES}
        for chapter in self.chapters:
            counts[chapter["stage"]] += 1
        for stage_id, total in counts.items():
            self.assertGreater(total, 0, f"stage {stage_id} has no chapters")
        self.assertEqual(sum(counts.values()), len(self.chapters))

    def test_script_accepts_the_example_file(self) -> None:
        code, out, err = run_main(["--data", str(EXAMPLE_DATA)])
        self.assertEqual(code, 0, err)
        self.assertIn("overall: 0/66 chapters done (0.0%)", out)
        self.assertIn("next unfinished chapters", out)


# --------------------------------------------------------------------------------------
# progress.py: failure handling — clear messages, never a traceback
# --------------------------------------------------------------------------------------

class TestProgressFailureHandling(TempFileTestCase):

    def assert_clean_failure(self, code: int, out: str, err: str, *needles: str) -> None:
        self.assertEqual(code, 1, "a broken progress file must exit 1")
        combined = out + err
        self.assertNotIn("Traceback", combined)
        for needle in needles:
            self.assertIn(needle, combined.lower())

    def test_missing_file(self) -> None:
        missing = Path(self._temporary_directory.name) / "nope.json"
        code, out, err = run_main(["--data", str(missing)])
        self.assert_clean_failure(code, out, err, "no progress file",
                                  "examples/progress.example.json")

    def test_empty_file(self) -> None:
        self.write_data(None, raw="")
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "empty")

    def test_whitespace_only_file(self) -> None:
        self.write_data(None, raw="   \n\t\n")
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "empty")

    def test_malformed_json(self) -> None:
        self.write_data(None, raw='{"chapters": [ ,,, ]')
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "not valid json")

    def test_json_array_instead_of_object(self) -> None:
        self.write_data([])
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "json object")

    def test_missing_chapters_key(self) -> None:
        self.write_data({"progress": []})
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "missing key 'chapters'")

    def test_empty_chapters_list(self) -> None:
        self.write_data(document([]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "empty", "progress.example.json")

    def test_chapter_not_an_object(self) -> None:
        self.write_data(document(["welcome"]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "expected an object")

    def test_bad_status(self) -> None:
        self.write_data(document([make_chapter(status="finished")]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "status 'finished'", "pending", "done")

    def test_bad_stage(self) -> None:
        self.write_data(document([make_chapter(stage="midgame")]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "stage 'midgame'")

    def test_missing_required_field(self) -> None:
        broken = make_chapter()
        del broken["title"]
        self.write_data(document([broken]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "missing required field 'title'")

    def test_empty_id(self) -> None:
        self.write_data(document([make_chapter(id="  ")]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "'id' must be a non-empty string")

    def test_duplicate_ids(self) -> None:
        self.write_data(document([make_chapter(), make_chapter(title="Welcome again")]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "duplicate id")

    def test_unknown_fields(self) -> None:
        self.write_data(document([make_chapter(notes="played with friends")]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "unknown field", "notes")

    def test_unknown_top_level_key(self) -> None:
        payload = document([make_chapter()])
        payload["player"] = "steve"
        self.write_data(payload)
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "unknown top-level key", "player")

    def test_bad_group_type(self) -> None:
        self.write_data(document([make_chapter(group=7)]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assert_clean_failure(code, out, err, "'group' must be a string")

    def test_next_limit_below_one(self) -> None:
        self.write_data(document([make_chapter()]))
        code, out, err = run_main(["--data", str(self.data_path), "--next", "0"])
        self.assert_clean_failure(code, out, err, "--next must be at least 1")

    def test_every_problem_is_reported_not_just_the_first(self) -> None:
        self.write_data(document([
            make_chapter(id="a", status="nope"),
            make_chapter(id="b", stage="late"),
        ]))
        code, out, err = run_main(["--data", str(self.data_path)])
        combined = (out + err).lower()
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("status 'nope'", combined)
        self.assertIn("stage 'late'", combined)


# --------------------------------------------------------------------------------------
# progress.py: completion math and ordering on fixed inputs
# --------------------------------------------------------------------------------------

class TestCompletionMath(unittest.TestCase):

    def fixed_chapters(self) -> "list[dict[str, Any]]":
        """Four stages, eight chapters, three done: math is checked against this."""
        return [
            make_chapter(id="welcome", stage="early-game", status="done"),
            make_chapter(id="mainquestline_part_1", title="Chapter 1: The Beginning",
                         group="Main Questline", stage="early-game", status="done"),
            make_chapter(id="mekanism", title="Mekanism", group="Tech",
                         stage="tech", status="done"),
            make_chapter(id="create", title="Create", group="Tech", stage="tech"),
            make_chapter(id="applied_energistics_2", title="Applied Energistics 2",
                         group="Storage", stage="tech"),
            make_chapter(id="ars_nouveau", title="Ars Nouveau", group="Magic",
                         stage="magic"),
            make_chapter(id="allthemodium", title="Chapter 2: Allthemodium",
                         group="Main Questline", stage="endgame"),
            make_chapter(id="chapter_2_the_star", title="Chapter 3: The ATM Star",
                         group="Main Questline", stage="endgame"),
        ]

    def test_percentage_rounding(self) -> None:
        self.assertEqual(progress.percentage(1, 3), 33.3)
        self.assertEqual(progress.percentage(2, 3), 66.7)
        self.assertEqual(progress.percentage(0, 5), 0.0)
        self.assertEqual(progress.percentage(5, 5), 100.0)
        self.assertEqual(progress.percentage(0, 0), 0.0)

    def test_overall_summary(self) -> None:
        summary = progress.overall_summary(self.fixed_chapters())
        self.assertEqual(summary, {"total": 8, "done": 3, "percent": 37.5})

    def test_stage_summary_counts_and_order(self) -> None:
        summary = progress.stage_summary(self.fixed_chapters())
        self.assertEqual([row["id"] for row in summary],
                         ["early-game", "tech", "magic", "endgame"],
                         "stages must report in progression order")
        by_id = {row["id"]: row for row in summary}
        self.assertEqual((by_id["early-game"]["done"], by_id["early-game"]["total"]), (2, 2))
        self.assertEqual(by_id["early-game"]["percent"], 100.0)
        self.assertEqual((by_id["tech"]["done"], by_id["tech"]["total"]), (1, 3))
        self.assertEqual(by_id["tech"]["percent"], 33.3)
        self.assertEqual((by_id["magic"]["done"], by_id["magic"]["total"]), (0, 1))
        self.assertEqual((by_id["endgame"]["done"], by_id["endgame"]["total"]), (0, 2))

    def test_stage_summary_keeps_empty_stages_visible(self) -> None:
        chapters = [make_chapter(id="welcome", stage="early-game", status="done")]
        summary = progress.stage_summary(chapters)
        self.assertEqual(len(summary), len(progress.STAGES))
        by_id = {row["id"]: row for row in summary}
        self.assertEqual(by_id["magic"], {"id": "magic", "title": "Magic",
                                          "total": 0, "done": 0, "percent": 0.0})

    def test_report_shows_math_and_stage_order(self) -> None:
        report = progress.format_report(self.fixed_chapters(), Path("x.json"), limit=10)
        self.assertIn("overall: 3/8 chapters done (37.5%)", report)
        self.assertIn("100.0%", report)
        self.assertIn("33.3%", report)
        stage_positions = [report.index(stage_id) for stage_id, _ in progress.STAGES]
        self.assertEqual(stage_positions, sorted(stage_positions),
                         "the report must list stages in progression order")


class TestNextChapterOrdering(TempFileTestCase):

    def test_next_pending_preserves_file_order_across_stages(self) -> None:
        chapters = [
            make_chapter(id="a", stage="early-game", status="done"),
            make_chapter(id="b", stage="endgame"),           # pending, later stage, still listed
            make_chapter(id="c", stage="early-game"),        # pending, early stage, first
            make_chapter(id="d", stage="tech", status="done"),
            make_chapter(id="e", stage="magic"),
        ]
        result = progress.next_pending(chapters, limit=10)
        self.assertEqual([chapter["id"] for chapter in result], ["b", "c", "e"],
                         "pending chapters must keep quest-book (file) order")

    def test_next_pending_respects_limit(self) -> None:
        chapters = [make_chapter(id=f"ch{i}") for i in range(5)]
        self.assertEqual(len(progress.next_pending(chapters, limit=3)), 3)
        self.assertEqual([c["id"] for c in progress.next_pending(chapters, limit=2)],
                         ["ch0", "ch1"])

    def test_pending_count_and_all_done(self) -> None:
        chapters = [make_chapter(id="a"), make_chapter(id="b", status="done")]
        self.assertEqual(progress.pending_count(chapters), 1)
        done = [make_chapter(id="a", status="done"), make_chapter(id="b", status="done")]
        self.assertEqual(progress.pending_count(done), 0)
        report = progress.format_report(done, Path("x.json"), limit=5)
        self.assertIn("100.0%", report)
        self.assertIn("all chapters done", report)
        self.assertNotIn("next unfinished chapters", report)

    def test_report_next_section_is_capped_and_counts_remainder(self) -> None:
        chapters = [make_chapter(id=f"ch{i}") for i in range(6)]
        chapters[0]["status"] = "done"
        report = progress.format_report(chapters, Path("x.json"), limit=2)
        self.assertIn("showing 2 of 5", report)
        self.assertIn("ch1", report)
        self.assertIn("ch2", report)
        self.assertNotIn("ch3", report)
        self.assertIn("quest book", report.lower(),
                      "the report must defer specifics to the in-game quest book")

    def test_end_to_end_ordering_via_main(self) -> None:
        chapters = [
            make_chapter(id="welcome", stage="early-game", status="done"),
            make_chapter(id="mekanism", title="Mekanism", group="Tech", stage="tech"),
            make_chapter(id="ars_nouveau", title="Ars Nouveau", group="Magic",
                         stage="magic"),
            make_chapter(id="allthemodium", title="Chapter 2: Allthemodium",
                         group="Main Questline", stage="endgame"),
        ]
        self.write_data(document(chapters))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assertEqual(code, 0, err)
        self.assertIn("overall: 1/4 chapters done (25.0%)", out)
        listed = [line for line in out.splitlines() if "] " in line and ". [" in line]
        self.assertEqual(len(listed), 3)
        self.assertIn("mekanism", listed[0])
        self.assertIn("ars_nouveau", listed[1])
        self.assertIn("allthemodium", listed[2])

    def test_valid_file_exits_zero_with_report_on_stdout(self) -> None:
        self.write_data(document([make_chapter()]))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("atm10 quest companion", out)
        self.assertIn("early-game", out)


class TestSchemaValidator(unittest.TestCase):
    """validate() as a pure function: exactly the problems, nothing invented."""

    def test_valid_document_has_no_problems(self) -> None:
        self.assertEqual(progress.validate(document([make_chapter()])), [])

    def test_group_field_is_optional(self) -> None:
        chapter = make_chapter()
        del chapter["group"]
        self.assertEqual(progress.validate(document([chapter])), [])

    def test_example_file_round_trips_through_the_validator(self) -> None:
        data = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        self.assertEqual(progress.validate(data), [])
        self.assertEqual(progress.validate(copy.deepcopy(data)), [])



# --------------------------------------------------------------------------------------
# verified pack data the endgame reference docs must reproduce
# --------------------------------------------------------------------------------------

# The 13 direct dependencies of the "ATM Star" quest in Chapter 3, as titled by the pack's
# own lang file (config/ftbquests/quests/lang/en_us/chapters/chapter_2_the_star.snbt).
STAR_COMPONENTS = (
    "Runic Star Altar",
    "Pulsating Black Hole",
    "Nexium Emitter",
    "Patrick Star",
    "Dimensional Seed",
    "Wither's Compass",
    "Improbable Probability Device",
    "Philosopher's Fuel",
    "Dragon Soul",
    "Creative Essence",
    "Oblivion Shard",
    "The Star's Casing",
    "Awakened Unobtainium-Vibranium Alloy Block",
)

# Bosses whose names come from verified quest titles, kill-task entity ids, or the
# structure quests that name their arena.
VERIFIED_BOSSES = (
    "Wither", "Warden", "Ender Dragon",
    "Naga", "Lich", "Minoshroom", "Hydra", "Knight Phantom", "Ur-Ghast",
    "Alpha Yeti", "Snow Queen", "Questing Ram",
    "Slider", "Valkyrie Queen", "Sun Spirit",
    "Netherite Monstrosity", "Ignis", "Ender Guardian", "Harbinger", "Leviathan",
    "Ancient Remnant", "Maledictus", "Scylla",
    "Piglich", "Chaos Guardian", "Dead King", "Archevoker",
    "Lunar Monstrosity", "Starlight Golem", "Gatekeeper",
    "Forgotten Guardian", "Wilden Chimera",
)

# Pack-repository files both endgame docs must name as their source.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
)

# Chapter 4: Creative -- the 38 quests of achapter_2r_6the_atm_star, by the titles its
# en_us lang file gives them at the same pinned commit (e5e3d1d83e, pack 8.2). Two quests
# carry no title in the config; the page must mark those, never derive a name for them.
CREATIVE_CHAPTER_ID = "achapter_2r_6the_atm_star"
CREATIVE_COMMIT = "e5e3d1d83e"
CREATIVE_TITLED_QUESTS = (
    "Fully Automated ATM Star",
    "Runic Crucible",
    "Automatic Hepheastus Forge",
    "Runic Star Altar",
    "Runic Enchanter",
    "Energy Cell (Creative)",
    "Creative Energy Cube",
    "Creative Jetpack",
    "Creative Compressed Iron Blocks",
    "Creative Compressor",
    "Creative Spellbook",
    "Creative Source Jar",
    "Creative Energy Battery",
    "Creative Energy Cell",
    "Creative Locomotive",
    "Creative Blood Drop",
    "Patrick Star... Bee?",
    "Starry Bee!",
    "Star Shards",
    "Sea Prism",
    "Terrastomp Prism",
    "Whirlwind Prism",
    "Smelter Prism",
    "Soul Binding Crystal",
    "Top ATM Star part",
    "Right ATM Star part",
    "Left ATM Star part",
    "Bottom Left ATM Star part",
    "Bottom Right ATM Star part",
    "But why?",
    "Lens of Certain Death",
    "Lens of the Killer",
    "Infused Patrick Star",
    "Mundabitur Dust",
    "Corrupti Dust",
    "Arcane Crystals",
)  # 36 titled quests; the other two are the untitled ones the page marks

# The eleven creative-tier quests, in the order the config lists them; every one of them
# depends on Fully Automated ATM Star and nothing else.
CREATIVE_ITEMS = (
    "Energy Cell (Creative)",
    "Creative Energy Cube",
    "Creative Jetpack",
    "Creative Compressed Iron Blocks",
    "Creative Compressor",
    "Creative Spellbook",
    "Creative Source Jar",
    "Creative Energy Battery",
    "Creative Energy Cell",
    "Creative Locomotive",
    "Creative Blood Drop",
)

# Every task item id the chapter's config states -- the multiblock kits, the bee chain,
# the five KubeJS star parts, the prisms, the dusts, the lens chain, and the two generic
# ids whose exact variant lives in the quest entry (ironjetpacks:jetpack, evilcraft:blood).
CREATIVE_TASK_ITEMS = (
    "allthetweaks:atm_star",
    "allthetweaks:atm_star_shard",
    "allthetweaks:atm_star_block",
    "allthetweaks:patrick_star",
    "kubejs:atm_star_shard_1",
    "kubejs:atm_star_shard_2",
    "kubejs:atm_star_shard_3",
    "kubejs:atm_star_shard_4",
    "kubejs:atm_star_shard_5",
    "modern_industrialization:star_altar",
    "modern_industrialization:runic_crucible",
    "modern_industrialization:runic_enchanter",
    "modern_industrialization:auto_forge",
    "forbidden_arcanus:hephaestus_forge_tier_5",
    "forbidden_arcanus:quantum_injector",
    "forbidden_arcanus:rune_block",
    "forbidden_arcanus:arcane_crystal",
    "forbidden_arcanus:arcane_crystal_block",
    "forbidden_arcanus:arcane_crystal_obelisk",
    "forbidden_arcanus:arcane_polished_darkstone",
    "forbidden_arcanus:arcane_polished_darkstone_pillar",
    "forbidden_arcanus:chiseled_arcane_polished_darkstone",
    "forbidden_arcanus:gilded_chiseled_polished_darkstone",
    "forbidden_arcanus:darkstone_pedestal",
    "forbidden_arcanus:polished_darkstone",
    "forbidden_arcanus:polished_darkstone_slab",
    "forbidden_arcanus:polished_darkstone_stairs",
    "forbidden_arcanus:mundabitur_dust",
    "forbidden_arcanus:corrupti_dust",
    "forbidden_arcanus:soul_binding_crystal",
    "forbidden_arcanus:sea_prism",
    "forbidden_arcanus:terrastomp_prism",
    "forbidden_arcanus:whirlwind_prism",
    "forbidden_arcanus:smelter_prism",
    "actuallyadditions:atomic_reconstructor",
    "actuallyadditions:lens_of_certain_death",
    "actuallyadditions:lens_of_the_killer",
    "apothic_enchanting:infused_breath",
    "minecraft:enchanted_book",
    "minecraft:enchanting_table",
    "minecraft:soul_lantern",
    "minecraft:warm_ocean",
    "mekanism:crusher",
    "mekanism:creative_energy_cube",
    "powah:energy_cell_creative",
    "ironjetpacks:jetpack",
    "pneumaticcraft:creative_compressed_iron_block",
    "pneumaticcraft:creative_compressor",
    "allthearcanistgear:creative_spell_book",
    "ars_nouveau:creative_source_jar",
    "integrateddynamics:energy_battery_creative",
    "ae2:creative_energy_cell",
    "railcraft:creative_locomotive",
    "evilcraft:blood",
)  # 54 ids: every item task plus the one biome task the config states

# The resource-farming guide's material map: the item, dimension, and structure ids the
# pack's own config states for the gated materials (same pinned commit, e5e3d1d83e).
RESOURCE_ITEM_IDS = (
    "allthemodium:allthemodium_ingot",
    "allthemodium:vibranium_ingot",
    "allthemodium:unobtainium_ingot",
    "allthemodium:piglich_heart",
    "allthemodium:vibranium_allthemodium_alloy_ingot",
    "allthemodium:unobtainium_allthemodium_alloy_ingot",
    "allthemodium:unobtainium_vibranium_alloy_ingot",
    "allthemodium:alloy_paxel",
    "minecraft:netherite_ingot",
    "kubejs:magical_soil",
    "mysticalagradditions:creative_essence",
    "mysticalagriculture:allthemodium_seeds",
    "mysticalagriculture:vibranium_seeds",
    "mysticalagriculture:unobtainium_seeds",
    "hostilenetworks:sim_chamber",
    "hostilenetworks:loot_fabricator",
    "hostilenetworks:deep_learner",
    "productivebees:configurable_honeycomb",
    "powah:energizing_orb",
    "ars_nouveau:enchanting_apparatus",
    "industrialforegoing:dissolution_chamber",
    "forbidden_arcanus:eternal_stella",
)

RESOURCE_DIMENSIONS = (
    "allthemodium:mining",
    "allthemodium:the_other",
    "allthemodium:the_beyond",
    "minecraft:ancient_city",
    "allthemodium:ancient_pyramid",
)

# Verified quest titles (en_us lang at e5e3d1d83e) the guide must quote when it says where
# the gated materials come from.
RESOURCE_QUEST_TITLES = (
    "Allthemodium",
    "Teleport Pad",
    "Mining Dimension",
    "The Other",
    "The Beyond",
    "Ancient City",
    "Allthemodium Ingot",
    "Allthemodium Smithing Template",
    "Vibranium Smithing Template",
    "Vibranium Ingot",
    "Unobtainium Smithing Template",
    "Unobtainium Ingot",
    "The Nether",
    "The End",
    "Overworld",
    "Piglich Boss",
    "Ancient Pyramid",
    "Vibranium - Allthemodium Alloy Ingot",
    "Unobtainium - Allthemodium Alloy Ingot",
    "Unobtainium - Vibranium Alloy Ingot",
    "Allthemodium Alloy Paxel",
    "Basic Ore Doubling",
    "Netherite Template",
    "Netherite Tier",
    "Ancient Metals",
    "Visit The Deep Dark!",
    "We've Struck Diamonds!",
)

# The farming systems the guide maps to their verified quest lines.
RESOURCE_FARM_TITLES = (
    "Mystical Agriculture",
    "Infusion Altar",
    "Insanium",
    "Awakened Supremium",
    "The Awakening",
    "Cognizant Dust",
    "Automating Awakened Supremium",
    "Creative Essence",
    "Allthemodium Bee",
    "Vibranium Bee",
    "Unobtainium Bee",
    "Ancient Bee",
    "Diamond Bee",
    "Draconic Bee",
    "Hostile Neural Networks",
    "Modeling Mobs",
    "Simulating Deaths",
    "Creating Loot",
    "The Data Center",
    "Productive Trees",
    "Sawing",
    "Stripping",
)


def stamped_document(chapters: "list[dict[str, Any]]", **stamps: Any) -> "dict[str, Any]":
    """A progress document carrying the pack-version stamp keys, like the example file."""
    payload: "dict[str, Any]" = {"pack_version": "8.x"}
    payload.update(stamps)
    payload["chapters"] = chapters
    return payload


# --------------------------------------------------------------------------------------
# --set: validation before write, clear errors, file untouched on failure
# --------------------------------------------------------------------------------------

class TestSetStatus(TempFileTestCase):

    def sample_chapters(self) -> "list[dict[str, Any]]":
        return [
            make_chapter(id="welcome", title="Welcome", stage="early-game"),
            make_chapter(id="mekanism", title="Mekanism", group="Tech", stage="tech"),
            make_chapter(id="mekanism_reactors", title="Mekanism: Reactors",
                         group="Tech", stage="tech"),
            make_chapter(id="ars_nouveau", title="Ars Nouveau", group="Magic", stage="magic"),
            make_chapter(id="chapter_2_the_star", title="Chapter 3: The ATM Star",
                         group="Main Questline", stage="endgame", status="done"),
        ]

    def write_sample(self, **stamps: Any) -> Path:
        return self.write_data(stamped_document(self.sample_chapters(), **stamps))

    def statuses(self) -> "dict[str, str]":
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        return {chapter["id"]: chapter["status"] for chapter in data["chapters"]}

    def test_marks_a_chapter_done_and_writes_the_file(self) -> None:
        self.write_sample()
        code, out, err = run_main(["--data", str(self.data_path), "--set", "mekanism", "done"])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertEqual(self.statuses()["mekanism"], "done")
        self.assertIn("set: mekanism", out)
        self.assertIn("wrote:", out)
        # The report follows the write, so the numbers shown are the numbers saved.
        self.assertIn("overall: 2/5 chapters done (40.0%)", out)
        self.assertLess(out.index("set: mekanism"), out.index("atm10 quest companion"))

    def test_reopens_a_done_chapter(self) -> None:
        self.write_sample()
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "chapter_2_the_star", "pending"])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.statuses()["chapter_2_the_star"], "pending")
        self.assertIn("(was done)", out)

    def test_accepts_an_exact_chapter_title_case_insensitively(self) -> None:
        self.write_sample()
        # A near-miss title is refused: fuzzy matching would mark the wrong chapter done.
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "Mekanism Reactors", "done"])
        self.assertEqual(code, 1)
        self.assertIn("unknown chapter", (out + err).lower())
        self.assertEqual(self.statuses()["mekanism_reactors"], "pending")
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "Mekanism: Reactors", "done"])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.statuses()["mekanism_reactors"], "done")
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "ars nouveau", "done"])
        self.assertEqual(code, 0, err)
        self.assertEqual(self.statuses()["ars_nouveau"], "done")

    def test_repeated_flags_are_applied_in_one_run(self) -> None:
        self.write_sample()
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "mekanism", "done",
                                   "--set", "welcome", "done",
                                   "--set", "chapter_2_the_star", "pending"])
        self.assertEqual(code, 0, err)
        statuses = self.statuses()
        self.assertEqual(statuses["mekanism"], "done")
        self.assertEqual(statuses["welcome"], "done")
        self.assertEqual(statuses["chapter_2_the_star"], "pending")
        self.assertIn("3 chapters updated", out)
        # welcome + mekanism done, chapter_2_the_star reopened: two of five.
        self.assertIn("overall: 2/5 chapters done (40.0%)", out)

    def test_unknown_chapter_id_fails_cleanly_and_changes_nothing(self) -> None:
        self.write_sample()
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--data", str(self.data_path), "--set", "mekanism2", "done"])
        self.assertEqual(code, 1, "an unknown chapter id must exit 1")
        self.assertNotIn("Traceback", out + err)
        self.assertIn("unknown chapter 'mekanism2'", err)
        self.assertIn("mekanism", err, "the closest known ids must be offered")
        self.assertIn("examples/progress.example.json", err)
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before,
                         "a rejected --set must leave the file byte-for-byte untouched")
        self.assertEqual(self.statuses()["mekanism"], "pending")

    def test_unknown_id_error_names_the_file_being_edited(self) -> None:
        self.write_sample()
        code, out, err = run_main(["--data", str(self.data_path), "--set", "nope", "done"])
        self.assertEqual(code, 1)
        self.assertIn(str(self.data_path), err)
        self.assertNotIn("Traceback", out + err)

    def test_invalid_status_fails_cleanly_and_changes_nothing(self) -> None:
        self.write_sample()
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--data", str(self.data_path), "--set", "mekanism", "finished"])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("status 'finished'", err)
        self.assertIn("done", err)
        self.assertIn("pending", err)
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before)

    def test_one_bad_request_cancels_the_whole_run(self) -> None:
        """Validation happens for every --set before any chapter is touched."""
        self.write_sample()
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "welcome", "done",
                                   "--set", "does_not_exist", "done"])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before,
                         "the good --set must not be applied when a later one is invalid")
        self.assertEqual(self.statuses()["welcome"], "pending")

    def test_a_no_op_reports_itself_and_does_not_rewrite(self) -> None:
        self.write_sample()
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--data", str(self.data_path),
                                   "--set", "chapter_2_the_star", "done"])
        self.assertEqual(code, 0, err)
        self.assertIn("already done", out)
        self.assertIn("unchanged", out)
        self.assertNotIn("wrote:", out)
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before)

    def test_write_preserves_order_stamps_and_schema(self) -> None:
        self.write_sample(pack_version_source="AllTheMods/ATM-10 config/ftbquests 2026-09-22")
        code, out, err = run_main(["--data", str(self.data_path), "--set", "mekanism", "done"])
        self.assertEqual(code, 0, err)
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        self.assertEqual(progress.validate(data), [])
        self.assertEqual(data["pack_version"], "8.x")
        self.assertIn("AllTheMods/ATM-10", data["pack_version_source"])
        self.assertEqual([chapter["id"] for chapter in data["chapters"]],
                         [chapter["id"] for chapter in self.sample_chapters()],
                         "quest-book order must survive a write")
        for chapter in data["chapters"]:
            self.assertEqual(list(chapter), [field for field in progress.CHAPTER_FIELD_ORDER
                                             if field in chapter],
                             "fields must stay in the documented canonical order")

    def test_no_temporary_files_are_left_behind(self) -> None:
        self.write_sample()
        code, out, err = run_main(["--data", str(self.data_path), "--set", "mekanism", "done"])
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(path.name for path in self.data_path.parent.iterdir()),
                         [self.data_path.name],
                         "the atomic write must clean up after itself")

    def test_write_refuses_a_document_that_breaks_the_schema(self) -> None:
        self.write_sample()
        before = self.data_path.read_text(encoding="utf-8")
        broken = {"chapters": [make_chapter(status="nope")]}
        with self.assertRaises(progress.ProgressError) as caught:
            progress.write_progress(self.data_path, broken)
        self.assertIn("does not match the schema", str(caught.exception))
        self.assertIn("status 'nope'", str(caught.exception))
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before,
                         "a document that fails validation must never reach the disk")

    def test_write_reports_an_unwritable_target_without_a_traceback(self) -> None:
        blocked = self.data_path.parent / "blocked.json"
        blocked.mkdir()  # a directory cannot be replaced by a file, on any platform
        with self.assertRaises(progress.ProgressError) as caught:
            progress.write_progress(blocked, stamped_document([make_chapter()]))
        self.assertIn("cannot write the progress file", str(caught.exception))
        leftovers = [path.name for path in self.data_path.parent.iterdir()
                     if path.name.startswith(".blocked.json.")]
        self.assertEqual(leftovers, [], "a failed write must not leave a temporary file")

    def test_set_on_a_missing_file_points_at_the_example(self) -> None:
        missing = self.data_path.parent / "nope.json"
        code, out, err = run_main(["--data", str(missing), "--set", "welcome", "done"])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("no progress file", (out + err).lower())
        self.assertIn("examples/progress.example.json", out + err)
        self.assertFalse(missing.exists(), "--set must not invent a progress file")

    def test_resolve_chapter_is_a_pure_lookup(self) -> None:
        chapters = self.sample_chapters()
        self.assertEqual(progress.resolve_chapter(chapters, "mekanism", Path("x.json"))["id"],
                         "mekanism")
        self.assertEqual(progress.resolve_chapter(chapters, "Ars Nouveau", Path("x.json"))["id"],
                         "ars_nouveau")
        with self.assertRaises(progress.ProgressError):
            progress.resolve_chapter(chapters, "create", Path("x.json"))


# --------------------------------------------------------------------------------------
# --stage: filtering the next-chapters list only
# --------------------------------------------------------------------------------------

class TestStageFilter(TempFileTestCase):

    def chapters(self) -> "list[dict[str, Any]]":
        return [
            make_chapter(id="welcome", stage="early-game", status="done"),
            make_chapter(id="mekanism", title="Mekanism", group="Tech", stage="tech"),
            make_chapter(id="ars_nouveau", title="Ars Nouveau", group="Magic", stage="magic",
                         status="done"),
            make_chapter(id="allthemodium", title="Chapter 2: Allthemodium",
                         group="Main Questline", stage="endgame"),
            make_chapter(id="chapter_2_the_star", title="Chapter 3: The ATM Star",
                         group="Main Questline", stage="endgame"),
        ]

    def test_next_pending_filters_by_stage(self) -> None:
        result = progress.next_pending(self.chapters(), limit=10, stage="endgame")
        self.assertEqual([chapter["id"] for chapter in result],
                         ["allthemodium", "chapter_2_the_star"])
        self.assertEqual([chapter["id"] for chapter in progress.next_pending(self.chapters(), 10)],
                         ["mekanism", "allthemodium", "chapter_2_the_star"],
                         "without a stage the list is unfiltered")

    def test_pending_count_filters_by_stage(self) -> None:
        self.assertEqual(progress.pending_count(self.chapters()), 3)
        self.assertEqual(progress.pending_count(self.chapters(), "endgame"), 2)
        self.assertEqual(progress.pending_count(self.chapters(), "magic"), 0)

    def test_parse_stage_accepts_the_four_ids_only(self) -> None:
        for stage_id in progress.STAGE_ORDER:
            self.assertEqual(progress.parse_stage(stage_id), stage_id)
        self.assertEqual(progress.parse_stage("  Endgame "), "endgame")
        for bad in ("midgame", "", "Tech & Automation"):
            with self.assertRaises(progress.ProgressError):
                progress.parse_stage(bad)

    def test_invalid_stage_fails_cleanly(self) -> None:
        self.write_data(document(self.chapters()))
        code, out, err = run_main(["--data", str(self.data_path), "--stage", "midgame"])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("--stage 'midgame'", err)
        for stage_id in progress.STAGE_ORDER:
            self.assertIn(stage_id, err)

    def test_report_lists_only_the_filtered_stage(self) -> None:
        report = progress.format_report(self.chapters(), Path("x.json"), limit=10,
                                        stage="endgame")
        self.assertIn("stage filter: endgame", report)
        self.assertIn("showing 2 of 2", report)
        self.assertIn("allthemodium", report)
        self.assertNotIn("mekanism", report.split("next unfinished chapters")[1],
                         "a filtered list must not show other stages' chapters")
        # The completion math is never filtered.
        self.assertIn("overall: 2/5 chapters done (40.0%)", report)
        self.assertIn("tech", report)

    def test_report_marks_the_filtered_stage_row(self) -> None:
        report = progress.format_report(self.chapters(), Path("x.json"), limit=10,
                                        stage="magic")
        stage_line = [line for line in report.splitlines() if line.strip().startswith("magic")]
        self.assertTrue(stage_line)
        self.assertIn("<==", stage_line[0])

    def test_stage_with_nothing_pending_says_so(self) -> None:
        report = progress.format_report(self.chapters(), Path("x.json"), limit=10,
                                        stage="magic")
        self.assertIn("no unfinished chapters in stage 'magic'", report)
        self.assertNotIn("next unfinished chapters", report)

    def test_all_done_message_is_unchanged_without_a_filter(self) -> None:
        done = [make_chapter(id="a", status="done"), make_chapter(id="b", status="done")]
        report = progress.format_report(done, Path("x.json"), limit=5)
        self.assertIn("all chapters done", report)
        self.assertNotIn("no unfinished chapters in stage", report)

    def test_end_to_end_stage_filter_via_main(self) -> None:
        self.write_data(stamped_document(self.chapters()))
        code, out, err = run_main(["--data", str(self.data_path), "--stage", "endgame",
                                   "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn("stage filter: endgame, showing 1 of 2", out)
        listed = [line for line in out.splitlines() if ". [" in line]
        self.assertEqual(len(listed), 1)
        self.assertIn("allthemodium", listed[0])


# --------------------------------------------------------------------------------------
# pack-version stamp and the drift check
# --------------------------------------------------------------------------------------

class TestPackVersionDrift(TempFileTestCase):

    def example_chapters(self) -> "list[dict[str, Any]]":
        return json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))["chapters"]

    def test_known_chapters_load_from_the_shipped_example(self) -> None:
        known = progress.load_known_chapters()
        self.assertIsNotNone(known)
        assert known is not None
        self.assertEqual(known.version, "8.x")
        self.assertEqual(known.total, 66)
        self.assertEqual(known.path, EXAMPLE_DATA)
        self.assertEqual(known.order, tuple(chapter["id"] for chapter in self.example_chapters()))
        self.assertIn("mekanism", known.ids)

    def test_known_chapters_is_none_when_the_example_is_unusable(self) -> None:
        missing = self.data_path.parent / "no-example.json"
        self.assertIsNone(progress.load_known_chapters(missing))
        for payload in ("", "not json", "[]", '{"chapters": []}', '{"chapters": "nope"}',
                        '{"chapters": [{"title": "no id"}]}'):
            path = self.write_data(None, raw=payload)
            self.assertIsNone(progress.load_known_chapters(path), f"accepted {payload!r}")

    def test_known_version_falls_back_when_the_example_is_unstamped(self) -> None:
        self.write_data({"chapters": [make_chapter()]})
        known = progress.load_known_chapters(self.data_path)
        self.assertIsNotNone(known)
        assert known is not None
        self.assertEqual(known.version, progress.DEFAULT_PACK_VERSION)

    def test_check_drift_is_clean_for_a_copy_of_the_example(self) -> None:
        chapters = self.example_chapters()
        self.assertEqual(progress.check_drift(chapters, progress.load_known_chapters(),
                                              {"pack_version": "8.x"}), [])

    def test_check_drift_is_silent_without_a_known_list(self) -> None:
        chapters = [make_chapter(id="something_invented")]
        self.assertEqual(progress.check_drift(chapters, None, {}), [])

    def test_unknown_chapter_id_warns_and_still_exits_zero(self) -> None:
        chapters = self.example_chapters() + [
            make_chapter(id="frobnicate", title="Frobnicate", group="Tech", stage="tech"),
        ]
        self.write_data(stamped_document(chapters))
        code, out, err = run_main(["--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertNotIn("Traceback", out)
        self.assertIn("pack drift", out)
        self.assertIn("frobnicate", out)
        self.assertIn("not in the known pack 8.x list", out)
        self.assertIn("quest book", out,
                      "a drift warning must defer to the in-game quest book")
        # The unknown chapter is still counted: a warning is not a rejection.
        self.assertIn("overall: 0/67 chapters done", out)

    def test_missing_known_ids_warn(self) -> None:
        self.write_data(stamped_document(self.example_chapters()[:10]))
        code, out, err = run_main(["--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn("56 chapter ids from the known pack 8.x list are missing", out)
        self.assertIn("basic_armor", out, "the first missing id is listed")
        self.assertIn("(+50 more)", out, "a long id list must be shortened")

    def test_version_mismatch_warns(self) -> None:
        self.write_data({"pack_version": "7.3", "chapters": self.example_chapters()})
        code, out, err = run_main(["--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn("stamped pack 7.3", out)
        self.assertIn("known chapter list is pack 8.x", out)

    def test_missing_stamp_warns(self) -> None:
        self.write_data(document(self.example_chapters()))
        code, out, err = run_main(["--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn('carries no "pack_version" stamp', out)
        self.assertIn("unstamped", out)

    def test_a_stamp_that_is_not_a_version_warns(self) -> None:
        self.write_data({"pack_version": "ATM10 eight", "chapters": self.example_chapters()})
        code, out, err = run_main(["--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn("does not look like a pack version", out)

    def test_report_shows_the_pack_line(self) -> None:
        self.write_data(stamped_document(self.example_chapters()))
        code, out, err = run_main(["--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn("pack: 8.x  (known chapter list: pack 8.x, 66 chapters)", out)
        self.assertNotIn("pack drift", out)

    def test_set_keeps_the_stamp_and_the_file_clean(self) -> None:
        self.write_data(stamped_document(self.example_chapters()))
        code, out, err = run_main(["--data", str(self.data_path), "--set", "mekanism", "done",
                                   "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertIn("set: mekanism", out)
        self.assertNotIn("pack drift", out)
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        self.assertEqual(data["pack_version"], "8.x")
        self.assertEqual(progress.validate(data), [])

    def test_validate_rejects_a_bad_stamp_and_unknown_top_level_keys(self) -> None:
        for payload, needle in (
            ({"pack_version": "", "chapters": [make_chapter()]}, "'pack_version' must be a non-empty string"),
            ({"pack_version": 8, "chapters": [make_chapter()]}, "'pack_version' must be a non-empty string"),
            ({"pack_version_source": 3, "chapters": [make_chapter()]}, "'pack_version_source' must be a non-empty string"),
            ({"pack": "8.x", "chapters": [make_chapter()]}, "unknown top-level key"),
        ):
            problems = progress.validate(payload)
            self.assertTrue(any(needle in problem for problem in problems),
                            f"{payload} should report {needle!r}, got {problems}")

    def test_validate_accepts_both_stamp_fields(self) -> None:
        self.assertEqual(progress.validate(stamped_document([make_chapter()],
                                                            pack_version_source="repo config")),
                         [])

    def test_version_pattern_accepts_pack_versions_only(self) -> None:
        for good in ("8.x", "8.X", "8", "8.2", "8.2.1"):
            self.assertTrue(progress.PACK_VERSION_RE.match(good), good)
        for bad in ("ATM10 eight", "v8.x", "8.x-dev", "", "eight"):
            self.assertIsNone(progress.PACK_VERSION_RE.match(bad), bad)

    def test_drift_check_never_blocks_a_report(self) -> None:
        """Drift is information: exit status stays 0 and the report is still complete."""
        chapters = [make_chapter(id="invented_chapter", title="Invented", stage="tech")]
        self.write_data(document(chapters))
        code, out, err = run_main(["--data", str(self.data_path)])
        self.assertEqual(code, 0, err)
        self.assertIn("atm10 quest companion", out)
        self.assertIn("overall: 0/1 chapters done", out)
        self.assertIn("pack drift", out)
        self.assertIn("invented_chapter", out)


# --------------------------------------------------------------------------------------
# --list, --json, and --sync CLI additions
# --------------------------------------------------------------------------------------

class TestListCommand(unittest.TestCase):

    def test_lists_every_known_chapter_grouped_by_progression_stage(self) -> None:
        known = progress.load_known_chapters()
        self.assertIsNotNone(known)
        assert known is not None
        code, out, err = run_main(["--list", "--data", "/does/not/exist/progress.json"])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        lines = out.splitlines()
        headings = [f"[{stage_id}] {title}" for stage_id, title in progress.STAGES]
        self.assertEqual([line for line in lines if line.startswith("[")], headings)
        listed_ids = [line[2:].split(" - ", 1)[0]
                      for line in lines if line.startswith("  ")]
        expected_ids = [chapter["id"] for stage_id, _ in progress.STAGES
                        for chapter in known.chapters if chapter["stage"] == stage_id]
        self.assertEqual(listed_ids, expected_ids)
        self.assertEqual(len(listed_ids), known.total)
        for chapter in known.chapters:
            self.assertIn(f"  {chapter['id']} - {chapter['title']}", out)
        self.assertNotIn("Traceback", out)

    def test_list_rejects_report_only_filters_cleanly(self) -> None:
        code, out, err = run_main(["--list", "--stage", "tech"])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("cannot be combined with --stage", err)


class TestJsonReport(TempFileTestCase):

    def sample_chapters(self) -> "list[dict[str, Any]]":
        return [
            make_chapter(id="welcome", title="Welcome", status="done"),
            make_chapter(id="mekanism", title="Mekanism", group="Tech", stage="tech"),
            make_chapter(id="ars_nouveau", title="Ars Nouveau", group="Magic", stage="magic"),
        ]

    def test_json_stdout_is_a_full_indented_machine_readable_report(self) -> None:
        self.write_data(stamped_document(self.sample_chapters()))
        code, out, err = run_main(["--json", "--data", str(self.data_path), "--next", "1"])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        report = json.loads(out)
        self.assertEqual(out, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        self.assertEqual(report["pack_version"], "8.x")
        self.assertEqual(report["known_pack_version"], "8.x")
        self.assertEqual(report["known_chapter_count"],
                         len(json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))["chapters"]))
        self.assertEqual(report["overall"], {"total": 3, "done": 1, "percent": 33.3})
        self.assertEqual([row["id"] for row in report["per_stage"]], list(progress.STAGE_ORDER))
        self.assertEqual(report["per_stage"][0]["done"], 1)
        self.assertEqual(report["per_stage"][1]["total"], 1)
        self.assertEqual(report["next_chapters"], [{
            "id": "mekanism", "title": "Mekanism", "stage": "tech", "group": "Tech",
            "status": "pending",
        }])
        self.assertEqual(report["pending_chapter_count"], 2)
        self.assertEqual(report["stage_filter"], None)
        self.assertIsInstance(report["pack_drift"], list)
        self.assertNotIn("atm10 quest companion", out)
        self.assertNotIn("Traceback", out)

    def test_json_supports_stage_filter_and_json_only_set_output(self) -> None:
        self.write_data(stamped_document(self.sample_chapters()))
        code, out, err = run_main([
            "--json", "--data", str(self.data_path), "--stage", "tech",
            "--next", "1", "--set", "mekanism", "done",
        ])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        report = json.loads(out)
        self.assertEqual(report["overall"]["done"], 2)
        self.assertEqual(report["stage_filter"], "tech")
        self.assertEqual([row["id"] for row in report["next_chapters"]], [])
        self.assertEqual(report["set_changes"], [{
            "id": "mekanism", "title": "Mekanism", "previous_status": "pending",
            "status": "done", "changed": True,
        }])
        self.assertEqual(progress.load_progress(self.data_path)[1]["status"], "done")

    def test_bad_json_input_fails_without_traceback_or_json_garbage(self) -> None:
        self.write_data(None, raw="{ definitely not JSON")
        code, out, err = run_main(["--json", "--data", str(self.data_path)])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)
        self.assertIn("not valid json", err.lower())


class TestSyncCommand(TempFileTestCase):

    @staticmethod
    def known_chapters() -> "list[dict[str, Any]]":
        return json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))["chapters"]

    def drifted_document(self) -> "dict[str, Any]":
        chapters = copy.deepcopy(self.known_chapters()[1:])
        # Put two records out of order to prove sync restores the book order as well.
        chapters[0], chapters[1] = chapters[1], chapters[0]
        chapters[1]["status"] = "done"
        chapters.append(make_chapter(id="removed_chapter", title="Removed Chapter", stage="tech"))
        return stamped_document(chapters, pack_version="7.3",
                                pack_version_source="previous catalog provenance")

    def test_sync_dry_run_prints_all_changes_and_never_writes(self) -> None:
        self.write_data(self.drifted_document())
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--sync", "--data", str(self.data_path)])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertIn("unknown chapter ids (will be dropped): 1", out)
        self.assertIn("removed_chapter", out)
        self.assertIn("known chapters missing from the file (will be added as pending): 1", out)
        self.assertIn("welcome", out)
        self.assertIn("pack_version: 7.3 -> 8.x", out)
        self.assertIn("chapter order: will be restored", out)
        self.assertIn("dry run: no file written", out)
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before)
        self.assertLess(out.index("sync preview"), out.index("dry run"))

    def test_sync_yes_drops_unknown_adds_missing_preserves_progress_and_stamps(self) -> None:
        self.write_data(self.drifted_document())
        code, out, err = run_main(["--sync", "--yes", "--data", str(self.data_path)])
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        self.assertLess(out.index("sync preview"), out.index("applied:"))
        self.assertIn("dropped 1 unknown", out)
        self.assertIn("added 1 missing as pending", out)
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        known = progress.load_known_chapters()
        assert known is not None
        self.assertEqual(data["pack_version"], known.version)
        self.assertEqual(data["pack_version_source"], "previous catalog provenance")
        self.assertEqual([chapter["id"] for chapter in data["chapters"]], list(known.order))
        self.assertNotIn("removed_chapter", [chapter["id"] for chapter in data["chapters"]])
        by_id = {chapter["id"]: chapter for chapter in data["chapters"]}
        self.assertEqual(by_id["welcome"]["status"], "pending")
        self.assertEqual(by_id["bounty_board"]["status"], "done")
        self.assertEqual(progress.validate(data), [])

    def test_clean_sync_does_not_rewrite_the_file(self) -> None:
        self.write_data(stamped_document(self.known_chapters()))
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--sync", "--yes", "--data", str(self.data_path)])
        self.assertEqual(code, 0, err)
        self.assertIn("result: no changes needed", out)
        self.assertIn("unchanged:", out)
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before)

    def test_sync_can_preview_and_create_a_missing_progress_file(self) -> None:
        missing = self.data_path.parent / "nested" / "progress.json"
        code, out, err = run_main(["--sync", "--data", str(missing)])
        self.assertEqual(code, 0, err)
        self.assertIn("progress file: missing", out)
        self.assertIn("known chapters missing from the file", out)
        self.assertFalse(missing.exists(), "a dry run must not create the file or parent directory")

        code, out, err = run_main(["--sync", "--yes", "--data", str(missing)])
        self.assertEqual(code, 0, err)
        self.assertTrue(missing.is_file())
        data = json.loads(missing.read_text(encoding="utf-8"))
        self.assertEqual([chapter["id"] for chapter in data["chapters"]],
                         [chapter["id"] for chapter in self.known_chapters()])
        self.assertTrue(all(chapter["status"] == "pending" for chapter in data["chapters"]))

    def test_sync_reports_malformed_files_cleanly_and_leaves_them_untouched(self) -> None:
        self.write_data(None, raw="{broken")
        before = self.data_path.read_text(encoding="utf-8")
        code, out, err = run_main(["--sync", "--yes", "--data", str(self.data_path)])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("not valid json", err.lower())
        self.assertEqual(self.data_path.read_text(encoding="utf-8"), before)

    def test_bad_option_combinations_and_path_values_never_traceback(self) -> None:
        for argv, needle in (
            (["--yes"], "only valid with --sync"),
            (["--sync", "--set", "welcome", "done"], "cannot be combined with --set"),
            (["--sync", "--data", "\x00"], "null character"),
        ):
            code, out, err = run_main(argv)
            self.assertEqual(code, 1)
            self.assertNotIn("Traceback", out + err)
            self.assertIn(needle, (out + err).lower())


# --------------------------------------------------------------------------------------
# the three endgame reference docs
# --------------------------------------------------------------------------------------

class TestEndgameReferenceDocs(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.star = STAR_CHECKLIST_MD.read_text(encoding="utf-8") if STAR_CHECKLIST_MD.is_file() else ""
        cls.boss = BOSS_CHECKLIST_MD.read_text(encoding="utf-8") if BOSS_CHECKLIST_MD.is_file() else ""
        cls.creative = (CREATIVE_CHECKLIST_MD.read_text(encoding="utf-8")
                        if CREATIVE_CHECKLIST_MD.is_file() else "")
        cls.star_lower = cls.star.lower()
        cls.boss_lower = cls.boss.lower()
        cls.creative_lower = cls.creative.lower()

    def assert_grounded(self, text: str, lowered: str, name: str) -> None:
        """Both endgame docs must carry the skill's grounding rules and their provenance."""
        self.assertGreater(len(text.strip()), 2000, f"{name} looks like a stub")
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, lowered, f"{name} must state the {needle!r} rule")
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), lowered, f"{name} must name its source: {source}")
        # The pack version the docs were read from, matching the example file's stamp.
        self.assertIn("8.2", text, f"{name} must date itself against the pack version read")
        self.assertIn("8.x", text, f"{name} must tie that version to the skill's 8.x stamp")
        self.assertRegex(lowered, r"never invented|not invented|never invent",
                         f"{name} must say its details were read, not invented")

    def test_star_checklist_exists_and_is_grounded(self) -> None:
        self.assertTrue(STAR_CHECKLIST_MD.is_file(), f"missing {STAR_CHECKLIST_MD}")
        self.assert_grounded(self.star, self.star_lower, "atm-star-checklist.md")

    def test_boss_checklist_exists_and_is_grounded(self) -> None:
        self.assertTrue(BOSS_CHECKLIST_MD.is_file(), f"missing {BOSS_CHECKLIST_MD}")
        self.assert_grounded(self.boss, self.boss_lower, "boss-checklist.md")

    def test_star_checklist_lists_every_chapter_3_component(self) -> None:
        for component in STAR_COMPONENTS:
            self.assertIn(component, self.star,
                          f"the ATM Star checklist is missing a verified component: {component}")
        self.assertIn("allthetweaks:atm_star", self.star)
        self.assertIn("13", self.star, "the doc must say the star quest has 13 dependencies")

    def test_star_checklist_is_organized_by_source_mod(self) -> None:
        """Components are grouped per mod, with the pack's own item ids and mod names."""
        for namespace in ("mekanism:", "ae2:", "create:", "ars_nouveau:", "occultism:",
                          "evilcraft:", "forbidden_arcanus:", "mysticalagradditions:",
                          "modern_industrialization:", "allthetweaks:", "allthemodium:",
                          "allthecompressed:", "twilightforest:", "cataclysm:",
                          "productivebees:", "productivetrees:", "irons_spellbooks:",
                          "industrialforegoing:", "pneumaticcraft:", "bigreactors:",
                          "hostilenetworks:", "deeperdarker:", "eternal_starlight:",
                          "justdirethings:", "oritech:", "powah:", "immersiveengineering:",
                          "stevescarts:", "rootsclassic:", "neovitae:", "pocketstorage:",
                          "generatorgalore:", "ironfurnaces:", "megacells:", "advanced_ae:",
                          "ae2wtlib:", "aeinfinitybooster:", "ftbfiltersystem:",
                          "apothic_enchanting:", "alltheores:", "minecraft:"):
            self.assertIn(namespace, self.star,
                          f"the star checklist must cite the {namespace} tasks it groups by")
        for mod in ("Mekanism", "Applied Energistics", "Create", "Ars Nouveau", "Occultism",
                    "Modern Industrialization", "Twilight Forest", "Cataclysm",
                    "Mystical Agriculture", "Productive Bees", "Hostile Neural Networks"):
            self.assertIn(mod, self.star, f"the star checklist must name the {mod} section")

    def test_star_checklist_refuses_to_invent_recipes(self) -> None:
        self.assertIn("no recipes", self.star_lower)
        self.assertIn("does not tell you", self.star_lower)

    def test_boss_checklist_names_the_verified_bosses(self) -> None:
        for boss in VERIFIED_BOSSES:
            self.assertIn(boss, self.boss,
                          f"the boss checklist is missing a verified boss: {boss}")

    def test_boss_checklist_gives_dimension_and_timing(self) -> None:
        for dimension in ("Twilight Forest", "The Aether", "The Nether", "The End",
                          "Overworld", "Otherside", "Undergarden", "The Other", "Bumblezone"):
            self.assertIn(dimension, self.boss, f"missing dimension: {dimension}")
        self.assertIn("roughly when", self.boss_lower)
        # The three boss lines the request called out by name.
        for line in ("Twilight Forest", "Cataclysm", "Aether"):
            self.assertIn(line, self.boss)
        # Boss order in the Twilight Forest line is verified from the trophy chain.
        positions = [self.boss.index(name) for name in
                     ("Naga", "Lich", "Minoshroom", "Hydra", "Knight Phantom", "Ur-Ghast",
                      "Alpha Yeti", "Snow Queen")]
        self.assertEqual(positions, sorted(positions),
                         "the Twilight Forest bosses must be listed in the pack's order")

    def test_boss_checklist_quotes_health_only_as_quest_text(self) -> None:
        self.assertIn("quest text", self.boss_lower)
        self.assertIn("no tactics", self.boss_lower)

    def test_the_docs_cross_reference_each_other_and_the_star(self) -> None:
        self.assertIn("boss-checklist.md", self.star)
        self.assertIn("atm-star-checklist.md", self.boss)
        self.assertIn("progression.md", self.boss)

    def test_creative_checklist_exists_and_is_grounded(self) -> None:
        self.assertTrue(CREATIVE_CHECKLIST_MD.is_file(), f"missing {CREATIVE_CHECKLIST_MD}")
        self.assert_grounded(self.creative, self.creative_lower, "creative-checklist.md")

    def test_creative_checklist_lists_every_verified_quest_title(self) -> None:
        self.assertEqual(len(CREATIVE_TITLED_QUESTS), 36)
        for title in CREATIVE_TITLED_QUESTS:
            self.assertIn(title, self.creative,
                          f"the creative checklist is missing a verified title: {title}")
        # Two of the 38 quests carry no title in the config; the page must mark each one
        # in place rather than derive a name for it.
        flat = re.sub(r"\s+", " ", self.creative)
        self.assertGreaterEqual(flat.count("(no title in the config)"), 2,
                                "both untitled quests must be marked")
        self.assertIn("(no title in the config)* \u2192 **Lens of Certain Death**", flat,
                      "the untitled Atomic Reconstructor quest must stay untitled")
        self.assertIn("| 2 | *(no title in the config)* | `apothic_enchanting:infused_breath`", flat,
                      "the untitled Infused Breath quest must stay untitled")
        self.assertIn("36 of the 38 quests carry an explicit title", flat)

    def test_creative_checklist_quotes_every_config_task_item(self) -> None:
        for item in CREATIVE_TASK_ITEMS:
            self.assertIn(item, self.creative,
                          f"the creative checklist must cite the config's task item {item}")

    def test_creative_checklist_covers_the_star_automation_line(self) -> None:
        self.assertRegex(self.creative, r"Quests in the chapter.*?38")
        self.assertIn("Fully Automated ATM Star", self.creative)
        self.assertIn("10 direct dependencies", self.creative)
        for multiblock in ("Runic Star Altar", "Runic Crucible",
                           "Automatic Hepheastus Forge", "Runic Enchanter"):
            self.assertIn(multiblock, self.creative)
        # The five parts, in the pack's own 1/5 ... 5/5 order, each next to its prism.
        parts = ("Top ATM Star part", "Right ATM Star part", "Bottom Right ATM Star part",
                 "Bottom Left ATM Star part", "Left ATM Star part")
        positions = [self.creative.index(part) for part in parts]
        self.assertEqual(positions, sorted(positions),
                         "the five star parts must stay in the pack's 1/5 ... 5/5 order")
        for number, (part, prism) in enumerate(zip(parts, ("Soul Binding Crystal",
                                                           "Whirlwind Prism", "Smelter Prism",
                                                           "Sea Prism", "Terrastomp Prism")),
                                                   start=1):
            self.assertIn(f"kubejs:atm_star_shard_{number}", self.creative)
            self.assertIn(prism, self.creative)
        # The bee chain and the terminal quest's other dependencies are named too.
        for title in ("Patrick Star... Bee?", "Starry Bee!", "Star Shards", "But why?",
                      "Arcane Crystals", "Mundabitur Dust", "Corrupti Dust",
                      "Lens of Certain Death", "Lens of the Killer", "Infused Patrick Star"):
            self.assertIn(title, self.creative)

    def test_creative_checklist_lists_the_eleven_items_in_config_order(self) -> None:
        self.assertEqual(len(CREATIVE_ITEMS), 11)
        positions = [self.creative.index(title) for title in CREATIVE_ITEMS]
        self.assertEqual(positions, sorted(positions),
                         "the eleven creative quests must be in the order the config lists them")
        flat = re.sub(r"\s+", " ", self.creative_lower)
        self.assertIn("eleven creative", flat)
        self.assertIn("by a single dependency", flat)
        self.assertIn("Unlimited Powah!", self.creative)
        self.assertIn("Get this first!", self.creative)

    def test_creative_checklist_dates_itself_to_the_pinned_commit(self) -> None:
        self.assertIn(CREATIVE_COMMIT, self.creative)
        self.assertIn("CHANGELOG.md", self.creative)
        self.assertIn("pack 8.2", self.creative)
        self.assertIn(CREATIVE_CHAPTER_ID, self.creative)
        self.assertIn("Chapter 4: Creative", self.creative)
        self.assertIn("Plus Star Automation!", self.creative)
        self.assertIn("Main Questline", self.creative)
        self.assertIn("Modular Routers", self.creative)
        self.assertIn("endgame", self.creative)

    def test_creative_checklist_says_the_book_is_a_canvas_not_a_numbered_list(self) -> None:
        flat = re.sub(r"\s+", " ", self.creative_lower)
        self.assertIn("canvas, not as a numbered list", flat)
        self.assertIn("in dependency order", flat)

    def test_creative_checklist_keeps_the_hedges(self) -> None:
        flat = re.sub(r"\s+", " ", self.creative_lower)
        for needle in ("no recipes", "does not tell you", "approximate", "quest text",
                       "never a guess"):
            self.assertIn(needle, flat, f"missing hedge: {needle}")
        self.assertIn("generic on purpose", flat,
                      "the two generic task ids must be flagged, not presented as exact")
        self.assertIn("no boss tasks", flat)
        self.assertIn("85mfe is the quest author's own figure", flat,
                      "quoted numbers must stay attributed to the quest text")

    def test_the_creative_doc_cross_references_its_siblings(self) -> None:
        for sibling in ("atm-star-checklist.md", "boss-checklist.md", "progression.md"):
            self.assertIn(sibling, self.creative,
                          f"creative-checklist.md must point at {sibling}")
        # ...and the star checklist, which stops where this one starts, points back.
        self.assertIn("creative-checklist.md", self.star)

    def test_skill_md_documents_the_new_reference_docs(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        for name in ("references/atm-star-checklist.md", "references/boss-checklist.md",
                     "references/creative-checklist.md"):
            self.assertIn(name, skill, f"SKILL.md must point at {name}")
        for behaviour in ("--set", "--stage", "--list", "--json", "--sync", "--yes",
                          "pack_version", "drift"):
            self.assertIn(behaviour, skill, f"SKILL.md must document {behaviour}")
        self.assertIn("two-space indentation", skill)
        self.assertIn("without `--yes`, it", skill)


# --------------------------------------------------------------------------------------
# the resource-farming guide
# --------------------------------------------------------------------------------------

class TestResourceFarmingGuide(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.guide = (RESOURCE_GUIDE_MD.read_text(encoding="utf-8")
                     if RESOURCE_GUIDE_MD.is_file() else "")
        cls.lowered = cls.guide.lower()
        # Whitespace-insensitive copy: the page wraps mid-sentence and inside quotes.
        cls.flat = re.sub(r"\s+", " ", cls.guide)
        cls.flat_lower = cls.flat.lower()

    def assert_grounded(self, text: str, lowered: str, name: str) -> None:
        """The resource guide carries the same grounding rules as the endgame docs."""
        self.assertGreater(len(text.strip()), 2000, f"{name} looks like a stub")
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, lowered, f"{name} must state the {needle!r} rule")
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), lowered, f"{name} must name its source: {source}")
        self.assertIn("8.2", text, f"{name} must date itself against the pack version read")
        self.assertIn("8.x", text, f"{name} must tie that version to the skill's 8.x stamp")
        self.assertRegex(lowered, r"never invented|not invented|never invent",
                         f"{name} must say its details were read, not invented")

    def test_guide_exists_and_is_grounded(self) -> None:
        self.assertTrue(RESOURCE_GUIDE_MD.is_file(), f"missing {RESOURCE_GUIDE_MD}")
        self.assert_grounded(self.guide, self.lowered, "resource-farming-guide.md")

    def test_guide_dates_itself_to_the_pinned_commit(self) -> None:
        self.assertIn("e5e3d1d83e", self.guide)
        self.assertIn("pack 8.2", self.guide)
        self.assertIn("2026-09-22", self.guide)
        self.assertIn("493", self.guide,
                      "the guide must quote the modlist's verified entry count")

    def test_guide_maps_every_gated_material_to_its_source_ids(self) -> None:
        # self.flat: the page wraps mid-sentence, so multi-word strings span lines.
        for item in RESOURCE_ITEM_IDS:
            self.assertIn(item, self.flat, f"the resource guide must cite {item}")
        for where in RESOURCE_DIMENSIONS:
            self.assertIn(where, self.flat, f"the resource guide must name {where}")

    def test_guide_quotes_the_verified_quest_titles(self) -> None:
        for title in RESOURCE_QUEST_TITLES:
            self.assertIn(title, self.flat, f"missing verified quest title: {title}")

    def test_guide_covers_the_farm_systems(self) -> None:
        for title in RESOURCE_FARM_TITLES:
            self.assertIn(title, self.flat, f"missing farm-system quest title: {title}")
        # Each system is tied to the config's own machine or crop ids.
        for needle in ("foundry pour", "foundry", "simulating mob kills for loot"):
            self.assertIn(needle, self.flat_lower)
        # The bee chain's three pour descriptions are the pack's words, in order.
        positions = [self.flat.index(bee) for bee in
                     ("Allthemodium Bee", "Vibranium Bee", "Unobtainium Bee")]
        self.assertEqual(positions, sorted(positions),
                         "the bee chain must stay in the pack's Diamond -> Ancient -> "
                         "Allthemodium -> Vibranium -> Unobtainium order")
        allthemodium_bee = self.flat.index("Allthemodium Bee")
        for earlier in ("Ancient Bee", "Diamond Bee"):
            self.assertLess(self.flat.index(earlier), allthemodium_bee,
                            f"{earlier} comes before Allthemodium Bee in the chain")

    def test_guide_keeps_the_where_hedges(self) -> None:
        # The pack's own distribution words, kept verbatim in the guide.
        for hedge in ("rarely", "very rarely", "approximate"):
            self.assertIn(hedge, self.lowered, f"missing hedge: {hedge}")
        for place in ("Ancient Cities", "Deep Dark Biome", "End Highlands"):
            self.assertIn(place, self.guide, f"missing quoted location: {place}")

    def test_guide_marks_untitled_quests_in_place(self) -> None:
        marked = self.flat.count("(no title in the config)")
        self.assertGreaterEqual(marked, 4,
                                "every untitled quest the guide relies on must be marked")
        self.assertIn("47 of `allthemodium`'s 54 quests", self.flat)
        self.assertIn("only five quests carry an explicit title", self.flat)

    def test_guide_refuses_recipes_coordinates_and_ore_levels(self) -> None:
        self.assertIn("No recipes, no coordinates, no ore levels.", self.guide)
        self.assertIn("never invent", self.lowered)
        self.assertIn("check the quest entry / jei", self.lowered)
        self.assertIn("treat every distribution detail here as approximate", self.flat_lower)

    def test_guide_cross_references_the_sibling_docs(self) -> None:
        for sibling in ("atm-star-checklist.md", "boss-checklist.md",
                        "creative-checklist.md", "progression.md"):
            self.assertIn(sibling, self.guide, f"the guide must point at {sibling}")

    def test_guide_maps_stages_to_the_skill_s_progression_model(self) -> None:
        for stage in ("early-game", "tech", "endgame"):
            self.assertIn(stage, self.lowered,
                          f"the guide must use the skill's {stage!r} stage")
        self.assertIn("references/progression.md", self.guide)
        self.assertIn("quests are optional", self.lowered)

    def test_skill_md_points_at_the_guide(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/resource-farming-guide.md", skill,
                      "SKILL.md must point at the new reference doc")
        self.assertIn("four researched docs", skill,
                      "SKILL.md must describe the four researched docs together")
        self.assertIn("no title in the config", skill,
                      "SKILL.md must repeat the untitled-quest marking rule")


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def imported_modules(self, source: str) -> "set[str]":
        found: "set[str]" = set()
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        return found

    def test_progress_script_imports_no_network_or_process_module(self) -> None:
        imported = self.imported_modules(SCRIPT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set(),
                         "progress.py must stay offline: no network, no subprocesses")
        self.assertTrue(imported <= set(("argparse", "difflib", "json", "os", "re", "sys",
                                         "tempfile", "pathlib", "typing", "__future__")),
                        f"unexpected import(s): {sorted(imported)}")

    def test_this_suite_imports_no_network_module(self) -> None:
        imported = self.imported_modules(Path(__file__).read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())

    def test_skill_md_promises_no_network(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8").lower()
        self.assertIn("no network", skill)
        self.assertIn("stdlib-only", skill)


if __name__ == "__main__":
    unittest.main()
