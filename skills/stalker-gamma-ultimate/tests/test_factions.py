#!/usr/bin/env python3
"""Grounding checks for `references/factions.md`.

Faction behaviour in GAMMA is `creatures/game_relations.ltx` (the
`[communities_relations]` / `[reputation_relations]` matrices and the
rank/reputation/goodwill ladders), plus the per-faction trader files whose
`buy_supplies` lines gate stock on faction goodwill. This suite pins the
identifiers, the goodwill thresholds and the supply ladder.

Run with the standard library only, offline:

    python3 tests/test_factions.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "factions.md"


class FactionsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "game_relations.ltx",
            "[communities_relations]",
            "new_game_start_locations.ltx",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_faction_count(self):
        self.assertIn("13", self.text)
        for faction in ("Duty", "Freedom", "Monolith", "Mercenary", "Clear Sky", "Bandit"):
            with self.subTest(faction=faction):
                self.assertIn(faction, self.text)

    def test_goodwill_constants(self):
        for value in ("goodwill_enemy = -1000", "goodwill_friend = 1000"):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_supply_gating_condition(self):
        self.assertIn("actor_goodwill_ge(stalker:2000)", self.text)
        self.assertIn("supplies_5", self.text)
        self.assertIn("supplies_2", self.text)

    def test_supply_tier_contents(self):
        self.assertIn("supply_1_wp", self.text)
        self.assertIn("supply_5_wp", self.text)
        self.assertIn("recipe_exo_1", self.text)

    def test_attitude_formula(self):
        self.assertIn("attitude", self.text)
        self.assertIn("community_goodwill", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/trading-economy.md",
            "references/quests-storylines.md",
            "references/armor-outfits.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
