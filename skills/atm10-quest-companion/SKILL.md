---
name: atm10-quest-companion
description: Guide for All the Mods 10 progression and quests.
version: 1.0.0
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
  magic line, storage network), or what the ATM Star endgame needs at a high level.
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
  chapters this skill does not know, trust his book and note the mismatch.

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

Run these from the skill directory (`<skills root>/gaming/atm10-quest-companion/`).
`progress.py` is stdlib-only Python 3.8+, needs no third-party packages and no network;
the interpreter is `python3` on Linux and macOS, `python` (or `py -3`) on Windows.

## Progress file

One JSON document, `{"chapters": [...]}`, one object per quest-book chapter, stored in
quest-book order (standalone chapters first, then the book's groups in order):

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
- When the choice is between alternatives (AE2 vs Refined Storage, Mekanism vs Create vs
  Modern Industrialization), present them as alternatives with their trade-offs and let
  the user pick; never invent a "required" path — the pack itself says quests are
  optional and mods are not gated.

### 3. Record completion and report progress

When the user says a chapter (or several) is done — or wants one reopened — edit
`data/progress.json`, flipping that chapter's `status` between `pending` and `done`.
Change only what the user reported; never mark chapters done on his behalf "because he
probably has". Then run the report:

```bash
python3 scripts/progress.py
```

```powershell
python scripts/progress.py
```

```
atm10 quest companion - chapter progress
data: <skill>/data/progress.json

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
chapters in quest-book order. Options: `--data PATH` for another file, `--next N` to cap
the list length (default 10). It never writes the file and never raises a traceback: a
missing, empty, malformed, or schema-breaking file is reported as one clear message with
exit status 1 — relay that message and the fix it suggests, do not paper over it.

Use the report to answer "what next?" too: the first listed pending chapter in the
player's current stage is the natural recommendation, cross-checked against what he told
you he has already built (the file may lag reality — update it first).

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
- The advice given names the next steps in quest-book order and grounds each in a
  chapter/mod from the references.
- No concrete requirement, item id, or recipe was stated from memory; specifics were
  pointed at the in-game quest book and JEI, with version-sensitive details flagged
  as approximate.
- `data/progress.json` is still untracked by git.
