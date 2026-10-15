#!/usr/bin/env python3
"""Grounding checks for `references/ballistics-damage.md`.

The combat-model page quotes four independent sources: the in-game manual's
*Ballistics System* article, the pack's `gamma_ammo_weapon_table.xlsx`, the
GAMMA patch files (`mod_system_actor_hitbox.ltx`, `mod_system_bleed_rework.ltx`,
`mod_system_items_armors_br_class_rework.ltx`) and `Patchnotes.md` 0.9.5. This
suite pins the ammunition identifiers, the BR-scale endpoints and the 0.9.5
caps so a rewrite cannot paraphrase a number into something the game does not
do.

Run with the standard library only, offline:

    python3 tests/test_ballistics_damage.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "ballistics-damage.md"


class BallisticsDamageDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "GROBBS",
            "gamma_ammo_weapon_table.xlsx",
            "mod_system_actor_hitbox.ltx",
            "mod_system_bleed_rework.ltx",
            "article_gamma_ballistics_text",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_br_scale_endpoints(self):
        self.assertIn("0.17", self.text)
        self.assertIn("0.80", self.text)
        self.assertIn("7.62×54R", self.text)
        for tier in ("BR1", "BR5", "BR6"):
            with self.subTest(tier=tier):
                self.assertIn(tier, self.text)

    def test_ammo_rows_are_quoted_from_the_table(self):
        for value in (
            "ammo_9x19_fmj",
            "ammo_9x19_ap",
            "ammo_7.62x54_ap",
            "ammo_12x70_buck",
            "ammo_12x76_zhekan",
            "ammo_k_ap",
            "ammo_k_hit",
        ):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_player_hitbox_count(self):
        self.assertIn("hitbox", self.text.lower())
        self.assertIn("three", self.text)

    def test_bleed_rework_values(self):
        self.assertIn("boost_bleeding_restore", self.text)
        self.assertIn("bleed_speed_k", self.text)
        self.assertIn("Tourniquet", self.text)

    def test_zero_nine_five_caps(self):
        self.assertIn("90 %", self.text)
        self.assertIn("BRC", self.text)
        self.assertIn("+3 % BRC", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/weapons.md",
            "references/armor-outfits.md",
            "references/mutants.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
