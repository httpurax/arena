# arena — Hermes skills

Personal collection of [Hermes Agent](https://github.com/NousResearch/hermes-agent) skills,
kept in one place so they can be copied into a Hermes install or used with other
Agent-Mode sessions.

## Skills

| Skill | What it does |
|---|---|
| [`application-security-engineering`](skills/application-security-engineering/) | Review code like a senior application security engineer — scope, threat modeling, manual review, safe validation, impact-based reporting, and root-cause remediation. Uses OWASP ASVS 5.0.0, WSTG, API Top 10:2023, and CWE. **License: UNLICENSED** (vendored; author: Zelyq; no upstream license declared). |
| [`course-material-ingestion`](skills/course-material-ingestion/) | Downloads Moodle course files under their real names (one folder per course), validates that each file is really what it claims to be, and rewrites Obsidian `[[wikilinks]]` to match what is on disk. |
| [`job-application-tracker`](skills/job-application-tracker/) | Keeps one structured job-hunt pipeline — every application, its status, the next step, and its deadline — and nudges when a next step is overdue or due within 3 days. Real data stays in an ignored `data/` file; the repo ships fictional examples only. |
| [`moodle-course-management`](skills/moodle-course-management/) | Audits Moodle materials, validates downloads, organizes local course files, and keeps manifests and wikilinks in sync. |
| [`study-flashcards`](skills/study-flashcards/) | Creates source-grounded flashcards and quizzes, with an interactive offline HTML study guide. |
| [`test-engineering`](skills/test-engineering/) | Designs reliable test strategies, local fixtures, boundary mocks, and flaky-test fixes. |

## Install the skills into Hermes

From the repo root, one command installs every skill under `skills/`:

```bash
python3 tools/install_skills.py
```

```powershell
python tools/install_skills.py
```

Each skill is **copied** (the repo copy is left alone) into the Hermes skills root, under the
category its `SKILL.md` declares, which is the layout Hermes loads:

```
<skills root>/research/course-material-ingestion/
<skills root>/productivity/job-application-tracker/
<skills root>/productivity/moodle-course-management/
<skills root>/productivity/study-flashcards/
<skills root>/software-development/application-security-engineering/
<skills root>/development/test-engineering/
```

The category is the `category` key under `metadata.hermes` in each skill's frontmatter. A skill
without one stops the run before anything is written. Re-running the installer replaces an
existing install of the same skill, so files removed from the repo do not linger behind.

| Command | Effect |
|---|---|
| `python tools/install_skills.py --dry-run` | Print what would be installed, and where. Change nothing. |
| `python tools/install_skills.py --skills-root PATH` | Install under `PATH` instead of the Hermes skills root below. |

The Hermes skills root is the first applicable entry in this table:

| # | Location | Platform |
|---|---|---|
| 1 | `--skills-root PATH` | when given |
| 2 | `$HERMES_HOME/skills` | any, when `HERMES_HOME` is set |
| 3 | `~/.hermes/skills` | Linux, macOS |
| 4 | `%LOCALAPPDATA%\hermes\skills` | Windows |

If none applies (for example, Windows with `LOCALAPPDATA` unset), the installer exits non-zero
and says what to set.

Then, in a Hermes session:

```
hermes skills list
```

To confirm the installed paths, run a helper script once by hand:

```bash
python3 "${HERMES_HOME:-$HOME/.hermes}/skills/research/course-material-ingestion/scripts/moodle_fetch.py" --help
```

```powershell
$hermes = if ($env:HERMES_HOME) { $env:HERMES_HOME } elseif ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'hermes' } else { Join-Path $HOME '.hermes' }
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
├── install_skills.py     # copies every skill into the Hermes skills root, under its category
├── test_install_skills.py# the installer's self-test (temp dirs only, no real install touched)
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
