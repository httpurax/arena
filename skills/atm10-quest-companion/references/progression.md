# ATM10 progression: the stages, in quest-book order

All the Mods 10 (ATM10) is a kitchen-sink pack for **Minecraft 1.21.1 on NeoForge** with
roughly **450–500 mods**. Its FTB Quests book is the backbone of progression: at the time
of writing (pack 8.x, checked against the official
[AllTheMods/ATM-10 quest config](https://github.com/AllTheMods/ATM-10/tree/main/config/ftbquests/quests))
it contains **66 chapters and ~4,790 quests**, organized into 4 standalone chapters plus
10 chapter groups.

## Grounding rule (read this first)

Everything below describes the pack's *structure* — which chapters exist, how they are
grouped and ordered, and roughly when players reach them. **The in-game quest book (FTB
Quests) and JEI are the only authoritative sources for what a specific quest requires and
what a specific recipe contains.** ATM10 is updated frequently; quest requirements, item
ids, and recipes change between versions. Where this document is unsure it says so
explicitly ("approximate", "varies by version"). Never present a detail from here as an
exact in-game requirement — point the player at the quest book entry or a JEI lookup
instead.

One design fact straight from the pack's own Welcome chapter: *"In this modpack, quests
are optional. Mods are not gated behind completing any quests!"* The quest book is a guide
and a reward dispenser, not a hard gate (the notable exception is the ATM Star endgame,
whose chapter tracks components that are genuinely required for the star).

## The quest book layout

Chapter groups in the order the book shows them (from `chapter_groups.snbt`):

1. **Main Questline** — Chapter 1: The Beginning → Chapter 2: Allthemodium →
   Chapter 3: The ATM Star → Chapter 4: Creative
2. **Tools and Gear** — Apotheosis Gear, Artifacts, Basic Armor, Basic Tools,
   Mahou Tsukai, Relics, Silent Gear
3. **Storage** — Basic Storage, Applied Energistics 2, Extended & Advanced AE,
   Refined Storage
4. **Logistics** — Basic Logistics, Integrated Dynamics, Modular Routers, Pylons
5. **Resources** — Apothic Spawners, Food and Farming, Hostile Neural Networks,
   Mystical Agriculture, Productive Bees, Productive Trees
6. **Tech** — Create, Draconic Evolution, Immersive Engineering, Industrial Foregoing,
   Just Dire Things, Mekanism, Mekanism: Reactors, Oritech, XyCraft, PneumaticCraft,
   RailCraft
7. **Modern Industrialization** — Steam Age → Electric Age → Digital Age → End Game
8. **Power** — Basic Power, Extreme Reactors, Generators N Furnaces, Powah
9. **Magic** — Apothic Enchanting, Ars Nouveau, EvilCraft, Forbidden & Arcanus,
   Iron's Spells 'n Spellbooks, Nature's Aura, Neo Vitae, Occultism, Theurgy
10. **Exploration** — The Aether, The Bumblezone, Auroral, Cataclysm, Deeper and Darker,
    Eternal Starlight, Ice and Fire, The Twilight Forest, The Undergarden

Plus 4 standalone chapters shown outside the groups: **Welcome, Bounty Board, Building
Tips, Tips and Tricks**. The Bounty Board chapter's 50 kill bounties — what each rung or
boss asks for and what the book pays — are checklisted in
`references/bounty-board-checklist.md`.

`examples/progress.example.json` ships all 66 chapters in that quest-book order
(standalone chapters first, then group by group, ordered by each chapter's
`order_index`), each tagged with one of the four progression stages below.

## The four progression stages

The stages are a *coarse map of when you typically touch things*, distilled from the
quest-book layout above and published ATM10 guides (GPORTAL wiki, all-themods.com,
community playthroughs). The pack itself does not label chapters with these stages, and
the boundaries are approximate — players overlap stages heavily and the pack explicitly
lets you play in any order.

### Stage 1 — Early game (foundations)

**Tracked chapters:** Welcome, Bounty Board, Building Tips, Tips and Tricks,
Chapter 1: The Beginning, and the "Basic" chapters — Basic Tools, Basic Armor,
Silent Gear, Apotheosis Gear, Artifacts, Relics, Basic Power, Basic Storage,
Basic Logistics, Food and Farming, Apothic Spawners.

**What it covers.** Vanilla-shaped bootstrapping with modded quality-of-life on top. The
Main Questline's Chapter 1 (quest titles observed in the pack config: *Stone Age, Our
First Pick, The Metal Age, An Iron Pick, We've Struck Diamonds!, Netherite Tier, To The
Nether!, The End, Summoning The Wither, Kill The Wither, Visit The Deep Dark!, Kill The
Warden, Wind Power, Solar Power, Lava Power, Basic Ore Doubling*) walks the vanilla arc
from wood to Netherite, into the Nether and the End, and ends with early boss kills and
first power/ore-doubling setups.

**What it unlocks.** Decent tools and armor (Silent Gear is the pack's modular tool
system), first machines and power gen, first storage upgrade past wooden chests, and the
habit of following the quest book for rewards. Guides consistently highlight early
quality-of-life wins here — vein-mining keybind, Waystones from village loot, an
Osmium Paxel from Mekanism, a Time in a Bottle (exact availability varies by version;
check JEI).

**Player's typical "what next" question here:** "I have iron/diamonds and a few machines —
which big mod do I commit to?" Answer: pick **one** tech path and **one** magic path (see
Stage 2/3) rather than sampling all 450+ mods.

### Stage 2 — Tech (and resource automation)

**Tracked chapters:** the Tech group (Create, Mekanism, Mekanism: Reactors, Immersive
Engineering, Industrial Foregoing, Just Dire Things, Oritech, XyCraft, PneumaticCraft,
RailCraft), Modern Industrialization (Steam → Electric → Digital → End Game),
Power (Powah, Extreme Reactors, Generators N Furnaces), Storage (Applied Energistics 2,
Extended & Advanced AE, Refined Storage), Logistics (Integrated Dynamics, Modular
Routers, Pylons), and the resource factories — Mystical Agriculture, Productive Bees,
Productive Trees, Hostile Neural Networks.

**What it covers.** The mid-game bulk of the pack: ore processing and multiplication
(Mekanism's chain is the canonical example), mechanical automation (Create), applied
digital storage (AE2 or Refined Storage — pick one), item/energy routing (Integrated
Dynamics, Modular Routers, Pylons), and scalable power (Powah, Extreme Reactors,
Mekanism reactors). Resource mods belong here because they *are* tech progression in a
kitchen-sink: Mystical Agriculture grows ores, Productive Bees and Hostile Neural
Networks automate mob/loot drops, and everything feeds the endgame's enormous material
costs.

**What it unlocks.** Near-infinite base resources, a real storage network, flight-capable
gear and big power plants — the prerequisites for the Main Questline's late chapters.
Community guides converge on the same advice: a full AE2 network, Mystical Agriculture
farms (with growth pylons/accelerators), and one serious power setup carry almost
everything else.

**Where players get stuck:** choosing between overlapping mods. The standard answer —
they are alternatives, not sequence: AE2 *or* Refined Storage; Mekanism *or* Create *or*
Modern Industrialization *or* Immersive Engineering as the primary tech line (though the
ATM Star eventually wants products from many of them).

### Stage 3 — Magic

**Tracked chapters:** the Magic group (Apothic Enchanting, Ars Nouveau, EvilCraft,
Forbidden & Arcanus, Iron's Spells 'n Spellbooks, Nature's Aura, Neo Vitae, Occultism,
Theurgy) plus Mahou Tsukai (booked under Tools and Gear but a magic mod).

**What it covers.** Spellcasting and enchanting (Ars Nouveau's glyph system, Iron's
Spells' spellbooks), summoning and dimensional storage (Occultism), blood/void mechanics
(EvilCraft), ritual enchanting (Apothic Enchanting), and the smaller magic lines
(Nature's Aura, Theurgy, Neo Vitae, Forbidden & Arcanus, Mahou Tsukai). Magic runs in
parallel with tech — the guides treat "one tech mod + one magic mod" as the sane pairing,
and the ATM Star chapter wants outputs from several magic mods.

**What it unlocks.** Flight, powerful gear enchants, automated rituals, and several
endgame-star components (e.g. Ars Nouveau and Occultism items appear among the ATM Star
chapter's quest titles). Ritual details and recipe ingredients are exactly where this
document must stay silent: read the quest entry and JEI, and each mod's own in-game guide
book (Patchouli/Modonomicon entries).

### Stage 4 — Endgame (Main Questline chapters 2–4, dimensions, bosses, the ATM Star)

**Tracked chapters:** Chapter 2: Allthemodium, Chapter 3: The ATM Star,
Chapter 4: Creative, Draconic Evolution, and the Exploration group (The Aether, The
Bumblezone, Auroral, Cataclysm, Deeper and Darker, Eternal Starlight, Ice and Fire, The
Twilight Forest, The Undergarden).

**What it covers.** The pack's defined endgame goal is crafting the **ATM Star**
(`allthetweaks:atm_star` — it is literally the quest book's icon). The Main Questline
walks it in three movements, all verified from the chapter quest titles:

- **Chapter 2: Allthemodium** — the three pack-exclusive super-metals: *Allthemodium*
  (Overworld deepslate levels; guides say Deep Dark, below roughly Y -40 — approximate,
  verify in-game), *Vibranium* (Nether), *Unobtainium* (End), plus their alloys, tools,
  armor sets, the Teleport Pad, the Mining Dimension, and the Piglich boss fight.
- **Chapter 3: The ATM Star** — 128 quests in pack 8.2, one component per major mod
  system. Observed quest titles include items from Mekanism, AE2, Create, Ars Nouveau,
  Occultism, EvilCraft, Iron's Spells, Forbidden & Arcanus, Productive Bees/Trees,
  Mystical Agriculture (Creative Essence), Industrial Foregoing, PneumaticCraft, Extreme
  Reactors, Draconic Evolution, Modern Industrialization, Oritech, Twilight Forest, Deeper
  and Darker and more. This chapter is the pack's "checklist of everything you built" —
  `references/atm-star-checklist.md` breaks it down by source mod, with the build order and
  the parts the pack marks optional.
- **Chapter 4: Creative** — post-star content: 38 quests in pack 8.2 that automate the
  star (the Runic Star Altar and its sibling multiblocks, the bees/Star Shards, the five
  star parts) and then spend it on creative-tier items (Creative Energy Cube, Creative
  Jetpack, Creative Spellbook, ...) behind the chapter's *Fully Automated ATM Star* quest.
  Requirements here are version-sensitive; treat every number as approximate and read the
  quests. `references/creative-checklist.md` maps the whole chapter, in dependency order.

The **Exploration** chapters are tracked in this stage because the dimensions and their
bosses (Twilight Forest's progression bosses, L'Ender's Cataclysm fights, Aether,
Undergarden, Eternal Starlight, ...) gate late-game materials and several star
components — though in practice many of them (Bumblezone, Twilight Forest) are quite
doable mid-game. The stage boundary is fuzzy here by design; say so when advising.
`references/boss-checklist.md` maps each of those bosses to its dimension, its arena, and
roughly when in the progression it lands.

## Using this document in a session

1. Ask where the player is: which Main Questline chapter, which big mods are built, what
   they are stuck on.
2. Map that to a stage above, then to the specific quest-book chapters that apply.
3. Recommend the next steps *in quest-book order within the relevant chapters*, and for
   any concrete requirement (counts, ingredients, boss mechanics) tell the player to read
   the quest entry / JEI — do not state numbers from memory or from this file. For
   endgame questions, work from `references/atm-star-checklist.md` (star components by
   source mod), `references/boss-checklist.md` (boss, dimension, arena, roughly when), and
   `references/creative-checklist.md` (what Chapter 4 asks for after the star, and what
   each creative item does); all three quote verified quest titles and still defer to the
   in-game book.
4. When a chapter is finished, record it in `data/progress.json` and run
   `scripts/progress.py` to show what is next.
