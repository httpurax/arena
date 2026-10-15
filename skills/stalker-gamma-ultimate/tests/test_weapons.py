#!/usr/bin/env python3
"""Grounding checks for `references/weapons.md`.

Every number and identifier on the weapons page came out of the pack: the
in-game manual's *Ballistics System* and *Repairs for Guns* articles, the NPE
ammo tutorial, `good_weapons.txt`, `gamma_ammo_weapon_table.xlsx`,
`140- Weapon Parts Overhaul - arti` and the Economy addon's price tables. This
suite pins the checkable ones so the page cannot drift.

Run with the standard library only, offline:

    python3 tests/test_weapons.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "weapons.md"


class WeaponsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "good_weapons.txt",
            "gamma_ammo_weapon_table.xlsx",
            "article_gamma_ballistics_text",
            "npe_gamma_tutorial_ammo.xml",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_repair_classes_and_the_60_percent_rule(self):
        self.assertIn("60 %", self.text)
        self.assertIn("maintain parts", self.text)
        self.assertIn("Type A", self.text)
        self.assertIn("Type D", self.text)
        # the four repair types in mod_system_weapons_kit_repair.ltx
        for repair_type in ("pistol", "shotgun", "rifle_5", "rifle_7"):
            with self.subTest(repair_type=repair_type):
                self.assertIn(repair_type, self.text)

    def test_ammo_table_values_are_quoted(self):
        for value in (
            "ammo_k_ap",
            "ammo_k_hit",
            "ammo_9x18_fmj",
            "ammo_7.62x51_ap",
            "ammo_23x75_shrapnel",
            "ammo_og-7b",
        ):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_br_scale_is_stated(self):
        self.assertIn("BR1", self.text)
        self.assertIn("BR6", self.text)
        self.assertIn("exo armours", self.text.lower())

    def test_keybind_facts(self):
        self.assertIn("Left Alt", self.text)
        self.assertIn("custom22", self.text)
        self.assertIn("grok_reload_bind_checker.script", self.text)

    def test_faction_doctrine_table(self):
        self.assertIn("WP", self.text)
        self.assertIn("NATO", self.text)
        self.assertIn("ANY", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/ballistics-damage.md",
            "references/crafting-repairs.md",
            "references/armor-outfits.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
