"""Self-tests for tools/run_skill_tests.py discovery logic.

Stdlib-only (unittest + tempfile), mirroring tools/test_lint_skills.py.
Only the discovery/skip logic is tested here; actually executing skill
suites is the CI unittest job's responsibility.
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_skill_tests import discover_skill_tests, skipped_skills


def make_skill(root: Path, name: str, with_tests: bool) -> Path:
    skill = root / name
    if with_tests:
        (skill / "tests").mkdir(parents=True)
        (skill / "tests" / "test_dummy.py").write_text(
            "import unittest\n"
            "class T(unittest.TestCase):\n"
            "    def test_ok(self):\n"
            "        self.assertTrue(True)\n",
            encoding="utf-8",
        )
    else:
        skill.mkdir(parents=True)
    return skill


class TestDiscovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.skills = Path(self.tmp.name) / "skills"
        self.skills.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_finds_skill_with_tests(self):
        make_skill(self.skills, "alpha", with_tests=True)
        found = discover_skill_tests(self.skills)
        self.assertEqual([p.name for p in found], ["alpha"])

    def test_skips_skill_without_tests(self):
        make_skill(self.skills, "beta", with_tests=False)
        self.assertEqual(discover_skill_tests(self.skills), [])
        self.assertEqual(
            [p.name for p in skipped_skills(self.skills)], ["beta"]
        )

    def test_mixed_tree(self):
        make_skill(self.skills, "zeta", with_tests=True)
        make_skill(self.skills, "alpha", with_tests=True)
        make_skill(self.skills, "beta", with_tests=False)
        self.assertEqual(
            [p.name for p in discover_skill_tests(self.skills)],
            ["alpha", "zeta"],
        )
        self.assertEqual(
            [p.name for p in skipped_skills(self.skills)], ["beta"]
        )

    def test_missing_skills_root(self):
        missing = Path(self.tmp.name) / "nope"
        self.assertEqual(discover_skill_tests(missing), [])
        self.assertEqual(skipped_skills(missing), [])

    def test_files_are_ignored(self):
        (self.skills / "README.md").write_text("hi", encoding="utf-8")
        make_skill(self.skills, "alpha", with_tests=True)
        self.assertEqual(
            [p.name for p in discover_skill_tests(self.skills)], ["alpha"]
        )
        self.assertEqual(skipped_skills(self.skills), [])


if __name__ == "__main__":
    unittest.main()
