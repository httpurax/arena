#!/usr/bin/env python3
"""Grounding checks for `references/mutants.md`.

Mutant behaviour lives in GAMMA's *Mutants Overhaul* configs
(`creatures/m_*.ltx`), the loot table `items/settings/mutant_loot.ltx`, the
pelts patch `mod_system_grok_pelts.ltx`, the ZCP spawn FAQ and the pack's
`Patchnotes.md` 0.9.5. This suite pins the creature and part identifiers, the
corpse `decay_time` budget and the 0.9.5 chimera-encounter change.

Run with the standard library only, offline:

    python3 tests/test_mutants.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "mutants.md"


class MutantsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "m_bloodsucker.ltx",
            "m_boar.ltx",
            "mutant_loot.ltx",
            "mod_system_grok_pelts.ltx",
            "Mutants Overhaul",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_creature_identifiers(self):
        for creature in ("bloodsucker", "chimera", "gigant", "burer"):
            with self.subTest(creature=creature):
                self.assertIn(creature, self.text)

    def test_loot_parts_and_hides(self):
        for part in (
            "mutant_part_krovosos_jaw",
            "mutant_part_chimera_claw",
            "mutant_part_pseudogigant_hand",
            "hide_bloodsucker",
            "hide_chimera",
        ):
            with self.subTest(part=part):
                self.assertIn(part, self.text)

    def test_corpse_decay_budget(self):
        self.assertIn("decay_time", self.text)
        self.assertIn("12000", self.text)

    def test_headline_part_prices(self):
        self.assertIn("mutant_part_heart_chimera", self.text)
        self.assertIn("5250", self.text)
        self.assertIn("mutant_part_lurker_meat", self.text)

    def test_vitals_and_stomp_facts(self):
        self.assertIn("health_hit_part", self.text)
        self.assertIn("pseudogiant_can_damage_objects_on_stomp", self.text)

    def test_zero_nine_five_chimera_change(self):
        self.assertIn("1 chimera + 2 pseudodogs", self.text)
        self.assertIn("South chimera are easier", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/anomalies.md",
            "references/ballistics-damage.md",
            "references/survival-mechanics.md",
            "references/trading-economy.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
