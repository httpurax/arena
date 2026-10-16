# Teleportation in ATM10 — get home and fast-travel (pack 8.2)

**What this page is.** The answer to *"How do I get home or travel between places I've
already found?"* in **All the Mods 10**. It separates the Welcome chapter's home
commands, Waystones, the Allthemodium Teleport Pad, Mekanism's powered network, and a
few Just Dire Things alternatives. The dimension guide covers **where to go next**;
this page covers **how to return or move between known places**. It is a map of the
pack's quest text and shipped settings, not a recipe or a promise about a server.

**Short answer (judgement about which to use first):** set a home with `/sethome base`
and return with `/home base`. Look for a Waystone when you want another repeatable
stop. A **Teleport Pad** goes to an ATM dimension, not to a named home. For a powered
network between built destinations, follow Mekanism's **Custom Portals!** and
**Portable Teleporter** quests. These routes are alternatives, not unlocks of one
another; choose what your current book and server actually offer.

## Provenance — everything here was read, not remembered

The quest titles, ids, task types and items, dependencies, and quoted instructions below
come from [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), **pack 8.2** (`config/bcc-common.toml`: `modpackVersion = "8.2"`), the
same snapshot as the other verified guides and the `"8.x"` example progress file:

| Pack file at that commit | What it verifies |
|---|---|
| `config/ftbquests/quests/chapters/welcome.snbt`, `allthemodium.snbt`, `mekanism.snbt`, `justdirethings.snbt` | quest ids, item or dimension tasks, task counts and dependency links |
| `config/ftbquests/quests/lang/en_us/chapters/{welcome,allthemodium,mekanism,justdirethings}.snbt` | English quest/task titles and the instructions quoted below (formatting codes removed) |
| `config/waystones-common.toml` | Waystones' actual world-generation, cost, cooldown, pet and JourneyMap switches |
| `config/crash_assistant/modlist.json` | Waystones 21.1.45, FTB Essentials 2101.1.10, Mekanism 10.7.19, Just Dire Things 1.5.7 and JourneyMap 1.21.1-6.0.9 |
| `config/bcc-common.toml` | pack version `8.2` |

**These are different kinds of evidence.** The Waystones file describes what the pack
*configures*, not a Waystones quest or a recipe. The Welcome text points to a
**per-world** FTB Essentials serverconfig file; the pack repository does **not** ship
that world's settings. No command limit or cooldown can be read from this snapshot.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** If a player's
  version or server differs from pack 8.2, trust the live book and settings. Check JEI
  for recipes; do not turn a task item into a crafting instruction.
- **The book gates nothing.** The Welcome chapter says *"In this modpack, quests are
  optional. Mods are not gated behind completing any quests!"* A dependency below is
  the book's order, not a lock on using the mod.
- **Titles are verified, not guessed from items.** Welcome's *Useful Commands* is a
  **task title**, not a quest title. The Just Dire Things entries below have *(no title
  in the config)*; their item names are not substitute quest titles.
- **Timing and route choice are judgement.** The source records dependencies, not an
  early/mid-game clock. There is no verified `/back`, `/tpa`, command quota, Waystone
  location, cross-mod portal interchange, or automatic chunk loading here. Ask the
  player's server/quest book rather than inventing one.

## Choose the right kind of travel

| What you need | Start here | Do not confuse it with |
|---|---|---|
| Return to your own base | Welcome's `/sethome` → `/home` | `/spawn` (Overworld spawn) or `/rtp` (random location) |
| Revisit several discovered spots | Waystones, if you find or place them *(choice: judgement)* | A JourneyMap marker or a guaranteed Waystone in every village |
| Reach the Mining Dimension / The Other / The Beyond | Chapter 2's **Teleport Pad** | A general home or a portal to any chosen dimension |
| Connect built locations, including across dimensions | Mekanism **Custom Portals!**; later carry a **Portable Teleporter** | A destination that works without a powered Teleporter |
| Link two nearby points or return to a death site | Just Dire Things' untitled Portal Gun / Swapper / Totem quests *(choice: judgement)* | A server `/back` command or a permanent home |

## 1. First trip home: the Welcome chapter's commands

The **Welcome** chapter (`welcome`, 6 config quests, including one hidden authoring
entry) has an untitled quest `7658C1C663394E85` with the **task** title **Useful
Commands** (task `10A16F89D4AD238D`, type `checkmark`). It has no dependencies. Its
own text teaches:

| Command in the quest | The quest's explanation |
|---|---|
| `/sethome farm` → `/home farm` | Set a named home and teleport back to it; substitute your own name, e.g. `base`. |
| `/spawn` | Teleport to the spawn of your **Overworld**, not necessarily your base. |
| `/rtp` | *"Random Teleport"* to a random location in the world; this is exploration, not a return trip. |

**Do this before wandering (judgement):** set a home at the base, then use `/home base`
to return. The quest explicitly warns that these commands **have cooldowns and
limits**, without giving any numbers. It points singleplayer to
`saves/(name of save)/serverconfig/ftbessentials.snbt` and servers to
`world/serverconfig/ftbessentials.snbt`. Those are *live world* paths, not settings
shipped in this repository. If a command is unavailable or delayed, check the current
world/server configuration; do not promise that it works on every multiplayer server.

## 2. Waystones: repeatable stops, not guaranteed village loot

The pack ships **Waystones 21.1.45**. Unlike the Welcome commands, the following
facts come from `config/waystones-common.toml`, not a quest about Waystones:

| Setting (pack 8.2) | Shipped value | Safe reading |
|---|---|---|
| `spawnInVillages = "REGULAR"` | regular generation | The config's comment says **some** supported villages; not every village and not a loot-chest guarantee. |
| `chunksBetweenWildWaystones = 25` | approximate chunk spacing | Not a promised coordinate or one Waystone every 25 chunks. |
| `wildWaystonesDimensionAllowList` | `minecraft:overworld`, `minecraft:the_nether`, `minecraft:the_end` | Limits **wild generation** to these three dimensions; it does not say where a placed stone can be used. |
| `enableCosts = false` | XP costs off | The `warpRequirements` still list XP formulas, including a cross-dimensional rule, but they are **not an active XP toll** while costs are disabled. |
| `enableCooldowns = true` | cooldown support on | The listed `add_cooldown(inventory_button, 300)` is conditional on the inventory-button source; do not claim a 300-tick cooldown on every teleport. |
| `transportPets = "DISABLED"`; `transportLeashed = "ENABLED"` | pets off, leashed mobs on | Do not promise an ordinary pet follows; `entityDenyList` also contains `minecraft:wither`. |
| `journeyMap = true` | markers for **activated** Waystones | JourneyMap waypoints are markers, not proof that clicking any map marker teleports you. |

The same config has `inventoryButton = ""`; it does not say `"ANY"` or `"NEAREST"`.
Do not promise a particular inventory shortcut or exact UI sequence. **Practical
choice (judgement):** look for a Waystone on a visit to a village or while exploring,
then follow the in-game Waystones interface for activation and destinations. For a
recipe, ask JEI. If a server changes these settings, use its current config instead.

## 3. The Teleport Pad is for three ATM dimensions

Chapter 2: Allthemodium's **Teleport Pad** quest `07FDA46D83F8360D` asks for one
`allthemodium:teleport_pad` and follows **Allthemodium Ingot** (`201EE3566D4D3123`).
That ingot quest recommends making **two** pads for the Mining Dimension and The
Other; it is advice in the quest text, not a requirement to finish both routes.
The Pad quest itself says to **shift-right-click with both main and offhand empty**.

| Place the Pad in (quest title) | Quest id after **Teleport Pad** | Destination in the quest's text |
|---|---|---|
| **Overworld** | `2C4299D33D419AA0` | Mining Dimension (`allthemodium:mining`) |
| **The Nether** | `0CC0632E8276C787` | The Other (`allthemodium:the_other`) |
| **The End** | `2EDE91023F7924FB` | The Beyond (`allthemodium:the_beyond`) |

Those three follow-on quests have `dimension` tasks for `minecraft:overworld`,
`minecraft:the_nether`, and `minecraft:the_end` respectively; the **destination**
labels above come from their descriptions, not from those task payloads. For how to
reach each vanilla dimension or what to do in the destination, use
`references/dimension-guide.md`. **This Pad is not a named-home Waystone** and the
book does not say it opens an arbitrary dimension.

## 4. Built destinations: Mekanism's powered Teleporters

The **Mekanism** chapter provides two separate branches (quest order, **not** a claim
that completing a quest unlocks an item):

| Verified quest (id) | Immediate book dependency | Verified task / instruction |
|---|---|---|
| **Custom Portals!** (`7B0DFA55B4D8B16D`) | **Metallurgic Infuser** | 9 `mekanism:teleporter_frame` and 1 `mekanism:teleporter`; quest says the Teleporter Block needs power and a named network. |
| **Portable Teleporter** (`2EA0C74AE7366656`) | **Chargepad** | 1 `mekanism:portable_teleporter`; quest says charge it, right-click to set its owner, then choose a network and teleport to a **powered** Teleporter. |

For two fixed stops: the *Custom Portals!* quest says to assemble a Teleporter
structure, power its controller, and select the same named network on the other
Teleporter. Its text says travel works *"anywhere in any Dimension"* **as long as the
machine is made and powered**. Follow its in-game pictures and JEI for the structure
and recipes; do not substitute a guessed frame layout.

For a return trip without a second walk-through structure, carry the charged,
owner-set **Portable Teleporter** and select a network with a powered destination.
Its own text explicitly says *"you can't Teleport to the Portable Teleporter, it's an
Item"*. The portable quest follows **Chargepad**, **not** *Custom Portals!* in the
quest graph, even though its usefulness depends on a powered Teleporter to travel to.
The snapshot gives no general energy budget, range, or promise that an unloaded base
will remain ticking; see `references/power-guide.md` and
`references/chunk-loading-guide.md` for those distinct questions.

## 5. Other tracked travel tools (optional, later: judgement)

These entries belong to the **Just Dire Things** chapter. **None has a quest title in
the English config**; the table identifies them by quest id and task item instead:

| Untitled quest id / task item | What its own description says |
|---|---|
| `16E02F671FBE9148` — `justdirethings:portalgun` | A powered Portal Gun shoots two linked portals: left-click blue, right-click orange, shift-right-click clears both. |
| `4F9932477EDDCB8E` — `justdirethings:portalgun_v2` | An Advanced Portal Gun needs power **and portal fluid**; it can select encoded locations. The text calls `V` the **default** keybind for its menu — check Controls if rebound. |
| `0B9BBE2A764631BF` — `justdirethings:blockswappert1` | A Simple Swapper can teleport players (also items, blocks and mobs) above it to a linked swapper; its text says to use the Ferricore wrench to link them. |
| `27FD46A8C958D259` — `justdirethings:totem_of_death_recall` | A Totem of Death Recall is **one-time use** for teleporting back to the location of death; it is not a standing `/home` or a documented `/back` command. |

These are not early-game promises or verified substitutes for an ATM dimension
portal. Ask the quest entry and JEI for requirements; the item labels above are **not
invented quest titles**.

## If a teleport does not work

1. **Home command:** did you set that name with `/sethome`? The Welcome quest warns
   about cooldowns and limits; the world's FTB Essentials config or server rules win.
2. **Waystone:** generation is not guaranteed at a given village, and wild generation
   is configured only for the three vanilla dimensions. Check the live UI/config, not
   a remembered coordinate or inventory key.
3. **Teleport Pad:** check the dimension where it was placed and empty **both** hands
   before shift-right-clicking. It does not select a saved home.
4. **Mekanism:** check the named network and power at the **destination** as well as
   the charged Portable Teleporter. Nothing on this page promises remote chunk loading.
5. **Just Dire Things:** read the specific item quest; the advanced gun needs portal
   fluid, and the death-recall totem is consumable.

## Cross-references

- `references/first-hour-walkthrough.md` — Welcome and the opening quests in order.
- `references/getting-started.md` — the first-day checklist and getting set up.
- `references/dimension-guide.md` — how to enter dimensions and what is in them.
- `references/flight-guide.md` — moving around *within* a dimension.
- `references/chunk-loading-guide.md` — keeping machines running while away.
- `references/power-guide.md` — powering a tech base, not a portal recipe.

## What this page deliberately does not tell you

- No invented `/back`, `/tpa`, home count, cooldown length for FTB Essentials, or
  guarantee that a given server permits commands.
- No guaranteed Waystone in a particular village or modded dimension, no waystone
  crafting recipe, and no claim that every teleport costs XP or takes 300 ticks.
- No arbitrary Teleport Pad destination, Mekanism energy figure, Portal Gun range, or
  cross-mod portal compatibility. A teleporter is **not** a chunk loader.
- No coordinates, guessed recipes, or generic keybinds. Verify the current quest,
  Waystones interface, JEI, and the server's actual settings.
