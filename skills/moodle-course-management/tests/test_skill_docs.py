#!/usr/bin/env python3
"""Offline checks for the Moodle course-management skill documentation.

The skill is documentation-only, so these tests protect its local cross-links,
platform declaration, and vault-only credential guidance without using a network
or requiring any non-stdlib package.
"""

from __future__ import annotations

import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
YOUTUBE_GUIDE = SKILL_ROOT / "references" / "youtube-videos.md"


class SkillDocumentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = SKILL_MD.read_text(encoding="utf-8")
        self.youtube_text = YOUTUBE_GUIDE.read_text(encoding="utf-8")

    def test_frontmatter_identifies_all_supported_platforms(self) -> None:
        self.assertIn("name: moodle-course-management", self.skill_text)
        self.assertIn("version: 1.0.0", self.skill_text)
        self.assertIn("platforms: [linux, macos, windows]", self.skill_text)

    def test_vault_credential_is_documented_as_an_external_reference(self) -> None:
        self.assertIn("MOODLE_VAULT_CREDENTIAL", self.skill_text)
        self.assertIn("configured in the user's Hermes vault", self.skill_text)
        self.assertIn("never stored in this repository", self.skill_text)

    def test_youtube_reference_exists_and_describes_media_verification(self) -> None:
        self.assertTrue(YOUTUBE_GUIDE.is_file())
        self.assertIn(
            "[references/youtube-videos.md](references/youtube-videos.md)",
            self.skill_text,
        )
        self.assertIn("Verify with `ffprobe`", self.youtube_text)

    def test_core_integrity_workflow_is_present(self) -> None:
        self.assertIn("`manifest.json` as the truth", self.skill_text)
        self.assertIn("`hashlib.sha256`", self.skill_text)
        self.assertIn("`[[wikilinks]]`", self.skill_text)


if __name__ == "__main__":
    unittest.main()
