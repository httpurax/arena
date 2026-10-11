# arena — Hermes skills

Personal collection of [Hermes Agent](https://github.com/NousResearch/hermes-agent) skills,
kept in one place so they can be copied into a Hermes install or used with other
Agent-Mode sessions.

## Skills

| Skill | What it does |
|---|---|
| [`course-material-ingestion`](skills/course-material-ingestion/) | Downloads Moodle course files under their real names (one folder per course), validates that each file is really what it claims to be, and rewrites Obsidian `[[wikilinks]]` to match what is on disk. |

## Install a skill into Hermes

Hermes loads user skills from `~/.hermes/skills/<category>/<skill-name>/`. Copy the folder
into place (this keeps the layout the `SKILL.md` frontmatter expects):

```bash
mkdir -p ~/.hermes/skills/research
cp -r skills/course-material-ingestion ~/.hermes/skills/research/
```

Then, in a Hermes session:

```
hermes skills list
```

If the skill has a helper script, run it once by hand to confirm the path:

```bash
python3 ~/.hermes/skills/research/course-material-ingestion/scripts/moodle_fetch.py --help
```

## Repo layout

```
skills/<skill-name>/
├── SKILL.md              # frontmatter + instructions the agent loads
├── scripts/              # stdlib-only helpers the skill calls
├── references/           # longer docs the skill points at
├── examples/             # sample inputs
└── tests/                # stdlib unittest suite, no network
```

## Running the tests

```bash
cd skills/course-material-ingestion
python3 -m unittest discover -s tests -v
```

The suite spins up a throwaway localhost HTTP server that imitates Moodle's
`view.php` → `pluginfile.php` redirects, `Content-Disposition` filenames, a login redirect,
and an HTML error page served with a `.pdf` name, so the failure paths are actually
exercised rather than described.

## Conventions

- `description` in the frontmatter stays under 60 characters — Hermes truncates long ones in
  listings.
- Scripts are stdlib-only so a skill never adds a dependency to the host environment.
- Anything the skill can get wrong is covered by a test.
