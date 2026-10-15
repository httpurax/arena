# Anomalies, dynamic zones and emissions — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: GAMMA's **zone configs** (`158- ABF - Jurkonov/gamedata/configs/zones/`,
`234- Dynamic Anomalies Overhaul - Demonized/…/zones/`,
`G.A.M.M.A. Actor Damage Balancer/…/zones/`, `G.A.M.M.A. Burnt Fuzz Balance/…/zones/`,
`G.A.M.M.A. Radiation Dynamic Areas/…/zones/`), the artefacts spawn-group config
`G.A.M.M.A. Artefacts Reinvention/…/items/settings/artefacts.ltx` and its per-map anomaly-field
references, the PDA manual articles **Radiations** (`article_gamma_radiation_text`) and
**Artefacts Reinvention**, the NPE ammo/artefact tutorials, the psionic/emission options in
`G.A.M.M.A. MCM values …/gamedata/configs/axr_options.ltx` (`alife/event/*`,
`alife/general/dynamic_anomalies`), ZCP's anomaly options and FAQ, and `Patchnotes.md` 0.9.5
(Gameplay/Balance/Crafting/Bugfix). Snapshot: GAMMA 0.9.5 @
`ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. The anomaly families that exist in GAMMA's configs

Every zone in GAMMA is one of a small number of engine classes. The shipped zone files and
their classes (this is the ground truth for "what kinds of anomaly are there?"):

| Zone file | Engine class | What it is in play |
|---|---|---|
| `zone_mine_gravitational.ltx` | `ZS_MINCE` / `ZS_GALAN` / `ZS_MBALD` | the gravitational "mincer"/vortex family; strong/average/weak variants, `max_start_power` **3.2 / 2.4 / 1.7 / 1.0** |
| `zone_mine_sphere.ltx` | `ZS_GALAN` | the sphere anomaly (Dynamic Anomalies Overhaul ships it explicitly), `max_start_power 0.65` |
| `zone_mine_electric.ltx` | `ZS_MBALD` | electro anomalies with weak/average variants, power values **0.66 → 1.00** |
| `zone_mine_thermal.ltx` | `ZS_MBALD` | thermal/burn anomalies with weak/average/strong sequences (0.4 → 1.0) |
| `zone_mine_acidic.ltx` | `ZS_MBALD` | acid anomalies |
| `zone_mosquitobald.ltx` | `ZS_MBALD` | "mosquito bald" — the swarm-type anomaly; power values from 1.30 to 3.30 across variants |
| `zone_burningfuzz.ltx` | `ZS_BFUZZ` | burnt fuzz (electrically charged fuzz), power 0.27 in the ABF set, with a weak variant (`zone_burning_fuzz_weak`) |
| `zone_hvatalka.ltx` | `ZS_BFUZZ` | GAMMA's *hvatalka* ("grabber") anomaly, `max_start_power 1.5` |
| `zone_fireball.ltx` | `ZS_TORRD` | the fireball field, with **electric** and **acidic** variants (`fireball_electric_zone`, `fireball_acidic_zone`), power 1.0 |
| `zone_field_acidic.ltx` | `ZS_RADIO` | **dynamic field** area (acid), four power steps 0 → 0.19, `attenuation 0.46` |
| `zone_field_thermal.ltx` | `ZS_RADIO` | dynamic thermal field, steps 0 → 0.50, `attenuation 0.54` |
| `zone_field_psychic.ltx` | `ZS_RADIO` | dynamic psi field, steps 0 → 1.24, `attenuation 0.5` |
| `zone_field_radioactive.ltx` | `ZS_RADIO` | dynamic radiation area, with a long ladder of intensities (0.0091 → 0.102 and up), shipped by **G.A.M.M.A. Radiation Dynamic Areas** |

Two families are visible in that table and they behave very differently:

- **`ZS_*` "mine"-style zones** (gravitational, electric, thermal, acidic, sphere, hvatalka,
  burnt fuzz, fireball): discrete hazards with strong/weak variants. These are the classic
  "anomaly" you circle with bolts and route around.
- **`ZS_RADIO` fields** (acidic / thermal / psychic / radioactive): **soft-edged dynamic
  areas** with graded power that you can (sometimes) walk through quickly, taking damage
  proportional to exposure. `G.A.M.M.A. Radiation Dynamic Areas` ships both the radioactive
  field definitions and the script (`gamma_dynamic_radiation_areas_from_arzsi.script`) that
  drives them; `radioactive_water_settings.ltx` covers radioactive water.

## 2. Dynamic anomalies (0.9.5's headline anomaly change)

`alife/general/dynamic_anomalies = true` in the pack's MCM defaults. What that does in 0.9.5:

- "**Much higher chance of dynamic anomalies artefacts spawn, but more T0 artefacts spawn
  there**" — dynamic anomalies are now the *routine* way to find artefacts, at the cost of
  mostly junk-tier results.
- "Slight boost to regular field artefacts spawn" — the fixed fields still matter.
- "**Artefacts despawn after 5 in game days if not picked** (considered stuck)" — if you clear
  a field and leave loot behind, it rots.
- "Crafting artefact using low cond artefact fix", "Artefacts on Belt cannot be used for
  crafting", "Artefact melter does not use belt artefacts and the UI properly reset" — the
  0.9.5 crafting fixes that mostly exist because of the dynamic-anomaly economy.
- The manual's frame: "**New artefact spawning system: artefacts spawn randomly in the current
  map of the player in anomalous fields so be sure to check them whenever you move around
  them!** Rare artefacts also respawn in the labs after emissions."

The `234- Dynamic Anomalies Overhaul - Demonized` addon (with `drx_da_main.script`,
`kd_tree.script`, `speed.script`) is the implementation: it re-writes zone configs for
electric and sphere anomalies to make them spawn/spin dynamically.

## 3. Radiation

The manual's *Radiation* article (`article_gamma_radiation_text`) is the source of truth for
player-facing behaviour:

- GAMMA "features **dynamic radiation** and a revamped radiation damage system"; **new random
  radiation patches are spawned when starting a new game**.
- "Radiation will slowly reduce your health (**much slower than Vanilla**) and will reduce your
  **max stamina**."
- "The more irradiated you are, the more likely **critical organs will be damaged**. This
  results in the player character coughing and losing a significant amount of health."
- The **radiation meter sits in the bottom-left corner** of the screen. "If it starts being
  filled, you just hit a radiation patch, try to back track to avoid traversing it."
- "**Radiation can also come from artefacts that are not in a container.**"
- Cures: "anti-rad drugs, cigarettes, tobacco, water, or alcohol". Prevention: "rad protecting
  drugs".
- **North = worse**: "The more to the north you go, the more dangerous the radiations will be.
  Be sure to have a good gas mask before going into northern areas. Entering the Army
  Warehouses or areas further North **without a gas mask or proper anti-radiation medication
  can kill you if you hit just one bad radiation patch**. Keep in mind that running into a
  strong radiation area will likely **make you unable to move, trapping you**."

Config side: intensities in `zone_field_radioactive.ltx` start as low as 0.0091 and run to
0.102+ across the "very weak → weak → average → strong" ladder, with `attenuation 0.5` for the
field and 0.1 for some variants. `G.A.M.M.A. Radiation Effects Overhaul` and
`radioactive_water_settings.ltx` tune the presentation and water hazard.

The **difficulty** layer includes a `radiation_day` toggle per gameplay preset (all three
shipped presets have `radiation_day = false`; when a player enables it, "the air will be
radiated, radiation power depends on many factors such as the weather, time cycle, the outfit
and helmet player is wearing and their protections against radiation" — `difficulty.ltx`
comments). Radiation damage also interacts with the **psy health** model — see
`references/survival-mechanics.md`.

## 4. Psy and psi storms

- Global options in the MCM defaults: `alife/event/psi_storm_state = true`,
  `alife/event/psi_storm_frequency = 48`, `alife/event/psi_storm_warning = siren`,
  `alife/event/psi_storm_task = true`, and **`alife/event/psi_storm_fate = turn_to_zombie`**.
  In other words, by default a psi storm *turns people into zombies* rather than killing them.
- Emission options beside them: `alife/event/emission_state = true`,
  `alife/event/emission_frequency = 24`, `alife/event/emission_warning = siren_radio`,
  `alife/event/emission_task = true`, **`alife/event/emission_fate = explode`** (the classic
  behaviour: anything unhidden is destroyed).
- GAMMA's own addons for this: **"G.A.M.M.A. Psy rework"**, **"G.A.M.M.A. Psy Fields in the
  North"**, **"G.A.M.M.A. Short Psi Storms"**, **"G.A.M.M.A. Radiation Dynamic Areas"**, and the
  community favourite **"Decoy phantoms spawn when psy health is low but they do not cause Psy
  damage (spooks)"** (0.9.5 Gameplay).
- The NPE healing tutorial defines the psy-health failure state: "You die if your Main Health
  reaches 0, if your Head Health reaches 0, if your Torso Health reaches 0 **or if your Psy
  Health reaches 0**", and lists the psy-restoring item families (psy-block, sleeping pills,
  etperazine, marijuana/joints, certain beverages, artefacts).

ZCP exposes an **Anomalies** menu (`ui_st_smr_anomalies.xml`) for players who want to change
how much of the Zone is anomalous.

## 5. Emission/psi-storm behaviour in practice

| Thing to know | Detail |
|---|---|
| Warnings | The pack's defaults warn by **siren** (psi storm) and **siren + radio** (emission), and can post a task (`emission_task`/`psi_storm_task = true`) |
| Frequency | Defaults are **every 24** (emission) and **every 48** (psi storm) in the engine's time units as configured in MCM; both are player-editable |
| Shelter | Under a roof, in a basement, in a lab — the same rules as Anomaly: if you are exposed when the blowout lands, `emission_fate = explode` applies |
| Mutants after emissions | "Rare artefacts also respawn in the labs after emissions" — emissions refresh lab artefact spawns |
| Corpses after emissions | **"NPCs Die in Emissions for Real" is disabled in 0.9.5**, so do not assume every exposed NPC dies |
| Pre-blowout atmosphere | **"11- Preblowout Murder"** and **"Demonized FDDA New Time Events"** are shipped — the weather/ambience before a blowout is intentionally ominous |
| Safe transitions | **"263- Safe Areas Transitions - Darkasleif"** exists because anomaly/safe-area edges are lethal when you sprint blindly |
| The community trick | For **electro** anomalies, throw a **bolt to discharge** the anomaly, then run past (Steam "Rookie's Guide" — community source, but consistent with bolts being the general-purpose anomaly probe) |

## 6. Anomaly fields are artefact factories

The link between anomalies and artefacts is one line of data: `artefacts.ltx` defines artefact
**groups** by element family and region (`af_fire_t1/t2/t3`, `af_chem_*`, `af_elec_*`,
`af_grav_*`, `af_psi_*`, plus the "smart mix" groups), and the per-map anomaly-field configs
(`configs/scripts/<map>/anomaly/*_anomal_zone.ltx`, e.g. `agr_2c_01_hg_anomal_zone.ltx`,
`esc_smart_terrain_5_4_anomal_zone.ltx`) reference those groups. So:

| Anomaly family you are standing in | Artefact families you can roll |
|---|---|
| Fire / thermal | `af_fire_t1`–`t3` (Itcher, Pin, Cristall, Fireball, Fire, Baloon …) |
| Chemical / acid | `af_chem_t1`–`t3` |
| Electric / electro | `af_elec_t1`–`t3` (Battery, Sparkler, Ring, Moonlight, Flash, Ice) |
| Gravitational | `af_grav_t1`–`t3` (Medusa, Night Star, Soul, Vyvert, Gravi, Gold Fish, Full Empty) |
| Psi | `af_psi_t1`–`t3` |
| Mixed fields / north | the `af_class_*` smart mixes and `af_class_north_all` |

See `references/artifacts.md` for the full group membership and tier logic.

## 7. Surviving the Zone's geometry

| Addon (shipped) | Why it exists |
|---|---|
| **Fairer Thermal Anomalies** (`216034`, community) | thermal damage feels unfair to many players |
| **G.A.M.M.A. Burnt Fuzz Balance** | tuning the fuzz family (power 0.27 in ABF's file) |
| **Disable Burnt Fuzz** (`207876`, community) | for people who hate it |
| **Particles Cinematic VFX 3.5** | visual rework of anomaly particles |
| **G.A.M.M.A. Light Sources Spawner**, **Ayra's Better Glowsticks Position** | torches/glowsticks for dark anomaly work |
| **"Turn this on if you stutter"**, **"G.A.M.M.A. No PDA Stutters"** | anomaly-heavy scenes are the worst-case performance scenario (see `references/performance-tuning.md`) |
| **G.A.M.M.A. Agroprom Underground Transition Randomizer** (0.9.5: "Randomized Agroprom Underground entrance") | the map's entrance is randomised per playthrough |
| **Safe Areas Transitions** | safe-area edges you must respect |

## 8. Gamma's own recommended field procedure (assembled from the sources above)

1. **Before you enter**: check the weather/time (emission/psi storm schedule), equip a
   detector, and check your anti-rad and psy meds.
2. **Chart the field with bolts** — limited by the `limited_bolts` difficulty flag (true in
   all three presets), which is why bolts are an economy: a `bolts_pack` yields **2** bolts and
   the Ecologists sell it (`bolts_pack = 2, 1` in `trade_ecolog_sakharov.ltx` /
   `trade_ecolog_hermann.ltx`). Throw, watch, walk.
3. **Discharge what you can** (electro/anomaly families that allow it), and *never* sprint into
   an un-charted field.
4. **Watch the detector's cadence** — faster beeps = closer.
5. **Watch the radiation meter (bottom-left)**; if it fills, **backtrack** rather than pushing
   through, and remember a strong patch can trap you in place.
6. **Cure with the right drug** (anti-rad, cigarettes/tobacco, water, alcohol for radiation;
   psy-block/etperazine/artefacts for psy).
7. **Extract, then process**: fuse junk, empower duplicates, sell duplicates to the Ecologists.
8. **If an emission catches you**, be under a roof/basement/lab — `emission_fate = explode`.

## 9. Quick answers

| Question | Answer |
|---|---|
| What anomaly types exist? | Gravitational (vortex/sphere/mincer), electric, thermal, acidic, psi, mosquito bald (swarm), burnt fuzz, hvatalka ("grabber"), fireball (with electric/acidic variants), and the dynamic `ZS_RADIO` fields: acidic, thermal, psychic, radioactive. |
| Why is the radiation patch killing me in the north? | Radiation scales with the north and can pin you in place. Gas mask + anti-rad medication is the manual's explicit requirement beyond Army Warehouses. |
| Are anomalies static? | No — the pack ships a Dynamic Anomalies Overhaul and enables `dynamic_anomalies` by default; artefacts spawn in both fixed fields and dynamic anomalies. |
| Where do artefact spawns come from? | The field's element family decides the artefact group; dynamic anomalies roll from the tier ladders with a heavy junk bias. |
| Why is my artefact gone? | 5 in-game days of not picking it up (0.9.5). |
| How often are emissions? | Configured in MCM: default emission event every 24, psi storm every 48 (engine units as shipped), with sirens and warnings. |
| What happens to people who do not shelter? | `emission_fate = explode`; psi storms default to `turn_to_zombie`. |
| Can I turn anomalies down? | Yes — ZCP ships an Anomalies options page; MCM also exposes dynamic-anomaly and event settings. |
| Best defence against psi fields? | Psy protection: helmets with psy boosts, psy-block/etperazine, psi artefacts, and psy resistance skills. |

Cross-references: artefact groups and detectors → `references/artifacts.md`; radiation and psy
health in the body model → `references/survival-mechanics.md`; psy-protection gear →
`references/armor-outfits.md`; anomaly-related quest content → `references/quests-storylines.md`;
populations affected by emissions → `references/mutants.md`; how damage is applied to your
body model (anomaly damage bypasses the BR scale) → `references/ballistics-damage.md`.
