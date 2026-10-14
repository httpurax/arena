# Chapter 4: Creative — the post-star checklist (38 quests, verified titles)

**What this page is.** The endgame-after-the-endgame map for **All the Mods 10**: what the
quest book's **Chapter 4: Creative** asks of a player who already holds an ATM Star, which
line each quest belongs to, and what the quest's own text says it gives back. It answers
"the star is done — what *is* this chapter?" and nothing more. It is a *map of the
chapter*, not a crafting guide.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, count, dependency, and quoted sentence below comes
from the official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10)
at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/achapter_2r_6the_atm_star.snbt` | the chapter's 38 quests, their task items and required counts, dependency links, and reward tables |
| `config/ftbquests/quests/lang/en_us/chapters/achapter_2r_6the_atm_star.snbt` | the English quest titles, subtitles, and the description text quoted below |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` | the chapter's own title and subtitle |
| `config/ftbquests/quests/lang/en_us/chapter_group.snbt` | the quest-book group the chapter sits in, `Main Questline` |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |

The book names this chapter **Chapter 4: Creative**, subtitle *"Plus Star Automation!"*,
icon `modularrouters:creative_module` (Modular Routers 13.2.7), group **Main Questline**,
`order_index` 3 — the fourth and last chapter of the Main Questline spine, after Chapter 3:
The ATM Star. The skill tracks it as `achapter_2r_6the_atm_star` (the config's filename),
stage `endgame`. The star itself, its 13 components, and the Runic Star Altar build live in
`references/atm-star-checklist.md`; this page starts where that one stops.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the task's required amount); where the config
  asks for one item, no count is printed.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Every
  "how" on this page is a quote from that quest's own description, marked as such, or a
  pointer to JEI. Do not fill a recipe in from memory or plausibility.
- **Approximate means approximate.** Mod names are the modlist's, but which machine tier,
  energy amount, or automation layout a player needs is version-sensitive; anything not
  quoted from the config is flagged as approximate.
- **Titles are the config's.** 36 of the 38 quests carry an explicit title. The other two
  are marked *(no title in the config)* — the book then shows the task item's own name.
  Do not present a derived name as a verified title.
- **Nothing here was invented, and nothing is added from memory.** A quest that is not on
  this page is not in this chapter: the answer is "open that quest in the book / look it up
  in JEI", never a plausible-sounding guess.

## How the chapter is shaped

One spine, one payoff. The chapter is the automation behind the star and the shopping list
you spend stars on:

| | |
|---|---|
| Quests in the chapter | **38** |
| Tasks in total | 72 (71 `item`, one `biome`) |
| Quests with no dependencies (the eight starting points) | 8 |
| Direct dependencies of the terminal quest, *Fully Automated ATM Star* | **10** |
| Creative-tier quests gated behind it, one dependency each | **11** |
| Quests carrying an explicit title in the config | 36 (the other two are marked below) |

Even so, the book lays a chapter out on a **canvas, not as a numbered list**, and the only
numbered quest subtitles in this chapter are the five star parts' own (*1/5* … *5/5*). So
this page does not invent a sequence: the spine below is written **in dependency order** (a
quest appears after everything it needs — verified from the config's `dependencies` lists),
and the eleven creative items are listed in the order the config lists them.

Read it as two halves:

1. **Rebuild the star, automatically** — 27 quests: the four multiblocks, the bee chain
   (and the Crusher shortcut) behind **Star Shards**, the five prism-line quests that feed
   the **five star parts**, the two dusts and the three-quest lens chain, the Runic
   Enchanter line behind **Infused Patrick Star**, and the terminal quest they all
   converge on.
2. **Spend the star** — 11 quests, each hanging directly off that terminal quest by a
   single dependency, each asking for one creative-tier item.

## The spine, in dependency order

### The four multiblocks (no dependencies)

The chapter's automation is built, not looted. Four quests ask for multiblock kits; none
of them depends on anything, so they can be done in any order.

| Verified quest title | Task items in the config |
|---|---|
| **Runic Star Altar** | `modern_industrialization:star_altar` |
| **Runic Crucible** | `modern_industrialization:runic_crucible`; `forbidden_arcanus:rune_block` ×4, `forbidden_arcanus:quantum_injector`, `forbidden_arcanus:arcane_crystal_block` ×5, `forbidden_arcanus:arcane_polished_darkstone_pillar` ×4, `forbidden_arcanus:arcane_polished_darkstone` ×4, `forbidden_arcanus:polished_darkstone_stairs` ×19, `forbidden_arcanus:gilded_chiseled_polished_darkstone`, `forbidden_arcanus:polished_darkstone` ×16 |
| **Automatic Hepheastus Forge** *(spelled that way in the config)* | `modern_industrialization:auto_forge`; `forbidden_arcanus:hephaestus_forge_tier_5`, `forbidden_arcanus:quantum_injector`, `forbidden_arcanus:darkstone_pedestal` ×8, `forbidden_arcanus:gilded_chiseled_polished_darkstone` ×9, `forbidden_arcanus:chiseled_arcane_polished_darkstone` ×4, `forbidden_arcanus:arcane_crystal_obelisk` ×4, `forbidden_arcanus:polished_darkstone_slab` ×24, `forbidden_arcanus:polished_darkstone_stairs` ×32, `forbidden_arcanus:arcane_polished_darkstone` ×8, `forbidden_arcanus:rune_block` ×4, `forbidden_arcanus:polished_darkstone` ×64, ×64, ×8 |
| **Runic Enchanter** | `modern_industrialization:runic_enchanter`; `forbidden_arcanus:quantum_injector`, `minecraft:soul_lantern` ×4, `minecraft:enchanting_table`, `forbidden_arcanus:darkstone_pedestal` ×8, `forbidden_arcanus:arcane_polished_darkstone_pillar` ×12, `forbidden_arcanus:gilded_chiseled_polished_darkstone` ×9, `forbidden_arcanus:polished_darkstone_slab` ×20, `forbidden_arcanus:polished_darkstone_stairs` ×42, `forbidden_arcanus:rune_block` ×16, `forbidden_arcanus:arcane_crystal_block` ×12, `forbidden_arcanus:polished_darkstone` ×64, ×8 |

What the quest text says each one is for, quoted:

- **Runic Star Altar** — *"Just like making the ATM Star normally, automating it needs to
  be within the Runic Star Altar!"*, and *"Check out the Quest in Chapter 3 to learn how to
  build and use it."* (Chapter 3's own Runic Star Altar quest is component #1 in
  `references/atm-star-checklist.md`, where the build and its upgrades are described.)
- **Runic Crucible** — *"Alright another Multiblock! This one requiring more ports than any
  Naval Base has seen!"*; it wants fluid input/output and item input/output hatches, and
  per its text *"Finally, we'll use the Liquid Souls, Liquefied Source, and some items from
  Mekanism to craft Obsidiansteel."* Obsidiansteel is what the Corrupti Dust line below
  needs automated.
- **Automatic Hepheastus Forge** (Modern Industrialization 2.5.8 `auto_forge` +
  Forbidden Arcanus 2.6.1 tier-5 forge) — *"One of the most important Multiblocks, mostly
  because we need it for the other Multiblocks."* and *"Or craft our Items needed for the
  Star Parts! You'll need a lot of Blood, Aureal, Souls, and Energy for them!"*
- **Runic Enchanter** — the pack's answer to *"Enchanting can't be completely automated!
  And you can't choose which Enchants you want, you have to get Lucky!"*; its text says
  *"You'll need to make Infused Dragon's Breath and Mending Books to remake the ATM Star!"*
  and that its inputs include Source and XP Fluid. Which enchants it can produce: the quest
  entry and JEI — not this page.

### The bees, and the Star Shards they make

Three quests, in a strict chain; **Star Shards** is the item every prism quest below also
requires, so this is the chapter's throughput bottleneck.

| # | Verified quest title | Task item | Needs |
|---|---|---|---|
| 1 | **Patrick Star... Bee?** | `biome minecraft:warm_ocean` (a biome task, not an item) | nothing |
| 2 | **Starry Bee!** | `allthetweaks:atm_star_block` | Patrick Star... Bee? |
| 3 | **Star Shards** | `allthetweaks:atm_star_shard` | Starry Bee! **and** *But why?* |

Quoted from the quest text: *"In order to automate ATM Star crafting, we'll need Star
Shards. In order to get Star Shards we'll need Starry Bees."* and *"You can rarely get
Patrick Bees by fishing in Warm Oceans!"*; then *"By Right Clicking a Patrick Bee with an
ATM Star Block, you'll get a Starry Bee!"* — with the warning *"You'll need another ATM
Star Block for them to pollinate... I probably should have told you that before..."* — and
*"The Starry Bees will make Starry Combs which can then be used in a Centrifuge to rarely
get Star Shards!"*

**But why?** (`mekanism:crusher`, no dependencies) is the alternate route: *"Technically you
can also use the Crusher to make the ATM Star into 5 Star Shards... But you'll need 262 to
make a new Star... So why would you?"* — and **Star Shards** repeats the arithmetic:
*"You'll need 262 Star Shards total to remake 1 Star... hope you've got a good Bee set
up!"*

### The five prism quests → the five star parts

Each star part needs one prisms-line quest, and each prism needs **Star Shards** plus the
**Automatic Hepheastus Forge**. Dependency links verified in the config; the parts are the
pack's own *1/5* … *5/5*, subtitled on the canvas in that order.

| Star part (verified title + subtitle) | Task item | Fed by (verified title) |
|---|---|---|
| **Top ATM Star part** *(1/5)* | `kubejs:atm_star_shard_1` | **Soul Binding Crystal** → `forbidden_arcanus:soul_binding_crystal` |
| **Right ATM Star part** *(2/5)* | `kubejs:atm_star_shard_2` | **Whirlwind Prism** → `forbidden_arcanus:whirlwind_prism` |
| **Bottom Right ATM Star part** *(3/5)* | `kubejs:atm_star_shard_3` | **Smelter Prism** → `forbidden_arcanus:smelter_prism` |
| **Bottom Left ATM Star part** *(4/5)* | `kubejs:atm_star_shard_4` | **Sea Prism** → `forbidden_arcanus:sea_prism` |
| **Left ATM Star part** *(5/5)* | `kubejs:atm_star_shard_5` | **Terrastomp Prism** → `forbidden_arcanus:terrastomp_prism` |

The five part quests are the only KubeJS items in the chapter (`kubejs:atm_star_shard_1`
… `_5`), i.e. pack-defined pieces — recipe-shaped detail is JEI's. In the quest quotes
below, *HNN* is the pack's shorthand for Hostile Neural Networks 6.5.1 and *MA* for
Mystical Agriculture 8.0.28 (both named in the modlist). What the quest text says about the
prisms, quoted:

- **Soul Binding Crystal** — *"The Soul Binding Crystal is the most difficult one to
  craft."*, with *"Finally, combine Souls with Liquid Aureal and the Holy Hand Grenade to
  make Enchanted Souls."*
- **Sea Prism** — *"Honestly just use MA for this one. It is the easiest way to get all of
  them."* (Mystical Agriculture 8.0.28.)
- **Terrastomp Prism** — *"This ones a little more expensive but also a little more fun!"*
  (diamonds, flint, dripstone — its text's own examples).
- **Whirlwind Prism** — *"This one I'd argue is the easiest to automate."* (phantom
  membranes, feathers, wool via HNN; the bat wing *"more difficult needing to be farmed via
  spawners"*).
- **Smelter Prism** — *"Very simple recipe, only needing Coal, Blaze Powder, and an Arcane
  Crystal Block."* — quoted; the recipe itself is the quest entry's and JEI's business.

### The two dusts and the lens chain

Three short branches off the spine, all verified:

| Branch | Quest chain (verified titles) | Task items |
|---|---|---|
| Mundabitur Dust | **Arcane Crystals** (no dependencies) → **Mundabitur Dust** | `forbidden_arcanus:arcane_crystal`; `forbidden_arcanus:mundabitur_dust` |
| Corrupti Dust | **Runic Crucible** (no dependencies) → **Corrupti Dust** | `modern_industrialization:runic_crucible` …; `forbidden_arcanus:corrupti_dust` |
| The Lenses | *(no title in the config)* → **Lens of Certain Death** → **Lens of the Killer** | `actuallyadditions:atomic_reconstructor`; `actuallyadditions:lens_of_certain_death`; `actuallyadditions:lens_of_the_killer` |

The lens chain is Actually Additions 1.3.26: the untitled first quest asks for the
**Atomic Reconstructor** — *"For such a simple recipe you actually get a pretty darn useful
Machine!"* — and the last one says *"Now we just need to craft! Craft the Lens of Certain
Death, with a Diamond Sword, and Enchanted Book of Sharpness V."*, adding *"You can get the
Enchanted Books from the Runic Enchanter!"*

On the dusts: **Arcane Crystals** says *"You'll have to mine for Arcane Crystals first;
then, you can use MA or Bees to make more!"*; **Mundabitur Dust** says automation needs
*"Bonemeal, Gunpowder, Redstone, Blaze Powder, and Phantom Membrane ... automated with HNN
or MA"*; **Corrupti Dust** ends *"Just Obsidiansteel will need to be automated from the
Runic Crucible."*

### Infused Patrick Star — the Runic Enchanter line

**Infused Patrick Star** (task `allthetweaks:patrick_star`) is the last dependency before
the terminal quest, and it has a two-quest tail behind it:

| # | Verified quest title | Task items |
|---|---|---|
| 1 | **Runic Enchanter** (multiblock, no dependencies) | see above |
| 2 | *(no title in the config)* | `apothic_enchanting:infused_breath`, `minecraft:enchanted_book` |
| 3 | **Infused Patrick Star** | `allthetweaks:patrick_star` |

Quest text, quoted: *"In order to remake the ATM Star we'll need an Infused Patrick Star,
which also needs a Patrick Star for it. Both are made via Runic Star Altar."*, and *"Throw
all of these into a Runic Star Altar, plus 85MFE, and we'll get our Infused Patrick
Star!"* The middle quest is where Infused Dragon's Breath and Mending Books come from (its
text calls them *"the two Items we need via Runic Enchanter"*), and Apothic Enchanting
1.6.2 supplies `apothic_enchanting:infused_breath`. **85MFE is the quest author's own
figure** — quote it as quest text, and confirm in the quest entry if it matters.

## The terminal quest: Fully Automated ATM Star

**Fully Automated ATM Star** (task `allthetweaks:atm_star`) closes the spine, with exactly
**10 direct dependencies**: Runic Star Altar; Infused Patrick Star; the five ATM Star parts;
Mundabitur Dust; Corrupti Dust; Lens of the Killer. Its own text, quoted:

> *"With the Infused Patrick Star, 5 Star Fragments, Corrupti Dust, Mundabitur Dust, and
> the Lens of the Killer we can rebuild ATM Stars, 100% automated!"*
>
> *"Now these Creative Items will be a breeze to craft!"*

The config's reward table for it pays **50 × `allthetweaks:atm_star_shard`**, **1 ×
`allthetweaks:patrick_star`**, and **50 XP levels** — quoted from the config, not a promise
about a future pack version. This is the quest the whole chapter exists for: once the spine
is automated, stars stop being a one-off and become a supply.

## The eleven creative-tier quests (in the config's order)

Every one of these hangs off *Fully Automated ATM Star* by a single dependency, and each
has exactly one task — the creative item itself. "What the quest text says" is a quote or
close paraphrase of that quest's own description; the mod and version are the modlist's.

| # | Verified quest title | Task item (config) | What the quest text says it gives you |
|---|---|---|---|
| 1 | **Energy Cell (Creative)** — subtitle *Unlimited Powah!* | `powah:energy_cell_creative` | Powah 6.2.10's creative energy cell; its text only warns about the Nitro Cell chain (*"I'm not doing this math, get a Recipe Tree"*) |
| 2 | **Creative Energy Cube** | `mekanism:creative_energy_cube` | *"Full Cubes work as an infinite energy storage"* (empty ones void energy); *"Energizing 4 empty Energy Cubes with an ATM Star you can get the full one."* |
| 3 | **Creative Jetpack** | `ironjetpacks:jetpack` | *"You'll neever need to worry about that again!"*; *"You might need to make every Jetpack before it, an ATM Star, plus more expensive Items"* (Iron Jetpacks 8.0.11) |
| 4 | **Creative Compressed Iron Blocks** | `pneumaticcraft:creative_compressed_iron_block` | *"This can be set to any temperature you want it to be set to, which can then be used in your Machines."*; *"8 Stacks of Compressed Iron Blocks equals 4,608 Compressed Iron Ingots"* |
| 5 | **Creative Compressor** | `pneumaticcraft:creative_compressor` | *"allows you to choose any Bar Pressure you want! Positive, Negative, even 0! It can be used within Machines."* |
| 6 | **Creative Spellbook** | `allthearcanistgear:creative_spell_book` | *"It has the same configs as an Unobtainium Spellbook but has infinite Mana and all Glyphs unlocked!"* (All The Arcanist Gear 1.21.1-21.3.2; built on the Ars Nouveau 5.13.1 creative book) |
| 7 | **Creative Source Jar** — subtitle *Get this first!* | `ars_nouveau:creative_source_jar` | *"This jar is always full of Source and can be linked to anything needing Source. Including the ATM Star multiblocks."*; its text adds *"Don't worry this will be changed to be even harder!"* |
| 8 | **Creative Energy Battery** | `integrateddynamics:energy_battery_creative` | *"The easiest infinite Energy storage, only needing 4 Energy Batteries (from ID) and a Star!"* (IntegratedDynamics 1.37.1) |
| 9 | **Creative Energy Cell** | `ae2:creative_energy_cell` | *"works like normal infinite energy storage, just this one can connect to your system"* (Applied Energistics 2 19.2.17) |
| 10 | **Creative Locomotive** | `railcraft:creative_locomotive` | *"They work like normal Locomotives just without needing Fuel or Energy! Just need Rails."* (Railcraft Reborn 1.2.10) |
| 11 | **Creative Blood Drop** | `evilcraft:blood` | *"you can fill any container that needs Blood infinitely!"* (EvilCraft 1.2.96) |

Two task ids are **generic on purpose** — *Creative Jetpack* points at
`ironjetpacks:jetpack` and *Creative Blood Drop* at `evilcraft:blood`, exactly as the config
lists them; which jetpack tier or which blood variant the entry wants is set in the quest
entry. Treat the mapping from those ids to a specific item as approximate and check the
book.

Also note that the pack has **two** items named "Creative Energy Cell" — the Powah one
(*Energy Cell (Creative)*) and the AE2 one (*Creative Energy Cell*). The quest text calls
that out for Powah: *"not to be confused with the other Creative Energy Cell"*. When a
player says "the creative energy cell", ask which mod's he means.

There are **no boss tasks** anywhere in this chapter — its 38 quests carry only `item` and
`biome` tasks — so nothing here needs `references/boss-checklist.md`; the bosses the star
itself needs (Cataclysm, Piglich, Warden, Twilight Forest) are Chapter 2/3 business and are
mapped there.

## Cross-references

- `references/atm-star-checklist.md` — Chapter 3's 13 star components by source mod,
  including the Runic Star Altar build this chapter's *Runic Star Altar* quest points back
  at, plus the Star's Casing and the awakened alloy.
- `references/boss-checklist.md` — every boss the pack tracks. Not needed for this chapter
  (no boss tasks), but the star's boss-gated components are listed there.
- `references/progression.md` — where Chapter 4 sits in the four-stage map, and how it fits
  the Main Questline order.

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item above is a quest *task*; JEI has the recipe, and recipes
  are where pack versions differ most.
- **Machine tiers, energy amounts, farm layouts, hatch counts.** The quests' own
  descriptions cover them in-game (quoted where this page quotes); the page stays out.
- **An order the book does not have.** The config links quests into a graph and lays them
  out on a canvas; the "1/5 … 5/5" subtitles are the five parts' own labels, not a
  chapter-wide sequence. Anything beyond the verified dependency order is *approximate*.
- **Reward tables beyond the terminal quest.** Only *Fully Automated ATM Star*'s three
  rewards are quoted here (it is the one the chapter's payoff hangs on); every other
  quest's rewards are in the book.
- **Anything not in the config.** If a player names a creative item, automation, or count
  that is not listed here, the answer is "open that quest in the book / look it up in JEI" —
  never a guess.
