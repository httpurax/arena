#!/usr/bin/env python3
"""Offline checks for the hyperframes-quickstart skill."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE_MD = SKILL_ROOT / "references" / "hyperframes-quickstart.md"


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
        self.assertIn("name: hyperframes-quickstart", frontmatter)
        self.assertIn("version: 1.0.0", frontmatter)
        self.assertIn("platforms: [linux, macos, windows]", frontmatter)
        self.assertIn("license: MIT", frontmatter)

    def test_skill_links_reference(self):
        text = _read(SKILL_MD)
        self.assertIn("references/hyperframes-quickstart.md", text)

    def test_quickstart_facts(self):
        combined = _read(SKILL_MD) + "\n" + _read(REFERENCE_MD)
        for expected in (
            "npx hyperframes init",
            "npx hyperframes preview",
            "npx hyperframes render",
            "npx skills add heygen-com/hyperframes",
            "output.mp4",
            "index.html",
            "data-composition-id",
            "window.__timelines",
            "headless Chrome",
            "FFmpeg",
            "Apache 2.0",
            "Node.js",
        ):
            self.assertIn(expected, combined)

    def test_reference_covers_validation(self):
        text = _read(REFERENCE_MD)
        for expected in ("doctor", "lint", "check", "renders/"):
            self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
