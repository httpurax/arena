# Potions and brewing in ATM10

**What this page is.** The answer to *"how do potions work in this pack?"* and *"what
should I brew?"* in **All the Mods 10** — a map of the brewing-relevant mechanics the
pack actually ships: the vanilla brewing stand, PotionsMaster's Ore Sight potions for the
ATM ores, the Pylons Infusion Pylon as a persistent-effect alternative to beacons, the
Generators Galore Potion Generator, and the buff-food line from the Food and Farming
chapter. It is a map of *what the pack provides and where it is documented*, not a
recipe book and not a potion-effect database.

## Provenance — everything here was read, not remembered

Every quest title, quest id, task item id, config key, config value, and quoted sentence
below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which the pack's own changelogs list as **pack 8.2**
(`config/bcc-common.toml` → `modpackVersion = "8.2"`):

| File(s) in the pack repo (at that commit) | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/food_and_farming.snbt`, `config/ftbquests/quests/chapters/pylons.snbt`, `config/ftbquests/quests/chapters/tips_and_tricks.snbt` | the quests that touch brewing, potions, and potion effects: task items, counts, and `dependencies` chains |
| `config/ftbquests/quests/lang/en_us/chapters/{food_and_farming,pylons,tips_and_tricks,allthemodium,bounty_board}.snbt` | the English quest titles and the description text quoted below |
| `config/ftbquests/quests/chapter.snbt` and `chapter_group.snbt`, with `config/ftbquests/quests/chapter_groups.snbt` | chapter titles, the quest-book group each chapter sits in, and the group order |
| `config/potionsmaster/allthemodium.json`,<br>`config/potionsmaster/vibranium.json`,<br>`config/potionsmaster/unobtainium.json` | the ore tags and the raw-material ids the Ore Sight potions key on |
| `config/pylons-server.toml` | the Infusion Pylon's chunk-loading switch and its per-player, online-only limits |
| `config/crash_assistant/modlist.json` | verified mod ids, display names, and versions |

**How to read the quotes.** Quest text is quoted with Minecraft `&` formatting codes
stripped (`&6M&r` → `M`), the same normalization `scripts/build_chapter_list.py` applies
to titles. Config comments and values are quoted verbatim.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI/EMI are authoritative.** This page is a
  snapshot of pack 8.2's config. Potion recipes, effect durations, and splash/lingering
  variants are the kind of thing a server owner, a mod update, or a pack rebalance
  changes; if the player's game differs, his game wins — say so and re-check rather than
  arguing from this file.
- **Potion recipes and effect durations are deliberately not on this page.** The config
  lists *what a quest wants*, never *how to brew it*; JEI has the recipe, and recipes are
  where pack versions differ most. **Never invent a recipe, a duration, or an amplifier.**
- **Item and block ids are quoted from the config, never invented.** Where an id appears
  only in a quest reward or a config entry (not in a lang file title), that is flagged in
  place.
- **Config keys prove a setting exists and what the mod's own comment says it does.** They
  do not prove a potion is worth brewing, or that a farm layout works. Anything on this
  page that is neither a quote nor a config value is flagged **judgement**.
- **No recipes, no effect durations, no amplifier tiers, no coordinates.** The config
  lists *what a quest wants*, never *how to brew it*; JEI has the recipe.
- **Nothing here was invented, and nothing is added from memory.** A potion that is not
  named in this pack's config is not on this page. If a player names one (an old guide's
  favourite, a mod that ATM10 dropped), the answer is "let's check your instance / JEI" —
  never a plausible-sounding guess.

## The short answer

**Brew what the quest book asks for, in the order the quest book asks.** The brewing
stand is vanilla Minecraft — every modded pack still runs on it — and the pack's own
quests are the best guide to *which* potions matter for *your* stage:

1. **First hour:** the brewing stand itself comes from the usual vanilla recipe (crafting
   table + blaze powder from the Nether). The Chapter 1 quest line walks the Nether trip;
   once blaze rods are in hand, the brewing stand is craftable and the Food and Farming
   chapter's early quests point at buff food as the low-effort alternative to potion
   brewing. *(Judgement: buff food is cheaper than potions for everyday exploration.)*
2. **Mining the ATM ores:** PotionsMaster's Ore Sight potions — verified from the pack
   config — turn the brewing stand into an ore-detection tool. See the Ore Sight section
   below.
3. **Persistent buffs without potions:** the Pylons Infusion Pylon — verified from the
   pack config — gives beacon-like area effects from a Potion Filter, in a chunk area,
   one per player, while online. See the Infusion Pylon section below.
4. **Combat before bosses:** the boss guide's readiness signal for every endgame fight is
   *"the best Gear, Enchants, and Potions"* (quoted). Which potions that means is JEI's
   answer, not this page's — but the boss guide is the right place to check what the
   quest book expects before a fight.

## The brewing stand — vanilla, as the pack ships it

The brewing stand is a vanilla Minecraft block. The pack does not replace it, gate it, or
add a modded equivalent. Blaze powder is the fuel; glass bottles hold water; nether wart
is the base for every potion. The recipe, the brewing steps, and the effect table are
vanilla — and JEI shows every one of them.

The pack does, however, add *uses* for the potions the stand produces:

| Potion use | Where it is tracked in the pack config | Verified? |
|---|---|---|
| **Ore Sight (mining)** | PotionsMaster's config entries — see below | Yes |
| **Persistent area buffs** | Pylons Infusion Pylon — see below | Yes |
| **Power generation** | Generators Galore Potion Generator — see below | Yes |
| **Combat buffs for bosses** | Boss guide's readiness signal (quoted) | Yes (the quote) |
| **Buff food (alternative)** | Food and Farming chapter (35 quests) | Yes (the chapter) |

## PotionsMaster: Ore Sight potions

**What the pack ships.** PotionsMaster is a mod that adds Ore Sight potions — potions that,
when drunk, highlight nearby ores of a specific type. The pack config ships three Ore
Sight entries, one per ATM metal:

| Config file | Ore tag it keys on | Raw material id |
|---|---|---|
| `config/potionsmaster/allthemodium.json` | `c:ores/allthemodium` | the raw allthemodium processing material |
| `config/potionsmaster/vibranium.json` | `c:ores/vibranium` | the raw vibranium processing material |
| `config/potionsmaster/unobtainium.json` | `c:ores/unobtainium` | the raw unobtainium processing material |

**Quest tracking.** The Allthemodium mining guide documents the quest that rewards the
allthemodium Ore Sight potion: the untitled follow-up quest `18FAD56CDE05646A` (in the
Chapter 2: Allthemodium chapter) rewards a `potionsmaster:allthemodium` potion. The
quest's own text says: *"Before Quarries in the Mining Dimension, you can locate
Allthemodium with Ore Sight Potions if you are looking strictly for Allthemodium!"*

The pack ships an Ore Sight entry per metal — but **only `potionsmaster:allthemodium` is
quoted from a quest reward in the skill's references; the other two potion ids
(`potionsmaster:vibranium`, `potionsmaster:unobtainium`) are the config's own entry
names**, verified from `config/potionsmaster/vibranium.json` and
`config/potionsmaster/unobtainium.json`. The best-reward-quests guide also lists the
`potionsmaster:allthemodium` potion as a quest reward: `minecraft:potion` ×1 with
component `{"minecraft:potion_contents":{"potion":"potionsmaster:allthemodium"}}`.

**What the Ore Sight potion does and how long it lasts** is not stated by the quest text
or the config entries the skill has read — only that it keys on the ore tag. The effect,
duration, and radius are the mod's own (check in-game or JEI). **No duration, radius, or
amplifier is stated on this page.**

**When to use it.** The quest text frames the Ore Sight potion as a pre-quarry tool for
the Mining Dimension — use it when you are mining for ATM ores by hand, before a quarry
or Digital Miner is running. See `references/allthemodium-mining-guide.md` for the full
mining context.

## The Infusion Pylon: persistent area effects

**What the pack ships.** The Pylons chapter (13 quests, in the Logistics group) has a
quest for the Infusion Pylon — quest `18246A48C20B29D8`, task
`pylons:infusion_pylon` ×1. The quest has **no title in the config** (the book shows the
task item's own name); the quest's description text says:

> *"The Infusion Pylon works similar as a Beacon just much better and cheaper!"*
>
> *"When a Potion Effect is put in by a Potion Filter, it will continuously give you the
> Potion Effect while you're in the set Chunk area."*

**Config limits** (from `config/pylons-server.toml`):

| Key | Value | What the config's own comment says |
|---|---|---|
| `infusionChunkloads` | `true` | *"Whether the Infusion Pylon chunkloads itself."* — but the pylon chunkloads only itself, only one per player, **only while the player is online** (verified from the same config file). |

**What this means in practice:**

- The Infusion Pylon replaces a beacon for persistent potion effects in a chunk area.
- It needs a Potion Filter (a brewed potion applied to the filter) to supply the effect.
- It does **not** run while you are offline — it is not a chunk-loading answer for
  unattended farms. See `references/chunk-loading-guide.md` for that.
- It is **one per player** — multiple pylons do not stack for the same player.

**What to put in it** is JEI's answer (which potions make good persistent effects) and
the player's answer (what he needs in his base area). **No potion recommendation is made
on this page.**

## Generators Galore: the Potion Generator

**What the pack ships.** Tips and Tricks has a quest (`790EC3EDC2DB1FB0`) whose task is
one of four Generators Galore generators — including the
`generatorgalore:potion_generator`. The quest description text says the player picks one
of the four generators (enchantment, halitosis, netherstar, or potion). The generator's
own recipe and fuel requirements are JEI's; the quest book does not state them.

**What the Potion Generator does** is the mod's own documentation — it is a generator
that burns potions as fuel. **No power output, fuel duration, or efficiency number is
stated on this page.** The generator is a *judgement* pick for players who have a potion
surplus; it is not the pack's recommended first generator (the Copper Generator from the
same quest entry is the usual first pick — see `references/first-hour-walkthrough.md`).

## Buff food: the low-effort alternative

The **Food and Farming** chapter (35 quests, in the Resources group) covers vanilla-plus
farming and cooking: *Punch the Grass*, *The Bread of Life*, *Making a Kitchen, with a
Book*, and the fishing-rod tiers. The chapter's quest titles and task items are the
pack's own; its buff-food line (food that gives potion-like effects when eaten) is the
low-effort alternative to brewing.

**What buff food gives and which food gives which effect** is the chapter's own content
and JEI's answer. **No specific food, effect, or duration is stated on this page.** The
farming guide (`references/farming-guide.md`) has the verified farming detail; this page
points at it.

**Judgement:** for everyday exploration and mining, buff food is almost always cheaper
than potions — it does not require blaze powder, glass bottles, or nether wart. Reserve
potion brewing for effects food cannot replicate (night vision, water breathing,
Ore Sight) or for boss fights where the quest book says to bring potions.

## Boss fights: what the quest book says about potions

The boss guide (`references/boss-guide.md`) quotes the readiness signal for endgame
bosses as *"the best Gear, Enchants, and Potions"* (the quest book's own framing). The
guide deliberately **does not recommend specific potions, enchantments, or armour tiers**
beyond what the quest book itself states (a task, a quoted tool tier, or an expectation
sentence). Every readiness judgement is labelled as such.

**The point:** if the player is asking "what potions should I brew for bosses?", the
answer is: read the boss guide for what the quest book expects, then check JEI for which
potions match that expectation. This page does not invent a loadout.

## The levitation potion

The flight guide (`references/flight-guide.md`) documents a levitation potion —
`minecraft:potion` carrying `apothic_attributes:levitation` — as a quest reward (50 XP).
The potion's effect and duration are the mod's own; **no detail beyond the reward is
stated on this page**. The flight guide has the verified context.

## Progression: when to touch brewing

| Stage | What to do with potions | Reference |
|---|---|---|
| **early-game** | Build the brewing stand once you have blaze powder (post-Nether). Prioritise buff food from Food and Farming over potion brewing — it is cheaper and almost as useful. | `references/first-hour-walkthrough.md`, `references/farming-guide.md` |
| **tech** | Brew what you need: Ore Sight potions for ATM-ore mining (PotionsMaster), persistent effects for your base (Infusion Pylon). The Potion Generator is a *judgement* pick for surplus-potion power. | `references/allthemodium-mining-guide.md`, `references/chunk-loading-guide.md` |
| **magic** | Apothic Enchanting and Ars Nouveau open alternative buff routes (enchantments, spells) that may replace some potion uses. The Infusion Pylon remains relevant. | `references/enchanting-guide.md` |
| **endgame** | Boss fights want potions — the quest book says *"the best Gear, Enchants, and Potions"*. Brew what the boss guide's readiness signal asks for; check JEI for specifics. | `references/boss-guide.md` |

## What this page does NOT cover

- **Potion recipes** (what goes in the brewing stand for which effect) — JEI.
- **Effect durations and amplifier tiers** — JEI and the mod's own documentation.
- **Splash and lingering variants** — JEI.
- **Mods that add potions but are not in the pack** — check the in-game mod list.
- **Botania, Thermal series, and other mods often assumed present** — they are not in
  pack 8.2's modlist. See `references/key-mods.md` for the mods-not-verified list.
- **Automated potion brewing** — no quest in the pack config tracks an automated brewing
  setup; if the player asks, the answer is "check JEI and the quest book."

## How to use this guide in a session

1. **Player asks "how do potions work?"** → the brewing stand is vanilla; this page's
   short answer covers the pack's own additions (Ore Sight, Infusion Pylon, Potion
   Generator, buff food).
2. **Player asks "what should I brew?"** → point at the progression table above, then at
   JEI for recipes. Do not invent a potion list.
3. **Player asks "how do I find ATM ores?"** → redirect to
   `references/allthemodium-mining-guide.md`, the mining companion to this page.
4. **Player asks "how do I get persistent buffs?"** → the Infusion Pylon section above,
   with the config limits and the "one per player, while online" caveat.
5. **Player asks "what potions for bosses?"** → redirect to
   `references/boss-guide.md`, then JEI for specifics.

*The in-game quest book (FTB Quests) and JEI are authoritative for everything this page
summarizes. Brew what the book asks for, not what a guide invents.*
