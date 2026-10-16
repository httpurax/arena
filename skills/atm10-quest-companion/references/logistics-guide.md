# Item and fluid logistics in ATM10: "why aren't my pipes moving anything?"

**What this page is.** The beginner transport map for **All the Mods 10**: choose an
item or fluid route, configure extraction and insertion, then diagnose a stalled line.
It expands the transport step in `references/automation-first-steps.md`; it is not a
recipe list or a complete reference for every logistics mod.

**Short answer (judgement).** Start with one source, one destination, and the matching
Pipez pipe. Test that simple link before adding filters or branching. If you already use
Mekanism, its transporters and pipes are an alternative; LaserIO adds node-and-card
routing, and Integrated Dynamics supplies a programmable route. These are alternatives,
not a mandatory progression through four mods.

## Provenance — everything here was read, not remembered

The verified titles, task items, dependencies, and quest-text excerpts below come from
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22, **pack 8.2**). This is the same snapshot as the sibling guides, not a claim
about the latest pack release.

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/basic_logistics.snbt` | the Basic Logistics chapter's 40 quests, task items and dependencies |
| `config/ftbquests/quests/lang/en_us/chapters/basic_logistics.snbt` | explicit English titles and descriptions, including the conflicting Pipez filter advice |
| `config/ftbquests/quests/chapters/mekanism.snbt` | the Mekanism logistics branch and its dependencies |
| `config/ftbquests/quests/lang/en_us/chapters/mekanism.snbt` | the Configurator, transporter, pipe and tube titles and descriptions |
| `config/bcc-common.toml` | `modpackVersion = "8.2"` |

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** If the player's
  installed book or machine GUI differs, trust it. This page describes pack 8.2 only.
- **No recipes.** Task items identify the quest, not how to craft the item. Use JEI.
  Filtered tasks are identified as such, not passed off as one exact required pipe tier.
- **Titles are explicit English config titles with formatting codes removed.** An entry
  marked *(no explicit title)* has an item/device label here, not a verified quest title.
- **Dependency order is not a mod gate.** Quests are optional; these branches can be
  pursued independently. The suggested first build and troubleshooting order are
  *judgement*, not quest requirements.
- **Quest descriptions are not compatibility tests or benchmarks.** No guaranteed rate,
  universal cross-mod connection, or measured performance ranking is claimed here.

## 1. Pipez — a first local link

All entries in this section are in **Basic Logistics**. Its **Logistics** root
(`6CD7D99AA102A5C3`) describes moving, managing, and storing resources. The Pipez branch
starts independently; its root has no quest dependencies.

| Verified quest title (or explicit untitled marker) | Quest id | Task / dependency trail |
|---|---|---|
| **Pipez** | `2329AA0AFBEF1E13` | `pipez:wrench`; no dependencies |
| **Item Pipez** | `36836AD948F96B9F` | `pipez:item_pipe`; depends on Pipez |
| **Fluid Pipez** | `33433A443B65D252` | `pipez:fluid_pipe`; depends on Pipez |
| **Energy Pipez** | `53EC96FA0E7C4ED4` | `pipez:energy_pipe`; depends on Pipez |
| **Universal Pipez** | `4FBAB3A0FBF8CE2F` | `pipez:universal_pipe`; depends on Item Pipez, Fluid Pipez, and Energy Pipez |
| **Gas Pipez** | `2F4458E9921DEB86` | `pipez:gas_pipe`; depends on Pipez |
| Destination filter tool *(no explicit title)* | `2A976D41F79C34B1` | `pipez:filter_destination_tool`; depends on Pipez |
| Pipe upgrades *(no explicit title)* | `6A962535CD68713E` | filtered `ftbfiltersystem:smart_filter` task accepting Basic, Improved, Advanced or Ultimate Pipez upgrades; depends on Pipez |

**What to configure (quest text).** Pipez says:

> Attach the specific Pipe to where you want to move items and use the Pipe Wrench to configure what side Pulls, Pushes, or doesn't connect.

Item Pipez specifically says to configure which side it pulls from. Fluid Pipez describes
moving fluids and connecting to sinks; that is not evidence that an item pipe can move
water. Universal Pipez describes **items, fluids, or energy** — do not extend that list
to chemicals. Gas Pipez explicitly says gas cannot be moved with the other Pipez and
points to the machine display and JEI to distinguish gas, fluid, and infuse types.
Keep the older quest term "Gas" attributed to the book; do not treat a fluid and a
Mekanism chemical as interchangeable because both appear in a tank-like GUI.

**Filtering caveat — the snapshot contradicts itself.** The destination-tool quest says:

> Pipez do have their own way of Filtering Items, you need atleast an Advanced Upgrade to get it though. When an Advanced Upgrade is in you can click the Add button to add Filters.

The upgrade quest instead says:

> Basic Upgrade allows Redstone Activation with Pipez, to change distribution either:Closest First, Farthest First, Round-Robin, or Random, and to add Filters.

It then says the higher upgrades only move more. **Do not resolve this contradiction
from memory or guarantee a minimum filtering tier.** Check the installed extraction GUI,
its upgrade tooltip and the live quest entry. The destination-tool description also
mentions Item, Tag or NBT filters, a destination selection, and whitelist/blacklist modes;
those are that quest's terms, not a promise that every upgrade exposes every option.

**First test (judgement).** Use a disposable item and spare inventories, check extraction
at the source and acceptance at the destination, then add one filter at a time. Test the
allow/deny direction with both a wanted and an unwanted item before connecting valuable
stock. Do not connect a disposal destination while testing.

## 2. Mekanism — use the machine's side configuration too

These entries are in **Mekanism**, not identically named entries in Basic Logistics.
The **Mekanism Logistics** quest depends on `4B35C01F5D0AAC58`; the three transport
quests below each depend on Mekanism Logistics, not on each other.

| Verified quest title | Quest id | Task / role |
|---|---|---|
| **Mekanism Logistics** | `5E116409DC7D30BB` | `mekanism:configurator`; the Configurator explanation |
| **Logistical Transporters** | `60ECCCAB66AAC05D` | filtered task accepting Basic through Ultimate logistical transporters; items/blocks |
| **Mechanical Pipes** | `33C69B5934BE4D64` | filtered task accepting Basic through Ultimate mechanical pipes; fluids |
| **Pressurized Tubes** | `3AF1DC02E9A0010C` | filtered task accepting Basic through Ultimate pressurized tubes; chemicals |

The Configurator description says holding Shift and scrolling changes its mode; using
it on pipes changes push/pull/both and on ports sets inputs and outputs. Read the mode
before interacting: its Wrench mode is described as dropping Mekanism machines/blocks,
not as a harmless generic connection toggle.

Logistical Transporters explicitly says, in quest text:

> They'll need to be set to Auto-Eject to Output Items.

That sentence refers to the machine's Side Configs. A pipe touching a machine is not by
itself proof that the machine is configured to output. Mechanical Pipes says it moves
fluids; Pressurized Tubes names chemicals, pigments and infuse types, and also points to
Side Configs and Auto-Eject. This page does not infer a particular machine's side colors,
port layout, or which substances that machine can expose. Inspect its actual GUI and JEI.

## 3. LaserIO — paired cards, not just connected nodes

Back in **Basic Logistics**, these quests each depend on **Laser IO**. The node and
filter entries have no explicit quest title; their labels below come from task items.

| Verified quest title (or explicit untitled marker) | Quest id | Task item |
|---|---|---|
| **Laser IO** | `5F1218CF8EFC607B` | `laserio:logic_chip`; no dependencies |
| Laser Node *(no explicit title)* | `5C0F6B1C93A52113` | `laserio:laser_node` |
| **Item Card** | `4C41FD926F31180B` | `laserio:card_item` |
| **Fluid Card** | `1C70D739CE464E25` | `laserio:card_fluid` |
| Basic Filter *(no explicit title)* | `47A2BEFB11F4D581` | `laserio:filter_basic` |

The node description tells the player to connect two nodes with the wrench by Shift
Right Clicking the first and Right Clicking the second, then put cards in the slots for
the correct direction. Item Card describes an **Extract** card at the source side and an
**Insert** card at the destination side. Fluid Card says the same pair is needed for tanks:

> No, it doesn't move Sources of Fluid in or out of the World.

The Basic Filter description distinguishes whitelist/allow from blacklist/deny and offers
NBT matching (its examples include enchantments and durability). Verify the installed
filter UI; do not assume a plain item-name match preserves those distinctions. Connected
nodes alone do not demonstrate that a card is present, on the correct face, or in the
correct mode. Start with one pair before adding more destinations (*judgement*).

## 4. Integrated Dynamics — importer, interface, cables, variable card

Also in **Basic Logistics**. **Integrated Dynamics** has no dependencies. Both importing
quests depend on **both** the cable quest and the variable-card quest; neither importing
quest depends on the other.

| Verified quest title (or explicit untitled marker) | Quest id | Task items / dependencies |
|---|---|---|
| **Integrated Dynamics** | `6E05B62A40D5A891` | `integrateddynamics:wrench` |
| Logic Cable *(no explicit title)* | `6112956E19017D2D` | `integrateddynamics:cable`; depends on Integrated Dynamics |
| Variable Card *(no explicit title)* | `03C40D6A5D722543` | `integrateddynamics:variable`; depends on Integrated Dynamics |
| **Item Importing** | `6F152402756DA35E` | `integratedtunnels:part_importer_item` and `integratedtunnels:part_interface_item` |
| **Fluid Importing** | `034F2CDF0830254B` | `integratedtunnels:part_importer_fluid` and `integratedtunnels:part_interface_fluid` |

Item Importing puts the importer on the source inventory, the interface on the second
inventory, connects them with Logic Cables, then puts a Variable Card in the importer.
Fluid Importing describes the corresponding tank-to-tank setup and says:

> Does not place or take Fluid Sources from in the world, it only moves Fluids from one Tank to another.

This is the importer-to-interface route actually described in this chapter, not a claim
that every Integrated Tunnels network must use this exact design. The quest's large
transfer-limit claims are not a measured throughput guarantee; no rate is recommended
here. Start with a small transfer limit while testing (*judgement*).

## 5. A stalled-transfer checklist (judgement, not quest requirements)

Work through one link at a time, with spare storage available:

1. **Source and destination:** is anything available to move, and can the destination
   accept it? Temporarily use spare inventories/tanks to isolate a machine-specific issue.
2. **Resource type:** items, fluids, energy and chemicals need the corresponding transport.
   A fluid pipe is not a chemical tube; use the machine display and JEI rather than guessing.
3. **Extraction and insertion:** check the configured source connection and destination
   face. For Mekanism, inspect machine Side Configs and output Auto-Eject as well.
4. **Routing controls:** check filters, allow/deny mode and any redstone control exposed
   by the installed upgrade. For Pipez, remember the conflicting filter-tier text above.
5. **Network-specific parts:** LaserIO needs correctly sided Extract/Insert cards;
   the documented Integrated Dynamics route needs its importer, interface and Variable Card.
6. **Destination full:** add storage or stop production. Do not solve a valuable-output
   backlog by enabling voiding without deciding what may safely be lost.
7. **Only stops when you leave:** investigate chunk loading at both endpoints via
   `references/chunk-loading-guide.md`. A transport connection is not proof of chunk loading
   or permission to run while offline.
8. **Moves, but slowly:** measure the actual bottleneck before adding upgrades or replacing
   the whole network. `references/lag-fix-guide.md` separates FPS issues from ticking issues;
   quest opinions about pipe lag are not measured comparisons for your base.

## What this page deliberately does not tell you

- **Recipes, crafting costs or guaranteed transfer rates.** Read JEI, the live tooltip
  and quest entry; no throughput table is copied from older quest prose.
- **A universal best pipe or performance ranking.** The four routes are alternatives.
- **Every logistics mod.** Transfer Labels, Modular Routers, storage-network import/export,
  and more advanced logic deserve their own live quest entries; omission is not absence.
- **Cross-dimensional links, wireless ranges or chunk allowances.** No such capability
  is inferred from the existence of a cable, node or interface.
- **Machine-specific side colors, chemical compatibility or a minimum Pipez filter tier.**
  Those need verification in the installed version, not a guessed rule.

## Cross-references

- `references/automation-first-steps.md` — why transport is an early automation priority.
- `references/getting-started.md` — the first base and machines before a larger network.
- `references/key-mods.md` — short primers for the logistics mods.
- `references/progression.md` — the Logistics and Tech groups in the stage map.
- `references/storage-ladder.md` — where transported output can be stored.
- `references/autocrafting-guide.md` — processing patterns and returning machine output.
- `references/ore-processing-ladder.md` — the processing chains transport connects.
- `references/power-guide.md` — generation, energy transport and storage, not item routing.
- `references/chunk-loading-guide.md` — keeping both ends running while away.
- `references/lag-fix-guide.md` — investigate performance rather than assuming a pipe is best.
