# The storage ladder: chests → backpacks → Refined Storage → AE2 (verified titles)

**What this page is.** The storage progression map for **All the Mods 10**: the four
chapters the quest book files under its **Storage** group, the tier ladders inside them,
what each rung unlocks, and the signals the pack itself gives for moving up a rung. It
answers *"my chests are full — what now, and what comes after that?"* and nothing more. It
is a *map of the chapters*, not a crafting guide and not a verdict on which mod is better.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, count, dependency link, `optional` flag, reward,
and quoted sentence below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the `"8.x"` that
`examples/progress.example.json` is stamped with. Same snapshot, same rules as
`references/atm-star-checklist.md`, `references/boss-checklist.md`, and
`references/creative-checklist.md`:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapter_groups.snbt` | the **Storage** group (`1AC60211DE7427FC`), third of the book's ten groups |
| `config/ftbquests/quests/chapters/storage.snbt` | **Basic Storage**: 90 quests, their task items and counts, dependency links, `optional` flags, reward tables, and the chapter's canvas `images` |
| `config/ftbquests/quests/chapters/applied_energistics_2.snbt` | **Applied Energistics 2**: 74 quests, same fields |
| `config/ftbquests/quests/chapters/extended__advanced_ae.snbt` | **Extended \& Advanced AE**: 56 quests, same fields |
| `config/ftbquests/quests/chapters/refined_storage.snbt` | **Refined Storage**: 72 quests, same fields |
| `config/ftbquests/quests/lang/en_us/chapters/<those four>.snbt` | the English quest titles, subtitles, and the description text quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt`, `chapter_group.snbt` | the four chapter titles and the group title `Storage` |
| `config/ftbquests/quests/chapters/chapter_2_the_star.snbt` | the cross-check in *Which one: Refined Storage or AE2?* — Chapter 3's storage tasks are all AE2-family |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (493 entries) |

Titles are quoted with Minecraft `&` colour codes stripped (`"&6Copper Chest"` → **Copper
Chest**, `"&dNetherite Upgrade"` → **Netherite Upgrade**), exactly as
`scripts/build_chapter_list.py` strips them for `examples/progress.example.json`. The
escaped ampersand in *Extended \& Advanced AE* is kept the way the config writes it: that
is the pack's own way of spelling a literal `&` that Minecraft must not read as a
formatting code.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the task's required amount, a reward's `count`,
  a number in a quest's own description). Where the config asks for one item, no count is
  printed.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Every
  "how" on this page is a quote from that quest's own description, marked as such, or a
  pointer to JEI. Do not fill a recipe in from memory or plausibility.
- **Every number in quotation marks is quest text, not a measured fact.** Slot counts,
  channel counts, energy buffers, ranges, and speed multipliers are the quest author's own
  words at pack 8.2; repeat them as *"the quest says X — verify in-game"*.
- **`…` inside a quote marks an elision or a paragraph break in the config's own text**
  (the lang files store multi-paragraph descriptions as separate entries). Nothing is
  silently joined, reworded, or punctuated: outside those marks a quote is the source
  string, with the pack's `\n` paragraph markers dropped.
- **"When to move up" is either quoted or it is this skill's reading.** In the *when to
  upgrade* table a signal in quotation marks is the pack's own text; a signal written
  without quotes is this skill's reading of the book's structure and is approximate. The
  rung labels themselves are always this skill's reading — the config states dependencies,
  never a ladder.
- **Titles are the config's.** 165 of the 292 quests in these four chapters carry an
  explicit title; the other 127 do not, and the book then shows the task item's own name.
  Untitled quests are written *(no title in the config)* below with their task item next
  to them — never present a derived name as a verified title.
- **The book lays chapters out on a canvas, not as a numbered list.** All four chapters
  carry `progression_mode: "flexible"` in the config, and the ladders below are written in
  **dependency order** (a rung appears after everything the config links it to), which is
  the only order the config actually states. Anything beyond that is *(skill's reading)*.
- **Nothing here was invented, and nothing is added from memory.** A storage mod, tier, or
  upgrade that is not on this page is not one these four chapters ask about: the answer is
  "open that quest in the book / look it up in JEI", never a plausible-sounding guess.

## The ladder at a glance

The **Storage** group holds exactly four chapters — 292 quests between them, 351 tasks
(338 `item`, 11 `checkmark`, one `advancement`, one `observation`). The skill tracks them
as four entries in `examples/progress.example.json`, group `Storage`. They are listed here
in the order a player typically meets them, chests first:

| Rung | Chapter title (config id) | `order_index` | Quests | Titled / untitled | Optional | What it is |
|---|---|---|---|---|---|---|
| 1 | **Basic Storage** (`storage`) | 0 | **90** | 40 / 50 | 44 | Every no-power way to hold items: vanilla chests, Sophisticated Storage chests and barrels, Sophisticated Backpacks, Functional Storage drawers, trash cans |
| 2a | **Refined Storage** (`refined_storage`) | 2 | **72** | 52 / 20 | 5 | The first digital network, option A: controller, disks, grids, autocrafters, cable tiers |
| 2b | **Applied Energistics 2** (`applied_energistics_2`) | 1 | **74** | 42 / 32 | 4 | The first digital network, option B: ME channels, storage cells, autocrafting, wireless terminals, spatial storage |
| 3 | **Extended \& Advanced AE** (`extended__advanced_ae`) | 2 | **56** | 31 / 25 | 3 | AE2's two addons in one chapter: ExtendedAE devices and Advanced AE's quantum endgame |

Two notes on that table, both from the config:

- **Rung numbers are this skill's reading, not the book's.** The book's own ordering is
  `order_index`: Basic Storage 0, Applied Energistics 2 1, and *both* Refined Storage and
  Extended \& Advanced AE 2. The shipped chapter list breaks that tie by config filename
  (`extended__advanced_ae` sorts before `refined_storage`), so `progress.py` lists them in
  that order and puts Applied Energistics 2 second — treat the pair's relative order, and
  this page's rung labels, as approximate.
- **Rungs 2a and 2b are alternatives, not steps.** Refined Storage and AE2 are two parallel
  digital-storage lines with their own addon families; the pack ships a full chapter for
  each and gates nothing behind either. See *Which one* below. Rung 3 is an addon chapter
  for the AE2 side only — Refined Storage's addons live inside its own chapter.

The config's own ids, for anyone diffing this page against the pack: chapter
`1DB294A8F8686321` (Basic Storage), `15AAF17B6665223D` (Refined Storage),
`07210DDF872160BA` (Applied Energistics 2), `51A2FE60D8B76FC6` (Extended \& Advanced AE),
all in group `1AC60211DE7427FC` (**Storage**). The stages in `references/progression.md`
map onto this ladder the way the shipped chapter list already records them: `storage` is
stage `early-game`, the other three are stage `tech`. The player's own pace is the only
clock.

## Rung 1 — Basic Storage (`storage`, 90 quests)

The chapter's own hub quest, **Basic Storage** (icon `integratedterminals:terminal_storage_portable`),
says what the rung is for: *"Welcome to the Basic Storage Chapter! You'll find all of the
basic ways to store items without needing power, as well as useful items for your storage
needs!"* Its task is a smart filter on the tag `c:chests` — the book opens the chapter by
asking for a chest. Nine quests in this chapter have no dependencies at all: **Basic
Storage**, **Vanilla Storage**, **Sophisticated Storage**, **Sophisticated Backpacks**,
**Functional Storage**, **Trash Cans**, **Dimensional Storage**, the untitled NBT warning
below, and the hidden authorship quest.

The chapter's `images` list carries its own canvas art —
`atm:textures/questpics/storage/functional1.png` and `functional2.png`,
`sophisticated1.png` … `sophisticated3.png`, two `helper_arrow.png` images, a
chest-minecart texture, an IntegratedDynamics aspect icon, and
`sophisticatedstorage:item/packing_tape`. That art is decoration, not quests: nothing on
this page is inferred from it, and no quest in the chapter asks for the packing tape.

### 1a. The vanilla line (6 quests)

| Verified quest title | Task item(s) in the config | What the quest text says |
|---|---|---|
| **Vanilla Storage** — subtitle *The Chest* | smart filter: `or(item(minecraft:chest)item(ars_nouveau:archwood_chest))` | *"Chests have 27 slots and can be made into a double chest to store twice that amount."* |
| *(no title in the config)* — subtitle *"I wonder what's in here?"* | `minecraft:trapped_chest` | *"Trapped Chests are the same as regular Chests only the emit a Redstone signal when opened and they can't be combined together into 1."* |
| *(no title in the config)* | `minecraft:barrel` | *"Barrels work the same as Chests only they can't be combined together into 1. They look cool though."* |
| *(no title in the config)* | `minecraft:ender_chest` | *"Ender Chests all share the same inventory and that inventory is different for every player."* |
| *(no title in the config)* | `minecraft:chest_minecart` | *"useful for transporting items across Rail systems"* |
| *(no title in the config)* | smart filter on the tag `minecraft:chest_boats` | *"You can open the chest while you're in the Boat or you can right-click on it."* |

All five children depend on **Vanilla Storage** and nothing else. Note the first quest's
filter: an Ars Nouveau archwood chest satisfies it, so the book already treats "a chest"
as a family rather than one item.

### 1b. Sophisticated Storage — the chest and barrel ladder (6 tier quests + 4 infrastructure)

Sophisticated Storage is 1.5.91 in the modlist. The tier chain is the config's, verified
link by link. Every tier task is a smart filter
that accepts the chest **or** the matching barrel, and every tier quest's reward table
pays the tier-upgrade item plus XP levels — quoted from the config, not a promise about a
future pack version:

| # | Verified quest title | Task filter (config) | Depends on | Reward item (config) |
|---|---|---|---|---|
| 1 | **Sophisticated Storage** — subtitle *"Vanilla Chest"* | tag `sophisticatedstorage:base_tier_wooden_storage` | — | random reward table + 10 XP levels |
| 2 | **Copper Chest** *(marked `optional`)* | `or(item(sophisticatedstorage:copper_chest)item(sophisticatedstorage:copper_barrel))` | Sophisticated Storage | `sophisticatedstorage:basic_to_copper_tier_upgrade` ×1 + 25 XP |
| 3 | **Iron Chest** — subtitle *Iron Chests?*, `dependency_requirement: "one_completed"` | `or(item(sophisticatedstorage:iron_chest)item(sophisticatedstorage:iron_barrel))` | Sophisticated Storage **or** Copper Chest | `sophisticatedstorage:basic_to_iron_tier_upgrade` ×1 + 50 XP |
| 4 | **Gold Chest** | `or(item(sophisticatedstorage:gold_chest)item(sophisticatedstorage:gold_barrel))` | Iron Chest | `sophisticatedstorage:iron_to_gold_tier_upgrade` ×1 + 50 XP |
| 5 | **Diamond Chest** | `or(item(sophisticatedstorage:diamond_chest)item(sophisticatedstorage:diamond_barrel))` | Gold Chest | `sophisticatedstorage:gold_to_diamond_tier_upgrade` ×1 + 100 XP |
| 6 | **Netherite Chest** — subtitle *So much room for activities!* | `or(item(sophisticatedstorage:netherite_chest)item(sophisticatedstorage:netherite_barrel))` | Diamond Chest | `sophisticatedstorage:diamond_to_netherite_tier_upgrade` ×1 + 100 XP |

The copper rung is a shortcut, in the quest's own words: *"The Copper Chest can be made
but is not needed to make an Iron Chest, it can be used if you want to save some Iron
though."* That is why **Iron Chest** carries `dependency_requirement: "one_completed"` —
either parent satisfies it (that reading is FTB Quests' own; the book shows it).

**What the chapter says the mod is for** (opening quest, quoted): *"Sophisticated Storage
allows you to upgrade your Chests and Barrels with metals to increase their storage! You
can also add upgrades to increase their functionality. These chests are just like a vanilla
Chest or Barrel, but they have a slot for a Storage Upgrade!"*

The four infrastructure quests, all untitled in the config and all rooted at the
**Sophisticated Storage** quest:

| Task item (config) | Depends on | What the quest text says |
|---|---|---|
| `sophisticatedstorage:upgrade_base` — subtitle *The Base for Upgrades* | Sophisticated Storage | *"To save you from having this entire quest section covered with upgrades, take a look at the Sophisticated Backpack upgrades"* … *"You'll need to make the Sophisticated Storage equivalent, but they function about the same."* |
| `sophisticatedstorage:controller` | Sophisticated Storage | *"The Storage Controller allows you to work with multiple storages as if they were one big storage multiblock … which can be combined with mods like Applied Energistics or Integrated Dynamics, as the Storage Controller acts as an in/out point for all storages attached to it."* Range, quoted: *"this works up to 14 blocks away from controller in all directions"* |
| `sophisticatedstorage:storage_tool` | the controller quest | *"just right click the Storage Controller to bind it and right click the storages to link them. The range for wireless linking is the same as regular, 14 blocks of space."* |
| `sophisticatedstorage:storage_link` | the controller **and** storage-tool quests | *"its a way to wirelessly connect a 'multiblock' of storages without needing to right-click each one of them. 14 blocks of range still applies."* |

That controller quest is the chapter's own bridge to rungs 2a and 2b: the pack explicitly
says a Sophisticated Storage controller can be the in/out point for an Applied
Energistics network.

### 1c. Sophisticated Backpacks — the portable ladder (6 tiers, a base, 41 upgrades)

**Sophisticated Backpacks** (3.26.3 in the modlist; subtitle *Inventories are too Small*,
task `sophisticatedbackpacks:backpack`) is the entry point; its text says *"Sophisticated
Backpacks offers upgradable Backpacks that can use filters to add nifty features!
Backpacks can be put in your Curios Back slot and they can be dyed."*

| # | Verified quest title | Task item | Depends on | Notes from the config |
|---|---|---|---|---|
| 1 | **Sophisticated Backpacks** | `sophisticatedbackpacks:backpack` | — | random reward table + 10 XP levels |
| 2 | **Copper Backpack** — subtitle *The First Upgrade* | `sophisticatedbackpacks:copper_backpack` | Sophisticated Backpacks | `optional`; rewards `minecraft:copper_ingot` ×1 + 25 XP |
| 3 | **Iron Backpack** | `sophisticatedbackpacks:iron_backpack` | Sophisticated Backpacks **or** Copper Backpack | `dependency_requirement: "one_completed"` |
| 4 | **Gold Backpack** | `sophisticatedbackpacks:gold_backpack` | Iron Backpack | |
| 5 | **Diamond Backpack** | `sophisticatedbackpacks:diamond_backpack` | Gold Backpack | |
| 6 | **Netherite Backpack** | `sophisticatedbackpacks:netherite_backpack` | Diamond Backpack | |

Behind the tiers sits one untitled quest for `sophisticatedbackpacks:upgrade_base`
(subtitle *The Base for Upgrades*, *"You will need these to make Backpack Upgrades."*)
with **23 quests hanging directly off it** and **41 upgrade quests in total** across the
family (6 tiers + this base + 41 upgrades = the chapter's 48 Sophisticated Backpacks
quests). Every one of those 41 is marked `optional` in the config — the `upgrade_base`
quest itself is not. Of the chapter's 44 optional quests, 42 are Sophisticated Backpacks
quests (the other two are **Copper Chest** and the hidden authorship quest): the pack
treats the whole upgrade tree as pick-what-you-want.

The upgrade families, grouped by this page for readability. Task items are all
`sophisticatedbackpacks:*`; the right-hand column gives the verified quest title where the
config has one, and *(no title in the config)* where it does not:

| Family | Task items in the config | Verified quest titles |
|---|---|---|
| Item handling | `pickup_upgrade`, `deposit_upgrade`, `refill_upgrade`, `restock_upgrade`, `filter_upgrade`, `magnet_upgrade`, `void_upgrade`, `feeding_upgrade`, `compacting_upgrade`, `tool_swapper_upgrade` | *(no title in the config)* — each carries the upgrade's own item name, and subtitles such as *Allows the backpack to pick up items.*, *All Stocked up*, and *Adds a filter for items you want to auto-delete in the backpack.* |
| Item handling, advanced | `advanced_pickup_upgrade`, `advanced_deposit_upgrade`, `advanced_refill_upgrade`, `advanced_restock_upgrade`, `advanced_filter_upgrade`, `advanced_magnet_upgrade`, `advanced_void_upgrade`, `advanced_feeding_upgrade`, `advanced_compacting_upgrade`, `advanced_tool_swapper_upgrade` | **Advanced Pickup Upgrade**, **Advanced Deposit Upgrade**, **Advanced Refill Upgrade**, **Advanced Restock Upgrade**, **Advanced Filter Upgrade**, **Advanced Magnet Upgrade**, **Advanced Void Upgrade**, **Advanced Feeding Upgrade**, **Advanced Compacting Upgrade**, **Advanced Tool Swapper Upgrade** |
| Processing GUIs | `smelting_upgrade`, `smoking_upgrade`, `blasting_upgrade`, `crafting_upgrade`, `stonecutter_upgrade`, `jukebox_upgrade` | *(no title in the config)*; the jukebox quest's subtitle is *Now we're jammin* |
| Processing, automatic | `auto_smelting_upgrade`, `auto_smoking_upgrade`, `auto_blasting_upgrade` | **Auto-Smelting Upgrade**, **Auto-Smoking Upgrade**, **Auto-Blasting Upgrade** |
| Fluids and power | `tank_upgrade`, `pump_upgrade`, `battery_upgrade` | *(no title in the config)* |
| Fluids and power, advanced | `advanced_pump_upgrade` → `xp_pump_upgrade` | **Advanced Pump Upgrade**, then **Experience Pump Upgrade** (subtitle *Storing XP*) |
| Capacity | `stack_upgrade_tier_1`, `stack_upgrade_tier_2`, `stack_upgrade_tier_3`, `stack_upgrade_tier_4` | **Stack Upgrade Tier 1**, **Stack Upgrade Tier 2**, **Stack Upgrade Tier 3**, **Stack Upgrade Tier 4** — the quest texts state the numbers: *"Increases stack size in the Backpack by 2"*, then *by 4*, *by 8*, *by 16* |
| Utility | `inception_upgrade`, `everlasting_upgrade` | *(no title in the config)*; the inception quest's subtitle is *Backpacks in your Backpacks?* and the everlasting quest's text is *"This upgrade makes it so the Backpack can't die."* |
| Chipped workbenches | one smart filter accepting any of `sophisticatedbackpacks:chipped/botanist_workbench_upgrade`, `…/glassblower_upgrade`, `…/carpenters_table_upgrade`, `…/loom_table_upgrade`, `…/mason_table_upgrade`, `…/alchemy_bench_upgrade`, `…/tinkering_table_upgrade` | *(no title in the config)* — *"Adds crafting GUIs for Chipped Workbenches to your Backpack."* |

All eleven `advanced_*` quests share the subtitle *More Filtering Options*, and the three
automatic-processing ones share *Automatic* — the config's own labels, not this page's. The
grouping into families above is this page's; the config only gives positions on a canvas
and dependency links.

### 1d. Functional Storage — the drawer line (21 quests)

**Functional Storage** (1.21.1-1.5.8 in the modlist; subtitle *Storage Drawers Distant
Relative*, task `minecraft:chest`, no dependencies) opens the family: *"Functional Storage
is a storage mod that adds various useful items to help with storage and ways of storing
stacks of the same items. This can be useful for items like Cobblestone, Dirt and more."*
The drawer quest
behind it (subtitle *Stacks on Stacks*, smart filter on the tag `functionalstorage:drawer`)
adds: *"Drawers can be 1x1, 2x1 or 2x2. Drawers can hold a ton of stacks of 1/2/4 items
depending on the type of Drawer."*

| Verified quest title | Task item (config) | What the quest text says |
|---|---|---|
| *(no title in the config)* | `functionalstorage:linking_tool` | *"Used to link Drawers to a Controller and to link up Ender Drawers."* |
| *(no title in the config)* | `functionalstorage:configuration_tool` | *"used to lock Drawers for them to remember the item it has inside"* |
| *(no title in the config)* — subtitle *The Brain of the Drawers* | `functionalstorage:storage_controller`, plus a smart filter accepting `functionalstorage:framed_storage_controller` too | *"the Controller acts as a 'Hub' … Max range is 40 blocks for all sides, or a cube of 80x80x80."* |
| *(no title in the config)* | `functionalstorage:controller_extension` | *"The Storage Access Point acts as a Storage Controller when linked to it"* |
| *(no title in the config)* — subtitle *Auto Compacts/Decompacts* | `functionalstorage:compacting_drawer` | *"can convert items placed inside to their nugget or block forms"* |
| *(no title in the config)* — subtitle *Auto Compacts/Decompacts* | `functionalstorage:simple_compacting_drawer` | *"will auto convert the item placed inside it into it's compacted form"* |
| *(no title in the config)* — subtitle *Dimensional Drawer...* | `functionalstorage:ender_drawer` | *"you can link 2 Ender Drawers to sync up their contents … just like an Ender Chest, but as a Drawer"* |
| *(no title in the config)* | smart filter accepting the seven `functionalstorage:framed_*` items | *"these can mimic a block's texture on the outside, and a different one in the front"* |
| *(no title in the config)* | smart filter accepting `functionalstorage:fluid_1`, `fluid_2`, `fluid_4` | *"there are also Fluid Drawers!"* |
| **Copper Upgrade** | `functionalstorage:copper_upgrade` | subtitle *x8 Storage Upgrade* |
| **Gold Upgrade** | `functionalstorage:gold_upgrade` | subtitle *x16 Storage Upgrade* |
| **Diamond Upgrade** | `functionalstorage:diamond_upgrade` | subtitle *x24 Storage Upgrade* |
| **Netherite Upgrade** | `functionalstorage:netherite_upgrade` | subtitle *x32 Storage Upgrade* |
| *(no title in the config)* | `functionalstorage:iron_downgrade` | *"will downgrade the Drawer's max space to a stack"* |
| *(no title in the config)* | `functionalstorage:collector_upgrade` | *"will make the Drawer vacuum items in from one of the sides"* |
| *(no title in the config)* — two quests | `functionalstorage:puller_upgrade`, and `functionalstorage:pusher_upgrade` | *"pull in items from any side"*, and *"push out items into any side"* |
| *(no title in the config)* | `functionalstorage:void_upgrade` | *"will void extra items that come when Drawers are full"* |
| *(no title in the config)* | `functionalstorage:redstone_upgrade` | *"0 - means empty. 15 - means full."* |

The four capacity upgrades are a strict chain in the config (copper → gold → diamond →
netherite), and their multipliers are the subtitles' own. **Tips and Tricks** carries a
second Functional Storage quest (verified title *Functional Storage*), so the pack points
at drawers from two chapters.

### 1e. The odds and ends, and the warning before you go digital

| Verified quest title | Task items (config) | Note |
|---|---|---|
| **Trash Cans** — subtitle *Getting Rid of The Excess* | `trashcans:item_trash_can`, `trashcans:liquid_trash_can`, `trashcans:energy_trash_can` | *"Trash Cans act as a way to destroy unwanted items, liquid, and power."* Trash Cans 1.1.0; **Mekanism: Reactors** has its own trash-can quest (*Toss it!*, `trashcans:ultimate_trash_can`) |
| **Dimensional Storage** | `dimstorage:dimensional_chest`, `dimstorage:dimensional_tank` | DimStorage 9.1.1; no dependencies, no description in the config |
| *(no title in the config)* — icon `minecraft:enchanted_book`, one `checkmark` task, no dependencies | — | The chapter's NBT warning, quoted in full below |

That last quest is the single most useful thing on this rung for a player about to build a
network, and it is the pack's own text, not this skill's opinion:

> *"Looking to create virtual storage using a mod like Applied Energistics 2? These are
> great ways to upgrade your storage, but it is important to talk about NBT Items and the
> best way to store them. NBT items are items with extra tags attached to them. Enchanted
> items, items with durability and more. … When you store a lot of these into a storage
> system like AE2, you run the chance of creating issues for your save or server. Because
> of this, it is best to store them in Chests or Bags!"*

So the ladder is not "replace rung 1 with rung 2": the pack keeps chests and backpacks in
service for exactly the items a digital network handles worst.

## Rung 2a — Refined Storage (`refined_storage`, 72 quests)

Listed before AE2 because it is the shorter jump from rung 1 — the chapter's own text
says a chest pile is a valid way in. **Refined Storage** (subtitle *Version 2*, task
`refinedstorage:controller`, no dependencies) opens: *"Refined Storage (RS or RS2) is a
mass storage mod that offers a network-based storage system."* … *"To get started with the
mod, you'll want to make the Controller."* … *"The Controller is the 'Core' of your storage
network. When provided with power, it gives life to all RS components connected."* Refined
Storage 2.0.9 in the modlist. Only two quests in this chapter have no dependencies: the controller
quest and the hidden authorship quest.

### The spine, in dependency order

| Step | Verified quest title | Task item(s) | Depends on (config) |
|---|---|---|---|
| 1 | **Refined Storage** | `refinedstorage:controller` | — |
| 2 | **Cables** — subtitle *Connecting the System* | `refinedstorage:cable` | Refined Storage |
| 3 | *(no title in the config)* — subtitle *Importing Items!* | `refinedstorage:importer` | Cables |
| 3 | *(no title in the config)* — subtitle *Exporting Items!* | `refinedstorage:exporter` | Cables |
| 3 | *(no title in the config)* — subtitle *Placing Blocks!* | `refinedstorage:constructor` | Cables |
| 3 | *(no title in the config)* — subtitle *Breaking Blocks!* | `refinedstorage:destructor` | Cables |
| 3 | *(no title in the config)* | `refinedstorage:external_storage` | Cables |
| 4 | *(no title in the config)* — subtitle *Floppy Time!* | `refinedstorage:disk_drive` | Refined Storage |
| 5 | *(no title in the config)* | `refinedstorage:storage_housing` | the disk-drive quest (`dependency_requirement: "one_started"`) |
| 6 | **The Grid** — subtitle *Don't go off the Grid* | `refinedstorage:grid` | the disk-drive quest |
| 7 | **The Better Grid** | `refinedstorage:crafting_grid` | The Grid |
| 8 | **Autocrafting** — subtitle *Follow the Pattern* | `refinedstorage:pattern` | The Grid |
| 9 | **Pattern Grid** | `refinedstorage:pattern_grid` | Autocrafting |
| 10 | **Autocrafter** — subtitle *Automated crafting!* | `refinedstorage:autocrafter` | Pattern Grid |
| 11 | **Monitoring Autocrafting** / **Managing Autocrafters** | `refinedstorage:autocrafting_monitor` / `refinedstorage:autocrafter_manager` | Pattern Grid / Autocrafter |

Also hanging directly off **Refined Storage**: **Wrench** (`refinedstorage:wrench`,
subtitle *You spin me right round'*), **Grid Networks** (`refinedstorage:network_transmitter`
+ `refinedstorage:network_receiver`, subtitle *Wirelessly Connecting Networks*), and
**Security Manager** (`refinedstorage:security_manager`, `optional`). Off the disk-drive
quest: *(no title in the config)* — subtitle *No more Manipulation!* — for
`refinedstorage:disk_interface`.

Two quotes worth repeating when a player asks whether he needs disks yet:

- **The Grid**: *"Great! We can store things virtually, but how do we see what's in the
  network? … The Grid can store Items, Fluids, Energy, Source, Souls, and Chemicals."*
- The untitled `refinedstorage:external_storage` quest: *"External Storage is a type of cable interface
  that is one of the most important items one can make in their Refined Storage journey …
  This works on many things, including but not limited to: Chests, Barrels, Drawers, Drawer
  Controllers, and more! If you can't make drives and have a bunch of chests everywhere,
  this is your best bet in creating a storage network!"* — i.e. the book's own answer to
  "I have rung 1 and no disks": point External Storage at the chests and drawers.

### The disk ladders

Item parts (all `count: 1`), with the config's own chain:

| Rung | Verified quest title | Task item | Depends on |
|---|---|---|---|
| 1 | **1k Storage Part** | `refinedstorage:1k_storage_part` | the storage-housing quest |
| 2 | **4k Storage Part** | `refinedstorage:4k_storage_part` | 1k |
| 3 | **16k Storage Part** | `refinedstorage:16k_storage_part` | 4k |
| 4 | **64k Storage Part** | `refinedstorage:64k_storage_part` | 16k |
| 5 | **Advanced Storage Housing** | `extradisks:advanced_storage_housing` | 64k **or** 4096B fluid part (`one_completed`) — *"required in order to craft high tier Storage Disks"* |
| 6 | **256k Storage Part** | `extradisks:256k_item_storage_part` | Advanced Storage Housing |
| 7 | **1024k Storage Part** | `extradisks:1024k_item_storage_part` | 256k |
| 8 | **4096k Storage Part** | `extradisks:4096k_item_storage_part` | 1024k |
| 9 | **16384k Storage Part** | `extradisks:16384k_item_storage_part` | 4096k |
| 10 | **65536k Storage Part** | `extradisks:65536k_item_storage_part` | 16384k |
| 11 | **262m Storage Part** | `extradisks:262144k_item_storage_part` | 65536k |
| 12 | **1048m Storage Part** | `extradisks:1048576k_item_storage_part` | 262m |

The fluid ladder mirrors it, in the config's own chain and with its own titles: **64B
Fluid Storage Part** (`refinedstorage:64b_fluid_storage_part`) → **256B Fluid Storage
Part** → **1024B Fluid Storage Part** → **4096B Fluid Storage Part**, then, off **Advanced
Storage Housing**, **16384B Fluid Storage Part** (`extradisks:16384b_fluid_storage_part`) →
**65536B Fluid Storage Part** → **262kB Fluid Storage Part** → **1048kB Fluid Storage
Part**. Titles are the pack's own shorthand — *262m* is a quest title,
`extradisks:262144k_item_storage_part` is the item it asks for. Extra Disks is `extradisks`
1.21.1-4.0.15 in the modlist.

**Other Storage Parts** (one quest, four tasks) widens what a disk can hold:
`refinedstorage_mekanism_integration:64b_chemical_storage_part`,
`refinedtypes:64k_energy_storage_part`, `refinedtypes:64b_source_storage_part`,
`refinedtypes:1k_soul_storage_part` — *"On top of items and fluids, Refined Storage can
also be used to store Chemicals, thanks to the Refined Storage - Mekanism Integration mod.
You can also store Energy, Source and Souls, thanks to the Refined Types mod."* (Refined
Storage - Mekanism Integration 1.1.1, Refined Types 1.21.1-0.3.2 in the modlist. The
**Industrial Foregoing** chapter asks for `refinedtypes:1k_soul_storage_part` too, in a
quest titled *Soul Storage?*.)

### Cable Tiers: elite → ultra → mega

Six device families get the same three-rung treatment from Cable Tiers
(`cabletiers` 1.21.1-0.6.14); the first rung of each is untitled in the config. The slot
counts and speed multipliers are the quests' own words:

| Family | Elite (18 slots, 2x) | Ultra (36 slots, 5x, Stack Upgrade integrated) | Mega (54 slots, 8x, Stack Upgrade integrated) |
|---|---|---|---|
| Importer | `cabletiers:elite_importer` | **Ultra Importer** | **Mega Importer** |
| Exporter | `cabletiers:elite_exporter` | **Ultra Exporter** | **Mega Exporter** |
| Constructor | `cabletiers:elite_constructor` | **Ultra Constructor** | **Mega Constructor** |
| Destructor | `cabletiers:elite_destructor` | **Ultra Destructor** | **Mega Destructor** |
| Disk Interface | `cabletiers:elite_disk_interface` | **Ultra Disk Interface** | **Mega Disk Interface** |
| Autocrafter | `cabletiers:elite_autocrafter` (18 *pattern* slots) | **Ultra Autocrafter** | **Mega Autocrafter** |

### Wireless, and scaling the network out

| Verified quest title | Task item(s) | What the quest text says |
|---|---|---|
| **Wireless Access** — subtitle *The 21st Century* | `refinedstorage:wireless_transmitter` | *"you'll need to start by creating a Wireless Transmitter … This is needed in order to use Wireless Grids."* (`dependency_requirement: "one_started"` on The Grid) |
| *(no title in the config)* — subtitle *On-The-Go Grid* | `refinedstorage:wireless_grid` | *"Allows you to access your network storage wirelessly."* |
| *(no title in the config)* | `refinedstorage_quartz_arsenal:wireless_crafting_grid` | wireless + crafting interface (Refined Storage - Quartz Arsenal 1.0.8) |
| *(no title in the config)* | `refinedstorage:wireless_autocrafting_monitor` | *"access your network crafting queue wirelessly"* |
| **Wireless Universal Grid** | `universalgrid:wireless_universal_grid` | *"access your network storage, your storage network with a crafting interface built in, and your crafting queue, all wirelessly"* (Universal Grid 1.21.1-0.3.2); depends on all three quests above |
| **Increasing Wifi Range** — subtitle *Better Signal* | `refinedstorage:range_upgrade` | *"The Wireless Transmitter can only hold 4 total."* |
| **Interdimensional Wireless Transmitter** — subtitle *TLDR: Good Wifi* | `interdimensionalwirelesstransmitter:interdimensional_wireless_transmitter` | *"infinite range, even across dimensions"* (1.21.1-0.1.5) |
| **Grid Networks** | `refinedstorage:network_transmitter`, `refinedstorage:network_receiver` | *"Because of the Controller limit, you'll probably end up wanting to connect different systems to your main hub without a billion cables connecting them."* |

### The upgrade and QoL quests

**Speeding Everything Up!** (`refinedstorage:speed_upgrade` + `refinedstorage:stack_upgrade`),
**Regulator Upgrade** (`refinedstorage:regulator_upgrade` + `refinedstorage:autocrafting_upgrade`),
**Destructor Upgrades** (`refinedstorage:silk_touch_upgrade` + a smart filter for
`fortune_1_upgrade`/`fortune_2_upgrade`/`fortune_3_upgrade`, `optional`), the
`optional` untitled `refinedstorage:storage_monitor` quest and the `optional` untitled
`refinedstorage:portable_grid` quest (its icon is `refinedstorage:creative_portable_grid`),
and the `optional` **Security Manager**.
Their texts describe keeping a machine stocked (*"telling your network that you want to
keep 64 Coal within a Furnace"*), enchanting a Destructor for a quarry loop, and granting
per-player permissions — all quest text, all worth reading in the book rather than here.

## Rung 2b — Applied Energistics 2 (`applied_energistics_2`, 74 quests)

**Applied Energistics 2** (subtitle *Virtual Storage System*, icon `ae2:quartz_cluster`,
chapter icon `ftbquests:custom_icon` → `ae2:block/controller_lights`) opens with the same
task as Basic Storage's hub — a smart filter on the tag `c:chests` — and says when to
start: *"Applied Energistics 2 (or AE2 for short) is an incredibly versatile digital
storage mod, allowing for extremely efficient storage and all sorts of automation
capabilities to greatly augment your modded Minecraft experience **from as early as you
want to the very endgame**."* The same description then hands the player to the mod's own
wiki — its last two entries read *"For more information on AE2 beyond this chapter, consult
the wiki over at"* and *"appliedenergistics.github.io."* AE2 is 19.2.17 in the modlist.
Only two quests in this chapter have no dependencies: this one and the hidden authorship
quest.

### Getting started (verified chain)

**Applied Energistics 2** → **First Things First** (`ae2:charger` + `ae2:inscriber`) →
**Meteorite hunting** (`ae2:meteorite_compass` as an `optional_task`, plus an
**advancement** task on `ae2:main/presses`; `dependency_requirement: "one_completed"`)
→ **Processors** (`ae2:logic_processor`, `ae2:calculation_processor`,
`ae2:engineering_processor`).

Two details the config states that are easy to miss:

- **Meteorite hunting** carries `dependency_requirement: "one_completed"` over two
  parents: **First Things First** and an `optional` magic-side quest (subtitle *For more
  accuracy*, task `ars_nouveau:dowsing_rod`) whose text reads *"Using a Dowsing Rod from
  Ars Nouveau will help you find the exact location of a Meteorite once you've used the
  Meteorite Compass to find its general location."* Either parent satisfies it. That
  dowsing rod and the `ars_nouveau:archwood_chest` alternative in **Vanilla Storage**'s
  filter are the only Ars Nouveau items these four chapters mention; every dependency link
  in all four chapters resolves to a quest in the same chapter.
- The resource line runs **Certus Quartz** (`ae2:certus_quartz_crystal`) → **Fluix**
  (`ae2:fluix_dust` + `ae2:fluix_crystal`) → **Basic Cabling** (smart filter on the tag
  `ae2:glass_cable`, with `ae2:covered_cable` and `ae2:covered_dense_cable` as
  `optional_task`s) → **Advanced Cabling** (tags `ae2:smart_cable`, `ae2:smart_dense_cable`).

### Power and channels — the numbers are the quests' own

| Untitled quest (config) | Task item | Quoted from its description |
|---|---|---|
| subtitle *Plug in* | `ae2:energy_acceptor` | *"RF/FE can be converted into the native AE at a ratio of 2:1 RF:AE"* |
| — | `ae2:energy_cell`, `ae2:dense_energy_cell` | *"an ME network on its own only has an internal buffer of 800AE without an ME Controller, with the controller adding an extra 8kAE per block … adding another 200kAE per regular Energy Cell and 1.6MAE per Dense Energy Cell"* |
| — | `ae2:energy_card` | *"can be applied to most chargeable devices like Portable Cells and Wireless Terminals"* |
| — | one `checkmark` task | *"Networks without an ME Controller are known as 'ad-hoc' networks and only support a maximum of 8 channels."* |
| — | `ae2:controller` | *"providing 32 channels out of each face of the block for a total of 216 channels … The controller can be up to 7x7x7 blocks in size … An ME Network may only contain one multiblock controller at any given time."* |

### Storage: cells, components, and the MEGA ladder

**The Storage** (subtitle *Items as a file system*) asks for `ae2:drive` with `ae2:chest`
as an `optional_task`: *"The ME Chest holds a single Cell at a time … The ME Drive can hold
up to 10 assorted Storage Cells in the space of a single block and a single ME channel."*
Beside it, two untitled quests: `ae2:cell_workbench` (partitioning, priority, the Inverter
Card) and `ae2:io_port` (subtitle *Defragmentation*).

| Rung | Verified quest title | Task item | Quoted capacity (quest text) |
|---|---|---|---|
| 1 | **Creating your first Storage Cell** — subtitle *The first kilobyte.* | `ae2:cell_component_1k` | *"providing 1024 'bytes' of storage"* |
| 2 | **4k Storage Component** — subtitle *x4* | `ae2:cell_component_4k` | *"4096 bytes"* |
| 3 | **16k Storage Component** — subtitle *x4^2* | `ae2:cell_component_16k` | *"16384 bytes"* |
| 4 | **64k Storage Component** — subtitle *x4^3* | `ae2:cell_component_64k` | *"65536 bytes"* |
| 5 | **256k Storage Component** — subtitle *x4^4* | `ae2:cell_component_256k` | *"The fifth and final AE2-standard tier"* |
| 6 | **1M Storage Component** — subtitle *The first MEGAbyte.* | `megacells:cell_component_1m` | *"There comes a point in any playthrough of a large modpack where even the highest standard tier of storage cell doesn't cut it … This is where the MEGA Cells add-on comes in"* |
| 7 | **4M Storage Component** | `megacells:cell_component_4m` | *"4194304 (4096k) bytes"* |
| 8 | **16M Storage Component** | `megacells:cell_component_16m` | *"16777216 (16384k) bytes"* |
| 9 | **64M Storage Component** | `megacells:cell_component_64m` | *"67108864 (65536k) bytes"* |
| 10 | **256M Storage Component** | `megacells:cell_component_256m` | *"The fifth and final MEGA tier"* |

MEGA Cells is 4.11.0 in the modlist. Around that spine:

- **Item Storage** (`ae2:item_storage_cell_1k`): *"ME Item Storage Cells can each hold up
  to 63 different types of items … a 1k Item Storage Cell containing only cobblestone can
  hold up to 8128 cobblestone (8*1024b - 8b/type * 1 type)."*
- The untitled fluid-cell quest (smart filter for `ae2:fluid_storage_cell_1k` … `_256k`):
  *"For fluids, 1 byte equals 8 buckets (8000mb)."* and *"both item and fluid cells use the
  same kind of storage component to make."*
- The untitled portable-cell quest (smart filter for the ten `ae2:portable_item_cell_*` and
  `ae2:portable_fluid_cell_*` sizes): *"a bit like a digital ME-flavoured backpack."*
- **Bulk Item Storage** (`megacells:bulk_item_cell`): *"limited to no more than one type of
  item storeable per cell but can store a practically INFINITE\* number of that item type …
  \*Technically 'max long'. If you know, you know."*
- Two cell cards off the workbench quest: `ae2:equal_distribution_card` (subtitle *ME
  Storage Cells Drawers* — *"comparable to something like a Functional Storage drawer"*)
  and `ae2:void_card` (*"pretty much the Void Upgrade from any Sophisticated Mod"*). Both
  quotes are the pack explicitly tying rung 2b back to rung 1.

### Getting items in and out

**The IO** (subtitle *OI, OI, OI!*, smart filter on the tag `ae2:interface`) branches into
five untitled quests — the book shows each item's own name for them — `ae2:import_bus`
(subtitle *The I*), `ae2:export_bus` (subtitle *The O*), `ae2:storage_bus` (subtitle *The
spare chest*: *"will allow the container to be used as though it were part of the ME
network"*), `ae2:annihilation_plane` (subtitle *GET IN*), and `ae2:formation_plane`
(subtitle *GET OUT*). The import and export buses each have a plane quest behind them.
Also off **The IO**: **P2P Tunnels** (`ae2:me_p2p_tunnel`) and the untitled
`ae2:memory_card` quest behind it, **Forgot to Mention** (`ae2:quartz_fiber`, on
subnetting), the untitled `ae2:capacity_card` quest, and two titled card quests —
**Loosely Speaking** (`ae2:fuzzy_card` + `ae2:inverter_card`) and **Redstone-Controlled
ME** (`ae2:redstone_card` + `ae2:toggle_bus`), which the untitled `ae2:crafting_card` quest
(subtitle *Automation in upgrade form!*) hangs off.

### Autocrafting

**Auto-Crafting** (subtitle *Order up*; smart filter on the tag `ae2:pattern_provider` plus
`ae2:pattern_access_terminal` — *"Up to 9 patterns can fit in one provider"*) →
**Patterns** (`ae2:pattern_encoding_terminal` + `ae2:blank_pattern`) → the untitled
`ae2:molecular_assembler` quest (*"Up to 6 MAs can be connected to a single Pattern
Provider"*) → the untitled `ae2:speed_card` quest (*"a full set of 5 cards reduces the time
taken for the MA to fulfil a craft from one second (with no cards) to one tick"*).

The crafting-CPU line, all untitled in the config and labelled by subtitle:
*Download more RAM* (`ae2:1k_crafting_storage` … `ae2:256k_crafting_storage` via one smart
filter) → *Download more CPU cores* (`ae2:crafting_accelerator`) → *Download more VRAM*
(`ae2:crafting_monitor`). Beside it: **ME Level Emitter** (`ae2:level_emitter`) and the
untitled `ae2:growth_accelerator` quest (*"Place these around your Budding Crystals"*).

The singularity line: **Condensed Matter** (`ae2:condenser` + `ae2:matter_ball`) →
**Hyper-Condensed Matter** (`ae2:singularity`, `ae2:ender_dust`, `ae2:tiny_tnt` — *"A single
singularity requires 256000 items to be voided. That's exactly 4000 stacks!"*) →
**Quantum Network Bridge** (`ae2:quantum_ring`, `ae2:quantum_link`,
`ae2:quantum_entangled_singularity`).

### Wireless

The untitled `ae2:wireless_access_point` + `ae2:wireless_booster` quest hangs off the
controller quest → **Wireless Terminals** (subtitle *This is what you're here for*;
`ae2:wireless_terminal` + `ae2:wireless_crafting_terminal`) → **Infinity Booster**
(`aeinfinitybooster:infinity_card` + `aeinfinitybooster:dimension_card`, AEInfinityBooster
1.21.1-1.0.0.58), and the untitled `ae2wtlib:quantum_bridge_card` quest (AE2WTLib 19.5.1)
which depends on both **Quantum Network Bridge** and **Wireless Terminals**.

### Spatial IO, tools, and the extras

**Spatial IO** (`ae2:spatial_io_port`) → the untitled `ae2:spatial_pylon` quest →
**Spatial Storage Cell** (smart filter for `ae2:spatial_storage_cell_2`, `_16`, `_128`:
*"a maximum of 2x2x2, 16x16x16 and 128x128x128 blocks' worth of space"*) plus the
`optional` `ae2:spatial_anchor` (*"functions as a chunk loader"*). Tools: **Quartz Wrench**
(tag `ae2:quartz_wrench`), **Network Tools** (`ae2:network_tool`), **Cable Anchor** (tag
`ae2:knife` + `ae2:cable_anchor` + `ae2:name_press`), **Color Applicator**
(`ae2:color_applicator`). **The... Weapons?** (subtitle *Too hot for the ATF*) bundles
`ae2:charged_staff`, `ae2:entropy_manipulator`, `ae2:matter_cannon` — the chapter's own
*"extra toys"*.

Finally, one `optional` untitled quest with a single `checkmark` task exists purely to hand
the player links: *"Here's some additional AE2 guides beyond the official AE2 guide, and
the in game one."* — clickable text for the AllTheGuides AE2 page
(`https://allthemods.github.io/alltheguides/mods/ae2/`) and three video guides. The pack
points at its own guide site; so can this skill, without vouching for any number in it.

## Rung 3 — Extended \& Advanced AE (`extended__advanced_ae`, 56 quests)

The chapter is one file covering two AE2 addons. Its entry quest, **Extended \& Advanced
AE** (task `ae2:fluix_crystal`, no dependencies), says: *"Extended and Advanced AE are
addons for Applied Energistics 2. Both of them focus on improving your experience, adding
improved versions of various devices, and more."* From it the config forks into two named
hubs — **ExtendedAE** (task `ae2:fluix_block`) and **Advanced AE** (task
`ae2:logic_processor`, icon `advanced_ae:shattered_singularity`) — and 14 quests belong to
the ExtendedAE side, 36 to the Advanced AE side (23 of those are Quantum Armor upgrade
cards), the rest being the two hubs, the entry quest, **Automating Entro Crystals**, and
two untitled `checkmark` quests.

### The ExtendedAE side (`extendedae` 1.21-2.2.38-neoforge)

**ExtendedAE**: *"an addon for Applied Energistics 2, focused on adding improved versions
of various devices, and bringing back some features from older versions of AE2."* … *"To get
started, get a Fluix Block."*

| Verified quest title | Task item(s) | What the quest text says |
|---|---|---|
| **The Crystals of Space and Time: Entro Crystals** | `extendedae:entro_seed`, an **observation** task on `extendedae:entro_budding_fully`, `extendedae:entro_crystal` | *"Right click the Fluix Block with the Entro Seed … Unlike with Certus, its decay is inevitable."* |
| **Automating Entro Crystals** *(optional)* | smart filter: `mysticalagriculture:entro_seeds` **or** a `productivebees:bee_type` component of `productivebees:entro` | *"Fortunately, there's a bee for that. And a seed, as well."* |
| **Complex Crafter: The Crystal Assembler** | `extendedae:crystal_assembler` | *"It's time we upgrade to the Crystal Assembler"* — the dependency every ExtendedAE device quest below hangs off |
| **Faster and Bigger: Extended Devices** | smart filter for the nine `extendedae:ex_*` devices (import/export bus, charger, inscriber, molecular assembler, drive, io port, interface, pattern provider) | *"The Extended Pattern Provider has 36 pattern slots, 4 times as many as an ordinary Pattern Provider"*; the ex buses *"work about 8x faster"* |
| **Blocks to Circuits: The Circuit Slicer** | `extendedae:circuit_cutter` | *"making up to 9 circuits at a time (or 4 in the case of certus or entro)"* |
| **Connections across long distances: The Wireless Connector** | `extendedae:wireless_connect`, `extendedae:wireless_tool` | *"it can only connect to Wireless Connectors up to about 1000 blocks away, and cannot connect across dimensions"* |
| **Branches of Connections: The Wireless Hub** | `extendedae:wireless_hub` | *"It can now connect to 8 different Wireless Connectors or Hubs. Note that the Hub can only transfer 32 channels in total."* |
| **Better Pattern Access: The Extended Pattern Access Terminal** | `extendedae:ex_pattern_access_part` | improved pattern search, highlight, and in-world provider highlight |
| **Can this Liquid: The ME Canner** | `extendedae:caner` | *"can fill or empty containers that can contain fluids, chemicals, energy"* |
| **Get-Yer-Crystals-Fixed: The Crystal Fixer** | `extendedae:crystal_fixer` | *"you can fix Budding Certus Crystals with Charged Certus Quartz, and Entroized Fluix with Ender Dust"* |
| **Actively Placing From The Network: The Active Formation Plane** | `extendedae:active_formation_plane` | *"It works like an ME Export Bus but it treats the world as its medium."* |
| **Matter Condenser in a Cell: The Void Cell** | `extendedae:void_cell` | *"It will delete anything that enters the ME system that matches the filter … or condenses them into Matter Balls or Singularities"* |
| **More Resources than you ever need: Infinity Cells** | smart filter accepting 25 `kubejs:*_cell` items plus `extendedae:infinity_water_cell` and `extendedae:infinity_cobblestone_cell` | *"These cells provide a limitless supply of a certain type of resource, such as Water, Cobblestone, Lava, etc."* |
| **Many Assemblers In One: The Assembler Matrix** | `extendedae:assembler_matrix_frame` + a smart filter for `assembler_matrix_wall`/`assembler_matrix_glass` | *"must be at least a 3x3x3 cuboid and up to a 7x7x7 cuboid"* |
| **Assembler Matrix Cores** | `extendedae:assembler_matrix_pattern`, `…_crafter`, `…_speed` | *"Craft Cores add 8 maximum parallel crafting jobs … Pattern Cores add 36 pattern slots … Installing more than 5 Speed Cores does not have an effect"* |

Two of those rows — **The Void Cell** and **Infinity Cells** — do not sit behind the Crystal
Assembler. They hang off an untitled `checkmark` quest whose whole text is *"These are
things from ExtendedAE that don't require Entro Crystals."*: the chapter's own split
between the Entro line and everything a player can build without it.

### The Advanced AE side (`advanced_ae` 1.6.12-1.21.1)

**Advanced AE**: *"an addon for Applied Energistics 2, that focuses on improving user
experience whenever you handle your ME System and **expanding the possibilities of end game
systems**."* That is the pack's own word for when this rung matters.

| Verified quest title | Task item(s) | Depends on |
|---|---|---|
| **Reaction Efficency: The Reaction Chamber** *(spelled that way in the config)* | `advanced_ae:reaction_chamber` | Advanced AE |
| **Quantum Ingredients** | `advanced_ae:shattered_singularity`, `advanced_ae:quantum_alloy`, `advanced_ae:quantum_processor` | Reaction Chamber |
| **Specific Sided Patterns: The Advanced Pattern Provider** | smart filter on the tag `advanced_ae:adv_pattern_provider` + `advanced_ae:adv_pattern_encoder` | Advanced AE |
| **Infinite Crafting Jobs: The Quantum Computer** | `advanced_ae:quantum_unit`, `advanced_ae:quantum_structure` | Quantum Ingredients |
| **Massive Crafting Storage: The Quantum Computer Storage** | `advanced_ae:quantum_storage_128`, `advanced_ae:quantum_storage_256` | Quantum Computer |
| **Co-Processing Oblivion: Quantum Computer Accelerator** | `advanced_ae:quantum_accelerator` | Quantum Computer |
| **Heart of the Crafts: Quantum Computer Core** | `advanced_ae:quantum_core` | Accelerator + Storage |
| **Co-Processing To Infinity: Quantum Computer Multi-Threader** | `advanced_ae:quantum_multi_threader` | Core + Crystal Assembler |
| **Unnecessarily Large Storage: Quantum Data Entangler** *(optional)* | `advanced_ae:data_entangler` | Core + Crystal Assembler |
| **Fully Automated Crafting: The Quantum Crafter** | `advanced_ae:quantum_crafter` | Accelerator |
| **The Ultimate Quantum Computer** | `advanced_ae:quantum_structure`, `quantum_accelerator`, `quantum_core`, `quantum_multi_threader` | Multi-Threader |
| **ME System As Armor: The Quantum Armor** | `advanced_ae:quantum_helmet`, `…_chestplate`, `…_leggings`, `…_boots` | Quantum Ingredients |
| **Upgrades for Quantum Armor** | `advanced_ae:quantum_upgrade_base` | Quantum Armor |

Quoted numbers on that side: *"Quantum Accelerators add 12 co-processing threads each"*;
the Multi-Threader *"multiplies co-processing threads in the Quantum Computer Multiblock by
6"* and — the line that ties this chapter to the endgame — *"It is also an ingredient for
the ATM Star."*; the Core *"has 256M crafting storage and 12 co-processing threads by
itself"*; the Data Entangler means *"a 256M quantum crafting storage will now give 1.5G
Crafting Storage"*; and **The Ultimate Quantum Computer** spells out its own build: *"218
Quantum Computer Structural Glass, 123 Quantum Computer Accelerators, 1 Quantum Computer
Core, and 1 Quantum Computer Multi-Threader are what we need. This gives us a total of
8928 co-processing threads."*

The 23 armor-card quests behind **Upgrades for Quantum Armor** are untitled except for
their subtitles, which the book shows: *Creative Flight* (`flight_card`), *No Flight Drift*
(`flight_drift_card`), *+20 Max HP* (`hp_buffer_card`), *+30% Evasion Chance*
(`evasion_card`), *+10 Strength* (`strength_card`), *+5 Attack Speed* (`attack_speed_card`),
*+2 Luck* (`luck_card`), *Up to +3 Step Height* (`step_assist_card`), *Up to +3 Jump
Height* (`jump_height_card`), *Up to +5 Reach* (`reach_card`),
and the rest by item id: `walk_speed_card`, `sprint_speed_card`, `swim_speed_card`,
`lava_immunity_card`, `water_breathing_card`, `auto_feeding_card`, `auto_stock_card`,
`magnet_card`, `regeneration_card`, `night_vision_card`, `recharging_card`,
`portable_workbench_card` (subtitle *Cell Workbench Wherever You Go*), `pick_craft_card`.
The armor's own text says why a storage chapter ends in a chestplate: *"it can Linked to
your Storage System! Then, you can automatically take Energy out from it and take out any
Item from it no matter where you are."*

The chapter's canvas art underlines the tie: its `images` list includes
`allthetweaks:item/atm_star` alongside the four Quantum Armor pieces and pictures of the
Assembler Matrix and the Quantum Computer.

## When to upgrade — the pack's own signals

A signal in quotation marks is the book's own text; one written without quotes is this
skill's reading of the book's structure, and is approximate. The rung to move to is never a
gate: an untitled quest in the pack's Welcome chapter says *"In this modpack, quests are
optional. Mods are not gated behind completing any quests!"* (see
`references/progression.md`).

| Signal | Where it comes from | Move to |
|---|---|---|
| *"Inventories are too Small"* | **Sophisticated Backpacks** subtitle | Rung 1c — a backpack, then its upgrade tree |
| Piles of one bulk item (cobblestone, dirt, seeds) | **Functional Storage** text: *"useful for items like Cobblestone, Dirt and more"*; Tips and Tricks: *"great for items you get a lot of, like Cobblestone or Seeds!"* | Rung 1d — drawers, then the x8 → x32 upgrades |
| Chests are right, but too small and too many | **Sophisticated Storage** text: *"upgrade your Chests and Barrels with metals to increase their storage"* | Rung 1b — copper → netherite tiers, then a controller |
| A spread-out base needs one inventory | the controller quest: *"acts as an in/out point for all storages attached to it"*, 14-block range | Rung 1b infrastructure (`controller`, `storage_tool`, `storage_link`) |
| *"If you can't make drives and have a bunch of chests everywhere, this is your best bet in creating a storage network!"* | the untitled `refinedstorage:external_storage` quest | Rung 2a — Refined Storage, starting with External Storage on the existing chests |
| You want one grid over everything, plus autocrafting | **Refined Storage** (*"network-based storage system"*) and **Applied Energistics 2** (*"from as early as you want to the very endgame"*) | Rung 2a or 2b — pick one; see below |
| Ad-hoc AE2 network hitting its channel ceiling | the channels quest: *"only support a maximum of 8 channels"*; controller: *"216 channels"* | Rung 2b — an ME Controller |
| Enchanted, damaged, or otherwise NBT-bearing items | the NBT quest: *"it is best to store them in Chests or Bags!"* | **Stay on rung 1** for those items |
| The top AE2 cell tier is not enough | **1M Storage Component**: *"even the highest standard tier of storage cell doesn't cut it"* | Rung 2b's MEGA ladder (`megacells`), then **Bulk Item Storage** for one-type bulk |
| The top RS disk tier is not enough | **Advanced Storage Housing**: *"required in order to craft high tier Storage Disks"* | Rung 2a's Extra Disks ladder (256k → 1048m) |
| Autocrafting throughput is the bottleneck | **Assembler Matrix Cores**, **Quantum Computer Accelerator** | Rung 3 — ExtendedAE matrix, then Advanced AE's quantum line |
| Machines need inputs on specific sides | **The Advanced Pattern Provider** — subtitle *Looking at you, Mekanism* | Rung 3 — `advanced_ae:adv_pattern_encoder` |
| The base spans dimensions | **Grid Networks** + **Interdimensional Wireless Transmitter**; **Quantum Network Bridge** | Rung 2a/2b wireless lines |
| The ATM Star is the goal | Chapter 3 asks for `ae2:singularity`, `ae2:quantum_ring`, `megacells:portable_item_cell_256m`, `advanced_ae:quantum_multi_threader`, `ae2wtlib:wireless_universal_terminal`, `aeinfinitybooster:infinity_card` | Rungs 2b and 3 — see `references/atm-star-checklist.md` |

## Which one: Refined Storage or AE2

Per `SKILL.md`, present these as alternatives with their trade-offs and let the player
pick; never invent a required path. What the config supports saying:

- **Both are full chapters in the same group**, both `progression_mode: "flexible"`, and
  neither chapter's quests depend on the other's. Nothing in these four chapters forces a
  choice.
- **Addon depth differs, and both are deep.** Refined Storage's chapter pulls in Extra
  Disks, Cable Tiers, Refined Types, Refined Storage - Mekanism Integration, Refined
  Storage - Quartz Arsenal, Universal Grid, and Interdimensional Wireless Transmitter.
  AE2's chapter pulls in MEGA Cells, AEInfinityBooster, and AE2WTLib, and has a whole
  second chapter (Extended \& Advanced AE) for ExtendedAE and Advanced AE.
- **The ATM Star line is AE2-family.** Verified in `chapter_2_the_star.snbt` at this
  commit: its storage-related tasks are `ae2:singularity`, `ae2:quantum_ring`,
  `megacells:portable_item_cell_256m` (also as an either/or with
  `modern_industrialization:blastproof_casing`), `advanced_ae:quantum_multi_threader`,
  `ae2wtlib:wireless_universal_terminal`, and `aeinfinitybooster:infinity_card` — and
  **no** `refinedstorage:`, `cabletiers:`, `extradisks:`, or `refinedtypes:` task appears
  in that chapter at all. A star-chasing player touches the AE2 line whether or not it is
  his main system; that is a fact about Chapter 3, not a verdict on Refined Storage, which
  remains a complete main system on its own.
- **Pocket Storage is the star's other storage ask** (`pocketstorage:psu_1` hub,
  `pocketstorage:psu_4` for the Pulsating Black Hole) and it is *not* in the Storage group
  — it is a Chapter 3 mod line. See `references/atm-star-checklist.md`.

## Near the ladder but not in it

- **Logistics group** — `basic_logistics` (**Basic Logistics**, 40 quests, from the
  titled *Item Pipez* (`pipez:item_pipe`) to untitled quests for Mekanism's logical
  transporters and a LaserIO `laserio:card_holder`), `integrated_dynamics`,
  `modular_router`, `pylons`. Moving items between inventories is that group's job; the
  Storage group holds them. `references/progression.md` maps the group.
- **Integrated Dynamics** is the other network-shaped storage option the pack ships
  (its chapter's own text: *"a logistics mod that can be used for storage, item/power/fluid
  transfer and more!"*), and the Sophisticated Storage controller quest names it alongside
  Applied Energistics. It is filed under Logistics, not Storage.
- **Trash Cans** appear twice: rung 1e here and **Mekanism: Reactors**' *Toss it!* quest.
- **Storage Delight** has a quest in **Building Tips** (*"all about Item Storage but making
  it look pretty"*), and **Functional Storage** has one in **Tips and Tricks**. Cosmetic
  and QoL storage lives outside the Storage group.
- **Sophisticated Storage In Motion**, **Sophisticated Backpacks Create Integration**, and
  the other storage-adjacent mods in `config/crash_assistant/modlist.json` have **no**
  quest in these four chapters: if the player asks about them, the answer is JEI and the
  mod's own docs, not this page.

## Cross-references

- `references/progression.md` — the Storage group's place in the book layout (group 3 of
  10) and in stage 2 (*"AE2 or Refined Storage — pick one"*).
- `references/key-mods.md` — the short primers for AE2 and Refined Storage in the tech
  line, and the "Small but verified" row for the Sophisticated/Functional family.
- `references/atm-star-checklist.md` — Chapter 3's AE2-family tasks (*Singularity*,
  *Quantum Computer Multi-Threader*, *Universal Wireless Terminal*, *256M Portable Item
  Cell*) and the Pocket Storage line.
- `references/creative-checklist.md` — Chapter 4's `ae2:creative_energy_cell` (*Creative
  Energy Cell*), the storage-adjacent creative item.
- `examples/progress.example.json` — the four chapter ids this page describes: `storage`
  (stage `early-game`), `applied_energistics_2`, `extended__advanced_ae`, `refined_storage`
  (all stage `tech`). Record them with `scripts/progress.py --set storage done`.

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item above is a quest *task*, a *reward*, or a quote from a
  quest's own description; JEI has the recipe, and recipes are where pack versions differ
  most. Where a quest description spells out ingredients (the Quantum Ingredients quest
  does), that is quoted quest text — verify it in JEI before building around it.
- **Slot counts for backpacks, chests, and drawers.** The config never states how many
  slots a `sophisticatedbackpacks:gold_backpack` or a `functionalstorage:oak_4` holds; the
  only capacity numbers on this page are the ones the quest texts and subtitles themselves
  print (*27 slots* for a vanilla chest, *x8 → x32* drawer upgrades, *+2 → +16* stack
  upgrades, AE2's byte tables, Cable Tiers' slot counts). Anything else is in the book.
- **Energy costs, channel budgets for a given build, throughput, or lag advice.** The
  quoted AE and channel figures are the quests' own; a real network's numbers depend on the
  player's build and pack version.
- **An order the book does not have.** All four chapters are `progression_mode:
  "flexible"`, and the rungs here are a reading of `order_index` plus the config's
  dependency links. Nine dependency entries in the AE2 chapter name a *task* id inside the
  same chapter rather than a quest id; each resolves to the quest that owns that task, and
  this page reads them that way — flagged here because it is the config's quirk, not a
  second meaning.
- **Which mod is better.** The pack ships both lines and gates nothing behind either.
- **Anything not in the config.** If a player names a storage mod, tier, upgrade, or count
  that is not listed here, the answer is "open that quest in the book / look it up in JEI" —
  never a guess.
