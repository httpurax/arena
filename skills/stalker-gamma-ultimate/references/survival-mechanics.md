# Survival: health, hunger, thirst, sleep, energy — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual articles **Healing and Medicines**
(`article_gamma_healing_text`), **Energy Management** (`article_gamma_energy_text`),
**Radiations** (`article_gamma_radiation_text`), **Cooking**, **Inventory** and **Money**; the
**NPE healing tutorial** (`npe_gamma_tutorial_heal.xml`, quoted verbatim throughout);
GAMMA's actor override
`G.A.M.M.A. Artefacts Reinvention/gamedata/configs/creatures/actor.ltx` (condition, stamina,
sleep, limping, immunity presets, bone damage); the **Skill System Balance** file
`G.A.M.M.A. Skill System Balance/…/plugins/skills/skill_haruka.ltx`; the physiological
multipliers in `G.A.M.M.A. Difficulty Presets Rebalance/…/difficulty.ltx`
(`thirst`, `sleep`, `radiation_day`, `battery_consumption`, `weapon_degradation`); the economy
preset block for loot/consumables; and `Patchnotes.md` 0.9.5 (Gameplay/Balance/UI/Bugfix).
Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. Health is five pools, not one bar

The NPE healing tutorial (verbatim):

> "Your health is divided in several individual health pools:
> **Main Health** (character icon), **Individual limbs health**, **Psy health**.
> You die if your Main Health reaches 0, if your Head Health reaches 0, if your Torso Health
> reaches 0 or if your Psy Health reaches 0. The Legs and Arms bars have various effects when
> being depleted: **damaged arms make your aim shake**; **damaged legs slow you down and deal
> damage to your Main Health when running on a broken leg.**"

| Pool | Refilled by | Failure mode |
|---|---|---|
| **Main Health** (red heart icon items) | medkits (slow), stimpacks (fast), artefacts/pelts/belt items with passive regeneration; "the higher the rank of the Medkit or the Stimpack, the better the health recovery" | death at 0 |
| **Head / Torso** | same first-aid + post-heal items | death at 0 |
| **Arms** | temp + permanent HP | aim shake while depleted |
| **Legs** | temp + permanent HP | slowed; running on a broken leg costs main health |
| **Psy** (blue-wave icon) | psy-block, sleeping pills, Etperazine, marijuana/joints, certain beverages, artefacts | death at 0 |

## 2. Temporary (yellow) vs permanent (white) limb health

> "Limb health pools contain two types of health: **Temporary Limb Health (in yellow)**, which
> gradually reduces with time, and **Permanent Limb Health (in white)**. Temporary Limb Health
> is restored using First-Aid items displaying a **red heart icon**, like Bandages, Medkits,
> Stimpacks… Temporary Limb Health **can be converted to Permanent Limb Health using Post-Heal
> items displaying a white heart icon**, like **Yadulin, Antidote, Ibuprofen**… Limbs Health
> restoration thus works by using a First-Aid item (ex: Bandage) followed by a Post-Heal item
> (ex: Ibuprofen). **The Temporary Limb Health is consumed before the Permanent Limb Health.
> Thus, during fights, simply use bandages until the fight ends, and then convert the
> Temporary Limb Health to Permanent Limb Health.**"

The manual adds the side-effect rule: "**Post-healing will give you side effects such as
extreme hunger or dizziness. Dizziness can be cured using stamina boosting medicine or
water.**" and notes that **damage-resistance injectors work** (shield icon) and that you
should **mark the most important medical items as favourites** rather than carrying everything.

## 3. Bleeding

> "When receiving damages, there's a probability that the fresh wounds bleed. Bleeding is
> indicated by a **blood droplet icon on the HUD**. The stronger the bleed, the more red the
> icon outline will be (**white > yellow > red**). Bleeds must be treated fast since they
> **aggravate and deal a lot of damage over time**. They can be treated using:
> **Bandage (slow bleed heal)**, **Tourniquet (fast bleed heal)**, **Artefacts, Pelts and Belt
> Items passive bleed heal properties**. Certain artefacts have **negative bleed recovery**,
> that needs to be counter balanced with positive bleed recovery, otherwise any bleed will
> quickly aggravate."

The blood-loss model is the *Prolonged Bleeding System* in `actor.ltx`:
`bleeding_v = 0.0015`, `wound_incarnation_v = 0.0002`, `min_wound_size = 0.0064`, and
`bleed_speed_k = 0.88` — "TotalWounds × bleed_speed_k". The first-aid item is
**`jgut`** (the tourniquet) as used by traders' `[trade_generic_sell]` tables (`jgut = 0.83`),
and both `jgut` and `bandage` are in every character's starting kit.

## 4. Radiation

From the manual's *Radiations* article:

- GAMMA has "**dynamic radiation** and a revamped radiation damage system" with **random
  radiation patches spawned at new game**.
- "Radiation will slowly reduce your health (**much slower than Vanilla**) and will reduce your
  **max stamina**."
- "The more irradiated you are, the more likely **critical organs will be damaged**. This
  results in the player character **coughing and losing a significant amount of health**."
- The **radiation meter sits in the bottom-left corner**; if it fills, "you just hit a radiation
  patch, try to **back track**".
- "**Radiation can also come from artefacts that are not in a container.**"
- Cures: "**anti-rad drugs, cigarettes, tobacco, water, or alcohol**"; prevention:
  "**rad protecting drugs**".
- "**Be sure to have a good gas mask before going into northern areas. Entering the Army
  Warehouses or areas further North without a gas mask or proper anti-radiation medication can
  kill you if you hit just one bad radiation patch.** Running into a strong radiation area will
  likely **make you unable to move, trapping you**."

The actor's radiation constants: `radiation_v = 0.00000001` per tick (air), and
`radiation_health_v = 0.0007` (health lost while irradiated); while sleeping
`radiation_v_sleep = 0.000014` and `radiation_health_v_sleep = 0.0012`. The zone exposure
caps are `radio_zone_max_power = 0.055`, `fire_zone_max_power = 1.15`,
`acid_zone_max_power = 0.25`, `psi_zone_max_power = 0.25`, `electra_zone_max_power = 4.0`.
Optional rule: each gameplay preset exposes a **`radiation_day`** flag (all shipped presets
ship it **`false`**) — when enabled, "the air will be radiated, radiation power depends on many
factors such as the weather, time cycle, the outfit and helmet player is wearing and their
protections against radiation."

## 5. Psy health

> "Certain enemies can deal damages to your brain through psi emissions (like **Controllers**).
> Items increasing your Psy Resistance also restore your Psy Health. These items display an
> icon with blue waves, this includes: **Psy-block, Sleeping Pills, Etperazine, Marijuana and
> joints, certain beverages, artefacts.**"

Actor-side maths: `psy_health_v = 0.0015` (passive psy recovery rate) and
`psy_health_v_sleep = 0.002`; `telepatic_immunity` comes from the difficulty immunity set
(1.00 → 2.50) and from armour/artefacts. See `references/armor-outfits.md` for which helmets
carry psy protection and `references/anomalies.md` for psi storms.

## 6. Stamina, weight and limping

The actor file's fatigue block (verbatim values) governs how long you can run:

| Key | Value | Meaning |
|---|---|---|
| `max_power_leak_speed` | `0.000001` | stamina drain when exhausted |
| `power_hit_part` | `0.035` | share of damage that hits stamina |
| `jump_power` / `jump_weight_power` | `0.018` / `0.2` | jump cost, scaled by load |
| `overweight_jump_k` | `1.03` | jump cost multiplier when overloaded |
| `walk_power` | `0.0002` | walking cost before weight |
| `walk_weight_power` | `0.0044` | walking cost per unit of load |
| `overweight_walk_k` | `2.5` | overload multiplier on `walk_weight_power` |
| `accel_k` / `sprint_k` | `1.3` / `4.0` | running and sprinting multipliers |
| `max_power_restore_speed` | `0.020` | stamina regeneration |
| `cant_walk_power_begin/end` | `0.0015` / `0.007` | below these you cannot walk |
| `cant_sprint_power_begin/end` | `0.08` / `0.10` | below these you cannot sprint |
| `limping_health_begin/end` | `0.09` / `0.12` | when leg damage makes you limp |
| `limping_power_begin/end` | `0.18` / `0.29` | when exhaustion makes you limp |

**Weight**: `max_item_mass = 50` (what you can carry comfortably), `max_walk_weight = 100`
(the absolute limit). Above 50 kg you slow down and burn stamina fast; at 100 kg you stop
moving. Armour and belt items raise the effective ceiling (`additional_inventory_weight`, up to
**+124.8 kg** on the Stolen Exoskeleton — see `references/armor-outfits.md`), and the
**Strength** skill raises it further (§9). The gameplay preset also exposes `max_weight` (50)
and the economy preset exposes its own `max_weight` (60).

## 7. Hunger, thirst and food

- **Satiety** (`satiety_v = 0.00002`) drains constantly; below the critical value
  (`satiety_critical = 0.2`) health begins to drop. Eating also has a stamina/health side:
  `satiety_power_v = 0.00325` (stamina gained while losing satiety) and
  `satiety_health_v = 0.00001`.
- **Sleeping** cuts hunger to `satiety_v_sleep = 0.000006`.
- **Thirst** is a *gameplay flag* per difficulty preset — `thirst = true` in **all three**
  shipped presets. Quench it with water (`water_drink`), flasks/canteens, mineral water, beer,
  vodka, tea. The manual's inventory advice: "**Water bottles are better weight-wise than
  canteens** to quench thirst. Keep the canteens in your main stash to cook with."
- **Cooking is the cheap food supply**: "**Cooking is essential, it will provide high calorie
  food for cheap**", all recipes are available from the start, the **basic kit works at
  bonfires without charcoal** and the **advanced kit needs liquid fuel** but produces
  **buff meals**. See `references/crafting-repairs.md` §7 for recipes.
- Food and drink families in the loot tables and trader stock: `tushonka`, `conserva`,
  `bread`, `kolbasa`, `tea__1`, `energy_drink__1`, `vodka__1`/`vodka2__1`, `water_drink__1`,
  `beer`, `flask`, `bottle_metal__1`, `glucose`/`glucose_s`.

## 8. Sleep and energy

From the manual's *Energy Management*, verbatim structure:

> "Energy in GAMMA is a balancing act between travel, food, drinks, medicine and sleep. Your
> character will be tired at the end of the day. You have to sleep to replenish your energy.
> **You can only sleep if you are tired enough. Using sleeping pills will allow you to
> forcefully sleep.** Depending on how the day was, you'll get tired faster or not. **Eating
> copious meals and taking sleep inducing drugs will make you tired** and get rest at the end
> of the day. However, **if you are eating small meals, and use energy drinks or caffeine
> tablets often, you'll have a hard time being tired enough to sleep** at the end of the day.
> You'll have a chance to **wake up early**. Be sure to try to sleep more than what you intend
> to sleep the correct amount of time, or **use better sleeping gear (mattress and sleeping
> bag)**. **Vodka and Beer can help you sleep as well.**"

Values: `max_sleep_hours = 12`, `sleep_time_factor = 1000`, and the default `g_sleep_time` is
**9**. While asleep the actor uses the `_sleep` variants of every condition constant —
`bleeding_v_sleep = 0.0` (bleeding stops), `wound_incarnation_v_sleep = 0.0005`,
`alcohol_v_sleep = -0.0025`, `max_power_leak_speed_sleep = -0.00001`
(i.e. stamina *recovers* in sleep), `morale_v_sleep = 0.000125`, and **`health_restore_v = 0.0`**
— the file's own note that natural health regeneration is switched off (you heal with items,
not time). Sleep items: `itm_sleepbag`, `itm_tent`, mattresses (hideout furniture), and
`drug_sleepingpills`.

**Energy drinks and caffeine tablets delay tiredness** — they are the tool for pushing a long
run, and the reason you cannot sleep when you spam them.

## 9. The skill system (Skill System Balance)

GAMMA ships **49- Skill System - Haruka** with a rebalance file
(`skill_haruka.ltx`) that defines four skill trees (plus their two stat sub-sections each).
Every tree shares the same economy:

```
[<skill>]
max_level         = 30
base_requirement  = 750
```

| Skill | Stats (verbatim) |
|---|---|
| **endurance** | `speed_modifier = 0.85`, `speed_modifier_increment = 0.0075`; `power_loss = 0.4`, `power_loss_increment = -0.0075` |
| **strength** | `weight_modifier = 0.5`, `weight_modifier_increment = 0.035`; `base_weight = 8`, `base_weight_increment = 0.0125`; `melee_damage = 1.0`, `melee_damage_increment = 0.025` |
| **survival** | `resistance = 1.0` ("damage multiplier, by default damage taken increases by x1.25"), `resistance_increment = 0`; `bleed_restore = 0`, `bleed_restore_increment = 0.00005`; `hunting_skill = -4`, `hunting_skill_increment = 0.25` |
| **scavenging** | `scavenging_skill = -4`, `scavenging_skill_increment = 0.25` |

Reading it: **30 levels, 750 points for the first one** (requirements escalate per level), and
each level moves a real stat — Endurance makes you faster and slower to tire, Strength makes you
carry more and hit harder, Survival improves bleed recovery and hunting, Scavenging improves
loot/skinning return. Skills level through doing (movement, weight carried, hunting, looting),
so a long-haul carrier will out-carry a sniper.

## 10. Injury, immunity and how damage lands on you

`actor.ltx` defines four difficulty immunity presets, chosen by the gameplay preset's
`actor_immunities = 1/2/3` selector:

| Immunity | novice (1) | stalker (2) | veteran (3) | master (4) |
|---|---|---|---|---|
| `burn_immunity` | 0.75 | 1.00 | 1.50 | 2.00 |
| `strike_immunity` | 0.30 | 0.33 | 0.42 | 0.50 |
| `shock_immunity` | 1.00 | 1.50 | 1.50 | 2.00 |
| `wound_immunity` | 0.50 | 0.70 | 0.85 | 1.00 |
| `radiation_immunity` | 0.90 | 0.90 | 0.90 | 0.90 |
| `telepatic_immunity` | 1.00 | 1.50 | 2.00 | 2.50 |
| `chemical_burn_immunity` | 0.75 | 1.00 | 1.75 | 2.00 |
| `explosion_immunity` | 0.39 | 0.52 | 0.65 | 0.79 |
| `fire_wound_immunity` | 0.40 | 0.50 | 0.75 | 1.00 |

(The default `g_game_difficulty` in `user.ltx` is **`gd_veteran`**, i.e. selector 3.)

Hard caps: `max_fire_wound_protection = 1.20`, `max_wound_protection = 2.20`. Bone-level
injury scales (`[actor_damage]`, format `<hit_scale>, <fwd_damage_anim_index>, <wound_scale>`):
`bip01_head`/`bip01_neck`/eyes/jaw = `1.0, 0, **2.0**`; `bip01_spine`/`spine1`/`spine2` =
`1.0, 0, 1.3–1.5`; `bip01_pelvis` = `0.9, 10, 1.2`; arms `0.7 → 0.5 → 0.25 (fingers)`;
legs `0.85 (thigh) → 0.65 (calf) → 0.5 (foot) → 0.25 (toe)`. So **head/neck wounds are
scaled 2×**, torso 1.5×, and extremities take progressively less.

Other survival-relevant actor values: `[actor_thd_gd_*]` sets `killing_hit_treshold = 0.0`,
`last_chance_health = 0.0`, `invulnerable_time = 0.0` in every preset — **there is no
last-chance or invulnerability mechanic in GAMMA**; `jump_speed = 6.85`, `crouch_coef = 0.45`,
`climb_coef = 0.625`, `run_coef = 2.41`, `sprint_koef = 2.08`, `walk_accel = 11.5`,
`camera_height_factor = 0.92`, `ph_mass = 94`, and quick-item defaults
`quick_item_1 = medkit`, `_2 = bandage`, `_3 = medkit_army`, `_4 = stimpack`.

## 11. Gear power and battery drain

- **Flashlights, NVGs, detectors and PDAs consume batteries** — the difficulty preset's
  `battery_consumption` multiplier is **0.5 (Tourist), 0.75 (Scavenger), 1.0 (Survivalist)**.
  Dead batteries are a real item: `batteries_dead` weighs **0.04 kg** and is a crafting input
  (`x_ammo_gauss`-adjacent recipes and exo PSU work use batteries), and every character starts
  with 2 of them.
- The manual reminds you that **detectors need batteries to work** and that **artefacts not in a
  container radiate you** — so a belt of artifacts is a radiation decision, not just a stat
  decision.
- **Weapon degradation** (`weapon_degradation` 0.5 / 0.75 / 1.0) and armour degradation
  (durability upgrades "reduce armor degradation", 0.9.5) are the long-run survival costs; the
  manual's whole repair chapter exists because of them.

## 12. Quick answers

| Question | Answer |
|---|---|
| Why am I still hurt after a medkit? | Medkits give **temporary (yellow)** limb HP; use a **post-heal** item (Ibuprofen, Fentanyl, Antidote, Yadulin) to convert it to permanent white HP. |
| What kills me instantly? | Main/Head/Torso health at 0, or **Psy health at 0**; there is no last-chance save. |
| How do I stop a bleed? | Bandage (slow), **tourniquet/`jgut` (fast)**, or a belt item with bleed recovery; watch artefacts with negative bleed recovery. |
| Why can't I sleep? | You are not tired enough — energy drinks/caffeine and small meals delay tiredness; sleeping pills force it; vodka/beer help. |
| How much can I carry? | `max_item_mass 50` kg, hard stop at `max_walk_weight 100` kg, raised by armour and the Strength skill. |
| Why do I suddenly limp? | `limping_health_begin = 0.09` leg damage, or stamina below `limping_power_begin = 0.18`. |
| Do I regenerate health over time? | No — `health_restore_v = 0.0`; healing is item-based. Sleep restores stamina, not health. |
| How do I cure radiation? | Anti-rad drugs, cigarettes/tobacco, water, alcohol; radioprotectors prevent it. Watch the bottom-left meter and **backtrack** out of patches. |
| Do artefacts hurt me? | Yes — radiation from artefacts **not in a container**, and some belt items have negative bleed recovery. |
| What does a "post-heal" side effect feel like? | Extreme hunger or dizziness; dizziness is cured by stamina-boosting medicine or water. |
| How do skills level? | Four trees (endurance, strength, survival, scavenging), max level 30, first level costs 750 points, each level changes a concrete stat. |
| Where do I get better food? | Cook it — basic kit at bonfires (no charcoal), advanced field cooker for buff meals. |

Cross-references: food/cooking recipes and the medical toolkit → `references/crafting-repairs.md`;
radiation and psy hazards in the world → `references/anomalies.md`; helmet and suit protection
values → `references/armor-outfits.md` and `references/artifacts.md`; damage maths on the
receiving end → `references/ballistics-damage.md`; difficulty, thirst, sleep and battery flags
in the settings → `references/keybinds-settings.md`; a HUD bar or buff that stopped working
after an update → `references/troubleshooting.md`.
