# Item and fluid transport in ATM10: connect machines, configure extraction, and filter outputs

**What this page is.** The logistics companion to
`references/automation-first-steps.md`: how to stop carrying items and buckets between
machines, which chapter explains each transport system, and what to check when nothing
moves. It maps **Pipez**, **Mekanism**, **Laser IO**, and **Integrated Dynamics** to the
pack's own quests. These are **alternatives, not a mandatory progression ladder**.

*Short answer (judgement):* start with a small Pipez connection if you only need to move
items or fluids. If you already use another system, follow its branch instead of
rebuilding everything. Configure extraction, check the receiving machine's sides, then
add filtering. This is practical advice, not a quest requirement or a throughput ranking.

## Provenance — everything here was read, not remembered

Quest titles, quest ids, task items, dependencies, and quoted descriptions were read
from [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10), `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), **pack 8.2** according to `CHANGELOG.md` — the same snapshot as the
"8.x" stamp in `examples/progress.example.json`.

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/basic_logistics.snbt` | Pipez, Laser IO, Integrated Dynamics tasks and dependencies |
| `config/ftbquests/quests/lang/en_us/chapters/basic_logistics.snbt` | Their explicit English titles and operating descriptions |
| `config/ftbquests/quests/chapters/mekanism.snbt` | Configurator and transport tasks and dependencies |
| `config/ftbquests/quests/lang/en_us/chapters/mekanism.snbt` | Mekanism transport titles and side-configuration text |
| `CHANGELOG.md` | Pack version and date |

Minecraft `&` formatting codes are stripped from titles and quotes. The chapter keys
are `basic_logistics` (**Basic Logistics**) and `mekanism` (**Mekanism**).

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** If the player's
  installed book differs, his book wins; re-check it rather than treating 8.2 as current.
- **Never invent requirements, recipes, counts, item ids, or transfer rates.** Task
  items identify what the book tracks; they are not recipes or a complete build bill.
- **Untitled quests stay untitled.** A device named in a description is not necessarily
  the quest's explicit title. Tables mark these entries *No explicit quest title*.
- **Dependencies are quest links, not proof of mod gating.** A verified branch below
  describes book order, not a requirement to finish every preceding mod before building.
- **Recommendations and diagnosis order are approximate/judgement.** Keep that label
  when advising. This page promises neither a fastest system nor a frame-rate gain.
- **Fluid is not a synonym for every machine substance.** The book separately describes
  items, fluids, and Mekanism chemicals. Check the machine and JEI rather than assuming
  one pipe handles them all.

## The choices at a glance

| Situation | Verified book anchor | Recommendation (judgement) |
|---|---|---|
| A simple chest-to-machine or tank-to-machine link | Basic Logistics: **Pipez**, **Item Pipez**, **Fluid Pipez** | A small starter connection; configure the pulling side before expanding |
| Machines already using Mekanism transport | Mekanism: **Mekanism Logistics**, **Logistical Transporters**, **Mechanical Pipes** | Keep the existing system; inspect both pipe modes and machine side configs |
| Directional cards and selective routing | Basic Logistics: **Laser IO**, **Item Card**, **Fluid Card** | An alternative when explicit extract/insert cards suit the build |
| Importers, interfaces, and programmable settings | Basic Logistics: **Integrated Dynamics**, **Item Importing**, **Fluid Importing** | An alternative if you want Variable Card control; follow its chapter's setup |

The table is not a measured performance comparison. None of these branches requires a
digital storage network or an autocrafting CPU merely because those have other guides.

## 1. Pipez — a first connection and its filters

### Verified quest trail (`basic_logistics`)

| Explicit quest title | Quest id | Task item |
|---|---|---|
| **Pipez** | `2329AA0AFBEF1E13` | `pipez:wrench` |
| **Item Pipez** | `36836AD948F96B9F` | `pipez:item_pipe` |
| **Fluid Pipez** | `33433A443B65D252` | `pipez:fluid_pipe` |
| **Gas Pipez** | `2F4458E9921DEB86` | `pipez:gas_pipe` |
| *No explicit quest title* | `2A976D41F79C34B1` | `pipez:filter_destination_tool` |

**Verified dependencies:** the four entries after **Pipez** each depend directly on
**Pipez**. They are sibling branches, not Item → Fluid → Gas → filtering.

**The pack's own words.** **Pipez** says: “Attach the specific Pipe to where you want
to move items and use the Pipe Wrench to configure what side Pulls, Pushes, or doesn't
connect.” **Item Pipez** says: “It will move Items from one Inventory to another.”
**Fluid Pipez** describes moving fluids such as water and lava. **Gas Pipez** separately
describes Mekanism gas transport and directs the player to the machine or JEI when the
substance type is unclear. Do not treat a fluid pipe as a chemical pipe.

**Filtering, from the untitled entry.** Its description says Pipez filtering needs
“atleast an Advanced Upgrade” (the quest's spelling). With that upgrade, use Add to
filter by Item, Tag, or NBT. The description also explains configuring the destination
with the Destination Filter by shift-right-clicking an inventory, and selecting
Whitelist or Blacklist. The task is the destination tool, **not** an Advanced Upgrade
recipe, an instruction to install every upgrade tier, or an explicit quest title.

**What to do first (judgement).** Get one source and one destination working with the
correct pipe and configured pulling side. Then add a filter if needed. Do not diagnose
a large mixed factory by changing all its upgrades at once.

## 2. Mekanism — transport type and machine sides are separate checks

### Verified quest trail (`mekanism`)

| Explicit quest title | Quest id | Task item |
|---|---|---|
| **Mekanism Logistics** | `5E116409DC7D30BB` | `mekanism:configurator` |
| **Logistical Transporters** | `60ECCCAB66AAC05D` | `ftbfiltersystem:smart_filter` |
| **Mechanical Pipes** | `33C69B5934BE4D64` | `ftbfiltersystem:smart_filter` |
| **Pressurized Tubes** | `3AF1DC02E9A0010C` | `ftbfiltersystem:smart_filter` |

**Verified dependencies:** each of the three transport entries depends directly on
**Mekanism Logistics**. They are alternatives for different contents, not three
successive upgrades. The smart-filter tasks accept members of the corresponding
transport family across tiers; **they do not ask you to craft a generic smart filter**.
Consult the actual quest entry for the accepted items.

**The pack's own words.** **Mekanism Logistics** has subtitle *The Configurator* and
says: “If you use it on Pipes it will change if they Push, Pull, or Both.” It separately
explains setting port inputs and outputs. **Logistical Transporters** says:
“Logistical Transporters will move Items and Blocks from one Inventory to another!”
Its machine-configuration instructions identify *Side Configs* and say:
“They'll need to be set to Auto-Eject to Output Items.”

**Mechanical Pipes** says: “Mechanical Pipes will move Fluids.” **Pressurized Tubes**
describes chemicals, pigments, and infuse types separately from those fluids, and also
points to the machine's Side Configs and Auto-Eject. Those statements identify the
book's routing categories, **not** a guarantee that any tube can insert any substance
into any machine slot. Check the receiving machine's own settings and recipe in JEI.

**What to do first (judgement).** Identify the content type, inspect the transport's
push/pull mode, then inspect the connected machine's input/output sides and ejection.
A connected texture alone is not evidence that the machine is configured to accept
what you are sending. Do not prescribe a universal side color or a throughput number
from memory.

## 3. Laser IO — nodes, extract cards, and insert cards

### Verified quest trail (`basic_logistics`)

| Explicit quest title | Quest id | Task item |
|---|---|---|
| **Laser IO** | `5F1218CF8EFC607B` | `laserio:logic_chip` |
| *No explicit quest title* | `7BC8F50A89A3BE1A` | `laserio:laser_wrench` |
| *No explicit quest title* | `5C0F6B1C93A52113` | `laserio:laser_node` |
| **Item Card** | `4C41FD926F31180B` | `laserio:card_item` |
| **Fluid Card** | `1C70D739CE464E25` | `laserio:card_fluid` |
| *No explicit quest title* | `47A2BEFB11F4D581` | `laserio:filter_basic` |

**Verified dependencies:** all five entries after **Laser IO** depend directly on
**Laser IO**, not on one another. The wrench, node, and basic-filter entries have no
explicit English quest title; the device names are not replacement titles.

**The pack's own words.** The node entry says cards go into slots for the correct
direction. For more distant inventories it describes a second node, linked using the
wrench by shift-right-clicking one and right-clicking the other. **Item Card** says:
“Set one to Extract and put it on the side of the Laser Node you want to Import from.
Then set the other to Insert and put it to the side you want the Items to Export to.”

**Fluid Card** describes extract and insert cards between tanks and explicitly says it
does not move fluid source blocks into or out of the world. The untitled basic-filter
entry describes whitelist/blacklist and optional NBT matching. These controls are that
entry's description, not proof that every transport mod shares the same settings.

**What to do first (judgement).** Check node links, card directions, and Extract versus
Insert before adding overclockers or more destinations. Use the filter entry when you
need selected items rather than transferring the whole inventory. No transfer-rate or
maximum-distance guarantee is made here.

## 4. Integrated Dynamics — importers, interfaces, and Variable Cards

### Verified quest trail (`basic_logistics`)

| Explicit quest title | Quest id | Task item |
|---|---|---|
| **Integrated Dynamics** | `6E05B62A40D5A891` | `integrateddynamics:wrench` |
| *No explicit quest title* | `6112956E19017D2D` | `integrateddynamics:cable` |
| *No explicit quest title* | `03C40D6A5D722543` | `integrateddynamics:variable` |
| **Item Importing** | `6F152402756DA35E` | `integratedtunnels:part_importer_item`, `integratedtunnels:part_interface_item` |
| **Fluid Importing** | `034F2CDF0830254B` | `integratedtunnels:part_importer_fluid`, `integratedtunnels:part_interface_fluid` |

**Verified dependencies:** the cable and variable entries each depend on
**Integrated Dynamics**; **Item Importing** and **Fluid Importing** each depend on
**both** of those untitled entries. The item and fluid routes are siblings.

**The pack's own words.** **Item Importing** says: “To get this working put the Item
Importer onto the Inventory you want Items pulled from.” It then describes putting
the Interface on the second inventory, connecting with Logic Cables, and placing a
Variable Card in the Importer. The variable entry describes changing settings through
the + button. Those device labels come from descriptions, not invented quest titles.

**Fluid Importing** uses the corresponding Fluid Importer and Fluid Interface between
tanks, with Logic Cables and a Variable Card. Its explicit limit: “Does not place or
take Fluid Sources from in the world, it only moves Fluids from one Tank to another.”

**What to do first (judgement).** Check source Importer, destination Interface, cable
connection, and Variable Card before attempting more complex logic. The quest's high
integer-limit language is not a measured sustainable transfer rate or a performance
promise; this guide intentionally gives no throughput recommendation.

## When nothing moves — a diagnostic order (judgement)

This is a suggested isolation sequence, **not** another quest dependency chain:

1. **What are you moving?** Item, fluid, or chemical? Match the route to the book's
   category. A tank-to-tank fluid route is not necessarily a world-fluid collector.
2. **Is extraction actually configured?** Check the Pipez pulling connection, Mekanism
   mode and Auto-Eject, Laser IO Extract/Insert cards, or Integrated Dynamics Importer
   and Variable Card for the branch you chose.
3. **Can the destination accept it?** Inspect the destination's input side, contents,
   and available space; use its quest entry and JEI for accepted inputs. Do not promise
   that arbitrary machines interoperate just because their pipes connect.
4. **Is a filter excluding it?** Inspect whitelist versus blacklist, destination
   selection, and NBT matching where that system documents them. Test with a known
   intended item; do not discard stored items or dismantle a working factory to test.
5. **Does it stop only when you leave?** Use `references/chunk-loading-guide.md`.
   Transport is not chunk loading and does not remove player-nearby requirements.
6. **Does it move, but the game stalls?** Use `references/lag-fix-guide.md` to separate
   FPS from TPS symptoms. The logistics quest text warns about mass pipe use, but it
   does not establish a benchmark; never promise that swapping systems fixes lag.

If those checks do not explain it, ask for the pack version, source and destination
machines, transported content, and visible side/card/filter settings. Say what is
unverified rather than supplying a plausible recipe, universal setting, or command.

## Cross-references

- `references/automation-first-steps.md` — where transport fits among first automations.
- `references/ore-processing-ladder.md` — the processing machines these links can serve.
- `references/storage-ladder.md` — storing output, including digital-network choices.
- `references/autocrafting-guide.md` — teaching networks recipes is a separate problem.
- `references/power-guide.md` — generation and energy transport, outside this page's scope.
- `references/chunk-loading-guide.md` — keeping the relevant chunks ticking.
- `references/lag-fix-guide.md` — diagnosing performance without promising gains.

## What this page deliberately does not tell you

- **Recipes, costs, layouts, coordinates, or keybinds.** JEI and the installed quest
  book supply version-specific instructions; task items are not recipes.
- **Transfer rates, energy budgets, or a fastest mod.** No remembered tier numbers or
  benchmarks; any such question needs the player's version and a verified source.
- **A mandatory mod order.** The four branches are alternatives; recommendation order
  is judgement, and a dependency is not a universal crafting gate.
- **Guaranteed wireless or cross-dimensional transport.** This guide verifies only
  the connections described above, not arbitrary remote endpoints or automatic loading.
- **Every logistics mod or every quest.** Energy, redstone, heat, advanced logic, and
  other branches exist; this is the item/fluid starter map, not an exhaustive chapter.
- **Unverified fixes.** If the references do not establish a behavior, say to check the
  quest entry / JEI and the player's own settings, rather than inventing it.
