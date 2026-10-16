# Mystical Agriculture and Mystical Agradditions progression in ATM10

**Short answer (judgement, not a quest requirement):** The mod's own ladder is a chain of
essence tiers — **Inferium** → **Prudentium** → **Tertium** → **Imperium** → **Supremium** →
**Awakened Supremium** → **Insanium** (Tier 6, from Mystical Agradditions) → **Creative
Essence** — and every tier is compacted from four of the tier below plus an Infusion Crystal.
Start it early: the pack's own *Inferium Farmland* quest says *"You'll want to start growing
Inferium as soon as you can!"*. Seeds are made on the **Infusion Altar**, planted on the
matching tier's **Farmland**, and the top of the ladder feeds Chapter 3's ATM Star. Which
seed to plant first, how big a plot to build, and whether to buy essence gear are choices —
the config does not rank them. Nothing below is a recipe: **JEI** and your book are.

## Provenance and limits

This is a snapshot of [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main`
commit [`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22, pack 8.2). The mod versions are
Mystical Agriculture 8.0.28, Mystical Agradditions 8.0.14, and Cucumber Library 8.0.16 — come from `config/crash_assistant/modlist.json`.
The quest titles, quest ids, task items, `Tier:` subtitles, dependencies, and every sentence
in quotation marks were read from the Mystical Agriculture chapter's config
(`config/ftbquests/quests/chapters/elmystical_agriculturerr.snbt` and
`config/ftbquests/quests/lang/en_us/chapters/elmystical_agriculturerr.snbt`), plus the
Chapter 3: The ATM Star entries named below, with this skill's own `scripts/snbt.py`; the
same snapshot is printed in full in `references/farming-guide.md` (all 191 quests of the
chapter, including the 125 seed quests) and summarised in
`references/resource-farming-guide.md` and `references/atm-star-checklist.md`. **The
in-game quest book is authoritative** if your installed pack differs; check it, and check
JEI for every recipe, count, growth rate, and energy cost. Advice explicitly marked
*judgement* is not a pack rule. No recipe, drop chance, growth rate, or machine speed is
stated here from memory, and no quest title or quest id appears on this page that is not in
that snapshot.

## The choices — the essence tiers, and what each is worth (*judgement*)

The **Needs** column is the config's own dependency link, and it is not always the tier
order: Prudentium hangs off *Infusion Crystal*, and Insanium hangs off Supremium rather than
off the awakened tier.

| Tier (config subtitle) | What the pack actually says | Recommendation (*judgement*) |
|---|---|---|
| **Inferium** — `Tier: 1` (`1CC4F8570A7A99EB`) | Entered through **Mystical Agriculture!** (`54735C5FCD2077B3`), which has no prerequisites and asks only for any item in the tag `c:seeds`. Its essence, per the quest text, comes *"from mining, killing mobs, or by making seeds to grow them!"* **Inferium Farmland** (`7DFF18CFEB0B8DBE`) asks for `mysticalagriculture:inferium_farmland` and `mysticalagriculture:inferium_seeds` and says *"You'll want to start growing Inferium as soon as you can!"*; it also warns *"certain seeds will require certain farmlands to be planted on."* | Your first plot and your long-term bulk source. Chapter 3's star arithmetic is quoted as *"So you'll need 36,864 Inferium Essence total!"*, so treat this as a farm you keep running, not a quest you finish. |
| **Prudentium** — `Tier: 2` (`73350AD668200E99`) | *"This is the Tier 2 Essence, made by combining 4 Inferium together with an Infusion Crystal."* Depends on **Infusion Crystal** (`217DB12EA32E1724`). | Compact early and often, and keep the crystal. The Tier 2 farmland also gates the cheap bulk seeds (coal, silicon, sulfur, redstone-tier metals sit one tier up). |
| **Tertium** — `Tier: 3` (`2C9C9CB71941DC01`) | Same sentence one tier up — 4 Prudentium plus an Infusion Crystal. | The usual mid-game rung: iron, copper, tin, redstone, glowstone and the alloy seeds are Tier 3, gated on Tertium Farmland. Build the plot you actually harvest here. |
| **Imperium** — `Tier: 4` (`66C52B137A4FF869`) | Same sentence again — 4 Tertium plus an Infusion Crystal. | Tech-stage rung: gold, steel, uranium, fluix, the alloy seeds, and the blaze / enderman / ghast mob seeds. |
| **Supremium** — `Tier: 5` (`67DBE6C59C0D9D1B`) | Its description carries a **typo in the config**: it reads *"This is the Tier 4 Essence, made by combining 4 Imperium together with an Infusion Crystal."* while its subtitle says `Tier: 5`; the subtitle and the dependency chain agree on 5. | The diamond / emerald / netherite rung, and the gate to the awakened tier. Do not "correct" the quote when you repeat it — say what the book says. |
| **Awakened Supremium** — `Tier: 5 - Awakened` (`7A103577EAE7B3F1`) | Needs **The Awakening** (Awakening Altar, pedestals ×4, Essence Vessels ×4) **and** **Cognizant Dust** ×4; the dust is *"dropped from the Wither and the Ender Dragon when killed by an Essence Weapon enchanted with Mystical Enlightenment."* | Endgame, and boss-gated: plan the two kills before you plan the farm (see `references/boss-guide.md`). |
| **Insanium** — `Tier: 6` (`202B1F54D3F06DAB`, `mysticalagradditions:insanium_essence`) | *"This is the Tier 6 Essence, made by combining 4 Supremium together with an Infusion Crystal."* Depends on Supremium, not on the awakened tier. | What Mystical Agradditions adds on top of the base mod, with **Insanium Farmland** and the cruxes. Only worth pushing into when the star's blocks are your goal. |
| **Creative Essence** — `Tier: Creative` (`6D0A876D4E4D35AB`, `mysticalagradditions:creative_essence`) | *"Creative Essence is needed to craft the ATM Star."* Depends on Insanium. | The top of the ladder is a star component, not a gear tier. Full mapping: `references/atm-star-checklist.md`. |

**Seed tiers, in one line.** Every seed quest in the chapter is untitled — the book shows the
seed's own item name — and carries a `Tier:` subtitle; `references/farming-guide.md` lists
all 125 by tier and by the gate each needs. Tier 6 and Magical seeds additionally need a
block placed below the farmland: *"To grow Tier 6 or Magical Seeds you need to have a
certain Crux placed directly below the Farmland they are growing on."* (Insanium Farmland),
and for the three ATM-ore seeds, `kubejs:magical_soil` — *"Allthemodium Seeds require
Magical Soil placed below in order for them to grow."*

**Armor and tool essences — the honest limit.** These snapshots verify exactly two
gear-adjacent things in the chapter: an **Essence Weapon** enchanted with **Mystical
Enlightenment**, named only inside the Cognizant Dust quote above, and an untitled
**Scythes** quest for the item tag `cucumber:scythes` (*"Scythes are tools that can farm
large areas of crops all at once."*). No armor or tool *set* is quoted here, because no
verified quest title, task item, or recipe for one is in this snapshot — so there is
**no unverified armor set claim on this page**. Look the sets up in JEI (which shows each
piece's own recipe and its tier) and in your book's untitled quests; the verified armor
ladder this pack's boss fights are measured against is diamond → netherite → allthemodium →
vibranium → unobtainium, in `references/armor-tools-ladder.md`. Choosing essence gear over
that ladder is *judgement*, not a quest requirement.

## Getting more essence (*judgement*, on verified machines)

| Route | What the pack's quest text says | When to take it (*judgement*) |
|---|---|---|
| **Infusion Altar** (`0B37355262121DD5`, altar plus pedestals ×8) | *"The Infusion Altar is how you make all of the seeds."* and *"In order for the Infusing to start, the Alter requires a Redstone signal."* (sic). The optional **Wand** quest: *"The Wand can be used to activate the Infusion Alter, just right-click on the altar to activate the infusion process."* | Always — this is the seed factory. Reached through **Prosperity Shards** (`2DDA04088C8220D2`, *"To find some Prosperity Ore, go mining."*) → **Prosperity Seed Base** (`1E0F92F07FDD162E`). |
| **Compacting** | Four of a tier plus a crystal make the next tier up, per the tier quotes above; **Master Infusion Crystal** (`mysticalagriculture:master_infusion_crystal`, needs Supremium) *"works the same as the Infusion Crystal but it never breaks."* | Swap to the master crystal once you can — the breakable one is a silent tax on bulk crafting. |
| **Seed Reprocessor** (untitled quest, subtitle *Recycling!*) | *"The Seed Reprocessor can convert essence seeds back into essences."* | Whenever a seed line over-produces; it turns spare seeds back into ladder fuel. |
| **Growth Accelerators** | *"Growth Accelerators of all tiers provide the same rate of growth ticks. Higher tiers however have a larger range, so you can stack more of them below a single plant."* The quests give ranges of 9 / 18 / 27 / 36 / 45 / 54 blocks, one per essence tier. | Under a single big plot rather than scattered. Higher tier means footprint, not speed — do not expect a faster tick from the upgrade alone. |
| **Tiered Farmland** | *"However, certain seeds will require certain farmlands to be planted on."* Each essence tier has a matching farmland quest, and Insanium Farmland adds the crux rule. | Match the farmland to the seed's own tier before you debug a crop that will not plant. |
| **Mob seeds and Soulium** | **Creating Mob Seeds** (needs Prudentium; Soulium Dagger, Soul Jars ×4, Soul Extractor): *"Most seeds are simple to make, but to make Mob Seeds, you'll need to head to the Nether to pick up some Soulium."* and *"Alternatively, you can fill Soul Jars inside of the Soul Extractor by inserting a jar and using mob items to fill them."* | Take the Soulium trip once, then decide between a dagger route and jars fed by a mob farm — the jar route pairs with `references/mob-farm-progression.md`. |
| **Harvester and upgrades** (untitled quests) | *"The Harvester can auto-harvest crops and re-plant them. Items collected by the Harvester are put into its internal inventory."* / *"Machine Upgrades are used to speed Mystical Agriculture machines."* / the Watering Can quest: *"Essence Watering cans have the ability of auto-watering."* / **Mystical Fertilizer** (optional): *"It instantly grows whatever it is used on to full maturity."* | Once a plot is producing by hand. Alternatives: the Harvester Pylon and Industrial Foregoing, both in `references/farming-guide.md`. |
| **Bees** (optional **Automating Awakened Supremium**) | *"Awakened Supremium and other tiered essences can be farmed using the Productive Bees mod."* | When the star's quantities make hand plots unrealistic. |
| **The Soulium Spawner** (untitled quest) | *"The Soulium Spawner uses mob essences to spawn mobs."* | Only if mob essences are your bottleneck; compare it with the spawner runes in `references/mob-farm-progression.md`. |

**Costs and caveats this snapshot does not settle.** No recipe, growth rate, drop chance, or
energy figure is quoted here, because the config does not state one. Mystical Agriculture's
machines need power and space (`references/power-guide.md`, `references/storage-ladder.md`);
anything you want ticking while you are away needs claimed, force-loaded chunks
(`references/chunk-loading-guide.md`); and a fast farm is a known TPS risk in this pack —
`references/lag-fix-guide.md` quotes the pack's own warning about over-modified harvesters.
Bulk autocrafting of the star's blocks is `references/autocrafting-guide.md` territory.

## Where this crosses into other guides

- `references/farming-guide.md` — the same chapter in full: all 191 quests, the 125 seed
  quests by `Tier:` subtitle, the other seven farming chapters, and the pack's own answer to
  *"what should I set up farming first?"*.
- `references/resource-farming-guide.md` — *"where do I get X?"*, including the allthemodium,
  vibranium, and unobtainium seeds as one route to the gated metals.
- `references/allthemodium-mining-guide.md` — the mining route to those same three ores.
- `references/atm-star-checklist.md` — Chapter 3's Mystical Agriculture hub and its quoted
  arithmetic: Creative Essence, 4 Insanium Blocks, 4 Insanium Gemstone Blocks, the Insanium
  Coal Block, the Awakened Supremium Ingot Block, and the Master Infusion Crystal.
- `references/armor-tools-ladder.md` — the verified armor and tool ladder to compare essence
  gear against.
- `references/boss-guide.md` and `references/boss-checklist.md` — the Wither and Ender Dragon
  kills the awakened tier depends on.
- `references/mob-farm-progression.md`, `references/chunk-loading-guide.md`,
  `references/lag-fix-guide.md`, `references/power-guide.md`, `references/storage-ladder.md`,
  `references/autocrafting-guide.md` — the supporting systems a big essence farm leans on.
- `references/progression-roadmap.md` — which phase of the pack you are in, and therefore
  which tier is worth pushing to next.

**What to do first (*judgement*):** Open the chapter through **Mystical Agriculture!** (any
seeds at all) and finish both entry lines — Inferium → **Inferium Farmland** and **Infusion
Crystal**, and **Prosperity Shards** → **Prosperity Seed Base** → **Infusion Altar**. Plant
Inferium Seeds on Inferium Farmland, and compact 4:1 up the ladder with the crystal you just
made. Only then pick the seeds you actually need from the tier table in
`references/farming-guide.md`, add a Harvester (or a Harvester Pylon) once the plot is
growing, and put Growth Accelerators under it rather than beside it. Push to the awakened and
Tier 6 rungs only when the star's components are the goal, and read
`references/atm-star-checklist.md` before you commit to that quantity of farming. There is
**no verified best plot size, growth rate, seed-crafting recipe, or essence-armor
requirement** here: no recipe, growth rate, drop chance, or energy figure appears in this
guide, consult the in-game quest book and JEI for your version.
