#!/usr/bin/env python3
"""Grounding checks for `references/armor-outfits.md`.

The armour page is built from `G.A.M.M.A. Outfits Balances/tools/armor_values.tsv`
(161 outfits) and `ballist_res_sections.tsv`, plus the in-game manual's *Protection
Plates*, *Repairs for Armor* and *Disguise* articles. This suite pins the table
dimensions, the class/repair-kit mapping and the headline numbers so a rewrite
cannot silently change the dataset.

Run with the standard library only, offline:

    python3 tests/test_armor_outfits.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "armor-outfits.md"


class ArmorOutfitsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "armor_values.tsv",
            "ballist_res_sections.tsv",
            "G.A.M.M.A. Outfits Balances",
            "article_gamma_reparm_text",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_dataset_size_and_class_counts(self):
        self.assertIn("161", self.text)
        # repair_type distribution from armor_values.tsv
        for fragment in (
            "outfit_medium",
            "outfit_heavy",
            "outfit_light",
            "outfit_exo",
            "outfit_novice",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_repair_thresholds(self):
        self.assertIn("50 %", self.text)
        self.assertIn("65 %", self.text)
        self.assertIn("Maintenance Kit", self.text)
        self.assertIn("Spare Parts", self.text)

    def test_stat_ranges_come_from_the_table(self):
        for fragment in (
            "hit_fraction_actor",
            "wound_protection",
            "artefact_count",
            "additional_inventory_weight",
            "0.6875",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_exo_speed_and_nosorog_line(self):
        self.assertIn("0.95", self.text)
        self.assertIn("Nosorog", self.text)
        self.assertIn("130 866", self.text)

    def test_br_class_mapping_is_present(self):
        self.assertIn("0.17", self.text)
        self.assertIn("0.265", self.text)
        self.assertIn("BRC", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/ballistics-damage.md",
            "references/crafting-repairs.md",
            "references/artifacts.md",
            "references/factions.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
