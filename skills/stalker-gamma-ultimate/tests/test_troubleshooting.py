#!/usr/bin/env python3
"""Grounding checks for `references/troubleshooting.md`.

The troubleshooting page rests on the official wiki's *Technical-Support-FAQ*
and *Installing-GAMMA* troubleshooting sections, the Anomaly log path
convention, the ZCP FAQ's engine-limit explanation and the bugfix list in
`Patchnotes.md` 0.9.5. This suite pins the log path, the version triple you are
told to verify and the specific script fixes that are worth knowing.

Run with the standard library only, offline:

    python3 tests/test_troubleshooting.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "troubleshooting.md"


class TroubleshootingDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "Technical-Support-FAQ",
            "Installing-GAMMA",
            "Patchnotes.md",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_log_path(self):
        self.assertIn("<Anomaly>/appdata/logs/xray_<user>.log", self.text)
        self.assertIn("appdata/logs", self.text)

    def test_version_triple(self):
        for value in ("v8.6", "MT-TEST_2026.5.5", "0.9.5"):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_renderer_and_dll_fixes(self):
        self.assertIn("DX11", self.text)
        self.assertIn(".NET Framework 3.5", self.text)
        self.assertIn("ModOrganizer.ini", self.text)

    def test_zero_nine_five_script_fixes(self):
        for value in ("pda.script", "smart_terrain", "xr_meet", "ui_inventory", "task_functor"):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_id_limit_section(self):
        self.assertIn("65535", self.text)
        self.assertIn("ZCP", self.text)

    def test_antivirus_and_update_resets(self):
        self.assertIn("antivirus", self.text.lower())
        self.assertIn("Bitdefender", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/installation-setup.md",
            "references/modding-guide.md",
            "references/performance-tuning.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
