# Resource farming guide: where the gated materials come from

**What this page is.** The material map for **All the Mods 10**: for the resources the
quest book treats as progression gates — the three Allthemodium metals, the templates and
mob drops that carry them, the alloy chain that ends in the ATM Star, and the farming
systems the book itself points at for the grindy parts — this page says **where each one
comes from** (dimension, ore, mob drop, or crafting chain) and **roughly which stage of
the game** it belongs to. It exists so a session can answer "where do I actually get
vibranium?" or "do I have to mine unobtainium one block at a time?" with the pack's own
words, instead of a plausible-sounding guess.

## Provenance — everything here was read, not remembered

Every quest title, item id, dimension id, structure id, and quoted sentence below comes
from the official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10),
`main` at the pinned commit **`e5e3d1d83e`** — the same snapshot the sibling endgame docs
were read from (2026-09-22, which `CHANGELOG.md` lists as **pack 8.2**, the "8.x" stamp in
`examples/progress.example.json`).

| File(s) in the pack repo | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/*.snbt` | each quest's task type and value (`item`, `dimension`, `structure`, `kill`, `checkmark`), required counts, and dependency links |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles and the description text quoted below (Minecraft `&` formatting codes stripped) |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (493 entries) |

Chapters read for this page: `allthemodium` (54 quests), `mainquestline_part_1` (36),
`elmystical_agriculturerr` — Mystical Agriculture (191), `productive_bees` (252),
`productive_trees` (167), and `hostile_neural_networks` (50). The star chapter itself is
mapped in `references/atm-star-checklist.md`, its bosses in
`references/boss-checklist.md`, and its post-star content in
`references/creative-checklist.md`; this page covers where the materials come from.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **"Where it is found" is either the quest's own words or a task type.** A quoted sentence
  is the pack author's; where the source is a `dimension`, `structure`, or `kill` task,
  that proves the book *tracks* that place or mob — not that the resource exists nowhere
  else. Ore distribution, biome rarity, and Y levels are exactly the details this page does
  not state: they are version-sensitive, and the player reads them off the quest entry and
  JEI. Treat every distribution detail here as approximate.
- **No recipes, no coordinates, no ore levels.** The config lists *what a quest wants*,
  never *how to craft it*; the few recipe-shaped sentences below are quotes from the
  quest's own description, marked as such. Never invent an item id, dimension, coordinate,
  or count: if a detail is not here, the answer is "check the quest entry / JEI".
- **Untitled quests are marked.** 47 of `allthemodium`'s 54 quests carry an explicit title
  in the lang file; for the rest the book shows the task item's own name, so a derived
  title would be a guess. `*(no title in the config)*` marks those in place — never present
  a derived name as a verified title.
- **Stages are the skill's, not the pack's.** The stage column combines
  `references/progression.md`'s four stages with the chapter a quest lives in and the
  dependency links around it. The pack gates nothing: its Welcome chapter says *"In this
  modpack, quests are optional. Mods are not gated behind completing any quests!"*

## The gated materials at a glance

"Tracked by" = chapter → verified quest title. Item ids are the config's own.

| Material | Where it comes from | Tracked by | Stage |
|---|---|---|---|
| Allthemodium (`allthemodium:allthemodium_ingot`) | Overworld ore in the cave walls around **Ancient Cities** and any **Deep Dark** biome | Chapter 2: Allthemodium → *Ancient City*, *Allthemodium Ingot* | endgame, the first gate |
| Vibranium (`allthemodium:vibranium_ingot`) | ore: rarely in **The Nether**, abundantly in **The Other** | Chapter 2: Allthemodium → *Vibranium Ingot* | endgame |
| Unobtainium (`allthemodium:unobtainium_ingot`) | ore: very rarely in **End Highlands** biomes, The End | Chapter 2: Allthemodium → *Unobtainium Ingot* | endgame |
| Allthemodium Smithing Template | archaeology: brush suspicious clay on **Ancient City** floors | Chapter 2: Allthemodium → *Allthemodium Smithing Template* | endgame |
| Vibranium Smithing Template | archaeology: brush suspicious soul sand in **Bastions**, The Nether | Chapter 2: Allthemodium → *Vibranium Smithing Template* | endgame |
| Unobtainium Smithing Template | **Trial Spawners** in The Other's **Dungeon** structure, Library Rooms | Chapter 2: Allthemodium → *Unobtainium Smithing Template* | endgame |
| Piglich Heart (`allthemodium:piglich_heart`) | mob drop: the **Piglich** boss, **Ancient Pyramid** in The Other | Chapter 2: Allthemodium → *Piglich Boss*, *Ancient Pyramid* | endgame |
| The three alloys | crafting chain: three different mod multiblocks, each wanting Piglich Hearts | Chapter 2: Allthemodium → *Vibranium - Allthemodium Alloy Ingot*, *Unobtainium - Allthemodium Alloy Ingot*, *Unobtainium - Vibranium Alloy Ingot* | endgame |
| Netherite | Ancient Debris → scraps + gold | Chapter 1: The Beginning → *Ancient Metals*, *Netherite Tier*, *Netherite Template* | early-game |
| Creative Essence (`mysticalagradditions:creative_essence`) | Mystical Agriculture: after the *Insanium* tier of the essence ladder | Mystical Agriculture → *Creative Essence* | endgame (the star wants it) |
| Awakened Supremium | Mystical Agriculture: Awakening Altar, or farmed with Productive Bees | Mystical Agriculture → *Awakened Supremium*, *The Awakening*, *Cognizant Dust*, *Automating Awakened Supremium* | tech → endgame |
| Nether Star | Wither kill, then farming routes: Hostile Neural Networks or nether star seeds | Hostile Neural Networks → *Creating Loot*; Mystical Agriculture → *(no title in the config)* nether star seeds | endgame (the star wants 111,537 of them, per the star checklist's quote) |

## Allthemodium — the first gate

The chapter hub quest is simply titled **Allthemodium**, and its task is a
`minecraft:netherite_ingot` — the book's way of saying Chapter 2 starts after vanilla is
finished. Everything below hangs off it in the order the dependency links give.

**For the mining detail — which dimension each of the three ores is in, where in it
they spawn, and what pickaxe / harvest tier each needs — see the companion page
`references/allthemodium-mining-guide.md`.** This page says *where a material comes
from*; that one says *how to go get the ore out of the ground*, quoting the pack's own
in-game ore tooltips and the Basic Tools chapter's Harvest Tier ladder.

- **Where.** *Ancient City* is a `structure minecraft:ancient_city` task whose description
  says: *"You can find the Ore in the walls of Caves around the Ancient Cities, it's
  Glowing so it'll be easy to spot just very rare!"* and *"You will also be able to locate
  it in any Deep Dark Biome."* (The same biome is a Chapter 1 task — *Visit The Deep
  Dark!* — so the trek is already on the book's map before Chapter 2 opens.)
- **What gates it.** The *Allthemodium Ingot* quest: *"To mine Allthemodium you'll need a
  Pickaxe that is Netherite Tier or higher!"* — that is the whole gate; there is no quest
  required first.
- **Ore processing is the book's own tip.** Same quest: *"first I recommend processing it
  either with Fortune, Occultism, or Mekanism to get more"*. Chapter 1's *Basic Ore
  Doubling* makes the same point for the early game: *"one of the easiest ways is by
  creating and using an Ore Hammer. ... Want more per raw ore? Check out the mod
  Occultism!"*
- **Then the pad.** *Allthemodium Ingot* continues: *"I recommend making 2 Teleport Pads
  with the Nuggets! You can use those to get to the Mining Dimension to find more
  Allthemodium or The Other to find other adventures."*
- **The Mining Dimension is the strip-mine answer.** Its pad goes down in the Overworld —
  the *Overworld* quest: *"Place the Teleport Pad in the Overworld to go to the Mining
  Dimension."* — and the *Mining Dimension* quest (a `dimension allthemodium:mining` task)
  describes it as *"a Superflat world with absolutely nothing on the surface. Below the
  surface is almost every single Ore."* with *"no Caves, no Mob Spawns, and nothing to get
  in your way"* — and warns that *"Ore spawns differ for the Y Level and layer"*. One untitled follow-up in the same chapter, a checkmark
  *(no title in the config)*, adds the modern caveat: quarries may *"Mine Allthemodium but
  Void the drops"*, so *"might want to be careful with your Quarries now!"*

## Vibranium — the Nether, or better, The Other

The *Vibranium Ingot* quest is the next ore step: *"Vibranium is the next ore after
Allthemodium, so of course it requires Allthemodium Pickaxe (or the same tier) to mine
it. You can find it rarely in The Nether or abundantly in The Other. It is also recommend
to Ore Process it to get more."* The *The Nether* quest before it is what places the
Teleport Pad — *"Place the Teleport Pad in The Nether to go to The Other."* — so the pad
built from Allthemodium Nuggets is the route to the better vibranium source.

The *The Other* quest (a `dimension allthemodium:the_other` task) is honest about the
trade: *"You can also mine for Vibranium (and other ores!) or find it and better in the
structures!"* — its structures being *"Piglin Village, Ancient Pyramid, and Dungeon"* —
and *"You can't set up Quarries for many blocks in The Other though, no cheesing anything
here."*

## Unobtainium — the End, not The Beyond

The *Unobtainium Ingot* quest opens by closing the obvious shortcut: *"No it isn't found in
The Beyond. You can find Unobtainium Ore very rarely in End Highlands Biomes. Those are
usually where End Cities spawn as well! You'll need a Vibranium Pickaxe (or same Tier) to
Mine the Ore."* The *The End* quest is the matching pad placement — *"Place the Teleport
Pad in The End to go to The Beyond."* — and *The Beyond* itself (a
`dimension allthemodium:the_beyond` task) is described as *"There's nothing here! You
might want an Angel Block."* So the third metal sends the player back to the End's high
biomes rather than to the new dimension.

## The three templates — archaeology and trial spawners

The smithing templates gate the gear tiers, and each comes from a different kind of site:

- *Allthemodium Smithing Template*: *"To get it you'll need to Brush suspicious Clay. You
  can find it in the floors of the Ancient City."*
- *Vibranium Smithing Template*: *"This one you can find by Brushing Suspicious Soul Sand.
  Which is found in Bastions in The Nether."*
- *Unobtainium Smithing Template*: *"You'll have to earn these by beating the Trial
  Spawners which are found in the Dungeon structure in The Other. More specifically the
  Library Rooms!"*

## Piglich Heart — the one mob drop the alloys need

The *Ancient Pyramid* `structure allthemodium:ancient_pyramid` quest leads to the *Piglich
Boss*, whose task item is `allthemodium:piglich_heart`. The quest text: *"The Piglich is a
Boss added by Allthemodium. He has 9999 Hearts and currently has no attacks but trust me
when he does they will be devastating! When killed he'll drop his Heart which will be
needed for Alloys and the ATM Star! (Look into ways of farming them like with HNN or
EnderIO!)"* — the pack's own pointer to the farming systems below. The star chapter's
own complaint about nether stars (*"Please I am begging you use HNN"*, quoted in
`references/atm-star-checklist.md`) is the same advice for a different drop.

## The three alloys — crafting chains, not ores

Each alloy quest is a one-line description and a crafting step, but the three merge quests
in between name the machine and its bill:

| Alloy (config item id) | Verified quest title | The chain, per the config's quest text |
|---|---|---|
| `allthemodium:vibranium_allthemodium_alloy_ingot` | *Vibranium - Allthemodium Alloy Ingot* | Powah's **Energizing Orb** (`powah:energizing_orb`, Powah 6.2.10): *"Place the Ingots, 2 Piglich Hearts, and a Compressed Block of Nitro Crystals X1 into the Orb (order doesn't matter). Then once 1 Billion FE is put into the Orb through the Rods it'll be ready!"* |
| `allthemodium:unobtainium_allthemodium_alloy_ingot` | *Unobtainium - Allthemodium Alloy Ingot* | Ars Nouveau's **Enchanting Apparatus** (`ars_nouveau:enchanting_apparatus`, Ars Nouveau 5.13.1): *"Start with an Arcane Core then put the Enchanting Apparatus ontop of it. Next, place Pedestals around the Enchanting Apparatus at the same Y Level. ... have Source nearby, and place the Source Gem in the Apparatus it will start!"* |
| `allthemodium:unobtainium_vibranium_alloy_ingot` | *Unobtainium - Vibranium Alloy Ingot* | Industrial Foregoing's **Dissolution Chamber** (`industrialforegoing:dissolution_chamber`, Industrial Foregoing 1.21-3.6.39): *"You'll need Pink Slime which you get from the Mob Slaughter Factory ... You'll also need Soul Lava ... found in The Other, common in the Piglin Village. After those you'll need to put your Ingots and Piglich Hearts in the exact order, power it, and it'll be done!"* |

All three depend on the *Piglich Boss* quest as well as their machine hub, so the heart
farm comes first. The three merge quests themselves carry no title in the config — each is
*(no title in the config)* and its task is that machine item
(`ars_nouveau:enchanting_apparatus`, `powah:energizing_orb`,
`industrialforegoing:dissolution_chamber`), which is how the book names them.

**Supporting materials dragged in:** Pink Slime (Mob Slaughter Factory), Soul Lava (The
Other, Piglin Village), Compressed Nitro Crystals (Powah's own chain), and — for the alloy
*tools*, not the ingots — Forbidden Arcanus's Eternal Stella: *"Eternal Stella can be used
to either make an Item Unbreakable ... Or you can use it to craft Alloy Tools!"*, per the
untitled `forbidden_arcanus:eternal_stella` quest *(no title in the config)* that the
tool quests depend on (`allthemodium:alloy_paxel` — *Allthemodium Alloy Paxel* — and its
sword/pick/shovel/axe/trident siblings).

## Farming the gated materials instead of mining them

Three resource-production chapters in the book's Resources group replace hand-farming of
materials — Mystical Agriculture, Productive Bees, and Hostile Neural Networks — and the
quests around the gated metals lean on all three.

### Mystical Agriculture (`elmystical_agriculturerr`, 191 quests)

The essence ladder runs *Inferium* → *Prudentium* → *Tertium* → *Imperium* → *Supremium* →
*Awakened Supremium* → *Insanium*, with *The Awakening* multiblock (Awakening Altar +
pedestals + Essence Vessels) and *Cognizant Dust* in between — *"dropped from the Wither
and the Ender Dragon when killed by an Essence Weapon enchanted with Mystical
Enlightenment"*. What matters for the gated metals:

- **Allthemodium, Vibranium and Unobtainium seeds exist** as endgame crops
  (`mysticalagriculture:allthemodium_seeds`, `mysticalagriculture:vibranium_seeds`,
  `mysticalagriculture:unobtainium_seeds`), each requiring *"Magical Soil placed below in
  order for them to grow"* (`kubejs:magical_soil`).
  Their quests are untitled in the config *(no title in the config)* and depend on
  *Insanium Farmland* and the *Infusion Altar*.
- **Nether Star, Dragon Egg and Nitro Crystal seeds** exist the same way: *"Nether Star
  Seeds require a Nether Star Crux placed below in order for them to grow"*, *"Dragon Egg
  Seeds require a Dragon Egg Crux placed below"*, *"Nitro Crystal Seeds require a Nitro
  Crystal Crux placed below"*. The *Insanium Farmland* quest states the rule: *"To grow
  Tier 6 or Magical Seeds you need to have a certain Crux placed directly below the
  Farmland they are growing on."*
- **The star's own crops** are tracked by titled quests: *Creative Essence* — *"Creative
  Essence is needed to craft the ATM Star."* — plus two untitled quests whose descriptions
  say an *Insanium Coal Block* and an *Awakened Supremium Ingot Block* are each *"needed
  to craft the ATM Star."*
- **Bees farm the top tier**: the *Automating Awakened Supremium* quest says *"Awakened
  Supremium and other tiered essences can be farmed using the Productive Bees mod."*

### Productive Bees (`productive_bees`, 252 quests)

The metal chain is a small, titled lineage — *Diamond Bee* → *Ancient Bee* →
*Allthemodium Bee* → *Vibranium Bee* → *Unobtainium Bee* — and each step is a Foundry
pour, per the quest text:

- *Allthemodium Bee*: *"Using a Foundry, pour Molten Allthemodium over an Ancient Bee
  Spawn Egg."*
- *Vibranium Bee*: *"Using a Foundry, pour Molten Vibranium over an Allthemodium Bee Spawn
  Egg."*
- *Unobtainium Bee*: *"Using a Foundry, pour Molten Unobtainium over an Vibranium Bee Spawn
  Egg."*

Every bee quest's task is `productivebees:configurable_honeycomb`, and the chapter's
opening warning applies to all of them: *"With the bee quests requiring combs, the recipes
will not be shown. Make sure to look them up in JEI if you need them!"* — so treat the
pours as direction, not as a recipe. (*Ancient Bee* sits behind *Diamond Bee*; *Draconic
Bee*, the end-tier bee, is lured with an Obsidian Nest in the End — its chain is its own,
not a shortcut to the three metals.)

### Hostile Neural Networks (`hostile_neural_networks`, 50 quests)

HNN is the mob-drop farm: *"Hostile Neural Networks (HNN for short) is a mod based around
simulating mob kills for loot!"* — the player collects data on mobs and runs simulations
from that data to produce their drops. The core line is *Welcome to Hostile Neural
Networks!* → *Modeling Mobs* /
*Learning Mobs* → *Simulating Deaths* → *Creating Loot* (Simulation Chamber
`hostilenetworks:sim_chamber`, Loot Fabricator `hostilenetworks:loot_fabricator`, Deep
Learner `hostilenetworks:deep_learner`), with *The Data Center* as the 7x7x7 endgame
multiblock. The *Creating Loot* quest gives the examples the rest of the book leans on:
*"Examples of Mob Predictions: - Ender Dragons for Dragon Eggs - Zombies for Iron -
Withers for Nether Stars"* — the route the star chapter's own quest text asks for (see
the *"Please I am begging you use HNN"* quote in `references/atm-star-checklist.md`).

### Productive Trees (`productive_trees`, 167 quests)

Tracked as a Resources chapter too (wood, saplings, and their products; e.g. *Productive
Trees*, *Sawing*, *Stripping*), but only five quests carry an explicit title in the config
and none of them names a progression-gated metal. Treat it as base-material farming, and
defer to the in-game book and JEI for what each tree yields.

## Early-game resource beats the book tracks (Chapter 1)

For "what do I farm first?", the Main Questline's own resource quests are the answer:
*Basic Ore Doubling* (Ore Hammer, or Occultism for more per ore), *Netherite Template*
(*"find the Netherite Smithing Template in chests found inside of Bastions"*), *Ancient
Metals* (*"Ancient Debris. This can be smelted down into Scraps that can be combined with
Gold to create Netherite Ingots"*), *Netherite Tier*, *We've Struck Diamonds!*, and
*Visit The Deep Dark!* — which is also where the Allthemodium line will send the player
back, several stages later.

## Using this page in a session

1. Find the material in the table above, then quote the quest title and the pack's own
   words about where it comes from — keep the hedges ("rarely", "very rarely",
   "approximate").
2. Map the player's stage with `references/progression.md`; the gated metals are all
   endgame, the farm systems are tech, and the Chapter 1 beats are early-game.
3. Send the player to the in-game quest entry and JEI for counts, recipes, ore levels, and
   current drops — and to `references/atm-star-checklist.md`,
   `references/boss-checklist.md`, and `references/creative-checklist.md` for what the
   materials are *for*.
4. Never answer a "where do I find it?" question from memory when the material is not on
   this page: "let's check your quest book / JEI" is the correct answer.
