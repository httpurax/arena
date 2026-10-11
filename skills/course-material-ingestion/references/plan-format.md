# Plan format for `moodle_fetch.py download`

`download` takes one JSON file describing what to fetch. It is written by hand or, better,
generated from `discover` output. A plan is either a single course object or a list of them.

## Shape

```json
[
  {
    "course": "Comprehension and Oral Expression 1",
    "resources": [
      { "id": 42, "url": "https://moodle.example.com/mod/resource/view.php?id=42",
        "title": "References" },
      { "id": 43, "url": "https://moodle.example.com/mod/resource/view.php?id=43" }
    ]
  },
  {
    "course": "University Work Techniques 1",
    "resources": [
      { "id": 91, "url": "https://moodle.example.com/mod/resource/view.php?id=91",
        "title": "1.1 Become an active learner" }
    ]
  }
]
```

| Field | Required | Notes |
|---|---|---|
| `course` | no | Folder name under `--dest`. Defaults to `Unsorted`. Sanitised for Windows. |
| `resources[].url` | yes | Any `mod/*/view.php?id=N` or a direct `pluginfile.php` URL. |
| `resources[].id` | no | Manifest identity. Defaults to the `id=` query value, else a URL hash. |
| `resources[].title` | no | Fallback filename only. It never overrides a name the server states. |

## Building one from `discover`

Pass the cookie in transiently — `--cookie-env` reads it out of an environment variable and
`--cookie-file -` reads it from a pipe, so neither form leaves a `cookies.txt` behind. With
no cookie flag at all the script falls back to `$MOODLE_SESSION_COOKIE`, which is the form
used below.

```bash
python3 scripts/moodle_fetch.py discover "https://moodle.example.com/course/view.php?id=123" --cookie-env MOODLE_SESSION_COOKIE > discovered.json

python3 - <<'PY'
import json
d = json.load(open("discovered.json"))
plan = [{"course": "Course name here", "resources": d["activities"]}]
json.dump(plan, open("plan.json", "w"), indent=2, ensure_ascii=False)
PY
```

The same thing, with the cookie piped in so it never sits in a variable either:

```bash
printf '%s' "$MOODLE_SESSION_COOKIE" \
  | python3 scripts/moodle_fetch.py discover "https://moodle.example.com/course/view.php?id=123" --cookie-file - > discovered.json
```

On Windows, use `python` (not `python3`) and PowerShell:

```powershell
python (Join-Path $hermes 'skills/research/course-material-ingestion/scripts/moodle_fetch.py') discover "https://moodle.example.com/course/view.php?id=123" --cookie-env MOODLE_SESSION_COOKIE > discovered.json
```

> **PowerShell:** `\` does not continue a line — it is passed through as a literal
> backslash. Use the backtick (`` ` ``), or keep the command on one line as above.

`discover` returns `modtype` per activity. Keep `resource`, `folder`, `page`, `url`, `book`,
and `file`; drop `assign`, `quiz`, `forum`, `feedback` — those are not files, and some of
them record a submission when opened.

## Collapsed sections and tile formats

`discover` sees only what the server renders. If `activity_count` looks low, fetch sections
one at a time (`--section 3`) or open the course with the browser and expand every tile
first, then re-run `discover` on the expanded page. The plan is complete when the number of
resources in it matches the number of download links visible in the browser.

## What `download` writes back: `manifest.json`

One flat list of resources; `verify` and `sync-links --manifest` read it.

```json
{
  "generated_at": "2026-10-11T14:31:02+00:00",
  "dest_root": "/home/nader/Courses",
  "resources": [
    {
      "id": "42",
      "course": "Comprehension and Oral Expression 1",
      "title": "References",
      "source_url": "https://moodle.example.com/mod/resource/view.php?id=42",
      "final_url": "https://moodle.example.com/pluginfile.php/1/mod_resource/content/0/References.pdf",
      "filename": "References.pdf",
      "path": "/home/nader/Courses/Comprehension and Oral Expression 1/References.pdf",
      "content_type": "application/pdf",
      "bytes": 61440,
      "sha256": "…",
      "status": "ok"
    }
  ]
}
```

`status` is one of:

| Status | Meaning | `verify` treats it as |
|---|---|---|
| `ok` | Downloaded and the bytes match the extension | pass |
| `suspect` | Downloaded, but the signature does not match the extension | pass with a warning |
| `truncated` | Fewer bytes arrived than `Content-Length` promised | fail |
| `html_error` | The server returned an HTML page; body moved aside as `<name>.bad` | fail |
| `too_large` | Skipped because of `--max-bytes` | fail |
| `error` | HTTP error or connection failure (`error` field has the reason) | fail |
| `session_expired` | The session died: a request came back as the login page, the run stopped, and this resource was not fetched | fail |

A run that stops because the session died also sets a top-level
`"stopped_reason": "session_expired"`, so a manifest that is short of resources is never
mistaken for a complete one. The `error` field says which resource proved the session was gone
(`redirected to the login page (...)`) and which were simply not attempted.

## Name collisions inside a course

Two resources can resolve to the same filename, for example two activities that both serve
`Notes.pdf`. `download` never overwrites one with the other. It decides by size first and
reads a file's bytes only when the sizes match:

| File already on disk under the name | What `download` does | Output |
|---|---|---|
| nothing | writes the file under its own name | none |
| same size, same SHA-256 | it is the same file: written over with identical bytes, one file on disk | none |
| same size, different bytes | keeps both: the download is saved as `Notes (2).pdf` (or the next free suffix) | a `WARN` line naming both files |
| different size | a different file: takes the next free suffix, no hashing | none |

Each resource keeps its own manifest entry, with its own `path` and `sha256`. A re-run does not pile
up copies: if the identical copy already sits under a suffix, it is reused. A collision warning does
not fail the run, but it means two activities in the plan share a name, so check that they really are
different files before relying on the names.

## Rename map for `sync-links`

When files were renamed outside `download`, hand `sync-links` a plain map. Keys are the
old wikilink targets, values are the new ones, both without the extension:

```json
{
  "Resource_1": "Grammar and Pronunciation",
  "Resource_2": "Script I",
  "U01 (2)": "U01 - Unit One"
}
```

`sync-links` also accepts `"previous_filename"` in a manifest entry, so a rename performed
by the agent can be recorded there and picked up on the next run.

## Session cookie for `download`

`download` needs the same session as `discover`, and takes it from the first source that
applies — an explicit flag always beats the ambient environment:

| Precedence | Flag | Where the value comes from |
|---|---|---|
| 1 | `--cookie 'MoodleSession=…'` | the command line (visible in history and `ps`) |
| 2 | `--cookie-file PATH` | a Cookie header or Netscape `cookies.txt` |
| 3 | `--cookie-file -` | stdin — nothing is written to disk |
| 4 | `--cookie-env VAR` | `$VAR` / `%VAR%` — the name is echoed, never the value |
| 5 | *(nothing given)* | `$MOODLE_SESSION_COOKIE`, if set |

```bash
# transient: cookie lives in the environment of this one command only
MOODLE_SESSION_COOKIE="MoodleSession=…" python3 scripts/moodle_fetch.py download plan.json --dest "~/Courses" --cookie-env MOODLE_SESSION_COOKIE
```

The value never appears in `manifest.json`, in stdout, or in any error message — a malformed
cookie file is reported by line number and field count, never by quoting the row.

## Re-running

`download --update` reuses the existing `manifest.json` and skips any id whose file is
already on disk with the same size. Add newly discovered ids to the plan and re-run to pick
up only what the lecturer added:

```bash
python3 scripts/moodle_fetch.py download plan.json --dest "~/Courses" --update --cookie-env MOODLE_SESSION_COOKIE
```

This is also how a run that hit an expired session is finished. When `download` stops on a
login redirect it keeps every file it already has, writes the manifest with the rest marked
`session_expired`, and tells you to re-authenticate. Take a fresh cookie, run the same command
again with `--update` — the finished files are skipped and it picks up where it stopped. Expect
`verify` to keep failing until no `session_expired` entry is left.
