# Boss checklist: which boss, which dimension, roughly when

**What this page is.** A boss map for **All the Mods 10**: every boss the pack's quest book
actually tracks, the dimension and structure it lives in, and roughly where in the
progression it lands. It exists so a session can answer "which boss do I need, where is it,
and am I ready?" without inventing a fight. For the dimensions themselves — what opens
each one, and in which order to visit them — see `references/dimension-guide.md`.

## Provenance — everything here was read, not remembered

Every boss name, dimension id, structure id, kill task, quest title, and quoted sentence
below comes from the official pack repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10), `main` branch as of
**2026-09-22** = **pack 8.2** (the "8.x" stamp in `examples/progress.example.json`):

| File(s) in the pack repo | What they supplied |
|---|---|
| `config/ftbquests/quests/chapters/*.snbt` | the boss quests' task types (`kill` with an entity id, `dimension`, `structure`, `advancement`) and their dependency links |
| `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the English quest titles, subtitles, and the description text quoted below |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (489 mod ids) |

Chapters read for this page: `mainquestline_part_1`, `bounty_board`, `allthemodium`,
`chapter_2_the_star`, `twilight_forest`, `aether`, `cataclysm`, `deeper_and_darker`,
`undergarden`, `eternal_starlight`, `ice__fire`, `bumblezone`, `auroral`,
`draconic_evolution`, `iron_spells_and_spellbooks`, `ars_nouveau`. Across the whole book
there are 213 `kill` tasks, 28 `dimension` tasks, 81 `structure` tasks and 54 `advancement`
tasks; the bosses below are the ones those tasks point at.

## Grounding rules (read before repeating any of this)

- **The in-game quest book and JEI are authoritative.** This is a snapshot of pack 8.2's
  config. If the player's book differs, his book wins.
- **Health numbers are the quest author's, quoted.** Where a "hearts" figure appears below
  it is taken from that quest's own description text in this pack version — flagged as
  *quest text*, never as a mechanic the skill verified. Do not add damage, armour, or
  respawn numbers that are not quoted.
- **No tactics, no gear lists, no drop tables.** The quest descriptions carry some of that
  and this page quotes only what identifies or locates the boss. For the fight itself: the
  quest entry, the mod's own in-game guide book (Patchouli/Modonomicon), and JEI for drops.
- **"Roughly when" is approximate by construction.** The pack does not gate anything behind
  bosses (its Welcome chapter says quests are optional and mods are not gated). The labels
  below combine the skill's four stages (`references/progression.md`) with the *order the
  chapter's own dependency links imply* — which is verified — and the readiness judgement,
  which is not.
- **Nothing here was invented, and nothing is added from memory.** Never invent a boss, an
  arena, a dimension, or a health number: a boss that is not in the config is not on this
  page, and if a player names one, the answer is "let's check your quest book / JEI" —
  never a plausible-sounding guess.

## The headline bosses at a glance

"Hearts" = quoted from that quest's description text (pack 8.2). "Tracked by" = chapter and
verified quest title.

| Boss | Dimension | Structure / arena | Tracked by | Hearts (quest text) | Roughly when |
|---|---|---|---|---|---|
| Wither | summoned (Overworld or Nether) | — | Chapter 1 *Kill The Wither*; Bounty Board *Kill The Wither* | — | early-game, after Nether access |
| Warden | Overworld | Ancient City / Deep Dark | Chapter 1 *Kill The Warden*; Deeper and Darker *Kill the Warden* | 500 | early→mid, Netherite-ish gear |
| Ender Dragon | The End | Exit portal / obsidian pillars | Bounty Board *Kill The Ender Dragon* (Chapter 1's *The End* is the `minecraft:end/dragon_egg` advancement) | — | early-game, end of Chapter 1's arc |
| Naga | Twilight Forest | the Courtyard | The Twilight Forest *Evening The Scales* (`twilightforest:naga_trophy`) | — | mid, first TF boss |
| Twilight Lich | Twilight Forest | Lich Tower | *Bring out your Dead* (`twilightforest:lich_trophy`) | — | mid, after the Naga |
| Minoshroom | Twilight Forest | Minoshroom Labyrinth (Labyrinth Swamp) | *Mighty Meef Stroganoff* (`twilightforest:minoshroom_trophy`) | — | mid |
| Hydra | Twilight Forest | Fire Swamp (subtitle *The Firey Swamp*) | *Hydra Slayer* (`twilightforest:hydra_trophy`) | — | mid-late |
| Knight Phantoms | Twilight Forest | Dark Forest underground structure | *The Dark Forest* (`twilightforest:knight_phantom_trophy`) | — | mid-late |
| Ur-Ghast | Twilight Forest | Dark Tower (Dark Forest) | *Tears of Fire* (`twilightforest:ur_ghast_trophy`) | — | late-mid TF line |
| Alpha Yeti | Twilight Forest | Snow biomes | *To the Snow Biomes!* (`twilightforest:alpha_yeti_trophy`) | — | late TF line |
| Snow Queen | Twilight Forest | — | *Clear Skies* (`twilightforest:snow_queen_trophy`) | — | end of the TF line; **star component** |
| Questing Ram | Twilight Forest | ruins | *Ramification* (`twilightforest:quest_ram_trophy`) | — | optional side boss |
| Slider | The Aether | Bronze Dungeon (underground) | The Aether *The Slider* (`kill aether:slider`) | 400 | mid, easiest Aether boss |
| Valkyrie Queen | The Aether | Silver Dungeon (on clouds) | *Valkyrie Queen* (`kill aether:valkyrie_queen`) | 500 | mid-late Aether |
| Sun Spirit | The Aether | Gold Dungeon (under a Golden Oak mound) | *Sun Spirit* (`kill aether:sun_spirit`) | — | late Aether |
| Netherite Monstrosity | The Nether | Soul Blacksmith | Cataclysm *Netherite Monstrosity* | "up to 9,600" | endgame |
| Ignis | The Nether | Burning Arena (summoned with Burning Ashes on the Altar of Flame) | Cataclysm *Ignis* | 7,200 | endgame |
| Ender Guardian | The End | Ruined Citadel (Void Altar) | Cataclysm *Ender Guardian* | 6,660 | endgame |
| The Harbinger | Overworld | Ancient Factory (deep underground) | Cataclysm *The Harbinger* | 4,680 | endgame |
| The Leviathan | Overworld oceans | Sunken City | Cataclysm *The Leviathan* | 6,400 | endgame |
| Ancient Remnant | Overworld deserts | Cursed Pyramid | Cataclysm *Ancient Remnant* | 2,700 | endgame |
| Maledictus | Overworld snowy mountains | Frosted Prison (Cursed Tombstone) | Cataclysm *Maledictus* | 8,400 | endgame |
| Scylla | Overworld, above oceans | Acropolis (top floor) | Cataclysm *Scylla* | "around 8658" | endgame |
| Piglich | Allthemodium's **The Other** | Ancient Pyramid | Chapter 2: Allthemodium *Piglich Boss* (`allthemodium:piglich_heart`) | "9999" (and "currently has no attacks") | endgame; **star component** |
| Chaos Guardian | The End | Chaos Islands "at an X/Z coordinate that is a multiple of 10k" | Draconic Evolution *Kill the Chaos Guardian* | two health bars | endgame |
| The Dead King | Overworld | Catacombs throne room | Iron's Spells *The Dead King* | 500 | mid-late |
| Archevoker | Overworld | Evoker Fort | Iron's Spells *Archevoker* | 60 | mid |
| Lunar Monstrosity | Eternal Starlight | Cursed Garden (maze) | Eternal Starlight *Lunar Monstrosity*; Bounty Board | 200 (1 damage per hit unless fire) | late |
| Starlight Golem | Eternal Starlight | Golem Forge (deep underground) | *Starlight Golem*; Bounty Board | 220 (two modes) | late |
| The Gatekeeper | Overworld | Portal Ruins | *The Gatekeeper and The Gate* (`#eternal_starlight:portal_ruins`) | — | mid-late; skippable after the Ender Dragon |
| Forgotten Guardian | The Undergarden | Catacombs | The Undergarden *Forgotten Guardian*; Bounty Board | 80 | mid-late |
| Wilden Chimera | Overworld | ritual | Bounty Board *Kill The Wilden Chimera* (`ars_nouveau:wilden_boss`) | — | mid-late magic |
| Dragons (stages 1–5) | The Other (and the Overworld) | Roosts (stages 1–3), Caves (stages 4–5) | Ice and Fire *Stage 1-3 …* / *Stage 4-5 …* per element | — | mid-late, dangerous |

## Vanilla and the Main Questline

Chapter 1: The Beginning (`mainquestline_part_1`, 36 quests) is where the vanilla bosses
live, and the chapter's dependency links give the arc: *Our First Pick → Stone Age → The
Metal Age → An Iron Pick → We've Struck Diamonds! → To The Nether!*, which then branches
three ways — *Finding The End → The End*, *Summoning The Wither → Kill The Wither*, and
*Ancient Metals → Visit The Deep Dark! → Kill The Warden*.

- **Wither** — `kill minecraft:wither`. The preparation quest *Summoning The Wither* asks
  for `minecraft:wither_skeleton_skull` ×3 and `minecraft:soul_sand` ×4, and its text
  describes the T shape. Quest text: *"It explodes. A lot. Don't do this near your base."*
- **Warden** — `kill minecraft:warden`, tracked twice: Chapter 1's *Kill The Warden* and the
  Deeper and Darker chapter's *Kill the Warden* (the one that quotes 500 Hearts and explains
  the Sculk Shrieker spawn rule). *Visit The Deep Dark!* is a `biome minecraft:deep_dark`
  task, and Chapter 2's Allthemodium line needs the Ancient City (`structure
  minecraft:ancient_city`) for its ore.
- **Ender Dragon** — the *kill* quest is in the Bounty Board, not Chapter 1. Chapter 1's
  *The End* is the advancement `minecraft:end/dragon_egg`, i.e. the egg after the fight.
  Say this when a player asks why his book shows the End "done" without a dragon kill quest.
- **Elder Guardian, Ravager, Piglin Brute** — Bounty Board kill quests (`kill
  minecraft:elder_guardian`, `minecraft:ravager`, `minecraft:piglin_brute`).

## The Twilight Forest — a strictly ordered line

The chapter hub in Chapter 3 says it plainly: *"Here you'll need to follow a strict order
of Bosses to kill and progress!"* The Twilight Forest chapter tracks its bosses by
**trophy item**, not by kill task, and the config's dependency links give the order
verified below. Portal, per the chapter's first quest text: *"make a 2x2 hole in the ground
and fill it with water. Surround the edges of the hole with flowers, and throw a Di[amond]"*.

1. **Naga** — *Evening The Scales* → `twilightforest:naga_trophy`; the quest text puts it
   "within the Courtyard" and calls it *"The first boss you'll have to kill"*
2. **Twilight Lich** — *Bring out your Dead* → `twilightforest:lich_trophy`; text: *"The
   Lich Tower is home to the Lich! The fight has 3 phases"*
3. **Minoshroom** — *Mighty Meef Stroganoff* → `twilightforest:minoshroom_trophy` (+
   `twilightforest:meef_stroganoff`); gated behind *To the Swamps!*, whose text names *"the
   Minoshroom Labyrinth"* in the Labyrinth Swamp, and the trophy quest adds *"To unlock the
   next area, you must eat it"* (the Meef Stroganoff)
4. **Hydra** — *Hydra Slayer* (subtitle *The Firey Swamp*) → `twilightforest:hydra_trophy`;
   text: *"Ranged attacks aren't as effective"*, and beating it opens the Dark Forest
5. **Knight Phantoms** — *The Dark Forest*: quest text says to enter the underground
   structure, place any boss trophy on the pedestal, and find them on the 3rd layer
6. **Ur-Ghast** — *Tears of Fire* (subtitle *Dark Carmonite Tower*): Dark Tower in the Dark
   Forest, reappearing blocks at the base; text recommends ranged and mentions 4 ghast traps
7. **Alpha Yeti** — *To the Snow Biomes!* → `twilightforest:alpha_yeti_trophy`
8. **Snow Queen** — *Clear Skies* → `twilightforest:snow_queen_trophy` ← **the star wants
   this one** (Chapter 3, Oblivion Shard line)

After the trophies, the chapter's late line is item-shaped rather than boss-shaped: *Lamp of
Cinders* (Giant's Pickaxe on Giant Obsidian in Troll Caves) → *Visiting the Giants*
(`twilightforest:magic_beans` + `twilightforest:uberous_soil`, Highland biome, Trolls) →
*Every Thorn has its Rose* (`twilightforest:thorn_rose` ×12, Thornlands) → *The Final Boss*
→ *The Real Final Boss* (four saplings: time, sorting, mining, transformation).

Two honest caveats from the pack's own text: *The Final Boss* is described as *"...is not
implemented. Instead, head to the giant castle in the Final Plateau and grab some door
blocks!"* (it asks for castle door blocks ×12 each of pink, yellow, blue, and more), and
*Ramification* (the **Questing Ram**, `twilightforest:quest_ram_trophy`) hangs off the
chapter's first quest, so it is an optional side boss, not part of the ordered line — its
text mentions Rainbow Wool in 16 colours and a dispenser.

## The Aether — three dungeons, three bosses

Dimension task: `dimension aether:the_aether`. Portal quest *Aether Portal* asks for
`minecraft:glowstone` ×10 and a `minecraft:water_bucket`, and its text jokes about the old
glowstone-and-water recipe — read the quest, do not guess the frame.

| Boss | Dungeon (structure task) | Where the dungeon is, per quest text | Hearts (quest text) |
|---|---|---|---|
| **Slider** | `aether:bronze_dungeon` | underground, "made of big square rooms made of Carved Stone"; find it by following Mossy Holystone down | 400 — "you'll need a Pickaxe to deal Damage" |
| **Valkyrie Queen** | `aether:silver_dungeon` | above ground on huge clouds, Angelic Stone; top floor, staircase at the back | 500 — fight unlocks after "10 Victory Medals" (Valkyries, 50 Hearts each, neutral until hit, "they'll fight one at a time") |
| **Sun Spirit** | `aether:gold_dungeon` | underground under a mound covered in Golden Oak Trees | not stated — right-click to anger it, then hit the Ice Crystals back to freeze it before damaging |

The chapter's other kill quests are mobs, not bosses: Sheepuff, Phyg, Aerwhale, Aerbunny,
Moa, Flying Cow, Aechor Plant, Blue/Golden Swet, Zephyr, Sentries, Cockatrice (10 Hearts,
spawns in the dark), Mimic (20 Hearts, dungeon chests). *Whoops!* is a
`dimension minecraft:overworld` task — falling out of the sky.

## L'Ender's Cataclysm (`cataclysm` — L_Ender's Cataclysm 1.21.1 3.33)

The pack's hardest fights, and the chapter is explicit about where they are: three
dimension quests — *Nether: Land of 2 bosses*, *Overworld: Land of 3 4 5 bosses*, *End: Land
of 1 lonely boss* — plus one `structure` quest per arena whose title names its boss. The
chapter also has an untitled quest subtitled *"Defeat all Cataclysm bosses"* (a checkmark),
and a chapter hub whose task is the advancement `minecraft:adventure/root`.

| Arena (`structure` id) | Dimension, per quest text | Boss | Hearts (quest text) |
|---|---|---|---|
| `cataclysm:soul_black_smith` — *Soul BlackSmith: Home of the Netherite Monstrosity* | Nether | **Netherite Monstrosity** | "up to 9,600", regenerates when no player is nearby |
| `cataclysm:burning_arena` — *Burning Arena: Home of the Ignis* | Nether (3 floors; Ignited Revenants on the 2nd drop Burning Ashes) | **Ignis** | 7,200 |
| `cataclysm:ruined_citadel` — *Ruined Citadel: Home of the Ender Guardian* | The End | **Ender Guardian** | 6,660 |
| `cataclysm:ancient_factory` — *Ancient Factory: Home of The Harbinger* | Overworld, deep underground | **The Harbinger** | 4,680 |
| `cataclysm:sunken_city` — *Sunken City: Home of The Leviathan* | Overworld oceans | **The Leviathan** | 6,400 — "invincible outside of Water" |
| `cataclysm:cursed_pyramid` — *Cursed Pyramid: Home of Ancient Remnant* | Overworld deserts | **Ancient Remnant** | 2,700, aided by a Wadjet and a Kobolediator |
| `cataclysm:frosted_prison` — *Frosted Prison: Home of the Maledictus* | Overworld snowy mountains | **Maledictus** | 8,400, summoned by right-clicking the Cursed Tombstone |
| `cataclysm:acropolis` — *Acropolis: Home of Scylla* | Overworld, a city in the clouds above oceans | **Scylla** | "around 8658", spawns at the top |

Minibosses and guards, each with its own verified kill quest: **The Prowler** (Ancient
Factory, 640 Hearts), **The Watchers** (Ancient Factory), **Coralssus** (Sunken City, 160),
**Deeplings** (Sunken City, five entity ids), **Coral Golem** (Sunken City, and oceans after
the Leviathan), **Ignited Revenant** (Burning Arena, 640), **Ignited Berserker** (Nether
Fortresses *after* Ignis, 65), **Ender Golem** (Ruined Citadel, 3,000), **Endermaptera**
(Ruined Citadel, 8), **Koboletons** and the minibosses **Kobolediator** (540) and **Wadjet**
(450) in the Cursed Pyramid, **Aptrgangr** (Frosted Prison, 480), **Draugrs** (Frosted
Prison), **Amethyst Crab** (Lush Caves, 1,200, initially neutral), **Clawdian** (Acropolis,
2,250), **Urchinkin** (6), **Octohost** (`cataclysm:symbiocto` + `cataclysm:drowned_host`),
**Cindaria** (60), **Hippocamtus** (85). Other structure quests without a named boss:
Abandoned Spire, Abandoned Temple, Abandoned Village, Amethyst Nest, Occupied Village
(`cataclysm:desert_occupied_village`), Desert Site, Desert Temple.

**Star relevance:** three Chapter 3 tasks are Cataclysm items — *Abyssal Sacrifice*
(`cataclysm:abyssal_sacrifice`, Dragon Soul), *Void Forge* (`cataclysm:void_forge`) and
*Meat Shredder* (`cataclysm:meat_shredder`) (both Oblivion Shard). Which boss drops which is
JEI's answer, not this page's.

## Deeper and Darker (`deeperdarker` 1.4.1) — the Warden and the Otherside

The chapter's spine is verified by its dependency links: *Visit an Ancient City* → **Kill
the Warden** (500 Hearts per quest text, spawned by Sculk Shriekers) → **Heart of the Deep**
(`deeperdarker:heart_of_the_deep`, a Warden drop) → **The Otherside** (`dimension
deeperdarker:otherside`, opened by placing the Heart on a frame of Reinforced Deepslate, per
the quest text) → the biome quests (**Deeplands**, **Blooming Caverns**) and their mobs.

Inside the Otherside: **Shattered** ("mini Wardens", 50 Hearts), **Shriek Worm** ("Mini
bosses with 100 Hearts", from Infested Sculk in the Deeplands), Sculk Centipede, Sculk
Snapper, Angler Fish, Sludge, Sculk Leech, plus the `structure deeperdarker:ancient_temple`
quest (*Ancient Temples*).

**Star relevance:** *Heart of the Deep* is a Chapter 3 task for the Wither's Compass.

## The Undergarden (`undergarden` 0.9.6)

Entered via `dimension undergarden:undergarden` (*Welcome to the Undergarden!*). Boss-grade
quests: **Forgotten Guardian** (80 Hearts per quest text, gated behind the chapter's
*Catacombs* quest — "a massive Golem made of Forgotten Ingots"), **Rotbeast** (80 Hearts,
"which I think qualifies as a Boss" — the quest author's words), **Greater Dweller** (100
Hearts, below Y 0), **Gwib**, **Forgotten**, Dweller, Brutes, Muncher, Stoneborn, Nargoyle,
Gloomper, Scintling, Sploogie, Gwibling, Mog, S'Mog, Rotbelcher, Rotling, Rotwalker,
Mysterious Pots (4 Hearts, disguised). *Warning* is the advancement
`undergarden:undergarden/contract_utheric_infection`.

## Eternal Starlight (`eternal_starlight` 0.9.1) — duel first, then two bosses

- **The Gatekeeper** — Overworld, `structure #eternal_starlight:portal_ruins`. Quest text:
  right-click to *"challenge them to a duel! Careful, they are very tough"*, and *"The
  Gatekeeper will also deem you worthy if you have defeated the Ender Dragon, and allow you
  to skip the duel."* Winning gives the Orb of Prophecy that opens the portal to
  `dimension eternal_starlight:starlight`.
- **Lunar Monstrosity** — *Cursed Garden* structure quest (a maze; the quest text says the
  boss is in the middle, found with a Seeking Eye plus offhand items). 200 Hearts and *"will
  only take 1 damage from each hit unless you use Fire"*; the companion quest *Burn it!*
  names Flint and Steel or a Saltpeter Matchbox.
- **Starlight Golem** — *Golem Forge* structure quest (deep underground, negative Y). 220
  Hearts, two modes; the companion quest *Powering down* is an `observation` task on
  `eternal_starlight:energy_block` — right-click the energy blocks when they turn blue to
  make it damageable.

The rest of the chapter's kill quests are mobs (Twilight Gaze, Nightfall Spider, Yeti,
Aurora Deer, Ratlin, Ent, Lonestar Skeleton, Thirst Walker, Tangled, Freeze, Crystallized
Moth, Gleech, Luminaris, Luminofish, Seeker, Shadow Snail, Rookfish).

**Star relevance:** *Chain of Souls* (`eternal_starlight:chain_of_souls`) feeds Dragon Soul.

## Ice and Fire (`iceandfire` — "Ice And Fire Community Edition" 2.0-beta.17)

This chapter's dimension task is **`allthemodium:the_other`** — in ATM10 the chapter frames
Ice and Fire as content of the pack's own *The Other* dimension (the hub quest is literally
titled *Ice and Fire* with that dimension task, and its text says *"Welcome to Ice and Fire!
Now in The Other"*). Whether a given creature also spawns in the Overworld in the player's
version is **approximate** — check in-game.

- **Dragons** — *Dragons and their Stages* explains the model: stages 1–5, element decides
  biome; *"Stages 1-3 will spawn in Roosts while Stage 4 and 5 spawn in Caves. Only 4 and 5
  will Drop Eggs."* Structure quests exist for all three elements × both:
  `iceandfire:fire_dragon_roost`, `ice_dragon_roost`, `lightning_dragon_roost`,
  `fire_dragon_cave`, `ice_dragon_cave`, `lightning_dragon_cave`; kill/loot quests *Stage
  1-3 …* and *Stage 4-5 …* per element (dragon blood items).
- **Other mythic bosses** (kill or advancement tasks, with the biome quest each hangs off in
  the config): **Cyclops** (650 Hearts, *The Other Desert*), **Death Worms** (desert, size
  scales health), **Gorgon** (300 Hearts, *The Other Soul Sand Valley*), **Sirens** (150),
  **Hydra** ("over 450 Hearts", *Ancient Warped Forest*), **Stymphalian Birds** (12 Hearts,
  4 armour), **Ghosts** (140 Hearts, cursed chests / graveyard soil at night), **Trolls**
  (500 Hearts, 10 armour), **Sea Serpents** (50–250+ Hearts by size), **Hippocampus** (20),
  **Hippogryph** (20, tameable), plus taming advancements for the Amphithere and Cockatrice.

## Allthemodium's Piglich (Chapter 2)

Verified chain in `allthemodium`: *The Nether* → **The Other** (`dimension
allthemodium:the_other`) → **Ancient Pyramid** (`structure allthemodium:ancient_pyramid`) →
**Piglich Boss** (task: `allthemodium:piglich_heart`). The quest text: *"The Piglich is a
Boss added by Allthemodium. He has 9999 Hearts and currently has no attacks but trust me
when he does they will be devastating! ... (Look into ways of farming them like with HNN or
EnderIO!)"* — quoted, and exactly the kind of detail that changes between versions.

The Other's structures per the chapter text: Piglin Village, Ancient Pyramid, Dungeon, plus
structures from When Dungeons Arise and Ice and Fire. Chapter 2 also has *Mining Dimension*
(`allthemodium:mining`), *The Beyond* (`allthemodium:the_beyond`), and *Teleport Pad*
(`allthemodium:teleport_pad`, shift-right-click with both hands empty).

**Star relevance:** *Piglich Heart Block* feeds Dragon Soul.

## Draconic Evolution's Chaos Guardian

*Where is he?* is a `dimension minecraft:the_end` task whose text locates the fight: *"Chaos
Shards are in Chaos Islands guarded by Chaos Guardians in the End. Go to the End at an X/Z
coordinate that is a multiple of 10k."* **Kill the Chaos Guardian** is
`kill draconicevolution:draconic_guardian`; its text says *"he has two health bars both need
to get taken to 0 to get the Chaos Shards"*.

## Iron's Spells 'n Spellbooks (`irons_spellbooks` 1.21.1-3.16.3)

Boss and boss-adjacent quests, each tied to a `structure` quest in the same chapter:

| Quest (verified title) | Entity / structure | Hearts (quest text) | Notes from the quest text |
|---|---|---|---|
| The Dead King | `kill irons_spellbooks:dead_king`; *Catacombs* = `structure irons_spellbooks:catacombs` | 500, "an actual Boss Bar (and music)" | Throne Room; "If it doesn't [reanimate] you might need to click him" |
| Archevoker | `kill irons_spellbooks:archevoker`; *Evoker Fort* | 60 | neutral until attacked |
| Cryomancer | `kill irons_spellbooks:cryomancer`; *Mountain Tower* | not stated | hostile, ice spells |
| Ancient Knight | `kill irons_spellbooks:citadel_keeper`; *Ancient Battleground*, *Citadel* (`irons_spellbooks:citadel`) | 60 | also from spawners; the Citadel is the Nether-side structure |
| Apothecarist | `kill irons_spellbooks:apothecarist`; *Mangrove Hut* | 60 | neutral trader |
| Pyromancer | `kill irons_spellbooks:pyromancer`; *Pyromancer Tower* | 60 | neutral trader |
| Priest | `kill irons_spellbooks:priest`; *Village* (`#minecraft:village`) | not stated | neutral village protector |
| Necromancers | `kill irons_spellbooks:necromancer` | "25 Points of Health" | *"They aren't bosses, just more Enemies!"* |

The chapter's *Adventure Time!* (`dimension minecraft:overworld`) says *"There's 6
structures in the Overworld that the bosses can spawn in! (There's a 7th but no boss in
there)."* The Nether side is *On a Highway to...* (`dimension minecraft:the_nether`), which
is what the *Citadel* and *Ancient Battleground* quests hang off — consistent with the
Citadel's text: *"almost entirely made of Blackstone"*.

## Ars Nouveau's Wilden Chimera

No kill quest in the Ars Nouveau chapter itself: the Bounty Board carries *Kill The Wilden
Chimera* (`kill ars_nouveau:wilden_boss`), and an untitled Ars Nouveau quest (task
`ars_nouveau:archmage_spell_book`) says the final spellbook tier needs the Wilden Chimera
killed via a ritual with a Ritual Brazier. Which ritual and which glyphs: the quest entry and
Ars Nouveau's own guide book — not here.

## The Bumblezone and Auroral: no boss fight

- **The Bumblezone** (`the_bumblezone` 7.16.1): *Your Highness* is the advancement
  `the_bumblezone:the_queens_desire/the_beginning` — the **Bee Queen** is a quest giver and
  trader, not a fight (*"so big she can't even move on her own"*; 16 of her quests give Bee
  Essence). The chapter's other advancement tasks are her `the_queens_desire/*` line.
- **Auroral** (`auroral` 1.21.1-1.1.2): the single quest is the advancement `auroral:root` —
  a night-time event in snowy biomes, no boss in the config.

## Bounty Board: the kill quests that double as a boss list

`bounty_board` (50 quests) tracks these kills, each `count 1` in the config: Ender Dragon,
Wither, Elder Guardian, Warden, Ravager, Piglin Brute, Wilden Chimera
(`ars_nouveau:wilden_boss`), Lunar Monstrosity, Starlight Golem, Forgotten Guardian,
Rotbeast, and *Kill The Trader Villager and His Annoying Llamas* (`minecraft:wandering_trader`
+ `minecraft:trader_llama`). Its variant quests pull in `variantsandventures`,
`creeperoverhaul`, and `endermanoverhaul` mobs. Useful as a low-pressure "gear up while you
build" list — and as a second place where the same boss is tracked, which is why a player's
book can show a boss quest complete while another is not.

## Bosses the ATM Star actually needs

Cross-reference with `references/atm-star-checklist.md`:

| Star component | Boss work behind it |
|---|---|
| Oblivion Shard | Snow Queen Trophy (Twilight Forest), Void Forge + Meat Shredder (Cataclysm) |
| Dragon Soul | Abyssal Sacrifice (Cataclysm), Piglich Heart Block (Allthemodium / The Other), Ender Dragon Data Model (Hostile Neural Networks — simulated, not killed) |
| Wither's Compass | Heart of the Deep (Warden, Overworld Ancient City) |

That is the practical answer to "do I have to do all the bosses?": for the star, no — the
config's Chapter 3 needs the Twilight Forest line up to the Snow Queen, three Cataclysm
items, the Piglich, and the Warden. Everything else on this page is gear, materials, or the
player's own ambition. Whether a specific item still comes from that boss in the player's
version is JEI's answer.

## What this page deliberately does not tell you

- **Fight mechanics beyond the quoted sentence.** Attack lists, phases, immunities, and
  arena gimmicks are in the quest descriptions in-game and the mod's guide book; quoting
  them here would go stale the moment the pack updates.
- **Gear recommendations.** "Bring good armour" is not advice; the player's current
  Allthemodium/Vibranium/Unobtainium tier and enchants decide it, and the skill must not
  invent a loadout.
- **Drop tables and loot ids.** JEI, in-game, on the mob.
- **Spawn rates, coordinates, or seed-specific locations.** Only the config's own hints are
  quoted (chaos islands at multiples of 10k, the Aether's Golden Oak mound, and so on).
