# Bounty Board — the 50-quest bounty checklist (verified titles)

**What this page is.** The tick-off map for **All the Mods 10**'s standalone **Bounty
Board** chapter: every bounty the chapter asks for, what each one wants killed and how
many, and what it pays — so a player can work the lines while playing and claim the
rewards that are easy to leave sitting in the book. It answers "which bounties are open
to me, what do they want, and what did I forget to claim?" and nothing more. It is a
*map of the chapter*, not a combat guide.

## Provenance — everything here was read, not remembered

Every quest title, entity id, kill count, dependency, reward, and quoted sentence below
comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/bounty_board.snbt` | the chapter's 50 quests, their kill tasks and required counts, dependency links, shapes, and reward tables |
| `config/ftbquests/quests/lang/en_us/chapters/bounty_board.snbt` | the English quest titles, subtitles, description text quoted below, and the named kill-task titles |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapter's own title, **Bounty Board** |
| `config/ftbquests/quests/reward_tables/common.snbt`, `config/ftbquests/quests/reward_tables/uncommon.snbt`, `config/ftbquests/quests/reward_tables/rare.snbt` with `config/ftbquests/quests/lang/en_us/reward_table.snbt` | the three random-reward tables the bounties roll on — **Reward: Common**, **Reward: Uncommon**, **Reward: Rare** (one roll each; contents deliberately not listed here) |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |

The book names this chapter **Bounty Board**, icon `minecraft:zombie_head`, with no
quest-book group (`group: ""` — a standalone chapter, shown outside the groups),
`order_index` 1, `progression_mode: "flexible"`. The skill tracks it as `bounty_board`,
stage `early-game`, second in the shipped chapter list after Welcome. There is **no
"Chapter 5" in this snapshot**: the numbered chapters are the Main Questline spine —
Chapter 1: The Beginning, Chapter 2: Allthemodium, Chapter 3: The ATM Star, Chapter 4:
Creative — and the Bounty Board is not one of them. If a player's book labels chapters
differently, his book wins (see Grounding rules).

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Entity ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the kill task's required `value`); a bounty
  with no printed count wants exactly what its task line says.
- **There are no collect quests in this chapter.** All 50 quests carry only `kill`
  tasks (87 of them), one `advancement` task, and two `checkmark` tasks — zero `item`
  tasks. Never turn a bounty into "bring me X items", and never present a mob's *drops*
  as a quest requirement: drops are JEI's answer, on the mob.
- **No recipes, no tactics, no drop tables, no loot pools.** The config lists *what a
  quest wants*, never *how to fight it*. The three random reward tables are named, not
  opened: their weighted contents are long, version-sensitive, and shown in-game on the
  quest itself. Quoted "Hearts" figures are the quest author's, marked *quest text*.
- **Approximate means approximate.** Which biome a variant spawns in, which farm or
  spawner setup fills a 100-kill line fastest, and any `random_bonus` on a fixed reward
  are version- and world-sensitive; anything not quoted from the config is flagged as
  approximate. A few fixed rewards carry the config's `random_bonus`, so a claimed count
  can come out higher than the base count printed here — the quest entry shows the roll.
- **Titles are the config's.** 25 of the 50 quests carry an explicit title in the lang
  file (Minecraft `&` formatting codes stripped, as elsewhere in this skill). The other
  25 are marked *(no title in the config)* — the book then shows the task's own icon or
  name. Do not present a derived name (including this page's "tier" labels) as a verified
  title.
- **Nothing here was invented, and nothing is added from memory.** A bounty that is not
  on this page is not in this chapter: the answer is "open that quest in the book / look
  it up in JEI", never a plausible-sounding guess.

## How the chapter is shaped

One hub, eight repeating lines, four variant hunts, and a ring of one-off kills:

| | |
|---|---|
| Quests in the chapter | **50** |
| Tasks in total | 90 (87 `kill`, one `advancement`, two `checkmark`) |
| Quests carrying an explicit title in the config | 25 (the other 25 are marked below) |
| Repeating bounty lines | 8 lines × 4 quests = **32** (5×/10×/50×/100× kills) |
| Variant hunts | **4** quests, 42 single kills between them |
| Single-kill bounties | **12** quests (11 one-kill quests + the two-kill trader quest) |
| Hub + hidden config quest | **2** (only the hub is playable; see below) |

The book lays a chapter out on a **canvas, not as a numbered list**, and this chapter
adds `progression_mode: "flexible"` — nothing here is a sequence the pack enforces. The
only order on this page is the config's own `dependencies`: each bounty line is a strict
chain (a tier appears after the tier before it), each variant hunt hangs off its line's
first tier, and the hub, the boss bounties, and the first tier of every line have **no
dependencies at all** — they are visible from the start. This page's *tier 1–4* labels
are its own shorthand for that chain (ascending canvas positions, ascending counts
5 → 10 → 50 → 100, the 100-kill quest drawn as a larger pentagon in the config); the
book itself does not number them.

Read it as three working lists:

1. **The eight bounty lines** — the bulk of the chapter and the easiest rewards to
   strand: finish a line while farming that mob anyway, and claim each tier.
2. **The four variant hunts** — one quest each, many one-off kills, unlocked by the
   matching line's first tier.
3. **The twelve single-kill bounties** — bosses and minibosses, most of them duplicates
   of kills tracked elsewhere (see `references/boss-checklist.md`); do the fight once,
   claim in both places.

## The hub and the hidden quest (2 quests)

- [ ] **Bounty Board** — task `advancement minecraft:adventure/kill_a_mob` (kill any
  mob). The chapter hub, subtitled *Killing All The Things*; its own text: *"Here you'll
  find all of the rewards you can get by slaying enemies."* Pays 10 XP. No dependencies.

The 50th quest is **not playable**: *(no title in the config)* — two `checkmark` tasks
(both titled *AllRightsReserved* in the lang file), flagged `invisible: true` and
`optional: true` in the chapter config. Its description is the pack's licensing notice
(*"This quest is intentionally hidden, if you're seeing this, you're in editing
mode."*). It is listed here only so the count reconciles — 50 in the config, 49 a
player can see and tick off. Do not send a player hunting for it.

## The eight bounty lines (32 quests)

Each line is one mob at 5, then 10, then 50, then 100 kills, chained by dependencies.
The titled first tier names the line; tiers 2–4 carry no title in the config. Fixed item
rewards and XP are quoted from the config; every tier from the second up also rolls one
random reward table, and every one of those random rewards is flagged
`exclude_from_claim_all: true` in the config — see *Claiming the rewards* below before
assuming Claim All collected them.

### Overworld lines

#### Zombies — `minecraft:zombie`

- [ ] **Overworld Bounty: Zombies** — kill `minecraft:zombie` ×5 — pays
  `minecraft:rotten_flesh` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:zombie` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:zombie` ×50 — pays
  `minecraft:rotten_flesh` ×20, `minecraft:iron_ingot` ×10, 1 × **Reward: Uncommon**,
  50 XP
- [ ] *(no title in the config)* — kill `minecraft:zombie` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

#### Skeletons — `minecraft:skeleton`

- [ ] **Overworld Bounty: Skeletons** — kill `minecraft:skeleton` ×5 — pays
  `minecraft:bone` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:skeleton` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:skeleton` ×50 — pays
  `minecraft:bone` ×20, `minecraft:arrow` ×10, 1 × **Reward: Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:skeleton` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

#### Creepers — `minecraft:creeper`

- [ ] **Overworld Bounty: Creepers** — kill `minecraft:creeper` ×5 — pays
  `minecraft:gunpowder` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:creeper` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:creeper` ×50 — pays
  `minecraft:gunpowder` ×20, 1 × **Reward: Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:creeper` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

#### Spiders — `minecraft:spider`

- [ ] **Overworld Bounty: Spiders** — kill `minecraft:spider` ×5 — pays
  `minecraft:spider_eye` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:spider` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:spider` ×50 — pays
  `minecraft:string` ×10, `minecraft:spider_eye` ×20, 1 × **Reward: Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:spider` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

#### Witches — `minecraft:witch`

- [ ] **Overworld Bounty: Witches** — kill `minecraft:witch` ×5 — pays
  `minecraft:glass_bottle` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:witch` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:witch` ×50 — pays
  `minecraft:redstone` ×10, `minecraft:sugar` ×10, `minecraft:glowstone_dust` ×10,
  1 × **Reward: Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:witch` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

### Nether lines

#### Blazes — `minecraft:blaze`

- [ ] **The Nether Bounty: Blazes** — kill `minecraft:blaze` ×5 — pays
  `minecraft:blaze_rod` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:blaze` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:blaze` ×50 — pays
  `minecraft:blaze_rod` ×10, 1 × **Reward: Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:blaze` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

#### Wither Skeletons — `minecraft:wither_skeleton`

- [ ] **The Nether Bounty: Wither Skeletons** — kill `minecraft:wither_skeleton` ×5 —
  pays `minecraft:coal` ×5, `minecraft:wither_skeleton_skull`, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:wither_skeleton` ×10 — pays
  1 × **Reward: Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:wither_skeleton` ×50 — pays
  `minecraft:wither_skeleton_skull` ×3, `minecraft:coal` ×30, 1 × **Reward:
  Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:wither_skeleton` ×100 — pays
  1 × **Reward: Rare**, 100 XP

### The End line

#### Endermen — `minecraft:enderman`

- [ ] **The End Bounty: Endermen** — kill `minecraft:enderman` ×5 — pays
  `minecraft:ender_pearl` ×5, 10 XP
- [ ] *(no title in the config)* — kill `minecraft:enderman` ×10 — pays 1 × **Reward:
  Common**, 25 XP
- [ ] *(no title in the config)* — kill `minecraft:enderman` ×50 — pays
  `minecraft:ender_pearl` ×8, 1 × **Reward: Uncommon**, 50 XP
- [ ] *(no title in the config)* — kill `minecraft:enderman` ×100 — pays 1 × **Reward:
  Rare**, 100 XP

## The four variant hunts (4 quests, 42 kills)

Each of these hangs off its line's first (5-kill) tier with `hide_until_deps_complete`,
so it appears only once that tier is done. Each task in the quest wants exactly one
kill; the quest completes when every listed variant is dead once. Spawn hints below are
quoted from the quest descriptions — where a variant actually spawns in the player's
version is approximate; the quest entry and JEI win.

- [ ] **Zombie Variants** (needs *Overworld Bounty: Zombies*) — kill
  `minecraft:husk` ×1, `minecraft:drowned` ×1, `variantsandventures:gelid` ×1,
  `variantsandventures:thicket` ×1 — pays `minecraft:trident`, 100 XP. Quest text:
  *"Husks- spawn in Deserts. Drowned- spawn Underwater. Gelid- spawn in Cold Biomes.
  Thickets- spawn in Jungles."* The two non-vanilla entities are Variants&Ventures
  1.0.26 (`variantsandventures`).
- [ ] **Skeleton Variants** (needs *Overworld Bounty: Skeletons*) — kill
  `minecraft:stray` ×1, `minecraft:bogged` ×1, `variantsandventures:murk` ×1,
  `variantsandventures:verdant` ×1 — pays `mysticalagriculture:inferium_bow`
  (Mystical Agriculture 8.0.28), 100 XP. Quest text: *"Strays- spawn in Cold Biomes.
  Bogged- spawn in Swamps and Trial Chambers. Murks- spawn underwater in Coral Reefs.
  Verdants- spawn in Jungles."*
- [ ] **Overhauled Creepers** (needs *Overworld Bounty: Creepers*) — kill one each of
  the 16 Creeper Overhaul 4.0.6 (`creeperoverhaul`) creepers:
  `creeperoverhaul:badlands_creeper`, `creeperoverhaul:dripstone_creeper`,
  `creeperoverhaul:spruce_creeper`, `creeperoverhaul:swamp_creeper`,
  `creeperoverhaul:cave_creeper`, `creeperoverhaul:birch_creeper`,
  `creeperoverhaul:ocean_creeper`, `creeperoverhaul:jungle_creeper`,
  `creeperoverhaul:desert_creeper`, `creeperoverhaul:dark_oak_creeper`,
  `creeperoverhaul:bamboo_creeper`, `creeperoverhaul:beach_creeper`,
  `creeperoverhaul:savannah_creeper`, `creeperoverhaul:hills_creeper`,
  `creeperoverhaul:mushroom_creeper`, `creeperoverhaul:snowy_creeper` — pays
  `creeperoverhaul:cave_creeper_spawn_egg`, `minecraft:gunpowder` ×64,
  `biomeswevegone:mini_cactus` (Oh The Biomes We've Gone 2.6.0), 100 XP. Quest text:
  *"Each have different drops and even some are friendly! All are afraid of cats
  though..."*
- [ ] **Overhauled Endermen** (needs *The End Bounty: Endermen*) — kill one each of the
  18 Enderman Overhaul 2.0.3 (`endermanoverhaul`) endermen:
  `endermanoverhaul:mushroom_fields_enderman`, `endermanoverhaul:swamp_enderman`,
  `endermanoverhaul:badlands_enderman`, `endermanoverhaul:end_islands_enderman`,
  `endermanoverhaul:cave_enderman`, `endermanoverhaul:snowy_enderman`,
  `endermanoverhaul:ice_spikes_enderman`, `endermanoverhaul:savanna_enderman`,
  `endermanoverhaul:crimson_forest_enderman`, `endermanoverhaul:windswept_hills_enderman`,
  `endermanoverhaul:nether_wastes_enderman`, `endermanoverhaul:desert_enderman`,
  `endermanoverhaul:coral_enderman`, `endermanoverhaul:dark_oak_enderman`,
  `endermanoverhaul:soulsand_valley_enderman`, `endermanoverhaul:flower_fields_enderman`,
  `endermanoverhaul:warped_forest_enderman`, `endermanoverhaul:end_enderman` — pays
  `endermanoverhaul:cave_enderman_spawn_egg`, `minecraft:ender_pearl` ×16,
  `endermanoverhaul:soul_pearl` ×8, 100 XP.

## The twelve single-kill bounties (12 quests)

None of these has a dependency; all are drawn larger in the config (`size: 1.5`) and all
pay only XP plus random-table rolls — one **Reward: Uncommon** at 250 XP, two at
500 XP. "Quest text" quotes are that bounty description's own words, including its
Hearts figures; the fight itself is `references/boss-checklist.md` and the mod's own
guide, not this page.

### Vanilla bosses and minibosses

- [ ] **Kill The Ender Dragon** — kill `minecraft:ender_dragon` ×1 — pays
  2 × **Reward: Uncommon**, 500 XP. Quest text: *"She has 200 Hearts"* (quest text) and
  the End Crystals heal her. This is the book's dragon *kill* quest — Chapter 1 tracks
  the egg advancement instead.
- [ ] **Kill The Wither** — kill `minecraft:wither` ×1 — pays 2 × **Reward: Uncommon**,
  500 XP. Quest text gives the T-shape summon (4 Soul Sand, 3 Wither Skeleton Skulls)
  and *"He has 300 Hearts"* (quest text).
- [ ] **Kill The Warden** — kill `minecraft:warden` ×1 — pays 2 × **Reward: Uncommon**,
  500 XP. Quest text: *"with 500 Hearts and over 20 Hearts damage with his attacks"*
  (quest text), spawned via Sculk Shriekers.
- [ ] **Kill A Elder Guardian** *(spelled that way in the config)* — kill
  `minecraft:elder_guardian` ×1 — pays 1 × **Reward: Uncommon**, 250 XP. Quest text:
  *"Three of them spawn there"* (Ocean Monuments) and *"They have 80 Hearts"* (quest
  text).
- [ ] **Kill A Ravager** — kill `minecraft:ravager` ×1 — pays 1 × **Reward: Uncommon**,
  250 XP. Quest text ties it to Raids (Bad Omen, then a Village).
- [ ] **Kill A Piglin Brute** — kill `minecraft:piglin_brute` ×1 — pays
  1 × **Reward: Uncommon**, 250 XP. Quest text: Bastions, *"They have 50 Hearts"*
  (quest text), *"They drop nothing"* — the bounty is the reward, not the corpse.
- [ ] **Kill The Trader Villager and His Annoying Llamas** — subtitle *"This is
  Personal" - AlfredGG*, flagged `optional: true` — kill
  `minecraft:wandering_trader` ×1 and `minecraft:trader_llama` ×2 (the lang file names
  the tasks *Kill 1 Wandering Trader* and *Kill 2 Trader Llamas*) — pays an iron sword
  the config names *Sword of AlfredGG* (`minecraft:iron_sword` with that custom name),
  100 XP. The joke bounty; nothing else gates on it.

### Modded bosses and minibosses

- [ ] **Kill The Wilden Chimera** — kill `ars_nouveau:wilden_boss` ×1 (Ars Nouveau
  5.13.1) — pays 2 × **Reward: Uncommon**, 500 XP. Quest text: *"He needs to be
  summoned through a ritual then fought!"*
- [ ] **Kill The Lunar Monstrosity** — kill `eternal_starlight:lunar_monstrosity` ×1
  (Eternal Starlight 0.9.1) — pays 2 × **Reward: Uncommon**, 500 XP. Quest text:
  *"This one lives in the middle of the Cursed Garden"*.
- [ ] **Kill The Starlight Golem** — kill `eternal_starlight:starlight_golem` ×1 —
  pays 2 × **Reward: Uncommon**, 500 XP. Quest text: *"He is charging in the Golem
  Forge awaiting for a Player to come fight him!"*
- [ ] **Kill The Forgotten Guardian** — kill `undergarden:forgotten_guardian` ×1
  (The Undergarden 0.9.6) — pays 2 × **Reward: Uncommon**, 500 XP. Quest text: *"He
  rests in the Catacomb Structure."*
- [ ] **Kill A Rotbeast** — kill `undergarden:rotbeast` ×1 — pays 1 × **Reward:
  Uncommon**, 250 XP. Quest text: *"Rotbeasts are Minibosses that spawn all over the
  Undergarden."*

Seven of these kills are tracked a second time in their home chapters (the dragon's egg
advancement in Chapter 1, the Warden in Deeper and Darker, and so on) — which is why a
book can show the same boss done in one chapter and open in this one. Kill once, claim
in both places; `references/boss-checklist.md` maps each boss to its dimension and
arena.

## Claiming the rewards (the part players miss)

- **Every random reward in this chapter is excluded from Claim All.** The config flags
  each `random` reward `exclude_from_claim_all: true` — all three tiers of every line
  (Common at 10 kills, Uncommon at 50, Rare at 100) and every boss bounty's Uncommon
  roll(s). Quoted as config, not as a promise about the button's name in a future
  version: open each finished quest and claim it individually, or the roll stays in the
  book. Fixed item and XP rewards are not flagged that way.
- **The pattern is worth memorising:** first tier = that mob's thematic drop ×5 + 10 XP;
  second = Common + 25 XP; third = a larger fixed drop + Uncommon + 50 XP; fourth =
  Rare + 100 XP. Variant hunts pay one fixed item set + 100 XP and no table roll. The
  hub pays only its 10 XP.
- **One roll means one roll.** Each table's config states `loot_size: 1` — one item per
  claim, weighted. This page names the tables (**Reward: Common**,
  **Reward: Uncommon**, **Reward: Rare**) and stops there: their contents are shown on
  the quest in-game, and quoting a weighted pool here would go stale first.
- Claiming changes nothing about the kill counts: a tier counts kills whether or not
  the previous tier's reward was claimed, but the next tier only *appears* down the
  dependency chain (tiers 2–4 carry `hide_until_deps_visible`). If a line looks shorter
  than four quests, an earlier tier is unfinished — check the book.

## Cross-references

- `references/boss-checklist.md` — the same twelve single-kill bounties mapped as
  bosses: dimension, structure/arena, and roughly when to attempt them. This page is
  the claim list; that page is the where-and-when list.
- `references/progression.md` — where the standalone Bounty Board sits (early-game,
  alongside Welcome) in the four-stage map and the quest-book order.
- `references/getting-started.md` — the first-hours context: the Bounty Board as the
  low-pressure kill-count chapter to run alongside Chapter 1.

## What this page deliberately does not tell you

- **Collect or craft requirements.** There are none in this chapter (zero `item`
  tasks) — anything phrased as "collect X items" for a bounty is invented; the quest
  entry wins.
- **Fight tactics, gear checks, or arena walkthroughs.** One quoted sentence per boss
  at most, attributed to the quest text; the fight is the quest entry, the mod's guide
  book, and `references/boss-checklist.md`.
- **Drop tables.** What a mob drops (including the descriptions' own "On death they
  will drop" lists, beyond the quotes above) is JEI, in-game, on the mob — not a quest
  requirement and not this page's list.
- **Reward-table contents.** The three tables are named and their roll counts quoted;
  their weighted item pools are deliberately not reproduced.
- **An order the book does not have.** `flexible` progression, one hub, eight chains,
  four hunts, twelve standalones: beyond the verified dependency links, any "do this
  line first" advice is approximate — offered as farming convenience, never as a gate.
- **Anything not in the config.** If a player names a bounty, a variant, or a count
  that is not listed here, the answer is "open that quest in the book / look it up in
  JEI" — never a guess.
