# Ore processing in ATM10 — the ladder, rung by rung (pack 8.2)

**What this page is.** The ore-processing progression map for **All the Mods 10**: the
pack's own answer to a beginner's *"am I wasting ores by smelting them raw?"*, then the
ladder the quest book actually lays out — the early **Ore Hammer**, **Mekanism**'s four
numbered ore-processing tiers (Crusher / Enricher / Purifier / Injection / Dissolution),
and the other ore lines the book points at (Occultism's crusher demons, Industrial
Foregoing's 2x–5x chain, Oritech, Create, Immersive Engineering, RailCraft, Modern
Industrialization). It is a *map of what the book asks for*, not a crafting guide.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, task count, and quoted sentence below comes from
the official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at
`main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** and whose
`config/bcc-common.toml` stamps `modpackVersion = "8.2"` — the "8.x" that
`examples/progress.example.json` is stamped with.

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/mekanism.snbt` | the Mekanism chapter's 90 quests: the four tier quests' and machine quests' task items, counts, and dependency links |
| `config/ftbquests/quests/lang/en_us/chapters/mekanism.snbt` | the English titles, subtitles ("Tier 1 Ore Processing" … "Tier 4 Ore Processing"), and the description text quoted below |
| `config/ftbquests/quests/chapters/mainquestline_part_1.snbt` + its lang file | Chapter 1's `Basic Ore Doubling` quest and the `Ore Hammers` task |
| `config/ftbquests/quests/chapters/occultism.snbt` + lang | the crusher-demon quests (`Our First Ritual`, `Ophyx' Calling`, `Fatma's Incentivized Attraction`, `Iesnium: Ore of the Otherworld`) |
| `config/ftbquests/quests/chapters/industrial_foregoing.snbt` + lang | the three **untitled** "Ore Processing: Step 1/2/3" quests and their 2x/3x/4x/5x text |
| `config/ftbquests/quests/chapters/oritech.snbt`, `create.snbt`, `immersive_engineering.snbt`, `railcraft.snbt`, `mi_steam.snbt`, `artifacts.snbt`, `allthemodium.snbt` + lang | the other ore routes named below, each quoted from its own quest text |
| `config/ftbquests/quests/lang/en_us/chapter.snbt`, `chapter_group.snbt` | chapter titles and the quest-book groups quoted below |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (493 entries) |

Quoted sentences have the pack's `&`/`&#RRGGBB` formatting codes stripped (that is how
they read in the book); nothing else is changed, including the pack's own typos.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the task's required amount); where the config
  asks for one item, no count is printed.
- **No recipes.** The config lists *what a quest wants* and what a quest's own text says,
  never *how to craft it*. Every "how" here is a quote from that quest's description,
  marked as such, or a pointer to JEI.
- **Approximate means approximate.** Mod names are the modlist's, but which machine tier,
  fluid or layout a player needs is version-sensitive; anything not quoted from the config
  is flagged.
- **Titles are the config's.** A quest with no title in the lang file is marked *(no title
  in the config)* — the book then shows the task item's own name. Do not present a derived
  name as a verified title.
- **Nothing here was invented, and nothing is added from memory.** If a machine, tier, or
  number is not on this page, the answer is "open that quest in the book / look it up in
  JEI", never a plausible-sounding guess.

## The beginner answer: raw smelting is not "wrong", it is lossy

The pack answers this itself, in Chapter 1's **Basic Ore Doubling** quest (id
`4E5238F00CEED8B2`, which depends on *The Metal Age*). Its full description, quoted:

> "Smelting down raw ores in the beginning is necessary, but you are missing out on extra
> resources!"
>
> "There are several ways to double your output per raw ore, but one of the easiest ways
> is by creating and using an Ore Hammer."
>
> "These will break down 1 raw ore into 2 ore dust, which can be smelted into ingots,
> effectively doubling your ingot output!"
>
> "Want more per raw ore? Check out the mod Occultism!"

So the honest reading of the book — not a number this page invented:

- **Smelting raw ore is a normal start, not a mistake.** The book calls it "necessary in
  the beginning"; nothing is lost permanently, and every ore stays re-processable once the
  machines exist.
- **It is the worst yield the pack offers.** The same quest's "doubling your ingot output"
  is the book's own comparison, and Mekanism's *Enrichment Chamber* quest says the same
  step in machine terms: *"We can get 2 Dust from 1 Ore."*
- **But the config never states the raw-smelting baseline** (the vanilla 1 ingot per raw
  ore). That is vanilla behaviour, not a config quote — treat the baseline as
  *approximate* and check the recipe in JEI/machine in-game.
- **Watch out for automatic smelting.** The Artifacts chapter's *Pickaxe Heater* quest
  (id `62622137648A4F56`, subtitle *Hands*) warns in its own text: *"While wearing the
  Pickaxe Heater, Ores that you Mined will automatically be Smelted!"* … *"Might want to
  be careful with it if you want Ore Processing."* A smelter-on-a-tool spends the ore's
  processing potential.
- **One quest asks for the raw ore, another for the block.** Mekanism's text distinguishes
  `Raw Ore` from `Ore Blocks` and gives the block the better rate; how you obtain a block
  instead of raw ore is ordinary game behaviour and the config does not explain it —
  *approximate*, verify in-game.

**The pack's own bottom line:** you are not "wasting" ores by smelting raw — you are
leaving the extra output on the table until you build the ladder below. Nothing in the
config forces ore processing; the Welcome chapter's own text says *"In this modpack,
quests are optional. Mods are not gated behind completing any quests!"*

## The ladder at a glance

Rungs are ordered by when the book introduces them, not by a number the config prints.
Every title in the second column is a verified quest title (styling stripped); ids are in
the sections below.

| Rung | Verified quest title | Chapter (group) | What the config's own text claims for this rung |
|---|---|---|---|
| 0. Vanilla smelting | *(no quest — starting behaviour)* | — | The book's baseline: "Smelting down raw ores in the beginning is necessary". |
| 1. Hammer it first | **Basic Ore Doubling** | Chapter 1: The Beginning (Main Questline) | 1 raw ore → 2 ore dust → ingots: "effectively doubling your ingot output". |
| 2. Mekanism Tier 1 | **Enrich then Smelt** (subtitle *Tier 1 Ore Processing*) | Mekanism (Tech) | "just 2 Machines! Enrichers and Smelters!"; "3 Raw Ore to get 4 Dust"; ore blocks give twice the dust. |
| 3. Mekanism Tier 2 | **Making Oxygen for Purifier** → **Crush and Enrich our Clumps** (both *Tier 2 Ore Processing*) | Mekanism (Tech) | Oxygen-fed Purifiers: "3 Ore Clumps from Ore Blocks or 2 Ore Clumps from Raw Ore", then crush → enrich → smelt. |
| 4. Mekanism Tier 3 | **Making Chlorine** → **Injecting Hydrogen Chloride** → **Shard, to Clump, to Dust, to Ingot** (all *Tier 3 Ore Processing*) | Mekanism (Tech) | Hydrogen Chloride → Shards: "Ore Blocks will get 4 Ore Shards while 3 Raw Ores will get 8 Ore Shards", then the Tier 2 loop again. |
| 5. Mekanism Tier 4 | **Creating Sulfuric Acid** → **Melting Ores with Acid and Crystallizing them** → **Making more Hydrogen Chloride** → **Crystal, Shard, Clump, ETC** (all *Tier 4 Ore Processing*) | Mekanism (Tech) | Acid dissolution into slurry → crystals → injected back to Shards: "2 Ore Shards from each Ore Crystal", then the same crush/enrich/smelt loop. |
| Alt A. Demon crushers | **Our First Ritual** → **Ophyx' Calling** / **Fatma's Incentivized Attraction** | Occultism (Magic) | Foliot → Djinni → Afrit → Marid: the Marid "gives you 6 dusts per raw ore it crushes" (quest text). |
| Alt B. 2x–5x machines | *(no title in the config)* *Ore Processing: Step 1 / 2 / 3* | Industrial Foregoing (Tech) | "2x / 3x / 4x / 5x ore processing rate" modes, each with its own time and catalyst (quest text). |
| Alt C. Oritech | **Ore Processing** (subtitle *Maximum output*) + **Clumps** (subtitle *Fragment raw ores*) | Oritech (Tech) | "a Centrifuge with a Fluid Addon and a Pulveriser or Fragment Forge". |

The "Alt" rungs are not a better or worse path in the pack's eyes — it ships all of them
and gates none. Pick the one whose chapter you are already playing; the book's Welcome
text is explicit that questlines "are meant to serve as mod guides".

## Rung 1 — the Ore Hammer (Chapter 1: The Beginning)

- **Verified quest title:** **Basic Ore Doubling** (id `4E5238F00CEED8B2`). Depends on
  **The Metal Age** (id `051E0C85E7B71CE0`); the task is a smart filter over the item tag
  `alltheores:ore_hammers`, and the task's own name in the lang file is **Ore Hammers**.
- **Verified quest title:** **The Metal Age** points at the material early: *"Copper is
  abundant and has plenty of uses for things like Ore Hammers or Drawer Upgrades, so make
  sure to grab plenty of it!"*
- The quest deliberately does **not** name a single hammer item: it accepts anything in
  the `alltheores:ore_hammers` tag. Which hammers that tag covers is the book's/JEI's
  answer, not this page's.

## Rungs 2–5 — the Mekanism ladder, tier by tier

All four tiers live in the **Mekanism** chapter (chapter id `23983F4DC524B14B`, group
`Tech`, `order_index` 5); the skill tracks it as the chapter file `mekanism.snbt`. The
tier quests hang off the chapter's machine-line quests — **Machines**
(`21D8B88155648EA6`, task `mekanism:steel_casing`), **Better Machines**
(`6263A27182B2CE3D`, task `mekanism:advanced_control_circuit`), **Even better Machines!**
(`71CF9E59F8F0B4A6`, task `mekanism:elite_control_circuit`), **Some of the best
Machines!** (`1ABD22AA58E093A6`, task `mekanism:ultimate_control_circuit`) — and the tier
tasks are smart filters: where the
config writes `or(item(mekanism:enrichment_chamber)item(mekanism:basic_enriching_factory)
…)`, **the book accepts any of those machines**, standalone or factory tier. Task labels
quoted in the tables are the filters' own custom names, typos included.

### Tier 1 — Enrich then Smelt

| Verified quest title (id) | Subtitle | Task items in the config |
|---|---|---|
| **Enrich then Smelt** (`119BED334E331C25`) | Tier 1 Ore Processing | a smart filter over `mekanism:enrichment_chamber` and its `basic_enriching_factory` / `advanced_enriching_factory` / `elite_enriching_factory` / `ultimate_enriching_factory` tiers, **and** the same shape for `mekanism:energized_smelter` and its `basic_smelting_factory` / `advanced_smelting_factory` / `elite_smelting_factory` / `ultimate_smelting_factory` tiers |

Quoted from the quest: *"The very first and simplest Ore Processing is just 2 Machines!
Enrichers and Smelters!"* … *"We can use Ore Blocks to get twice the Dust or Raw Ore to
get 1/3 more. So 3 Raw Ore to get 4 Dust."* … *"Throw the Ore into the Enricher and you'll
get Dust! Then, Smelt that Dust to get Ingots!"* … *"Congrats, you just Ore Processed!"*

The two machines have their own quests (verified titles **Enrichment Chamber**, id
`08DDE018A804BFE7`, subtitle *Breaks Raw Ores into Dusts*, and **Energized Smelter**, id
`488DBE69595F38F8`, subtitle *Mekanism's Powered Furnace*). The Enrichment Chamber's text
gives the rate plainly: *"We can get 2 Dust from 1 Ore."*

The **Crusher** quest (id `7AE502EDB73BD57A`, subtitle *It Crushes Things.*) hangs off
the same machine hub and is where the clump/dust steps below get their machine: *"We can
get Dust from Ingots, Cobble from Stone, and Bio Fuel from Plants!"*

### Tier 2 — Oxygen and the Purifier

| Verified quest title (id) | Subtitle | Task items in the config |
|---|---|---|
| **Making Oxygen for Purifier** (`445CC9AAA6F8AAB6`) | Tier 2 Ore Processing | `mekanism:electric_pump`, `mekanism:electrolytic_separator`, and a smart filter over `mekanism:purification_chamber` and its `basic_purifying_factory` / `advanced_purifying_factory` / `elite_purifying_factory` / `ultimate_purifying_factory` tiers |
| **Crush and Enrich our Clumps** (`67E7A9A65B14C933`) | Tier 2 Ore Processing | smart filters labelled **Crushers** (`mekanism:crusher` and its `basic_crushing_factory` / `advanced_crushing_factory` / `elite_crushing_factory` / `ultimate_crushing_factory` tiers), **Enrichers** (as in Tier 1), **Smelters** (as in Tier 1) |

Quoted: *"For the next Tier of Ore Processing we'll need Purifiers and they'll need
Oxygen."* … *"Now that the Purifier has Oxygen, we can place our Ores into it to get 3 Ore
Clumps from Ore Blocks or 2 Ore Clumps from Raw Ore."* Then the loop: *"To start, Crush
each Clump to get 2 Dirty Ore Dust."* … *"We can't Smelt Dirty Dust, it'll ruin the
Furnace! So we'll need to Enrich them to get our regular Dust."* … *"And like usual,
Smelt the Dust to get Ingots."*

The **Purification Chamber** quest (id `33415CB421F7620A`) describes the machine as
*"technically an Upgrade to the Enrichment Chamber"* that *"combines Ores with Oxygen to
get more Ingots out of them!"*

### Tier 3 — Chlorine, Hydrogen Chloride, Shards

| Verified quest title (id) | Subtitle | Task items in the config |
|---|---|---|
| **Making Chlorine** (`7485BCBE366501DF`) | Tier 3 Ore Processing | `mekanism:electric_pump`, `mekanism:thermal_evaporation_block` ×33, `mekanism:thermal_evaporation_controller`, `mekanism:thermal_evaporation_valve` ×2, `mekanism:electrolytic_separator` |
| **Injecting Hydrogen Chloride** (`0E175356D43E6A10`) | Tier 3 Ore Processing | `mekanism:electric_pump`, `mekanism:electrolytic_separator`, `mekanism:chemical_infuser`, `mekanism:chemical_injection_chamber` |
| **Shard, to Clump, to Dust, to Ingot** (`0095422BC87AA135`) | Tier 3 Ore Processing | smart filters labelled **Purifiers**, **Crushers**, **Enrichers**, **Smelters** |

Quoted: *"If we want even more Ores! We'll need a better way of Processing our Ores.
Hydrogen won't work, let's try Hydrogen Chloride."* The Thermal Evaporation Plant makes
*"Brine"*; the Separator splits it into *"Sodium"* and *"Chlorine"*, and *"Sodium is
helpful for Fission Reactor... but not Ore Processing!"* Then: *"Pipe that Hydrogen
Chloride into a Chemical Injection Chamber to Inject Ores to get Shards."* … *"Ore Blocks
will get 4 Ore Shards while 3 Raw Ores will get 8 Ore Shards."* Finally the third quest
repeats the previous tier's loop: *"Throw those Ore Shards into a Purifier with Oxygen
(most likely from our previous Electrolytic Separator) to make Ore Clumps."* … *"Now we
just repeat steps from previous Tier."*

### Tier 4 — Sulfuric Acid and Crystals

| Verified quest title (id) | Subtitle | Task items in the config |
|---|---|---|
| **Creating Sulfuric Acid** (`75E4751F7A802A44`) | Tier 4 Ore Processing | `alltheores:sulfur`, `mekanism:chemical_oxidizer`, `mekanism:electric_pump`, `mekanism:electrolytic_separator`, `mekanism:chemical_infuser`, `mekanism:rotary_condensentrator` |
| **Melting Ores with Acid and Crystallizing them** (`77FB313845779AED`) | Tier 4 Ore Processing | `mekanism:chemical_infuser`, `mekanism:chemical_dissolution_chamber`, `mekanism:chemical_washer`, `mekanism:chemical_crystallizer` |
| **Making more Hydrogen Chloride** (`6DC1E08D019FD543`) | Tier 4 Ore Processing | `mekanism:electric_pump` ×2, `mekanism:thermal_evaporation_block` ×33, `mekanism:thermal_evaporation_controller`, `mekanism:thermal_evaporation_valve` ×2, `mekanism:electrolytic_separator` ×2, `mekanism:chemical_infuser`, `mekanism:chemical_injection_chamber` |
| **Crystal, Shard, Clump, ETC** (`7934873E784C4B3C`) | Tier 4 Ore Processing | `mekanism:electric_pump`, `mekanism:electrolytic_separator`, smart filters labelled **Purificaters** *(the config's spelling)*, **Crushers**, **Enrichers**, **Smelters** |

Quoted from the chain: *"First, and most important, for Sulfuric Acid, is Sulfur! Mine
some then Oxidize it to get Sulfur Dioxide."* … *"Pipe the Sulfuric Acid into a C.D.C. to
Melt down our Ores with Acid. This will give us Dirty Ore Slurry, a Chemical form of
Ores."* … *"3 Raw Ore will give 2 Buckets of Ore Slurry and 1 Ore Block will give 1 Bucket
of Ore Slurry."* … *"Every 5mb of Dirty Slurry will be turned into 3mb of Ore Slurry."* …
*"Each 200mb of Ore Slurry is equal to 1 Crystal."* Then the crystals go back through
injection: *"With our Chemical Injector, we can Inject the Crystals with Hydrogen Chloride
to get 2 Ore Shards from each Ore Crystal."* — and the last quest runs the shard → clump →
dust → ingot loop again.

The three Tier 4 machines have their own quests with their own one-liners: **Chemical
Dissolution Chamber** (id `6B8040401B512E50`) — *"another Machine only used for Ore
Processing"*; **Chemical Washer** (id `60B52705049D1BA5`) — *"The Chemical Washer is only
for Ore Processing."* and *"the Chemical Washer will make the Dirty Slurry, Clean!"*; and
**Chemical Crystallizer** (id `602A6CF9D5B66AD3`) — *"Just throw some Clean Ore Slurry
into the Crystallizer and it will turn it into Ore Crystals."* The **Chemical Injection
Chamber** (id `27512B0434531195`) adds: *"And most important, using Hydrogen Chloride into
Ore Blocks to get Ore Shards for Processing!"*

Supporting quests the tier tasks lean on (verified titles, no subtitles): **Chemical
Infuser** (`376532CD98D39781`), **Rotary Condensentrator** (`603BEDD49070ECAD`),
**Electrolytic Separator** (`18783C62009934DB`), **Thermal Evaporation Plant**
(`120572510F525930`, tasks `mekanism:thermal_evaporation_block` ×33,
`mekanism:thermal_evaporation_controller`, `mekanism:thermal_evaporation_valve`),
**Chemical Oxidizer** (`2A793B35FE25003C`), and the two tag quests that show the machine
outputs in general terms: **Enriched Items** (`0F326EEEC2EBE4E5`, subtitle *Enrich your
items first!*, filter `ftbfiltersystem:item_tag(mekanism:enriched)`) and **Crushed to
Dust!** (`47F38E606AD3FF53`, filter `or(item_tag(c:dusts))`).

## "Doubling"/"tripling"/"quadrupling" — which words are the pack's?

Players (and mod guides) number these tiers as 2x/3x/4x/5x. In the config at this commit:

- **The pack's own words:** the quest title **Basic Ore Doubling**; the quest text
  *"effectively doubling your ingot output"*; Industrial Foregoing's *"2x ore processing
  rate"*, *"3x ore processing rate"*, *"4x ore processing rate"*, *"5x ore processing
  rate"*; and Mekanism's subtitles **Tier 1 Ore Processing** … **Tier 4 Ore Processing**.
- **Not the pack's words:** the en_us quest text never says "tripling", and its only
  "quadrupling" is a Productive Bees line about comb blocks — not ore processing. There is
  no "Tier 5" anywhere in the ore text; Mekanism's ladder stops at Tier 4.
- **Therefore:** the mapping *Tier 1 = doubling, Tier 2 = tripling, Tier 3 = quadrupling,
  Tier 4 = quintupling/5x* is **community shorthand, approximate** — the tier *order* and
  the per-step numbers above are the config's; the multiplier *names* are not. Do not
  quote them as the book's. If a player asks "which tier is the 5x one?", the answer is
  "the one the book calls Tier 4 — check the quest entry and JEI".

## Other ore routes the book itself offers

Each row is grounded in that chapter's own quest text, quoted; none of them is required
for any other (the Welcome chapter: *"quests are optional"*).

| Route | Verified quest title (id) | The config's own words |
|---|---|---|
| Occultism — Foliot Crusher | **Our First Ritual** (`4F35D04721DFC9FF`, subtitle *Aviar's Circle*) | *"These rituals are used to summon different types of useful Demons to assist you in crushing, smelting, and more as you get to higher tiers of rituals."* … *"For our first ritual, we want to summon a Foliot Crusher Demon. This Demon will crush items for us, which is something we'll need to make some of the higher level Chalks!"* |
| Occultism — Djinni Crusher | **Ophyx' Calling** (`5FE507DAEE770507`, subtitle *An alternate path for light blue*) | *"Djinnis are able to crush ores more efficiently than Foliots, but not as efficiently as Afrits or Marids."* |
| Occultism — Marid Crusher | **Fatma's Incentivized Attraction** (`2AD68066C1948C90`, subtitle *Maximum Summon*) | *"what if I told you that you could summon a demon that gives you 6 dusts per raw ore it crushes?"* … *"The Marid Crusher does exactly that."* |
| Occultism — for ores the standard chain cannot double | **Iesnium: Ore of the Otherworld** (`33106E24A3B5DDD8`) | *"Since you can't break this ore down into double the dusts using the standard methods, try using your Foliot Crusher to double your ingots per raw ore!"* |
| Industrial Foregoing — Step 1 | *(no title in the config)*, subtitle **Ore Processing: Step 1** (`0B35172E47705205`) | *"Yes, Industrial Foregoing has ore processing too. This one uses Liquid Meat to convert an ore into Raw Ore Meat."* Task: `industrialforegoing:washing_factory`. |
| Industrial Foregoing — Step 2 | *(no title in the config)*, subtitle **Ore Processing: Step 2** (`1684D52FDAAC894B`) | *"This machine has 4 modes. 1. 2x ore processing rate, 5 seconds to process. 2. 3x ore processing rate, 45 seconds to process. 3. 4x ore processing rate, 120 seconds to process. Uses Pink Slime as a catalyst. 4. 5x ore processing rate, 300 seconds to process. Uses Ether Gas as a catalyst."* Task: `industrialforegoing:fermentation_station`. |
| Industrial Foregoing — Step 3 | *(no title in the config)*, subtitle **Ore Processing: Step 3** (`34AA079FFAFC64BD`) | *"The final step of the ore processing lineup of Industrial Foregoing, the Fluid Sieving Machine. This will use sand to filter out the useful part of Fermented Ore Meat, giving us some dust."* Task: `industrialforegoing:fluid_sieving_machine`. |
| Oritech | **Ore Processing** (`3DD27DED791C6A0B`, subtitle *Maximum output*) and **Clumps** (`4EAD06B0B3AD7D6E`, subtitle *Fragment raw ores*) | *"To process ores using Oritech, you need to use a Centrifuge with a Fluid Addon and a Pulveriser or Fragment Forge."* Related untitled quests: *(no title in the config)*, subtitle *"A better pulverizer"* (`175509632CBF8631`, task `oritech:fragment_forge_block`) — *"Improves yield on all pulverisation recipes."* — and *(no title in the config)*, subtitle *"Allows additions of fluids to centrifuge"* (`310FA9380CB3E0BB`, task `oritech:machine_fluid_addon`). |
| Create | **Crushing Wheels** (`3F02EF19112D23BE`) | *"What Items? Crushed Ores from Ores, Items from Stones and Netherrack…"* The quest also notes you need **2** wheels and that they must spin in opposite directions. Task: `create:crushing_wheel`. |
| Immersive Engineering | **Crusher** (`32384DE59539557D`) | *"This can be very helpful especially with taking Raw Ores into Dust. If we use Raw Ore Blocks it will give us more Dust than what the Hammer will give, also some have a chance at giving an entirely new type of Dust!"* |
| RailCraft | **Crusher** (`21693C4DE6531D73`) | *"It can crush blocks to get the crafting materials, like bricks from a brick staircase, or dusts from ingots."* Task: `railcraft:crusher` (multiblock, per its text). |
| Modern Industrialization | **Forge Hammer** (`0DAF5D42694EA8C9`, in *Steam Age: New Beginnings*) | *"Forge Hammer is the beginning of your journey. It has a lot of uses like getting a better output out of your ores to making components for future crafts."* A follow-up untitled quest (`1036837C9AD3F301`, task `alltheores:copper_dust`) adds: *"The Forge Hammer will allow you to easily crush Copper Ingots or Ore forms into its Dusts."* |
| Modern Industrialization — macerator | *(no title in the config)* (`164EA8EE10CA1583`, task `modern_industrialization:bronze_macerator`) | The config gives this quest no title and no description — the book shows the item; ask the quest entry/JEI what the machine does. |

Two more ore-related quotes worth keeping in the same voice:

- **Allthemodium** chapter, **Vibranium Ingot** (`144BB025516E0994`): *"It is also
  recommend to Ore Process it to get more."* (their spelling) — the endgame ores are
  explicitly called out for processing too.
- **Artifacts** chapter, **Pickaxe Heater** (`62622137648A4F56`) — the anti-processing
  warning quoted in the beginner answer above.

## Where this sits in the quest book

| Chapter (config id) | Book title | Group | `order_index` | Quests |
|---|---|---|---|---|
| `mainquestline_part_1` | Chapter 1: The Beginning | Main Questline | 0 | 36 |
| `mekanism` | Mekanism | Tech | 5 | 90 |
| `industrial_foregoing` | Industrial Foregoing | Tech | 3 | 78 |
| `oritech` | Oritech | Tech | 7 | 56 |
| `create` | Create | Tech | 0 | 89 |
| `immersive_engineering` | Immersive Engineering | Tech | 2 | 127 |
| `railcraft` | RailCraft | Tech | 10 | 52 |
| `occultism` | Occultism | Magic | 7 | 64 |
| `mi_steam` | Steam Age: New Beginnings | Modern Industrialization | 0 | 30 |

Counts are the config's quest totals for those chapters at this commit; the skill's
`examples/progress.example.json` tracks the same chapters. The Main Questline comes
before the mod chapters in the book's own order, so a beginner following the spine meets
**Basic Ore Doubling** long before any Mekanism tier.

## What this page deliberately does not tell you

- **Recipes.** Not one. Every item above is a quest *task* or a name quoted from quest
  text; JEI has the recipe, and recipes are where pack versions differ most.
- **A per-ore total for each tier.** The config gives per-step and per-input numbers (the
  quotes above); it never prints "Tier N = Nx per raw ore". Multiply nothing on the
  player's behalf — send him to the quest entry, the machine's in-game GUI, and JEI.
- **Machine tiers, fluids, speeds, energy, and layouts beyond the quoted sentences.** The
  quests' own descriptions cover them in-game; anything here that is not a quote is
  *approximate*.
- **The community multiplier names.** "Doubling", "tripling", "quadrupling", "5x" are
  mapped to the book's tiers only as community shorthand (see above) — the book's own
  labels are *Tier 1*–*Tier 4 Ore Processing* and the three *Ore Processing: Step 1/2/3*
  subtitles it prints.
- **Anything not in the config.** If a player names an ore machine, tier, or number that
  is not on this page, the answer is "open that quest in the book / look it up in JEI" —
  never a guess.

## Cross-references

- `references/progression.md` — the four-stage map; Chapter 1 lists *Basic Ore Doubling*
  among its quests, and Mekanism sits in the Tech stage.
- `references/key-mods.md` — what Mekanism, Occultism, Industrial Foregoing, Oritech and
  the rest do and when to start them.
- `references/getting-started.md` — the first-hours route that reaches the Ore Hammer.
- `references/creative-checklist.md` — where a Mekanism **Crusher** shows up again in the
  endgame: Chapter 4's *But why?* quest (task `mekanism:crusher`) notes the Crusher can
  turn an ATM Star into Star Shards — *"Technically you can also use the Crusher to make
  the ATM Star into 5 Star Shards... But you'll need 262 to make a new Star... So why
  would you?"*
- `references/atm-star-checklist.md` — the star components, several of which are
  Mekanism-machine products that a working ore line feeds.
