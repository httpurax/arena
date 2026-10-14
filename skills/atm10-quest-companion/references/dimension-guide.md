# Dimension guide: which dimension to open first, and when

**What this page is.** A dimension map for **All the Mods 10**: every dimension the pack's
quest book actually sends the player to, what opens it, which chapter and stage it belongs
to, what the book sends you there for (bosses, resources, key quests), and a recommended
order to open them in. It exists so a session can answer "where do I go next, and am I
ready for it?" without inventing a portal.

## Provenance — everything here was read, not remembered

Every dimension id, quest title, task, dependency link, and quoted sentence below comes from
the official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at
`main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File(s) in the pack repo (at that commit) | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/*.snbt` | every `dimension` task, the `advancement`, `structure`, `biome`, `kill` and `item` tasks around them, and the dependency links the visit order leans on |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, task titles, and the description text quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt`, `chapter_group.snbt` | chapter titles and the quest-book group each chapter sits in |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |

**How the list was built.** All 66 chapter files (4,790 quests) were scanned for
`dimension` tasks: there are **28**, in 15 chapters, naming **12 dimension ids**. Two
`advancement` tasks stand in for entering a dimension — Chapter 1's
`minecraft:story/enter_the_nether` and the Twilight Forest's `twilightforest:root` — and the
Twilight Forest has no `dimension` task at all. Together that is the whole set: the **13
destinations** below.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a snapshot
  of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **The book gates nothing.** Its Welcome chapter says so: *"In this modpack, quests are
  optional. Mods are not gated behind completing any quests!"* Every "unlocked by" below is
  what the *game* needs — an item, a boss kill, a structure — plus the quest that tracks it,
  never a lock the book puts on the dimension.
- **Portals are quoted, never reconstructed.** For each dimension the page names the quest
  that opens it, the task items the config gives that quest, and — where the quest's own
  description explains the way in — a short quote marked as quest text. **No portal
  recipes:** how to craft a Teleport Pad, a Catalyst, or an Orb of Prophecy is JEI's
  answer, and a frame the quest text does not spell out is never filled in from memory.
- **No coordinates.** None, not even "roughly": places are named the way the config names
  them — a dimension, a biome, a structure. Where a quest's text carries a location hint,
  this page points at that quest instead of copying its numbers.
- **"Roughly when" and the visit order are approximate by construction.** Each step says
  what is **verified** (a dependency link in the config, or a sentence in a quest's text)
  and what is *approximate* (a readiness judgement). The **stage tag** is the skill's
  bookkeeping bucket from `examples/progress.example.json`, not a difficulty rating: all
  nine Exploration chapters are tagged `endgame` there, including the ones that are
  comfortable much earlier (`references/progression.md` says the same).
- **Nothing here was invented, and nothing is added from memory.** Never invent a
  dimension, a portal, an item id, or a coordinate: a dimension that is not in the config is
  not on this page, and if a player names one, the answer is "let's check your quest book /
  JEI" — never a plausible-sounding guess.

## The dimensions at a glance

In recommended visit order — the reasoning is in
[The recommended visit order](#the-recommended-visit-order) below.
"Unlocked by" = the verified quest title(s) on the way in; "stage tag" = the skill's stage
for that chapter; "roughly when" is approximate.

| # | Dimension | Dimension id (config) | Unlocked by (verified quest) | Chapter (config id) · group | Stage tag | Roughly when | Go there for |
|---|---|---|---|---|---|---|---|
| 1 | Overworld | `minecraft:overworld` | — you start here (*Welcome to All The Mods 10!*) | Welcome (`welcome`) | `early-game` | from the start | everything early; the Ancient Cities and Portal Ruins later dimensions start from |
| 2 | The Nether | `minecraft:the_nether` | Chapter 1 *To The Nether!* | Chapter 1: The Beginning (`mainquestline_part_1`) · Main Questline | `early-game` | early — right after diamonds | Netherite, the Wither; Vibranium later |
| 3 | The Twilight Forest | none — entry is the advancement `twilightforest:root` | *Welcome to the Twilight Forest!* | The Twilight Forest (`twilight_forest`) · Exploration | `endgame` | opens early (a diamond); the boss line runs late | a strictly ordered boss line ending at the Snow Queen — **star component** |
| 4 | The End | `minecraft:the_end` | Chapter 1 *Finding The End* → *The End* | Chapter 1: The Beginning · Main Questline | `early-game` | the close of Chapter 1 | the Ender Dragon (also your pass past the Gatekeeper, row 9); Unobtainium later |
| 5 | The Bumblezone | `the_bumblezone:the_bumblezone` | *The Bumblezone!* → *Into the Hive* | The Bumblezone (`bumblezone`) · Exploration | `endgame` | early→mid | the Bee Queen's 16 quests and 32 structures; no boss, nothing the star needs |
| 6 | The Aether | `aether:the_aether` | *Aether Portal* → *The Aether* | The Aether (`aether`) · Exploration | `endgame` | mid, after the Nether | three dungeons and their bosses, Zanite and Gravitite gear; nothing the star needs |
| 7 | The Undergarden | `undergarden:undergarden` | *The Undergarden* → *Welcome to the Undergarden!* | The Undergarden (`undergarden`) · Exploration | `endgame` | mid; its Depths later | the Catacombs and the Forgotten Guardian; Cloggrum, Froststeel, Utheric, Forgotten ingots |
| 8 | The Otherside | `deeperdarker:otherside` | *Kill the Warden* → *Heart of the Deep* → *The Otherside* | Deeper and Darker (`deeper_and_darker`) · Exploration | `endgame` | mid-late — after the Warden | Ancient Temples, Warden-gear materials, the Soul Elytra |
| 9 | The Starlight (Eternal Starlight) | `eternal_starlight:starlight` | *The Gatekeeper and The Gate* → *Eternal Starlight* | Eternal Starlight (`eternal_starlight`) · Exploration | `endgame` | late — after the Ender Dragon | the Lunar Monstrosity (Chain of Souls — **star component**), the Starlight Golem, new ores |
| 10 | Mining Dimension | `allthemodium:mining` | Chapter 2 *Teleport Pad* → *Overworld* → *Mining Dimension* | Chapter 2: Allthemodium (`allthemodium`) · Main Questline | `endgame` | Chapter 2 — one of the first two pads | ore without caves or mobs: more Allthemodium |
| 11 | The Other | `allthemodium:the_other` | Chapter 2 *Teleport Pad* → *The Nether* → *The Other* | Chapter 2: Allthemodium · Main Questline; Ice and Fire (`ice__fire`) · Exploration | `endgame` | Chapter 2 — one of the first two pads | Vibranium, the Piglich (**star component**), Ice and Fire, the Unobtainium Smithing Template, Soul Lava, the Divine Pact |
| 12 | The Beyond | `allthemodium:the_beyond` | Chapter 2 *Teleport Pad* → *The End* → *The Beyond* | Chapter 2: Allthemodium · Main Questline | `endgame` | optional | empty building space — *"There's nothing here!"* |
| 13 | Neo Vitae's realm | `neovitae:dungeon` | *Tier III: The Master's Orb* → *Highway to Hell* / *Breaching the Veil* | Neo Vitae (`neo_vitae`) · Magic | `magic` | late in that chapter | the Mines and the Foreman, Demonite, Hellforged Parts |

## Dimension by dimension

### 1. Overworld (`minecraft:overworld`)

- **Unlocked by:** nothing — you start here. The Welcome chapter's first quest, *Welcome to
  All The Mods 10!*, is itself a `dimension minecraft:overworld` task.
- **Chapter / stage:** Welcome (`welcome`, 6 quests), a standalone chapter · `early-game`.
- **Roughly when:** from the start, and back again all game.
- **Go there for:** the doors to other dimensions sit here —
  - **Ancient Cities** (`structure minecraft:ancient_city`): Chapter 2's *Ancient City*,
    where its Allthemodium line starts, and Deeper and Darker's *Visit an Ancient City*,
    whose Warden drops the Heart of the Deep and whose Reinforced Deepslate frame is the
    Otherside portal (row 8).
  - **Portal Ruins** (`structure #eternal_starlight:portal_ruins`): Eternal Starlight's
    *The Gatekeeper and The Gate* (row 9).
  - **Boss arenas and relics:** Cataclysm's *Overworld: Land of 3 4 5 bosses*, Iron's
    Spells' *Adventure Time!* (*"There's 6 structures in the Overworld that the bosses can
    spawn in!"*), Relics' *Overworld*, and Forbidden & Arcanus' *Relics*.
- **Not a visit:** Apothic Enchanting's *A Gate* and *Another Gate* are `dimension
  minecraft:overworld` tasks used as switches (*"This gate only exists to allow for either
  the Seashelf or Hellshelf path to be taken while also forcing the Frontier World Tier
  quest from Apotheosis Gear."*), and The Aether's *Whoops!* completes when you fall out of
  the Aether (*"Next time, just use the Portal!"*).

### 2. The Nether (`minecraft:the_nether`)

- **Unlocked by:** Chapter 1's *To The Nether!* — tasks `minecraft:obsidian` ×10 and the
  advancement `minecraft:story/enter_the_nether`; it depends on *We've Struck Diamonds!*
  (`minecraft:diamond`). Quest text: *"With a Diamond tier pickaxe, you'll be able to mine
  Obsidian. Obsidian can be used to create a portal to the Nether."*
- **Chapter / stage:** Chapter 1: The Beginning (`mainquestline_part_1`, 36 quests) · Main
  Questline · `early-game`.
- **Roughly when:** early — the Main Questline's next step after diamonds (**verified**
  dependency).
- **Go there for:** Chapter 1's *Ancient Metals* (`minecraft:netherite_ingot`) → *Netherite
  Tier*, and *Summoning The Wither* → *Kill The Wither*; *Finding The End* also hangs off
  *To The Nether!*. Later, Chapter 2's *The Nether* (where the Teleport Pad goes for The
  Other), *Vibranium Ingot* (*"You can find it rarely in The Nether or abundantly in The
  Other."*), and *Vibranium Smithing Template* (from Bastions, per its text). Arenas and
  loot: Cataclysm's *Nether: Land of 2 bosses*, Iron's Spells' *On a Highway to...*
  (*Citadel*, *Ancient Battleground*), and Relics' *The Nether* (*"These Relics can be
  found in Ruined Portals, Nether Fortresses, and Bastions throughout The Nether!"*).

### 3. The Twilight Forest

- **Unlocked by:** *Welcome to the Twilight Forest!* (subtitle *Enter the Twilight Forest*),
  whose task is the advancement `twilightforest:root` — the config has no `dimension` task
  for the Twilight Forest, so this page gives no dimension id for it. Quest text: *"To
  create the portal to get to the Twilight Forest, make a 2x2 hole in the ground and fill it
  with water. Surround the edges of the hole with flowers, and throw a Diamond into the
  water."* Chapter 3's *Twilight Forest* quest asks for `minecraft:diamond` and says the
  same.
- **Chapter / stage:** The Twilight Forest (`twilight_forest`, 56 quests) · Exploration ·
  `endgame` tag. Mod: The Twilight Forest 4.8.3345.
- **Roughly when:** opening it is early — Chapter 1's *We've Struck Diamonds!* says
  diamonds *"also allow you to visit new dimensions like the Twilight Forest!"*
  (**verified** quest text). Finishing it is not: the boss line is strictly ordered and its
  tail is late (*approximate*).
- **Go there for:** the boss line, in the chapter's verified dependency order — *Evening The
  Scales* (Naga) → *Bring out your Dead* (Lich) → *To the Swamps!* → *Mighty Meef
  Stroganoff* (Minoshroom) → *Hydra Slayer* → *The Dark Forest* (Knight Phantoms) → *Tears
  of Fire* (Ur-Ghast) → *To the Snow Biomes!* (Alpha Yeti) → *Clear Skies* (Snow Queen) →
  *Visiting the Giants* → an untitled quest (subtitle *The giants look like me, but are
  nothing LIKE me*) → *Lamp of Cinders* → *Every Thorn has its Rose* → *The Final Boss* →
  *The Real Final Boss*. Trophies and arenas: `references/boss-checklist.md`. Gear: Basic
  Armor's *Ironwood Armor*, *Steeleaf Armor*, *Knightmetal Armor*, *Fiery Armor*, *Arctic
  Gear*, and *Yeti Outfit* all point here.
- **Star relevance:** Chapter 3's *Snow Queen Trophy* (`twilightforest:snow_queen_trophy`)
  feeds the Oblivion Shard — *"You'll need to kill the Alpha Yeti in order to enter the
  Glacier Biome."* Chapter 3's *Twilight Forest* quest warns: *"Here you'll need to follow
  a strict order of Bosses to kill and progress!"*

### 4. The End (`minecraft:the_end`)

- **Unlocked by:** Chapter 1's *Finding The End* — tasks `minecraft:ender_eye` ×10 and the
  advancement `minecraft:story/follow_ender_eye` — then *The End* (advancement
  `minecraft:end/dragon_egg`). Quest text: *"Make your way to the Stronghold, find the End
  Portal, and complete the frame using the Eyes of Ender to create the portal to The End."*
- **Chapter / stage:** Chapter 1: The Beginning · Main Questline · `early-game`.
- **Roughly when:** the close of Chapter 1 (**verified**: *To The Nether!* → *Finding The
  End* → *The End*).
- **Go there for:** the Ender Dragon (*"In The End, you'll find the final boss of Vanilla
  Minecraft: The Ender Dragon."*) — which is also what lets the Eternal Starlight
  Gatekeeper wave you through (row 9). Later: Chapter 2's *The End* (where the Teleport Pad
  goes for The Beyond) and *Unobtainium Ingot* (*"You can find Unobtainium Ore very rarely
  in End Highlands Biomes."*); Cataclysm's *End: Land of 1 lonely boss*; Draconic
  Evolution's *Where is he?* (subtitle *Finding Chaos Island*: *"To get into Draconic
  Evolution you'll need Chaos Shards. Chaos Shards are in Chaos Islands guarded by Chaos
  Guardians in the End."* — the quest's own text says where to look); Relics' *The End*.

### 5. The Bumblezone (`the_bumblezone:the_bumblezone`)

- **Unlocked by:** *The Bumblezone!* → *Into the Hive* (subtitle *Unbeelievable*). Quest
  text: *"To get into the Bumblezone you'll first need a Beehive. Normal Beehives and
  Advanced Beehives it's not picky!"* and *"Then you'll need to either throw an Enderpearl
  into it or have a Piston push you into it!"* The way back is the *Escaping* quest: *"This
  Void won't kill you, instead it will teleport you back to where you were in the
  Overworld!"*
- **Chapter / stage:** The Bumblezone (`bumblezone`, 114 quests) · Exploration · `endgame`
  tag. Mod: The Bumblezone 7.16.1.
- **Roughly when:** early→mid (*approximate*): the way in needs only a beehive and an ender
  pearl. Read the chapter's untitled phobia-warning quest (subtitle *Bee careful!*) first.
- **Go there for:** no boss fight. *Throne Pillar* → *Your Highness* (the Bee Queen,
  advancement `the_bumblezone:the_queens_desire/the_beginning`): *"In order to advance in
  Bumblezone you will need Bee Essence which you get from doing all 16 of her quests."* Plus
  eight biome quests, 32 `structure` quests (the *Honey Compass* finds the *Cell Maze*), and
  Basic Armor's *Bee Armor 1* and *Bee Armor 2*.
- **Star relevance:** none — no Chapter 3 or Chapter 4 task names a Bumblezone item.

### 6. The Aether (`aether:the_aether`)

- **Unlocked by:** *Aether Portal* → *The Aether*. The portal quest's tasks are
  `minecraft:glowstone` ×10 and a `minecraft:water_bucket`; its text is a joke about the
  old glowstone-and-water portal (*"Yeah right, I'm not 7, I'm not falling for that
  again!"*) — read the quest in-game and do not guess the frame.
- **Chapter / stage:** The Aether (`aether`, 73 quests) · Exploration · `endgame` tag. Mod:
  The Aether 1.5.10.
- **Roughly when:** mid (*approximate*). Glowstone is a Nether material in vanilla, so the
  Aether naturally follows the Nether; JEI may show other sources in ATM10.
- **Go there for:** *"The Aether is a Sky Dimension, flying high above the Overworld."*
  Three dungeons, each hanging directly off *The Aether* with no order between them in the
  config: *Bronze Dungeon* (*"The Bronze Dungeon is the easiest and simplest Dungeon."*) →
  *The Slider* → *Bronze Key*; *Silver Dungeon* (*"The Silver Dungeon is the easiest
  Dungeon to find because its above ground."*) → *10 Victory Medals* → *Valkyrie Queen* →
  *Silver Key*; *Gold Dungeon* → *Sun Spirit* → *Gold Key*. Materials: *Ambrosium*,
  *Zanite*, *Gravitite*, *Skyroot Trees*, *Holystone*, *Aerclouds*.
- **Star relevance:** none — no other chapter in the book asks for an `aether:` item, so the
  Aether is optional for the star.

### 7. The Undergarden (`undergarden:undergarden`)

- **Unlocked by:** *The Undergarden* (subtitle *Making the Portal*; task
  `undergarden:catalyst`) → *Welcome to the Undergarden!*. Quest text: *"Getting to the
  Undergarden is similar to getting to The Nether. You'll need to craft a Portal."* and
  *"Once formed, you can activate it by using the Catalyst on it."* The frame materials are
  in that quest's text; the Catalyst's recipe is JEI's.
- **Chapter / stage:** The Undergarden (`undergarden`, 82 quests) · Exploration · `endgame`
  tag. Mod: The Undergarden 0.9.6.
- **Roughly when:** mid (*approximate*), with its deepest layer later — the chapter's
  *Greater Dweller* says *"You'll need a Forgotten Pickaxe or Allthemodium Pickaxe to Mine
  the Dreadrock in the way."*
- **Go there for:** *Catacombs* (`structure undergarden:catacombs`) → *Forgotten Guardian*
  (the Bounty Board's *Kill The Forgotten Guardian*: *"The Forgotten Guardian is the Boss
  of the Undergarden."*); the *Rotbeast*; materials *Cloggrum* (*"Cloggrum is the Iron of
  the Undergarden."*), *Froststeel*, *Utheric*, *Regalium* (*"Regalium is the Emerald
  equivalent in Undergarden."*), and *Forgotten* (*"Forgotten Ingots need to be obtained
  through the Catacombs; whether it be looting the Chests or killing the Forgotten
  Guardian."*); the *Forgotten Vestige* ruins. Basic Armor's *Cloggrum Armor*, *Froststeel
  Armor*, and *Utherium Armor* point here. Read *Warning* (Utheric infection) before a long
  trip.
- **Star relevance:** none in Chapter 3 or Chapter 4.

### 8. The Otherside (`deeperdarker:otherside`)

- **Unlocked by:** the chapter's verified spine *Visit an Ancient City* (`structure
  minecraft:ancient_city`) → *Kill the Warden* (`kill minecraft:warden`) → *Heart of the
  Deep* (`deeperdarker:heart_of_the_deep`) → *The Otherside* (subtitle *Hello from...*).
  Quest text: *"We can use the Heart of the Deep on a frame of Reinforced Deepslate to get
  our Portal to the Otherside. There can't be any Blocks blocking the Portal Frame or else
  it won't work."* The frame is already standing in the Ancient City: *"We'll also find the
  Portal Frame made of Reinforced Deepslate."*
- **Chapter / stage:** Deeper and Darker (`deeper_and_darker`, 45 quests) · Exploration ·
  `endgame` tag. Mod: Deeper and Darker 1.4.1.
- **Roughly when:** mid-late — after the Warden (**verified** chain). Chapter 1 itself
  reaches the Warden after Netherite: *Ancient Metals* → *Visit The Deep Dark!* → *Kill The
  Warden* (**verified**).
- **Go there for:** the biome quests *Deeplands*, *Blooming Caverns*, *Echoing Forest*, and
  *Overcast Columns*; *Ancient Temples* (subtitle *The only structure*); *Warden Upgrade
  Template* and *Reinforced Echo Shard*, which both depend on *The Otherside* in the config
  and lead to *Warden Armor*, *Warden Tools*, and *Warden Weapons*; *Soul Elytra* and
  *Sonorous Staff*; the *Shriek Worm* mini-boss.
- **Star relevance:** Chapter 3's *Heart of the Deep* (Wither's Compass) asks for the same
  item that lights this portal — its text: *"This can be used for the ATM Star, or to
  activate the Portal in the Ancient City!"* The Warden drops it in the Overworld, so the
  star needs the Heart, not the trip.

### 9. The Starlight — Eternal Starlight (`eternal_starlight:starlight`)

- **Unlocked by:** *The Gatekeeper and The Gate* (`structure #eternal_starlight:portal_ruins`)
  → *Eternal Starlight* (task title *Visit the Starlight*); the sibling quest *Orb of
  Prophecy* (`eternal_starlight:orb_of_prophecy`) says *"The Orb of Prophecy can be crafted
  or obtained through beating the Gatekeeper!"* Quest text: *"In order to get to the
  Starlight Dimension you'll need to find Portal Ruins in the Overworld."* The Gatekeeper
  is a duel — *"Careful, they are very tough."* — but *"The Gatekeeper will also deem you
  worthy if you have defeated the Ender Dragon, and allow you to skip the duel."* Then:
  *"Right Click the Portal with the Orb to activate it!"*
- **Chapter / stage:** Eternal Starlight (`eternal_starlight`, 193 quests — the biggest
  Exploration chapter) · Exploration · `endgame` tag. Mod: Eternal Starlight 0.9.1.
- **Roughly when:** late — after the Ender Dragon, the cheap way past the Gatekeeper
  (**verified** quest text). Taking the duel earlier is possible, but the quest calls the
  Gatekeeper very tough (*approximate*).
- **Go there for:** *"A Dimension where it is constantly Dusk, and no you can't change
  that."* Two bosses, both found with *Finding the Bosses* (`eternal_starlight:seeking_eye`):
  → *Monstrosity Items* → *Cursed Garden* → *Burn it!* → *Lunar Monstrosity*; and →
  *Golem Items* → *Golem Forge* → *Powering down* → *Starlight Golem*. Materials:
  *Deepsilver*, *Thermal Springstone*, *Starlit Diamond*, *Glacite*, *Aethersent* (after a
  *Meteor Shower*), *Saltpeter Powder*. Basic Armor's *Aethersent Armor*, *Thermal
  Springstone Armor*, and *Glacite Armor* point here.
- **Star relevance:** *Chain of Souls* (`eternal_starlight:chain_of_souls`) is a Chapter 3
  task feeding the Dragon Soul; in this chapter it depends on *Lunar Monstrosity* — *"The
  Chain of Souls can be crafted from drops by Lunar Monstrosity."*

### The Teleport Pad: one item, three dimensions (Chapter 2)

Chapter 2 opens by saying where it sits: *"Obviously now that you are in Chapter 2, you
have beaten Vanilla Minecraft!"* and *"By now you should have Netherite and have killed all
the bosses Minecraft has."* Its verified spine is *Allthemodium*
(`minecraft:netherite_ingot`) → *Ancient City* → *Allthemodium Ingot* → **Teleport Pad**
(`allthemodium:teleport_pad`) → one `dimension` quest per vanilla dimension, each saying
where the pad goes from there:

| Place the pad in… | Quest (its text) | Leads to | Dimension quest |
|---|---|---|---|
| the Overworld | *Overworld* — *"Place the Teleport Pad in the Overworld to go to the Mining Dimension."* | Mining Dimension | *Mining Dimension* (`allthemodium:mining`) |
| the Nether | *The Nether* — *"Place the Teleport Pad in The Nether to go to The Other."* | The Other | *The Other* (`allthemodium:the_other`) |
| the End | *The End* — *"Place the Teleport Pad in The End to go to The Beyond."* | The Beyond | *The Beyond* (`allthemodium:the_beyond`) |

Using it, per the *Teleport Pad* quest: *"Place it down in one of the Minecraft dimensions
to teleport to a different dimension."* and *"To teleport you need to shift right click
with your main and offhand empty!"* The pad's recipe is JEI's. The order between the three
is the quest book's own advice, in *Allthemodium Ingot*: *"I recommend making 2 Teleport
Pads with the Nuggets! You can use those to get to the Mining Dimension to find more
Allthemodium or The Other to find other adventures."* and *"After that I recommend
upgrading your Pickaxe so you can Mine Vibranium."* All three dimensions belong to
Chapter 2: Allthemodium (`allthemodium`, 54 quests) · Main Questline · `endgame`. Mod:
Allthemodium 3.0.1.

### 10. Mining Dimension (`allthemodium:mining`)

- **Unlocked by:** a Teleport Pad placed in the Overworld — Chapter 2's *Teleport Pad* →
  *Overworld* → *Mining Dimension* (task title *Visit The Mining Dimension*).
- **Chapter / stage:** Chapter 2: Allthemodium · Main Questline · `endgame`.
- **Roughly when:** Chapter 2, with one of the two pads the quest text recommends making
  first (**verified**). Going here before The Other is a judgement call (*approximate*):
  more Allthemodium means the Allthemodium-tier pickaxe that Vibranium needs — *"it
  requires Allthemodium Pickaxe (or the same tier) to mine it"*, says *Vibranium Ingot*.
- **Go there for:** *"The Mining Dimension is a Superflat world with absolutely nothing on
  the surface."* — *"Below the surface is almost every single Ore."* — *"The Mining
  Dimension has no Caves, no Mob Spawns, and nothing to get in your way."* One catch, from
  the untitled follow-up quest (task title *Quarried*): quarries there now *"will Mine
  Allthemodium but Void the drops"*, and *"I recommend Mining with Ore Sight Potions if you
  are looking strictly for Allthemodium!"*
- **Star relevance:** none by name; it is a source of the Allthemodium the whole chapter
  runs on (Basic Tools' *Harvest Tier 5*: *"Tier 5 is basically just for Allthemodium Ore,
  not much else."*).

### 11. The Other (`allthemodium:the_other`)

- **Unlocked by:** a Teleport Pad placed in the Nether — Chapter 2's *Teleport Pad* → *The
  Nether* → *The Other* (task title *Visit The Other*). Ice and Fire's hub quest *Ice and
  Fire* is a second `dimension allthemodium:the_other` task: *"Welcome to Ice and Fire! Now
  in The Other"*.
- **Chapter / stage:** Chapter 2: Allthemodium · Main Questline · `endgame`; and Ice and
  Fire (`ice__fire`, 87 quests) · Exploration · `endgame` tag. Mods: Allthemodium 3.0.1;
  Ice And Fire Community Edition 2.0-beta.17.
- **Roughly when:** Chapter 2, with the other of the two pads the quest text recommends
  making first (**verified**). Its quest warns: *"You can't set up Quarries for many blocks
  in The Other though, no cheesing anything here."*
- **Go there for:** *"The Structures are: Piglin Village, Ancient Pyramid, and Dungeon,
  plus some structures from When Dungeons Arise and Ice and Fire."*
  - **Vibranium** — *"You can find it rarely in The Nether or abundantly in The Other."*
  - **The Piglich** — *Ancient Pyramid* (`structure allthemodium:ancient_pyramid`) →
    *Piglich Boss* (task `allthemodium:piglich_heart`).
  - **Unobtainium Smithing Template** — *"You'll have to earn these by beating the Trial
    Spawners which are found in the Dungeon structure in The Other. More specifically the
    Library Rooms!"*
  - **Soul Lava** — Chapter 2's untitled Dissolution Chamber quest: *"You'll also need Soul
    Lava which is found in The Other, common in the Piglin Village."*
  - **Divine Pact** — Forbidden & Arcanus' *Divine Pact*: *"Divine Pact is the most
    difficult to obtain, you'll need to search Piglin Villages and Ancient Pyramids in The
    Other to find them!"*
  - **Ice and Fire** — the whole chapter. Its biome quests use The Other's own biome ids
    (`allthemodium:soul_sand_valley`, `allthemodium:warped_forest`, `allthemodium:desert`,
    `allthemodium:crimson_forest`, and the biome `allthemodium:the_other` — *"The Other is
    the Biome, while The Other is the Dimension."*). Dragons, the Hydra, the Cyclops, the
    Gorgon: `references/boss-checklist.md`.
- **Star relevance:** the most of any dimension. Chapter 3's *Piglich Heart Block*
  (*"Piglich is a Boss added by Allthemodium which lives in the Ancient Pyramid in The
  Other."*) and *Soul Lava Bee Spawn Egg* (*"It can be found in The Other very rarely
  underground, or common in Piglich Villages!"*) both feed the Dragon Soul; and the Divine
  Pact is where Forbidden & Arcanus' *Soul Binding Crystal* starts (*"First, you'll need a
  Divine Pact Relic, which are found in The Other."*) — the same crystal Chapter 4's *Soul
  Binding Crystal* asks for on the way to a *Top ATM Star part*.

### 12. The Beyond (`allthemodium:the_beyond`)

- **Unlocked by:** a Teleport Pad placed in the End — Chapter 2's *Teleport Pad* → *The
  End* → *The Beyond* (task title *Visit The Beyond*).
- **Chapter / stage:** Chapter 2: Allthemodium · Main Questline · `endgame`.
- **Roughly when:** optional — no quest in the book depends on *The Beyond* (**verified**).
- **Go there for:** the quest text, whole: *"Welcome to The Beyond!"* *"There's nothing
  here!"* *"You might want an Angel Block."* Not Unobtainium — Chapter 2's *Unobtainium
  Ingot*: *"No it isn't found in The Beyond."*
- **Star relevance:** none.

### 13. Neo Vitae's realm (`neovitae:dungeon`)

- **Unlocked by:** two rites after *Tier III: The Master's Orb* (tasks
  `neovitae:blood_orb_master` and `neovitae:ritual_diviner_dusk`). *Highway to Hell* (tasks
  `neovitae:standard_key` ×2 and `dimension neovitae:dungeon`): *"The Highway to Hell
  ritual opens a permanent gate into the Endless Realm."* *Breaching the Veil*: *"We perform
  the Breaching the Edge of Demon Realm rite and tear a one-time wound through the veil in
  a single move — on the other side, an Antechamber opens up."* Ritual layouts are the
  quest entries' and the mod's own guide's business, not this page's.
- **Chapter / stage:** Neo Vitae (`neo_vitae`, 49 quests) · Magic · `magic` tag. Mod: Neo
  Vitae 1.1.26.
- **Roughly when:** late in that chapter (**verified**: both quests depend on *Tier III: The
  Master's Orb*, the top of the altar ladder). One wrinkle, *approximate*: *The Tau
  Harvest*, which the config places *before* Tier III, says *"Only the Antechamber, past
  the veil, grows this strange fruit."* — the quest text and the dependency links disagree
  about when you first get in, so follow the quest entries in-game.
- **Go there for:** *Highway to Hell* → *The Mines* (`neovitae:mine_entrance_key`) → *The
  Foreman* → *Demonite* (*"Demonite is the only real source of Hellforged metal, the
  material that carries the altar's final tiers."*); *Breaching the Veil* → *Deeper Locks*
  (`neovitae:mine_key`) → *Doubling Down on Runes* (Intricate Hellforged Parts).
- **Star relevance:** none tied to the dimension.

## The recommended visit order

The book gates nothing, so this is a recommendation. **Verified** steps rest on a
dependency link or a quest's own sentence; *approximate* steps are judgement.

1. **Overworld → the Nether.** Chapter 1's spine: *We've Struck Diamonds!* → *To The
   Nether!* (**verified**).
2. **The Twilight Forest, as soon as you hold a diamond.** *We've Struck Diamonds!* says
   so (**verified**). Take the first bosses now and come back for the rest — the line is
   strictly ordered and its tail is late (*approximate*: how far to push before moving on).
3. **The End.** *To The Nether!* → *Finding The End* → *The End* (**verified**). Alongside
   it, Chapter 1 sends you to the Wither and, after Netherite, the Deep Dark and the Warden;
   the book does not order those three branches against each other.
4. **The cheap side dimensions — the Bumblezone, the Aether, the Undergarden — in any
   order** (*approximate*). The Bumblezone needs a beehive and an ender pearl; the Aether's
   portal quest asks for glowstone; the Undergarden needs its Catalyst (JEI) and keeps its
   Depths for a Forgotten or Allthemodium pickaxe. None of the three feeds the star, so
   they can also wait.
5. **The Otherside, once the Warden is down** (**verified**: *Kill the Warden* → *Heart of
   the Deep* → *The Otherside*).
6. **Eternal Starlight, once the Ender Dragon is down** (**verified** quest text:
   dragon-slayers skip the Gatekeeper's duel). Its Lunar Monstrosity is a star step (the
   Chain of Souls).
7. **Chapter 2's pads: the Mining Dimension and The Other first, The Beyond if ever.**
   *Allthemodium Ingot* → *Teleport Pad* (**verified**), and *Allthemodium Ingot*'s own
   text recommends two pads — Mining Dimension and The Other — then a pickaxe upgrade so
   you can mine Vibranium. The Other is where Chapters 2–4 meet: Vibranium, the Piglich,
   the Unobtainium Smithing Template, Soul Lava, the Divine Pact, and the whole Ice and
   Fire chapter. Unobtainium itself is back in the End's End Highlands (quest text), not
   The Beyond.
8. **Late and optional: Neo Vitae's realm** (after *Tier III: The Master's Orb*,
   **verified**), plus the endgame return trips to the vanilla dimensions — Cataclysm's
   arenas in all three (*"There is no certain pattern of which bosses to kill first"*, says
   its hub quest) and Draconic Evolution's Chaos Islands in the End.

**The short version for "I only want the star":** the Twilight Forest up to the Snow Queen;
the Warden (Overworld) for the Heart of the Deep; Eternal Starlight's Lunar Monstrosity for
the Chain of Souls; The Other for the Piglich and Soul Lava; Cataclysm's arenas. The Aether,
the Bumblezone, the Undergarden, the Otherside itself, the Mining Dimension, The Beyond, and
Neo Vitae's realm are not on that path.

## Where the dimensions meet the ATM Star

Cross-reference with `references/atm-star-checklist.md` (Chapter 3) and
`references/creative-checklist.md` (Chapter 4). Every task below is a verified quest title,
and "feeds" is its dependency link in the config:

| Dimension | Task (chapter) | Feeds |
|---|---|---|
| The Twilight Forest | *Snow Queen Trophy* (Chapter 3) | Oblivion Shard |
| Overworld (the Warden's Ancient City) | *Heart of the Deep* (Chapter 3) | Wither's Compass |
| Eternal Starlight | *Chain of Souls* (Chapter 3) | Dragon Soul |
| The Other | *Piglich Heart Block*, *Soul Lava Bee Spawn Egg* (Chapter 3) | Dragon Soul |
| The Other (Divine Pact, per Forbidden & Arcanus) | *Soul Binding Crystal* (Chapter 4) | *Top ATM Star part* |
| Overworld · Nether · End (Cataclysm's arenas) | *Abyssal Sacrifice*; *Void Forge* and *Meat Shredder* (Chapter 3) | Dragon Soul; Oblivion Shard |

Which Cataclysm boss gives which item is `references/boss-checklist.md`'s and JEI's answer,
not this page's.

## Related pages

- `references/boss-checklist.md` — every boss named here, with its arena and roughly when.
- `references/atm-star-checklist.md` — Chapter 3's components by source mod.
- `references/creative-checklist.md` — Chapter 4, after the star.
- `references/progression.md` — the four stages, and why the Exploration chapters sit in
  `endgame`.
- `references/key-mods.md` — the mods behind each dimension.

## What this page deliberately does not tell you

- **Portal recipes and frame layouts** beyond the quoted quest text — JEI and the quest
  entry. The page names what a portal quest asks for; it never writes a recipe.
- **Coordinates, Y levels, seeds, distances.** None. Where a quest carries a location hint
  (Draconic Evolution's *Where is he?*, Eternal Starlight's *Golem Forge*), read that quest.
- **Fight mechanics and gear checks.** `references/boss-checklist.md` quotes what identifies
  a boss; the rest is the quest entry and the mod's own guide book.
- **Drop tables.** JEI, in-game.
- **Dimensions the book does not track.** Other mods in the pack may add places of their
  own; if no quest in the config goes there, it is not on this page — check the in-game
  quest book and JEI before saying anything about it.
