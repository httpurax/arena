#!/usr/bin/env python3
"""Grounding checks for `references/installation-setup.md`.

The install page is only worth anything if its numbers and steps match the
official install procedure. This suite pins the facts that were read from
GAMMA's `README.md`, the official wiki (`Installing-GAMMA`, the
`Technical-Support-FAQ`) and the repository root, and fails if the page drifts
off them:

* the two archive checksums are quoted exactly;
* the launcher version, the launcher button names and the MO2 executable name
  are the real ones;
* the disk-space figures and per-component download sizes are the wiki's;
* the forbidden-renderer rule and the two-folder rule survive.

Run with the standard library only, offline:

    python3 tests/test_installation_setup.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "installation-setup.md"

ANOMALY_SHA256 = "E564D9110E673EACFA5604B0837F6E6208EAE4CD46CD5682326ED59F931527AE"
GAMMA_SHA256 = "2ceda1782b0b7737747c16974f1fe014bc1915caf1b08a1cba71e7950485192d"


class InstallationSetupDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        self.assertIn("Installing-GAMMA", self.text)
        self.assertIn("Technical-Support-FAQ", self.text)
        self.assertIn("ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0", self.text)

    def test_archive_checksums_are_exact(self):
        self.assertIn(ANOMALY_SHA256, self.text)
        self.assertIn(GAMMA_SHA256, self.text)
        self.assertIn("Anomaly-1.5.3-Full.2.7z", self.text)
        self.assertIn("GAMMA RC3.7z", self.text)

    def test_official_launcher_sequence_is_intact(self):
        for fragment in (
            "AnomalyLauncher.exe",
            "First Install Initialization",
            "Anomaly (DX11)",
            "v8.6",
            "ModOrganizer.ini",
            ".Grok's Modpack Installer",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_disk_and_download_budgets(self):
        self.assertIn("150 GB", self.text)
        self.assertIn("175", self.text)
        self.assertIn("9 GB", self.text)
        self.assertIn("11 GB", self.text)
        self.assertIn("27 GB", self.text)

    def test_renderer_and_folder_rules(self):
        self.assertIn("DX10", self.text)
        self.assertIn("broken", self.text)
        self.assertIn("same drive", self.text)
        self.assertIn("antivirus", self.text.lower())

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/modding-guide.md",
            "references/troubleshooting.md",
            "references/performance-tuning.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
