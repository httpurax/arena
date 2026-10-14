---
name: atm10-quest-companion
description: Guide for All the Mods 10 progression and quests.
version: 1.1.1
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: gaming
---

# ATM10 Quest Companion

A progression companion for **All the Mods 10** (ATM10), the ~500-mod kitchen-sink pack
for Minecraft 1.21.1 (NeoForge) whose FTB Quests book holds 66 chapters and roughly
4,790 quests. The skill knows the pack's main stages — early game → tech → magic →
endgame (the ATM Star) — tells the player what to do next from wherever he is, and keeps
a local record of which chapters are finished.

## When to Use

- The user says where he is in ATM10 (a quest chapter, a base he has built, a boss or
  resource he is stuck on) and asks *what should I do next?*
- The user finishes a quest chapter and wants it recorded ("mark Mekanism done").
- The user asks what a stage of the pack involves, which mod to commit to (tech line,
  magic line, storage network), what the ATM Star endgame needs at a high level, or what
  comes *after* the star (Chapter 4: Creative, star automation, creative-tier items).
- The user asks for a progress report: overall completion, per-stage completion, or the
  next unfinished chapters in quest-book order.

## When Not to Use

- The user plays a different pack (ATM9, ATM10: To the Sky, another kitchen sink) — the
  chapter list here is ATM10's; say so and fall back to general advice.
- The user wants exact quest requirements, item ids, or recipes recited — this skill must
  not invent them (see Research Grounding below); point at the quest book and JEI.
- The user wants game-installation troubleshooting beyond the setup notes in
  `references/getting-started.md`.

## Research Grounding (read before advising)

The references in this skill were built from real sources: the pack's own quest config in
the official `AllTheMods/ATM-10` GitHub repository (chapter groups, order, and quest
titles), the published ATM10 mod list, and community guides. They capture the pack's
**structure** — which chapters exist, in what order, and roughly when players reach them.

They do **not** capture exact requirements, and this skill must never pretend otherwise:

- **The in-game quest book (FTB Quests) and JEI are authoritative** for what a quest
  needs, what a recipe contains, and what an item does. Always defer to them, and say so
  when the user asks for specifics.
- **Never invent quest requirements, item ids, counts, or recipes.** If a detail is not
  in the references and not stated by the user, say "check the quest entry / JEI" — do
  not fill the gap from memory or plausibility.
- **Uncertain details are flagged in the docs as approximate** (ore levels, tier names,
  mod availability, version-sensitive mechanics). When repeating such a detail, keep the
  hedge: "guides say roughly X — verify in-game".
- ATM10 updates often; the chapter list here matches pack 8.x. If the user's book shows
  chapters this skill does not know, trust his book and note the mismatch — then refresh
  the list with the pack-update workflow below.
- **The four endgame docs date themselves.** `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`, and
  `references/armor-tools-ladder.md` were read from the
  pack repository's `config/ftbquests/quests/chapters/*.snbt` and
  `lang/en_us/chapters/*.snbt` (mod names and versions from
  `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"` stamp in
  `examples/progress.example.json`; the creative checklist pins the exact commit
  (`e5e3d1d83e`). The item ids, quest titles, and quoted counts there are that snapshot's;
  the pack changes them between versions. Quote them as *what the book asked for in 8.2*,
  and still defer to the in-game quest book and JEI.

## Setup — first run only

Real progress lives in `data/progress.json`, which is **never committed**: the skill
ships a `.gitignore` that excludes `data/`. Create the private file by copying the
shipped example (all 66 chapters, quest-book order, every status `pending`):

```bash
mkdir -p data && cp examples/progress.example.json data/progress.json
```

```powershell
New-Item -ItemType Directory -Force data | Out-Null
Copy-Item examples/progress.example.json data/progress.json
```

Alternatively, `python3 scripts/progress.py --sync --yes` (or `python` on Windows) can
initialize a missing progress file after displaying its full preview; without `--yes`, it
never creates or changes a file.

Run these from the skill directory (`<skills root>/gaming/atm10-quest-companion/`).
`progress.py` is stdlib-only Python 3.8+, needs no third-party packages and no network;
the interpreter is `python3` on Linux and macOS, `python` (or `py -3`) on Windows.

## Progress file

One JSON document — `{"chapters": [...]}` plus the two optional stamp fields below — with
one object per quest-book chapter, stored in quest-book order (standalone chapters first,
then the book's groups in order):

| Field | Required | Notes |
|---|---|---|
| `id` | yes | The chapter's config filename, unique, e.g. `mekanism`. |
| `title` | yes | Human title as the book shows it, e.g. `Mekanism`. |
| `group` | no | Quest-book group (`Main Questline`, `Tech`, ...); empty for standalone chapters. |
| `stage` | yes | One of `early-game`, `tech`, `magic`, `endgame` — the four progression stages. |
| `status` | yes | `pending` or `done`. Nothing else. |

Chapters come from `examples/progress.example.json`; do not add, drop, or rename chapters
in the real file unless the user's in-game book genuinely differs (pack update), and say
so when editing.

Next to `chapters` the document may carry two optional stamp fields:

| Field | Required | Notes |
|---|---|---|
| `pack_version` | no | The ATM10 version the chapter list was researched from, e.g. `"8.x"`. |
| `pack_version_source` | no | Where that list was read from, and when. |

Both must be non-empty strings when present; any other top-level key is rejected. The
example file ships both, and `progress.py` uses them for the drift check below.

## Behaviors

### 1. Locate the player

Ask (or take from what he said): which Main Questline chapter he is on, which big mods
are built and running, and what he is stuck on. Map that to a stage in
`references/progression.md`:

- just spawned / iron-and-diamond phase → **early-game**
- machines, power, storage network, resource farms → **tech**
- spells, rituals, enchanting overhaul → **magic**
- allthemodium/vibranium/unobtainium, dimensions and bosses, ATM Star components →
  **endgame**

Stages overlap by design; use them to orient, not to gate.

### 2. Tell him the next meaningful steps, in order

- Work from `references/progression.md` (stages, quest-book order) and
  `references/key-mods.md` (what each mod does, when to start it, what it leads to).
  First-hour and setup questions go to `references/getting-started.md`.
- Give the next steps **in quest-book order** within the relevant chapters — a short,
  ordered list ("1. finish the X chapter up to Y; 2. start Z; 3. ..."), not a lecture.
- For each step, name the chapter/mod it belongs to and *why* it is next (what it
  unlocks), grounded in the references.
- For any concrete requirement (item counts, ingredients, ore levels, boss mechanics),
  point at the quest entry and JEI instead of stating numbers — per Research Grounding
  above. Flag anything version-sensitive as approximate.
- **Endgame questions go to the three endgame docs.** "What does the ATM Star need?" →
  `references/atm-star-checklist.md`: Chapter 3's components grouped by source mod, with
  the verified quest titles and item ids, the build order, and the parts the pack marks
  optional. "Which boss, where, and when?" → `references/boss-checklist.md`: boss →
  dimension → arena → roughly when, from verified kill, structure, and dimension tasks.
  "I have the star — now what?" ("what is Chapter 4: Creative?", "how do I automate the
  star?", "what does the Creative Jetpack do?") → `references/creative-checklist.md`:
  Chapter 4's 38 quests in dependency order — the four automation multiblocks, the bees
  and Star Shards, the five prisms and star parts, the dusts and the lens chain, the
  terminal *Fully Automated ATM Star* quest, and the eleven creative-tier items it gates.
  Quote them as what the book asks for, keep their hedges, and still send the player to
  the in-game quest book and JEI for current counts and drops.
- When the choice is between alternatives (AE2 vs Refined Storage, Mekanism vs Create vs
  Modern Industrialization), present them as alternatives with their trade-offs and let
  the user pick; never invent a "required" path — the pack itself says quests are
  optional and mods are not gated.

### 3. Record completion and report progress

When the user says a chapter (or several) is done — or wants one reopened — record it with
`--set`:

```bash
python3 scripts/progress.py --set mekanism done --set "Chapter 2: Allthemodium" done
```

```powershell
python scripts/progress.py --set mekanism done --set "Chapter 2: Allthemodium" done
```

`--set` takes a chapter `id` (`mekanism`) or its exact `title` (`Mekanism`; case and
surrounding spaces ignored) plus `done` or `pending` — `pending` reopens a finished
chapter. Repeat the flag for several chapters; they are all applied in one atomic write.
Every request is validated **before** anything is written, so an unknown id, a near-miss
title, or a bad status exits 1 with one message that names the closest known ids and
points at `examples/progress.example.json` — and the file is left untouched. A change that
would alter nothing is reported as `already done` and the file is not rewritten. The script
never raises a traceback, and it refuses to overwrite the file with a document that fails
the schema.

Change only what the user reported; never mark chapters done on his behalf "because he
probably has".

The report itself — a `--set` run prints its change lines, then exactly this:

```bash
python3 scripts/progress.py
```

```powershell
python scripts/progress.py
```

```
atm10 quest companion - chapter progress
data: <skill>/data/progress.json
pack: 8.x  (known chapter list: pack 8.x, 66 chapters)

overall: 16/66 chapters done (24.2%)

per stage (progression order)
  early-game  Early Game             16/16  done (100.0%)
  tech        Tech & Automation       0/27  done (  0.0%)
  magic       Magic                   0/10  done (  0.0%)
  endgame     Endgame & Exploration   0/13  done (  0.0%)

next unfinished chapters (quest-book order, showing 3 of 50)
    1. [endgame] Chapter 2: Allthemodium (allthemodium, group: Main Questline)
    2. [endgame] Chapter 3: The ATM Star (chapter_2_the_star, group: Main Questline)
    3. [endgame] Chapter 4: Creative (achapter_2r_6the_atm_star, group: Main Questline)

the in-game quest book (FTB Quests) and JEI are authoritative for what each chapter
actually requires; this list only tracks completion.
```

*(Illustrative output, shortened with `--next 3`; a real report reflects the user's own
file. Note the list is quest-book order, not advice order — the Main Questline spine
outranks the mod chapters in the book, so pair it with the stage guidance from
`references/progression.md` when recommending what to play next.)*

The script prints overall completion, per-stage percentages, and the next unfinished
chapters in quest-book order. Options:

| Option | Effect |
|---|---|
| `--data PATH` | Use another progress file (default `data/progress.json`). |
| `--next N` | Cap the next-chapters list (default 10). |
| `--stage STAGE` | List only that stage's unfinished chapters: `early-game`, `tech`, `magic`, `endgame`. Counts and percentages stay whole-file — the stage table shows every stage and marks the filtered row with `<==`. A stage with nothing left says so. |
| `--set CHAPTER STATUS` | Record `CHAPTER` (id or exact title) as `done` or `pending`, then report. Repeatable; validates every request before writing. |
| `--list` | Print every known chapter as `id - title`, grouped under stage headings in progression order. Does not read the progress file. |
| `--json` | Print the full report as JSON with two-space indentation. It includes `pack_version` (the file's stamp, or `null`), `known_pack_version`, `known_chapter_count`, `overall` (`done`, `total`, `percent`), `per_stage`, `next_chapters`, `pending_chapter_count`, and `pack_drift`. It honors `--next` and `--stage`; combining it with `--set` keeps stdout valid JSON and adds structured `set_changes`. |
| `--sync` | Preview unknown ids to drop, known ids to add as `pending`, pack-version changes, and any chapter-order correction. A missing file is previewed as all known chapters missing. Exits 0 without writing. |
| `--yes` | Apply the preview only when used with `--sync`. Drops unknown ids, adds missing chapters as `pending`, restores quest-book order, and sets `pack_version` to the known version. Preserves existing statuses and optional `pack_version_source`. Writes only if something changes. |

```bash
python3 scripts/progress.py --stage endgame --next 5
python3 scripts/progress.py --list
python3 scripts/progress.py --json --next 5
python3 scripts/progress.py --sync                 # preview only
python3 scripts/progress.py --sync --yes           # apply after reviewing the preview
```

```powershell
python scripts/progress.py --stage endgame --next 5
python scripts/progress.py --list
python scripts/progress.py --json --next 5
python scripts/progress.py --sync                 # preview only
python scripts/progress.py --sync --yes           # apply after reviewing the preview
```

`--list`, `--json`, and `--sync` are separate output modes. `--yes` is valid only with
`--sync`; `--sync` cannot be combined with `--set` or `--stage`. An invalid stage or status
exits 1 with the valid values named. The script never raises a traceback: a missing, empty,
malformed, or schema-breaking progress file is reported as one clear message with exit
status 1 — relay that message and the fix it suggests, do not paper over it. Bad CLI syntax
uses argparse's clear usage error rather than a traceback.

Use the report to answer "what next?" too: the first listed pending chapter in the
player's current stage is the natural recommendation, cross-checked against what he told
you he has already built (the file may lag reality — update it first).

### Pack drift: a warning, never an error

Every report compares the file with the shipped chapter list for pack 8.x. If the file
carries chapter ids the pack does not have, is missing ids it should have, or was stamped
with a different — or no — `pack_version`, the report prints a `pack drift` block listing
the ids (at most six per line, then `(+N more)`) and **still exits 0**, counting every
chapter as usual. A pack update is information, not a broken file.

Relay the warning when it appears and say that the user's in-game quest book is
authoritative. Never silently reconcile the file: `--sync` first prints every id and
version change it would make, and `--sync --yes` is used only after the player explicitly
approves that preview. The dry run does not write anything.

### Pack updates: rebuilding the chapter list

When the pack moves on, rebuild `examples/progress.example.json` from the new pack
config instead of hand-editing it. `scripts/build_chapter_list.py` is the offline tool
for this — stdlib-only Python 3.8+, no network ever: it reads a local checkout the user
provides and rewrites one JSON file; it fetches nothing itself.

1. **Clone the new pack config.** The user needs a local AllTheMods/ATM-10 clone at the
   new release (the skill never bundles pack data; any checkout path works):

   ```bash
   git clone https://github.com/AllTheMods/ATM-10
   git -C ATM-10 checkout <release tag or commit>   # already-cloned: git -C ATM-10 fetch --tags first
   ```

2. **Run the script**, naming the checkout and the commit it sits at:

   ```bash
   python3 scripts/build_chapter_list.py /path/to/ATM-10 --commit e5e3d1d83e
   ```

   ```powershell
   python scripts/build_chapter_list.py C:\path\to\ATM-10 --commit e5e3d1d83e
   ```

   It parses the quest config with the bundled SNBT reader (`scripts/snbt.py`) —
   `config/ftbquests/quests/chapters/*.snbt` for ids and quest counts,
   `chapter_groups.snbt` for quest-book order, `lang/en_us/chapter.snbt` and
   `chapter_group.snbt` for titles (Minecraft `&` formatting codes stripped) — stamps
   the pack version from `config/bcc-common.toml` (pack `8.2` stamps `8.x`: the skill
   tracks the chapter list per major line, and the exact version goes into
   `pack_version_source`), then rewrites the example file. Before writing it prints the
   semantic changes (new/removed/retitled chapters, order or stamp changes) so it is
   easy to review the diff that lands; a second run with nothing moved reports
   `unchanged` and writes nothing.

   Stage assignments come from the script's `STAGE_ASSIGNMENTS` table, not from the
   pack: the quest book has no stage notion. A chapter the table does not know (a pack
   update added it) stops the build with a clear error naming it — never a traceback,
   and never a guessed stage. Place it in `early-game`/`tech`/`magic`/`endgame` per
   `references/progression.md`, then re-run.

3. **Review the diff** like any other researched change:

   ```bash
   git diff -- examples/progress.example.json
   ```

   Check that new chapters landed in sensible groups and stages, and that a drop+add
   pair is really a renamed chapter (its old completion history reconciles in the next
   step). If the diff is wrong, fix the checkout or the stage table — not the output.

4. **Reconcile the player's progress file** once the new list is approved: preview with
   `python3 scripts/progress.py --sync`, then apply with `--sync --yes` only after the
   player approves the preview (a dropped chapter's history is gone afterwards — say
   so). The `pack drift` warning disappears once both files carry the new list.

`--check` does the read-and-compare half without writing: exit 1 plus the change
summary when the shipped file would differ, exit 0 when it is already current — useful
before starting a review:

```bash
python3 scripts/build_chapter_list.py /path/to/ATM-10 --check
```

The shipped list is reproducible: rebuilding from pack 8.2 (main `e5e3d1d83e`)
regenerates `examples/progress.example.json` chapter-for-chapter, and the skill's tests
prove the pipeline against a small SNBT fixture rather than the full pack clone.

## Privacy

This repository is public; the user's playthrough data is not part of it.

- Real progress goes in `data/progress.json` only; `data/` is ignored by this skill's
  `.gitignore`. If it is ever staged, stop and say so.
- `examples/progress.example.json` is generic pack data (the public chapter list, all
  `pending`) — the only progress-shaped file that may be committed.
- Progress data holds no personal information by design; do not add notes fields with
  usernames, server addresses, or anything else identifying.

## Completion Checklist

Before saying the companion is up to date, confirm:

- Every status change matches what the user actually reported — nothing invented,
  nothing silently dropped.
- `progress.py` exits 0 and its percentages match the file (done/total per stage and
  overall).
- Any `pack drift` warning the report printed was relayed to the user, not hidden; no
  chapter was added, dropped, or restamped without explicit approval of a `--sync` preview.
- The advice given names the next steps in quest-book order and grounds each in a
  chapter/mod from the references.
- Endgame answers quoted verified titles or ids from `references/atm-star-checklist.md` /
  `references/boss-checklist.md` / `references/creative-checklist.md` /
  `references/armor-tools-ladder.md`, kept their hedges, and still pointed at the
  in-game quest book and JEI for current counts.
- No concrete requirement, item id, or recipe was stated from memory; specifics were
  pointed at the in-game quest book and JEI, with version-sensitive details flagged
  as approximate.
- `data/progress.json` is still untracked by git.
