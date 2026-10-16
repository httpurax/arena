#!/usr/bin/env python3
"""Offline checks for the fish-audio-quickstart skill."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE_MD = SKILL_ROOT / "references" / "fish-audio-quickstart.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSkillFiles(unittest.TestCase):
    def test_required_files_exist(self):
        self.assertTrue(SKILL_MD.is_file())
        self.assertTrue(REFERENCE_MD.is_file())

    def test_frontmatter(self):
        text = _read(SKILL_MD)
        match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        self.assertIn("name: fish-audio-quickstart", frontmatter)
        self.assertIn("version: 1.0.0", frontmatter)
        self.assertIn("platforms: [linux, macos, windows]", frontmatter)
        self.assertIn("license: MIT", frontmatter)

    def test_skill_links_reference(self):
        text = _read(SKILL_MD)
        self.assertIn("references/fish-audio-quickstart.md", text)

    def test_quickstart_facts(self):
        combined = _read(SKILL_MD) + "\n" + _read(REFERENCE_MD)
        for expected in (
            "fish-audio-sdk",
            "FISH_API_KEY",
            "api.fish.audio/v1/tts",
            "s2.1-pro",
            "s2.1-pro-free",
            "reference_id",
            "npm install fish-audio",
            "welcome.mp3",
            "output.mp3",
        ):
            self.assertIn(expected, combined)

    def test_reference_covers_errors(self):
        text = _read(REFERENCE_MD)
        for status in ("401", "402", "400", "429"):
            self.assertIn(status, text)


if __name__ == "__main__":
    unittest.main()
