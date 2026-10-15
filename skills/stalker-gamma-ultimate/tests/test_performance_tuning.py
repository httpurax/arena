#!/usr/bin/env python3
"""Grounding checks for `references/performance-tuning.md`.

GAMMA's performance story is the patched engine (`MT-TEST_2026.5.5`), the
Meatchunk prefetcher, the shipped graphics baseline in `user.ltx` and the
population/option knobs the pack exposes (`axr_options.ltx`, the ZCP FAQ). The
official FAQ explicitly does not cover performance, so every claim here is
either a patch note or a config value — and this suite pins them.

Run with the standard library only, offline:

    python3 tests/test_performance_tuning.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "performance-tuning.md"


class PerformanceTuningDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "MT-TEST_2026.5.5",
            "Patchnotes.md",
            "user.ltx",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_prefetcher_and_ram_requirement(self):
        self.assertIn("17 Gb required minimum", self.text)
        self.assertIn("prefetch", self.text.lower())

    def test_renderer_rules(self):
        self.assertIn("renderer_r4", self.text)
        self.assertIn("DX10", self.text)
        self.assertIn("broken", self.text)

    def test_zero_nine_five_optimisations_are_named(self):
        for name in ("grok_gotta_go_fast", "callbacks_gameobject", "Rostok"):
            with self.subTest(name=name):
                self.assertIn(name, self.text)

    def test_population_and_graphics_knobs(self):
        self.assertIn("axr_options.ltx", self.text)
        self.assertIn("alife", self.text.lower())

    def test_ultrawide_note(self):
        self.assertIn("ultrawide", self.text.lower())
        self.assertIn("Dynamic Aspect Ratio Tweaks", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/troubleshooting.md",
            "references/installation-setup.md",
            "references/keybinds-settings.md",
            "references/modding-guide.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
