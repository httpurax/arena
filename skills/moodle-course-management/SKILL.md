---
name: moodle-course-management
description: Manage Moodle course content and local file organization.
version: 1.0.0
author: Jinx
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [moodle, courses, obsidian, files, scraping]
    category: productivity
    related_skills: [obsidian]
---

# Moodle Course Management

## Credential Handling

**Vault reference placeholder:** `<MOODLE_VAULT_CREDENTIAL — configured in the user's Hermes vault; never stored in this repository>`.

Use the user's configured Moodle vault credential only at runtime. Its real value belongs in the
user-level Hermes vault or credential store, outside this repository. Never copy it into this
skill, a command line, `manifest.json`, course notes, logs, or any committed file.

## When to Use
- Managing, auditing, or crawling Moodle portal materials.
- Deduplicating and sorting educational files into an organized local vault.
- Maintaining index notes and wikilinks for downloaded coursework.

## Workflow

### 1. Audit & Extraction
- **Always use `manifest.json` as the truth:** When auditing for missing files, compare against a `manifest.json` which tracks the expected ID-based resources for each course, rather than relying on filesystem existence alone.
- **Handle Moodle format-tiles by navigating sections, not clicking tiles:** A course whose `document.body.className` contains `format-tiles` hides its activities behind tiles, so a page-level link scan sees almost nothing and returns a false "nothing new". Collect the section URLs instead, then visit each one:
  - course-index links matching `a[href*="/course/section.php?id="]`
  - each tile's `dataset.trueSectionid` → `/s1/course/section.php?id=<id>`

  Clicking `.tile` elements alone leaves section content unrendered.
- **Scraping resources:** On each section page, scan for `mod/resource/view.php`, `mod/url`, `mod/page`, `mod/forum`, `pluginfile.php`, and direct media links (`opus`, `mp3`, `mp4`). Treat `mod/url` as an external redirect — open it to resolve the real destination before deciding there is a file to fetch.
- **Download during the audit, do not stop at a report:** when the vault is the destination, fetch new files in the same run and update the notes before reporting. An audit that ends at "found 4 new items" leaves the fetch to the user.
- **Validate every download before filing it:** magic bytes (`%PDF`, `PK\x03\04` for OOXML, `ftyp` at offset 4 for mp4), byte size, and an HTML sniff. A small body starting `<!DOCTYP` is a login or error page saved under a document extension — delete it and report the failure.
- **Append newly downloaded resources to `manifest.json`** before finishing, so the next run treats them as baseline instead of re-downloading them.
- **YouTube videos:** Use the `youtube-content` skill for transcripts and derived formats. To capture the video file itself, see [references/youtube-videos.md](references/youtube-videos.md).

### 2. Organizing & Cleaning
- **Deduplication:** When moving loose files from `Downloads`, always deduplicate `(N)`-numbered copies **by hash** (`hashlib.sha256`), not by filename alone. Two files with different names may contain identical content.
- **Label Validation:** Never trust generic labels like "File.docx" or "Script.docx". Always inspect file content (e.g., read `word/document.xml` in `.docx` files) to determine the true topic before sorting.

### 3. Recurring checks (cron)

When the audit runs on a schedule instead of on demand, the job's dependencies must be verified before
its first browser action, and its output must be checked against disk before it is believed.

- **Prove the automation browser is alive before blaming the page.** A browser-driven cron job that
  reports "cannot find the login button" almost always means the dedicated Chrome on the debug port
  died — not that the portal changed. Check the port first:

  ```
  curl -s --max-time 5 http://127.0.0.1:9222/json/version
  ```

  If the response has no `Browser` key, relaunch in the background and re-check once:

  ```
  terminal(command='"/c/Program Files/Google/Chrome/Application/chrome.exe" --remote-debugging-port=9222
    --user-data-dir="<dedicated dir>" --no-first-run --no-default-browser-check', background=true)
  ```

  Report the browser as the blocker; never report a missing page element without that proof.
- **Give the job the toolsets it needs to finish.** A vault-upkeep job needs `browser`, `terminal`,
  and `file`. With only `browser` it can discover new files but cannot download them or update notes.
- **A truncated report means unfinished work.** When a cron run's response is a dangling sentence,
  do not trust its summary. Check disk state — mtimes, manifest entry count, note contents — and
  finish the edits it skipped before telling the user anything.

### 4. Maintenance & Integrity
- **Index Sync:** After sorting files, verify the index note (e.g., `UFC Semester 1.md`) counts vs. actual file count on disk.
- **Link Integrity:** Use regular expressions to verify `[[wikilinks]]` in course notes against files on disk. Fix broken or stale links immediately after moving files.

## Pitfalls
- **Collapsible Content:** Scraping a `format-tiles` course by clicking tiles returns almost no activities, so "nothing new" is a false negative. Navigate every `/course/section.php?id=` URL instead.
- **Report-only audits:** A recurring check that lists new files without downloading them makes the user run the fetch by hand. When the job's purpose is vault upkeep, give it write toolsets (`file`, `terminal`) alongside `browser` and download in the same run.
- **Label Reliance:** Relying on generic download labels ("File", "U01") causes misclassification; always verify content against existing course notes before sorting.
- **Silent Duplication:** Moving files without hashing leads to a bloated vault with byte-identical documents.
- **Blaming the portal for a dead browser.** A scheduled browser job that finds no login form is usually
  reporting its own missing dependency. Probe the debug port before concluding the page changed.
- **Believing a cron run's summary over disk state.** A truncated or fragmentary response is a
  half-finished task. Verify manifest counts and note contents, then complete the skipped steps.
- **Re-baselining from a fragment.** If a run's report is unusable, rebuild the manifest by comparing
  every on-disk file against the course's discovered activity URLs, then store that count in the job
  prompt so the next run diffs against truth instead of repeating a stale number.
