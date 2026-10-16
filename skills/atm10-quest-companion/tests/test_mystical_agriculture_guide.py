#!/usr/bin/env python3
"""Offline contract for guide #21: the Mystical Agriculture progression guide.

The fixture is intentionally frozen here: no checkout or network is needed at test time.
Every quoted title, id, and sentence in the guide was read from the pack-8.2 snapshot of
config/ftbquests/quests/{,lang/en_us/}chapters/elmystical_agriculturerr.snbt (commit
e5e3d1d83e) and is already printed in references/farming-guide.md.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references" / "mystical-agriculture-guide.md"

# (verified quest title, quest id) — titles are the config's, ids are 16 hex characters.
VERIFIED = (
    ("Mystical Agriculture!", "54735C5FCD2077B3"),
    ("Inferium", "1CC4F8570A7A99EB"),
    ("Inferium Farmland", "7DFF18CFEB0B8DBE"),
    ("Infusion Crystal", "217DB12EA32E1724"),
    ("Prosperity Shards", "2DDA04088C8220D2"),
    ("Prosperity Seed Base", "1E0F92F07FDD162E"),
    ("Infusion Altar", "0B37355262121DD5"),
    ("Prudentium", "73350AD668200E99"),
    ("Tertium", "2C9C9CB71941DC01"),
    ("Imperium", "66C52B137A4FF869"),
    ("Supremium", "67DBE6C59C0D9D1B"),
    ("Awakened Supremium", "7A103577EAE7B3F1"),
    ("Insanium", "202B1F54D3F06DAB"),
    ("Creative Essence", "6D0A876D4E4D35AB"),
)

# Item ids are allowed in backticks; quest ids must be 16 uppercase hex characters.
NON_QUEST_HEX = ("e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025",)


class TestMysticalAgricultureGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUIDE.read_text(encoding="utf-8")

    def test_file_exists_and_not_empty(self):
        self.assertTrue(GUIDE.is_file(), "references/mystical-agriculture-guide.md is missing")
        self.assertGreater(len(self.text.strip()), 800)
        self.assertTrue(self.text.startswith("# "), "the guide must open with an H1")

    def test_minimum_short_answer_heading(self):
        self.assertIn("**Short answer (judgement, not a quest requirement):**", self.text)
        self.assertIn("**What to do first (*judgement*):**", self.text)
        # The short answer sits above every section, as in the base-spots guide.
        short = self.text.index("**Short answer")
        first_h2 = self.text.index("\n## ")
        self.assertLess(short, first_h2)

    def test_section_basic(self):
        for heading in ("## Provenance and limits", "## The choices",
                        "## Getting more essence", "## Where this crosses into other guides",
                        "**What to do first (*judgement*):**"):
            self.assertIn(heading, self.text)
        for needle in ("e5e3d1d83e", "2026-09-22", "pack 8.2",
                       "Mystical Agriculture 8.0.28", "Mystical Agradditions 8.0.14",
                       "elmystical_agriculturerr", "config/crash_assistant/modlist.json",
                       "in-game quest book is authoritative", "JEI", "judgement"):
            self.assertIn(needle, self.text)
        self.assertGreaterEqual(self.text.count("|---|"), 3,
                                "the template tables (choices, get-more) must be present")

    def test_essence_ladder_is_complete_and_in_order(self):
        for tier in ("Inferium", "Prudentium", "Tertium", "Imperium", "Supremium",
                     "Awakened Supremium", "Insanium", "Creative Essence"):
            self.assertIn(tier, self.text)
        ladder = ("Inferium", "Prudentium", "Tertium", "Imperium", "Supremium",
                  "Awakened Supremium", "Insanium", "Creative Essence")
        rows = [self.text.index("| **%s**" % tier) for tier in ladder]
        self.assertEqual(rows, sorted(rows),
                         "the tier table must run Inferium -> Creative Essence")

    def test_verified_titles_are_attached_to_the_correct_ids(self):
        self.assertEqual(len({row[1] for row in VERIFIED}), len(VERIFIED))
        for title, quest_id in VERIFIED:
            with self.subTest(title=title):
                self.assertRegex(self.text, re.escape("**" + title + "**") +
                                 r"[^\n]{0,120}" + re.escape("`" + quest_id + "`"))

    def test_no_invented_ids_recipes_or_armor_claims(self):
        ids = set(re.findall(r"`([0-9A-F]{16})`", self.text))
        self.assertEqual(ids, {row[1] for row in VERIFIED})
        for blob in NON_QUEST_HEX:
            self.assertNotIn("`%s`" % blob, self.text)
        self.assertIn("no unverified armor set claim", self.text)
        self.assertIn("no verified best plot size", self.text)
        for invented in ("Supremium Armor quest", "Essence Armor quest", "Tertium Armor quest",
                         "growth accelerator pylon", "resource chicken"):
            self.assertNotIn(invented, self.text)

    def test_cross_references_point_at_existing_guides(self):
        self.assertIn("references/farming-guide.md", self.text)
        refs = set(re.findall(r"references/([a-z0-9-]+\.md)", self.text))
        self.assertGreaterEqual(len(refs), 10)
        for name in sorted(refs):
            with self.subTest(reference=name):
                self.assertTrue((ROOT / "references" / name).is_file(),
                                "dangling cross-reference: references/%s" % name)


if __name__ == "__main__":
    unittest.main()
