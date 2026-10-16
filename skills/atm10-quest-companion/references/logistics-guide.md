# Logistics in ATM10 — how to move items, fluids, energy, and gas (verified quests, pack 8.2)

**What this page is.** The transport companion to `references/automation-first-steps.md` and
`references/storage-ladder.md`. The first ranks *item transport* third of the five things a
beginner should automate and stops there; the second covers where things end up once they stop
moving. This page is only about **the moving**: the four chapters of the pack's own
**Logistics** group — *Basic Logistics* (Pipez, Mekanism transport, the Integrated Dynamics
tunnel parts, LaserIO, and Transfer Labels), *Integrated Dynamics*, *Modular Routers*, and
*Pylons* — plus the transport quests in the *Mekanism* chapter that *Basic Logistics* assumes
you will read. For each option it answers the same three questions, in the pack's own words:
what the book says it is for, which item ids the book tracks, and what the book's own text
says about **lag** — the only ranking evidence the quest config offers. It is a map of the
quest book, not a plumbing tutorial: no recipes, no throughput maths, no layouts, no "best mod".

## The short answer

1. **Start with Pipez.** *Basic Logistics* opens with the quest **Pipez**, which the config
   describes as *"Pipez is the simplest Logistics Mod."* Five pipes hang off it —
   **Item Pipez**, **Fluid Pipez**, **Energy Pipez**, **Universal Pipez**, **Gas Pipez** — one
   quest each, each tasking one pipe and rewarding 16 of it.
2. **Already committed to Mekanism? Take its transport from this chapter and skip the Basic
   tier.** The five Mekanism quests inside *Basic Logistics* carry no title at all, task a
   `ftbfiltersystem:smart_filter`, and *reward* the **Advanced** tier:
   `mekanism:advanced_logistical_transporter`, `mekanism:advanced_mechanical_pipe`,
   `mekanism:advanced_universal_cable`, `mekanism:advanced_thermodynamic_conductor`,
   `mekanism:advanced_pressurized_tube` — 16 of each. The tier ladder itself lives in the
   *Mekanism* chapter, whose quest texts print the per-tier figures.
3. **Worried about lag? The pack ranks its own three answers for you, in parentheses.** The
   Pipez quest says *"(Can be laggy when used in mass, still not as laggy as Mekanism pipes
   though)."*, the Mekanism quest says *"(These can cause a bit of lag when used in mass so be
   careful with them)."*, and the Integrated Dynamics quest says
   *"(Least laggy pipe solution, these are recommended)."* Those three sentences are the only
   ordering the config states; anything beyond them is this skill's judgement.
4. **Want transport that also reads and thinks? Integrated Dynamics.** It gets its own
   chapter (28 quests, only 4 of them titled) on top of the tunnel parts in
   *Basic Logistics*, and it is the one whose shipped config actually publishes a rate:
   `energyRateLimit = 2147483647`, which is the "Integer Limit (Over 2 billion)" its quest text
   brags about.
5. **Want transport with no pipes at all? Modular Routers.** One block, a *Buffer*, and 30+
   modules; the chapter is 55 quests of modules, upgrades, augments and filters, ending in a
   *Sender Module MK3* that the text says ignores axis, line of sight, and dimension.
6. **Pylons is in the group and moves nothing.** Three of its five pylons keep mobs, players,
   and blocks out of an area; one harvests crops; one beams a potion effect at you. Say so
   plainly rather than pretending it is a pipe.
7. **Nothing else in the pack is quested for transport.** *Basic Logistics* never asks for an
   EnderIO or Logistics Networks item even though both jars ship, and the pack writes **no**
   config file for Pipez, LaserIO, Modular Routers, or Transfer Labels — those run on mod
   defaults. Anything else is a JEI question, not a quest-book question.

*Titles, ids, tasks, rewards, and quotes below are verified against the pack config at commit
`e5e3d1d83e`; the lag ranking in points 1–6 is judgement, and the in-game quest book and JEI
stay authoritative.*

## Provenance — everything here was read, not remembered

Every quest title, quest subtitle, quest id, chapter id, task item, reward item, dependency
link, `optional` flag, quoted sentence, and config value below comes from the official pack
repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10), `main` at the pinned
commit **`e5e3d1d83e`** (full SHA `e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025`) — the same
snapshot every sibling doc in this skill was read from. `CHANGELOG.md` dates that commit
**2026-09-22** and lists it as **pack 8.2**; `config/bcc-common.toml` carries
`modpackVersion = "8.2"` at the same commit, and the skill's chapter list is stamped `"8.x"`.

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/basic_logistics.snbt` | the 40 quests of *Basic Logistics*: ids, `dependencies`, `optional` flags, task items, reward items and counts, `x`/`y` clusters, chapter id and icon |
| `config/ftbquests/quests/lang/en_us/chapters/basic_logistics.snbt` | its English titles, subtitles, and every description quoted here |
| `config/ftbquests/quests/chapters/integrated_dynamics.snbt` + `lang/en_us/chapters/integrated_dynamics.snbt` | the 28 quests of *Integrated Dynamics* and their text |
| `config/ftbquests/quests/chapters/modular_router.snbt` + `lang/en_us/chapters/modular_router.snbt` | the 55 quests of *Modular Routers* and their text |
| `config/ftbquests/quests/chapters/pylons.snbt` + `lang/en_us/chapters/pylons.snbt` | the 13 quests of *Pylons* and their text |
| `config/ftbquests/quests/chapters/mekanism.snbt` + `lang/en_us/chapters/mekanism.snbt` | the *Mekanism* chapter's transport quests and the tier figures its own texts print |
| `config/ftbquests/quests/chapter_groups.snbt` + `lang/en_us/chapter_group.snbt` | the group id `3D4E23B1100491AB` and its title *Logistics*, and the group order |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the four chapter titles and *Basic Logistics*'s subtitle *And LaserIO* |
| `config/integrateddynamics-common.toml`, `config/integratedtunnels-common.toml` | the Integrated Dynamics and Integrated Tunnels settings quoted below |
| `config/integratedterminals-common.toml`, `config/integratedcrafting-common.toml` | the two companion mods' shipped files — named in the mods table, and the reason this page says nothing about their internals |
| `config/pylons-server.toml` | the Pylons settings quoted below |
| `config/crash_assistant/modlist.json` | the mod names and versions in the mods table, and the transport mods that ship without a quest |
| `config/bcc-common.toml`, `CHANGELOG.md` | the pack version and date this page is stamped with |

**How it was read.** The four chapters' 136 quests were parsed with this skill's own
stdlib reader (`scripts/snbt.py`), not by hand: every task item, reward item, `dependencies`
link, and `optional` flag was taken from the parsed compound, and every title, subtitle, and
description from the matching `lang/en_us/chapters/*.snbt` key. Minecraft `&` and `&#RRGGBB`
formatting codes are stripped and whitespace is collapsed throughout — the way the book renders
them — so a quote here is the config's sentence, not its markup. A quest is written
*(no title in the config)* when its lang entry has no `title` key; the book then shows the task
item's own name, and this page never invents a label for it.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a snapshot
  of pack 8.2's config. If the player's book or his `config/` folder differs from anything
  here, **his game wins** — say so and re-research rather than arguing from this file.
- **Titles are the config's, never invented.** 105 of the group's 136 quests carry no title at
  all (*Basic Logistics* 21 of 40, *Integrated Dynamics* 24 of 28, *Modular Routers* 48 of 55,
  *Pylons* 12 of 13); those are marked *(no title in the config)* in every table below, and a
  quest not on this page may still exist — the answer for those is "open the chapter in the
  book", never a plausible-sounding guess.
- **The lag ordering is the pack's only ranking, and it is prose.** Three parenthetical
  sentences in *Basic Logistics* compare Pipez, Mekanism pipes, and Integrated Dynamics. They
  are quoted as what the pack's author wrote — not a benchmark, not a measured TPS figure, and
  nothing like one. Every other ordering on this page is marked *(judgement)*.
- **No recipes, no item counts beyond the chapter's own rewards, no throughput maths, no
  layouts.** Where a quest text prints a tier figure, it is quoted verbatim and attributed to
  that quest; it is never multiplied, summed, or converted. Which mod a given player should
  pick is a judgement call, not a config fact.
- **Config values are what the pack ships, not what the player runs.** The Integrated
  Dynamics and Pylons figures below are 8.2's files at the pinned commit. Any of them can be
  changed in a live install, and this page points at the player's own `config/` folder rather
  than insisting.
- **Absence is reported as absence, with the search.** "Not in the group" below means the
  four chapters' task and reward items were searched at that commit and the id does not appear;
  it does not mean the mod is missing from the pack, and it never becomes a promise that a
  feature does not exist.
- **Nothing here was invented.** Every id in the tables is one the config itself writes, as a
  task item, a reward item, a chapter icon, or a value in the shipped `.toml` files quoted.
  If a detail is not on this page, the answer is "check the quest entry / JEI" — not a guess.

## The Logistics group at a glance

The quest book groups its 66 chapters into eleven sections; **Logistics**
(`3D4E23B1100491AB`) is one of them, and it holds exactly four chapters, in this order. Titles
are the book's (`lang/en_us/chapter.snbt`), filenames are what `progress.py` and this skill
track (`examples/progress.example.json` agrees with all four ids, titles, groups, and stages):

| filename | Book title | Group | order | quests |
|---|---|---|---|---|
| `basic_logistics` | Basic Logistics | Logistics | 0 | 40 |
| `integrated_dynamics` | Integrated Dynamics | Logistics | 1 | 28 |
| `modular_router` | Modular Routers | Logistics | 2 | 55 |
| `pylons` | Pylons | Logistics | 3 | 13 |

| Chapter | Chapter id | Icon the book shows | Untitled quests | Optional quests |
|---|---|---|---|---|
| *Basic Logistics* (subtitle *And LaserIO*) | `3DEB33F78398EAD6` | `pipez:wrench` | 21 of 40 | 6 |
| *Integrated Dynamics* | `69299302373C4CBC` | `integrateddynamics:crystalized_menril_chunk` | 24 of 28 | 6 |
| *Modular Routers* | `0AB4F9AED808DE48` | `modularrouters:modular_router` | 48 of 55 | 1 |
| *Pylons* | `5712300EF4E5E846` | `pylons:infusion_pylon` | 12 of 13 | 1 |

Two things the config says about the group as a whole, worth repeating when a player asks why
the chapters feel uneven:

- **The chapter filenames are singular, the book titles are not.** The file is
  `modular_router.snbt`; the title is **Modular Routers**. Skill output and progress files use
  the filename.
- **Every chapter carries one hidden author-credit quest, marked optional and worth nothing:**
  `230582AAFC0A1632`, `6ABDBE41880CFDA9`, `2BB5769119BA2472`, and `5E02AE661945306C` — two
  `checkmark` tasks each, no rewards, and the same text: *"This quest is intentionally hidden,
  if you're seeing this, you're in editing mode."* Never treat one as content, and never count
  it as a step.

## What the book says logistics is

Before any mod, *Basic Logistics* defines the subject (**Logistics**, `6CD7D99AA102A5C3`, no
dependencies, `gear` shape, task `ftbfiltersystem:smart_filter`, reward `minecraft:chest` ×2):

> *"Logistics: A system of moving, managing, and storing items or resources. In Modded
> Minecraft it's quite the same, moving items! With Modded you will need items and by the
> thousands, heck if you want the Star it gets in the millions! So you'll need to move items
> from factories, machines, farms, and especially chests. That's what Logistics is for."*

Two things to keep from that entry: the pack frames transport as a **scale** problem tied to
the ATM Star's material bill, and its intro quest asks for a **filter**, not a pipe — the same
`ftbfiltersystem:smart_filter` appears as the task item of 8 of the chapter's 40 quests and of
4 of *Integrated Dynamics*' 28. The book teaches filtering as the skill; the pipes are the
reward.

## The options, as the chapter is arranged

*Basic Logistics* is not one mod's chapter — its 40 quests cluster into five blocks, and the
`x`/`y` positions plus the dependency links separate them cleanly. "Tasks" counts the task items
by mod namespace (a quest can carry two).

| Block | Hub quest (id) | Tasks in the block | The pack's own verdict |
|---|---|---|---|
| Pipez | **Pipez** (`2329AA0AFBEF1E13`) | 7 `pipez:*`, 2 untitled upgrade quests tasking `pipez:filter_destination_tool` and `ftbfiltersystem:smart_filter` | *"Pipez is the simplest Logistics Mod."* |
| Mekanism | **Mekanism** (`34CFE1439262AA72`) | 1 `mekanism:configurator`, then 5 untitled quests tasking `ftbfiltersystem:smart_filter` | *"(These can cause a bit of lag when used in mass so be careful with them)."* |
| Integrated Dynamics | **Integrated Dynamics** (`6E05B62A40D5A891`) | 1 `integrateddynamics:wrench`, 1 `integrateddynamics:cable`, 1 `integrateddynamics:variable`, and 6 tasks that are Integrated Tunnels parts (three importers, three interfaces) | *"(Least laggy pipe solution, these are recommended)."* |
| LaserIO | **Laser IO** (`5F1218CF8EFC607B`) | 17 `laserio:*` | *"LaserIO is DireWolf's continuation of EnderIO's Logistics."* |
| Transfer Labels | **Transfer Labels** (`6CD60A9D88227005`) | 1 `ftbfiltersystem:smart_filter`, reward `transfer_labels:label_accessor` | *"Ever wanted to fit a pipe between blocks?"* |

The chapter also has the definition quest above and the hidden credit quest. Six of its quests
have no dependencies at all — the five hubs plus **Transfer Labels** — so *which* transport line
a player starts on is genuinely his choice; nothing in this chapter gates one behind another.

## 1. Pipez — the five pipes

One quest per pipe type, each depending on **Pipez** except **Universal Pipez**, which the
config links to all three of Item / Fluid / Energy (verified dependency list, not an
assumption):

| Verified quest title | Quest id | Task | Reward |
|---|---|---|---|
| **Pipez** | `2329AA0AFBEF1E13` | `pipez:wrench` | `minecraft:iron_ingot` ×3 |
| **Item Pipez** | `36836AD948F96B9F` | `pipez:item_pipe` | `pipez:item_pipe` ×16 |
| **Fluid Pipez** | `33433A443B65D252` | `pipez:fluid_pipe` | `pipez:fluid_pipe` ×16 |
| **Energy Pipez** | `53EC96FA0E7C4ED4` | `pipez:energy_pipe` | `pipez:energy_pipe` ×16 |
| **Universal Pipez** | `4FBAB3A0FBF8CE2F` | `pipez:universal_pipe` | `pipez:universal_pipe` ×16 |
| **Gas Pipez** | `2F4458E9921DEB86` | `pipez:gas_pipe` | `pipez:gas_pipe` ×16 |
| *(no title in the config)* | `2A976D41F79C34B1` | `pipez:filter_destination_tool` | `pipez:advanced_upgrade` |
| *(no title in the config)* | `6A962535CD68713E` | `ftbfiltersystem:smart_filter` | `pipez:advanced_upgrade` |

The pack's own words, quoted:

- **Pipez** — *"Attach the specific Pipe to where you want to move items and use the Pipe Wrench
  to configure what side Pulls, Pushes, or doesn't connect."* … *"Other Wrenches do work with
  Pipez as well!"*
- **Item Pipez** — *"It will move Items from one Inventory to another. Could be from one Chest
  to another, could be a Farm to a System, or even a Quarry to a Smelter."*
- **Fluid Pipez** — *"This can be connected to Sinks to move Infinite Water!"*
- **Energy Pipez** — *"Every Tech Mod needs Energy, whether it's FE, RF or something else!"* …
  *"Some Machines have strict IO ports for Energy so make sure to check for those!"*
- **Universal Pipez** — *"They can move Items, Fluids, or Energy."*
- **Gas Pipez** — *"Gas can't be moved with any of the other Pipez so if you need to move
  Hydrogen or Lithium you'll need Gas Pipez."* — and the author's own hedge: *"(I've always had
  problems telling whether the Mekanism item is Gas, Fluid, or even Infuse Type."* … *"If it
  doesn't you can check JEI for other recipes that might involve it!)"*
- *(no title in the config)* `2A976D41F79C34B1`, the filtering entry — *"Pipez do have their own
  way of Filtering Items, you need atleast an Advanced Upgrade to get it though."* (sic) …
  *"To set it, Shift Right Click an Inventory with it."*
- *(no title in the config)* `6A962535CD68713E`, the upgrade entry — *"All Upgrades increase the
  amount the Pipez move and also grant more options to use with the Pipe."* … *"Basic Upgrade
  allows Redstone Activation with Pipez, to change distribution either:Closest First, Farthest
  First, Round-Robin, or Random, and to add Filters."* … *"Improved, Advanced, and Ultimate
  upgrades don't grant anything new they just move more!"*

That last line is the whole Pipez ladder in one sentence: **Basic** buys behaviour, the upper
three tiers buy volume only. The chapter never tasks an upgrade item itself; both upgrade quests
reward `pipez:advanced_upgrade`, and JEI owns the recipes.

## 2. Mekanism transport — Advanced tier, handed out

*Basic Logistics*' Mekanism block opens with **Mekanism** (`34CFE1439262AA72`, task
`mekanism:configurator`, reward `alltheores:steel_ingot` ×3):

> *"The different Machines are picky with Configurations and will need to be changed in their
> GUI to properly move items. Then you can use the Meka Pipes to move whatever you need to move!
> But wait it's not just Mekanism these work for! They work for plenty of other machines as
> well! Just need to be Configured with a Wrench to Push and Pull."*

Behind it sit five quests, all untitled, all tasking a Smart Filter, all rewarding **16 Advanced
pieces** — the chapter skips the Basic tier on purpose:

| Subtitle the book shows | Quest id | Reward | What its text says it carries |
|---|---|---|---|
| *Blocks+Items* | `30DE4F5BC3EDB555` | `mekanism:advanced_logistical_transporter` ×16 | *"Logical Transporters are what Meka uses to move Items and Blocks across distance."* |
| *Fluids* | `1834B5C1F8435D7A` | `mekanism:advanced_mechanical_pipe` ×16 | *"Mechanical Pipes are how Meka lets the Fluids flow."* |
| *Energy* | `493D04D954E4FBA0` | `mekanism:advanced_universal_cable` ×16 | *"Mekanism is Tech Mod... why are you surprised it needs Energy for its Machines?"* |
| *Heat* | `316B513FE568EF57` | `mekanism:advanced_thermodynamic_conductor` ×16 | *"Thermal Evaporation Plants and Fusion Reactors both use Heat to work. And Conductors is how you will be moving Heat!"* |
| *Gas+More* | `4BC2D7FCDD792DBA` | `mekanism:advanced_pressurized_tube` ×16 | *"Gases are the main ones as if you're using Mekanism you will be using Gases like Hydrogen and Oxygen."* … *"Slurries are used with Ore Processing."* |

Note the pattern before repeating it: **one transport type per state of matter.** The tube
quest's own list is Gases, *"Infuse Types are similar like Coal Infuse and Redstone Infuse"*,
*"Slurries are used with Ore Processing"*, and *"Dye Pigments are the essence of Color"*. A
player asking "why can't my pipe carry this?" has a config-backed answer: the pack splits
items/blocks, fluids, energy, heat, and chemicals across five different rungs.

**Where the real numbers live.** The tier ladder is in the *Mekanism* chapter
(`23983F4DC524B14B`, 90 quests, Tech group), where each transport quest's own text prints its
figures. All five of these quest texts task a `ftbfiltersystem:smart_filter`, like the
*Basic Logistics* entries above — the book checks that you *configured* the line, not that you
crafted a stack:

| Verified quest title (Mekanism chapter) | Quest id | The tier lines the quest itself prints |
|---|---|---|
| **Logistical Transporters** (*Items*) | `60ECCCAB66AAC05D` | *"Basic: will move 2 Blocks/Items across 1 Block each Second."* … *"Ultimate: will move 2 stacks of Items or Blocks across 10 Blocks each Second."* |
| **Mechanical Pipes** (*Fluids*) | `33C69B5934BE4D64` | *"Basic: will hold 2 Buckets of Fluids and move 250mB of Fluid each Tick."* … *"Ultimate: will hold 128 Buckets and will move 32 Buckets each Tick."* |
| **Universal Cables** | `62827AA1AD29A222` | *"Basic: will hold and move 3.2kFE per Tick."* … *"Ultimate: will hold and move 3.27mFE per Tick."* |
| **Pressurized Tubes** (*Chemicals, Pigments, Infuse Types*) | `3AF1DC02E9A0010C` | *"Basic: will hold 4 Buckets of Chemicals and move 750mB of Chemicals each Tick."* |
| **Thermodynamic Conductors** (*Heat*) | `66A450CAC07232E1` | *"I'm not sure what these numbers mean but following the pattern: more expensive, more good!"* |
| **Mekanism Logistics** (*The Configurator*) | `5E116409DC7D30BB` | *"If you use it on Pipes it will change if they Push, Pull, or Both. You can use it on Ports to set Inputs and Outputs. And even on Bins to set them to Auto-Export below them."* |
| **Bins** (*Drawers*) | `73E6878553BA6908` | *"You like Drawers? Mekanism gives us some! Just these are called Bins."* … *"Ultimate: holds 4,096 Stacks."* |
| **Quantum Entangloporters** (*Wireless Power, Gases, Fluids, Everything.*) | `7CC49360D07086B8` | *"With 2 Quantum Entangloporters we can Wirelessly move Items, Fluids, Chemicals, Heat, and Energy!"* — task `mekanism:quantum_entangloporter` |

Those are the only figures this page states about Mekanism transport, and they are the quest's
own sentences. The **Configurator** entry is the answer to "my Meka machine won't accept
items": *You should know Logistics by know! This Quest will now be reserved to explaining the
Configurator!* (sic) — its modes are quoted in the table above. The **Entangloporter** is the
pack's only *wireless, cross-dimension* transport item with a quest in this group, and the
book's own gloss on it is *"Oh come on this is just Magic!"*

## 3. LaserIO — nodes, cards, filters, overclockers

**Laser IO** (`5F1218CF8EFC607B`, task and reward `laserio:logic_chip`) is the largest block in
*Basic Logistics*: 17 of its 40 quests task a `laserio:*` item.

> *"LaserIO is DireWolf's continuation of EnderIO's Logistics. It's all about moving items via
> Lasers! Who doesn't love Lasers?! And it all starts with the Logic Chip."*

The shape the chapter teaches, in dependency order, all verified:

| Verified quest title | Quest id | Task | The model, in the quest's words |
|---|---|---|---|
| *(no title in the config)* | `7BC8F50A89A3BE1A` | `laserio:laser_wrench` | *"These are just used to Connect Laser Nodes to each other and to Connectors."* |
| *(no title in the config)* | `5C0F6B1C93A52113` | `laserio:laser_node` | *"Now this is the true Heart of LaserIO! The Laser Nodes are where the actual Cards will go into in order to work."* … *"They will move Items from any adjacent Inventory in the 4 Cardinal Directions and Up and Down."* |
| **Item Card** | `4C41FD926F31180B` | `laserio:card_item` | *"Set one to Extract and put it on the side of the Laser Node you want to Import from. Then set the other to Insert and put it to the side you want the Items to Export to."* |
| **Fluid Card** | `1C70D739CE464E25` | `laserio:card_fluid` | *"Works exactly like the Item Cards, you need Extract and Insert Cards."* … *"No, it doesn't move Sources of Fluid in or out of the World."* |
| **Energy Card** | `52F85CED20C8B1E9` | `laserio:card_energy` | *"Energy has to get around somehow, preferably where we want it to go."* |
| **Redstone Card** | `47768B1FFD57D56E` | `laserio:card_redstone` | *"If we can have Wireless FE why not Wireless Redstone?"* |
| **Chemical Card** | `6718043D0F2D1830` | `laserio:card_chemical` | *"Everything Pressurized Tubes can move, these cards can. Gas, Infuse Types, and Pigments."* |
| *(no title in the config)* | `47A2BEFB11F4D581` | `laserio:filter_basic` | *"Simply put Items into it and they are now filtered."* … *"Matching NBT Data would mean having same Enchantments, Durabilitiy, or even Mobs inside of whatever Item."* (sic) |
| *(no title in the config)* | `2A6900E87DE8BAE0` | `laserio:filter_mod` | *"But instead of only being that Item it will be any Item from that Mod."* |
| *(no title in the config)* | `3065EA195D0A36BA` | `laserio:filter_tag` | *"(You can also find Tags by doing /kubejs hand to find what's the Tags of the Item in your hand.)"* |
| *(no title in the config)* | `06767BA0AFE8C1EE` | `laserio:filter_count` | *"It will then wait until that set Number of Items is there to start taking Items. It will also leave that amount in the first Inventory."* |
| *(no title in the config)* — **optional** | `617695A9CA45D88F` | `laserio:card_holder` | *"You can store multiple Cards in it and when you open a Laser Node the Card Holder will open up as well like a second Inventory."* |
| *(no title in the config)* — **optional** | `308935C85364B04D` | `laserio:card_cloner` | *"Left Click a Card with the Cloner to copy its Data, then Right Click a Card to give it that Data!"* |
| *(no title in the config)* — **optional** | `7EE27C3908008E20` | `laserio:laser_connector` | *"If you need to string your Laser Nodes a far distance try using Connectors!"* |

**The overclocker limits are subtitles, not lore.** Two untitled quests carry the config's own
`Max:` subtitles — *(no title in the config)* `046C417B2ADF3AA7` (*Max: 4*, task
`laserio:overclocker_card`) and `0BB562FB44B0AAA7` (*Max: 8*, task
`laserio:overclocker_node`). The card quest's text is where the pack prints its own numbers —
*"Cards have their limits. Item Extration can only extract 8 items per Operation. Fluid Extract
at only 5 Buckets."* (sic) — and the node quest's is where the placement differs: *"These go
into the Node itself on bottom right and boost how fast it does Operations."* Quote the limit
with its `Max:` subtitle and never as a transfer rate the config does not state.

## 4. Integrated Dynamics — the option the pack calls least laggy

ID appears **twice**, and players mix the two up, so keep them apart:

**a) The tunnel parts, inside *Basic Logistics*.** Hub quest **Integrated Dynamics**
(`6E05B62A40D5A891`, task `integrateddynamics:wrench`, reward
`integrateddynamics:crystalized_menril_chunk` ×3):

> *"Integrated Dynamics is all about Logistics! It's practically the definition of Logistic.
> It's all about moving, managing, and storing items. Heck you might not even need the Wrench
> for it, it's so well designed! Get one just incase though."* …
> *"(Least laggy pipe solution, these are recommended)."*

Its three-step trail, all verified: *(no title in the config)* `6112956E19017D2D` for
`integrateddynamics:cable` — *"Logic Cables are different from other Pipez or Meka pipes. The
other Pipes act as hoppers, the items move from 1 Inventory, into the Pipe, then into the 2nd
Inventory. Logic Cables just skip the middle man which also skips a lotta lag."* — then
*(no title in the config)* `03C40D6A5D722543` for `integrateddynamics:variable` (reward
`integrateddynamics:variable_transformer_input` ×4), and then the three titled importing quests,
each with **two** tasks (an importer plus its interface):

| Verified quest title | Quest id | Tasks |
|---|---|---|
| **Item Importing** | `6F152402756DA35E` | `integratedtunnels:part_importer_item`, `integratedtunnels:part_interface_item` |
| **Fluid Importing** | `034F2CDF0830254B` | `integratedtunnels:part_importer_fluid`, `integratedtunnels:part_interface_fluid` |
| **Energy Importing** | `76CECFB244F39F18` | `integratedtunnels:part_importer_energy`, `integratedtunnels:part_interface_energy` |

Two caveats the config prints in those texts and worth relaying verbatim: *"It can be changed
to Import Items at the Integer Limit (Over 2 Billion)."* — and, on the energy pair, *"I do have
to say I found it having problems with Importing or Exporting to Flux Plugs and Points so be
mindful of that."* The fluid one adds the limit no one asks about until it bites: *"Does not
place or take Fluid Sources from in the world, it only moves Fluids from one Tank to another."*

**b) The whole mod, in its own chapter.** *Integrated Dynamics* (`69299302373C4CBC`, 28
quests, only 4 titled) starts from a tree, not a pipe. **Integrated Dynamics**
(`499CF9F39CED8899`, subtitle *Growing Menril*) tasks `ftbfiltersystem:smart_filter` and
rewards the guidebook `integrateddynamics:on_the_dynamics_of_integration` plus
`integrateddynamics:menril_planks` ×10:

> *"Integrated Dynamics (ID) is a logistics mod that can be used for storage, item/power/fluid
> transfer and more! Menril trees can be found in Meneglin biomes."* (sic) … *"read the
> guidebook given as a reward for this quest if you want to go further in depth."*

That last sentence is the correct answer to any ID question this page does not cover: **the
pack ships a guidebook for the mod and points at it.** Then the chapter's own chain, in
dependency order:

| Verified quest title | Quest id | Task | The step |
|---|---|---|---|
| *(no title in the config)* | `68498ADEF9765F81` | `integrateddynamics:squeezer` | *"Jump on the Squeezer to turn them into Menril Resin."* … *"You can empty the Squeezer by giving it a Redstone signal."* |
| *(no title in the config)* | `62B4A37CFDECA679` | `integrateddynamics:drying_basin` | *"After 7.5 seconds the Menril Resin will turn into a Block of Crystallized Menril."* |
| **Crystallized Menril Chunks** (*The Main Crafting Ingredient*) | `72F57D77C3FB366D` | `integrateddynamics:crystalized_menril_chunk` | *"These chunks are the main crafting ingredient of ID."* |
| **Logic Cables** (*Making Networks*) | `4A05C037C0EE40BD` | `integrateddynamics:cable` | *"They are just for connecting Importers and Interfaces."* |
| **Variable Cards** | `79C1105A84B8BF8F` | `integrateddynamics:variable` | *"You can change how much is Importer, which Item Slot, which Channel, practically everything with just that Card."* |
| *(no title in the config)* (*Importing*) | `73EA326304C01C3B` | `ftbfiltersystem:smart_filter` | *"Put an Importer onto the inventory you want stuff pulled from."* |
| *(no title in the config)* (*Exporting*) | `33F4A7613764A016` | `ftbfiltersystem:smart_filter` | *"Works like Importers do, only they export instead."* |
| *(no title in the config)* (*Moving Stuff!*) | `65FA86357BC60573` | `checkmark` | the three-step summary, quoted below |
| *(no title in the config)* (*Interfaces Have GUIs!*) | `450EDE68EC992A5A` | `ftbfiltersystem:smart_filter` | *"You can think of this like an AE2 Storage Bus."* |
| *(no title in the config)* | `1B5C86AE05678420` | `checkmark` | the interface GUI options, quoted below |
| *(no title in the config)* (*Getting Advanced*) | `4D4152032F0410D2` | `integrateddynamics:logic_programmer` | *"The Logic Programmer lets you set the value of variables."* |
| *(no title in the config)* | `1568CBFA09827137` | `integrateddynamics:portable_logic_programmer` | *"Same thing as Logic Programmer, only this one can be used anywhere."* |
| *(no title in the config)* (*AUTO CRAFT*) | `65D89991A45BC042` | `integratedcrafting:part_interface_crafting` | *"Place a Crafting Interfaces on a crafting table and right-click on it, this will give you some slots for Variable Cards."* (sic) |
| *(no title in the config)* (*Shows Recipes*) | `56BF647EA84FFF7E` | `integratedterminals:part_terminal_crafting_job` | *"Shows which crafting recipes are happening at any time."* |
| *(no title in the config)* (*Storing Energy*) | `6D75CF34957ECCD9` | `integrateddynamics:energy_battery` | *"The Energy Battery lets you store FE. To transfer it, you will need Energy Interfaces."* |
| *(no title in the config)* (*Providing Energy!*) — **optional** | `4D62C62B523C69EC` | `integrateddynamics:coal_generator` | *"The Generator generates FE using burnable fuels like Coal."* |
| *(no title in the config)* | `2F37E284BB83BFF6` | `integrateddynamics:wrench` | *"The Wrench is used to rotate or destroy certain blocks, shift right-click in the air to change modes."* |

The chapter's own summary of the moving part is the best beginner explanation in the whole
group — *(no title in the config)* `65FA86357BC60573`, *Moving Stuff!*:

> *"It's time to move stuff from one place to another. Here are the steps: 1. Place an interface
> on an inventory (like a Chest or a Tank) 2. Place an Importer or an Exporter on another
> inventory, depending on whether you want to pull or send stuff to it. 3. Hook the both up with
> Cables, place a Variable Card into the Importer or Exporter, and there you go!"*

And *(no title in the config)* `1B5C86AE05678420` lists what an interface's GUI is for —
*"Set Side"*, *"Ticks/Operation: If an interface is set to 10 ticks/operation, it will
import/export once every 10 ticks (0.5 seconds)."*, *"Priority: Sends items to the inventory
with the higher priority interface on it."*, and *"Item/Energy Channels: This will split your
system into multiple channels."* Its sibling `437F4945AFBE0825` is where the book warns about
the one setting people abuse: *"In here you can change transfer rates to be able to send
INFINITE items/fluids/energy, as well as being able to do some other stuff."*

**Menril has two optional farm routes, both quested** (so a player who hates the tree line has
an out): *(no title in the config)* `232A06C9FF0EE7B2` (*Automating Menril*, task
`mysticalagriculture:menril_seeds`, *"Menril Seeds can be used to automate Menril Berries,
Menril Logs and Menril Saplings."*) and `3C9539083BCC145C` (*Automating Menril*, task
`productivebees:configurable_honeycomb`, *"Menril Bees can be used to automate Crystallized
Menril Chunks."*). The `references/farming-guide.md` page is where those two lines continue.

**The pack's own ID settings, from the shipped configs.** These are the values ATM10 8.2
writes; a live install can differ, and the player's `config/` folder wins:

| Setting (file) | Shipped value | Why it matters here |
|---|---|---|
| `energyRateLimit` (`integrateddynamics-common.toml`) | `2147483647` | the number behind the quest text's *"Integer Limit (Over 2 billion)"* — and the ceiling on the *"INFINITE"* claim above |
| `fluidRateLimit` (`integratedtunnels-common.toml`) | `2147483647` | same ceiling on the fluid side |
| `ingredientNetworkObserverFrequencyMin` and `ingredientNetworkObserverFrequencyMax` (`integrateddynamics-common.toml`) | `5` / `40` | the comment calls the first *"The fastest possible frequency in ticks at which ingredient network should be observed."* and the second *"The slowest possible frequency in ticks at which ingredient network should be observed."* |
| `inventoryUnchangedTickTimeout` (`integratedtunnels-common.toml`) | `10` | *"How many ticks importers/exporters should sleep until checking targets again when they were previously unchanged."* |
| `ejectItemsOnBlockDropOverflow` / `ejectItemsOnInconsistentSimulationMovement` (`integratedtunnels-common.toml`) | `true` / `true` | both comments say the alternative is voiding: *"Will be voided otherwise"* / *"If disabled, items can be voided."* |
| `safeMode` (`integrateddynamics-common.toml`) | `false` | its comment: *"When enabled, networks will stop ticking and values will not be shown and evaluated again. This can be used to fix crashing networks by temporarily enabling this option"* |
| `recreateCorruptedNetworks` (`integrateddynamics-common.toml`) | `true` | *"If corrupted networks should automatically be restored on first tick."* |
| `logChangeEvents`, `analytics` (`integrateddynamics-common.toml`) | `false`, `false` | the pack ships ID quiet: no change-event spam, no analytics request |
| `defaultPartUpdateFreq` / `maxPartOffset` (`integrateddynamics-common.toml`) | `1` / `32` | new parts' default update rate, and how far a part may reach |
| `filledMenrilLogChance` (`integrateddynamics-common.toml`) | `10` | the worldgen 1-in-10 chance a Menril log spawns resin-filled |

The two **void** switches and `safeMode` are the ones to mention when an ID network "ate"
something; quote the comments, not advice, and send the player to his own file.

## 5. Modular Routers — transport with no pipes at all

*Modular Routers* (`0AB4F9AED808DE48`, 55 quests, 7 titled) is the largest chapter in the
group, and it is not a pipe mod: one block with a **Buffer**, plus Modules, Upgrades, and
Augments. Its four concept quests are what to read first, all verified:

| Verified quest title | Quest id | Task | The rule the quest prints |
|---|---|---|---|
| **Modular Routers** | `63E4529AF8894018` | `modularrouters:modular_router` | *"Also the Buffer is the single item slot in the Router where items will come and go through. And it will need Redstone signal for most modules to work."* |
| **Modules** | `233C7CAA573D6045` | `modularrouters:blank_module` | *"Modules determine the action the Router preforms."* (sic) … *"Filtering and Upgrades go into the Modules themselves."* |
| **Upgrades** | `75FE0B514448865B` | `modularrouters:blank_upgrade` | *"Upgrades go directly into the Router and the Router can hold 5 of them."* |
| **Augments** | `6648BC7D14233006` | `modularrouters:augment_core` | *"Augments are similar to Upgrades but for the individual Modules!"* |

**The Redstone caveat is in the hub quest, not buried.** *"And it will need Redstone signal for
most modules to work"* is the answer to "I built a Router and nothing happens" — quote it, and
leave the fix (a Redstone Block, a Detector Module, or a **Sync Upgrade**, which the chapter
treats separately) to the player.

**The rate ladder, in the quests' own numbers.** *(no title in the config)* `309B6B8368E535A0`
(**Speed Upgrade**) says *"A Router does it's action every time it has one of it's ticks."*
(sic) … *"Default is 20 Ticks or 1 Second."*; *(no title in the config)* `4CC963F5AECF285A`
(**Stack Upgrade**) says *"1 Stack Upgrade is 2 Items, 2 Stacks 4 Items, and 6 Stacks is 64
Items a second."*; and *(no title in the config)* `5FB29F3F4DF17765` warns that the module-level
version of that does not stack with the router-level one: *"This does not stack with Upgrades
though... infact it overrides them."* (sic)

**The sender ladder is the interesting part, and it is verified by `dependencies`:**
`sender_module_1` → `sender_module_2` → `sender_module_3`, all untitled
(`6063F4B7BE4D394C`, `38954551309F42A7`, `2405663C033CBDF1`):

- MK1: *"will only move items into Inventories on the same XYZ axis as the Router and with
  direct line of sight. If there is a block in the way, the MK1 Sender will not send."*
- MK2: *"MK2 doesn't need direct line of sight or to be on same XYZ axis. Will have to be in the
  same Dimension though, unless you have..."*
- MK3: *"MK3 doesn't worry about XYZ axis, line of sight, or Dimension. As long as the Inventory
  is in the same Minecraft World it can move items into it."*

The puller pair (`1AA81C41431FD145` → `475E1B94A61B9EB0`) mirrors it: *"The Inventory has to be
adjacent to the Router"* versus *"Just not only from adjacent Inventories, but any Inventory
nearby!"*

**Everything else the chapter is.** Roughly: 20 module quests (activator, breaker, detector,
distributor, dropper, flinger, fluid and fluid MK2, placer, player, puller MK1/MK2, sender
MK1/MK2/MK3, extruder MK1/MK2, vacuum, void, energy output, energy distributor), 9 upgrade
quests (blast, camouflage, energy, fluid, muffler, security, speed, stack, sync), 11 augment
quests (fast pickup, filter round robin, mimic, pickup delay, pushing, range down, range up,
redstone, regulator, stack, xp vacuum), and 5 filter quests (bulk item, inspection, mod, regex,
tag). Four of those deserve quoting because players ask about exactly them:

- **Void Module** — *(no title in the config)* `185074907753AE77`: *"Any items that come into
  the Router, will be deleted forever!"* … *"Recommend using Filters with this one..."*
- **Security Upgrade** — `10672B5991E5FC34`: *"It's my stuff, no touchy."* … *"Only you can use
  and mess with the Router after putting in the Upgrade."*
- **Blast Upgrade** — `20D4568857887D38`: *"TNT won't break it, Wither won't break it, only
  you."*
- **Muffler Upgrade** — `2447208F1DC74FFE`: *"Routers can be noisy, and noise definitely stacks
  when you have hundreds of them."*

**The chapter's one prank, and what to learn from it.** A quest sits between the module quests
and the filters, untitled, `checkmark`-only, rewarding `modularrouters:blank_module` ×3 — and
its description is: *"HAHAHA did I scare you with the Creative item in the quests? Don't worry
you won't need the item to finish this chapter, I just wanted to scare you I can have fun
sometimes..."* (`71FDF8CD953E46FC`, verified). If a player reports that *Modular Routers* wants
a creative item, the config's answer is that no task in the chapter demands one: 56 of its
tasks are `modularrouters:*` items and the other 4 are three `checkmark` tasks and one
`ftbfiltersystem:smart_filter`.

**Three worked examples, and they are the only other titled quests.** *Routers for Farming*
(`0D5691403AEC25A8`, tasks `modularrouters:activator_module` + `modularrouters:vacuum_module`):
*"Finally put it all in the Router, Power it with Redstone, and let it farm!"*; *Routers for
Mining* (`067AB3E4C4492F0D`, `modularrouters:breaker_module` + `modularrouters:placer_module`):
*"Breaker needs the Pickaxe used to craft it to be Enchanted first, the Module itself can't be
Enchanted."*; *Routers for Mob Farms* (`53A5F5E49EA8D5AF`, `modularrouters:vacuum_module` +
`modularrouters:void_module` + `ftbfiltersystem:smart_filter`): *"get rid of the Stone Swords
with a Void Module. To make sure it doesn't delete everything use a Whitelist Filter with the
Stone Sword in it and not matching Damage."* The mob-farm one also carries the caveat to repeat:
*"(Does not include way of killing mobs)."* and the storage advice *"I recommend a Drawer
System"*. All three depend directly on the hub quest, so they are reachable on day one of the
chapter.

## 6. Pylons — filed under Logistics, moves nothing

*Pylons* (`5712300EF4E5E846`, 13 quests, **1** titled) sits in the Logistics group and is not a
transport mod. Say this first when a player asks "what do pylons have to do with pipes?", then
answer what the chapter actually wants. Its hub quest **Pylons** (`30B0240543253EFB`, task
`minecraft:polished_blackstone`, XP reward only) says:

> *"Don't let the size of the mod make you underestimate it! It provides many Pylons which can be
> used for many things to help make playing Minecraft easier. To get started you'll need some
> Polished Blackstone to make them."*

The five pylon quests and the six filter quests, all verified (every one is untitled in the
config; the book shows the item's own name, sometimes with a subtitle):

| Subtitle / book name | Quest id | Task | Reward | What it does, per its own text |
|---|---|---|---|---|
| *Get off my lawn!* | `32E52AD6EF194A60` | `pylons:expulsion_pylon` | `minecraft:diamond` ×2, XP | *"When placed down it will keep any Players who aren't whitelisted from a set amount of Chunks around it."* |
| — | `5B5FC539BD1F4A73` | `pylons:interdiction_pylon` | `minecraft:netherite_ingot`, XP | *"This Pylon is all about blocking Mob Spawns."* |
| — | `12ED1EE85E146A4B` | `pylons:harvester_pylon` | `minecraft:wheat_seeds` ×4, XP | *"Harvester Pylons work as a very simple Auto-Farm."* |
| — | `18246A48C20B29D8` | `pylons:infusion_pylon` | `minecraft:emerald` ×2, XP | *"The Infusion Pylon works similar as a Beacon just much better and cheaper!"* |
| *Accidental Destruction no more!* | `2F5263A4166BFCD6` | `pylons:protection_pylon` | `minecraft:honeycomb` ×4, XP | *"This Pylon prevents you from accidentally destroying certain Blocks/Mobs in the selected Chunk radius."* |
| — | `403F76908A8A5661` | `pylons:player_filter` | XP | *"Right Click a Player with it to set them in it, and then put it into the Pylon to Whitelist them!"* |
| *He's uninvited!* | `011F787E620DE9E8` | `pylons:mob_filter` | `minecraft:torch` ×10, XP | *"Each Filter can only hold 1 Mob so if you want Zombies, Skeletons, Spiders, Creepers, and Endermen to no longer spawn you'll need 5 Mob Filters."* |
| — | `77B185799366ACD2` | `pylons:block_filter` | `minecraft:honeycomb`, XP | *"To set the Block Filter you just have to click the Block you want to prevent accidentally breaking, with the Block Filter."* |
| — | `09D18512037386C1` | `pylons:potion_filter` | `minecraft:brewing_stand`, `minecraft:blaze_powder` ×3, XP | *"This also works with modded Potion Effects or ones you can't usually get through Potions like Haste or Resistance."* |
| *Finally peace and quiet.* | `5C2C29ECA67F9B49` | `pylons:lifeless_filter` | `minecraft:nether_star`, XP | *"With the Lifeless Filter you will never have to worry about any Mob spawns within a 25x25 Block area."* |
| — | `034A9FBCA6D79BB6` | `ftbfiltersystem:smart_filter` | `minecraft:enchanted_book`, XP | *"The Harvester Pylon needs a Hoe to work."* |

The **harvester's tool rule** and its **TPS warning** are both in this chapter's own text, and
both belong in an answer about pylons: *"Put the Pylon on or in the Water Source and it will
automatically harvest and replant Crops that are fully grown in the set area around it."*,
*"(Careful when using a lot of modifiers with it like Lilypads or fertilizer as when it goes
very fast farming it can be a TPS eater)."*, and on the hoe: *"(Hoes that can't break will work
forever, Hoes that can will need to be replaced)."*

**Why that last one matters, from the shipped config.** `config/pylons-server.toml` at the same
commit is what makes the hoe rule bite — and it is one of the few places the pack *changed* a
default:

| Setting | Shipped value | The file's own comment |
|---|---|---|
| `harvesterWorkDelay` | `20` | *"Delay between harvest attempts (in ticks)."* — the comment lists `Default: 60`, `Range: 10 ~ 120`, so the pack shipped it **three times faster** than the mod's default |
| `harvesterRequiresTool` | `true` | *"Whether the harvester requires a hoe to work."* … *"If enabled, it will use 1 durability per harvest action"* |
| `harvesterCanBeAutomated` | `false` | *"By default, unbreakable tools are required for full automation."* |
| `harvesterRequiresPower` | `false` | *"If enabled, it will disable the tool requirement and instead have an RF cost per block."* |
| `infusionChunkloads` | `true` | *"This is limited to one pylon per player, while the player is online."* |
| `infusionMinimumDuration` / `infusionRequiredDuration` | `60` / `3600` | the second: *"By default this is 3600 seconds/1 hour, which is equivalent to 7.5 vanilla extended potions."* |
| `infusionMaximumPotency` | `3` | *"This value is 0-indexed, so a Resistance V potion would be potency 4."* |
| `infusionDeniedEffects` | six effects | `minecraft:absorption`, `tombstone:ghostly_shape`, `irons_spellbooks:heartstop`, `relics:immortality`, `irons_spellbooks:evasion`, `irons_spellbooks:abyssal_shroud` |
| `expulsionAllowedDimensions` | four dimensions | `minecraft:overworld`, `allthemodium:the_beyond`, `eternal_starlight:starlight`, `compactmachines:compact_world` |
| `expulsionPylonMaxRadius` | `2` | *"Does not include center chunk, so a radius of 2 equals a 5x5 chunk diameter."* — and the chapter's own range claim is the same: *"The Chunks are set in it's GUI in the top left from 1x1, 3x3, or 5x5 Chunks."* |
| `expulsionPylonCanExplode` | `false` | *"Whether the Expulsion Pylon can be destroyed with explosions."* |
| `teamSupportEnabled` | `true` | *"Whether team support is enabled if a compatible mod (FTB Teams, Argonauts) is installed"* |

Three things to relay from that table instead of inventing an answer: the **Infusion Pylon
chunk-loads itself** but only *while the player is online* and only one per player, so it is not
a substitute for `references/chunk-loading-guide.md`; the **Expulsion Pylon is allowed in only
four dimensions** and *Also no it can't be set too close to Spawn* (its own words) because
`expulsionWorldSpawnRadius = 1`; and the **harvester is fast by the pack's own choice**, which is
precisely the *TPS eater* the quest warns about. `infusionDeniedEffects` is the answer to "why
won't my Absorption work?"

## 7. Transfer Labels — a pipe that fits in one block of space

Still *Basic Logistics*, still unranked by the pack: **Transfer Labels**
(`6CD60A9D88227005`, subtitle *When you gotta fit a pipe between your blocks*, no dependencies,
task `ftbfiltersystem:smart_filter`, reward `transfer_labels:label_accessor`).

> *"Ever wanted to fit a pipe between blocks? Allow me to introduce you to Transfer Labels.
> Transfer Labels can be used for items and fluids."* … *"You can place Labels on blocks by sneak
> right clicking onto blocks."* … *"You can access Labels through blocks using the Label
> Accessor."* … *"You can accelerate the Labels by adding the same type of Label in the amount or
> speed slots."*

The mod is `transfer_labels-0.1.9.jar` (`Transfer Labels` 0.1.9 in `modlist.json`), it has no
chapter of its own, and it has no shipped config file — one quest is the pack's whole treatment
of it. Do not expand on it beyond those quoted lines.

## Which one to build, and when *(judgement)*

Nothing in the quest config ranks these. The only order the pack states is the three
parentheticals in *Basic Logistics*, quoted in the short answer, and they compare exactly three
options. Everything in this table is **this skill's judgement** for a beginner, offered as a
recommendation, with the verified anchor you can check in the book:

| If you… | Build *(judgement)* | Verified anchor to open |
|---|---|---|
| have a chest and a machine and no pipes yet | Pipez — the item pipe | *Basic Logistics* → **Pipez** → **Item Pipez** |
| are already deep in Mekanism, or need gases/heat | Mekanism transport, starting at the Advanced pieces the chapter gives you | *Basic Logistics* → **Mekanism** (`34CFE1439262AA72`); tiers in *Mekanism* → **Logistical Transporters** |
| care most about TPS | Integrated Dynamics' importer/interface pair | *Basic Logistics* → **Integrated Dynamics**; the 3 steps in its *Moving Stuff!* quest |
| want long-distance runs and don't want pipe networks | LaserIO nodes + cards | *Basic Logistics* → **Laser IO** |
| want *no* pipes, plus farms/mining/mob-cleaning in one block | Modular Routers | *Modular Routers* → **Modular Routers**, then the three *Routers for…* quests |
| want an auto-farm, a mob-free base, or a beacon without a beacon | Pylons | *Pylons* → **Pylons**, then the pylon you actually want |
| need a run through a wall you already built | Transfer Labels | *Basic Logistics* → **Transfer Labels** |

Two honesty rules when giving this table: **AE2 and Refined Storage also move items**, and at
scale they are the better answer for storage-shaped problems — that comparison belongs to
`references/storage-ladder.md` and `references/autocrafting-guide.md`, not here; and *nothing in
the pack's config says you must finish any of these chapters*, because the Welcome chapter says
quests are optional and mods are not gated.

## What the pack ships for these mods (and what it does not)

Verified against the repository tree and `config/crash_assistant/modlist.json` at
`e5e3d1d83e` (489 mods). The versions are the mod list's own `name` / `version` fields:

| Mod | Version | Chapter(s) | Shipped config in the pack |
|---|---|---|---|
| Pipez | 1.21.1-1.2.31 | *Basic Logistics* | **no config file** — defaults |
| LaserIO | 1.9.11 | *Basic Logistics* | **no config file** — defaults |
| IntegratedDynamics | 1.37.1 | *Basic Logistics*, *Integrated Dynamics* | `integrateddynamics-common.toml`, `integrateddynamicscompat-common.toml` |
| IntegratedTunnels | 1.12.0 | *Basic Logistics* | `integratedtunnels-common.toml` |
| IntegratedTerminals | 1.10.0 | *Integrated Dynamics* | `integratedterminals-common.toml` |
| IntegratedCrafting | 1.7.2 | *Integrated Dynamics* | `integratedcrafting-common.toml` |
| IntegratedScripting | 1.0.27 | — (no quest in the group) | no config file |
| Modular Routers | 13.2.7 | *Modular Routers* | **no config file** — defaults |
| Mekanistic Routers | 1.2.0 | — (no quest in the group) | no config file |
| Pylons | 5.4.2 | *Pylons* | `pylons-server.toml` |
| FTB Filter System | 21.1.4 | the `ftbfiltersystem:smart_filter` tasks everywhere | no config file |
| Transfer Labels | 0.1.9 | *Basic Logistics* | **no config file** — defaults |
| Mekanism | 10.7.19 | *Mekanism* (Tech), used by this group | `Mekanism/`, `mekanismcovers.json` |

- **The `ftbfiltersystem:smart_filter` task is the pack's own standard.** 14 quests across the
  group ask for a Smart Filter instead of the machine being taught: 8 in *Basic Logistics*, 4 in
  *Integrated Dynamics*, 1 in *Modular Routers* and 1 in *Pylons*. Teach filtering, reward the
  pipe: that is the chapter's design, and it is why a player who crafts a stack of transporters
  but never opens a filter GUI still has unfinished quests.
- **Two other transport mods ship and are not quested here.** `enderio-8.2.12-beta.jar`
  (EnderIO) and `logisticsnetworks-1.21.1-1.16.3.jar` are in the mod list, and neither
  `enderio:` nor `logisticsnetworks:` appears as a task or reward item in any of the four
  chapters — EnderIO's name shows up in the group exactly once, inside LaserIO's own
  description. The book's only EnderIO-adjacent advice is therefore *"LaserIO is DireWolf's
  continuation of EnderIO's Logistics."* Whether another chapter tracks a conduit is a
  quest-book search the player can run; this page claims nothing about it. Likewise
  `mekanisticrouters-1.2.0.jar` (Mekanistic Routers) and
  `integratedscripting-1.21.1-neoforge-1.0.27.jar` (IntegratedScripting) ship, but no quest in
  the group asks for either.
- **There is no fifth Logistics chapter.** The group holds exactly the four chapters above, in
  that order, per `chapter_groups.snbt` and each chapter's `order_index`. Storage-side
  automation (AE2, Refined Storage, Extended & Advanced AE) lives in the **Storage** group and is
  covered by `references/storage-ladder.md` and `references/autocrafting-guide.md`.

## Related pages

- `references/automation-first-steps.md` — the parent page: it ranks *item transport* third of
  five first automations and points at this one for the detail.
- `references/storage-ladder.md` — where moved items land: chests → drawers → AE2 / Refined
  Storage, the side-by-side the transport chapters assume.
- `references/power-guide.md` — the generation and storage these cables feed; energy transport is
  one column there, not its subject.
- `references/ore-processing-ladder.md` and `references/farming-guide.md` — the two factories a
  transport line usually exists to serve; both have their own "what to set up first" ordering.
- `references/chunk-loading-guide.md` — why a router farm or harvester pylon stops the moment you
  walk off, and what actually force-loads it.
- `references/lag-fix-guide.md` — the pack's own settings to look at when a big pipe network is
  the cause; this page quotes the three lag parentheticals and the harvester's *TPS eater* note,
  and measures nothing.
- `references/autocrafting-guide.md` — ID's `integratedcrafting:part_interface_crafting` quest is
  autocrafting in a different mod; the AE2/RS chains are there.
- `references/mob-farm-progression.md` — the *Routers for Mob Farms* example is a third of a mob
  farm; the rest is there.
- `references/key-mods.md` and `references/progression.md` — what each mod is for, and the stage
  labels this page borrows.

## What this page deliberately does not tell you

- **No recipes.** Not for a pipe, a module, a card, or a pylon — not even the Mekanism upgrade
  pattern, which its own quest texts describe in prose ("combine 8 of the same Tier with a
  Control Circuit"). Prose quoted here is not a recipe tree; JEI is the recipe.
- **No throughput maths.** The per-tier figures this page carries are the quoted sentences of
  specific quests, per tier, per type. Nothing here is multiplied into "items per second for your
  base", compared across mods in numbers, or converted between FE/RF, buckets, and mB.
- **No layouts, block counts, or "one pipe per machine" style rules.** The config never places
  anything.
- **No "which mod is best" verdict.** The only ranking the pack states is three parenthetical
  sentences about lag; the table above is judgement and must be repeated as such.
- **No claim about a transport mod outside this group.** No EnderIO conduit tier list, no
  Logistics Networks, no Mekanistic Routers content, no Integrated Scripting — those mods are in
  the pack, and the four chapters never quest them, which is all this page knows.
- **No current-player specifics.** Whether a *his* Router needs power, whether *his* Pylons
  config was changed, whether *his* book still has 40 quests in `basic_logistics` — his install
  answers, this snapshot does not.
- **Where the config and its own text disagree, both are printed.** *Basic Logistics* calls its
  Mekanism rungs *Logical Transporters* in one description while the reward item is
  `mekanism:advanced_logistical_transporter`, and the chapter's Energy Importing entry carries a
  Flux Networks caveat no other source in the group repeats. This page quotes both and picks
  neither.

## Using this page in a session

1. **Name the state of matter first** — items, fluids, energy, heat, chemicals, or "not moving
   at all" (Pylons). The chapters are split that way, and so is the answer.
2. **Lead with what the pack itself said**, in quotes: the *"simplest"* line for Pipez, the
   Advanced-tier rewards for the Mekanism block, the three lag parentheticals, *Moving Stuff!*
   for ID, the Redstone line for Routers. Add the quest title and, when the book has no title,
   say *(no title in the config)* and name the quest id.
3. **Keep the labels.** *(judgement)* stays judgement; the `Max: 4` / `Max: 8` subtitles stay
   subtitles; the config values stay "what pack 8.2 ships, your `config/` wins".
4. **Route the leftovers**: storage-shaped questions to `references/storage-ladder.md`,
   autocrafting to `references/autocrafting-guide.md`, "it stops when I leave" to
   `references/chunk-loading-guide.md`, "the pipes are costing me TPS" to
   `references/lag-fix-guide.md`, and any recipe, rate, or exact requirement to the in-game
   quest book and JEI.
