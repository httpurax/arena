# ATM10: the first hour — from spawn to your first quests done

**What this page is.** The beginner's answer to *"I just started, what do I do first?"*
for **All the Mods 10** — the first ~60 minutes, in order, from the moment you spawn to
the point where the pack's own opening quests are checked off. It walks the book's two
opening pages: the **Welcome** chapter (5 player-visible quests) and the opening chain of
**Chapter 1: The Beginning**, then names the branches off that chain a beginner can
actually reach inside an hour. It is a *route*, not a tutorial: it tells you which quest
to do next and why, not how to craft anything.

Everything quoted here was read from the pack's own quest config — and everything the
config does not say is labelled judgement.

## Provenance — everything here was read, not remembered

Every quest title, quest id, task item id, task count, reward, dependency, chapter id,
chapter group, and config key below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which the pack's own `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/welcome.snbt` | the Welcome chapter: its id, order index, icon, and all six of its quests with their tasks and rewards |
| `config/ftbquests/quests/chapters/mainquestline_part_1.snbt` | Chapter 1: The Beginning — its 36 quests, dependencies, task items, counts, and rewards |
| `config/ftbquests/quests/lang/en_us/chapters/welcome.snbt`, `.../mainquestline_part_1.snbt` | the English quest titles, task titles, subtitles, and the description text quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapter titles (`Welcome`, `Chapter 1: The Beginning`) |
| `config/ftbquests/quests/chapter_groups.snbt` + `lang/en_us/chapter_group.snbt` | the quest-book groups and their order (Main Questline is first) |
| `config/ftbquests/quests/data.snbt` | the pack-wide quest-book switches quoted under "Two pack-wide switches" |
| `config/ftbquests/quests/lang/en_us/reward_table.snbt` + `reward_tables/common.snbt`, `reward_tables/uncommon.snbt` | the two random-reward tables the opening quests roll on: **Reward: Common** and **Reward: Uncommon** |
| `config/bcc-common.toml` | the pack version: `modpackVersion = "8.2"` |
| `config/ftbultimine-server.snbt` | the shipped FTB Ultimine settings quoted under "Free speed-ups" |
| `CHANGELOG.md` | the version and date stamp: **8.2**, 2026-09-22 |
| `config/crash_assistant/modlist.json` | the mod ids and versions behind the mod names named here (493 entries) |

Quest titles and quoted text are shown with Minecraft's `&` formatting codes stripped
(`&6M&r` → `M`), the way the book renders them.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs from anything here, his
  book wins — say so and re-check, rather than arguing from this file.
- **Titles are the config's, never invented.** Every quest name below was read from the
  lang files named above. Four of the Welcome chapter's player-visible quests carry **no
  quest title in the config** — the book shows them by their *task* title, and this page
  says so instead of inventing one. The same is true of four Chapter 1 entries. Where the
  config has a title it is quoted; where it does not, the entry is marked *(no title in
  the config)* and never renamed.
- **The route order is the config's; the timing is judgement.** Quest order and
  dependencies are verified in the config. "What fits in an hour" is this skill's
  judgement — FTB Quests has no clock, quests are optional, and nothing is gated. Marked
  *(judgement)* wherever it appears.
- **No recipes, no coordinates, no seed tricks, no layouts.** The config lists *what a
  quest wants*, never how to make it. Every "how" here is a quote from a quest's own
  text or a pointer to JEI. Do not fill anything in from memory or plausibility.
- **Item ids below are quoted from config task entries, never invented** — and only the
  ones that anchor a claim appear.
- **Anything uncertain is flagged approximate.** When repeating such a detail, keep the
  hedge: "guides say roughly X — verify in-game".

## The short answer

If the player only reads one thing:

1. **Open the quest book first — before you build anything.** Finish the **Welcome**
   chapter: 5 player-visible quests, 50 XP total, and it is where the pack teaches the
   commands, chunk claiming, and teams (`Welcome` is the book's ungrouped chapter with
   `order_index: 0`).
2. **Then start Chapter 1: The Beginning** and follow its opening chain in order. The
   first six quests are the vanilla opening the book itself calls the guided route:
   logs → crafting table → wooden pickaxe → 16 cobblestone + a furnace → iron + copper →
   an iron pickaxe.
3. **Take the cheap side quests as you pass them** — *Crafting, but on a Stick* (optional),
   the untitled coal entry, *Lava Bucket*, and *Basic Ore Doubling* — they pay materials
   you were going to gather anyway.
4. **Stop at the iron pickaxe and look around.** From there the chapter forks into
   redstone, diamonds, ore doubling, and three starter generators; picking one of those
   is where hour two begins (`references/automation-first-steps.md` continues from here).

*The ordering above follows verified dependencies; the "first hour" framing is
judgement. The in-game quest book is authoritative for what any entry actually asks.*

## Step 0 — Open the quest book before you touch a tree

The quest book is FTB Quests, and the Welcome chapter's own icon is the book itself
(`ftbquests:book`). Open it from the book item or its keybind — if the book is not on
the hotbar, check the **Controls** screen rather than assuming a default (*judgement —
the pack's config does not name a keybind*).

Two pack-wide switches in `config/ftbquests/quests/data.snbt` shape how the book behaves
from the first minute, and both are worth telling a beginner up front:

| Config key (pack 8.2) | Value | What it means for the first hour |
|---|---|---|
| `default_autoclaim_rewards` | `"disabled"` | Finishing a quest does **not** hand you the reward — open the entry and claim it. The pack's opening quests pay XP and starter items you do not want to lose. |
| `default_consume_items` | `false` | A task checks off the item **without taking it**. Your furnace, your iron pick, your ingots stay in your inventory. |

The same file also ships `detection_delay: 60` and `emergency_items_cooldown: 300`;
what those do to your book's timing is the mod's own business — trust the entry in front
of you rather than a number here.

## Step 1 — the Welcome chapter, quest by quest

**Welcome** — chapter id `5B00676D79306EA2`, `order_index: 0`, no quest-book group
(`group: ""`), 6 quests in the file (5 for players plus one hidden authoring entry).
Every player-visible quest in it pays **10 XP**.

| Book entry (as the config titles it) | Quest id | Kind of title | Task | Reward |
|---|---|---|---|---|
| **Welcome to All The Mods 10!** | `3BC0A50886A3222B` | quest title | `dimension` task for `minecraft:overworld` | 10 XP |
| **Quests** | `3708A4780ACEB34E` | *task* title — *(no title in the config)* | `checkmark` | 10 XP |
| **Useful Commands** | `7658C1C663394E85` | *task* title — *(no title in the config)* | `checkmark` | 10 XP |
| **Claiming Chunks** | `0C93D7A607AB8B83` | *task* title — *(no title in the config)* | `checkmark` | 10 XP |
| **Creating a Team** | `5AC1BE754210429E` | *task* title — *(no title in the config)* | `checkmark` | 10 XP |
| *(hidden authoring entry — not for players)* | `49EDAA2F57D3BF1D` | none | 2 × `checkmark` titled `AllRightsReserved` | none |

Three things matter about that table:

- **The first quest completes on its own.** *Welcome to All The Mods 10!* has exactly one
  task, a `dimension` task for `minecraft:overworld` — so it is satisfied by being in the
  Overworld, which is where you spawned. Its quest text is *"ATM10 is a kitchensink pack
  that allows you to explore the world of modded Minecraft in your own way!"* and
  *"If you have any questions or issues, feel free to join the ATM discord!"*
- **The other four are self-declared checkmarks.** There is nothing to fetch; you read
  each entry and tick it. Do all four immediately — 40 XP for reading four short pages.
- **One of them is the pack's only chunk-loading tutorial.** *Claiming Chunks* is worth
  reading properly even though it costs nothing: its text is *"To claim chunks, open up
  your map using M, then click the Claimed Chunks icon in the top left."*, *"To claim a
  chunk, left click and drag to claim."* and *"To force load a chunk, shift-left click
  the chunk. If done properly, you'll see lines across the chunk."* Claiming early is
  what keeps a later farm running (`references/chunk-loading-guide.md`).

What the rest of the chapter's text says, quoted:

- **Quests** — *"In this modpack, quests are optional. Mods are not gated behind
  completing any quests!"* and *"A lot of the individual questlines outside of the Main
  questline are meant to serve as mod guides. If you want to follow the progression, make
  sure to check out the Main Questline!"* — this is the pack telling you the route is a
  recommendation, not a gate.
- **Useful Commands** — *"There are plenty of helpful commands within ATM. Here are a
  few:"*, then the config's own list: `/sethome` (`/sethome farm` … `/home farm`),
  `/spawn`, and `/rtp` (*"Random Teleport" will teleport you to a random location in the
  world.*). Its closing line is *"Note: These commands have cooldowns and limits."* — the
  pack states no numbers, so neither does this page.
- **Creating a Team** — *"If you want to create a team for you and your friends, use the
  command /ftbteams party create (name of team) to create the team!"* Irrelevant solo;
  the first thing to do on a shared server.

## Step 2 — Chapter 1: The Beginning — the opening chain

**Chapter 1: The Beginning** — chapter id `732824E03978A934`, the `order_index: 0`
chapter of the **Main Questline** group (`2084F3F6FB861C5B`, the group
`chapter_groups.snbt` lists first), 36 quests, chapter icon `minecraft:crafting_table`.

Its root quest has no dependencies, so the chain below is available from minute one. The
dependencies in the last column are verified in the config; the task items and counts are
quoted from the config's own task entries.

| # | Verified quest title | Quest id | Task(s) as configured | Reward | Depends on |
|---|---|---|---|---|---|
| 1 | **Welcome to Getting Started!** | `5CF320E9C4C1B1E1` | 1 × anything in `minecraft:logs` | 4 × `minecraft:torch`, 4 × `minecraft:cooked_beef` | — (chapter root) |
| 2 | **Putting the Craft in Minecraft** | `282CE3A088AE5CFB` | 1 × `minecraft:crafting_table` | 10 XP | #1 |
| 3 | **Our First Pick** | `7975C7145572C438` | 1 × `minecraft:wooden_pickaxe` | 2 × `minecraft:oak_log`, 1 × **Reward: Common**, 10 XP | #2 |
| 4 | **Stone Age** | `7D38BC3DB3406F51` | 16 × `c:cobblestones`, 1 × `minecraft:furnace` | 10 XP | #3 |
| 5 | **The Metal Age** | `051E0C85E7B71CE0` | 1 × `minecraft:iron_ingot`, 1 × `minecraft:copper_ingot` | 1 × **Reward: Uncommon**, 25 XP | #4 |
| 6 | **An Iron Pick** | `698A959C9E449592` | 1 × `minecraft:iron_pickaxe` | 50 XP | #5 |

**This is the pack's own "what do I do first".** The chain is the vanilla opening with
the pack's starter rewards stapled on, and quest #1 pays the two things a first hour
actually runs out of — light and food. What its text says, quoted:

- **Welcome to Getting Started!** — *"ATM10 is a Kitchensink pack, meaning you are free
  to explore and play the modpack any way that you want!"*, *"However, there is an
  endgame goal: Making the ATM Star!"*, *"This questline serves as a guide for all
  players, whether you are brand new to Minecraft or you've played through previous ATM
  packs."* and the instruction: *"Just like almost every modpack, gather some wood to get
  started!"*
- **Putting the Craft in Minecraft** — *"Sure, you could craft in your inventory using
  the 2x2 crafting grid, but that won't get you far. We need to upgrade by making a
  Crafting Table!"*
- **Our First Pick** — *"Pickaxes allow you to break most stone and metal blocks. This
  wooden one won't last long, so make sure to gather some Cobblestone with it!"*
- **Stone Age** — *"Cobblestone unlocks the next part of progression by allowing you to
  craft a Furnace to smelt our ores."* and *"You'll also want to upgrade your pickaxe to
  stone to mine better ores like Iron!"*
- **The Metal Age** — *"Copper is abundant and has plenty of uses for things like Ore
  Hammers or Drawer Upgrades, so make sure to grab plenty of it!"* and *"Iron is probably
  one of the most important ores you'll want to get every time you run into it. The world
  of modded MC pretty much runs on Iron."*
- **An Iron Pick** — *"The next step of progression is to make an Iron Pickaxe."* and
  *"This pickaxe can mine some of the rarer ores in the game, including Diamond!"*

## Step 3 — the first branches (what hour one realistically reaches)

Past *An Iron Pick* the chapter forks. These are the forks whose dependencies are already
satisfied by the chain above, so any of them is a legal next step; which to take first is
judgement.

### Branch A — two cheap side quests worth knowing about

| Verified quest title | Quest id | Task(s) as configured | Reward | Notes |
|---|---|---|---|---|
| **Crafting, but on a Stick** | `378BF828DC931F0C` | 1 × `crafting_on_a_stick:crafting_table` | 10 XP | `optional: true`; depends on *Putting the Craft in Minecraft* |
| **Archaeology!** | `3ADCAD65EA6900BA` | 1 × `minecraft:brush` | 1 × `minecraft:brush`, 50 XP | depends on *The Metal Age* |

*Crafting, but on a Stick* is one of the two optional quests the chapter offers right
after the crafting table, and its own text explains why it is worth the detour:
*"Personally, I hate having to run to a block just to
craft. That's where the Crafting Table on a Stick comes in!"*, *"This item works as a
Portable Crafting Table!"* and *"Tip: You can also put this in your Curios slot and set a
Keybind to open it!"* The same mod also has an entry in the **Tips and Tricks** chapter
(*Crafting... on a Stick!*, `0790D3BB481162A6`) that calls it *"a must have in the early
game"* — two routes to the same item, either is fine.

### Branch B — the resource quests you trip over while mining

| Verified quest title | Quest id | Task(s) as configured | Reward |
|---|---|---|---|
| **Redstone** | `4DE1158931F84F22` | 4 × `minecraft:redstone` | 25 XP |
| **We've Struck Diamonds!** | `76406EFFF8CBA6B4` | 1 × `minecraft:diamond` | 1 × **Reward: Uncommon**, 50 XP |
| **Basic Ore Doubling** | `4E5238F00CEED8B2` | 1 × any item in `alltheores:ore_hammers` | 3 × `alltheores:iron_dust`, 3 × `alltheores:copper_dust`, 25 XP |
| *(no title in the config — task `Coal`; subtitle "Smelt your logs")* | `24C9BA6DC32CFAD9` | 1 × anything in `minecraft:coals` | 6 × `minecraft:oak_log` |
| **Lava Bucket** | `72E1C19156633391` | 1 × `minecraft:bucket` **or** 1 × `mekanism:basic_fluid_tank` | 1 × `minecraft:iron_ingot` |

The ones worth doing on sight:

- **Basic Ore Doubling** — the earliest "make my time back" quest in the pack, and the
  config puts it directly behind *The Metal Age* (dependency verified). Its text: *"Smelting
  down raw ores in the beginning is necessary, but you are missing out on extra
  resources!"*, *"These will break down 1 raw ore into 2 ore dust, which can be smelted
  into ingots, effectively doubling your ingot output!"* and, for more later, *"Want more
  per raw ore? Check out the mod Occultism!"* It pays iron and copper dust outright.
- **Redstone** — *"Once you have an Iron or better tier Pickaxe, you'll be able to mine
  Redstone."*, *"Redstone starts your journey into many technical mods, like creating
  power or making fancy gadgets."* and *"This is a resource you will want a lot of!"* It
  is the dependency of the power-cable entry in Branch C, so it is on the path to power.
- **Lava Bucket** — *"Buckets and Tanks are a great early way to move around lava."* It
  is also the dependency of *Lava Power*, so it unlocks Branch C.
- **The untitled coal entry** — *"Coal is your first real source of power. If you are
  running low and can't find any Coal, an alternative would be to use Charcoal."* The
  config shows it as a "Coal" task with the subtitle *"Smelt your logs"*; treat charcoal
  as fine.

`references/ore-processing-ladder.md` picks up the doubling question where this leaves it.

### Branch C — the starter generators, and the wiring behind them

Every quest in this branch is in Chapter 1; the quest book's Power group (the *Basic
Power* and *Powah* chapters) picks the thread up afterwards. *Lava Power* is the one on
the path from *Lava Bucket*; *Wind Power* and *Solar Power* are both `optional: true` and
both depend on *Lava Power*.

| Verified quest title | Quest id | Task(s) as configured | Reward | Optional? | Depends on |
|---|---|---|---|---|---|
| **Lava Power** | `346860B8EBC4C28C` | 1 × `powah:magmator_basic` **or** `powah:magmator_starter` **or** `generatorgalore:magmatic_generator` | 1 × `minecraft:lava_bucket`, 2 × `minecraft:crying_obsidian`, 6 × `minecraft:obsidian`, 1 × **Reward: Common** | no | *Lava Bucket* |
| **Wind Power** | `2CCAA7C0FEDEB573` | 1 × `mekanismgenerators:wind_generator` | 1 × **Reward: Common** | yes | *Lava Power* |
| **Solar Power** | `3B6F1BD64C0C570F` | 1 × `powah:solar_panel_basic` **or** `mekanismgenerators:solar_generator` | 1 × **Reward: Common** | yes | *Lava Power* |
| *(no title in the config)* | `5792CC9E3AFAB229` | 1 × `generatorgalore:copper_generator` | 1 × `minecraft:coal_block` | no | the untitled coal entry |
| **Generators Galore** | `790EC3EDC2DB1FB0` | 1 × `generatorgalore:enchantment_generator` **or** `generatorgalore:halitosis_generator` **or** `generatorgalore:netherstar_generator` **or** `generatorgalore:potion_generator` | 1 × **Reward: Common** | no | the untitled `generatorgalore:copper_generator` entry |

What the text says, quoted — *Lava Power*: *"Now that you have all this lava what will
you do with it? More early game power!"*; *Wind Power*: *"If you are like most this is
the power you are after. All you do is place it as high as you can and get free power."*;
*Solar Power*: *"Just like wind generation this will give you lots of power without
giving it any resources. The only downside here is it has to be daytime."*;
*Generators Galore*: *"As was mentioned before, this mod adds a ton of fun ways to
generate power that require specific builds."*

**The wiring quests sit right behind them**, both depending on earlier entries and both
paying 3 items plus 50 XP:

| Book entry | Quest id | Task(s) as configured | Reward | Depends on |
|---|---|---|---|---|
| *(no title in the config — task `Power Cables`)* | `4869C413646CC4CC` | 1 × `mekanism:basic_universal_cable` **or** `pipez:energy_pipe` **or** `powah:energy_cable_basic` | 3 × `minecraft:redstone_block`, 50 XP | *Redstone* |
| *(no title in the config — task `Power Storage`)* | `672134A1A620EEAB` | 1 × `mekanism:basic_energy_cube` **or** `powah:energy_cell_starter` | 3 × `mekanism:ultimate_universal_cable`, 50 XP | the cables entry |

Their text is deliberately mod-neutral — *"Transferring power out of your generators is
probably a good idea, but how can you do it?"* … *"To start, you can use Energy Pipes
from the Pipez mod, or you can use the Powah Energy Cables if you have already started
using that mod."*, and *"Note: You only have to make one of the items to complete the
quest."* Which generator-and-cable family to commit to is judgement; the book offers
alternatives on purpose. *Generators Galore* is also the follow-on quest for
`generatorgalore:copper_generator`, whose own entry has no title in the config.

### Branch D — the furnace line, if you have the metals

| Verified quest title | Quest id | Task(s) as configured | Reward | Notes |
|---|---|---|---|---|
| **Furnace Upgrades!** | `2AEBE3F28996A6ED` | 1 × `ironfurnaces:iron_furnace` **or** `ironfurnaces:copper_furnace` **or** `ironfurnaces:upgrade_iron` **or** `ironfurnaces:upgrade_copper` | 10 XP | depends on the untitled coal entry |
| **Furnace Augments** | `7EC01E7DB045DB05` | 1 × `ironfurnaces:augment_blasting`, `ironfurnaces:augment_smoking`, `ironfurnaces:augment_factory`, `ironfurnaces:augment_generator`, `ironfurnaces:augment_speed`, or `ironfurnaces:augment_fuel` | 10 XP | `optional: true`; depends on *Furnace Upgrades!* |

*Furnace Upgrades!* — *"With our new metals, we can upgrade our Furnace using the mod
Iron Furnaces!"* and *"These Furnaces make automation easier by allowing you to auto-pull
or push from the sides using the config on the left of the interface."* The augments
entry (optional) spells out what each augment does, in the config's own words: Blasting,
Smoking, Factory, Speed, Fuel Efficiency. Reasonable hour-one value, but strictly
optional — the vanilla furnace already satisfied *Stone Age*.

## Free speed-ups the pack itself ships *(verified config)*

Two things a beginner can use in minute one, both evidenced in the pack's files rather
than in a guide:

- **FTB Ultimine is in the pack and configured generously.** `config/ftbultimine-server.snbt`
  ships `max_blocks: 64`, `exhaustion_per_block: 20.0d`, `experience_per_block: 0.0d`,
  `require_tool: false`, and `merge_tags` covering `minecraft:base_stone_overworld`,
  `c:ores/*`, `forge:ores/*` and `integrateddynamics:menril_logs` — i.e. stone and ores
  count as one block for the tool. It also ships right-click harvesting, tilling and
  axe-stripping switches, all `true`. Hold the Ultimine key while mining or chopping: it
  is the biggest time-saver in the first hour *(judgement — the config ships the settings,
  not the advice)*. **The pack's config does not name the keybind** — check Controls
  (*judgement: the mod's default is the grave key, but verify in your own Controls screen
  rather than trusting that*).
- **The map is on `M`** — that one *is* in the config, quoted above in *Claiming Chunks*.

The **Tips and Tricks** chapter (`1BE666F01EFFC00D`, 23 quests) is the chapter the pack
built for exactly this: compasses for finding biomes and structures
(*Compasses for Searching*), Tool Belt, Easy Villagers, Building Gadgets, Functional
Storage, and Simple Magnets. It is ungrouped and its quests are cheap — a good "I have 10
spare minutes" page, **not** a prerequisite for anything.

## A route you can actually run in an hour *(judgement)*

The dependencies below are verified in the config. **The minute-by-minute split is
judgement** — it assumes a normal overworld spawn, a wooden-tier tool set, and no
detours into cave systems. Adjust freely; nothing here is gated.

| Minutes *(judgement)* | Do this | Verified anchor |
|---|---|---|
| 0–5 | Open the book. Tick all four Welcome checkmark quests and claim their XP. Set `/sethome`, then claim and force-load the chunks around your spawn. | `3708A4780ACEB34E`, `7658C1C663394E85`, `0C93D7A607AB8B83`, `5AC1BE754210429E` |
| 5–12 | Punch trees. That satisfies **Welcome to Getting Started!** — claim the 4 torches and 4 cooked beef. | `5CF320E9C4C1B1E1` |
| 12–18 | Crafting table, then **Putting the Craft in Minecraft**; make the wooden pickaxe for **Our First Pick** (claim the 2 logs and the **Reward: Common**). | `282CE3A088AE5CFB`, `7975C7145572C438` |
| 18–30 | Dig for cobblestone (16 for the task) and build the furnace: **Stone Age**. Craft a stone pickaxe on the way — the quest text tells you to. | `7D38BC3DB3406F51` |
| 30–45 | Find iron and copper — a surface cave or a small ravine is enough. **The Metal Age** wants one ingot of each and pays a **Reward: Uncommon**. | `051E0C85E7B71CE0` |
| 45–55 | Make the iron pickaxe: **An Iron Pick**. The config's own text says this pickaxe reaches diamond, and *Redstone* is gated behind it too. | `698A959C9E449592` |
| 55–60 | Bank the easy ones: **Crafting, but on a Stick** (optional), the untitled coal entry, and **Lava Bucket** — three quests for items you already have or will trip over. | `378BF828DC931F0C`, `24C9BA6DC32CFAD9`, `72E1C19156633391` |

If the player has *more* than an hour, the natural continuation is **Basic Ore Doubling**
(`4E5238F00CEED8B2`) and then one starter generator — `references/automation-first-steps.md`
ranks exactly those five automations in order.

## What is **not** a first-hour problem *(judgement)*

Keeping a beginner out of rabbit holes is most of the value of this page. None of the
following is *wrong*, but none of it is where the pack's opening points:

- **Don't chase the ATM Star.** The chapter text says there *"is an endgame goal: Making
  the ATM Star"* — that is the destination, not the first hour.
- **Don't pick a tech line yet.** Mekanism, Create, Modern Industrialization and the rest
  have full chapters; the book offers them as alternatives and gates nothing. Committing
  before you have iron is judgement against, not for.
- **Don't build a storage network.** AE2 and Refined Storage are both fully quested and
  both a mid-tech-stage decision. Chests and drawers are correct in hour one.
- **Don't grind Mystical Agriculture yet.** It is the highest-leverage farm in the pack,
  and the book's own *Inferium Farmland* entry says *"You'll want to start growing
  Inferium as soon as you can!"* — "as soon as you can" is once you have a base area and
  a steady food supply, i.e. after this page (*timing: judgement*).
- **Don't leave the quest book closed.** Of everything on this page, the one habit worth
  forming in the first hour is checking the book before wandering off — the opening
  chapter pays materials for things you were going to do anyway.

## What this page deliberately does not tell you

- **Recipes.** Not one, not for a crafting table, a wooden pickaxe or an ore hammer. JEI,
  in-game.
- **Counts beyond the quoted ones.** The numbers in the tables are the config's own task
  and reward counts, presented as pack 8.2's. Anything not quoted here is "open the
  entry".
- **Coordinates, y-levels, ore heights, biome lists, or where to walk.** The config says
  none of it, so neither does this page. *The Metal Age*'s own advice is the extent of
  it: grab copper when you see it, and always grab iron.
- **A keybind the config does not name.** Only `M` (the map, from *Claiming Chunks*) and
  the commands `/sethome`, `/home`, `/spawn`, `/rtp`, `/ftbteams party create` appear
  here, because those are the ones the chapter's own text quotes.
- **An official first-hour order.** FTB Quests has no clock and the pack gates nothing —
  *"quests are optional. Mods are not gated behind completing any quests!"*. The route is
  a recommendation built on the config's dependencies; a player who wants to wander off
  and dig is playing the pack exactly as intended.
- **Titles for quests that have none.** Four Welcome entries and several Chapter 1
  entries are untitled in the config; they are marked, not renamed.

## Cross-references

- `references/getting-started.md` — install, Java, RAM, and the wider first-hours
  checklist this page sits inside.
- `references/automation-first-steps.md` — the next five things after hour one, ranked,
  with verified anchors.
- `references/ore-processing-ladder.md` — what *Basic Ore Doubling* leads to.
- `references/chunk-loading-guide.md` — the *Claiming Chunks* quest in full, and the
  chunk loaders this pack's config enables or disables.
- `references/progression-roadmap.md` — where Chapter 1 sits in the recommended order for
  all 66 chapters.
- `references/key-mods.md` — what the mods named here (Iron Furnaces, Pipez, Mekanism,
  Powah, Generator Galore) actually do and when to start them.

---

*This doc was grounded in `config/ftbquests/quests/chapters/welcome.snbt` and
`.../mainquestline_part_1.snbt`, their `lang/en_us/chapters/*.snbt` titles and
descriptions, `chapter_groups.snbt`, `data.snbt`, `lang/en_us/reward_table.snbt`,
`config/ftbultimine-server.snbt`, and `config/bcc-common.toml` from AllTheMods/ATM-10 at
commit `e5e3d1d83e` (pack 8.2, 2026-09-22). Quest titles, ids, task items, counts,
rewards and dependencies are quoted from that config; the ordering rationale and every
timing estimate are judgement. The in-game quest book and JEI are authoritative.*
