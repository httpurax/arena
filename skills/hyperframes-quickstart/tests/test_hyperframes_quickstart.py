#!/usr/bin/env python3
"""Offline checks for the hyperframes-quickstart skill.

Validates the shape of the two documents (frontmatter, SKILL.md as a short entry
point that links the reference) and, more usefully, that every command and URL the
guide prints is one this repo actually verified upstream: CLI invocations must use
`npx hyperframes`, subcommands and URL hosts are allowlisted, and the uncertainty
marker has to stay in place. No network, stdlib only.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCE_MD = SKILL_ROOT / "references" / "hyperframes-quickstart.md"

SKILL_NAME = SKILL_ROOT.name  # the frontmatter `name` must equal the directory name

# Subcommands verified against the upstream README and the hyperframes-cli skill.
KNOWN_SUBCOMMANDS = frozenset(
    {"init", "preview", "render", "lint", "check", "snapshot", "doctor",
     "catalog", "add", "skills", "timeline"}
)

# Hosts the guide may name. Add a host here deliberately, with an upstream source,
# before any document references it.
ALLOWED_URL_HOSTS = frozenset(
    {"github.com", "cdn.jsdelivr.net", "hyperframes.heygen.com", "www.npmjs.com"}
)

UNCERTAINTY_MARKER = "verify on github.com/heygen-com/hyperframes"

CLI_INVOCATION_RE = re.compile(r"\bnpx\s+hyperframes\s+([a-z][a-z-]*)")
UNPREFIXED_INVOCATION_RE = re.compile(
    r"(?<![`\w-])hyperframes\s+(?:%s)\b" % "|".join(sorted(KNOWN_SUBCOMMANDS))
)
URL_RE = re.compile(r"https?://[^\s<>()\"'`]+")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md has no frontmatter block")
    return match.group(1)


def _fence_balanced(text: str) -> bool:
    return sum(1 for line in text.splitlines() if line.startswith("```")) % 2 == 0


class TestSkillStructure(unittest.TestCase):
    def test_required_files_exist(self):
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md is missing")
        self.assertTrue(REFERENCE_MD.is_file(), "references guide is missing")

    def test_frontmatter_keys_and_values(self):
        frontmatter = _frontmatter(_read(SKILL_MD))
        self.assertIn("version: 1.0.0", frontmatter)
        self.assertIn("license: MIT", frontmatter)
        self.assertIn("platforms: [linux, macos, windows]", frontmatter)
        self.assertIn("category: development", frontmatter)

    def test_name_matches_directory(self):
        frontmatter = _frontmatter(_read(SKILL_MD))
        self.assertIn("name: %s" % SKILL_NAME, frontmatter)

    def test_description_stays_under_listing_limit(self):
        match = re.search(r"^description:\s*(.+)$", _frontmatter(_read(SKILL_MD)), re.MULTILINE)
        self.assertIsNotNone(match, "frontmatter has no description")
        description = match.group(1).strip().strip("'\"")
        self.assertLessEqual(len(description), 60, "descriptions are truncated past 60 chars")

    def test_skill_md_is_an_entry_point(self):
        text = _read(SKILL_MD)
        self.assertLessEqual(len(text.splitlines()), 150, "long docs belong in references/")
        self.assertNotIn("<!doctype html>", text, "the HTML skeleton belongs in the reference")

    def test_skill_links_reference(self):
        self.assertIn("references/hyperframes-quickstart.md", _read(SKILL_MD))

    def test_code_fences_balanced(self):
        self.assertTrue(_fence_balanced(_read(SKILL_MD)), "SKILL.md has an unclosed fence")
        self.assertTrue(_fence_balanced(_read(REFERENCE_MD)), "reference has an unclosed fence")

    def test_reference_length_is_a_guide_not_a_book(self):
        lines = len(_read(REFERENCE_MD).splitlines())
        self.assertGreaterEqual(lines, 120)
        self.assertLessEqual(lines, 400)


class TestCommandsAreVerified(unittest.TestCase):
    def test_no_unprefixed_cli_invocations(self):
        for path in (SKILL_MD, REFERENCE_MD):
            for number, line in enumerate(_read(path).splitlines(), start=1):
                if "npx hyperframes" in line:
                    continue
                self.assertIsNone(
                    UNPREFIXED_INVOCATION_RE.search(line),
                    "%s:%d shows a hyperframes command without the npx prefix" % (path.name, number),
                )

    def test_only_verified_subcommands(self):
        combined = _read(SKILL_MD) + "\n" + _read(REFERENCE_MD)
        found = {match.group(1) for match in CLI_INVOCATION_RE.finditer(combined)}
        self.assertTrue(found, "no CLI invocations found at all")
        self.assertLessEqual(
            found, set(KNOWN_SUBCOMMANDS),
            "documented subcommand(s) outside the verified set: %s" % sorted(found - KNOWN_SUBCOMMANDS),
        )

    def test_required_quickstart_commands_present(self):
        combined = _read(SKILL_MD) + "\n" + _read(REFERENCE_MD)
        for command in (
            "npx hyperframes init",
            "npx hyperframes preview",
            "npx hyperframes render",
            "npx hyperframes lint",
            "npx hyperframes check",
            "npx skills add heygen-com/hyperframes",
            "npx hyperframes skills update",
        ):
            self.assertIn(command, combined)


class TestUrlsAreAllowlisted(unittest.TestCase):
    def test_every_url_host_is_known(self):
        for path in (SKILL_MD, REFERENCE_MD):
            for raw in URL_RE.findall(_read(path)):
                url = raw.rstrip(".,;:)")
                host = url.split("//", 1)[1].split("/", 1)[0].split(":", 1)[0].lower()
                self.assertIn(
                    host, ALLOWED_URL_HOSTS,
                    "%s names an unverified host (%s): add it deliberately or drop it" % (path.name, host),
                )

    def test_uncertainty_marker_present_in_both_documents(self):
        for path in (SKILL_MD, REFERENCE_MD):
            self.assertIn(UNCERTAINTY_MARKER, _read(path), "%s lost the uncertainty marker" % path.name)

    def test_skill_forbids_inventing_commands(self):
        self.assertIn("Never invent commands", _read(SKILL_MD))


class TestReferenceCoversTheTopics(unittest.TestCase):
    def test_reference_covers_requested_topics(self):
        text = _read(REFERENCE_MD)
        for expected in (
            "Apache",                    # what it is / license
            "headless Chrome",           # how a render works
            "Node.js 22",                # requirements
            "FFmpeg",
            "npx hyperframes doctor",    # environment diagnosis
            "A First Composition in HTML",
            "index.html",
            "data-composition-id",       # first composition in HTML
            "data-duration",
            "window.__timelines",
            "gsap.timeline({ paused: true })",
            "npx hyperframes preview",   # previewing
            "npx hyperframes render",    # rendering to MP4
            "--quality delivery",
            "ffprobe",                   # output verification
            "npx skills add",            # agent skills
            "faceless",                  # the pipeline this is for
            "catalog",
            "media-use",
        ):
            self.assertIn(expected, text, "reference no longer covers %r" % expected)

    def test_reference_prints_a_renderable_skeleton(self):
        text = _read(REFERENCE_MD)
        for expected in (
            'data-composition-id="main"',
            'data-width="1920"',
            'data-duration="5"',
            'class="clip"',
            'window.__timelines["main"]',
            "gsap.fromTo",
        ):
            self.assertIn(expected, text)

    def test_reference_names_its_upstream_sources(self):
        text = _read(REFERENCE_MD)
        for source in ("minimal-composition", "quickstart.mdx", "hyperframes-cli"):
            self.assertIn(source, text, "provenance for %r is missing" % source)

    def test_verified_versus_recheck_section_exists(self):
        text = _read(REFERENCE_MD)
        self.assertIn("Verified on", text)
        self.assertIn("Version-dependent", text)


if __name__ == "__main__":
    unittest.main()
