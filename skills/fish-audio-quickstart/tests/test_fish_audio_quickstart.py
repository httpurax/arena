#!/usr/bin/env python3
"""Offline checks for the Fish Audio quickstart skill documentation."""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE = SKILL_ROOT / "references" / "fish-audio-quickstart.md"


class FishAudioQuickstartTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = SKILL_MD.read_text(encoding="utf-8")
        self.reference_text = REFERENCE.read_text(encoding="utf-8")

    def test_frontmatter_is_present(self) -> None:
        self.assertIn("name: fish-audio-quickstart", self.skill_text)
        self.assertIn("version: 1.0.0", self.skill_text)
        self.assertIn("platforms: [linux, macos, windows]", self.skill_text)

    def test_reference_exists_and_is_linked(self) -> None:
        self.assertTrue(REFERENCE.is_file())
        self.assertIn("[references/fish-audio-quickstart.md]", self.skill_text)

    def test_core_quickstart_facts_are_documented(self) -> None:
        for token in (
            "FISH_API_KEY",
            "https://api.fish.audio/v1/tts",
            "s2.1-pro-free",
            "pip install fish-audio-sdk",
            "npm install fish-audio",
            "reference_id",
            "welcome.mp3",
        ):
            self.assertIn(token, self.skill_text + self.reference_text)

    def test_troubleshooting_statuses_are_documented(self) -> None:
        for status in ("401", "402", "400", "429"):
            self.assertIn(status, self.reference_text)


if __name__ == "__main__":
    unittest.main()
