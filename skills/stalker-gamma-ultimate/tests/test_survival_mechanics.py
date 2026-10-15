#!/usr/bin/env python3
"""Grounding checks for `references/survival-mechanics.md`.

The survival page quotes the manual's *Healing and Medicines* and *Energy*
articles, GAMMA's `actor.ltx` actor override, the 30-level `skill_haruka.ltx`
trees and the difficulty presets. This suite pins the body-model numbers
(carry weight, bleed, stamina) and the medical-item names so the page cannot
quietly change what "temporary limb health" means.

Run with the standard library only, offline:

    python3 tests/test_survival_mechanics.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "survival-mechanics.md"


class SurvivalMechanicsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "actor.ltx",
            "skill_haruka.ltx",
            "article_gamma_healing_text",
            "article_gamma_energy_text",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_temporary_vs_permanent_health(self):
        self.assertIn("Temporary Limb Health", self.text)
        self.assertIn("Permanent Limb Health", self.text)
        for item in ("Ibuprofen", "Yadulin", "Antidote"):
            with self.subTest(item=item):
                self.assertIn(item, self.text)

    def test_health_pools(self):
        self.assertIn("health pools", self.text)
        self.assertIn("Psy", self.text)

    def test_actor_ltx_values(self):
        for value in (
            "max_item_mass = 50",
            "max_walk_weight = 100",
            "max_sleep_hours",
            "power_hit_part",
        ):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_bleed_model(self):
        self.assertIn("bleed", self.text.lower())
        self.assertIn("blood droplet", self.text)

    def test_skill_trees(self):
        for tree in ("survival", "scavenging", "endurance", "strength"):
            with self.subTest(tree=tree):
                self.assertIn(tree, self.text)

    def test_hunger_thirst_sleep(self):
        for word in ("hunger", "thirst", "sleep"):
            with self.subTest(word=word):
                self.assertIn(word, self.text.lower())

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/artifacts.md",
            "references/keybinds-settings.md",
            "references/troubleshooting.md",
            "references/anomalies.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
