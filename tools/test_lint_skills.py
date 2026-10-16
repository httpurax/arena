#!/usr/bin/env python3
"""test_lint_skills.py - self-test for the skill conformance linter.

The linter is only useful if it has teeth, so this proves both directions:

  * the committed fixture at tools/fixtures/broken-skill/ is rejected, with the exact rules
    named (a missing description, a version that is not X.Y.Z, two embedded fake secrets),
    and without the fake secret values being echoed into the report;
  * this repository's own skills/ tree is accepted;
  * a few throwaway trees in a temp directory exercise the remaining rules (missing
    SKILL.md, name/version/platform mismatches, invalid YAML, a failing tests/ suite, a
    minimal conforming skill).

Run it with:
    python tools/test_lint_skills.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
LINTER = TOOLS_DIR / "lint_skills.py"
FIXTURE_ROOT = TOOLS_DIR / "fixtures"
SKILLS_ROOT = REPO_ROOT / "skills"

RUN_TIMEOUT_SECONDS = 900

GOOD_FRONTMATTER = """\
---
name: {name}
description: A throwaway skill that exists only inside a temp directory.
version: 0.1.0
author: nobody
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [test]
    category: testing
---
# {name}
"""


def run_linter(root: Path) -> "tuple[int, str]":
    """Run the linter exactly as CI does, from the repo root, and capture its report."""
    proc = subprocess.run(
        [sys.executable, str(LINTER), str(root)],
        cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=RUN_TIMEOUT_SECONDS,
    )
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def write_skill(root: Path, name: str, frontmatter: str = None, files: "dict[str, str]" = None):
    """Create <root>/<name>/ with a SKILL.md and any extra files."""
    skill = root / name
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        frontmatter if frontmatter is not None else GOOD_FRONTMATTER.format(name=name),
        encoding="utf-8",
    )
    for relative, text in (files or {}).items():
        path = skill / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return skill


def rules_in(output: str) -> "set[str]":
    """The set of rule ids the report mentions, e.g. {'frontmatter.version', ...}."""
    return set(re.findall(r"\[([a-z_]+\.[a-z_.\-]+)\]", output))


class BrokenFixtureTest(unittest.TestCase):
    """tools/fixtures/broken-skill/ is committed exactly so this test can exist."""

    def setUp(self):
        self.returncode, self.output = run_linter(FIXTURE_ROOT)

    def test_broken_fixture_is_rejected(self):
        self.assertNotEqual(self.returncode, 0, f"the broken fixture was accepted:\n{self.output}")
        self.assertIn("FAIL", self.output)
        self.assertIn("1 skill checked: 0 ok, 1 failed", self.output)

    def test_every_deliberate_violation_is_reported_by_rule(self):
        expected = {
            "frontmatter.description",      # missing entirely
            "frontmatter.version",          # 1.0 is not X.Y.Z
            "secrets.api-key-literal",      # scripts/broken.py
            "secrets.password-literal",     # a fenced code block in SKILL.md
        }
        self.assertEqual(
            rules_in(self.output), expected,
            f"expected exactly {sorted(expected)}:\n{self.output}",
        )

    def test_report_names_the_offending_files(self):
        self.assertIn("tools/fixtures/broken-skill/SKILL.md", self.output)
        self.assertIn("tools/fixtures/broken-skill/scripts/broken.py", self.output)

    def test_secret_values_are_withheld_from_the_report(self):
        fixture = (FIXTURE_ROOT / "broken-skill").rglob("*")
        values = []
        for path in fixture:
            if path.is_file():
                for match in re.finditer(r"[\"']([^\"']*not-a-real[^\"']*)[\"']",
                                         path.read_text(encoding="utf-8")):
                    values.append(match.group(1))
        self.assertTrue(values, "the fixture no longer contains a fake secret to detect")
        for value in values:
            self.assertNotIn(value, self.output,
                             "the linter echoed a suspected secret into its report")


class RealRepositoryTest(unittest.TestCase):
    """The other half of the self-test: the repo as it stands must pass."""

    @staticmethod
    def skill_names() -> list[str]:
        """Return the repository skills the linter will consider, in its stable order."""
        return sorted(
            entry.name
            for entry in SKILLS_ROOT.iterdir()
            if entry.is_dir() and not entry.name.startswith(".") and entry.name != "__pycache__"
        )

    def test_this_repo_is_accepted(self):
        returncode, output = run_linter(SKILLS_ROOT)
        self.assertEqual(returncode, 0, f"the repo failed its own linter:\n{output}")
        count = len(self.skill_names())
        noun = "skill" if count == 1 else "skills"
        self.assertIn(f"{count} {noun} checked: {count} ok, 0 failed", output)

    def test_per_skill_summary_says_what_was_checked(self):
        _, output = run_linter(SKILLS_ROOT)
        for name in self.skill_names():
            self.assertRegex(output, rf"OK\s+{re.escape(name)}\s+frontmatter ok")
        self.assertIn("compile", output)
        self.assertIn("secret scan clean", output)
        # The skill's own suite must have run and passed - the count may grow over time.
        self.assertRegex(output, r"tests: \d+ tests passed")


class RuleTest(unittest.TestCase):
    """Throwaway trees: each one isolates a rule the committed fixture does not cover."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="lint-skills-selftest-")
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_missing_skill_md_is_rejected(self):
        skill = self.root / "no-manifest-skill"
        skill.mkdir()
        (skill / "README.md").write_text("# not a skill\n", encoding="utf-8")
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertIn("skill_md.missing", output)
        self.assertIn("no-manifest-skill/SKILL.md", output)
        # The skill lives outside the repo, so the report falls back to an absolute path.
        # It must use forward slashes there too - a Windows backslash would not match the
        # path a reader (or CI annotation) is expected to open.
        self.assertNotIn("\\", output, "the report used a backslash path")

    def test_frontmatter_key_rules_are_enforced(self):
        write_skill(self.root, "mismatched-skill", textwrap.dedent("""\
            ---
            name: some-other-name
            description:
            version: 2.0
            license: MIT
            platforms: [linux, solaris]
            ---
            # mismatch
            """))
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertEqual(rules_in(output), {
            "frontmatter.name",         # does not match the directory
            "frontmatter.description",  # present but empty
            "frontmatter.version",      # not X.Y.Z
            "frontmatter.platforms",    # solaris is not an allowed platform
        }, output)

    def test_missing_required_keys_are_reported(self):
        write_skill(self.root, "bare-skill", "---\nname: bare-skill\n---\n")
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertEqual(rules_in(output), {
            "frontmatter.description", "frontmatter.version",
            "frontmatter.license", "frontmatter.platforms",
        }, output)

    def test_invalid_yaml_frontmatter_is_rejected(self):
        write_skill(self.root, "tabbed-skill", "---\nname: tabbed-skill\nmetadata:\n\ttags: [x]\n---\n")
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertIn("frontmatter.invalid", output)
        self.assertIn("tab character", output)

    def test_python_that_does_not_compile_is_rejected(self):
        write_skill(self.root, "syntax-skill", files={"scripts/broken.py": "def oops(:\n    pass\n"})
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertIn("python.compile", output)
        self.assertIn("syntax-skill/scripts/broken.py", output)

    def test_failing_test_suite_is_rejected(self):
        write_skill(self.root, "failing-tests-skill", files={
            "tests/test_nothing.py": "import unittest\n\n\n"
                                    "class T(unittest.TestCase):\n"
                                    "    def test_it_fails(self):\n"
                                    "        self.assertEqual(1, 2)\n",
        })
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertIn("tests.failed", output)
        self.assertIn("AssertionError", output)  # the suite's own output is shown

    def test_minimal_conforming_skill_is_accepted(self):
        write_skill(self.root, "minimal-skill")
        returncode, output = run_linter(self.root)
        self.assertEqual(returncode, 0, output)
        self.assertIn("no .py files", output)
        self.assertIn("no tests/ directory", output)
        self.assertIn("1 skill checked: 1 ok, 0 failed", output)

    def test_description_over_60_chars_is_rejected(self):
        long_description = "A" * 61
        write_skill(self.root, "long-desc-skill", textwrap.dedent(f"""\
            ---
            name: long-desc-skill
            description: {long_description}
            version: 0.1.0
            license: MIT
            platforms: [linux]
            ---
            # long-desc-skill
            """))
        returncode, output = run_linter(self.root)
        self.assertNotEqual(returncode, 0, output)
        self.assertEqual(rules_in(output), {"frontmatter.description"}, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
