#!/usr/bin/env python3
"""lint_skills.py - conformance gate for every skill in this repo.

Rules applied to each directory directly under the skills root:

    skill_md     SKILL.md exists
    frontmatter  the frontmatter block is valid YAML in the subset this checker accepts and
                 the required keys exist, are non-empty, and are well-formed: `name` equals
                 the directory name, `version` is X.Y.Z, every `platforms` entry is one of
                 linux / macos / windows
    python       every .py file under the skill compiles (py_compile, no bytecode left behind)
    secrets      no text file contains an embedded credential: a credential-named literal
                 (api_key = "...", password = "...", ...), a PEM private key block, a
                 basic-auth URL, or a vendor key format (AWS, GitHub, Slack, Google, sk-...)
    tests        when the skill ships a tests/ directory, `python -m unittest discover -s tests`
                 passes from the skill directory

Exit status is 0 only when every skill passes. A failure names the exact file, line, and
rule, and never echoes the matched value of a suspected secret.

The frontmatter parser is a deliberately small, strict YAML subset rather than a YAML
library, because this has to run on a bare interpreter with no third-party packages. It
accepts what SKILL.md frontmatter in this repo actually uses - block mappings, nested block
mappings, block and flow lists of scalars, plain/single/double-quoted scalars, comments -
and reports everything else (anchors, aliases, tags, block scalars, flow mappings, tabs for
indentation, multi-line plain scalars) as an error instead of guessing. That direction is
intentional: an unsupported-but-valid construct gets a clear message, while invalid YAML can
never be waved through.

Usage:
    python tools/lint_skills.py [skills-root]

The optional argument defaults to <repo>/skills and exists so the self-test in
tools/test_lint_skills.py can point this same checker at a fixture tree.
"""

from __future__ import annotations

import argparse
import os
import py_compile
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOT = REPO_ROOT / "skills"

REQUIRED_KEYS = ("name", "description", "version", "license", "platforms")
ALLOWED_PLATFORMS = ("linux", "macos", "windows")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")

# Directories that are never part of a skill's source: build caches, VCS metadata, virtualenvs.
SKIP_DIR_NAMES = frozenset(
    {"__pycache__", ".git", ".hg", ".svn", ".mypy_cache", ".pytest_cache", ".ruff_cache",
     "node_modules", "venv", ".venv", ".tox", ".nox"}
)
SKIP_FILE_SUFFIXES = frozenset({".pyc", ".pyo", ".pyd", ".so", ".dylib", ".dll", ".zip",
                                ".gz", ".whl", ".png", ".jpg", ".jpeg", ".gif", ".ico",
                                ".pdf", ".woff", ".woff2", ".ttf"})

TESTS_TIMEOUT_SECONDS = 600
TEST_OUTPUT_TAIL_LINES = 25


# ---------------------------------------------------------------------------
# embedded-secret patterns
# ---------------------------------------------------------------------------

def _quoted_literal(key_pattern: str) -> "re.Pattern[str]":
    """`<key> = "..."` or `<key>: '...'` for any of the credential names in key_pattern.

    Keys are matched case-insensitively. The value must be quoted and non-empty, so prose
    ("never print the password, log it, ...") and code that reads a value from the
    environment (`password = os.environ["X"]`) do not trip the rule.
    """
    return re.compile(r"(?i)\b(?:%s)\b\s*[:=]\s*['\"][^'\"]+['\"]" % key_pattern)


# Bare `secret = "..."` is deliberately NOT a rule here. This repo's own test suite uses a
# module constant named SECRET as an intentional fake - a canary proving the session cookie
# never reaches stdout, stderr, or manifest.json - and matching it would force an allowlist.
# Scoped names (client_secret, secret_key, api_secret, ...) are covered instead: real
# credentials in these skills always carry a scoped name, so nothing loses protection.
#
# Rule names are stable identifiers: tools/test_lint_skills.py and CI output refer to them.
SECRET_PATTERNS: "tuple[tuple[str, re.Pattern[str]], ...]" = (
    ("private-key-block", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("api-key-literal", _quoted_literal(r"api[_-]?key")),
    ("password-literal", _quoted_literal(r"passwd|password|pwd")),
    ("client-secret-literal",
     _quoted_literal(r"client[_-]?secret|secret[_-]?key|api[_-]?secret|app[_-]?secret")),
    ("access-key-literal",
     _quoted_literal(r"access[_-]?key(?:[_-]?id)?|aws[_-]?secret[_-]?access[_-]?key")),
    ("token-literal",
     _quoted_literal(r"access[_-]?token|auth[_-]?token|api[_-]?token|bearer[_-]?token|"
                     r"refresh[_-]?token|id[_-]?token|token")),
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("openai-style-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("github-token",
     re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("basic-auth-url", re.compile(r"\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s:@]+@")),
)


# ---------------------------------------------------------------------------
# frontmatter: a strict YAML subset
# ---------------------------------------------------------------------------

class FrontmatterError(ValueError):
    """The frontmatter is missing, unclosed, or not YAML in the accepted subset."""


@dataclass
class _Entry:
    """One significant frontmatter line: its line number in SKILL.md, indent, and text."""

    number: int
    indent: int
    text: str


def _strip_comment(text: str) -> str:
    """Drop a trailing `# comment`, ignoring `#` inside quotes.

    A `#` starts a comment only at the start of the text or after whitespace, matching YAML.
    """
    out: "list[str]" = []
    quote = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            if quote == '"' and ch == "\\" and i + 1 < len(text):
                out.append(text[i:i + 2])  # kept verbatim; escapes are the parser's job
                i += 2
                continue
            if ch == quote:
                if quote == "'" and text[i:i + 2] == "''":
                    # a doubled '' is an escaped quote inside the scalar, not the end of it
                    out.append("''")
                    i += 2
                    continue
                quote = ""
            out.append(ch)
            i += 1
            continue
        if ch in "\"'":
            quote = ch
        elif ch == "#" and (not out or out[-1] in " \t"):
            break
        out.append(ch)
        i += 1
    return "".join(out).rstrip()


def _tokenize(body: "Sequence[str]", first_line_number: int) -> "list[_Entry]":
    """Turn frontmatter body lines into significant entries, rejecting tabs for indentation."""
    entries: "list[_Entry]" = []
    for offset, raw in enumerate(body):
        number = first_line_number + offset
        if raw.strip() == "":
            continue
        leading = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in leading:
            raise FrontmatterError(
                f"line {number}: tab character in indentation (YAML forbids tabs as indentation)"
            )
        text = _strip_comment(raw[len(leading):])
        if text.strip() == "":
            continue
        entries.append(_Entry(number, len(leading), text))
    return entries


def _parse_quoted(text: str, number: int) -> str:
    """Parse a single- or double-quoted scalar that must span the whole of `text`."""
    quote = text[0]
    out: "list[str]" = []
    i = 1
    escapes = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'", "0": "\0"}
    while i < len(text):
        ch = text[i]
        if quote == '"' and ch == "\\":
            if i + 1 >= len(text):
                raise FrontmatterError(f"line {number}: unterminated escape in quoted scalar")
            nxt = text[i + 1]
            out.append(escapes.get(nxt, nxt))
            i += 2
            continue
        if ch == quote:
            if quote == "'" and text[i:i + 2] == "''":
                out.append("'")
                i += 2
                continue
            trailing = text[i + 1:].strip()
            if trailing:
                raise FrontmatterError(
                    f"line {number}: unexpected text after a quoted scalar: {trailing!r}"
                )
            return "".join(out)
        out.append(ch)
        i += 1
    name = "single" if quote == "'" else "double"
    raise FrontmatterError(f"line {number}: unterminated {name}-quoted scalar")


def _split_flow_items(inner: str, number: int) -> "list[str]":
    """Split a flow sequence body on top-level commas, honouring quoted commas."""
    items: "list[str]" = []
    buf: "list[str]" = []
    quote = ""
    i = 0
    while i < len(inner):
        ch = inner[i]
        if quote:
            buf.append(ch)
            if quote == '"' and ch == "\\" and i + 1 < len(inner):
                buf.append(inner[i + 1])
                i += 2
                continue
            if ch == quote:
                if quote == "'" and inner[i:i + 2] == "''":
                    buf.append("'")
                    i += 2
                    continue
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
        elif ch in "[]{":
            raise FrontmatterError(
                f"line {number}: nested collections inside a flow sequence are not supported"
            )
        elif ch == ",":
            items.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if quote:
        raise FrontmatterError(f"line {number}: unterminated quoted scalar in a flow sequence")
    items.append("".join(buf))
    return items


def _parse_flow_sequence(text: str, number: int) -> "list[Any]":
    if not text.endswith("]"):
        raise FrontmatterError(f"line {number}: unterminated flow sequence {text!r}")
    inner = text[1:-1].strip()
    if not inner:
        return []
    values = []
    for part in _split_flow_items(inner, number):
        part = part.strip()
        if part == "":
            raise FrontmatterError(f"line {number}: empty item in flow sequence {text!r}")
        values.append(_parse_value(part, number))
    return values


def _parse_value(text: str, number: int) -> Any:
    """Parse one inline scalar or flow sequence."""
    if text[:1] in ("'", '"'):
        return _parse_quoted(text, number)
    if text.startswith("["):
        return _parse_flow_sequence(text, number)
    if text.startswith("{"):
        raise FrontmatterError(
            f"line {number}: flow mappings ({{...}}) are not supported; use block mappings"
        )
    if text[:1] in ("|", ">"):
        raise FrontmatterError(
            f"line {number}: block scalars ({text[:1]}) are not supported; use a quoted scalar"
        )
    if text[:1] in ("&", "*", "!", "?", "@", "`"):
        raise FrontmatterError(
            f"line {number}: anchors, aliases, tags, and directives are not supported: {text!r}"
        )
    if text == "-" or text.startswith("- "):
        raise FrontmatterError(
            f"line {number}: a sequence entry is not a value; use a flow sequence or put the "
            f"list on the next line: {text!r}"
        )
    if text[:1] in (",", "]", "}"):
        raise FrontmatterError(f"line {number}: {text[:1]!r} cannot start a scalar: {text!r}")
    if ": " in text or text.endswith(":"):
        raise FrontmatterError(
            f"line {number}: a plain scalar cannot contain ': '; quote it: {text!r}"
        )
    return text


def _split_key(text: str, number: int) -> "tuple[str, str]":
    """Split `key:` / `key: value` into its parts, accepting only simple plain keys."""
    if text.endswith(":"):
        key, rest = text[:-1].strip(), ""
    else:
        match = re.match(r"^(.*?):[ \t]+(.*)$", text)
        if not match:
            raise FrontmatterError(
                f"line {number}: expected 'key: value' or 'key:' with a nested block: {text!r}"
            )
        key, rest = match.group(1).strip(), match.group(2).strip()
    if not key:
        raise FrontmatterError(f"line {number}: empty mapping key")
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.\-]*", key):
        raise FrontmatterError(f"line {number}: unsupported mapping key {key!r}")
    return key, rest


def _looks_like_list_mapping(text: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9_.\-]+:", text))


def _parse_mapping(entries: "Sequence[_Entry]", i: int, indent: int) -> "tuple[dict[str, Any], int]":
    mapping: "dict[str, Any]" = {}
    while i < len(entries) and entries[i].indent == indent:
        entry = entries[i]
        if entry.text.startswith("- "):
            raise FrontmatterError(
                f"line {entry.number}: unexpected list item inside a mapping: {entry.text!r}"
            )
        key, rest = _split_key(entry.text, entry.number)
        if key in mapping:
            raise FrontmatterError(f"line {entry.number}: duplicate key {key!r}")
        if rest == "":
            if i + 1 < len(entries) and entries[i + 1].indent > indent:
                mapping[key], i = _parse_block(entries, i + 1, entries[i + 1].indent)
            else:
                mapping[key], i = None, i + 1
        else:
            mapping[key] = _parse_value(rest, entry.number)
            i += 1
    if i < len(entries) and entries[i].indent > indent:
        raise FrontmatterError(
            f"line {entries[i].number}: bad indentation for {entries[i].text!r} "
            f"(indent {entries[i].indent}, expected {indent})"
        )
    return mapping, i


def _parse_sequence(entries: "Sequence[_Entry]", i: int, indent: int) -> "tuple[list[Any], int]":
    items: "list[Any]" = []
    while i < len(entries) and entries[i].indent == indent and (
        entries[i].text == "-" or entries[i].text.startswith("- ")
    ):
        entry = entries[i]
        rest = entry.text[1:].strip()
        if rest == "":
            if i + 1 < len(entries) and entries[i + 1].indent > indent:
                value, i = _parse_block(entries, i + 1, entries[i + 1].indent)
            else:
                value, i = None, i + 1
        else:
            if _looks_like_list_mapping(rest):
                raise FrontmatterError(
                    f"line {entry.number}: list items that open a mapping are not supported; "
                    f"use a flow sequence or plain scalars: {rest!r}"
                )
            value = _parse_value(rest, entry.number)
            i += 1
        items.append(value)
    if i < len(entries) and entries[i].indent > indent:
        raise FrontmatterError(
            f"line {entries[i].number}: bad indentation for {entries[i].text!r} "
            f"(indent {entries[i].indent}, expected {indent})"
        )
    return items, i


def _parse_block(entries: "Sequence[_Entry]", i: int, indent: int) -> "tuple[Any, int]":
    if entries[i].text == "-" or entries[i].text.startswith("- "):
        return _parse_sequence(entries, i, indent)
    return _parse_mapping(entries, i, indent)


def parse_frontmatter(text: str) -> "dict[str, Any]":
    """Return the frontmatter mapping of a SKILL.md body, or raise FrontmatterError."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("missing frontmatter: the file must start with a '---' line")
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
        if lines[index].strip() == "...":
            raise FrontmatterError(
                f"line {index + 1}: '...' is not a valid frontmatter terminator; use '---'"
            )
    if end is None:
        raise FrontmatterError("frontmatter is never closed with a '---' line")
    entries = _tokenize(lines[1:end], first_line_number=2)
    if not entries:
        raise FrontmatterError("frontmatter is empty")
    if entries[0].indent != 0:
        raise FrontmatterError(
            f"line {entries[0].number}: frontmatter must start at column 0, not indented"
        )
    value, index = _parse_block(entries, 0, 0)
    if index != len(entries):
        raise FrontmatterError(
            f"line {entries[index].number}: could not parse {entries[index].text!r}"
        )
    if not isinstance(value, dict):
        raise FrontmatterError("frontmatter must be a YAML mapping of keys to values")
    return value


# ---------------------------------------------------------------------------
# frontmatter rule checks
# ---------------------------------------------------------------------------

def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _check_frontmatter(data: "dict[str, Any]", skill_name: str) -> "list[tuple[str, str]]":
    """Return (rule, message) pairs for every frontmatter violation."""
    problems: "list[tuple[str, str]]" = []

    for key in REQUIRED_KEYS:
        if key not in data:
            problems.append((f"frontmatter.{key}", f"required key {key!r} is missing"))
        elif _is_empty(data[key]):
            problems.append((f"frontmatter.{key}", f"required key {key!r} is empty"))

    name = data.get("name")
    if name is not None and not isinstance(name, str):
        problems.append(("frontmatter.name", f"name must be a scalar string, got {type(name).__name__}"))
    elif isinstance(name, str):
        if name != skill_name:
            problems.append((
                "frontmatter.name",
                f"name {name!r} does not match the directory name {skill_name!r}",
            ))

    description = data.get("description")
    if description is not None and not isinstance(description, str):
        problems.append((
            "frontmatter.description",
            f"description must be a scalar string, got {type(description).__name__}",
        ))

    version = data.get("version")
    if version is not None and not isinstance(version, str):
        problems.append((
            "frontmatter.version",
            f"version must be a scalar string, got {type(version).__name__}",
        ))
    elif isinstance(version, str) and version and not VERSION_RE.match(version):
        problems.append((
            "frontmatter.version",
            f"version {version!r} is not X.Y.Z (three dot-separated integers, e.g. 1.2.2)",
        ))

    if isinstance(description, str) and len(description) > 60:
        problems.append(("frontmatter.description", "description exceeds 60 characters"))

    license_value = data.get("license")
    if license_value is not None and not isinstance(license_value, str):
        problems.append((
            "frontmatter.license",
            f"license must be a scalar string, got {type(license_value).__name__}",
        ))

    platforms = data.get("platforms")
    if platforms is not None:
        if not isinstance(platforms, list):
            problems.append((
                "frontmatter.platforms",
                f"platforms must be a list, got {type(platforms).__name__}",
            ))
        else:
            allowed = ", ".join(ALLOWED_PLATFORMS)
            for entry in platforms:
                if not isinstance(entry, str) or entry not in ALLOWED_PLATFORMS:
                    problems.append((
                        "frontmatter.platforms",
                        f"platforms entry {entry!r} is not one of: {allowed}",
                    ))

    return problems


# ---------------------------------------------------------------------------
# per-rule checks
# ---------------------------------------------------------------------------

@dataclass
class Problem:
    """One failed rule, tied to the file (and line, when known) that failed it."""

    path: Path
    rule: str
    message: str
    line: "Optional[int]" = None
    detail: str = ""

    def render(self, display: str) -> "list[str]":
        location = f"{display}:{self.line}" if self.line else display
        lines = [f"{location}  [{self.rule}] {self.message}"]
        for detail_line in self.detail.splitlines():
            lines.append(f"      | {detail_line}")
        return lines


@dataclass
class SkillResult:
    """Everything the linter learned about one skill."""

    name: str
    path: Path
    problems: "list[Problem]" = field(default_factory=list)
    notes: "list[str]" = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def _skipped(path: Path, root: Path) -> bool:
    """True for files that are build output rather than skill source."""
    relative = path.relative_to(root)
    if any(part in SKIP_DIR_NAMES or part.startswith(".") for part in relative.parts[:-1]):
        return True
    return path.suffix.lower() in SKIP_FILE_SUFFIXES


def _iter_files(root: Path, suffix: str = "") -> "list[Path]":
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and not _skipped(path, root)
        and (not suffix or path.suffix.lower() == suffix)
    )


def _check_python(skill_dir: Path) -> "tuple[int, list[Problem]]":
    """Compile every .py file. Bytecode goes to a temp dir so the tree stays clean."""
    problems: "list[Problem]" = []
    py_files = _iter_files(skill_dir, ".py")
    with tempfile.TemporaryDirectory(prefix="lint-skills-pyc-") as tmp:
        for index, path in enumerate(py_files):
            cfile = os.path.join(tmp, f"{index:04d}.pyc")
            try:
                py_compile.compile(str(path), cfile=cfile, doraise=True)
            except py_compile.PyCompileError as exc:
                line = getattr(exc, "lineno", None)
                message = getattr(exc, "msg", None) or str(exc)
                problems.append(Problem(path, "python.compile", str(message).strip(), line))
            except (OSError, ValueError) as exc:
                problems.append(Problem(path, "python.compile", str(exc).strip()))
    return len(py_files), problems


def _is_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return b"\x00" in handle.read(8192)
    except OSError:
        return True


def _check_secrets(skill_dir: Path) -> "tuple[int, list[Problem]]":
    """Scan every text file in the skill for embedded credentials."""
    problems: "list[Problem]" = []
    scanned = 0
    for path in _iter_files(skill_dir):
        if _is_binary(path):
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            problems.append(Problem(path, "secrets.unreadable", str(exc).strip()))
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for rule_name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    # Never echo the match: the report names the rule and the location only.
                    problems.append(Problem(
                        path, f"secrets.{rule_name}",
                        "embedded credential-like literal "
                        "(value withheld; move it to an environment variable or the runtime arg)",
                        number,
                    ))
    return scanned, problems


def _tail(text: str, limit: int = TEST_OUTPUT_TAIL_LINES) -> str:
    lines = text.strip().splitlines()
    return "\n".join(lines[-limit:])


def _run_tests(skill_dir: Path) -> "tuple[Optional[str], list[Problem]]":
    """Run `python -m unittest discover -s tests` for the skill, if it has a tests/ dir."""
    tests_dir = skill_dir / "tests"
    if not tests_dir.is_dir():
        return None, []

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"  # keep a Windows console from choking on the output
    env.pop("PYTHONPATH", None)  # the skill's own tree must stand on its own
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]
    try:
        proc = subprocess.run(
            command, cwd=str(skill_dir), env=env, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=TESTS_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, [Problem(
            skill_dir, "tests.timeout",
            f"python -m unittest discover -s tests did not finish in {TESTS_TIMEOUT_SECONDS}s",
        )]
    except OSError as exc:
        return None, [Problem(skill_dir, "tests.failed", f"could not run the suite: {exc}")]

    stdout = proc.stdout.decode("utf-8", "replace")
    stderr = proc.stderr.decode("utf-8", "replace")
    combined = stdout + stderr
    match = re.search(r"^Ran (\d+) tests? in ", combined, re.MULTILINE)
    count = match.group(1) if match else None

    if proc.returncode != 0:
        ran = f" ({count} tests ran)" if count else ""
        problems = [Problem(
            tests_dir, "tests.failed",
            f"python -m unittest discover -s tests exited {proc.returncode}{ran}",
            detail=_tail(combined),
        )]
        return count, problems
    if count is None:
        return None, [Problem(
            tests_dir, "tests.failed",
            "the suite reported success but ran no tests",
        )]
    return count, []


# ---------------------------------------------------------------------------
# one skill, then all of them
# ---------------------------------------------------------------------------

def check_skill(skill_dir: Path) -> SkillResult:
    """Apply every rule to one skill directory."""
    result = SkillResult(name=skill_dir.name, path=skill_dir)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        result.problems.append(Problem(skill_md, "skill_md.missing", "SKILL.md does not exist"))
        result.notes.append("no SKILL.md")
    else:
        try:
            text = skill_md.read_text(encoding="utf-8-sig")
        except OSError as exc:
            result.problems.append(Problem(skill_md, "skill_md.unreadable", str(exc).strip()))
        else:
            try:
                data = parse_frontmatter(text)
            except FrontmatterError as exc:
                result.problems.append(Problem(skill_md, "frontmatter.invalid", str(exc)))
                result.notes.append("frontmatter invalid")
            else:
                violations = _check_frontmatter(data, skill_dir.name)
                result.problems.extend(
                    Problem(skill_md, rule, message) for rule, message in violations
                )
                result.notes.append("frontmatter ok" if not violations else "frontmatter invalid")

    py_count, py_problems = _check_python(skill_dir)
    result.problems.extend(py_problems)
    if not py_problems:
        noun = "file" if py_count == 1 else "files"
        result.notes.append(f"{py_count} .py {noun} compile" if py_count else "no .py files")

    scanned, secret_problems = _check_secrets(skill_dir)
    result.problems.extend(secret_problems)
    if not secret_problems:
        noun = "file" if scanned == 1 else "files"
        result.notes.append(f"secret scan clean ({scanned} text {noun})")

    test_count, test_problems = _run_tests(skill_dir)
    result.problems.extend(test_problems)
    if test_problems:
        result.notes.append("tests failed")
    elif test_count is None:
        result.notes.append("no tests/ directory")
    else:
        noun = "test" if test_count == "1" else "tests"
        result.notes.append(f"tests: {test_count} {noun} passed")

    return result


def _display(path: Path) -> str:
    """Render a path for the report, with forward slashes on every platform.

    Repo-relative when the path is inside the working directory (the common case in CI),
    absolute otherwise. Forward slashes everywhere because the report is read by humans and
    CI on Windows too, and a stray `\\` would not match the paths quoted out of it.
    """
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _skill_dirs(root: Path) -> "list[Path]":
    """Every directory directly under the root: each one is a skill and must conform.

    Hidden directories (`.github`, `.venv`, ...) are tooling, not skills. `__pycache__` is
    build output. Nothing else is skipped: a directory without a SKILL.md is a failure, not
    a silent omission.
    """
    return sorted(
        (path for path in root.iterdir()
         if path.is_dir() and not path.name.startswith(".") and path.name not in SKIP_DIR_NAMES),
        key=lambda path: path.name,
    )


def lint(root: Path, out: "Iterable[str]" = sys.stdout) -> int:
    """Lint every skill under root; write the report to out; return the exit status."""
    write = out.write if hasattr(out, "write") else out.append
    write(f"skill conformance lint: {_display(root)}\n")

    results = [check_skill(skill_dir) for skill_dir in _skill_dirs(root)]
    if not results:
        write(f"FAIL  no skill directories found under {_display(root)}\n")
        return 1

    failed = [result for result in results if not result.ok]
    width = max(len(result.name) for result in results)

    for result in results:
        if result.ok:
            write(f"OK    {result.name:<{width}}  {'; '.join(result.notes)}\n")
        else:
            count = len(result.problems)
            noun = "problem" if count == 1 else "problems"
            write(f"FAIL  {result.name:<{width}}  {count} {noun}\n")
            for problem in result.problems:
                for line in problem.render(_display(problem.path)):
                    write(f"          {line}\n")

    ok_count = len(results) - len(failed)
    write(f"\n{len(results)} {'skill' if len(results) == 1 else 'skills'} checked: "
          f"{ok_count} ok, {len(failed)} failed\n")
    return 1 if failed else 0


def _configure_output() -> None:
    """Force UTF-8 on stdout/stderr.

    CI on Windows redirects these to a pipe, where Python falls back to the ANSI codepage;
    a report quotes text taken from the skills (a bad scalar, a failing suite's output),
    which can contain anything, and an encoding error in the linter would be reported as a
    crash instead of a rule failure.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):  # a stream that cannot be reconfigured
                pass


def main(argv: "Optional[Sequence[str]]" = None) -> int:
    _configure_output()
    parser = argparse.ArgumentParser(
        prog="lint_skills.py",
        description="Check every skill under a skills root for conformance.",
    )
    parser.add_argument(
        "root", nargs="?", default=str(DEFAULT_ROOT),
        help=f"skills root to lint (default: {DEFAULT_ROOT})",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR  {args.root}: not a directory", file=sys.stderr)
        return 2
    return lint(root)


if __name__ == "__main__":
    sys.exit(main())
