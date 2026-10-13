# The ATM Star: component checklist by source mod (Chapter 3)

**What this page is.** The endgame checklist for **All the Mods 10**: every component the
quest book's **Chapter 3: The ATM Star** asks for, grouped by the mod it comes from. It
answers "what is left for the star, and which of my mods does each piece touch?" — nothing
more. It is a *map of the chapter*, not a crafting guide.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, item id, count, and quoted sentence below comes from the
official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10),
`main` branch as of **2026-09-22**, which `CHANGELOG.md` lists as **pack 8.2** — the "8.x"
that `examples/progress.example.json` is stamped with. Three files were read:

| File in the pack repo | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/chapter_2_the_star.snbt` | the chapter's 128 quests, their task items, required counts, and dependency links |
| `config/ftbquests/quests/lang/en_us/chapters/chapter_2_the_star.snbt` | the English quest titles, subtitles, and the description text quoted below |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (489 mod ids) |

The lang file names this chapter `Chapter 3: The ATM Star` in the group `Main Questline`,
with chapter icon `allthetweaks:atm_star` — the same chapter the skill tracks as
`chapter_2_the_star`. (The config filename says "chapter_2"; the book's own title says
Chapter 3. Both are the pack's, so both are quoted as they are.)

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the task's required amount); where the config
  says one, no count is printed. Item ids are the pack's own strings.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Every
  "how" here is a quote from the quest's own description, marked as such, or a pointer to
  JEI. Do not fill in a recipe from memory or plausibility.
- **Approximate means approximate.** Mod display names are the modlist's, but which machine
  tier, energy amount, or farm layout a player needs is version-sensitive; anything not
  quoted from the config is flagged.
- **Quest titles are the config's.** 102 of the 128 quests carry an explicit title. The
  other 26 do not: the book then shows the task item's own name, and 14 of them carry a
  subtitle instead. Those are marked *(no title in the config)* below with the subtitle
  quoted where one exists — do not present a derived name as a verified title.

## How the chapter is shaped

The quest **ATM Star** (task `allthetweaks:atm_star`, subtitle *"Does this mean you win?"*)
has exactly **13 direct dependencies** — the components. Each component depends on a set of
mod-line quests, and each mod line hangs off a **hub quest** titled with the mod's name
("Mekanism", "Ars Nouveau", "Powah", ...). 48 quests have no dependencies at all: those 31
mod hubs, 3 build-it-yourself components, 7 Patrick Star block quests, 5 compressed-block
quests, and 2 untitled entries.

So the practical reading order is: pick a component → see which mods it draws on → do the
mod's line. The book does not force an order between components.

## The 13 components (verified titles, in the order the config lists them)

| # | Component quest title | Task item (config) |
|---|---|---|
| 1 | Runic Star Altar | 19 `forbidden_arcanus` block tasks + `modern_industrialization:star_altar` (see below) |
| 2 | Pulsating Black Hole | `allthetweaks:pulsating_black_hole` |
| 3 | Nexium Emitter | `allthetweaks:nexium_emitter` |
| 4 | Patrick Star | `allthetweaks:patrick_star` |
| 5 | Dimensional Seed | `allthetweaks:dimensional_seed` |
| 6 | Wither's Compass | `allthetweaks:withers_compass` |
| 7 | Improbable Probability Device | `allthetweaks:improbable_probability_device` |
| 8 | Philosopher's Fuel | `allthetweaks:philosophers_fuel` |
| 9 | Dragon Soul | `allthetweaks:dragon_soul` |
| 10 | Creative Essence | `mysticalagradditions:creative_essence` |
| 11 | Oblivion Shard | `allthetweaks:oblivion_shard` |
| 12 | The Star's Casing | `allthemodium:unobtainium_allthemodium_alloy_block` ×28, `allthecompressed:nether_star_block_3x` ×15 |
| 13 | Awakened Unobtainium-Vibranium Alloy Block | `allthemodium:unobtainium_vibranium_alloy_block` ×2 |

Nine of the thirteen are `allthetweaks` items (AllTheTweaks 2.10.0) — the pack's own
endgame mod, which is why their recipes are only in JEI and the star altar. The other four
are the Runic Star Altar build, Creative Essence, the casing blocks, and the awakened alloy.

## The three "either/or" quests (verified titles)

Three quests have titles that offer a choice, each with both options as dependencies and a
`ftbfiltersystem:smart_filter` task (FTB Filter System 21.1.4). The titles are the pack's;
that "either one satisfies it" is the natural reading is *approximate* — confirm in the
quest entry.

| Verified quest title | Option A | Option B | Feeds |
|---|---|---|---|
| Mechanical Arm or Large Advanced Motor | `create:mechanical_arm` (Create 6.0.10) | `modern_industrialization:large_advanced_motor` (Modern Industrialization 2.5.8) | Nexium Emitter |
| Blaze Burner or Uranium Quad Fuel Rods | `create:blaze_burner` | `modern_industrialization:uranium_fuel_rod_quad` | Philosopher's Fuel |
| Either or Blastproof Casings and 256M Portable Item Cells | `modern_industrialization:blastproof_casing` | `megacells:portable_item_cell_256m` (MEGA Cells 4.11.0) | Improbable Probability Device |

The Modern Industrialization hub quest's own description backs the choice up: *"thankfully
we don't need to go to the last one for the Star. Infact now, it is entirely optional! If
you'd rather play with Create to create (get it?) the ATM Star you can!"*

## Components by source mod

Format: **verified quest title** → task item (×count only when the config states more than
one) → the component it feeds. *(no title in the config)* marks a quest whose book name is
derived from its item; a quoted subtitle is given when the config has one.

### AllTheCompressed (`allthecompressed` 4.4.0) — bulk blocks

| Quest | Task item | Feeds |
|---|---|---|
| *(no title in the config; subtitle "59,049 Obsidian")* | `allthecompressed:obsidian_5x` | Dimensional Seed |
| *(no title in the config; subtitle "59,049 End Stone")* | `allthecompressed:end_stone_5x` | Dimensional Seed |
| *(no title in the config; subtitle "6,561 Diamond Blocks")* | `allthecompressed:diamond_block_4x` | Dimensional Seed |
| *(no title in the config; subtitle "6,561 Emerald Blocks")* | `allthecompressed:emerald_block_4x` | Dimensional Seed |
| *(no title in the config; subtitle "531,441 Netherrack")* | `allthecompressed:netherrack_6x` | Dimensional Seed |
| — (part of The Star's Casing quest) | `allthecompressed:nether_star_block_3x` ×15 | The Star's Casing |

The subtitles are the config's own arithmetic for the compressed tiers. The casing quest's
description spells out the nether-star cost: *"For 17 X3 Netherstar Blocks you'll need
111,537 Netherstars. (Please I am begging you use HNN just don't spawn and kill 111,537,
please!)"*

### Allthemodium (`allthemodium` 3.0.1) — hub task `allthemodium:allthemodium_ingot`

| Quest | Task item | Feeds |
|---|---|---|
| Piglich Heart Block | `allthemodium:piglich_heart_block` | Dragon Soul |
| The Star's Casing *(component hub)* | `allthemodium:unobtainium_allthemodium_alloy_block` ×28 | The Star's Casing |
| Awakened Unobtainium-Vibranium Alloy Block *(component hub)* | `allthemodium:unobtainium_vibranium_alloy_block` ×2 | itself → ATM Star |

The Piglich is a boss in the pack's own Allthemodium dimension line — see
`references/boss-checklist.md`. The casing quest says the 28 alloy blocks are made *"using
an Enchanting Apparatus from Ars Nouveau"*, and the awakened-alloy quest says it needs a
Star Altar run with *"the Unobtainium-Vibranium Block, 4 Unbreaking I Books, 4 Awakened
Supremium Gemstones, and 4 Awakened Supremium Essence"* plus *"85 Million FE"* (quoted
numbers; verify in the quest entry and JEI).

### Apothic Mods — hub task `minecraft:bookshelf`

| Quest | Task item | Feeds |
|---|---|---|
| Infused Dragon's Breath | `apothic_enchanting:infused_breath` (Apothic Enchanting 1.6.2) | Dragon Soul |
| *(no title in the config)* | `minecraft:tipped_arrow` | Wither's Compass |
| *(no title in the config)* | `allthetweaks:mini_nether` | Dimensional Seed |
| *(no title in the config)* | `allthetweaks:mini_end` | Dimensional Seed |
| *(no title in the config)* | `allthetweaks:mini_exit` | Dimensional Seed |

The hub's description: *"The Apothic mods have multiple cores... The Attributes and
Enchanting mods are what you'll need to follow to get the ATM Star!"* The pack's modlist
carries Apothic Attributes 2.10.1, Apothic Enchanting 1.6.2, Apothic Spawners 1.4.0, and
Apotheosis 8.8.0 — which of them a given task wants is the quest entry's business, not
this page's (approximate mapping).

### Applied Energistics 2 (`ae2` 19.2.17) and its addons — hub task `ae2:certus_quartz_crystal`

| Quest | Task item | Feeds |
|---|---|---|
| Singularity | `ae2:singularity` | Improbable Probability Device |
| 256M Portable Item Cell | `megacells:portable_item_cell_256m` (MEGA Cells 4.11.0) | Improbable Probability Device (either/or) |
| Quantum Computer Multi-Threader | `advanced_ae:quantum_multi_threader` (Advanced AE 1.6.12-1.21.1) | Nexium Emitter |
| Universal Wireless Terminal | `ae2wtlib:wireless_universal_terminal` (AE2WTLib 19.5.1) | Nexium Emitter |
| *(no title in the config)* | `aeinfinitybooster:infinity_card` (AEInfinityBooster 1.21.1-1.0.0.58) | Nexium Emitter |
| *(no title in the config)* | `ae2:quantum_ring` | Pulsating Black Hole |

The 256M cell quest's description mentions *"2 256M Portable Item Cells, 2 Blastproof
Casings, or a mix of both"* for the Improbable Probability Device — quoted, verify in-game.

### Ars Nouveau (`ars_nouveau` 5.13.1) — hub task `ars_nouveau:source_gem`

| Quest | Task item | Feeds |
|---|---|---|
| Glyph of Wither | `ars_nouveau:glyph_wither` | Wither's Compass |

Ars Nouveau also appears without its own quest: The Star's Casing description says the 28
alloy blocks are made with an Ars Nouveau **Enchanting Apparatus**.

### Cataclysm (`cataclysm` — L_Ender's Cataclysm 1.21.1 3.33) — hub task: advancement

| Quest | Task item | Feeds |
|---|---|---|
| Abyssal Sacrifice | `cataclysm:abyssal_sacrifice` | Dragon Soul |
| Meat Shredder | `cataclysm:meat_shredder` | Oblivion Shard |
| Void Forge | `cataclysm:void_forge` | Oblivion Shard |

All three are boss loot — the hub's description says the mod's structures are *"all around
the Overworld, The Nether, and The End"*. Which boss drops what is in
`references/boss-checklist.md` and JEI, not here.

### Create (`create` 6.0.10) — hub task `minecraft:andesite`

| Quest | Task item | Feeds |
|---|---|---|
| Mechanical Arm | `create:mechanical_arm` | Nexium Emitter (either/or) |
| Blaze Burner | `create:blaze_burner` | Philosopher's Fuel (either/or) |

### Deeper and Darker (`deeperdarker` 1.4.1) — hub task `minecraft:echo_shard`

| Quest | Task item | Feeds |
|---|---|---|
| Heart of the Deep | `deeperdarker:heart_of_the_deep` | Wither's Compass |

The Heart of the Deep is a Warden drop (see `references/boss-checklist.md`); the hub's
description starts *"If only that giant portal in the Ancient City did something!"*

### Eternal Starlight (`eternal_starlight` 0.9.1+1.21.1+neoforge) — hub task `eternal_starlight:book`

| Quest | Task item | Feeds |
|---|---|---|
| Chain of Souls | `eternal_starlight:chain_of_souls` | Dragon Soul |

The hub description says the dimension is entered by beating the **Gatekeeper** at Portal
Ruins in the Overworld — again, boss details live in `references/boss-checklist.md`.

### EvilCraft (`evilcraft` 1.2.96) — hub task `evilcraft:dark_gem`

| Quest | Task item | Feeds |
|---|---|---|
| Lightning Bomb | `evilcraft:lightning_bomb` | Pulsating Black Hole |
| Mace of Destruction | `evilcraft:mace_of_destruction` | Oblivion Shard |
| 2 Piercing Vengeance Focuses | `evilcraft:piercing_vengeance_focus` ×2 | Oblivion Shard |
| Dark Tank full of Eclipse Ember Fuel | `evilcraft:dark_tank` | Philosopher's Fuel |

The Dark Tank task's title is the config's: the tank must hold that fuel. Which fluid id and
how much is JEI/quest-entry territory — not stated here.

### Extreme Reactors (`bigreactors` 1.21.1-2.4.28) — hub task `alltheores:uranium_ingot`

| Quest | Task item | Feeds |
|---|---|---|
| Insanite Blocks | `bigreactors:insanite_block` | Philosopher's Fuel |

The namespace is `bigreactors`; the modlist's display name is Extreme Reactors. The hub
description warns the recipes are confusing — read them in JEI.

### Forbidden & Arcanus (`forbidden_arcanus` — modlist name "Forbidden Arcanus" 2.6.1) — hub task `forbidden_arcanus:arcane_crystal`

| Quest | Task item | Feeds |
|---|---|---|
| Eternal Stella | `forbidden_arcanus:eternal_stella` | Oblivion Shard |
| Smelter Prism | `forbidden_arcanus:smelter_prism` | Philosopher's Fuel |

The **Runic Star Altar** component is also this mod's blocks (see below).

### Generator Galore (`generatorgalore` 1.21.1-1.7.0) — hub task `minecraft:furnace`

| Quest | Task item | Feeds |
|---|---|---|
| 64x Magmatic Generator | `generatorgalore:magmatic_generator_64x` | Philosopher's Fuel |
| Ender Generator | `generatorgalore:ender_generator` | Philosopher's Fuel |
| *(no title in the config)* | `generatorgalore:netherstar_generator_64x` | Wither's Compass |

### Hostile Neural Networks (`hostilenetworks` 6.5.1) — hub task `hostilenetworks:blank_data_model`

| Quest | Task item | Feeds |
|---|---|---|
| Ender Dragon Data Model | `hostilenetworks:data_model` | Dragon Soul |

The hub description: *"Hostile Neural Networks is all about simulating Mobs for farming
their Loot!"* — which is also what the casing quest recommends for the 111,537 nether stars.

### Immersive Engineering (`immersiveengineering` 12.4.2-194) — hub task `immersiveengineering:hammer`

| Quest | Task item | Feeds |
|---|---|---|
| Tesla Coil | `immersiveengineering:tesla_coil` | Nexium Emitter |

### Industrial Foregoing (`industrialforegoing` 1.21-3.6.39) — hub task `industrialforegoing:dryrubber`

| Quest | Task item | Feeds |
|---|---|---|
| Explosive Mycelial Generator | `industrialforegoing:mycelial_explosive` | Pulsating Black Hole |
| Wither Builder | `industrialforegoing:wither_builder` | Wither's Compass |

### Iron Furnaces (`ironfurnaces` 4.3.2) — hub task `minecraft:furnace`

| Quest | Task item | Feeds |
|---|---|---|
| 2 Rainbow Furnaces *(title in the config carries colour codes)* | `ironfurnaces:million_furnace` ×2 | Improbable Probability Device |
| Rainbow Coal *(ditto)* | `ironfurnaces:rainbow_coal` | Philosopher's Fuel |

### Iron's Spells 'n Spellbooks (`irons_spellbooks` 1.21.1-3.16.3) — hub task `irons_spellbooks:arcane_essence`

| Quest | Task item | Feeds |
|---|---|---|
| Lightning Upgrade Orb | `irons_spellbooks:lightning_upgrade_orb` | Improbable Probability Device |
| Wither Skull Scroll | `irons_spellbooks:scroll` | Wither's Compass |

The chapter's hub title reads "Iron's Spells and Spellbooks"; the modlist's display name is
"Iron's Spells 'n Spellbooks". The scroll task is a generic `scroll` id — which spell it
must hold is stated in the quest entry, not here.

### Just Dire Things (`justdirethings` 1.5.7) — hub task `justdirethings:gooblock_tier1`

| Quest | Task item | Feeds |
|---|---|---|
| Paradox Machine | `justdirethings:paradoxmachine` | Pulsating Black Hole |

### Mekanism (`mekanism` 10.7.19) — hub task `alltheores:steel_ingot` (AllTheOres 3.2.0)

| Quest | Task item | Feeds |
|---|---|---|
| 2 Antimatter Pellets | `mekanism:pellet_antimatter` ×2 | Improbable Probability Device |
| *(no title in the config)* | `mekanism:module_gravitational_modulating_unit` | Nexium Emitter |

### Modern Industrialization (`modern_industrialization` 2.5.8) — hub task `modern_industrialization:forge_hammer`

| Quest | Task item | Feeds |
|---|---|---|
| Blastproof Casing | `modern_industrialization:blastproof_casing` | Improbable Probability Device (either/or) |
| Large Advanced Motor | `modern_industrialization:large_advanced_motor` | Nexium Emitter (either/or) |
| Uranium Quad Fuel Rods | `modern_industrialization:uranium_fuel_rod_quad` | Philosopher's Fuel (either/or) |
| — (part of the Runic Star Altar quest) | `modern_industrialization:star_altar` | Runic Star Altar |

### Mystical Agriculture (`mysticalagriculture` 8.0.28) + Mystical Agradditions (`mysticalagradditions` 8.0.14) — hub task `mysticalagriculture:inferium_essence`

| Quest | Task item | Feeds |
|---|---|---|
| Master Infusion Crystal | `mysticalagriculture:master_infusion_crystal` | Creative Essence |
| 4 Insanium Blocks | `mysticalagradditions:insanium_block` ×4 | Creative Essence |
| 4 Insanium Gemstone Blocks | `mysticalagradditions:insanium_gemstone_block` ×4 | Creative Essence |
| Awakened Supremium Ingot Block | `mysticalagriculture:awakened_supremium_ingot_block` | Philosopher's Fuel |
| Insanium Coal Block | `mysticalagradditions:insanium_coal_block` | Philosopher's Fuel |
| Witherproof Bricks | `mysticalagriculture:witherproof_bricks` | Wither's Compass |
| *(no title in the config)* | `mysticalagradditions:nether_star_crux` | Wither's Compass |
| **Creative Essence** *(component)* | `mysticalagradditions:creative_essence` | itself → ATM Star |

The component quest itself (title *Creative Essence*, subtitle *"Ability to create life."*)
has no description in the config; the arithmetic is in the **4 Insanium Blocks** quest's
description instead: *"For Creative Essence you'll need 4 Insanium Essence Blocks. Each
Block is 9 Essence now let me do the math... You'll need 9,216 Inferium Essence to get just
one of these Blocks. So you'll need 36,864 Inferium Essence total!"* (quoted; the two
insanium quests above ask for 4 blocks each).

### Neo Vitae (`neovitae` 1.1.26)

| Quest | Task item | Feeds |
|---|---|---|
| *(no title in the config, no subtitle — this mod's entry quest is the item itself)* | `neovitae:teleposer` | Dimensional Seed |

### Occultism (`occultism` 1.224.4) — hub task `occultism:datura_seeds`

| Quest | Task item | Feeds |
|---|---|---|
| Empty Soul Gem | `occultism:soul_gem` | Dragon Soul |
| Dragon Familiar in a Creature Catcher | `ftbfiltersystem:smart_filter` | Dragon Soul |
| Stable Wormhole | `occultism:stable_wormhole` | Pulsating Black Hole |

The Dragon Familiar quest's description explains the ritual (*"Ihagan's Enthrallment"*,
sacrificing a horse, then a Creature Catcher on the resulting Dragon Familiar) — quoted
flavour, exact ingredients in the quest entry and JEI.

### Oritech (`oritech` 1.2.12) — hub task `oritech:magnetic_coil`

| Quest | Task item | Feeds |
|---|---|---|
| Manhattan Module | `oritech:nuke` | Pulsating Black Hole |

### PneumaticCraft: Repressurized (`pneumaticcraft` 8.2.23) — hub task `pneumaticcraft:ingot_iron_compressed`

| Quest | Task item | Feeds |
|---|---|---|
| Aerial Interface | `pneumaticcraft:aerial_interface` | Improbable Probability Device |
| Micromissiles | `pneumaticcraft:micromissiles` | Pulsating Black Hole |

### Pocket Storage (`pocketstorage` 1.2.5) — hub task `pocketstorage:psu_1`

| Quest | Task item | Feeds |
|---|---|---|
| *(no title in the config)* | `pocketstorage:psu_4` | Pulsating Black Hole |

### Powah (`powah` 6.2.10) — hub task `powah:dielectric_paste`

| Quest | Task item | Feeds |
|---|---|---|
| Nitro Player Transmitter | `powah:player_transmitter_nitro` | Nexium Emitter |

### Productive Bees (`productivebees` 1.21.1-13.13.5) — hub task `minecraft:honeycomb`

| Quest | Task item | Feeds |
|---|---|---|
| Soul Lava Bee Spawn Egg | `productivebees:spawn_egg_configurable_bee` | Dragon Soul |
| Withered Comb Block | `productivebees:configurable_comb` | Wither's Compass |

Both tasks are *configurable* bee/comb items: which bee or comb type the quest wants is set
in the quest entry (the titles say Soul Lava and Withered) — the exact NBT is not
reproduced here.

### Productive Trees (`productivetrees` 1.21.1-1.1.1) — hub task `productivetrees:pollen`

| Quest | Task item | Feeds |
|---|---|---|
| Socotra Dragon Sapling | `productivetrees:socotra_dragon_sapling` | Dragon Soul |

### Roots Classic (`rootsclassic` 1.21.1-1.5.10) — hub task `rootsclassic:verdant_sprig`

| Quest | Task item | Feeds |
|---|---|---|
| *(no title in the config)* | `rootsclassic:crystal_staff` | Pulsating Black Hole |

### Steve's Carts (`stevescarts` — modlist name "StevesCarts2" 1.2.18) — hub task `stevescarts:component_stabilized_metal`

| Quest | Task item | Feeds |
|---|---|---|
| Galadorian Drills | `stevescarts:module_galgadorian_drill` ×2 | Oblivion Shard |

### The Twilight Forest (`twilightforest` 4.8.3345) — hub task `minecraft:diamond`

| Quest | Task item | Feeds |
|---|---|---|
| Snow Queen Trophy | `twilightforest:snow_queen_trophy` | Oblivion Shard |

The hub description gives the portal (a 2×2 water pool surrounded by flowers, drop a
diamond in) and warns: *"Here you'll need to follow a strict order of Bosses to kill and
progress!"* — that order is in `references/boss-checklist.md`.

### Vanilla Minecraft — the Patrick Star blocks

Seven dependency-free quests, all `minecraft` concrete, no titles in the config (the
subtitles are quoted):

| Subtitle (verified) | Task item |
|---|---|
| 13 Wet Dark Pink Blocks | `minecraft:magenta_concrete` ×13 |
| 8 Dry Dark Pink Blocks | `minecraft:magenta_concrete_powder` ×8 |
| 11 Wet Pink Blocks | `minecraft:pink_concrete` ×11 |
| 5 Dry Pink Blocks | `minecraft:pink_concrete_powder` ×5 |
| 8 Wet Green Blocks | `minecraft:green_concrete` ×8 |
| 8 Dry Green Blocks | `minecraft:green_concrete_powder` ×8 |
| 2 Wet Light Green Blocks | `minecraft:lime_concrete` ×2 |

They all feed **Patrick Star** (`allthetweaks:patrick_star`). "Wet" vs "dry" is the pack's
wording for concrete vs concrete powder; that reading is *approximate* — the quest entry
settles it.

## The three components you build rather than collect

**Runic Star Altar** — one quest with 20 item tasks: `modern_industrialization:star_altar`
plus `forbidden_arcanus` blocks (`polished_darkstone` ×64 and further stacks,
`polished_darkstone_stairs` ×64 and ×48, `polished_darkstone_slab` ×20,
`arcane_polished_darkstone_pillar` ×40, `gilded_chiseled_polished_darkstone` ×17,
`arcane_polished_darkstone` ×8, `chiseled_arcane_polished_darkstone` ×4,
`darkstone_pedestal` ×8, `arcane_crystal_obelisk` ×8, `arcane_crystal_block` ×4,
`rune_block` ×16, `quantum_injector`, `magnetized_darkstone_pedestal`, `polished_darkstone`
×2). The description says it is *"a 15x8x15 Structure"* built from the Runic Star Altar
block with a Modern Industrialization wrench, with Item Input/Output Hatches and Energy
Inputs added afterwards. A second untitled quest subtitled *"Runic Star Altar does not work
without upgrades"* lists energy-upgrade options (Runic Attuned Crystals from Forbidden and
Arcanus, or MI upgrades by tier) — quoted numbers, verify in-game.

**The Star's Casing** — `allthemodium:unobtainium_allthemodium_alloy_block` ×28 (made with
an Ars Nouveau Enchanting Apparatus, per the quest text) and
`allthecompressed:nether_star_block_3x` ×15 (*"111,537 Netherstars"*, per the quest text).

**Awakened Unobtainium-Vibranium Alloy Block** — ×2, made in the Star Altar multiblock from
the Unobtainium-Vibranium block plus 4 Unbreaking I books, 4 Awakened Supremium Gemstones
and 4 Awakened Supremium Essence, with *"85 Million FE"* (all quoted from the quest text).

## Boss-gated components

Four components need a boss kill or boss loot, so the star checklist and the boss checklist
have to be read together (`references/boss-checklist.md`):

| Component | Needs | Source chapter |
|---|---|---|
| Oblivion Shard | Snow Queen Trophy | The Twilight Forest |
| Oblivion Shard | Void Forge, Meat Shredder | Cataclysm |
| Dragon Soul | Abyssal Sacrifice | Cataclysm |
| Dragon Soul | Piglich Heart Block | Allthemodium (Chapter 2 / The Other) |
| Dragon Soul | Ender Dragon Data Model | Hostile Neural Networks |
| Wither's Compass | Heart of the Deep (Warden drop) | Deeper and Darker |

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item above is a quest *task*; JEI has the recipe, and the
  recipe is where pack versions differ most.
- **Machine tiers, energy rates, farm layouts, automation.** The chapter's own quests cover
  them; Chapter 4 (`achapter_2r_6the_atm_star`, "Chapter 4: Creative") is where the pack
  puts the post-star automation, including quests titled *Fully Automated ATM Star*, *Runic
  Star Altar*, *Creative Energy Cube*, *Creative Jetpack*, and *Creative Spellbook*.
- **Order.** The book does not require one between components; the dependency links only
  say a component needs its mod lines finished first.
- **Anything not in the config.** If a player asks about a component, mod, or count that is
  not listed here, the answer is "open that quest in the book / look it up in JEI" — never a
  guess.
