#!/usr/bin/env python3
"""Grounding checks for `references/anomalies.md`.

The anomaly page is a catalogue of the shipped zone files and their engine
classes (`158- ABF - Jurkonov/gamedata/configs/zones/`, the Dynamic Anomalies
Overhaul, G.A.M.M.A. Radiation Dynamic Areas) plus the manual's artefact and
emission articles. This suite pins the file names, the class constants and a
few power values so the table cannot drift away from the configs.

Run with the standard library only, offline:

    python3 tests/test_anomalies.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "anomalies.md"


class AnomaliesDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "ABF - Jurkonov",
            "configs/zones/",
            "Dynamic Anomalies Overhaul",
            "G.A.M.M.A. Radiation Dynamic Areas",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_zone_files_are_real(self):
        for zone in (
            "zone_mine_gravitational.ltx",
            "zone_mine_sphere.ltx",
            "zone_mine_electric.ltx",
            "zone_mine_thermal.ltx",
            "zone_mine_acidic.ltx",
            "zone_mosquitobald.ltx",
            "zone_burningfuzz.ltx",
            "zone_hvatalka.ltx",
            "zone_fireball.ltx",
            "zone_field_radioactive.ltx",
        ):
            with self.subTest(zone=zone):
                self.assertIn(zone, self.text)

    def test_engine_classes(self):
        for cls in ("ZS_MBALD", "ZS_BFUZZ", "ZS_TORRD", "ZS_RADIO", "ZS_GALAN"):
            with self.subTest(cls=cls):
                self.assertIn(cls, self.text)

    def test_power_values_from_the_configs(self):
        for value in ("max_start_power", "3.2", "0.65", "1.5", "0.0091"):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_field_vs_mine_distinction(self):
        self.assertIn("dynamic field", self.text.lower())
        self.assertIn("attenuation", self.text)

    def test_zero_nine_five_and_manual_rules(self):
        self.assertIn("respawn", self.text.lower())
        self.assertIn("emissions", self.text.lower())

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/artifacts.md",
            "references/survival-mechanics.md",
            "references/ballistics-damage.md",
            "references/mutants.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
