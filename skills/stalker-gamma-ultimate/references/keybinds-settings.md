# Keybinds, MCM options and settings — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: GAMMA's shipped defaults
`G.A.M.M.A/modpack_patches/appdata/user.ltx` (the profile the installer drops into
`Anomaly/appdata/`; lines 1–341 read in full), the keybind command table in
`G.A.M.M.A. Keybinds fixes/gamedata/configs/ui/ui_keybinding.xml` (mirrored in
*G.A.M.M.A. Close Quarter Combat*), the pack's MCM defaults
`G.A.M.M.A. MCM values - Rename to keep your personal changes/gamedata/configs/axr_options.ltx`
(3 250 lines of `section/option = value` pairs), the progression/difficulty matrix
`G.A.M.M.A. Difficulty Presets Rebalance/…/difficulty.ltx` (`[econ_1..3]`, `[gdiff_1..3]`), the
in-game manual's **Traders Progression**, **Energy Management** and **Arterfacts Reinvention**
articles, the **NPE tutorial** modules (`G.A.M.M.A. Tutorials/gamedata/configs/text/eng/*.xml`),
the `109- MCM Mod Configuration Menu - RavenAscendant` addon, and the wiki's
*Technical-Support-FAQ* (resolution, fonts, ultrawide). Snapshot: GAMMA 0.9.5 @
`ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. Where settings live (and why they reset)

| File / place | What it holds |
|---|---|
| `Anomaly/appdata/user.ltx` | engine + gameplay cvars and **all keybinds** (this is the file the wiki tells you to back up) |
| `GAMMA/mods/G.A.M.M.A. MCM values - Rename to keep your personal changes/…/axr_options.ltx` | every MCM option's default; rename the mod to freeze your personal set |
| `MCM` in-game (main menu → Mod Configuration Menu) | per-mod options, including difficulty/economy switches |
| **Extra Options** menu in-game | the live controls for progression/difficulty multipliers (per `difficulty.ltx`'s own header: "later on you can control them from 'Extra Options' menu in-game") |
| The launcher | renderer, install location, modlist profile |

> "Every time you click 'Install / Update GAMMA' in the GAMMA Launcher, your modlist, settings,
> and mod settings will reset. This is *on purpose*, as it helps repair broken installs.
> Remember to make backups before clicking that button." — wiki FAQ

## 2. Default keybinds (`user.ltx`, verbatim)

Movement and camera:

| Action | Key | Action | Key |
|---|---|---|---|
| forward / back | `W` / `S` | strafe left / right | `A` / `D` |
| crouch | **Left Ctrl** | accel (walk→run) | **Left Shift** |
| sprint toggle | `X` | jump | `Space` |
| lean left / right (`llookout`/`rlookout`) | `Q` / `E` | safe mode / lower weapon (`safemode`) | `B` |
| freelook | `mouse4` | cam zoom in / **mask clean** (`cam_zoom_in`) | `T` |
| item animation (`cam_zoom_out`) | (its own bind) | | |

Inventory, HUD and world:

| Action | Key | Action | Key |
|---|---|---|---|
| inventory | `I` (secondary `TAB`) | torch | `L` |
| night vision | `N` | **detector** (`show_detector`) | `6` |
| use / interact | `F` | drop | its own bind |
| quick use 1–4 | `F1`–`F4` | quick save / quick load | `F5` / `F9` |
| pause | `Pause` | screenshot | `F12` |
| console | `` ` `` | quit | `Esc` |
| **active jobs** (`active_jobs` → the engine token is `kCAPITAL`) | **Caps Lock** | | |

Weapons (this is the part that surprises new players):

| Action | Key | Notes |
|---|---|---|
| fire | `mouse1` | |
| zoom / aim (`wpn_zoom`) | `mouse2` | |
| **reload** (`wpn_reload`) | **`F10`** | *not* `R` — `R` is the unjam key |
| unjam (`kb_unjam` → `custom22`) | **`R`** | Weapon Parts Overhaul binding |
| weapon selector 1/2/3/4/5 | `1`…`5` (slots `wpn_1`, `wpn_2`, `wpn_3`, `wpn_5`, `wpn_6`) | |
| next weapon | `Y` | |
| **ammo-type selector** | **`Y`** | script `key_bindings.kWPN_NEXT` in `item_weapon.script` drives the ammo wheel, and can also toggle a suppressor |
| fire-mode next / prev | `0` / `9` | |
| weapon function (`wpn_func`) | `V` | |
| zoom-dec (`wpn_zoom_dec`) | `KANJI` key | |
| quick melee (`kb_quickmeele` → `custom24`) | `mouse3` | |
| **under-barrel grenade launcher** | **Left Alt** (`custom21`; `use_separate_ubgl_keybind 1`) | 0.9.5 engine feature |
| grenade throw (`kb_grenade_throw` → `custom19`) | `G` | |
| unload all (`kb_unload_all` → `custom15`) | `U` | |
| suppressor toggle (`kb_suppressor` → `custom13`) | `7` | |
| geiger counter (`kb_geiger` → `custom14`) | `8` | |

Companions and PDA:

| Action | Key |
|---|---|
| companion wheel (`kb_companion_wheel` → `custom18`) | `C` |
| teleport companions (`kb_tp_companion` → `custom23`) | `J` |
| companion orders (`kb_companion_combat/movement/move/cover/loot` → `custom1`–`custom5`) | NumPad 1–5 |
| map (`kb_map` → `custom20`) | its own bind |
| scores (`kb_scores`) | `Tab`-family screen |
| radio / music player / volume up-down / next-prev track / switch playlist | `custom7`–`custom12`, `custom16` |
| HUD toggle (`kb_hud` → `custom6`) | NumPad Enter |
| debugger (`kb_debugger` → `custom17`) | `F7` |

The full command list is the pack's `ui_keybinding.xml`; GAMMA ships **G.A.M.M.A. Keybinds
fixes** and **G.A.M.M.A. Close Quarter Combat** precisely because those bindings are
patched into the UI (the two files carry the same command table, and the comment inside says the
author loads them after the two conflicting mods for compatibility). If a key does nothing,
check that file for what the command is called before assuming the feature is missing.

## 3. Gameplay cvars shipped in `user.ltx`

| Setting | Default | Meaning |
|---|---|---|
| `g_game_difficulty` | **`gd_veteran`** | the rank used for difficulty-scaled systems |
| `g_sleep_time` | `9` | hours the "sleep" action will try to sleep |
| `g_dispersion_base` / `g_dispersion_factor` | `1.3` / `1.5` | player-side dispersion tuning (see `references/ballistics-damage.md`) |
| `g_important_save` | `on` | keep the important-save system on |
| `crash_save` / `crash_save_count` | `off` / `10` | keep 10 crash saves around |
| `g_autopickup`, `g_multi_item_pickup` | `on` | the auto-loot conveniences (bodies and containers) |
| `g_use_tracers` | `on` | visible bullet tracers |
| `g_simple_pda` / `g_3d_pda` | `on` / `on` | PDA presentation |
| `time_factor` | `1.000000` | 1:1 time scale |
| `texture_lod` | `0` | texture detail (0 = full) |
| `particle_update_mod` | `0.5` | particle update rate modifier (performance knob) |
| `ai_die_in_anomaly` | `0` | NPCs do **not** die to anomalies (a GAMMA-specific tuning) |
| `ai_use_old_vision` | `0` | new AI vision model |
| `ai_aim_use_smooth_aim`, `ai_aim_predict_time` | `1`, `0.4` | AI aiming behaviour |
| `use_separate_ubgl_keybind` | `1` | UBGL gets its own key (Left Alt) |
| `pseudogiant_can_damage_objects_on_stomp` | `0` | the giant's stomp does not destroy objects |
| `cam_inert` / `cam_slide_inert` | `0.` / `0.25` | camera inertia |
| `mouse_sens` / `mouse_sens_aim` | `0.071` / `1.` | mouse sensitivity |
| `discord_status` / `discord_update_rate` | `on` / `0.5` | Discord rich presence |
| `snd_device` | **`OpenAL Soft`** | audio backend (0.9.5 reworked sound) |
| `snd_efx` | `off` | EFX reverb off by default (the patch notes added *indoor spatial audio with reverb according to room size* — turn this on to hear it) |
| `snd_volume_eff` / `snd_volume_music` | `0.9` / `0.7` | effects / music volume |
| `snd_cache_size` | `256` | sound cache |
| `renderer` | **`renderer_r4`** (DX11) | DX10 is broken; DX8/DX9 need the community modlist |
| `vid_mode` | `1920x1080` | edit this line directly if a resolution change crashes the game (wiki FAQ) |
| `rs_screenmode` | `fullscreen` | |
| `rs_v_sync` | `off` | |
| `rs_c_brightness` / `rs_c_contrast` / `rs_c_gamma` | `0.985` / `0.92` / `1.0` | GAMMA's calibrated picture |
| `r__tf_aniso` | `16` | anisotropic filtering |
| `r3_dynamic_wet_surfaces` | `on` | wet-surface shader |
| `r3_use_dx10_1` | `on` | (used with DX11 renderer) |
| `r4_enable_tessellation` | `off` | tessellation is opt-in (heavy) |
| `r2_ssao*` | mostly `off`/`disabled` | SSAO/HBAO/HDAO off by default |
| `r2_sun_quality` | `st_opt_medium` | sun shadow quality |
| `r2_sunshafts_mode` / `_quality` | `volumetric` / `st_opt_high` | god rays |
| `scope_*` | `scope_factor 0.66`, `scope_blur_inner 0.2`, … | scope rendering (blur, fog, sway) |

These are the values GAMMA's own profile ships — treat them as the intended baseline before
"optimising" anything (see `references/performance-tuning.md` for what actually helps).

## 4. Progression & difficulty presets (`difficulty.ltx`)

The file's own header defines the two axes: economy (`[econ_1]` Tourist, `[econ_2]` Scavenger,
`[econ_3]` Survivalist) and gameplay difficulty (`[gdiff_1]` Easy, `[gdiff_2]` Medium,
`[gdiff_3]` Hard; the header also describes a `gdiff_4` Hardcore design).

**Economy axis** (see the full table in `references/trading-economy.md` §6): multiplier set
covering `goodwill`, `rewards`, `repair`, `upgrade`, `buy`, `sell`, `loots`, `money_loots`,
`stash_chance`, `weapon_degradation`, `battery_consumption`, `random_items`, `scope_chance`,
`arty_chance`, `restock`, `percentage_parts`, `limited_bolts`, `arty_degradation`,
`bkpk_degradation`, `outfit_drops`.

**Gameplay axis**, shipped verbatim:

| Value | gdiff_1 (Easy) | gdiff_2 (Medium) | gdiff_3 (Hard) | Meaning (file's comments) |
|---|---|---|---|---|
| `actor_immunities` | 1 | 2 | 3 | picks the actor immunity preset (`1..4`) |
| `hit_power` | 1 | 1 | 1 | bullet fire-wound factor vs NPCs (0.5 → 3) |
| `dispersion_base` | 2.3 | 2.0 | 1.7 | NPC dispersion base |
| `dispersion_factor` | 3.2 | 2.2 | 1.7 | dispersion scaling |
| `power_loss_bias` | 0.3 | 0.3 | 0.3 | stamina-loss multiplier (`0 → 1`) |
| `max_weight` | 50 | 50 | 50 | base carry weight |
| `thirst` | true | true | true | thirst feature |
| `sleep` | true | true | true | sleep feature |
| `radiation_day` | false | false | false | ambient radiation-day mode |
| `notify_geiger` / `notify_anomaly` | false / false | false / false | **true** / false | HUD proximity notifications |

Note what is **identical** across difficulties: `hit_power`, `power_loss_bias`, `max_weight`,
`thirst`, `sleep`, `radiation_day` — GAMMA keeps those constant and moves the dials that matter
for fairness (`actor_immunities`, dispersion) instead. `[exclude_from_multi]` lists the items
that are excluded from multiplayer: the PDAs and all twelve faction patches.

## 5. MCM: the option groups that matter

`axr_options.ltx` is 3 250 lines of `group/subgroup/option = value` defaults. The groups a
GAMMA player actually touches:

**A-Life / world (`alife/*`)** — the "A-Life" of the Zone:

| Option | Default |
|---|---|
| `alife/general/alife_mutant_pop` | **1.5** |
| `alife/general/alife_stalker_pop` | 1 |
| `alife/general/dynamic_anomalies` | **true** |
| `alife/general/dynamic_relations` | false |
| `alife/general/excl_dist` | 75 |
| `alife/general/offline_combat` | full |
| `alife/general/heli_spawn` | false |
| `alife/general/war_goodwill_reset` | false |
| `alife/event/emission_state` / `_frequency` / `_warning` / `_task` / `_fate` | true / **24** / `siren_radio` / true / `explode` |
| `alife/event/psi_storm_state` / `_frequency` / `_warning` / `_task` / `_fate` | true / **48** / `siren` / true / `turn_to_zombie` |
| `alife/dynamic_news/*` | a dozen toggles (loot, surge, weather, time, nearby activity…) all `true`, `message_duration = 10` |

**Warfare (`alife/warfare/*`)** — per-faction warfare tuning with one block per faction
(`army`, `bandit`, `csky`, `dolg`, `ecolog`, `freedom`, `greh`, `isg`, `killer`, `monolith`,
`renegade`, `stalker`, `zombied`) each carrying `base_count_modifier`, `base_priority`,
`expansion_aggression`, `flag_priority`, per-level priorities and `keep_last_base`. Defaults
ship **mild** (`base_count_modifier = 0`, `keep_last_base = false`) — the Warfare addon is
optional and normally disabled.

**Other groups visible in the defaults** (each is an addon's own options page):
`auto_looter/*` (`proximity_looting_refire_time = 2`), `dotmarks/*` (interaction dot timing),
`drx_da/*` (`delete_dynamic_anomalies = false`), `extra_level_transitions/*`, `fddar/*`
(body-search times), `fftd/*` (fast-travel config: `gen/combat_timeout = 10`,
`gtcfg/add_travel_time = true`), `ssfx_module/*` (screen-space shaders),
`wpo/*` (Weapon Parts Overhaul), `aol_hf/*` (hideout furniture: `use_ingame_time = false`),
`ap/*` (`causes/*` decay times of 300 s for basekill/massacre systems).

## 6. Which addons own which settings

| Setting you want to change | Where to look |
|---|---|
| Difficulty, economy, thirst/sleep, carry weight, dispersion | **Extra Options** in-game, or `difficulty.ltx` |
| Anomaly/mutant/stalker populations, squad sizes, spawn templates | **ZCP** (`smr_*` options) and `axr_options.ltx`'s `alife/*` |
| Weather, time, emissions | MCM weather/atmosphere pages (`ssfx_module`, weather MCM) |
| HUD (dot marks, prompts, hunger/thirst/sleep bars) | `164- Hunger Thirst Sleep UI 0.71`, `dotmarks/*`, `336- Item UI Improvements`, `G.A.M.M.A. UI` |
| NPE tutorials on/off | MCM → **NPE Modules → G.A.M.M.A.** (each NPE card's own text tells you: "You can see this tutorial again by going into Mod Config Menu (MCM) > NPE Modules > G.A.M.M.A. and by unticking the tutorial") |
| Companion behaviour | MCM companion options (`302- Minimalist companion UI`, `G.A.M.M.A. Companions Rework`) |
| Fan/profanity, animation replies | `wpo/profanity_timeout = true` and the Weapon Parts Overhaul page |
| Fonts (1440p/4K) | enable **Tactical Fonts for Anomaly** (wiki FAQ) |
| Ultrawide / 16:10 | enable the optional **Dynamic Aspect Ratio Tweaks** (it ships with GAMMA, *after the "End of List" separator*); 4:3 is **not** supported |
| Resolution | `vid_mode` in `user.ltx` if the in-game change crashes |
| Gunfire volume | 0.9.5 added a **"Gunfire Volume" setting slider** |

## 7. Backups that actually preserve your settings

The wiki's procedure, condensed:

1. **Delete nothing**: back up `Anomaly/appdata/user.ltx` (settings + keybinds).
2. Back up `Anomaly/appdata/savedgames`.
3. Rename `G.A.M.M.A. MCM values - Rename to keep your personal changes` to something like
   *My MCM Backup* — after an update it lands at the bottom of the modlist, disabled; re-enable
   it to restore your MCM options.
4. Copy the default **G.A.M.M.A.** profile in MO2 to a personal profile **before** you start
   changing the modlist, and work on the copy.

**These backups are snapshots** — they never update, and major version updates invalidate them
by design.

## 8. Quick answers

| Question | Answer |
|---|---|
| How do I reload? | **F10** — `R` is unjamming. |
| How do I switch ammo type? | **Y** (the ammo wheel is driven by `kWPN_NEXT`). |
| How do I use the under-barrel launcher? | **Left Alt**. |
| How do I open a detector? | **6** (`show_detector`). |
| Where is the active-jobs list? | **Caps Lock**. |
| How do I switch off a tutorial? | MCM → NPE Modules → G.A.M.M.A. |
| Where do I change difficulty/economy mid-game? | In-game **Extra Options** menu (the values come from `difficulty.ltx`). |
| Why did my settings reset? | Every launcher update resets modlist, settings and mod settings on purpose. |
| What renderer should I use? | DX11 (`renderer_r4`); **DX10 is broken**; DX8/DX9 requires the community DX8/DX9 modlist. |
| Can I play at 21:9 or 4K? | Yes — enable Dynamic Aspect Ratio Tweaks for ultrawide/16:10; 4:3 is unsupported; if the resolution change crashes, edit `vid_mode`. |
| Where are the MCM defaults I should back up? | `G.A.M.M.A. MCM values - Rename to keep your personal changes/…/axr_options.ltx`. |
| Is ambience/reverb on? | `snd_efx` ships `off`; GAMMA added indoor spatial audio, so you may want it on. |
| Which sound device? | `OpenAL Soft` by default. |

Cross-references: install-time renderer choices and the launcher →
`references/installation-setup.md`; what the difficulty multipliers actually do to money →
`references/trading-economy.md`; dispersion and damage cvars →
`references/ballistics-damage.md`; performance-oriented cvars →
`references/performance-tuning.md`; MCM/ZCP conflicts and modlist ordering →
`references/modding-guide.md`; ZCP populations → `references/mutants.md`; how the preset
multipliers land on your body (thirst, sleep, radiation days, stamina) →
`references/survival-mechanics.md`; the goodwill multiplier these presets apply to faction
standing → `references/factions.md`; and what to check when a settings file itself is the
problem (resets after an update, `ModOrganizer.ini`, corrupted `user.ltx`) →
`references/troubleshooting.md`.
