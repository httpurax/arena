#!/usr/bin/env python3
"""Offline contract for the pack-8.2 base guide; verified against ATM-10 e5e3d1d83e.

The fixture is intentionally frozen here: no checkout or network is needed at test time.
IDs/titles were read from config/ftbquests/quests/lang/en_us/chapters/*.snbt
and checked in config/ftbquests/quests/chapters/*.snbt at that commit.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references" / "base-spots-guide.md"
SKILL = ROOT / "SKILL.md"

# (English config file, quest or task, ID, explicit English title stripped of & codes)
VERIFIED = (
    ("allthemodium", "quest", "2C4299D33D419AA0", "Overworld"),
    ("allthemodium", "quest", "07FDA46D83F8360D", "Teleport Pad"),
    ("allthemodium", "quest", "6D738730B371B152", "Mining Dimension"),
    ("allthemodium", "task", "681CB7DF06F2F506", "Visit The Mining Dimension"),
    ("welcome", "task", "103C42C743E2A2DB", "Claiming Chunks"),
    ("building_tips", "quest", "0539AF15A10B2859", "Compact Machines"),
)
UNTITLED = ("applied_energistics_2", "quest", "2897FA291E5A38D8")


class TestBaseSpotsGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUIDE.read_text(encoding="utf-8")
        cls.skill = SKILL.read_text(encoding="utf-8")

    def test_snapshot_and_sources(self):
        for needle in ("e5e3d1d83e", "2026-09-22", "pack 8.2", "lang/en_us/chapters/",
                       "config/hyperbox-common.toml", "auto_force_hyperbox_chunks = false",
                       "in-game quest book is authoritative", "JEI"):
            self.assertIn(needle, self.text)

    def test_verified_titles_are_attached_to_the_correct_ids(self):
        self.assertEqual(len({row[2] for row in VERIFIED}), len(VERIFIED))
        for chapter, kind, quest_id, title in VERIFIED:
            with self.subTest(chapter=chapter, kind=kind, title=title):
                self.assertRegex(self.text, re.escape("“" + title + "”") +
                                 r"[^\n]{0,80}" + re.escape("`" + quest_id + "`"))
        self.assertIn("`" + UNTITLED[2] + "`", self.text)
        self.assertIn("no explicit quest title", self.text)

    def test_no_fictional_quest_titles_or_ids(self):
        # Every typographic quoted label is one of the explicit titles above.
        quoted = set(re.findall(r"“([^”]+)”", self.text))
        self.assertEqual(quoted, {row[3] for row in VERIFIED})
        ids = set(re.findall(r"`([0-9A-F]{16})`", self.text))
        self.assertEqual(ids, {row[2] for row in VERIFIED} | {UNTITLED[2]})
        for made_up in ("Hyperbox quest", "Compact Machine Base", "Mining Base Quest",
                        "Chunk Loader quest", "Spatial Anchor quest"):
            self.assertNotIn(made_up, self.text)

    def test_choice_is_advice_not_a_claimed_requirement(self):
        for needle in ("Overworld", "Mining Dimension", "Compact Machines", "judgement",
                       "not a quest requirement", "not a quoted quest title",
                       "**not** evidence that Compact Machines behave the same way",
                       "No recipe", "no verified best coordinate"):
            self.assertIn(needle, self.text)
        self.assertIn("references/base-spots-guide.md", self.skill)
        self.assertIn("version: 1.4.0", self.skill)


if __name__ == "__main__":
    unittest.main()
