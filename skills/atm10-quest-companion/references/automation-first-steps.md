# ATM10: what to automate first — the five highest-impact automations for a beginner

**What this page is.** The answer to the first real automation question every ATM10
beginner asks — *"what should I automate first?"* — as **five things to automate, ordered
by impact**, from the ore you are already mining to the auto-crafting network that ties
everything together. Every quest title, subtitle, task item, and quoted sentence below was
read from the pack's own quest config; the **ordering and the impact reasoning are this
skill's judgement**, marked as such wherever they appear. It is a *priority map*, not a
build guide: how to construct any of these machines is the quest entry's and JEI's job.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, count, and quoted sentence below comes from the
official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at
`main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with. The same commit the three endgame docs
pin (`references/creative-checklist.md` and friends).

Quest titles, subtitles, task items, dependencies, and the quoted description text were
read from `config/ftbquests/quests/chapters/<chapter>.snbt` and
`config/ftbquests/quests/lang/en_us/chapters/<chapter>.snbt` for these chapters (chapter
titles, groups, and quest counts from the same files; the skill's chapter ids are the
config filenames):

| Chapter (book title, group) | Config file | Quests | What it supplied here |
|---|---|---|---|
| Chapter 1: The Beginning (Main Questline) | `mainquestline_part_1` | 36 | *Basic Ore Doubling*, *Furnace Upgrades!*, *Furnace Augments*, the Chapter 1 power quests |
| Mekanism (Tech) | `mekanism` | 90 | the *Tier 1–4 Ore Processing* quest line, the machines, the transporters |
| Create (Tech) | `create` | 89 | *Crushing Wheels*, *Millstone*, *Encased Fan*, *Item Logistics*, *Mechanical Harvester*, *Mechanical Crafter* |
| Oritech (Tech) | `oritech` | — | its own *Ore Processing* line |
| Steam Age: New Beginnings (Modern Industrialization) | `mi_steam` | 30 | *Forge Hammer*, the steam quarry quest |
| Basic Power (Power) | `basic_power` | 34 | *Early Game Power Options*, *Transferring Power*, *Storing Power*, the two *Automated Flux Dust* quests |
| Generators N Furnaces (Power) | `generators` | 47 | the Iron Furnaces chain and the *Augment:* quests |
| Basic Logistics (Logistics) | `basic_logistics` | 40 | *Pipez* and friends, *Item Pipez*, the *Logistics* intro |
| Pylons (Logistics) | `pylons` | 13 | the Harvester Pylon quest (untitled in the config) |
| Mystical Agriculture (Resources) | `elmystical_agriculturerr` | 191 | *Inferium*, *Inferium Farmland*, *Infusion Altar*, the tier ladder and seed quests |
| Productive Bees (Resources) | `productive_bees` | 252 | *Advanced Beehive*, the Centrifuge quest (untitled in the config) |
| Industrial Foregoing (Tech) | `industrial_foregoing` | 78 | *Plants*, *Item & Fluid Transport*-style conveyor and machine quests |
| Applied Energistics 2 (Storage) | `applied_energistics_2` | — | *Auto-Crafting*, *Patterns*, the Annihilation Plane quest (untitled in the config) |
| Refined Storage (Storage) | `refined_storage` | — | *Autocrafting*, *Autocrafter*, *Pattern Grid* |
| Hostile Neural Networks (Resources) | `hostile_neural_networks` | 50 | named as a *later* automation, not a first one |
| Occultism (Magic) | `occultism` | — | *Demon Mining*, where Chapter 1 points for "more per raw ore" |
| Chapter 2: Allthemodium (Main Questline) | `allthemodium` | — | the endgame *Mining Dimension* quarry advice, quoted as context |

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **The five-item ordering is judgement, not pack data.** The book does not rank
  automations, quests are optional, and nothing is gated. The order here reflects what the
  Chapter 1 / Tech / Power chapters teach first and what each automation pays for; flag it
  as judgement whenever repeating it.
- **Titles are the config's.** Quests the config gives no title are marked *(no title in
  the config)* and identified by their task item — never present a derived name as a
  verified title.
- **Item ids and counts are quoted from the config, never invented.** A count is shown
  only where the config states one (a task's required amount). Where the config accepts
  any of several items (filter tasks), this page says so instead of picking one.
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Every
  "how" below is a quote from that quest's own description, marked as such, or a pointer
  to JEI.
- **Numbers stay attributed.** Yields like "2 Dust from 1 Ore" or "3 Raw Ore to get 4
  Dust" are the quest author's own figures, quoted from quest text — verify in the quest
  entry and JEI before relying on them.
- **Anything not quoted from the config is flagged approximate.** Which mod's machines a
  player ends up using, how much power a line needs, and when to move on are
  version-sensitive and player-dependent.

## The short answer

Automate **the ore you are already mining** first — the book itself says so in Chapter 1's
**Basic Ore Doubling**: *"Smelting down raw ores in the beginning is necessary, but you
are missing out on extra resources!"* Then automate **power**, **item movement**,
**farms**, and finally **auto-crafting**. The five, in this skill's judgement order:

| # | Automate this | Anchor quests (verified titles) | Where they live |
|---|---|---|---|
| 1 | Ore doubling → first ore-processing line | **Basic Ore Doubling**; **Enrich then Smelt** *(Tier 1 Ore Processing)* | Chapter 1: The Beginning; Mekanism |
| 2 | Power: generate, transfer, store | **Wind Power**, **Solar Power**, **Lava Power**, **Generators Galore**; **Early Game Power Options**, **Transferring Power**, **Storing Power** | Chapter 1: The Beginning; Basic Power |
| 3 | Item movement: pipes, belts, transporters | **Pipez**, **Item Pipez**; **Logistical Transporters**; **Item Logistics** | Basic Logistics; Mekanism; Create |
| 4 | Farms: auto-harvest crops, then grow resources | the Harvester Pylon quest *(no title in the config)*; **Inferium Farmland** | Pylons; Mystical Agriculture |
| 5 | Auto-crafting from a storage network | **Auto-Crafting**, **Patterns** (AE2) — or **Autocrafting**, **Autocrafter** (RS) | Applied Energistics 2; Refined Storage |

Why this order (judgement): #1 doubles every metal you mine from day one and is the only
one Chapter 1 itself assigns; #2 is what turns machines from things you click into things
that run; #3 removes the walking-and-shoveling between them; #4 makes resources arrive
without mining; #5 multiplies all of the above but assumes you already have a network
worth automating. Each section below names the verified quests to follow and quotes what
their own text says.

## 1. Ore doubling — then your first ore-processing line

**Why first (judgement):** every tool, machine, and cable in the pack is made of metal,
and doubling your ore output doubles all of it. It is also the earliest automation the
book asks for: **Basic Ore Doubling** sits in Chapter 1: The Beginning, right after
**The Metal Age** (verified dependency in the config).

### What Chapter 1 says (quoted)

**Basic Ore Doubling** (task: one item with the tag `alltheores:ore_hammers` — the config
accepts any ore hammer in that tag; reward: `alltheores:iron_dust` and
`alltheores:copper_dust`):

> *"There are several ways to double your output per raw ore, but one of the easiest ways
> is by creating and using an Ore Hammer."*
>
> *"These will break down 1 raw ore into 2 ore dust, which can be smelted into ingots,
> effectively doubling your ingot output!"*
>
> *"Want more per raw ore? Check out the mod Occultism!"*

The hammer's own recipe is JEI's business — this page only quotes what the quest says.
The Occultism pointer is real: its chapter (Magic group) later carries **Demon Mining**,
whose text describes a *"Dimensional Mineshaft"* with a *"Mining Demon confined to a
lamp"* — an end-of-magic-stage automation, not a first one (judgement).

### The machine upgrade: Mekanism's Tier 1 line

The Mekanism chapter — its intro quest is literally titled **Mekanism**, subtitle *"The
Start of Your Own Factory"* — builds ore processing as four labelled tiers. The config's
quest subtitles stamp them **Tier 1 Ore Processing** (1 quest), **Tier 2 Ore Processing**
(2 quests), **Tier 3 Ore Processing** (3 quests), and **Tier 4 Ore Processing** (4
quests); there is no "Tier 5 Ore Processing" subtitle anywhere in the chapter. A beginner
wants Tier 1, and can stop there happily (judgement):

- **Enrich then Smelt** *(Tier 1 Ore Processing)* — task: any enriching machine **and**
  any smelting machine (the config's filters accept `mekanism:enrichment_chamber` or any
  `*_enriching_factory` tier, and `mekanism:energized_smelter` or any
  `*_smelting_factory` tier). Quoted:
  > *"The very first and simplest Ore Processing is just 2 Machines! Enrichers and
  > Smelters!"*
  >
  > *"We can use Ore Blocks to get twice the Dust or Raw Ore to get 1/3 more. So 3 Raw
  > Ore to get 4 Dust."*
  >
  > *"Throw the Ore into the Enricher and you'll get Dust! Then, Smelt that Dust to get
  > Ingots!"* — and then, *"Congrats, you just Ore Processed!"*
- The two machines have their own quests: **Enrichment Chamber** *(subtitle "Breaks Raw
  Ores into Dusts")* — *"We can get 2 Dust from 1 Ore."* — and **Energized Smelter**
  *(subtitle "Mekanism's Powered Furnace")* — *"It uses Energy to Smelt Items!"*, with
  the quest's own nudge: *"no more using Coal to power our Furnaces, we need Coal for
  Steel!"*

**Later tiers exist — do not start with them (judgement).** Tier 2 (**Making Oxygen for
Purifier**, **Crush and Enrich our Clumps**) already adds an Electrolytic Separator and,
per the quest text, yields *"3 Ore Clumps from Ore Blocks or 2 Ore Clumps from Raw Ore"*;
Tier 3 (**Making Chlorine**, **Injecting Hydrogen Chloride**, **Shard, to Clump, to Dust,
to Ingot**) wants a Thermal Evaporation Plant — the **Making Chlorine** task list alone
asks for `mekanism:thermal_evaporation_block` ×33 plus controller and valves — and yields
*"4 Ore Shards"* per ore block, *"8 Ore Shards"* per 3 raw ores; Tier 4 (**Creating
Sulfuric Acid**, **Melting Ores with Acid and Crystallizing them**, **Making more
Hydrogen Chloride**, **Crystal, Shard, Clump, ETC**) adds the dissolution/washer/
crystallizer chemistry. Climb those when Tier 1's throughput stops keeping up — the quest
texts above are the book's own ladder.

### The other verified routes (alternatives, not a required path)

Kitchen-sink rule: pick the mod you enjoy; none of these is gated (judgement):

- **Create** — **Crushing Wheels** (task: `create:crushing_wheel` ×2): *"Once they are
  spinning (fast and in the right directions) you can have Items Dropped in between them
  and they will be Crushed."* — *"Crushed Ores from Ores"* per the same text. The cheaper
  **Millstone** and the **Encased Fan** (subtitle *"This blows!"* — *"We can use Lava to
  Blast Items like a Furnace. Getting Ingots from Ores..."*) cover early grinding and
  smelting.
- **Modern Industrialization** — **Forge Hammer** (task `modern_industrialization:forge_hammer`):
  *"Forge Hammer is the beginning of your journey. It has a lot of uses like getting a
  better output out of your ores..."*
- **Oritech** — its own line: **Oritech Beginnings** *(subtitle "Find nickel ore to find
  begin your journey" — spelled that way in the config)*, **Refining Ores** *(subtitle
  "Turning one into more")*, **Clumps** *(subtitle "Fragment raw ores")*, and **Ore
  Processing** *(subtitle "Maximum output")*, whose task accepts any of the Oritech gems
  (the filter lists `oritech:iron_gem`, `oritech:platinum_gem`, `oritech:gold_gem`,
  `oritech:copper_gem`, `oritech:nickel_gem`, `oritech:uranium_gem`).

### The cheapest smelting automation, while you are here

The ore line's back half is a furnace, and Chapter 1 automates that too: **Furnace
Upgrades!** (task: any of `ironfurnaces:iron_furnace`, `ironfurnaces:copper_furnace`,
`ironfurnaces:upgrade_iron`, `ironfurnaces:upgrade_copper`) says Iron Furnaces *"make
automation easier by allowing you to auto-pull or push from the sides using the config on
the left of the interface."* Its follow-up **Furnace Augments** lists the Factory augment:
*"Converts the Furnace to use power instead of fuel, and upgrades it to a factory,
allowing it to smelt multiple items at once."* The Generators N Furnaces chapter carries
the same items as **Augment: Factory** (`ironfurnaces:augment_factory`).

## 2. Power you can walk away from: generate, transfer, store

**Why second (judgement):** a machine you have to stand next to and refuel is not
automation. Chapter 1 itself sequences this right after metals — **Lava Power**, **Wind
Power** (task `mekanismgenerators:wind_generator`), **Solar Power**, and **Generators
Galore** (*"this mod adds a ton of fun ways to generate power that require specific
builds"*) — and the Basic Power chapter is built as three hubs.

Verified quests, in the chapter's own hub structure:

- **Early Game Power Options** *(subtitle "Starter Power")* — *"These don't produce a ton
  of power, but they are typically easy or cheap to get in the early game!"* Its siblings
  **Mid Game Power Options** (task: `minecraft:diamond`) and **End Game Power Options**
  *(subtitle "More Power Than You'll Need")* show the intended ramp — start at the early
  hub and don't overbuild (judgement).
- **Transferring Power** — cables and pipes: **Pipez: Energy Pipes** (`pipez:energy_pipe`,
  `pipez:wrench`), **Mekanism: Universal Cables** *(subtitle "Mekanism's Energy Transfer
  Pipe")*, and **Mekanism: Quantum Entangloporter** *(subtitle "Doesn't just work for
  Power")* for later.
- **Storing Power** — buffer so machines don't brown out (judgement): **Mekanism: Energy
  Cubes**, **RFTools Power: Powercells**, **Integrated Dynamics: Energy Battery**
  *(subtitle "Batteries Included")*.

The Generators N Furnaces chapter is the fuel-burner ladder if you want it: **The
Furnace** *(subtitle "It all starts here")* through **Copper Generator**
(`generatorgalore:copper_generator`), **Iron Generator**, **Gold Generator**, **Diamond
Generator**. Which generator is "best" at any moment is version-sensitive — the quest
entries and JEI decide, not this page (approximate).

## 3. Moving items: pipes, belts, transporters

**Why third (judgement):** with doubling and power running, the remaining chore is
carrying stacks between machines by hand. The Basic Logistics chapter's own intro quest,
**Logistics**, puts it plainly: *"you'll need to move items from factories, machines,
farms, and especially chests. That's what Logistics is for."*

Pick one system and learn it (alternatives, not a required path):

- **Pipez** — the chapter calls it *"the simplest Logistics Mod"*: *"Attach the specific
  Pipe to where you want to move items and use the Pipe Wrench to configure what side
  Pulls, Pushes, or doesn't connect."* **Item Pipez** (`pipez:item_pipe`): *"It will move
  Items from one Inventory to another. Could be from one Chest to another, could be a Farm
  to a System, or even a Quarry to a Smelter."* The quest text even flags the trade-off:
  *"(Can be laggy when used in mass, still not as laggy as Mekanism pipes though)."*
- **Mekanism** — **Logistical Transporters** *(subtitle "Items")*: *"Logistical
  Transporters will move Items and Blocks from one Inventory to another!"*, with the
  side-config caveat quoted in the quest (*machines need their Side Configs set to
  Auto-Eject*). **Mekanism Logistics** *(subtitle "The Configurator")* teaches the wrench:
  *"If you use it on Pipes it will change if they Push, Pull, or Both."*
- **Create** — **Item Logistics** (`create:belt_connector`): *"Item Logistics is important
  to Create. Millstones need Items, Deployers need Items, Mechanical Mixers need Items,
  and so on. Now how does Create want us to move Items? With Belts!"* Plus **Andesite
  Funnel** — *"Funnels are like if a Hopper and Dispenser had a baby."*
- **Industrial Foregoing** — **Item & Fluid Transport** and **Conveyor Insertion &
  Extraction** (the config escapes both ampersands: `"Item \& Fluid Transport"`), tasks
  `industrialforegoing:item_transporter_type` and `industrialforegoing:fluid_transporter_type`,
  if that's your chosen tech line.

## 4. Farms: auto-harvest crops now, grow resources soon

**Why fourth (judgement):** food stops being an errand, and Mystical Agriculture turns
farming into *resource* generation — the MA chapter's own intro (**Mystical Agriculture!**)
calls it *"a resource generation mod that allows you to grow a large variety of vanilla
and modded resources using Seeds."* `references/getting-started.md` already flags starting
MA early-ish; this is the quest-grounded version.

### The one-block auto-farm

The Pylons chapter's harvester quest is *(no title in the config)*; its task is
`pylons:harvester_pylon`, and its text is the whole pitch:

> *"Harvester Pylons work as a very simple Auto-Farm. Put the Pylon on or in the Water
> Source and it will automatically harvest and replant Crops that are fully grown in the
> set area around it."*
>
> *"It will need a Hoe to use on the Plants and will need an Inventory like a chest above
> it to put the Crops."* — and the quest's own warning: *"(Careful when using a lot of
> modifiers with it like Lilypads or fertilizer as when it goes very fast farming it can
> be a TPS eater)."*

Machine-based alternatives in the same spirit: Create's **Mechanical Harvester** (*"will
automatically Farm Mature Crops, and Replant them"* — it *"has to be moved by a
Contraption to work"*), and Industrial Foregoing's **Plants** (`industrialforegoing:plant_gatherer`,
`industrialforegoing:plant_sower`): *"The Plant Gatherer harvests plants in its working
area... The Plant Sower automatically plants crops and saplings."*

### Then the resource farm: Mystical Agriculture

The verified starter chain in the MA chapter (dependencies from the config):

1. **Inferium** (subtitle *"Tier: 1"*, task `mysticalagriculture:inferium_essence`) —
   *"Inferium Essence is the base tier of all essences. You can get this from mining,
   killing mobs, or by making seeds to grow them!"*
2. **Inferium Farmland** (`mysticalagriculture:inferium_farmland`,
   `mysticalagriculture:inferium_seeds`) — the book's own timing advice: *"You'll want to
   start growing Inferium as soon as you can!"*
3. **Infusion Altar** *(subtitle "Creating Seeds"*, `mysticalagriculture:infusion_altar` +
   `mysticalagriculture:infusion_pedestal` ×8*)* — *"The Infusion Altar is how you make
   all of the seeds. Place down the Altar first and it'll show you where to place the
   Pedestals after."*
4. **Infusion Crystal** (`mysticalagriculture:infusion_crystal`) — *"The Infusion Crystal
   is need in order to 'tier up' seeds. For example if you combine the crystal with 4
   Inferium Essence you will get 1 Prudentium Essence."* (spelled that way in the config;
   quest-text arithmetic — quote, don't promise.)
5. Growth aids: **Inferium Growth Accelerator** *(subtitle "Range: 9 Blocks")*, and later
   the untitled *Recycling!* quest (`mysticalagriculture:seed_reprocessor`).

From there the chapter's tier ladder is verified: **Prudentium** *(subtitle "Tier: 2")* →
**Tertium** *(subtitle "Tier: 3")*, each with its own farmland quests (**Prudentium
Farmland**, **Tertium Farmland**). At Tier 3 the seed quests turn to metals and mob drops
— most carry *(no title in the config)* and are identified by their tasks, e.g.
`mysticalagriculture:iron_seeds`, `mysticalagriculture:redstone_seeds`,
`mysticalagriculture:certus_quartz_seeds` *(subtitle "Tier: 3")*. Growing iron instead of
mining it is the payoff that makes this list (judgement). How to automate the *harvest*
of an MA field: the farm machines above, or a storage network's importers (section 5) —
the config doesn't prescribe one; check the quest entries.

## 5. Auto-crafting from your storage network

**Why fifth (judgement):** auto-crafting multiplies everything above — but only once you
have a network worth multiplying. `references/getting-started.md` puts the choice at the
point where "chests stop scaling"; both networks have full chapters, and the pack forces
neither (approximate timing, judgement).

The two alternatives, with their verified entry quests:

- **Applied Energistics 2** — **Auto-Crafting** *(subtitle "Order up"*, task
  `ae2:pattern_access_terminal`*)*: *"AE2's
  auto-crafting system begins with the ME Pattern Provider. The Pattern Provider holds
  certain items called Patterns (covered in the next quest) which are programmed to hold
  some recipe that turns input items into a certain output. Up to 9 patterns can fit in
  one provider."* Then **Patterns** (`ae2:pattern_encoding_terminal`,
  `ae2:blank_pattern`): *"Patterns are what hold an encoded recipe to be fulfilled by a
  Pattern Provider."* — and crucially for sections 1–4, *"a more general 'processing'
  recipe, wherein any input items can be sent out by the provider into some other machine
  block or specialised processing plant."* Bonus crossover: the *(no title in the
  config)* Annihilation Plane quest *(subtitle "GET IN"*, task `ae2:annihilation_plane`*)*
  says the plane *"can be enchanted in the same way as a regular digging tool"* and is
  *"ideal for processing ore blocks when enchanted with Fortune, for example."* A second
  untitled quest (task `ae2:growth_accelerator`) covers speeding up crystal growth:
  *"Place these around your Budding Crystals, give them some power, and watch your
  crystals grow!"*
- **Refined Storage** — **Autocrafting** *(subtitle "Follow the Pattern"*, task
  `refinedstorage:pattern`)*: *"Patterns are the bread and butter of autocrafting."* Then
  **Autocrafter** *(subtitle "Automated crafting!"*, task `refinedstorage:autocrafter`*)*:
  *"Once a recipe is placed into the
  machine, you'll be able to 'Request' an item to be crafted from your Grid."* — and, like
  AE2, processing patterns face machines: *"if you point the Autocrafter at a Furnace, you
  can put a recipe inside for a recipe you need a Furnace for"*, with an importer on the
  furnace side. Supporting quests: **Pattern Grid** (`refinedstorage:pattern_grid`),
  **Monitoring Autocrafting**, **Managing Autocrafters**.

Present these as the two doors they are — trade-offs and which is "better" are
version-sensitive and player-dependent; the quest chapters and JEI decide (approximate).

## Quick wins just off the top five

Verified, cheap, and worth doing while the big five are still forming (judgement order):

- **Bees that drop off their own combs.** Productive Bees: **Capturing Bees!**
  (*"Right-clicking a bee with this will capture it!"*) → **Your First Beehive**
  (`minecraft:beehive`) → **Advanced Beehive** *(subtitle "No more shearing.")*: *"Bees
  will fly in and out of these, and drop off Honeycombs in the inventory."* The untitled
  Centrifuge quest *(subtitle "Processing Honeycombs")* adds: *"getting a Powered
  Centrifuge soon after is a must."*
- **Flux dust, hands-free.** Basic Power carries **two** quests titled **Automated Flux
  Dust** — one via bees (*"Flux Dust can be automated using Productive Bees!"*, task
  `productivebees:spawn_egg_configurable_bee`), one via XyCraft (*"Flux Dust can also be
  automated using XyCraft!"*, tasks `xycraft_machines:extractor`,
  `appflux:charged_redstone_block`). Relevant only once Flux Networks power is on the
  table.
- **Crafting bigger than 3×3, automatically.** Create's **Mechanical Crafter**: *"can be
  used for Auto-Crafting and Recipes that are bigger than 3x3 Crafting Grid like the
  Crushing Wheel."*

## What NOT to automate first (judgement, with verified signposts)

- **Mekanism Tier 3/4 ore chemistry.** The task lists above (thermal evaporation ×33,
  dissolution/washer/crystallizer) are the config's own evidence that these are
  factory-scale projects. Tier 1 first.
- **Quarries.** The steam quarry quest in Steam Age: New Beginnings is *(no title in the
  config)*, subtitled *"Infinite Resources"* — *"The Quarry is a multiblock to generate
  resources. It requires Drills and Steam to function."* — and its task list wants
  `modern_industrialization:steam_quarry` plus `modern_industrialization:steel_machine_casing`
  ×13 and hatches: deep into the Steel phase of that chapter. The pack's own quarry
  advice, *"I recommend setting up a Quarry."*, sits in the endgame **Mining Dimension**
  quest of Chapter 2: Allthemodium. Digging up the world belongs after power, processing,
  and storage are running (judgement).
- **Mob-drop factories.** Hostile Neural Networks (**Simulating Deaths**, **Creating
  Loot**) and the MA mob-seed line are excellent — later. Their chapters assume power and
  resource infrastructure already exist (judgement; see the tier subtitles in section 4).
- **Chapter 4: Creative's multiblocks.** Those are post-ATM-Star automation and live in
  `references/creative-checklist.md`.

## Using this page when advising a player

- Answer *"what should I automate first?"* with the numbered list above, in order, and say
  plainly that the ordering is judgement while the quests quoted are the book's.
- Anchor each recommendation to its verified quest title and chapter so the player can
  open it in the book — then let the quest entry and JEI supply counts, recipes, and
  current numbers.
- If the player has already committed to a tech line (Mekanism vs Create vs Modern
  Industrialization vs Oritech), recommend the route inside *that* line from section 1's
  alternatives; never invent a "required" path — the pack gates nothing.
- Keep the hedges: yields and FE figures are quest-text quotes, timings are approximate,
  and the in-game quest book is authoritative over everything on this page.

## Cross-references

- `references/getting-started.md` — first hours, the Chapter 1 walk-through, and the
  "start MA early-ish" advice this page grounds in quests.
- `references/progression.md` — the four stages; sections 1–4 here are early-game → tech,
  and the stage map says when each chapter is naturally reached.
- `references/key-mods.md` — one-paragraph primers for Mekanism, Create, AE2/RS, MA, and
  the rest named above.
- `references/creative-checklist.md` — the *end* of the automation road: star automation
  and the creative-tier quests, from the same pinned commit.

## What this page deliberately does not tell you

- **Recipes.** Not one. Ore hammers, machines, patterns — JEI has every recipe, and
  recipes are where pack versions differ most.
- **Energy amounts, throughput numbers, farm layouts.** The quoted yields ("2 Dust from 1
  Ore", "3 Raw Ore to get 4 Dust", "Up to 9 patterns") are quest-text figures; anything
  beyond them is in the quest entries and the mods' own guide books.
- **A ranking the pack endorses.** The book has no "automate this first" order; the
  five-item ranking is this skill's judgement, built from what Chapter 1 assigns and what
  each automation unlocks.
- **Anything not in the config.** If a player names a machine, item, or automation that is
  not listed here, the answer is "open that quest in the book / look it up in JEI" — never
  a guess.
