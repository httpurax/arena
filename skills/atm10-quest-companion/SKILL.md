---
name: atm10-quest-companion
description: Guide for All the Mods 10 progression and quests.
version: 1.5.0
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
endgame (the ATM Star) — tells the player what to do next from wherever he is, keeps a
full recommended play order for all 66 chapters in four phases, and records which
chapters are finished. A brand-new player gets a first-hour walkthrough: spawn → the
Welcome chapter → Chapter 1: The Beginning's opening chain, every step quoted from the
pack's own quest config.
endgame (the ATM Star) — tells the player what to do next from wherever he is, and keeps
a local record of which chapters are finished. It also maps power: which
generation and storage to build at each stage, how the mods' power systems relate,
and when to upgrade.
endgame (the ATM Star) — tells the player what to do next from wherever he is, keeps
a local record of which chapters are finished, and answers "the game is lagging" from the
pack's own shipped config rather than from generic advice.

## When to Use

- The user says where he is in ATM10 (a quest chapter, a base he has built, a boss or
  resource he is stuck on) and asks *what should I do next?*
- The user has just started and asks the beginner's very first question — *"I just
  started, what do I do first?"*, "what do I do in my first hour?", "I spawned, now
  what?", "what should I build first?" — answered from
  `references/first-hour-walkthrough.md`.
- The user asks the beginner automation question — *what should I automate first?* —
  about ore processing, power, item transport, storage, or the first resource/food farm
  (answered from `references/automation-first-steps.md`).
- The user asks "which quests are worth doing for their rewards?" or wants a short,
  high-value reward pick list grounded in the pack config.
- The user finishes a quest chapter and wants it recorded ("mark Mekanism done").
- The user asks what a stage of the pack involves, which mod to commit to (tech line,
  magic line, storage network), what the ATM Star endgame needs at a high level, or what
  comes *after* the star (Chapter 4: Creative, star automation, creative-tier items).
- The user asks which dimension to open next, what unlocks one (the Twilight Forest, the
  Aether, the Undergarden, Eternal Starlight, Allthemodium's The Other, ...), which
  chapter it belongs to, or what it is worth going there for.
- The user asks which bosses this pack has, in what order to fight them, where the
  arena is, what to bring to start the fight, or what gear the quest book expects him
  to have first — answered from `references/boss-guide.md`, the order-and-tactics
  companion to `references/boss-checklist.md`.

- The user asks which Bounty Board bounties are open, what a bounty wants killed and
  how many, or which finished bounties still have rewards waiting to be claimed.
- The user asks where a gated material comes from or how to farm it ("where do I find
  vibranium?", "how do I get more allthemodium?", "do I have to mine unobtainium?", "what
  are all these mats for?") — answer from `references/resource-farming-guide.md`.
- The user asks a **mining** question about the three ATM ores specifically — which
  dimension allthemodium, vibranium, or unobtainium is in, where in that dimension it
  spawns, or what pickaxe / mining level it needs ("where does allthemodium spawn?",
  "what pickaxe do I need for vibranium?", "is unobtainium in The Beyond?", "what
  harvest tier is unobtainium?") — answer from
  `references/allthemodium-mining-guide.md`, the mining companion to
  `references/resource-farming-guide.md`.
- The user asks which power system to build (Powah or Mekanism or reactors or …),
  which power generation or storage fits his stage, whether two mods' power connects,
  or when to upgrade the setup he has.
  magic line, storage network), how to grow storage from chests to a network, what the ATM
  Star endgame needs at a high level, or what comes *after* the star (Chapter 4: Creative,
  star automation, creative-tier items).
- The user asks what to farm or what to set up farming first: Mystical Agriculture's
  essence and seed tiers, mob farms (spawners, Industrial Foregoing, Hostile Neural
  Networks), Productive Bees and Trees, crops and food — or resource chickens, which pack
  8.2 does not have.
- The user asks a **Mystical Agriculture** progression question — which essence tier comes
  next, which `Tier:` a seed sits in, what Insanium or Creative Essence unlock, where the
  essence armor, tool, and weapon sets fit, or how to get more essence — answered from
  `references/mystical-agriculture-guide.md`; the chapter's full quest inventory stays in
  `references/farming-guide.md`.
  magic line, storage network), where to build a base (Overworld vs Mining Dimension vs
  compact interiors), what the ATM Star endgame needs at a high level, or what comes
  *after* the star (Chapter 4: Creative, star automation, creative-tier items).
- The user asks how to keep a farm running while he is away ("my farm stops when I
  leave", "do I need a chunk loader?", "how do I force-load my base?") — chunk claiming
  and force-loading, the chunk loaders this pack's config actually enables or disables,
  and the spawner runes that remove the player requirement.
- The user asks how to make the game craft things for him ("how do I get autocrafting
  running?", AE2 or Refined Storage patterns, crafting CPUs, Autocrafters) — see
  `references/autocrafting-guide.md`.
- The user asks about **ore processing** — "am I wasting ores by smelting them raw?",
  "how do I double/triple my ores?", "what is the Mekanism ore-processing chain, and when
  do I start it?" (see `references/ore-processing-ladder.md`).
- The user asks *when can I fly?* — which flight item comes first, whether the pack has an
  Angel Ring or a flight totem, or when creative flight becomes possible.
- The user asks for a progress report: overall completion, per-stage completion, or the
  next unfinished chapters in quest-book order.
- The user asks about enchanting — "how do I get the best enchants?", why his Eterna is
  stuck at 30, what Infusion or a given shelf is for, or how high an enchantment like
  Sharpness can go in this pack → `references/enchanting-guide.md`.
- The user reports lag — low FPS, stuttering, a slowly ticking server — and asks how to fix
  it ("how do I fix lag?"): which of the pack's own settings and machines to look at, in
  what order, per `references/lag-fix-guide.md`.

## When Not to Use

- The user plays a different pack (ATM9, ATM10: To the Sky, another kitchen sink) — the
  chapter list here is ATM10's; say so and fall back to general advice.
- The user wants exact quest requirements, item ids, or recipes recited — this skill must
  not invent them (see Research Grounding below); point at the quest book and JEI.
- The user wants game-installation troubleshooting beyond the setup notes in
  `references/getting-started.md`, or hardware-level help (drivers, OS settings, GPU
  choices) — `references/lag-fix-guide.md` covers what the *pack* ships and deliberately
  stops at the machine.

## Research Grounding (read before advising)

The references in this skill were built from real sources: the pack's own quest config in
the official `AllTheMods/ATM-10` GitHub repository (chapter groups, order, and quest
titles), the published ATM10 mod list, and community guides. They capture the pack's
**structure** — which chapters exist, in what order, and roughly when players reach them.

Most references map structure, not exact requirements. The pinned config checklists
and reward guide below quote specific verified fields only; do not extrapolate beyond
those fields or pretend the skill knows every requirement:

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
- **The snapshot docs date themselves.** The three endgame docs —
  `references/atm-star-checklist.md`, `references/boss-checklist.md`, and
  `references/creative-checklist.md` — and the dimension guide,
  `references/dimension-guide.md`, were read from the pack repository's
  `config/ftbquests/quests/chapters/*.snbt` and `lang/en_us/chapters/*.snbt` (mod names
  and versions from `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"`
  stamp in `examples/progress.example.json`; the creative checklist and the dimension
  guide pin the exact commit (`e5e3d1d83e`). The item ids, dimension ids, quest titles, and
  quoted counts there are that snapshot's; the pack changes them between versions. Quote
  them as *what the book asked for in 8.2*, and still defer to the in-game quest book and
  JEI.
- **The verified checklists date themselves.** `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`, and
  `references/bounty-board-checklist.md` were read from the pack repository's
  `config/ftbquests/quests/chapters/*.snbt` and `lang/en_us/chapters/*.snbt` (the bounty
  checklist also from `config/ftbquests/quests/reward_tables/*.snbt`; mod names and
  versions from `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"`
  stamp in `examples/progress.example.json`; the creative and bounty-board checklists
  pin the exact commit (`e5e3d1d83e`). The item ids, quest titles, and quoted counts
  there are that snapshot's; the pack changes them between versions. Quote them as
  *what the book asked for in 8.2*, and still defer to the in-game quest book and JEI.
- **The three endgame docs and the roadmap date themselves.**
  `references/atm-star-checklist.md`, `references/boss-checklist.md`,
  `references/creative-checklist.md`, and `references/progression-roadmap.md` were read
  from the pack repository's `config/ftbquests/quests/chapters/*.snbt` and
- **The four endgame docs date themselves.** `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`, and
  `references/armor-tools-ladder.md` were read from the
- **The researched docs date themselves.** `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`, and
  `references/mob-farm-progression.md` were read from the
  pack repository's `config/ftbquests/quests/chapters/*.snbt` and
- **The endgame and ore-processing docs date themselves.**
  `references/atm-star-checklist.md`, `references/boss-checklist.md`,
  `references/creative-checklist.md`, and `references/ore-processing-ladder.md` were read
  from the pack repository's `config/ftbquests/quests/chapters/*.snbt` and
  `lang/en_us/chapters/*.snbt` (mod names and versions from
  `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"` stamp in
  `examples/progress.example.json`; the creative checklist and the roadmap pin the exact
  commit (`e5e3d1d83e`). The item ids, quest titles, and quoted counts there are that
  snapshot's; the pack changes them between versions. Quote them as *what the book asked
  for in 8.2*, and still defer to the in-game quest book and JEI.
- **The roadmap's order is a recommendation, not pack canon.**
  `references/progression-roadmap.md` sequences all 66 chapters into four phases (early,
  mid, late, endgame), but the pack itself enforces almost no order — quests are optional,
  mods are not gated, and the whole book holds exactly five cross-chapter dependency
  links (Modern Industrialization's four-age ladder, and Apothic Enchanting after
  Apotheosis Gear). Present the order as advice, keep the Main Questline's own Chapter
  1→2→3→4 numbering as the pack's, and never present the roadmap's picks between
  alternative mods as required.
- **The five researched docs date themselves.** `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`,
  `references/resource-farming-guide.md`, and
  `references/allthemodium-mining-guide.md` were read from the pack repository's
  `config/ftbquests/quests/chapters/*.snbt` and `lang/en_us/chapters/*.snbt` (mod names and
  versions from `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"` stamp
  in `examples/progress.example.json`; the creative checklist, the resource-farming
  guide, and the allthemodium mining guide pin the exact commit (`e5e3d1d83e`). The
  item ids, quest titles, and quoted counts
  there are that snapshot's; the pack changes them between versions. Quote them as *what
  the book asked for in 8.2*, and still defer to the in-game quest book and JEI.
- **The resource guide never locates anything the config does not.** "Where it is found"
  there is either the quest's own quoted words or the task type that tracks the place
  (a `dimension`, `structure`, or `kill` task) — never a coordinate, an ore level, or a
  remembered map. Repeat its "rarely / very rarely / approximate" hedges, keep untitled
  quests marked *(no title in the config)*, and send the player to JEI for drops and ore
  distribution.
  `examples/progress.example.json`; the creative checklist pins the exact commit
  (`e5e3d1d83e`). The item ids, quest titles, and quoted counts there are that snapshot's;
  `examples/progress.example.json`; the creative checklist and the mob-farm progression
  doc pin the exact commit (`e5e3d1d83e`). The item ids, quest titles, and quoted counts
  there are that snapshot's;
  the pack changes them between versions. Quote them as *what the book asked for in 8.2*,
  and still defer to the in-game quest book and JEI.
- **The power guide shares that snapshot.** `references/power-guide.md` was read from
  the same pack repository at the same commit (`e5e3d1d83e`, pack 8.2): the Power
  group's four chapters (`basic_power`, `extreme_reactors`, `generators`, `powah`),
  Chapter 1's first-power quests, and the power lines inside the tech chapters, with
  mod names and versions from the same `modlist.json`. Its quest titles, task items,
  and quoted output figures are that snapshot's, and every bridge it does not verify
  (rotation↔FE, EU↔FE, OP↔FE) is flagged approximate rather than assumed.
- **The storage ladder is dated the same way.** `references/storage-ladder.md` was read
  from that same pack **8.2** snapshot (`e5e3d1d83e`): the four Storage-group chapter
  files (`storage`, `refined_storage`, `applied_energistics_2`, `extended__advanced_ae`),
  their `lang/en_us/chapters/*.snbt` titles, subtitles, and descriptions,
  `chapter_groups.snbt`, `config/crash_assistant/modlist.json`, and
  `config/ftbquests/quests/chapters/chapter_2_the_star.snbt` for the Chapter 3
  cross-check. Its tier chains, item ids, quest titles, and quoted numbers are that
  snapshot's — quote them as *what the book asked for in 8.2*, keep the hedges, and still
  defer to the in-game quest book and JEI for recipes, slot counts, and current numbers.
- **So does the farming guide.** `references/farming-guide.md` was read from the same
  files at the same commit (`e5e3d1d83e`, pack 8.2) for the eight farming chapters —
  Mystical Agriculture, Apothic Spawners, Hostile Neural Networks, Productive Bees,
  Productive Trees, Food and Farming, Industrial Foregoing, Pylons. Its quest titles,
  quest ids, tier subtitles, and seed tiers are that snapshot's; its "what to set up
  first" order is marked as judgement, because the config does not order the farming
  chapters against each other. It also records what the config does *not* have — no
  resource-chicken mod, no growth-acceleration pylon — so never invent one.
- **So does the Mystical Agriculture guide.** `references/mystical-agriculture-guide.md`
  is a re-reading of the same commit (`e5e3d1d83e`, pack 8.2), limited to the Mystical
  Agriculture chapter (`elmystical_agriculturerr`) and the Chapter 3 entries it feeds; its
  mod versions (Mystical Agriculture 8.0.28, Mystical Agradditions 8.0.14) are the
  modlist's. Its tier ladder, quoted sentences, and quest ids are that snapshot's and are
  the same facts `references/farming-guide.md` prints in full; its tier advice, plot
  advice, and gear advice are marked *judgement*. It deliberately states no recipe, growth
  rate, drop chance, or energy cost, and it quotes no essence armor or tool *set*, because
  the snapshot verifies only the Essence Weapon named in the Cognizant Dust quote — never
  invent a set, a tier for one, or a requirement for one. Still defer to the in-game quest
  book and JEI.
  (`e5e3d1d83e`). `references/base-spots-guide.md` also pins that commit, drawing on
  the Welcome, Building Tips, Allthemodium, and AE2 quest config plus the Hyperbox config;
  its base recommendation is labelled judgement rather than a quest requirement. The item
  ids, quest titles, and quoted counts in these snapshots can change between versions.
  Quote them as *what the book asked for in 8.2*, and still defer to the in-game quest
  book and JEI.
- **The endgame docs and the automation doc date themselves.**
  `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`, and
  `references/automation-first-steps.md` were read from the
  pack repository's `config/ftbquests/quests/chapters/*.snbt` and
  `lang/en_us/chapters/*.snbt` (mod names and versions from
  `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"` stamp in
  `examples/progress.example.json`; the creative checklist and the automation doc pin the
  exact commit (`e5e3d1d83e`). The item ids, quest titles, quoted counts, and quoted
  quest text there are that snapshot's; the pack changes them between versions. Quote
  them as *what the book asked for in 8.2*, keep the automation doc's ranking marked as
  judgement, and still defer to the in-game quest book and JEI.
- **The enchanting guide dates itself the same way.** `references/enchanting-guide.md`
  was read from the same pinned commit (`e5e3d1d83e`, pack **8.2**): the Apothic
  Enchanting and Apotheosis Gear chapters' `*.snbt` and `lang/en_us/chapters/*.snbt` files,
  plus `config/apotheosis/enchantments.cfg` for every enchantment's configured
  `Max Level` and `Max Loot Level`. Its Eterna / Quanta / Arcana figures and shelf set-ups
  are quest text, not formulas — repeat them as quoted and approximate, and send exact
  infusion windows to JEI and the enchanting table's own pool view.
- **The three endgame docs and the lag guide date themselves.**
  `references/atm-star-checklist.md`, `references/boss-checklist.md`,
  `references/creative-checklist.md`, and `references/lag-fix-guide.md` were read from the
  pack repository's `config/ftbquests/quests/chapters/*.snbt` and
  `lang/en_us/chapters/*.snbt` (mod names and versions from
  `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"` stamp in
  `examples/progress.example.json`; the creative checklist and the lag guide pin the exact
  commit (`e5e3d1d83e`). The item ids, quest titles, and quoted counts there are that
  snapshot's; the pack changes them between versions. Quote them as *what the book asked
  for in 8.2*, and still defer to the in-game quest book and JEI.
- **The lag guide quotes config, and the player's own config wins.** Every setting in
  `references/lag-fix-guide.md` is a value shipped in the pack repository at that commit
  (`config/memorysettings.json`, `config/modernfix-mixins.properties`,
  `config/alltheleaks.json`, the per-mod `*-client.toml` / `*-server.toml` files, and the
  rest named in its provenance table). It is a snapshot of *defaults*, not of the user's
  install: never recite a value as what his file says, never name a config key that is not
  in that table, and never state a frame-rate gain — nothing here can measure his machine.
  Which of the two problems he has (client FPS vs server TPS), the order of the steps, and
  anything about his hardware are judgement, and the doc labels them as such.
- **The four config-pinned docs date themselves.** `references/atm-star-checklist.md`,
  `references/boss-checklist.md`, `references/creative-checklist.md`, and
  `references/chunk-loading-guide.md` were read from the pack repository's
  `config/ftbquests/quests/chapters/*.snbt` and `lang/en_us/chapters/*.snbt` (mod names and
  versions from `config/crash_assistant/modlist.json`) at pack **8.2** — the `"8.x"` stamp
  in `examples/progress.example.json`; the creative checklist and the chunk-loading guide
  pin the exact commit (`e5e3d1d83e`), and the chunk-loading guide also reads the pack's
  shipped mod configs (`config/*.toml`, `config/*.json`), its `kubejs/` tweaks and
  localization overrides, and its `changelogs/`. The item ids, quest titles, config values,
  and quoted counts there are that snapshot's; the pack changes them between versions.
  Quote them as *what the book and the config said in 8.2*, and still defer to the in-game
  quest book and JEI.
- **The autocrafting guide dates itself the same way.** `references/autocrafting-guide.md`
  was read from the same commit (`e5e3d1d83e`, pack 8.2) — the Storage chapters
  `applied_energistics_2`, `refined_storage`, and `extended__advanced_ae` (quest files
  plus their `lang/en_us/chapters/*.snbt` titles and descriptions, mod versions from
  `config/crash_assistant/modlist.json`). Its quest titles, task item ids, and quoted
  counts are that snapshot's; quote them as what the book asked for in 8.2, and still
  defer to the in-game quest book and JEI.
  (`e5e3d1d83e`), and the ore ladder is read from that same commit. The item ids, quest
  titles, and quoted counts there are that snapshot's; the pack changes them between
  versions. Quote them as *what the book asked for in 8.2*, and still defer to the
  in-game quest book and JEI.
- **The flight guide dates itself too.** `references/flight-guide.md` was read from the same
  commit (`e5e3d1d83e`, pack 8.2): the same chapter and lang files, plus the pack's Iron
  Jetpacks tier files (`config/ironjetpacks/jetpacks/*.json`). Its titles, task items, and
  quotes are verified; its *(judgement)* labels — how early a flight item arrives — are
  read off dependency chains, so repeat them as judgement. Its absent list (no Angel Ring,
  no flight totem, no quest for the vanilla Elytra) is what the 8.2 book and modlist lack;
  never fill those gaps from memory.

- **The first-hour doc dates itself the same way.**
  `references/first-hour-walkthrough.md` was read from the same commit (`e5e3d1d83e`,
  pack 8.2): the **Welcome** chapter (`config/ftbquests/quests/chapters/welcome.snbt`,
  6 quests) and the opening of `mainquestline_part_1.snbt` (**Chapter 1: The
  Beginning**, 36 quests), their `lang/en_us/chapters/*.snbt` titles and descriptions,
  `chapter_groups.snbt`, the quest book's own `data.snbt` switches, and
  `config/ftbultimine-server.snbt`. Its quest titles, ids, task items, counts, rewards
  and dependencies are that snapshot's; quote them as *what the book asked for in 8.2*.
  The walkthrough's **order** follows verified dependencies, but the whole "what fits in
  an hour" framing — every minute estimate, and the "don't do this yet" list — is
  **judgement**; repeat it as such. Four Welcome entries and several Chapter 1 entries
  have no title in the config: mark them, never rename them. State no recipe,
  coordinate, or keybind the config does not, and still defer to the in-game quest book
  and JEI.
- **The boss guide dates itself the same way.** `references/boss-guide.md` was read
  from the same commit (`e5e3d1d83e`, pack 8.2): the boss chapters Chapter 1, Bounty
  Board, Twilight Forest, Aether, Cataclysm, Deeper and Darker, Undergarden, Eternal
  Starlight, Allthemodium, Draconic Evolution, Iron's Spells, Ars Nouveau, Ice and
  Fire, Chapter 3 and Basic Armor, their `lang/en_us/chapters/*.snbt` titles and
  descriptions, and `config/crash_assistant/modlist.json`. Its quest titles, quest
  ids, task ids, and quoted "Hearts" figures are verified; its fight order is verified
  only where a dependency link or quest sentence states it (the Twilight trophy line,
  the summoning gates), and everywhere else is *(judgement)*; its gear column is
  a config task, a tool tier quoted from quest text, or labelled judgement — never
  a loadout. The fights the book tracks by trophy item, drop item, advancement,
  structure, or dimension task are never restated as plain kill tasks, and The Final
  Boss stays what its quest says it is (not implemented). Still defer to the in-game
  quest book and JEI.

- **The reward guide is also a pinned snapshot.** `references/best-reward-quests.md`
  uses only quest config from pack **8.2**, `main` commit `e5e3d1d83e` (2026-09-22).
  It quotes actual titles, quest ids, fixed item rewards and stored components; priorities
  and value judgements are explicitly approximate. Do not confuse a reward with a task,
  recipe or unlock, rename untitled quests, or promise specific loot-table outcomes.
  The in-game quest book remains authoritative if the player's version differs.

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
- **"I just started — what do I do first?" goes to
  `references/first-hour-walkthrough.md`:** the route from spawn to the first quests
  done — the **Welcome** chapter's five player-visible quests (10 XP each), then
  **Chapter 1: The Beginning**'s opening chain (*Welcome to Getting Started!* →
  *Putting the Craft in Minecraft* → *Our First Pick* → *Stone Age* → *The Metal Age* →
  *An Iron Pick*) and the branches off it (*Crafting, but on a Stick*, *Basic Ore
  Doubling*, *Lava Bucket*, the starter generators), each quoted with the config's own
  task items, counts, rewards and dependencies. Give the steps in that order, keep the
  doc's *(judgement)* labels on the timing and on its "not a first-hour problem" list,
  mark its untitled entries as untitled rather than renaming them, and state no recipe,
  coordinate, or keybind the config does not.
- **"Which chapter first, second, third?" goes to `references/progression-roadmap.md`:**
  all 66 chapters as one recommended play order in four phases (early / mid / late /
  endgame), one grounded line per chapter. Relay it as what it is — a recommendation
  built on the pack-8.2 config, not pack canon — and let the player's book and
  interests override it whenever they differ.
  First-hour and setup questions go to `references/getting-started.md`. For "where
  should I build my base?", use `references/base-spots-guide.md`: distinguish the
  Overworld default (judgement) from the Mining Dimension's verified mining role and
  Building Tips' Compact Machines quest; do not promise cross-dimensional connections or
  automatic chunk loading.
- **Mob-farm questions go to `references/mob-farm-progression.md`.** "How do I farm mob
  drops?" ("is there a mob grinder?", "how do spawners work here?", "where do spawn eggs
  come from?") → the dark-room-to-Data-Center ladder: the Bounty Board kill tiers, the
  Apothic Spawners chapter's silk-touch spawners, runes, and upgrade runes, the seven
  cross-mod spawners, the egg routes, the Industrial Foregoing / EvilCraft kill machines,
  Hostile Neural Networks' simulated kills, and the loot-routing quests. Quote them as
  what the book tracked in pack 8.2, keep the doc's hedges (the dark-room grinder is
  general knowledge, not quest content; no soul-shard quests exist), and still send the
  player to the in-game quest book and JEI for current counts and recipes.
- Give the next steps **in quest-book order** within the relevant chapters — a short,
- **Reward-shopping questions** ("which quests are worth doing for their rewards?")
  go to `references/best-reward-quests.md`. Offer a few picks matching the player's
  current route, quote the verified title and fixed payoff, and label the priority as
  judgement (approximate). This is advice order, not quest-book order. Check dependencies
  and tasks in the book before suggesting a detour; treat table rewards as uncertain
  and do not infer effects or technical bridges from item ids or components.
- For progression advice (rather than reward shopping), give the next steps
  **in quest-book order** within the relevant chapters — a short,
  ordered list ("1. finish the X chapter up to Y; 2. start Z; 3. ..."), not a lecture.
- For each step, name the chapter/mod it belongs to and *why* it is next (what it
  unlocks), grounded in the references.
- For any concrete requirement (item counts, ingredients, ore levels, boss mechanics),
  point at the quest entry and JEI instead of stating numbers — per Research Grounding
  above. Flag anything version-sensitive as approximate.
- **Beginner automation questions go to `references/automation-first-steps.md`.** "What
  should I automate first?" → the five first automations in impact order — ore
  processing, power, item transport, storage, farms — each anchored to verified quest
  titles, ids, and quest text from the pack 8.2 config, with the ranking itself marked as
  judgement and the in-game quest book and JEI still authoritative for requirements and
  recipes.
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
- **Boss-order, arena, and gear questions go to `references/boss-guide.md`.**
  "Which boss, in what order, and with what gear?", "where is the boss arena?",
  "what do I need to summon it?", "am I geared enough for Cataclysm / the Chaos
  Guardian?" -> the recommended fight order built on the pack-8.2 config: vanilla
  first, the Twilight Forest trophy line in its one strict (verified) order, the
  Aether's three dungeons and Cataclysm's eight in any order, then the Chaos
  Guardian — each fight with its verified tracking quest, arena (structure id or
  the place quest text names), summoning gate, and the gear signal the book
  itself states (a task, a quoted tool tier, or an expectation sentence), with
  every readiness judgement labelled as such. Pair it with
  `references/boss-checklist.md` for the full inventory. Never invent a tactic,
  an enchantment, or a required armour tier the guide does not quote.

- **Dimension questions go to `references/dimension-guide.md`.** "Which dimension should I
  open first?", "what unlocks the Aether / The Other?", "is the Undergarden worth it yet?"
  → the 13 destinations the config's 28 `dimension` tasks (plus the Twilight Forest's
  `twilightforest:root` advancement) reach, in a recommended visit order: each with its
  verified unlock quest and dimension id, its chapter and stage tag, what the book sends
  the player there for (bosses, resources, key quests, star components), and a "roughly
  when" that marks which steps are verified dependency links or quest text and which are
  approximate judgement. The book gates nothing, so present the order as a
  recommendation. Portal recipes and coordinates are deliberately not on that page — send
  the player to the quest entry and JEI for those.
- **Bounty questions go to the bounty doc.** "Which bounties are open, what do they
  want, and what haven't I claimed?" → `references/bounty-board-checklist.md`: the
  standalone Bounty Board chapter's 50 quests (49 playable — the 50th is a hidden,
  invisible config quest) as a tick-off list: the hub, the eight 5/10/50/100-kill
  bounty lines, the four variant hunts, and the twelve single-kill boss/miniboss
  bounties, each with its verified kill counts and the fixed, XP, and random-table
  rewards it pays. The chapter is kill-only — it has no collect or item tasks, so never
  phrase a bounty as collecting items — and it is not "Chapter 5": the config gives it
  no group and no number. Note the claim trap the config states: every random reward
  is excluded from Claim All, so finished bounties must be claimed quest by quest.
  Where a bounty duplicates a boss tracked elsewhere, pair it with
  `references/boss-checklist.md` for dimension, arena, and roughly when.
- **"Where do I get X?" goes to the resource guide.** `references/resource-farming-guide.md`
  maps each gated material — allthemodium, vibranium, unobtainium, their smithing
  templates, the Piglich Heart, the three alloys, Creative Essence, nether stars — to where
  it comes from (dimension, ore, mob drop, or crafting chain) and roughly which stage it
  belongs to, plus the farming systems the book itself points at (Mystical Agriculture,
  Productive Bees, Hostile Neural Networks). Quote its verified quest titles and the pack's
  own "where" sentences, keep the rare/very-rare hedges, and never add a coordinate, ore
  level, or recipe of your own — the quest entry and JEI settle those.
- **Allthemodium-ore questions go to the mining guide.** "Which dimension is
  allthemodium in?", "where does vibranium spawn?", "what pickaxe mines unobtainium?",
  "what harvest tier are the ATM ores?" → `references/allthemodium-mining-guide.md`:
  the three ores with their ore block ids, the dimension each is in, the biome tag that
  gates spawning, the pickaxe tier each needs, and the pack's own in-game tooltip lines
  quoted verbatim, plus the Basic Tools chapter's Harvest Tier 1–6 ladder. Quote the
  tooltip line and the quest title, keep the rare/very-rare hedges, and publish no ore
  level, coordinate, or recipe — where two pack sources disagree (vibranium's biome tag
  versus its tooltip), print both rather than picking one.
- **Power questions go to the power guide.** "Which power should I build?", "Powah or
  Mekanism or a reactor?", "does Create power run my machines?", "when to upgrade
  power?" → `references/power-guide.md`: the pack's own Early/Mid/End Power hubs
  expanded per stage (which generation and storage to build, in the order the Basic
  Power chapter routes them), the FE core versus the separate systems the quests
  verify (Create rotation, MI steam→EU electricity, PneumaticCraft pressure, AE2's
  AE, Draconic OP — and the only bridges between them the book names), and the
  upgrade triggers, flagged approximate where the book gives no figure. Quote its
  verified titles and ids, keep its hedges, and never convert an unquoted FE/t,
  EU/t, or OP figure from memory.
- When the choice is between alternatives (AE2 vs Refined Storage, Mekanism vs Create vs
  Modern Industrialization, Powah vs Mekanism vs Extreme Reactors for power), present
  them as alternatives with their trade-offs and let the user pick; never invent a
  "required" path — the pack itself says quests are optional and mods are not gated,
  and its power quests accept either/or alternatives at every stage.
- **Storage questions go to `references/storage-ladder.md`.** "My chests are full",
  "backpack, drawers, or bigger chests?", "when do I start a storage network?", "Refined
  Storage or AE2?", "what does the next storage tier unlock?" → the Storage group's four
  chapters in dependency order: **Basic Storage** (90 quests — the vanilla chest line,
  Sophisticated Storage's copper → netherite chests and barrels, Sophisticated Backpacks,
  Functional Storage's drawers), then **Refined Storage** (72) and **Applied Energistics
  2** (74) as the two alternative first networks, then **Extended \& Advanced AE** (56)
  on the AE2 side. The doc carries the verified titles, the item ids each rung asks for,
  the pack's own quoted signals for moving up a rung, and the AE2-family items Chapter 3
  wants. Quote them as what the book asks for, keep the hedges, and send the player to the
  in-game quest book and JEI for recipes, slot counts, and current numbers.
- **Farming questions go to `references/farming-guide.md`.** "What should I set up farming
  first?" → its short answer: food, then Mystical Agriculture's Inferium (the pack's own
  *Inferium Farmland* quest says to start it as soon as you can), a crop harvester, one
  mob-drop route, then bees before trees — present that order as the judgement it is.
  "Which tier is this seed?" → its table of all 125 seed quests by `Tier:` subtitle.
  "How do I farm mobs?" → its three routes: Apothic Spawners (and the upgrade-rune
  ladder), Industrial Foregoing's machines, Hostile Neural Networks. "Where are the
  resource chickens?" → not in pack 8.2: say so, point at what does that job here
  (Mystical Agriculture seeds, Productive Bees, Hostile Neural Networks), and never name
  a chicken mod.
- **Mystical Agriculture progression questions go to
  `references/mystical-agriculture-guide.md`.** "Which essence tier do I need next?",
  "what tier is this seed?", "how do I get Insanium / Creative Essence?", "where do the
  essence armor and tool essences fit?", "how do I get more essence faster?" → its tier
  ladder (Inferium → Prudentium → Tertium → Imperium → Supremium → Awakened Supremium →
  Insanium → Creative Essence) with each tier's verified quote, id, and dependency, and its
  get-more table (Infusion Altar, Seed Reprocessor, Growth Accelerators, tiered farmland,
  Soulium and mob seeds, Harvester, bees). Quote its titles and ids as written there, keep
  its *judgement* labels, send gear questions to JEI and
  `references/armor-tools-ladder.md`, and the full 125-seed inventory to
  `references/farming-guide.md`. Never state a recipe, a growth rate, or an essence-armor
  requirement.
- **Enchanting questions go to `references/enchanting-guide.md`.** "How do I get the best
  enchants?", "why is my Eterna capped at 30?", "what does a Hellshelf / Seashelf /
  Sculkshelf do?", "how high can Sharpness go?" → the Apothic Enchanting chapter's 58
  quests in dependency order: the three table stats (Eterna, Quanta, Arcana) in the quest
  text's words, the two Eterna ceilings (the Apotheosis World Tier and each shelf's own
  maximum), the shelf ladder up to the *Best Enchanting set-up* quest and the *Enchanting
  Table of the Raven*, the shelves that steer the pool, and every vanilla enchantment's
  configured `Max Level`. Lead with its short answer, quote titles and ids as written
  there, and keep its hedges: stat windows are quest text — JEI and the table's pool
  view are authoritative.
- **"How do I fix lag?" goes to `references/lag-fix-guide.md`.** Work it in its own
  order, and answer both halves of the question: first *which* lag it is (client FPS vs
  server TPS — the pack's quest text uses both words), then the ladder — memory against the
  pack's own table in `config/memorysettings.json`, shaders, the video settings that
  actually exist, the machines and farms the quest book itself calls laggy (*Pipez*,
  *Mekanism*, *Bio-Generator*, the Harvester Pylon, *Sea Prism*'s mass breeder warning),
  item and entity spam, chunk loaders, and finally measuring with the spark and Observable
  that already ship with the pack. Quote the guide's config values as *what the pack ships
  by default*, keep its judgement labels, never name a setting that is not in its
  provenance table, and never promise a frame-rate gain. Tell him nothing needs installing:
  the performance mods are already in the pack.
- **"How do I keep my farm running while I'm away?" goes to
  `references/chunk-loading-guide.md`.** It is a cross-stage question, so answer it from
  where the player is rather than treating it as a stage: the FTB Chunks answer (claim,
  then shift-left-click to force-load) works in the first hour and is what the Welcome
  chapter's *Claiming Chunks* task teaches; the AE2 Spatial Anchor and the Apothic
  Spawners *Ignore Players* rune arrive in tech. Work down that page's ordered answer,
  quote its verified quest titles and config values, keep its `judgement` and
  `translation` flags, and **never state a claim or force-load limit** — the pack ships no
  FTB Chunks config, so any number would be invented.
- **Autocrafting questions go to the autocrafting guide.** "How do I make the game craft
  things for me?", "how do I get autocrafting running?", "AE2 or Refined Storage?",
  "what is a Pattern / crafting CPU / Autocrafter?" → `references/autocrafting-guide.md`:
  the two Storage autocrafting chains in dependency order (AE2 *Auto-Crafting* → *Patterns*
  → Assemblers and the crafting CPU; Refined Storage *Autocrafting* → *Pattern Grid* →
  *Autocrafter*), the network prerequisites before them, and the Extended & Advanced AE
  scale-up behind them. Present AE2 and Refined Storage as alternatives, walk the chosen
  chain in the guide's order, keep its hedges, and still send the player to the in-game
  quest book and JEI for recipes and current counts.
- **Ore-processing questions go to `references/ore-processing-ladder.md`.** "Am I wasting
  ores by smelting them raw?" → the pack's own answer from Chapter 1's *Basic Ore
  Doubling* (smelting raw is "necessary" early, but the Ore Hammer's 1 raw ore → 2 ore
  dust is the book's own doubling), then the ladder it introduces: Mekanism's four tier
  quests (*Enrich then Smelt* → *Making Oxygen for Purifier* / *Crush and Enrich our
  Clumps* → *Making Chlorine* / *Injecting Hydrogen Chloride* / *Shard, to Clump, to
  Dust, to Ingot* → *Creating Sulfuric Acid* / *Melting Ores with Acid and Crystallizing
  them* / *Making more Hydrogen Chloride* / *Crystal, Shard, Clump, ETC*), plus the other
  routes the book lists (Occultism's crusher demons, Industrial Foregoing's *Ore
  Processing: Step 1/2/3*, Oritech, Create, Immersive Engineering, RailCraft, Modern
  Industrialization). Quote the config's own numbers per step; the community
  "doubling/tripling/quadrupling" names are **approximate shorthand** — the book's labels
  are *Tier 1*–*Tier 4 Ore Processing* and Industrial Foregoing's 2x–5x lines. Never
  invent a tier, machine, or per-ore total.
- **Flight questions go to `references/flight-guide.md`.** "When can I fly?", "is there an
  Angel Ring?", "how do I get creative flight?" → the flight items the book tracks,
  cheapest first: the dependency-free Wood jetpack and Charging Station in Tips and
  Tricks, XyCraft's tethered balloon, the elytra add-ons, then the creative-flight
  upgrades (Just Dire Things, Advanced AE, Draconic Evolution, the MekaSuit) and the
  Creative Jetpack — each with its verified quest, task item, and dependency chain. Lead
  with the cheapest reliable path, keep the doc's *(judgement)* labels on timing, say
  plainly what the 8.2 book does not have, and send recipes and energy numbers to JEI.
- When the choice is between alternatives (AE2 vs Refined Storage, Mekanism vs Create vs
  Modern Industrialization), present them as alternatives with their trade-offs and let
  the user pick; never invent a "required" path — the pack itself says quests are
  optional and mods are not gated. `references/storage-ladder.md` has the verified
  side-by-side for the storage pair, including the fact that Chapter 3's storage tasks are
  all AE2-family.

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
  chapter/mod from the references. Play-order recommendations came from
  `references/progression-roadmap.md` and were offered as a recommendation, not canon.
- Endgame answers quoted verified titles or ids from `references/atm-star-checklist.md` /
  `references/boss-checklist.md` / `references/creative-checklist.md`, kept their hedges,
  and still pointed at the in-game quest book and JEI for current counts.
- Boss answers followed the fight order in `references/boss-guide.md` — the Twilight
  line in its strict verified order, parallel lines left unordered, gear limited
  to what the quests state or clearly-labelled judgement — and still pointed at
  the in-game quest book and JEI.

- Dimension answers named the verified unlock quest and dimension id from
  `references/dimension-guide.md`, kept its verified/approximate labels, and supplied no
  portal recipe or coordinates.
- Bounty answers quoted verified titles, entity ids, and counts from
  `references/bounty-board-checklist.md`, never rephrased a kill bounty as a collect
  quest, reminded the player that the chapter's random rewards are excluded from
  Claim All, and still pointed at the in-game quest book and JEI.
- Resource answers came from `references/resource-farming-guide.md` (or the quest book /
  JEI), kept its "rarely / very rarely / approximate" hedges and its *(no title in the
  config)* markings, and stated no coordinate, ore level, or recipe the config does not.
- Allthemodium-ore mining answers came from `references/allthemodium-mining-guide.md`:
  they named the ore's dimension and spawn biome from the pack's biome tags and its own
  in-game tooltip lines, gave the needed pickaxe and the harvest tier from the Basic
  Tools chapter, and published no ore level, coordinate, or recipe. Where the page's two
  sources disagree (vibranium's biome tag versus its tooltip), both were relayed rather
  than one chosen, and the answer still pointed at the in-game quest book, the ore
  tooltip, and JEI.
- Power answers quoted verified titles or ids from `references/power-guide.md`, kept
  its approximate flags (including every unconverted output figure and every
  unverified cross-system bridge), and still pointed at the quest entry and JEI.
- Storage answers quoted verified titles or ids from `references/storage-ladder.md`,
  presented Refined Storage and AE2 as alternatives rather than a required path, kept the
  hedges (no invented slot counts, recipes, or energy numbers), and pointed at the in-game
  quest book and JEI for current specifics.
  `references/boss-checklist.md` / `references/creative-checklist.md` /
  `references/armor-tools-ladder.md`, kept their hedges, and still pointed at the
  in-game quest book and JEI for current counts.
- Farming answers quoted verified titles, ids, and tiers from
  `references/farming-guide.md`, labelled its "what to set up first" order as judgement,
  and claimed no farm, seed, or mod the config does not have (no resource chickens in
  pack 8.2).
- Automation answers quoted verified quest titles from
  `references/automation-first-steps.md`, kept the 1–5 ranking marked as judgement, and
  still pointed at the in-game quest book and JEI for requirements and recipes.
- First-hour answers quoted verified quest titles and ids from
  `references/first-hour-walkthrough.md`, gave the Welcome chapter and Chapter 1's
  opening chain in dependency order with the config's own task items and rewards, kept
  its *(judgement)* labels on timing and on the "don't do this yet" list, marked
  untitled entries as untitled instead of renaming them, and stated no recipe,
  coordinate, or keybind the config does not.
- Enchanting answers quoted verified titles, ids, and configured levels from
  `references/enchanting-guide.md`, kept every Eterna / Quanta / Arcana figure attributed
  to the quest text, and pointed at JEI and the table's pool view for exact windows.
- Chunk-loading answers came from `references/chunk-loading-guide.md`: they quoted the
  Welcome chapter's verified claim/force-load steps, named only chunk loaders this pack's
  config verifies, kept the four switches it ships **off** off, stated no claim or
  force-load limit, and flagged every `judgement` call and every `translation` of the
  pack's bundled pt_br/ru_ru strings.
- Autocrafting answers followed `references/autocrafting-guide.md` in dependency order,
  quoted its verified titles or ids with their hedges, and still pointed at the in-game
  quest book and JEI for recipes and current counts.
- Ore-processing answers came from `references/ore-processing-ladder.md`, quoted the
  config's own per-step numbers instead of a computed per-ore total, flagged the
  community "doubling/tripling/quadrupling" names as approximate, marked untitled quests
  as untitled, and still pointed at the quest entry and JEI.
- Flight answers quoted verified titles or ids from `references/flight-guide.md`, kept its
  *(judgement)* labels on timing, and promised nothing the 8.2 book lacks — no Angel Ring,
  no flight totem, no elytra location.
- Mob-farm answers quoted verified titles or ids from `references/mob-farm-progression.md`,
  marked the vanilla dark-room grinder as general knowledge rather than pack content, and
  still pointed at the in-game quest book and JEI for current recipes and rates.
- No concrete requirement, item id, or recipe was stated from memory; specifics were
  pointed at the in-game quest book and JEI, with version-sensitive details flagged
  as approximate.
- Any lag answer named the kind of lag first, quoted only settings that
  `references/lag-fix-guide.md` verifies from the pack config, kept its
  approximate/judgement hedges, promised no frame-rate number, and told the user his own
  `config/` folder and the in-game quest book win over the guide's 8.2 snapshot.
- Reward answers used `references/best-reward-quests.md` for verified titles/ids and
  fixed payoffs, kept judgement/uncertainty labels, and deferred to the current book.
- `data/progress.json` is still untracked by git.
