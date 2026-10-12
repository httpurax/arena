#!/usr/bin/env python3
"""test_install_skills.py - self-test for tools/install_skills.py.

Stdlib-only (unittest + tempfile). Nothing here touches a real Hermes install: every test
either passes an explicit environment and home directory, or passes --skills-root pointing
into a temp directory. The one test that reads the real environment does so under a
--dry-run and with HERMES_HOME pointed at a temp directory.

Covers: skills root resolution order (env mocked), category mapping (including the two real
skills in this repo), dry-run making no changes, missing-category failure, copy-not-move,
overwrite of an existing install, and the unresolvable-root exit status.

Run it with:
    python tools/test_install_skills.py
"""

from __future__ import annotations

import io
import ntpath
import os
import posixpath
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
INSTALLER = TOOLS_DIR / "install_skills.py"
REPO_SKILLS = REPO_ROOT / "skills"

sys.path.insert(0, str(TOOLS_DIR))

import install_skills  # noqa: E402
from install_skills import InstallError, build_plan, discover_skills, main, resolve_skills_root  # noqa: E402

LINUX_HOME = "/home/alice"
WIN_LOCAL_APP_DATA = r"C:\Users\alice\AppData\Local"
WIN_HOME = r"C:\Users\alice"

SKILL_TEMPLATE = """\
---
name: {name}
description: A throwaway skill for the installer self-test.
version: 0.1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [test]
{category_line}---
# {name}
"""


def make_skill(skills_dir: Path, name: str, category: "str | None" = "testing",
               extra_files: "dict[str, str] | None" = None) -> Path:
    """Create <skills_dir>/<name>/ with a SKILL.md declaring `category` (or none, if None)."""
    skill = skills_dir / name
    skill.mkdir(parents=True)
    category_line = f"    category: {category}\n" if category is not None else ""
    (skill / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, category_line=category_line), encoding="utf-8"
    )
    (skill / "scripts").mkdir()
    (skill / "scripts" / "helper.py").write_text("print('hi')\n", encoding="utf-8")
    for relative, text in (extra_files or {}).items():
        path = skill / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return skill


def snapshot(path: Path) -> "dict[str, bytes | None]":
    """Every file and directory under `path` mapped to its bytes (None for a directory)."""
    if not path.exists():
        return {}
    result: "dict[str, bytes | None]" = {}
    for entry in sorted(path.rglob("*")):
        key = entry.relative_to(path).as_posix()
        result[key] = entry.read_bytes() if entry.is_file() else None
    return result


def run_main(argv, *, env, home=None, platform_name="linux", skills_dir=None):
    """Run main() with captured output. Returns (exit status, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    status = main(
        argv,
        env=env,
        home=home,
        platform_name=platform_name,
        skills_dir=skills_dir if skills_dir is not None else REPO_SKILLS,
        stdout=out,
        stderr=err,
    )
    return status, out.getvalue(), err.getvalue()


class TempTree(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="install-skills-selftest-")
        self.addCleanup(self._tmp.cleanup)
        self.base = Path(self._tmp.name)
        self.skills = self.base / "repo-skills"
        self.skills.mkdir()
        self.root = self.base / "hermes" / "skills"


class RootResolutionOrderTest(unittest.TestCase):
    """resolve_skills_root with the environment and home directory mocked."""

    def test_hermes_home_wins_on_linux(self):
        resolved = resolve_skills_root(
            {"HERMES_HOME": "/opt/hermes", "LOCALAPPDATA": WIN_LOCAL_APP_DATA},
            LINUX_HOME, "linux")
        self.assertEqual(resolved.path, posixpath.join("/opt/hermes", "skills"))
        self.assertEqual(resolved.source, "$HERMES_HOME/skills")

    def test_hermes_home_wins_over_dot_hermes_on_macos(self):
        resolved = resolve_skills_root({"HERMES_HOME": "/opt/hermes"}, LINUX_HOME, "darwin")
        self.assertEqual(resolved.path, posixpath.join("/opt/hermes", "skills"))

    def test_hermes_home_wins_on_windows(self):
        resolved = resolve_skills_root(
            {"HERMES_HOME": r"D:\hermes", "LOCALAPPDATA": WIN_LOCAL_APP_DATA},
            WIN_HOME, "win32")
        self.assertEqual(resolved.path, ntpath.join(r"D:\hermes", "skills"))
        self.assertEqual(resolved.source, "$HERMES_HOME/skills")

    def test_empty_or_blank_hermes_home_is_treated_as_unset(self):
        for value in ("", "   "):
            resolved = resolve_skills_root({"HERMES_HOME": value}, LINUX_HOME, "linux")
            self.assertEqual(resolved.path, posixpath.join(LINUX_HOME, ".hermes", "skills"))

    def test_linux_falls_back_to_dot_hermes(self):
        resolved = resolve_skills_root({}, LINUX_HOME, "linux")
        self.assertEqual(resolved.path, posixpath.join(LINUX_HOME, ".hermes", "skills"))
        self.assertEqual(resolved.source, "~/.hermes/skills")

    def test_macos_falls_back_to_dot_hermes(self):
        resolved = resolve_skills_root({}, LINUX_HOME, "darwin")
        self.assertEqual(resolved.path, posixpath.join(LINUX_HOME, ".hermes", "skills"))

    def test_windows_uses_localappdata_and_never_dot_hermes(self):
        resolved = resolve_skills_root(
            {"LOCALAPPDATA": WIN_LOCAL_APP_DATA}, WIN_HOME, "win32")
        self.assertEqual(resolved.path,
                         ntpath.join(WIN_LOCAL_APP_DATA, "hermes", "skills"))
        self.assertNotIn(".hermes", resolved.path)
        self.assertEqual(resolved.source, "%LOCALAPPDATA%\\hermes\\skills")

    def test_windows_without_localappdata_is_unresolvable(self):
        with self.assertRaises(InstallError) as ctx:
            resolve_skills_root({}, WIN_HOME, "win32")
        self.assertIn("LOCALAPPDATA", str(ctx.exception))
        self.assertIn("--skills-root", str(ctx.exception))

    def test_posix_without_home_is_unresolvable(self):
        with self.assertRaises(InstallError) as ctx:
            resolve_skills_root({}, None, "linux")
        self.assertIn("HERMES_HOME", str(ctx.exception))

    def test_skills_root_override_beats_every_environment_rule(self):
        resolved = resolve_skills_root(
            {"HERMES_HOME": "/opt/hermes", "LOCALAPPDATA": WIN_LOCAL_APP_DATA},
            LINUX_HOME, "win32", override="/tmp/explicit")
        self.assertEqual(resolved.path, "/tmp/explicit")
        self.assertEqual(resolved.source, "--skills-root")

    def test_empty_skills_root_override_is_rejected(self):
        with self.assertRaises(InstallError):
            resolve_skills_root({}, LINUX_HOME, "linux", override="  ")

    def test_default_environment_is_read_from_os_environ(self):
        # With no env argument, main() reads the real os.environ. Pin HERMES_HOME to a temp
        # directory and use --dry-run, so this exercises the default wiring and writes nothing.
        with tempfile.TemporaryDirectory(prefix="install-skills-env-") as tmp:
            out, err = io.StringIO(), io.StringIO()
            with mock.patch.dict(os.environ, {"HERMES_HOME": tmp}):
                with redirect_stdout(out), redirect_stderr(err):
                    status = main(["--dry-run"], skills_dir=REPO_SKILLS)
            self.assertEqual(status, 0, err.getvalue())
            self.assertIn(os.path.join(tmp, "skills"), out.getvalue())
            self.assertIn("$HERMES_HOME/skills", out.getvalue())
            self.assertEqual(list(Path(tmp).iterdir()), [], "dry run created files")


class CategoryMappingTest(TempTree):
    def test_repo_skills_map_to_their_installed_categories(self):
        plans = build_plan(discover_skills(REPO_SKILLS), self.root)
        destinations = {p.name: p.destination.relative_to(self.root).as_posix() for p in plans}
        self.assertEqual(destinations, {
            "course-material-ingestion": "research/course-material-ingestion",
            "moodle-course-management": "productivity/moodle-course-management",
        })

    def test_category_is_read_from_metadata_hermes(self):
        make_skill(self.skills, "alpha", category="research")
        plans = build_plan(discover_skills(self.skills), self.root)
        self.assertEqual(plans[0].category, "research")
        self.assertEqual(plans[0].destination, self.root / "research" / "alpha")

    def test_top_level_category_key_does_not_count(self):
        skill = make_skill(self.skills, "misplaced", category=None)
        (skill / "SKILL.md").write_text(
            "---\nname: misplaced\ndescription: x\nversion: 0.1.0\nlicense: MIT\n"
            "platforms: [linux]\ncategory: research\n---\n", encoding="utf-8")
        with self.assertRaises(InstallError) as ctx:
            build_plan(discover_skills(self.skills), self.root)
        self.assertIn("misplaced", str(ctx.exception))

    def test_missing_category_fails_and_names_the_skill(self):
        make_skill(self.skills, "good-skill", category="research")
        make_skill(self.skills, "orphan-skill", category=None)
        with self.assertRaises(InstallError) as ctx:
            build_plan(discover_skills(self.skills), self.root)
        self.assertIn("orphan-skill", str(ctx.exception))
        self.assertIn("no category", str(ctx.exception))

    def test_missing_category_stops_the_whole_run_with_nothing_written(self):
        make_skill(self.skills, "good-skill", category="research")
        make_skill(self.skills, "orphan-skill", category=None)
        status, out, err = run_main(["--skills-root", str(self.root)],
                                    env={}, skills_dir=self.skills)
        self.assertEqual(status, 1)
        self.assertIn("ERROR", err)
        self.assertIn("orphan-skill", err)
        self.assertNotIn("INSTALLED", out)
        self.assertFalse(self.root.exists(), "a partial install was written")

    def test_unusable_category_values_are_rejected(self):
        for index, bad in enumerate(("../escape", "nested/dir", "two words", '""')):
            with self.subTest(category=bad):
                # A fresh skills tree per value keeps the cases independent of each other.
                skills = self.base / f"case-{index}"
                skill_name = f"bad-skill-{index}"
                make_skill(skills, skill_name, category=bad)
                with self.assertRaises(InstallError) as ctx:
                    build_plan(discover_skills(skills), self.root)
                message = str(ctx.exception)
                self.assertIn(skill_name, message)
                if bad == '""':
                    self.assertIn("must be a non-empty string", message)
                else:
                    self.assertIn("not a plain directory name", message)


class DryRunTest(TempTree):
    def test_dry_run_creates_nothing_when_root_is_absent(self):
        make_skill(self.skills, "alpha", category="research")
        status, out, _ = run_main(["--dry-run", "--skills-root", str(self.root)],
                                  env={}, skills_dir=self.skills)
        self.assertEqual(status, 0)
        self.assertIn("DRY-RUN", out)
        self.assertIn("nothing was changed", out)
        self.assertFalse((self.base / "hermes").exists(), "dry run created a directory")

    def test_dry_run_leaves_an_existing_install_byte_identical(self):
        make_skill(self.skills, "alpha", category="research")
        existing = self.root / "research" / "alpha"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("installed version\n", encoding="utf-8")
        (existing / "stale.txt").write_text("from an older release\n", encoding="utf-8")
        before = snapshot(self.base)

        status, out, _ = run_main(["--dry-run", "--skills-root", str(self.root)],
                                  env={}, skills_dir=self.skills)

        self.assertEqual(status, 0)
        self.assertIn("would replace", out)
        self.assertEqual(snapshot(self.base), before, "dry run changed the filesystem")

    def test_dry_run_still_fails_on_missing_category(self):
        make_skill(self.skills, "orphan", category=None)
        status, _, err = run_main(["--dry-run", "--skills-root", str(self.root)],
                                  env={}, skills_dir=self.skills)
        self.assertEqual(status, 1)
        self.assertIn("orphan", err)


class InstallBehaviourTest(TempTree):
    def test_install_copies_the_folder_and_keeps_the_source(self):
        source = make_skill(self.skills, "alpha", category="research",
                            extra_files={"references/notes.md": "notes\n"})
        source_before = snapshot(source)

        status, out, _ = run_main(["--skills-root", str(self.root)],
                                  env={}, skills_dir=self.skills)

        self.assertEqual(status, 0)
        installed = self.root / "research" / "alpha"
        self.assertEqual(snapshot(installed), source_before)
        self.assertTrue(source.is_dir(), "the source skill was moved away")
        self.assertEqual(snapshot(source), source_before)
        self.assertIn("INSTALLED  alpha (research)", out)

    def test_existing_install_is_overwritten_in_full(self):
        make_skill(self.skills, "alpha", category="research")
        existing = self.root / "research" / "alpha"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("old\n", encoding="utf-8")
        (existing / "removed-upstream.txt").write_text("stale\n", encoding="utf-8")

        status, out, _ = run_main(["--skills-root", str(self.root)],
                                  env={}, skills_dir=self.skills)

        self.assertEqual(status, 0)
        self.assertFalse((existing / "removed-upstream.txt").exists(),
                         "a stale file survived the overwrite")
        source_md = (self.skills / "alpha" / "SKILL.md").read_bytes()
        self.assertEqual((existing / "SKILL.md").read_bytes(), source_md)
        self.assertIn("REPLACED  alpha (research)", out)

    def test_bytecode_caches_are_not_copied(self):
        make_skill(self.skills, "alpha", category="research", extra_files={
            "__pycache__/helper.cpython-311.pyc": "bytecode",
            "scripts/other.pyc": "bytecode",
        })
        status, _, _ = run_main(["--skills-root", str(self.root)],
                                env={}, skills_dir=self.skills)
        self.assertEqual(status, 0)
        installed = self.root / "research" / "alpha"
        self.assertFalse((installed / "__pycache__").exists())
        self.assertFalse((installed / "scripts" / "other.pyc").exists())
        self.assertTrue((installed / "scripts" / "helper.py").is_file())

    def test_installing_a_skill_into_its_own_source_is_refused(self):
        make_skill(self.skills, "alpha", category="alpha")
        # The destination would be <skills>/alpha/alpha, inside the source tree.
        status, out, err = run_main(["--skills-root", str(self.skills)],
                                    env={}, skills_dir=self.skills)
        self.assertEqual(status, 1)
        self.assertIn("overlaps", err)
        self.assertNotIn("INSTALLED", out)

    def test_root_that_is_a_file_fails_cleanly(self):
        self.root.parent.mkdir(parents=True)
        self.root.write_text("not a directory\n", encoding="utf-8")
        make_skill(self.skills, "alpha", category="research")
        status, _, err = run_main(["--skills-root", str(self.root)],
                                  env={}, skills_dir=self.skills)
        self.assertEqual(status, 1)
        self.assertIn("not a directory", err)

    def test_unresolvable_root_exits_nonzero_and_writes_nothing(self):
        make_skill(self.skills, "alpha", category="research")
        status, out, err = run_main([], env={}, home=None, platform_name="win32",
                                    skills_dir=self.skills)
        self.assertEqual(status, 1)
        self.assertIn("ERROR", err)
        self.assertIn("LOCALAPPDATA", err)
        self.assertEqual(out, "")

    def test_missing_skills_directory_fails(self):
        status, _, err = run_main(["--dry-run", "--skills-root", str(self.root)],
                                  env={}, skills_dir=self.base / "no-such-dir")
        self.assertEqual(status, 1)
        self.assertIn("skills directory not found", err)


class CommandLineTest(TempTree):
    def test_script_runs_as_a_program_in_dry_run_mode(self):
        # Exercises the real entry point in a child interpreter, against a temp root.
        proc = subprocess.run(
            [sys.executable, str(INSTALLER), "--dry-run", "--skills-root", str(self.root)],
            capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("DRY-RUN", proc.stdout)
        self.assertIn("research", proc.stdout)
        self.assertIn("productivity", proc.stdout)
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
