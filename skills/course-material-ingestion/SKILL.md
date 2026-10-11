---
name: course-material-ingestion
description: Download Moodle course files and keep notes in sync.
version: 1.0.0
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
- The session cookie, passed to the script as `--cookie 'MoodleSession=...'` or via a
  `--cookie-file` containing either the raw `Cookie:` header value or a Netscape
  `cookies.txt`. Treat it as a credential: never print it, log it, commit it, or paste it
  into chat, notes, or the manifest.
- `scripts/moodle_fetch.py` is stdlib-only Python 3.8+. No third-party packages.

## How to Run

```bash
S=~/.hermes/skills/research/course-material-ingestion/scripts/moodle_fetch.py

# 1. What does this URL actually serve?
python "$S" resolve "https://moodle.example.com/mod/resource/view.php?id=1234" \
    --cookie-file cookies.txt

# 2. Download a whole course from a plan file (see references/plan-format.md)
python "$S" download plan.json --dest "~/Courses" --cookie-file cookies.txt

# 3. Prove the files on disk are real and match the manifest
python "$S" verify --manifest "~/Courses/manifest.json" --root "~/Courses"

# 4. Rewrite wikilinks in the notes to the names on disk
python "$S" sync-links "~/Obsidian/Vault/Semester 1" --manifest "~/Courses/manifest.json" \
    --dry-run
```

Every command exits non-zero when it finds a problem, so a pipeline cannot mistake "finished"
for "correct". Drop `--dry-run` from `sync-links` only after reading the diff.

## Quick Reference

| Action | Command |
|---|---|
| Resolve a URL to its final file, name, type, size | `resolve <url> [--cookie-file f]` |
| Download a plan and write `manifest.json` | `download plan.json --dest DIR [--cookie-file f]` |
| Re-download only what is missing or changed | `download plan.json --dest DIR --update` |
| Validate files against a manifest | `verify --manifest m.json --root DIR` |
| List URLs found on a course page | `discover <course-url> [--cookie-file f]` |
| Rewrite wikilinks from a rename map | `sync-links NOTES_DIR --map map.json [--dry-run]` |
| Rewrite wikilinks from a manifest | `sync-links NOTES_DIR --manifest m.json [--dry-run]` |

## Procedure

① **Establish the session, do not rebuild it.** Ask the user to open Moodle in their browser
and log in. Read the session cookie from that authenticated session — in Hermes, browse to
the site with `browser_navigate` and take the cookie from the browser session; if the
environment cannot expose it, ask the user to copy it from DevTools → Application → Cookies.
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
