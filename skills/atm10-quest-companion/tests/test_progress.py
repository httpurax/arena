#!/usr/bin/env python3
"""Offline tests for the atm10-quest-companion skill.

Stdlib-only and network-free: the skill's script reads one local JSON file, so every
case here is a temp file, a fixed chapter list, or a pure function call.

Covered:

  * the frontmatter identity (``name`` matches the directory) and the documented
    research-grounding rule (in-game quest book + JEI authoritative, uncertain details
    flagged as approximate, nothing invented);
  * the shipped example file: it exists, validates against the schema, every chapter is
    pending, ids are unique, and the quest-book order is preserved (standalone chapters
    first, then the pack's groups in order, contiguous within each group);
  * ``scripts/progress.py``: a missing, empty, malformed, or schema-breaking progress
    file is reported as one clear message with exit status 1, never a traceback;
  * completion math against fixed inputs (per stage and overall, one-decimal rounding,
    empty-stage and all-done edges) and next-chapter ordering (file order across stages,
    ``--next`` cap, done chapters skipped);
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
        for path in (PROGRESSION_MD, KEY_MODS_MD, GETTING_STARTED_MD):
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
        self.assertEqual(set(self.data), {"chapters"})
        self.assertIsInstance(self.chapters, list)

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


if __name__ == "__main__":
    unittest.main()
