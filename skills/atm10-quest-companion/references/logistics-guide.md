# The logistics guide: moving items, fluids, gases, and energy (verified titles)

**What this page is.** The logistics and routing map for **All the Mods 10**: the four
chapters the quest book files under its **Logistics** group (**Basic Logistics**,
**Integrated Dynamics**, **Modular Routers**, **Pylons**), plus the cross-referenced
transport lines in **Mekanism** and **Basic Power**. It answers *"how do I move items,
fluids, gases, and power between machines and chests?"*, *"Pipez vs LaserIO vs Mekanism
transporters vs Integrated Dynamics vs Modular Routers — which should I use?"*, *"why
won't my Mekanism machine output into a pipe?"*, and *"how do Pipez upgrades, LaserIO
cards, or Modular Router modules work?"* It is a *map of the chapters and their rules*,
not a crafting guide and not a factory layout book.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, quest id, task item, count, dependency link, `optional` flag,
and quoted sentence below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** (`config/bcc-common.toml` carries
`modpackVersion = "8.2"`) — the `"8.x"` stamp in `examples/progress.example.json`:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapter_groups.snbt` | the **Logistics** group (`3D4E23B1100491AB`), fourth of the book's ten groups |
| `config/ftbquests/quests/chapters/basic_logistics.snbt` | **Basic Logistics**: 40 quests (44 tasks), Pipez, Mekanism pipes preview, Integrated Dynamics preview, LaserIO, and Transfer Labels |
| `config/ftbquests/quests/chapters/integrated_dynamics.snbt` | **Integrated Dynamics**: 28 quests (29 tasks), Menril processing, Logic Cables, Variable Cards, Tunnels, Logic Programmer, and autocrafting |
| `config/ftbquests/quests/chapters/modular_router.snbt` | **Modular Routers**: 55 quests (60 tasks), the router, upgrades, augments, modules, filters, and farm/mining/mob builds |
| `config/ftbquests/quests/chapters/pylons.snbt` | **Pylons**: 13 quests (14 tasks), the five area-utility pylons and their filters |
| `config/ftbquests/quests/chapters/mekanism.snbt` and `basic_power.snbt` | Mekanism's full logistics tree (tier rates, Configurator modes, Side Configs, *Quantum Entangloporters*) and Basic Power's *Transferring Power* hub (*Flux Networks*) |
| `config/ftbquests/quests/chapters/chapter_2_the_star.snbt` | Chapter 3 cross-check: zero ATM Star tasks require items from `pipez`, `laserio`, `integrateddynamics`, `integratedtunnels`, `modularrouters`, `pylons`, or `transfer_labels` |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, and description text quoted below (Minecraft `&` and hex `&#RRGGBB` formatting codes stripped) |
| `config/ftbquests/quests/lang/en_us/chapter.snbt`, `chapter_group.snbt` | the four chapter titles and the group title `Logistics` |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (493 entries) |

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Titles and item ids are the config's, never invented.** Across the four
  Logistics-group chapters, **31 of the 136 quests** carry an explicit title in the lang
  files; the other **105** do not, and the book then displays the task item's own name.
  Untitled quests are marked *(no title in the config)* below with their quest id and task
  item — never present a derived name as a verified quest title.
- **No recipes, no coordinates, no unquoted transfer rates.** The config lists *what a
  quest wants* and what its own text says — never a crafting grid or an unquoted throughput
  table. Every rate or cap on this page is a direct quote from quest text or subtitle,
  attributed as such; send recipes and unquoted numbers to JEI and the quest entry.
- **Every number or lag claim in quotation marks is quest text, not a benchmark.** When a
  quest says *"Over 2 Billion"*, *"8 items per Operation"*, or *"Least laggy pipe
  solution"*, repeat it as what the quest book says at pack 8.2.
- **Where two quests in the same chapter disagree, print both.** In `basic_logistics`, the
  Pipez upgrades quest (`6A962535CD68713E`) says the **Basic Upgrade** lets you add
  filters, while the destination-tool quest (`2A976D41F79C34B1`) says *"you need atleast an
  Advanced Upgrade to get it though"*. Both quotes are printed below rather than smoothed
  over; the in-game pipe GUI settles which upgrade unlocks which filter slot.
- **Alternatives stay alternatives, and picks are marked *(judgement)*.** The pack gates
  nothing: its Welcome chapter says *"In this modpack, quests are optional. Mods are not
  gated behind completing any quests!"* And unlike the Storage group (where Chapter 3's
  storage tasks are all AE2-family), `chapter_2_the_star.snbt` has **zero** tasks from any
  Logistics-group mod — your choice of pipes never gates the ATM Star.

## The short answer — which logistics mod when *(judgement)*

The pack ships several overlapping transport mods on purpose. Because none of them gates
the ATM Star, pick the simplest tool that fits the job *(judgement — approximate trade-offs
distilled from the quest descriptions below)*:

1. **First lines (early-game, cheapest setup): Pipez** (`pipez` `1.21.1-1.2.31`, in
   **Basic Logistics**). One pipe type per resource (**Item Pipez**, **Fluid Pipez**,
   **Energy Pipez**, **Gas Pipez**) plus **Universal Pipez** for items + fluids + energy;
   shift-right-click the extracting end with a wrench (`pipez:wrench`). Its own quest text
   calls it *"the simplest Logistics Mod"* and warns *"(Can be laggy when used in mass,
   still not as laggy as Mekanism pipes though)."*
2. **Tight multi-side machine setups (one block, many resources): LaserIO** (`laserio`
   `1.9.11`, in **Basic Logistics**). One `laserio:laser_node` can push and pull items,
   fluids, energy, redstone, and Mekanism chemicals on any of its six faces at the same
   time using directional cards (**Item Card**, **Fluid Card**, **Energy Card**,
   **Redstone Card**, **Chemical Card**).
3. **Zero-block gap between touching machines: Transfer Labels** (`transfer_labels`
   `0.1.9`, in **Basic Logistics**). Sneak-right-click a label onto a block face to move
   items or fluids between adjacent blocks without placing a pipe block at all.
4. **Inside a Mekanism line (or for Mekanism Heat and wireless everything): Mekanism**
   (`Mekanism` `10.7.19`, in **Basic Logistics** and **Mekanism**). **Pressurized Tubes**
   (or **Gas Pipez** / LaserIO's **Chemical Card**) move Mekanism gases, infuse types,
   slurries, and pigments; **Thermodynamic Conductors** move Heat; **Quantum
   Entangloporters** move items, fluids, chemicals, heat, and energy wirelessly. Remember
   the quest book's #1 Mekanism rule: set the machine's GUI **Side Configs** and turn
   **Auto-Eject** on, or use `mekanism:configurator` on the pipe.
5. **High-rate / low-lag cable networks: Integrated Dynamics + Integrated Tunnels**
   (`integrateddynamics` `1.37.1`, `integratedtunnels` `1.12.0`, in **Basic Logistics**
   and **Integrated Dynamics**). Its quest in **Basic Logistics** calls it *"(Least laggy
   pipe solution, these are recommended)"* because **Logic Cables** *"skip the middle man"*
   between **Importers**/**Exporters** and **Interfaces**, and its importer quests note a
   configurable rate up to *"the Integer Limit (Over 2 Billion)"*.
6. **Wireless single-block routing and in-world actions (mob farms, crop farms, block
   breaking/placing): Modular Routers** (`modularrouters` `13.2.7`, in **Modular
   Routers**). One `modularrouters:modular_router` pulls, sends (up to cross-dimensional
   with `modularrouters:sender_module_3`), vacuums drops, voids trash, places blocks, or
   breaks blocks with no pipes between the router and the target.

## The Logistics group at a glance

The **Logistics** group (`3D4E23B1100491AB`) is the fourth of ten groups in
`config/ftbquests/quests/chapter_groups.snbt`. It holds **4 chapters**, **136 quests**
(**31 titled**, **105 untitled**, **14 optional**), and **147 tasks** (**135 `item`**,
**12 `checkmark`**, zero other task types). Each chapter includes one hidden, optional
2-checkmark staff-attribution quest (`230582AAFC0A1632`, `6ABDBE41880CFDA9`,
`2BB5769119BA2472`, `5E02AE661945306C`) that says *"This quest is intentionally hidden, if
you're seeing this, you're in editing mode."*

| `order_index` | Chapter title (config filename) | Chapter id | `progression_mode` | Quests (tasks) | Titled / untitled | Optional | Skill stage (`progress.example.json`) | What it covers |
|---|---|---|---|---|---|---|---|---|
| 0 | **Basic Logistics** (`basic_logistics`) | `3DEB33F78398EAD6` | default (omitted) | **40** (44) | 19 / 21 | 6 | `early-game` | **Logistics** hub, **Pipez** (8 quests), **Mekanism** pipes overview (6), **Integrated Dynamics** overview (6), **Laser IO** (17), **Transfer Labels** (1), hidden quest (1) |
| 1 | **Integrated Dynamics** (`integrated_dynamics`) | `69299302373C4CBC` | default (omitted) | **28** (29) | 4 / 24 | 6 | `tech` | Menril tree & resin processing, **Logic Cables**, **Variable Cards**, Interfaces/Importers/Exporters, Logic Programmer, Crafting Interface, Energy Battery |
| 2 | **Modular Routers** (`modular_router`) | `0AB4F9AED808DE48` | `"flexible"` | **55** (60) | 7 / 48 | 1 | `tech` | **Modular Routers**, **Upgrades** (9), **Augments** (11), **Modules** (21 + 1 checkmark), filters (5), and **Routers for Mob Farms / Mining / Farming** |
| 3 | **Pylons** (`pylons`) | `5712300EF4E5E846` | default (omitted) | **13** (14) | 1 / 12 | 1 | `tech` | **Pylons** root (`minecraft:polished_blackstone`) plus the 5 area pylons (Expulsion, Interdiction, Harvester, Infusion, Protection) and their 6 filter/hoe quests |

## Chapter 1 of the group — Basic Logistics (`basic_logistics`, 40 quests)

The chapter's root-concept quest is **Logistics** (`6CD7D99AA102A5C3`, no dependencies,
task: smart filter on tag `c:tools/wrench`), which defines the role of the whole group:

> *"Logistics: A system of moving, managing, and storing items or resources. In Modded
> Minecraft it's quite the same, moving items! With Modded you will need items and by the
> thousands, heck if you want the Star it gets in the millions! So you'll need to move
> items from factories, machines, farms, and especially chests. That's what Logistics is
> for."*

Six quests in `basic_logistics` have no dependencies: **Logistics** (`6CD7D99AA102A5C3`),
**Pipez** (`2329AA0AFBEF1E13`), **Mekanism** (`34CFE1439262AA72`), **Integrated Dynamics**
(`6E05B62A40D5A891`), **Laser IO** (`5F1218CF8EFC607B`), **Transfer Labels**
(`6CD60A9D88227005`), plus the hidden authorship quest (`230582AAFC0A1632`).

### 1a. Pipez (`pipez` `1.21.1-1.2.31` — 8 quests in `basic_logistics`)

All seven children depend directly on **Pipez** (`2329AA0AFBEF1E13`), except **Universal
Pipez** (`4FBAB3A0FBF8CE2F`), which depends on **Item Pipez**, **Fluid Pipez**, and
**Energy Pipez**:

| Verified quest title | Quest id | Task item(s) | Depends on | What the quest text says |
|---|---|---|---|---|
| **Pipez** | `2329AA0AFBEF1E13` | `pipez:wrench` | — | *"Pipez is the simplest Logistics Mod."* … *"Attach the specific Pipe to where you want to move items and use the Pipe Wrench to configure what side Pulls, Pushes, or doesn't connect. Other Wrenches do work with Pipez as well! (Can be laggy when used in mass, still not as laggy as Mekanism pipes though)."* |
| **Item Pipez** | `36836AD948F96B9F` | `pipez:item_pipe` | `2329AA0AFBEF1E13` | *"The simplest of the simplest of Pipes, the Item Pipe. It will move Items from one Inventory to another. Could be from one Chest to another, could be a Farm to a System, or even a Quarry to a Smelter."* |
| **Fluid Pipez** | `33433A443B65D252` | `pipez:fluid_pipe` | `2329AA0AFBEF1E13` | *"You'll most likely need to move those Fluids and a good way of doing so is with Fluid Pipes. This can be connected to Sinks to move Infinite Water!"* |
| **Energy Pipez** | `53EC96FA0E7C4ED4` | `pipez:energy_pipe` | `2329AA0AFBEF1E13` | *"Every Tech Mod needs Energy, whether it's FE, RF or something else! Energy Pipez don't discriminate, it just moves! Some Machines have strict IO ports for Energy so make sure to check for those!"* |
| **Gas Pipez** | `2F4458E9921DEB86` | `pipez:gas_pipe` | `2329AA0AFBEF1E13` | *"These Pipez are mostly due to Mekanism. Mekanism adds the last state of matter in the form of Gas. Gas can't be moved with any of the other Pipez so if you need to move Hydrogen or Lithium you'll need Gas Pipez."* |
| **Universal Pipez** | `4FBAB3A0FBF8CE2F` | `pipez:universal_pipe` | `33433A443B65D252`, `36836AD948F96B9F`, `53EC96FA0E7C4ED4` | *"Why worry about what's being moved when you can just move everything! Universal Pipez are even less discriminatory than Energy Pipez. They can move Items, Fluids, or Energy."* |
| *(no title in the config)* | `6A962535CD68713E` | smart filter: `or(item(pipez:basic_upgrade)item(pipez:improved_upgrade)item(pipez:advanced_upgrade)item(pipez:ultimate_upgrade))` | `2329AA0AFBEF1E13` | *"All Upgrades increase the amount the Pipez move and also grant more options to use with the Pipe. Basic Upgrade allows Redstone Activation with Pipez, to change distribution either:Closest First, Farthest First, Round-Robin, or Random, and to add Filters. Improved, Advanced, and Ultimate upgrades don't grant anything new they just move more!"* |
| *(no title in the config)* | `2A976D41F79C34B1` | `pipez:filter_destination_tool` | `2329AA0AFBEF1E13` | *"Pipez do have their own way of Filtering Items, you need atleast an Advanced Upgrade to get it though. When an Advanced Upgrade is in you can click the Add button to add Filters. Then you can add: Item, Tag, or NBT in the Filter. There you can also add the set Destination Filter. To set it, Shift Right Click an Inventory with it. You'll also have to set it to either Whitelist the Filter or Blacklist, so only the Filter or everything but the Filter."* |

**Two config notes to keep straight:**

1. **What Universal Pipez moves:** the quest text for **Universal Pipez** (`4FBAB3A0FBF8CE2F`)
   names *"Items, Fluids, or Energy"*, whereas **Gas Pipez** (`2F4458E9921DEB86`) says
   *"Gas can't be moved with any of the other Pipez"* and Basic Power's **Pipez: Energy
   Pipes** (`4EEAB467C722ECE7`) calls Universal Pipe *"an All-In-One Pipe"*. Verify in-game
   whether your pack version's Universal Pipe moves Mekanism gas or requires `pipez:gas_pipe`.
2. **Which Pipez upgrade unlocks filtering:** the two untitled Pipez quests disagree inside
   the same chapter — `6A962535CD68713E` says **Basic Upgrade** unlocks Redstone mode,
   distribution modes (*Closest First*, *Farthest First*, *Round-Robin*, *Random*), and
   Filters, while `2A976D41F79C34B1` says *"you need atleast an Advanced Upgrade to get it
   though"*. Check the upgrade tooltip and pipe GUI in-game; the game wins.

### 1b. Mekanism pipes in `basic_logistics` (6 quests) and `mekanism` (7 quests)

**Basic Logistics** opens its Mekanism branch with **Mekanism** (`34CFE1439262AA72`, task
`mekanism:configurator`) and five untitled smart-filter quests (one per pipe family, each
accepting `basic_`, `advanced_`, `elite_`, or `ultimate_`). The **Mekanism** chapter
(`mekanism`, 90 quests, stage `tech`) carries the corresponding titled quests with the
author's per-tier numbers:

| Family (subtitle in `basic_logistics`) | `basic_logistics` quest id (all 5 children are *(no title in the config)*) | `mekanism` titled quest (quest id) | Four tier item ids (`mekanism:*`) | Quoted capacities and rates from `mekanism.snbt` (quest text — verify in-game) |
|---|---|---|---|---|
| **Configurator** (hub) | **Mekanism** (`34CFE1439262AA72`, titled) | **Mekanism Logistics** (`5E116409DC7D30BB`, subtitle *The Configurator*) | `mekanism:configurator` | *"By Holding Shift and Scrolling you can change the Mode of the Configurator. Wrench: will Drop Mekanism Machines and Blocks when used on them. Rotate: will simply Rotate the direction of the Block. Empty: will make it work like a Gauge Dropper. The rest of them will make the Configurator interact with Machines to change their Configs! If you use it on Pipes it will change if they Push, Pull, or Both."* |
| *Blocks+Items* | `30DE4F5BC3EDB555` | **Logistical Transporters** (`60ECCCAB66AAC05D`, subtitle *Items*) | `basic_logistical_transporter`, `advanced_logistical_transporter`, `elite_logistical_transporter`, `ultimate_logistical_transporter` | *"Basic: will move 2 Blocks/Items across 1 Block each Second. Advanced: will move 32 Blocks/Items across 2 Blocks each Second. Elite: will move a stack of Items or Blocks across 4 Blocks each Second. Ultimate: will move 2 stacks of Items or Blocks across 10 Blocks each Second."* |
| *Fluids* | `1834B5C1F8435D7A` | **Mechanical Pipes** (`33C69B5934BE4D64`, subtitle *Fluids*) | `basic_mechanical_pipe`, `advanced_mechanical_pipe`, `elite_mechanical_pipe`, `ultimate_mechanical_pipe` | *"Basic: will hold 2 Buckets of Fluids and move 250mB of Fluid each Tick. Advanced: will hold 8 Buckets of Fluids and move a Bucket of Fluid each Tick. Elite: will hold 32 Buckets of Fluid and will move 8 Buckets each Tick. Ultimate: will hold 128 Buckets and will move 32 Buckets each Tick."* |
| *Gas+More* | `4BC2D7FCDD792DBA` | **Pressurized Tubes** (`3AF1DC02E9A0010C`, subtitle *Chemicals, Pigments, Infuse Types*) | `basic_pressurized_tube`, `advanced_pressurized_tube`, `elite_pressurized_tube`, `ultimate_pressurized_tube` | Moves *"Gases"*, *"Infuse Types"*, *"Slurries"*, and *"Dye Pigments"*. *"Basic: will hold 4 Buckets of Chemicals and move 750mB of Chemicals each Tick. Advanced: will hold 16 Buckets of Chemicals and move 2 Buckets of Chemicals each Tick. Elite: will hold 256 Buckets of Chemicals and will move 64 Buckets each Tick. Ultimate: will hold 1,024 Buckets and will move 256 Buckets each Tick."* |
| *Heat* | `316B513FE568EF57` | **Thermodynamic Conductors** (`66A450CAC07232E1`, subtitle *Heat*) | `basic_thermodynamic_conductor`, `advanced_thermodynamic_conductor`, `elite_thermodynamic_conductor`, `ultimate_thermodynamic_conductor` | *"Thermal Evaporation Plants and Fusion Reactors both use Heat to work. And Conductors is how you will be moving Heat!"* (*"I'm not sure what these numbers mean but following the pattern: more expensive, more good!"*) |
| *Energy* | `493D04D954E4FBA0` | **Universal Cables** (`62827AA1AD29A222`) and Basic Power's **Mekanism: Universal Cables** (`5C47935A3B2877FF`) | `basic_universal_cable`, `advanced_universal_cable`, `elite_universal_cable`, `ultimate_universal_cable` | *"Basic: will hold and move 3.2kFE per Tick. Advanced: will hold and move 51.2kFE per Tick. Elite: will hold and move 409.6kFE per Tick. Ultimate: will hold and move 3.27mFE per Tick."* |

**Why won't my Mekanism machine output into a pipe?** Both **Mekanism** (`34CFE1439262AA72`)
and **Logistical Transporters** / **Pressurized Tubes** state the exact fix: *"The
different Machines are picky with Configurations and will need to be changed in their GUI
to properly move items"* — open the machine's GUI, click **Side Configs** in the top left,
assign the output face, and toggle **Auto-Eject** on (or use the `mekanism:configurator` on
the pipe connection to set it to Pull).

**Wireless Mekanism transport:** **Quantum Entangloporters** (`7CC49360D07086B8` in
`mekanism`, subtitle *Wireless Power, Gases, Fluids, Everything.*, and **Mekanism: Quantum
Entangloporter** `7FE969CB4B419FC6` in `basic_power`, task
`mekanism:quantum_entangloporter`) — *"With 2 Quantum Entangloporters we can Wirelessly
move Items, Fluids, Chemicals, Heat, and Energy!"* Type a network name, click the checkmark
button, select that channel on the second block, and configure **Side Configs** +
**Auto-Eject**.

### 1c. LaserIO (`laserio` `1.9.11` — 17 quests in `basic_logistics`)

Root quest **Laser IO** (`5F1218CF8EFC607B`, task `laserio:logic_chip`, no dependencies)
introduces the mod: *"LaserIO is DireWolf's continuation of EnderIO's Logistics. It's all
about moving items via Lasers! … And it all starts with the Logic Chip."*

| Verified quest title | Quest id | Task item | `optional` | Depends on | Subtitle / what the quest text says |
|---|---|---|---|---|---|
| **Laser IO** | `5F1218CF8EFC607B` | `laserio:logic_chip` | no | — | Root quest for the LaserIO tree |
| *(no title in the config)* | `7BC8F50A89A3BE1A` | `laserio:laser_wrench` | no | `5F1218CF8EFC607B` | *"used to Connect Laser Nodes to each other and to Connectors."* |
| *(no title in the config)* | `5C0F6B1C93A52113` | `laserio:laser_node` | no | `5F1218CF8EFC607B` | *"The Laser Nodes are where the actual Cards will go into in order to work. They will move Items from any adjacent Inventory in the 4 Cardinal Directions and Up and Down. In order to move to Farther Inventories you'll need a second Node and Connect them with the Wrench by Shift Right Clicking 1 and Right Clicking the 2nd."* |
| *(no title in the config)* | `7EE27C3908008E20` | `laserio:laser_connector` | **yes** | `5C0F6B1C93A52113` | *"If you need to string your Laser Nodes a far distance try using Connectors! Just use the Wrench like normal."* |
| **Item Card** | `4C41FD926F31180B` | `laserio:card_item` | no | `5F1218CF8EFC607B` | *"Set one to Extract and put it on the side of the Laser Node you want to Import from. Then set the other to Insert and put it to the side you want the Items to Export to."* Supports Round Robin extraction. |
| **Fluid Card** | `1C70D739CE464E25` | `laserio:card_fluid` | no | `5F1218CF8EFC607B` | *"you need Extract and Insert Cards. Just this time you take from Tanks holding Fluids to another Tank. No, it doesn't move Sources of Fluid in or out of the World."* |
| **Energy Card** | `52F85CED20C8B1E9` | `laserio:card_energy` | no | `5F1218CF8EFC607B` | *"Move it around just the same as with Items, Fluids, and Chemicals!"* |
| **Redstone Card** | `47768B1FFD57D56E` | `laserio:card_redstone` | no | `5F1218CF8EFC607B` | *"You can Input a Redstone Signal with the Card then use an Output Card to Output the Signal somewhere else!"* |
| **Chemical Card** | `6718043D0F2D1830` | `laserio:card_chemical` | no | `5F1218CF8EFC607B` | *"Everything Pressurized Tubes can move, these cards can. Gas, Infuse Types, and Pigments."* |
| *(no title in the config)* | `47A2BEFB11F4D581` | `laserio:filter_basic` | no | `5F1218CF8EFC607B` | Whitelist/blacklist and optional NBT matching (*"Enchantments, Durabilitiy, or even Mobs inside of whatever Item"*). |
| *(no title in the config)* | `06767BA0AFE8C1EE` | `laserio:filter_count` | no | `47A2BEFB11F4D581` | *"It will then wait until that set Number of Items is there to start taking Items. It will also leave that amount in the first Inventory."* |
| *(no title in the config)* | `3065EA195D0A36BA` | `laserio:filter_tag` | no | `47A2BEFB11F4D581` | Filter by item tag; notes `/kubejs hand` to inspect tags in hand. |
| *(no title in the config)* | `2A6900E87DE8BAE0` | `laserio:filter_mod` | no | `47A2BEFB11F4D581` | *"instead of only being that Item it will be any Item from that Mod."* |
| *(no title in the config)* | `046C417B2ADF3AA7` | `laserio:overclocker_card` | **yes** | `5F1218CF8EFC607B` | Subtitle: **Max: 4**. *"Item Extration can only extract 8 items per Operation. Fluid Extract at only 5 Buckets. … Throw some Overclockers in the top right of the Card and it'll upgrade the cap they can transfer!"* |
| *(no title in the config)* | `0BB562FB44B0AAA7` | `laserio:overclocker_node` | **yes** | `5F1218CF8EFC607B` | Subtitle: **Max: 8**. *"These go into the Node itself on bottom right and boost how fast it does Operations."* |
| *(no title in the config)* | `617695A9CA45D88F` | `laserio:card_holder` | **yes** | `5F1218CF8EFC607B` | *"when you open a Laser Node the Card Holder will open up as well like a second Inventory."* |
| *(no title in the config)* | `308935C85364B04D` | `laserio:card_cloner` | **yes** | `5F1218CF8EFC607B` | *"Left Click a Card with the Cloner to copy its Data, then Right Click a Card to give it that Data!"* |

### 1d. Transfer Labels (`transfer_labels` `0.1.9` — 1 quest in `basic_logistics`)

- **Transfer Labels** (`6CD60A9D88227005`, subtitle *When you gotta fit a pipe between your
  blocks*, task: smart filter `mod(transfer_labels)`, no dependencies) — *"Transfer Labels
  can be used for items and fluids. … You can place Labels on blocks by sneak right clicking
  onto blocks. You can interact with the Label by holding another Label or a Label Accessor
  and right clicking the placed Label. … You can accelerate the Labels by adding the same
  type of Label in the amount or speed slots."*

## Chapter 2 of the group — Integrated Dynamics (`integrated_dynamics`, 28 quests) + `basic_logistics` preview (6 quests)

The pack introduces Integrated Dynamics (`integrateddynamics` `1.37.1`) and its tunnel/UI
addons (`integratedtunnels` `1.12.0`, `integratedcrafting` `1.7.2`, `integratedterminals`
`1.10.0`, `integratedscripting` `1.0.27`) in two places: a 6-quest quick-start in **Basic
Logistics** and a full 28-quest chapter in **Integrated Dynamics**.

### 2a. The 6-quest preview in `basic_logistics`

1. **Integrated Dynamics** (`6E05B62A40D5A891`, task `integrateddynamics:wrench`, no
   dependencies) — *"(Least laggy pipe solution, these are recommended)."*
2. *(no title in the config)* (`6112956E19017D2D`, task `integrateddynamics:cable`, depends
   on `6E05B62A40D5A891`) — *"Logic Cables are different from other Pipez or Meka pipes.
   The other Pipes act as hoppers, the items move from 1 Inventory, into the Pipe, then
   into the 2nd Inventory. Logic Cables just skip the middle man which also skips a lotta
   lag. They are just for connecting Importers and Interfaces."*
3. *(no title in the config)* (`03C40D6A5D722543`, task `integrateddynamics:variable`,
   depends on `6E05B62A40D5A891`) — *"Variable Cards are necessary for starting
   Interactions like Importing Items. You will put them in one of the slots of the Importer
   to add them. From there you can edit everything via the + Button."*
4. **Item Importing** (`6F152402756DA35E`, tasks `integratedtunnels:part_importer_item` +
   `integratedtunnels:part_interface_item`, depends on `6112956E19017D2D` and
   `03C40D6A5D722543`) — *"put the Item Importer onto the Inventory you want Items pulled
   from. Next, put the Interface on the second Inventory and connect them with Logic
   Cables. Then, put in the Variable Card into the Importer and change it as you please. It
   can be changed to Import Items at the Integer Limit (Over 2 Billion)."*
5. **Fluid Importing** (`034F2CDF0830254B`, tasks `integratedtunnels:part_importer_fluid` +
   `integratedtunnels:part_interface_fluid`, same deps) — *"Also can pull Liquids at the
   Integer Limit. Does not place or take Fluid Sources from in the world, it only moves
   Fluids from one Tank to another."*
6. **Energy Importing** (`76CECFB244F39F18`, tasks `integratedtunnels:part_importer_energy`
   + `integratedtunnels:part_interface_energy`, same deps) — *"I do have to say I found it
   having problems with Importing or Exporting to Flux Plugs and Points so be mindful of
   that."*

### 2b. The full `integrated_dynamics` chapter (28 quests: 4 titled, 24 untitled, 6 optional)

Only four quests in `integrated_dynamics.snbt` carry a title in the lang file; the other 24
are *(no title in the config)* (several carry subtitles):

| Step in dependency order | Verified quest title | Quest id | Subtitle | Task item(s) / type | `optional` | Depends on | Key quest quote / role |
|---|---|---|---|---|---|---|---|
| 1 | **Integrated Dynamics** | `499CF9F39CED8899` | *Growing Menril* | smart filter: tag `integrateddynamics:menril_logs` | no | — | *"Menril trees can be found in Meneglin biomes."* |
| 2 | *(no title in the config)* | `6C9191DA4B1039D6` | — | `integrateddynamics:menril_berries` | no | `499CF9F39CED8899` | *"Menril Berries give you Night Vision for a short amount of time when eaten."* |
| 3 | *(no title in the config)* | `232A06C9FF0EE7B2` | *Automating Menril* | `mysticalagriculture:menril_seeds` | **yes** | `6C9191DA4B1039D6` | *"Menril Seeds can be used to automate Menril Berries, Menril Logs and Menril Saplings."* |
| 4 | *(no title in the config)* | `68498ADEF9765F81` | — | `integrateddynamics:squeezer` | no | `499CF9F39CED8899` | *"Jump on the Squeezer to turn them into Menril Resin. You can empty the Squeezer by giving it a Redstone signal."* |
| 5 | *(no title in the config)* | `62B4A37CFDECA679` | — | `integrateddynamics:drying_basin` | no | `68498ADEF9765F81` | *"After 7.5 seconds the Menril Resin will turn into a Block of Crystallized Menril."* |
| 6 | **Crystallized Menril Chunks** | `72F57D77C3FB366D` | *The Main Crafting Ingredient* | `integrateddynamics:crystalized_menril_chunk` | no | `62B4A37CFDECA679` | *"the main crafting ingredient of ID."* |
| 7 | *(no title in the config)* | `2F37E284BB83BFF6` | — | `integrateddynamics:wrench` | no | `72F57D77C3FB366D` | *"rotate or destroy certain blocks, shift right-click in the air to change modes."* |
| 8 | *(no title in the config)* | `3C9539083BCC145C` | *Automating Menril* | `productivebees:configurable_honeycomb` (`productivebees:menril`) | **yes** | `72F57D77C3FB366D` | *"Menril Bees can be used to automate Crystallized Menril Chunks."* |
| 9 | *(no title in the config)* | `6D75CF34957ECCD9` | *Storing Energy* | `integrateddynamics:energy_battery` | no | `72F57D77C3FB366D` | *"The Energy Battery lets you store FE. To transfer it, you will need Energy Interfaces."* |
| 10 | *(no title in the config)* | `4D62C62B523C69EC` | *Providing Energy!* | `integrateddynamics:coal_generator` | **yes** | `6D75CF34957ECCD9` | *"generates FE using burnable fuels like Coal."* |
| 11 | *(no title in the config)* | `44DA091B53473723` | — | `integrateddynamics:mechanical_squeezer` | **yes** | `6D75CF34957ECCD9`, `68498ADEF9765F81` | *"The Mechanical Squeezer uses energy to squeeze."* |
| 12 | *(no title in the config)* | `7413BB136EF9D6C5` | — | `integrateddynamics:mechanical_drying_basin` | **yes** | `6D75CF34957ECCD9`, `62B4A37CFDECA679` | *"The Mechanical Drying Basin uses energy to dry"* |
| 13 | **Logic Cables** | `4A05C037C0EE40BD` | *Making Networks* | `integrateddynamics:cable` | no | `72F57D77C3FB366D` | Connects Interfaces, Importers, and Exporters |
| 14 | **Variable Cards** | `79C1105A84B8BF8F` | — | `integrateddynamics:variable` | no | `4A05C037C0EE40BD` | Placed in Importer/Exporter slots to start transfer or filter |
| 15 | *(no title in the config)* | `450EDE68EC992A5A` | *Interfaces Have GUIs!* | smart filter: `part_interface_energy`, `part_interface_item`, `part_interface_fluid` (`integratedtunnels:*`) | no | `72F57D77C3FB366D` | *"Interfaces read whatever they're looking at. You can think of this like an AE2 Storage Bus."* |
| 16 | *(no title in the config)* | `3BC94B0B922C0708` | — | `integrateddynamics:variable_transformer_input` | no | `79C1105A84B8BF8F` | Crafting ingredient for importing parts |
| 17 | *(no title in the config)* | `6D9FA4DF842C1010` | — | `integrateddynamics:variable_transformer_output` | no | `79C1105A84B8BF8F` | Crafting ingredient for exporting parts |
| 18 | *(no title in the config)* | `73EA326304C01C3B` | *Importing* | smart filter: `part_importer_energy`, `part_importer_world_energy`, `part_importer_item`, `part_importer_world_item`, `part_importer_fluid`, `part_importer_world_fluid`, `part_importer_world_block` (`integratedtunnels:*`) | no | `3BC94B0B922C0708` | *"It can be changed to import things at the Integer Limit (Over 2 billion)."* |
| 19 | *(no title in the config)* | `33F4A7613764A016` | *Exporting* | smart filter: `part_exporter_energy`, `part_exporter_world_energy`, `part_exporter_item`, `part_exporter_world_item`, `part_exporter_fluid`, `part_exporter_world_fluid`, `part_exporter_world_block` (`integratedtunnels:*`) | no | `6D9FA4DF842C1010` | *"Works like Importers do, only they export instead."* |
| 20 | *(no title in the config)* | `65FA86357BC60573` | *Moving Stuff!* | `checkmark` | no | `73EA326304C01C3B`, `33F4A7613764A016`, `450EDE68EC992A5A` | 3-step summary: 1. Interface on inventory; 2. Importer/Exporter on other inventory; 3. Connect with Cables and insert a Variable Card |
| 21 | *(no title in the config)* | `1B5C86AE05678420` | — | `checkmark` | no | `65FA86357BC60573` | Explains Interface GUI: *Set Side*, *Ticks/Operation*, *Priority*, *Item/Energy Channels* |
| 22 | *(no title in the config)* | `437F4945AFBE0825` | — | `checkmark` | no | `65FA86357BC60573` | Explains Importer/Exporter GUI and the `"+"` button on inserted Variable Cards |
| 23 | *(no title in the config)* | `4D4152032F0410D2` | *Getting Advanced* | `integrateddynamics:logic_programmer` | no | `65FA86357BC60573` | *"The Logic Programmer lets you set the value of variables. This can be set to to items and fluids for filtering, or even values."* |
| 24 | *(no title in the config)* | `1568CBFA09827137` | — | `integrateddynamics:portable_logic_programmer` | no | `4D4152032F0410D2` | Portable version of the Logic Programmer |
| 25 | *(no title in the config)* | `60D9F04E91171D16` | — | `integrateddynamics:variablestore` | no | `4D4152032F0410D2` | Stores Variable Cards for advanced networks |
| 26 | *(no title in the config)* | `65D89991A45BC042` | *AUTO CRAFT* | `integratedcrafting:part_interface_crafting` | no | `4D4152032F0410D2` | Autocrafting via Recipe Variable Cards on a crafting table |
| 27 | *(no title in the config)* | `56BF647EA84FFF7E` | *Shows Recipes* | `integratedterminals:part_terminal_crafting_job` | no | `65D89991A45BC042` | *"Shows which crafting recipes are happening at any time."* |
| 28 | *(no title in the config)* | `6ABDBE41880CFDA9` | — | `checkmark` ×2 | **yes** | — | Hidden staff-attribution quest |

## Chapter 3 of the group — Modular Routers (`modular_router`, 55 quests)

**Modular Routers** (`modularrouters` `13.2.7`) is the only Logistics-group chapter with
`progression_mode: "flexible"`. Of its **55 quests**, **7 are titled** and **48 are
untitled** (*(no title in the config)*).

### 3a. The 7 titled quests in `modular_router`

| Verified quest title | Quest id | Task item(s) | Depends on | What the quest text says |
|---|---|---|---|---|
| **Modular Routers** | `63E4529AF8894018` | `modularrouters:modular_router` | — | *"It all starts with the Router! So make one! Also the Buffer is the single item slot in the Router where items will come and go through. And it will need Redstone signal for most modules to work."* |
| **Modules** | `233C7CAA573D6045` | `modularrouters:blank_module` | `63E4529AF8894018` | *"Modules determine the action the Router preforms. … Modules go into the Router themselves and multiple can be installed. Filtering and Upgrades go into the Modules themselves."* |
| **Upgrades** | `75FE0B514448865B` | `modularrouters:blank_upgrade` | `63E4529AF8894018` | *"Upgrades go directly into the Router and the Router can hold 5 of them. Upgrades directly affect all Modules that they can and usually can stack!"* |
| **Augments** | `6648BC7D14233006` | `modularrouters:augment_core` | `63E4529AF8894018` | *"Augments are similar to Upgrades but for the individual Modules!"* |
| **Routers for Mob Farms** | `53A5F5E49EA8D5AF` | `modularrouters:vacuum_module`, `modularrouters:void_module`, plus smart filter `or(item(modularrouters:sender_module_1)item(modularrouters:sender_module_2)item(modularrouters:sender_module_3))` | `63E4529AF8894018` | *"First, you want to get Items into the Buffer with a Vacuum Module. Next, get rid of the Stone Swords with a Void Module. … Then, use a Sender Module to send the Loot to the Storage System."* |
| **Routers for Mining** | `067AB3E4C4492F0D` | `modularrouters:breaker_module`, `modularrouters:placer_module` | `63E4529AF8894018` | *"You can use a Placer to place down the Ores, then let an Enchanted Breaker Mine the Ores. Breaker needs the Pickaxe used to craft it to be Enchanted first, the Module itself can't be Enchanted."* |
| **Routers for Farming** | `0D5691403AEC25A8` | `modularrouters:activator_module`, `modularrouters:vacuum_module` | `63E4529AF8894018` | *"Then you'll need an Activator Module and direct it toward the Crops. After that, put a Vacuum Module in your Router to collect the Crops. Finally put it all in the Router, Power it with Redstone, and let it farm!"* |

### 3b. The 48 untitled quests in `modular_router` (all *(no title in the config)*)

Every quest below carries no title in `lang/en_us/chapters/modular_router.snbt`:

- **9 Router Upgrades** (all depend on **Upgrades** `75FE0B514448865B`):
  `20D4568857887D38` (`modularrouters:blast_upgrade` — *"TNT won't break it, Wither won't
  break it, only you"*), `09E25B1CD6CABD5A` (`modularrouters:camouflage_upgrade`),
  `1069244EB72F64CA` (`modularrouters:energy_upgrade`), `4FA5192164E4A427`
  (`modularrouters:fluid_upgrade`), `2447208F1DC74FFE` (`modularrouters:muffler_upgrade`),
  `10672B5991E5FC34` (`modularrouters:security_upgrade`), `309B6B8368E535A0`
  (`modularrouters:speed_upgrade`), `4CC963F5AECF285A` (`modularrouters:stack_upgrade`),
  `553C44F85E508DE3` (`modularrouters:sync_upgrade`).
- **11 Module Augments** (all depend on **Augments** `6648BC7D14233006`; `5FB29F3F4DF17765`
  also depends on `4CC963F5AECF285A`):
  `0CE236731DF15DFF` (`modularrouters:fast_pickup_augment`), `76062D375E4CC8DD`
  (`modularrouters:filter_round_robin_augment`), `2DD5F0693780B10A`
  (`modularrouters:mimic_augment`), `674F28BCA2E4A3C8`
  (`modularrouters:regulator_augment`), `177396B9C4F9B3E2`
  (`modularrouters:pickup_delay_augment`), `5560F303C452E110`
  (`modularrouters:pushing_augment`), `1A806C1A54B26EB5`
  (`modularrouters:range_down_augment`), `4EAFE7B240AF0A4D`
  (`modularrouters:range_up_augment`), `3025081DA6D2B398`
  (`modularrouters:redstone_augment`), `5FB29F3F4DF17765`
  (`modularrouters:stack_augment`), `6B747129A85AA768`
  (`modularrouters:xp_vacuum_augment`).
- **21 Modules + 1 Checkmark quest** (rooted at **Modules** `233C7CAA573D6045`):
  - **Item pullers, senders, and distributors:** `1AA81C41431FD145`
    (`modularrouters:puller_module_1`) → `475E1B94A61B9EB0`
    (`modularrouters:puller_module_2`); `6063F4B7BE4D394C`
    (`modularrouters:sender_module_1`) → `38954551309F42A7`
    (`modularrouters:sender_module_2`) → `2405663C033CBDF1`
    (`modularrouters:sender_module_3`); `326C63F7DC713E71`
    (`modularrouters:distributor_module`, depends on `233C7CAA573D6045` and
    `38954551309F42A7`).
  - **Fluids and energy:** `247DAE5B4E1AC7F1` (`modularrouters:fluid_module`) →
    `73D60868024FF907` (`modularrouters:fluid_module_2`); `346B9339E3D66478`
    (`modularrouters:energy_output_module`) → `2B60D123123A5E8E`
    (`modularrouters:energy_distributor_module`, depends on `326C63F7DC713E71` and
    `346B9339E3D66478`).
  - **World interaction, player, and item handling:** `71A1FD0772453B51`
    (`modularrouters:activator_module`), `53B58FC3958750E7`
    (`modularrouters:breaker_module`), `36DED7099E80ED51`
    (`modularrouters:placer_module`), `40788326E791845D`
    (`modularrouters:extruder_module_1`, depends on `233C7CAA573D6045`,
    `53B58FC3958750E7`, `36DED7099E80ED51`), `00E1F1279F97557B`
    (`modularrouters:extruder_module_2`), `7F8DEDD0A54D1E11`
    (`modularrouters:dropper_module`) → `3C54C36CE97A48DC`
    (`modularrouters:flinger_module`), `01C5D8357D8B0D62`
    (`modularrouters:detector_module`), `0DC8B68CDF945348`
    (`modularrouters:player_module`), `417B88FEB1B8F44E`
    (`modularrouters:vacuum_module`), `185074907753AE77`
    (`modularrouters:void_module`), plus checkmark quest `71FDF8CD953E46FC`.
- **5 Filters** (rooted at `143AE6889BDA9EF5` `modularrouters:bulk_item_filter`, which
  depends on **Modules** `233C7CAA573D6045`): `4A03A671757B2EBF`
  (`modularrouters:inspection_filter`), `6E5954C257726F86` (`modularrouters:mod_filter`),
  `72A71E1D6D8996FD` (`modularrouters:regex_filter`), and `37F2BE3C2BAF7C2D`
  (`modularrouters:tag_filter`).
- **1 Hidden authorship quest:** `2BB5769119BA2472` (`checkmark` ×2, `optional: true`).

## Chapter 4 of the group — Pylons (`pylons`, 13 quests) and wireless power cross-checks

- **Why Pylons is in the Logistics group:** the book files **Pylons** (`pylons`,
  `5712300EF4E5E846`, `order_index` 3, `pylons` `5.4.2`) under **Logistics**, even though
  the five pylons are chunk-area utility blocks rather than item pipes. Its only titled
  quest is **Pylons** (`30B0240543253EFB`, task `minecraft:polished_blackstone`); the 11
  playable untitled quests (*(no title in the config)*) cover `pylons:expulsion_pylon`
  (`32E52AD6EF194A60`, subtitle *Get off my lawn!*) + `pylons:player_filter`
  (`403F76908A8A5661`), `pylons:interdiction_pylon` (`5B5FC539BD1F4A73`) +
  `pylons:mob_filter` (`011F787E620DE9E8`, subtitle *He's uninvited!*) +
  `pylons:lifeless_filter` (`5C2C29ECA67F9B49`, subtitle *Finally peace and quiet.*),
  `pylons:harvester_pylon` (`12ED1EE85E146A4B` — deposits harvested crops into an inventory
  above it) + hoe filter (`034A9FBCA6D79BB6`, tag `minecraft:hoes`), `pylons:infusion_pylon`
  (`18246A48C20B29D8`) + `pylons:potion_filter` (`09D18512037386C1`), and
  `pylons:protection_pylon` (`2F5263A4166BFCD6`, subtitle *Accidental Destruction no more!*)
  + `pylons:block_filter` (`77B185799366ACD2`), plus hidden quest `5E02AE661945306C`. Full
  details live in `references/chunk-loading-guide.md` and `references/farming-guide.md`.
- **Wireless power in `basic_power`:** Basic Power's **Transferring Power** hub
  (`1F81EA5E45424308`, task `minecraft:iron_ingot`) links to **Pipez: Energy Pipes**
  (`4EEAB467C722ECE7`), **Mekanism: Universal Cables** (`5C47935A3B2877FF`), **Mekanism:
  Quantum Entangloporter** (`7FE969CB4B419FC6`), and **Flux Networks** (`35CC898E0E49FE58`,
  subtitle *The Ultimate Wireless Power Solution*, task `fluxnetworks:flux_dust`,
  `Flux Networks` `8.0.0`) — see `references/power-guide.md`.
- **Logistics mods in `modlist.json` without a quest chapter in pack 8.2:** **Super Factory
  Manager (SFM)** (`sfm` `4.34.0`), **XNet** (`xnet` `1.21-7.0.7`), and **Ender IO**
  (`enderio` `8.2.12-beta`) are shipped in `config/crash_assistant/modlist.json` at commit
  `e5e3d1d83e`, but none of them has a chapter in `config/ftbquests/quests/chapters/`. Say
  so if the player asks about them, and point him to JEI rather than inventing quests.

## What moves what — capability matrix (from the quest config)

| Resource type | Pipez (`basic_logistics`) | Mekanism (`basic_logistics` + `mekanism`) | LaserIO (`basic_logistics`) | Integrated Dynamics + Tunnels | Modular Routers (`modular_router`) | Transfer Labels (`basic_logistics`) |
|---|---|---|---|---|---|---|
| **Items** | `pipez:item_pipe`, `pipez:universal_pipe` | **Logistical Transporters**, **Quantum Entangloporters** | `laserio:card_item` in `laserio:laser_node` | `integratedtunnels:part_importer_item` / `part_exporter_item` + `part_interface_item` on `integrateddynamics:cable` | Puller Mk1/Mk2, Sender Mk1/Mk2/Mk3, Distributor, Vacuum | Yes (items and fluids) |
| **Fluids** | `pipez:fluid_pipe`, `pipez:universal_pipe` | **Mechanical Pipes**, **Quantum Entangloporters** | `laserio:card_fluid` (tank-to-tank only) | `integratedtunnels:part_importer_fluid` / `part_exporter_fluid` + `part_interface_fluid` (tank-to-tank only) | `modularrouters:fluid_module`, `modularrouters:fluid_module_2` + `modularrouters:fluid_upgrade` | Yes (items and fluids) |
| **Mekanism Gases & Chemicals** (gas, infuse, slurry, pigment) | `pipez:gas_pipe` | **Pressurized Tubes**, **Quantum Entangloporters** | `laserio:card_chemical` | Not tracked in the quests | Not tracked in the quests | Not tracked in the quests |
| **Energy (FE)** | `pipez:energy_pipe`, `pipez:universal_pipe` | **Universal Cables**, **Quantum Entangloporters** | `laserio:card_energy` | `integratedtunnels:part_importer_energy` / `part_exporter_energy` + `part_interface_energy` | `modularrouters:energy_output_module`, `modularrouters:energy_distributor_module` + `modularrouters:energy_upgrade` | No |
| **Mekanism Heat** | No | **Thermodynamic Conductors**, **Quantum Entangloporters** | No | No | No | No |
| **Wireless Redstone** | No (Redstone Upgrade controls the pipe itself) | No | `laserio:card_redstone` | No | `modularrouters:detector_module` / `modularrouters:redstone_augment` (local router control) | No |

## Cross-references

- `references/automation-first-steps.md` — ranks item transport #3 among the first five
  beginner automations, between power (#2) and storage (#4).
- `references/storage-ladder.md` and `references/autocrafting-guide.md` — where the routed
  items go once pipes and routers deliver them (Sophisticated Storage controllers, AE2, and
  Refined Storage).
- `references/power-guide.md` — the full power-transfer and wireless-power picture
  (**Transferring Power**, **Flux Networks**, **Quantum Entangloporters**).
- `references/ore-processing-ladder.md` — the Mekanism Tier 1–4 ore-processing chain whose
  machines require **Side Configs**, **Auto-Eject**, and **Pressurized Tubes**.
- `references/lag-fix-guide.md` — the pack's own lag warnings on mass **Pipez**, **Mekanism**
  pipes, and the **Harvester Pylon**, and why **Integrated Dynamics** is called the least
  laggy pipe solution in `basic_logistics`.
- `references/chunk-loading-guide.md` and `references/farming-guide.md` — full coverage of
  the **Pylons** chapter and farm collection routes.
- `references/progression.md` and `references/key-mods.md` — how the Logistics group maps
  onto `early-game` and `tech`.

## What this page deliberately does not tell you

- **No recipes.** Every item named here is a quest task item or filter entry; JEI has the
  crafting recipe.
- **No unquoted transfer rates.** Where a quest description states a number (*"8 items per
  Operation"*, *"5 Buckets"*, *"Over 2 Billion"*, or Mekanism's Basic–Ultimate figures), it
  is quoted as quest text; where the quest gives no number (Pipez upgrade speeds, Modular
  Router tick rates), this page does not invent one.
- **No factory layouts or coordinates.** How you route your base is up to you; the in-game
  quest book and JEI settle every concrete requirement.
