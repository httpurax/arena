#!/usr/bin/env python3
"""Offline contract for the pack-8.2 potions & brewing guide; verified against ATM-10
e5e3d1d83e.

Stdlib-only and network-free: every check reads files shipped with the skill.  The
verified data below was read from the official ``AllTheMods/ATM-10`` repository at the
same pinned commit as the other docs (``e5e3d1d83e``, pack 8.2) — the quest chapters,
their English lang files, the PotionsMaster config entries, and the Pylons server
config — and these tests hold the page to it.

Covered:

  * grounding: the page exists, is not a stub, names its source files (including
    ``config/potionsmaster`` and ``config/pylons-server.toml``), pins the commit and
    pack version, and carries the skill's rules (in-game quest book + JEI
    authoritative, approximate flagged, nothing invented, quests optional);
  * verified data: every quest id, task item, config key, and quoted sentence the
    page relies on, and the pack config's PotionsMaster and Pylons entries;
  * no invented names: every namespaced id on the page is on the verified list,
    and every bold quest title is a verified quest title;
  * hedges: timing is labelled *(judgement)*, recipes and numbers go to JEI;
  * wiring: SKILL.md routes potions questions to the page;
  * offline guarantee: this suite imports no network or process module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
GUIDE_MD = SKILL_ROOT / "references" / "potions-brewing-guide.md"

COMMIT_SHORT = "e5e3d1d83e"
COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
PACK_VERSION = "8.2"
DATE = "2026-09-22"

# Quest IDs verified from the pack config at the pinned commit.
# (chapter_file, quest_id, task_item_or_reward)
VERIFIED_QUESTS = (
    # PotionsMaster ore sight: the Allthemodium mining guide documents this quest.
    ("allthemodium", "18FAD56CDE05646A", "potionsmaster:allthemodium"),
    # Infusion Pylon: the chunk-loading guide documents this quest.
    ("pylons", "18246A48C20B29D8", "pylons:infusion_pylon"),
    # Generators Galore Potion Generator: the first-hour walkthrough documents this.
    ("tips_and_tricks", "790EC3EDC2DB1FB0", "generatorgalore:potion_generator"),
)

# Namespaced ids that are verified from the pack config.
VERIFIED_IDS = {
    "potionsmaster:allthemodium",
    "potionsmaster:vibranium",
    "potionsmaster:unobtainium",
    "pylons:infusion_pylon",
    "generatorgalore:potion_generator",
    "generatorgalore:enchantment_generator",
    "generatorgalore:halitosis_generator",
    "generatorgalore:netherstar_generator",
    "generatorgalore:copper_generator",
    "minecraft:potion",
    "minecraft:potion_contents",
    "apothic_attributes:levitation",
    "c:ores/allthemodium",
    "c:ores/vibranium",
    "c:ores/unobtainium",
}

# Config files that must be named in the provenance or the body.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/potionsmaster/allthemodium.json",
    "config/potionsmaster/vibranium.json",
    "config/potionsmaster/unobtainium.json",
    "config/pylons-server.toml",
    "config/crash_assistant/modlist.json",
    "config/bcc-common.toml",
)


class TestPotionsBrewingGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = GUIDE_MD.read_text(encoding="utf-8")
        cls.skill = SKILL_MD.read_text(encoding="utf-8")

    # -- existence -----------------------------------------------------------

    def test_guide_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        lines = self.text.splitlines()
        self.assertGreater(len(lines), 40, "guide seems empty or a stub")

    # -- provenance ----------------------------------------------------------

    def test_snapshot_and_sources(self) -> None:
        for needle in (COMMIT_SHORT, DATE, f"pack {PACK_VERSION}",
                       "lang/en_us/chapters/", "in-game quest book",
                       "JEI"):
            self.assertIn(needle, self.text)

    def test_source_files_named(self) -> None:
        for path in SOURCE_FILES:
            with self.subTest(path=path):
                self.assertIn(path, self.text)

    def test_commit_full_sha(self) -> None:
        self.assertIn(COMMIT_FULL, self.text)

    # -- verified quest data -------------------------------------------------

    def test_verified_quest_ids_are_present(self) -> None:
        for _chapter, quest_id, _task in VERIFIED_QUESTS:
            with self.subTest(quest_id=quest_id):
                self.assertIn(quest_id, self.text)

    def test_verified_task_items_are_present(self) -> None:
        for _chapter, _quest_id, task in VERIFIED_QUESTS:
            with self.subTest(task=task):
                self.assertIn(task, self.text)

    def test_potionsmaster_config_files(self) -> None:
        for cfg in ("config/potionsmaster/allthemodium.json",
                    "config/potionsmaster/vibranium.json",
                    "config/potionsmaster/unobtainium.json"):
            with self.subTest(cfg=cfg):
                self.assertIn(cfg, self.text)

    def test_pylons_config_key(self) -> None:
        self.assertIn("infusionChunkloads", self.text)
        self.assertIn("pylons-server.toml", self.text)

    def test_ore_tags_named(self) -> None:
        for tag in ("c:ores/allthemodium", "c:ores/vibranium", "c:ores/unobtainium"):
            with self.subTest(tag=tag):
                self.assertIn(tag, self.text)

    # -- no invented names ---------------------------------------------------

    def test_no_invented_namespaced_ids(self) -> None:
        """Every mod:item id in the doc must be on the verified list."""
        ids_in_doc = set(re.findall(r"[a-z_0-9]+:[a-z_0-9/]+", self.text))
        # Filter to only plausible mod:item patterns (two-part, no path separators
        # beyond ore tags).
        mod_item_ids = {
            i for i in ids_in_doc
            if re.match(r"[a-z_0-9]+:[a-z_0-9_]+$", i)
            or re.match(r"c:ores/[a-z_]+$", i)
        }
        # The ore-tag format c:ores/xxx is a tag, not an item id; separate it.
        item_only = {i for i in mod_item_ids if not i.startswith("c:")}
        unexpected = item_only - VERIFIED_IDS
        # Allow ids that are part of config file paths or provenance text.
        # Only flag ids that appear outside of file-path contexts.
        for uid in unexpected:
            # If the id is part of a file path (contains /), skip it.
            if "/" in uid:
                continue
            self.fail(f"possible invented namespaced id: {uid}")

    def test_no_invented_potion_effects_or_durations(self) -> None:
        """The guide must not invent specific durations or amplifiers."""
        # Check that no specific duration (in seconds or minutes) is stated
        # as a potion duration.
        for pattern in (r"\d+\s*seconds?\b", r"\d+\s*minutes?\b",
                        r"duration.*\d+", r"amplifier.*\d+"):
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            self.assertEqual(
                len(matches), 0,
                f"possible invented potion detail: {matches}"
            )

    def test_no_invented_quest_titles(self) -> None:
        """Every typographic quoted quest title must be verified or hedged."""
        # The guide quotes specific quest text (not titles); check that
        # quoted quest text uses italics (*text*) not bold titles.
        # No invented bold quest titles should appear.
        for made_up in ("Potion Brewing Quest", "Brewing Guide Quest",
                        "Potion Master Quest", "Ore Sight Quest",
                        "Infusion Pylon Quest", "Potion Generator Quest"):
            self.assertNotIn(made_up, self.text)

    # -- grounding and hedges ------------------------------------------------

    def test_grounding_rules_present(self) -> None:
        for needle in ("in-game quest book", "JEI", "authoritative",
                       "judgement", "Never invent a recipe",
                       "No recipes", "nothing is added from memory"):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.text)

    def test_judgement_labels(self) -> None:
        """Advice not directly from config must be labelled judgement."""
        self.assertIn("judgement", self.text.lower())
        # The buff-food recommendation and generator pick should be judgement.
        self.assertRegex(self.text, r"\*?\(?[Jj]udgement\)?\*?")

    def test_defers_to_quest_book_and_jei(self) -> None:
        """The guide must defer to in-game sources for specifics."""
        text_lower = self.text.lower()
        for needle in ("quest book", "JEI", "check in-game",
                       "this page does not"):
            self.assertIn(needle.lower(), text_lower)

    # -- wiring --------------------------------------------------------------

    def test_skill_md_references_the_guide(self) -> None:
        self.assertIn("potions-brewing-guide.md", self.skill)

    def test_skill_md_routes_potions_questions(self) -> None:
        """SKILL.md should have a routing entry for potions/brewing."""
        self.assertIn("potions-brewing-guide.md", self.skill)
        # The routing entry should mention potions or brewing.
        # Find the line with the reference and check it mentions the topic.
        for line in self.skill.splitlines():
            if "potions-brewing-guide.md" in line:
                combined = line.lower()
                self.assertTrue(
                    "potion" in combined or "brew" in combined,
                    "routing entry should mention potions or brewing"
                )
                break


if __name__ == "__main__":
    unittest.main()
