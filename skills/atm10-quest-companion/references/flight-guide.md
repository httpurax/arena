# Flight in ATM10 — "when can I fly?" (verified quests, pack 8.2)

**What this page is.** The answer to the beginner question "when can I fly?" for **All the
Mods 10**: every flight item the quest book tracks — jetpacks, a tethered balloon, elytra
add-ons, the creative-flight upgrades, the Creative Jetpack — with what each quest's own
text says it does and the dependency chain that says *when* the book expects it. It names
the cheapest reliable path and says what the book does **not** contain. It is a *map of
the quest book*, not a crafting guide.

## The short answer

1. **You can fly in the early game — with a jetpack.** The standalone **Tips and Tricks**
   chapter has an **Iron Jetpacks** quest with **no dependencies** that asks for the *Wood*
   jetpack, and a **Charging Gadgets** quest — also dependency-free — for a Charging
   Station that makes FE from *"Furnace Fuel"*. The jetpack flies on FE, and *"yes you will
   drop if you run out of Energy"*. That pair is the cheapest reliable path in the book
   *(judgement: no other wearable, go-anywhere flight item has a quest without
   prerequisites — the balloon below is tethered, the bee chestplates only hop — and the
   pack builds the first tier around planks; the full recipe is JEI's)*.
2. **Creative-style flight comes early only on a leash.** XyCraft's *"Up!"* quest calls its
   Balloon on a Stick *"an early and restrictive source of Creative Flight"* — go too far
   and *"you'll get detached and fall"*.
3. **Unrestricted creative flight is a mid-to-late goal** *(judgement, read off the chains
   below)*: Just Dire Things' Flight upgrade (it only fits the Eclipse Alloy chestplate,
   which comes after the Warden) or the Advanced AE Quantum Armor's flight card; later
   Draconic Evolution's Draconic Flight Module. The MekaSuit's Gravitational Modulating
   Unit is star-tier, and the Creative Jetpack comes after the star.
4. **Not in the 8.2 book:** an Angel Ring, a flight totem, or a quest for the vanilla
   Elytra — see *Not in the 8.2 book* at the end.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, component, dependency, reward, and quoted sentence
below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/*.snbt` | every quest named here: task items and their components (which jetpack tier a task wants), `dependencies`, rewards, `optional` flags |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, and every description quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapter titles |
| `config/ironjetpacks/jetpacks/*.json` | the pack's 17 Iron Jetpacks tiers: `name`, `tier`, `disable`, `creative`, `curios`, `craftingMaterial`, `capacity`, `usage` |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (489 mods) — and the absence of any angel-ring mod |
| `config/bcc-common.toml` | `modpackVersion = "8.2"` |

**How it was searched.** All 66 chapter files and their English lang files were parsed
with the skill's own stdlib reader (`scripts/snbt.py`). Task item ids were searched for
`elytra`, `jetpack`, `flight`, `angel`, `wing`, `glider`, and `levitat`; titles, subtitles,
and descriptions for *fly / flying / flight / elytra / jetpack / angel ring / wings /
glide / levitate / hover / soar*. Every hit was read, mobs that merely fly were dropped,
and each remaining quest's `dependencies` were followed back to its chapter's root.
"Absent" on this page means *searched for and not found* in that snapshot.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids, components, and counts are quoted from the config, never invented.** A
  count appears only where the config states one.
- **No recipes.** The quest config lists *what a quest wants*, never *how to craft it*;
  the jetpack config names each tier's `craftingMaterial`, the material a tier is built
  around, not its recipe. Every "how" on this page is a quote from that quest's own
  description, marked as such, or a pointer to JEI.
- **Approximate means approximate.** *When* a player gets somewhere is a judgement read off
  the dependency chains and marked *(judgement)*. Energy, fuel, flight speed, and tether
  range are not in the quest config and are not given here.
- **Titles are the config's.** Many flight entries carry no title (Just Dire Things'
  upgrades, Ars Nouveau's glyphs and rituals, PneumaticCraft's upgrades, the Advanced AE
  cards). They are marked *(no title in the config)*, with the subtitle where the config
  gives one — the book then shows the task item's own name. Do not present a derived name
  as a verified title.
- **Quests guide, they do not gate.** The pack's Welcome chapter: *"In this modpack, quests
  are optional. Mods are not gated behind completing any quests!"* A dependency chain below
  is the book's order, not a lock on the recipe.
- **Nothing here was invented, and nothing is added from memory.** A flight item that is
  not on this page is not tracked by the 8.2 book: the answer is "look it up in JEI", never
  a plausible-sounding guess.

## The ladder at a glance

| Roughly when *(judgement)* | Verified quest — chapter | Task item (config) | The quest's own words | What the book puts in front of it |
|---|---|---|---|---|
| Early game | **Iron Jetpacks** — Tips and Tricks | `ironjetpacks:jetpack`, component `ironjetpacks:jetpack_id` = `ironjetpacks:wood` | *"They will use FE to fly"* | nothing — no dependencies |
| Early game | *(no title in the config)*, subtitle *"Up!"* — XyCraft | `xycraft_machines:stake` | *"an early and restrictive source of Creative Flight"* | nothing — one of the chapter's four starting quests |
| Early tech | **Jetpack**, subtitle *"Requires Hydrogen to Work!"* — Mekanism | `mekanism:jetpack` | *"it requires Hydrogen as Fuel instead of Energy!"* | *Mekanism → Osmium → Metallurgic Infuser → Infused Alloy → Power! → Chargepad* |
| Mid tech | *(no title in the config)*, subtitle *"Max: 1"* — PneumaticCraft | `pneumaticcraft:jet_boots_upgrade_1` | *"Allows you to fly like Iron Man."* | *Pneumatic Armor* — 24 quests upstream |
| Mid, after the Warden | *(no title in the config)* — Just Dire Things | `justdirethings:upgrade_flight` | *"Grants the player creative flight."* | *Armor Upgrades*; only the Eclipse Alloy chestplate takes it |
| Mid to late tech | *(no title in the config)*, subtitle *"Creative Flight"* — Extended & Advanced AE | `advanced_ae:flight_card` | no description; the armor's own quest lists *"Flight, Night Vision, and even the ability to recharge."* | *Upgrades for Quantum Armor* — 6 quests upstream |
| Late | **Draconic Flight Module** — Draconic Evolution | `draconicevolution:item_draconic_flight` | *"Creative Flight to be more exact."* | *Modules! → Wyvern Flight Module*, plus a chestplate |
| Endgame, star tier | **Gravitational Modulating Unit**, subtitle *"Bodyarmor"* — Mekanism: Reactors | `mekanism:module_gravitational_modulating_unit` | *"Literally just Creative Flight."* | *Modification Station*; the MekaSuit Bodyarmor it goes in has 17 quests upstream |
| After the star | **Creative Jetpack** — Chapter 4: Creative | `ironjetpacks:jetpack`, component `ironjetpacks:jetpack_id` = `ironjetpacks:creative` | *"you'll neever need to worry about that again!"* | *Fully Automated ATM Star* |

"Quests upstream" counts every quest the entry transitively depends on in the config — how
far into its chapter it sits, not what it costs.

## 1. The cheapest reliable path: Tips and Tricks

**Tips and Tricks** is a standalone chapter (no chapter group, 23 quests; the skill files
it under `early-game`). Two of its quests are all a first flight needs, and neither has a
dependency:

| Verified quest title | Task item (config) | Mod (modlist) |
|---|---|---|
| **Charging Gadgets** | `charginggadgets:charging_station` | Charging Gadgets 1.14.1 |
| **Iron Jetpacks** | `ironjetpacks:jetpack` with `ironjetpacks:jetpack_id` = `ironjetpacks:wood` | Iron Jetpacks 8.0.11 |

What their own text says:

- **Charging Gadgets** — *"The Charging Station is a very helpful Early Game Block."* …
  *"Either Pipe in Energy or use Furnace Fuel to make Energy in the form of FE."* … *"Then,
  you can put any Item that needs charging into the Right most Slot."* Its reward includes
  a Basic Energy Cube (`mekanism:basic_energy_cube`) that the config hands over
  pre-charged.
- **Iron Jetpacks** — *"To start making them you'll need to start with a Wood Jetpack!
  This can be upgraded all the way to a Creative Jetpack."* … *"They all can be placed in
  your Chestplate Slot, or Back Curio, or Curio Curio."* … *"All of them also need FE to
  work, you can use any Item Charger to charge them! They will use FE to fly and yes you
  will drop if you run out of Energy."*
- **Controls, as the quest prints them** (players can rebind keys): *"To fly you'll need to
  turn on your Engine (V), then when you hold Space you'll fly up and drop when you let
  go."* Hover is *"(Unbinded)"* — no default key — and holds you *"at the same altitude;
  being able to go higher with (Space) and lower with (Shift)"*. Throttle is *"(,)"* down
  and *"(.)"* up.

Both feed the chapter's capstone, *(no title in the config)*, subtitle *"Complete all the
tips!"*.

**Why this is the recommendation** *(judgement)*: it flies anywhere, its one limit is
charge, nothing in the book stands in front of it, and the Wood tier's `craftingMaterial`
in `config/ironjetpacks/jetpacks/wood.json` is `tag:minecraft:planks`. What else the
jetpack's recipe needs is JEI's to show — do not recite it from memory.

**Keeping it charged.** Besides the Charging Station, the book itself names these item
chargers:

- Basic Power's **Mekanism: Energy Cubes** — the Basic Energy Cube *"can charge items
  inside of the interface!"* (the same cube *Charging Gadgets* hands out).
- Basic Power's **Flux Networks** — *"You can even charge your Jetpacks while you are
  flying with this mod."* — and its **Wireless Charging** quest (the Flux Controller's
  "Wireless Charging" tab).
- Mekanism's **Chargepad** (`mekanism:chargepad`), the quest just before Mekanism's own
  *Jetpack*.

### The jetpack ladder (pack config)

`config/ironjetpacks/jetpacks/` defines 17 jetpacks. None is switched off (`"disable":
false` in every file), and every one can be worn as a Curio (`"curios": true`):

| `tier` | Jetpacks |
|---|---|
| 0 | wood |
| 1 | stone, copper |
| 2 | iron, bronze, silver |
| 3 | gold, electrum, invar, steel |
| 4 | diamond, platinum |
| 5 | emerald |
| 6 | allthemodium |
| 7 | vibranium |
| 8 | unobtainium |
| -1 (`"creative": true`) | creative |

Across tiers 0–8, a higher `tier` always has a larger `capacity` and a larger `usage` in
these files — more charge held, more spent. The quest says the versions *"each work all
the same"*; which earlier jetpack a tier's recipe consumes is JEI's to show.

## 2. Early but leashed: XyCraft's balloon

*(no title in the config)*, subtitle *"Up!"* — task `xycraft_machines:stake` (XyCraft
Machines 0.7.53), one of the four XyCraft quests with no dependencies. Its text in full:
*"The Balloon on a Stick is an early and restrictive source of Creative Flight."* …
*"Place down the stick and you'll be attached to a balloon! Double touch space to start
Flying just not too far. Go too far and you'll get detached and fall."* Its reward is a
Levitation potion (`minecraft:potion` carrying `apothic_attributes:levitation`) and 50 XP.

*(Judgement)* Good for building tall around one spot, not for travel. The tether's range
is not in the config — test it in-game before trusting a drop to it.

## 3. Mekanism's hydrogen jetpack

**Jetpack**, subtitle *"Requires Hydrogen to Work!"* — `mekanism:jetpack` (Mekanism
10.7.19), at the end of a six-quest chain: *Mekanism → Osmium → Metallurgic Infuser →
Infused Alloy → Power! → Chargepad → Jetpack*. Its text: *"The Mekanism Jetpack works
similar to Iron Jetpacks just with different Modes and it requires Hydrogen as Fuel
instead of Energy!"* … *"Funny enough the Electrolytic Separator also has Hydrogen when it
has Oxygen!"* Modes switch on *"(G)"*: Regular, Hover, Vector, Disabled. Its reward is a
Basic Chemical Tank (`mekanism:basic_chemical_tank`) pre-filled with `mekanism:hydrogen`.

*(Judgement)* An alternative for a player already running Mekanism, not a cheaper first
flight than the Wood jetpack.

## 4. Elytra and gliding

**No quest asks for a vanilla Elytra.** `minecraft:elytra` appears nowhere in the 8.2
quest config — not as a task, a reward, or an icon — so the book never says where to find
one, and neither does this page. The book still assumes you have one in places:

| Verified quest title — chapter | Task (config) | What the quest says |
|---|---|---|
| **Ignitium Elytra Chestplate** — Cataclysm | `cataclysm:ignitium_elytra_chestplate` | *"Just combine an Ignitium Chestplate with an Elytra... that simple!"* — after *Ignitium Armor* and *Mechanical Fusion Anvil*; *Ignitium Armor* says its ingot is *"dropped from the Ignis"* |
| **Soul Elytra** — Deeper and Darker | `deeperdarker:soul_elytra` | *"works just like a normal Elytra, just now with more Durability and Armor Points!"*; crafting one starts from *"an Elytra"* |
| **Ancient Hoops** — The Bumblezone | structure `the_bumblezone:ancient_hoops` | *"Looks like a great place to use the Elytra at!"* |
| **Allthemodium Armor** — Chapter 2: Allthemodium | any Allthemodium armor piece | the helmets give *"no Elytra Damage"* |

**Gliding without giving up your chestplate** — upgrades that add elytra flight to armor:

| Verified quest — chapter | Task item (config) | The quest's own words |
|---|---|---|
| **Elytra Unit**, subtitle *"Bodyarmor"* — Mekanism: Reactors | `mekanism:module_elytra_unit` | *"Elytra or MekaSuit Bodyarmor... Why not both?"* |
| *(no title in the config)*, subtitle *"Max: 1"* — PneumaticCraft | `pneumaticcraft:elytra_upgrade` | *"Allows you to use an Elytra while still having your Pneumatic Chestplate on."* |
| *(no title in the config)* — Just Dire Things | `justdirethings:upgrade_elytra` | *"Provides the player with an Elytra"*; valid on the Celestigem and Eclipse Alloy chestplates |
| **Wyvern Flight Module** — Draconic Evolution | `draconicevolution:item_wyvern_flight` | *"With this on your Chestplate you can Glide! As if you were using an Elytra (But without cost of Armor)."* |

**Gliding without an elytra:** Relics' **Kinetic Belt** (subtitle *"Not all relics are
meant to keep you grounded..."*; *"Hidden within the mysterious dungeons of the End"*; its
*Gliding* ability works *"By holding the jump key"*), and Ars Nouveau's *(no title in the
config)* quest for `ars_nouveau:glyph_glide`, which hangs off an untitled checkmark quest
on Tier 3 glyphs (*"Tier 3 Glyphs require 10 levels of experience to be made. They also
require an Archmage Spell Book."*). Silent Gear has a *(no title in the config)* quest for
`silentgear:elytra_blueprint` with no description — what it builds is JEI's to show.

## 5. Short hops and rides, not sustained flight

- **Valkyrie Armor** — The Aether, optional, after *Silver Key*: *"When wearing all 5 parts
  of it you can hold Space to Fly! Only for a short time though."*
- The Bumblezone's bee chestplates — *(no title in the config)*, tasks
  `the_bumblezone:bumble_bee_chestplate_1` and `the_bumblezone:bumble_bee_chestplate_2`:
  *"While wearing it you can hold Space Bar to fly for a little."*
- Ars Nouveau's *(no title in the config)* quest for `ars_nouveau:belt_of_levitation`
  (after *Enchanting Apparatus*): *"This belt allows you to levitate. To activate, just
  sneak while in the air, either while falling or from jumping."*
- Artifacts' **Cloud in a Bottle** (subtitle *"Belt"*): a double jump, not flight.
- **Mounts that fly** — Ice and Fire's **Rule the Skys with the Hippogryph** (advancement
  `iceandfire:iceandfire/tame_hippogryph`; *"When Flying you can use Space Bar to Fly up"*),
  **Taming the Amphithere**, and **Commanding your Dragon**; The Bumblezone's **Beehemoth**
  (*"more similar to a Wild Flying Horse"*). The skill files both chapters under `endgame`
  (Exploration group).

## 6. Mid-game creative flight: Just Dire Things or Advanced AE

The book does not order these two against each other *(judgement: pick the line you
already run)*.

### Just Dire Things — the Flight upgrade on an Eclipse Alloy chestplate

- **The upgrade:** *(no title in the config)*, task `justdirethings:upgrade_flight` (Just
  Dire Things 1.5.7) — *"Ability Type: Passive"*, *"Grants the player creative flight."* It
  hangs off **Armor Upgrades**, which sits behind the blank-upgrade quest and
  **Ferricore**.
- **The chestplate:** each JDT armor quest lists its *"Valid Upgrades"*. Only the Eclipse
  Alloy chestplate's list (`justdirethings:eclipsealloy_chestplate`) includes *Flight*; the
  Celestigem chestplate's includes *Elytra*; the Ferricore and Blazegold chestplates list
  neither.
- **What that means for *when*:** **Eclipse Alloy** is *"acquired by performing Goo Spread
  on Netherite Blocks using tier four goo"*, and the tier-four goo quest says *"Shadowpulse
  Goo is the fourth and final tier of goo added by JDT and requires Ancient City and Warden
  materials to craft."* So: after the Warden (Chapter 1's *Kill The Warden*; see
  `boss-checklist.md`) and with Netherite blocks to spare.
- **Applying it:** *"The smithing table is used to apply upgrades to JDT tools and
  armor."* Armor abilities are toggled in the configuration menu — *"Use a JDT tool or wand
  to open the menu and click on your armor to configure the abilities of that armor
  piece."*

### Advanced AE — the Quantum Armor's flight card

**ME System As Armor: The Quantum Armor** (Extended & Advanced AE; tasks
`advanced_ae:quantum_helmet`, `advanced_ae:quantum_chestplate`,
`advanced_ae:quantum_leggings`, `advanced_ae:quantum_boots`; Advanced AE 1.6.12-1.21.1)
says its upgrades include *"Flight, Night Vision, and even the ability to recharge."* The
chain, in dependency order:

*Extended & Advanced AE → Advanced AE → Reaction Efficency: The Reaction Chamber → Quantum
Ingredients → ME System As Armor: The Quantum Armor → Upgrades for Quantum Armor →*
*(no title in the config)*, subtitle *"Creative Flight"* (`advanced_ae:flight_card`) →
*(no title in the config)*, subtitle *"No Flight Drift"* (`advanced_ae:flight_drift_card`).

*Upgrades for Quantum Armor* (`advanced_ae:quantum_upgrade_base`) says to *"open the
Quantum Armor Configuration Menu by pressing its respective keybind (N by default)."* The
same armor also appears in Basic Armor as an optional quest with no dependencies, **Quantum
Armor (AE2)**.

## 7. Late: Draconic Evolution's flight modules

*Modules! → Wyvern Flight Module → Draconic Flight Module → Chaotic Flight Module*
(`draconicevolution:item_wyvern_flight`, `draconicevolution:item_draconic_flight`,
`draconicevolution:item_chaotic_flight`; Draconic Evolution 3.1.4.633):

- **Wyvern Flight Module** — gliding: *"I don't like to call it flying, rather 'falling
  with style'."*
- **Draconic Flight Module** — *"Okay now this ones give both Gliding and actual Flying,
  Creative Flight to be more exact."*
- **Chaotic Flight Module** — no description in the config.

The modules go on a chestplate: **Wyvern Chestplate** (after *Wyvern Tier*), **Draconic
Chestplate** (after *Draconic Tier*), **Chaotic Chestplate** (after *Chaotic Tier*). Which
module fits which item is shown in-game — *Modules!*: *"The lowest button on the right will
show what Modules can be applied to the Item you are holding."* The chapter starts at
**Draconic Evolution**, whose ore *"spawns in all (Vanilla) Dimensions but the most is in
the End!"* The skill files the chapter under `endgame`.

## 8. Endgame: the MekaSuit's Gravitational Modulating Unit

All in Mekanism: Reactors, all subtitled *"Bodyarmor"*:

| Verified quest title | Task item (config) | The quest's own words |
|---|---|---|
| **Gravitational Modulating Unit** | `mekanism:module_gravitational_modulating_unit` | *"Literally just Creative Flight."* … *"yes it will use Energy to Fly!"* |
| **Gravitational Modulating Additional Unit** | `gmut:module_gravitational_modulating_additional_unit` (Gravitational Modulating Additional Unit 6.4) | *"Both will need to be Installed to use them!"* … *"You can ascend faster! And even Fly always!"* |
| **Jetpack Unit** | `mekanism:module_jetpack_unit` | *"You won't be able to use this Unit while you have the Gravitational Modulating Unit on."* |
| **Elytra Unit** | `mekanism:module_elytra_unit` | *"Why not both?"* |

**The gate.** In the graph the module quests hang off **Modification Station** alone, but
every one goes into **MekaSuit Bodyarmor** — and that quest sits behind a *(no title in
the config)* quest for `mekanism:pellet_antimatter`, which needs **Super-Critical Phase
Shifter** (the SPS): 17 quests upstream, through fission, polonium, and plutonium. The
Bodyarmor's own text calls it an upgrade to the Unobtainium chestplate and adds: *"It will
need a few other Items in order to upgrade it though, like an Antimatter Pellet, Polonium
Pellets, and even an Ultimate Induction Cell!"*

**Star tier.** Chapter 3: The ATM Star tracks the same module in its own *(no title in the
config)* quest — *"This Module, when put into the MekaSuit Chestplate, will give you
Creative Flight. You only need some of the most expensive Items in the game to craft it!"*
— as an input of **Nexium Emitter**, one of the star's components (see
`atm-star-checklist.md`).

## 9. After the star: the Creative Jetpack

Chapter 4: Creative's **Creative Jetpack** — task `ironjetpacks:jetpack` with component
`ironjetpacks:jetpack_id` = `ironjetpacks:creative` — has one dependency, **Fully
Automated ATM Star**. Its text: *"Don't you hate when you run out of Energy in your
Jetpack? Well you'll neever need to worry about that again!"* (sic) … *"You might need to
make every Jetpack before it, an ATM Star, plus more expensive Items but hey it is worth
it!"* In the jetpack config the creative tier is `"creative": true` with
`craftingMaterial` `"null"`. `creative-checklist.md` calls this task id generic; the
component above is where the entry pins the creative tier.

## Not in the 8.2 book (searched, and absent)

- **Angel Ring.** No quest, task, or text names one, and no angel-ring mod is in
  `modlist.json`. The only "angel" items in the config are Utilitarian's Angel Block
  (`utilitarian:angel_block`, a quest reward), a Construction Stick template
  (`constructionstick:template_angel`), and the Aether's Angelic Stone
  (`aether:angelic_stone`) — none of them a ring, none described as giving flight.
- **Flight totems.** No totem in the book grants flight. The totems it does name are
  `artifacts:chorus_totem`, `minecraft:totem_of_undying`,
  `justdirethings:totem_of_death_recall`, and `undergarden:denizen_totem`.
- **A vanilla Elytra quest.** `minecraft:elytra` appears nowhere in the quest config.
- **A fly command.** No quest text mentions one. Whether a server grants flight by command
  is that server's setup, not the quest book's.
- **Flight from the other magic chapters.** Beyond Ars Nouveau, no magic chapter (Iron's
  Spells 'n Spellbooks, Occultism, EvilCraft, Theurgy, Mahou Tsukai, Forbidden & Arcanus,
  Nature's Aura, Neo Vitae, Apothic Enchanting) tracks a flight item.
- **What the Ritual of Flight does.** Ars Nouveau's *(no title in the config)* quest for
  `ars_nouveau:ritual_flight` has no description. It hangs off the untitled quest for
  `ars_nouveau:ritual_brazier`, which says to *"check out each of them using the Worn
  Notebook"* — read it there.

## Cross-references

- `progression.md` — the stages; this page shows flight starts in the early game.
- `key-mods.md` — what Mekanism, Ars Nouveau, and Just Dire Things are for.
- `boss-checklist.md` — the Warden (gates Just Dire Things' tier-four goo) and the Ignis
  (drops the Ignitium ingot).
- `atm-star-checklist.md` — the Nexium Emitter and the rest of the star.
- `creative-checklist.md` — the Creative Jetpack among Chapter 4's eleven creative items.

## What this page deliberately does not tell you

- **No recipes**, beyond quoted quest text and the Wood tier's `craftingMaterial`.
- **No numbers** for energy, fuel, flight speed, or tether range. The jetpack files'
  `capacity` and `usage` values are the mod's internal figures; they are compared above,
  not restated as gameplay advice.
- **No elytra location**, because the book has none.
- **Keybinds** only as the quests print them; players rebind them.
- **No server-command advice.**
