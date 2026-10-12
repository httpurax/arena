#!/usr/bin/env python3
"""install_skills.py - copy every skill in this repo into a Hermes skills root.

    python tools/install_skills.py [--dry-run] [--skills-root PATH]

Every directory directly under skills/ that contains a SKILL.md is a skill. Its category is
read from the frontmatter key `metadata.hermes.category` (for example `research` or
`productivity`), and the skill is copied to:

    <skills-root>/<category>/<skill-name>/

which is the layout Hermes loads. Skills are copied, never moved, and an existing install of
the same skill is replaced in full, so files removed from the repo do not linger.

Skills root, first applicable entry wins:

    1. --skills-root PATH                 explicit override
    2. $HERMES_HOME/skills                any platform, when HERMES_HOME is set and non-empty
    3. ~/.hermes/skills                   Linux and macOS
    4. %LOCALAPPDATA%\\hermes\\skills        Windows

Every skill is validated before anything is written, so a skill without a usable category
stops the whole run with nothing changed.

Exit status: 0 on success (a dry run included); 1 when the skills root cannot be resolved,
a skill has no usable category, or a copy fails; 2 for bad command-line usage.

Stdlib-only. The frontmatter is read with the strict parser from tools/lint_skills.py, so the
installer and the linter agree on what a category is.
"""

from __future__ import annotations

import argparse
import ntpath
import os
import posixpath
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Mapping, Optional, Sequence

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from lint_skills import FrontmatterError, parse_frontmatter  # noqa: E402

# A category becomes a directory name under the skills root, so it must be one plain segment.
CATEGORY_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
IGNORED_ON_COPY = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")


class InstallError(Exception):
    """A condition that stops the install. Raised before any file is written, where possible."""


@dataclass(frozen=True)
class ResolvedRoot:
    """The skills root and the rule that produced it, for the report."""

    path: str
    source: str


@dataclass(frozen=True)
class PlannedInstall:
    """One skill, its category, and where it will be copied."""

    name: str
    source: Path
    category: str
    destination: Path
    replaces: bool


# ---------------------------------------------------------------------------
# skills root resolution
# ---------------------------------------------------------------------------

def resolve_skills_root(
    env: Mapping[str, str],
    home: Optional[str],
    platform_name: str,
    override: Optional[str] = None,
) -> ResolvedRoot:
    """Return the Hermes skills root, following the order in the module docstring.

    Pure: it reads only the arguments it is given, so callers and tests control the
    environment. `home` is the user's home directory, or None when it cannot be determined.
    """
    if override is not None:
        if not override.strip():
            raise InstallError("--skills-root was given an empty path")
        return ResolvedRoot(os.path.expanduser(override), "--skills-root")

    join = ntpath.join if platform_name == "win32" else posixpath.join

    hermes_home = (env.get("HERMES_HOME") or "").strip()
    if hermes_home:
        return ResolvedRoot(join(hermes_home, "skills"), "$HERMES_HOME/skills")

    if platform_name == "win32":
        local_app_data = (env.get("LOCALAPPDATA") or "").strip()
        if local_app_data:
            return ResolvedRoot(join(local_app_data, "hermes", "skills"),
                                "%LOCALAPPDATA%\\hermes\\skills")
        raise InstallError(
            "cannot resolve the Hermes skills root: HERMES_HOME and LOCALAPPDATA are both unset. "
            "Set HERMES_HOME, or pass --skills-root PATH."
        )

    if home:
        return ResolvedRoot(join(home, ".hermes", "skills"), "~/.hermes/skills")
    raise InstallError(
        "cannot resolve the Hermes skills root: HERMES_HOME is unset and the home directory is "
        "unknown. Set HERMES_HOME, or pass --skills-root PATH."
    )


def _detect_home() -> Optional[str]:
    try:
        home = str(Path.home())
    except (RuntimeError, KeyError, OSError):
        return None
    return home if os.path.isabs(home) else None


# ---------------------------------------------------------------------------
# discovery and category lookup
# ---------------------------------------------------------------------------

def discover_skills(skills_dir: Path) -> list[Path]:
    """Return every skill directory (one containing SKILL.md), sorted by name."""
    if not skills_dir.is_dir():
        raise InstallError(f"skills directory not found: {skills_dir}")
    found = [
        entry
        for entry in sorted(skills_dir.iterdir(), key=lambda p: p.name)
        if entry.is_dir()
        and not entry.name.startswith((".", "_"))
        and (entry / "SKILL.md").is_file()
    ]
    if not found:
        raise InstallError(
            f"no skills found under {skills_dir} (a skill is a directory containing SKILL.md)"
        )
    return found


def read_category(skill_dir: Path) -> str:
    """Return `metadata.hermes.category` from the skill's SKILL.md, or raise InstallError."""
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    try:
        text = skill_md.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise InstallError(f"{name}: cannot read {skill_md}: {exc}") from exc
    try:
        data = parse_frontmatter(text)
    except FrontmatterError as exc:
        raise InstallError(f"{name}: invalid frontmatter in {skill_md}: {exc}") from exc

    metadata = data.get("metadata")
    hermes = metadata.get("hermes") if isinstance(metadata, dict) else None
    category = hermes.get("category") if isinstance(hermes, dict) else None

    hint = f"add `category: <name>` under metadata.hermes in {skill_md}"
    if category is None:
        raise InstallError(f"{name}: no category declared; {hint}")
    if not isinstance(category, str) or not category.strip():
        raise InstallError(f"{name}: category must be a non-empty string; {hint}")
    category = category.strip()
    if not CATEGORY_RE.fullmatch(category):
        raise InstallError(
            f"{name}: category {category!r} is not a plain directory name "
            f"(letters, digits, '-' and '_'); {hint}"
        )
    return category


# ---------------------------------------------------------------------------
# planning and applying
# ---------------------------------------------------------------------------

def _overlaps(source: Path, destination: Path) -> bool:
    """True when the destination is the source, inside it, or contains it."""
    src = source.resolve()
    dst = destination.resolve()
    return dst == src or src in dst.parents or dst in src.parents


def build_plan(skill_dirs: Sequence[Path], root: Path) -> list[PlannedInstall]:
    """Validate every skill and compute its destination. Writes nothing."""
    if root.exists() and not root.is_dir():
        raise InstallError(f"skills root {root} exists and is not a directory")

    plans: list[PlannedInstall] = []
    for skill_dir in skill_dirs:
        category = read_category(skill_dir)
        category_dir = root / category
        if category_dir.exists() and not category_dir.is_dir():
            raise InstallError(
                f"{skill_dir.name}: {category_dir} exists and is not a directory"
            )
        destination = category_dir / skill_dir.name
        if _overlaps(skill_dir, destination):
            raise InstallError(
                f"{skill_dir.name}: destination {destination} overlaps the skill's own source; "
                "choose a skills root outside the repository's skills/ tree"
            )
        plans.append(PlannedInstall(
            name=skill_dir.name,
            source=skill_dir,
            category=category,
            destination=destination,
            replaces=destination.exists() or destination.is_symlink(),
        ))
    return plans


def _remove_existing(destination: Path) -> None:
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
    elif destination.is_dir():
        shutil.rmtree(destination)


def apply_plan(plans: Sequence[PlannedInstall], *, dry_run: bool, out: IO[str]) -> None:
    """Copy each planned skill into place, or only describe the copy when dry_run is set."""
    for item in plans:
        if dry_run:
            verb = "would replace" if item.replaces else "would install"
            print(f"DRY-RUN    {item.name}: {verb} {item.destination}", file=out)
            continue
        try:
            _remove_existing(item.destination)
            item.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(item.source, item.destination, ignore=IGNORED_ON_COPY)
        except OSError as exc:
            raise InstallError(
                f"{item.name}: copy to {item.destination} failed: {exc}"
            ) from exc
        label = "REPLACED" if item.replaces else "INSTALLED"
        print(f"{label}  {item.name} ({item.category}) -> {item.destination}", file=out)


# ---------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------

def main(
    argv: Optional[Sequence[str]] = None,
    *,
    env: Optional[Mapping[str, str]] = None,
    home: Optional[str] = None,
    platform_name: Optional[str] = None,
    skills_dir: Path = SKILLS_DIR,
    stdout: Optional[IO[str]] = None,
    stderr: Optional[IO[str]] = None,
) -> int:
    """Run the installer. Returns the process exit status.

    With env=None the real environment, home directory, and platform are used. Passing env
    lets callers (the self-test) pin all three without touching the machine's Hermes install.
    """
    out = sys.stdout if stdout is None else stdout
    err = sys.stderr if stderr is None else stderr

    parser = argparse.ArgumentParser(
        prog="install_skills.py",
        description="Copy every skill under skills/ into the Hermes skills root, "
                    "under its category.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would be installed and change nothing")
    parser.add_argument("--skills-root", metavar="PATH",
                        help="install under PATH instead of the resolved Hermes skills root")
    args = parser.parse_args(argv)

    if env is None:
        env = os.environ
        if home is None:
            home = _detect_home()
    if platform_name is None:
        platform_name = sys.platform

    try:
        resolved = resolve_skills_root(env, home, platform_name, args.skills_root)
        root = Path(resolved.path)
        plans = build_plan(discover_skills(skills_dir), root)
    except InstallError as exc:
        print(f"ERROR  {exc}", file=err)
        return 1

    state = "" if root.exists() else ", does not exist yet"
    print(f"Skills root: {root} (from {resolved.source}{state})", file=out)

    try:
        apply_plan(plans, dry_run=args.dry_run, out=out)
    except InstallError as exc:
        print(f"ERROR  {exc}", file=err)
        return 1

    count = len(plans)
    noun = "skill" if count == 1 else "skills"
    if args.dry_run:
        print(f"Dry run: {count} {noun} would be installed; nothing was changed.", file=out)
    else:
        print(f"Installed {count} {noun} into {root}.", file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
