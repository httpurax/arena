# Performance tuning — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: `Patchnotes.md` (0.9.5 **Engine**, **Performance** and **Newly added
addons** sections; the 0.9.4 engine line; and the historically-noted optimisations), GAMMA's
shipped profile `G.A.M.M.A/modpack_patches/appdata/user.ltx` (the graphics cvars that ship with
the pack), the wiki's *Technical-Support-FAQ* ("This does not cover performance issues" — it
explicitly defers those to the Discord, so this page sticks to the pack's own data), GAMMA's
README requirements, and the modlist's own performance addons (in the launcher's addon list).
Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. What engine you are running

GAMMA 0.9.5 upgraded the runtime: **"GAMMA now uses the test branch of the MultiThreading (MT)
modification of the Anomaly engine by Demonized (currently version `MT-TEST_2026.5.5`).
Depending on your rig, you should have much better performance overall and fewer stutters."**
(The previous release line, 0.9.4, used `STALKER-Anomaly-modded-exes_2025.7.12`.)

Practical consequences of the MT engine:

| Point | Detail |
|---|---|
| Threading | multi-threaded rendering/streaming — CPU core count matters more than it used to |
| Prefetching | GAMMA ships a **Meatchunk prefetcher**; 0.9.5's note is short and absolute: **"(17 Gb required minimum)"** |
| 1st-person legs | 0.9.5's engine list says **"Disabled 1st Person Legs mod to use In Engine version instead"** — the legs are engine-side now |
| Renderer | DX11 (`renderer_r4`) is the supported path; **DX10 is broken**, DX8/DX9 need the community modlist |

If you are on an older GAMMA, "it stutters" is the historical answer: the 0.9.5 engine swap is
the single biggest performance change the pack has shipped.

## 2. What 0.9.5 actually optimised

Verbatim from the Performance section and the general description:

- **`grok_gotta_go_fast` script performance increase**
- **`callbacks_gameobject` optimisation crash fix**
- **Updated Meatchunk prefetcher (17 Gb required minimum)**
- **reduced Rostok population**
- **Meat spoiling performance fix (once every 10s instead of every frame)**
- **Optimised inventory management and items transfers**
- Plus, from the general description: the **Inventory Open Lag Reducer by Sea-Ex**, **Inventory
  Antifreeze by Demonized**, "fast transfer code optimizations", and "some scripts running every
  frame were optimized as well to use other, less demanding callbacks".
- And: **"Interaction Dot Marks enabled again since the performance impact is now mostly
  fixed"** — i.e. that feature was off for a *performance* reason in an earlier release.
- The pack is honest about the trade-off: **"Some of the newly added features impact performance
  slightly, and these will be investigated further after the 0.9.5 patch release."**

Older-but-still-relevant optimisations in the same file: "Spreaded timed scripts execution over
time to avoid stutters", "Optimised Guns World models by Burn, fixes many FPS issues in certain
maps like Agroprom, Dead City and Rostok", and "Potentially reduced prefetcher memory footprint".

## 3. The settings that matter (and what GAMMA ships)

Baseline first — these are the pack's own defaults in `user.ltx`, i.e. what the authors
consider playable:

| Cvar | GAMMA default | Why it matters |
|---|---|---|
| `renderer` | `renderer_r4` | DX11 |
| `r4_enable_tessellation` | **`off`** | tessellation is the single heaviest optional feature |
| `r2_ssao` / `r2_ssao_mode` | `st_opt_off` / `disabled` | SSAO/HBAO/HDAO off by default |
| `r2_sun_quality` | `st_opt_medium` | sun-shadow quality |
| `r2_sunshafts_mode` / `_quality` | `volumetric` / `st_opt_high` | god-rays; drop these first if you need frames |
| `r3_dynamic_wet_surfaces` | `on` | wet shader |
| `r__enable_grass_shadow` | `off` | grass shadows are expensive |
| `r2_sun_details` | `off` | per-detail sun pass |
| `texture_lod` | `0` | texture detail (raising the number lowers quality *and* VRAM use) |
| `particle_update_mod` | `0.5` | particle update rate |
| `r__optimize_dynamic_geom` | `1` | geometry optimisation |
| `r__optimize_shadow_geom` / `r__optimize_static_geom` | `on` / `1` | geometry optimisation |
| `r__use_precompiled_shaders` | `on` | avoids shader compilation hitches |
| `r__tf_aniso` | `16` | anisotropic filtering (cheap on modern GPUs) |
| `snd_cache_size` | `256` | sound cache — large values trade RAM for fewer audio hitches |
| `snd_efx` | `off` | EFX/reverb processing |
| `cam_inert` / `cam_slide_inert` | `0.` / `0.25` | camera smoothing |

**Where to change them:** in-game graphics options for the standard ones; `user.ltx` directly
for the ones the menu does not expose. The wiki's only performance-adjacent note is that if a
resolution change crashes the game you should edit `vid_mode` in `user.ltx` by hand.

## 4. The pack's own performance addons (in the launcher list)

| Addon | What it addresses |
|---|---|
| **Inventory Open Lag Reducer** (Sea-Ex) | the pause when opening containers/inventory |
| **Inventory Antifreeze** (Demonized) | the same class of hitch, engine-side |
| **Turn this on if you stutter** | the pack literally ships a toggle with this name |
| **G.A.M.M.A. No PDA Stutters** | PDA-related hitches |
| **Serious Workshop optimization** (0.9.4: "Workshop optimization by Serious") | crafting/workshop UI |
| **Dark Valley Bandit Base FPS optimisation** | an optional addon that *darkens* the base to win frames — the patch notes are candid: "the boost isn't tremendous and the base becomes very dark" |
| **Lower Weapon Sprint Optimized** (+ "Black list guns list") | weapon-lowering animation cost |
| **Squad Filler** (xcvb) | fills squads with fewer actor-level objects |
| **Cypret's SafeSpawn** | replaced "Spawning Shenanigans Prevention" — spawn safety without the overhead |
| **Distant gunfire audio rework** / audio caches | audio hitches, not FPS |
| **G.A.M.M.A. Reliable Animation Settings** | animation-related settings |
| **Optional Modern UI font**, **Tactical Fonts** | readability (not perf) but commonly confused with it |

Three things the pack's list implies: **stutter (frame pacing) is the community's main
complaint, not raw FPS**; the fix is usually the inventory/PDA/spawner layer, not the renderer;
and GAMMA deliberately keeps several "turn this off" addons shipped-and-disabled rather than
pre-installing them.

## 5. Performance-relevant gameplay knobs (often the real answer)

If your problem is "the game is fine until X happens", the cause is usually population, anomalies
or shadow-casting entities:

| Knob | Where | Effect |
|---|---|---|
| `alife/general/alife_mutant_pop` (default **1.5**) and `alife_stalker_pop` (1) | MCM (`axr_options.ltx`) | the total number of simulated squads — the biggest single FPS lever in the field |
| `alife/general/excl_dist` (75) | MCM | how far from the player the simulation runs detail |
| `alife/warfare/*` | MCM | Warfare's per-faction expansion drives the largest sustained populations; the defaults ship it effectively calm (`base_count_modifier = 0`, `keep_last_base = false`) |
| `alife/general/dynamic_anomalies` (true) | MCM | dynamic anomaly spawning (see `references/anomalies.md`) |
| ZCP squad size / variance / spawn templates | ZCP menus | see `references/mutants.md` — and read the **"Not enough IDs"** warning before raising them |
| Emission/psi-storm frequency (24 / 48) | MCM | blowouts kill off squads and change the population curve |
| `restock` (24 h vs 48 h) | economy preset | trader refresh cadence, not FPS — but it changes how much simulated trading runs |
| `battery_consumption`, `weapon_degradation` | economy preset | item churn volume |

## 6. Resolution, aspect ratio and display

| Topic | Facts |
|---|---|
| **Ultrawide / 16:10** | supported via the optional **Dynamic Aspect Ratio Tweaks**, which ships with GAMMA *after* the "End of List" separator — enable it in MO2 |
| **4:3** | **not supported** |
| **2K/4K** | fine, but if changing resolution in-game crashes, edit `vid_mode` in `Anomaly/appdata/user.ltx` |
| **Fonts at 1440p/4K** | enable **Tactical Fonts for Anomaly** for your resolution |
| **Fullscreen/exclusive** | `rs_screenmode fullscreen`, `rs_v_sync off` by default; windowed mode with a borderless tool is a common stutter cure on multi-monitor setups |
| **DX10** | **"DX10 is broken. Do not play with it."** (wiki) |
| **DX8/DX9** | follow the dedicated DX8/DX9 modlist project (the wiki links it); do not mix those addons into a DX11 list |

## 7. Disk, RAM and page-file reality

- The launcher's own requirement is **at least 150 GB free**, ideally **175–200 GB** (wiki); the
  install is Anomaly + GAMMA + the mods, and the pack's addon count is in the hundreds.
- The **prefetcher wants ~17 GB** (`Meatchunk prefetcher (17 Gb required minimum)`).
- Keep the two folders **on the same drive**, **not in a restricted location**, and **out of
  OneDrive/Documents/Program Files** (see `references/installation-setup.md` §3) — those rules are
  about correctness, but they also prevent the classic "slow, stuttering install on a synced
  virtualised folder" problem.
- **Antivirus exclusions** matter for more than installation: real-time scanning of a
  several-hundred-thousand-file modpack is a permanent performance tax.

## 8. Diagnosing your own stutter (a GAMMA-shaped checklist)

1. **Identify the trigger.** Opening inventory → the inventory addons. PDA → `No PDA Stutters`.
   Entering Rostok/Agroprom/Dead City → historically the gun world models and Rostok population
   (both addressed). First shot after loading a shader → `r__use_precompiled_shaders`.
2. **Check the population.** Drop `alife_mutant_pop` from 1.5 to 1.0 and see whether the field
   stutter changes. If it does, the problem is simulation, not rendering.
3. **Check the engine.** Confirm you are on 0.9.5+ (`MT-TEST_2026.5.5`); anything older is a
   different baseline.
4. **Check VRAM.** Lower `texture_lod` (raise the number), disable `r2_sunshafts_*`,
   `r3_dynamic_wet_surfaces`, `r4_enable_tessellation`.
5. **Check prefetch/RAM.** 17 GB-class prefetch plus the game plus mods; if you are paging, no
   graphics tweak will save you.
6. **Check the modlist.** Every addon you added yourself is a candidate; see
   `references/modding-guide.md` §6 for the safe bisect procedure.
7. **Do not chase "FPS configs" that edit `appdata` while the game runs** — `user.ltx` is
   rewritten on exit and your changes will silently vanish.

## 9. Quick answers

| Question | Answer |
|---|---|
| What engine does 0.9.5 use? | The MultiThreading test branch by Demonized, `MT-TEST_2026.5.5`. |
| How much RAM does the prefetcher want? | The pack states **17 GB minimum**. |
| How much disk? | ≥150 GB free, 175–200 GB recommended. |
| Which renderer? | DX11; DX10 is broken; DX8/DX9 only via the community modlist. |
| Biggest single FPS lever? | Population — `alife_mutant_pop` (1.5) and the Warfare/ZCP spawn settings. |
| What ships disabled for performance reasons? | Tessellation, SSAO/HBAO/HDAO, grass shadows, EFX, `r2_sun_details`, and previously the Interaction Dot Marks. |
| What did 0.9.5 fix about stutter? | Inventory open lag, inventory "antifreeze", transfer code, per-frame script callbacks, meat spoiling tick, Rostok population. |
| Is there an official "performance guide"? | The wiki FAQ explicitly does **not** cover performance issues and points to the Discord; the pack's own answers are the patch notes and the shipped addons. |
| Where do I disable ReShade/SSFX? | MCM → `ssfx_module/*` (e.g. `ssfx_pp/ssfx_bloom/use_weather_mcm`), and via the optional screenspace-shaders install. |
| Does ultrawide hurt performance? | It costs fill-rate (more pixels); enable Dynamic Aspect Ratio Tweaks and drop sunshafts/tessellation if needed. |

Cross-references: the graphics/MCM cvars in full → `references/keybinds-settings.md`;
population systems and the ID limit → `references/mutants.md` and `references/anomalies.md`;
installation requirements and the two-folder rules → `references/installation-setup.md`;
modlist hygiene and bisecting a bad addon → `references/modding-guide.md`; crash triage →
`references/troubleshooting.md`.
