# Bounty Board checklist — all 50 quests, tick-off list (verified titles, pack 8.2)

**What this page is.** The tick-off list for **All the Mods 10**'s **Bounty Board** chapter:
every quest the config holds, what each one asks the player to do, what the book pays for
it, and how the fifty hang together. It answers "what is left on the Bounty Board, and what
can I claim?" — a page to work through while doing something else, and a map for the
rewards a player would otherwise walk past. It is a *map of the chapter*, not a combat,
farming, or loot guide.

## Provenance — everything here was read, not remembered

Every quest title, kill entity, count, reward, dependency, and quoted sentence below comes
from the official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10)
at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/bounty_board.snbt` | the chapter's 50 quests, their tasks (entity ids and counts), dependencies, canvas positions, and reward entries |
| `config/ftbquests/quests/lang/en_us/chapters/bounty_board.snbt` | the 25 English quest titles, the 2 subtitles, 18 description texts, and 9 task titles |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapter's own title, *Bounty Board* |
| `config/ftbquests/quests/reward_tables/*.snbt` | the names of the three loot-crate tables the bounty rolls draw from (`common`, `uncommon`, `rare`) and their roll size |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |

## Where this chapter sits

| | |
|---|---|
| Config filename / skill id | `bounty_board` |
| Book title | **Bounty Board** |
| Group | none — a standalone chapter (`group: ""`), rendered outside the book's groups |
| Book position | `order_index` 1 — second in the standalone run at the top of the chapter list, right after *Welcome* |
| Tracked by this skill as | number 2 of 66 in `examples/progress.example.json`, stage `early-game` |
| Progression mode | `flexible` — the config gates nothing behind it |
| Chapter icon | `minecraft:zombie_head` |

**On the numbering.** The config's own title for this chapter is just *Bounty Board*: no
chapter number appears on it, and no chapter title in pack 8.2 carries the number 5 (the
numbered ones run *Chapter 1: The Beginning* → *Chapter 4: Creative*). If a guide or a
player calls this the "Chapter 5" of the quest book, treat that as a label of convenience —
open the *Bounty Board* entry and let the in-game book settle it.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Everything on the board is a kill task.** All 87 kill tasks, and the hub's single
  `advancement` task, are listed below; this chapter contains **no item-collect and no
  craft tasks**. If a player describes a "hand in X items" bounty, it is not in this
  chapter — ask what the quest entry says, and never invent a task, an item id, or a count.
- **Titles are the config's.** 25 of the 50 quests carry an explicit title; the other 25 do
  not (the 10/50/100 rungs of the eight ladders, and one invisible authoring quest). Those
  are marked *(no title in the config)* — the book then shows the task's own name. Do not
  present a derived name as a verified title.
- **Rewards are quoted from the config, counts included.** An item's `×N` is the reward
  entry's count in the chapter file; a `+` bonus is the config's `random_bonus` field (the
  book rolls the extra — treat the exact bonus as approximate). Loot-crate rolls say which
  named table the roll draws from, not what it contains.
- **Approximate means approximate.** Mob behaviour, spawn areas, and farm designs are
  version- and world-sensitive; the few description hints this page quotes are marked
  *quest text* and verified only against the pack's own words.
- **Nothing here was invented, and nothing is added from memory.** A quest that is not on
  this page is not in this chapter: the answer is "open that quest in the book / look it up
  in JEI", never a plausible-sounding guess.

## How the chapter is shaped

Fifty quests, ninety tasks, one idea: kill things, get paid. The config's own arithmetic:

| | |
|---|---|
| Quests in the chapter | **50** (49 visible; one is `invisible: true`, an authoring leftover) |
| Tasks in total | 90 — 87 `kill`, 1 `advancement` (the hub), 2 `checkmark` (the invisible quest) |
| Distinct kill entity ids | 63 |
| Quests carrying an explicit title | 25 |
| Quests paying XP | 49; total `xp` rewards in the config add up to **6,490 XP** |
| Kills needed to clear every kill task | **1,376** (1,320 in the ladders, 42 in the four variant quests, 14 across the twelve boss bounties) |
| Quests with no dependencies | 22 (the eight first rungs, the twelve boss bounties, the hub, the invisible quest) |
| Loot-crate rolls in the config | 42 — 8 `common`, 26 `uncommon`, 8 `rare` |

That is three groups:

1. **The eight kill-count ladders — 36 quests.** Eight mobs, each with four rungs
   (5 → 10 → 50 → 100 kills, 165 kills per ladder), and four extra "variants" quests
   hanging off four of the ladders. This is the board's bulk.
2. **The twelve boss and miniboss bounties — 12 quests.** One kill each per boss (the
   Trader bounty asks for three kills), all one-off, all independent.
3. **The hub and one authoring leftover — 2 quests.** *Bounty Board* itself, and a quest
   the config marks `invisible: true`.

The book lays the chapter out on a canvas, so this page follows the canvas: the eight
ladders are numbered below in the order the config's `x` coordinates put them left to
right, then the middle column of boss bounties, then the hub.

## The eight kill-count ladders (36 quests)

Each ladder is one mob in four rungs. The rungs chain by dependency — 5 unlocks 10 unlocks
50 unlocks 100 — and the last rung is drawn as a pentagon (`shape`, the only quests in the
chapter that set one); the first rung is the only titled one. The eight ladders are
independent of each other and of the hub.

The book reveals them as the player goes: the eight 10-kill rungs carry
`hide_until_deps_visible: true`, and the four side quests carry
`hide_until_deps_complete: true`, so a rung appears once the rung below it is visible and
the side quest once the first rung is done. (The Zombies 5-kill rung is the one quest
carrying an explicit `false`; those are the chapter's only reveal flags — the one
invisible quest is the authoring leftover below.)

| # | Ladder (verified title) | Mob (verified task entity) | Rungs (kills) | Side quest |
|---|---|---|---|---|
| 1 | *Overworld Bounty: Zombies* | `minecraft:zombie` | 5 / 10 / 50 / 100 | *Zombie Variants* |
| 2 | *Overworld Bounty: Skeletons* | `minecraft:skeleton` | 5 / 10 / 50 / 100 | *Skeleton Variants* |
| 3 | *Overworld Bounty: Creepers* | `minecraft:creeper` | 5 / 10 / 50 / 100 | *Overhauled Creepers* (16 mobs) |
| 4 | *Overworld Bounty: Spiders* | `minecraft:spider` | 5 / 10 / 50 / 100 | — |
| 5 | *Overworld Bounty: Witches* | `minecraft:witch` | 5 / 10 / 50 / 100 | — |
| 6 | *The Nether Bounty: Blazes* | `minecraft:blaze` | 5 / 10 / 50 / 100 | — |
| 7 | *The Nether Bounty: Wither Skeletons* | `minecraft:wither_skeleton` | 5 / 10 / 50 / 100 | — |
| 8 | *The End Bounty: Endermen* | `minecraft:enderman` | 5 / 10 / 50 / 100 | *Overhauled Endermen* (18 mobs) |

Every ladder shares the same reward shape. Read the per-ladder tables below for the items;
the pattern is:

| Rung | Pays |
|---|---|
| 5 kills | one ladder item ×5, + 10 XP |
| 10 kills | 25 XP **+ one `common` loot-crate roll** |
| 50 kills | a larger item bundle (with `random_bonus` on some entries), + 50 XP **+ one `uncommon` loot-crate roll** |
| 100 kills | 100 XP **+ one `rare` loot-crate roll** |
| side quest | ladder-specific items, + 100 XP (no roll) |

### 1. Overworld Bounty: Zombies — `minecraft:zombie`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *Overworld Bounty: Zombies* | kill 5 zombies | `minecraft:rotten_flesh` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:rotten_flesh` ×20, `minecraft:iron_ingot` ×10 (+ `random_bonus` 10) + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |
| side | *Zombie Variants* | kill 1 husk, 1 drowned, 1 `variantsandventures:gelid`, 1 `variantsandventures:thicket` | `minecraft:trident` + 100 XP |

The variants quest's own text names the spawn areas of the mod's zombies — *quest text*:
*"Husks- spawn in Deserts. Drowned- spawn Underwater. Gelid- spawn in Cold Biomes.
Thickets- spawn in Jungles."*

### 2. Overworld Bounty: Skeletons — `minecraft:skeleton`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *Overworld Bounty: Skeletons* | kill 5 skeletons | `minecraft:bone` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:bone` ×20, `minecraft:arrow` ×10 (+ `random_bonus` 10) + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |
| side | *Skeleton Variants* | kill 1 stray, 1 bogged, 1 `variantsandventures:murk`, 1 `variantsandventures:verdant` | `mysticalagriculture:inferium_bow`, + 100 XP |

*Quest text* on the variants: *"Strays- spawn in Cold Biomes. Bogged- spawn in Swamps and
Trial Chambers. Murks- spawn underwater in Coral Reefs. Verdants- spawn in Jungles."*

### 3. Overworld Bounty: Creepers — `minecraft:creeper`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *Overworld Bounty: Creepers* | kill 5 creepers | `minecraft:gunpowder` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:gunpowder` ×20 + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |
| side | *Overhauled Creepers* | kill one of each of Creeper Overhaul's 16 creepers — see the id list below | `creeperoverhaul:cave_creeper_spawn_egg`, `minecraft:gunpowder` ×64, `biomeswevegone:mini_cactus`, + 100 XP |

This is the chapter's longest checklist side quest: sixteen entity ids, one kill each, all in
one quest entry. The config's own ids, in the order it lists them (Creeper Overhaul 4.0.6):

- `creeperoverhaul:badlands_creeper`, `creeperoverhaul:dripstone_creeper`,
  `creeperoverhaul:spruce_creeper`, `creeperoverhaul:swamp_creeper`
- `creeperoverhaul:cave_creeper`, `creeperoverhaul:birch_creeper`,
  `creeperoverhaul:ocean_creeper`, `creeperoverhaul:jungle_creeper`
- `creeperoverhaul:desert_creeper`, `creeperoverhaul:dark_oak_creeper`,
  `creeperoverhaul:bamboo_creeper`, `creeperoverhaul:beach_creeper`
- `creeperoverhaul:savannah_creeper`, `creeperoverhaul:hills_creeper`,
  `creeperoverhaul:mushroom_creeper`, `creeperoverhaul:snowy_creeper`

### 4. Overworld Bounty: Spiders — `minecraft:spider`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *Overworld Bounty: Spiders* | kill 5 spiders | `minecraft:spider_eye` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:string` ×10 (+ `random_bonus` 10), `minecraft:spider_eye` ×20 + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |

### 5. Overworld Bounty: Witches — `minecraft:witch`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *Overworld Bounty: Witches* | kill 5 witches | `minecraft:glass_bottle` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:redstone` ×10, `minecraft:sugar` ×10, `minecraft:glowstone_dust` ×10 (each with `random_bonus` 10) + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |

### 6. The Nether Bounty: Blazes — `minecraft:blaze`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *The Nether Bounty: Blazes* | kill 5 blazes | `minecraft:blaze_rod` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:blaze_rod` ×10 (+ `random_bonus` 10) + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |

### 7. The Nether Bounty: Wither Skeletons — `minecraft:wither_skeleton`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *The Nether Bounty: Wither Skeletons* | kill 5 wither skeletons | `minecraft:coal` ×5, `minecraft:wither_skeleton_skull` ×1 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:wither_skeleton_skull` ×3, `minecraft:coal` ×30 + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |

Skulls are this ladder's theme: it is the only ladder that pays
`minecraft:wither_skeleton_skull`, ×1 at the 5-kill rung and ×3 at the 50-kill rung.

### 8. The End Bounty: Endermen — `minecraft:enderman`

| Rung | Title in the book | Asks | Pays (config) |
|---|---|---|---|
| 5 | *The End Bounty: Endermen* | kill 5 endermen | `minecraft:ender_pearl` ×5 + 10 XP |
| 10 | *(no title in the config)* | kill 10 | 25 XP + `common` roll |
| 50 | *(no title in the config)* | kill 50 | `minecraft:ender_pearl` ×8 (+ `random_bonus` 8) + 50 XP + `uncommon` roll |
| 100 | *(no title in the config)* | kill 100 | 100 XP + `rare` roll |
| side | *Overhauled Endermen* | kill one of each of Enderman Overhaul's 18 endermen — see the id list below | `endermanoverhaul:cave_enderman_spawn_egg`, `minecraft:ender_pearl` ×16, `endermanoverhaul:soul_pearl` ×8, + 100 XP |

The config's own ids, in the order it lists them (Enderman Overhaul 2.0.3):

- `endermanoverhaul:mushroom_fields_enderman`, `endermanoverhaul:swamp_enderman`,
  `endermanoverhaul:badlands_enderman`, `endermanoverhaul:end_islands_enderman`
- `endermanoverhaul:cave_enderman`, `endermanoverhaul:snowy_enderman`,
  `endermanoverhaul:ice_spikes_enderman`, `endermanoverhaul:savanna_enderman`
- `endermanoverhaul:crimson_forest_enderman`, `endermanoverhaul:windswept_hills_enderman`,
  `endermanoverhaul:nether_wastes_enderman`, `endermanoverhaul:desert_enderman`
- `endermanoverhaul:coral_enderman`, `endermanoverhaul:dark_oak_enderman`,
  `endermanoverhaul:soulsand_valley_enderman`, `endermanoverhaul:flower_fields_enderman`
- `endermanoverhaul:warped_forest_enderman`, `endermanoverhaul:end_enderman`

## The twelve boss and miniboss bounties (12 quests)

Each of these hangs off the middle of the canvas, has **no dependencies**, and asks for a
single kill (the Trader bounty, three), so all twelve can be taken at any time — in
practice the pack's progression decides when the player is ready. None of them chains:
each is a one-off, with no follow-up rung.

Most double up with a kill or loot quest elsewhere in the book — the Wither and the Warden
in Chapter 1, the Lunar Monstrosity and Starlight Golem in Eternal Starlight, the Forgotten
Guardian and Rotbeast in The Undergarden — while `references/boss-checklist.md` records the
Ender Dragon kill (Chapter 1 tracks the egg advancement instead) and the Elder Guardian,
Ravager, Piglin Brute, and Wilden Chimera kills as live here. That page also maps where
each boss lives and roughly when to fight it. One config flag worth knowing: the Trader
bounty is the only *visible* quest marked `optional: true` (the invisible authoring quest
below carries the flag too).

| Verified quest title | Kill task (config) | Pays (config) |
|---|---|---|
| *Kill The Ender Dragon* | `minecraft:ender_dragon` ×1 | 500 XP + two `uncommon` rolls |
| *Kill The Wither* | `minecraft:wither` ×1 | 500 XP + two `uncommon` rolls |
| *Kill The Warden* | `minecraft:warden` ×1 | 500 XP + two `uncommon` rolls |
| *Kill The Lunar Monstrosity* | `eternal_starlight:lunar_monstrosity` ×1 | 500 XP + two `uncommon` rolls |
| *Kill The Starlight Golem* | `eternal_starlight:starlight_golem` ×1 | 500 XP + two `uncommon` rolls |
| *Kill The Wilden Chimera* | `ars_nouveau:wilden_boss` ×1 | 500 XP + two `uncommon` rolls |
| *Kill The Forgotten Guardian* | `undergarden:forgotten_guardian` ×1 | 500 XP + two `uncommon` rolls |
| *Kill A Elder Guardian* | `minecraft:elder_guardian` ×1 | 250 XP + one `uncommon` roll |
| *Kill A Ravager* | `minecraft:ravager` ×1 | 250 XP + one `uncommon` roll |
| *Kill A Piglin Brute* | `minecraft:piglin_brute` ×1 | 250 XP + one `uncommon` roll |
| *Kill A Rotbeast* | `undergarden:rotbeast` ×1 | 250 XP + one `uncommon` roll |
| *Kill The Trader Villager and His Annoying Llamas* | `minecraft:wandering_trader` ×1 **and** `minecraft:trader_llama` ×2 | the *Sword of AlfredGG* (`minecraft:iron_sword` with that custom name and lore in the config) + 100 XP |

Two notes a player will ask about:

- **The Ender Dragon's kill quest is here, not in Chapter 1.** Chapter 1's *The End* is
  the `minecraft:end/dragon_egg` advancement (the egg after the fight); the Bounty Board
  carries the `kill minecraft:ender_dragon` task. That mismatch is the pack's, and it is
  why a book can show the End "done" without a dragon kill quest completed.
- **Which ones the pack itself calls minibosses.** Four of the descriptions say so in
  their own words — the Elder Guardian (*"I consider him a Miniboss"*), the Ravager
  (*"The Ravager is a Miniboss that only spawns in harder Raids"*), the Piglin Brute
  (*"I consider them Minibosses"*), and the Rotbeast (*"Rotbeasts are Minibosses that spawn
  all over the Undergarden"*). Those are quest text, quoted; the rest of the titles above
  are the config's as written, typos included.

## The hub and one authoring leftover (2 quests)

- ***Bounty Board*** (subtitle *Killing All The Things*) — the chapter's hub, drawn
  larger than the rest (`size: 2.0`), with no dependencies and one `advancement` task:
  `minecraft:adventure/kill_a_mob` (vanilla's "Monster Hunter"). It pays 10 XP. Its
  description, quoted: *"Here you'll find all of the rewards you can get by slaying
  enemies."* The task is vanilla's own *Monster Hunter* advancement, so it completes with
  a hostile-mob kill — which mobs count is vanilla's rule, so let the book confirm it in
  play. The hub's job is to introduce the board.
- **The invisible authoring quest** *(no title in the config)* — one quest is
  `invisible: true` and `optional: true`, with two `checkmark` tasks both titled
  `AllRightsReserved` and no rewards. Its description is the pack's authoring notice and
  ends: *"This quest is intentionally hidden, if you're seeing this, you're in editing
  mode."* It is never visible in a normal playthrough, so **49 of the 50 quests are
  playable** — this page lists it because the count of 50 in the config includes it.

## Rewards and claiming them

- **The board pays in loot crates.** 42 reward entries across the chapter are `random`
  rolls into named tables: the 10-kill rungs roll **`common`**, the 50-kill rungs and most
  boss bounties roll **`uncommon`**, and the 100-kill rungs roll **`rare`** (each table's
  `loot_size` is 1 — one entry per roll). What each table contains is the book's and JEI's
  business, not this page's — deliberately not listed below.
- **Claim the rolls in the quest entry.** Every one of those 42 roll entries carries
  `exclude_from_claim_all: true` in the config — FTB's flag for a reward the book's
  *Claim All* button skips (that reading of the flag is this page's, so confirm in-game).
  The 32 item rewards are *not* excluded. Practical instruction for a player using Claim
  All: open each bounty and claim the crate roll — otherwise it sits there.
- **XP is the other half.** 49 quests pay XP, 6,490 XP across the chapter in the config's
  own numbers. The 500-XP bounties are the seven major fights; the 250-XP ones are the
  four minibosses; the ladders pay 10 / 25 / 50 / 100 by rung.
- **The 5-kill rungs are the cheapest XP on the board** (10 XP each, the same as the hub)
  and the only rungs with no loot-crate roll; the rolls start at rung two, and the material
  bundles at rung three.

## Cross-references

- `references/boss-checklist.md` — the same twelve bosses as chapters 1/Exploration
  quests: dimensions, arenas, the quest text's hearts figures, and roughly when to fight
  each one. Read it before promising a player he is ready for a bounty.
- `references/progression.md` — where the Bounty Board sits in the four-stage map (it is
  tagged `early-game`) and how the standalone chapters relate to the Main Questline.
- `references/getting-started.md` — the board described as a low-pressure way to gear up
  while doing other things, from the same config.
- `references/atm-star-checklist.md` / `references/creative-checklist.md` — the endgame
  checklists. **Nothing on the Bounty Board feeds the ATM Star**: every task here is a
  kill task or the hub's advancement, and Chapter 3's star components are item tasks, so
  no bounty appears there and none should be promised as progress toward the star.

## What this page deliberately does not tell you

- **Where each mob spawns and how to farm it.** The quest descriptions give a hint or two
  (quoted above where they do); biomes, spawn rates, and farm designs are version- and
  world-sensitive and belong to the quest entry, the mod's own guide book, and JEI. The
  *Overhauled Creepers* / *Overhauled Endermen* entries, with 16 and 18 entity ids, are
  exactly where a player should read the quest text rather than hunt from memory.
- **Fight mechanics, hearts, drop tables.** `references/boss-checklist.md` quotes what the
  pack's own text says about the boss bounties; the fights themselves are the quest entry's
  and the mod's guide book's business.
- **What the loot crates contain.** The three tables are named and their roll size is
  quoted; their contents change between versions and are in the book.
- **An order the book does not impose.** The ladders chain rung by rung, but the eight
  ladders and the twelve boss bounties are mutually independent — "finish the Bounty
  Board in order" is not a thing the config says.
- **Anything not in the config.** If a player names a bounty, a mob, or a reward that is
  not listed here, the answer is "open that quest in the book / look it up in JEI" — never
  a guess.
