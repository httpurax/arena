"""Offline tests for references/progression-roadmap.md.

Stdlib-only and network-free: every case reads files that ship with the skill and
compares them against each other - never the network, never a pack clone.

The roadmap is the skill's recommended play order for all 66 quest-book chapters,
grouped into four phases (early / mid / late / endgame), one line per chapter. The
order itself is author's judgement and must be flagged as a recommendation, not pack
canon; the chapter ids, titles, groups, quest counts, and quoted quest titles must be
pack-8.2 config data (AllTheMods/ATM-10 at main e5e3d1d83e), consistent with the
shipped ``examples/progress.example.json``. These tests hold the doc to that split.

Covered:

  * existence and substance (not a stub);
  * provenance: the pack repo, the pinned commit, pack 8.2, the date, the config files
    read, and the 66-chapter / 4,790-quest totals;
  * grounding rules: the in-game quest book and JEI authoritative, uncertain details
    approximate, the order flagged as a recommendation and not pack canon, and the
    never-invent rule for item ids, recipes, and coordinates;
  * structure: the four phase headings with the expected chapter counts
    (16 + 37 + 10 + 3 = 66) and the enforcing/cross-reference sections;
  * content: every chapter of the example file appears exactly once, numbered 1..66 in
    order, with its title, group, stage, and verified quest count intact;
  * the five verified cross-chapter dependency links are named as the pack's only ones;
  * SKILL.md points at the roadmap and keeps the recommendation caveat.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ROADMAP_MD = SKILL_ROOT / "references" / "progression-roadmap.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"
SKILL_MD = SKILL_ROOT / "SKILL.md"

COMMIT = "e5e3d1d83e"
PACK_DATE = "2026-09-22"
TOTAL_CHAPTERS = 66
TOTAL_QUESTS = 4790
PHASES = (
    ("Phase 1 — Early game", 16),
    ("Phase 2 — Mid game", 37),
    ("Phase 3 — Late game", 10),
    ("Phase 4 — Endgame", 3),
)

# Per-chapter quest counts, read from the pack-8.2 config (AllTheMods/ATM-10 at main
# e5e3d1d83e, config/ftbquests/quests/chapters/*.snbt). The sum must stay 4,790.
VERIFIED_QUEST_COUNTS = {
    "welcome": 6,
    "bounty_board": 50,
    "building_tips": 91,
    "tips_and_tricks": 23,
    "mainquestline_part_1": 36,
    "allthemodium": 54,
    "chapter_2_the_star": 128,
    "achapter_2r_6the_atm_star": 38,
    "apotheosis_gear": 30,
    "artifacts": 50,
    "basic_armor": 128,
    "basic_tools": 77,
    "mahou_tsukai": 35,
    "relics": 26,
    "silent_gear": 69,
    "storage": 90,
    "applied_energistics_2": 74,
    "extended__advanced_ae": 56,
    "refined_storage": 72,
    "basic_logistics": 40,
    "integrated_dynamics": 28,
    "modular_router": 55,
    "pylons": 13,
    "apotheosis_2": 36,
    "food_and_farming": 35,
    "hostile_neural_networks": 50,
    "elmystical_agriculturerr": 191,
    "productive_bees": 252,
    "productive_trees": 167,
    "create": 89,
    "draconic_evolution": 140,
    "immersive_engineering": 127,
    "industrial_foregoing": 78,
    "justdirethings": 154,
    "mekanism": 90,
    "mekanism_reactors": 94,
    "oritech": 56,
    "xycraft": 27,
    "pneumaticcraft": 127,
    "railcraft": 52,
    "mi_steam": 30,
    "mi_electric": 50,
    "mi_digital": 66,
    "mi_endgame": 25,
    "basic_power": 34,
    "extreme_reactors": 33,
    "generators": 47,
    "powah": 109,
    "apothic_enchanting": 58,
    "ars_nouveau": 130,
    "evilcraft": 45,
    "forbidden__arcanus": 62,
    "iron_spells_and_spellbooks": 103,
    "natures_aura": 25,
    "neo_vitae": 49,
    "occultism": 64,
    "theurgy": 45,
    "aether": 73,
    "bumblezone": 114,
    "auroral": 21,
    "cataclysm": 110,
    "deeper_and_darker": 45,
    "eternal_starlight": 193,
    "ice__fire": 87,
    "twilight_forest": 56,
    "undergarden": 82,
}

ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*"                 # # column
    r"\|\s*(.+?)\s*"                  # chapter title
    r"\|\s*`([a-z0-9_]+)`\s*"         # chapter id in backticks
    r"\|\s*(.+?)\s*"                  # group
    r"\|\s*(\d+)\s*"                  # quest count
    r"\|\s*(early-game|tech|magic|endgame)\s*"  # stage tag
    r"\|\s*(.+?)\s*\|\s*$",           # the one-line description
    re.UNICODE,
)


def clean_title(title: str) -> str:
    """Match the example file's escaped ampersands to the doc's plain ones."""
    return title.replace("\\", "").strip()


class TestProgressionRoadmapDoc(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.missing = not ROADMAP_MD.is_file()
        cls.text = "" if cls.missing else ROADMAP_MD.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()
        with EXAMPLE_DATA.open(encoding="utf-8") as fh:
            cls.example = json.load(fh)
        cls.example_by_id = {ch["id"]: ch for ch in cls.example["chapters"]}
        cls.rows = [ROW_RE.match(line) for line in cls.text.splitlines()
                    if ROW_RE.match(line)]

    def setUp(self) -> None:
        self.assertFalse(self.missing, f"missing {ROADMAP_MD}")

    # ---------------------------------------------------------------- existence

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertGreater(len(self.text.strip()), 8000,
                           "progression-roadmap.md looks like a stub")

    def test_doc_names_itself_as_a_play_order_for_all_chapters(self) -> None:
        self.assertIn("recommended play order", self.lower)
        self.assertIn("66 chapters", self.lower)
        self.assertIn("one-line", self.lower)

    # --------------------------------------------------------------- provenance

    def test_provenance_names_the_pack_repo_and_pinned_commit(self) -> None:
        self.assertIn("AllTheMods/ATM-10", self.text)
        self.assertIn(COMMIT, self.text)
        self.assertIn("main", self.lower)
        self.assertIn(PACK_DATE, self.text)
        self.assertIn("pack 8.2", self.text)
        self.assertIn("8.x", self.text)
        self.assertIn("CHANGELOG.md", self.text)

    def test_provenance_names_the_config_files_read(self) -> None:
        for source in ("config/ftbquests/quests/chapters/*.snbt",
                       "chapter_groups.snbt",
                       "lang/en_us/chapter.snbt",
                       "lang/en_us/chapters/*.snbt",
                       "examples/progress.example.json"):
            self.assertIn(source, self.text, f"the provenance table must name {source}")

    def test_provenance_states_the_verified_totals(self) -> None:
        self.assertIn("4,790", self.text)
        self.assertIn("quest count", self.lower)

    def test_provenance_separates_the_skill_stage_table_from_pack_data(self) -> None:
        self.assertIn("stage", self.lower)
        self.assertIn("the quest book has no stage notion", self.lower,
                      "the doc must keep the skill's stage table distinct from pack data")

    # ---------------------------------------------------------- grounding rules

    def test_grounding_rules_are_stated(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lower,
                          f"the roadmap must state the {needle!r} rule")

    def test_order_is_flagged_as_recommendation_not_canon(self) -> None:
        self.assertIn("recommendation, not pack canon", self.lower)
        self.assertGreaterEqual(self.lower.count("recommend"), 3,
                                "the recommendation framing must run through the doc")
        self.assertIn("quests are optional", self.lower,
                      "the doc must carry the pack's own no-gating statement")

    def test_never_invent_rule_covers_ids_recipes_coordinates(self) -> None:
        self.assertIn("no item ids, no recipes, no coordinates", self.lower)
        self.assertIn("nothing here was invented", self.lower)

    # ---------------------------------------------------------------- structure

    def test_key_sections_are_present(self) -> None:
        for section in ("What this page is",
                        "Provenance — everything here was read, not remembered",
                        "Grounding rules",
                        "How the phases map to the skill's stages",
                        "What the pack itself enforces",
                        "Using this document in a session"):
            self.assertIn(section, self.text, f"missing section: {section}")

    def test_four_phase_headings_with_expected_counts(self) -> None:
        for heading, count in PHASES:
            self.assertIn(f"{heading} ({count} chapters)", self.text,
                          f"missing or miscounted phase heading: {heading}")

    def test_phase_counts_sum_to_the_whole_book(self) -> None:
        self.assertEqual(sum(count for _, count in PHASES), TOTAL_CHAPTERS)

    def test_phases_are_named_early_mid_late_endgame(self) -> None:
        for word in ("Early game", "Mid game", "Late game", "Endgame"):
            self.assertIn(word, self.text, f"missing phase name: {word}")

    # ------------------------------------------------------------ chapter rows

    def test_lists_exactly_66_chapter_rows(self) -> None:
        self.assertEqual(len(self.rows), TOTAL_CHAPTERS,
                         "the roadmap must hold exactly one row per chapter")

    def test_rows_are_numbered_one_to_sixty_six_in_order(self) -> None:
        numbers = [int(row.group(1)) for row in self.rows]
        self.assertEqual(numbers, list(range(1, TOTAL_CHAPTERS + 1)))

    def test_every_example_chapter_appears_exactly_once(self) -> None:
        ids = [row.group(3) for row in self.rows]
        self.assertEqual(sorted(ids), sorted(self.example_by_id),
                         "the roadmap's chapters must be exactly the example file's")
        self.assertEqual(len(ids), len(set(ids)), "a chapter id appears twice")

    def test_row_titles_groups_and_stages_match_the_example_file(self) -> None:
        for row in self.rows:
            chapter_id = row.group(3)
            expected = self.example_by_id[chapter_id]
            self.assertEqual(row.group(2), clean_title(expected["title"]),
                             f"{chapter_id}: title drifted from the example file")
            group = row.group(4)
            if expected.get("group"):
                self.assertEqual(group, expected["group"],
                                 f"{chapter_id}: group drifted")
            else:
                self.assertIn("standalone", group,
                              f"{chapter_id}: standalone chapter must be marked")
            self.assertEqual(row.group(6), expected["stage"],
                             f"{chapter_id}: stage drifted from the example file")

    def test_row_quest_counts_match_pack_82(self) -> None:
        self.assertEqual(sum(VERIFIED_QUEST_COUNTS.values()), TOTAL_QUESTS,
                         "the verified-count table itself must sum to the pack total")
        for row in self.rows:
            chapter_id = row.group(3)
            self.assertEqual(int(row.group(5)), VERIFIED_QUEST_COUNTS[chapter_id],
                             f"{chapter_id}: quest count does not match pack 8.2")

    def test_every_row_carries_a_one_line_description(self) -> None:
        for row in self.rows:
            self.assertGreaterEqual(len(row.group(7)), 20,
                                    f"{row.group(3)}: description looks empty")

    def test_phase_1_holds_exactly_the_early_game_chapters(self) -> None:
        first_16 = {row.group(3) for row in self.rows[:16]}
        expected = {ch["id"] for ch in self.example["chapters"]
                    if ch["stage"] == "early-game"}
        self.assertEqual(first_16, expected,
                         "phase 1 must be exactly the skill's early-game chapters")

    def test_phase_4_holds_the_main_questline_finale_in_book_numbering(self) -> None:
        last_3 = [row.group(3) for row in self.rows[-3:]]
        self.assertEqual(last_3, ["allthemodium", "chapter_2_the_star",
                                  "achapter_2r_6the_atm_star"],
                         "the endgame phase must run Chapter 2 → 3 → 4")

    def test_mid_game_phase_holds_tech_and_magic_chapters(self) -> None:
        mid = {row.group(3) for row in self.rows[16:53]}
        expected = {ch["id"] for ch in self.example["chapters"]
                    if ch["stage"] in ("tech", "magic")}
        self.assertEqual(mid, expected,
                         "phase 2 must be exactly the tech and magic chapters")

    def test_late_game_phase_holds_the_endgame_explorers_and_draconic(self) -> None:
        late = {row.group(3) for row in self.rows[53:63]}
        expected = {ch["id"] for ch in self.example["chapters"]
                    if ch["stage"] == "endgame"
                    and ch["id"] not in ("allthemodium", "chapter_2_the_star",
                                         "achapter_2r_6the_atm_star")}
        self.assertEqual(late, expected,
                         "phase 3 must be the endgame chapters outside the Main Questline")

    # ------------------------------------------------------- grounded specifics

    def test_quotes_verified_quest_titles_from_each_phase(self) -> None:
        # One or two config-verified titles per phase, quoted in the doc.
        for title in ("Stone Age",                      # phase 1 (Chapter 1)
                      "Basic Ore Doubling",             # phase 1 (Chapter 1)
                      "Andesite Alloys",                # phase 2 (Create)
                      "Fission Reactor",                # phase 2 (Mekanism: Reactors)
                      "The Energizing Orb",             # phase 2 (Powah)
                      "Kill the Chaos Guardian",        # phase 3 (Draconic Evolution)
                      "Valkyrie Queen",                 # phase 3 (The Aether)
                      "ATM Star",                       # phase 4 (the star itself)
                      "Fully Automated ATM Star"):      # phase 4 (Chapter 4)
            self.assertIn(title, self.text,
                          f"the roadmap should quote the verified title {title!r}")

    def test_names_the_only_verified_cross_chapter_dependencies(self) -> None:
        self.assertIn("five cross-chapter dependency links", self.lower)
        for name in ("Electric Age", "Steam Age", "Digital Age", "End Game",
                     "Apothic Enchanting", "Apotheosis Gear"):
            self.assertIn(name, self.text,
                          f"the dependency list must name {name}")

    def test_says_main_questline_numbering_is_the_packs(self) -> None:
        for title in ("Chapter 1: The Beginning", "Chapter 2: Allthemodium",
                      "Chapter 3: The ATM Star", "Chapter 4: Creative"):
            self.assertIn(title, self.text, f"the spine must be named: {title}")

    def test_marks_untitled_chapters_instead_of_inventing_names(self) -> None:
        flat = re.sub(r"\s+", " ", self.lower)
        self.assertIn("untitled in the config", flat,
                      "chapters with mostly untitled quests must be marked as such")

    # --------------------------------------------------------- cross-references

    def test_cross_references_the_sibling_docs(self) -> None:
        for name in ("references/progression.md", "references/key-mods.md",
                     "references/atm-star-checklist.md", "references/boss-checklist.md",
                     "references/creative-checklist.md"):
            self.assertIn(name, self.text, f"the roadmap must point at {name}")

    def test_explains_how_it_differs_from_quest_book_order(self) -> None:
        self.assertIn("quest-book order", self.lower)
        self.assertIn("scripts/progress.py", self.text)

    # ------------------------------------------------------------------ SKILL.md

    def test_skill_md_documents_the_roadmap(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/progression-roadmap.md", skill,
                      "SKILL.md must point at the roadmap")
        self.assertIn("recommendation", skill.lower(),
                      "SKILL.md must carry the recommendation-not-canon caveat")


if __name__ == "__main__":
    unittest.main()
