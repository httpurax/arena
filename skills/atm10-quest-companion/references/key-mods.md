# Key mods in ATM10 — short primers

**Inclusion rule:** every mod below is verified to be in All the Mods 10 — each has its
own FTB Quests chapter in the pack's official quest config (AllTheMods/ATM-10, 8.x), or
is a confirmed core utility (JEI, FTB Quests). If a mod is not listed here, do not assume
it is in the pack — check the in-game mod list or CurseForge/Modrinth page first.

**Detail rule:** what each mod *does* and *when to start it* below is stable, general
knowledge. Exact recipes, item ids, quest task counts, and machine numbers are **not**
reproduced here — they change between pack versions. For any concrete requirement, the
in-game quest book entry plus a JEI recipe lookup are authoritative. Where even the
general picture is uncertain (e.g. which mods a grouped chapter covers), it is marked
approximate.

## Core utilities (always relevant)

| Mod | What it does | Notes |
|---|---|---|
| **FTB Quests** | The quest book itself: 66 chapters, ~4,790 quests, rewards. | The progression spine. Its Welcome chapter states quests are optional and no mod is gated behind them. |
| **JEI (Just Enough Items)** | Recipe and usage lookup for every item in the pack. | The authoritative answer to "how do I craft X / what is X for". Use it instead of any guide's numbers, including this skill's. |

## Tech line

| Mod | What it does | When to start | Unlocks / leads to |
|---|---|---|---|
| **Mekanism** | The pack's flagship tech mod: ore processing chain (multiplication tiers), machines, digital miner, logistics pipes, jetpacks. Separate "Mekanism: Reactors" chapter for fission/fusion. | Right after basic power/iron-level machines; it is the most-recommended first tech commitment. | Ore multiplication feeds everything; reactors and the Digital Miner power the mid-game; star components in Chapter 3. |
| **Create** | Rotational mechanical automation: presses, mixers, crushers, trains, aesthetic factories. | Early tech stage; pairs well with anything. | Bulk processing; several star components (e.g. Blaze Burner-related tasks — see the quest chapter). |
| **Applied Energistics 2 (AE2)** | ME networks: mass digital item storage, autocrafting, channels. Extended & Advanced AE (addon) has its own chapter. | As soon as chests stop scaling — mid tech stage. | Autocrafting is the backbone for ATM Star component mass-production. Alternative: Refined Storage. |
| **Refined Storage** | Simpler digital storage/autocrafting alternative to AE2. | Same point as AE2; pick **one** of the two as your main system. | Same role; the quest book has chapters for both. |
| **Modern Industrialization** | TechMod-style staged progression with its own four quest chapters: Steam Age → Electric Age → Digital Age → End Game. | Whenever you want a *guided* tech ladder instead of Mekanism's open sandbox. | Its End Game chapter feeds star components. |
| **Immersive Engineering** | Multiblock industrial machines with a retro look: crushers, excavators, refinery. | Mid tech stage, optional. | Quest chapter + star components. |
| **Industrial Foregoing** | Mob farming, sludge/sewage processing, "mycelial" generators, black hole units. | Mid tech stage. | Meat Shredder / mycelial generator star components; mob drop automation. |
| **Powah** | Power generation and cables across tiers, from basic to "blazing"/spiritual tiers (naming approximate — check the chapter). | Early-mid, when Basic Power outgrows you. | Big power for reactors/farms. |
| **Extreme Reactors** | Large multiblock fission reactors (and turbines). | Mid-late, when power demand explodes. | Uranium fuel-rod star components. |
| **Generators N Furnaces** | Chapter grouping early generator and furnace upgrades (which exact mods it covers varies by version — read the chapter; Iron Furnaces-style upgrades are the usual suspects, approximate). | Early game. | Faster smelting, first power variety. |
| **PneumaticCraft** | Compressed-air machines, programmable drones, heat mechanics. | Mid-late tech, optional but its chapter is large. | Drone automation; star components (e.g. Micromissiles-related tasks — see chapter). |
| **Oritech** | Newer multiblock tech mod (machinery, ore processing alternatives). | Mid tech, optional. | Star components per its quest list. |
| **XyCraft** | Tech/magic hybrid: crystals, fluid/energy structures ("XyCraft: World/Light/Machines" family, approximate split). | Mid, optional. | Quest chapter rewards. |
| **RailCraft** | Trains, rails, and rail logistics revival for 1.21. | Optional, any time after iron. | Chapter 4 wants a Creative Locomotive — trains matter at the very end. |
| **Draconic Evolution** | Classic endgame power: draconic reactors, energy cores, chaos guardians. | Late game — it is expensive by design. | Top-tier power/armor; star components. |
| **Just Dire Things** | Newer QoL/breaking mod: powerful tools, ore lasers, automation helpers (Dire-inspired). | Mid-late; the community rates it a strong fast-track. | Star components (e.g. "Eternal Stella" appears in Chapter 3/4 quest titles). |

## Logistics, storage, and QoL infrastructure

| Mod | What it does | When to start | Unlocks / leads to |
|---|---|---|---|
| **Integrated Dynamics** | Logic/energy/item cables with programmable connectors; dynamic tank/crystal menagerie. | When you need smarter item routing than pipes. | Automation glue for farms and machines. |
| **Modular Routers** | One-block item/fluid/energy routing with upgrade modules. | Early-mid; cheap and everywhere useful. | Compact automation without full networks. |
| **Pylons** | Utility pylons: Harvester (a crop auto-farm), Infusion (potion effects), Expulsion, Interdiction (blocks mob spawns), and Protection — chunk-area helpers that are not chunk loaders. The 13-quest chapter (pack 8.2 config) covers exactly these five; no growth-acceleration pylon exists. | Early-mid, once a crop plot needs automating. Which crops the Harvester Pylon accepts (Mystical Agriculture's included) is not in the config — check in-game. `references/chunk-loading-guide.md` has the verified roster and what each pylon's own quest text says. | Farm automation; see `farming-guide.md`. |
| **Silent Gear** | Modular tools/armor built from material parts (blueprint + parts system). | First hours — it replaces vanilla tool progression. | Better-than-diamond gear before Netherite/Allthemodium tiers. |
| **Apotheosis (Gear / Spawners / Apothic Enchanting)** | Enchanting overhaul: gem sockets on gear ("Apotheosis Gear"), spawner capture/modification ("Apothic Spawners"), and the enchanting table rework ("Apothic Enchanting"). | Gear sockets early; spawners when you want mob farms; the enchanting chapter alongside the gear chapter — its first quests need nothing from Apotheosis Gear, but its World Tier gate quests require the Gear chapter's World Tier quests (verified, pack 8.2: `references/enchanting-guide.md`). | Enchant cap raising, mob farming, endgame gear. |
| **Hostile Neural Networks** | Data-model mob simulation: kill mobs virtually for their drops. | Mid — pairs with spawners/loot. | Drop farms for star components (e.g. Ender Dragon Data Model is a Chapter 3 title). |

## Resource farming

| Mod | What it does | When to start | Unlocks / leads to |
|---|---|---|---|
| **Mystical Agriculture** | Grow resources: inferium → prudentium → tertium → imperium → supremium essence tiers, resource seeds, growth accelerators. | Early-mid; the single highest-leverage farm in the pack. | Seeds for metals/essences; Creative Essence is a Chapter 3 star component. |
| **Productive Bees** | Bees that produce resources; huge chapter (252 quests). | Mid, after basic farms. | Resource bees (Soul Lava Bee Spawn Egg etc. appear in star quests). |
| **Productive Trees** | Resource-bearing trees; large chapter (167 quests). | Mid, alongside bees. | Tree-based resource lines for the star. |
| **Food and Farming** | Vanilla+ farming, cooking mods, and food QoL grouped in one chapter. | Any time — start early for buff food. | Sustainable food for boss fights. |

The verified farming detail — Mystical Agriculture's full tier ladder (through Insanium,
Tier 6, via Mystical Agradditions) and which tier every seed is, the three mob-farm
routes, what the pack has instead of resource chickens, and what to set up first — is in
`farming-guide.md`.

## Magic line

| Mod | What it does | When to start | Unlocks / leads to |
|---|---|---|---|
| **Ars Nouveau** | Spellcrafting: craft your own spells from glyphs, ritual circles, golems/familiars, starbuncle automation. | The most-recommended first magic mod; early-mid. | Permanent utility spells (flight, light); multiple star components. |
| **Occultism** | Demon summoning: divination, spirit fire, dimensional storage (satchel/storage actuator), possessed machines. | Mid magic. | Storage + star components (Chapter 3 lists Occultism tasks). |
| **EvilCraft** | Blood magic lite: blood infra, dark tanks, vengeance, werewolves-ish flavor (approximate — check the chapter). | Mid magic, optional. | Creative Blood Drop appears in Chapter 4 titles. |
| **Iron's Spells 'n Spellbooks** | RPG spellcasting: spellbooks, scrolls, casting gear, the Dead King boss. | Any time — combat-focused. | Spellbook star components; boss gear. |
| **Forbidden & Arcanus** | Magic/tech hybrid: arcana, rituals, Hephaestus forge. | Mid-late. | "Automatic Hepheastus Forge" is a Chapter 4 quest. |
| **Nature's Aura** | Aura-based nature magic: altars, offerings, aura collectors. | Mid magic, small chapter (25 quests). | Niche star components. |
| **Theurgy** | Summoning/knowledge magic (small chapter, 45 quests; mechanics approximated — read its in-game guide). | Mid magic, optional. | Niche components. |
| **Neo Vitae** | Newer magic mod with its own chapter (49 quests) and its own dimension (`neovitae:dungeon`, opened by rites after *Tier III: The Master's Orb* — see `references/dimension-guide.md`); details are version-fresh, so treat everything beyond "it has a chapter" as approximate. | Mid-late magic, optional. | Chapter rewards. |
| **Mahou Tsukai** | Anime-flavored magic: large spell repertoire, reality-marble-style powers. | Optional magic side-path (booked under Tools and Gear). | Utility spells. |
| **Apothic Enchanting** | The enchanting-table overhaul chapter: shelves set three table stats (Eterna, Quanta, Arcana), and your Apotheosis World Tier caps Eterna (verified walkthrough: `references/enchanting-guide.md`). | From your first enchanting table (the chapter's first task); its tier gates follow the Apotheosis Gear World Tier quests. | High-tier enchants, up to each enchantment's configured max level. |

## Exploration and dimensions

Which dimension to open first, what unlocks each one, and a recommended visit order — from
verified quest titles at pack 8.2 — are in `references/dimension-guide.md`; the "When to
go" column below is the orientation-level summary.

| Mod / Chapter | What it does | When to go | Notes |
|---|---|---|---|
| **The Twilight Forest** | Classic dimension with an ordered boss progression (Naga → Lich → ... → Ur-Ghast and beyond; boss order approximate — follow the dimension's own progression). | Mid game; one of the easier dimensions. | 56-quest chapter; star-relevant loot. |
| **The Aether** | The revived classic sky dimension; bosses: Slider, Valkyrie Queen, Sun Spirit. | Mid game. | 73-quest chapter. |
| **The Bumblezone** | Bee dimension, pairs with Productive Bees. | Mid game. | 114-quest chapter. |
| **The Undergarden** | Dark cavern dimension with its own materials. | Mid game. | 82-quest chapter. |
| **Deeper and Darker** | Deep Dark / Sculk extension dimension ("Otherside" per quest metadata). | Mid-late — sculk gear is strong. | Chapter 3 star titles reference it. |
| **Cataclysm (L'Ender's Cataclysm)** | Hardcore boss mod: Netherite Monstrosity, Ignis, Ender Guardian, etc. | Late game — these are the pack's hardest fights. | 110-quest chapter. |
| **Ice and Fire** | Dragons and mythic beasts; dragon bone/steel gear. | Mid-late, dangerous. | 87-quest chapter, ties to "The Other" dimension per quest metadata. |
| **Eternal Starlight** | Newer magic dimension with bosses (Lunar Monstrosity, Starlight Golem, Gatekeeper). | Late-ish; biggest exploration chapter (193 quests). | Details version-fresh — treat as approximate. |
| **Auroral** | Small chapter (21 quests); newer content — treat specifics as approximate and read the chapter in-game. | Optional. | — |
| **Mining Dimension / The Other / The Beyond** | Pack-tied dimensions reached with Chapter 2's Teleport Pad — placed in the Overworld, the Nether, or the End respectively, per the chapter's quest text (`references/dimension-guide.md`); the pad's recipe is JEI's. | Late game. | Where Allthemodium/Vibranium/Unobtainium gathering happens per the main questline. |

## Small but verified: worth knowing early

| Mod | What it does | Notes |
|---|---|---|
| **Waystones** | Teleport back to activated waystones. | Verified in the published ATM10 mod list. Guides recommend grabbing waystones from village loot early for cheap travel. |
| **Roots Classic** | Druidic wands and nature rituals. | Verified in the mod list; "Roots Classic" also appears as a Chapter 3 (ATM Star) quest title. |
| **Iron Furnaces** | Upgraded furnaces (iron/gold/diamond/... tiers). | Verified in the mod list; matches Chapter 1's "Furnace Upgrades!" quest title. Guides push it as a first-hour build. |
| **FTB Ultimine** | Vein-mining: harvest many blocks at once (default keybind commonly `~`). | Verified in the mod list. The single biggest time-saver for mining and tree-chopping; check Controls for the exact bind. |
| **Sophisticated Storage / Backpacks, Functional Storage, Pipez** | Chest/barrel/drawer upgrades, portable storage, simple pipes. | Verified in the mod list *and* in the quest config: `references/storage-ladder.md` maps the "Basic Storage" chapter (Sophisticated Storage, Sophisticated Backpacks, Functional Storage) quest by quest, and "Basic Logistics" covers Pipez. |
| **LaserIO** | Node-and-card routing: cards configure what a Laser Node pulls, pushes, or stores. | Verified in the mod list (1.9.11) and in the quest config — the "Basic Logistics" chapter has a quest whose task is `laserio:card_holder`. |
| **Corail Tombstone, JourneyMap, FTB Chunks, FTB Essentials** | Death recovery, minimap/waypoints, chunk claiming and force-loading, `/home` `/rtp` `/spawn` commands. | Verified in the mod list; the Welcome chapter teaches the commands and chunk claiming. For keeping a farm running while the player is away, `references/chunk-loading-guide.md` has the verified claim/force-load steps and every chunk loader this pack's config actually enables or disables. |
| **Time in a Bottle** | Store time in bottles to speed up machines. | Verified in the mod list; guides list it among early-game milestones. |

## Mods frequently assumed present but NOT verified here

Do not claim these are in ATM10 without checking in-game first:

- **Botania** — several general "ATM10" beginner articles suggest it as a magic choice,
  but it does **not** appear in the published 8.x mod list's magic section, and it has no
  quest chapter. The verified magic lineup is the Magic group in `progression.md` (Ars
  Nouveau, Occultism, EvilCraft, ...) plus Roots Classic and Reliquary-style mods. Treat
  Botania as absent unless JEI says otherwise.
- **Thermal series** — a staple of *other* kitchen sinks and often mentioned in generic
  advice; it is **not** in pack 8.2's `config/crash_assistant/modlist.json`. (LaserIO,
  Super Factory Manager, and Botany Pots, often lumped in with it, *are* in that modlist;
  Botany Pots has no quests — see `farming-guide.md`.)

The safe move for any mod: search its signature item in JEI in-game — if the item
resolves, the mod is there; then let JEI and the quest book supply every detail.
