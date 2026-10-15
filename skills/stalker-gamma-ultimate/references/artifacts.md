# Artefacts — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual's **Artefacts Reinvention** article
(`article_gamma_arty_text`) and **Lore**/**Money** articles, the **NPE artefacts tutorial**
(`npe_gamma_tutorial_artefact.xml`: detector tiers, perkifacts, empowering, fusion, pelts and
tech items), GAMMA's artefact spawn-group config
`G.A.M.M.A. Artefacts Reinvention/…/items/settings/artefacts.ltx`, the per-artefact stats
patch `mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx`, the melter item definition
`items_grok_artefacts_melter.ltx` and the **Grizzly detector** definition
`items_grok_detector.ltx`, the pack's values grid `artefacts_values.xlsx`, the plates patch
`mod_system_grok_plates_rework.ltx`, the pelts patch `mod_system_grok_pelts.ltx`, and
`Patchnotes.md` 0.9.5 (Gameplay, Balance, Crafting, Bugfix).
Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

GAMMA rebuilt artefacts into a **tiered, randomised, craftable protection economy**. The
README states the design in one line: artefacts "are immediately useable but need to be
empowered by combining artefacts to achieve higher protection levels (using a specific tool
buyable at Ecologists)".

---

## 1. What an artefact is in GAMMA

| Property | Meaning |
|---|---|
| **Tier** | Junk / T0 → T1 → T2 → T3 → Special. Higher tier = stronger protection |
| **Condition ("quality", "wrenched %")** | every spawned artefact arrives at a **random low condition**; condition = how much of its protection it delivers |
| **Belt slot** | artefacts are belt items; your armour's `artefact_count` decides how many you can wear (1–6; see `references/armor-outfits.md`) |
| **Container** | an artefact outside a container irradiates you (manual, radiation article) |
| **Type** | **defensive artefacts** (protection stats) vs **perkifacts** (procedural perks) vs **tech items** and **pelts** (belt items, see §7) |

## 2. Tiers, and which artefacts live in which tier

The spawn config groups artefacts by **elemental family** and **region** (south / mid /
north). The file's own comments map the language to tiers:

- `weak` = tier 1 ("junk south / weaker stuff", "junk north / a bit stronger stuff")
- `elemental` / `psi-gravi` / `phyto-chem` = T1 (south) → T2 (mid) → T3 (north)
- a "smart mix" of T1+T2 for general fields, plus `north_all` for the north
- the top of the scale (`af_compass`, `af_monolith`, `af_oasis_heart`, `af_death_lamp`,
  `af_glass`, `af_baloon`, `af_bat`, `af_atom`, `af_ice`, `af_full_empty`, `af_black_spray`)
  appear only in late/northern groups

Verbatim group contents from `artefacts.ltx` (this is the actual spawn logic — the definitive
answer to "where do I find <artefact>?"):

| Group | Members |
|---|---|
| `[af_fire_t1]` | `af_itcher`, `af_dummy_glassbeads` |
| `[af_fire_t2]` | `af_pin`, `af_cristall`, `af_lobster_eyes` |
| `[af_fire_t3]` | `af_fireball`, `af_fire`, `af_baloon` |
| `[af_chem_t1]` | `af_cristall_flower`, `af_blood`, `af_mincer_meat`, `af_soul` |
| `[af_chem_t2]` | `af_vyvert`, `af_eye`, `af_bracelet`, `af_fuzz_kolobok` |
| `[af_chem_t3]` | `af_baloon`, `af_glass` |
| `[af_elec_t1]` | `af_dummy_battery`, `af_electra_sparkler` |
| `[af_elec_t2]` | `af_cristall`, `af_ring`, `af_electra_moonlight` |
| `[af_elec_t3]` | `af_electra_flash`, `af_ice` |
| `[af_grav_t1]` | `af_medusa`, `af_mincer_meat`, `af_night_star`, `af_soul` |
| `[af_grav_t2]` | `af_vyvert`, `af_empty`, `af_gravi`, `af_sponge`, `af_fuzz_kolobok` |
| `[af_grav_t3]` | `af_full_empty`, `af_gold_fish`, `af_glass` |
| `[af_psi_t1]` | `af_cristall_flower`, `af_soul` |
| `[af_psi_t2]` | `af_pin`, `af_lobster_eyes`, `af_electra_moonlight`, `af_eye`, `af_bracelet`, `af_fuzz_kolobok`, `af_dummy_dummy` |
| `[af_psi_t3]` | `af_electra_flash`, `af_glass`, `af_black_spray` |
| `[af_death]` | `af_death_lamp` |
| `[af_class_weak_low]` (junk south) | `af_skull_miser`, `af_ear`, `af_tapeworm`, `af_fonar`, `af_chelust`, `af_peas`, `af_zhelch`, `af_cocoon`, `af_moh`, `af_ball`, `af_spaika`, `af_sandstone`, `af_signet`, `af_generator`, `af_black_angel`, `af_kislushka` |
| `[af_class_weak_high]` (junk north) | `af_lighthouse`, `af_star_phantom`, `af_cell`, `af_serofim`, `af_medallion`, `af_dragon_eye`, `af_kogot`, `af_generator`, `af_elektron`, `af_grapes`, `af_repei`, `af_sun` |
| `[af_class_elemental_south]` | `af_medusa`, `af_electra_sparkler`, `af_itcher`, `af_sandstone`, `af_pin`, `af_mincer_meat`, `af_dummy_battery`, `af_dummy_glassbeads` |
| `[af_class_elemental_mid]` | `af_cristall`, `af_ring`, `af_electra_moonlight`, `af_lobster_eyes` |
| `[af_class_elemental_north]` | `af_fireball`, `af_gold_fish`, `af_fire`, `af_electra_flash` |
| `[af_class_psio_gravi_south]` | `af_night_star`, `af_soul`, `af_fountain`, `af_cristall_flower`, `af_dummy_battery` |
| `[af_class_psio_gravi_mid]` | `af_vyvert`, `af_dummy_dummy`, `af_eye`, `af_gravi`, `af_gold_fish`, `af_empty` |
| `[af_class_psio_gravi_north]` | `af_ice`, `af_black_spray`, `af_full_empty`, `af_atom` |
| `[af_class_phyto_chem_south]` | `af_lobster_eyes`, `af_mincer_meat`, `af_blood`, `af_signet`, `af_dummy_glassbeads` |
| `[af_class_phyto_chem_mid]` | `af_fuzz_kolobok`, `af_sponge`, `af_bracelet`, `af_empty` |
| `[af_class_phyto_chem_north]` | `af_glass`, `af_death_lamp`, `af_baloon` |
| `[af_class_junk]` (smart mix) | `af_sun`, `af_lighthouse`, `af_star_phantom`, `af_bat`, `af_grapes` |
| `[af_class_mix_electro]` | `af_electra_sparkler`, `af_ring`, `af_dummy_dummy`, `af_dummy_battery`, `af_fountain`, `af_cristall_flower`, `af_electra_moonlight`, `af_tapeworm`, `af_generator`, `af_mincer_meat` |
| `[af_class_mix_fire]` | `af_itcher`, `af_medusa`, `af_signet`, `af_sandstone`, `af_pin`, `af_dummy_glassbeads`, `af_cristall`, `af_sun`, `af_dragon_eye`, `af_lobster_eyes` |
| `[af_class_mix_psio_gravi]` | `af_night_star`, `af_soul`, `af_fountain`, `af_cristall_flower`, `af_dummy_battery`, `af_vyvert`, `af_dummy_dummy`, `af_eye`, `af_gravi`, `af_gold_fish` |
| `[af_class_mix_phyto_chem]` | `af_lobster_eyes`, `af_mincer_meat`, `af_blood`, `af_signet`, `af_dummy_glassbeads`, `af_fuzz_kolobok`, `af_sponge`, `af_bracelet`, `af_empty` |
| `[af_class_north_all]` | `af_cell`, `af_serofim`, `af_medallion`, `af_dragon_eye`, `af_kogot`, `af_generator`, `af_elektron`, `af_repei`, `af_atom`, `af_cristall`, `af_ring`, `af_electra_moonlight`, `af_vyvert`, `af_dummy_dummy`, `af_eye`, `af_gravi`, `af_gold_fish`, `af_fuzz_kolobok`, `af_sponge`, `af_bracelet`, `af_empty`, `af_fireball`, `af_electra_flash`, `af_fire`, `af_gold_fish`, `af_full_empty`, `af_black_spray`, `af_ice`, `af_bat`, `af_death_lamp`, `af_compass`, `af_glass`, `af_baloon`, `af_monolith`, `af_oasis_heart` |

The file also carries the emission-type multipliers used when a field rolls for an artefact:

```
[settings]
psi_storm_chance = 0.6
surge_chance    = 1.2
```

## 3. How spawning works (0.9.5 rules)

- **Random field spawns**: "artefacts spawn randomly in the current map of the player in
  anomalous fields so be sure to check them whenever you move around them!" (manual).
- **Rare artefacts respawn in the labs after emissions** (manual) — labs are a renewable
  source of the good stuff.
- 0.9.5 increased the dynamic-anomaly spawn rate but tilted the mix toward junk: "Much higher
  chance of dynamic anomalies artefacts spawn, but more **T0** artefacts spawn there."
- **Artefacts despawn after 5 in-game days if not picked** (0.9.5, considered "stuck").
- The pack notes "Slight boost to regular field artefacts spawn" in the same patch.
- **Spawn locations are per-anomaly-field** (the config's group names are referenced from
  `configs/scripts/<map>/anomaly/*_anomal_zone.ltx` files), so the element family you meet
  depends on the anomaly type of the field — see `references/anomalies.md`.

## 4. Detectors

Detectors are how artefacts become visible. The NPE tutorial gives the tier table:

| Detector | Detects up to |
|---|---|
| **Echo** | T1 artefacts |
| **Bear** | T2 artefacts |
| **Grizzly** and better | T4 artefacts |

Other facts verified from the files and manual:

- **The Grizzly** is GAMMA's own detector (`detector_grizzly`, cost **27 560 RU**, `tier = 4`,
  `af_radius = 30`, `af_vis_radius = 4`), and the manual describes its selling point: "New
  Grizzly Detector to find all artefacts even with NVGs on. **Craftable with an advanced
  toolkit**."
- The detector item config lists per-artefact classes with individual beep sounds and
  frequencies (`af_class_1 … af_class_8`, `af_sound_*`, `af_freq_*`, e.g. `0.05, 2`), which is
  why different artefacts sound different.
- **Detectors need batteries** ("Beware that detectors need batteries to work" — NPE). This
  interacts with the difficulty setting `battery_consumption` (0.5 / 0.75 / 1.0 across the
  three economy presets) and the "G_FLAT's Msv Above Radiation Icon" style HUD addons.
- Detectors are equipped/shown with the detector key — **default `6`** ("You just equipped an
  Artefact Detector. These can be used using the '6' key (by default)"). See
  `references/keybinds-settings.md`.
- Quality-of-life addons shipped for detectors: **Apathy's Better Detector Position**,
  **R3zy's Detectors Enhanced Shaders Patch**, **Wildkins's DAO Svarog Patch**,
  **G.A.M.M.A. Free Zoom v3** (also known as "Kute's Free Zoom Rewrite") — the community guide
  recommends Free Zoom specifically to read the Svarog's screen while walking slowly.
- Detector recipes (craft.ltx, section "devices"): `x_detector_simple` (needs a
  `broken_detector` + resistors/transistors/capacitors), `x_detector_advanced` (from a simple
  detector), `x_detector_geiger`, `x_detector_grizzly` (2 × `recipe_advanced_2` +
  `detector_advanced` + 14/14/14 of the electronic parts), `x_detector_scientific` (3 ×
  `recipe_expert_2` + a Grizzly + 32/32/32 parts). **You craft upward from broken detectors.**

## 5. Quality, empowering and the Artefact Melter

### Quality

"New artefacts quality system: artefacts spawn with a random low condition (or 'quality') to
mimic that every artefact is different." (manual)

### Empowering (fuse the same artefact into itself)

- "Combine **two exactly similar** artefacts to sum their condition / quality."
- "You can combine **any junk artefact with any other junk artefact** at a reduced rate."
- NPE tutorial, with the example: "**22 % Wrenched + 32 % Wrenched = 54 % Wrenched**".

### The Artefact Melter (the tool)

| Property | Value (from `items_grok_artefacts_melter.ltx`) |
|---|---|
| Section | `itm_artefactskit` |
| Cost | **15 000 RU** (manual: "Buy it at Sakharov or Herman for about 30k RU" — the trader price is what the player pays; the item's base cost is 15 000) |
| Weight | 1.5 kg (1.0 empty) |
| **Charges (`max_uses`)** | **10** |
| Tier | 3 |
| Modes | right-click → menu (`use1` = `grok_artefacts_melter.menu_tool`), plus `workshop_tool.tool_artefact_craft` |
| Repairable sections | the full ~80-entry artefact list (`repair_parts_sections`), `repair_parts_multi = 4`, `repair_use_actor_effects = true` |

Manual instructions:

- "You can craft stronger artefacts (right click > **Fuse Artefacts**) or empower them (right
  click > **Empower artefacts**)."
- "**Every action you take with the artefacts melter will consume some charges.**"
- "You can refill the melter by **holding Left Alt key and dragging it on top of any
  artefact**." — hence: "Keeping an empty melter on you is a good way to replenish it on your
  way through the zone with unwanted artefacts."
- Where to buy: **Sakharov or Hermann** (Ecologists).
- Safety addon in the pack: **Flueno's Safer Artifact Melting** (0.9.5 disabled "safe
  artifact melting" because "artefacts don't emit rads anymore").

## 6. Crafting artefacts (tier conversion)

From the manual's *Artefact Crafting*, plus the recipe menu:

| Conversion | Cost (manual: "mS" = money units shown by the menu) |
|---|---|
| **Junk → Tier 1** | 7 |
| **Tier 1 → Tier 2** | 12 |
| **Tier 2 → Tier 3** | 23 |
| **Tier 3 → Special** | (no cost quoted in the manual) |

- "Access the craft menu as usual. There will be a new crafting subsection: **Artefacts**."
- "Defensive Artefacts can be crafted using the Artefact Melter. Right-click the Artefact
  Melter, select 'fusio', and craft artefacts following the recipes requirements
  (alternatively, you can access the menu through the workbench UI)." (NPE)
- **New recipes are bought from Ecologists**, and "The highest tier of artefacts can only be
  crafted through a set of recipes found on **high rank stalkers**" (NPE).
- Recipe books and their prices come from `mod_system_grok_recipes.ltx`:
  `recipe_basic_1…4`, `recipe_advanced_1…4`, `recipe_expert_1…4`, plus a dedicated
  `recipe_ammo_4`. Base costs in the shipped file: basic 1 000 / 3 200 / 5 000 / 6 000,
  advanced 3 000 / 10 000 / 10 000 / 36 000, expert 7 000 / 16 000 / 29 000 / 48 000,
  `recipe_ammo_4` 65 000. The `craft.ltx` comment block names them by purpose ("Basic
  equipment / Basic electronics / Basic upgrades / Tier 2 artefacts", and so on), and 0.9.5
  **raised the T3 artefact recipe book from 36 k to 99 k** — the artefact endgame is
  deliberately expensive.
- Restrictions that matter: **"Artefacts on Belt cannot be used for crafting"** and "Artefact
  melter does not use belt artefacts" (0.9.5, to stop you accidentally destroying your
  equipped protection) — plus the low-condition crafting fix in the same patch.

## 7. Belt items other than defensive artefacts

The NPE tutorial lists them explicitly:

- **Pelts** — "obtained from skinning mutants. **The better the knife, the better the
  condition of the Pelts. Only one Pelt can be equipped at a time**, but they only provide
  bonuses." Data examples: `hide_flesh` (6 200 RU, power restore + chemical immunity
  0.37332), `hide_boar` (6 200 RU, **+12 kg** carry, burn immunity 0.24375). 0.9.5: Boar and
  Pseudogiant pelts give **BRC and BRC mitigation**.
- **Tech items** — "can be bought from traders or crafted. **Upgraded versions of the Tech
  Items can only be obtained through upgrading the base Tech Items** from the crafting [menu]."
  The shipped tech items (all belt, all craftable) are `af_surge` / `af_surge_up`
  (environmental surge controller: 8 500 RU → 25 000 RU, caps 0.05 → 0.1 on burn/shock/chem,
  immunities 0.1625/0.1212/0.24888 → 0.24375/0.1818/0.37332), `af_frames` / `af_frames_up`
  (anti-psi frames, 14 200 RU), `af_grid`, `af_freon`, `af_cooler`, `af_camelbak`, and the
  armour-plate line `af_kevlar` / `af_kevlar_up` / `af_plates` / `af_plates_up` (0.9.5:
  plates give no BR % but higher tiers add strike resistance: kevlar explosion 0.0403 →
  0.0806; plates strike 0.0909 → 0.1454, explosion 0.134 → 0.2).
- **Perkifacts** — a 0.9.5-era system (Perk-Based Artefacts addon): "Perkifacts always spawn
  at **100 % efficiency**. However their efficiency **decreases over time when they are
  equipped**. Perkifacts provide extremely diverse and situational buffs and capacities.
  These effects are often **increased depending on the number of the same Perkifact** that you
  have equipped on your belt." The pack's balancing patch for them is
  `mod_system_momopate_pba_tweaks.ltx`.
- **Junk artefacts as currency** — the spawn config's own note: junk artefacts are "usually
  not having big direct benefits except possibility to trade it or use it as currency".

## 8. The protection values (the `+ / -` grid)

`artefacts_values.xlsx` is the pack's own table of what an artefact's condition percentage is
worth, as a grid from the weakest to the strongest roll. Columns run `+ … ++++++` (and
`- … ------` for the drawbacks). Verbatim rows:

| Stat | 1st step | 2nd | 3rd | 4th | 5th | 6th |
|---|---|---|---|---|---|---|
| Chem | 0.12444 | 0.24888 | 0.37332 | 0.49776 | 0.6222 | 0.74664 |
| Burn | 0.08125 | 0.1625 | 0.24375 | 0.325 | 0.40625 | 0.4875 |
| Electric | 0.0606 | 0.1212 | 0.1818 | 0.2424 | 0.303 | 0.3636 |
| Strike | 0.205 | 0.41 | 0.69 | 0.82 | 1.025 | 1.23 |
| Explosive | 0.22667 | 0.47 | 0.68 | 0.90668 | 1.13335 | 1.36002 |
| Rupture | 0.07125 | 0.1425 | 0.21375 | 0.285 | 0.35625 | 0.4275 |
| Ballistic | 0.097431 | 0.194862 | 0.292293 | 0.4 | 0.5 | 0.584586 |
| Bleed | 0.02045 | 0.04079 | 0.061185 | 0.08158 | 0.101975 | 0.12237 |
| Stamina | 0.000336735 | 0.00067347 | 0.001010205 | 0.00134694 | 0.001683675 | 0.00202041 |
| Psy | 0.0555556 | 0.1111112 | 0.1666668 | 0.2222224 | 0.277778 | 0.3333336 |
| Rad | 0.00043 | 0.00086 | 0.00129 | 0.00172 | 0.00215 | 0.00258 |

And the matching negative column (drawbacks), first steps: Chem `-0.15555`, Burn `-0.1015625`,
Electric `-0.07575`, Strike `-0.25625`, Explosive `-0.2833375`, Rupture `-0.0890625`,
Ballistic `-0.125`, Bleed `-0.02045`, Stamina `-0.000336735`, Psy `-0.0694445`.

**Interpretation:** an artefact's *final* protection is its base stat scaled by its condition
step — which is exactly why empowering (summing condition) is the core grind, and why two
"identical" artefacts are never identical.

Per-artefact stats live in `mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx`. Examples read
directly from it:

| Artefact | Cost | Notable stats |
|---|---|---|
| `af_itcher` | 36 800 | `burn_cap = 0.05`; burn immunity 0.1625, chemical **−0.27**, explosion 0.47 |
| `af_pin` | 42 200 | `burn_cap 0.10`, `telepatic_cap 0.05` |
| `af_cristall` | 63 600 | `burn_cap 0.15`; burn 0.24375, shock 0.1818 |
| `af_fireball` | 93 600 | `af_rank 2`, `burn_cap 0.20`, `wound_cap 0.10`; burn 0.41, strike **−0.74** |
| `af_blood` | 44 400 | `bleeding_restore_speed 0.004082`, `chemical_burn_cap 0.05` |
| `af_mincer_meat` | 62 600 | `bleeding_restore_speed −0.002045` (a *drawback*) |
| `af_bracelet` | 75 880 | `power_restore_speed 0.00066`, chem immunity 0.37332 |
| `af_baloon` | 94 800 | `health_restore_speed −0.0006`, chem 0.77, burn 0.33 |

0.9.5 rebalance notes on individual artefacts: **Moonlight shock and telepathic caps +10**,
and the **Compass BR % cap was raised by 5 % to 15 %**. Artefacts from the *New Storylines*
addon (`af_ah_o1`, `af_ah_o2`, class `SCRPTART`, 4 000 RU, `can_trade = false`) are
**quest artefacts** — they cannot be sold.

## 9. Artefacts and the economy

- **Selling artefacts to the Ecologists is one of the three canonical money-makers**
  (manual, *Money*: "doing tasks without picking fights, selling mutant parts or selling
  artefacts to the ecologists").
- The Artefact Hunters questline pays for artefacts and was buffed in 0.9.5 ("Increased money
  rewards for Artefact Hunters Quests").
- **Fetch tasks will not ask for belt artefacts** since 0.9.5 ("Fetch quests won't pick belt
  artefacts for completion") — you will not be asked to hand over the artefact you are wearing.
- The **hideout artefact harvester** (0.9.5, hideout furniture from DoktorDauerfeuer) exists
  as an artefact sink with returns: "you can place an artifact in it, which is then degraded to
  passively generate items, with results depending on the artifact. Outcomes range from wood
  parts to mutant meat to ammo crafting materials, up to… other artifacts."
- **Artefacts are also crafting inputs**: the melter refills from any artefact (Left-Alt drag),
  and tier conversion consumes them in bulk.

### 9.1 What each artefact is worth (verbatim `cost` values)

The item file `mod_system_zzzzzzzzzzzzzzzzz_grok_artifacts.ltx` sets a `cost` on every
artefact (each section inherits from `af_base`). The full T1 → Special ladder, sorted:

| Tier | Artefacts and their base cost (RU) |
|---|---|
| **Junk / low** | `af_moh` 1 800 · `af_ear` 1 900 · `af_kogot` 2 110 · `af_skull_miser` 2 200 · `af_kislushka` 2 200 · `af_peas` 2 485 · `af_ball` 2 800 · `af_serofim` 2 800 · `af_atom` 2 800 · `af_repei` 3 000 · `af_signet` 3 300 · `af_tapeworm` 3 600 · `af_dragon_eye` 3 900 · `af_zhelch` 4 000 · `af_fountain` 4 700 · `af_cocoon` 4 900 · `af_sandstone` 4 950 · `af_spaika` 5 000 · `af_fonar` 5 080 · `af_fire_loop` 5 080 · `af_grapes` 5 300 · `af_black` 5 400 · `af_star_phantom` 5 400 · `af_elektron` 5 900 · `af_cell` 6 000 · `af_sun` 6 200 · `af_chelust` 6 400 · `af_lighthouse` 6 500 · `af_generator` 6 520 · `af_black_angel` 6 700 · `af_medallion` 6 800 · `af_bat` 8 600 |
| **T1 (~36 000–55 000)** | `af_itcher` 36 800 · `af_pin` 42 200 · `af_electra_sparkler` 43 200 · `af_blood` 44 400 · `af_cristall_flower` 45 600 · `af_dummy_glassbeads` 49 600 · `af_medusa` 49 800 · `af_soul` 52 400 · `af_dummy_battery` 54 400 |
| **T2 (~60 000–88 000)** | `af_mincer_meat` 62 600 · `af_cristall` 63 600 · `af_night_star` 66 400 · `af_vyvert` 71 000 · `af_lobster_eyes` 71 280 · `af_eye` 73 800 · `af_dummy_dummy` 74 400 · `af_bracelet` 75 880 · `af_fuzz_kolobok` 81 200 · `af_ring` 84 440 · `af_empty` 85 520 · `af_electra_moonlight` 87 200 |
| **T3 (~93 000–111 000)** | `af_fireball` 93 600 · `af_fire` 93 850 · `af_baloon` 94 800 · `af_gravi` 95 000 · `af_electra_flash` 97 800 · `af_ice` 102 800 · `af_glass` 108 800 · `af_black_spray` 110 640 |
| **Special / top** | `af_gold_fish` 132 400 · `af_full_empty` 143 300 · **`af_compass` 149 000 · `af_oasis_heart` 149 000 · `af_monolith` 149 000 · `af_ah_f1` 149 000 · `af_tlf_prometheus` 149 000** · `af_death_lamp` 150 000 |

### 9.2 The fusion recipes, verbatim

`craft.ltx` writes artefact cooking as `x_af_<result> = 6, recipe_<book>, <inputs…>` — six
output per craft, gated on the recipe book, and always mixing **junk artefacts plus mutant
parts**. The whole T1/T2 chain (abridged to the first inputs of each line):

```
x_af_medusa        = 6, recipe_basic_0,    af_spaika,1,             mutant_part_dog_tail,2,  mutant_part_cat_claw,2
x_af_vyvert        = 6, recipe_basic_4,    af_mincer_meat,1,        mutant_part_lurker_tail,2, mutant_part_fracture_hand,1
x_af_empty         = 6, recipe_basic_4,    af_medusa,1,             mutant_part_fang_psevdodog,1, mutant_part_snork_mask,1
x_af_cristall      = 6, recipe_basic_4,    af_dummy_glassbeads,1,   mutant_part_fang_psevdodog,1, mutant_part_zombi_hand,2
x_af_fireball      = 6, recipe_advanced_4, af_cristall,1,af_lobster_eyes,1, mutant_part_pseudogigant_eye,3
x_af_fire          = 6, recipe_advanced_4, af_pin,1,af_eye,1,        mutant_part_chimera_claw,2, mutant_part_chimera_kogot,3
x_af_full_empty    = 6, recipe_advanced_4, af_empty,1,af_vyvert,1,   mutant_part_pseudogigant_hand,4
x_af_gold_fish     = 6, recipe_advanced_4, af_gravi,1,               mutant_part_burer_hand,3, mutant_part_controller_hand,1, mutant_part_chimera_claw,2
x_af_ice           = 6, recipe_advanced_4, af_ring,1,                mutant_part_krovosos_jaw,2, mutant_part_chimera_claw,2, mutant_part_controller_glass,1
x_af_black_spray   = 6, recipe_advanced_4, af_dummy_dummy,1,af_sponge,1, mutant_part_controller_glass,2, mutant_part_burer_hand,3
x_af_compass       = 6, recipe_expert_4,   af_full_empty,1,af_black_spray,1, mutant_part_controller_glass,4, mutant_part_heart_chimera,4
x_af_oasis_heart   = 6, recipe_expert_4,   af_ice,1,af_glass,1,       mutant_part_heart_bloodsucker,6, mutant_part_heart_chimera,4
x_af_monolith      = 6, recipe_expert_4,   af_electra_flash,1,af_baloon,1, mutant_part_pseudogigant_hand,4, mutant_part_pseudogigant_eye,4
x_af_fire_loop     = 6, recipe_expert_4,   af_fire,1,af_fireball,1,   mutant_part_heart_chimera,6, mutant_part_controller_hand,6
```

That is the mechanical link between the mutant economy and the artefact economy: **chimeras,
controllers and pseudogiants are the bottleneck for the top artefacts**, and junk artefacts
(`af_spaika`, `af_mincer_meat`, `af_signet`, `af_sun`, `af_zhelch`, `af_generator`,
`af_fonar`, `af_ear`, `af_black_angel`, `af_sandstone`, `af_skull_miser`) are the seeds.

### 9.3 Recipe books and tech items (what to buy from the Ecologists)

From `mod_system_grok_recipes.ltx` (actual loaded costs) and `mod_system_grok_tech.ltx`:

| Recipe book | Cost | Unlocks (per `craft.ltx`'s own header) |
|---|---|---|
| `recipe_basic_1` | 5 000 | Basic equipment (mechanics) |
| `recipe_advanced_1` | 10 000 | Advanced equipment |
| `recipe_expert_1` | 16 000 | Expert equipment |
| `recipe_basic_2` | 3 200 | Basic electronics |
| `recipe_advanced_2` | 10 000 | Advanced electronics |
| `recipe_expert_2` | 29 000 | Expert electronics |
| `recipe_basic_3` | 1 000 | Basic upgrades |
| `recipe_advanced_3` | 3 000 | Advanced upgrades |
| `recipe_expert_3` | 7 000 | Expert upgrades |
| `recipe_basic_4` | 6 000 | **Tier 2 artefacts** (Ecologists) |
| `recipe_advanced_4` | 36 000 | **Tier 3 artefacts** |
| `recipe_expert_4` | 48 000 | **Special artefacts** — and 0.9.5 raised the *trader* price of the tier-3 book: "**Increased price of T3 artefact recipe book (36k > 99k)**" |
| `recipe_ammo_4` | 65 000 | Ammo-tier recipe book |

Three rules from the patch history that shape this system (still true in 0.9.5):

- **Every artefact recipe consumes both artefacts and mutant parts** — "Artefacts crafting
  remade: all recipes need mutant parts and artefacts. **T0 > T1 and T1 > T2 artefacts crafting
  only require one artefact. T2 > T3 and T3 > T4 require two artefacts and mutant parts**"
  (0.9.3), and "Removed artefacts melter charges for crafting recipes" (0.9.3) — the melter's
  charges are for *empowering*, not for fusion.
- **The top recipes are not for sale**: "**Artefacts Tier 4 recipes are now drop only (same
  chance as exo repair kit)**" (0.9.4), and "the highest tier of artefacts can only be crafted
  through a set of recipes found on **high rank stalkers**" (NPE tutorial).
- **Ecologists in the north** are the source of the T3/T4 books: "T3 and T4 artefacts recipes
  can only be bought from the **North Ecologist traders**" (0.9.3).

**Belt tech items** (`mod_system_grok_tech.ltx`) and their upgrade costs — the cheaper,
non-artefact half of the belt build:

| Base item | Cost | Upgraded | Cost |
|---|---|---|---|
| `af_surge` (Environmental Surge Controller) | 8 500 | `af_surge_up` | 25 000 |
| `af_frames` (Anti-Psi Frames) | 14 200 | `af_frames_up` | 28 400 |
| `af_grid` | 12 650 | `af_grid_up` | 25 300 |
| `af_freon` | 9 850 | `af_freon_up` | 19 700 |
| `af_cooler` | 18 420 | `af_cooler_up` | 36 840 |
| `af_camelbak` | 8 500 | `af_camelbak_up` | 17 000 |

Their absorption blocks are explicit: `af_surge` gives `burn_immunity 0.1625`,
`shock_immunity 0.1212`, `chemical_burn_immunity 0.24888` and caps
(`burn_cap = 0.05`, `shock_cap = 0.05`, `chemical_burn_cap = 0.05`), and the `_up` version doubles
those (`0.24375 / 0.1818 / 0.37332`, caps `0.1`). Tech items are bought from traders or crafted,
and "**Upgraded versions of the Tech Items can only be obtained through upgrading the base Tech
Items from the crafting UI**" (NPE tutorial).

## 10. Practical artefact workflow

1. **Equip a detector** before entering any field; the detector key is `6` by default.
2. **Throw bolts to chart the paths** through the field (bolts are limited by the
   `limited_bolts` difficulty flag), then walk the detour and let the detector's beep rate
   guide you.
3. **Pick up everything** — junk artefacts are currency, melter fuel, and tier-conversion
   fodder. (Junk+junk can be fused at a reduced rate.)
4. **Empower before crafting**: two identical artefacts sum their condition; convert upward
   only when fusing cannot help you any more.
5. **Do not craft or melt with belt-equipped artefacts** — the game will refuse (0.9.5) but it
   is worth knowing why.
6. **Sell duplicates to the Ecologists** when you have more than your belt can hold, and keep
   one of each family you actually use.

## 11. Quick answers

| Question | Answer |
|---|---|
| Where do artefacts come from? | Random spawns in anomaly fields on the current map, rare respawns in labs after emissions, and (rarely) from stashes/tasks/packages. |
| Why can't I see any? | You need a detector equipped, and the detector must cover the tier (Echo→T1, Bear→T2, Grizzly→T4). |
| Why is my artefact weak? | Spawned condition. Empower it with a duplicate, or fuse junk into stronger tiers. |
| Where is the Melter? | Buy from **Sakharov or Hermann** (Ecologists); craft-refill its charges by Left-Alt-dragging artefacts onto it; it holds 10 charges per fill. |
| How do I get a Grizzly? | Craft it with an **advanced toolkit** from a `detector_advanced` plus electronics parts — or find/buy one. |
| Do artefacts irradiate me? | Yes, if not in a container. That is the manual's warning about radiation sources. |
| Can I sell artefacts? | To the Ecologists, and via Artefact Hunters tasks; quest artefacts (`can_trade = false`) cannot be sold. |
| How many can I wear? | As many as your armour's belt slots allow (`artefact_count`, 1–6; most common 3 and 2). |
| Why did my artefact vanish from a field? | 0.9.5 despawns unpicked artefacts after 5 in-game days. |
| Are pelts artefacts? | They share the belt, provide only bonuses in 0.9.5, and only **one** at a time; their condition depends on your knife. |

Cross-references: anomaly types and where fields are → `references/anomalies.md`; armour belt
slots, plates and BRC → `references/armor-outfits.md`; damage types explained →
`references/ballistics-damage.md`; recipes, toolkits and the workbench →
`references/crafting-repairs.md`; selling → `references/trading-economy.md`; radiation,
immunity and what a belt of artefacts does to your body → `references/survival-mechanics.md`.
