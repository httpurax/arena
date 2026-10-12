"""Run every skill's own test suite.

Discovers each directory under ``skills/`` that contains a ``tests/``
folder and runs ``python -m unittest discover -s tests`` inside it.
Skills without a ``tests/`` directory are skipped, not failed.

Stdlib-only by convention: no install step is needed before this script,
on any platform CI runs (Ubuntu/Windows) or any supported Python.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"


def discover_skill_tests(skills_root: Path = SKILLS_ROOT) -> list[Path]:
    """Return the skill directories that contain a ``tests/`` folder.

    Sorted by directory name for stable output. Skills without ``tests/``
    are silently skipped here; the caller reports them.
    """
    if not skills_root.is_dir():
        return []
    found = [
        entry
        for entry in skills_root.iterdir()
        if entry.is_dir() and (entry / "tests").is_dir()
    ]
    return sorted(found, key=lambda p: p.name)


def skipped_skills(skills_root: Path = SKILLS_ROOT) -> list[Path]:
    """Skill directories that have no ``tests/`` folder (skipped, not failed)."""
    if not skills_root.is_dir():
        return []
    skipped = [
        entry
        for entry in skills_root.iterdir()
        if entry.is_dir() and not (entry / "tests").is_dir()
    ]
    return sorted(skipped, key=lambda p: p.name)


def run_suite(skill_dir: Path) -> int:
    """Run one skill's unittest suite. Returns the suite's exit code."""
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        cwd=skill_dir,
        capture_output=True,
        text=True,
    )
    # unittest writes its report to stderr; show it so CI logs stay useful.
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


def main() -> int:
    suites = discover_skill_tests()
    skipped = skipped_skills()

    for skill in skipped:
        print(f"SKIP  {skill.name}/ (no tests/ directory)")

    if not suites:
        print("No skill test suites found under skills/.")
        return 0

    failures: list[str] = []
    for skill in suites:
        print(f"RUN   {skill.name}/")
        rc = run_suite(skill)
        if rc == 0:
            print(f"PASS  {skill.name}/")
        else:
            print(f"FAIL  {skill.name}/ (exit {rc})")
            failures.append(skill.name)

    if failures:
        print(f"\n{len(failures)} suite(s) failed: {', '.join(failures)}")
        return 1
    print(f"\nAll {len(suites)} suite(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
