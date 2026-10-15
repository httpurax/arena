#!/usr/bin/env python3
"""Grounding checks for `references/artifacts.md`.

Artefacts in GAMMA are entirely data-driven: `artefacts.ltx` (tier groups and
spawn fields), `mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx` (per-artefact
stats and `cost`), `craft.ltx` (`x_af_*` fusion recipes) and
`mod_system_grok_recipes.ltx` (recipe-book prices). This suite pins the exact
identifiers and prices quoted on the page — including the 0.9.5 change that
raised the T3 recipe book from 36 000 to 99 000.

Run with the standard library only, offline:

    python3 tests/test_artifacts.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "artifacts.md"


class ArtifactsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "artefacts.ltx",
            "mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx",
            "craft.ltx",
            "npe_gamma_tutorial_artefact.xml",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_artefact_identifiers_are_real(self):
        for af_id in (
            "af_medusa",
            "af_fireball",
            "af_compass",
            "af_oasis_heart",
            "af_monolith",
            "af_black_spray",
            "af_full_empty",
        ):
            with self.subTest(af_id=af_id):
                self.assertIn(af_id, self.text)

    def test_melter_facts(self):
        self.assertIn("max_uses", self.text)
        self.assertIn("15 000", self.text)
        self.assertIn("Melter", self.text)

    def test_cost_ladder_endpoints(self):
        self.assertIn("1 800", self.text)
        self.assertIn("149 000", self.text)
        self.assertIn("150 000", self.text)

    def test_fusion_recipe_form(self):
        self.assertIn("x_af_", self.text)
        self.assertIn("recipe_basic_4", self.text)
        self.assertIn("recipe_expert_4", self.text)
        self.assertIn("mutant_part_", self.text)

    def test_recipe_book_prices_and_the_0_9_5_raise(self):
        # verbatim patch-note fragment for the 0.9.5 T3 book price change
        self.assertIn("36k > 99k", self.text)
        self.assertIn("36 000", self.text)
        self.assertIn("65 000", self.text)

    def test_belt_tech_items_and_upgrades(self):
        self.assertIn("af_surge", self.text)
        self.assertIn("af_frames", self.text)
        self.assertIn("af_grid", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/anomalies.md",
            "references/survival-mechanics.md",
            "references/crafting-repairs.md",
            "references/armor-outfits.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
