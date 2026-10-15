#!/usr/bin/env python3
"""Grounding checks for `references/keybinds-settings.md`.

The settings page is read straight out of the shipped defaults: `user.ltx`,
`ui_keybinding.xml` and `ui_st_keybinding.xml`, the MCM defaults in
`axr_options.ltx`, `difficulty.ltx` and the audio/HUD configs. This suite pins
the awkward bindings (reload on F10, unjam on R, detector on 6), the renderer
string and the AXRToolset option groups.

Run with the standard library only, offline:

    python3 tests/test_keybinds_settings.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "keybinds-settings.md"


class KeybindsSettingsDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "user.ltx",
            "axr_options.ltx",
            "difficulty.ltx",
            "ui_keybinding.xml",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_reload_and_unjam_are_documented(self):
        self.assertIn("F10", self.text)
        self.assertIn("kb_unjam", self.text)
        self.assertIn("custom22", self.text)

    def test_zero_nine_five_ubgl_key(self):
        self.assertIn("use_separate_ubgl_keybind", self.text)
        self.assertIn("Left Alt", self.text)

    def test_detector_and_jobs_keys(self):
        self.assertIn("6", self.text)
        self.assertIn("Caps Lock", self.text)

    def test_user_ltx_cvars(self):
        for cvar in ("renderer_r4", "vid_mode", "1920x1080"):
            with self.subTest(cvar=cvar):
                self.assertIn(cvar, self.text)

    def test_difficulty_preset_axes(self):
        self.assertIn("[econ_1", self.text)
        self.assertIn("[gdiff_1", self.text)
        self.assertIn("Tourist", self.text)

    def test_mcm_option_groups(self):
        self.assertIn("alife/", self.text)
        self.assertIn("Extra Options", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/installation-setup.md",
            "references/troubleshooting.md",
            "references/factions.md",
            "references/survival-mechanics.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
