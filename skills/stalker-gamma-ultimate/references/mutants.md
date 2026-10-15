# Mutants — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: GAMMA's **Mutants Overhaul** creature configs
(`G.A.M.M.A. Mutants Overhaul/gamedata/configs/creatures/m_bloodsucker.ltx`, `m_boar.ltx`,
`m_cat.ltx`, `m_controller.ltx`, `m_fracture.ltx`, `m_giant.ltx`, `m_zombie.ltx`), the
Economy addon's loot tables `items/settings/mutant_loot.ltx` and price patch
`mod_system_mutant_parts_price_gamma.ltx`, the pelt patch `mod_system_grok_pelts.ltx`, the NPE
artefact tutorial's pelt paragraph, the hunting-kit rework
(`G_FLAT's and Grok's Hunting Kit Rework/…/mod_system_gamma_hunting_kit.ltx`), ZCP's own
`FAQs.txt` (population and "Not enough IDs"), the Global MCM defaults in `axr_options.ltx`
(`alife/general/alife_mutant_pop = 1.5`), and `Patchnotes.md` 0.9.5 (Balance → "Mutant and NPC
Spawns rebalance") and 0.9.3/0.9.1 sections. Snapshot: GAMMA 0.9.5 @
`ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. The roster GAMMA actually spawns

The loot tables are the cleanest roster of what exists in the pack, because every mutant that
can be skinned has an entry. From `mutant_loot.ltx` (section names verbatim):

| Mutant | Also in | Notable drops (item, count, probability) |
|---|---|---|
| **Bloodsucker** (`bloodsucker`) | Mutants Overhaul | `hide_bloodsucker` 1 / 0.10, `mutant_part_krovosos_jaw` 1 / 0.35, `mutant_part_krovosos_meat` 2 / 0.24, `mutant_part_heart_bloodsucker` 1 / 0.45 |
| **Boar** | Mutants Overhaul | `hide_boar` 0.08, `mutant_part_boar_leg` 4 / 0.18, `mutant_part_boar_chop` 3 / 0.20, `mutant_part_tusk_boar` 2 / 0.38 |
| **Burer** | 158-ABF | `hide_burer` 0.20, `mutant_part_burer_hand` 2 / 0.31, `mutant_part_brain_burer` 1 / 0.25 |
| **Chimera** | ZCP / spawn tables | `hide_chimera` 0.10, `mutant_part_chimera_kogot` 2 / 0.45, `mutant_part_chimera_claw` 4 / 0.24, `mutant_part_chimera_meat` 2 / 0.50, `mutant_part_heart_chimera` 1 / 0.25 |
| **Controller** | Mutants Overhaul (7 variants) | `mutant_part_controller_glass` 1 / 0.38, `mutant_part_controller_hand` 2 / 0.28, `hide_controller` 0.16 |
| **Dog** | vanilla AI | `mutant_part_dog_liver`/`_heart`/`_tail` 0.3/0.3/0.22, `mutant_part_dog_meat` 2 / 0.22 |
| **Flesh** | — | `hide_flesh` 0.12, `mutant_part_flesh_eye` 2 / 0.22, `mutant_part_flesh_meat` 3 / 0.22 |
| **Pseudogiant** (`gigant`) | Mutants Overhaul | `hide_pseudogiant` 0.16, `mutant_part_pseudogigant_hand` 2 / 0.44, `mutant_part_pseudogigant_eye` 2 / 0.44 |
| **Psy-dog** (`psy_dog`) | — | `mutant_part_fang_psevdodog` 4 / 0.33, `hide_psy_dog` 0.20, `mutant_part_controller_glass` 1 / 0.22, tail 0.44, meat 2 / 0.30 |
| **Pseudodog** | — | `mutant_part_fang_psevdodog` 4 / 0.33, `hide_pseudodog` 0.08, tail 0.27, meat 2 / 0.22 |
| **Snork** | — | `mutant_part_snork_leg` 2 / 0.37, `_hand` 0.1, `_mask` 0.1 |
| **Tushkano** | — | `mutant_part_tushkano_head` 1 / 0.31, `mutant_part_tushkano_meat` 1 / 0.44 |
| **Cat** | Mutants Overhaul | `mutant_part_cat_thyroid` 2 / 0.4, `mutant_part_cat_claw` 4 / 0.20, `mutant_part_cat_tail` 1 / 0.44 |
| **Fracture (zombified stalker)** | Mutants Overhaul | `mutant_part_fracture_hand` 2 / 0.44 |
| **Zombie** | Mutants Overhaul | `mutant_part_zombi_hand` 2 / 0.15, and bolts (`bolt = 6, 0.01`) |
| **Lurker** | — | `hide_lurker` 0.16, `mutant_part_lurker_tail` 1 / 0.45, `_eye` 2 / 0.22, `_meat` 2 / 0.34 |
| **Psysucker** | — | `hide_psysucker` 0.24, `mutant_part_psysucker_hand` 2 / 0.4, meat 2 / 0.22 |
| **Karlik (dwarf)** | — | `mutant_part_controller_glass` 1 / 0.22, `mutant_part_brain_burer` 1 / 0.22 |
| **Crows** | ambient | `mutant_part_crow_beak` 0.02, `swiss_knife` 0.022, `roubles` 2 / 0.3, `bullet_pistol_ap` 3 / 0.05 |

Beyond the loot roster, the pack ships dedicated configs and addons for the heavy hitters:
**Poltergeist** (`m_poltergeist`), **Snork**, **Burer**, **Night Mutants** (`248-`, mutants
that hunt at night), **HD mutant models** (`Umbrellord`), **New mutants icons parts**, and
**158-ABF** (Jurkonov) which carries additional creature tuning.

Also relevant: the pack's **Sin and Mutants are Allies** patch implies Sin squads and mutants
coexist rather than fight — expect mixed encounters in Sin territory.

## 2. Mutant damage model: they are *soft* targets

The NPE ammo tutorial's third card is the authoritative statement:

> **"Flesh Damage — Mutants are considered soft targets and are easier to defeat using high
> damage rounds. Armor Penetration hardly matters when hunting mutants."**

This is why the manual's anti-mutant list exists: **HP ammo, .357 magnum, .45 Hydrashock,
buckshots, slugs, 7.62×25 Pst** — all high-`ammo_k_hit`, low-`ammo_k_ap` rounds (see
`references/ballistics-damage.md` for the numbers). It is also why the tutorial adds the
counter-intuitive note: "a high rate of fire and a low recoil can often achieve better results
than bigger, slower, less controllable guns."

Per-mutant stat tuning lives in the Mutants Overhaul files. Verbatim examples:

| Config | `health_hit_part` | Notes |
|---|---|---|
| `m_bloodsucker` | **1.0** (was 0.8) | `health_restore_v = 0.0001`; influences defined for **fire**, **psy** and **radiation** (`fire_max_power 5`, `psy_max_power 5`, `radiation_max_power 0.01`, with linear/quadratic falloff terms); `spawn_phantom = m_phantom_bloodsucker`, `can_spawn_phantom = false` |
| `m_boar` | **1.0** | `health_restore_v` unset; attack/damage sections present |
| `m_cat` | **0.8** | `health_restore_v = 0.00002` |
| `m_controller` | **0.25** | `health_restore_v = 0.00007` |
| `m_fracture` | **0.4** | — |
| `m_giant` | **1** | `health_restore_v = 0.00003` |
| `m_zombie` | **1.0** | — |

`health_hit_part` is the multiplier applied to damage landing on that creature's "vital"
bone region — a lower number means a *smaller* weak point. A **controller at 0.25** and a
**fracture at 0.4** are therefore the two creatures where headshots are least rewarding, while
bloodsuckers, boars, giants and zombies take full damage on the vitals. (This is where
"the Controller takes forever to die" comes from, mechanically.)

**Controller variants** present in the config: `m_controller_normal`, `m_controller_normal2`,
`m_controller_psy`, `m_controller_normal666`, `m_controller_normal777`,
`m_controller_normal888`, `m_controller_normal1111` — i.e. a family of normal/psy versions
with numbered variants used by spawn tables.

**Bloodsucker influences** deserve their own note: the bloodsucker has separate
**fire / psy / radiation** influence curves with `max_power`, `linear_factor` and
`quadratic_factor`, which is what makes the "invisible enemy that damages you from a distance"
feel work.

## 3. Loot, skinning and pelts

### How corpse looting works

`mutant_loot.ltx` header: **`decay_time = 12000` seconds — after that a corpse can no longer
be looted.** Entries are `item, count, probability` triples grouped per mutant, mixed from
`misc_low` and `misc_high` pools. The `misc_high` pool (used for burer, controller, fracture
and karlik) includes medical supplies, drugs, food, cigarettes, tools and oddities —
verbatim examples: `medkit__1, 4, 0.0001`, `stimpack_army, 1, 0.005`, `drug_psy_blockade__1,
1, 0.001`, `roubles, 8, 0.08`, `vodka__1, 1, 0.002`, `joint, 4, 0.025`, `swiss_knife, 1,
0.0052`, `porn, 1, 0.007`.

### Pelts (the good loot)

Hidden items with belt bonuses come from `hide_*` sections; only **one pelt at a time** can be
equipped, and — the NPE tutorial again — **"The better the knife, the better the condition of
the Pelts."** Data from `mod_system_grok_pelts.ltx`:

| Pelt | Cost | Effect |
|---|---|---|
| `hide_flesh` | 6 200 RU | `power_restore_speed = 0.00099`, chemical immunity 0.37332 |
| `hide_boar` | 6 200 RU | **`additional_inventory_weight = 12`** (and `additional_inventory_weight2 = 12`), burn immunity 0.24375 |
| (family) | — | `hide_bloodsucker`, `hide_burer`, `hide_chimera`, `hide_controller`, `hide_lurker`, `hide_psy_dog`, `hide_pseudogiant`, `hide_psysucker` |

0.9.5 gave **Boar Pelt and Pseudogiant Pelt BRC and BRC mitigation** (see
`references/armor-outfits.md` §6 for what BRC means).

### Parts prices

`mod_system_mutant_parts_price_gamma.ltx` sets individual part values — the two entries read
verbatim: `mutant_part_heart_chimera = 5250`, `mutant_part_lurker_meat = 608`. Chimera hearts
are the expensive end; common meat is bulk income. **Selling mutant parts is one of the three
canonical ways to make money** (manual, *Money*), alongside no-combat tasks and artefacts to
the Ecologists.

### Hunting kit

The hunting-kit rework (`mod_system_gamma_hunting_kit.ltx`) defines `kit_hunt` as an `i_tool`
weighing **1.7 kg**, with a `disassemble_parts` list (`textile_patch_m, textile_patch_m,
swiss_knife`). The base game's crafting recipe for it (from `craft.ltx`) is
`x_kit_hunt = sewing_thread ×12, prt_o_fabrics_4 ×8, swiss_knife ×8, wpn_knife ×1` — i.e. a
committed skinning/harvesting investment. Related addons: **"G_FLAT's and Grok's Hunting Kit
Rework"**, **"G.A.M.M.A. Mutant Unstucker Remade"**, **"Monsters Unstucker"** (mutants
extricating themselves from geometry bugs).

## 4. Mutants bleeding, phantoms and other shipped mutant behaviours

| Addon (shipped in the list) | What it does |
|---|---|
| **Arszi's Mutant Bleeding** (`194204`) + `G.A.M.M.A. Arzsi's Mutants Bleeding Fixes` | mutants can bleed from damage |
| **Night Mutants** (`248-`) | night-specific mutant squads (`squad_descr_night_mutants.ltx`) |
| **More Dangerous Phantoms** (Demonized) + **Maybelline's Restore XCV phantoms** | phantom behaviour tuning |
| **NPCs Die in Emissions for Real** (`265-`) | **disabled in 0.9.5** — worth knowing, because players still expect it to work |
| **Sin and Mutants are Allies** | faction/mutant relations patch |
| **Tougher important NPCs and companions** (`51-`) | not mutants, but it changes who survives your fights |
| **Skill System** (`49-`) + `G.A.M.M.A. Skill System Balance` | survival/hunting skills that affect **hunting skill** and **bleed restore** — see `references/survival-mechanics.md` |
| **Monsters Unstucker / Mutant Unstucker Remade** | fixes for mutants stuck in terrain |

## 5. Populations: how many mutants exist, and how that changes

- **Global mutant population factor**: the pack's MCM defaults (`axr_options.ltx`) ship
  `alife/general/alife_mutant_pop = 1.5` (stalker population is `1`), plus
  `alife/general/excl_dist = 75` (exclusion distance around the player) and
  `alife/general/dynamic_anomalies = true`. These are player-visible MCM options.
- **ZCP (Zone Customization Project)** is the granular control surface. Its FAQ documents:
  squad sizes and a *variance* multiplier ("A squad size of 3 will lead to squads with triple
  the size of vanilla … a variance of 0.5 will lead to squads between half and 1.5× the size"),
  disabling mutant types (and replacing them with random spawns if you enable it), and *spawn
  templates* that decide what replaces removed mutants. Its spawn-group files
  (`spawn_groups/balanced.ltx`) assign per-faction mutant weights, e.g.
  `simulation_bloodsucker = 4`, `simulation_chimera = 2.3`.
- **The engine limitation you will meet if you crank this up**: ZCP's FAQ explains the
  "**Not enough IDs**" crash — the engine has **65 535 IDs** for stalkers, mutants, items and
  so on; stashes, spawn-heavy addons and huge populations all consume them. Its recommended
  remedies: load an earlier save and delete player stashes, trigger an emission to kill off
  stalkers, and then lower population/squad size/variance.
- **0.9.5 rebalanced mutant and NPC spawns deliberately**:
  - "**Chimera duo/trio replaced by 1 chimera + 2 pseudodogs**";
  - "**More pseudodogs in the north**", "Bit more pseudodogs in TC";
  - "**South chimera are easier** (weak, normal or normal2), **north chimera are stronger**";
  - "**Poltergeists as predatory_day + bigger squads + more common flame polter**";
  - "Bit more renegades in the north start maps" (people, not mutants, but the same patch);
  - **"Much less tanky ghost zombie from swamp quest"** (a bug-fix-flavoured balance change);
  - and the south-to-north population shift tied to the **psy helmet** storyline
    ("South / North population balance upon receiving the psy helmet to better tier the
    population across the Zone following the storyline progression").

  The design intent from the patch notes: "packs of chimeras should be rarer in the north.
  Moreover, as you progress with the story, the south will progressively become emptier as the
  north gets more populated, which should improve the tasking shifts as well."

## 6. Fighting mutants: what actually works

Built only from the mechanics above plus the two shipped gameplay knobs that bear on it:

| Threat | What the data says to do |
|---|---|
| **Anything common (dogs, fleshes, boars, tushkano, zombies)** | Buckshot or HP — high `ammo_k_hit`, cost-efficient. Snork packs want a fast weapon, not a big one. |
| **Bloodsucker** | It has separate fire/psy/radiation influence curves; kill it fast with high damage (it regenerates at `health_restore_v 0.0001`). `health_hit_part 1.0` means vitals take full damage. |
| **Controller** | `health_hit_part 0.25` — aim for the vitals only if you can hold the shot; otherwise out-damage it. Psy protection (psy-block, artefacts, helmets) is the defensive half; see `references/survival-mechanics.md`. |
| **Pseudogiant** | `health_hit_part 1` (vitals work), heavy ammo or shotguns at close range. Note the shipped `user.ltx` flag **`pseudogiant_can_damage_objects_on_stomp = 0`** — by default its stomp does **not** destroy objects, so hiding behind cover is legitimate. |
| **Chimera** | 0.9.5 changed encounters to **1 chimera + 2 pseudodogs**; southern chimeras are the weak/normal variants, northern ones hit harder. `hide_chimera` and the chimera heart (5 250 RU) make them lucrative. |
| **Poltergeist** | Since 0.9.5 they are `predatory_day` with bigger squads and more flame variants — treat them as an area-denial threat, not a loot piñata. |
| **Burer/Psysucker** | Both have `hide_*` drops and `misc_high` loot, so they are worth the ammo. Psysucker hides are the better of the two (0.24 vs 0.20 drop chance). |
| **Karlik** | Loot-only interesting: two `misc_high`-tier parts (controller glass and burer brain) at 0.22 each. |

Two reminders that follow from the loot table: **mutants give you bolts back** (zombies drop
`bolt`), and **corpses rot** — you have `decay_time` 12 000 seconds to loot them.

## 7. Quick answers

| Question | Answer |
|---|---|
| Which ammo for mutants? | HP, buckshot, slugs, .357 Magnum, .45 Hydrashock, 7.62×25 Pst, and generally anything with high damage / low AP. |
| Why does the Controller take so little damage? | `health_hit_part = 0.25`; only a quarter of the vital-region damage applies. |
| How do I get pelts? | Skin mutants; the knife's quality determines the pelt's condition; you can only wear one pelt at a time. |
| Why can't I loot this corpse any more? | `decay_time` — 12 000 seconds after death. |
| Chimeras keep showing up with dogs — bug? | No: 0.9.5 deliberately replaced chimera duos/trios with "1 chimera + 2 pseudodogs". |
| Where are the toughest mutants? | The north, and ZCP lets you make that worse. Southern chimeras are explicitly weaker than northern ones. |
| Why do I get "Not enough IDs" after raising populations? | The engine's 65 535-ID limit; lower population/squad size/variance and clear stashes (ZCP FAQ). |
| Can I turn mutants off? | Yes, via ZCP's mutant options — but existing squads are not despawned; they die off or you start a new game. |
| Do mutants drop anything worth carrying? | Yes — hearts, jaws, claws, pelts and `misc_high` loot. Hearts (`mutant_part_heart_chimera` 5 250 RU) are the headline. |

Cross-references: damage and AP mechanics → `references/ballistics-damage.md`; pelt bonuses
and belt slots → `references/armor-outfits.md` and `references/artifacts.md`; mutant part
prices and task rewards → `references/trading-economy.md`; which mutants lurk where →
`references/anomalies.md`; population changes over the story → `references/quests-storylines.md`.
