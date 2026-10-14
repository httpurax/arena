# Autocrafting in ATM10: AE2 and Refined Storage — how to make the game craft things for you

**What this page is.** The beginner autocrafting map for **All the Mods 10**: how to get
from chests and a crafting table to a network that crafts on request. It answers the
question *"how do I make the game craft things for me?"* — which quests to do, in which
order, on either of the pack's two storage systems — and nothing more. It is a *map of
three quest chapters*, not a crafting guide.

Short answer: teach the network a recipe once (a **Pattern**), put that Pattern where the
system can execute it (AE2: a Pattern Provider plus a Molecular Assembler and a crafting
CPU; Refined Storage: an Autocrafter), then request the result from the network instead of
crafting it by hand. Everything below is that sentence expanded into the quest book's own
order.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, count, dependency, and quoted sentence below comes
from the official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10)
at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/applied_energistics_2.snbt` | the AE2 chapter's 74 quests, their task items and required counts, dependency links, and canvas positions |
| `config/ftbquests/quests/chapters/refined_storage.snbt` | the Refined Storage chapter's 72 quests, task items, counts, and dependency links |
| `config/ftbquests/quests/chapters/extended__advanced_ae.snbt` | the Extended & Advanced AE chapter's 56 quests, task items, counts, and dependency links |
| `config/ftbquests/quests/lang/en_us/chapters/applied_energistics_2.snbt` | the English quest titles, subtitles, and description text quoted for AE2 |
| `config/ftbquests/quests/lang/en_us/chapters/refined_storage.snbt` | the same for Refined Storage |
| `config/ftbquests/quests/lang/en_us/chapters/extended__advanced_ae.snbt` | the same for Extended & Advanced AE |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the three chapters' own titles |
| `config/ftbquests/quests/lang/en_us/chapter_group.snbt` | the quest-book group the chapters sit in, `Storage` |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (489 mod ids) |
| `config/bcc-common.toml` | the pack version itself (`modpackVersion` 8.2) |

The book names the chapters **Applied Energistics 2**, **Refined Storage**, and
**Extended & Advanced AE**, all in the group **Storage**. The skill tracks them as
`applied_energistics_2`, `refined_storage`, and `extended__advanced_ae` (the config
filenames), stage `tech`. The pre-network chapter in the same group is **Basic Storage**
(`storage`, 90 quests, stage `early-game`): if chests and drawers still meet the need,
nothing on this page is required yet. The star components that later draw on AE2 live in
`references/atm-star-checklist.md`; this page stops at a working first autocraft and the
scale-up quests behind it.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file. The in-game quest book is authoritative
  wherever this page is uncertain.
- **Item ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the task's required amount); where the config
  asks for one item, no count is printed. Item ids are the pack's own strings. Where a
  task is a filtered `ftbfiltersystem:smart_filter` (FTB Filter System 21.1.4), the filter
  is quoted instead of pretending the task names a plain item.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Every
  "how" on this page is a quote from that quest's own description, marked as quest text,
  or a pointer to JEI. Do not fill a recipe in from memory or plausibility.
- **Approximate means approximate.** Which system feels simpler, when to scale up, machine
  tiers, energy amounts, and farm layouts are version-sensitive or a matter of judgement;
  anything not quoted from the config is flagged as approximate or judgement.
- **Titles are the config's.** 42 of the AE2 chapter's 74 quests, 52 of the Refined Storage
  chapter's 72, and 31 of the Extended & Advanced AE chapter's 56 carry an explicit
  `quest.*.title`. The rest are marked *(no title in the config)* — the book then shows the
  task item's own name (or its task title, where the lang file gives one). Do not present a
  derived name as a verified title.
- **Nothing here was invented, and nothing is added from memory.** A quest, item, or count
  that is not on this page was not in the three chapters read: the answer is "open that
  quest in the book / look it up in JEI" — never a guess, never a plausible-sounding bridge
  between the two systems.

## How autocrafting is shaped in this pack

Two complete systems, one idea. Both chapters teach the same loop in their own words —
store a recipe as a Pattern, let a machine execute it, request the result — and the book
lays each chapter out on a **canvas, not as a numbered list**, so the chains below are
written **in dependency order** (a quest appears after the quests the config says it
depends on; the three AE2 chain quests directly off *Auto-Crafting* — *Patterns*, the
crafting-CPU quest, and *ME Level Emitter* — can be done in any order among themselves):

| Chapter (config filename) | Quests | Titled in the config | Role on this page |
|---|---|---|---|
| Applied Energistics 2 (`applied_energistics_2`) | 74 | 42 (32 marked *(no title in the config)* below where relevant) | ME network + autocrafting (Applied Energistics 2 19.2.17) |
| Refined Storage (`refined_storage`) | 72 | 52 (20 untitled) | RS network + autocrafting (Refined Storage 2.0.9) |
| Extended & Advanced AE (`extended__advanced_ae`) | 56 | 31 (25 untitled) | AE2 addons: bigger providers, the Assembler Matrix, the Quantum Computer (ExtendedAE 1.21-2.2.38-neoforge, Advanced AE 1.6.12-1.21.1, MEGA Cells 4.11.0) |

**Pick one system as the main network first** — that is judgement, not pack data
(approximate: either system carries a base; building both autocrafting setups before the
first craft doubles the prerequisite work). The pack's own framing, quoted: AE2's hub quest
calls AE2 *"an incredibly versatile digital storage mod"*, and the Refined Storage hub says
*"To get started with the mod, you'll want to make the Controller"* because *"The Controller
is the 'Core' of your storage network."* The verifiable differences are structural:

|  | AE2 (verified from the chapter) | Refined Storage (verified from the chapter) |
|---|---|---|
| Recipe store | Pattern in a Pattern Provider (*Auto-Crafting*); up to 9 patterns per provider (quest text) | Pattern in an Autocrafter (*Autocrafter*) |
| Craft executor | Molecular Assembler on the provider's face (untitled quest, `ae2:molecular_assembler`) | The Autocrafter itself; facing a machine executes processing patterns (quest text) |
| Job holder | A crafting CPU multiblock is required before a job can run (untitled quest, subtitle *Download more RAM*) | No CPU quest exists in the RS chapter — the chain goes Grid → Pattern → Autocrafter |
| Request | From the network terminal side; progress shown by the Crafting Monitor quest line | From the Grid: *"pressing Control + Shift whilst clicking on the item"* (quest text) |
| Watch / cancel | Crafting Monitor *"displays the overall item being crafted"* (quest text) | Crafting Monitor shows the queue so the player can *"cancel crafts that aren't working"* (quest text) |

Two manual-crafting lookalikes, so they are not mistaken for autocrafting: AE2's
**Terminals** quest pairs `ae2:terminal` with `ae2:crafting_terminal`, whose text is a
*"built-in crafting grid"* for crafting by hand from network stock; Refined Storage's
**The Better Grid** (`refinedstorage:crafting_grid`) is *"a crafting interface"* on the
storage view. Both are convenience crafting — the player still crafts. Autocrafting starts
at the Pattern quests below.

## AE2: the network you need before the first autocraft

The *Auto-Crafting* quest itself only depends on **Basic Cabling**, but its own text assumes
a powered, cabled network with somewhere to stand and request from. In the chapter's order,
that is this prerequisite run (all verified titles unless marked):

| # | Verified quest title | Task items in the config | Why it comes first (quest text) |
|---|---|---|---|
| 1 | **Applied Energistics 2** *(hub, subtitle Virtual Storage System)* | `ftbfiltersystem:smart_filter` filtered to `item_tag(c:chests)` | The chapter entry point; its text points at the AE2 wiki for depth beyond the chapter |
| 2 | **First Things First** | `ae2:charger`, `ae2:inscriber` | *"Two of the very first things you will need"* — the Charger charges Certus Quartz; the Inscriber makes Printed Circuits and Processors |
| 3 | **Meteorite hunting** | `ae2:meteorite_compass` *(optional task)* + the `ae2:main/presses` advancement | The Mysterious Cube holds *"all of the different Presses used in the Inscriber"* |
| 4 | **Processors** | `ae2:logic_processor`, `ae2:calculation_processor`, `ae2:engineering_processor` | *"an important crafting ingredient used to make the large majority of ME-connected devices"* |
| 5 | **Certus Quartz** | `ae2:certus_quartz_crystal`, `ae2:certus_quartz_dust` | *"To get started with AE2, you will need to mine an important resource"* |
| 6 | *(no title in the config; subtitle Plug in)* | `ae2:energy_acceptor` | Converts RF/FE to AE at *"2:1 RF:AE"* (quest text), directly through an ME Controller or through the acceptor |
| 7 | **Fluix** | `ae2:fluix_dust`, `ae2:fluix_crystal` | *"used throughout the vast majority of AE2 devices and serving as a base for crafting all of the cabling"* (how Fluix is made: the quest entry and JEI) |
| 8 | **Basic Cabling** | `ftbfiltersystem:smart_filter` tasks for `item_tag(ae2:glass_cable)`, plus covered cables *(optional tasks)* | Glass/covered cable carries *"up to 8 channels"*, dense *"up to 32 channels"* (quest text) |
| 9 | *(no title in the config; checkmark task titled Foreword on Channels)* | checkmark only | Ad-hoc networks without a controller *"only support a maximum of 8 channels"* (quest text) |
| 10 | **Terminals** | `ae2:terminal`, `ae2:crafting_terminal` | The window into the network — manual crafting grid included, not yet autocrafting (see above) |
| 11 | *(no title in the config)* | `ae2:controller` | *"32 channels out of each face"* per controller block, multiblock *"up to 7x7x7"* (quest text); one controller multiblock per network, a second *"will cause a conflict, shutting down the whole network"* |
| 12 | **The Storage** | `ae2:drive` (+ `ae2:chest` as an optional task) | The ME Drive *"can hold up to 10 assorted Storage Cells"* on one channel; the ME Chest holds a single cell |
| 13 | **Creating your first Storage Cell** | `ae2:cell_component_1k` | The 1k component gives *"1024 'bytes' of storage for a given cell"* (quest text); larger components are their own quest line |

What this buys: power in (step 6), a cabled network (8, 11), a terminal to see it (10), and
cells to hold stock (12, 13). Skip the controller (11) only while the 8-channel ad-hoc limit
in step 9 still fits — approximate judgement; the book's order builds it before *The
Storage* completes the set.

## AE2: the autocrafting chain, in dependency order

One hub, three chain spokes. **Auto-Crafting** is the hub; everything else in this section
depends on it directly or through one of its spokes, exactly as the config links them. (A
fourth direct dependent, the crystal-growth quest, is called out separately below precisely
because it is not part of the chain.)

| # | Verified quest title | Task items in the config | Needs | What the quest text says it does |
|---|---|---|---|---|
| 1 | **Auto-Crafting** *(subtitle Order up)* | `ftbfiltersystem:smart_filter` filtered to `item_tag(ae2:pattern_provider)` (task title *ME Pattern Provider*); `ae2:pattern_access_terminal` | Basic Cabling | *"AE2's auto-crafting system begins with the ME Pattern Provider"*; *"Up to 9 patterns can fit in one provider"*; the Pattern Access Terminal exists to *"remotely access the contents of any and all providers on your wider ME network"* |
| 2 | **Patterns** | `ae2:pattern_encoding_terminal`, `ae2:blank_pattern` | Auto-Crafting | *"Patterns are what hold an encoded recipe to be fulfilled by a Pattern Provider"*; a pattern holds *"either a regular crafting recipe"* (Molecular Assembler) *"or a more general 'processing' recipe"* (items sent into another machine) |
| 3 | *(no title in the config)* | `ae2:molecular_assembler` | Patterns | *"AE2's equivalent of an automatic crafting table, required to fulfil any and all crafting pattern jobs"*; *"Up to 6 MAs can be connected to a single Pattern Provider"*; an Assembler *"will not themselves take up a channel"*; standalone, its own pattern slot crafts inserted matches |
| 4 | *(no title in the config; subtitle Download more RAM; task title Crafting Storage)* | `ftbfiltersystem:smart_filter` filtered to any of `ae2:1k_crafting_storage`, `ae2:4k_crafting_storage`, `ae2:16k_crafting_storage`, `ae2:64k_crafting_storage`, `ae2:256k_crafting_storage` | Auto-Crafting | *"Before you can carry out an auto-crafting job, you need a device to actually store the request itself"* — the crafting CPU, *"a multiblock structure requiring at least one Crafting Storage block"* that *"must be a solid cuboid"* |
| 5 | *(no title in the config; subtitle Download more CPU cores)* | `ae2:crafting_accelerator` | the Crafting Storage quest (4) | The co-processor lets providers *"work concurrently to make multiple required ingredients"*; *"one co-processor 'thread'"* per base block, the MEGA Cells unit *"provides 4 threads"* (quest text) |
| 6 | *(no title in the config; subtitle Download more VRAM)* | `ae2:crafting_monitor` | the co-processing quest (5) | *"displays the overall item being crafted, along with the remaining quantity"* of it |
| 7 | *(no title in the config)* | `ae2:speed_card` | the Molecular Assembler quest (3) | As an Assembler upgrade (the book calls it the Acceleration Card): *"a full set of 5 cards reduces the time taken for the MA to fulfil a craft from one second (with no cards) to one tick"* (quest text) |
| 8 | **ME Level Emitter** | `ae2:level_emitter` | Auto-Crafting | Emits redstone as a stocked item *"falls below, goes above or equals the given quantity"*; the book's example is switching machines on *"to auto-craft a resource when it falls below a given minimum amount"* |
| 9 | **Redstone-Controlled ME** | `ae2:redstone_card`, `ae2:toggle_bus` | ME Level Emitter | Devices (or, through a Toggle Bus, whole *"sections"* of the network) work *"only when powered with redstone"* (quest text) |
| 10 | *(no title in the config; subtitle Automation in upgrade form!)* | `ae2:crafting_card` | Redstone-Controlled ME | In an Interface or Export Bus the card *"automatically send[s] out its own crafting requests"*; in a Level Emitter it can emit *"specifically to craft the item"* even *"without even requiring a crafting pattern"* where only a redstone signal is needed (quest text) |

One sibling to not confuse with the chain: a further quest off *Auto-Crafting* asks for
`ae2:growth_accelerator` and is about speeding Budding Crystal growth. It is crystal supply,
not autocrafting, and this page does not list it as a step.

A minimal first AE2 autocraft is therefore steps 1–4 with stock in the cells: encode one
recipe onto a Pattern (2), place it in the provider from (1) with an Assembler from (3)
against it, give the network the CPU from (4), then request the product and watch it in the
monitor from (6). Multi-step recipes are the CPU's job — its text names *"interim items for
multi-step crafts"* explicitly. Which recipes to encode first is judgement (approximate:
start with whatever the player currently hand-crafts in stacks — processors and cables are
the book's own early examples), never a pack requirement.

### Processing patterns (both AE2 kinds)

**Patterns** (2) is the whole recipe: crafting patterns execute in a Molecular Assembler;
processing patterns send inputs *"into some other machine block or specialised processing
plant"* and the network expects the output back. Placement, piping, and return wiring for a
given machine are the quest entry's and JEI's business — this page does not tell you a
machine setup the config does not describe. For machines that need different inputs on
different faces, the addon answer is verified below (*Specific Sided Patterns: The Advanced
Pattern Provider*).

## Refined Storage: the network you need before the first autocraft

Shorter run-up, same shape — controller, storage, a Grid to look through:

| # | Verified quest title | Task items in the config | Why it comes first (quest text) |
|---|---|---|---|
| 1 | **Refined Storage** *(hub, subtitle Version 2)* | `refinedstorage:controller` | *"The Controller is the 'Core' of your storage network. When provided with power, it gives life to all RS components connected."* |
| 2 | *(no title in the config; subtitle Floppy Time!)* | `refinedstorage:disk_drive` | Holds the disks: *"These have 8 slots for Storage Disks"* |
| 3 | *(no title in the config)* | `refinedstorage:storage_housing` | Housing + Storage Part makes a Storage Disk, which *"is used to store your items virtually once placed inside of the Disk Drive"* |
| 4 | **Cables** *(subtitle Connecting the System)* | `refinedstorage:cable` | *"Early on, you can get by with placing blocks next to each other"*, Cables *"allow you to extend out"* |
| 5 | **The Grid** *(subtitle Don't go off the Grid)* | `refinedstorage:grid` | *"To access the system, you'll need to create a Grid"*; it can show *"Items, Fluids, Energy, Source, Souls, and Chemicals"* (quest text) |
| 6 | **The Better Grid** | `refinedstorage:crafting_grid` | The Crafting Grid adds the manual crafting interface (not autocrafting — see the lookalikes note above) |

Storage-part tiers, wireless access, and import/export blocks all hang off this spine as
their own quests; none of them is a prerequisite the config sets for the Autocrafter chain
below beyond **The Grid** itself.

## Refined Storage: the autocrafting chain, in dependency order

| # | Verified quest title | Task items in the config | Needs | What the quest text says it does |
|---|---|---|---|---|
| 1 | **Autocrafting** *(subtitle Follow the Pattern)* | `refinedstorage:pattern` | The Grid | *"Patterns are the bread and butter of autocrafting. These store recipes to let your RS network know how to craft items."* |
| 2 | **Pattern Grid** | `refinedstorage:pattern_grid` | Autocrafting | *"allows you to imprint recipes onto Patterns"*; the book's method is JEI's `+` button into the grid, a blank Pattern in the top slot, then the arrow to imprint — *"You'll then want to put the Pattern into an Autocrafter!"* |
| 3 | **Autocrafter** *(subtitle Automated crafting!)* | `refinedstorage:autocrafter` | Pattern Grid | *"The Autocrafter is how we store Patterns for our network to know how to craft items"*; request by *"pressing Control + Shift whilst clicking on the item you have a recipe for"* in the Grid (quest text) |
| 4 | **Monitoring Autocrafting** | `refinedstorage:autocrafting_monitor` | Pattern Grid | *"allows you to see what items are currently in your crafting queue"* — *"if you want to be able to cancel crafts that aren't working or are bugged"* |
| 5 | **Managing Autocrafters** | `refinedstorage:autocrafter_manager` | Autocrafter | *"allows you to access all your Autocrafters from one block"* (the book spells the block "Autocrafer Manager" in its description; the task item is `refinedstorage:autocrafter_manager`) |
| 6 | *(no title in the config)* | `refinedstorage:wireless_autocrafting_monitor` | Wireless Access + Monitoring Autocrafting | *"Allows you to access your network crafting queue wirelessly."* |

The return path for machine crafts is its own untitled quest off **Cables**:
`refinedstorage:importer` — *"you can use these on Furnaces to pull the finished product out
into your system."* That is exactly the loop the Autocrafter text describes.

### Processing patterns and the faster Autocrafters

The Autocrafter text gives the processing pattern directly, quoted: *"if you point the
Autocrafter at a Furnace, you can put a recipe inside for a recipe you need a Furnace for,
like smelting Raw Processors. As long as the Autocrafter is attached to your system and the
Furnace has an Importer attached to it, the Crafter will allow you to request the smelted
version of the Processor!"* Raw Processors are the quest's example, not a required first
recipe; any other machine's wiring is the quest entry and JEI, not this page.

Speed and capacity then scale through the Cable Tiers line (Cable Tiers 1.21.1-0.6.14) —
slot counts and speed multipliers are quest text, quoted:

| Verified quest title | Task item | Quest text |
|---|---|---|
| *(no title in the config)* | `cabletiers:elite_autocrafter` | *"has 18 Pattern slots and works 2x faster"* |
| **Ultra Autocrafter** | `cabletiers:ultra_autocrafter` | *"has 36 Pattern slots, works 5x faster, and has a Stack Upgrade integrated"* |
| **Mega Autocrafter** | `cabletiers:mega_autocrafter` | *"has 54 Pattern slots, works 8x faster, and has a Stack Upgrade integrated"* |

The chapter's general speed quests apply to crafters too: **Speeding Everything Up!** covers
the Speed Upgrade (*"Want your crafters to work faster? This is the upgrade!"*) and the Stack
Upgrade. No base-Autocrafter slot count is stated in the config, so none is printed here.

A minimal first RS autocraft is steps 1–3 with stock in the disks: imprint one recipe in the
Pattern Grid (2), put the Pattern in the Autocrafter (3), then Control+Shift-click the
product in the Grid and confirm it in the monitor (4). No CPU, assembler, or channel step
exists in this chapter's chain — that absence is verified from the dependency links above,
not a claim that RS has no limits anywhere; read the quest entries for the rest.

## Extended & Advanced AE: the later AE2 scale-up (optional)

Nothing in this section is needed for a first autocraft. It is the pack's answer once one
provider and one Assembler stop keeping up, and every line below still runs on the AE2
network above. The chapter opens at its hub **Extended & Advanced AE** (`ae2:fluix_crystal`),
then forks: **ExtendedAE** (`ae2:fluix_block`) toward Entro Crystals, and **Advanced AE**
(`ae2:logic_processor`) toward the Quantum line. The gateway machine for the Extended
devices is **Complex Crafter: The Crystal Assembler** (`extendedae:crystal_assembler`), behind
**The Crystals of Space and Time: Entro Crystals** (`extendedae:entro_seed`,
`extendedae:entro_crystal`): *"To make all these ExtendedAE devices, a Crafting Table's
hammer and pliers won't cut it."*

| Verified quest title | Task items in the config | What the quest text says it does |
|---|---|---|
| **Faster and Bigger: Extended Devices** | `ftbfiltersystem:smart_filter` for any Extended device, including `extendedae:ex_pattern_provider` (task title *Extended Devices*) | *"The Extended Pattern Provider has 36 pattern slots, 4 times as many as an ordinary Pattern Provider"*; Extended buses *"work about 8x faster"* (quest text) |
| **Many Assemblers In One: The Assembler Matrix** *(subtitle Many Molecular Assemblers and Pattern Providers in One Channel)* | `extendedae:assembler_matrix_frame` ×43; wall/glass (`extendedae:assembler_matrix_wall` or `extendedae:assembler_matrix_glass`) ×125 | *"a multiblock that can effectively contain multiple Molecular Assemblers and Pattern Providers, all in one channel"*; *"at least a 3x3x3 cuboid and up to a 7x7x7 cuboid"*, *"completely filled and can't be hollow"*, *"at least one pattern core and craft core"*; the quest gives 25 frames and 25 walls toward its own example (quest text) |
| **Assembler Matrix Cores** | `extendedae:assembler_matrix_pattern` ×35, `extendedae:assembler_matrix_crafter` ×35, `extendedae:assembler_matrix_speed` ×5 | *"Pattern Cores add 36 pattern slots"*, *"Craft Cores add 8 maximum parallel crafting jobs"*, Speed Cores work like an Acceleration Card and *"more than 5 Speed Cores does not have an effect"* (quest text) |
| **Specific Sided Patterns: The Advanced Pattern Provider** *(subtitle Looking at you, Mekanism)* | `ftbfiltersystem:smart_filter` filtered to `item_tag(advanced_ae:adv_pattern_provider)` (task title *Advanced Pattern Providers*); `advanced_ae:adv_pattern_encoder` | Configure *"the face to which any individual item in a pattern is sent to"*, *"such as with the Metallurgic Infuser from Mekanism"* — *"with a single block and no pipes or a subnet"* (quest text) |
| **Better Pattern Access: The Extended Pattern Access Terminal** | `extendedae:ex_pattern_access_part` | The Pattern Access Terminal plus pattern search, pattern highlight, and a *"Pattern Provider In-World Highlight"* for finding *"which of your Pattern Providers are stuck"* (quest text) |
| **Quantum Ingredients** | `advanced_ae:shattered_singularity`, `advanced_ae:quantum_alloy`, `advanced_ae:quantum_processor` | *"Some ingredients you'll need to make the Quantum Computer, Crafter, and Armor."* (how each is made: the quest entry and JEI — not reproduced here) |
| **Infinite Crafting Jobs: The Quantum Computer** | `advanced_ae:quantum_unit`, `advanced_ae:quantum_structure` | *"capable of running unlimited crafting jobs, and sharing co-processing threads among them"*; a cuboid *"of at least 3x3x3 size and up to 7x7x7"*, or one Core alone; *"Exactly one Quantum Computer Core"*, glass outside only, no empty spaces (quest text) |
| **Massive Crafting Storage: The Quantum Computer Storage** | `advanced_ae:quantum_storage_128` ×2, `advanced_ae:quantum_storage_256` | *"expand the crafting storage of the Quantum Core"* and are *"required to make a Quantum Computer Core"* |
| **Co-Processing Oblivion: Quantum Computer Accelerator** | `advanced_ae:quantum_accelerator` | *"add 12 co-processing threads each"*; *"all crafting jobs being run by the Quantum Computer are able to share all co-processors"* (quest text) |
| **Heart of the Crafts: Quantum Computer Core** | `advanced_ae:quantum_core` | *"It has 256M crafting storage and 12 co-processing threads by itself"* and *"is also the only block capable of forming a Quantum Computer by itself"* (quest text) |
| **Co-Processing To Infinity: Quantum Computer Multi-Threader** | `advanced_ae:quantum_multi_threader` | *"multiplies co-processing threads in the Quantum Computer Multiblock by 6"*; only one per multiblock; *"It is also an ingredient for the ATM Star."* |
| **Fully Automated Crafting: The Quantum Crafter** | `advanced_ae:quantum_crafter` | A keep-stock auto-crafter: *"You can also regulate how much of each ingredient you want to keep, and up to how many of the product you want to keep in stock"*; *"Won't accept crafting requests from Pattern Providers, though."* (quest text) |
| **The Ultimate Quantum Computer** | `advanced_ae:quantum_structure` ×200, `advanced_ae:quantum_accelerator` ×100, plus Core and Multi-Threader | The book's maximal example: *"218 Quantum Computer Structural Glass, 123 Quantum Computer Accelerators"* for *"a total of 8928 co-processing threads"* (the author's own figures, quoted as quest text) |

Two naming traps the config itself creates, flagged rather than smoothed over: the Advanced
Pattern Provider quest's task is titled *Advanced Pattern Providers* while the quest is
*Specific Sided Patterns: The Advanced Pattern Provider* — both are quoted as they are; and
the Advanced AE line's earlier quest is titled *Reaction Efficency: The Reaction Chamber*
(spelled that way in the config), on the path to **Quantum Ingredients**. When a player says
"the quantum crafter", confirm whether he means the Quantum Computer (a crafting CPU) or
*Fully Automated Crafting: The Quantum Crafter* (the keep-stock block) — the book uses both
names for different quests.

When any of this is worth building is judgement (approximate: when single-Assemblers queue,
when one 9-pattern provider fills, or when a star-scale job needs the threads). The ATM Star
line draws on this chapter directly — the star checklist's Quantum Computer Multi-Threader
and related entries are in `references/atm-star-checklist.md`.

## A first autocraft, end to end

1. **Finish the prerequisite run** for the chosen system (AE2 steps 1–13 or RS steps 1–6
   above) until the terminal/Grid shows the stock the recipe will consume.
2. **Encode one simple recipe** — AE2: **Patterns** onto `ae2:blank_pattern` at
   `ae2:pattern_encoding_terminal`; RS: **Pattern Grid** at `refinedstorage:pattern_grid`
   onto `refinedstorage:pattern`. Pick something currently hand-crafted in batches
   (judgement; the books' own examples are processors and cables).
3. **Install the Pattern** — AE2: into the Pattern Provider from *Auto-Crafting* with a
   Molecular Assembler against it, and the crafting CPU from the *Download more RAM* quest
   built as its solid cuboid; RS: into the Autocrafter from *Autocrafter*.
4. **Request a small amount first** — RS: Control+Shift-click the product in the Grid (quest
   text); AE2: request it from the network and watch the Crafting Monitor line. Small first
   requests are judgement (approximate) — they make a missing intermediate recipe visible
   before it eats the stockpile.
5. **Watch it land, then scale the recipe set** — one Pattern per recipe, more providers /
   Autocrafters (or the Extended line) as the pattern count grows. Keep-stock automation
   (AE2 **ME Level Emitter** + the Crafting Card quest; Advanced AE's Quantum Crafter) comes
   after on-request crafting works, in the books' dependency order, not before.

## When it stalls

Only the checks the quests themselves support are listed; the rest is the quest entry, the
mod's in-game guidance, and JEI:

- **Nothing to request.** The Pattern is not encoded or not installed: AE2 *Patterns* and the
  Pattern Access Terminal (*Auto-Crafting*) show where patterns live; RS *Pattern Grid* shows
  the imprint step. An unencoded blank Pattern crafts nothing.
- **Request starts, never finishes.** AE2: read the Crafting Monitor quest line (what is
  still being crafted) and check the CPU exists (the *Download more RAM* quest — no CPU, no
  job) and that Assemblers front the providers holding the patterns. RS: open *Monitoring
  Autocrafting* — its stated purpose is cancelling *"crafts that aren't working or are
  bugged"*. For a stuck provider at scale, the Extended Pattern Access Terminal's in-world
  highlight (quest text) exists for exactly that hunt.
- **A machine step never returns its output.** Processing patterns only send inputs out.
  RS states the return half explicitly (an Importer on the machine, *Autocrafter* quest
  text); AE2's *Patterns* text sends inputs *"into some other machine"* without naming a
  return block on this page — check that quest entry and JEI for the machine's setup rather
  than assuming a part this page has not verified.
- **The network itself is dark or full.** AE2 power and channels are the *Plug in* and
  *Foreword on Channels* quests (8-channel ad-hoc limit; controller for more); storage
  fullness is *The Storage* / RS disk quests. Exact draw and channel bookkeeping beyond
  those quoted figures: the quest entries and JEI.

Anything beyond this list — a specific machine's sides, a fluid step, a recipe substitution —
is not verified here (approximate at best): open the quest, check JEI, and trust the book
over this page.

## Cross-references

- `references/progression.md` — where the Storage group sits in the four-stage map and why
  AE2 *or* Refined Storage is a choice, not a sequence.
- `references/key-mods.md` — what AE2, Refined Storage, and their addons do at primer level.
- `references/getting-started.md` — the Basic Storage step that comes before either network.
- `references/atm-star-checklist.md` — the Chapter 3 components this setup later feeds,
  including its AE2 hub line and the Quantum Computer Multi-Threader.
- `references/creative-checklist.md` — Chapter 4's post-star automation, which assumes
  autocrafting already works.

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item above is a quest *task*; JEI has the recipe, and recipes
  are where pack versions differ most. That includes the Quantum Ingredients descriptions,
  which do describe production in the book — this page still does not tell you those steps.
- **Build layouts beyond the quoted quest text.** Cuboid rules, channel counts, slot counts,
  and thread counts appear only as attributed quest text above. Hatch layouts, cable routing
  for a specific base, and machine-side wiring for a named machine: the quest entry and JEI.
- **An order the book does not have.** The chains are in dependency order from the config's
  `dependencies` lists; sibling spokes (the three chain quests directly off *Auto-Crafting*,
  the RS tier line) have no book order between them. Anything beyond that order is
  approximate.
- **A "best" system.** The comparison table is limited to what the two chapters verify;
  which one a player should main is judgement, flagged as such where this page offers it.
- **Anything not in the config.** If a player names a crafter, upgrade, pattern type, or
  count that is not listed here, the answer is "open that quest in the book / look it up in
  JEI" — never a guess.
st in the book / look it up in
  JEI" — never a guess.
