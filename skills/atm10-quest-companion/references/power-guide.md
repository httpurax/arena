# Power guide: which system to build at each stage

**What this page is.** The power map for **All the Mods 10**: which generation and
storage to build in the early, mid, late, and endgame stages, how the different mods'
power systems relate (what connects to what, and what does not), and when to upgrade.
It answers "what should I power my base with *now*, and what do I replace it with
later?" — nothing more. It is a *map of the quest book's power chapters*, not a
crafting guide.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, and quoted sentence below comes from the
official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10)
at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/basic_power.snbt` + `lang/en_us/chapters/basic_power.snbt` | the pack's own staged power chapter (34 quests): its Early/Mid/End hubs, and its transfer and storage lines |
| `config/ftbquests/quests/chapters/powah.snbt`, `extreme_reactors.snbt`, `generators.snbt` + their `lang/en_us/chapters/*.snbt` | the other three Power-group chapters (109, 33, and 47 quests) |
| `config/ftbquests/quests/chapters/mainquestline_part_1.snbt` + its lang file | Chapter 1's first-power quests (*Wind Power*, *Solar Power*, *Lava Power*, *Generators Galore*) |
| `config/ftbquests/quests/chapters/mekanism.snbt`, `mekanism_reactors.snbt`, `create.snbt`, `mi_steam.snbt`, `mi_electric.snbt`, `mi_digital.snbt`, `draconic_evolution.snbt`, `industrial_foregoing.snbt`, `oritech.snbt`, `pneumaticcraft.snbt`, `immersive_engineering.snbt`, `justdirethings.snbt`, `applied_energistics_2.snbt`, `achapter_2r_6the_atm_star.snbt` + their lang files | the power lines that live inside the tech, storage, and post-star chapters (generation, storage, and conversion quests only) |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` and `chapter_group.snbt` | the chapter titles and the `Power` group the four power chapters sit in |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |
| `config/bcc-common.toml` | the pack version itself (`8.2`) |

The quest-book group is **Power**, and it holds exactly four chapters, in book order:
**Basic Power** (`basic_power`), **Extreme Reactors** (`extreme_reactors`),
**Generators N Furnaces** (`generators`), and **Powah** (`powah`). Most of the pack's
serious power, however, is quested inside other chapters — Mekanism and
Mekanism: Reactors, Create, Modern Industrialization's ages, Draconic Evolution, and
the endgame lines surfaced through Basic Power's hubs — so this page follows the
quests, not just the group tab.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config at the commit above. If the player's book differs,
  his book wins — say so and re-research rather than arguing from this file.
- **Item ids below are quoted from the config, never invented.** An id is shown only
  where a quest task in the config states it. Where the config asks for one item, no
  count is printed; a count appears only where the config or the quoted quest text
  states one.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*.
  Every "how" here is a quote from that quest's own description, marked as such, or
  a pointer to JEI. Do not fill in a recipe from memory or plausibility.
- **Approximate means approximate.** Which tier a player needs, how much generation
  is enough, and whether one mod's cable suits one specific machine are
  version-sensitive. Anything not quoted from the config is flagged as approximate,
  including this page's own "when to upgrade" triggers.
- **Titles are the config's.** Titles are quoted with Minecraft `&` formatting codes
  stripped (the same normalisation `scripts/build_chapter_list.py` applies). Where a
  quest carries no title in the config, it is marked *(no title in the config)* and
  identified by its task item instead — the book then shows the item's own name. Do
  not present a derived name as a verified title. This matters most in Powah: only
  17 of its 109 quests carry an explicit title (32 of 34 in Basic Power do).
- **Nothing here was invented, and nothing is added from memory.** A generator,
  cable, or converter that is not in the config is not on this page. If a player
  names one, the answer is "open that quest in the book / look it up in JEI" —
  never a plausible-sounding guess.

## The short answer

The book itself stages power for you. Basic Power's hub quest **Basic Power**
(subtitle *All The Power!*, task `minecraft:redstone`) branches into
**Early Game Power Options** (subtitle *Starter Power*), **Mid Game Power Options**,
and **End Game Power Options** (subtitle *More Power Than You'll Need*), plus
stand-alone **Transferring Power** and **Storing Power** lines. This guide expands
each hub with the mod chapters behind it, and splits the stretch between the Mid
and End hubs into a "late" stage — the pack has no "Late" hub, so that boundary is
this guide's own, and it is **approximate**.

| Stage (skill stage) | Build this generation | Build this storage | Move it with |
|---|---|---|---|
| Early (`early-game`) | **Coal Generators** / **Heat Generator**, then **Wind Power** / **Solar Power** / **Lava Power** | one of the Chapter 1 storage choices (Mekanism cube or Powah cell) | one cable family from the Chapter 1 transfer choices |
| Mid (`tech`) | **Mekanism: Gas-Burning Generator**, Powah's second tier, or a first Extreme Reactors passive reactor | **Mekanism: Energy Cubes** tiered up, **RFTools Power: Powercells**, or Flux storage | **Pipez: Energy Pipes** or **Mekanism: Universal Cables**, then **Flux Networks** for wireless |
| Late (`tech` → `endgame`) | Powah **Reactor (Blazing)** and up, actively cooled Extreme Reactors + turbine, Mekanism fission + turbine | **More Power Storage** (the Induction Matrix line) | tiered cables; **Mekanism: Quantum Entangloporter** for long-haul |
| Endgame (`endgame`) | **Mekanism: Fusion Reactor**, **Industrial Foregoing: Mycelial Reactor**, or **Dyson Cube** | **Draconic Evolution: Energy Core**, then the post-star creative cells | Flux at scale; Draconic pylons for the core only |

Stages overlap by design (see `references/progression.md`); use the table to orient,
not to gate. And the pack never forces one line: Basic Power's storage and transfer
quests are `ftbfiltersystem:smart_filter` tasks listing alternatives — any one of
them satisfies the quest. Treat "Mekanism *or* Powah *or* …" as alternatives
throughout, exactly as Chapter 1's storage quest puts it: *"The choice is yours."*
(quoted) and *"You only have to make one of the items to complete the quest."*

## How the systems relate — what connects to what

Read this section before mixing mods. The pack runs **one common tech-power core**
and several **separate systems that do not plug into it directly**. The evidence is
the quest book's own structure and descriptions, quoted below; anything beyond the
quote is flagged approximate.

### The FE core (most tech mods)

Most tech power in the book is one shared currency, named **FE** in the quest text:

- Mekanism states it outright in **Power!** (task `mekanism:energy_tablet`):
  *"Mekanism uses FE to run Machines!"* (quoted) — and its generators are the
  `mekanismgenerators` line below.
- Powah's hub **Welcome to Powah!!!** (task `powah:uraninite_raw`) describes the mod
  as *"all about generating, storing, and transmitting Power"*, *"Ranging from basic
  FE generation to Reactors that produce 250k FE/t"* (quoted figures — the quest
  author's, verify in-game).
- Extreme Reactors' passive output is a *Power Tap FE* part
  (`bigreactors:basic_reactorpowertapfe_active`, and the turbine equivalent), and
  its controller text reports *"how much FE/t the reactor is producing"* (quoted).
- Industrial Foregoing's first generator is described in its chapter as generating
  *"a small amount of FE using burnable fuels like Coal"* (quoted; the quest itself
  is *(no title in the config)*, task `industrialforegoing:pitiful_generator`), and
  **Bio Power**'s generator *"uses Biofuel made from the Bioreactor to generate FE"*
  (quoted).

Because the same transferring/storing quests accept several mods' parts as
either/or alternatives (see Transfer and Storage below), the book treats FE
generation, cables, and storage from different mods as interchangeable *for those
jobs*. Whether a specific cable face or side-configuration suits a specific
machine in the player's version is **approximate** — the quest entry, the machine's
own side configuration, and JEI settle it.

### Create: Rotational Power is not FE

Create runs on rotation, not FE. **Rotational Power** (task `create:shaft`) says
*"All Machines will need some sort of Rotational Power to work"* and that shafts
and cogs *"will move that Rotational Power to our Machines"* (quoted). Its two
measures are **Speed** (task `create:speedometer`) and **Stress** (task
`create:stressometer`): *"Stress Units (Su) are power loads for our Machines"*
(quoted). Its sources are **Hand Crank**, **Water Wheels**
(`create:water_wheel` / `create:large_water_wheel`), **Windmills**
(`create:windmill_bearing` + `create:white_sail`), and **Steam Engine**
(`create:steam_engine` + `create:fluid_tank` + `create:shaft`).

No quest in the chapters read offers a rotation-to-FE converter, and no FE cable
drives a Create machine. If a player asks how to turn FE into rotation (or the
reverse), the answer is to check JEI for a converter in his version — do not name
one from memory. (Immersive Engineering's **Energy from moving things!**, task
`immersiveengineering:dynamo`, is a different design with a similar shape: a
kinetic source — waterwheel or windmill, per its text — feeding FE out to
connected blocks. The two mods' kinetic systems are not stated to connect to each
other; treat any bridge as approximate until JEI confirms it.)

### Modern Industrialization: steam first, then its own electricity

MI's Steam Age runs on steam, not FE: the boiler quest is *(no title in the
config)* (task `modern_industrialization:bronze_boiler`), and its text says the
boiler *"converts water into steam. Steam will act as fuel for your machines to
work in the Steam Age."* (quoted). Electricity arrives with **The Electric Age**
(task `modern_industrialization:battery_alloy_ingot`): two generator quests, both
*(no title in the config)* — the steam turbine
(`modern_industrialization:lv_steam_turbine`; *"put steam in and pull electricity
out"*, quoted) and the diesel generator
(`modern_industrialization:lv_diesel_generator`; *"converts a variety of liquid
fuels to electricity"*, quoted) — under the checkmark quest **Electricity
Generation**. Its transfer quest **LV Cables** (`modern_industrialization:tin_cable`
/ `copper_cable` / `silver_cable` filter) measures transfer in **EU/t**: *"LV
cables can transfer 256 EU/t at most."* (quoted figure; a higher tier appears as
*(no title in the config)*, task `modern_industrialization:superconductor_cable`,
in the End Game chapter).

The quests read name MI's unit EU and gate cables and machine hulls by voltage
tier. They do **not** state that MI electricity interchanges with FE, and this page
does not either: whether (and how) MI power feeds FE machines in the player's
version is **approximate** — check the cables and machines in JEI. The same caution
applies in reverse to MI's nuclear line: the **Digital Age** reactor quest is
*(no title in the config)* (task `modern_industrialization:nuclear_reactor`), and
its text says *"We will be using it to generate Deuterium and Tritium"* (quoted) —
resource processing, not a verified electricity plant. Do not list it as one.

### PneumaticCraft: pressure, with a two-way FE bridge

PneumaticCraft *"is all about Pressure!"* (quoted, chapter hub
**PneumaticCraft: Repressurized**). Pressure is made by **Generating Pressure**
(task `pneumaticcraft:air_compressor`, burnable fuel) and its compressor family —
**Pressure from the Sun** (`pneumaticcraft:solar_compressor`), **Pressure from
Liquids** (`pneumaticcraft:liquid_compressor`), **Pressure from Heat**
(`pneumaticcraft:thermal_compressor`), **Pressure from Lightning**
(`pneumaticcraft:electrostatic_compressor`), plus the two advanced compressors
(*(no title in the config)*). Pressure itself is not FE — but the chapter verifies
a bridge in **both** directions:

- **Pressure from Power** (task `pneumaticcraft:flux_compressor`): *"Simply pump
  some FE in and it will start generating some [pressure]."* (quoted) — FE → pressure.
- **Generating Power** (task `pneumaticcraft:pneumatic_dynamo`): *"The Pneumatic
  Dynamo allows you to turn your pressure in FE."* (quoted, pack spelling) —
  pressure → FE.

So PneumaticCraft machines run on pressure; FE only enters or leaves through those
two blocks. Rates and pressure tiers are JEI territory.

### AE2: AE is converted from FE, not FE itself

The Applied Energistics 2 energy quests are *(no title in the config)* (tasks
`ae2:energy_acceptor`, then `ae2:energy_cell` / `ae2:dense_energy_cell`). Their
text is explicit: *"the vast majority of an ME network uses its own dedicated
power system called AE. RF/FE can be converted into the native AE at a ratio of
2:1 RF:AE, either directly through an ME Controller, or through the Energy
Acceptor"* (quoted, including the 2:1 figure — the quest author's, verify
in-game), while *"the Inscriber and Charger will natively accept RF/FE"* (quoted).
Budget an AE network in AE, fed from the FE core — the two are related by that
conversion, not identical.

### Draconic Evolution: OP stays inside Draconic

Draconic's currency is its own. **What is Energy or as we call it, OP?** (task
`draconicevolution:crystal_binder`) says OP is *"the Energy source of Draconic
Evolution"*, moved *"with IO Relay Crystals"* (quoted), and charged into items
through the transfusion line (**Adding OP to items**). Storage is the **Energy
Core Mulitblock** *(title spelled that way in the config)* (task
`draconicevolution:energy_core`) with **Energy Core Stabilizers** and pylons —
*"Pylons are how you get OP in and out of the Energy Core."* (**Power comes and
goes through these**, quoted). No quest read converts OP to or from FE. Treat the
Draconic core as an endgame FE-adjacent bank only in the loose sense the book
gives it — Basic Power files it under **Storing Power** with subtitle *Basically
Infinite Storage* — and check JEI before claiming any adapter in a given version
(approximate).

### Wireless transfer (still FE, no wires)

Two verified wireless layers move the FE core's power without cables:

- **Flux Networks** (subtitle *The Ultimate Wireless Power Solution*; Flux
  Networks 8.0.0): *"The mod itself does not have a way to
  generate power, but it can store and wirelessly transmit power, even across
  dimensions."* (quoted, **Flux Networks**, task `fluxnetworks:flux_dust`). The
  chain is **The "Core" Crafting Materials** (`fluxnetworks:flux_core`,
  `fluxnetworks:flux_block`) → **Starting Your Network** (`fluxnetworks:flux_plug`,
  which *"draw[s]"* power from the block it is attached to, quoted) → *(no title in
  the config; subtitle *Becoming a Network Admin!*, checkmark task)* → **Accessing
  Network Power** (`fluxnetworks:flux_point`), **Flux Storage**
  (`fluxnetworks:basic_flux_storage`), and **Wireless Charging**
  (`fluxnetworks:flux_controller`, which keeps inventory items — jetpacks named in
  the text — charged). Flux Dust itself has two automation quests, both titled
  **Automated Flux Dust** (a Productive Bees route and an XyCraft route,
  `xycraft_machines:extractor` + `appflux:charged_redstone_block`).
- **Mekanism: Quantum Entangloporter** (task `mekanism:quantum_entangloporter`):
  *"this machine allows you to transfer anything wirelessly"* — *"individual items,
  energy, or even gases from Mekanism"* (quoted). It is a transfer block, not a
  generator.

Powah adds its own wireless wrinkles inside its system: the transmitter quests
are *(no title in the config)* (starter task `powah:player_transmitter_starter`)
— *"The Player Transmitter will charge a player's items wirelessly"* (quoted,
same-dimension with the basic binding card, dimensional with the upgraded one,
per its text) — and the Ender Cell line (starter task `powah:ender_cell_starter`)
stores power *"for a channel in your Ender Network"* (quoted). Whether a Powah
wireless channel carries another mod's FE unchanged is **approximate** — the quest
entry settles it.

### What is deliberately not connected here

- **Steam (MI), Rotational Power (Create), Pressure (PneumaticCraft), AE (AE2),
  and OP (Draconic Evolution)** are five separate systems above. The only
  cross-system bridges the chapters read verify are PneumaticCraft's two FE
  converters and AE2's FE→AE conversion. Everything else a player might assume
  (rotation→FE, EU↔FE, OP↔FE) is unstated in the quests read: say so, and send
  him to JEI.
- Chapter 1's transfer text mentions one more cable family by name — *"this pack
  has EnderIO and you can use the Energy Conduits from it"* (quoted). The modlist
  does carry Ender IO (8.2.12-beta), but no quest task in the chapters read asks
  for an Ender IO conduit, and Ender IO has no chapter file in the book at this
  commit. Treat conduits as **present-but-unquested (approximate)**: confirm the
  exact conduit in JEI rather than quoting this page for it.

## Early game — first machines, first power

*The pack's staging:* **Early Game Power Options** (subtitle *Starter Power*):
*"These don't produce a ton of power, but they are typically easy or cheap to get
in the early game!"* (quoted). Chapter 1 walks the same ground with **Wind Power**
(task `mekanismgenerators:wind_generator`; *"place it as high as you can and get
free power"*, quoted), **Solar Power** (`powah:solar_panel_basic` or
`mekanismgenerators:solar_generator`; *"it has to be daytime"*, quoted), and
**Lava Power** (`powah:magmator_basic` / `powah:magmator_starter` /
`generatorgalore:magmatic_generator`).

**Generation to build (pick one to start, add the free ones):**

| Verified quest title | Task item (config) | Notes (quoted where marked) |
|---|---|---|
| **Coal Generators** (subtitle *Fossil Fuels*) | filter: `actuallyadditions:coal_generator` or `justdirethings:generatort1` or `rftoolspower:coalgenerator` | *"some of the easiest generators to make… They also automatically distributes power to adjacent blocks."* Any one satisfies the quest. |
| **Heat Generator** | `mekanismgenerators:heat_generator` | Passive (lava around it) or active (burns coal/wood, *"not very efficient"*). |
| **Mekanism: Renewable Energy** (subtitle *The Power of the Sun...*) | filter: `mekanismgenerators:solar_generator`, `mekanismgenerators:advanced_solar_generator`, or `mekanismgenerators:wind_generator` | Solar *"does not work during the night"*; wind output depends on Y level and clear sky (quest text). |
| **Wind Power** / **Solar Power** / **Lava Power** (Chapter 1) | see above | The Main Questline's own first-power trio. |
| *(no title in the config)* | `industrialforegoing:pitiful_generator` | *"generates a small amount of FE using burnable fuels like Coal"* (Industrial Foregoing chapter text). |
| *(no title in the config)* | `justdirethings:generatort1` | *"Just a simple coal generator."* (Just Dire Things chapter text); a fluid-fuel sibling (`justdirethings:generatorfluidt1`) and a handheld `justdirethings:pocket_generator` sit next to it. |

Mekanism's own chapter adds the same family with its own titles — **Solar
Generator**, **Advanced Solar Generator**, **Wind Generator**, **Heat Generator**
— and one explicit warning: **Bio-Generator** (task
`mekanismgenerators:bio_generator`) is described as *"heavily nerfed"* with a
recommendation not to rely on it (quest text; exact figures are the entry's, not
this page's). Do not route a new player to it as the early staple.

Powah's first machines are all *(no title in the config)* at the `starter` tier,
behind **Welcome to Powah!!!** → **Starting with Dielectric Mats**
(`powah:dielectric_paste` + `powah:dielectric_casing`) and gated a step later by
**Tier: Tiny** (`powah:capacitor_basic_tiny`): the thermo generator (`powah:thermo_generator_starter`; over a heat source with water, per its text), furnator (`powah:furnator_starter`; burns coal/wood), solar panel (`powah:solar_panel_starter`; direct sun), magmator (`powah:magmator_starter`; lava), and **Reactor (Starter)** (`powah:reactor_starter` — the one titled quest of the family; its text calls it a *"3x4x3 multiblock generator that burns Urananite as fuel"* and asks for 36 reactor blocks, quoted).

Generator Galore's opening tier (Generators N Furnaces chapter) is the material
ladder **Copper Generator**, **Iron Generator**, **Gold Generator**, **Diamond
Generator**, **Netherite Generator**, **Emerald Generator**, **Obsidian
Generator** (`generatorgalore:copper_generator` through
`generatorgalore:obsidian_generator`), alongside the fuel-flavoured
**Magmatic Generator**, **Ender Generator**, **Honey Generator**, **Potion
Generator**, **Enchantment Generator**, **Halitosis Generator**, and two
*(no title in the config)* entries (`generatorgalore:culinary_generator`,
`generatorgalore:netherstar_generator`). Chapter 1's **Generators Galore** quest
samples four of them by filter. What fuel each one wants in the player's version
is JEI's answer — the titles name the theme, they are not a fuel table.

**Storage to build:** Chapter 1's storage quest is *(no title in the config)*:
`mekanism:basic_energy_cube` **or** `powah:energy_cell_starter` — *"You only have
to make one of the items to complete the quest."* (quoted). Basic Power's
**Storing Power** line offers the same choice widened: **Mekanism: Energy Cubes**
(the basic→ultimate family), **RFTools Power: Powercells** (`rftoolspower:cell1`
/ `cell2` / `cell3`; *"multi-block storage units that can be customized and
upgraded"*, quoted), and **Integrated Dynamics: Energy Battery** (subtitle
*Batteries Included*, task `integrateddynamics:energy_battery`; batteries
*"can be combined in a crafting grid to increase the overall storage"*, quoted).

**Transfer to build:** Chapter 1's transfer quest is likewise *(no title in the
config)*: `mekanism:basic_universal_cable` **or** `pipez:energy_pipe` **or**
`powah:energy_cable_basic`. Pick the family that matches the generators you chose;
Chapter 1's storage text calls Powah's cells *"great storage using Energy Cells
that can be upgraded"* (quoted) — the pack presents these as alternatives, not a
sequence.

**When to upgrade (approximate):** when the Early hub's own words stop being true
— the coal line needs constant refuelling, or solar/wind stalls overnight stall
your machines. The book's trigger for leaving this stage is the Mid hub's opening:
*"You can't power your base off of Coal forever!"* (quoted, **Mid Game Power
Options**). Any FE/t threshold for "enough" would be invented; there is none here.

## Mid game — the first real power plant

*The pack's staging:* **Mid Game Power Options** (task `minecraft:diamond`):
*"If you've got a decent amount of resources available, it's time to upgrade your
power setup! These options usually require a little setting up, but produce
enough power to carry you far into your playthrough."* (quoted).

**Generation to build (one primary line is enough):**

| Line | Verified quest titles / task items | Shape, from the config |
|---|---|---|
| Mekanism gas | **Mekanism: Gas-Burning Generator** (subtitle *MELON POWER!*, task `mekanismgenerators:gas_burning_generator`) | Ethylene chain in its own text: Crusher → Bio Fuel → Pressurized Reaction Chamber (Water + Bio Fuel + Hydrogen from an Electrolytic Separator) → generator. *"can produce a good amount of power"* (quoted). |
| Powah, second tier | **The Energizing Orb** (`powah:energizing_orb` + cable/rod filters) → **Tier: Basic** (`powah:capacitor_basic`), **Tier: Energized** (`powah:steel_energized`) → **Reactor (Basic)**, **Reactor (Hardened)** | Every starter machine repeats per tier (thermo/furnator/solar/magmator/reactor, cells, batteries, cables, transmitters, energizing rods — nearly all *(no title in the config)*, identified by their `powah:*_<tier>` task items). The orb *"will energize items using nearby Energizing Rods"*, and *"you'll eventually need to create energized mats"* (quoted). |
| Extreme Reactors, passive | **Our First Reactor** → **Fueling our Passive Reactor** → **Expanding Our Reactors** | *"the smallest passive reactor possible, the 3x3x3"* (quoted) from `bigreactors:basic_reactorcasing`, `basic_reactorcontroller`, `basic_reactorsolidaccessport`, `basic_reactorpowertapfe_active`, `basic_reactorcontrolrod`, `basic_reactorfuelrod`. Fuelled with `alltheores:uranium_ingot` (×4 where the config states it, under **Fueling our Passive Reactor**). Waste line: **Dealing with Waste** (`bigreactors:cyanite_ingot`) → **Reprocessing our Waste** → **Blutonium**. |
| Generator Galore, stacked | **8x What a deal!** (any `generatorgalore:*_generator_8x` from its 15-option filter) | The same generator families, stacked. The 64x step is *(no title in the config)* (nine-option `*_generator_64x` filter, whose family also supplies Chapter 3 star quests — see `references/atm-star-checklist.md`). |
| Immersive Engineering | **Energy from moving things!** (`immersiveengineering:dynamo`) → **Energy from Temperature** (`immersiveengineering:thermoelectric_generator`) → **Diesel Generator** | Diesel multiblock (built around `immersiveengineering:generator` blocks); its text ranks its fuels *"Creasote Oil, Biodiesel, and High-Cetane Biodiesel… in order from worst to best"* (quoted, pack spelling). The windmill feeding the dynamo is *(no title in the config)* (`immersiveengineering:windmill`). |
| Industrial Foregoing / Oritech side lines | **Bio Power** (`industrialforegoing:bioreactor` + `biofuel_generator`); Oritech generators, all *(no title in the config)* (`oritech:basic_generator_block`, `lava_generator_block`, `bio_generator_block`, `fuel_generator_block`) | Biofuel → FE (quoted above). Oritech's four blocks carry no quest description in the config — what each burns beyond its name is JEI's answer, not this page's. Its transfer/storage quests are titled **Transfering Energy** *(spelled that way in the config)* (`oritech:energy_pipe` family) and **Storing Energy** (`oritech:small_storage_block`, `large_storage_block`). |
| Modern Industrialization (guided ladder) | **The Electric Age** → **Electricity Generation** | Steam first (Steam Age boiler, above), then the LV steam turbine / diesel generator pair. A player committed to MI does not need a second mid-game plant *for MI machines*; how MI electricity meets his FE core is the approximate question flagged above. |

Basic Power routes the player at exactly this point: **Extreme Reactors:
Reactors** (subtitle *Customizable Reactors!*, task `alltheores:uranium_ingot`)
hangs off **Mid Game Power Options**, and **More Powah!** (task `powah:uraninite`)
does the same for the Powah chapter. The book's mid-game menu is therefore
"gas, Powah tiers, or a first reactor" — present all three, do not crown one.

**Storage to build:** tier up what you have. **Mekanism: Energy Cubes** accepts
any of basic/advanced/elite/ultimate (and, in Basic Power's filter, the creative
cube); Mekanism's chapter quest **Energy Cubes** covers the four non-creative
tiers, and its text gives each tier's capacity — quoted capacities are the quest
author's figures, so repeat them only as quest text and verify in-game.
**More Power Storage** (two induction filters: `mekanism:*_induction_provider`
and `mekanism:*_induction_cell`) hangs off **Mekanism: Energy Cubes** and points
at the Induction Matrix: *"Mekanism's Induction Matrix is one of the best ways to
store your power."* (quoted). **Flux Storage** covers the wireless side.

**Transfer to build:** **Transferring Power** offers **Pipez: Energy Pipes**
(`pipez:energy_pipe` + `pipez:wrench`; shift-right-click with the wrench sets
extraction, per its text) with **Pipez: Upgrades** (basic/improved/advanced/
ultimate filters — *"they just move more!"*, quoted), and **Mekanism: Universal
Cables** (subtitle *Mekanism's Energy Transfer Pipe*; basic→ultimate filter).
Add **Flux Networks** here even if generation stays wired: it is the book's
answer for remote bases and cross-dimension power, and it charges the gear the
player is already flying in (see Wireless above).

**When to upgrade (approximate):** when one maxed mid-game line plus its storage
still drains overnight, or a new consumer class lands (an ME network's AE draw, a
Mekanism ore-processing line, a reactor's own support machines). The book's own
late-game advice is to scale before replacing: *"Make your Reactors bigger.
Upgrade your Thermo Generators to Nitro. Go wild."* (quoted, **End Game Power
Options** introduction). Try that first; jump to the late lines when scaling a
single line stops being cheaper than the multiblock — that cost comparison is the
player's JEI check, not a number this page can give.

## Late game — multiblock power and serious storage

This stage is the second half of the book's Mid hub shading into its End hub;
the boundary is approximate, and the pack labels none of it "late". What changes
is the shape: single blocks give way to multiblocks with support chains.

**Generation to build:**

- **Powah, top tiers.** The reactor dependency chain verifies the ladder order:
  **Reactor (Starter)** → **Reactor (Basic)** → **Reactor (Hardened)** →
  **Reactor (Blazing)** → **Reactor (Niotic)** → **Reactor (Spirited)** →
  **Reactor (Nitro)**, gated by **Tier: Energized**, **Tier: Blazing**, **Tier:
  Niotic**, **Tier: Spirited**, and **Tier: Nitro** (`powah:crystal_nitro` for the
  last). The whole machine family repeats at each tier (*(no title in the
  config)*, `powah:*_blazing` through `powah:*_nitro`), ending in
  `powah:player_transmitter_nitro` — the same transmitter Chapter 3's star wants
  (see `references/atm-star-checklist.md`). **Reactor (Starter)**'s text is the
  family's shape: a 3x4x3 uranium-fuelled multiblock, cooled for more output
  (quoted in the Early section; the starter numbers do not transfer to higher
  tiers — JEI has each tier's).
- **Extreme Reactors, actively cooled + turbine.** **Building An Actively Cooled
  Reactor** (subtitle *To Make Steam!!*, `bigreactors:reinforced_reactorcasing`
  + fluid port) turns reactor heat into vapour; **Making Turbines**,
  **Turbine Ports**, **Creating The Turbine Shaft**, **Turbine Construction**,
  and **The Turbine** (task type `forge_energy` — the book's own generic energy
  task, not an item) turn that vapour into power: *"Turbines… input vapors like
  Steam made by Actively Cooled Reactors to create TONS of power!"* (quoted,
  **Making Turbines**). Mind the parts rule from **Reactor Building
  Components**: *"when a part says 'Basic', this means that it can only be used
  with other basic parts"* and basic parts *"can only be used to build smaller
  reactors"* (quoted) — the reinforced line is the scale-up. End-material quests
  (**Ludicrite \& Ridiculite**, **Insanite**, **Insanite Block** —
  `bigreactors:insanite_block`, also a Chapter 3 star task) close the chapter.
- **Mekanism fission, boiler, and turbine.** Mekanism: Reactors builds
  **Fission Reactor** (`mekanismgenerators:fission_reactor_casing`,
  `fission_reactor_port` ×4, `fission_reactor_logic_adapter`,
  `fission_fuel_assembly`, `control_rod_assembly` — counts as the config states
  them) on its fuel chain (**Preparing Uranium**, **Fissile Fuel**, **Sodium
  Coolant** / **Water Coolant**, **Radioactivity**), makes steam in
  **Thermoelectric Boiler** (`mekanism:boiler_casing` + valves/disperser/
  superheating elements), and burns it in **Turbine** — **Making Energy with a
  Turbine** is the quest title that says what the multiblock is for. Safety and
  waste quests (**Advanced Fail Safe**, **Fission Reactor Logic Adapter**) are
  part of the build, not optional flavour — but their settings are the quest
  entry's, never this page's.
- **MI's later ages** keep their own ladder (Digital Age, End Game chapters).
  Their power-relevant content in the quests read is the cable end of the line
  (the superconductor task above) and the nuclear processing warning in the
  Systems section. A dedicated MI power plant beyond the LV pair is not verified
  by a titled quest here — check the MI chapters and JEI rather than assuming
  one (approximate).

**Storage to build:** **Energized Induction Matrix** (`mekanism:induction_casing`
×32, `induction_port` ×2 — counts as the config states them) with its
**Induction Cells** (subtitle *Storage*) and **Induction Providers** (subtitle
*Transport*) tier filters. This is the *"best power storage Mekanism has to
offer"* pointer that **More Power Storage** makes (quoted). Build it when cube
tiers stop holding a night's surplus (approximate trigger).

**When to upgrade (approximate):** when a late multiblock's support chain
(fuel, coolant, steam) is automated and still the buffer trends down, or the
next project is on the End hub's list (fusion-scale consumers, star components,
Chapter 4 automation). At that point the choice is no longer a bigger version of
the same block — it is one of the three endgame lines below.

## Endgame — fusion, swarms, and a sun

*The pack's staging:* **End Game Power Options** (subtitle *More Power Than
You'll Need*, task `minecraft:netherite_ingot`). Its text first tells the player
to scale the mid-game lines (quoted in Mid, above), *"However, you may need even
more power."* Three quests hang off it:

| Verified quest title | Task item (config) | What the quest text claims (quoted; verify in-game) |
|---|---|---|
| **Mekanism: Fusion Reactor** (subtitle *Fusion Activate!*) | `mekanismgenerators:fusion_reactor_controller` | *"The Fusion Reactor can produce up to 80MRF/t"* — quoted exactly as written (the book writes MRF here, FE elsewhere; do not convert). Full build in Mekanism: Reactors: **Fusion Reactor** (`fusion_reactor_controller`, `laser_focus_matrix`, `fusion_reactor_frame`, `reactor_glass`, `fusion_reactor_port` ×2) on the **Deuterium** / **Tritium** / **D-T Fuel** chain. |
| **Industrial Foregoing: Mycelial Reactor** (subtitle *It's not Yourcelial Reactor*) | `industrialforegoing:mycelial_reactor` | *"consists of all the Mycelial Generators working at the same time, near the reactor block, and it produces a total of 25MFE/t"* — one of every mycelial generator, each with its own automated input; *"you don't need to stop at one, you can make more reactors."* Chapter 3 also wants one part by name (*Explosive Mycelial Generator*, `industrialforegoing:mycelial_explosive`). |
| **Dyson Cube** (subtitle *The power of the Sun, in the palm of your hand*) | `dysoncubeproject:em_railejector_controller` + `dysoncubeproject:ray_receiver_controller` | *"the ultimate power source, producing an insane 1GFE/t!"* — with the ejector/receiver constraints and the beam/sail counts its text states (orbital launches cannot fire at midday, night, or rain, per that text). The mod is Dyson Cube Project 1.0.5 in the modlist. Treat the whole entry as the pack's flex goal, not a recommendation to rush. |

**Storage to finish on:** **Draconic Evolution: Energy Core** (subtitle
*Basically Infinite Storage*) hangs off **Storing Power**, and the Draconic
chapter builds it through **Energy Core Mulitblock** → **Tier 1** … **Tier 8**
(`draconicevolution:energy_core_stabilizer`, `draconium_block`,
`minecraft:redstone_block`, and awakened blocks at the top; Tier 7 sits after
Tier 8 in the config's quest list — the tier order quoted here is the titles',
and the chapter's dependency links are the order to trust in-game). Its text
says the final tier *"can hold 9,223,372,036,854,775,808 FE basically infinite
power"* (quoted figure — the quest author's, and a sign of the intended scale,
not a target to quote back as a requirement). The Draconic reactor line
(**Building the Reactor**, **Reactor Stabilizers**, **Reactor Energy Injector**,
**Fuel for our Reactor**) is likewise endgame content, but it produces and
consumes OP inside Draconic's own system (Systems section) — do not budget it
as an FE plant without an in-game conversion check (approximate).

**After the star:** Chapter 4 turns power infinite. Four of its creative-tier
quests are power items, each gated behind *Fully Automated ATM Star* by a single
dependency (see `references/creative-checklist.md`): **Energy Cell (Creative)**
(subtitle *Unlimited Powah!*, `powah:energy_cell_creative`), **Creative Energy
Cube** (`mekanism:creative_energy_cube`), **Creative Energy Battery**
(`integrateddynamics:energy_battery_creative`), and **Creative Energy Cell**
(`ae2:creative_energy_cell`). Note the book's own warning, carried in the
creative checklist: Powah and AE2 both field an item the quests call a creative
energy cell — when a player says "the creative energy cell", ask which mod's he
means. Basic Power already foreshadows one of them: its **Mekanism: Energy
Cubes** filter includes the creative cube among the satisfying options.

**When to upgrade (approximate):** there is nothing above this stage except
more of it — a second reactor, a second fusion plant, a bigger Draconic tier.
If endgame generation still starves, the bottleneck the quests point at is
usually fuel/coolant automation or transfer (tier up the cables, add Flux
points with higher limits — *"Each Plug or Point can be named, have a custom
priority level, and have a custom power transfer limit"*, quoted from the
untitled Flux UI quest) rather than a missing mod. Confirm in the Flux network
statistics and JEI before building anything new.

## Cross-references

- `references/progression.md` — where Basic Power (early) and Powah / Extreme
  Reactors / Generators N Furnaces (tech) sit in the four-stage map.
- `references/key-mods.md` — the one-line primers for Mekanism, Powah, Extreme
  Reactors, Create, and Modern Industrialization that this page expands.
- `references/atm-star-checklist.md` — the star quests that touch power
  (Generator Galore's 64x generators, the Explosive Mycelial Generator,
  Powah's Nitro Player Transmitter, Extreme Reactors' Insanite Blocks).
- `references/creative-checklist.md` — Chapter 4's four creative power items in
  their verified order, behind *Fully Automated ATM Star*.

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item above is a quest *task*; JEI has the recipe,
  and recipes are where pack versions differ most.
- **Unquoted FE/t figures, cable capacities, cell capacities, reactor
  dimensions, or fuel values.** The few numbers printed here are quoted from
  quest descriptions and attributed as such. Everything else — including which
  Powah tier or reactor size a given base "needs" — is the quest entry's and
  JEI's business, and any threshold this page implies is approximate.
- **A single "best" power mod.** The book offers alternatives at every stage
  (either/or filters, three endgame lines). Crowning one would invent a
  requirement the pack does not have.
- **Converters the quests do not name.** Rotation↔FE, EU↔FE, OP↔FE, and magic
  resources (Source and its kin, which have their own chapters and are outside
  this page's files) get no conversion claim here. If JEI shows one in the
  player's version, it wins — say so and note the mismatch.
- **Anything not in the config.** If a player asks about a generator, cable, or
  storage block that is not listed here, the answer is "open that quest in the
  book / look it up in JEI" — never a guess.
