# Mob farm progression: from a dark-room grinder to late-game spawner setups

**What this page is.** The answer to the beginner question *"how do I farm mob drops?"* in
**All the Mods 10**, laid out as a ladder: kill mobs where they spawn, put the mob you want
on a spawner, then automate — up to setups that need no mobs at all. Every quest title,
item id, and machine name below was read from the pack's own quest config; the build-order
judgements are flagged as such.

## Provenance — everything here was read, not remembered

Every quest title (and the quoted sentences) below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10), `main` branch as of
**2026-09-22** = **pack 8.2** (the `"8.x"` stamp in `examples/progress.example.json`),
commit `e5e3d1d83e`:

| File(s) in the pack repo | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/apotheosis_2.snbt` | the Apothic Spawners chapter: 36 quests, their `item` tasks (spawner blocks, runes, eggs, chains) and dependency links |
| `config/ftbquests/quests/chapters/hostile_neural_networks.snbt` | the simulation line: 50 quests, deep learner → data models → simulation chamber → loot fabricator → data center |
| `config/ftbquests/quests/chapters/elmystical_agriculturerr.snbt` | Mystical Agriculture's soul route (Soul Jars, Soul Extractor, Soulium Spawner, Mob Seeds) |
| `config/ftbquests/quests/chapters/evilcraft.snbt`, `industrial_foregoing.snbt` | the kill-and-collect machines (Spirit Furnace farm; Mob Crusher / Mob Slaughter Factory / Mob Duplicator) |
| `config/ftbquests/quests/chapters/bounty_board.snbt`, `mainquestline_part_1.snbt` | the kill tasks that reward mob killing (87 kill tasks in the Bounty Board alone) |
| `config/ftbquests/quests/chapters/modular_router.snbt`, `refined_storage.snbt`, `tips_and_tricks.snbt` | loot-collection quests that mention mob farms |
| `config/ftbquests/quests/chapters/apothic_enchanting.snbt`, `forbidden__arcanus.snbt`, `natures_aura.snbt` | supporting quests: Infusing Spawner Runes, Occult Ender Lead, Spawner Scraps / Quantum Catcher, Altar of Birthing |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, and the description text quoted below |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (490 mod ids) |

## Grounding rules (read before repeating any of this)

- **The in-game quest book and JEI are authoritative.** This is a snapshot of pack 8.2's
  config. If the player's book differs, his book wins.
- **Numbers in quotes are the quest author's, not the skill's.** Spawn delays, spawn
  counts, drop percentages, and structure sizes below appear only where a quest
  description states them in this pack version. Do not add rates, power costs, or ranges
  that no quest states.
- **The vanilla dark-room grinder is general Minecraft knowledge, not pack content.** The
  pack's 8.2 config contains **no** quest that tracks a dark room, a mob tower, or natural
  spawning mechanics — this was checked (`grep` for "dark room", "mob farm", "grinder"
  across all chapter and lang files). Where this page describes one, it is marked
  *approximate / general knowledge*, and the in-game game mechanics — not a quest — are
  the reference.
- **No soul-shard quests exist in 8.2.** There are no "Soul Shard" items or quests anywhere
  in the config (checked); if a player asks for soul shards, say the book does not track
  them in this pack version and point at the spawner routes the book *does* track below.
- **"Roughly when" is approximate by construction.** The pack's Welcome chapter says:
  *"In this modpack, quests are optional. Mods are not gated behind completing any
  quests!"* — so the ladder below is the skill's judgement layered on the config's
  dependency links, which are verified.
- **Nothing here was invented.** A machine, rune, or egg source that is not in the config
  is not on this page; if a player names one, the answer is "let's check your quest book /
  JEI" — never a plausible-sounding guess.

## The short answer

1. **Kill mobs where they already spawn** (cave, night surface, or a dark room you build —
   general knowledge; no quest asks for the room). The Bounty Board pays for exactly this.
2. **Mine a spawner with Silk Touch** (Apotheosis brings that back) and modify it with
   Spawner Runes — the **Apothic Spawners** chapter walks the whole system.
3. **Get the mob you want onto a spawner** via spawn eggs — five verified routes below.
4. **Go automated**: the pack's "Other Spawners" section lists seven mod spawners, and
   Industrial Foregoing / EvilCraft add kill-and-collect machines.
5. **Skip mobs entirely**: Hostile Neural Networks simulates the kills and fabricates the
   loot.
6. **Collect the drops** with Modular Routers (the pack has a quest for exactly this).

## Why farm mobs at all: what the book actually asks

The config tracks **kills**, not farms — the farm is the player's route to the counts.
Verified kill tasks a farmer feeds:

- **Bounty Board** (`bounty_board`, standalone chapter, 50 quests): **87 kill tasks**.
  Eight core hostile mobs each carry a four-tier ladder — zombie, skeleton, creeper,
  spider, enderman, blaze, witch, wither skeleton, at **5 / 10 / 50 / 100** kills per tier
  (values quoted from the `kill` tasks). Verified titles include
  *Overworld Bounty: Zombies* and *The Nether Bounty: Blazes* (formatting codes
  stripped). The board also tracks variant mobs (Creeper Overhaul's biome creepers,
  Enderman Overhaul's biome endermen, Variants&Ventures' skeleton variants), one tier
  each.
- **Chapter 1: The Beginning** (`mainquestline_part_1`): *Kill The Warden*
  (`kill minecraft:warden`) and *Kill The Wither* (`kill minecraft:wither`) — the only two
  kill tasks in the Main Questline's first chapter. A wither-skeleton or blaze farm feeds
  the Wither summons (see `references/boss-checklist.md`: the *Summoning The Wither* quest
  text asks for *"at least 3 Wither Skeleton Skulls"* (`minecraft:wither_skeleton_skull`)
  and *"at least 4 pieces of Soul Sand"* (`minecraft:soul_sand`); its item tasks track one
  of each).
- **Kill quests across the exploration chapters** (Aether, Twilight Forest trophies,
  Cataclysm, and so on) are boss hunts, not farms — same doc.

## Stage 1 — the dark-room grinder (general knowledge, no quest)

Before any machine exists, a hostile-mob farm is vanilla mechanics: a dark spawning area,
a way to move mobs, and a way to kill them. **The pack's config never mentions this** — no
quest, no item, no chapter. Treat any advice here as the skill's judgement:

- The player's first "farm" is usually just killing night spawns for the Bounty Board's
  5-kill tiers — no build required.
- A dark-room box with fall damage, lava blades, or a player wielding a Looting sword all
  work; *which one* is the player's choice, and the pack does not gate any of it.
- Approximate, verify in game: spawning needs low light for hostile mobs (the Apothic
  Spawners chapter's *Ignore Light* quest text confirms the light rule in passing:
  *"Some mobs (mostly monsters) need certain Light Levels to spawn. Hostile ones needing
  lower levels and passive needing higher ones."*).

## Stage 2 — the Apothic Spawners chapter (the hub)

Chapter `apotheosis_2`, titled **Apothic Spawners** (subtitle *"And Other Spawners"*),
in the **Resources** group, staged early-game by this skill; **36 quests**, chapter icon
`minecraft:spawner`. Apotheosis (mod `apotheosis`, "Apotheosis" 8.8.0 in the modlist) and
Apothic Spawners (`apothic_spawners`, 1.4.0) supply the system. The chapter's root quest:

- ***Apothic Spawners*** — task: `minecraft:spawner`. Quest text: *"Remember being able to
  mine Spawners with Silk Touch? Well it's back thanks to Apotheosis! There's also many new
  Modifications you can add to Spawners by right clicking any of these items."* This is the
  pack's own answer to "how do I get a spawner": **Silk Touch**, then right-click items
  onto it.

The chapter's verified dependency chain hangs everything off one quest:

1. ***Blowing up Spawners*** — tasks: `apotheosis:spawner_chain` ×1, `minecraft:tnt` ×1.
   Quest text: *"When you blow up a Spawner, it will become highly unstable, spawning a
   large amount of its respective mob, and leaving Spawner Chains behind. … How many
   chains, you might be wondering? At the time of writing, 48-57."* (Counts are the quest
   author's, quoted.)
2. ***Basic Modifications*** (subtitle) — task: `apotheosis:spawner_rune`. Quest text:
   *"Spawner Runes are the base material for modifying Spawners."* All basic rune quests
   depend on this one, which depends on *Blowing up Spawners* — **Spawner Chains are the
   crafting material the book points at**.
3. The rune quests — verified titles and task items, split by the chapter's own links:

| Depends on | Quest title (verified) | Task item (verified) |
|---|---|---|
| Basic Modifications | *Ignore Light* | `apotheosis:ignore_light_spawner_rune` |
| Basic Modifications | *Youthful* | `apotheosis:youthful_spawner_rune` |
| Basic Modifications | *Spawn Range* | `apotheosis:spawn_range_spawner_rune` |
| Basic Modifications | *Redstone Active* | `apotheosis:redstone_control_spawner_rune` |
| Basic Modifications | *Health* | `apotheosis:initial_health_spawner_rune` |
| Basic Modifications | *Burning* | `apotheosis:burning_spawner_rune` |
| Basic Modifications | *Quiet down you'll wake up the mobs!* | `apotheosis:silent_spawner_rune` |
| Basic Modifications | *Opposite Day* | `minecraft:quartz` |
| Advanced Modifications | *No AI* | `apotheosis:no_ai_spawner_rune` |
| Advanced Modifications | *Ignore Players* | `apotheosis:ignore_players_spawner_rune` |
| Advanced Modifications | *Ignore All Conditions* | `apotheosis:ignore_conditions_spawner_rune` |
| Advanced Modifications | *Echoing* | `apotheosis:echoing_spawner_rune` |

   - *Ignore Light*'s text names the rune in game: *"Using a Rune of Perpetual Twilight
     makes it so you never have to worry about Light Levels"* — for a mob farm this is the
     classic "spawn anywhere, anytime" rune. It does **not** ignore other requirements
     (quoted: livestock still need Grass).
   - *Opposite Day* is the quartz trick: *"With Quartz in your offhand and the other
     Spawner Modification item in your main it will do the opposite of its role."*
4. ***Advanced Modifications*** (subtitle) — task: `apotheosis:infused_spawner_rune`.
   Quest text: *"For more advanced modifications to Spawners, you'll need to Infuse your
   Spawner Runes. … We'll need at least 70 Eterna, 30% Quanta, and 50% Arcana in an
   Enchanting Table."* The Apothic Enchanting chapter's ***Infusing Spawner Runes*** quest
   (`apothic_enchanting`, id `4EE6824A970EEB35`) teaches the same numbers and offers three
   shelf combinations to reach them (14 Deepshelves; 13 Glowing Hellshelves + 2
   Deepshelves; 12 Crystalline Seashelves + 2 Deepshelves — quoted from that quest's text).

### The four Spawner Upgrade Runes (the late-game speed tier)

Four untitled quests (no title in the config; identified by their task items) form the
speed ladder. Their names and numbers below are quoted from each quest's description:

| Task item (verified) | Name per quest text | Stats per quest text | Gate per quest text |
|---|---|---|---|
| `apotheosis:frontier_spawner_upgrade_rune` | *"The Frontiersman's Spawner Upgrade Rune … the first … cheapest, and … weakest"* | min delay 150 / max 600, spawn count 7, max entities 12, activation range 24 | — |
| `apotheosis:ascent_spawner_upgrade_rune` | *"The Wayfarer's Spawner Upgrade Rune … 2nd tier"* | 100 / 400, count 10, max 18, range 32 | any Spawn Egg works for crafting |
| `apotheosis:summit_spawner_upgrade_rune` | *"The Mountaineer's Spawner Upgrade Rune … 3rd tier"* | 50 / 200, count 13, max 24, range 40 | *"Yes, you'll need to fight a Warden for this."* |
| `apotheosis:pinnacle_spawner_upgrade_rune` | *"The Thundering Spawner Upgrade Rune, the 4th and final tier … highest potential"* | 20 / 20, count 16, max 32, range 48 | *"Endersurge Gems can be obtained in The End."* (quest text) |

The quests text also explains the mechanics being tuned: *"To determine when the Spawner
will spawn it picks a random number between the Maximum and Minimum Spawn Delay. The speed
is expressed in ticks where 20 ticks equals 1 second."*

### Getting the mob you want: the verified spawn-egg routes

A hidden header quest (untitled in the config, task titled **"Spawn Eggs"**) anchors five
egg sources; its text: *"Usually you can't get Spawn Eggs, but that's the same with
Spawners and here we are! … once you do, right click it on a Spawner to change the mobs it
spawns."*

| Route | Quest (verified title/subtitle) | Task items (verified) | What the quest text says (quoted) |
|---|---|---|---|
| Capturing enchant | *Capturing Books* (task title) | a `minecraft:enchanted_book` filter matching stored enchantment `apothic_spawners:capturing` | *"Capturing is an Enchantment for Swords to make Mobs rarely drop their Eggs. … Every level gives you a 0.5% chance at getting an Egg each kill and the highest level you can normally get is VII (7)."* |
| Reliquary charms | *Mob Charm Fragments* (task title) | `reliquary:mob_charm_fragment` (quest reward: `reliquary:mob_charm_belt`) | *"They are from Reliquary and rarely drop from their respective mobs. Some can even be crafted! Take 2 and a normal Egg and you can craft a Spawn Egg."* |
| MGU swab | untitled quest | `mob_grinding_utils:mob_swab`, `mob_grinding_utils:gm_chicken_feed` | *"Simply right click a mob with the Swab then craft Chicken Feed with it … feed a Chicken it. Unfortunately the Chicken won't survive the procedure but hey, Spawn Eggs! … Not all mobs can be swabbed, though."* |
| EvilCraft spirits | *Creating Spawn Eggs* | `evilcraft:spirit_reanimator` | *"Give it a lot of Blood and an Egg, and of course a Box of Eternal Closure with the Spirit you want to create the Spawn Egg from … Some mobs cannot be used to create Spawn Eggs."* |
| Occult Ender Lead | *That's no Spawn Egg!* (subtitle) | `apothic_enchanting:occult_ender_lead` | *"This is technically not a Spawn Egg, but … due to its ability to bind mobs to Spawners."* The Apothic Enchanting chapter's *Occult Ender Lead* quest calls it *"The third and final tier of Ender Lead … unbreakable and can even bind mobs to Spawners"* (75 Eterna / 85% Quanta / 60–85% Arcana quoted there). |

## Stage 3 — "Other Spawners": the cross-mod spawner blocks

The chapter's second hidden header (untitled; text: *"These are spawners provided by mods
besides Apothic Spawners."*) hangs seven mod spawners off the root quest. Verified quest
subtitles and task items — all tasks live **in the Apothic Spawners chapter**, not in the
mods' own chapters:

| Quest subtitle (verified) | Task item(s) (verified) | Mechanic per quest text (quoted, trimmed) |
|---|---|---|
| *EnderIO's Spawner* | `enderio:powered_spawner` | *"you'll need a filled Soul Vial and a Broken Spawner … craft the Powered Spawner with it! Then, place it down, give it a Capacitor, and power it."* Also *"fill Soul Vials directly, without the need of a Clicker."* |
| *Draconic Evolution's Spawner* | `draconicevolution:stabilized_spawner` | *"When you use one of the Cores on a Spawner it will become a Stabilized Spawner. … The better the Core the more mobs spawn and at a faster rate."* |
| *PneumaticCraft's Spawner* | `pneumaticcraft:pressurized_spawner` | needs a vanilla spawner first; *"place a Spawner Extrator [sic] above the Spawner"* to pull a Spawner Core, craft the Pressurized Spawner around the Empty Spawner; *"ignores Light Level, and is Redstone Activated."* |
| *Mob Grinding Utils' Spawner* | `mob_grinding_utils:entity_spawner`, `mob_grinding_utils:xpsolidifier`, `mob_grinding_utils:solid_xp_mould_baby` | *"Mob Grinding Utils is all about Mob Farming so of course it has a Spawner! … It'll need 3 things to work though: a Spawn Egg, XP Jelly Babies, and a Redstone signal."* |
| *Mystical Agriculture's Spawner* | `mysticalagriculture:soulium_spawner` | *"It uses Mob Essence and Energy to spawn the mobs. Mob Essence is gotten through harvesting Mob Plants, made by Soul Jars. So you'll have to kill the mobs first, or use the Soul Extractor."* |
| *Industrial Foregoing's Spawner* | `industrialforegoing:mob_duplicator` | *"It uses Essence along with a mob in a Mob Imprisonment Tool to spawn a copy of that mob. Bosses … are blacklisted."* |
| *Ars Nouveau's Spawner* | `ars_additions:source_spawner` | *"This spawner will, as its name implies, make use of Source as fuel. To decide on a mob to spawn, you'll need a Containment Jar holding the mob in the area."* |

Plus one support quest at the same level: *"Don't you despawn on me, Mobs"* (subtitle) —
`pneumaticcraft:spawner_agitator`; its text explains that with Apothic Spawners in the pack
the Agitator *"will keep spawned mobs from despawning incase you leave the chunks."*

Mod display names and versions above are from `config/crash_assistant/modlist.json`:
Ender IO (`enderio`) 8.2.12-beta, Draconic Evolution (`draconicevolution`) 3.1.4.633,
PneumaticCraft: Repressurized (`pneumaticcraft`) 8.2.23, Mob Grinding Utils
(`mob_grinding_utils`) 1.1.10+mc1.21.1, Mystical Agriculture (`mysticalagriculture`)
8.0.28, Industrial Foregoing (`industrialforegoing`) 1.21-3.6.39, Ars Additions
(`ars_additions`) 1.21.1-21.3.0.

## Kill-and-collect machines (no spawner required)

Two chapters track machines that kill mobs and convert them directly:

**Industrial Foregoing** (chapter `industrial_foregoing`, Tech group). Three untitled
quests; the machine names are quoted from their description text:

- *Mob Crusher* (name per quest text) — task `industrialforegoing:mob_crusher`:
  *"deletes mobs in its working area, collecting that mob's loot, as well as converting
  the Experience that mob would get into Essence. You can also optionally use the would be
  Experience to apply Looting to the Mob Crusher instead."* Bosses are blacklisted.
- *Mob Slaughter Factory* (name per quest text) — task
  `industrialforegoing:mob_slaughter_factory`: *"converts that mob into Pink Slime and
  Liquid Meat. Passive Mobs -> More Pink Slime. Hostile Mobs -> More Meat."*
- The Mob Duplicator above is the matching spawner for this line.

**EvilCraft** (chapter `evilcraft`, Magic group). The pack gives blood magic its own farm:

- ***Mob Farms using Blood*** — tasks: `evilcraft:spirit_furnace` ×1,
  `evilcraft:dark_blood_brick` ×**33** (count verified). Quest text: *"EvilCraft has its
  own Mob Farm! To start this, you'll need to craft at least 33 Dark Blood Bricks. With
  these, we'll build a structure that is strong enough to contain the summoned spirits.
  You'll also need a spirit trapped in a Box of Eternal Closure. This will determine the
  drops you'll get. … The minimum size is 3x4x3."* (Sizes are the quest author's.)
- Support line, verified titles: *Revenge of the Spirits* (Vengeance Spirits spawn on mob
  deaths; the Vengeance Ring attracts more), *Capturing Spirits*
  (`evilcraft:vengeance_focus` + `evilcraft:box_of_eternal_closure`), *Garmonbozia* (the
  Blood Infuser turns slain Vengeance Spirits into the high-end material).

## No kills at all: the Hostile Neural Networks chapter

Chapter `hostile_neural_networks` ("Hostile Neural Networks" — HNN 6.5.1 in the modlist),
**Resources** group, 50 quests, staged tech by this skill. Its own intro quest says what
it is: *"a mod based around simulating mob kills for loot! … you will be collecting 'data'
on mobs, then running simulations from the data to create their drops!"* For "how do I
farm mob drops" this is the endgame answer: farm **data**, fabricate **drops**.

Verified quest chain (titles in config order):

1. *Welcome to Hostile Neural Networks!* — task `minecraft:redstone`.
2. *Learning Mobs* — task `hostilenetworks:deep_learner`. *"Each Learner can hold 4 Data
   Models … it will collect data for the models placed inside!"*
3. *Modeling Mobs* — task `hostilenetworks:blank_data_model`. Right-click a mob to turn
   the framework into that mob's Data Model, *"then start killing that specific mob with
   the Deep Learner in your inventory."*
4. *Simulating Deaths* — tasks `hostilenetworks:sim_chamber` +
   `hostilenetworks:prediction_matrix`. Two simulation modes: *"Training: The Data Model
   gains data, without producing any Generalized Predictions or Mob Predictions"* (and the
   producing mode).
5. *Leveling Up Data Models* — task `hostilenetworks:data_model`. *"Data Models start out
   at the first tier: Faulty. You'll need to at least level it to Basic if you'd like to
   run some simulations on it!"* The HUD shows the kill counts needed.
6. *Creating Loot* — task `hostilenetworks:loot_fabricator`: *"When given power and a
   successful Mob Prediction, you will be able to choose which item you'd like to get from
   that mob's Data Model. The machine will remember your choice, so it can be automated."*
   The quest's own examples: *"Ender Dragons for Dragon Eggs, Zombies for Iron, Withers
   for Nether Stars"* — quest text, not a verified drop table.
7. *The Data Center* — tasks `hostilenetworks:data_center`,
   `hostilenetworks:data_center_io_port`, `ftbfiltersystem:smart_filter` ×2: *"a 7x7x7
   multiblock combining the functionalities of the Simulation Chamber and the Loot
   Fabricator … capable of handling 25 Self Aware Data Models concurrently … produces
   loot directly."* (Size and counts quoted from the quest text.)

Dimension prediction quests are **untitled** (no title in the config); their subtitles
are the verified labels — *Makes various Overworld Materials*
(`hostilenetworks:overworld_prediction`), *Makes various Nether Materials*
(`hostilenetworks:nether_prediction`), *Makes various End Materials*
(`hostilenetworks:end_prediction`), *Makes various Twilight Forest Materials*
(`hostilenetworks:twilight_prediction`), and *Makes various Starlight Materials*
(`kubejs:starlight_prediction`). Thirty-seven more
untitled quests (37 in total) task `hostilenetworks:prediction` each — the chapter is
much bigger than its seven titled quests suggest.

## The Mystical Agriculture soul route

Mystical Agriculture (chapter `elmystical_agriculturerr`, Resources) ties mob farming to
its seed line:

- ***Creating Mob Seeds*** — *"you'll need to head to the Nether to pick up some Soulium.
  With the stone and ore that you find, you'll need to use these to make the Soulium Dagger
  and Soul Jars. Using the dagger to kill mobs, you'll be able to gather their souls, which
  are used in the Infusion Altar to create the respective mob seeds. Alternatively, you can
  fill Soul Jars inside of the Soul Extractor by inserting a jar and using mob items …
  adding Rotten Flesh will give a portion of a Zombie Soul."*
- An untitled quest tasks `mysticalagriculture:soul_extractor` with the same Soul
  Extractor text; another untitled quest tasks `mysticalagriculture:soulium_spawner` (the
  spawner in the table above) — *"if you put in some Ghast Essence you can spawn a Ghast."*
- *Cognizant Dust* — *"dropped from the Wither and the Ender Dragon when killed by an
  Essence Weapon enchanted with Mystical Enlightenment"* (quest text): a boss farm, not a
  grinder farm, but it is the pack's stated source.
- One more tie-in, quoted: *"Awakened Supremium and other tiered essences can be farmed
  using the Productive Bees mod."* — the bee route is an alternative farm for the same
  materials (see `references/key-mods.md`).

## Passive mobs and the odd ones out

- **Nature's Aura** (chapter `natures_aura`, Magic): ***Altar of Birthing*** (subtitle
  *"Makin' Babies with Magic"*) — task `naturesaura:animal_spawner`: *"You can make a
  large number of vanilla mobs with the Altar of Birthing. Spirits of Birthing are made by
  breeding animals in areas with large amounts of aura."* That is the pack's tracked route
  for farming **passive** mobs — including the eggs the spawner system wants (per the
  quest text quoted above, *"right click it on a Spawner to change the mobs it spawns"*).
- **Forbidden & Arcanus** (chapter `forbidden__arcanus`, Magic): an untitled quest's text
  explains where *Spawner Scraps* come from — *"The Spawner Scraps are drops from Mining a
  Spawner without Silk Touch, so it'll break the Spawner"* — and the same quest introduces
  the *Quantum Catcher*, *"a very useful Tool for moving Mobs"* (catch and release, priced
  in Aureal by mob health). Useful plumbing around any mob farm; the tier-2 Arcane Forge
  upgrade in the same chapter consumes Spawner Scrap.

## Collecting the loot

- **Modular Routers** (chapter `modular_router`, Logistics): ***Routers for Mob Farms*** —
  tasks `modularrouters:vacuum_module`, `modularrouters:void_module`, and an
  `ftbfiltersystem:smart_filter` matching the sender modules (`modularrouters:sender_module_1`
  through `_3`, per the task's filter component). Quest text walks a wither-skeleton farm:
  *"get Items into the Buffer with a Vacuum Module. Next, get rid of the Stone Swords with
  a Void Module … use a Whitelist Filter with the Stone Sword in it and not matching
  Damage. After, that you'll need a place to put the Loot, I recommend a Drawer System.
  Then, use a Sender Module to send the Loot to the Storage System."*
- **Refined Storage** (chapter `refined_storage`, Storage): the *Grid Networks* quest
  (subtitle *"Wirelessly Connecting Networks"*) suggests the remote use case: *"The
  Receiver should go wherever you want your external network to be. For example, this can
  be a separate part of your base where you have Bees, a mob farm, etc."*
- **Tips and Tricks** (standalone): *Simple Magnets* — *"You can also place Demagnetization
  Coils at your Mob Farms and other factories that involve dropped items to prevent
  this"* (the magnet picking up drops mid-build).

## The ladder at a glance (judgement, not config)

| Approximate point in the pack | Farm setup | Book anchor (verified) |
|---|---|---|
| first nights | kill night spawns; Bounty Board tiers ×5/10 | Bounty Board kill tasks |
| iron gear, first spawner found | Silk Touch it; blow up copies for chains; basic runes | *Apothic Spawners* → *Blowing up Spawners* → *Basic Modifications* |
| enchanting up | spawn eggs (Capturing sword, charms, swab); *Ignore Light* on the farm spawner | the "Spawn Eggs" section; *Ignore Light* |
| tech stage | automated kills: Mob Crusher; agitator anti-despawn; loot routing | IF untitled quests; *Don't you despawn on me, Mobs*; *Routers for Mob Farms* |
| tech/magic split | HNN data farm; EvilCraft blood farm; Soul Extractor line | *Simulating Deaths*; *Mob Farms using Blood*; *Creating Mob Seeds* |
| late game | infused runes + upgrade runes (Warden-gated tier 3); EnderIO/PnC/Draconic spawners; Data Center | *Advanced Modifications*; the four upgrade runes; *The Data Center* |

This ordering is the skill's reading of the config's dependency links plus the chapter
stages in `examples/progress.example.json` — the pack itself never gates anything (the
Welcome chapter: quests are optional, mods are not gated).

## What the config does not contain (checked, pack 8.2)

- **No dark-room, tower, or natural-spawning quest** anywhere in the 66 chapters.
- **No Soul Shard item or quest** — "soul shards" are not part of this pack's tracked
  spawner progression; the tracked route is Apothic Spawners + the mod spawners above.
- **No mob drop rates, spawn-cap numbers, or farm dimensions** beyond the spawn-delay,
  spawn-count, and structure figures quoted from quest text.
- **No fan, conveyor, or cursed-earth items from Mob Grinding Utils** — the chapter's MGU
  tasks are only `entity_spawner`, `xpsolidifier`, `solid_xp_mould_baby`, `mob_swab`,
  `gm_chicken_feed`. If a player has other MGU items in hand, that is the mod, not the
  book.

## What this page deliberately does not tell you

- **Recipes.** None are quoted; the crafting steps for runes, upgrade runes, and every
  machine are JEI's answer, and the Apothic Enchanting chapter owns the infusion setup.
- **Rates and power.** No FE/tick, no mobs-per-hour, no range-addon numbers — no quest
  states them, so none appear here.
- **Drop tables.** What a zombie *drops* is JEI/in-game; HNN's "Zombies for Iron" line is
  quoted as quest flavor, not verified mechanics.
- **Build tutorials.** How high a fall kills a zombie at full HP is general Minecraft
  knowledge and version-sensitive — verify in game.

## Where to go next

- Stage order and chapter placement: `references/progression.md`.
- What each farming mod is for and when to start it: `references/key-mods.md`.
- The boss kills a farm feeds (Wither skulls, Warden, bounty bosses):
  `references/boss-checklist.md`.
- Where mob-derived items feed the endgame (Hostile Neural Networks' Dragon Egg Data
  Model, soul/soulium lines): `references/atm-star-checklist.md`.
