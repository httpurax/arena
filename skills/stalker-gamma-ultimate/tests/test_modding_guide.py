#!/usr/bin/env python3
"""Grounding checks for `references/modding-guide.md`.

The modding page documents machinery that exists in the shipped pack:
`modlist.txt` load order, the per-addon folder layout, `meta.ini`, the DLTX
config-patching framework and the pack's own data tables. This suite pins those
identifiers so the page cannot quietly drift into describing a generic MO2
setup instead of GAMMA's.

Run with the standard library only, offline:

    python3 tests/test_modding_guide.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "modding-guide.md"


class ModdingGuideDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        self.assertIn("modlist.txt", self.text)
        self.assertIn("DLTX", self.text)
        self.assertIn("ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0", self.text)

    def test_repo_identifiers_are_real(self):
        for fragment in (
            "modpack_data/modlist.txt",
            "modpack_maker_list.txt",
            "meta.ini",
            "modpack_addons",
            "gamedata",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_snapshot_counts_are_stated(self):
        self.assertIn("385", self.text)   # shipped addon folders
        self.assertIn("239", self.text)   # mod_system_*.ltx patch files
        self.assertIn("473", self.text)   # source URLs in modpack_maker_list.txt

    def test_dltx_form_survives(self):
        # DLTX adds a property to an existing section and can inherit sections.
        self.assertIn("![", self.text)
        self.assertIn(":", self.text)

    def test_safe_procedure_is_stated(self):
        self.assertIn("load order", self.text.lower())
        self.assertIn("overwrite", self.text.lower())
        self.assertIn("profile", self.text.lower())

    def test_traps_section_warns_about_loose_files(self):
        self.assertIn("Anomaly/gamedata/", self.text)
        self.assertIn("user.ltx", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/installation-setup.md",
            "references/troubleshooting.md",
            "references/performance-tuning.md",
            "references/keybinds-settings.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
