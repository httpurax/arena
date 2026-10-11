---
name: course-material-ingestion
description: Download Moodle course files and keep notes in sync.
version: 1.1.0
author: Nader Amine (httpurax), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Moodle, Obsidian, Downloads, Notes, Courses, PDF]
    category: research
    related_skills: [obsidian, pdf, docx, note-taking]
---

# Course Material Ingestion Skill

Pull every file out of a Moodle (or Moodle-like) course onto disk — PDFs, Word docs,
PowerPoints, audio — one folder per course, under the file's **real name**, and keep
Obsidian notes' `[[wikilinks]]` pointing at those exact names.

It is deliberately paranoid about two failure modes that look like success: a download that
silently saves a login page as `Resource_3.pdf`, and notes that link to files that do not
exist. It does not log in for you, does not store credentials, and does not touch grading or
submission endpoints.

## When to Use

- A user asks to "download my course", "grab the Moodle files", "organise this semester".
- Notes already exist but their `[[wikilinks]]` are placeholders (`Resource_1`, `File.docx`)
  or point at files that were never actually downloaded.
- Files are on disk but named by URL id, `view.php`, or a mangled redirect slug.
- Re-syncing a course after the lecturer added material: only new ids get fetched.

Skip it for a single file the user just wants to read once — `browser_navigate` to the file
and let the browser handle the download.

## Prerequisites

- An authenticated Moodle session in the user's browser. Never ask for the password; ask the
  user to log in themselves, then read the `MoodleSession` cookie out of that session.
- The session cookie, handed to the script through one of these sources — **highest
  precedence first**, and an explicit flag always beats the ambient environment:

  | Source | How it is supplied | Notes |
  |---|---|---|
  | `--cookie 'MoodleSession=…'` | the value on the command line | visible in shell history and in `ps`; last resort |
  | `--cookie-file PATH` | a file holding a `Cookie:` header or a Netscape `cookies.txt` | prefer `-` over a real file |
  | `--cookie-file -` | the cookie piped in on stdin | nothing is ever written to disk |
  | `--cookie-env VAR` | read out of `$VAR` / `%VAR%` | **the default choice**; the variable name is echoed, its value never is |
  | *(no flag given)* | `$MOODLE_SESSION_COOKIE`, if it happens to be set | ambient pickup — the script says so on stderr, without the value |

  Treat it as a credential: never print it, log it, commit it, or paste it into chat, notes,
  or the manifest. The script puts it on the wire and nowhere else — it never echoes the
  value, never writes it into `manifest.json`, and its error messages describe a malformed
  cookie line by number rather than quoting it.
- `scripts/moodle_fetch.py` is stdlib-only Python 3.8+. No third-party packages.
- An interpreter on `PATH`: `python3` on Linux and macOS, `python` or `py -3` on Windows
  (Windows has no `python3` unless the Store alias is installed).

### Getting the session cookie without copy-paste

`MoodleSession` is set `HttpOnly`, so **the page cannot hand it to you**: `document.cookie`
in a devtools console returns blank for it, and a `Cookie:` header copy-pasted out of the
Network tab goes stale the moment the session rotates. Read it from the browser's own cookie
store instead:

1. Ask the user to log into Moodle in their browser, then `browser_navigate` to the course
   page so the session is live. If the page bounces to `/login/index.php`, the login did not
   take — fix that first.
2. Read the cookie off the **browser's cookie surface**, not the page: over CDP that is
   `Storage.getCookies` / `Network.getCookies`, which return `HttpOnly` cookies because they
   come from the browser's store rather than from the page's JS. Use whatever cookie API
   your browser tool exposes; a JS evaluation in the page is the one thing that cannot work.
3. Keep it transient. Put the value into an environment variable for the one command that
   needs it and let it die with the shell:

   ```bash
   export MOODLE_SESSION_COOKIE="MoodleSession=<value from the cookie surface>"
   python3 "$S" download plan.json --dest "$HOME/Courses"
   unset MOODLE_SESSION_COOKIE
   ```

   ```powershell
   $env:MOODLE_SESSION_COOKIE = "MoodleSession=<value from the cookie surface>"
   python $S download plan.json --dest "~/Courses"
   Remove-Item Env:MOODLE_SESSION_COOKIE
   ```

   Or skip the variable entirely and pipe it — `… | python "$S" download plan.json
   --dest "~/Courses" --cookie-file -` — so it never lands on disk or in history. Do not
   write `cookies.txt` unless the user explicitly asks for a reusable file; it is gitignored
   here for a reason.

**If the browser cannot expose cookies** — the tool has no cookie surface, or the session
lives in a profile it cannot see — do not fall back to asking the user to dig the value out
of DevTools by hand. Navigate the browser straight at the file URL and let the browser
download it with its own session: `browser_navigate` to the `mod/resource/view.php?id=N`
link (or the `pluginfile.php` URL) and let the browser's download handling save the file.
Then run `verify` / `sync-links` against whatever landed in the downloads folder. `download`
is for when the browser route is not available, not a prerequisite for it.

## How to Run

Resolve the script once, then use it. Hermes does not always live in the user's profile, so
find the skill directory in this order:

1. `$HERMES_HOME/skills/<category>/<skill-name>/` when `HERMES_HOME` is set — this wins
   everywhere, including Windows, where it is normally `%LOCALAPPDATA%\hermes`.
2. `~/.hermes/skills/...` on Linux and macOS.
3. `%LOCALAPPDATA%\hermes\skills\...` on Windows when `HERMES_HOME` is not set.

**bash / zsh / Git Bash / WSL**

```bash
S="${HERMES_HOME:-$HOME/.hermes}/skills/research/course-material-ingestion/scripts/moodle_fetch.py"

# 1. What does this URL actually serve?
python3 "$S" resolve "https://moodle.example.com/mod/resource/view.php?id=1234" --cookie-env MOODLE_SESSION_COOKIE

# 2. Download a whole course from a plan file (see references/plan-format.md)
python3 "$S" download plan.json --dest "~/Courses" --cookie-env MOODLE_SESSION_COOKIE

# 3. Prove the files on disk are real and match the manifest
python3 "$S" verify --manifest "~/Courses/manifest.json" --root "~/Courses"

# 4. Rewrite wikilinks in the notes to the names on disk
python3 "$S" sync-links "~/Obsidian/Vault/Semester 1" --manifest "~/Courses/manifest.json" --dry-run
```

**PowerShell (5.1 and 7+, Windows)**

```powershell
$hermes = if ($env:HERMES_HOME) { $env:HERMES_HOME } elseif ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'hermes' } else { Join-Path $HOME '.hermes' }
$S = Join-Path $hermes 'skills/research/course-material-ingestion/scripts/moodle_fetch.py'

# 1. What does this URL actually serve?
python $S resolve "https://moodle.example.com/mod/resource/view.php?id=1234" --cookie-env MOODLE_SESSION_COOKIE

# 2. Download a whole course from a plan file (see references/plan-format.md)
python $S download plan.json --dest "~/Courses" --cookie-env MOODLE_SESSION_COOKIE

# 3. Prove the files on disk are real and match the manifest
python $S verify --manifest "~/Courses/manifest.json" --root "~/Courses"

# 4. Rewrite wikilinks in the notes to the names on disk
python $S sync-links "~/Obsidian/Vault/Semester 1" --manifest "~/Courses/manifest.json" --dry-run
```

Three things differ between the two shells, and each one has bitten someone:

- **`\` is not a line continuation in PowerShell.** bash swallows a trailing backslash and
  joins the lines; PowerShell passes it through as a literal character, so a wrapped bash
  command either errors or silently sends a `\` as an argument. Use the backtick
  (`` ` ``) — PowerShell's escape *and* continuation character — or write each command on
  one line, as above. Backtick-line-continuation also fails silently if a space follows it.
- **`python3` usually does not exist on Windows.** Use `python`, or `py -3`.
- **`--dest "~/Courses"` is fine on Windows.** The script runs every path argument through
  `Path.expanduser()`, which resolves `~` to `%USERPROFILE%` on Windows and `$HOME`
  elsewhere — so the quoted form works on both, and you never rely on the shell to expand
  it (bash will not expand a quoted `~`, and PowerShell will not expand a quoted one for a
  native command either). Forward slashes are accepted; the script sanitises filenames for
  Windows on its own.

Every command exits non-zero when it finds a problem, so a pipeline cannot mistake "finished"
for "correct". Drop `--dry-run` from `sync-links` only after reading the diff.

## Quick Reference

| Action | Command |
|---|---|
| Resolve a URL to its final file, name, type, size | `resolve <url> [cookie flags]` |
| Download a plan and write `manifest.json` | `download plan.json --dest DIR [cookie flags]` |
| Re-download only what is missing or changed | `download plan.json --dest DIR --update [cookie flags]` |
| Validate files against a manifest | `verify --manifest m.json --root DIR` |
| List URLs found on a course page | `discover <course-url> [cookie flags]` |
| Rewrite wikilinks from a rename map | `sync-links NOTES_DIR --map map.json [--dry-run]` |
| Rewrite wikilinks from a manifest | `sync-links NOTES_DIR --manifest m.json [--dry-run]` |

`[cookie flags]` is any one of `--cookie-env VAR`, `--cookie-file PATH`, `--cookie-file -`
(stdin), or `--cookie 'MoodleSession=…'`; with none of them the script falls back to
`$MOODLE_SESSION_COOKIE` if it is set. `verify` and `sync-links` accept the same flags for
symmetry but never read a cookie — they work entirely off the manifest and the notes.

## Procedure

① **Establish the session, do not rebuild it.** Ask the user to open Moodle in their browser
and log in. `browser_navigate` to the course page, then read `MoodleSession` off the
browser's own cookie surface (CDP `Storage.getCookies` / `Network.getCookies`) — not from
`document.cookie`, which is empty for an `HttpOnly` cookie. Keep the value transient: export
it into `MOODLE_SESSION_COOKIE` for the one run that needs it, or pipe it in with
`--cookie-file -`, and never echo it into chat or the transcript. If the browser cannot
expose cookies at all, `browser_navigate` straight at each file URL and let the browser
download with its own session; do not ask the user to hand-copy a value out of DevTools.
Cookies expire: re-extract instead of reusing a stored one.

② **Enumerate resources, one section at a time.** Collapsed sections and tile-based course
formats hide activities from a naive scrape of `course/view.php?id=N`. Expand everything if
the page offers an "Expand all" control; otherwise fetch each section explicitly with
`course/view.php?id=N&section=M`, or open each tile with `browser_navigate`. Confirm counts
(`SECTION 3 — 7 activities`) against the rendered page before moving on; a missing tile is a
silent 20% loss.

③ **Resolve before you download.** Every `mod/resource/view.php?id=N` is a landing page, not
a file. `resolve` follows the redirect chain and reads `Content-Disposition`, so the real name
comes from `pluginfile.php/.../References.pdf`, never from link text like `Resource_1`.
Repeated identical results across different ids — four different `id`s all resolving to
`U01 (2).pdf` — mean you are reading a cached redirect target; re-check with a fresh request
before trusting it.

④ **Download and validate in the same breath.** `download` streams each file to a temporary
name, then checks it before renaming it into place: extension-specific magic bytes (`%PDF`,
`PK\x03\x04` for OOXML, `OggS`, `ID3`), declared `Content-Length` vs bytes written, and an
HTML sniff. A file that is really a login page or an error page is recorded as `html_error`
in the manifest and moved aside with a `.bad` suffix — never silently kept.

⑤ **Organise one folder per course.** Folder names come from the course title on the course
page; filenames are sanitised for Windows (`<>:"/\|?*` stripped, trailing dots/spaces
trimmed, 150-char cap preserving the extension) but otherwise left exactly as Moodle serves
them, including accents, parentheses, and Arabic/French characters. Collisions inside a course
get ` (2)`, ` (3)` suffixes.

⑥ **Keep a manifest.** `manifest.json` at the destination root records, per resource:
`course`, `id`, `source_url`, `final_url`, `title`, `filename`, `path`, `bytes`, `sha256`,
`status`. It is the single source of truth for step ⑦ and makes re-runs idempotent — `--update`
skips any id whose sha256 still matches.

⑦ **Reconcile the notes.** After renaming or downloading, note files still point at the old
placeholders. `sync-links` rewrites `[[Resource_3]]`, `[[Resource_3|alias]]`, and
`[[Resource_3#Heading]]` to the real stem from the manifest, preserving any alias and anchor.
Add `--map` when the rename happened outside the manifest. Always preview with `--dry-run`
first and report the diff.

⑧ **Verify, then report.** Run `verify`. Report per-course counts (files on disk, total size)
and name the failures explicitly — an honest "41 of 49, 8 are error pages" beats a green
summary built on HTML saved as `.pdf`.

## Pitfalls

- **HTML saved as a document.** A login redirect returns HTTP 200 with `text/html`. Any file
  whose first bytes are `<!DOCTYPE html` or `<html` and whose extension is not `.html` is a
  failure, not a download.
- **Placeholder names.** Moodle's DOM rarely exposes the activity title as link text. Trust
  the redirect target and `Content-Disposition`; use the activity title only as a fallback
  and label it as such in the manifest.
- **Tile and collapsed formats.** Guessing `section=` numbers on a tile-format course
  duplicates or skips material. Derive section ids from the rendered course page.
- **One `view.php` per resource.** A `pluginfile.php` URL copied straight from the browser is
  already final — `resolve` must be a no-op on it, not a second redirect dance.
- **Audio and video are large.** `.opus`, `.mp3`, `.m4a` on a course page is normal; warn on
  and respect a size cap, and never let one 3.8 GB lecture disk-fill the vault.
- **Never re-run a submission or feedback URL.** Only `resource`, `folder`, `page`, `url`,
  `book`, and `file` module types are ingestion targets.
- **`document.cookie` is empty — that is not a failure of your extraction.** `MoodleSession`
  is `HttpOnly` by design, so the page's JS cannot see it. A JS evaluation returning nothing
  means you used the wrong surface; go back to the browser's cookie store.
- **A `#HttpOnly_` row in `cookies.txt` is data, not a comment.** curl comments HttpOnly
  cookies out that way, so the one row the skill needs looks skipped. The script parses
  those rows; a hand-rolled `grep -v '^#'` would silently drop them.
- **A wrapped bash command on Windows is not the same command.** `\` at end-of-line is bash
  syntax; PowerShell needs a backtick. When a Windows user reports a strange argument or
  "unrecognized arguments", look for a stray `\` before rewriting anything else.
- **An ambient cookie can surprise you.** If `MOODLE_SESSION_COOKIE` is set, the script uses
  it when no flag is given and says so on stderr. That is a convenience, not a substitute
  for a fresh session: an expired ambient cookie produces the same login-redirect failures
  as none at all, just less obviously.

## Verification

A run is done only when all of these hold, and `verify` proves it:

1. Every manifest entry with `status: ok` exists on disk, has `bytes > 0`, and its sha256
   matches the recorded value.
2. No file on disk in a course folder is detected as HTML while claiming a non-HTML extension.
3. The number of `ok` entries per course equals the number of download links found on that
   course page in step ② (minus clearly non-file activities: quizzes, forums, assignments).
4. `sync-links --dry-run` reports zero unresolved wikilinks pointing at a `Resource_N`,
   `view.php`, or `File.docx` placeholder, and no `[[...]]` target in the notes is missing
   from disk.
5. The report names every failure; a partial success is reported as partial.
