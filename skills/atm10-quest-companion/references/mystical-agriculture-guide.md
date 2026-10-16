# Mystical Agriculture & Mystical Agradditions — progression guide (ATM10)

**Short answer (judgement, not a quest requirement):** Start the **Mystical Agriculture**
chapter at the bottom — **“Inferium”** (`1CC4F8570A7A99EB`), its farmland and its seeds,
growing while you do anything else — then climb the essence ladder in the chapter's own
dependency order: **“Inferium”** → **“Prudentium”** → **“Tertium”** → **“Imperium”** →
**“Supremium”** → **“Awakened Supremium”** → **“Insanium”** → **“Creative Essence”**, where
the last two rungs come from **Mystical Agradditions**. Your real output is seeds: the
chapter's seed quests are sorted by a `Tier:` subtitle, and each tier is gated on its own
farmland (from Tier 6 up, on a crux placed below the farmland instead). None of this is a
quest requirement about *where*, *how large*, or *how fast* a farm has to be — it is a
reading of the ladder the book already lays out, and every extra recommendation below is
labelled *judgement*.

## Provenance and limits

This page **reproduces this skill's verified snapshot instead of re-reading the pack
repository while writing it**. Every tier, `Tier:` subtitle, quest id, dependency and quoted
sentence below is carried over from `references/farming-guide.md`, which was read from the
official [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) repository at `main`
commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22, pack 8.2 — the version `CHANGELOG.md` lists, the `modpackVersion`
`config/bcc-common.toml` stamps, and the `"8.x"` stamp in `examples/progress.example.json`).
The quest titles, subtitles and descriptions come from
`config/ftbquests/quests/lang/en_us/chapters/elmystical_agriculturerr.snbt` and the matching
`config/ftbquests/quests/chapters/elmystical_agriculturerr.snbt` at that commit; mod names
and versions (**Mystical Agriculture 8.0.28**, **Mystical Agradditions 8.0.14**, Cucumber
Library 8.0.16) come from `config/crash_assistant/modlist.json`. No pack file was re-read for
this page, so read the ids here as *what the book asked for in 8.2*, not as a live check of
your install. **The in-game quest book is authoritative** if your installed pack differs;
check it (and JEI for recipes). Advice explicitly marked *judgement* is not a pack rule. No
recipe, growth rate, drop chance, accelerator value, or machine-to-machine link is implied
here.

Grounding rules for everything below:

- **Only the config's own words are quoted.** Text in straight quotes is quest text from the
  snapshot; everything else is this page's summary or a labelled recommendation.
- **Titles are the config's.** A name the snapshot gives a title to is written here in
  typographic double quotes (as in the tables below). A name
  written without quotes (an item id, or a task name such as *Scythes*) is not a title —
  several of this chapter's quests have no title in the config, and the book shows the task
  item's own name instead. Do not present a derived name as a verified title.
- **Ids only where the snapshot has them.** Most titles below carry the id
  `references/farming-guide.md` records; a few verified titles there carry none, and are
  marked *(id not in the snapshot)*.
- **No recipes, no numbers from memory.** Item ids and the quoted sentences are the
  snapshot's; how a seed is assembled, how much anything yields, and how fast it grows are
  in JEI and in-game, never here.
- **Approximate means approximate.** Whether a given harvester or planter accepts a
  Mystical Agriculture seed is version-sensitive and not in the config — check in-game.
- **The order and the emphasis are judgement, and labelled so.** The config links quests
  into a graph inside the chapter; it does **not** tell the player to farm a specific tier
  first, to build a certain layout, or to make gear at any point. Those calls are marked
  *judgement*.

## The ladder — the tiers the chapter actually has

The **Needs** written in the table are the quest's real dependency in the config, not an
implied one. Prudentium hangs off **“Infusion Crystal”** (which hangs off Inferium), and
**“Insanium”** hangs off Supremium — not off the awakened rung.

| Rung | What the pack actually says | Recommendation (*judgement*) |
|---|---|---|
| **“Inferium”** (`1CC4F8570A7A99EB`) — subtitle `Tier: 1`, task `mysticalagriculture:inferium_essence`, needs *“Mystical Agriculture!”* (`54735C5FCD2077B3`) | The chapter's entry rung; its farmland quest **“Inferium Farmland”** (`7DFF18CFEB0B8DBE`) asks for `mysticalagriculture:inferium_farmland` plus `mysticalagriculture:inferium_seeds`. **“Prosperity Shards”** (`2DDA04088C8220D2`) and **“Infusion Crystal”** (`217DB12EA32E1724`) also open off Inferium. | Start here and start early — it is the cheapest rung and everything above it is built from it. How much land you give it is your call. |
| **“Prudentium”** (`73350AD668200E99`) — `Tier: 2`, task `mysticalagriculture:prudentium_essence`, needs *“Infusion Crystal”* | Quoted: *"This is the Tier 2 Essence, made by combining 4 Inferium together with an Infusion Crystal."* Its farmland quest asks for Prudentium Farmland, and it is the gate for **“Creating Mob Seeds”** *(id not in the snapshot)*. | Make the Infusion Crystal before planning the jump to Tier 2 — the crystal is what the book makes the rung depend on. |
| **“Tertium”** (`2C9C9CB71941DC01`) — `Tier: 3`, task `mysticalagriculture:tertium_essence`, needs *“Prudentium”* | The config repeats the tier sentence one rung up (the same "combining 4 … together with an Infusion Crystal" wording), and adds a Tertium Farmland quest. | Only worth it once the previous rung is steady; seeds, not essence, are usually the reason to climb. |
| **“Imperium”** (`66C52B137A4FF869`) — `Tier: 4`, task `mysticalagriculture:imperium_essence`, needs *“Tertium”* | Same sentence pattern again, plus Imperium Farmland. This is where the metal and alloy seeds live (see the seed table). | Climb when you want those seeds; this rung is mid-game, not a wall. |
| **“Supremium”** (`67DBE6C59C0D9D1B`) — `Tier: 5`, task `mysticalagriculture:supremium_essence`, needs *“Imperium”* | **The config's description carries a typo here:** it reads *"This is the Tier 4 Essence, made by combining 4 Imperium together with an Infusion Crystal."* while the subtitle says `Tier: 5` and the dependency chain agrees on 5 — quote the subtitle, not the sentence's number. **“Master Infusion Crystal”** (`mysticalagriculture:master_infusion_crystal`, *id not in the snapshot*) also needs Supremium: *"The Master Infusion Crystal works the same as the Infusion Crystal but it never breaks."* | Treat Supremium as the last *ordinary* rung; everything past it leaves the crop-only line. |
| **“Awakened Supremium”** (`7A103577EAE7B3F1`) — `Tier: 5 - Awakened`, task `mysticalagriculture:awakened_supremium_essence`, needs **“The Awakening”** *and* **“Cognizant Dust”** | The Awakening asks for `mysticalagriculture:awakening_altar`, `mysticalagriculture:awakening_pedestal` ×4 and `mysticalagriculture:essence_vessel` ×4; Cognizant Dust is `mysticalagriculture:cognizant_dust` ×4, quoted: *"This special Dust is dropped from the Wither and the Ender Dragon when killed by an Essence Weapon enchanted with Mystical Enlightenment."* | Expect two boss trips before this rung (see `references/boss-checklist.md`). It has no farmland of its own; its accelerator quest goes furthest (`Range: 54 Blocks`). |
| **“Insanium”** (`202B1F54D3F06DAB`) — `Tier: 6`, task `mysticalagradditions:insanium_essence`, needs *“Supremium”* | **Mystical Agradditions** territory. Quoted: *"This is the Tier 6 Essence, made by combining 4 Supremium together with an Infusion Crystal."* Its farmland, Insanium Farmland (`mysticalagradditions:insanium_farmland`), is where cruxes start mattering. | Climb it for Tier 6 seeds and the ATM Star components, not for the essence itself. |
| **“Creative Essence”** (`6D0A876D4E4D35AB`) — `Tier: Creative`, task `mysticalagradditions:creative_essence`, needs *“Insanium”* | Quoted: *"Creative Essence is needed to craft the ATM Star."* The two other chapter entries the star wants are `mysticalagradditions:insanium_coal_block` (needs Insanium) and `mysticalagriculture:awakened_supremium_ingot_block` (needs Awakened Supremium), each with its own "needed to craft the ATM Star" line. | Endgame only. Chapter 3's side of these components is in `references/atm-star-checklist.md`. |

Two things the tiers share, both quoted from the config:

- **Growth Accelerators.** *"Growth Accelerators of all tiers provide the same rate of growth
  ticks. Higher tiers however have a larger range, so you can stack more of them below a
  single plant."* The tier's accelerator quest carries the accelerator's `Range:` subtitle —
  9, 18, 27, 36, 45 and 54 Blocks as you go up the ladder. The config gives no title for
  those quests, so none is quoted here.
- **Farmland.** *"However, certain seeds will require certain farmlands to be planted on."*
  Every tier's farmland quest asks for that tier's farmland block — and from Tier 6 up the
  rule changes shape, next section.

### Cruxes, soil, and the top of the ladder

- Quoted from Insanium Farmland: *"To grow Tier 6 or Magical Seeds you need to have a
  certain Crux placed directly below the Farmland they are growing on."* Every Tier 6 seed
  quest also asks for its matching crux —
  `mysticalagradditions:awakened_draconium_crux`, `mysticalagradditions:dragon_egg_crux`,
  `mysticalagradditions:nether_star_crux`, `mysticalagradditions:nitro_crystal_crux` — and
  every Magical seed quest asks for `kubejs:magical_soil` instead (quoted: *"Allthemodium
  Seeds require Magical Soil placed below in order for them to grow."*).
- The Star's own numbers for these blocks come from Chapter 3, not from this chapter; that
  count is in `references/atm-star-checklist.md` and is not repeated here.
- *(judgement)* Treat the cruxes as a checkpoint: if a Tier 6 or Magical seed will not
  progress, the placement under the farmland is the first thing to check, not the seed.

## Which tier is my seed?

Every seed quest in the chapter is untitled — the book shows the seed's own item name — and
carries a `Tier:` subtitle. The count and gate below are the snapshot's; every seed id is
`mysticalagriculture:<name>_seeds`.

| `Tier:` subtitle | Seed quests | Gate besides **“Infusion Altar”** (`0B37355262121DD5`) |
|---|---|---|
| `Tier: 1` | 9 | Inferium Farmland |
| `Tier: 2` | 17 (materials) + 9 (mob seeds) | Prudentium Farmland for the first group; **“Creating Mob Seeds”** opens the mob line |
| `Tier: 3` | 27 (metals and materials) + 6 (mob seeds) | Tertium Farmland for the first group; the matching essence quest for the mob seeds |
| `Tier: 4` | 28 (metals, alloys, gems) + 5 (mob drops, plus `experience`) | Imperium Farmland for the first group; the matching essence quest for the second |
| `Tier: 5` | 16 + 1 | Supremium Farmland for the first group; Supremium for `wither_skeleton` |
| `Tier: 6` | 4 (`awakened_draconium`, `dragon_egg`, `nether_star`, `nitro_crystal`) | Insanium Farmland, **and** the matching crux below it |
| `Tier: Magical` | 3 (`allthemodium`, `unobtainium`, `vibranium`) | Insanium Farmland, **and** `kubejs:magical_soil` below it |

The mob seeds are the ones that need a detour: **“Creating Mob Seeds”** (needs *Prudentium*;
`mysticalagriculture:soulium_dagger`, `mysticalagriculture:soul_jar` ×4,
`mysticalagriculture:soul_extractor`) says *"Most seeds are simple to make, but to make Mob
Seeds, you'll need to head to the Nether to pick up some Soulium."* — and *"Alternatively,
you can fill Soul Jars inside of the Soul Extractor by inserting a jar and using mob items to
fill them."* That is the whole "soul" system in this guide: Soulium and Soul Jars for mob
seeds, nothing more, and no numbers are claimed for it.

Full seed name lists by tier are in `references/farming-guide.md`; they are not duplicated
here so the two pages cannot drift apart.

## Getting more out of the ladder — the chapter's own helpers

| Quest in the config | Task items | What its text says (quoted) |
|---|---|---|
| *(no title in the config; task* Scythes*)* | item tag `cucumber:scythes` | *"Scythes are tools that can farm large areas of crops all at once."* |
| *(no title in the config)* | `mysticalagriculture:harvester` | *"The Harvester can auto-harvest crops and re-plant them. Items collected by the Harvester are put into its internal inventory."* |
| **“Mystical Fertilizer”** (optional) | `mysticalagriculture:mystical_fertilizer` | *"It instantly grows whatever it is used on to full maturity."* |
| *(no title in the config; subtitle* Recycling!*)* | `mysticalagriculture:seed_reprocessor` | *"The Seed Reprocessor can convert essence seeds back into essences."* |
| *(no title in the config)* | `mysticalagriculture:watering_can` | *"Essence Watering cans have the ability of auto-watering."* |
| *(no title in the config; task* Machine Upgrades*)* | any `mysticalagriculture:*_upgrade` (inferium through awakened supremium) | *"Machine Upgrades are used to speed Mystical Agriculture machines."* |
| *(no title in the config)* | `mysticalagriculture:soulium_spawner` | *"The Soulium Spawner uses mob essences to spawn mobs."* |
| **“Wand”** (optional) | `mysticalagriculture:wand` | *"The Wand can be used to activate the Infusion Alter, just right-click on the altar to activate the infusion process."* (sic — the config spells it "Alter") |

The chapter's own crafting backbone, quoted: **“Infusion Altar”** — *"The Infusion Altar is
how you make all of the seeds."* — and *"In order for the Infusing to start, the Alter
requires a Redstone signal."* (sic). **“Prosperity Shards”** (`2DDA04088C8220D2`) and
**“Prosperity Seed Base”** (`1E0F92F07FDD162E`, `mysticalagriculture:prosperity_seed_base`)
are the line that leads there; **“Infusion Crystal”** (`217DB12EA32E1724`,
`mysticalagriculture:infusion_crystal`) leads to the tiers.

Cross-mod bridges only where the config states them (quote-by-quote detail is in
`references/farming-guide.md`): the optional **“Automating Awakened Supremium”** says
*"Awakened Supremium and other tiered essences can be farmed using the Productive Bees
mod."*; Productive Bees' craftable flowers are made *"with MA Essence"*; Apothic Spawners'
spawner line says *"Mob Essence is gotten through harvesting Mob Plants, made by Soul
Jars."*; and the Pylons chapter offers *"Harvester Pylons work as a very simple Auto-Farm."*
for a crop plot.

## Armor, tools, and what the essences feed

*(judgement, and deliberately thin)* This snapshot records **no verified armor, tool, or
weapon quests** for Mystical Agriculture — the chapter's 191 quests leave 138 untitled, and
none of the titles carried over here names a suit or a blade. So this page quotes no gear
quest, no stats, no slot counts, and no enchantment: the mod's gear tiers, their recipes and
their effects are **JEI and the in-game book's** business, and so is whether a given essence
is spent on gear rather than on the next tier. What the snapshot *does* say about the
essences' higher purpose is the Star: **“Creative Essence”** — *"Creative Essence is needed
to craft the ATM Star."* — plus the Insanium Coal Block and Awakened Supremium Ingot Block
lines above.

## Cross-references

- `references/farming-guide.md` — the source of everything verified on this page: the full
  tier table, all 125 seed quests by subtitle, the mob-seed detour, and the cross-mod
  bridges. Go there for the seed name lists.
- `references/atm-star-checklist.md` — Chapter 3's Mystical Agriculture and Mystical
  Agradditions components (`mysticalagriculture:master_infusion_crystal`,
  `mysticalagradditions:insanium_block` ×4, `mysticalagradditions:insanium_gemstone_block` ×4,
  `mysticalagriculture:awakened_supremium_ingot_block`,
  `mysticalagradditions:insanium_coal_block`, `mysticalagriculture:witherproof_bricks`,
  `mysticalagradditions:nether_star_crux`, `mysticalagradditions:creative_essence`) and the
  quoted "9,216 Inferium Essence" arithmetic.
- `references/boss-checklist.md` — the Wither and the Ender Dragon, the two sources the
  config gives for Cognizant Dust.
- `references/automation-first-steps.md` — where the farm sits in the beginner automation
  order, and the chapter's `Tier: 1` entry point.
- `references/progression-roadmap.md` and `references/progression.md` — the Resources group
  in quest-book order, for when to open this chapter at all.
- `references/key-mods.md` — the one-line "what Mystical Agriculture is for" entry.
- `references/chunk-loading-guide.md` — whether a farm keeps running while you are away: the
  config's chunk-loading picture, not a promise about your plot.

## What to do first (*judgement*):

1. Open the Resources group's Mystical Agriculture chapter and run its entry line in order:
   **“Mystical Agriculture!”** → **“Inferium”** → **“Inferium Farmland”**, with
   **“Prosperity Shards”** → **“Prosperity Seed Base”** → **“Infusion Altar”** beside it —
   then **“Infusion Crystal”** when you want Tier 2.
2. Plant Inferium early and leave it alone. It is the material every rung above it consumes,
   and it costs almost nothing to keep growing while you do something else.
3. Add automation only when hand-harvesting starts to annoy you: the chapter's own harvest
   line (*Scythes* → `mysticalagriculture:harvester`) plus **“Mystical Fertilizer”** if you
   want speed on demand. Which crop-harvesting block accepts which seed is in-game.
4. Climb one rung at a time, taking the seeds you actually want with you. Tier 2–5 are
   farmland-gated; Tier 6 and Magical need a crux or Magical Soil **under** the farmland
   first.
5. Treat the Awakened Supremium rung as a boss project, and Insanium → Creative Essence as
   the ATM Star's tail end; check `references/boss-checklist.md` and
   `references/atm-star-checklist.md` before committing resources to either.
6. For gear, recipes, growth rates, accelerator stacking, or which harvester takes which
   crop: the in-game quest book and JEI, not this page. There is no verified best layout,
   plot size, seed order, or speed-up figure in this snapshot, and this page invents none.
