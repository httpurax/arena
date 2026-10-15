# Ballistics and damage — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual's **Ballistics System** article
(`article_gamma_ballistics_text`), the **NPE ammo tutorial** ("Using the right tool for the
right job" / "Armor Penetration" / "Flesh Damage"), the pack's own **BR breakpoint** comment
block and armour BR values in
`G.A.M.M.A. Actor Damage Balancer/…/mod_system_items_armors_br_class_rework.ltx`, the actor
hitbox patch `mod_system_actor_hitbox.ltx`, the bleed rework `mod_system_bleed_rework.ltx`,
`gamma_ammo_weapon_table.xlsx`, `G.A.M.M.A. Difficulty Presets Rebalance/…/difficulty.ltx`,
`G.A.M.M.A. Outfits Balances/…/ballist_res_sections.tsv`, the shipped `user.ltx`
(`g_dispersion_base`, `g_dispersion_factor`, `g_hit_pwr_modif`), `Patchnotes.md` 0.9.5
(**Balance → Armor Overhaul**, **UI**), and `README.md`'s design bullet list.
Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

GAMMA's combat model is called **GROBBS — Grok's Balanced Overhaul Of Ballistic System**.
The manual's description of the intent:

> "It changes the bullets and armor penetration from **PLAYER to NPCs** (not the other way
> around) using EFT's ammunition system as an inspiration. The goal is to have a more
> realistic ballistic system where you must take into account the armor of your enemy and the
> ammo type you are using."

Two consequences people take a long time to internalise:

1. **Armour penetration is a *player-side* system.** When you shoot an NPC, its armour's
   armour value is what your bullet must beat. (NPCs shooting *you* run through the player
   damage balancer instead — see §6.)
2. **Ammo beats guns.** Damage and penetration are dominated by the cartridge plus barrel
   condition, which is why 0.9.5 removed the damage stat from the gun tooltip.

---

## 1. The core rule (verbatim mechanics)

From `article_gamma_ballistics_text`:

- "**Ammo Armor Penetration (AP) power is compared to the limb armor of the opponent.**"
- "**If the AP power > limb armor, damage is applied.** If AP power is less than limb armor,
  no damage is applied and **limb armor is reduced based on AP power**."
- "Ammo with low AP power thus need to break an opponent's limb armor before starting to do
  damage. AP ammo is thus required to kill heavily armored targets."
- "FMJ and HP ammo will still work, but the enemy armor must be destroyed by many of these
  bullets to start doing damage."
- "**Leg and face armor are reduced.**"

So every engagement against an armoured stalker is a two-phase fight: *grind the armour of
the limb you are hitting* (phase 1), *then kill* (phase 2). Shooting a Nosorog with pistol FMJ
means phase 1 may never end.

The NPE tutorial adds the spatial model:

> "Stalkers have armor values split following three areas: **Head, Upper Body and Legs**. Each
> limb group has its own armor value depending on the armor the stalker wears. Each bullet
> gradually reduces the armor of the limb group it hits, depending on the bullet AP value."

This is visible in the data: `Outfits Balances/tools/ballist_res_sections.tsv` contains one
row per armour family listing the bone-protection value for every bone, and **hands and feet
are always exactly 0.3 × the torso value** (e.g. `actor_armor_55`: spine 0.6875, hands/feet
0.20625; `actor_armor_32`: 0.4 → 0.12; `actor_armor_3`: 0.0375 → 0.01125). Limb shots are the
mechanically intended answer to heavy armour — and the reason "Leg and face armor are
reduced".

## 2. The BR scale (0.17 → 0.80)

GAMMA names armour-penetration classes after the **Russian BR classification**, and the
manual gives the in-game reading of it:

| BR class | Penetrates |
|---|---|
| BR1–BR2 | light armour |
| BR3–BR4 | middle-class armour |
| BR5 | heavy armour |
| BR6 | exo armour |

Bullets display their armour penetration value **in their description**, so you can always
read the exact number in-game. The 0.9.5 armour rework publishes the **breakpoints** each
bullet family sits at (comment block in `mod_system_items_armors_br_class_rework.ltx`):

| BR value | Ammunition family |
|---|---|
| **0.17** | pistol FMJ |
| **0.23** | slugs |
| **0.27** | rifle FMJ |
| **0.33** | sniper FMJ |
| **0.38** | pistol AP |
| **0.45** | sniper UP **and** AP slug |
| **0.49** | 5.45×39 AP |
| **0.52** | 5.56×45 AP |
| **0.57** | 7.62×39 AP |
| **0.62** | 7.62×51 AP |
| **0.80** | 7.62×54R AP |

Against the armour side of the same file:

| Armour | BR class (`br_class` = `hit_fraction_actor`) |
|---|---|
| Nosorog line (all six faction Nosorogs) | 0.17 |
| Exo line (`*_exo_outfit`) | 0.265 |
| heavy suits | 0.28 |
| mid suits | 0.34 / 0.37 / 0.40 |
| IBAz / heavy assault | 0.47 / 0.48 / 0.50 / 0.52 |
| light jackets | ~0.79 and up |

**How to read that table in one sentence:** pistol FMJ (0.17) is at *exactly* Nosorog class,
rifle FMJ (0.27) mostly grinds exos, 5.45/5.56 AP (0.49/0.52) is the first common round that
beats a Nosorog outright, and 7.62×54R AP (0.80) defeats everything in the game's armour
scale.

## 3. Ammunition types: what to load, and when

| Type | What it is for | Cost character | Notes from the manual |
|---|---|---|---|
| **FMJ** | lightly armoured stalkers; general use | cheap | "should be used to kill lightly armored targets or as a cheaper and less effective replacement for AP ammo against armored targets" |
| **HP** | **mutants** | a bit more than FMJ | "even less AP power than FMJ"; mutants are soft targets |
| **AP** | every armoured target, up to endgame | expensive | "Expensive but will defeat any endgame heavily armored target. … They are end game ammo, don't use them against lightly armored targets or you will waste money" |
| **Slugs** | mutants *and* stalkers | mid | "AP Slugs are best against stalkers" |
| **Buckshot** | early stalkers, mutants | cheap | "will work as inexpensive, early game ammo against stalkers. Forget about it mid and late game: Good for mutants, bad for exos" |
| **Sniper** | precision kills | very expensive | ".338 Lapua will one shot most enemies with a hit to the chest if you can afford it" |
| **Special anti-mutant rounds** | mutants | — | "HP ammo, .357 magnum, .45 Hydrashock, buckshots, slugs, 7.62x25 Pst" |

### Faction ammunition doctrine (who you are actually fighting)

| Faction | Behaviour | Source |
|---|---|---|
| **Monolith** | "only using AP ammo" | manual |
| **Sin** | "only using AP ammo, mainly using heavy machine guns, and much more resistant than a normal human being" | manual |
| **ISG / UNISG** | "very good gear, only use AP ammo and have a higher ammo penetration resistance" | manual |
| **Master and Legend stalkers** | "use AP ammo" for most of them | manual |
| NATO factions (Mercenaries, Clear Sky, Freedom, UNISG) | supply NATO ammo/attachments | manual + `good_weapons.txt` |
| WP factions (Military, Loner, Duty, Bandits, Renegades, Monolith) | supply WP ammo/attachments | manual + `good_weapons.txt` |
| Monolith NPCs specifically | "about 50 % chance to have a NATO or WP gun" | manual |

0.9.5 bugfix list contains a revealing entry for Sin: "**Fixed Sin increased AP res (10 %)**" —
i.e. Sin's AP resistance is a deliberate stat, not flavour text.

**Practical loadout advice (derived, not invented):** carry a cheap FMJ/HP load for mutants
and scavenging, and a magazine of the best AP you can afford for the armoured factions you
expect to meet. Sniper ammo pays for itself only against targets your rifle can actually
kill in one hit.

## 4. The ammo spreadsheet, decoded

`gamma_ammo_weapon_table.xlsx` documents how GAMMA derives damage. Its header row defines the
model, and the reference row is `7.62x51`:

- `base game dmg = 66`, `reference Joules = 3562`, `reference damage = 70.29`.
- Per ammo: `Ammo`, `Type` (AP / DMG / Perf / EX), `price`, `price/round`,
  `damage per Rouble`, `pen per Rouble`, **`ammo_k_ap`** (the AP multiplier),
  **`ammo_k_hit`** (the damage multiplier), **`gun power`** (weapon coefficient),
  `total damage = gun power × ammo_k_hit × base game dmg`, `in game displayed power`,
  `IRL Joules`, `IRL Speed`, `Overpen damage factor`,
  `Joules multiplier to ref`, `In game power based on Joules`,
  `In game power adjusted by overpen factor`.

Selected rows (verbatim from the sheet):

| Ammo | Type | Price (per unit) | Price/round | `ammo_k_ap` | `ammo_k_hit` | gun power | total damage |
|---|---|---|---|---|---|---|---|
| `ammo_9x19_fmj` | Perf | 645 | 43 | 0.17 | 0.70 | 0.45 | 20.79 |
| `ammo_9x19_ap` | AP | 2350 | 156.7 | 0.34 | 0.70 | 0.45 | 20.79 |
| `ammo_9x18_pmm` | DMG | 1150 | 76.7 | 0.08 | 1.40 | 0.45 | 41.58 |
| `ammo_5.45x39_fmj` | Perf | 1350 | 90 | 0.27 | 1.14 | 0.50 | 37.62 |
| `ammo_5.45x39_ap` | AP | 5100 | 340 | 0.47 | 1.10 | 0.50 | 36.30 |
| `ammo_5.56x45_ap` | AP | 5500 | 366.7 | 0.52 | 1.05 | 0.50 | 34.65 |
| `ammo_7.62x39_ap` | AP | 5900 | 393.3 | 0.55 | 1.17 | 0.58 | 44.79 |
| `ammo_7.62x51_ap` | AP | 7500 | 500 | 0.62 | 0.89 | 1.00 | 58.74 |
| `ammo_7.62x54_ap` | AP | 9500 | 950 | 0.80 | 0.85 | 1.10 | 61.71 |
| `ammo_338_federal` | DMG | 4000 | 400 | 0.18 | **10.70** | 0.85 | **600.27** |
| `ammo_357_hp_mag` | DMG | 2600 | 200 | 0.30 | 2.60 | 0.60 | 102.96 |
| `ammo_12x70_buck` | DMG | 750 | 75 | 0.27 | 3.78 | 0.80 | 199.58 |
| `ammo_12x76_zhekan` | Perf | 1450 | 145 | 0.23 | 2.70 | 0.80 | 142.56 |
| `ammo_23x75_shrapnel` | DMG | 2000 | 200 | 0.36 | 9.00 | 0.48 | 285.12 |
| `ammo_magnum_300` | AP | 17000 | 1700 | 1.40 | 1.26 | 1.20 | 99.79 |
| `ammo_og-7b` (RPG) | EX | 12490 | 416.3 | 0.37 | 3.00 | 3.00 | 594 |

Read the two `k` columns as the design levers: **AP rounds trade damage for penetration**
(e.g. 9×19 AP has the same `ammo_k_hit` as FMJ but 2× the `ammo_k_ap`), and **"DMG" rounds
are mutant killers** (9×18 PMM, .357 HP, buckshot, shrapnel, the absurd `.338 Federal` at
`ammo_k_hit = 10.7`). Shotgun payloads carry huge `ammo_k_hit` with tiny `ammo_k_ap` — which
is exactly why buckshot mangles mutants and bounces off exos.

The sheet also models **overpenetration**: a shot that passes through a soft target deals
reduced damage, derived from IRL joules and a per-cartridge `Overpen damage factor`. That is
why the sheet carries both a "Joules power" and an "adjusted by overpen factor" column.

## 5. Range, dispersion and 3D ballistics

- **3D ballistics is on by default in 0.9.5**: "guns will shoot where the barrel is aiming,
  which puts more emphasis on using lasers for hip firing." Laser rendering was improved (the
  laser's size/brightness changes with distance) as part of the same patch.
- Dispersion is a *difficulty* setting as well as a weapon property. The shipped `user.ltx`
  carries `g_dispersion_base 1.3` and `g_dispersion_factor 1.5`; `difficulty.ltx` overrides
  them per gameplay preset: **Easy 2.3 / 3.2**, **Medium 2.0 / 2.2**, **Hard 1.7 / 1.7**.
  Lower is *harder* (less NPC inaccuracy cushion — the presets use larger dispersion for
  easier play).
- The **Community's most common complaint about 0.9.5** — that guns no longer show a damage
  stat — is answered by the same model: damage = ammo × gun power × barrel condition. The
  Reddit discussion of 0.9.5 notes that "damage is largely tied to it's ammo" while
  acknowledging that some guns do punch above their weight, and that GAMMA removed most
  calibre conversions to keep the weapon/ammo pairings clean.
- Shooting **through bushes/obstacles** applies a damage debuff (community-reported in the
  same thread; 0.9.5 also rebalanced a "transparency threshold" so NPCs cannot shoot the
  player through bushes as easily).

## 6. The other half: how the player takes damage

GAMMA's player-side model is the **Actor Damage Balancer** (ADD), and it is a separate system
from GROBBS.

### Hitboxes

`mod_system_actor_hitbox.ltx` defines exactly **three** boxes for the player:

| Box | Centre (x, y, z) | Size |
|---|---|---|
| head | 0.0, 0.90, 0.0 | 0.25 × 0.90 × 0.25 |
| torso | 0.0, 0.65, 0.0 | 0.30 × 0.65 × 0.25 |
| legs | 0.0, 0.20, 0.0 | 0.30 × 0.20 × 0.35 |

(Note the head box's 0.90 vertical size — head/upper-body is a single large target; you are
not protecting a pinhead.)

### Bleeding

`mod_system_bleed_rework.ltx` rebalances the anti-bleed items and the rate bleeding takes
hold:

| Item | Cost | `boost_time` | `boost_bleeding_restore` |
|---|---|---|---|
| Tourniquet (`jgut`) | 2 100 RU | 10 | 0.05 |
| Bandage (`bandage`) | 950 RU | 25 | 0.004 |

Plus a global `[actor_condition] bleed_speed_k = 5` — bleeding escalates quickly, and the
tourniquet is the *fast* answer while the bandage is the *slow* one (the NPE healing tutorial
says the same in words: "Bandage (slow bleed heal). Tourniquet (fast bleed heal)").

### Armour immunities, defensive boosts and explosives

The balancer ships four more patches that shape incoming damage:

- `mod_system_items_armor_immunities.ltx` — per-armour damage-type immunity handling;
- `mod_system_items_defensive_boosts_rebalance.ltx` — rebalances defensive-boost items
  (drugs/injectors that raise resistances; "damage resistance injectors work (indicated by a
  shield icon)" per the manual);
- `mod_system_grok_explosives_rebalance.ltx` — grenades/mines;
- `mod_system_momopate_pba_tweaks.ltx` — the Perk-Based Artefacts interaction
  (`st_zzz_momopate_pba_tweaks.xml` carries the text).

### Difficulty presets that touch damage

From `difficulty.ltx` `[gdiff_*]` (Easy / Medium / Hard):

| Setting | Easy (`gdiff_1`) | Medium (`gdiff_2`) | Hard (`gdiff_3`) |
|---|---|---|---|
| `actor_immunities` (selector into `actor.ltx`) | 1 | 2 | 3 |
| `hit_power` (bullet power *vs NPCs*) | 1 | 1 | 1 |
| `dispersion_base` | 2.3 | 2.0 | 1.7 |
| `dispersion_factor` | 3.2 | 2.2 | 1.7 |
| `power_loss_bias` (stamina drain) | 0.3 | 0.3 | 0.3 |
| `max_weight` (base carry kg) | 50 | 50 | 50 |

Plus the shipped `user.ltx` baseline: **`g_game_difficulty gd_veteran`** and
`g_hit_pwr_modif 1.` — the difficulty selector and the bullet-power modifier both exist and
are exposed in the Extra Options menu.

## 7. Armour caps and the 0.9.5 BRC change

Quoting the 0.9.5 Balance section:

- "**max res caps to 90 %**"
- "**BRC Mitigation limited to 90 % max**"
- "Remove BR% from plates, added strike res to higher tiers"
- "Boar pelt and Pseudogiant pelt give BRC and BRC mitigation"
- "Kogot and Ear give **+3 % BRC premitigation each (stacks)**"
- "**BR Class Premitigation stat display in inventory**"

If a player asks "why does my 100 % protection build still take damage?", the answer is in
those lines: resistances are capped, and BRC mitigation itself is capped, so stacking beyond
the cap is wasted. The gameplay reason: 0.9.5 wanted belt loadouts to be a choice between
**BR %**, **BRC + BRC mitigation**, or a mix.

## 8. Quick answers

| Question | Answer |
|---|---|
| Why is my gun useless against exos? | Your AP is below their BR class. Exos sit at 0.265; Nosorogs at 0.17. FMJ rifle rounds grind armour instead of damaging flesh. Load AP or hit limbs. |
| Which ammo kills mutants? | HP, buckshot, slugs, .357/.45 "DMG" rounds, shrapnel, and the anti-mutant list from the manual (7.62×25 Pst included). Penetration is irrelevant to mutants. |
| Why do my bullets "do nothing" while the enemy's HP bar barely moves? | You are in armour-grinding phase. Every hit reduces the limb's armour; damage starts once your AP beats what is left. |
| Is the .338 a one-shot? | The manual says yes — a chest hit will one-shot most enemies "if you can afford it". |
| Where do I see AP values? | In item descriptions (bullets display their penetration), and the BR breakpoint table above tells you what class to aim for. |
| Does barrel condition affect damage/penetration? | Yes — explicitly: "The barrel changes the damage the gun deals and the strength of ammo penetration. A gun with a very bad barrel condition will deal almost no damage." |
| Why did the gun damage stat vanish? | 0.9.5 UI change (the Reddit thread confirms it was intentional). Use the ammo table and the new recoil stat. |
| How do I preview an enemy's protection? | You cannot; but you can learn the BR classes per faction loadout — Monolith/Sin/ISG are AP-only and tough, low-tier Bandits/Renegades are not. |
| Why do NPCs hit me through bushes less often now? | 0.9.5 "Edited transparency threshold for stalkers so it's not as easy for NPCs to shoot the player through bushes while remaining balanced." |

Cross-references: ammo prices and trader supply → `references/trading-economy.md`; which kit
fixes the barrel → `references/weapons.md` and `references/crafting-repairs.md`; armour BR
values in full → `references/armor-outfits.md`; mutant-specific damage rules →
`references/mutants.md`; the difficulty presets that set these dispersion and damage
multipliers → `references/keybinds-settings.md`.
