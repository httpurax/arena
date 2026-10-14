# Boss guide: fight order, arenas, and the gear the book expects

**What this page is.** The tactics-and-order companion to `references/boss-checklist.md`
for **All the Mods 10**. The checklist is the inventory — every boss the quest book
tracks, with its dimension and arena. This page answers the next questions: *in what
order do I fight them, where exactly is the arena, what do I have to bring or build to
start the fight, and what gear does the quest book itself expect at that step?* Where
the checklist deliberately stops (it states *No tactics, no gear lists*), this page
adds only what the pack config states — a dependency link, a summoning task, a tool
tier named in quest text — plus readiness advice that is labelled **judgement** every
time. For the dimensions themselves see `references/dimension-guide.md`; for what the
ATM Star needs see `references/atm-star-checklist.md`.

## Provenance — everything here was read, not remembered

Every quest title, quest id, task, dependency link, and quoted sentence below comes
from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `CHANGELOG.md` lists as **pack 8.2** — the "8.x" that
`examples/progress.example.json` is stamped with:

| File(s) in the pack repo (at that commit) | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/*.snbt` | the boss quests' task types (`kill` with an entity id, `item` trophies and summoning items, `structure`, `dimension`, `biome`, `advancement`, `observation`) and their `dependencies` links |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, and the description text quoted below (Minecraft formatting codes stripped) |
| `config/crash_assistant/modlist.json` | verified mod display names and versions |
| `config/bcc-common.toml` | `modpackVersion = "8.2"` |

**How the list was built.** All 66 chapter files (4,790 quests) were scanned: there
are 213 `kill` tasks, 81 `structure` tasks, 28 `dimension` tasks and 54 `advancement`
tasks in the whole book. The headline fights below are the boss-grade subset the
checklist already inventories — a named boss quest with an arena, a summoning gate,
or a star link — read in full in these chapters: Chapter 1: The Beginning
(`mainquestline_part_1`, 36 quests), Bounty Board (`bounty_board`, 50 quests), The
Twilight Forest (`twilight_forest`, 56 quests), The Aether (`aether`, 73 quests),
Cataclysm (`cataclysm`, 110 quests), Deeper and Darker (`deeper_and_darker`, 45
quests), The Undergarden (`undergarden`, 82 quests), Eternal Starlight
(`eternal_starlight`, 193 quests), Chapter 2: Allthemodium (`allthemodium`, 54
quests), Draconic Evolution (`draconic_evolution`, 140 quests), Iron's Spells 'n
Spellbooks (`iron_spells_and_spellbooks`, 103 quests), Ars Nouveau (`ars_nouveau`,
130 quests), Ice and Fire (`ice__fire`, 87 quests), Chapter 3: The ATM Star
(`chapter_2_the_star`, 128 quests), and Basic Armor (`basic_armor`, 128 quests).
Ordinary mob kills stay in the checklist and in
`references/bounty-board-checklist.md`; they are not repeated here.

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative.** This page is a
  snapshot of pack 8.2's config. If the player's book differs, his book wins — say so
  and re-research rather than arguing from this file.
- **Titles and ids are the config's, quoted.** A boss the book tracks by a trophy or
  heart item is never rewritten as a `kill` quest here, and a fight the book tracks
  by `advancement` is never rewritten as a `kill` task. Where two chapters reuse one
  title (the book does this a lot), the chapter and quest id disambiguate.
- **"Hearts" figures are quest text, quoted.** They are the quest author's numbers
  in this pack version, flagged as *quest text* — never a verified mechanic, and
  never a difficulty ranking by themselves.
- **Tactics are quoted or labelled.** A tactic below is either a sentence from that
  quest's own description (quoted, marked *quest text*) or marked *(judgement)*.
  Nothing else is presented as a fight mechanic. Full attack lists, phases beyond
  the quoted lines, immunities, and drop tables belong to the quest entry, the mod's
  own in-game guide book, and JEI.
- **Order is verified only where a dependency link or quest sentence states it.**
  Everything else — which parallel line to visit first, when the player is "ready" —
  is a recommendation and is marked *(judgement)* or *approximate*. The pack itself
  gates nothing: the Welcome chapter states *"In this modpack, quests are optional.
  Mods are not gated behind completing any quests!"*
- **Gear means what the book states, not a loadout.** See the next-but-one section:
  a summoning task, a tool tier named in quest text, or an explicit sentence such
  as *"probably some pretty good armor"* is **verified**; an armour tier suggested
  from the stage of the game is *(judgement)*. Never invent an enchantment, a
  weapon, or a protection level the config does not name.
- **No coordinates, no recipes.** Arenas are named the way the config names them —
  a dimension, a `structure` id, or the place name in quest text. The one location
  hint the config itself prints in numbers (the Chaos Islands) is quoted as quest
  text and never extended. How to craft a summoning item is JEI's answer.
- **Nothing here was invented, and nothing is added from memory.** Never invent a
  boss, an arena, a dimension id, or a count: a boss that is not in the config is
  not on this page, and if a player names one, the answer is "let's check your
  quest book / JEI" — never a plausible-sounding guess.

## The short answer: fight them in this order

1. **Vanilla first** *(book branches verified; the order between the branches is
   judgement)*: the Ender Dragon, the Wither, then the Warden. Chapter 1 routes all
   three off the Nether and never orders them against each other.
2. **The Twilight Forest line, strictly in its own order** (**verified**): Naga →
   Twilight Lich → Minoshroom → Hydra → Knight Phantoms → Ur-Ghast → Alpha Yeti →
   Snow Queen. Chapter 3's hub quest states the rule: *"Here you'll need to follow
   a strict order of Bosses to kill and progress!"*
3. **The Aether's three dungeons, in any order** (**verified** parallel): Slider,
   Valkyrie Queen, Sun Spirit each hang directly off the dimension quest.
4. **Mid-game exploration, in any order** *(judgement)*: the Forgotten Guardian,
   Eternal Starlight's two bosses (the Gatekeeper duel is skippable after the Ender
   Dragon — **verified** quest text), the Dead King, and the Wilden Chimera.
5. **The Other, once Chapter 2's Teleport Pad exists** (**verified** gate): the
   Piglich, and Ice and Fire's dragons and mythic beasts framed as The Other's
   content.
6. **Cataclysm's eight last, in any order the player likes**: the chapter hub
   states *"There is no certain pattern of which bosses to kill first, but some
   are stronger than others, and some give loot that will help against the
   others."* The Chaos Guardian closes the list — its crystal stage is the one
   fight whose quest text asks for a Draconic weapon first (quoted below).

That order is a recommendation built on the pack-8.2 config. Only steps 2, the
gates in 5, and the quoted skips are pack-stated; the rest is judgement, and the
player's book and interests override it whenever they differ.

## How to read "the gear the book expects"

The book almost never requires armour for a boss. What it does state falls into
three kinds, and this page never upgrades one kind into another:

- **A task gate (verified).** The fight cannot be tracked — and in the quest text
  cannot be started — without an item the config names: skulls for the Wither,
  medals for the Valkyrie Queen, ashes, a star, a necklace, a key, a sacrifice, a
  fire source for the Lunar Monstrosity. These are listed per boss below with
  their quest ids and counts exactly as the config states them.
- **A tool tier named in quest text (verified quote).** Examples: the Slider
  needs a pickaxe (*"you'll need a Pickaxe to deal Damage"*; *"The better the
  Pickaxe the more Damage."*), Allthemodium needs *"a Pickaxe that is Netherite
  Tier or higher"*, and the Stage 4-5 dragon text demands *"the best Gear,
  Enchants, and Potions."* Quoted means quoted — the page does not turn "best
  Gear" into a shopping list.
- **An explicit expectation sentence (verified quote).** Chapter 1's *Gearing Up*
  (`2EC9668ED4EA47CB`) is satisfied by one diamond piece but its text recommends
  more: *"This quest only requires you to make one Diamond tool or armor piece,
  but it's probably good to get a full set!"* The Wither summoning quest asks for
  *"probably some pretty good armor"*. Chapter 2's hub (`4B2146C9527C54E7`)
  states the pack's own baseline for everything after it: *"By now you should
  have Netherite and have killed all the bosses Minecraft has."*

The armour ladder those sentences refer to is tracked in Basic Armor
(`basic_armor`, 128 quests) as five separate quests with no dependencies between
them in the config — *Diamond Armor* (`5DDC15AAFD2CAF47`), *Netherite Armor*
(`074EC1E636CD6605`), *Allthemodium Armor* (`6C5F9D0D447EFB9C`), *Vibranium Armor*
(`72DDA413D73E3235`), *Unobtainium Armor* (`6F76DA3BBAE8337B`) — whose descriptions
chain the crafting prerequisites in words (Netherite to craft Allthemodium,
Allthemodium Armor to create Vibranium, Vibranium Armor to make Unobtainium;
see `references/armor-tools-ladder.md`). Chapter 1 mirrors the first two steps as
*Gearing Up* → *Netherite Tier* (`0F026D5A17CCCF51`). When this page says a later
fight "expects Netherite-or-better" *(judgement)*, it means that ladder position
read off the chapter's place in the book — not a lock the config enforces.

## The fight order at a glance

Headline fights in the recommended order. "Tracked by" is the verified quest that
records the fight (quest id in backticks); "Arena" is the config's `structure` id
or, where the book gives no structure task, the place named in quest text;
"Hearts" is quoted quest text only, and *—* means the tracking quest states no
figure. The Cataclysm block is ordered by its quoted Hearts figure as a
*(judgement)* starting point — the chapter itself imposes no order.

| # | Boss — tracked by (chapter) | Arena (dimension · structure / place) | Summon / entry (verified) | Hearts (quest text) | Star? |
|---|---|---|---|---|---|
| 1 | Ender Dragon — *Kill The Ender Dragon* (`728BE1816DA23DC0`, Bounty Board) | The End · End Island (quest text) | *Finding The End* (`61C49BC2B384FB80`) → *The End* (`6EE5BE5693E8ACE4`) | 200 | via data model, simulated |
| 2 | Wither — *Kill The Wither* (`69A517AB8A801939`, Chapter 1) | summoned (quest text: not near your base) | *Summoning The Wither* (`4A4C71C43519D5FE`): `minecraft:wither_skeleton_skull` ×3, `minecraft:soul_sand` ×4 | 300 | feeds the Harbinger gate |
| 3 | Warden — *Kill the Warden* (`3D579A1F7EFEDD5C`, Deeper and Darker) | Overworld · Ancient City (`minecraft:ancient_city`) | *Visit an Ancient City* (`0B11EAB8D76529E0`); Chapter 1 reaches it after *Ancient Metals* (`5E799B92358A8732`) | 500 | Heart → Wither's Compass |
| 4 | Naga — *Evening The Scales* (`3531B28F14CF72A2`) | Twilight Forest · Courtyard (quest text) | trophy task `twilightforest:naga_trophy` | — | no |
| 5 | Twilight Lich — *Bring out your Dead* (`0107D516E038E0DB`) | Twilight Forest · Lich Tower (quest text) | trophy task `twilightforest:lich_trophy`; after the Naga (**verified**) | — | no |
| 6 | Minoshroom — *Mighty Meef Stroganoff* (`04440BB2EFFD6DD9`) | Twilight Forest · Minoshroom Labyrinth (quest text) | trophy task `twilightforest:minoshroom_trophy`, plus eating the stroganoff (quest text) | — | no |
| 7 | Hydra — *Hydra Slayer* (`7026E46FD8B3A81D`, subtitle *The Firey Swamp*) | Twilight Forest · Fire Swamp (quest text) | trophy task `twilightforest:hydra_trophy` | — | no |
| 8 | Knight Phantoms — *The Dark Forest* (`3DCF26B53AE1EBF6`) | Twilight Forest · Dark Forest underground structure (quest text) | trophy task `twilightforest:knight_phantom_trophy`; pedestal entry (quest text) | — | no |
| 9 | Ur-Ghast — *Tears of Fire* (`688C911ECFB2F134`, subtitle *Dark Carmonite Tower*) | Twilight Forest · Dark Tower (quest text) | trophy task `twilightforest:ur_ghast_trophy` | — | no |
| 10 | Alpha Yeti — *To the Snow Biomes!* (`31BB7EB95CE73C1A`) | Twilight Forest · Yeti cave (quest text) | trophy task `twilightforest:alpha_yeti_trophy` | — | unlocks the Glacier |
| 11 | Snow Queen — *Clear Skies* (`6FD41DF7704466A4`) | Twilight Forest · Aurora Palace (quest text) | trophy task `twilightforest:snow_queen_trophy` | — | **yes — Oblivion Shard** |
| 12 | Slider — *The Slider* (`24E124F12CFF2A50`) | The Aether (`aether:the_aether`) · `aether:bronze_dungeon` | *Bronze Dungeon* (`4BF7F82F1C8680B9`); bring a pickaxe (quest text) | 400 | no |
| 13 | Valkyrie Queen — *Valkyrie Queen* (`0D2F07FC0F804223`) | The Aether · `aether:silver_dungeon` | *10 Victory Medals* (`52007C01B52F7295`, task `aether:victory_medal`) after *Silver Dungeon* (`5900ADCC247CD5F9`) | 500 | no |
| 14 | Sun Spirit — *Sun Spirit* (`08E4892F96828EC4`) | The Aether · `aether:gold_dungeon` | *Gold Dungeon* (`5A5D4DFE4175FB42`); anger it by right-clicking (quest text) | — | no |
| 15 | Forgotten Guardian — *Forgotten Guardian* (`1054168AFD8520D4`) | Undergarden (`undergarden:undergarden`) · `undergarden:catacombs` | *Catacombs* (`00CB8D60E7831A57`) after the Catalyst portal quest *The Undergarden* (`6C4B93FE64BD418D`) | 80 | no |
| 16 | Lunar Monstrosity — *Lunar Monstrosity* (`0576C32B0FB360B0`) | Eternal Starlight (`eternal_starlight:starlight`) · `eternal_starlight:cursed_garden` | *Burn it!* (`4C23D7E3DC8327C2`) fire gate, after *Finding the Bosses* (`36BCCF7395658A5C`, task `eternal_starlight:seeking_eye`) | 200 | **yes — Chain of Souls** |
| 17 | Starlight Golem — *Starlight Golem* (`10AB188AC6FB24D3`) | Eternal Starlight · `eternal_starlight:golem_forge` | *Powering down* (`6E970CF05B96EB20`, `observation` on `eternal_starlight:energy_block`) | 220 | no |
| 18 | The Dead King — *The Dead King* (`0436DF3308681913`) | Overworld · `irons_spellbooks:catacombs` | *Catacombs* (`6DB5732177AABB87`); touch the remains (quest text) | 500 | no |
| 19 | Wilden Chimera — *Kill The Wilden Chimera* (`56DA46DC82F6665D`, Bounty Board) | Overworld · ritual (quest text) | `kill ars_nouveau:wilden_boss`; ritual in the Ars Nouveau chapter (quest text) | — | Archmage spellbook gate |
| 20 | Piglich — *Piglich Boss* (`5BA986D7928BF09F`) | The Other (`allthemodium:the_other`) · `allthemodium:ancient_pyramid` | *Ancient Pyramid* (`24934231538B6492`); tracked by `allthemodium:piglich_heart`, not a kill task | 9999 | **yes — Dragon Soul** |
| 21 | Stage 4-5 dragons — *Stage 4-5 Fire Dragon* (`765CD913CC3896B2`) | The Other · dragon caves (quest text) | caves after *Dragons and their Stages* (`6800E0113DE9A4DB`, task `iceandfire:dragonbone`) | as a Warden (quest text) | no |
| 22 | Ancient Remnant — *Ancient Remnant* (`33B1D3FD4C0B5514`) | Overworld deserts · `cataclysm:cursed_pyramid` | *Necklace of the desert* (`0B7F2B63D867D221`, task `cataclysm:necklace_of_the_desert`) resurrects it (quest text) | 2,700 | no |
| 23 | The Harbinger — *The Harbinger* (`17CA9D80D8EC3EF7`) | Overworld, deep underground · `cataclysm:ancient_factory` | *Nether Star* (`7AED8FD7FB023AD8`, task `minecraft:nether_star`) powers it up (quest text) | 4,680 | **yes — Void Forge / Meat Shredder** |
| 24 | The Leviathan — *The Leviathan* (`746DE905D45A396C`) | Overworld oceans · `cataclysm:sunken_city` | *Abyssal Sacrifice* (`1C5EA7D62BAF2108`, task `cataclysm:abyssal_sacrifice`) in the Cataclysm chapter | 6,400 | sacrifice feeds Dragon Soul |
| 25 | Ender Guardian — *Ender Guardian* (`2B115519A21F9CB7`) | The End · `cataclysm:ruined_citadel` (Void Altar, quest text) | *Ruined Citadel: Home of the Ender Guardian* (`21A0FD474FBB49F7`); approach to spawn (quest text) | 6,660 | no |
| 26 | Ignis — *Ignis* (`7D57A14810BC0CBE`) | The Nether · `cataclysm:burning_arena` | *Burning Ashes* (`7F4963FCAE5337EC`, task `cataclysm:burning_ashes`) on the altar (quest text) | 7,200 | Infernal Forge → Void Forge |
| 27 | Maledictus — *Maledictus* (`71055E7BBB337C4D`) | Overworld snowy mountains · `cataclysm:frosted_prison` | *Strange Key* (`55278DDC31951DA5`, task `cataclysm:strange_key`), then right-click the Cursed Tombstone (quest text) | 8,400 | no |
| 28 | Scylla — *Scylla* (`713006AB89E43C6D`) | Overworld, above oceans · `cataclysm:acropolis` (top floor, quest text) | *Acropolis: Home of Scylla* (`573DD5834B321D0A`); approach to spawn (quest text) | around 8658 | no |
| 29 | Netherite Monstrosity — *Netherite Monstrosity* (`53154550397E9704`) | The Nether · `cataclysm:soul_black_smith` | *Soul BlackSmith: Home of the Netherite Monstrosity* (`0F8F0F7880235BA2`) | up to 9,600 | **yes — Void Forge** |
| 30 | Chaos Guardian — *Kill the Chaos Guardian* (`5C2CF51D28F84CBE`) | The End · Chaos Islands (quest text, quoted below) | *Locate and Destroy 14 Guardian Crystals* (`106D08542AAFA166`) first (quest-text stage) | two health bars (quest text) | Chaos Shards |

Two title collisions the table keeps apart on purpose: Chapter 3 also has an
*Abyssal Sacrifice* quest (`2A444F4CCC72545D`, task `cataclysm:abyssal_sacrifice`)
— the same item counted toward the star — and an *Eternal Starlight* hub
(`792990DC06DB98F9`) that is not the dimension quest *Eternal Starlight*
(`6314B892B569A0A5`, task `dimension eternal_starlight:starlight`). Same words,
different quests; the id is the difference.

## Vanilla first: Chapter 1's three branches

Chapter 1: The Beginning (`mainquestline_part_1`, 36 quests) gives the verified
spine *We've Struck Diamonds!* → *To The Nether!* (`0F3D51FFD2FE8DCB`, tasks
`minecraft:obsidian` ×10 and advancement `minecraft:story/enter_the_nether`), then
branches three ways without ordering the branches. That is the whole verified
structure; which branch a player finishes first is *(judgement)*.

- **Ender Dragon — the End branch.** *Finding The End* (`61C49BC2B384FB80`, task
  `minecraft:ender_eye` ×10) → *The End* (`6EE5BE5693E8ACE4`), which is the
  advancement `minecraft:end/dragon_egg` — the egg after the fight, not a kill
  task. The kill itself is tracked only by the Bounty Board's *Kill The Ender
  Dragon* (`728BE1816DA23DC0`, `kill minecraft:ender_dragon`). Arena, per quest
  text: the End Island and its obsidian pillars. Tactics, quoted: *"You'll have
  to break the End Crystals on the pillars as they heal her, in order to kill
  her!"* and *"She has 200 Hearts and can attack with Fireballs or ramming into
  you."* Gear: no armour task gates this branch; the branch starts from *Gearing
  Up*'s diamond step *(judgement: finish the diamond set the quest text
  recommends before travelling)*.
- **Wither — the summon-it-yourself branch.** *Summoning The Wither*
  (`4A4C71C43519D5FE`) asks for `minecraft:wither_skeleton_skull` ×3 and
  `minecraft:soul_sand` ×4, and *Kill The Wither* (`69A517AB8A801939`,
  `kill minecraft:wither`) depends on it (**verified**). Its text gives the T
  shape and the book's only vanilla gear sentence: *"You'll also need at least
  4 pieces of Soul Sand, and probably some pretty good armor."* Bounty text adds
  the one phase note this page repeats: *"When taken to half Health he will
  gain a shield against Projectiles and will need to be killed with a Sword or
  Axe."* (Bounty *Kill The Wither*, `09C82CDDA800D8C9`, 300 Hearts *quest
  text*.) Arena: wherever the player builds it — *"It explodes. A lot. Don't do
  this near your base."*
- **Warden — the Deep Dark branch.** *Ancient Metals* (`5E799B92358A8732`, task
  `minecraft:netherite_ingot`) → *Visit The Deep Dark!* (`6EDAB29FBD3C60A3`,
  `biome minecraft:deep_dark`) → Chapter 1's *Kill The Warden*
  (`6D09511D64DDC282`, `kill minecraft:warden`). Deeper and Darker tracks the
  same kill again as *Kill the Warden* (`3D579A1F7EFEDD5C`) after *Visit an
  Ancient City* (`0B11EAB8D76529E0`, `structure minecraft:ancient_city`), then
  *Heart of the Deep* (`6E38CF6E7360E9CA`, task `deeperdarker:heart_of_the_deep`)
  → *The Otherside* (`76F14C2B866B4EAD`, task `dimension deeperdarker:otherside`).
  Tactics, quoted: *"He has 500 Hearts"* and *"he is Blind. He can only find you
  with Sound, or Smell if you are close enough!"* Gear signal: the branch hangs
  off the Netherite-ingot quest (**verified** dependency), which is the closest
  the book comes to expecting Netherite here — it still requires no armour
  piece. Miniboss company: the Bounty Board's *Kill A Elder Guardian*
  (`08D1CC753F6B4283`, `kill minecraft:elder_guardian`) — its text calls the
  Elder Guardian a Miniboss in Ocean Monuments with *"80 Hearts"* — plus *Kill
  A Ravager* (`734411D931A8CDBF`) and *Kill A Piglin Brute*
  (`3813F5C1760C3A79`). None of the three gates anything above.

## The Twilight Forest: the one strict order

The Twilight Forest (`twilight_forest`, 56 quests; The Twilight Forest
4.8.3345) is the only boss line whose full order is **verified** by dependency
links. Entry is *Welcome to the Twilight Forest!* (`4193303999597249`,
advancement `twilightforest:root`) — the config has no `dimension` task for this
dimension, so this page prints no dimension id for it. The portal, per that
quest's text and Chapter 3's *Twilight Forest* (`1682CED78D9D4BA7`, task
`minecraft:diamond`): a 2x2 water pool ringed with flowers and a thrown diamond
(quoted in `references/dimension-guide.md`). Every boss below is tracked by its
trophy item, never by a `kill` task, and no quest in the line tasks any armour
— the gear expectation is the diamond that opens the portal, then *(judgement)*
whatever the player has grown into; the line's own armour quests (*Naga Scale
Armor* and its successors) are rewards hanging off the trophies, not gates.

1. **Naga** — *Evening The Scales* (`3531B28F14CF72A2`). Quest text: *"The first
   boss you'll have to kill on your adventure in the Twilight Forest can be
   found within the Courtyard."*
2. **Twilight Lich** — *Bring out your Dead* (`0107D516E038E0DB`), in the Lich
   Tower. The text's three phases in one line each: reflect the Ender-Pearl
   shots to break the shields, melee through the summoned Zombies, then
   *"Kill him fast!"* when the scepter charges run out (*quest text*).
3. **Minoshroom** — via *To the Swamps!* (`4B95D48D7525FFAD`, tasks
   `twilightforest:maze_map` and `twilightforest:raw_meef` ×3) to *Mighty Meef
   Stroganoff* (`04440BB2EFFD6DD9`) in the Minoshroom Labyrinth. Unlock rule,
   quoted: *"To unlock the next area, you must eat it."* — the stroganoff, not
   just the trophy.
4. **Hydra** — *Hydra Slayer* (`7026E46FD8B3A81D`). Tactic, quoted: *"Ranged
   attacks aren't as effective, meaning you'll need to get up close and
   personal."*
5. **Knight Phantoms** — *The Dark Forest* (`3DCF26B53AE1EBF6`). Entry, quoted:
   place any acquired boss trophy on the pedestal to enter the underground
   structure; the Phantoms are on the 3rd layer (*quest text*, condensed —
   read the quest for the full wording).
6. **Ur-Ghast** — *Tears of Fire* (`688C911ECFB2F134`) in the Dark Tower.
   Tactic, quoted: *"The Ur-Ghast is recommended to kill with a ranged
   weapon."* The same text names the floor's Ghast traps as optional help.
7. **Alpha Yeti** — *To the Snow Biomes!* (`31BB7EB95CE73C1A`), in *"a massive
   Yeti cave"* (*quest text*).
8. **Snow Queen** — *Clear Skies* (`6FD41DF7704466A4`) at the top of the Aurora
   Palace. Tactic, quoted: *"You'll only be able to hit her top half, as she's
   protected by Ice."* Chapter 3's *Snow Queen Trophy* (`7D1A27CBF1508712`,
   task `twilightforest:snow_queen_trophy`) is why the line matters for the
   star, and its text repeats the gate: *"You'll need to kill the Alpha Yeti
   in order to enter the Glacier Biome."*

After the Queen the chapter turns item-shaped — *Visiting the Giants*
(`58BD1063A19777DC`) → *Lamp of Cinders* (`5CBA8C89FE717B9C`) → *Every Thorn
has its Rose* (`2951B1D7080C5EF9`, task `twilightforest:thorn_rose` ×12) →
*The Final Boss* (`420158B1736A1354`) → *The Real Final Boss*
(`0ED7B25DC1AA767B`) — and *Ramification* (`4DA0725E089D7C91`, task
`twilightforest:quest_ram_trophy`, the Questing Ram) hangs off the entry quest
as an optional side boss. See the last section for what *The Final Boss*
actually asks for.

## The Aether: three dungeons, no order between them

The Aether (`aether`, 73 quests; The Aether 1.5.10) opens with *Aether Portal*
(`27F62C4B42B16015`, tasks `minecraft:glowstone` ×10 and
`minecraft:water_bucket`) → *The Aether* (`5825892699A8DCB7`, task
`dimension aether:the_aether`). All three dungeon quests depend only on *The
Aether* (**verified** parallel — the book orders nothing here, whatever order
players usually learn). Each dungeon then gates its boss, and each boss drops
the key quest after it: *Bronze Key* (`3DB036804AD70497`, task
`aether:bronze_dungeon_key`), *Silver Key* (`26D6FC091B7A8B38`, task
`aether:silver_dungeon_key`), *Gold Key* (`5C6BA6BBEC75EB71`, task
`aether:gold_dungeon_key`). No armour task appears anywhere in the chapter;
*(judgement)* the Bronze-first habit matches the quest text calling the Bronze
Dungeon *"the easiest and simplest Dungeon."*

- **Slider** — *Bronze Dungeon* (`4BF7F82F1C8680B9`, `structure
  aether:bronze_dungeon`, underground, found by following Mossy Holystone down,
  *quest text*) → *The Slider* (`24E124F12CFF2A50`, `kill aether:slider`).
  The one tool gate: bring the best pickaxe to hand (**verified** quote
  above); at 100 Hearts *"his Eyes will turn Red and he'll move faster"*
  (*quest text*, 400 Hearts total).
- **Valkyrie Queen** — *Silver Dungeon* (`5900ADCC247CD5F9`, `structure
  aether:silver_dungeon`, above ground on clouds) → *10 Victory Medals*
  (`52007C01B52F7295`) → *Valkyrie Queen* (`0D2F07FC0F804223`, `kill
  aether:valkyrie_queen`, 500 Hearts *quest text*). The medals come from the
  dungeon's Valkyries: *"They have 50 Hearts each and are Neutral until you
  Hit them."* (*quest text*).
- **Sun Spirit** — *Gold Dungeon* (`5A5D4DFE4175FB42`, `structure
  aether:gold_dungeon`, underground under a Golden Oak mound) → *Sun Spirit*
  (`08E4892F96828EC4`, `kill aether:sun_spirit`). Start and damage rule,
  quoted: anger it by right-clicking to talk, then *"Hit the Ice Crystals at
  him to Freeze him! Once Frozen you can finally Hit him."* No Hearts figure
  is stated — do not supply one.

## Mid-game exploration: Undergarden, Eternal Starlight, Iron's Spells, and the Wilden Chimera

Four independent lines. The config orders none of them against the others, so
their relative order here is *(judgement)* — roughly: cheapest entry first.
What *is* verified inside each line is stated as such.

**The Undergarden** (`undergarden`, 82 quests; The Undergarden 0.9.6). *The
Undergarden* (`6C4B93FE64BD418D`, task `undergarden:catalyst`, subtitle *Making
the Portal*) → *Welcome to the Undergarden!* (`1C232674CD04024D`, task
`dimension undergarden:undergarden`) → *Catacombs* (`00CB8D60E7831A57`,
`structure undergarden:catacombs`) → *Forgotten Guardian*
(`1054168AFD8520D4`, `kill undergarden:forgotten_guardian`): *"The Forgotten
Guardian is a massive Golem made of Forgotten Ingots."* and *"They have 80
Hearts"* (*quest text*). Beside it, *Rotbeast* (`70FD8856BFCD9AEE`, `kill
undergarden:rotbeast`, 80 Hearts *quest text* — *"which I think qualifies as a
Boss"*, the author's words) and *Greater Dweller* (`1A23BBF444D17A63`, `kill
undergarden:greater_dweller`, 100 Hearts *quest text*), whose text carries
the chapter's one tool gate: *"You'll need a Forgotten Pickaxe or Allthemodium
Pickaxe to Mine the Dreadrock in the way."* The Bounty Board double-tracks
two of them (*Kill The Forgotten Guardian*, `199932BF623A6785`; *Kill A
Rotbeast*, `2CA9394459C24012`) — finishing the fight can complete both books
at once.

**Eternal Starlight** (`eternal_starlight`, 193 quests; Eternal Starlight
0.9.1). The gate is a duel with no kill task: *The Gatekeeper and The Gate*
(`429785E8F64929CE`, `structure #eternal_starlight:portal_ruins`) in the
Overworld. Quoted in full because it is the pack's clearest readiness signal:
*"Careful, they are very tough."* and *"The Gatekeeper will also deem you
worthy if you have defeated the Ender Dragon, and allow you to skip the
duel."* Winning (or skipping) leads to *Orb of Prophecy*
(`37355F60E45777FE`, task `eternal_starlight:orb_of_prophecy`) and *Eternal
Starlight* (`6314B892B569A0A5`). Inside, *Finding the Bosses*
(`36BCCF7395658A5C`) plus an offhand item per structure (the two filter quests
*Monstrosity Items* and *Golem Items* — their item lists live in the quest
entries, not here) routes to both bosses in parallel (**verified**: both hang
off *Finding the Bosses*):

- **Lunar Monstrosity** — *Cursed Garden* (`40786B63E2901D11`, `structure
  eternal_starlight:cursed_garden`, a maze with the boss in the middle) →
  *Burn it!* (`4C23D7E3DC8327C2`, filter: `minecraft:flint_and_steel` or
  `eternal_starlight:saltpeter_matchbox`) → *Lunar Monstrosity*
  (`0576C32B0FB360B0`, `kill eternal_starlight:lunar_monstrosity`). Damage
  rule, quoted: *"will only take 1 damage from each hit unless you use
  Fire."* (200 Hearts *quest text*.) Chapter 3's *Chain of Souls*
  (`5A955C0F53AED3ED`, task `eternal_starlight:chain_of_souls`) is crafted
  from its drops (*quest text*), which is why this boss is on the star path.
- **Starlight Golem** — *Golem Forge* (`375F0A098589CF29`, `structure
  eternal_starlight:golem_forge`, deep underground) → *Powering down*
  (`6E970CF05B96EB20`) → *Starlight Golem* (`10AB188AC6FB24D3`, `kill
  eternal_starlight:starlight_golem`, 220 Hearts, two modes *quest text*).
  The damage window, quoted: *"Right Click the Energy Blocks when they turn
  blue."* to make it damageable.

The Otherside's two minibosses belong to the Warden branch above: after *The
Otherside*, *Shattered* (`5E287410EE969244`, `kill deeperdarker:shattered`,
50 Hearts *quest text*) and *Shriek Worm* (`774D61FEFABEFD9A`, `kill
deeperdarker:shriek_worm`, *"Mini bosses with 100 Hearts"* *quest text*).
Neither gates the portal or the star.

**Iron's Spells 'n Spellbooks** (`iron_spells_and_spellbooks`, 103 quests;
Iron's Spells 'n Spellbooks 1.21.1-3.16.3). Each boss hangs off its structure
quest with no order between structures (**verified** parallel). The headline
fight is *The Dead King* (`0436DF3308681913`, `kill
irons_spellbooks:dead_king`) behind *Catacombs* (`6DB5732177AABB87`,
`structure irons_spellbooks:catacombs`): *"He has 500 Hearts and has an
actual Boss Bar (and music)."* (*quest text*) and *"If it doesn't [reanimate]
you might need to click him"* — start by touching the remains (*quest text*,
condensed). The supporting cast, each with its own structure: *Archevoker*
(`68B44B9E939F4228`, `kill irons_spellbooks:archevoker`, 60 Hearts *quest
text*, neutral until attacked) behind *Evoker Fort* (`641888DC7BC40AA9`,
`structure irons_spellbooks:evoker_fort`); *Cryomancer*
(`555ED1E39131D91B`, `kill irons_spellbooks:cryomancer`) behind *Mountain
Tower* (`13F77C38AC015E9F`, `structure irons_spellbooks:mountain_tower`);
*Ancient Knight* (`395A33977B18B9AD`, `kill irons_spellbooks:citadel_keeper`,
60 Hearts *quest text*) behind *Citadel* (`6187837A51BA09DC`, `structure
irons_spellbooks:citadel`) on the Nether side. No gear task gates any of
them; *(judgement)* treat the Dead King as the line's exam and the 60-Heart
fights as warm-ups — that ranking is read off quoted Hearts, not stated by
the book.

**Wilden Chimera** (Ars Nouveau 5.13.1). There is no kill quest in the Ars
Nouveau chapter itself: the Bounty Board carries *Kill The Wilden Chimera*
(`56DA46DC82F6665D`, `kill ars_nouveau:wilden_boss`) — *"He needs to be
summoned through a ritual then fought!"* — and an untitled Ars Nouveau quest
(`17D7D34F519F7E5F`, task `ars_nouveau:archmage_spell_book`) states the
stakes: *"To create the final tier of your Spellbook, you'll need to have
killed the Wilden Chimera."* by completing a ritual with a Ritual Brazier
(*quest text*, condensed). Which ritual and which glyphs belong to that
quest entry and the mod's guide book — not here. The untitled quest stays
untitled on this page; do not rename it.

## The Other: Piglich and Ice and Fire

Chapter 2: Allthemodium (`allthemodium`, 54 quests; Allthemodium 3.0.1)
supplies the verified gate for this whole section: *Allthemodium*
(`4B2146C9527C54E7`, task `minecraft:netherite_ingot`) → *Ancient City* →
*Allthemodium Ingot* (`201EE3566D4D3123`, task
`allthemodium:allthemodium_ingot`) → *Teleport Pad* (`07FDA46D83F8360D`, task
`allthemodium:teleport_pad`) → *The Nether* → *The Other*
(`15FEA03A2CDBA33B`, task `dimension allthemodium:the_other`). The tool ladder
the chapter quotes on the way: Allthemodium needs a Netherite-tier pickaxe,
Vibranium (*Vibranium Ingot*, `144BB025516E0994`) needs *"Allthemodium
Pickaxe (or the same tier)"*, Unobtainium (*Unobtainium Ingot*,
`4A079D40C0AF6BC3`) needs a Vibranium-tier pickaxe (all *quest text*). That
ladder — plus the hub's Netherite expectation quoted earlier — is the gear
the book expects here; anything more specific is *(judgement)*.

- **Piglich** — *Ancient Pyramid* (`24934231538B6492`, `structure
  allthemodium:ancient_pyramid`) → *Piglich Boss* (`5BA986D7928BF09F`), whose
  task is the drop item `allthemodium:piglich_heart`, not a kill. Quoted
  whole, because later versions may change it: *"He has 9999 Hearts and
  currently has no attacks but trust me when he does they will be
  devastating!"* Chapter 3's *Piglich Heart Block* (`501A0AEEC73C0790`, task
  `allthemodium:piglich_heart_block`) counts the farming for the star:
  *"You'll need 9 of them dead to make a Block of it..."* (*quest text*) —
  how to farm them is that quest's and JEI's business.
- **Ice and Fire** (`ice__fire`, 87 quests; Ice And Fire Community Edition
  2.0-beta.17) frames itself as The Other's content: its hub *Ice and Fire*
  (`7B21D2FAD5F3246A`) is a second `dimension allthemodium:the_other` task —
  *"Welcome to Ice and Fire! Now in The Other"*. Its dragon model, from
  *Dragons and their Stages* (`6800E0113DE9A4DB`): *"Stages 1-3 will spawn
  in Roosts while Stage 4 and 5 spawn in Caves. Only 4 and 5 will Drop
  Eggs."* Roosts and caves exist per element (`iceandfire:fire_dragon_roost`,
  `iceandfire:ice_dragon_roost`, `iceandfire:lightning_dragon_roost`,
  `iceandfire:fire_dragon_cave`, `iceandfire:ice_dragon_cave`,
  `iceandfire:lightning_dragon_cave`); the book tracks the fights by loot
  and advancement, not by `kill` tasks — *Stage 1-3 Fire Dragon*
  (`32992E3534B86521`, blood item `iceandfire:fire_dragon_blood` and its Ice
  and Lightning siblings) for the roosts, *Stage 4-5 Fire Dragon*
  (`765CD913CC3896B2`) for the caves. The cave text is the book's bluntest
  gear sentence: *"If you want to fight these massive Dragons you will need
  the best Gear, Enchants, and Potions."* with health *"as a Warden"* and
  armour matching full Netherite (*quest text*, condensed) — bring the top
  of the ladder above *(judgement: Vibranium-or-better, after Chapter 2's
  pickaxe ladder)*. The mythic supporting cast (Cyclops in `iceandfire:cyclops_cave`,
  Gorgon behind `iceandfire:gorgon_temple`, Sirens at `iceandfire:siren_island`,
  Hydra at `iceandfire:hydra_cave`, plus Death Worms, Stymphalian Birds,
  Ghosts, Trolls, Sea Serpents, Hippocampus) is inventoried with its quoted
  Hearts in the checklist; none of it gates the star, and this page adds no
  tactics beyond what those quests print. Whether a given creature also
  spawns in the Overworld in the player's version is *approximate* — the
  chapter itself notes the Hippocampus and Sea Serpents *"haven't been moved
  yet!"* to The Other (*quest text*) — so check in-game.

## Endgame: Cataclysm's eight and the Chaos Guardian

**Cataclysm** (`cataclysm`, 110 quests; L_Ender's Cataclysm 1.21.1 3.33). The
hub *Cataclysm* (`689F32883C4E9502`, advancement `minecraft:adventure/root`)
fans out to three dimension quests — *Nether: Land of 2 bosses*
(`565376084F05ED6E`, task `dimension minecraft:the_nether`), *Overworld: Land
of 3 4 5 bosses* (`0496E8E786262464`, task `dimension minecraft:overworld`),
*End: Land of 1 lonely boss* (`392EAE8BE71510C1`, task `dimension
minecraft:the_end`) — then one `structure` quest per arena, then the kill.
An untitled checkmark quest (subtitle *Defeat all Cataclysm bosses*,
`2790EB2E347D28DE`) depends on all eight kills (**verified** set). Four of
the eight have a summoning gate the config tasks explicitly; the other four
spawn on approach (*quest text*). No armour task gates any of them; the
*(judgement)* readiness line is the top of the Basic Armor ladder plus the
Wither already dead (the Harbinger gate below makes that one **verified**).

In the glance table's *(judgement)* Hearts order, with only the quoted
tactic that changes how the fight starts:

- **Ancient Remnant** (2,700 Hearts *quest text*) — resurrect it first:
  brush the pyramid shaft's Suspicious Sand for the necklace, then
  *"Right Click the Ancient Remnant with the Necklace of Desert to
  resurrect it!"* (*quest text*). Weakness, quoted: *"If you hit his
  Necklace he will be knocked down for a little bit"* (*quest text*,
  condensed).
- **The Harbinger** (4,680) — feed the powered-down Harbinger a Nether Star
  (*Nether Star* quest, subtitle *Powering The Harbinger*): *"To power up
  The Harbinger you'll need a Nether Star, which you get from killing the
  Wither."* Weakness, quoted: *"he is weak to the EMPs!"* (*quest text*) —
  the factory's own EMP loot is the hint the book intends.
- **The Leviathan** (6,400) — craft and bring the sacrifice from the Sunken
  City's own food chain (Deepling drops, Coral Golem and Coralssus coral;
  the *Abyssal Sacrifice* quest lists them). Arena rule, quoted: *"invincible
  outside of Water"* (*quest text*) — fight it in the water.
- **Ender Guardian** (6,660) — approach the Void Altar to spawn it (*quest
  text*). At half health *"his Mask will break"* and the arena floor gives
  way to the lower level (*quest text*, condensed).
- **Ignis** (7,200) — kill Ignited Revenants on the arena's second floor for
  ashes, then use them on the altar on the third (*Burning Arena: Home of
  the Ignis*, `50C9CB8FB16E453D`, *quest text*). Phase note, quoted: at
  around 4,800 Hearts it turns light blue, attacks quicker, and gains
  Lifesteal (*quest text*, condensed). Its drop starts the post-fight
  upgrade the book tracks next: *Ignitium* is *"an upgrade for Netherite"*
  whose ingot is *"dropped from the Ignis"* (*quest text*) — a reward,
  never an entry requirement.
- **Maledictus** (8,400) — the prison's miniboss holds the key: *Aptrgangr*
  (`4D822D92492E1F53`, `kill cataclysm:aptrgangr`) → *Strange Key*
  (`55278DDC31951DA5`) opens the sealed door, then *"Right Clicking the
  Cursed Tombstone"* summons the boss (all *quest text* / **verified**
  dependencies).
- **Scylla** (around 8658 Hearts and 12 Armor Points *quest text*) — climb
  to the top floor and approach to spawn her (*quest text*). The miniboss
  on the way down the page, *Clawdian* (2,250 Hearts *quest text*), is the
  arena's real warm-up *(judgement)*.
- **Netherite Monstrosity** (up to 9,600) — no summoning item; it is simply
  the Soul Blacksmith's resident (*quest text*). Sustain warning, quoted:
  *"He will regenerate Hearts when no Player is nearby."* — do not walk
  away mid-fight (*quest text*; the "stay nearby" advice is the obvious
  reading, flagged as such).

Star links inside the eight: Chapter 3's *Void Forge*
(`5B2FD54E425D5C9D`, task `cataclysm:void_forge`) needs the Harbinger and
the Netherite Monstrosity plus a Ruined Citadel miniboss, and *Meat Shredder*
(`4BD203AD481DDE8F`, task `cataclysm:meat_shredder`) needs the Harbinger —
*"after a very difficult and long boss fight"* (*quest text*). Which boss
drops which crafting item is JEI's answer; the quests above name the two
fights, this page does not extend the drop list.

**Chaos Guardian** (Draconic Evolution 3.1.4.633). *Where is he?*
(`45EE60207C466D6C`, subtitle *Finding Chaos Island*, task `dimension
minecraft:the_end`) prints the book's only numeric location hint, quoted as
written: *"Go to the End at an X/Z coordinate that is a multiple of 10k."*
Then *Locate and Destroy 14 Guardian Crystals* (`106D08542AAFA166` — its
task is the item `draconicevolution:infused_obsidian`; the crystal stage
itself is described, not tasked) → *Kill the Chaos Guardian*
(`5C2CF51D28F84CBE`, `kill draconicevolution:draconic_guardian`). Two
quoted sentences carry the whole tactic: *"Destroying these crystals is no
easy task without a Draconic weapon."* and *"he has two health bars both
need to get taken to 0 to get the Chaos Shards."* The Draconic-weapon line
is the book's one explicit weapon expectation in the endgame — treat the
Draconic line as this fight's gear gate (**verified** quote; how far up
that line is enough is *approximate* — ask JEI and the chapter). *Chaos
Shard{s}* (`6B8F2E05429C185F`, task `draconicevolution:chaos_shard` ×5)
counts the reward.

## If you only want the ATM Star

The star does not need most of this page. Chapter 3's verified boss work
(cross-reference `references/atm-star-checklist.md`) is exactly:

| Star task (Chapter 3) | Boss work behind it (this page) |
|---|---|
| *Snow Queen Trophy* (`7D1A27CBF1508712`) → Oblivion Shard | the Twilight line up to the Snow Queen (steps 4–11) |
| *Heart of the Deep* (`1EB04FE105ACA4BE`) → Wither's Compass | the Warden (step 3); the Otherside trip itself is not required |
| *Chain of Souls* (`5A955C0F53AED3ED`) → Dragon Soul | the Lunar Monstrosity (step 16) |
| *Piglich Heart Block* (`501A0AEEC73C0790`) → Dragon Soul | the Piglich, nine hearts (step 20) |
| *Abyssal Sacrifice* (`2A444F4CCC72545D`), *Void Forge* (`5B2FD54E425D5C9D`), *Meat Shredder* (`4BD203AD481DDE8F`) → Dragon Soul / Oblivion Shard | the Harbinger and the Netherite Monstrosity, plus Sunken City and Ruined Citadel miniboss drops (steps 23, 24 and 29) |

The Ender Dragon appears only as a simulated data model for the Dragon Soul
— *"In order to get it Self Aware you need to keep killing the Dragon"*
(*Ender Dragon Data Model* quest text, condensed) is about training the
model, and Hostile Neural Networks' simulated kills are covered in
`references/mob-farm-progression.md`. Everything else in the glance table —
the Aether, the Undergarden, the Dead King, the Chimera, the dragons, the
other five Cataclysm bosses, the Chaos Guardian — is gear, materials, or
the player's own ambition. Whether a specific star item still comes from
that boss in the player's version is JEI's answer.

## Not a fight, not implemented, or not a boss

- **The Final Boss is not a boss.** *The Final Boss* (`420158B1736A1354`)
  asks for castle door blocks (`twilightforest:pink_castle_door`,
  `twilightforest:yellow_castle_door`, `twilightforest:blue_castle_door`,
  `twilightforest:violet_castle_door`, ×12 each) because, quoted, *"...is
  not implemented."* Do not gear up for it; grab the doors in the Final
  Plateau castle (*quest text*). *The Real Final Boss*
  (`0ED7B25DC1AA767B`) behind it collects four saplings, no fight.
- **The Bee Queen gives quests; she is not fought.** The Bumblezone's *Your
  Highness* (`5C040191740A53C8`) is the advancement
  `the_bumblezone:the_queens_desire/the_beginning` — a trader and quest
  giver. The chapter's few `kill` tasks are ordinary mobs.
- **Auroral has no boss in the config.** Its chapter (`auroral`) contains
  no `kill` task at all — a night-time event, nothing to gear for.
- **The Gatekeeper is a gate, not a kill.** No quest tasks killing the
  Gatekeeper; the duel, the skip after the Ender Dragon, and the Orb are
  the whole mechanic the book tracks (quoted above).
- **Trader and villager "bounties" are jokes, not bosses.** The Bounty
  Board's *Kill The Trader Villager and His Annoying Llamas* is author
  humour in quest text; this page does not rank it. Likewise the Cataclysm
  chapter's item and armour quests after the kills are crafting follow-ups,
  not further fights.

## Related pages

- `references/boss-checklist.md` — the full inventory this page orders: every
  tracked boss and miniboss, dimension, arena, quoted Hearts.
- `references/dimension-guide.md` — what opens each dimension, in visit
  order, with the portal quests quoted.
- `references/atm-star-checklist.md` — Chapter 3's components by source mod.
- `references/bounty-board-checklist.md` — the same kills double-tracked as
  bounties, with their rewards and the Claim All trap.
- `references/armor-tools-ladder.md` — the Diamond-to-Unobtainium ladder the
  gear column refers to.
- `references/progression.md` — the four stages behind every "roughly when"
  here.

## What this page deliberately does not tell you

- **Full fight mechanics.** Attack lists, phase timings, and arena gimmicks
  beyond the quoted starting rules belong to the quest entry in-game and
  the mod's own guide book; quoting more here would go stale first.
- **Loadouts.** No enchantment, weapon, or potion is recommended beyond the
  items and tool tiers the quests themselves name. "Best Gear" stays the
  quest author's words — JEI and the player's current tier decide the rest.
- **Drop tables and respawn rules.** Only the drops a quest sentence names
  are repeated; JEI, in-game, on the mob, settles the rest.
- **Coordinates, distances, and spawn chances.** None, beyond the Chaos
  Islands hint quoted verbatim from its quest. Structure-finding items the
  quests name (the Seeking Eye above) are as precise as this page gets.
- **Bosses the book does not track.** Other mods in the pack may add fights
  of their own; if no quest in the 8.2 config points at one, it is not on
  this page — check the in-game quest book and JEI before saying anything
  about it. When uncertain, say so: the in-game quest book is authoritative,
  and this snapshot loses to it every time.
