# Lag fix guide: "how do I fix lag?" in ATM10

**What this page is.** The triage path for **All the Mods 10** when FPS drops, the game
stutters, or a server starts ticking slowly: what to check first, which settings the pack
actually ships, and which of the pack's own machines and farms its quest book already
warns about. It exists so a session can answer a beginner's "how do I fix lag?" with the
pack's own numbers instead of generic advice — and without inventing a single setting.

## Provenance — everything here was read, not remembered

Every quest title, quoted sentence, config key, and mod version below comes from the
official pack repository [AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at
`main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22), which `config/bcc-common.toml` names **All the Mods 10** version **8.2** — the
"8.x" stamp in `examples/progress.example.json`:

| File in the pack repo (at that commit) | What it supplied |
|---|---|
| `config/memorysettings.json` | the pack's own memory thresholds, its recommended-allocation table, and its "how to allocate RAM" link |
| `config/modernfix-mixins.properties` | the two lines the pack sets beyond ModernFix's defaults, and the file's own editing rules |
| `config/alltheleaks.json` | which leak fixes the pack ships on and off |
| `config/spark/config.json` | spark's shipped configuration (`backgroundProfiler`) |
| `config/iris.properties` | the shader config as shipped |
| `kubejs/assets/embeddium/lang/pt_br.json` | the 74 Sodium option keys the pack ships translations for (its own proof of which video settings exist) |
| `config/Mekanism/client.toml`, `config/immersiveengineering-client.toml`, `config/immersiveengineering-server.toml`, `config/integrateddynamics-common.toml`, `config/integratedtunnels-common.toml`, `config/ae2-common.toml`, `config/ars_nouveau-client.toml` | the shipped render, particle, and tick-rate knobs |
| `config/ftbultimine-server.snbt`, `config/quarryplus.toml`, `config/fluxnetworks-server.toml`, `config/mahoutsukai-server.toml` | the shipped chunk-loading and bulk-mining limits |
| `config/crashutilities-server.toml` | the pack's automatic item clear, memory checker, and chunk-purge settings |
| `defaultconfigs/incontrol/spawn.json` | the mob-count caps the pack applies to new worlds |
| `config/ftbquests/quests/chapters/*.snbt` and `config/ftbquests/quests/lang/en_us/chapters/*.snbt` | the verified quest titles, task items, and the lag/TPS/FPS sentences quoted below |
| `config/crash_assistant/modlist.json` | verified mod display names and versions (**493 mods**) |
| `config/crash_assistant/config.toml` | where the pack's crash screen sends a player |
| `MOD_ISSUES.md` | the per-mod issue-tracker list the pack publishes |

## Grounding rules (read before repeating any of this)

- **The in-game quest book (FTB Quests) and JEI are authoritative**, and so is the player's
  own `config/` folder. Everything below is the *shipped default* at pack 8.2. If his file
  or his book says otherwise, his wins — say so and re-check rather than arguing from this
  page.
- **Config values are quoted, never guessed.** A key is shown only where that file states
  it, with the file's own comment where the comment matters. No setting, path, command, or
  item id on this page comes from memory.
- **Quest quotes are the quest author's.** Where the book says something is laggy, that is
  quoted verbatim as *quest text* — it is the pack's opinion at 8.2, not a measurement.
- **Everything not read from the config is flagged as approximate or as judgement.** The
  FPS-vs-TPS split, the order of the triage steps, and anything about the player's own
  hardware are judgement; they are labelled. Effect sizes ("this will gain you X FPS") are
  never stated, because nothing here can measure them.
- **No recipes, no item counts, no new mods.** Nothing to craft appears here, and this page
  never tells a player to install anything: the performance mods are already in the pack.
- **The pack updates often.** These are 8.2's values. If the player's config differs, trust
  his file, and rebuild the chapter list with the pack-update workflow in `SKILL.md`.

## Step 0 — decide which kind of lag it is (judgement, but decide first)

The pack's own quest text uses the two words for two different problems, which is a useful
hint that they are not the same problem:

- **FPS / client lag** — the picture is choppy, breaking a block feels slow, menus stutter.
  The quest book's *Ancient Remnant* entry (Cataclysm) even blames a boss fight for it:
  *"His charge will hurt you and your FPS as it destroys every Block in his path."*
- **TPS / server lag** — the world reacts late: blocks pop back after being broken, mobs
  freeze and jump, machines tick slowly. In singleplayer the same machine runs both sides,
  so both can happen at once. The book's *Bio-Generator* (Mekanism) blames farms:
  *"That is because you buttheads keep making massive Melon Farms that eat Servers TPS!"*

Rough tell (judgement): if the frame counter drops while you stand still in a quiet place,
look at the **client** (steps 1–4). If the world itself feels delayed — or other players
feel it too — look at **what is ticking** (steps 5–7). `F3` shows both the FPS and, on a
server, the tick rate; the mods in step 7 measure properly.

## Step 1 — memory: the pack states its own numbers

`config/memorysettings.json` (memorysettings mod 6.0) ships these values, quoted:

| Key | Shipped value | The file's own description |
|---|---|---|
| `minimumClient` | `6000` | "Set the clients minimum memory warning threshold in MB. Choose the lowest value possible which keeps the pack playable. default:2500, min 2500, max 25000" |
| `maximumClient` | `32000` | "Set the clients maximum memory warning threshold in MB. …" |
| `minimumServer` | `4096` | same wording for the server |
| `maximumServer` | `128000` | same wording for the server |
| `disableWarnings` | `false` | "Disable the memory warnings, default: false" |
| `warningTolerance` | `200` | "Set how many percent the memory is allowed to deviate from the recommended for the system before warning about it, default: 30, max 100" |
| `recommendedMemory` → `"memory values"` | `"16000:8000"`, `"32000:12000"`, `"48000:12000"`, `"64000:12000"` | "Set the recommended memory values based off system memory in MB. [\"system memory:recommended\"]" |

Read the last row as the pack's own allocation table: **a 16 GB machine → 8000 MB, a 32/48/64
GB machine → 12000 MB.** That matches `references/getting-started.md` (8 GB on a 16 GB
system). The same file's `howtolink` points at
`https://apexminecrafthosting.com/how-to-allocate-more-ram/` — the pack's own "how do I
change this" link; where the slider lives is the launcher's business and is approximate
(CurseForge app: Settings → Minecraft → Java Settings → Allocated Memory, per
`getting-started.md`).

Two things to say to a player here, both judgement: allocating **below** the pack's
recommended figure is the common beginner mistake, and allocating **far above** it is not
free either — `getting-started.md` warns that oversized heaps stutter and that the OS plus a
browser need the rest of a 16 GB machine. The shipped `warningTolerance` is `200`, above the
documented `max 100`, so the pack's own chat warning fires very late — do not wait for it
(judgement).

## Step 2 — the performance mods are already installed; there is nothing to add

Verified from `config/crash_assistant/modlist.json` (493 mods), with the modlist's own
display names and versions:

| Mod | Version | What it is here for |
|---|---|---|
| ModernFix | 5.27.24+mc1.21.1 | load time, memory, and general fixes |
| Sodium | 0.8.13+mc1.21.1 | the renderer — the video-settings screen in step 4 |
| Sodium Extra | 0.9.4+mc1.21.1 | extra Sodium options |
| ImmediatelyFast | 1.6.14+1.21.1 | rendering fast paths |
| Invasive Optimizations | 1.0.24 | optimization mixins |
| I'm Fast | 1.0.3 | optimization mod |
| Ferrite Core | 7.0.3 | model/memory footprint |
| All The Leaks | 1.1.13+1.21.1-neoforge | memory-leak fixes (`MOD_ISSUES.md` lists it as "AllTheLeaks (Memory Leak Fix)") |
| memorysettings mod | 6.0 | the allocation warnings in step 1 |
| spark | 1.10.124 | the profiler in step 7 |
| Observable | 5.4.4 | the in-game lag finder in step 7 |
| AI-Improvements | 0.5.3 | cheaper mob AI |
| FastFurnace / Fast Workbench / Fast Suite | 9.0.1 / 9.1.3 / 6.0.7 | recipe-lookup caching |
| FlickerFix | 6.1.0 | z-fighting fix |
| Model Gap Fix | 1.21-1.10 | model gaps |

*(Mod names and versions are the modlist's; the one-line "what it is for" column is
judgement from those names — the pack does not annotate its mod list.)*

**Sodium, not Embeddium.** The 8.2 modlist lists Sodium and no Embeddium entry. The repo
still carries `kubejs/assets/embeddium/lang/ru_ru.json` (7 `embeddium.*` keys only), and its
`pt_br.json` sibling translates **Sodium** keys — so an older doc (including this skill's
`getting-started.md`, now corrected) saying "Embeddium" describes an earlier pack. Check the
in-game mod list, not the folder name.

Two shipped configs worth knowing before touching anything:

- `config/modernfix-mixins.properties` — the pack sets exactly two lines beyond the
  defaults, at the bottom of the file: `mixin.perf.dynamic_resources=true` and
  `stability_level=BETA`. The file's own header says to prefer the in-game config screen,
  that "Changes will, however, require restarting the game to take effect", that a broken
  option is disabled by adding `option=false` at the bottom, and that "You may reset to
  defaults by deleting this file" — deleting it would also drop the pack's two settings, so
  add lines instead of deleting (judgement).
- `config/alltheleaks.json` ships `ingredientDedupe: true`,
  `skipTickingUnloadedFluxNetworks: true`, and `entitySectionCME`, `debugItemStackModifications`,
  `scoreboardDebug`, `debugNativeImage`, `disableEternalStarlightProgress` all `false`. The
  `debug*` keys are diagnostics, not fixes: turn them on only when someone asks for a log
  (judgement).

## Step 3 — shaders: the pack's shader config, as shipped

`config/iris.properties` ships `enableShaders=true` with **`shaderPack=` empty** — i.e.
shaders are enabled but no pack is selected out of the box — plus
`maxShadowRenderDistance=32`, `allowUnknownShaders=true`, `colorSpace=SRGB`. Iris is
1.8.14-beta.1+mc1.21.1 and **Euphoria Patcher** 1.10.5-r5.9.3-neoforge is present (the
patcher for Euphoria Patches shader packs).

So: **if the lag started when a shader pack was installed, that is the first thing to
remove** — turn shaders off in the shader screen and re-test (judgement, but it isolates the
variable). Related shipped detail: `config/ars_nouveau-client.toml` has
`opaque_particles = false` with the note "Disables translucent particles. Disable if your
particles are invisible with shaders." — Ars Nouveau particles and shaders are known to
interact. Which shader pack costs what on a given GPU is system-dependent and is not stated
here.

## Step 4 — video settings (client FPS): which ones exist, verified

The pack repo ships **no** Sodium or video-settings file at this commit: the only render
config there is `config/iris.properties` (step 3), and the only `options.txt` in the whole
repo is `config/fancymenu/options.txt` — the FancyMenu pack-menu settings (`default_gui_scale
= '2'`, `force_fullscreen = 'false'`), not Minecraft's video settings. So the client
performance settings live in the player's own instance and on the in-game **Video Settings**
screen (the click path is approximate; the settings themselves are verified below).

Which settings exist is not a guess: `kubejs/assets/embeddium/lang/pt_br.json` (74 keys)
translates Sodium's own option keys, including the three option pages
`sodium.options.pages.quality`, `sodium.options.pages.performance`,
`sodium.options.pages.advanced`, `sodium.options.performance_impact_string`, and the impact
labels `sodium.option_impact.low/medium/high/extreme/varies`. Each option appears in that
file as `sodium.options.<name>.tooltip` (and for some also `.name` or `.value`), so the
option names below are written as their `<name>` stem:

- `sodium.options.view_distance.tooltip` — the pack's own Portuguese tooltip translates to
  "render distance controls how far terrain is rendered; smaller distances mean less
  terrain is rendered, improving the frame rate" (translation of the shipped string).
- `sodium.options.simulation_distance.tooltip` — translates to "controls how far terrain
  and entities are loaded and processed; smaller distances can reduce the load on the
  internal server and can improve the frame rate" (translation).
- Quality knobs: `graphics_quality`, `particle_quality`, `clouds_quality`, `weather_quality`,
  `leaves_quality`, `smooth_lighting`, `biome_blend`, `entity_distance`, `entity_shadows`,
  `mipmap_levels`, `vignette`, `v_sync`, `fps_limit`.
- Advanced knobs: `use_entity_culling`, `use_block_face_culling`, `use_fog_occlusion`,
  `animate_only_visible_textures`, `chunk_update_threads`, `always_defer_chunk_updates`,
  `cpu_render_ahead_limit`, `use_persistent_mapping`, `translucent_face_sorting`,
  `use_compact_vertex_format`, `use_no_error_context`.

Order to turn things down (judgement): **render distance, then simulation distance, then
particles, clouds, weather, leaves, biome blend, entity distance/shadows.** Simulation
distance also affects the internal server, so it is the one that helps both kinds of lag.
Two pack-specific notes: turning **particles** to minimum will hide the hint the Occultism
quest *Iesnium: Ore of the Otherworld* depends on — *"Note: If you don't see the particle,
make sure your particle settings are turned on!"* — so raise particles again for that one;
and `sodium.console.broken_nvidia_driver` is one of the shipped strings, i.e. the renderer
itself warns about a broken driver in the log when that applies.

## Step 5 — the lag the quest book itself warns about (verified quest text)

The book names its own known offenders. Quote these to a player rather than guessing; the
mod and version are the modlist's, the sentence is the quest's:

| Verified quest title | Quest-book chapter | What the quest text says |
|---|---|---|
| **Pipez** (task `pipez:wrench`; Pipez 1.21.1-1.2.31) | Basic Logistics | *"(Can be laggy when used in mass, still not as laggy as Mekanism pipes though)."* |
| **Mekanism** (task `mekanism:configurator`; Mekanism 10.7.19) | Basic Logistics | *"(These can cause a bit of lag when used in mass so be careful with them)."* |
| **Integrated Dynamics** (task `integrateddynamics:wrench`; IntegratedDynamics 1.37.1) | Basic Logistics | *"(Least laggy pipe solution, these are recommended)."* |
| *(no title in the config)* — task `integrateddynamics:cable` | Basic Logistics | *"The other Pipes act as hoppers… Logic Cables just skip the middle man which also skips a lotta lag."* |
| **Logic Cables** | Integrated Dynamics | the same "skips a lotta lag" sentence, in that chapter's own wording |
| **Bio-Generator** | Mekanism | *"This Generator has been heavily nerfed though, so it is recommened to not use it!"* [sic] *"That is because you buttheads keep making massive Melon Farms that eat Servers TPS!"* |
| *(no title in the config)* — task `pylons:harvester_pylon` (Pylons 5.4.2) | Pylons | *"(Careful when using a lot of modifiers with it like Lilypads or fertilizer as when it goes very fast farming it can be a TPS eater)."* |
| **Simulated Hydroponic Bed** | Industrial Foregoing (1.21-3.6.39) | *"Ever feel like the standard Hydroponic Bed is too laggy? … Allow me to introduce the Simulated Hydroponic Bed."* |
| **Sea Prism** | Chapter 4: Creative | *"Please don't make mass Turtle breeders and mass Guardian slaughter farms. TPS is important!"* |
| **Ancient Remnant** | Cataclysm (L_Ender's Cataclysm 3.33) | *"His charge will hurt you and your FPS as it destroys every Block in his path."* — a boss fight tanking FPS is expected, not a broken install |
| *(no title in the config)* — task `modularrouters:fast_pickup_augment` (Modular Routers 13.2.7) | Modular Routers | *"This upgrade lets the Vacuum Module not wait and immediately pick up the items. Very good for less lag!"* |

Two takeaways that fall out of the book rather than out of this page: **pipe choice is a
performance choice** in ATM10 (the book ranks Integrated Dynamics best and warns about
Pipez and Mekanism in bulk), and **farms that spawn or tick mobs are the pack's named TPS
sink** (melon farms, mass turtle breeders, mass guardian farms, an over-modified harvester
pylon). Redesign those before editing a config file.

## Step 6 — entity spam, item spam, and chunk loading

**Dropped items are capped automatically.** `config/crashutilities-server.toml` (Crash
Utilities 9.0.4) ships `["Item Clear"]` with `enabled = true`, `timer = 5` ("Waiting time
between Checks in Minutes"), `maximum = 1000` ("Do a clear if there are more than X items"),
`warnings = "5,20"`, `titletext = "ITEMCLEAR INCOMING!"` and
`warningtext = "ITEMCLEAR IN % SECONDS"`. On a server, that message is the pack working, not
a bug — and a base that triggers it every five minutes has a drops problem to fix. The same
file ships `["Memory Checker"] enabled = false` (with `heapdump = false`, whose comment reads
"Run /spark heapdump when memory fills up more than 95 % the first time") and
`["Ftb Chunks"] enabled = false` (`days = 7`), so neither of those runs by default.

**Mob counts are capped in new worlds.** `defaultconfigs/incontrol/spawn.json` (InControl
1.21-10.3.0) ships 11 rules, each `{"mob": …, "mincount": N, "result": "deny"}`:
`minecraft:bat` at `5`, and `minecraft:zombie`, `minecraft:skeleton`, `minecraft:creeper`,
`minecraft:spider`, `minecraft:enderman`, `minecraft:cave_spider`, `minecraft:drowned`,
`irons_spellbooks:necromancer`, `creeperoverhaul:cave_creeper`, and
`creeperoverhaul:dripstone_creeper` at `15`. The exact semantics of `mincount` + `deny` are
In Control's own (approximate — check that mod's docs); what is verified is that the pack
ships these caps, i.e. natural spawn pressure is already limited. A player-made farm is not
covered by them.

**Chunk loading is the quiet one.** Verified pieces:

- The Welcome chapter's *Claiming Chunks* quest (task title in the config) teaches
  force-loading: *"To claim a chunk, left click and drag to claim. To force load a chunk,
  shift-left click the chunk. If done properly, you'll see lines across the chunk."* — open
  the map with `M`. Force-loaded chunks keep ticking with nobody there, so un-force-load
  what a base no longer needs (judgement).
- The AE2 quest for `ae2:spatial_anchor` *(no title in the config)* says the Spatial Anchor
  *"simply functions as a chunk loader"* and *"will force-load all the chunks occupied by
  the ME network across all cables and devices, excluding subnetworks, as long as the
  network remains powered."* — a long cable run is a long chunk load (judgement).
- `config/quarryplus.toml` ships `enableChunkLoader = true` (QuarryPlus 21.1.164),
  `config/fluxnetworks-server.toml` ships `enableChunkLoading = false` (Flux Networks), and
  `config/mahoutsukai-server.toml` ships `FAMILIAR_CHUNKLOADS = true`. So the pack's chunk
  loaders are not all on by default — check the actual chunk map rather than assuming.
- `config/ftbultimine-server.snbt` ships `max_blocks: 64` ("Max amount of blocks that can be
  ultimined at once"), which is also what keeps vein-mining from turning into a frame-time
  spike.

## Step 7 — measure instead of guessing

- **spark 1.10.124 is in the pack**, and `config/spark/config.json` ships
  `backgroundProfiler: false` — nothing is profiling in the background by default, so a
  profile has to be started on purpose. Its header links
  `https://spark.lucko.me/docs/Configuration`; use spark's own documentation for the
  subcommands (this page invents none — the only one quoted anywhere in the pack config is
  `/spark heapdump`, in the Crash Utilities comment above).
- **Observable 5.4.4 is in the pack** — an in-game lag finder; use its own in-game docs and
  keybinds rather than a remembered command.
- **memorysettings** reports the allocation problem itself (step 1).
- For **crashes** rather than lag: Crash Assistant 1.11.12 is the pack's crash screen, and
  `config/crash_assistant/config.toml` sets `help_link = "https://discord.gg/allthemods"`.
  The repo's `MOD_ISSUES.md` lists an issue tracker per mod and says, verbatim: *"Report only
  bugs/unintended behaviours that might be exclusive to the mod, **DO NOT** report crashes
  and disconnects, those need to be filtered by us, until we redirect you to the modders
  issue page"*. `config/lmft.json`
  (`disableIngameError: true`) belongs to "Load My F***ing Tags" 1.1.1+1.21.9 and is not a
  performance setting.

## The beginner answer, in order

1. **FPS or TPS?** (step 0). Quiet place, frame counter, `F3`.
2. **Allocation vs the pack's table** (step 1): 8000 MB on a 16 GB machine, 12000 MB on
   32 GB and up — not more "to be safe".
3. **Shaders off** if a shader pack is installed (step 3), then re-test.
4. **Video settings** (step 4): render distance → simulation distance → particles, clouds,
   weather, leaves, biome blend, entity distance/shadows.
5. **Ask what the base is doing** (steps 5–6): pipes in bulk, melon/mob farms, mass
   breeders, an over-modified harvester pylon, drops on the floor, force-loaded chunks.
   Redesign beats tweaking.
6. **Mod render knobs, only if a specific mod is implicated** (below) — e.g. Mekanism's
   `berRange`, Integrated Dynamics' `dynamicShape`, the Immersive Engineering Excavator's
   particles.
7. **Measure** with spark / Observable (step 7) before editing config files; on a server,
   config files belong to the server and most need a restart (judgement).

## Shipped per-mod knobs, quoted (only if a mod is implicated)

| File | Key = shipped value | The file's own comment |
|---|---|---|
| `config/Mekanism/client.toml` | `berRange = 256` | "Range at which Block Entity Renderer's added by Mekanism can render at… Lowering this will likely increase your performance, at the cost of multiblock contents and wind generators 'popping' in" |
| `config/Mekanism/client.toml` | `machineEffects = true`, `multiblockFormation = true`, `radiationParticleRadius = 30`, `radiationParticleCount = 100`, `magneticAttraction = true`, `toolAOE = true` | under `[rendering.particle]`, "Settings for configuring Mekanism's Particles" |
| `config/integrateddynamics-common.toml` | `dynamicShape = true` | "If cable shapes should be determined dynamically. Disable this if FPS issues would occur." |
| `config/integrateddynamics-common.toml` | `cacheCableModels = true` | "If cable models should be cached for rendering optimization." |
| `config/integrateddynamics-common.toml` | `partOverlayRenderdistance = 15`, `partOffsetRenderDistance = 16` | "The maximum render distance for part overlays to render. The higher, the more resource intensive." |
| `config/integrateddynamics-common.toml` | `ingredientNetworkObserverThreads = 4`, `ingredientNetworkObserverEnableMultithreading = true`, observer frequency min `5` / max `40` | "The number of threads that the ingredient network observer can use." |
| `config/integrateddynamics-common.toml` | `safeMode = false` | "When enabled, networks will stop ticking… This can be used to fix crashing networks by temporarily enabling this option." |
| `config/integratedtunnels-common.toml` | `worldInteractionEvents = true` | "If particles should be shown and sounds should be played when tunnels are interacting with the world." |
| `config/integratedtunnels-common.toml` | `inventoryUnchangedTickTimeout = 10` | "How many ticks importers/exporters should sleep until checking targets again when they were previously unchanged." |
| `config/immersiveengineering-server.toml` | `[machines.excavator] particles = true` | "Set this to false to disable the ridiculous amounts of particles the Excavator spawns" |
| `config/immersiveengineering-server.toml` | `[wires] enableWireDamage = true` | "This shouldn't cause significant lag but possibly will." |
| `config/immersiveengineering-client.toml` | `increasedTileRenderdistance = 1.5` | "Increase the distance at which certain TileEntities (specifically windmills) are still visible… set it to 1 for default render distance" |
| `config/ae2-common.toml` | `formationPlaneEntityLimit = 128` | under `[automation]` (no comment in the file) |
| `config/ae2-common.toml` | `[tickRates]` `InterfaceMin = 5` / `InterfaceMax = 120`, `ImportBusMin = 5` / `ImportBusMax = 40`, `ExportBusMin = 5` / `ExportBusMax = 60`, `AnnihilationPlaneMin = 2` / `AnnihilationPlaneMax = 120`, `METunnelMin = 5` / `METunnelMax = 20`, `InscriberMin = 1` / `InscriberMax = 20`, `ChargerMin = 10` / `ChargerMax = 10` | "Min / Max Tickrates for dynamic ticking… adjust with care, non standard rates are not supported or tested." |
| `config/ars_nouveau-client.toml` | `opaque_particles = false` | "Disables translucent particles. Disable if your particles are invisible with shaders." |

Change one at a time and re-measure (judgement). Server-side files on a server belong to the
host and are not the client's to edit; most of these need a restart to apply.

## What this page deliberately does not tell you

- **Any FPS number, gain, or target.** Nothing here can measure the player's machine, so no
  claim like "this doubles your FPS" appears. Anything quantitative is either a quoted
  config value or explicitly labelled judgement.
- **Mods to install or remove.** The performance mods ship with the pack (step 2); adding to
  a 493-mod pack is the player's call and is not advised here.
- **Config keys that are not in the files.** Only keys verified at commit `e5e3d1d83e` are
  named. If a player asks for a setting that is not in the table, the answer is "open that
  mod's in-game config screen / read its config file", never a plausible key name.
- **Recipes, item counts, farm layouts.** Quest text is quoted where it identifies a lag
  source; the *how* belongs to the quest entry and JEI.
- **Server hosting advice.** The server memory thresholds are quoted from
  `config/memorysettings.json`; how to apply them is the host's documentation.
- **Driver, OS, or GPU advice** beyond the shipped `sodium.console.broken_nvidia_driver`
  string that says the renderer reports a broken driver in the log.
- **Anything about a different pack.** These are ATM10 8.2's files; ATM9, ATM10 Lite, and
  ATM10: To the Sky have their own configs.

## Cross-references

- `references/getting-started.md` — RAM allocation for a 16 GB machine, launcher paths, and
  the first-hour setup this page assumes is already done.
- `references/key-mods.md` and `references/progression.md` — what the mods named above are
  for, and where their chapters sit in the four-stage map.
- `references/creative-checklist.md` — the *Sea Prism* quest and its TPS warning in context
  (Chapter 4's prism line).
- `references/boss-checklist.md` — the *Ancient Remnant* fight, whose charge the book says
  costs FPS.
- `SKILL.md` → **Research Grounding** — the rules this page follows, and the pack-update
  workflow that refreshes it when the pack moves past 8.2.
