# ATM10: getting started (first hours + setup)

Sources for this page: the official AllTheMods/ATM-10 quest config (Welcome and
Chapter 1 chapters, read directly), the published ATM10 mod list, and community beginner
guides (all-themods.com, GPORTAL wiki, blockpatch, r/allthemods). Where guides disagree
or a detail is version-sensitive, it is marked approximate. **The in-game quest book and
JEI override everything written here.**

## What the pack is

- **Minecraft 1.21.1, NeoForge** (pack 8.x at the time of writing), ~450–500 mods,
  kitchen-sink: nothing is gated behind quests, the quest book guides rather than forces.
- Java **21** is required (the pack will not launch on older Java).
- Install through the CurseForge app or Modrinth app; both list "All the Mods 10".
  There is also a skyblock spin-off (*ATM10: To the Sky*) — this skill covers the normal
  overworld pack, not the skyblock variant.

## RAM allocation (16 GB system)

- **Client (singleplayer or connecting to a server): allocate 8 GB.** The community range
  is 6–10 GB; 8 GB is the sweet spot on a 16 GB machine. Set it in the CurseForge app:
  Settings → Minecraft → Java Settings → Allocated Memory (or per-profile options).
- **Do not allocate more than ~10 GB to the client.** Java's garbage collector stutter
  gets worse with oversized heaps, and the OS plus a browser/Discord need the rest of the
  16 GB. Over-allocation is a more common cause of lag than under-allocation.
- **Dedicated server (if hosting for friends) is separate:** published guidance puts the
  ATM10 server floor at ~10 GB, 12 GB for a small group, more for 5+ players; the
  official server files ship `-Xms4G -Xmx8G` in `user_jvm_args.txt` which hosts raise to
  fit. A 16 GB *machine* cannot host a 10–12 GB server and a 8 GB client at once — run
  the server elsewhere or lower expectations.
- Performance mods are already in the pack — the 8.2 modlist names **ModernFix, Sodium,
  Sodium Extra, ImmediatelyFast, FerriteCore, All The Leaks, memorysettings, spark** and
  more (`references/lag-fix-guide.md` lists them with versions). There is nothing to
  install: if FPS is low, drop render distance and shader load before blaming RAM
  (approximate — system-dependent).

## First hour checklist

1. **Spawn in, open the quest book immediately** (FTB Quests — the book item or its
   keybind; check Controls if it is not on the hotbar). Do the **Welcome** chapter: it
   teaches `/sethome`, `/home`, `/rtp`, `/spawn`, chunk claiming via the map, and FTB
   teams, and hands out starting rewards. Its *Claiming Chunks* task is also the pack's
   only chunk-loading tutorial — see `references/chunk-loading-guide.md`.
2. **Start Chapter 1: The Beginning** and follow it. Its early quests (verified titles):
   *Our First Pick → Stone Age → The Metal Age → An Iron Pick → Furnace Upgrades! →
   Crafting, but on a Stick*. Furnace upgrades = Iron Furnaces; crafting-on-a-stick is a
   QoL mod in the pack.
3. **Learn the vein-mine keybind** (FTB Ultimine, commonly `~`). Holding it while mining
   ore or chopping trees is the single biggest early time-saver.
4. **Loot a village** before building anything big: guides highlight grabbing **Waystones**
   (cheap fast travel), loot, and checking for Artifacts/Relics trinkets.
5. **Set up Basic Power** (the chapter): wind/solar/lava generators and a first furnace
   line — Chapter 1 quests *Wind Power, Solar Power, Lava Power, Generators Galore* walk
   through it. Mekanism's basic generator + wind generator are the commonly recommended
   start (per guides; check the chapter).
6. **Get Silent Gear tools going** — the pack's tool progression replaces the vanilla
   grind (Basic Tools chapter). Guides flag the **Osmium Paxel** (Mekanism) as an early
   all-in-one tool worth making as soon as osmium is available (approximate timing).
7. **Basic Storage**: Sophisticated Storage chests/barrels with upgrades, or Functional
   Storage drawers. Do not sink hours into wooden chests — a storage mod comes soon after
   (AE2 or Refined Storage).

## First day / first week

- **Pick one tech line and one magic line.** The universal community advice for kitchen
  sinks: do not sample all ~500 mods. Canonical pairings: **Mekanism** or **Create** or
  **Modern Industrialization** (guided four-age ladder) for tech; **Ars Nouveau** or
  **Iron's Spells** or **Occultism** for magic. The quest book's group tabs make trying
  one chapter cheap.
- **Follow Chapter 1 to its end** before wandering: it takes you through diamonds →
  Netherite → the Nether → the End → Wither → Deep Dark/Warden (verified quest titles).
  Community players who "did the FULL quests in order" report it as the smoothest route.
- **Start Mystical Agriculture early-ish** (Resources group): inferium farming scales into
  ore seeds and is the highest-leverage farm in the pack — its own *Inferium Farmland*
  quest says *"You'll want to start growing Inferium as soon as you can!"* A crop
  harvester the book teaches (the Harvester Pylon, Mystical Agriculture's Harvester, or
  Industrial Foregoing's Plant Gatherer) automates the harvest; which crops each accepts
  is not in the config, so check in-game. What to farm, and what to set up first:
  `references/farming-guide.md`.
- **Choose your storage network** (AE2 vs Refined Storage) once chests stop scaling —
  this is a mid-tech-stage decision; both have full chapters, and Extended & Advanced AE
  / MEGA-style addons extend AE2 (addon availability approximate; check the mod list).
- **Bounty Board chapter** gives kill-count quests with loot rewards — a low-pressure way
  to gear up while doing other things.

## When you are stuck

- Stuck on a quest's *requirements*: open that quest in the book — tasks list exact items
  and counts; click through to JEI for recipes. Never trust a remembered number (or a
  number in this skill's docs) over the live quest entry.
- Stuck on *what to do next*: look at the Main Questline group; its four chapters are the
  intended spine (Chapter 1 → Allthemodium → The ATM Star → Creative).
- Stuck on *performance*: work through `references/lag-fix-guide.md` — FPS or TPS, the
  pack's own memory table, shaders, the video settings the pack ships translations for, the
  machines and farms the quest book calls laggy, and the profilers (spark and Observable
  both ship with the pack; read their own docs for the commands).
- Stuck on a *farm that stops when you leave it*: that is chunk loading, not a broken farm.
  `references/chunk-loading-guide.md` has the verified claim-and-force-load steps from the
  Welcome chapter, the chunk loaders this pack's config actually enables, and the four it
  ships switched **off** — plus the rule that no claim or force-load *limit* is quoted
  anywhere, because the pack repo ships no FTB Chunks config.
- Stuck on a *boss*: the Exploration chapters (Twilight Forest, Cataclysm, ...) and the
  mods' own in-game guide books (Patchouli/Modonomicon entries) carry the mechanics; the
  quest book lists the boss quests but not tactics.

## Multiplayer notes (approximate, from hosting guides)

- Claim chunks (FTB Chunks, taught in the Welcome chapter) before building together; force
  load the ones a shared farm needs (`references/chunk-loading-guide.md`).
- Lootr makes loot chests per-player, so shared exploration does not race.
- `/ftbteams party create <name>` shares quest progress within a team (from the Welcome
  chapter's quest text).
