# The ATM10 roadmap: a recommended play order for all 66 chapters

**What this page is.** The order to play **All the Mods 10** in: all **66 chapters** of the
FTB Quests book laid out as one recommended play order, from the first hour to the ATM Star
and past it, grouped into four phases — **early, mid, late, endgame** — with a one-line
"what this chapter is about" for each. It answers "which chapter first, second, third?" —
nothing more. The **order is this skill's recommendation, not pack canon**; the chapters,
titles, groups, quest counts, and the handful of hard dependency links are the pack's, read
from its config. It is a *reading of the book*, not a walkthrough.

## Provenance — everything here was read, not remembered

Every chapter id, chapter title, group name, quest count, and quoted quest title below
comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10), `main` branch at commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with. At that commit the book holds exactly
**66 chapters and 4,790 quests** — the total below is the sum of the per-chapter quest
counts in the tables. Files read:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/*.snbt` | the 66 chapter ids, each chapter's quest count and `order_index`, and the book's dependency links |
| `config/ftbquests/quests/chapter_groups.snbt` | the quest-book groups and the order the book shows them in |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` and `chapter_group.snbt` | the English chapter and group titles |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles quoted in the "what it is about" lines |
| `examples/progress.example.json` (this skill) | the four-stage tag on each chapter — the skill's own stage table, not pack data |

The **stage tags are this skill's progression model** (`references/progression.md`,
`scripts/build_chapter_list.py`): the quest book has no stage notion. The phases below
group those stages for play-order purposes, and each table row keeps the chapter's stage
tag visible so recommendation and skill data stay distinguishable.

## Grounding rules (read before following this order)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **This page is a recommendation, not pack canon.** The pack enforces almost no order:
  quests are optional and mods are not gated (the pack's own Welcome chapter says so), and
  in the whole 4,790-quest book there are exactly **five cross-chapter dependency links**
  (verified, listed under "What the pack itself enforces"). Everything else — every "do X
  before Y" the phase order implies — is this skill's advice, offered as advice.
- **Approximate means approximate.** Phase boundaries, "roughly when", and every choice
  between overlapping mods (AE2 *or* Refined Storage, Mekanism *or* Create *or* Modern
  Industrialization, which magic mod first) are the author's judgement based on the config
  and community playthrough patterns, not facts the pack states. Verify in-game.
- **No item ids, no recipes, no coordinates.** This page never lists them, because it
  never needs them: it orders chapters, it does not solve them. For any concrete
  requirement — counts, ingredients, ore levels, boss mechanics — read the quest entry and
  JEI. Do not fill a gap in a one-liner from memory or plausibility.
- **Quest titles are the config's.** A title in *italics* below is a quest title quoted
  from pack 8.2's lang file. Several chapters carry mostly untitled quests (the book then
  shows the task item's own name); those are marked, and nothing is derived for them. One
  line per chapter cannot describe every quest — it names verified titles that characterize
  the chapter, never a complete list.
- **Nothing here was invented, and nothing is added from memory.** A chapter that is not
  in the config is not on this page; a quest title not in the config is not quoted. If a
  player names a chapter this page does not know, the answer is "let's look at your quest
  book" — never a plausible-sounding guess.

## How the phases map to the skill's stages

| Phase | Chapters | Stage tags | In one line |
|---|---|---|---|
| Phase 1 — Early game | 1–16 | `early-game` | orientation, Chapter 1's vanilla arc, first gear, power, storage, farms |
| Phase 2 — Mid game | 17–53 | `tech` and `magic` | the automation bulk: a real storage network, resource factories, tech lines, the magic line |
| Phase 3 — Late game | 54–63 | `endgame` (Exploration group + Draconic Evolution) | dimensions, bosses, and Draconic-tier power — the star's raw-material sources |
| Phase 4 — Endgame | 64–66 | `endgame` (Main Questline chapters 2–4) | Allthemodium → the ATM Star → Creative |

Phases are a reading aid, not gates: players overlap them heavily, and the pack itself
lets you play in any order. The numbering below is this page's recommended sequence.

## Phase 1 — Early game (16 chapters)

Orientation and the vanilla arc, then the "basic" gear and infrastructure chapters. All 16
carry the skill's `early-game` tag. Nothing here needs a machine beyond a furnace tier.

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 1 | Welcome | `welcome` | — (standalone) | 6 | early-game | The pack's own introduction — its only titled quest is *"Welcome to All The Mods 10!"*; read it before anything else. |
| 2 | Bounty Board | `bounty_board` | — (standalone) | 50 | early-game | Kill-bounty quests (*Overworld Bounty: Zombies*, *The Nether Bounty: Blazes*) plus the book's standing boss hunts (*Kill The Ender Dragon*, *Kill The Wither*, *Kill The Warden*, even *Kill The Lunar Monstrosity* later). |
| 3 | Building Tips | `building_tips` | — (standalone) | 91 | early-game | A decor/build toolbox tour: *Blocks!*, *Paxel*, *Rechiseled*, *Chipped*, *Building Gadgets*, the Macaw's mod family. |
| 4 | Tips and Tricks | `tips_and_tricks` | — (standalone) | 23 | early-game | One-off quality-of-life wins: *Infinite Water*, *Personal Shrinking Device*, *Tool Belt*, *Easy Villagers*, *Iron Jetpacks*. |
| 5 | Chapter 1: The Beginning | `mainquestline_part_1` | Main Questline | 36 | early-game | The book's tutorial spine: *Stone Age* → *We've Struck Diamonds!* → *To The Nether!* → *The End*, closing with boss kills (*Summoning The Wither*, *Kill The Warden*) and first infrastructure (*Wind Power*, *Solar Power*, *Lava Power*, *Basic Ore Doubling*). |
| 6 | Basic Tools | `basic_tools` | Tools and Gear | 77 | early-game | The harvest-tier ladder (*Harvest Tier 1* … *Harvest Tier 6*); most of its quests are untitled in the config — the book shows the tools themselves. |
| 7 | Basic Armor | `basic_armor` | Tools and Gear | 128 | early-game | Every armor line the book tracks, from *Leather Armor* through *Netherite Armor* to the *Allthemodium/Vibranium/Unobtainium* sets and the mage outfits (*Pyromancer Outfit*, *Battlemages Outfit*). |
| 8 | Silent Gear | `silent_gear` | Tools and Gear | 69 | early-game | The modular tool/armor system: *Salvager*, grader catalysts, and the Productive Metalworks foundry line (*Building the Foundry*, *Casting Items*). |
| 9 | Apotheosis Gear | `apotheosis_gear` | Tools and Gear | 30 | early-game | Affix loot and gem socketing: *Sigil of Socketing*, the reforging tables, and the *World Tier* ladder (*Frontier* → *Pinnacle*). |
| 10 | Artifacts | `artifacts` | Tools and Gear | 50 | early-game | The accessory collection — nearly one quest per artifact (*Golden Hook*, *Fire Gauntlet*, *Cloud in a Bottle*, *Novelty Drinking Hat*). |
| 11 | Relics | `relics` | Tools and Gear | 26 | early-game | The second accessory line (*Sphere of Self-Sacrifice*, *Piglin Mask*, *Ring of the Seven Deadly Sins*), hunted across *Overworld*, *The Nether*, and *The End*. |
| 12 | Basic Power | `basic_power` | Power | 34 | early-game | First power, surveyed honestly: *Heat Generator*, *Coal Generators*, moving it (*Pipez: Energy Pipes*), with *Mid Game Power Options* and *End Game Power Options* previewed for later. |
| 13 | Basic Storage | `storage` | Storage | 90 | early-game | Chests before networks: *Iron Chest* → *Netherite Chest*, Sophisticated Backpacks and their upgrade ladders, Functional Storage. |
| 14 | Basic Logistics | `basic_logistics` | Logistics | 40 | early-game | First item/fluid/energy movement: the *Pipez* family (*Item Pipez*, *Gas Pipez*), *Laser IO*, the import/card quests. |
| 15 | Food and Farming | `food_and_farming` | Resources | 35 | early-game | Vanilla-plus farming and cooking: *Punch the Grass*, *The Bread of Life*, *Making a Kitchen, with a Book*, the fishing-rod tiers. |
| 16 | Apothic Spawners | `apotheosis_2` | Resources | 36 | early-game | Captured-spawner engineering: *Ignore Light*, *No AI*, *Redstone Active*, *Blowing up Spawners* — the base for every mob farm to come. |

## Phase 2 — Mid game (37 chapters)

The automation bulk: `tech` (27 chapters) plus `magic` (10). This is where the roadmap's
advice matters most, because the mods overlap heavily — treat every pick below as the
author's recommendation, and present the alternatives as alternatives.

### Storage and power first (17–21)

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 17 | Generators N Furnaces | `generators` | Power | 47 | tech | Furnace tiers (*Iron Furnace* → *Rainbow Furnace*) and generator tiers (*Honey Generator* → *Ender Generator*) — cheap smelting and power growth. |
| 18 | Powah | `powah` | Power | 109 | tech | Tiered tech power: *The Energizing Orb* and reactors from *Reactor (Starter)* to *Reactor (Nitro)* across the *Energized* → *Nitro* tiers. |
| 19 | Applied Energistics 2 | `applied_energistics_2` | Storage | 74 | tech | The ME network: *Meteorite hunting*, storage cells up *256M*, *Auto-Crafting*, *Quantum Network Bridge*. The roadmap's pick for a main storage system (Refined Storage, below, is the alternative — a recommendation, not a rule). |
| 20 | Extended & Advanced AE | `extended__advanced_ae` | Storage | 56 | tech | AE2's addon lines: *Entro Crystals*, the *Assembler Matrix*, and *The Quantum Computer* crafting chain. Run after AE2. |
| 21 | Refined Storage | `refined_storage` | Storage | 72 | tech | The simpler alternative to AE2: *The Grid*, *Autocrafting*, disk parts from *1k Storage Part* upward. Pick this **or** AE2 — the book has chapters for both. |

### Stand up the resource factories (22–26)

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 22 | Mystical Agriculture | `elmystical_agriculturerr` | Resources | 191 | tech | Grow your resources: the *Inferium* → *Insanium* essence tiers, seed and *Growth Accelerator* lines, *Master Infusion Crystal*; *Creative Essence* is an ATM Star component. |
| 23 | Productive Bees | `productive_bees` | Resources | 252 | tech | The book's biggest chapter: resource bees for nearly every material (*Allthemodium Bee*, *Unobtainium Bee*, *Draconic Bee*). |
| 24 | Productive Trees | `productive_trees` | Resources | 167 | tech | The resource-tree sibling; almost all of its quests are untitled in the config — the book shows the trees and products. |
| 25 | Hostile Neural Networks | `hostile_neural_networks` | Resources | 50 | tech | Simulate mob kills for their drops: *Learning Mobs*, *Simulating Deaths*, *The Data Center*. |
| 26 | Pylons | `pylons` | Logistics | 13 | tech | Small automation helpers (harvest and growth pylons per the guides — approximate; only one titled quest in the config, so read the chapter in-game). |

### Add routing and logic (27–28)

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 27 | Modular Routers | `modular_router` | Logistics | 55 | tech | One-block routing: *Modules*, *Upgrades*, *Routers for Mob Farms*, *Routers for Mining*, *Routers for Farming*. |
| 28 | Integrated Dynamics | `integrated_dynamics` | Logistics | 28 | tech | Logic-driven cables and tanks: *Logic Cables*, *Variable Cards*, *Crystallized Menril Chunks*. |

### The tech lines (29–38)

Pick one primary line and go deep — the roadmap's order is Mekanism first, but Create,
Immersive Engineering, or Modern Industrialization are full alternatives (the star will
eventually want products from several; see Phase 4).

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 29 | Mekanism | `mekanism` | Tech | 90 | tech | The flagship tech line: *Metallurgic Infuser* → the ore-multiplication ladder (*Shard, to Clump, to Dust, to Ingot*), jetpacks, *Dynamic Tank Multiblock*, *Logistical Transporters*. |
| 30 | Mekanism: Reactors | `mekanism_reactors` | Tech | 94 | tech | Mekanism's second half: *Fission Reactor* and *Fusion Reactor*, turbines, the *MekaSuit* and *Meka-Tool*, *Digital Miner*, QIO storage. |
| 31 | Create | `create` | Tech | 89 | tech | Rotational automation: *Andesite Alloys*, presses, mixers, *Contraptions*, and full *Trains*. |
| 32 | Immersive Engineering | `immersive_engineering` | Tech | 127 | tech | Multiblock industry with wire power: *Coke Oven*, *Crusher*, *Excavator*, *Arc Furnace*, the metal-press line. |
| 33 | Industrial Foregoing | `industrial_foregoing` | Tech | 78 | tech | Factory quality-of-life: conveyor transport, *Laser Drill*, machine-frame tiers, *Pink Slime & Liquid Meat*, *Infinity Tools*. |
| 34 | Just Dire Things | `justdirethings` | Tech | 154 | tech | Tool-and-QoL fast track: *Ferricore*, *Blazegold*, *Eclipse Alloy*, *Tool Upgrades*, *Time Crystal* (most quests untitled in the config). |
| 35 | Oritech | `oritech` | Tech | 56 | tech | Newer multiblock tech: *Machine Cores*, *Ore Processing*, energy transfer and storage. |
| 36 | XyCraft | `xycraft` | Tech | 27 | tech | Crystals and storage tanks: the *Xychorium Gems* colors, *The Tank*, item/fluid IOs. |
| 37 | PneumaticCraft | `pneumaticcraft` | Tech | 127 | tech | Pressure tech: *The Pressure Chamber*, oil refining, *Programming Drones*, *Pneumatic Armor*, *Jet Boots*. |
| 38 | RailCraft | `railcraft` | Tech | 52 | tech | Rails and trains: *Steam Locomotive*, the track tiers, *Tunnel Bore* — Chapter 4 eventually wants a *Creative Locomotive*. |

### Modern Industrialization: the one guided ladder (39–42)

The pack wires these four chapters to each other with dependency links — the only fully
ordered tech ladder in the book (verified; see "What the pack itself enforces").

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 39 | Steam Age: New Beginnings | `mi_steam` | Modern Industrialization | 30 | tech | MI step 1: *Forge Hammer*, *Bronze*, first circuits and rubber. |
| 40 | Electric Age: No more rookie | `mi_electric` | Modern Industrialization | 50 | tech | MI step 2: *Electricity Generation*, *LV-MV Transformers*, *Crude Oil Processing*. |
| 41 | Digital Age | `mi_digital` | Modern Industrialization | 66 | tech | MI step 3: *Titanium Ingot*, advanced components, *Centrifuging Uranium Dust* (most quests untitled in the config). |
| 42 | End Game | `mi_endgame` | Modern Industrialization | 25 | tech | MI's last step; none of its quests carries a title in the config — subtitles include *Nuclear Batteries*, *Freezing Argon with Helium*, *This is the End*. |

### Scale power up (43)

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 43 | Extreme Reactors | `extreme_reactors` | Power | 33 | tech | Big multiblock reactors and turbines: *Our First Reactor*, waste reprocessing, *Ludicrite & Ridiculite*. |

### The magic line (44–53)

Runs in parallel with tech, not after it — the roadmap's picks (Ars Nouveau first) are
advice. Several of these lines feed ATM Star components directly (quoted titles in
`references/atm-star-checklist.md`).

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 44 | Ars Nouveau | `ars_nouveau` | Magic | 130 | magic | The roadmap's pick for a first magic mod: spell books, *Magebloom Seed*, *Enchanting Apparatus*, *Summoning Help!* (most quests untitled in the config). |
| 45 | Apothic Enchanting | `apothic_enchanting` | Magic | 58 | magic | The enchanting overhaul — the pack itself gates it on Apotheosis Gear (verified dependency): shelf libraries (*Hellshelves* → *Endshelves*), *Arcana*, *Eterna*, *Quanta*. |
| 46 | Iron's Spells 'n Spellbooks | `iron_spells_and_spellbooks` | Magic | 103 | magic | RPG spellcasting: spellbook and ink tiers, the magic schools (*Fire*, *Ice*, *Ender*, …), structures, and *The Dead King* boss line. |
| 47 | Occultism | `occultism` | Magic | 64 | magic | Ritual summoning: *Our First Ritual*, the chalk ladder, familiars, *Demonic Magical Storage!*. |
| 48 | Forbidden & Arcanus | `forbidden__arcanus` | Magic | 62 | magic | Arcane crafting: *Arcane Crystals*, the five-tier forge line, *Mundabitur Dust*, *Obsidiansteel* — several Chapter 3/4 star titles trace here. |
| 49 | EvilCraft | `evilcraft` | Magic | 45 | magic | Blood magic: *Collecting Blood*, *The Blood Infuser*, weather control (*Stop the Rain!*). |
| 50 | Nature's Aura | `natures_aura` | Magic | 25 | magic | Aura magic: *Ritual of the Forest*, *Bottles of Aura*, *Altar of Birthing*. |
| 51 | Theurgy | `theurgy` | Magic | 45 | magic | Alchemy: the salt lines (*Strata Salt*), *Sal Ammoniac*, *Making Mercury*, the three-vessel reproduction ritual. |
| 52 | Neo Vitae | `neo_vitae` | Magic | 49 | magic | Orb-and-ritual progression (*Tier I: The Ring of Runes* → *Tier V: The Pinnacle*), *The Hellfire Forge*. |
| 53 | Mahou Tsukai | `mahou_tsukai` | Tools and Gear | 35 | magic | Anime-flavored magic (booked under Tools and Gear, tagged magic by the skill): *Getting Morgan*, *Caliburn*, the scroll spells. |

## Phase 3 — Late game (10 chapters)

Dimensions, bosses, and Draconic-tier power — all tagged `endgame` by the skill. In
practice several of these (Twilight Forest, Bumblezone) are doable mid-game, and the star
chapter wants their outputs, which is why they sit before the Main Questline finale in
this order — a recommendation, and a fuzzy boundary by design (see
`references/boss-checklist.md` for roughly when each boss lands).

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 54 | Draconic Evolution | `draconic_evolution` | Tech | 140 | endgame | Endgame power and gear: *Fusion Crafting*, tiered energy cores (*Tier 1* → *Tier 8*), the Wyvern → Chaotic tool tiers, *Kill the Chaos Guardian*. |
| 55 | The Twilight Forest | `twilight_forest` | Exploration | 56 | endgame | The classic progression dimension, boss-ordered (*Evening The Scales*, *Bring out your Dead*, *Hydra Slayer*, *The Final Boss*, *The Real Final Boss*). |
| 56 | The Aether | `aether` | Exploration | 73 | endgame | The sky dimension: *Bronze Dungeon*/*The Slider*, *Valkyrie Queen*, *Sun Spirit*, and full gear ladders (*Gravitite*, *Valkyrie Armor*). |
| 57 | The Bumblezone | `bumblezone` | Exploration | 114 | endgame | The bee dimension — pairs with Productive Bees: honey labyrinth structures, the essence quests (*Essence of Raging*, *Essence of Life*), *Beehemoth*. |
| 58 | The Undergarden | `undergarden` | Exploration | 82 | endgame | The cavern dimension: *Stoneborn* traders, the *Forgotten Guardian* boss, the *Cloggrum*/*Froststeel*/*Utheric* gear lines. |
| 59 | Deeper and Darker | `deeper_and_darker` | Exploration | 45 | endgame | Warden tech: *Heart of the Deep*, *The Otherside* dimension, *Warden Armor*, *Soul Elytra*. |
| 60 | Cataclysm | `cataclysm` | Exploration | 110 | endgame | The pack's hardest boss gauntlet: *Netherite Monstrosity*, *Ignis*, *The Leviathan*, *The Harbinger*, *Ender Guardian*, *Ancient Remnant*, *Maledictus*. |
| 61 | Ice and Fire | `ice__fire` | Exploration | 87 | endgame | Dragons and mythic beasts: dragon roosts and caves by stage, *Fire Dragonsteel*, the *Gorgon*, *The Hydra*, *Trolls* — plus quests for *The Other* dimension. |
| 62 | Eternal Starlight | `eternal_starlight` | Exploration | 193 | endgame | The biggest exploration chapter: a full dimension with its own bosses (*Lunar Monstrosity*, *Starlight Golem*, *The Gatekeeper and The Gate*) and gear sets (*Glacite*, *Deepsilver*, *Aethersent*). |
| 63 | Auroral | `auroral` | Exploration | 21 | endgame | Small and newer: *Shimmersteel*, *Shimmerweave Armor*, *Auroral Infusion* — specifics are version-fresh; read the chapter in-game (approximate). |

## Phase 4 — Endgame (3 chapters)

The Main Questline's finale — the pack's own numbered spine (its chapter titles say
"Chapter 2", "Chapter 3", "Chapter 4"). This part of the order is the pack's, not the
roadmap's.

| # | Chapter | id | Group | Quests | Stage | What it is about |
|---|---|---|---|---|---|---|
| 64 | Chapter 2: Allthemodium | `allthemodium` | Main Questline | 54 | endgame | The pack's super-metals: *Allthemodium Ingot*, *Vibranium Ingot*, *Unobtainium Ingot*, the three alloy ingots, the armor/tool ladders, *Teleport Pad*, *Mining Dimension*, *The Other*, *The Beyond*, and the *Piglich Boss* fight. |
| 65 | Chapter 3: The ATM Star | `chapter_2_the_star` | Main Questline | 128 | endgame | The pack's goal: one *ATM Star* assembled from 13 components drawn from every major mod line — see `references/atm-star-checklist.md` for the whole chapter. |
| 66 | Chapter 4: Creative | `achapter_2r_6the_atm_star` | Main Questline | 38 | endgame | Post-star: automate the star (*Runic Star Altar*, the sibling multiblocks, *Star Shards*, the five star parts), then spend it behind *Fully Automated ATM Star* on the creative-tier items — see `references/creative-checklist.md`. |

## What the pack itself enforces (and what it does not)

Verified from the config at pack 8.2 — this list is short, which is exactly why the rest
of the order is advice:

- **The Main Questline is numbered.** The book's own titles run *Chapter 1: The Beginning*
  → *Chapter 2: Allthemodium* → *Chapter 3: The ATM Star* → *Chapter 4: Creative*, in that
  `order_index` order, inside the book's first group.
- **Exactly five cross-chapter dependency links exist in the whole book** (counted from
  the chapters' `dependencies` fields): Modern Industrialization's *Electric Age* links to
  *Steam Age*, *Digital Age* to *Electric Age*, *End Game* to *Digital Age* (and to
  *Electric Age*) — and four *Apothic Enchanting* quests link to *Apotheosis Gear*. Those
  five edges are canon; nothing else in the book chains one chapter to another.
- **Everything else is free order.** The Welcome chapter says quests are optional and mods
  are not gated. The phases above are a recommended reading of the config, community
  playthrough patterns, and each chapter's own quest list — offer them as advice, and let
  the player's book and interests decide.

## Using this document in a session

1. Locate the player with `references/progression.md` (stage, what is built, what is
   stuck) and `references/key-mods.md` (what each mod does, when to start it).
2. Find his phase here, and give the next steps as the next chapters in this order —
   naming what each unlocks, from the one-liners and the referenced docs.
3. When the choice between mods matters (storage, tech line, magic mod), present the
   alternatives this page flags — never present the roadmap's pick as required.
4. Endgame detail comes from the dated checklists:
   `references/atm-star-checklist.md` (the star's components by source mod),
   `references/boss-checklist.md` (boss → dimension → arena → roughly when), and
   `references/creative-checklist.md` (Chapter 4 after the star).
5. This page is **not** quest-book order: `examples/progress.example.json` and
   `scripts/progress.py` report chapters in quest-book order, which is a different
   sequence. Say which order you are using when it matters.
6. Record finished chapters with `scripts/progress.py --set` and re-run the report.

*The in-game quest book (FTB Quests) and JEI are authoritative for everything this page
summarizes. The order above is a recommendation; the player plays the pack his way.*
