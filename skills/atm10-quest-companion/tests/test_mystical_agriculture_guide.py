#!/usr/bin/env python3
"""Offline contract for the Mystical Agriculture guide (guide #21).

The fixture is intentionally frozen here: no checkout or network is needed at test time.
Every title, id and count asserted below is carried over from
references/farming-guide.md, which was read from the AllTheMods/ATM-10 repository at
`main` commit e5e3d1d83e (2026-09-22, pack 8.2) -- the quest chapters
elmystical_agriculturerr (quest file + lang/en_us) and config/crash_assistant/modlist.json.
The Mystical Agriculture guide re-quotes that snapshot rather than re-reading the repo, so
this test pins the parts that must not drift: the tier titles, their ids, and the rule that
unverified labels are never presented as quest titles.

Run from the skill directory:

    python -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references" / "mystical-agriculture-guide.md"
FARMING = ROOT / "references" / "farming-guide.md"
SKILL = ROOT / "SKILL.md"

# (title, quest id) pairs the farming snapshot records together -- (id not in the snapshot)
# titles are listed separately, below.
VERIFIED_IDS = (
    ("Mystical Agriculture!", "54735C5FCD2077B3"),
    ("Inferium", "1CC4F8570A7A99EB"),
    ("Prudentium", "73350AD668200E99"),
    ("Tertium", "2C9C9CB71941DC01"),
    ("Imperium", "66C52B137A4FF869"),
    ("Supremium", "67DBE6C59C0D9D1B"),
    ("Awakened Supremium", "7A103577EAE7B3F1"),
    ("Insanium", "202B1F54D3F06DAB"),
    ("Creative Essence", "6D0A876D4E4D35AB"),
    ("Inferium Farmland", "7DFF18CFEB0B8DBE"),
    ("Infusion Crystal", "217DB12EA32E1724"),
    ("Infusion Altar", "0B37355262121DD5"),
    ("Prosperity Shards", "2DDA04088C8220D2"),
    ("Prosperity Seed Base", "1E0F92F07FDD162E"),
)

# Verified titles the snapshot carries without an id, plus the two optional quests.
TITLES_WITHOUT_ID = (
    "Creating Mob Seeds",
    "The Awakening",
    "Cognizant Dust",
    "Master Infusion Crystal",
    "Mystical Fertilizer",
    "Automating Awakened Supremium",
    "Wand",
)

ALL_TITLES = tuple(row[0] for row in VERIFIED_IDS) + TITLES_WITHOUT_ID

# Essence ladder in the chapter's own dependency order.
LADDER = ("Inferium", "Prudentium", "Tertium", "Imperium", "Supremium",
          "Awakened Supremium", "Insanium", "Creative Essence")


class TestMysticalAgricultureGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUIDE.read_text(encoding="utf-8")
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.lines = cls.text.splitlines()

    def test_file_exists_and_not_empty(self):
        self.assertTrue(GUIDE.is_file(), "references/mystical-agriculture-guide.md is missing")
        self.assertGreater(len(self.text.strip()), 2000, "guide looks truncated")
        self.assertGreater(len(self.lines), 40)

    def test_minimum_short_answer_heading(self):
        self.assertTrue(self.lines[0].startswith("# "), "guide must open with an H1 title")
        self.assertIn("ATM10", self.lines[0])
        starts = [i for i, line in enumerate(self.lines[:16])
                  if line.startswith("**Short answer")]
        self.assertEqual(len(starts), 1, "exactly one bolded short-answer paragraph near the top")
        block = []
        for line in self.lines[starts[0]:]:
            if not line.strip():
                break
            block.append(line)
        short = " ".join(block)
        self.assertIn("judgement, not a quest requirement", short)
        self.assertIn("Mystical Agriculture", short)
        self.assertIn("Mystical Agradditions", short)
        self.assertGreaterEqual(len(block), 4, "short answer should be a full paragraph")
        for heading in ("## Provenance and limits",
                        "## What to do first (*judgement*):",
                        "## Cross-references"):
            self.assertIn(heading, self.text)

    def test_section_basic(self):
        for tier in LADDER:
            self.assertIn("“" + tier + "”", self.text)
        for needle in ("Mystical Agriculture 8.0.28", "Mystical Agradditions 8.0.14",
                       "e5e3d1d83e", "2026-09-22", "pack 8.2",
                       "config/ftbquests/quests/chapters/", "lang/en_us/chapters/",
                       "config/crash_assistant/modlist.json",
                       "in-game quest book is authoritative", "JEI",
                       "references/farming-guide.md", "Tier: Magical",
                       "mysticalagradditions:insanium_essence",
                       "mysticalagriculture:inferium_essence",
                       "mysticalagriculture:soul_jar",
                       "mysticalagriculture:awakened_supremium_ingot_block",
                       "Creative Essence is needed to craft the ATM Star."):
            self.assertIn(needle, self.text, needle)

    def test_verified_ids_are_attached_to_the_right_titles(self):
        self.assertEqual(len({row[1] for row in VERIFIED_IDS}), len(VERIFIED_IDS))
        for title, quest_id in VERIFIED_IDS:
            with self.subTest(title=title):
                self.assertRegex(self.text,
                                 re.escape("“" + title + "”") +
                                 r"[^\n]{0,80}" +
                                 re.escape("`" + quest_id + "`"))

    def test_no_invented_quest_titles_or_ids(self):
        # Every typographic quoted label is a title the snapshot verified.
        quoted = set(re.findall(r"“([^”]+)”", self.text))
        self.assertEqual(quoted, set(ALL_TITLES))
        # Every 16-hex id is one the farming snapshot recorded.
        ids = set(re.findall(r"`([0-9A-F]{16})`", self.text))
        self.assertEqual(ids, {row[1] for row in VERIFIED_IDS})
        for fabricated in ("Supremium Armor quest", "Awakened Supremium Armor",
                           "Insanium Armor", "Mystical Agriculture Armor quest",
                           "Essence Farmland quest", "Hyperbox quest", "ARMOR quest"):
            self.assertNotIn(fabricated, self.text)

    def test_untitled_quests_are_marked_as_untitled(self):
        # Gear and helper entries carry no title in the config: the guide must say so
        # rather than dress an item name up as a quest title.
        self.assertGreaterEqual(self.text.count("no title in the config"), 5)
        self.assertIn("no verified armor, tool, or", self.text)
        self.assertIn("not a title", self.text)
        self.assertIn("(id not in the snapshot)", self.text)

    def test_judgement_is_labelled_and_not_a_claimed_requirement(self):
        for needle in ("judgement", "not a quest requirement", "no recipe",
                       "No recipe", "no verified best layout",
                       "does **not** tell the player"):
            self.assertIn(needle, self.text.lower() if needle.islower() else needle)
        self.assertIn("## What to do first (*judgement*):", self.text)
        # It must not claim the tier order is a quest requirement.
        for overclaim in ("you must start with Inferium", "required to farm",
                          "the quest requires you to"):
            self.assertNotIn(overclaim, self.text.lower())

    def test_skill_md_points_at_the_guide(self):
        self.assertIn("references/mystical-agriculture-guide.md", self.skill)
        self.assertTrue(FARMING.is_file(), "sibling farming guide went missing")


if __name__ == "__main__":
    unittest.main()
