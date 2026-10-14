# Apothic Enchanting — how to get the best enchants (58 quests, verified titles)

**What this page is.** The answer to the beginner question "how do I get the best
enchants?" in **All the Mods 10**, read from the quest book's **Apothic Enchanting**
chapter and the pack's Apotheosis enchantment config. As the chapter's first quest puts
it, *"Enchanting gets a few changes with Apotheosis."* — and *"To summarize it, 15
Bookshelves won't be enough now."* Shelves give the table **three stats**, the best
shelves are made by **infusing** items in the table itself, and how high the table can go
is capped by your Apotheosis **World Tier**. The `apothic_enchanting:` items come from
Apothic Enchanting 1.6.2, one of the Apothic mods alongside Apotheosis 8.8.0. This page
maps that chapter — what each quest asks for, in dependency order — quotes what the
quests' own text says about the stats, and lists how high the config lets every vanilla
enchantment go. It is a *map of the chapter and its config*, not a crafting guide.

## The short answer: how do I get the best enchants?

1. **Three table stats decide what you get — Eterna, Quanta, Arcana — and the shelves
   around the table set them.** In the chapter's own words, Eterna *"sets the Enchantment
   Level"*, Arcana *"makes rare Enchantments more common"*, and Quanta mixes the pool up,
   but *"the more you have it, the more common weaker Enchantments will get."*
2. **Two ceilings cap Eterna.** Your **World Tier** — 30 on Haven, 45 on Frontier, 60 on
   Ascent, 75 on Summit, 100 on Pinnacle, per the quest *Eterna* — and **each shelf's own
   maximum**, from 30 for Basic Bookshelves up to 100 for the Draconic Endshelf. That is
   why the quest *The Frontier Calls* is subtitled *"Why is my Eterna capped to 30?"*
3. **So climb both ladders together.** The World Tier quests live in the **Apotheosis
   Gear** chapter, and this chapter's four tier quests depend on them; the shelf quests
   climb Hellshelves *or* Seashelves → their infused versions → Deepshelves →
   Sculkshelves → Endshelves (the table in "Tier by tier" below).
4. **The finish line is the quest *Best Enchanting set-up*** — 5 Soul-Touched
   Sculkshelves, 5 Echoing Sculkshelves, a Draconic Endshelf, a Geode-Encased Bookshelf
   of Stability, and a Deepshelf of Arcane Treasures — whose text promises *"every stat
   maxed out, every good Enchantment available"*. After it, *Enchanting Table of the
   Raven* sets the three stats directly, *"without the need for shelves."*
5. **Steer the pool instead of rerolling blindly.** The Geode shelf removes Quanta's
   weak-enchant penalty, the filtering shelf blacklists an enchantment, the *Enchanting
   Clues* shelves reveal enchantments before you pick, the treasure shelf adds ones like
   Mending — and the ? button in the table's GUI shows the pool ("Steering what the table
   offers").
6. **Each enchantment's maximum level is configured** in `config/apotheosis/enchantments.cfg`:
   `minecraft:sharpness` goes to **9** (originally 5), `minecraft:efficiency` to **9**,
   `minecraft:fortune`, `minecraft:looting`, and `minecraft:unbreaking` to **8**, while
   `minecraft:mending` stays **1**. *Which* Eterna reaches which level is not in the
   config — the table's pool view and JEI are the place to check.
7. **Bank and merge books in the Enchantment Library** — it only pays out up to *"the
   highest Level of Book you've put in"*.

Every number above is a quote from the pack 8.2 config, not a formula: the in-game quest
book and JEI stay authoritative.

## Provenance — everything here was read, not remembered

Every quest title, subtitle, task item, count, dependency, stat figure, and quoted sentence
below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** (`config/bcc-common.toml` stamps
the same `modpackVersion`) — the "8.x" that `examples/progress.example.json` is stamped
with:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/ftbquests/quests/chapters/apothic_enchanting.snbt` | the chapter's 58 quests, their task items and required counts, dependency links, the six `quest_links`, and the few reward lines quoted |
| `config/ftbquests/quests/lang/en_us/chapters/apothic_enchanting.snbt` | the English quest titles, subtitles, task titles, and the description text quoted below |
| `config/ftbquests/quests/chapters/apotheosis_gear.snbt` and its `lang/en_us/chapters/` file | the five World Tier quests (and their intro quest) that this chapter links to and depends on, and their quoted requirements |
| `config/ftbquests/quests/chapters/` `apotheosis_2.snbt`, `chapter_2_the_star.snbt`, `achapter_2r_6the_atm_star.snbt`, `tips_and_tricks.snbt`, `industrial_foregoing.snbt`, and their `lang/en_us/chapters/` files | the enchanting quests in other chapters ("Where enchanting touches the rest of the book") |
| `config/ftbquests/quests/lang/en_us/chapter.snbt` and `chapter_group.snbt` | chapter titles and their quest-book groups |
| `config/apotheosis/enchantments.cfg` | every enchantment's `Max Level`, `Max Loot Level`, and `Forced Level Cap` |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |

The book names the chapter **Apothic Enchanting** (no subtitle), icon
`apothic_enchanting:apothic_enchanting_table`, group **Magic**, `order_index` 0 — the first
chapter of the Magic group. The skill tracks it as `apothic_enchanting` (the config's
filename), stage `magic`. Its two companions are **Apotheosis Gear** (`apotheosis_gear`,
group Tools and Gear, stage `early-game`) — home of the World Tiers — and **Apothic
Spawners** (`apotheosis_2`, group Resources, stage `early-game`). The mods, per the
modlist: Apotheosis 8.8.0, Apothic Enchanting 1.6.2, Apothic Attributes 2.10.1, and Apothic
Spawners 1.4.0.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so and
  re-research rather than arguing from this file.
- **Item ids and counts below are quoted from the config, never invented.** A count is
  shown only where the config states one (the task's required amount); where a task asks
  for one item, no count is printed. Shelf counts *inside quotes* are the quest author's
  suggested set-ups, not task requirements.
- **Stat figures are quest text, not formulas.** Every Eterna / Quanta / Arcana number on
  this page is quoted from a quest description. The config holds no formula for what the
  table rolls; the chapter itself says *"(To know the Levels needed you can check JEI or
  follow these Quests)"*. Treat every quoted set-up as approximate — two quests even
  suggest different set-ups for the same infusion ("Where enchanting touches the rest of
  the book").
- **No recipes.** The config lists *what a quest wants*, never *how to craft it*. Where a
  quest's own text describes a recipe, it is quoted and marked as quest text; otherwise,
  JEI. Do not fill a recipe in from memory or plausibility.
- **Titles are the config's.** 57 of the 58 quests carry an explicit title. The other one
  is marked *(no title in the config)* — the book then shows the task item's own name.
  Shelf names such as "Geode-Encased Bookshelf of Stability" are quoted as the quest text
  spells them; an item id is paired with such a name only where a quest's task and text
  point at the same item.
- **Nothing here was invented, and nothing is added from memory.** A quest that is not on
  this page is not in this chapter: the answer is "open that quest in the book / look it
  up in JEI", never a plausible-sounding guess.

## How the chapter is shaped

| | |
|---|---|
| Quests in the chapter | **58** |
| Tasks in total | 65 (58 `item`, 5 `advancement`, 2 `dimension`) |
| Quests with no dependencies (the four starting points) | 4 — *Apothic Enchanting*, *Enchantment Library*, *Flimsy Ender Lead*, *Gem Case* |
| Dependencies on another chapter | 4 — each a World Tier quest in **Apotheosis Gear** |
| Apotheosis Gear quests shown on this canvas as quest links | 6 — *Invaders/Bosses and World Tiers* and the five *World Tier:* quests |
| Either-or gate quests (`dependency_requirement: "one_completed"`) | 2 — *A Gate*, *Another Gate* |
| Quests carrying an explicit title in the config | 57 (the other one is marked below) |

The book lays the chapter out on a **canvas, not as a numbered list**, so this page does
not invent a sequence: the ladders below are written **in dependency order** (a quest
appears after everything it needs — verified from the config's `dependencies` lists). The
shape is one long spine with side branches:

- **The spine** — the max-enchanting line: *Apothic Enchanting* → *Vanilla Max is just the
  start* → *Infusing* → *Hellshelves* or *Seashelves* → *A Gate* → *The Frontier Calls* →
  *Infused Hellshelves* or *Infused Seashelf* → *Glowing Hellshelf* or *Crystalline
  Seashelf* → *Another Gate* → *Ascent to 60* → *Deepshelf* → *Soul-Touched Deepshelf* and
  *Echoing Deepshelf* → *Soul-Touched Sculkshelf* and *Echoing Sculkshelf* → *Ahh,
  Pinnacle, at last* → *Infused Dragon's Breath* → *Endshelves* → *Draconic Endshelf* →
  *Best Enchanting set-up*; and *Draconic Endshelf* → *God-Fused Pearl* → *Enchanting
  Table of the Raven*.
- **Side branches** — the stat primers (*Eterna*, *Quanta*, *Arcana*, *Negative amounts*),
  the control shelves, the tomes, the two libraries and the two gem cases, the ender
  leads, and a run of infusions that make items rather than shelves.

## The three table stats, in the quest text's words

Three quests, each hanging off *Infusing*, define the stats. Defaults and maximums are the
quest text's figures:

| Stat (verified quest title) | Task item | Default → max (quest text) | What it does, quoted |
|---|---|---|---|
| **Eterna** | one item from the `c:bookshelves` tag (task "Bookshelves") | 0 → set by your World Tier | *"Eterna sets the Enchantment Level which determines what Enchantments you can or will get!"* |
| **Quanta** | `apothic_enchanting:hellshelf` | 15% → 100% | *"Quanta helps to mix up the Enchantment Pool, making it easier to get a whole bunch of different Enchantments."* — but *"the more you have it, the more common weaker Enchantments will get."* |
| **Arcana** | `apothic_enchanting:seashelf` | 0% → 100% | *"it increases the amount of Enchantments you get; and makes rare Enchantments more common."* — e.g. *"Smite is a very common Enchantment but Looting is much more rare."* |

**Infusing** (task: advancement `minecraft:story/enchant_item`) explains what the stats
unlock: *"Infusion is a special version of Enchanting which ironically is used for better
Enchantments."* and *"When the right amount of Eterna, Quanta, and Arcana is reached the
Enchantments will offer Infusion."* The Eterna quest adds that *"Almost all Bookshelves
will give Eterna but each has max they can set it to."*, and *Unbreakable Charms* notes
that shelves are not the only source: *"Yes, some Skulls and other Items besides
Bookshelves give stats!"* — which is why some quoted set-ups below include a Skeleton
Skull or a Candle.

## Ceiling 1 — your World Tier caps Eterna

*The Frontier Calls* says it plainly: *"You might have noticed that your Eterna refuses to
go above 30, even if you used Hellshelves or Seashelves. This is because World Tiers
determine your Max Eterna now."* World Tiers belong to the **Apotheosis Gear** chapter:
this chapter shows six of that chapter's quests as quest links — the five World Tier
quests and their intro, **Invaders/Bosses and World Tiers** — and makes four of its own
quests depend on them.

| World Tier (verified Apotheosis Gear title) | Max Eterna (quest text) | This chapter's quest that waits for it | What the Gear quest says it takes, quoted |
|---|---|---|---|
| **World Tier: Haven** | 30 | — (none; it is *"The 1st World Tier"*) | *"To get it you just need to hold an Affixed Item in your Hand!"* |
| **World Tier: Frontier** | 45 | **The Frontier Calls** — *"Why is my Eterna capped to 30?"* | *"You need a full set of Affixed Armor plus an Affixed Tool or Weapon."* |
| **World Tier: Ascent** | 60 | **Ascent to 60** — *"Max Eterna to 60"* | *"you'll need everything being Uncommon or better."* and *"You'll also need to kill an Invader aka an Apothic Boss"* |
| **World Tier: Summit** | 75 | **To reach the Summit** — *"Max Eterna to 75"* | *"upgrade your Armor and Tool/Weapon from Uncommon to Rare (or better)! You'll also need to kill The Wither."* |
| **World Tier: Pinnacle** | 100 | **Ahh, Pinnacle, at last** — *"Max Eterna to 100"* | *"you'll need to Kill the Ender Dragon atleast once, and equip all Epic or Mythic Armor and Tool/Weapon."* |

- Every tier quest's task is the matching advancement — `apotheosis:progression/haven`,
  `apotheosis:progression/frontier`, `apotheosis:progression/ascent`,
  `apotheosis:progression/summit`, `apotheosis:progression/pinnacle` — and this chapter's
  four tier quests use the same advancements as the Gear chapter's.
- *A Gate* exists *"to allow for either the Seashelf or Hellshelf path to be taken while
  also forcing the Frontier World Tier quest from Apotheosis Gear."* That is the precise
  form of the shorthand "the enchanting chapter requires Apotheosis Gear": its first steps
  do not; its World Tier gates do.
- *To reach the Summit* is off the spine — *"This one is not required for the main shelf
  progression, but is necessary for certain Infusions."* — though in the Gear chapter
  *World Tier: Pinnacle* depends on *World Tier: Summit*, so the climb passes through
  Summit anyway. *Ahh, Pinnacle, at last* also needs **both** Sculkshelf quests.
- The World Tier menu, per the quest text of **Invaders/Bosses and World Tiers**: *"To
  access the World Tier Menu, Hold CTRL and press T."* (Controls are a player setting, so
  treat the key as approximate.)
- The Gear chapter's untitled Gateway quest (task "Apothic Gateways", Gateways To Eternity
  5.1.0 `gateways:gate_pearl`) adds: *"There are Gateways based on each World Tier (except
  Haven), providing waves of monsters and Invaders."* and *"Once you beat the final wave,
  you get a variety of rewards, useful for finishing their respective World Tier."*

The bosses those tiers name — the Wither, the Ender Dragon (and the Warden, for the
Sculkshelves) — are mapped in `references/boss-checklist.md`.

## Tier by tier — which shelves open where

The pairing below is the config's own dependency graph: each shelf quest is listed under
the first tier quest it waits for, directly or through its prerequisites (the Haven row
waits for none). Shelf maximums are each shelf quest's own figure.

| World Tier → Eterna cap | To reach it (Gear quest, short) | Shelf quests this chapter opens there | Shelf max Eterna (quest text) |
|---|---|---|---|
| Haven → 30 | hold an Affixed Item | *Apothic Enchanting*, *Vanilla Max is just the start*, *Infusing*, *Hellshelves* / *Seashelves* | 30 (Basic Bookshelves) |
| Frontier → 45 | full Affixed armor + tool/weapon | *The Frontier Calls* → *Infused Hellshelves* / *Infused Seashelf* → *Glowing Hellshelf* / *Crystalline Seashelf* | 60 (the infused shelves) |
| Ascent → 60 | Uncommon-or-better gear, one Invader | *Ascent to 60* → *Deepshelf* → *Soul-Touched Deepshelf* / *Echoing Deepshelf* → *Soul-Touched Sculkshelf* / *Echoing Sculkshelf* | 75 (the Deepshelf upgrades), 80 (the Sculkshelves) |
| Summit → 75 | Rare-or-better gear, the Wither | *To reach the Summit* (off the spine; certain infusions) | — |
| Pinnacle → 100 | the Ender Dragon, all Epic/Mythic gear | *Ahh, Pinnacle, at last* → *Infused Dragon's Breath* → *Endshelves* → *Draconic Endshelf* → *Best Enchanting set-up* | 90 (Endshelves), 100 (Draconic Endshelf) |

## Ceiling 2 — the shelf ladder, in dependency order

| Step | Verified quest title | Task item(s) in the config | Stats / max Eterna, per the quest text | Needs (verified titles) |
|---|---|---|---|---|
| 1 | **Apothic Enchanting** | `minecraft:enchanting_table` or `apothic_enchanting:apothic_enchanting_table` (one task, "Enchanting Tables") | — | nothing |
| 2 | **Vanilla Max is just the start** | 15 items from the `c:bookshelves` tag (task "Bookshelves") | Basic Bookshelves: *"a max of 30"* | Apothic Enchanting |
| 3 | **Infusing** | advancement `minecraft:story/enchant_item` | — | Vanilla Max is just the start |
| 4 | **Hellshelves** *or* **Seashelves** | `apothic_enchanting:hellshelf` ×11 / `apothic_enchanting:seashelf` ×11 | *"3% Quanta and 3 Eterna"* / *"3% Arcana and 3 Eterna"* | Infusing |
| 5 | **A Gate** (either-or) | `dimension minecraft:overworld` | — | Seashelves *or* Hellshelves |
| 6 | **The Frontier Calls** | advancement `apotheosis:progression/frontier` | tier cap → 45 | World Tier: Frontier (Apotheosis Gear) and A Gate |
| 7 | **Infused Hellshelves** *or* **Infused Seashelf** | `apothic_enchanting:infused_hellshelf` ×8 / `apothic_enchanting:infused_seashelf` ×8 | *"5 Eterna with a max of 60 Eterna, along with 5% Quanta"* / *"more Eterna at 5 with a max of 60. Also more Arcana at 5%"* | Hellshelves / Seashelves, and The Frontier Calls |
| 8 | **Glowing Hellshelf** *or* **Crystalline Seashelf** | `apothic_enchanting:glowing_hellshelf` ×13 / `apothic_enchanting:crystal_seashelf` ×12 | *"the same Eterna and Quanta, but give 3.3333% Arcana"* / *"the same 5 Eterna, 5% Arcana, and now have 3% Quanta"* | Infused Hellshelves / Infused Seashelf |
| 9 | **Another Gate** (either-or) | `dimension minecraft:overworld` | — | Glowing Hellshelf *or* Crystalline Seashelf |
| 10 | **Ascent to 60** | advancement `apotheosis:progression/ascent` | tier cap → 60 | World Tier: Ascent (Apotheosis Gear) and Another Gate |
| 11 | **Deepshelf** | `apothic_enchanting:deepshelf` | its infusion needs *"60 Eterna, 40% Quanta, and 40% Arcana"* | Ascent to 60 |
| 12 | **Soul-Touched Deepshelf** and **Echoing Deepshelf** | `apothic_enchanting:soul_touched_deepshelf` / `apothic_enchanting:echoing_deepshelf` | *"a ton more Quanta at 15%"*, *"increases max Eterna to 75"* / *"a whole lot more Arcana at 15%"*, *"raising the max Eterna to 75"* | Deepshelf |
| 13 | **Soul-Touched Sculkshelf** and **Echoing Sculkshelf** | `apothic_enchanting:soul_touched_sculkshelf` / `apothic_enchanting:echoing_sculkshelf` | *"10 Eterna, 15% Quanta, and 10% Arcana"* / *"10 Eterna, 10% Quanta, and 15% Arcana"*; each *"a max Eterna of 80"* | Soul-Touched Deepshelf / Echoing Deepshelf |
| 14 | **Ahh, Pinnacle, at last** | advancement `apotheosis:progression/pinnacle` | tier cap → 100 | **both** Echoing Sculkshelf and Soul-Touched Sculkshelf, and World Tier: Pinnacle (Apotheosis Gear) |
| 15 | **Infused Dragon's Breath** | `apothic_enchanting:infused_breath` | its suggested set-up gives *"80 Eterna, 25% Quanta and 100% Arcana"* | Negative Enchantments Removal and Ahh, Pinnacle, at last |
| 16 | **Endshelves** | `apothic_enchanting:endshelf` | *"only giving 5 for each. But their max Eterna of 90 is incredible!"* | Infused Dragon's Breath |
| 17 | **Draconic Endshelf** (and **Pearlescent Endshelf**) | `apothic_enchanting:draconic_endshelf` / `apothic_enchanting:pearl_endshelf` | *"it has the max Eterna of 100"* / *"max Eterna 90, but this isn't what we want for max Enchanting"* | Endshelves |
| 18 | **Best Enchanting set-up** | five tasks (next section) | the 100-Eterna build | Draconic Endshelf |

Notes from the quest text, quoted:

- **Pick a path.** *"The Nether can be pretty scary, if you'd rather voyage the Sea, use
  Seashelves!"* The two paths rejoin at *Another Gate*, and *Deepshelf* opens with *"This
  is where the seperation of Hellshelves and Seashelves end!"* (spelled that way in the
  config). For that quest's infusion it suggests *"We can get that with 12 Crystalline
  Seashelves or 13 Glowing Hellshelves!"*
- **The task counts are a down payment.** Several shelf quests ask for fewer shelves than
  the next step needs and pay the rest as a reward: *Hellshelves* asks for 11 and rewards
  5 (*"Make the first 11 and I'll give you the last 5 Hellshelves!"*); *Infused
  Hellshelves* asks for 8 (*"for the ones we want we'll need 13 Infused Hellshelves!"*);
  *Infused Seashelf* asks for 8 (*"Craft 8 and I'll reward you the rest!"*).
- **Infusing a shelf uses the shelves you already have.** *Infused Hellshelves*: *"Once we
  get those 15 Hellshelves around our Enchantment Table, we'll have 45 Eterna and 30%
  Quanta in our Table."* — *"This is the perfect amount to Infuse our Hellshelves!"*
- **The Sculkshelves cost a Warden.** Both Sculkshelf quests: *"Yes, you'll need to kill
  the Warden."* — and both reward an `apothic_enchanting:warden_tendril`.
- **Side shelves on the ladder:** **Blazing Hellshelf** (`apothic_enchanting:blazing_hellshelf`,
  needs Infused Hellshelves) — *"they aren't the cheap option we are looking for"*;
  **Heart-Forged Seashelf** (`apothic_enchanting:heart_seashelf`, needs Infused Seashelf) —
  *"It's a little expensive but gives lots of Arcana!"*. The control shelves are in
  "Steering what the table offers".

## The finish line: *Best Enchanting set-up*, then the Raven

**Best Enchanting set-up** — subtitle *"Without the Enchanting Table of the Raven"*, needs
*Draconic Endshelf* — asks for five tasks, and its text names the same five items in the
same order:

| Task item (config) | Count | What the quest text says it contributes, quoted |
|---|---|---|
| `apothic_enchanting:soul_touched_sculkshelf` | 5 | *"First, is the 5 Soul-Touched Sculkshelves and 5 Echoing Sculkshelves. These will give us all the Quanta and Arcana we need!"* |
| `apothic_enchanting:echoing_sculkshelf` | 5 | (the same sentence) |
| `apothic_enchanting:draconic_endshelf` | 1 | *"Next, is the Draconic Endshelf which will give us 100 Eterna, as in amount of Eterna and the max level."* |
| `apothic_enchanting:geode_shelf` | 1 | *"Third, is the Geode-Encased Bookshelf of Stability, this will make it so the Quanta doesn't backstab us with awful Enchantments!"* |
| `apothic_enchanting:treasure_shelf` | 1 | *"Last is optional but you should add it, the Deepshelf of Arcane Treasures. That Bookshelf will allow us to get Enchantments we normally wouldn't, like Mending!"* |

Its pitch: *"Ever want the most perfect Enchantments? Like, every stat maxed out, every
good Enchantment available? Then, you'll need these!"* One mismatch to keep in mind: the
text calls the treasure shelf optional *for the set-up*, but the config lists it as one of
this quest's five tasks — the book decides what completes the quest.

Past the shelves, two quests:

- **God-Fused Pearl** (`apotheosis:god_fused_pearl`, subtitle *"We're infusing ANYTHING at
  this rate"*, needs Draconic Endshelf) — an infusion window of *"100 Eterna, 9.65-11.00%
  Quanta, and 58.75-60.0% Arcana"*, with the suggested set-up *"1 Draconic Endshelf, 6
  Geode-Encased Bookshelves of Stability, 1 Echoing Sculkshelf, 5 Soul-Touched
  Sculkshelves, 1 Stoneshelf, and 1 Candle."* Its input comes from gear: *"Godforged
  Pearls can be obtained by salvaging Mythic Items in a Salvaging Table."* — and the Gear
  chapter's *Godforged Pearl* quest says *"Mythics are found only in World Tier: Summit
  and in World Tier: Pinnacle, where they are most common."*
- **Enchanting Table of the Raven** (`apothic_enchanting:raven_enchanting_table`, subtitle
  *Quoth the Raven "Nevermore"*, needs God-Fused Pearl) — the end of the spine: *"a
  powerful upgrade to the Enchanting Table, allowing you to customize the Eterna, Quanta,
  and Arcana values of the Table, without the need for shelves."* and *"This can allow you
  to achieve any Infusion with ease."*

## Steering what the table offers

The most useful sentence in the chapter for a beginner is in *Negative Enchantments
Removal*: *"We can see the Pool of Enchantments available by clicking the ? in the Top
Right of the Enchantment Table's GUI when an Item is being Enchanted."* Check the pool
before spending XP. Then shape it:

| Verified quest title | Task item(s) (config) | Needs | What its text says, quoted |
|---|---|---|---|
| **Negative Enchantments Removal** | `apothic_enchanting:geode_shelf` | Infusing | *"The higher the Quanta is, the better the chance we get a weaker Enchantment gets."* (sic) — *"With the Geode-Encased Bookshelf of Stability it will get rid of the increased chances of worse Enchantments."* |
| **Remove Enchantments from Pool** | `apothic_enchanting:filtering_shelf` | Infused Seashelf | *"Place an Enchantment Book, you want to Blacklist, in an empty spot in this Seashelf."* — *"Then, when you Enchant, this Enchantment won't show up on Items or Books."* |
| **Enchanting Clues** | `apothic_enchanting:sightshelf`, `apothic_enchanting:sightshelf_t2` | Infused Hellshelves | *"Each Enchanting Clue will tell you 1 Enchantment before you actually use it."* |
| **Best Enchanting set-up** (its fifth task) | `apothic_enchanting:treasure_shelf` | Draconic Endshelf | *"That Bookshelf will allow us to get Enchantments we normally wouldn't, like Mending!"* |
| **Negative amounts** | `apothic_enchanting:beeshelf`, `apothic_enchanting:stoneshelf`, `apothic_enchanting:melonshelf` | Eterna, Quanta, and Arcana | *"Some Infusions need very, very exact amounts of Eterna, Quanta, or Arcana."* — *"Each lowers the amount of its respective quantities."* |

Per its quest text, the Geode shelf takes *"a Bookshelf, 7 Calcite, and 1 Budding
Amethyst"* (quest text; JEI has the recipe), and the quest warns: *"Budding Amethyst can
not be collected from Mining, even with Silk Touch. You'll need either a Ritual or Infusion
to get one then!"* — this chapter's infusion route is *Making Budding Amethyst* (below).

**Tomes** narrow the pool another way. **Tomes** (task `minecraft:book`, needs Infusing):
*"Tomes can be Enchanted, like Items, to get certain Enchantments."* Five quests hang off
it: the four pool tomes below, and *Tome of Scrapping* (in "Moving enchantments").

| Verified quest title | Task (one item from) | What its text says, quoted |
|---|---|---|
| **Tool Tomes** | `apothic_enchanting:pickaxe_tome`, `apothic_enchanting:fishing_tome` | *"It will give Efficiency, Fortune, and Silk Touch."* (its Tome of Miners) |
| **Armor Tomes** | `apothic_enchanting:helmet_tome`, `apothic_enchanting:chestplate_tome`, `apothic_enchanting:leggings_tome`, `apothic_enchanting:boots_tome` | *"If you want the best chance for just Protection try the Chestplate Tome!"* |
| **Weapon Tomes** | `apothic_enchanting:weapon_tome`, `apothic_enchanting:bow_tome` | *"Tomes of Weaponry will give Enchantments for Swords and Axes."* |
| **ETC. Tomes** | `apothic_enchanting:other_tome` | *"The rest of the Enchantments come from this Tome."* |

How a tome's enchantments then move onto gear is not in this chapter's text — check the
quest entry and JEI.

## How high each enchantment can go — `config/apotheosis/enchantments.cfg`

The pack ships `config/apotheosis/enchantments.cfg` — its header: *"This file contains
configurable data for each enchantment."* — with one block per enchantment, **117** in
pack 8.2. In the file's own words, each block sets:

- `Max Level` — *"The max level of this enchantment"*, its comment naming the original cap
  (e.g. *"originally 5."* in the `minecraft:sharpness` block);
- `Max Loot Level` — *"The max level of this enchantment available from loot sources."*;
- `Forced Level Cap` — *"The enforced effective max level of this enchantment. Regardless
  of NBT and other buffs, this enchantment will never exceed this level. -1 to disable."*;
- `Max Power Function` / `Min Power Function` — the enchanting-power formulas, left empty
  (the default) for every entry.

What pack 8.2 sets:

- **84 of the 117** entries have a `Max Level` above their original cap, **32** keep it,
  and exactly **one** is lowered: `apothic_enchanting:miners_fervor`, originally 5, set to
  `Max Level` 1 and `Max Loot Level` 1 — the only value in the file that differs from its
  own stated default.
- `Max Loot Level` equals the original cap for every other entry: loot sources stay at the
  original levels, and only `Max Level` is raised.
- `Forced Level Cap` is `-1` (disabled) for every entry.
- The highest `Max Level` in the file is 13, held by twelve entries — eleven Corail
  Tombstone enchantments and `the_bumblezone:neurotoxins`.

Every vanilla (`minecraft:`) entry — 42 — as configured (a raised `Max Level` in bold):

| Enchantment id | Originally | `Max Level` | `Max Loot Level` |
|---|---|---|---|
| `minecraft:aqua_affinity` | 1 | 1 | 1 |
| `minecraft:bane_of_arthropods` | 5 | **10** | 5 |
| `minecraft:binding_curse` | 1 | 1 | 1 |
| `minecraft:blast_protection` | 4 | **9** | 4 |
| `minecraft:breach` | 4 | **8** | 4 |
| `minecraft:channeling` | 1 | 1 | 1 |
| `minecraft:density` | 5 | **10** | 5 |
| `minecraft:depth_strider` | 3 | **7** | 3 |
| `minecraft:efficiency` | 5 | **9** | 5 |
| `minecraft:feather_falling` | 4 | **11** | 4 |
| `minecraft:fire_aspect` | 2 | **5** | 2 |
| `minecraft:fire_protection` | 4 | **9** | 4 |
| `minecraft:flame` | 1 | 1 | 1 |
| `minecraft:fortune` | 3 | **8** | 3 |
| `minecraft:frost_walker` | 2 | **7** | 2 |
| `minecraft:impaling` | 5 | **10** | 5 |
| `minecraft:infinity` | 1 | 1 | 1 |
| `minecraft:knockback` | 2 | **5** | 2 |
| `minecraft:looting` | 3 | **8** | 3 |
| `minecraft:loyalty` | 3 | **9** | 3 |
| `minecraft:luck_of_the_sea` | 3 | **8** | 3 |
| `minecraft:lure` | 3 | **8** | 3 |
| `minecraft:mending` | 1 | 1 | 1 |
| `minecraft:multishot` | 1 | 1 | 1 |
| `minecraft:piercing` | 4 | **8** | 4 |
| `minecraft:power` | 5 | **9** | 5 |
| `minecraft:projectile_protection` | 4 | **11** | 4 |
| `minecraft:protection` | 4 | **8** | 4 |
| `minecraft:punch` | 2 | **5** | 2 |
| `minecraft:quick_charge` | 3 | **5** | 3 |
| `minecraft:respiration` | 3 | **7** | 3 |
| `minecraft:riptide` | 3 | **9** | 3 |
| `minecraft:sharpness` | 5 | **9** | 5 |
| `minecraft:silk_touch` | 1 | 1 | 1 |
| `minecraft:smite` | 5 | **10** | 5 |
| `minecraft:soul_speed` | 3 | **7** | 3 |
| `minecraft:sweeping_edge` | 3 | **8** | 3 |
| `minecraft:swift_sneak` | 3 | **5** | 3 |
| `minecraft:thorns` | 3 | **5** | 3 |
| `minecraft:unbreaking` | 3 | **8** | 3 |
| `minecraft:vanishing_curse` | 1 | 1 | 1 |
| `minecraft:wind_burst` | 3 | **8** | 3 |

Apothic Enchanting's own 20 entries (a changed `Max Level` in bold — the one lowered value
is Miner's Fervor's):

| Enchantment id | Originally | `Max Level` | `Max Loot Level` |
|---|---|---|---|
| `apothic_enchanting:berserkers_fury` | 3 | 3 | 3 |
| `apothic_enchanting:boon_of_the_earth` | 5 | 5 | 5 |
| `apothic_enchanting:chainsaw` | 1 | 1 | 1 |
| `apothic_enchanting:chromatic` | 1 | 1 | 1 |
| `apothic_enchanting:crescendo_of_bolts` | 5 | 5 | 5 |
| `apothic_enchanting:endless_quiver` | 1 | 1 | 1 |
| `apothic_enchanting:growth_serum` | 1 | 1 | 1 |
| `apothic_enchanting:icy_thorns` | 3 | **5** | 3 |
| `apothic_enchanting:infusion` | 1 | 1 | 1 |
| `apothic_enchanting:knowledge_of_the_ages` | 3 | 3 | 3 |
| `apothic_enchanting:life_mending` | 3 | 3 | 3 |
| `apothic_enchanting:miners_fervor` | 5 | **1** | 1 |
| `apothic_enchanting:natures_blessing` | 3 | **7** | 3 |
| `apothic_enchanting:rebounding` | 3 | **5** | 3 |
| `apothic_enchanting:reflective_defenses` | 5 | **7** | 5 |
| `apothic_enchanting:scavenger` | 3 | 3 | 3 |
| `apothic_enchanting:shield_bash` | 4 | **7** | 4 |
| `apothic_enchanting:stable_footing` | 1 | 1 | 1 |
| `apothic_enchanting:tempting` | 1 | 1 | 1 |
| `apothic_enchanting:worker_exploitation` | 1 | 1 | 1 |

One cross-check between config and quest text: `apothic_spawners:capturing` is originally
3 with `Max Level` 7, and the Apothic Spawners chapter's untitled quest whose task is
titled "Capturing Books" says *"the highest level you can normally get is VII (7)."* The other 54 entries
(Corail Tombstone, Twilight Forest, EvilCraft, Ars Nouveau, and more) are in the file.

**What the config does not say** is which Eterna — or which shelves — the table needs
before it offers a given level. That is the pool view's job (the ? button) and JEI's, and
the Enchantment Library's rule applies to books you merge: *"if you only put in Sharpness
III, you can only take out Sharpness III."*

## Keeping and combining books — the two libraries

| Verified quest title | Task item | Needs | What its text says, quoted |
|---|---|---|---|
| **Enchantment Library** | `apothic_enchanting:library` | nothing (a starting point) | *"The Enchantment Library is the single greatest Enchanted Book storage, ever!"*; books are *"held in Points"*: *"Level 1, is 1 Point. Level 2 is 2 Points. Level 3 is 4 Points. Level 4 is 8 Points."*; *"Each Book is stored to a max of 32768 Points"*; *"You can Click different Books to add to the Book in the Orange Slot, similar to combining Books in an Anvil."*; and the catch, *"The max Level of Enchanted Book is determined by the highest Level of Book you've put in."* |
| **Library of Alexandria** — *"Just imagine if Rome never burned..."* | `apothic_enchanting:ender_library` | Enchantment Library, Other Infusion Items, and Ahh, Pinnacle, at last | *"It can hold higher Levels of Enchanted Books, but it will still need the Level of Book to get taken out at that Level."*; *"the Library of Alexandria can hold 1.1 Billion Points of each Book!"*; it is made by infusing the Enchantment Library: *"Use 4 Soul-Touched Sculkshelves, 4 Echoing Sculkshelves, 1 Draconic Endshelf, 5 Geode-Encased Bookshelves of Stability, and a Skeleton Skull."* |

The Enchantment Library's recipe, as its quest text gives it: *"To Craft it you'll need 4
Ender Chests, 1 Enchanting Table, and 4 of any of the Infused Bookshelves: Infused
Hellshelf, Infused Seashelves, and Deepshelves."* — so although the quest has no
dependencies, it is reachable only once you have infused shelves. Quest text; confirm in
JEI.

## Moving enchantments — the scrapping tomes, and disenchanting

| Verified quest title | Subtitle | Task item | Needs |
|---|---|---|---|
| **Tome of Scrapping** | *"Half Enchantments, breaks Items"* | `apothic_enchanting:scrap_tome` | Tomes |
| **Tome of Superior Scrapping** | *"All Enchantments, breaks Item"* | `apothic_enchanting:improved_scrap_tome` | Other Infusion Items, Tome of Scrapping, and The Frontier Calls |
| *(no title in the config)* | *"All Enchantments, doesn't break"* | `apothic_enchanting:extraction_tome` | Other Infusion Items, Tome of Superior Scrapping, and Ascent to 60 |

Quoted: *"By combining an Item with the Tome in an Anvil, we can take half the Enchantments
off the Item."* and *"This will end up breaking and voiding the Item after it is done. I
don't recommend using it, rather you should upgrade it!"* (Tome of Scrapping); the upgrade
infusion suggests *"3 Echoing Sculkshelves and 15 Basic Bookshelves"* — *"Or, if you want
this Tome on Frontier, you can use 8 Crystalline Seashelves."* (Tome of Superior
Scrapping). The untitled quest's text names its item: *"The Tome of Extraction is the Tome
we are looking for! It will take off all Enchantments and leave the Item alone!"* — and
for its infusion, *"We can just use our previous Sculkshelf setup for this."*

The **Tips and Tricks** chapter's **Disenchanting Methods** quest has one task (task title
"Disenchantment Methods") that accepts any of 11 items: the three tomes above,
`minecraft:anvil`, `disenchanting_table:disenchanting_table` (Dis-Enchanting Table 5.0.2),
`draconicevolution:disenchanter`, `industrialforegoing:enchantment_extractor`,
`tombstone:book_of_disenchantment`, `actuallyadditions:lens_of_disenchanting`,
`evilcraft:purifier`, and `evilcraft:blook` — its text describes each method; read it
there.

## XP — *Crafting EXP?*

**Crafting EXP?** (task `minecraft:honey_bottle`, needs Other Infusion Items): *"EXP is
very important for Apotheosis Enchanting! Every Enchant requires it!"* Its infusion route:
*"With Infusion we can transform Honey Bottles into Bottles O' Enchanting."* — *"It goes
from 1 Bottle O' Enchanting, to 8, to 32!"* — with the suggested set-ups *"only 2 Echoing
Sculkshelves"*, *"5 Echoing Sculkshelves and 1 Soul-Touched Sculkshelf"*, and *"5 Echoing
Sculkshelves, 3 Soul-Touched, and 1 Draconic Endshelf"*. The chapter's own reward tables
add up to **311 XP levels** across its quests (config figure).

## The other infusions in this chapter

These make items, not shelves, on the same table. Each quest needs **Other Infusion
Items** (task: `minecraft:lapis_lazuli` ×3 — *"It's not just Bookshelves that can be
Infused!"*) plus the tier quest listed; every window is the quest's own text — confirm in
JEI before building.

| Verified quest title | Task item | Also needs | Window, quoted |
|---|---|---|---|
| **Making a real Trident** | `apothic_enchanting:inert_trident` | The Frontier Calls | *"between 40 Eterna, 20%-50% Quanta, and atleast 35% Arcana"* |
| **Ender Lead** | `apothic_enchanting:ender_lead` | Flimsy Ender Lead, The Frontier Calls | *"at least 45 Eterna, 25% Quanta, and 40% Arcana"* |
| **Making Budding Amethyst** | `minecraft:budding_amethyst` | Ascent to 60 | *"60 Eterna, between 30% and 50% Quanta, and 50% Arcana"* |
| **Infinite Echo Shards?** | `minecraft:echo_shard` | To reach the Summit | *"70 Eterna, 50% Quanta, and 50% Arcana"* |
| **Infusing Spawner Runes** | `apotheosis:infused_spawner_rune` | To reach the Summit | *"at least 70 Eterna, 30% Quanta, and 50% Arcana"* |
| **Occult Ender Lead** — *"Nothing to do with Occultism I swear"* | `apothic_enchanting:occult_ender_lead` | Ender Lead, To reach the Summit | *"at least 75 Eterna, 85% Quanta, and between 60-85% Arcana"* |
| **Unbreakable Charms** | one Apotheosis item from the `curios:charm` tag (task "Permanent Charms") | Ahh, Pinnacle, at last | *"100 Eterna, between 8.5% and 13.5% Quanta, and between 32.5% and 37.5% Arcana"* |

Also on the canvas, outside the enchanting line: **Flimsy Ender Lead**
(`apothic_enchanting:flimsy_ender_lead`, a starting point — *"It can only hold animals, and
breaks after 8 uses."*), and the Apotheosis gem storage pair **Gem Case**
(`apotheosis:gem_case`, a starting point) → **Gem Case of House Fabergé**
(`apotheosis:ender_gem_case`, subtitle *"Gustav Fabergé would be proud"*, needs Gem Case
and Ahh, Pinnacle, at last).

## Where enchanting touches the rest of the book

| Chapter (verified) | Quest (verified title, or marked) | Task item | What its text says, quoted |
|---|---|---|---|
| **Chapter 3: The ATM Star** | **Apothic Mods** (hub) | `minecraft:bookshelf` | *"The Attributes and Enchanting mods are what you'll need to follow to get the ATM Star!"* |
| Chapter 3 | **Infused Dragon's Breath** (feeds Dragon Soul) | `apothic_enchanting:infused_breath` | a *different* set-up from this chapter's quest of the same name: *"You can use 2 Soul-Touched Sculkshelves, 3 Heart-Forged Seashelves, 8 Normal Bookshelves, and 1 Geode-Encased Bookshelf of Stability."* (this chapter suggests 4 Echoing + 4 Soul-Touched Sculkshelves + 6 Geode shelves) |
| Chapter 3 | *(no title in the config)* | `allthetweaks:mini_nether` | *"The main part of the recipe for the Miniature Nether Portal is the Hellshelf of Masterful Sight."* |
| Chapter 3 | *(no title in the config)* | `allthetweaks:mini_end` | *"The Mini End Portal will need quite a few Endshelves."* |
| Chapter 3 | *(no title in the config)* | `allthetweaks:mini_exit` | *"There you'll need Soul-Touched Sculkshelves to Enchant it and to make the Portal."* |
| **Chapter 4: Creative** | **Runic Enchanter** | `modern_industrialization:runic_enchanter` (and its multiblock parts) | *"Enchanting can't be completely automated! And you can't choose which Enchants you want, you have to get Lucky!"* |
| **Apothic Spawners** | *(no title in the config)* — task "Capturing Books" | a `minecraft:enchanted_book` carrying `apothic_spawners:capturing` at level 1–7 | *"It's a rare one so keep looking for one and check out Apothic Enchanting to help."* |
| Apothic Spawners | *(no title in the config)* — subtitle *"That's no Spawn Egg!"* | `apothic_enchanting:occult_ender_lead` | *"Check out the Apothic Enchanting chapter to learn more about how to get this Lead."* |
| Apothic Spawners | *(no title in the config)* — subtitle *"Advanced Modifications"* | `apotheosis:infused_spawner_rune` | *"We'll need at least 70 Eterna, 30% Quanta, and 50% Arcana in an Enchanting Table."* |
| **Tips and Tricks** | **Disenchanting Methods** | one of 11 items (above) | the disenchanting options, one by one |
| **Industrial Foregoing** | *(no title in the config)* | `industrialforegoing:enchantment_factory` | *"The Enchantment Factory is basically an automated Enchanting Table."* — *"it will enchant that item with something random."* |

## Cross-references

- `references/progression.md` — where the Magic stage (this chapter) and the early-game
  Apotheosis Gear and Apothic Spawners chapters sit in the four-stage map.
- `references/key-mods.md` — the Apotheosis family's row: what each part does and when to
  start it.
- `references/boss-checklist.md` — the Wither, the Warden, and the Ender Dragon, which the
  World Tier and Sculkshelf quests require.
- `references/atm-star-checklist.md` — the Apothic Mods hub and *Infused Dragon's Breath*
  → Dragon Soul, plus the mini portals → Dimensional Seed.
- `references/creative-checklist.md` — the Runic Enchanter, Chapter 4's answer to
  enchanting that cannot be automated.

## What this page deliberately does not tell you

- **Recipes.** Only where a quest's own text states one is it quoted, and marked; JEI has
  the real recipe, and recipes are where pack versions differ most.
- **Formulas.** Which Eterna gives which enchantment level, how Quanta and Arcana weight a
  roll, and the exact window of an infusion are not in the config. Use the table's ? pool
  view, JEI, and the quest entries; every figure quoted here is approximate until the book
  confirms it.
- **A tier list of enchantments.** "Best" depends on the gear; the config only says how
  high each one can go, and this page does not rank them.
- **An order the book does not have.** The spine is dependency order, not a mandated
  sequence; the Hellshelf/Seashelf split is the pack's own either-or. Anything beyond the
  verified dependency order is *approximate*.
- **Reward tables.** Except where they explain a quest (the shelf top-ups, the XP total),
  rewards are in the book.
- **Anything not in the config.** If a player names an enchantment level, shelf, or
  set-up that is not listed here, the answer is "open that quest in the book / look it up
  in JEI" — never a guess.
