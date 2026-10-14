# Farming guide — what to farm in ATM10, and what to set up first (verified quest titles)

**What this page is.** The farming map for **All the Mods 10**: which quest chapters farm
what, the order the config gives each farm's tiers in, and a short, marked-as-judgement
answer to the beginner question **what should I set up farming first?** It covers
Mystical Agriculture's essence and seed tiers, the three mob-farm routes (spawners,
Industrial Foregoing's machines, Hostile Neural Networks' simulations), what the pack does
— and does not — have in place of resource chickens, Productive Bees and Productive Trees,
and the crop and food quests. It is a *map of the farming quests*, not a crafting guide.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, quest id, task item, count, dependency, and quoted sentence
below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** (`config/bcc-common.toml` stamps
the same `modpackVersion`) — the "8.x" that `examples/progress.example.json` is stamped
with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/<id>.snbt` for the eight farming chapters: `elmystical_agriculturerr`, `apotheosis_2`, `hostile_neural_networks`, `productive_bees`, `productive_trees`, `food_and_farming`, `industrial_foregoing`, `pylons` | every quest's id, task items and required counts, dependency links, and optional/hidden flags |
| `config/ftbquests/quests/lang/en_us/chapters/<id>.snbt` for the same chapters | the English quest titles, subtitles, and the description text quoted below |
| the same two files for `tips_and_tricks`, `chapter_2_the_star` (*Chapter 3: The ATM Star*), `allthemodium` (*Chapter 2: Allthemodium*), `basic_power`, `generators`, `pneumaticcraft`, `immersive_engineering`, `building_tips` | the farming quests and sentences that live outside the farming chapters (each named where it is used) |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapters' own titles and subtitles |
| `config/ftbquests/quests/lang/en_us/chapter_group.snbt` | the quest-book groups the chapters sit in (`Resources`, `Tech`, `Logistics`) |
| `config/crash_assistant/modlist.json` | verified mod display names and versions — and the *absence* of any resource-chicken mod |

The chapters were parsed with this skill's own `scripts/snbt.py`. A chapter id below is
the config's filename, which is also the id `examples/progress.example.json` tracks it by.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids and counts below are quoted from the config, never invented.** A count (×4)
  is shown only where the config states one; where a quest asks for one item, no count is
  printed.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Every
  "how" on this page is a quote from that quest's own description, marked as such, or a
  pointer to JEI. Do not fill a recipe, a growth rate, a drop chance, or an energy cost in
  from memory or plausibility.
- **Approximate means approximate.** Mod names and versions are the modlist's; which crop
  a harvester accepts, how fast anything grows, and which farm layout works are
  version-sensitive and not in the config — anything not quoted from it is flagged as
  approximate.
- **Titles are the config's.** Farming chapters lean on untitled quests: 138 of Mystical
  Agriculture's 191 quests have no title (every seed quest is identified only by a `Tier:`
  subtitle), and Productive Trees titles 5 of its 167. Such quests are marked *(no title
  in the config)*, with the subtitle when the config gives one — the book then shows the
  task item's own name. Do not present a derived name as a verified title.
- **The "what first" order is judgement, and labelled so.** The config links quests into
  a graph *inside* each chapter; it does not order the farming chapters against each
  other. Every step marked **judgement** is this page's advice, built on the verified facts
  printed next to it.
- **Nothing here was invented, and nothing is added from memory.** A farm, seed, mob, or
  mod that is not on this page is "open the quest book / look it up in JEI", never a
  plausible-sounding guess.

## The farming chapters at a glance

| Chapter (book title) | Chapter id (config filename) | Book group | Quests | Titled | What it farms |
|---|---|---|---|---|---|
| **Apothic Spawners** — subtitle *And Other Spawners* | `apotheosis_2` | Resources | 36 | 14 | mob spawners, their modifier runes, and seven other mods' spawners |
| **Food and Farming** | `food_and_farming` | Resources | 35 | 31 | crops, animals, fishing, the kitchen |
| **Hostile Neural Networks** | `hostile_neural_networks` | Resources | 50 | 7 | mob drops by simulation — no live mobs |
| **Mystical Agriculture** | `elmystical_agriculturerr` | Resources | 191 | 53 | resource crops, in essence tiers |
| **Productive Bees** | `productive_bees` | Resources | 252 | 195 | resource bees and their combs |
| **Productive Trees** | `productive_trees` | Resources | 167 | 5 | bred trees, pollinated by bees |
| **Industrial Foregoing** | `industrial_foregoing` | Tech | 78 | 24 | machine-run mob, animal, and crop farms |
| **Pylons** | `pylons` | Logistics | 13 | 1 | the Harvester Pylon auto-farm |

Each of these chapters also carries exactly one invisible quest — an "AllRightsReserved"
licence notice that only shows in the book's editing mode — and the counts above include
it. The Resources group lists its six chapters in the order of the table's first six rows
(`order_index` 0–5). This skill's stage map (`references/progression.md`, itself
approximate) files Food and Farming and Apothic Spawners under **early game** and the
other four Resources chapters under **tech**.

## What should I set up farming first? (the short answer)

**In one line (judgement):** food today, Mystical Agriculture's Inferium this week, a
harvester once the plot grows, then one mob-drop route, then bees — and trees after the
bees. Resource chickens are not in this pack.

The order is **judgement** — the pack does not sequence its farming chapters — but each
step stands on the verified quests named in it:

1. **Food, on day one — Food and Farming.** Five of its quests have no prerequisites at
   all (*Food and Farming*, *The Planter*, *We're doing this the Old Fashioned way*,
   *Making a Kitchen, with a Book*, *The Start of a Fisher*), and the wheat line is short:
   **The Planter** (any hoe) → **Punch the Grass** (`minecraft:wheat_seeds` ×8) →
   **Wheat** (`minecraft:wheat` ×3) → **The Bread of Life** (`minecraft:bread` ×3).
2. **Mystical Agriculture's Inferium — as early as you can.** That is the pack's own
   advice, in the **Inferium Farmland** quest: *"You'll want to start growing Inferium as
   soon as you can!"* The chapter's entry quest, **Mystical Agriculture!**, has no
   prerequisites and asks only for any seeds (item tag `c:seeds`), and **Inferium** says
   the essence comes *"from mining, killing mobs, or by making seeds to grow them!"* The
   first resource seeds need two short lines finished: **Inferium** → **Inferium
   Farmland**, and **Prosperity Shards** (*"To find some Prosperity Ore, go mining."*) →
   **Prosperity Seed Base** → **Infusion Altar**. Why so early: the star. Chapter 3's
   *Mystical Agriculture* quest says *"You'll need to do a lot of farming with this mod to
   make the ATM Star!"*, and its *4 Insanium Blocks* quest does the arithmetic: *"So
   you'll need 36,864 Inferium Essence total!"*
3. **Automate the harvest once a plot is growing.** Among the crop auto-harvesters the
   quest book teaches are the Harvester Pylon (Pylons chapter — it needs the **Pylons**
   quest and a hoe), Mystical Agriculture's own Harvester (behind that chapter's Scythes
   quest), and Industrial Foregoing's **Plants** pair (Plant Gatherer + Plant Sower,
   behind its Plastic quest); more automatic farms (the Garden Cloche, the Hydroponic Bed)
   are under *Crops and food* below. **Judgement:** take the one whose chapter you have
   already opened. *Which* crops each accepts — Mystical Agriculture's included — is not
   stated in the config: check in-game (approximate).
4. **Mob drops: pick one route.** A spawner farm (**Apothic Spawners** — the chapter
   starts from a vanilla `minecraft:spawner`, which its first quest says you can mine with
   Silk Touch), a machine farm (Industrial Foregoing — Mob Slaughter Factory after its
   Plastic quest; Mob Crusher and Mob Duplicator after **Advanced Machine Frame**), or a
   simulation (**Hostile Neural Networks** — Chapter 3's hub quest for it: *"Hostile Neural
   Networks is all about simulating Mobs for farming their Loot!"*). **Judgement:**
   simulation when you want drops without a live mob farm; the star's own quests reach for
   it — *The Star's Casing*: *"(Please I am begging you use HNN just don't spawn and kill
   111,537, please!)"*
5. **Bees, then Trees.** This order is not judgement — the quest text sets it (no
   dependency links the two chapters). **Productive Trees**: *"To get Pollinated Leaves you
   need Pollen. For Pollen you need Bees."* Bees also farm Mystical Agriculture's essences
   (the essence bees, below).
6. **Resource chickens: skip — pack 8.2 has none.** See *Resource chickens* below for what
   does that job here.

## Mystical Agriculture — `elmystical_agriculturerr` (191 quests)

Mystical Agriculture 8.0.28, with Mystical Agradditions 8.0.14 (Tier 6 — Insanium — and
the cruxes) and Cucumber Library 8.0.16 (whose `cucumber:scythes` item tag one tool quest
uses). Chapter icon `mysticalagradditions:insanium_essence`. 53 of the 191 quests carry a
title, and 6 are optional: **Mystical Fertilizer**, **Enchanter**, **Wand**, **Witherproof
Blocks**, **Automating Awakened Supremium**, and the hidden notice.

### Getting in: the two entry lines

| Verified quest title | Quest id | Task items in the config | Needs |
|---|---|---|---|
| **Mystical Agriculture!** | `54735C5FCD2077B3` | any item in tag `c:seeds` (task *Seeds*) | nothing |
| **Inferium** | `1CC4F8570A7A99EB` | `mysticalagriculture:inferium_essence` | Mystical Agriculture! |
| **Inferium Farmland** | `7DFF18CFEB0B8DBE` | `mysticalagriculture:inferium_farmland`, `mysticalagriculture:inferium_seeds` | Inferium |
| **Infusion Crystal** | `217DB12EA32E1724` | `mysticalagriculture:infusion_crystal` | Inferium |
| **Prosperity Shards** | `2DDA04088C8220D2` | `mysticalagriculture:prosperity_shard` ×4 | Mystical Agriculture! |
| **Prosperity Seed Base** | `1E0F92F07FDD162E` | `mysticalagriculture:prosperity_seed_base` | Prosperity Shards |
| **Infusion Altar** | `0B37355262121DD5` | `mysticalagriculture:infusion_altar`, `mysticalagriculture:infusion_pedestal` ×8 | Prosperity Seed Base |

Quoted: *"The Infusion Altar is how you make all of the seeds."*, and *"In order for the
Infusing to start, the Alter requires a Redstone signal."* (sic). The optional **Wand**
quest (`mysticalagriculture:wand`, needs *Inferium*): *"The Wand can be used to activate
the Infusion Alter, just right-click on the altar to activate the infusion process."*

### The essence tiers, in the config's order

Each tier's quest carries its tier as a subtitle, and the **Needs** column is the quest's
actual dependency: Prudentium hangs off *Infusion Crystal* (which hangs off Inferium), and
Insanium hangs off Supremium — not off the awakened tier.

| Tier (subtitle) | Verified quest title | Quest id | Task item | Needs | Growth accelerator quest (subtitle) | Farmland quest |
|---|---|---|---|---|---|---|
| `Tier: 1` | **Inferium** | `1CC4F8570A7A99EB` | `mysticalagriculture:inferium_essence` | Mystical Agriculture! | Inferium Growth Accelerator (*Range: 9 Blocks*) | Inferium Farmland |
| `Tier: 2` | **Prudentium** | `73350AD668200E99` | `mysticalagriculture:prudentium_essence` | Infusion Crystal | Prudentium Growth Accelerator (*Range: 18 Blocks*) | Prudentium Farmland |
| `Tier: 3` | **Tertium** | `2C9C9CB71941DC01` | `mysticalagriculture:tertium_essence` | Prudentium | Tertium Growth Accelerator (*Range: 27 Blocks*) | Tertium Farmland |
| `Tier: 4` | **Imperium** | `66C52B137A4FF869` | `mysticalagriculture:imperium_essence` | Tertium | Imperium Growth Accelerator (*Range: 36 Blocks*) | Imperium Farmland |
| `Tier: 5` | **Supremium** | `67DBE6C59C0D9D1B` | `mysticalagriculture:supremium_essence` | Imperium | Supremium Growth Accelerator (*Range: 45 Blocks*) | Supremium Farmland |
| `Tier: 5 - Awakened` | **Awakened Supremium** | `7A103577EAE7B3F1` | `mysticalagriculture:awakened_supremium_essence` | The Awakening **and** Cognizant Dust | Awakened Supremium Growth Accelerator (*Range: 54 Blocks*) | — |
| `Tier: 6` | **Insanium** | `202B1F54D3F06DAB` | `mysticalagradditions:insanium_essence` | Supremium | — | Insanium Farmland |
| `Tier: Creative` | **Creative Essence** | `6D0A876D4E4D35AB` | `mysticalagradditions:creative_essence` | Insanium | — | — |

What the tier quests say, quoted: *"This is the Tier 2 Essence, made by combining 4
Inferium together with an Infusion Crystal."* — and the same sentence one tier up for
Tertium and Imperium, and for Insanium: *"This is the Tier 6 Essence, made by combining 4
Supremium together with an Infusion Crystal."* **Supremium's description carries a
typo:** it reads *"This is the Tier 4 Essence, made by combining 4 Imperium together with
an Infusion Crystal."* while its subtitle says `Tier: 5`; the subtitle and the dependency
chain agree on 5.

- **Awakening.** **The Awakening** (`mysticalagriculture:awakening_altar`,
  `mysticalagriculture:awakening_pedestal` ×4, `mysticalagriculture:essence_vessel` ×4)
  and **Cognizant Dust** (`mysticalagriculture:cognizant_dust` ×4) both need *Supremium*.
  Quoted: *"This special Dust is dropped from the Wither and the Ender Dragon when killed
  by an Essence Weapon enchanted with Mystical Enlightenment."* — so the awakened tier runs
  through two bosses (see `references/boss-checklist.md`).
- **Growth accelerators.** Quoted from **Inferium Growth Accelerator**: *"Growth
  Accelerators of all tiers provide the same rate of growth ticks. Higher tiers however
  have a larger range, so you can stack more of them below a single plant."*
- **Farmland.** Quoted from **Inferium Farmland**: *"However, certain seeds will require
  certain farmlands to be planted on."*
- **Master Infusion Crystal** (`mysticalagriculture:master_infusion_crystal`, needs
  *Supremium*): *"The Master Infusion Crystal works the same as the Infusion Crystal but it
  never breaks."*

### Which tier is my seed? (all 125 seed quests)

Every seed quest is untitled — the book shows the seed's own item name — carries a
`Tier:` subtitle, and depends on **Infusion Altar** plus one gate. Every seed id is
`mysticalagriculture:<name>_seeds`; the names below are the `<name>` part, exactly as the
config spells it.

| Subtitle | Seed quests | Gate (besides *Infusion Altar*) | Seeds (`mysticalagriculture:<name>_seeds`) |
|---|---|---|---|
| `Tier: 1` | 9 | Inferium Farmland | air, deepslate, dirt, earth, fire, ice, stone, water, wood |
| `Tier: 2` | 17 | Prudentium Farmland | aluminum, amethyst, coal, coral, dye, grains_of_infinity, honey, kivi, limestone, menril, nature, nether, rubber, saltpeter, silicon, sulfur, unexplored_wood |
| `Tier: 2` | 9 | Creating Mob Seeds | armadillo, chicken, cow, fish, pig, sheep, slime, squid, turtle |
| `Tier: 3` | 27 | Tertium Farmland | azure_silver, black_quartz, brass, bronze, certus_quartz, conductive_alloy, copper, copper_alloy, crimson_iron, darkstone, glowstone, graphite, iron, ironwood, lead, nether_quartz, obsidian, prismarine, quartz_enriched_iron, redstone, redstone_alloy, silver, sky_stone, steeleaf, tin, xychorium_gem, zinc |
| `Tier: 3` | 6 | Tertium | creeper, phantom, rabbit, skeleton, spider, zombie |
| `Tier: 4` | 28 | Imperium Farmland | blazing_crystal, compressed_iron, constantan, dark_steel, electrum, end, energetic_alloy, energized_steel, fiery_ingot, fluix, fluorite, gold, hop_graphite, invar, knightmetal, lapis_lazuli, nickel, osmium, peridot, pulsating_alloy, refined_glowstone, refined_obsidian, ruby, sapphire, soularium, soulium, steel, uranium |
| `Tier: 4` | 5 | Imperium | blaze, breeze, enderman, experience, ghast |
| `Tier: 5` | 16 | Supremium Farmland | cyanite, diamond, draconium, emerald, end_steel, enderium, entro, iridium, netherite, niotic_crystal, platinum, sky_steel, spirited_crystal, uraninite, vibrant_alloy, yellorium |
| `Tier: 5` | 1 | Supremium | wither_skeleton |
| `Tier: 6` | 4 | Insanium Farmland | awakened_draconium, dragon_egg, nether_star, nitro_crystal |
| `Tier: Magical` | 3 | Insanium Farmland | allthemodium, unobtainium, vibranium |

Notes, all from the config:

- The rows gated on an essence quest rather than a farmland quest are the mob seeds — plus
  `experience`, whose quest also asks for `mysticalagriculture:experience_capsule`.
  **Creating Mob Seeds** (needs *Prudentium*; `mysticalagriculture:soulium_dagger`,
  `mysticalagriculture:soul_jar` ×4, `mysticalagriculture:soul_extractor`) explains them:
  *"Most seeds are simple to make, but to make Mob Seeds, you'll need to head to the Nether
  to pick up some Soulium."* — and *"Alternatively, you can fill Soul Jars inside of the
  Soul Extractor by inserting a jar and using mob items to fill them."*
- Every `Tier: 6` quest also asks for its matching crux
  (`mysticalagradditions:awakened_draconium_crux`, `mysticalagradditions:dragon_egg_crux`,
  `mysticalagradditions:nether_star_crux`, `mysticalagradditions:nitro_crystal_crux`), and
  every `Tier: Magical` quest asks for `kubejs:magical_soil`. Quoted from **Insanium
  Farmland** (`mysticalagradditions:insanium_farmland`): *"To grow Tier 6 or Magical Seeds
  you need to have a certain Crux placed directly below the Farmland they are growing
  on."*; and from the seed quests: *"Nether Star Seeds require a Nether Star Crux placed
  below in order for them to grow."*, *"Allthemodium Seeds require Magical Soil placed
  below in order for them to grow."*
- With the eight essence quests above, 133 of the chapter's quests carry a `Tier:`
  subtitle.

### Running the farm

| Quest | Task items in the config | Needs | What its text says (quoted) |
|---|---|---|---|
| *(no title in the config)* | item tag `cucumber:scythes` (task *Scythes*) | Mystical Agriculture! | *"Scythes are tools that can farm large areas of crops all at once."* |
| *(no title in the config)* | `mysticalagriculture:harvester` | the Scythes quest | *"The Harvester can auto-harvest crops and re-plant them. Items collected by the Harvester are put into its internal inventory."* |
| *(no title in the config)* | `mysticalagriculture:watering_can` | Mystical Agriculture! | *"Essence Watering cans have the ability of auto-watering."* |
| **Mystical Fertilizer** (optional) | `mysticalagriculture:mystical_fertilizer` | Mystical Agriculture! | *"It instantly grows whatever it is used on to full maturity."* |
| *(no title in the config; subtitle* Recycling!*)* | `mysticalagriculture:seed_reprocessor` | Mystical Agriculture! | *"The Seed Reprocessor can convert essence seeds back into essences."* |
| *(no title in the config)* | any of `mysticalagriculture:inferium_upgrade`, `mysticalagriculture:prudentium_upgrade`, `mysticalagriculture:tertium_upgrade`, `mysticalagriculture:imperium_upgrade`, `mysticalagriculture:supremium_upgrade`, `mysticalagriculture:awakened_supremium_upgrade` (task *Machine Upgrades*) | Prosperity Shards **and** Inferium | *"Machine Upgrades are used to speed Mystical Agriculture machines."* |
| *(no title in the config)* | `mysticalagriculture:soulium_spawner` | Mystical Agriculture! | *"The Soulium Spawner uses mob essences to spawn mobs."* |

### Where the chapter meets the ATM Star

- **Creative Essence**: *"Creative Essence is needed to craft the ATM Star."*
- *(no title in the config)* `mysticalagradditions:insanium_coal_block` (needs
  *Insanium*): *"An Insanium Coal Block is needed to craft the ATM Star."*
- *(no title in the config)* `mysticalagriculture:awakened_supremium_ingot_block` (needs
  *Awakened Supremium*): *"An Awakened Supremium Ingot Block is needed to craft the ATM
  Star."*

Chapter 3's side of these — its *Mystical Agriculture* hub, *4 Insanium Blocks*, *4
Insanium Gemstone Blocks*, *Insanium Coal Block*, and *Awakened Supremium Ingot Block* —
is mapped in `references/atm-star-checklist.md`.

## Mob farms

Three verified routes in three chapters — spawners, machines, simulation — plus Gateways
in Tips and Tricks.

### Apothic Spawners — `apotheosis_2` (36 quests)

Apothic Spawners 1.4.0 (the Apotheosis 8.8.0 family). The chapter's first quest,
**Apothic Spawners** (`minecraft:spawner`, no prerequisites): *"Remember being able to
mine Spawners with Silk Touch? Well it's back thanks to Apotheosis!"*

The modification spine, in dependency order:

1. **Apothic Spawners** → **Blowing up Spawners** (`apotheosis:spawner_chain`,
   `minecraft:tnt`): *"When you blow up a Spawner, it will become highly unstable,
   spawning a large amount of its respective mob, and leaving Spawner Chains behind."*
2. → *(no title in the config; subtitle* Basic Modifications*)* `apotheosis:spawner_rune`:
   *"Spawner Runes are the base material for modifying Spawners."* Eight titled rune
   quests hang off it: **Burning**, **Health**, **Youthful**, **Spawn Range**, **Ignore
   Light**, **Redstone Active**, **Opposite Day** (`minecraft:quartz`), and **Quiet down
   you'll wake up the mobs!**
3. → *(no title in the config; subtitle* Advanced Modifications*)*
   `apotheosis:infused_spawner_rune`: *"We'll need at least 70 Eterna, 30% Quanta, and 50%
   Arcana in an Enchanting Table."* Four titled rune quests hang off it: **Echoing**
   (*"Any mobs spawned will have the loot that they drop multiplied."*), **Ignore
   Players**, **Ignore All Conditions** (*"The must-need for all Spawners."*), and **No
   AI**.

The upgrade-rune ladder — four untitled quests, named and ranked in their own text, each
setting the spawner's stats to fixed values (quoted from the config, where *"20 ticks
equals 1 second"*; the in-game tooltip is authoritative):

| Rank (per the quest text) | Name in the quest text | Task item | Needs | Min / max spawn delay (ticks) | Spawn count | Max entities | Activation range |
|---|---|---|---|---|---|---|---|
| 1st — *"the cheapest, and, of course, weakest"* | Frontiersman's Spawner Upgrade Rune | `apotheosis:frontier_spawner_upgrade_rune` | Basic Modifications | 150 / 600 | 7 | 12 | 24 |
| 2nd | Wayfarer's Spawner Upgrade Rune | `apotheosis:ascent_spawner_upgrade_rune` | Basic Modifications | 100 / 400 | 10 | 18 | 32 |
| 3rd — *"Yes, you'll need to fight a Warden for this."* | Mountaineer's Spawner Upgrade Rune | `apotheosis:summit_spawner_upgrade_rune` | Advanced Modifications | 50 / 200 | 13 | 24 | 40 |
| 4th — *"the 4th and final tier"* | Thundering Spawner Upgrade Rune | `apotheosis:pinnacle_spawner_upgrade_rune` | Advanced Modifications | 20 / 20 | 16 | 32 | 48 |

**Getting spawn eggs.** The chapter's *(no title in the config)* checkmark quest *Spawn
Eggs* (needs *Apothic Spawners*): *"There's a few ways of obtaining Spawn Eggs but once
you do, right click it on a Spawner to change the mobs it spawns."* Five quests hang off
it:

- capturing books (task *Capturing Books* — an enchanted book carrying
  `apothic_spawners:capturing`, levels I–VII): *"Every level gives you a 0.5% chance at
  getting an Egg each kill and the highest level you can normally get is VII (7)."*;
- `mob_grinding_utils:mob_swab` + `mob_grinding_utils:gm_chicken_feed` (Mob Grinding
  Utils 1.1.10+mc1.21.1) — see *Resource chickens* below;
- Mob Charm Fragments (task *Mob Charm Fragments*, `reliquary:mob_charm_fragment`;
  Reliquary Reincarnations 2.0.80);
- `evilcraft:spirit_reanimator` (EvilCraft 1.2.96);
- *(subtitle* That's no Spawn Egg!*)* `apothic_enchanting:occult_ender_lead`, included
  *"due to its ability to bind mobs to Spawners"*.

**Other mods' spawners.** The *(no title in the config)* checkmark quest *Other Spawners*
has no prerequisites (*"These are spawners provided by mods besides Apothic
Spawners."*); its seven quests are untitled, each subtitled with its mod:

| Subtitle | Task items in the config | What its text says it runs on (quoted) |
|---|---|---|
| *EnderIO's Spawner* | `enderio:powered_spawner` | *"First, you'll need a filled Soul Vial and a Broken Spawner."* |
| *Draconic Evolution's Spawner* | `draconicevolution:stabilized_spawner` | *"The better the Core the more mobs spawn and at a faster rate."* |
| *Ars Nouveau's Spawner* | `ars_additions:source_spawner` | *"This spawner will, as its name implies, make use of Source as fuel."* |
| *Mob Grinding Utils' Spawner* | `mob_grinding_utils:entity_spawner`, `mob_grinding_utils:xpsolidifier`, `mob_grinding_utils:solid_xp_mould_baby` | *"It'll need 3 things to work though: a Spawn Egg, XP Jelly Babies, and a Redstone signal."* |
| *Mystical Agriculture's Spawner* | `mysticalagriculture:soulium_spawner` | *"It uses Mob Essence and Energy to spawn the mobs."* |
| *PneumaticCraft's Spawner* | `pneumaticcraft:pressurized_spawner` | *"Once you do that the Spawner will now need Pressure to work, ignores Light Level, and is Redstone Activated."* |
| *Industrial Foregoing's Spawner* | `industrialforegoing:mob_duplicator` | *"It uses Essence along with a mob in a Mob Imprisonment Tool to spawn a copy of that mob."* |

Also off *Apothic Spawners*: *(subtitle* Don't you despawn on me, Mobs*)*
`pneumaticcraft:spawner_agitator` — with Apothic Spawners in the pack, *"it won't change
that but rather will keep spawned mobs from despawning incase you leave the chunks."*
(sic).

### Industrial Foregoing's farm machines — `industrial_foregoing` (Tech group, 78 quests)

Industrial Foregoing 1.21-3.6.39. The chapter tiers its machines by frame, each frame
quest subtitled with its tier: **Industrial Foregoing** (`Tier: 1`,
`industrialforegoing:machine_frame_pity`) → **Simple Machine Frame** (`Tier: 2`) →
**Advanced Machine Frame** (`Tier: 3`) → **Supreme Machine Frame** (`Tier: 4`). The farm
machines, by the quest each needs:

| Quest | Task items in the config | Needs | Quoted |
|---|---|---|---|
| *(no title in the config)* | `industrialforegoing:mob_slaughter_factory` | the Plastic quest *(no title;* `industrialforegoing:plastic`*)* | *"The Mob Slaughter Factory deletes mobs in its working area, and converts that mob into Pink Slime and Liquid Meat."* |
| **Animals** | `industrialforegoing:animal_rancher`, `industrialforegoing:animal_feeder`, `industrialforegoing:animal_baby_separator` | the Plastic quest | *"The Animal Feeder feeds animals so they can breed."* |
| **Plants** | `industrialforegoing:plant_gatherer`, `industrialforegoing:plant_sower` | the Plastic quest | *"When supplied with Ether Gas, the Plant Gatherer will automatically replant crops."* |
| **Sewer** | `industrialforegoing:sewer`, `industrialforegoing:sewage_composter`, `industrialforegoing:sewage_bucket` | the Plastic quest | *"The Sewage Composter can turn Sewage into Fertilizer."* |
| *(no title in the config)* | `industrialforegoing:hydroponic_bed` | Simple Machine Frame | *"The Hydroponic Bed uses Energy and Water to grow crops and saplings planted on it."* |
| *(no title in the config)* | `industrialforegoing:plant_fertilizer` | Simple Machine Frame **and** Sewer | *"Applies Bone Meal or Fertilizer to plants in its working area."* |
| *(no title in the config)* | `industrialforegoing:marine_fisher` | Simple Machine Frame | *"Must be placed above a 3x3 Water pool (or bigger)."* |
| *(no title in the config; subtitle* Endless Gateway Crusher, too*)* | `industrialforegoing:mob_crusher` | Advanced Machine Frame | *"The Mob Crusher deletes mobs in its working area, collecting that mob's loot, as well as converting the Experience that mob would get into Essence."* |
| *(no title in the config)* | `industrialforegoing:mob_duplicator` | Advanced Machine Frame | *"Basically the spawner of Industrial Foregoing."* |
| **Simulated Hydroponic Bed** (*HNN but for crops?*) | `industrialforegoing:hydroponic_simulation_processor`, `industrialforegoing:simulated_hydroponic_bed` | the Hydroponic Bed quest | *"This will use a Hydroponic Simulation Processor and a seed/sapling to grow any crop of your choice...virtually."* |

### Hostile Neural Networks — `hostile_neural_networks` (50 quests): drops without a mob farm

Hostile Neural Networks 6.5.1. The chapter's spine — its seven titled quests:

| Verified quest title | Task items in the config | Needs |
|---|---|---|
| **Welcome to Hostile Neural Networks!** | `minecraft:redstone` | nothing |
| **Learning Mobs** (*The Learning HUD*) | `hostilenetworks:deep_learner` | Welcome to Hostile Neural Networks! |
| **Modeling Mobs** (*"Gathering Data"* — the quote marks are part of the subtitle) | `hostilenetworks:blank_data_model` | Welcome to Hostile Neural Networks! |
| **Leveling Up Data Models** | `hostilenetworks:data_model` (task *Data Models*) | Modeling Mobs **and** Learning Mobs |
| **Simulating Deaths** | `hostilenetworks:sim_chamber`, `hostilenetworks:prediction_matrix` | Learning Mobs **and** Modeling Mobs |
| **Creating Loot** | `hostilenetworks:loot_fabricator` | Simulating Deaths |
| **The Data Center** (*No Generative AI was used to make this quest*) | `hostilenetworks:data_center`, `hostilenetworks:data_center_io_port`, plus obsidian (task *Obsidians*) and black stained glass (task *Black Stained Glass*) | Creating Loot |

- **Data-model tiers named in the config — three, no more.** *"Data Models start out at
  the first tier: Faulty. You'll need to at least level it to Basic if you'd like to run
  some simulations on it!"*, and The Data Center *"is capable of handling 25 Self Aware
  Data Models concurrently"*. Any tier between Basic and Self Aware is the model's in-game
  tooltip, not this page.
- **What it makes**, quoted from **Creating Loot**'s examples: *"Ender Dragons for Dragon
  Eggs"*, *"Zombies for Iron"*, *"Withers for Nether Stars"*.
- **37 mob-prediction quests** hang off *Creating Loot*, one `hostilenetworks:prediction`
  per data model. 33 are optional; the four required ones are the Piglich
  (`hostilenetworks:allthemodium/piglich`), Ender Dragon, Warden, and Wither models. Five
  more untitled quests off *Simulating Deaths* ask for the generalized predictions,
  subtitled *Makes various Overworld / Nether / End / Twilight Forest / Starlight
  Materials* (`hostilenetworks:overworld_prediction`, `hostilenetworks:nether_prediction`,
  `hostilenetworks:end_prediction`, `hostilenetworks:twilight_prediction`,
  `kubejs:starlight_prediction`).

### Gateways (Tips and Tricks)

An untitled Tips and Tricks quest (task *Gateways*, `gateways:gate_pearl`; Gateways To
Eternity 5.1.0): *"Gateways are easy ways to get Passive Mobs and Loot Rewards!"* — but
*"You'll need to Fight off Waves of Monsters."*

## Resource chickens — not in ATM10 8.2

The pack has **no resource-chicken mod and no chicken quest line**. Checked against
`config/crash_assistant/modlist.json` at the pinned commit: of its 489 mod entries, the
only one with "chicken" in its id or name is **CodeChicken Lib** (`codechickenlib`
4.6.1.529) — a code library, not a farming mod — and none of the quest book's 66
chapters is about chickens.

What the quest book *does* ask for that involves a chicken:

| Chapter | Quest | Task items in the config |
|---|---|---|
| Mystical Agriculture | *(no title in the config;* `Tier: 2`*)*, gated on *Creating Mob Seeds* | `mysticalagriculture:chicken_seeds` |
| Hostile Neural Networks | *(no title in the config)*, optional, off *Creating Loot* | `hostilenetworks:prediction` for the `hostilenetworks:chicken` model |
| Food and Farming | **I'm not gonna make an Egg pun** | `minecraft:egg` ×3 |
| Food and Farming | **The Chickens Must Go** (*Yummy Fried Chicken!*; needs the egg quest) | `minecraft:feather` ×10, `minecraft:chicken` ×5 |
| Apothic Spawners, and Tips and Tricks (subtitle *A way to get Spawn Eggs*) | *(no title in the config)* | `mob_grinding_utils:mob_swab`, `mob_grinding_utils:gm_chicken_feed` |

The last one is the opposite of a resource chicken: *"Simply right click a mob with the
Swab then craft Chicken Feed with it, seeds, and a bucket of any kind of XP Fluid."* —
then *"Unfortunately the Chicken won't survive the procedure but hey, Spawn Eggs!"*

**When a player asks for resource chickens:** say they are not in pack 8.2, and point at
what does that job here — Mystical Agriculture's resource seeds, Productive Bees'
resource bees, and Hostile Neural Networks' simulated drops. If his game has resource
chickens, his pack is not 8.2's config: trust his game and re-research.

## Productive Bees and Productive Trees

### Productive Bees — `productive_bees` (252 quests)

Productive Bees 1.21.1-13.13.5 (the bee upgrades are `productivelib:` items; the modlist
has no separate entry for that namespace). The opening spine, all titled:

**Productive Bees!** (`minecraft:honeycomb`, `minecraft:honey_bottle`) → **Capturing
Bees!** (`productivebees:bee_cage` ×4) → **Your First Beehive** (`minecraft:beehive`) →
**Advanced Beehive** (*No more shearing.*; item tag `productivebees:advanced_beehives`) →
**Expansion Box** (item tag `productivebees:expansion_boxes`).

The first quest's warning holds for the whole chapter: *"Important Note: With the bee
quests requiring combs, the recipes will not be shown. Make sure to look them up in JEI if
you need them!"* Combs are processed in a Centrifuge — the untitled *Processing
Honeycombs* quest (task *Centrifuges*): *"While you can definitely just use a regular
Centrifuge in the beginning, getting a Powered Centrifuge soon after is a must."*

Past the hive, an untitled honey-treat quest (`productivebees:honey_treat`) opens three
hubs: *Honey Treats Required* (task *Nest Spawning*; 15 nest quests hang off it — *"If you
want to turn your Bee Farm into a factory for resources, you'll need to start by spawning
in Bees with Nests."*), *The Bees and the Bees* (task *Breeding and Converting Bees*; 186
quests hang off it), and an untitled checkmark (task *Allthemodium Progression*): *"If you
want the ATM bees, it takes a lot of capturing and breeding and feeding."*

Bee lines, as the config titles and subtitles them (a subtitle naming two bees is the
pair the quest's own text says to breed; the comb's products are JEI's):

| Verified quest title | Subtitle in the config | Needs (quest) |
|---|---|---|
| **Iron Bee** | *Ashy Mining + Crystalline* | The Bees and the Bees |
| **Gold Bee** | *Crystalline + Mason* | The Bees and the Bees |
| **Coal Bee** | *Magmatic + Leafcutter* | The Bees and the Bees |
| **Redstone Bee** | *Glowing + Chocolate Mining* | Glowing Bee |
| **Lapis Bee** | *Redstone + Blue Banded* | Redstone Bee |
| **Diamond Bee** | *Ender + Lapis* | Ender Bee **and** Lapis Bee |
| **Emerald Bee** | *Diamond Bee + Slimy Bee* | Diamond Bee **and** Slimy Bee |
| **Ancient Bee** | *Feed Diamond Bee a Block of Netherite* | Diamond Bee |
| **Allthemodium Bee** | — | Ancient Bee |
| **Vibranium Bee** | — | Allthemodium Bee |
| **Unobtainium Bee** | — | Vibranium Bee |

The last three are the ATM-metal ladder; each quest's text names a Foundry pour onto the
previous bee's spawn egg (*"Using a Foundry, pour Molten Allthemodium over an Ancient Bee
Spawn Egg."*).

Mystical Agriculture's essences have bees too: **Inferium Bee**, **Prudentium Bee**,
**Tertium Bee**, **Imperium Bee**, **Supremium Bee**, and **Insanium Bee** (each
subtitled *Infusion Crafting*), and **Awakened Supremium Bee** (*Awakened Crafting*) — all
off *The Bees and the Bees*.

Gene traits get five titled quests off **Gene Samples** (*To make the ultimate bee*):
**Productivity** (*"There are 4 levels of this: Normal, Medium, High, Very High. Very High
is what we are after."*), **Weather Tolerance**, **Behavior**, **Endurance**, and
**Temper**.

### Productive Trees — `productive_trees` (167 quests)

Productive Trees 1.21.1-1.1.1. Only 5 quests carry a title — **Productive Trees**,
**Stripping**, **Sawing**, **Purple Crepe Myrtle Sapling**, and **Moonlight Magic Crepe
Myrtle Sapling**. The rest are untitled sapling quests whose subtitle names the two parent
trees (*Oak + Birch*, *Spruce + Birch*, …) or where the sapling is found (*Bastion
Chests*, *End City Chests*, *Ancient City Chests*, *Shipwreck Chests*, *Desert Pyramid
Chests*, *Cold Ocean Ruin Sus Blocks*).

The entry quest, **Productive Trees** (any vanilla sapling — task *Saplings*), sets the
order with Productive Bees: *"Productive Trees is a sister Mod to Productive Bees."* and
*"For Pollen you need Bees."* Its rewards include a pollen sieve upgrade
(`productivelib:upgrade_pollen_sieve`). Saplings that cannot be pollinated mutate instead
— the *Self Breeding?* quest (task *Self Mutation*): *"These saplings have a random chance
to grow into another tree."*

## Crops and food

### Food and Farming — `food_and_farming` (35 quests)

The chapter's lines, by dependency (all titled unless marked):

- **Crops.** **Food and Farming** (item tag `c:crops`) stands alone. **The Planter**
  (*"To till Dirt into Farmland you'll need a Hoe."*) → **Punch the Grass**
  (`minecraft:wheat_seeds` ×8) → **Wheat** (`minecraft:wheat` ×3) → **The Bread of Life**
  (`minecraft:bread` ×3). *Punch the Grass* also opens **Sugar Sugar**
  (`minecraft:sugar_cane`) → **You're so sweet** (`minecraft:sugar` ×3), and *(no title in
  the config; subtitle* Flax on, Flax off*)* `silentgear:flax_seeds` → **Flax String**
  (`silentgear:flax_string` ×3).
- **Animals.** **We're doing this the Old Fashioned way** (`minecraft:lead`) → **It's
  Clippin' Time** (shears) → **Mary had a Little Lamb** (wool ×3) → **Purchasing Farm
  Supplies** (`farmingforblockheads:market`; Farming for Blockheads 21.1.13: *"Spoiler:
  It's usually just 1 Emerald per item, luckily, they have EVERYTHING."*). The lead quest
  also opens **Leather** (`minecraft:leather` ×3) → **Milk a Cow - Profit**, and **I'm not
  gonna make an Egg pun** → **The Chickens Must Go**.
- **Fishing** (Aquaculture 2 2.7.21). **The Start of a Fisher** (`minecraft:fishing_rod`)
  → **Iron Fishing Rod** → **Golden Fishing Rod** → **Diamond Fishing Rod** → **Neptunium
  Fishing Rod** (`aquaculture:iron_fishing_rod`, `aquaculture:gold_fishing_rod`,
  `aquaculture:diamond_fishing_rod`, `aquaculture:neptunium_fishing_rod`).
- **Kitchen** (Cooking for Blockheads 21.1.24). **Making a Kitchen, with a Book** →
  **Cooking with the power of Diamonds** → **THE BEST THING SINCE SLICED BREAD**
  (`cookingforblockheads:cooking_table`), which opens the kitchen blocks — among them **A
  Cow in a Jar** (*"This block produces milk over time"*) and **The Sink = Infinite
  Water**.

### Other crop helpers the quest book teaches

| Chapter (mod version) | Quest | Task items in the config | Quoted |
|---|---|---|---|
| Pylons (Pylons 5.4.2) | *(no title in the config)* — needs **Pylons** (`minecraft:polished_blackstone`) and a hoe quest (task *Hoes*) | `pylons:harvester_pylon` | *"Harvester Pylons work as a very simple Auto-Farm."*; *"The area can be set to 3x3, 5x5, 7x7, or 9x9 Blocks around the Pylon."*; it *"will need an Inventory like a chest above it to put the Crops"* |
| Immersive Engineering (12.4.2-194) | *(no title in the config)* | `immersiveengineering:cloche` | *"Our beloved Garden Cloche! It is an automatic Farm, and with this Quest is simple to use!"* |
| PneumaticCraft: Repressurized (8.2.23) | *(no title in the config; subtitle* Faster Crops*)* | `pneumaticcraft:crop_support` | *"Crop Supports can be placed over your crops to make them grow faster."* |

The Pylons chapter's five pylons are the Harvester, Infusion, Expulsion, Interdiction,
and Protection Pylons (`pylons:harvester_pylon`, `pylons:infusion_pylon`,
`pylons:expulsion_pylon`, `pylons:interdiction_pylon`, `pylons:protection_pylon`). None of
them is a growth accelerator, and the chapter never mentions Mystical Agriculture — for
faster crops, use the growth options on this page (Growth Accelerators, Mystical
Fertilizer, the Plant Fertilizer, the Crop Support).

### In the modlist, but no quest teaches them

These farming mods are in pack 8.2's modlist yet appear in no quest at all: **BotanyPots**
21.1.44, **BotanyPots-Mystical** 21.1.12, **BotanyTrees** 21.1.7, **Mama's Herbs and
Harvest** 1.21.1-21, **Tree Tap** 1.21.1-0.4.6, and **ModularBees**
1.21.1-3.4-neoforge. Pam's HarvestCraft (Crops 1.0.9, plus its Food Core, Food Extended,
and Trees parts) shows up only as quest icons and rewards, and Farmer's Delight 1.3.4 only
in Building Tips' **Farmer's Delight** quest (any Farmer's Delight block), which treats it
as decoration. For any of these, JEI is the only guide: do not present quest steps for
them.

## How the farming systems connect — only the bridges the config states

| From → to | Where the config says it | Quoted |
|---|---|---|
| Mystical Agriculture → Productive Bees | Mystical Agriculture's optional **Automating Awakened Supremium** (`productivebees:spawn_egg_configurable_bee`, the Awakened Supremium bee) | *"Awakened Supremium and other tiered essences can be farmed using the Productive Bees mod."* |
| Mystical Agriculture → Productive Bees | Productive Bees' **Craftable flowers** (a rose bush, peony, lilac, or sunflower) | its subtitle, *"2 tall flowers can be crafted with MA Essence"* |
| Productive Bees → Productive Trees | **Productive Trees** (the entry quest), and Chapter 3's *Productive Trees* | *"For Pollen you need Bees."*; *"No, Trees do not use Wheat to breed, they use Bees."* |
| Mystical Agriculture → spawners | Apothic Spawners' *Mystical Agriculture's Spawner* | *"Mob Essence is gotten through harvesting Mob Plants, made by Soul Jars."* |
| HNN or Mystical Agriculture → Dragon Eggs | Chapter 3's untitled `allthetweaks:mini_exit` quest | *"First for Dragon Eggs you don't have to keep milking the Dragon you can use HNN or MA to get them or an Extrator to make more!"* (sic) |
| HNN → Nether Stars | Chapter 3's *The Star's Casing* | *"(Please I am begging you use HNN just don't spawn and kill 111,537, please!)"* |
| HNN or Ender IO → Piglich hearts | Chapter 2's *Piglich Boss* | *"(Look into ways of farming them like with HNN or EnderIO!)"* |
| Productive Bees → Flux Dust | Basic Power's **Automated Flux Dust** | *"Flux Dust can be automated using Productive Bees!"* |
| Productive Bees or Mystical Agriculture → Compressed Iron | PneumaticCraft's untitled *Tired of blowing stuff up?* quest (`mysticalagriculture:compressed_iron_seeds`, or the compressed-iron bee's comb) | *"If you wish to automate this process you can use Productive Bees or Mystical Agriculture."* |
| Productive Bees → power | Generators' **Honey Generator** (`generatorgalore:honey_generator`) | *"Honey Generator uses Liquid Honey to make Energy."* |

Anything beyond these — a bee that makes a seed, a seed a given harvester accepts, a
spawner a pylon protects — is not in the config: check in-game.

## Cross-references

- `references/atm-star-checklist.md` — Chapter 3's components by source mod, including its
  Mystical Agriculture, Productive Bees and Trees, and Hostile Neural Networks sections,
  where this page's star quotes come from.
- `references/boss-checklist.md` — the Wither and the Ender Dragon (Cognizant Dust's
  sources) and the Warden (the Mountaineer's rune): where and roughly when.
- `references/creative-checklist.md` — the post-star bees (*Patrick Star... Bee?*,
  *Starry Bee!*) behind Star Shards.
- `references/progression.md` — the Resources group in quest-book order, and the
  four-stage map.
- `references/key-mods.md` — one-line overviews of the farming mods.
- `references/getting-started.md` — first-day and first-week advice.

## What this page deliberately does not tell you

- **Recipes.** Not one — not for seeds, essences, cruxes, bees, trees, or machines. JEI
  has them, and recipes are where pack versions differ most.
- **Rates.** Growth speed, drop chances, comb yields, energy costs, and accelerator
  stacking maths: the quests' own descriptions cover what they cover (quoted where this
  page quotes); the rest is in-game.
- **Which crop goes in which harvester.** Whether the Harvester Pylon, the Garden Cloche,
  a Hydroponic Bed, or a Botany Pot takes a given Mystical Agriculture crop is not in the
  config — approximate at best; check in-game.
- **Farm layouts.** No build plans; the quests' pictures and text are in the book.
- **An order the book does not have.** The config orders quests inside a chapter, not the
  farming chapters against each other; the "what first" list is judgement and says so.
- **Anything not in the config.** If a player names a seed, bee, spawner, or farming mod
  that is not listed here, the answer is "open that quest in the book / look it up in
  JEI" — never a guess.
