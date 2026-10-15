#!/usr/bin/env python3
"""Grounding checks for `references/quests-storylines.md`.

GAMMA ships its quests through addons (`197- New Storylines`, the story-artefact
config `mod_system_storylines.ltx`, ZCP spawn changes) and documents them in the
manual's *Storylines & Missions* and *Stashes* articles. This suite pins the
storyline list, the story-artefact identifiers and the stash rules that the
guide quotes verbatim.

Run with the standard library only, offline:

    python3 tests/test_quests_storylines.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "quests-storylines.md"


class QuestsStorylinesDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "article_gamma_story_text",
            "article_gamma_stashes_text",
            "mod_system_storylines.ltx",
            "New Storylines",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_story_artefacts_are_quest_items(self):
        for value in ("af_ah_o1", "af_ah_o2", "SCRPTART", "can_trade = false", "cost = 4000"):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_character_creation_keys(self):
        self.assertIn("[character_creation]", self.text)

    def test_stash_rules_are_quoted(self):
        self.assertIn("Unmarked stashes are almost always empty", self.text)
        self.assertIn("Stashes must be marked", self.text)
        self.assertIn("stash_chance", self.text)

    def test_task_types_and_progression(self):
        self.assertIn("task", self.text.lower())
        self.assertIn("stash", self.text.lower())

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/factions.md",
            "references/crafting-repairs.md",
            "references/trading-economy.md",
            "references/troubleshooting.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
