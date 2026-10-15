#!/usr/bin/env python3
"""Grounding checks for `references/crafting-repairs.md`.

The crafting page is anchored on the in-game manual's *Crafting*, *Repairs for
Guns*/*Repairs for Armor* and *Disassembly* articles, the pack's own
`toolkits_chance.xlsx`, `craft.ltx` and `mod_system_grok_recipes.ltx`. This
suite pins the six toolkit tiers, the portable-workbench interaction, the
`max_uses = 3` repair-kit setting and the recipe-book cost ladder.

Run with the standard library only, offline:

    python3 tests/test_crafting_repairs.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "crafting-repairs.md"


class CraftingRepairsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "toolkits_chance.xlsx",
            "mod_system_grok_recipes.ltx",
            "article_gamma_crafting_text",
            "article_gamma_cooking_text",
            "article_gamma_repgun_text",
            "article_gamma_reparm_text",
            "article_gamma_inventory_text",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_six_toolkit_tiers(self):
        self.assertIn("6 types of toolkits", self.text)
        for tier in ("Basic", "Advanced", "Expert", "Medical", "Ammo"):
            with self.subTest(tier=tier):
                self.assertIn(tier, self.text)

    def test_portable_workbench_interaction(self):
        self.assertIn("Right click any toolkit", self.text)
        self.assertIn("portable workbench", self.text)

    def test_expert_toolkit_map_rule(self):
        self.assertIn("Red Forest", self.text)

    def test_repair_kit_uses(self):
        self.assertIn("max_uses = 3", self.text)

    def test_percent_thresholds(self):
        self.assertIn("60 %", self.text)
        self.assertIn("65 %", self.text)

    def test_per_map_toolkit_chances(self):
        for map_id in ("l06_rostok", "l07_military", "pripyat", "zaton"):
            with self.subTest(map_id=map_id):
                self.assertIn(map_id, self.text)

    def test_recipe_books_and_cost_ladder(self):
        self.assertIn("recipe_advanced_1", self.text)
        self.assertIn("recipe_expert_2", self.text)
        self.assertIn("recipe_expert_4", self.text)
        self.assertIn("99 000", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/weapons.md",
            "references/armor-outfits.md",
            "references/artifacts.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
