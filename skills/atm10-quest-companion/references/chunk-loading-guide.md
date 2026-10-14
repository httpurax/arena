# Chunk loading: how to keep a farm running while you're away

**What this page is.** The answer to the beginner question *"how do I keep my farm running
while I'm away?"* in **All the Mods 10** — the mechanics the pack actually ships for
keeping chunks ticking with no player in them: FTB Chunks' claimed-chunk force-loading,
the chunk-loader blocks and upgrades the pack's own configs enable or disable, and the two
spawner runes the quest book offers as an alternative. It is a map of *what the pack
provides and where it is documented*, not a farm-design guide and not a chunk-loader
crafting guide.

## Provenance — everything here was read, not remembered

Every quest title, quest id, task item id, config key, config value, changelog line, and
quoted sentence below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which the pack's own changelogs list as **pack 8.2**
(`config/bcc-common.toml` → `modpackVersion = "8.2"`) — the "8.x" stamp in
`examples/progress.example.json`:

| File(s) in the pack repo (at that commit) | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/welcome.snbt` | the *Claiming Chunks* quest: its id, task id, task type, reward, and its `ftbchunks:` custom icon |
| `config/ftbquests/quests/lang/en_us/chapters/welcome.snbt` | the task title `Claiming Chunks` and the claim/force-load instructions quoted below |
| `config/ftbquests/quests/chapters/applied_energistics_2.snbt`, `apotheosis_2.snbt`, `draconic_evolution.snbt`, `pylons.snbt`, `productive_bees.snbt` | the other quests that touch chunk loading: task items, counts, `optional` flags, and `dependencies` chains |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles and the description text quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` and `chapter_group.snbt`, with `config/ftbquests/quests/chapter_groups.snbt` | chapter titles, the quest-book group each chapter sits in, and the group order |
| `config/crash_assistant/modlist.json` | verified mod ids, display names, and versions (493 entries) |
| `config/Mekanism/general.toml`, `config/ae2-common.toml`, `config/pneumaticcraft-common.toml`, `config/pylons-server.toml`, `config/quarryplus.toml`, `config/mahoutsukai-server.toml`, `config/iceandfire/iaf-common.json`, `config/fluxnetworks-server.toml`, `config/hyperbox-common.toml`, `config/crashutilities-server.toml` | the chunk-loading switches the pack ships, with each key's own comment text |
| `kubejs/assets/emi/index/stacks/removals.json` | the three chunk-loading items the pack hides from the EMI index |
| `kubejs/server_scripts/Tweaks/tags.js` | the pack's own `ftbchunks:interact_whitelist` block-tag tweak |
| `kubejs/assets/<modid>/lang/{pt_br,ru_ru}.json` | the only place four chunk-loader ids appear anywhere in the repo — see the warning below |
| `changelogs/CHANGELOG-ATM10-2.31-2.32.md`, `CHANGELOG-ATM10-4.15-5.0.md`, `CHANGELOG-ATM10-8.1-8.2.md` | the pack's own record of disabling Flux Networks chunk loading, removing Modular Machinery Reborn, and the FTB Chunks version bump to 2101.1.22 |
| `MOD_ISSUES.md` | where the pack tells you to report an FTB Chunks bug |

**How to read the quotes.** Quest text is quoted with Minecraft `&` formatting codes
stripped (`&6M&r` → `M`), the same normalization `scripts/build_chapter_list.py` applies
to titles. Config comments and values are quoted verbatim.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests), the FTB Chunks map screen, and JEI/EMI are
  authoritative.** This page is a snapshot of pack 8.2's config. Chunk loading is exactly
  the kind of thing a server owner, a rank setup, or a pack update changes; if the
  player's game differs, his game wins — say so and re-check rather than arguing from
  this file.
- **No claim or force-load limit is quoted anywhere on this page, on purpose.** The pack
  repository ships **no FTB Chunks config file at all** at this commit (the only FTB
  configs under `config/` are `ftbquests/` and `ftbultimine-server.snbt`), so how many
  chunks a player may claim or force-load is *not stated in the repo*. FTB Ranks 2101.1.5
  and FTB Teams 2101.1.11 are in the mod list, and both are the usual home of such limits
  — but a number recited here would be invented. Read the limit off the player's own
  claim screen and config. **Never invent a limit.**
- **Item and block ids are quoted from the config, never invented.** Where an id appears
  only in the pack's non-English localization overrides, that is flagged in place.
- **Non-English localization is evidence that an id exists, not of its English name.**
  Four chunk-loader ids below are found *only* in `kubejs/assets/<modid>/lang/pt_br.json`
  and `ru_ru.json` — community translations the pack bundles (the 8.1→8.2 changelog lists
  *"Updated PT_BR Localizations (#4389)"*). Those files prove the id is real in this pack
  and, in two cases, describe what it does. **The repo carries no `en_us` name for them**,
  so any English rendering on this page is a *translation of the shipped pt_br/ru_ru
  string*, marked as such — the real in-game name comes from the game and JEI.
- **Config keys prove a setting exists and what the mod's own comment says it does.** They
  do not prove a machine is worth building, or that a farm layout works. Anything on this
  page that is neither a quote nor a config value is flagged **judgement**.
- **No recipes, no farm layouts, no coordinates, no energy numbers.** The config lists
  *what a quest wants*, never *how to craft it*; JEI has the recipe, and recipes are where
  pack versions differ most.
- **Nothing here was invented, and nothing is added from memory.** A chunk loader that is
  not named in this pack's config is not on this page. If a player names one (an old
  guide's favourite, a mod that ATM10 dropped), the answer is "let's check your instance /
  JEI" — never a plausible-sounding guess.

## The short answer

**Claim the chunks your farm sits in, then force-load them.** That is the pack's own
instruction, from the first chapter of the quest book, and it needs no machine, no mod
progression, and no item:

1. Press **M** to open the map and click the **Claimed Chunks** icon in the top left.
2. **Left-click and drag** to claim the chunks the farm occupies.
3. **Shift-left-click** a claimed chunk to **force load** it — *"If done properly, you'll
   see lines across the chunk."*

Claiming alone is not enough: the pack's own Crash Utilities config makes the distinction
explicit when it says its purge option counts *"LOADED not Claimed Chunks"*. A claimed
chunk protects your builds; a **force-loaded** chunk is what keeps ticking while you are
somewhere else. Force-load only the chunks the farm actually needs — every extra loaded
chunk is tick work the server does forever (**judgement**).

Everything below is what to do when that is not enough, when it stops working, or when the
farm is a mob farm whose spawner has its own rules.

## Step 1 — FTB Chunks, taught by the Welcome chapter

The Welcome chapter (config filename `welcome`, chapter id `5B00676D79306EA2`, book title
**Welcome**, standalone — no quest-book group, `order_index: 0`, 6 quests) is the first
thing in the book, and one of its six quests is the chunk-claiming lesson. Verified from
`config/ftbquests/quests/chapters/welcome.snbt` and its `en_us` lang file:

| Field in the config | Value |
|---|---|
| Quest id | `0C93D7A607AB8B83` |
| Quest title key in `lang/en_us/chapters/welcome.snbt` | **absent** — the config gives this quest no `quest.<id>.title` |
| Task id / type | `103C42C743E2A2DB` / `checkmark` |
| **Task title (verified)** | **`Claiming Chunks`** (`task.103C42C743E2A2DB.title`) |
| Task payload | none — a `checkmark` task has no item |
| Reward | `xp` 10 |
| Quest icon | `ftbquests:custom_icon` with component `"ftbquests:icon": "ftbchunks:textures/waypoint_home.png"` |
| Dependencies | none |
| Size on the chapter canvas | `1.5` |

Because the config puts the title on the **task**, not the quest, this page calls it *the
**Claiming Chunks** quest* after that verified task title. How the book renders a quest
with no title of its own is the mod's business, not the repo's — read the label off the
player's own book and do not present a derived name as a verified quest title.

Its full description, quoted with `&` codes stripped:

> *"To claim chunks, open up your map using M, then click the Claimed Chunks icon in the top
> left.*
>
> *To claim a chunk, left click and drag to claim.*
>
> *To force load a chunk, shift-left click the chunk. If done properly, you'll see lines
> across the chunk."*

That is the entire force-loading tutorial the quest book contains. Note what it does *not*
say: no limit, no command, no cost. **Do not fill those gaps in.**

The chapter's five siblings, for orientation (verified task titles; the first quest is the
only one with an explicit quest title):

| Quest id | Title the config gives | Task |
|---|---|---|
| `3BC0A50886A3222B` | quest title `Welcome to All The Mods 10!` (`&d` in the config) | `dimension` → `minecraft:overworld` |
| `3708A4780ACEB34E` | *(no title in the config)*; task title `Quests` | `checkmark` |
| `7658C1C663394E85` | *(no title in the config)*; task title `Useful Commands` | `checkmark` |
| `0C93D7A607AB8B83` | *(no title in the config)*; task title **`Claiming Chunks`** | `checkmark` |
| `5AC1BE754210429E` | *(no title in the config)*; task title `Creating a Team` | `checkmark` |
| `49EDAA2F57D3BF1D` | *(no title in the config)*; two `AllRightsReserved` checkmark tasks | the pack's hidden authorship notice |

Two of those are directly relevant to a farm that has to survive the player leaving:

- **`Useful Commands`** — the pack's `/sethome` / `/home` / `/spawn` / `/rtp` lesson. Its
  text uses a farm as the worked example: *"/sethome (name of home) | Lets you set a home
  that you can teleport back to using /home (name). Example: /sethome farm - then teleport
  with /home farm."* It also names where FTB Essentials' per-world config lives —
  *"For Singleplayer | saves/(name of save)/serverconfig/ftbessentials.snbt"* and *"For
  Servers | world/serverconfig/ftbessentials.snbt"* — and warns *"These commands have
  cooldowns and limits."* Those paths are FTB Essentials'; whether FTB Chunks writes a
  per-world serverconfig the same way is **not verified in this repo** (approximate —
  check the player's own instance).
- **`Creating a Team`** — *"If you want to create a team for you and your friends, use the
  command /ftbteams party create (name of team) to create the team!"* On a shared world,
  claims belong to a team, so a team is how several players keep one farm loaded
  (**judgement** about the consequence; the command is quoted).

The mods behind all of this, from `config/crash_assistant/modlist.json`: **FTB Chunks
2101.1.22**, **FTB Teams 2101.1.11**, **FTB Ranks 2101.1.5**, **FTB Essentials
2101.1.10**, **FTB Library 2101.1.36**, **FTB Quests 2101.1.36**, plus **Journeymap
1.21.1-6.0.9**. The 8.1→8.2 changelog records the FTB Chunks bump
*"FTB Chunks (2101.1.21) -> (2101.1.22)"*. The quest text says only *"your map"* and does
not name a mod — do not attribute the **M** screen to one.

One pack-authored FTB Chunks tweak is in the repo, at
`kubejs/server_scripts/Tweaks/tags.js` line 6:

```js
allthemods.add('ftbchunks:interact_whitelist', ['@waystones'])
```

That adds every **Waystones** block (Waystones 21.1.45) to the `ftbchunks:interact_whitelist`
block tag. The tag name and its members are verified; what FTB Chunks does with that tag is
the mod's behaviour and is **not defined in this repo** — the obvious reading is that
waystones stay usable inside other players' claims (**judgement**; verify in-game).

## Step 2 — the one chunk-loading device the quest book actually tracks

Across all 66 chapters, exactly **one** quest has a chunk loader as its task item: the AE2
**Spatial Anchor**. Verified from `config/ftbquests/quests/chapters/applied_energistics_2.snbt`
(chapter id `07210DDF872160BA`, book title **Applied Energistics 2**, group **Storage**,
74 quests) and its `en_us` lang file:

| Field in the config | Value |
|---|---|
| Quest id | `2897FA291E5A38D8` |
| Title / subtitle in the lang file | **absent** — *(no title in the config)*; called *the Spatial Anchor quest* here, after its own text |
| Task | `item`, id `68A36AB341CC016D` → `ae2:spatial_anchor`, count **1** |
| `optional` | **true** |
| Dependency | `18DFB25DC48D8BF7` — also *(no title in the config)*; task `ae2:spatial_pylon` ×1 |
| Its dependency | `01F3F0C25BA72BDA` — verified title **`Spatial IO`**, task `ae2:spatial_io_port` ×1 |
| Rewards | one `random` reward-table draw (`table_id: 5871764666515020368`) + `xp` 100 |
| Position on the canvas | `x: 21.5`, `y: 5.5` |

Its description, quoted in full with `&` codes stripped:

> *"The Spatial Anchor is a companion device from the Spatial IO lineage that simply
> functions as a chunk loader. When connected to an ME network, the Anchor will force-load
> all the chunks occupied by the ME network across all cables and devices, excluding
> subnetworks, as long as the network remains powered."*

So the book's own answer for an AE2 player is: the anchor loads the chunks **the network
occupies** — cables and devices — **excluding subnetworks**, and only **while powered**.
That makes it a natural fit for a farm whose output already goes into the ME system
(**judgement**). Two AE2 config keys in `config/ae2-common.toml` are the pack's settings
for it, quoted verbatim:

- `spatialAnchorEnableRandomTicks = true` — *"#Whether Spatial Anchors should force random
  chunk ticks and entity spawning."*
- `chunkLoggerTrace = false` — *"#Enable stack trace logging for the chunk loading debug
  command"* (a debug switch, and evidence the mod has a chunk-loading debug command; the
  command's syntax is **not** in the repo).

**The pack hides this item from the EMI index.** `kubejs/assets/emi/index/stacks/removals.json`
lists, among its removals:

```
"item:ae2:spatial_anchor",
"item:mekanism:upgrade_anchor",
"item:mekanism:dimensional_stabilizer",
```

Those are the only three chunk-loading items on that list. The file is EMI's *index
removal* list, so what is verified is that these three are hidden from the item browser;
whether they remain craftable and functional is **not** stated by this file and is
**judgement** — the AE2 chapter still documents the Spatial Anchor and still asks for one
as a quest task, which is the strongest signal in the repo that it works. If a player says
*"I can't find the Spatial Anchor / Anchor Upgrade in EMI"*, this is why: send him to the
quest entry and to FTB Chunks instead of guessing at a recipe (**Applied Energistics 2
19.2.17**, **Mekanism 10.7.19**, both from the mod list).

## Step 3 — mob farms: the quest book's two spawner answers

A mob farm away from the player has two problems, and the pack's **Apothic Spawners**
chapter (config filename `apotheosis_2`, chapter id `0E81CBCD6B1D1895`, book title
**Apothic Spawners**, group **Resources**, 36 quests) addresses both. Neither is chunk
loading — one removes the player requirement from the spawner, the other stops the mobs
despawning.

**1. *Ignore Players* — verified quest title.** Quest `30EB438C66324213`, one `item` task
(`211FBEB0E4FF1FD6`) for `apotheosis:ignore_players_spawner_rune` ×1, reward `xp_levels` 5,
dependency `503AC506720FC59E`. Quoted with `&` codes stripped:

> *"A Rune of Solitude will do part what the Spawner Upgrade Runes do but much better.
> Players no longer need to be near the spawner. As long as its chunk-loaded it will
> spawn."*

Read the second sentence carefully: the rune removes the **player-proximity** requirement,
and then *still* asks for the chunk to be loaded. It is a partner for Step 1, not a
replacement for it (**judgement** about the pairing; both sentences are quoted).

Its place in the chapter, verified from the config's `dependencies` chains — the book lays
chapters out on a canvas, so this is a dependency order, not a numbered list:

| # | Quest id | Title the config gives | Task item |
|---|---|---|---|
| 1 | `310969B8FE0A94DE` | **`Apothic Spawners`** (the chapter hub) | `minecraft:spawner` ×1 |
| 2 | `321C15EBBE2D3D30` | **`Blowing up Spawners`** | `apotheosis:spawner_chain` ×1, `minecraft:tnt` ×1 |
| 3 | `17C87EB8ED8A27AB` | *(no title in the config)* | the basic rune quest; siblings titled **`Ignore Light`**, **`Youthful`**, **`Spawn Range`**, **`Redstone Active`**, **`Opposite Day`**, **`Health`**, **`Burning`** all hang off it |
| 4 | `503AC506720FC59E` | *(no title in the config)* | `apotheosis:infused_spawner_rune` ×1 — the infusion quest, whose text asks for *"at least 70 Eterna, 30% Quanta, and 50% Arcana in an Enchanting Table"* |
| 5 | `30EB438C66324213` | **`Ignore Players`** | `apotheosis:ignore_players_spawner_rune` ×1 |

*Ignore Players* is one of four infused-rune quests behind step 4; its siblings are the
verified titles **`No AI`** (`apotheosis:no_ai_spawner_rune`), **`Ignore All Conditions`**
(`apotheosis:ignore_conditions_spawner_rune`) and **`Echoing`** (`apotheosis:echoing_spawner_rune`).
Note the namespace: the runes are `apotheosis:` (**Apotheosis 8.8.0**) even though the
chapter is named for **Apothic Spawners 1.4.0** — both are in the mod list.

**2. The Spawner Agitator quest — despawn prevention.** Quest `1102B27CBF564127`, one
`item` task (`3839A67493B2E5C3`) for `pneumaticcraft:spawner_agitator` ×1, reward `xp` 50,
dependency `310969B8FE0A94DE` (the hub). *(No title in the config)* — called *the Spawner
Agitator quest* here. Quoted:

> *"Spawner Agitators are different from the other listed Modification items, this one is
> provided by PneumaticCraft instead of Apothic Spawners. Without the Apothic Spawners mod
> being in the Modpack, having an Agitator on a Spawner will make it spawn mobs no matter
> where the Player is. With Apothic Spawners, which yes we do have, it won't change that
> but rather will keep spawned mobs from despawning incase you leave the chunks."*

That last clause is the whole point for this page: **in ATM10 the Agitator does not make
the spawner work without a player** — Apothic Spawners is installed, so it keeps the
*spawned mobs* from despawning when the player leaves the chunks. Pair it with *Ignore
Players* and Step 1; do not sell it as a chunk loader (**judgement** about the pairing;
every clause above is quoted).

The same chapter's spawner roster, for a player who asks what else there is — these are
task items of quests hanging off `0F0E227FC3EC0D90`, all *(no title in the config)*:
`enderio:powered_spawner`, `draconicevolution:stabilized_spawner`, `ars_additions:source_spawner`,
`pneumaticcraft:pressurized_spawner`, `mysticalagriculture:soulium_spawner`,
`industrialforegoing:mob_duplicator`, `mob_grinding_utils:entity_spawner` (with
`mob_grinding_utils:xpsolidifier` and `mob_grinding_utils:solid_xp_mould_baby`). **The repo
says nothing about whether any of these runs without a player** — that is the quest entry's
and JEI's answer, not this page's. Do not infer it from the names.

## Step 4 — chunk loader blocks and upgrades the pack's configs verify

These are the mechanisms whose existence and on/off state the pack repository itself
states. "Verified from" is the config key and its own comment text, quoted; nothing else.

| Mechanism | Mod (mod-list version) | Verified from | What the config says, quoted |
|---|---|---|---|
| **Anchor Upgrade** (`mekanism:upgrade_anchor`) and **Dimensional Stabilizer** (`mekanism:dimensional_stabilizer`) | Mekanism 10.7.19 | `config/Mekanism/general.toml` → `allowChunkloading = true` | *"#Controls whether Mekanism allows players to load chunks. If this is disabled, neither the Anchor Upgrade nor the Dimensional Stabilizer will provide any functionality."* Both ids also appear in the EMI removal list above. No quest in the book tracks either. |
| **Chunk Loader in machines** | QuarryPlus 21.1.164 | `config/quarryplus.toml` → `enableChunkLoader = true` | *"#Enable Chunk Loader in machines. Default: true"* — the pack leaves it on. Same file: `removeCommonMaterialsByChunkDestroyer = true` (*"#Remove common materials(Base blocks in Over world and the Nether) obtained by Chunk Destroyer. Default: true"*), and in `[enableMap]` `chunk_marker = true`, `quarry = true`, `flexible_marker = true`, but **`adv_quarry = false`** — the pack turned the Advanced Quarry off. **No quest tracks any of it:** the single `quarryplus:` id in the whole quest config is the *icon* of a Productive Bees quest (`6E093D16B12E12B3`, *(no quest title in the config)*, icon `quarryplus:quarry`, one `checkmark` task `471F062B01D0DDA1` titled **`Quarry Bee`**, reward `xp` 100, dependency `17419401147B5C02`). |
| **Chunkloader Upgrade** for drones (`pneumaticcraft:chunkloader_upgrade`) and Programmable Controller chunk loading | PneumaticCraft: Repressurized 8.2.23 | `config/pneumaticcraft-common.toml` → `chunkload_offline_time = 300`; `allow_navigate_to_unloaded_chunks = false`; the id and the GUI keys from `kubejs/assets/pneumaticcraft_repressurized/lang/pt_br.json` | *"#Time in seconds after a player logs out that drones and Programmable Controllers belonging to that player can no long chunk-load. Set to 0 to allow indefinite offline chunkloading."* and *"#When false, drones may not navigate or teleport into unloaded chunks. Setting this true may lead to server performance and stability issues - beware."* |
| **Infusion Pylon chunkloads itself** (`pylons:infusion_pylon`) | Pylons 5.4.2 | `config/pylons-server.toml` → `infusionChunkloads = true`; quest `18246A48C20B29D8` | *"#Whether the Infusion Pylon chunkloads itself."* / *"#This is limited to one pylon per player, while the player is online."* — **while the player is online**, so it is not an away-farm answer. |
| **Familiar chunk loads** | Mahou Tsukai 1.21.1-v1.36.28 | `config/mahoutsukai-server.toml` → `FAMILIAR_CHUNKLOADS = true` | *"#Familiar chunk loads"* — the whole comment. Which familiar, and what area: not stated in the repo. |
| **Summoning Crystal chunk loading** | Ice And Fire Community Edition 2.0-beta.17 | `config/iceandfire/iaf-common.json` → `"chunkLoadSummonCrystal": true`; config-label key in `kubejs/assets/iceandfire_community_edition/lang/pt_br.json` | no comment in the JSON. The pt_br label `config.iceandfire.dragon.chunkLoadSummonCrystal` translates as *"Summoning Crystal Chunk Loads"* (**translation**; no `en_us` string in the repo). |
| **Chunk Loader block** (`naturesaura:chunk_loader`, plus a `.disabled` name variant) | NaturesAura 41.10 | `kubejs/assets/natures_aura/lang/pt_br.json` and `ru_ru.json` only | The id is verified; **nothing else about it is in this repo** — no config, no quest, no `en_us` name. The pt_br name translates literally as *"Eye of the World"* (**translation** — the English name may well differ; read it in-game). |
| **Chunk Loader block** (`immersiveengineering:chunk_loader`) | Immersive Engineering 12.4.2-194 | `kubejs/assets/immersiveengineering/lang/pt_br.json` and `ru_ru.json` only | Same status. `config/immersiveengineering-server.toml` mentions chunks 19 times and **every one is worldgen or retrogen** (`retrogen_excavator_veins`, `attempts_per_chunk`, the Core Sample Drill, the Excavator's per-chunk `yield = 38400`) — none is about chunk loading. The pt_br name translates literally as *"Resonant Observer"* (**translation**). |
| **Ritual of Arcane Permanence** (`ars_additions:ritual_chunk_loading`) | Ars Additions 1.21.1-21.3.0 | `kubejs/assets/ars_additions/lang/pt_br.json` and `ru_ru.json` only | Both files carry a `ars_additions.ritual_desc.ritual_chunk_loading` string and an `item.ars_additions.ritual_chunk_loading` name. The pt_br description translates as *"The Ritual of Arcane Permanence forces nearby chunks to stay loaded when constantly supplied with source"* (**translation**; "source" = Ars Nouveau's Source resource). The pt_br item name translates as *"Arcane Permanence"*. No quest, no `en_us` string, no Source cost in the repo. |
| **Warp Indexes need a loaded chunk** | Ars Additions 1.21.1-21.3.0 | `kubejs/assets/ars_additions/lang/pt_br.json`, key `ars_additions.page1.warp_indexes` | The pt_br page text ends *"Both Warp Indexes require your Storage Lectern to be in a loaded chunk"* (**translation**). Relevant because remote access to a farm's storage stops when its chunk unloads. |

Two of those rows deserve the emphasis a beginner will miss:

- **PneumaticCraft's offline cap is the classic "my farm stopped" cause on a server.** The
  shipped value is `chunkload_offline_time = 300` — five minutes after the player logs out,
  his drones and Programmable Controllers stop chunk-loading. The comment's own fix (*"Set
  to 0 to allow indefinite offline chunkloading"*) is a **server-owner** config change, not
  something a player can do in-game. Say that plainly and do not promise it will be
  changed. The pt_br drone-tooltip text also gives the upgrade's tiers: one upgrade keeps
  the drone's own chunk loaded, two load five chunks in a cardinal cross, three load a 3x3
  of nine (**translation** of the shipped pt_br string; the same text points at
  `allow_navigate_to_unloaded_chunks` for teleporting into unloaded chunks).
- **The three "mod has a chunk loader block" rows (Nature's Aura, Immersive Engineering,
  Ars Additions) are the weakest evidence on this page.** Their ids exist in this pack's
  bundled translations and nowhere else. Present them as *"the id is in the pack's
  localization overrides; the quest book does not track it and the repo ships no config for
  it — check JEI and the mod's own in-game guide book"*, never as a recommendation.

### Not available in 8.2 — do not carry these over from an older guide

- **`modular_machinery_reborn:chunkloader`** — Modular Machinery Reborn and its two
  companion mods were removed in pack 5.0: `changelogs/CHANGELOG-ATM10-4.15-5.0.md` lists
  the commit *"fix: remove modular machinery"* and, under *Removed (3)*, *"Modular Machinery
  Reborn (2.3.2)"*, *"Modular Machinery Reborn ArsNouveau (2.0.3)"*, *"Modular Machinery
  Reborn Mekanism (2.0.6)"*. No `modular_machinery_reborn` entry exists in
  `config/crash_assistant/modlist.json` at 8.2. Old ATM10 guides that name its chunkloader
  are out of date.

## Step 5 — what the pack turned **off**

Four switches ship disabled in this pack. All four are quoted, and each is a real reason a
player's "it should be loading" claim fails:

| Config key (file) | Value | The mod's own comment, quoted |
|---|---|---|
| `enableChunkLoading` (`config/fluxnetworks-server.toml`) | **`false`** | *"#Allows flux devices to enable chunk loading."* The pack's changelog records the change itself: `changelogs/CHANGELOG-ATM10-2.31-2.32.md` → *"Disable Fluxnet Chunkloading"*. So **Flux Networks 8.0.0 devices do not chunk-load in ATM10** as shipped. |
| `auto_force_hyperbox_chunks` (`config/hyperbox-common.toml`) | **`false`** | *"#Enable automatic forceloading of hyperbox chunks. #While this is enabled, the primary chunks of hyperbox worlds will be kept loaded while the #parent hyperbox's chunk is loaded..."* and *"#If this is disabled, no automatic enabling or disabling of forceloading will be done. In this case, #hyperbox's interiors will only tick while occupied by a player, or while forceloaded through #other means."* A farm inside one therefore needs the parent chunk force-loaded, or a player inside. **Caveat:** `config/hyperbox-common.toml` is in the repo, but there is **no `hyperbox` entry** in `config/crash_assistant/modlist.json` at this commit — treat the mod's availability in 8.2 as unverified and check the player's instance. |
| `["Ftb Chunks"] enabled` (`config/crashutilities-server.toml`) | **`false`** (`days = 7`) | *"#If Ftb chunks is installed enable automatic purge of loaded chunks for people who have not been online for some amount of days. (Note LOADED not Claimed Chunks)"* / *"#Number of days after which a players chunks will be unloaded. Warning! This relies on the modify date of the player data file."* Off as shipped — but it is a **server** switch, and a server that turns it on will unload the force-loaded farm of anyone offline for `days`. Crash Utilities 9.0.4. Worth asking about on a server before blaming the farm. |
| `allow_navigate_to_unloaded_chunks` (`config/pneumaticcraft-common.toml`) | **`false`** | *"#When false, drones may not navigate or teleport into unloaded chunks. Setting this true may lead to server performance and stability issues - beware."* Not a loader switch, but the reason a drone farm can stall at a chunk border. |

For contrast, the Mekanism, AE2, QuarryPlus, Mahou Tsukai, and Pylons switches in Step 4
all ship **on** (`allowChunkloading = true`, `spatialAnchorEnableRandomTicks = true`,
`enableChunkLoader = true`, `FAMILIAR_CHUNKLOADS = true`, `infusionChunkloads = true`).
Whether any of them is what a given player should use is **judgement** — the config only
proves the pack did not disable them.

## Chunk *areas* that are not chunk loading (a common mix-up)

Several ATM10 features are measured in chunks and do not load anything. The **Pylons**
chapter (config filename `pylons`, chapter id `5712300EF4E5E846`, book title **Pylons**,
group **Logistics**, 13 quests) is where most of the confusion starts; its hub quest
`30B0240543253EFB` carries the verified title **`Pylons`** (`&lPylons` in the config) and
asks for `minecraft:polished_blackstone` ×1.

| Pylon / filter | Quest id, task item | What the quest text actually says (quoted) |
|---|---|---|
| **Harvester Pylon** | `12ED1EE85E146A4B` → `pylons:harvester_pylon` ×1, *(no title in the config)* | *"Harvester Pylons work as a very simple Auto-Farm. Put the Pylon on or in the Water Source and it will automatically harvest and replant Crops that are fully grown in the set area around it."* / *"The area can be set to 3x3, 5x5, 7x7, or 9x9 Blocks around the Pylon."* / *"It will need a Hoe to use on the Plants and will need an Inventory like a chest above it to put the Crops."* / *"(Careful when using a lot of modifiers with it like Lilypads or fertilizer as when it goes very fast farming it can be a TPS eater)."* |
| **Infusion Pylon** | `18246A48C20B29D8` → `pylons:infusion_pylon` ×1, *(no title in the config)* | *"The Infusion Pylon works similar as a Beacon just much better and cheaper!"* / *"When a Potion Effect is put in by a Potion Filter, it will continuously give you the Potion Effect while you're in the set Chunk area."* A chunk **area**, and it chunkloads only itself, only one per player, only while online (config above). |
| **Expulsion Pylon** | `32E52AD6EF194A60` → `pylons:expulsion_pylon` ×1, *(no title in the config)* | *"When placed down it will keep any Players who aren't whitelisted from a set amount of Chunks around it."* / *"The Chunks are set in it's GUI in the top left from 1x1, 3x3, or 5x5 Chunks."* Protection measured in chunks — it loads nothing. |
| **Interdiction Pylon** | `5B5FC539BD1F4A73` → `pylons:interdiction_pylon` ×1, *(no title in the config)* | *"This Pylon is all about blocking Mob Spawns."* — *"You can use Mob Filters to block spawns of only certain Mobs or use the Lifeless Filter to block all Mob spawns!"* |
| **Lifeless Filter** | `5C2C29ECA67F9B49` → `pylons:lifeless_filter` ×1, *(no title in the config)* | *"With the Lifeless Filter you will never have to worry about any Mob spawns within a 25x25 Block area."* / *"That's enough to cover every distance Mobs spawn near the player."* — blocks, not chunks, and again no loading. |
| **Hoes** (the Harvester's requirement) | `034A9FBCA6D79BB6`, *(no quest title in the config)*; task title **`Hoes`** → `ftbfiltersystem:smart_filter` with filter `ftbfiltersystem:item_tag(minecraft:hoes)` | *"The Harvester Pylon needs a Hoe to work."* / *"(Hoes that can't break will work forever, Hoes that can will need to be replaced)."* |

`config/pylons-server.toml` sets the numbers behind those quotes, verbatim:
`harvesterWorkDelay = 20` (its comment says *"# Default: 60"*, so the pack runs it faster),
`harvesterRequiresTool = true`, `harvesterCanBeAutomated = false` (*"#By default,
unbreakable tools are required for full automation."*), `harvesterRequiresPower = false`,
`harvesterPowerCost = 5`, `teamSupportEnabled = true` (*"#Whether team support is enabled
if a compatible mod (FTB Teams, Argonauts) is installed"*), `expulsionPylonMaxRadius = 2`
(*"#Limit the max radius for expulsion pylons. #Does not include center chunk, so a radius
of 2 equals a 5x5 chunk diameter."*), `expulsionWorldSpawnRadius = 1`,
`expulsionPylonCanExplode = false`, and `expulsionAllowedDimensions = ["minecraft:overworld",
"allthemodium:the_beyond", "eternal_starlight:starlight", "compactmachines:compact_world"]`.
Those four dimension ids are the only ones this page names, and they are the config's.

**Why the Harvester Pylon belongs on a chunk-loading page at all:** it is the pack's own
*"very simple Auto-Farm"*, and like every other machine it only works in a loaded chunk.
Force-load its chunk (Step 1) and it keeps harvesting and replanting while the player is
away — but note `harvesterCanBeAutomated = false`, so the hoe has to be unbreakable to run
indefinitely. **That last sentence is judgement**, built from two quoted config values; the
repo does not spell out the combination.

Two more chunk-measured things that are not chunk loading, so they are not mistaken for it:

- **Draconic Evolution's *Quantum Energy Tunnel*** — quest `4B9FF9E972B0E530` (verified
  title), task `draconicevolution:item_draconic_energy_link` ×1, behind **`Wireless Energy
  Link`** (`20D8DA523E900A52`, task `draconicevolution:item_wyvern_energy_link` ×1) which
  is behind **`Modules!`** (`4EFFE300EC781C3E`). This one *does* depend on chunk loading:
  *"It doesn't work between Dimensions! Thankfully the better ones can, just make sure the
  other side is chunkloaded."* A cross-dimension farm feed therefore needs **both** ends
  loaded (**judgement** on the consequence; the sentence is quoted).
- **Neo Vitae's per-chunk Spiritus** — the Neo Vitae chapter (config filename `neo_vitae`,
  book title **Neo Vitae**, group **Magic**, 49 quests) uses "chunk" as a *resource unit*,
  not a loading unit: quest `298458E916F65407`, verified title **`The Aura Between
  Worlds`**, task `neovitae:vas_maleficum` ×1, says *"We burn Spiritus in the Vas Maleficum
  and the chunk's air thickens with will."* A farm built on that mechanic reads the chunk
  it sits in; it does not load anything (Neo Vitae 1.1.26 — the mod list's id is
  `neovitae`, the quest chapter's filename is `neo_vitae`).

## Answering the beginner question

The question is *"how do I keep my farm running while I'm away?"* Answer in this order, and
stop as soon as the player's case is covered:

1. **Force-load the farm's chunks.** Welcome chapter → the quest whose task is titled
   *Claiming Chunks*: **M** → **Claimed Chunks** icon → drag to claim → **shift-left-click**
   to force-load → *"you'll see lines across the chunk"*. This is the pack's own answer, it
   costs nothing, and it works from the first hour. It is also the *only* answer that needs
   no mod progression.
2. **Ask what kind of farm it is** before recommending anything else — crop, mob, bee,
   tree, quarry, or a dimensional one. The pack's configs treat those differently, and
   guessing wastes the player's time.
3. **Mob farm?** Apothic Spawners → *Ignore Players* (`apotheosis:ignore_players_spawner_rune`)
   removes the player requirement but its own text still says *"As long as its chunk-loaded
   it will spawn"*; the Spawner Agitator quest only stops despawning. Step 1 is still
   needed.
4. **AE2 network already there?** The Spatial Anchor quest is the book's one documented
   chunk loader: it force-loads the chunks the ME network occupies, excluding subnetworks,
   while powered. Warn that the pack hides `ae2:spatial_anchor` from the EMI index, so the
   player may not find it by browsing.
5. **On a server, check the switches before debugging the farm.** Flux Networks chunk
   loading is **off** (`enableChunkLoading = false`, and the changelog says so);
   PneumaticCraft stops chunk-loading **300 seconds** after the owner logs out
   (`chunkload_offline_time = 300`); Crash Utilities can purge a long-offline player's
   **loaded** chunks (`enabled = false` as shipped, `days = 7`); Hyperbox interiors do not
   auto-force-load (`auto_force_hyperbox_chunks = false`).
6. **Never state a limit.** How many chunks the player may claim or force-load is not in
   this repo. Read it off his claim screen / his server's config, and say that the in-game
   book and the FTB Chunks screen are authoritative.

Two follow-ups worth asking, because the answer differs: **singleplayer or server?** (every
switch in step 5 is a server-side config, and a singleplayer world keeps ticking only while
the game runs) and **how big is the farm, in chunks?** (the force-load step is per chunk,
and the pack's quest text gives no budget — **judgement**, not a quoted rule).

## When it still does not work

Grounded checks only, in the order the repo supports them:

- **Are the lines actually across the chunk?** The quest text makes the visual check
  explicit: *"If done properly, you'll see lines across the chunk."* Claimed-but-not-loaded
  is the most common miss, and the Crash Utilities comment (*"LOADED not Claimed Chunks"*)
  is the pack's own reminder that the two states differ.
- **Is the whole farm inside the loaded area?** A farm straddling a chunk border needs
  every chunk it touches. The config gives no way to compute that from here — the map
  screen does (**judgement**).
- **Is the machine's own requirement met?** The Harvester Pylon needs a hoe and an
  inventory above it (`harvesterRequiresTool = true`); the Spatial Anchor needs a *powered*
  network; the Infusion Pylon chunkloads only itself, only one per player, only while
  online. Each of those is quoted above.
- **Is a server-side switch off?** See step 5. `enableChunkLoading = false` (Flux
  Networks), `chunkload_offline_time = 300` (PneumaticCraft), `auto_force_hyperbox_chunks =
  false` (Hyperbox), `allow_navigate_to_unloaded_chunks = false` (drone pathing).
- **Did the player find the item in EMI and give up?** `ae2:spatial_anchor`,
  `mekanism:upgrade_anchor`, and `mekanism:dimensional_stabilizer` are in
  `kubejs/assets/emi/index/stacks/removals.json`. Point at the AE2 quest entry instead.
- **Is it a bug?** `MOD_ISSUES.md` sends FTB Chunks issues to
  `https://github.com/FTBTeam/FTB-Mods-Issues/issues` (listed there as *"FTB Chunks
  (Forge)"*). Pack-level problems go to the ATM Discord, which the Welcome chapter's first
  quest names: *"If you have any questions or issues, feel free to join the ATM discord!"*

## Cross-references

- `references/getting-started.md` — the first-hour checklist, where chunk claiming is step 1
  and the Welcome chapter's commands are listed; and the multiplayer note about claiming
  before building together.
- `references/key-mods.md` — what Pylons, AE2, Mekanism, PneumaticCraft, and the FTB
  utility mods are for and when the player reaches them; the Pylons row there calls the
  mod's chunk helpers *"chunk-ish"* and points here for the detail.
- `references/progression.md` — the four stages, for judging whether a player asking this
  question is early-game (Step 1 only) or mid-tech (Steps 2–4 worth discussing).
- `references/creative-checklist.md` — Chapter 4's star automation. Not chunk loading, but
  the same rule applies there: an automated star line still needs its chunks loaded to run
  unattended (**judgement**; that page quotes no chunk-loading mechanic).

## What this page deliberately does not tell you

- **A claim or force-load limit.** No number of chunks, no rank permission node, no
  per-team budget. The repo ships no FTB Chunks or FTB Ranks config, so any figure would be
  invented. The player's own claim screen is the source.
- **Command syntax.** No `/forceload`, no `/ftbchunks` subcommands, no admin incantation.
  The only commands quoted anywhere on this page are the ones the Welcome chapter's own
  text quotes: `/sethome`, `/home`, `/spawn`, `/rtp`, `/ftbteams party create`.
- **Recipes and costs.** Not one — not for the Spatial Anchor, not for a rune, not for a
  chunk loader block. JEI, in-game.
- **Farm designs, rates, or layouts.** How many crops per chunk, what a good mob farm looks
  like, how fast a quarry runs: none of it is in the config, and the pack's own Harvester
  Pylon text warns that speed can be *"a TPS eater"*.
- **A chunk loader the config does not name.** If a player names one that is not on this
  page — from another pack, another version, or a mod ATM10 removed — the answer is *"let's
  check your instance and JEI"*, never a guess. The one removal this page can prove is
  Modular Machinery Reborn's, in pack 5.0.
- **English names for the four localization-only ids.** `naturesaura:chunk_loader`,
  `immersiveengineering:chunk_loader`, `pneumaticcraft:chunkloader_upgrade`, and
  `ars_additions:ritual_chunk_loading` appear in the repo only inside bundled pt_br/ru_ru
  translations. Their in-game English names, costs, areas, and recipes are the game's and
  JEI's to give.
