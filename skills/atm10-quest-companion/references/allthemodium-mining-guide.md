# Allthemodium mining guide: where the three ATM ores spawn and what mines them

**What this page is.** The mining companion to `references/resource-farming-guide.md`. That
page says **where a gated material comes from** across the whole pack — ores, templates, mob
drops, alloys, and the farms that replace mining. This one covers only the three
Allthemodium ores — **allthemodium**, **vibranium**, and **unobtainium** — and answers just
three questions for each, with the pack's own words:

1. **Which dimension** is it in?
2. **Where in that dimension** does it spawn?
3. **What pickaxe / mining level** does it need?

Everything below was read out of the pack's own config: the quest book's chapter files and
their English lang entries, the biome tags the pack ships for ore spawning, the harvest-tier
ladder in the Basic Tools chapter, and — most directly — the **in-game item tooltips the
pack installs on the ore blocks themselves**. Nothing here is remembered from playing, from
a wiki, or from another pack.

## Provenance — everything here was read, not remembered

Every quest title, quest id, item id, biome id, dimension id, tier number, and quoted
sentence below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10), `main` at the pinned commit
**`e5e3d1d83e`** (full SHA `e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025`) — the same snapshot
the sibling endgame docs were read from. `CHANGELOG.md` dates that commit **2026-09-22**,
which it lists as **pack 8.2** — the `"8.x"` stamp in `examples/progress.example.json`;
`config/bcc-common.toml` carries `modpackVersion = "8.2"` at the same commit.

| File(s) in the pack repo | What they supplied |
|---|---|
| `kubejs/client_scripts/tooltips.js` | the pack's **own in-game tooltip lines** on the three ore blocks: the mining requirement and the spawn location, verbatim |
| `kubejs/data/atm10/tags/worldgen/biome/allthemodium_spawnable.json`<br>`.../vibranium_spawnable.json`<br>`.../unobtainium_spawnable.json` | the biome tags that gate where each ore generates, and the ids inside them |
| `config/ftbquests/quests/chapters/allthemodium.snbt` | quest ids, task types and values (`item`, `dimension`, `structure`, `checkmark`), dependency links, reward items |
| `config/ftbquests/quests/lang/en_us/chapters/allthemodium.snbt` | the English quest titles and the description text quoted below (Minecraft `&` formatting codes stripped) |
| `config/ftbquests/quests/chapters/basic_tools.snbt` + its `lang/en_us` file | the **Harvest Tier 1–6** ladder and the `Tier: N` subtitle on each pickaxe quest |
| `config/potionsmaster/allthemodium.json`,<br>`config/potionsmaster/vibranium.json`,<br>`config/potionsmaster/unobtainium.json` | the ore tags and the raw-material ids the Ore Sight potions key on |
| `kubejs/data/industrialforegoing/recipe/laser_drill_ore/raw_materials/*.json` | the three laser-drill entries: which biome tag each reads, and which pickaxe it takes as its catalyst |
| `config/crash_assistant/modlist.json` | the mod jar the ores come from: `allthemodium-3.0.1_mc_1.21.1.jar` — **Allthemodium 3.0.1** |

Chapters read for this page: `allthemodium` — **Chapter 2: Allthemodium** (`4293754F9B2D05F0`,
**54 quests**, group *Main Questline*, stage `endgame`) and `basic_tools` — **Basic Tools**
(`4B9D26E0087CD163`, **77 quests**, group *Tools and Gear*, stage `early-game`). Both ids,
titles, and counts agree with `examples/progress.example.json`.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a snapshot
  of pack 8.2's config. If the player's book or his tooltips differ, **his game wins** — say
  so and re-research rather than arguing from this file.
- **The pack's own tooltips are the strongest source here, and they are still a snapshot.**
  The "Needs at least …" and "Found in …" lines quoted below are strings the pack installs on
  the ore items, not something a player typed — but they are 8.2's strings. A pack update can
  change them, and a mod added on top can change what actually generates.
- **A biome tag proves *where the pack gates generation*, not the only place ore appears.**
  `atm10:vibranium_spawnable` holds two vanilla Nether biomes while the tooltip says *"Found
  in any Nether biome"* — two pack sources that do not say the same thing. This page prints
  both and marks the gap; it does not pick a winner.
- **No ore levels, no coordinates, no counts per chunk, no recipes.** The config names the
  biome and the mining tier. It does not publish a Y range for these ores, and this page will
  not supply one — anything about distribution that the config does not state is
  **approximate** at best and belongs in the quest entry and JEI, not here. Where the pack
  ships a number that is *not* an ore level (the laser drill's own configured depth band), it
  is pointed at and deliberately not repeated.
- **Untitled quests are marked.** Several of the quests this page leans on carry no title in
  the lang file; the book shows the task item's own name instead. `*(no title in the config)*`
  marks those — never present a derived name as a verified title.
- **Stages are the skill's, not the pack's.** The `endgame` / `early-game` tags come from
  `references/progression.md`'s four stages via `examples/progress.example.json`. The pack
  gates nothing: its Welcome chapter says *"In this modpack, quests are optional. Mods are
  not gated behind completing any quests!"*
- **Nothing here was invented.** Every id in the tables below is one the config contains. If
  a detail is not on this page, the answer is "check the quest entry / JEI" — not a guess.

## The three ores at a glance

"Tracked by" = chapter → verified quest title. Item and biome ids are the config's own.
Harvest tiers are the `Tier: N` subtitles the Basic Tools chapter puts on the pickaxe quests.
Each ore then gets its own section under [Ore by ore](#ore-by-ore), with the pack's exact
words for where it spawns and what mines it.

| Ore | Ore block id(s) | Dimension | Spawns in | Needed pickaxe | Harvest tier | Tracked by |
|---|---|---|---|---|---|---|
| Allthemodium | `allthemodium:allthemodium_ore`, `allthemodium:allthemodium_slate_ore` | the Overworld — `minecraft:overworld` (and the Mining Dimension — `allthemodium:mining`) | the **Deep Dark** biome — `minecraft:deep_dark` | Netherite or better | 5 | Chapter 2: Allthemodium → *Ancient City*, *Allthemodium Ingot* |
| Vibranium | `allthemodium:vibranium_ore`, `allthemodium:other_vibranium_ore` | The Nether — `minecraft:the_nether` (and The Other — `allthemodium:the_other`) | Nether biomes — tag lists `minecraft:crimson_forest`, `minecraft:warped_forest` | Allthemodium or better | 6 | Chapter 2: Allthemodium → *Vibranium Ingot* |
| Unobtainium | `allthemodium:unobtainium_ore` | The End — `minecraft:the_end` | **End Highlands** — `minecraft:end_highlands` | Vibranium or better | 6 | Chapter 2: Allthemodium → *Unobtainium Ingot* |

The three raw materials, for the ore-processing step and the Ore Sight potions that key on
them, are `allthemodium:raw_allthemodium`, `allthemodium:raw_vibranium`, and
`allthemodium:raw_unobtainium`; the ore tags are `c:ores/allthemodium`, `c:ores/vibranium`,
and `c:ores/unobtainium`.

## Ore by ore

### 1. Allthemodium — `allthemodium:allthemodium_ore`

**Ore ids:** `allthemodium:allthemodium_ore` and `allthemodium:allthemodium_slate_ore`. The
pack's tooltip script attaches the same three lines to both, so treat them as the same
progression step. The raw drop is `allthemodium:raw_allthemodium`.

**Dimension:** the **Overworld** — `minecraft:overworld`. The chapter tracks it with its own
`dimension minecraft:overworld` task, and the spawn biome the pack gates it on —
`minecraft:deep_dark` — is a vanilla Overworld biome. There is a **second source the
book itself points at**: the Mining Dimension, `allthemodium:mining`, which the chapter
also tracks with a dimension task — the *Allthemodium Ingot* quest's own words are
*"You can use those to get to the Mining Dimension to find more Allthemodium"*.

**Where it spawns:** the **Deep Dark**, per the biome tag `atm10:allthemodium_spawnable`,
whose single value is `minecraft:deep_dark`. The tooltip adds the detail that makes it
findable — it *"will always spawn air exposed"*, so it is a cave-wall ore, not a buried one.
In the Mining Dimension the tooltip places it in the **Deep Slate Layer**.

**Mined by:** **Netherite or better.** The tooltip line is *"Needs at least Netherite to be
mined"*; the quest says the same thing in the author's own words.

**Harvest tier:** **5.** The Basic Tools chapter's *Harvest Tier 5* quest wants
`allthemodium:raw_allthemodium` as its task item, and both the `minecraft:netherite_pickaxe`
quest and the `mekanismtools:refined_obsidian_pickaxe` quest carry the subtitle `Tier: 5`.

**Tracked by:** Chapter 2: Allthemodium (`allthemodium`, 54 quests) — whose hub quest is
simply titled *Allthemodium* (`4B2146C9527C54E7`) — → *Ancient City* (`111E4ACF7D570EE8`, a
`structure minecraft:ancient_city` task) → *Allthemodium Ingot* (`201EE3566D4D3123`, whose
task is the ingot itself).

**The pack's own words.** The tooltip, verbatim:

> Needs at least Netherite to be mined
> Found in the Deep Dark Biome and will always spawn air exposed
> Also found in the Deep Slate Layer of Mining Dimension

The *Ancient City* quest:

> Only the hardest Structure in Vanilla Minecraft. So of course that's where you'll have to
> look for Allthemodium! You can find the Ore in the walls of Caves around the Ancient
> Cities, it's Glowing so it'll be easy to spot just very rare! You will also be able to
> locate it in any Deep Dark Biome.

The *Allthemodium Ingot* quest:

> To mine Allthemodium you'll need a Pickaxe that is Netherite Tier or higher! Once you
> finally get the Ore (first I recommend processing it either with Fortune, Occultism, or
> Mekanism to get more) then you can get a few choices of what to do with it. I recommend
> making 2 Teleport Pads with the Nuggets! You can use those to get to the Mining Dimension
> to find more Allthemodium or The Other to find other adventures. After that I recommend
> upgrading your Pickaxe so you can Mine Vibranium. The rest is all up to you!

**The Mining Dimension is the volume answer** *(judgement, from the quest text's own
framing).* The *Mining Dimension* quest (`6D738730B371B152`) describes it as *"a Superflat
world with absolutely nothing on the surface. Below the surface is almost every single Ore."*
with *"no Caves, no Mob Spawns, and nothing to get in your way. It's just Stone types and
Ores!"*, and warns that *"Ore spawns differ for the Y Level and layer in the Mining
Dimension."* — **the pack is telling you it will not give you a Y level, and neither will
this page.** The route in is the *Teleport Pad* quest
(`07FDA46D83F8360D`) and the *Overworld* quest (`2C4299D33D419AA0`): *"Place the Teleport Pad
in the Overworld to go to the Mining Dimension."*

### 2. Vibranium — `allthemodium:vibranium_ore`

**Ore ids:** `allthemodium:vibranium_ore` and `allthemodium:other_vibranium_ore` — two ids
the pack's tooltip script names on the same line, so read them as one ore. The raw drop is
`allthemodium:raw_vibranium`.

**Dimension:** **The Nether** (`minecraft:the_nether`), with **The Other**
(`allthemodium:the_other`) as the richer second source. Both are tracked by the chapter's own
dimension tasks.

**Where it spawns:** **Nether biomes.** The tooltip says *"Found in any Nether biome"*. The
pack's own biome tag `atm10:vibranium_spawnable` is narrower — it lists exactly two values,
`minecraft:crimson_forest` and `minecraft:warped_forest`. **These two config sources do not
agree**, and this page will not smooth it over: the tag is what gates generation in 8.2, the
tooltip is what the player actually reads on the item. Check both in-game; the quest book and
JEI win. The Other is a location, not a biome list: the *The Other* quest
(`15FEA03A2CDBA33B`) says *"You can also mine for Vibranium (and other ores!) or find it and
better in the structures!"* — its structures being *"Piglin Village, Ancient Pyramid, and
Dungeon"* — and *"You can't set up Quarries for many blocks in The Other though, no cheesing
anything here."*

**Mined by:** **Allthemodium or better.** The tooltip line is *"Needs at least AllTheModium
to be mined"*; the quest words it as *"it requires Allthemodium Pickaxe (or the same tier) to
mine it"*.

**Harvest tier:** **6.** The Basic Tools chapter's *Allthemodium Pickaxes* quest
(`609D03E335CF32E2`) carries the subtitle `Tier: 6`, and its task filter names all four
tier-6 picks: `allthemodium:allthemodium_pickaxe`, `allthemodium:vibranium_pickaxe`,
`allthemodium:unobtainium_pickaxe`, and `allthemodium:alloy_pick`.

**Tracked by:** Chapter 2: Allthemodium → *Vibranium Ingot* (`144BB025516E0994`, whose task
is the ingot). The route to the better source runs through *Teleport Pad*
(`07FDA46D83F8360D`) → *The Nether* (`0CC0632E8276C787`): *"Place the Teleport Pad in The
Nether to go to The Other."*

**The pack's own words.** The tooltip, verbatim:

> Needs at least AllTheModium to be mined
> Found in any Nether biome
> Also found in The Other

The *Vibranium Ingot* quest:

> Vibranium is the next ore after Allthemodium, so of course it requires Allthemodium Pickaxe
> (or the same tier) to mine it. You can find it rarely in The Nether or abundantly in The
> Other. It is also recommend to Ore Process it to get more. Sadly, while it's a cool colored
> ATM ore, it has the least uses for different Items.

**"Rarely" and "abundantly" are the pack's own adverbs** — they are a relative hint from the
author, not a measured rate. Treat the Nether as the first, thinner source and The Other as
the one worth the trip.

### 3. Unobtainium — `allthemodium:unobtainium_ore`

**Ore ids:** `allthemodium:unobtainium_ore` — the only one of the three with a single block
id in the pack's tooltip script. The raw drop is `allthemodium:raw_unobtainium`.

**Dimension:** **The End** (`minecraft:the_end`), tracked by the chapter's own `dimension
minecraft:the_end` task.

**Where it spawns:** **End Highlands**, per the biome tag `atm10:unobtainium_spawnable`,
whose single value is `minecraft:end_highlands`. The tooltip agrees: *"Found in the End
Highlands"*. The quest adds the landmark that makes the biome findable: *"Those are usually
where End Cities spawn as well!"*

**Mined by:** **Vibranium or better.** The tooltip line is *"Needs at least Vibranium to be
mined"*; the quest says *"You'll need a Vibranium Pickaxe (or same Tier) to Mine the Ore."*

**Harvest tier:** **6.** The same tier as vibranium, which is why the *Harvest Tier 6* quest
spans both and why the chapter's *"or same Tier"* wording holds. That quest's task item is
`allthemodium:raw_unobtainium`.

**Tracked by:** Chapter 2: Allthemodium → *Unobtainium Ingot* (`4A079D40C0AF6BC3`, whose
task is the ingot). The End itself is the chapter's *The End* quest
(`2EDE91023F7924FB`), a `dimension` task for `minecraft:the_end`.

**The pack's own words.** The tooltip, verbatim:

> Needs at least Vibranium to be mined
> Found in the End Highlands

The *Unobtainium Ingot* quest:

> No it isn't found in The Beyond. You can find Unobtainium Ore very rarely in End Highlands
> Biomes. Those are usually where End Cities spawn as well! You'll need a Vibranium Pickaxe
> (or same Tier) to Mine the Ore. Do I need to still tell you to Ore process it?

**The obvious shortcut is closed on purpose.** The third ore sends the player *back* to the
End, not forward into the new dimension. The *The Beyond* quest (`11E957CDEFA0CAAB`) is a
`dimension` task for `allthemodium:the_beyond`, and it is described as *"Welcome to The Beyond!
There's nothing here! You might want an Angel Block."* — and the *Unobtainium Ingot* quest
opens by killing the guess: *"No it isn't found in The Beyond."*

## What mines them: the harvest tier ladder

The tier numbers above are not this page's invention — they are the **Basic Tools** chapter
(`4B9D26E0087CD163`, 77 quests, *Tools and Gear*), which ships a six-step *Harvest Tier*
ladder. Each rung is a quest whose **task item is the ore or block that tier unlocks**, and
whose description says what the tier is for:

| Tier | Verified quest title | Quest id | Task item | The config's description |
|---|---|---|---|---|
| 1 | *Harvest Tier 1* | `57F47BA495B27F83` | `minecraft:cobblestone` | *"Tier 1 Harvest Level is the lowest pickaxe level, needing a pickaxe. Any pickaxe can mine these. Items that are Tier 1 would be like Stone, Furnace, and Coal Ore."* |
| 2 | *Harvest Tier 2* | `3917DECAEF56A06A` | `minecraft:raw_iron` | *"Tier 2 is the stone pickaxe level. It's almost only for mining Iron items."* |
| 3 | *Harvest Tier 3* | `6601450C63FEEE61` | `minecraft:diamond` | *"Tier 3 is Iron Pickaxe level, it mines most ores like Diamond, Emerald, and Gold."* |
| 4 | *Harvest Tier 4* | `17FE0C7748DD65CA` | `minecraft:ancient_debris` | *"Tier 4 is Diamond tool level, used to get Obsidian and Netherite. Also some modded ores like Uranium and Platinum."* |
| 5 | *Harvest Tier 5* | `03E05018D64DDEE1` | `allthemodium:raw_allthemodium` | *"Tier 5 is basically just for Allthemodium Ore, not much else."* |
| 6 | *Harvest Tier 6* | `09733948CBCB3FB9` | `allthemodium:raw_unobtainium` | *"Tier 6 is the highest tier, anything that is breakable can be mined with it, including Vibranium and Unobtainium."* |

The ladder is a dependency chain — each tier quest depends on the one below it — so the book
teaches the tiers in order.

### Which pickaxe sits at which tier

The same chapter stamps a `Tier: N` subtitle on each pickaxe quest. These are the ones that
matter for the three ores:

| Pickaxe | Tier | Quest id | Task |
|---|---|---|---|
| `minecraft:netherite_pickaxe` | 5 | `299F56B753286D0C` | the pickaxe item |
| `mekanismtools:refined_obsidian_pickaxe` | 5 | `512396B331108BAF` | the pickaxe item |
| `allthemodium:allthemodium_pickaxe` | 6 | `609D03E335CF32E2` | *Allthemodium Pickaxes* filter — also `allthemodium:vibranium_pickaxe`, `allthemodium:unobtainium_pickaxe`, `allthemodium:alloy_pick` |
| `mysticalagriculture:supremium_pickaxe` | 6 | `58DDD32F849940A0` | *Supremium Pickaxes* filter — also `mysticalagriculture:awakened_supremium_pickaxe` |

Two things follow, and both reconcile the two chapters rather than contradicting them:

- **Netherite is the Allthemodium gate**, because netherite sits at tier 5 and
  `allthemodium:allthemodium_ore` is the tier-5 ore. The *Allthemodium Ingot* quest's
  *"Netherite Tier or higher"* and the ladder's *"Tier 5 is basically just for Allthemodium
  Ore"* are the same statement in two vocabularies.
- **Vibranium and unobtainium share a tier.** Chapter 2 words them as two separate gates
  (*"Allthemodium Pickaxe"* for vibranium, *"Vibranium Pickaxe"* for unobtainium), but the
  ladder puts both ores at tier 6 and stamps **all three ATM picks plus the alloy pick** at
  tier 6. That is exactly why the chapter says *"(or the same tier)"* / *"(or same Tier)"* —
  any tier-6 pickaxe clears both ores. **Verification note:** the tier numbers are read from
  the quest subtitles, not from a mod's code; if an in-game tooltip disagrees with a tier
  number, the game wins.

## Getting more per ore

This page is about **where the ore is and what mines it** — the doubling/tripling chain is
`references/ore-processing-ladder.md`'s job. What belongs here is what Chapter 2's own text
says about the mining trip:

- **Process it.** All three ore quests say so, in near-identical words — *"first I recommend
  processing it either with Fortune, Occultism, or Mekanism to get more"*, *"It is also
  recommend to Ore Process it to get more"*, and the exasperated *"Do I need to still tell you
  to Ore process it?"*
- **Ore Sight potions.** The untitled follow-up quest `18FAD56CDE05646A`
  *(no title in the config)* — a `checkmark` task, icon `allthemodium:allthemodium_slate_ore`,
  rewarding a `potionsmaster:allthemodium` potion — says: *"Before Quarries in the Mining
  Dimension used to mine everything but leave Allthemodium Ore. Now it will Mine Allthemodium
  but Void the drops... might want to be careful with your Quarries now! I recommend Mining
  with Ore Sight Potions if you are looking strictly for Allthemodium!"* The pack ships an
  Ore Sight entry per metal — `config/potionsmaster/allthemodium.json`,
  `vibranium.json`, and `unobtainium.json` — keyed to `c:ores/allthemodium`,
  `c:ores/vibranium`, and `c:ores/unobtainium`. **Only `potionsmaster:allthemodium` is quoted
  from a quest reward on this page; the other two potion ids are the config's own entry names,
  not quoted from a quest** — check JEI before promising them.
- **Quarries are a trap for Allthemodium, and banned in The Other.** The same untitled quest
  warns that a Mining Dimension quarry will *"Mine Allthemodium but Void the drops"*, and the
  *The Other* quest states *"You can't set up Quarries for many blocks in The Other though, no
  cheesing anything here."* Hand-mining is the book's own recommendation for these three.
- **Industrial Foregoing's laser drill reads the same biome tags.** The pack ships a laser
  drill entry for each raw metal
  (`kubejs/data/industrialforegoing/recipe/laser_drill_ore/raw_materials/raw_allthemodium.json`,
  `raw_vibranium.json`, `raw_unobtainium.json`), each whitelisting its matching
  `atm10:*_spawnable` biome tag and taking the matching pickaxe as its catalyst —
  `allthemodium:allthemodium_pickaxe`, `allthemodium:vibranium_pickaxe`,
  `allthemodium:unobtainium_pickaxe`. That is a **cross-check on the dimension and tier
  tables above from a second, independent config file**, not a recommendation. **Those recipes
  carry a configured depth band of their own — that number belongs to the drill, not to world
  generation, so this page does not repeat it as an ore level.** Read it off the recipe in
  JEI.

## Related pages

- `references/resource-farming-guide.md` — the parent page: where every gated material comes
  from, including the three smithing templates, the Piglich Heart, and the three alloys that
  this page's ores feed.
- `references/ore-processing-ladder.md` — how to turn the raw drops into more ingots.
- `references/armor-tools-ladder.md` — what the three metals and the alloy tier are *for*.
- `references/dimension-guide.md` — how to reach the Mining Dimension, The Other, and The
  Beyond (Teleport Pad routing), and what else each is worth a trip for.
- `references/atm-star-checklist.md` — what the ATM Star asks for out of all this.
- `references/progression.md` — the four stages this page tags ores with.

## What this page deliberately does not tell you

- **No ore levels.** The config gives biomes and tiers, not Y ranges. The *Mining Dimension*
  quest says outright that *"Ore spawns differ for the Y Level and layer"* — the pack declines
  to publish them, and so does this page. The laser drill's own configured depth band is the
  drill's setting, not a spawn range.
- **No coordinates, and no "go to X, Z".** Nothing here points at a place on a map.
- **No recipes** — not the Teleport Pad, not the pickaxes, not the Ore Sight potions, not the
  laser drill. Those are JEI's.
- **No counts per chunk, no veins-per-biome, no rates.** *"Very rare"*, *"rarely"*, and
  *"abundantly"* are the pack author's own hedges and they are quoted, never converted into
  numbers.
- **No mod-added behaviour.** Another mod in the pack can move or duplicate these ores;
  another pack version can change the biome tags. This page describes **pack 8.2 at commit
  `e5e3d1d83e`**.
- **Where two pack sources disagree, both are printed.** The vibranium biome tag
  (crimson + warped forest) versus its tooltip (*"any Nether biome"*) is the live example.
  This page never silently picks one.

## Using this page in a session

1. Answer the three questions in order — **dimension, where in it, what pickaxe** — quoting
   the tooltip line and the quest title, not a remembered rule.
2. Keep the hedges. *"Very rare"* stays *"very rare"*; a tier number is always *"per the Basic
   Tools chapter's subtitle"*.
3. Point the player at the in-game quest book, the ore's own tooltip, and JEI for anything
   this page withholds — Y levels, recipes, rates, and the current tier of any tool.
4. If the material is not one of these three ores, this is the wrong page — use
   `references/resource-farming-guide.md`.
