# arena — Hermes skills

Personal collection of [Hermes Agent](https://github.com/NousResearch/hermes-agent) skills,
kept in one place so they can be copied into a Hermes install or used with other
Agent-Mode sessions.

## Skills

| Skill | What it does |
|---|---|
| [`course-material-ingestion`](skills/course-material-ingestion/) | Downloads Moodle course files under their real names (one folder per course), validates that each file is really what it claims to be, and rewrites Obsidian `[[wikilinks]]` to match what is on disk. |
| [`moodle-course-management`](skills/moodle-course-management/) | Audits Moodle materials, validates downloads, organizes local course files, and keeps manifests and wikilinks in sync. |

## Install a skill into Hermes

Hermes loads user skills from a skills root, resolved in this order:

| # | Location | Platform |
|---|---|---|
| 1 | `$HERMES_HOME/skills/<category>/<skill-name>/` | any, when `HERMES_HOME` is set |
| 2 | `~/.hermes/skills/...` | Linux, macOS |
| 3 | `%LOCALAPPDATA%\hermes\skills\...` | Windows |

Copy the folder into place (this keeps the layout the `SKILL.md` frontmatter expects):

```bash
mkdir -p "${HERMES_HOME:-$HOME/.hermes}/skills/research"
cp -r skills/course-material-ingestion "${HERMES_HOME:-$HOME/.hermes}/skills/research/"
```

**PowerShell (Windows):**

```powershell
$hermes = if ($env:HERMES_HOME) { $env:HERMES_HOME } elseif ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'hermes' } else { Join-Path $HOME '.hermes' }
New-Item -ItemType Directory -Force -Path (Join-Path $hermes 'skills/research')
Copy-Item -Recurse -Force skills/course-material-ingestion (Join-Path $hermes 'skills/research/')
```

> **PowerShell gotcha:** a trailing `\` does *not* continue a line the way it does in bash —
> it is passed through as a literal backslash. Use the backtick (`` ` ``), or write the
> command on one line as above.

Then, in a Hermes session:

```
hermes skills list
```

If the skill has a helper script, run it once by hand to confirm the path:

```bash
python3 "${HERMES_HOME:-$HOME/.hermes}/skills/research/course-material-ingestion/scripts/moodle_fetch.py" --help
```

```powershell
python (Join-Path $hermes 'skills/research/course-material-ingestion/scripts/moodle_fetch.py') --help
```

On Windows the interpreter is `python` (or `py -3`); `python3` only exists if the Microsoft
Store alias is installed. Paths the script is given — `--dest "~/Courses"`, `--manifest
"~/Courses/manifest.json"` — are expanded by the script itself with `Path.expanduser()`
(`%USERPROFILE%` on Windows, `$HOME` elsewhere), so `~` needs no help from the shell on
either platform.

## Repo layout

```
skills/<skill-name>/
├── SKILL.md              # frontmatter + instructions the agent loads
├── scripts/              # stdlib-only helpers the skill calls
├── references/           # longer docs the skill points at
├── examples/             # sample inputs
└── tests/                # stdlib unittest suite, no network
tools/
├── lint_skills.py        # conformance gate: frontmatter, compile, secrets, tests
├── test_lint_skills.py   # the linter's self-test (broken fixture rejected, repo accepted)
└── fixtures/broken-skill # a deliberately non-conforming skill, committed for that test
```

## Running the tests

[![tests](https://github.com/httpurax/arena/actions/workflows/test.yml/badge.svg)](https://github.com/httpurax/arena/actions/workflows/test.yml)

CI runs this suite on `ubuntu-latest` and `windows-latest` across Python 3.11 and 3.12, with no
install step — the skill is stdlib-only, so there is nothing to resolve before the tests:

```bash
cd skills/course-material-ingestion
python3 -m unittest discover -s tests -v
```

```powershell
cd skills/course-material-ingestion
python -m unittest discover -s tests -v
```

The suite spins up a throwaway localhost HTTP server that imitates Moodle's
`view.php` → `pluginfile.php` redirects, `Content-Disposition` filenames, a login redirect,
an HTML error page served with a `.pdf` name, and a session that expires halfway through a
plan, so the failure paths are actually exercised rather than described. It also covers the
session-cookie sources (precedence, Netscape parsing, stdin) and asserts the invariant that
the cookie value never appears in `manifest.json`, on stdout, or in an error message.

## Linting

`tools/lint_skills.py` is the conformance gate for everything under `skills/`. For every
directory directly under it, it checks that `SKILL.md` exists and its frontmatter is valid
YAML with non-empty `name`, `description`, `version`, `license`, and `platforms` (where
`name` matches the directory, `version` is `X.Y.Z`, and each platform is `linux`, `macos`,
or `windows`); that every `.py` file compiles; that no text file carries an embedded
credential; and that a skill shipping a `tests/` directory passes
`python -m unittest discover -s tests`. It is stdlib-only, so it runs on a bare interpreter:

```bash
python3 tools/lint_skills.py          # exit 0 = every skill conforms, non-zero = file + rule
```

Failures name the exact file, line, and rule, and never echo the matched value of a
suspected secret. The scan covers credential-named literals (`api_key = "…"`,
`password = "…"`, PEM private-key blocks), vendor key formats, and basic-auth URLs; it
deliberately does not flag the bare name `secret`, because the test suite here uses a
constant named `SECRET` as a fake canary, and an allowlist would only weaken the signal.

`tools/test_lint_skills.py` is the linter's own self-test: the broken fixture under
`tools/fixtures/broken-skill/` (missing `description`, `version: 1.0`, two fake secrets)
must be rejected with those rules named, and this repo must pass. CI runs the linter and
its self-test on the same matrix as the skill suite.

## Conventions

- `description` in the frontmatter stays under 60 characters — Hermes truncates long ones in
  listings.
- Scripts are stdlib-only so a skill never adds a dependency to the host environment.
- Anything the skill can get wrong is covered by a test.
- Commands in `SKILL.md` are shown for bash *and* PowerShell when a skill supports Windows;
  a session cookie is taken transiently (`--cookie-env`, `--cookie-file -`) rather than from
  a file, and its value is never echoed, logged, or written to an artifact.
