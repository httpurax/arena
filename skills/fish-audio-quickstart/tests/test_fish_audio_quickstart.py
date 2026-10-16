"""Conformance checks for the Fish Audio quickstart's source map and safety rules."""

from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]


class FishAudioQuickstartTests(unittest.TestCase):
    def test_skill_frontmatter_and_reference_are_present(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: fish-audio-quickstart", skill)
        self.assertIn("category: software-development", skill)
        self.assertIn("references/fish-audio-quickstart.md", skill)

    def test_reference_points_to_canonical_docs_for_major_tasks(self):
        reference = (SKILL_DIR / "references" / "fish-audio-quickstart.md").read_text(
            encoding="utf-8"
        )
        for url in (
            "https://docs.fish.audio/developer-guide/getting-started/quickstart.md",
            "https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech.md",
            "https://docs.fish.audio/api-reference/endpoint/openapi-v1/speech-to-text.md",
            "https://docs.fish.audio/api-reference/endpoint/websocket/tts-live.md",
            "https://docs.fish.audio/api-reference/openapi.json",
        ):
            with self.subTest(url=url):
                self.assertIn(url, reference)

    def test_instructions_protect_credentials_and_avoid_stale_api_guesses(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        reference = (SKILL_DIR / "references" / "fish-audio-quickstart.md").read_text(
            encoding="utf-8"
        )
        combined = skill + reference
        self.assertIn("FISH_API_KEY", combined)
        self.assertIn("Never invent", skill)
        self.assertIn("confirm endpoint", reference)
        self.assertIn("server-side", skill)


if __name__ == "__main__":
    unittest.main()
