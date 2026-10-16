# ATM10: what should I automate first? — the first 5 automations (verified quest titles)

**What this page is.** The beginner's answer to *"what should I automate first?"* for
**All the Mods 10**: five useful first automations — ore processing, power, item
transport, storage, and farms — **ordered by impact for a beginner**, each one anchored
to verified quests from the pack's own quest config. It is a *priorities map*, not a
build guide: it tells you what to aim at first and which quests walk you there, not how
to craft or lay anything out.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, quest id, chapter name, dependency, task item, and quoted
sentence below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/mainquestline_part_1.snbt` | Chapter 1 quests, dependencies, task items |
| `config/ftbquests/quests/chapters/mekanism.snbt`, `basic_power.snbt`, `basic_logistics.snbt`, `storage.snbt` | the Tech / Power / Logistics / Storage chapter quests and links |
| `config/ftbquests/quests/chapters/elmystical_agriculturerr.snbt`, `hostile_neural_networks.snbt`, `productive_bees.snbt`, `industrial_foregoing.snbt`, `food_and_farming.snbt` | the Resources-group and farm chapter quests |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, and description text quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapter titles (e.g. *Chapter 1: The Beginning*) |
| `config/ftbquests/quests/chapter_groups.snbt` + `lang/en_us/chapter_group.snbt` | the quest-book groups (Main Questline, Tech, Resources, Storage, Logistics, Power) |
| `CHANGELOG.md` | the pack version and date: **8.2**, 2026-09-22 |

Quest titles and quoted text are shown with Minecraft's `&` formatting codes stripped,
the way the book renders them. The skill tracks chapters as their config filenames
(`mekanism`, `basic_logistics`, ...); both forms appear below.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs from anything here, his
  book wins — say so, and re-research rather than arguing from this file.
- **Titles are the config's, never invented.** Every quest name in `**bold**` or in the
  anchors table was read from the lang files above. A quest not on this page may still
  exist in the book — the answer for those is "open the chapter in the book", never a
  plausible-sounding guess.
- **The ranking is judgement, not the pack's.** Nothing in the quest config ranks
  automations for you; FTB Quests has no notion of "impact". The order below (and the
  "why this rank" lines) is this skill's judgement for a *beginner* — marked
  *approximate/judgement* throughout. The pack itself says quests are optional and mods
  are not gated, so any working order is legal; a player whose book or playstyle differs
  should trust his own situation.
- **No recipes, no counts, no layouts.** The config lists *what a quest wants* and what
  its own text says — never a recipe tree, an energy budget, or a factory layout. Every
  "how" here is a quote from a quest's description or a pointer to JEI. Do not fill
  anything in from memory or plausibility.
- **Item ids below are quoted from config task entries, never invented** — and only a
  handful appear, exactly where they anchor a claim.
- **Anything uncertain is flagged approximate** (machine tiers, throughput, which mod a
  beginner should pick among alternatives). When repeating such a detail, keep the hedge.

## The short answer

Automate in this order — each step feeds the next, and the whole ladder is what the
book's early chapters are walking you toward:

| Rank | Automate this | Verified anchor quest(s) | Chapter (group) |
|---|---|---|---|
| **1** | **Ore processing** — double (and better) every ore you mine | *Basic Ore Doubling* → *Enrich then Smelt* → *Enrichment Chamber* | *Chapter 1: The Beginning* (Main Questline), then *Mekanism* (Tech) |
| **2** | **Power** — steady energy for the machines above | *Lava Power* → *Wind Power* / *Solar Power*; *Early Game Power Options* | *Chapter 1: The Beginning*, then *Basic Power* (Power) |
| **3** | **Item transport** — move items between machines and chests hands-free | *Pipez* → *Item Pipez*; *Logistical Transporters* | *Basic Logistics* (Logistics), *Mekanism* (Tech) |
| **4** | **Storage** — make the influx storable and self-managing | *Basic Storage* → *Sophisticated Storage* → *Auto-Smelting Upgrade* | *Basic Storage* (Storage) |
| **5** | **Farms & renewable resources** — grow food and materials instead of gathering | *Mystical Agriculture!* → *Inferium*; alternatives *Simulating Deaths*, *Productive Bees!* | *Mystical Agriculture*, *Hostile Neural Networks*, *Productive Bees* (Resources) |

**If you only do one thing: automate ore processing first.** The book itself puts
*Basic Ore Doubling* right behind *The Metal Age* (dependency verified in the config) —
it is the earliest "make my time back" quest in the pack. The rest of the list is the
supporting cast: power keeps the machines running, transport makes them a line, storage
catches what they produce, and farms eventually remove the gathering entirely.

*The ranking is judgement (marked approximate); the quest titles, ids, chapters, and
quotes are verified against the pack 8.2 config, and the in-game quest book is
authoritative for what any quest actually requires.*

## 1. Ore processing — double what you mine *(highest impact; judgement)*

**Why this rank (judgement).** Ore processing multiplies the output of *every* mining
trip you will ever take, from the first iron vein to the ATM Star's material bill — no
other early automation compounds like it. The pack agrees on the timing: *Basic Ore
Doubling* depends directly on *The Metal Age* (verified in the config), so the book
introduces it in the first hours, in *Chapter 1: The Beginning* (Main Questline, 36
quests).

**The verified trail.**

| Verified quest title | Quest id | What the config shows |
|---|---|---|
| **The Metal Age** | `051E0C85E7B71CE0` | Chapter 1; tasks `minecraft:iron_ingot`, `minecraft:copper_ingot` — the dep of the next quest |
| **Basic Ore Doubling** | `4E5238F00CEED8B2` | Chapter 1; depends on *The Metal Age* |
| **Enrich then Smelt** | `119BED334E331C25` | *Mekanism* (90 quests); subtitle *Tier 1 Ore Processing* |
| **Enrichment Chamber** | `08DDE018A804BFE7` | *Mekanism*; subtitle *Breaks Raw Ores into Dusts*; task `mekanism:enrichment_chamber` |
| **Crusher** | `7AE502EDB73BD57A` | *Mekanism*; subtitle *It Crushes Things.*; task `mekanism:crusher` |
| **Energized Smelter** | `488DBE69595F38F8` | *Mekanism*; subtitle *Mekanism's Powered Furnace*; task `mekanism:energized_smelter` |

What the quest text says, quoted:

- **Basic Ore Doubling** — *"Smelting down raw ores in the beginning is necessary, but
  you are missing out on extra resources!"*; *"There are several ways to double your
  output per raw ore, but one of the easiest ways is by creating and using an Ore
  Hammer."*; *"These will break down 1 raw ore into 2 ore dust, which can be smelted into
  ingots, effectively doubling your ingot output!"*; and a pointer to a second route:
  *"Want more per raw ore? Check out the mod Occultism!"* (Occultism has its own chapter,
  Magic group — the quest book is the map for it, not this page.)
- **Enrich then Smelt** (subtitle *Tier 1 Ore Processing*) — *"The very first and
  simplest Ore Processing is just 2 Machines! Enrichers and Smelters! We can use Ore
  Blocks to get twice the Dust or Raw Ore to get 1/3 more. So 3 Raw Ore to get 4 Dust."*,
  ending *"Congrats, you just Ore Processed!"* — the raw figures are that quest text's
  own; confirm in the entry if they matter.
- **Enrichment Chamber** — *"We can get 2 Dust from 1 Ore."* (quest text), with the
  subtitle *Breaks Raw Ores into Dusts*.

**The ladder beyond Tier 1.** The *Mekanism* chapter carries the full processing line,
each stage marked by the config's own subtitles: *Tier 1 Ore Processing* on **Enrich then
Smelt**, *Tier 2 Ore Processing* on **Crush and Enrich our Clumps** and **Making Oxygen
for Purifier**, *Tier 3 Ore Processing* on **Injecting Hydrogen Chloride** and **Shard,
to Clump, to Dust, to Ingot**, *Tier 4 Ore Processing* on **Creating Sulfuric Acid**,
**Melting Ores with Acid and Crystallizing them**, and **Crystal, Shard, Clump, ETC**.
The machines that gate the tiers are quests in the same chapter — **Purification
Chamber**, **Chemical Injection Chamber**, **Chemical Dissolution Chamber**,
**Chemical Crystallizer** — each depending on the previous tier's machine line
(dependencies verified). Which tier to stop at for a given point in the game is
*approximate/judgement*; the quest entries and JEI say what each step costs.

**Other routes in the book (alternatives, not a sequence).** *Industrial Foregoing*
(Tech) has its own ore-processing line — three untitled quests subtitled *Ore Processing:
Step 1*, *Ore Processing: Step 2*, and *Ore Processing: Step 3* (no title in the config;
the book shows them by their task items), hung on its machine-frame ladder (Steps 1 and
3 depend on *Advanced Machine Frame*, Step 2 on *Simple Machine Frame* — dependencies
verified). Treat Mekanism vs Industrial Foregoing vs Create as alternatives with
trade-offs and let the player pick; the pack gates nothing.

## 2. Power — keep the machines running *(prerequisite for everything above; judgement)*

**Why this rank (judgement).** The processing line and everything after it runs on
energy, so a beginner's second automation should be generators plus the wiring to feed
the machines. The book spends *Chapter 1* on three starter generators, then hands you a
whole Power group (Basic Power, Generators N Furnaces, Powah, Extreme Reactors) when
you outgrow them.

**The verified trail.**

| Verified quest title | Quest id | What the config shows |
|---|---|---|
| **Lava Bucket** | `72E1C19156633391` | Chapter 1; the dep of *Lava Power* |
| **Lava Power** | `346860B8EBC4C28C` | Chapter 1; depends on *Lava Bucket* |
| **Wind Power** | `2CCAA7C0FEDEB573` | Chapter 1; depends on *Lava Power*; task `mekanismgenerators:wind_generator` |
| **Solar Power** | `3B6F1BD64C0C570F` | Chapter 1; depends on *Lava Power* |
| **Generators Galore** | `790EC3EDC2DB1FB0` | Chapter 1; the mod-addition quest for that generator pack |
| **Basic Power** | `4AB0DD227471FDBF` | *Basic Power* chapter root (34 quests); subtitle *All The Power!* |
| **Early Game Power Options** | `42D173B9FF8D16E4` | *Basic Power*; subtitle *Starter Power*; depends on *Basic Power* |
| **Transferring Power** | `1F81EA5E45424308` | *Basic Power*; depends on *Basic Power* |
| **Storing Power** | `76EA017B12E8F01B` | *Basic Power*; depends on *Basic Power* |

What the quest text says, quoted:

- **Lava Power** — *"Now that you have all this lava what will you do with it? More
  early game power!"*
- **Wind Power** — *"If you are like most this is the power you are after. All you do is
  place it as high as you can and get free power."*
- **Solar Power** — *"Just like wind generation this will give you lots of power without
  giving it any resources. The only downside here is it has to be daytime."*
- **Generators Galore** — *"As was mentioned before, this mod adds a ton of fun ways to
  generate power that require specific builds."*
- **Basic Power** (root) — *"This chapter is dedicated to all things power related!
  Here you'll find the basic ways to generate, store, and transfer power."*
- **Early Game Power Options** — *"These are good ways to get you started with
  generating power. These don't produce a ton of power, but they are typically easy or
  cheap to get in the early game!"*
- **Transferring Power** — *"There are several options, both wired and wireless, for
  transferring power."* **Storing Power** — *"This section shows you different ways to
  store your power!"* — both are section-style quests: the chapters behind them (Mekanism
  cables, Pipez energy pipes, Flux Networks, energy cells) are the actual menus.

Which generator to commit to (lava, wind, solar, a Powah line, a reactor) is
*approximate/judgement* — the book deliberately offers alternatives.

## 3. Item transport — move things without hoppers *(the enabler; judgement)*

**Why this rank (judgement).** Transport is what turns "machines I feed by hand" into
"lines that run themselves". It is cheap relative to everything else, and the two
previous steps (ore processing + power) become hands-free the moment items can flow.

**The verified trail.** *Basic Logistics* (Logistics group, 40 quests) is built for
exactly this question, and its root quest defines the job:

- **Logistics** (`6CD7D99AA102A5C3`) — *"Logistics: A system of moving, managing, and
  storing items or resources. In Modded Minecraft it's quite the same, moving items!"*
  and *"you'll need to move items from factories, machines, farms, and especially
  chests. That's what Logistics is for."*
- **Pipez** (`2329AA0AFBEF1E13`) — the chapter's starter mod: *"Pipez is the simplest
  Logistics Mod."* → **Item Pipez** (`36836AD948F96B9F`): *"The simplest of the simplest
  of Pipes, the Item Pipe. It will move Items from one Inventory to another. Could be
  from one Chest to another, could be a Farm to a System, or even a Quarry to a
  Smelter."* Then **Fluid Pipez** (`33433A443B65D252`) and **Energy Pipez**
  (`53EC96FA0E7C4ED4`), converging on **Universal Pipez** (`4FBAB3A0FBF8CE2F`,
  depends on all three — verified). Tasks are the config's: `pipez:wrench`,
  `pipez:item_pipe`, `pipez:fluid_pipe`, `pipez:energy_pipe`, `pipez:universal_pipe`.
- **Alternatives in the same chapter (pick one, the pack gates nothing):** **Laser IO**
  (`5F1218CF8EFC607B`, task `laserio:logic_chip`) — card-based nodes; **Integrated
  Dynamics** (`6E05B62A40D5A891`, task `integrateddynamics:wrench`) — programmable
  cables and tunnels (*Item Importing* and friends hang off it).
- **The Mekanism way** (Tech group): **Mekanism Logistics** (subtitle *The Configurator*,
  task `mekanism:configurator`) branches to **Logistical Transporters** (subtitle
  *Items*) and **Mechanical Pipes** (subtitle *Fluids*). The transporter quest text
  spells out the machine-side part: *"Logistical Transporters will move Items and Blocks
  from one Inventory to another!"* and *"In order to move Items to Machines though, we'll
  need to change the Configs within the Machine. ... Side Configs. They'll need to be set
  to Auto-Eject to Output Items."* **Mechanical Pipes** — *"Mechanical Pipes will move
  Fluids."*

Pipez vs Laser IO vs Integrated Dynamics vs Mekanism transporters is an
*approximate/judgement* trade-off (simplicity vs control vs cross-mod polish); present
them as alternatives and let the player pick.

## 4. Storage — make the influx work for you *(capture the output; judgement)*

**Why this rank (judgement).** The first three steps produce more items than wooden
chests can absorb; storage is where a beginner's throughput otherwise leaks back into
sorting chores. The *Basic Storage* chapter (Storage group, 90 quests) is deliberately
power-free and upgrade-driven — ideal to automate early.

**The verified trail.**

| Verified quest title | Quest id | What the config shows |
|---|---|---|
| **Basic Storage** | `5A94A2664BFDD7B9` | chapter root — *"all of the basic ways to store items without needing power"* |
| **Sophisticated Storage** | `5E4BC0F59C90433A` | subtitle *"Vanilla Chest"*; upgradeable chests/barrels |
| **Functional Storage** | `0682DC1F2417DAEB` | subtitle *Storage Drawers Distant Relative*; drawers-style bulk storage |
| **Auto-Smelting Upgrade** | `3A1D07AED2A841E4` | subtitle *Automatic*; task `sophisticatedbackpacks:auto_smelting_upgrade` |
| **Stack Upgrade Tier 1** | `7E9E03274A88347D` | capacity upgrade (later tiers in the same chapter) |
| **Advanced Void Upgrade** | `2FC15D3916DBF4E4` | overflow control (subtitle *More Filtering Options*) |

What the quest text says, quoted:

- **Basic Storage** — *"Welcome to the Basic Storage Chapter! You'll find all of the
  basic ways to store items without needing power, as well as useful items for your
  storage needs!"*
- **Sophisticated Storage** — *"Sophisticated Storage allows you to upgrade your Chests
  and Barrels with metals to increase their storage! You can also add upgrades to
  increase their functionality."*
- **Auto-Smelting Upgrade** — the whole quest text is *"Auto-smelt items in the
  Backpack."* — a small automation that quietly applies #1 to whatever you carry.

When the book's storage chapter stops scaling, the next decision is a digital network —
**Applied Energistics 2 vs Refined Storage**, both fully quested (Storage group:
*Applied Energistics 2*, *Extended & Advanced AE*, *Refined Storage*). That choice is
*approximate/judgement*; per this skill's rules, present them as alternatives with
trade-offs and let the player pick — never call one "required".

## 5. Farms & renewable resources — stop gathering by hand *(the long game; judgement)*

**Why this rank (judgement).** Last on this list only because it ramps up *after* the
line above exists to process and store its output; in payoff it is the biggest of the
five long-term. The Resources group (Food and Farming, Hostile Neural Networks,
Mystical Agriculture, Productive Bees, Productive Trees) is where the pack keeps its
resource factories, and the community-guidance doc in this skill already flags
Mystical Agriculture as the highest-leverage farm (*approximate — guides say; verify
in-game*).

**Food first if you haven't.** *Food and Farming* (Resources, 35 quests) has the everyday
case: the quest **The Planter** (`43021923E220CF68`) is subtitled *"Wait until you get
Machines for this..."* — i.e. the book itself tells you machine farming comes once you
have machines. The scalable food answer sits in **Industrial Foregoing** (Tech):
**Plants** (`6C001E18093FC037`) tasks `industrialforegoing:plant_gatherer` and
`industrialforegoing:plant_sower`, and its text says *"The Plant Gatherer harvests plants
in its working area."* and *"When supplied with Ether Gas, the Plant Gatherer will
automatically replant crops. The Plant Sower automatically plants crops and saplings."*

**Then materials — three verified routes (alternatives, not a ladder):**

1. **Mystical Agriculture** (Resources, 191 quests) — grow ores and mob drops from
   seeds. Root quest **Mystical Agriculture!** (`54735C5FCD2077B3`): *"Mystical
   Agriculture is a resource generation mod that allows you to grow a large variety of
   vanilla and modded resources using Seeds."* The first steps, verified:
   **Inferium** (subtitle *Tier: 1*, depends on *Mystical Agriculture!*) — *"Inferium
   Essence is the base tier of all essences. You can get this from mining, killing mobs,
   or by making seeds to grow them!"* — feeding **Inferium Growth Accelerator**
   (subtitle *Range: 9 Blocks*, depends on *Inferium*, task
   `mysticalagriculture:inferium_growth_accelerator`); the seed-making side hangs off
   the same root quest: **Prosperity Shards** → **Prosperity Seed Base** →
   **Infusion Altar** (subtitle *Creating Seeds*, tasks `mysticalagriculture:infusion_altar`,
   `mysticalagriculture:infusion_pedestal` ×8 — the config's count), dependencies
   verified. Which crops to grow first and when to stop is *approximate/judgement*.
2. **Hostile Neural Networks** (Resources, 50 quests) — automate mob loot without a
   spawner room. The verified chain: **Welcome to Hostile Neural Networks!** →
   **Learning Mobs** (subtitle *The Learning HUD*, task `hostilenetworks:deep_learner`)
   + **Modeling Mobs** (task `hostilenetworks:blank_data_model`) → **Simulating Deaths**
   (tasks `hostilenetworks:sim_chamber`, `hostilenetworks:prediction_matrix`) →
   **Creating Loot** (task `hostilenetworks:loot_fabricator`) → **The Data Center**.
   Quest text, quoted: *"The Simulation Chamber is the main machine within HNN. When
   given power, it will run simulations based on the Data Model that is placed inside."*
   and *"The Loot Fabricator is the machine that gets you that sweet, sweet loot from
   Mob Predictions. ... The machine will remember your choice, so it can be automated."* —
   its own examples: *"Ender Dragons for Dragon Eggs"*, *"Zombies for Iron"*, *"Withers
   for Nether Stars"*.
3. **Productive Bees** (Resources, 252 quests) — passive generation from bees. Root
   quest **Productive Bees!** (`13AA91D39A2CABF2`): *"To get started with the mod,
   you'll first need to find some Honeycombs and Honey Bottles!"* — with the pack's own
   pointer: *"Make sure to look them up in JEI if you need them!"* Then **Searching for
   Nests** (task `productivebees:nest_locator`) and **Your First Beehive** (`109AD73F016D576B`):
   *"Using the vanilla method, go ahead and make yourself a Beehive to have your own
   little setup! These can hold 3 Bees each, but we won't be using it for long..."*

**The mid-game goal to keep in view:** Industrial Foregoing's **Laser Drill**
(`418E57E34FFC19E1`, subtitle *Void Miner*, tasks `industrialforegoing:laser_drill` ×4
plus `industrialforegoing:ore_laser_base` and `industrialforegoing:fluid_laser_base`)
gated behind its **Advanced Machine Frame** — a void-based ore generator once the early
line is humming. *Approximate timing (mid-game) — judgement; the entry is authoritative.*

## How the ranking was decided (and how to disagree)

*Judgement, stated openly: nothing in the pack ranks automations.* The order above is
this skill's recommendation for a beginner, weighing three things: how early the pack
lets you start it (verified dependencies), how much manual work it removes per hour
spent, and whether it multiplies everything after it. Under that lens ore processing
earns #1 (compounding multiplier, day-one availability), power and transport are the
prerequisites the machines need, storage catches the output, and farms convert the whole
system from "gather-process" to "renewable". A different playstyle legitimately
reorders it — a player dying to hunger automates food first; a builder on a server
picks storage earlier. When advising, say which part is verified (titles, ids,
chapters, quotes) and which is the judgement call (the ranking itself), and let the
in-game quest book — which is authoritative — settle anything concrete.

## Next after these five

- **A digital storage network** — AE2 vs Refined Storage (see #4), then autocrafting.
- **The rest of the Mekanism ladder** — tiers 2–4 (see #1), plus *Mekanism: Reactors*
  when power demand outgrows starters.
- **Loot and resource scale-out** — *The Data Center* (HNN), more bees, Mystical
  Agriculture's tier essences, the *Laser Drill*.
- **Automating the ATM Star itself** — the post-star question gets its own page:
  `references/creative-checklist.md` maps Chapter 4's automation multiblocks and the
  terminal quest *Fully Automated ATM Star*, in dependency order, with verified titles.

## Cross-references

- `references/item-fluid-transport-guide.md` — the dedicated follow-up to #3: choosing
  item/fluid transport, extraction, filters, and diagnosing a stalled connection.

- `references/progression.md` — the four stages and quest-book order this ranking sits
  inside.
- `references/getting-started.md` — first hours and setup (the quests before #1 even
  start).
- `references/key-mods.md` — what Mekanism, Pipez-adjacent logistics mods, AE2/RS, and
  the farm mods each do, when to start them, what they lead to.
- `references/creative-checklist.md` — the endgame version of this question: automating
  the star.

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item named here is a quest *task* or a quote; JEI has the
  recipe, and recipes are where pack versions differ most.
- **Counts and numbers beyond quotes.** Figures like "2 Dust from 1 Ore" appear only as
  quoted quest text, attributed as such; anything this page does not quote is "check the
  quest entry / JEI".
- **Machine tiers, energy amounts, throughput, layouts, coordinates.** The page stays
  out; the quests' own descriptions cover them in-game (quoted where quoted).
- **An official order.** The pack does not rank automations; the 1–5 ladder is this
  skill's judgement, marked approximate, and the in-game quest book overrides it.
- **Anything not in the config.** If a player names an automation, machine, or mod this
  page does not list, the answer is "open that chapter in the book / look it up in JEI"
  — never a guess.
