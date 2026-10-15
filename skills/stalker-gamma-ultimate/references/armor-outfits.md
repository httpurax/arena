# Armor and outfits — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: GAMMA's armour table **`armor_values.tsv`** and bone-protection table
**`ballist_res_sections.tsv`** from `G.A.M.M.A. Outfits Balances/tools/` (161 outfits, 22
columns), the shipped balance patches `mod_system_grok_plates_rework.ltx`,
`mod_system_items_armors_br_class_rework.ltx` (699 lines, with the pack's own **BR
breakpoint** comment block), `mod_system_grok_pelts.ltx`, the armour-speed table
`configs/items/settings/outfit_speed.ltx`, the **NPE armour-repair tutorial**
(`npe_gamma_tutorial_repair_armor.xml`), the PDA manual articles *Protection Plates*
(`article_gamma_plates_text`) and *Disguise* (`article_gamma_disguise_text`), and
`Patchnotes.md` 0.9.5 ("Armor Overhaul" sections in *General description* and *Balance*).
Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d1`.

0.9.5 is the version that **rebuilt every armour stat from scratch**, so a 2023 guide's
"best suit" ranking is worthless now. The pack's own framing:

> "There's no 'best suit'; they all come with pros and cons, and it's up to how you like to
> play to prioritize certain types of suits." — *Patchnotes.md*, 0.9.5

---

## 1. The armour classes

GAMMA's armour table classifies all 161 outfits into **types** (`New Type`). The count of
entries per type in the shipped table:

| Type | Entries | Character |
|---|---|---|
| `Exo` | 12 | classic exoskeletons |
| `Exolight` | 18 | lighter exo variants (0.9.5 addition in the type list) |
| `Protoexo` | 7 | late "exo-prototype" suits; the most expensive gear in the game |
| `Nosorog` | 6 | the armoured Exo line (Rhino) — the top of the BR-scale |
| `SEVA` / `Heavy SEVA` / `Hybrid SEVA` | 12 / 3 / 2 | sealed combination suits |
| `NBC` | 7 | NBC/sealed suits |
| `PS5` / `PS6` / `IB AZ` / `SSP` / `Skat` / `MC Suit` | 6 / 6 / 7 / 6 / 9 / 6 | military suit families |
| `Sunrise` / `Jacket` / `LC Suit` / `Trenchcoat` / `Overcoat` / `Ghillie` / `Nomad` / `Wastelander` / `ACE` / `Sin Heavycoat` | 6 / 9 / 4 / 2 / 2 / 1 / 1 / 1 / 1 / 2 | light and faction-flavour gear |
| `Metal` / `CS-3B` / `CS1` / `CS2` / `CS-3` / `STS` / `STS-H` / `Beril-5M` / `Beril-5H "Goshen"` / `Voyager` / `Predator` / `Skat Exo` | 1 / 1 / 1 / 3 / 4 / 2 / 1 / 5 / 1 / 1 / 2 / 2 | everything else |

Faction distribution of the table (a good proxy for what you can loot from whom): Duty 25,
Mercenary 23, Free Stalkers 18, Freedom 14, Clear Sky 13, Bandit 12, UNISG 11, Monolith 11,
Ecologist 9, Unknown 9, Military 8, Sin 5, Renegade 3.

**Every armour carries its class on its icon** (NPE tutorial), and that class decides which
repair kit you need. The shipped repair-type distribution is: `outfit_medium` 57,
`outfit_heavy` 50, `outfit_light` 21, `outfit_exo` 20, `outfit_novice` 13.

| Armour class (UI) | Internal repair type | Repair kit |
|---|---|---|
| **Light** (jackets, novice gear) | `outfit_novice` / `outfit_light` | Light Repair Kit |
| **Medium** | `outfit_medium` | Medium Repair Kit |
| **Heavy** | `outfit_heavy` | Heavy Repair Kit |
| **Exo** (exoskeletons, Nosorog, proto-exo) | `outfit_exo` | Exo Repair Kit |

## 2. What the stats mean

The armour table's columns are the stat set GAMMA balances (and what the in-game
tooltip shows). Read them as *fractions of damage blocked*, per damage type:

`radiation_protection, chemical_burn_protection, shock_protection, burn_protection,
telepatic_protection, strike_protection, explosion_protection, wound_protection`
(ballistic), plus `cost`, `artefact_count` (**belt slots**), `Speed`,
`additional_inventory_weight` (**carry bonus in kg**), `inv_weight`, and `repair_type`.

Two more columns matter for ballistics:

| Column | Meaning |
|---|---|
| `bip01_spine` / `bones_koeff_protection` | the armour's per-bone protection table. Hands and feet get **a fraction of the spine value** — the shipped table uses **0.3 ×** (e.g. spine `0.6875` → hands/feet `0.20625`; spine `0.3625` → `0.10875`). That is why leg/arm hits penetrate "well-armoured" people |
| `hit_fraction_actor` | the damage fraction that gets through before the BR class system (see `references/ballistics-damage.md`) |

### The numbers in circulation

All read from `armor_values.tsv` (draft table — verify in game):

| Metric | Range in the table |
|---|---|
| Cost | **6 458 RU** (Armored Leather Jacket) → **224 759 RU** (Sunrise Exoskeleton) |
| Belt slots (`artefact_count`) | 1 (14 outfits) up to **6** (2 outfits); most common are 3 (62) and 2 (57) |
| Movement `Speed` multiplier | **0.90** (UNISG Exosuit) → **1.12** ("Sunset" tactical suit; Redline Leather Jacket) |
| `hit_fraction_actor` | 0.24 (best protection) → 0.94 (worst) |
| Carry bonus | up to **+124.8 kg** (Stolen Exoskeleton); exos generally +100 kg class |
| Best ballistic `wound_protection` in the table | IBAz line (Military Stalker IBAz Suit / IBAz Universal Protection Suit, ≈0.862), then Interceptor Body Armor (≈0.790) |

Examples to calibrate your expectations:

| Outfit | Faction | Type | Cost | Spine bone protection | `hit_fraction_actor` | Belt slots | Speed | Carry bonus |
|---|---|---|---|---|---|---|---|---|
| Military Service Outfit | Military | Metal | 8 167 | 0.20 | 0.79 | 1 | 0.97 | +10.8 kg |
| Stolen Exoskeleton | Bandit | Exo | 155 905 | 0.55 | 0.53 | 2 | 1.06 | +124.8 kg |
| Looted Exosuit | Bandit | Exolight | 87 336 | 0.525 | 0.56 | 2 | 0.96 | +65 kg |
| Military Stalker Nosorog | Military | Nosorog | 130 866 | 0.6875 | 0.31 | 2 | 1.02 | +103.5 kg |

**Exoskeletons do not make you slow in the shipped table — they mostly slow your *sprint*.**
`outfit_speed.ltx` sets a `[sprint_speed]` of **0.95** for *every* exo, exolight, nosorog and
proto-exo outfit (the full list is in the file), while walking `[speed]` varies per outfit:
`army_nosorog_outfit = 1.02`, `army_outfit = 0.97`, `bandit_exo_outfit = 1.06`,
`bandit_nbc_outfit = 1.12`, `bandit_scientific_outfit = 1.04`, and so on. This is the
*Outfits Affects Movespeed* system: your suit is a mobility build decision, not just a
protection number.

The **UNISG Exosuit (0.90)** and **UNISG LC Suit (0.91)** are the slowest entries in the
shipped table; the fastest are the light `Sunset` tactical suit and the Redline Leather
Jacket at **1.12**.

## 3. BR class and armour penetration (why armour feels different in 0.9.5)

0.9.5 changed how bullets interact with armour: **BR Class (BRC) now gives additional
multiplicative protection on top of BR %**, so bullet damage depends on two "defence buckets"
that belt attachments can feed — you can build around BRC + BRC Mitigation, or stack BR %,
or both. Caps matter: **max res caps are 90 %** and **BRC mitigation is limited to 90 %**.

The pack's own BR breakpoint comment (at the top of
`mod_system_items_armors_br_class_rework.ltx`) is the cleanest explanation of the scale:

```
;---- BR BREAKPOINTS
;---- 0.17 - PISTOL FMJ
;---- 0.23 - SLUGS
;---- 0.27 - RIFLE FMJ
;---- 0.33 - SNIPER FMJ
;---- 0.38 - PISTOL AP
;---- 0.45 - SNIPER UP + AP SLUG
;---- 0.49 - 5.45 AP
;---- 0.52 - 5.56 AP
;---- 0.57 - 7.62x39 AP
;---- 0.62 - 7.62x51 AP
;---- 0.80 - 7.62x54r AP
```

And the armour side of the same file (`hit_fraction_actor` = `br_class` in most entries):

| Armour group | BR class |
|---|---|
| NOSOROG (`army_nosorog_outfit`, `dolg_nosorog_outfit`, `freedom_nosorog_outfit`, `isg_nosorog_outfit`, `merc_nosorog_outfit`, `monolith_nosorog_outfit`) | **0.17** |
| EXOS (the `*_exo_outfit` family) | **0.265** |
| several heavy suits | 0.28 |
| mid suits | 0.34 / 0.37 / 0.40 |
| IBAz & heavy assault sets | 0.47 / 0.48 / 0.50 / 0.52 |
| light jackets | up to ~0.79 (and beyond in the wider table) |

Practical reading: **a Nosorog shrugs off anything below 0.17 AP** (all pistol FMJ, slugs,
rifle and sniper FMJ — they only grind the armour), and needs **5.45 AP / 5.56 AP and up** to
be threatened. Conversely, light jackets are penetrated by pistol FMJ. This is the mechanical
reason GAMMA's factions are described as "AP-only" in the north.

## 4. Repairing armour

From the NPE armour tutorial, which is the authoritative in-game text:

- **Below 50 %:** you need an **armour Repair Kit and Spare Parts**, used **at a
  workbench** (or by right-clicking a toolkit to open the portable workbench). "The
  resulting armor condition is based on the average of all parts." **Swapping parts does not
  consume repair kit charges.**
- **Repairing spare parts themselves:** use the appropriate repair item on the part (the
  game tells you which: right-click the part → *details*, or hover it to see the highlighted
  repair item you own). See `references/crafting-repairs.md` for the item list.
- **At or above 65 %:** use **Maintenance Kits** — the game's own words: "Maintenance Kits
  correspond to **Sewing Kits and Glues**. … can be purchased readily at any mechanic
  trader." Maintenance kits can be boosted with **Supportive Materials** (the condition gain
  is shown when you right-click the kit).
- **Hold Left Ctrl while hovering a looted armour** to preview its stats **at 100 %
  condition** — the tutorial recommends this before deciding whether a suit is worth
  repairing.
- **Mechanics cannot repair armour in GAMMA** (manual, `article_gamma_reparm_text`): "In
  GAMMA, mechanics cannot repair armor."

Manual-side summary (`article_gamma_reparm_text`): armours are found in stashes or on dead
stalkers; collect parts **above 50 %** condition and repair them to 100 %; below 50 % you
must change the parts; "Be sure to maintain your armor condition often with repair items."
0.9.5 also made **helmet and armour repair kits more expensive** at the top end: "Increased
cost and crafting cost of Type D cleaning kit and repair kit", "Increase exo and heavy repair
kits costs and crafting costs" (Economy section), plus new crafting gating (Exo Repair Kit
now crafts from a Heavy Repair Kit + sewing kits; see `references/crafting-repairs.md`).

Optional related addons (all shipped, mostly **disabled by default** — check your MO2 list):
`G.A.M.M.A. Armors repair like WPO`, `G.A.M.M.A. Helmets need armor repair kits`,
`G.A.M.M.A. Armors no integrated helmet`, `G.A.M.M.A. Armors Balancing`,
`G.A.M.M.A. Exo Balance`, `G.A.M.M.A. Starter items are not broken`.

## 5. Helmets

- Helmets have their own protection stats and their own role: **psy protection** and the
  gas-mask requirement for the north. "Entering the Army Warehouses or areas further North
  without a gas mask or proper anti-radiation medication can kill you if you hit just one bad
  radiation patch" (manual, radiation article).
- 0.9.5 introduced **helmet psy-boost** handling
  (`mod_system_items_helmets_psy_boost.ltx`), **defensive-boost rebalancing**
  (`mod_system_items_defensive_boosts_rebalance.ltx`) and an **armour-immunity** pass
  (`mod_system_items_armor_immunities.ltx`) inside `G.A.M.M.A. Actor Damage Balancer`.
- Gameplay consequences that the community asks about: the **PSY helmet** is the
  progression marker that repopulates the north ("South / North population balance upon
  receiving the psy helmet" — 0.9.5 Progression), and the shipped *hideout furniture*
  expansion adds helmet storage/QoL.
- Optional addons exist for looks only (`G.A.M.M.A. No Masks Textures`) and for a
  no-integrated-helmet rule (`G.A.M.M.A. Armors no integrated helmet`) — they change what you
  can wear, so treat them as difficulty options.

## 6. Belt items: artefacts, plates, pelts

Your armour's `artefact_count` is the number of **belt slots**; the belt holds defensive
artefacts, plates and pelts (see `references/artifacts.md`).

**Protection plates** (manual, *Protection Plates* + 0.9.5 Balance):

- Plates are "on par with artefacts protection, reaching about **15 % ballistic and explosive
  protection**".
- They **no longer have electric-resistance penalties** and **do not protect you from mutants**.
- **They cannot be bought** any more; basic Kevlar plates come from questlines or are crafted
  from armour parts. The upgrade chain: **T1 Kevlar → T2 Kevlar → T3 metallic → T4 metallic**,
  upgraded through crafting with large amounts of armour parts (armour parts are marked with
  the hammer-and-pincer icon).
- 0.9.5 change: **plates lost their BR %** and higher tiers instead gained **strike
  resistance**. In the shipped values, `af_kevlar` gives 0.0403 explosion immunity (0.0806
  upgraded) and `af_plates` gives 0.0909 strike / 0.134 explosion (0.1454 / 0.2 upgraded).

**Pelts** (from skinning mutants, `mod_system_grok_pelts.ltx`): only **one pelt at a time**,
and pelts provide *only* bonuses. Examples straight from the file: `hide_flesh` 6 200 RU with
`power_restore_speed = 0.00099` and chemical immunity 0.37332; `hide_boar` 6 200 RU with
**+12 kg carry weight** and burn immunity 0.24375. 0.9.5 gave **Boar Pelt and Pseudogiant
Pelt** BRC and BRC mitigation, and stacked **+3 % BRC pre-mitigation each** for **Kogot and
Ear** artefacts. The community "Rookie's Guide" gives the same family of examples from play
(Controller Scalp +30 % psychic, Pseudodog Fur +30 electro, Flesh Hide +30 chemical, Boar
Pelt +30 fire, Psy-dog Fur +15 to several resistances) — treat those as community-reported.
**The better your knife, the better the condition of the pelt you get** (NPE artefact
tutorial).

## 7. Disguise (wearing another faction's armour)

Manual, *Disguise*:

- You can wear another faction's armour and be considered a member of that faction **if the
  faction patch is attached**. Tearing the patch off returns you to your own faction.
- **Attach the patch out of sight** of other stalkers, or the disguise is immediately blown.
- **Armour condition affects how easily you are spotted**, and **high-ranked stalkers see
  through disguises more easily** than low-ranked ones.
- Ecologist armour is described as "especially powerful" for this, but "very hard to get your
  hands on in GAMMA".
- Shipped addons interact here: `G.A.M.M.A. Disguise does not remove patches`,
  `G.A.M.M.A. Killing Friends Reduces Goodwill`, and the disguise system pairs with faction
  relations (see `references/factions.md`).

## 8. Armour progression, in practice

1. **Novice (jackets, `outfit_novice`):** 6.5–8 k RU tier. Protection is symbolic; treat the
   armour as inventory space with a little ballistic resistance. Belt slots 1.
2. **Light/medium suits (`outfit_light`, `outfit_medium`):** where most of the table lives
   (78 entries). This is where "Repair Kit class = Light/Medium" and the first real carry
   bonuses arrive.
3. **Heavy suits (`outfit_heavy`, 50 entries):** IBAz/PS5/SEVA families; good ballistic
   numbers, some BR class ~0.34–0.52, often 2–4 belt slots.
4. **Exo and Exolight (`outfit_exo`, `outfit_exolight`):** the powered-armour tier. Sprint
   drops to 0.95, carry jumps to the +65…+125 kg range, BR class 0.265. Requires the **Exo
   Repair Kit** (the most expensive kit in the game since 0.9.5) and, per the manual and
   shipped addons, exoskeleton **PSU/battery** upkeep ("Maintaining an exoskeleton armor will
   also be a money sink since you often need to buy expensive exo batteries" — *Money*
   article). 0.9.5 added an **Exo battery crafting recipe from Gauss ammo**.
5. **Nosorog / Protoexo (13 entries):** the endgame. BR class 0.17 (Nosorog), highest
   protection, 3–5 belt slots, and the (re-enabled) **Nosorog despawn-latency fix** in 0.9.5
   Bugfix list — a hint that these suits used to be lost on map transitions. The pack ships
   `G.A.M.M.A. No Exos in the South` as an optional restriction if you want exoskeletons to
   stay a northern phenomenon.

Because armour cannot be bought, progression is **stash- and corpse-driven**: 0.9.5's Economy
notes "Bit less armors in stashes" — a deliberate tightening — so expect to repair what you
kill people for. `G_A.M.M.A. Armor Exchange` exists as an optional addon if you want to trade
armour after all.

## 9. Quick answers

| Question | Answer |
|---|---|
| Why am I so slow? | Check `Speed` for the suit and, above all, whether it is an exo (`sprint_speed 0.95` for the whole exo family). Your carry load and stamina skills also matter. |
| Why does my armour do nothing against bullets? | Check the **BR class** of your suit vs the ammo: 0.17 Nosorog vs pistol FMJ = immune-by-comparison; a jacket (0.7+) vs AP rifle rounds = paper. See `references/ballistics-damage.md`. |
| Which repair kit for my suit? | The class on the icon: Light/Medium/Heavy/Exo. Kits cost more the higher the class (0.9.5 raised Exo/Heavy). |
| How do I fix armour between 50 % and 65 %? | Parts-swapping below 50 %; maintenance kits (sewing kits, glues) at/above 65 %. In the 50–65 band you are expected to keep swapping parts until you are above 65 %. |
| Can a mechanic repair my armour? | No. |
| Can I buy plates? | No, not any more — questlines or crafting with armour parts. |
| Best belt loadout? | Depends on the two defence buckets: BR % vs **BRC + BRC mitigation**. Kogot/Ear stack +3 % BRC pre-mitigation each; pellets/pelts add BRC and BRC mitigation in 0.9.5. |
| How do I preview a looted suit? | Hold **Left Ctrl** while hovering it to see its stats at 100 %. |

Cross-references: what BR %, BRC and AP mean numerically → `references/ballistics-damage.md`;
kits, workbenches, spare parts → `references/crafting-repairs.md`; belt artefacts and
detectors → `references/artifacts.md`; disguise and relations → `references/factions.md`.

---

## Appendix A — the complete armour table (all 161 outfits)

Reproduced from `G.A.M.M.A. Outfits Balances/tools/armor_values.tsv` (the pack's own
conversion of the community Google Sheet, sheet id
`1FmRZTwhCTGSNaFHi7I9vgO9fXBiU4PeApEzvIwsBsUM`). Sorted by **cost ascending** — the gear
ladder from a jacket to a Nosorog. Columns: item id, in-game name, faction, type, cost in
RU, ballistic `wound_protection`, `hit_fraction_actor` (the BR class — **lower is better**;
see `references/ballistics-damage.md`), belt slots (`artefact_count`), `Speed`, carry bonus
in kg, item weight in kg, and the repair class.

| # | Item id | Name | Faction | Type | Cost | Wound prot. | BR | Belt | Speed | Carry | Wt | Repair |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `bandit_novice_outfit_alt` | Armored Leather Jacket | Bandit | Jacket | 6458 | 0.072 | 0.87 | 1 | 1.08 | 9.1 | 5 | `outfit_novice` |
| 2 | `cs_novice_outfit` | Clear Sky Leather Jacket | Clear Sky | Jacket | 6534 | 0.086 | 0.92 | 1 | 1.08 | 12 | 5 | `outfit_novice` |
| 3 | `svoboda_novice_outfit` | Freedom Leather Jacket | Freedom | Jacket | 6581 | 0.086 | 0.91 | 1 | 1.07 | 12 | 5 | `outfit_novice` |
| 4 | `bandit_novice_outfit` | Black Leather Jacket | Bandit | Jacket | 7065 | 0.101 | 0.94 | 1 | 1.11 | 15.6 | 4 | `outfit_novice` |
| 5 | `novice_outfit` | Leather Jacket | Unknown | Jacket | 7290 | 0.101 | 0.92 | 1 | 1.08 | 12 | 5 | `outfit_novice` |
| 6 | `dolg_novice_outfit` | Duty Leather Jacket | Duty | Jacket | 7494 | 0.187 | 0.92 | 1 | 1.09 | 12 | 4 | `outfit_novice` |
| 7 | `army_outfit` | Military Service Outfit | Military | Metal | 8167 | 0.072 | 0.79 | 1 | 0.97 | 10.8 | 12 | `outfit_novice` |
| 8 | `novice_outfit_camo` | Firearm Enthusiast's Jacket | Unknown | Jacket | 11766 | 0.101 | 0.9 | 2 | 1.06 | 10 | 8 | `outfit_novice` |
| 9 | `redline_novice_outfit` | Redline Leather Jacket | Unknown | Jacket | 12656 | 0.101 | 0.92 | 2 | 1.12 | 10 | 5 | `outfit_novice` |
| 10 | `novice_outfit_tourist` | Tourist’s Jacket | Free Stalkers | Jacket | 14116 | 0.115 | 0.93 | 2 | 1.08 | 14.4 | 4 | `outfit_novice` |
| 11 | `trenchcoat_outfit` | Overcoat | Unknown | Overcoat | 20895 | 0.201 | 0.86 | 2 | 1.05 | 18 | 8 | `outfit_novice` |
| 12 | `trenchcoat_freedom_brown_outfit` | Heavy Freedom Overcoat | Freedom | Overcoat | 31044 | 0.158 | 0.85 | 1 | 1.04 | 18 | 8 | `outfit_novice` |
| 13 | `cs_light_novice_outfit` | CS-1 Body Armor | Clear Sky | CS1 | 31058 | 0.144 | 0.83 | 2 | 1.01 | 13 | 9 | `outfit_novice` |
| 14 | `cs_medium_outfit` | CS-3a Body Armor | Clear Sky | CS-3 | 32623 | 0.201 | 0.69 | 2 | 1.01 | 24 | 17 | `outfit_medium` |
| 15 | `renegademerc_outfit` | Renegade LC Suit | Renegade | MC Suit | 33088 | 0.244 | 0.58 | 1 | 0.94 | 31 | 28 | `outfit_medium` |
| 16 | `banditmerc_outfit` | Fenced LC Suit | Bandit | LC Suit | 35087 | 0.144 | 0.8 | 2 | 1.01 | 18.2 | 7 | `outfit_light` |
| 17 | `cs_light_outfit` | CS-2a Body Armor | Clear Sky | CS2 | 40148 | 0.129 | 0.81 | 2 | 1.01 | 12 | 9 | `outfit_light` |
| 18 | `isg_lcs_outfit` | UNISG LC Suit | UNISG | MC Suit | 43393 | 0.201 | 0.54 | 2 | 0.91 | 27.9 | 34 | `outfit_medium` |
| 19 | `trenchcoat_green_outfit` | Heavy Green Overcoat | Unknown | L. Trenchcoat | 43628 | 0.259 | 0.8 | 3 | 1.05 | 22 | 12 | `outfit_light` |
| 20 | `merc_fighter_outfit` | Mercenary LC-F Suit | Mercenary | LC Suit | 43872 | 0.129 | 0.7 | 2 | 0.96 | 10.5 | 16 | `outfit_light` |
| 21 | `specops_outfit` | Berill-5M Armored Suit | Military | Beril-5M | 44431 | 0.546 | 0.67 | 1 | 1.02 | 34.2 | 18 | `outfit_medium` |
| 22 | `merc_outfit` | Mercenary LC Suit | Mercenary | MC Suit | 45649 | 0.201 | 0.58 | 2 | 0.94 | 23.2 | 28 | `outfit_medium` |
| 23 | `dolg_red_outfit` | PS5-M Hunter Suit | Duty | Predator | 45855 | 0.259 | 0.77 | 3 | 1.07 | 16 | 8 | `outfit_light` |
| 24 | `specops_dolg_outfit` | PS5-B Battle Armor | Duty | Beril-5M | 46043 | 0.546 | 0.7 | 2 | 1.05 | 38 | 14 | `outfit_medium` |
| 25 | `isg_lcs_urban_outfit` | UNISG LC-UC Suit | UNISG | CS-3 | 46099 | 0.201 | 0.63 | 2 | 0.98 | 21.6 | 2 | `outfit_medium` |
| 26 | `merc_scout_outfit` | Mercenary LC-S Suit | Mercenary | LC Suit | 47600 | 0.129 | 0.74 | 2 | 1 | 18 | 12 | `outfit_light` |
| 27 | `merc_sunset_outfit` | Mercenary LCz Suit | Mercenary | CS-3 | 47723 | 0.201 | 0.66 | 2 | 1.01 | 18 | 17 | `outfit_medium` |
| 28 | `nbc_merc_outfit` | Load-bearing 'Twilight' Tactical Suit | Mercenary | NBC | 47987 | 0.115 | 0.75 | 3 | 1.09 | 25.5 | 7 | `outfit_light` |
| 29 | `isg_camo_outfit` | UNISG Mk2 Tactical Body Armor | UNISG | PS6 | 49847 | 0.388 | 0.57 | 2 | 0.95 | 21.6 | 3 | `outfit_medium` |
| 30 | `military_outfit` | Skat-9 Armored Suit | Military | Skat | 50549 | 0.374 | 0.43 | 1 | 0.99 | 37.8 | 34 | `outfit_heavy` |
| 31 | `svoboda_heavy_outfit_2` | Sentinel of Freedom | Freedom | PS5 | 51168 | 0.273 | 0.64 | 3 | 1.04 | 20 | 14 | `outfit_medium` |
| 32 | `nbc_dolg_outfit` | PS5-Mt Suit | Duty | NBC | 51662 | 0.158 | 0.77 | 3 | 1.1 | 34 | 6 | `outfit_light` |
| 33 | `trenchcoat_brown_outfit` | Heavy Brown Overcoat | Unknown | Trenchcoat | 52133 | 0.345 | 0.73 | 3 | 1.05 | 22 | 12 | `outfit_medium` |
| 34 | `isg_lcs_camo_outfit` | UNISG LC-C Suit | UNISG | LC Suit | 53390 | 0.129 | 0.7 | 3 | 0.95 | 12.6 | 12 | `outfit_light` |
| 35 | `svoboda_light_outfit` | Wind of Freedom | Freedom | PS6 | 53399 | 0.345 | 0.6 | 2 | 0.97 | 24 | 25 | `outfit_medium` |
| 36 | `military_exolight_outfit` | Military Stalker Exosuit | Military | Exolight | 53636 | 0.575 | 0.39 | 1 | 0.92 | 45 | 42 | `outfit_heavy` |
| 37 | `merc_sun_outfit` | Twilight Tactical Suit | Mercenary | PS6 | 53949 | 0.388 | 0.6 | 2 | 0.98 | 18 | 25 | `outfit_medium` |
| 38 | `dolg_outfit` | PS5-M Universal Protection Suit | Duty | PS5 | 55364 | 0.417 | 0.67 | 3 | 1.06 | 20 | 13 | `outfit_medium` |
| 39 | `stalker_autumn_outfit` | Autumn Stalker Suit | Free Stalkers | CS2 | 55420 | 0.158 | 0.81 | 3 | 0.99 | 14.4 | 8 | `outfit_light` |
| 40 | `trenchcoat_dolg_brown_outfit` | Heavy Duty Overcoat | Duty | Trenchcoat | 55586 | 0.374 | 0.72 | 3 | 1.06 | 22 | 11 | `outfit_medium` |
| 41 | `cs_stalker_outfit` | CS-2b Body Armor | Clear Sky | Sunrise | 55694 | 0.287 | 0.71 | 2 | 1.07 | 16 | 11 | `outfit_medium` |
| 42 | `dolg_voin_outfit` | PS6-V Warrior Suit | Duty | PS6 | 57395 | 0.517 | 0.64 | 2 | 0.99 | 24 | 22 | `outfit_medium` |
| 43 | `merc_jackal_outfit` | Mercenary LTS-J Body Suit | Mercenary | MC Suit | 58615 | 0.158 | 0.65 | 3 | 0.95 | 25.5 | 22 | `outfit_medium` |
| 44 | `greh_ps5_outfit` | Volos Flak Armor | Sin | PS5 | 59328 | 0.244 | 0.69 | 4 | 1.03 | 16 | 14 | `outfit_medium` |
| 45 | `stalker_outfit` | Sunrise Stalker Suit | Free Stalkers | CS2 | 59933 | 0.158 | 0.83 | 3 | 1.01 | 24 | 8 | `outfit_light` |
| 46 | `stalker_salamander_outfit` | Salamander Stalker Suit | Free Stalkers | STS | 62115 | 0.259 | 0.78 | 3 | 1.01 | 15.6 | 8 | `outfit_light` |
| 47 | `merc_coyote_outfit` | Mercenary MTS-C Body Suit | Mercenary | MC Suit | 62915 | 0.23 | 0.56 | 3 | 0.93 | 21.8 | 31 | `outfit_medium` |
| 48 | `svoboda_heavy_outfit` | Guardian of Freedom | Freedom | Beril-5M | 64427 | 0.374 | 0.67 | 3 | 1.03 | 38 | 15 | `outfit_medium` |
| 49 | `greh_armored_outfit` | Irij Flak Armor | Sin | MC Suit | 65642 | 0.158 | 0.64 | 4 | 0.92 | 24.8 | 28 | `outfit_medium` |
| 50 | `ghillie_outfit` | Ghillie Suit | Unknown | Ghillie | 67100 | 0.287 | 0.83 | 4 | 1.1 | 14 | 5 | `outfit_light` |
| 51 | `cs_nbc_outfit` | CS-2t Suit | Clear Sky | NBC | 67798 | 0.115 | 0.77 | 3 | 1.09 | 34 | 7 | `outfit_light` |
| 52 | `ecolog_guard_outfit` | ISRIT Guard Jumpsuit | Ecologist | PS6 | 70952 | 0.474 | 0.71 | 3 | 0.98 | 24 | 2 | `outfit_medium` |
| 53 | `military_sky_outfit` | CS-4b Armored Suit | Clear Sky | Skat | 72114 | 0.287 | 0.48 | 2 | 1.01 | 42 | 28 | `outfit_heavy` |
| 54 | `monolith_outfit` | Monolith X-18 Suit | Monolith | PS6 | 72323 | 0.431 | 0.64 | 2 | 0.97 | 21.6 | 25 | `outfit_medium` |
| 55 | `specops_bandit_outfit` | Deserter's B-5M Armored Suit | Bandit | Beril-5M | 72498 | 0.46 | 0.76 | 2 | 1.07 | 49.4 | 1 | `outfit_medium` |
| 56 | `bandit_ps5_outfit` | Fenced PS5-M Universal Protection Suit | Bandit | PS5 | 73138 | 0.345 | 0.74 | 2 | 1.08 | 26 | 1 | `outfit_medium` |
| 57 | `merc_nighthunter_outfit` | Mercenary STS-N Body Armor | Mercenary | STS-H | 73194 | 0.33 | 0.47 | 2 | 1.03 | 20.2 | 23 | `outfit_heavy` |
| 58 | `military_merc_outfit` | Mercenary Skat-9 Armored Suit | Mercenary | Skat | 74159 | 0.287 | 0.43 | 2 | 1.01 | 31.5 | 28 | `outfit_heavy` |
| 59 | `isg_exolight_outfit` | UNISG Exosuit | UNISG | Exolight | 74250 | 0.431 | 0.34 | 2 | 0.9 | 45 | 42 | `outfit_heavy` |
| 60 | `military_monolit_outfit` | Monolith Skat-9 Armored Suit | Monolith | Skat | 74310 | 0.316 | 0.48 | 2 | 1 | 37.8 | 28 | `outfit_heavy` |
| 61 | `military_freedom_outfit` | Liberated Skat-9 Armored Suit | Freedom | Skat | 74850 | 0.259 | 0.43 | 2 | 1 | 42 | 28 | `outfit_heavy` |
| 62 | `cs_heavy_outfit` | CS-3b Body Armor | Clear Sky | CS-3B | 74933 | 0.359 | 0.64 | 2 | 1.03 | 28 | 24 | `outfit_heavy` |
| 63 | `dolg_scout_outfit` | PS5-R Scout Vest | Duty | PS5 | 75384 | 0.374 | 0.7 | 2 | 1.08 | 24 | 9 | `outfit_medium` |
| 64 | `stalker_bear_outfit` | Bear Stalker Suit | Free Stalkers | Sunrise | 75411 | 0.359 | 0.71 | 3 | 1.05 | 19.2 | 14 | `outfit_medium` |
| 65 | `dolg_heavy_outfit` | PSZ-9d Body Armor | Duty | Skat | 77173 | 0.374 | 0.48 | 2 | 1.02 | 42 | 25 | `outfit_heavy` |
| 66 | `merc_exolight_outfit` | Mercenary Exosuit | Mercenary | Exolight | 77213 | 0.431 | 0.39 | 2 | 0.93 | 37.5 | 35 | `outfit_heavy` |
| 67 | `stalker_tigerstripe_outfit` | Tigerstripe Stalker Suit | Free Stalkers | Sunrise | 77237 | 0.417 | 0.77 | 3 | 1.09 | 19.2 | 8 | `outfit_medium` |
| 68 | `merc_wolven_outfit` | Mercenary STS-W Body Armor | Mercenary | STS | 77833 | 0.201 | 0.74 | 3 | 1.01 | 9.8 | 9 | `outfit_light` |
| 69 | `stalker_predator_outfit` | Predator Stalker Suit | Free Stalkers | Predator | 77990 | 0.244 | 0.79 | 4 | 1.06 | 19.2 | 8 | `outfit_light` |
| 70 | `dolg_pantsir_outfit` | PSZ-7p Shell Armor | Duty | Skat | 78078 | 0.417 | 0.52 | 2 | 1.04 | 42 | 22 | `outfit_heavy` |
| 71 | `monolith_exolight_outfit` | Monolith Exosuit | Monolith | Exolight | 78246 | 0.474 | 0.45 | 2 | 0.92 | 45 | 35 | `outfit_heavy` |
| 72 | `renegade_scientific_outfit` | Renegade SEVA Suit | Renegade | SEVA | 78600 | 0.287 | 0.67 | 2 | 1 | 22 | 17 | `outfit_medium` |
| 73 | `exo_wood_outfit` | Woodland Exosuit | Unknown | Exolight | 78678 | 0.474 | 0.45 | 2 | 0.93 | 50 | 35 | `outfit_heavy` |
| 74 | `svoboda_exolight_outfit` | Warrior of Freedom | Freedom | Exolight | 78798 | 0.374 | 0.39 | 2 | 0.92 | 50 | 35 | `outfit_heavy` |
| 75 | `light_voen_outfit` | Military Stalker IBAz Suit | Military | IBAZ | 78908 | 0.862 | 0.63 | 1 | 1.05 | 18 | 24 | `outfit_heavy` |
| 76 | `bandit_sun_outfit` | Sunset Tactical Suit | Bandit | Sunrise | 79046 | 0.316 | 0.77 | 2 | 1.1 | 20.8 | 8 | `outfit_medium` |
| 77 | `stalker_drought_outfit` | Drought Stalker Suit | Free Stalkers | Sunrise | 80015 | 0.345 | 0.74 | 3 | 1.07 | 19.2 | 1 | `outfit_medium` |
| 78 | `stalker_graphite_outfit` | Graphite Stalker Suit | Free Stalkers | Sunrise | 80015 | 0.345 | 0.74 | 3 | 1.07 | 19.2 | 1 | `outfit_medium` |
| 79 | `exo_dolg_outfit` | PSZ-10d Duty Battlesuit | Duty | Exolight | 80520 | 0.675 | 0.49 | 2 | 0.97 | 28 | 25 | `outfit_heavy` |
| 80 | `military_bandit_outfit` | Looted Skat-9 Armored Suit | Bandit | Skat | 81432 | 0.316 | 0.58 | 2 | 1.04 | 54.6 | 2 | `outfit_heavy` |
| 81 | `monolith_nbc_outfit` | Tactical Monolith Suit | Monolith | NBC | 81756 | 0.129 | 0.77 | 3 | 1.08 | 30.6 | 7 | `outfit_light` |
| 82 | `isg_outfit` | UNISG Mk1 Tactical Body Armor | UNISG | PS5 | 83283 | 0.316 | 0.6 | 3 | 1.02 | 18 | 17 | `outfit_medium` |
| 83 | `greh_armored_camo_outfit` | Vyriy Flak Armor | Sin | CS-3 | 83932 | 0.158 | 0.71 | 4 | 0.99 | 19.2 | 17 | `outfit_medium` |
| 84 | `dolg_exolight_outfit` | PSZ-10d Duty Battlesuit | Duty | Exolight | 84671 | 0.575 | 0.45 | 2 | 0.94 | 50 | 32 | `outfit_heavy` |
| 85 | `nbc_freedom_outfit` | Keeper of Freedom | Freedom | NBC | 84780 | 0.101 | 0.75 | 3 | 1.08 | 34 | 7 | `outfit_light` |
| 86 | `specops_merc_outfit` | Mercenary B-5M Armored Suit | Mercenary | Beril-5M | 85384 | 0.417 | 0.67 | 2 | 1.04 | 28.5 | 15 | `outfit_medium` |
| 87 | `bandit_exolight_outfit` | Looted Exosuit | Bandit | Exolight | 87336 | 0.474 | 0.56 | 2 | 0.96 | 65 | 24 | `outfit_heavy` |
| 88 | `isg_scientific_outfit` | UNISG SEVA Suit | UNISG | SEVA | 87591 | 0.23 | 0.64 | 3 | 0.97 | 19.8 | 2 | `outfit_medium` |
| 89 | `exo_merc_urban_outfit` | Mercenary Urban Exosuit | Mercenary | Exolight | 87872 | 0.474 | 0.34 | 2 | 0.92 | 56.2 | 45 | `outfit_heavy` |
| 90 | `exo_merc_grass_outfit` | Mercenary Grassland Exosuit | Mercenary | Exolight | 88368 | 0.431 | 0.44 | 3 | 0.96 | 18.8 | 28 | `outfit_heavy` |
| 91 | `nbc_outfit` | Tactical Stalker Suit | Free Stalkers | NBC | 89789 | 0.144 | 0.79 | 4 | 1.09 | 40.8 | 6 | `outfit_light` |
| 92 | `bandit_nbc_outfit` | Load-bearing 'Sunset' Tactical Suit | Bandit | NBC | 90972 | 0.129 | 0.82 | 3 | 1.12 | 44.2 | 5 | `outfit_light` |
| 93 | `monolith_scientific_outfit` | Monolith Scientific Suit | Monolith | SEVA | 91922 | 0.259 | 0.7 | 3 | 0.99 | 19.8 | 17 | `outfit_medium` |
| 94 | `merc_scientific_outfit` | Mercenary SEVA Suit | Mercenary | SEVA | 92625 | 0.23 | 0.67 | 3 | 1 | 16.5 | 17 | `outfit_medium` |
| 95 | `light_isg_outfit` | UNISG IBAz Suit | UNISG | IBAZ | 93184 | 0.647 | 0.59 | 2 | 1.04 | 18 | 24 | `outfit_heavy` |
| 96 | `svoboda_scientific_outfit` | Watchman of Freedom | Freedom | SEVA | 93555 | 0.201 | 0.67 | 3 | 0.99 | 22 | 17 | `outfit_medium` |
| 97 | `cs_scientific_outfit` | CS-4a SEVA Suit | Clear Sky | SEVA | 95750 | 0.23 | 0.7 | 3 | 1 | 22 | 17 | `outfit_medium` |
| 98 | `travel_outfit` | Voyager Stalker Suit | Free Stalkers | Voyager | 96307 | 0.216 | 0.85 | 6 | 0.96 | 43.2 | 5 | `outfit_light` |
| 99 | `monolith_scientific_light_outfit` | Monolith Patchwork Science Suit | Monolith | SEVA | 96460 | 0.201 | 0.73 | 3 | 1.03 | 25.2 | 14 | `outfit_medium` |
| 100 | `light_freedom_outfit` | Defender of Freedom | Freedom | IBAZ | 97944 | 0.575 | 0.63 | 2 | 1.06 | 20 | 2 | `outfit_heavy` |
| 101 | `exo_dolg_urban_outfit` | PSZ-10g Urban Battlesuit | Duty | Exolight | 98417 | 0.632 | 0.4 | 2 | 0.93 | 75 | 4 | `outfit_heavy` |
| 102 | `bandit_scientific_dark_outfit` | Patchwork Anomaly Suit | Bandit | SEVA | 99421 | 0.259 | 0.76 | 3 | 1.03 | 28.6 | 12 | `outfit_medium` |
| 103 | `dolg_scientific_red_outfit` | PS5-9Md Light Scientific Suit | Duty | SEVA | 99450 | 0.273 | 0.72 | 3 | 1.04 | 18 | 14 | `outfit_medium` |
| 104 | `dolg_scientific_outfit` | PS5-9Md Universal Scientific Suit | Duty | SEVA | 99763 | 0.316 | 0.7 | 3 | 1.01 | 22 | 15 | `outfit_medium` |
| 105 | `nomad_outfit` | Nomad Stalker Suit | Free Stalkers | Nomad | 100114 | 0.402 | 0.69 | 4 | 0.99 | 31.2 | 21 | `outfit_medium` |
| 106 | `light_monolit_outfit` | Monolith IBAz Assault Suit | Monolith | IBAZ | 101336 | 0.718 | 0.66 | 2 | 1.06 | 18 | 2 | `outfit_heavy` |
| 107 | `light_merc_outfit` | Mercenary IBAz Suit | Mercenary | IBAZ | 101650 | 0.647 | 0.63 | 2 | 1.07 | 15 | 2 | `outfit_heavy` |
| 108 | `wastelander_outfit` | Wastelander Stalker Suit | Free Stalkers | Wastelander | 101663 | 0.244 | 0.72 | 5 | 0.99 | 28.8 | 12 | `outfit_medium` |
| 109 | `renegade_exo_outfit` | Renegade Exoskeleton | Renegade | Exo | 102279 | 0.517 | 0.35 | 1 | 1.03 | 96 | 7 | `outfit_exo` |
| 110 | `dolg_heavy_redline_outfit` | PSZ-9kl Command Armor | Duty | Skat | 102898 | 0.374 | 0.48 | 3 | 1.02 | 42 | 25 | `outfit_heavy` |
| 111 | `cs_exolight_outfit` | CS-5 Exosuit | Clear Sky | Exolight | 103230 | 0.431 | 0.45 | 3 | 0.93 | 50 | 35 | `outfit_heavy` |
| 112 | `exo_merc_wood_outfit` | Mercenary Woodland Exosuit | Mercenary | Exolight | 104810 | 0.503 | 0.42 | 3 | 0.94 | 37.5 | 32 | `outfit_heavy` |
| 113 | `merc_scientific_armored_outfit` | Mercenary SEVA Body Armor | Mercenary | Hybrid SEVA | 105419 | 0.216 | 0.63 | 3 | 1.01 | 19.5 | 19 | `outfit_medium` |
| 114 | `freedom_exo_vineleaf_outfit` | Hero of Freedom | Freedom | Exolight | 107536 | 0.431 | 0.36 | 3 | 0.94 | 42 | 38 | `outfit_heavy` |
| 115 | `light_dolg_outfit` | IBAz Universal Protection Suit | Duty | IBAZ | 109080 | 0.862 | 0.66 | 2 | 1.08 | 20 | 18 | `outfit_heavy` |
| 116 | `exolight_outfit` | Exosuit | Free Stalkers | Exolight | 109647 | 0.517 | 0.5 | 3 | 0.93 | 60 | 32 | `outfit_heavy` |
| 117 | `bandit_scientific_outfit` | Looted SEVA Suit | Bandit | Hybrid SEVA | 112190 | 0.244 | 0.73 | 3 | 1.04 | 33.8 | 13 | `outfit_medium` |
| 118 | `monolith_trenchcoat_outfit` | Monolith Overcoat | Monolith | Sin Heavycoat | 114062 | 0.402 | 0.68 | 3 | 1.04 | 27.9 | 21 | `outfit_heavy` |
| 119 | `exo_dolg_wood_outfit` | PSZ-10l Forest Battlesuit | Duty | Exolight | 115444 | 0.675 | 0.47 | 3 | 0.95 | 50 | 29 | `outfit_heavy` |
| 120 | `exo_dolg_red_outfit` | PSZ-10d Venator Battlesuit | Duty | Exolight | 115995 | 0.489 | 0.5 | 3 | 0.95 | 55 | 32 | `outfit_heavy` |
| 121 | `scientific_outfit` | SEVA Bodysuit | Free Stalkers | SEVA | 116790 | 0.287 | 0.73 | 4 | 1 | 26.4 | 15 | `outfit_medium` |
| 122 | `merc_exo_outfit` | Mercenary Exoskeleton | Mercenary | Exo | 119274 | 0.431 | 0.35 | 2 | 1.03 | 72 | 7 | `outfit_exo` |
| 123 | `dolg_scientific_wood_outfit` | PS5-9Md Light Pathfinder | Duty | SEVA | 119572 | 0.273 | 0.68 | 4 | 0.99 | 24 | 2 | `outfit_medium` |
| 124 | `greh_trenchcoat_outfit` | Sin Heavy Overcoat | Sin | Sin Heavycoat | 121805 | 0.287 | 0.7 | 6 | 1.04 | 24.8 | 21 | `outfit_heavy` |
| 125 | `military_exo_outfit` | Military Stalker Exoskeleton | Military | Exo | 123260 | 0.575 | 0.35 | 2 | 1.01 | 86.4 | 84 | `outfit_exo` |
| 126 | `dolg_specops_red_outfit` | PS5-B2 Veteran Battlesuit | Duty | Beril-5H "Goshen" | 123638 | 0.69 | 0.58 | 2 | 1.06 | 42 | 22 | `outfit_heavy` |
| 127 | `cs_scientific_outfit_good` | CS-4a Pathfinder | Clear Sky | Heavy SEVA | 129360 | 0.33 | 0.54 | 3 | 0.98 | 28 | 28 | `outfit_heavy` |
| 128 | `merc_combat_scientific_outfit` | Mercenary Pathfinder | Mercenary | Heavy SEVA | 130095 | 0.33 | 0.49 | 3 | 0.98 | 21 | 28 | `outfit_heavy` |
| 129 | `hybrid_outfit` | Hybrid Armored Suit | Unknown | Heavy SEVA | 130795 | 0.359 | 0.54 | 3 | 1.01 | 28 | 28 | `outfit_heavy` |
| 130 | `army_nosorog_outfit` | Military Stalker Nosorog | Military | Nosorog | 130866 | 0.603 | 0.31 | 2 | 1.02 | 103.5 | 102 | `outfit_exo` |
| 131 | `military_proto_exo_outfit` | Skat-9 Exoskeleton | Military | Skat Exo | 132330 | 0.431 | 0.39 | 2 | 1.06 | 86.4 | 6 | `outfit_exo` |
| 132 | `light_loner_outfit` | Interceptor Body Armor | Free Stalkers | IBAZ | 134285 | 0.79 | 0.69 | 3 | 1.07 | 24 | 18 | `outfit_heavy` |
| 133 | `ecolog_outfit_blue` | SSP-99M "Sapphire" | Ecologist | SSP | 137017 | 0.086 | 0.91 | 4 | 1.01 | 15 | 6 | `outfit_medium` |
| 134 | `ecolog_outfit_red` | SSP-99Ě "Ruby" | Ecologist | SSP | 137017 | 0.086 | 0.91 | 4 | 1.01 | 15 | 6 | `outfit_medium` |
| 135 | `ecolog_outfit_white` | SSP-99 "Diamond" | Ecologist | SSP | 137017 | 0.086 | 0.91 | 4 | 1.01 | 15 | 6 | `outfit_medium` |
| 136 | `ecolog_outfit_yello` | SSP-99 Topaz | Ecologist | SSP | 137017 | 0.086 | 0.91 | 4 | 1.01 | 15 | 6 | `outfit_medium` |
| 137 | `ecolog_outfit_green` | SSP-99M Bodysuit | Ecologist | SSP | 139744 | 0.086 | 0.91 | 4 | 1.01 | 15 | 6 | `outfit_medium` |
| 138 | `isg_exo_outfit` | UNISG Exoskeleton | UNISG | Exo | 144300 | 0.431 | 0.29 | 3 | 1 | 86.4 | 84 | `outfit_exo` |
| 139 | `merc_ace_outfit` | Mercenary ACE Scientific Suit | Mercenary | ACE | 148992 | 0.33 | 0.54 | 4 | 0.97 | 21 | 26 | `outfit_heavy` |
| 140 | `dolg_proto_exo_outfit` | PS5-M Exoskeleton | Duty | Protoexo | 151238 | 0.417 | 0.7 | 4 | 1.09 | 96 | 36 | `outfit_heavy` |
| 141 | `ecolog_outfit_orange` | SSP-99 Bodysuit | Ecologist | SSP | 151369 | 0.086 | 0.91 | 5 | 1.01 | 15 | 6 | `outfit_medium` |
| 142 | `isg_nosorog_outfit` | UNISG Nosorog | UNISG | Nosorog | 154909 | 0.46 | 0.24 | 3 | 1.01 | 103.5 | 102 | `outfit_exo` |
| 143 | `bandit_exo_outfit` | Stolen Exoskeleton | Bandit | Exo | 155905 | 0.474 | 0.53 | 2 | 1.06 | 124.8 | 49 | `outfit_exo` |
| 144 | `monolith_exo_outfit` | Monolith Exoskeleton | Monolith | Exo | 156366 | 0.474 | 0.41 | 3 | 1.02 | 86.4 | 7 | `outfit_exo` |
| 145 | `cs_exo_outfit` | CS-5 Exoskeleton | Clear Sky | Exo | 158105 | 0.431 | 0.41 | 3 | 1.03 | 96 | 7 | `outfit_exo` |
| 146 | `merc_nosorog_outfit` | Mercenary Nosorog | Mercenary | Nosorog | 160095 | 0.46 | 0.31 | 3 | 1.04 | 86.2 | 85 | `outfit_exo` |
| 147 | `svoboda_exo_outfit` | Paragon of Freedom | Freedom | Exo | 160395 | 0.374 | 0.35 | 3 | 1.02 | 96 | 7 | `outfit_exo` |
| 148 | `monolith_nosorog_outfit` | Monolith Nosorog | Monolith | Nosorog | 170079 | 0.503 | 0.37 | 3 | 1.03 | 103.5 | 85 | `outfit_exo` |
| 149 | `cs_stalker_proto_exo_outfit` | CS-2b Exoskeleton | Clear Sky | Protoexo | 172368 | 0.316 | 0.7 | 4 | 1.08 | 96 | 4 | `outfit_heavy` |
| 150 | `dolg_exo_outfit` | PSZ-10d Exoskeleton | Duty | Exo | 174200 | 0.575 | 0.41 | 3 | 1.04 | 96 | 63 | `outfit_exo` |
| 151 | `freedom_nosorog_outfit` | Champion of Freedom | Freedom | Nosorog | 174585 | 0.402 | 0.31 | 3 | 1.03 | 115 | 85 | `outfit_exo` |
| 152 | `exo_outfit` | Exoskeleton | Free Stalkers | Exo | 176027 | 0.517 | 0.47 | 3 | 1.03 | 115.2 | 63 | `outfit_exo` |
| 153 | `dolg_heavy_proto_exo_outfit` | PSZ-9d Exoskeleton | Duty | Skat Exo | 176580 | 0.431 | 0.45 | 3 | 1.09 | 96 | 45 | `outfit_exo` |
| 154 | `isg_proto_exo_outfit` | UNISG Tactical Exoskeleton | UNISG | Protoexo | 176841 | 0.316 | 0.64 | 4 | 1.05 | 86.4 | 48 | `outfit_heavy` |
| 155 | `greh_exo_outfit` | Vyraj Power Armor | Sin | Exo | 183961 | 0.33 | 0.44 | 5 | 1.01 | 76.8 | 7 | `outfit_exo` |
| 156 | `dolg_nosorog_outfit` | PSZ-10d Nosorog | Duty | Nosorog | 189919 | 0.603 | 0.37 | 3 | 1.05 | 115 | 76 | `outfit_exo` |
| 157 | `monolith_proto_exo_outfit` | X-18 Exoskeleton | Monolith | Protoexo | 190695 | 0.345 | 0.7 | 4 | 1.07 | 86.4 | 4 | `outfit_heavy` |
| 158 | `ecolog_exo_outfit` | Scientific Exoskeleton | Ecologist | Exo | 192198 | 0.517 | 0.53 | 4 | 1.03 | 96 | 56 | `outfit_exo` |
| 159 | `svoboda_light_proto_exo_outfit` | Wind of Freedom Exoskeleton | Freedom | Protoexo | 200732 | 0.273 | 0.67 | 4 | 1.07 | 96 | 4 | `outfit_heavy` |
| 160 | `ecolog_proto_exo_outfit` | SSP-99M Exoskeleton | Ecologist | Protoexo | 206010 | 0.374 | 0.76 | 5 | 1.08 | 96 | 32 | `outfit_heavy` |
| 161 | `stalker_proto_exo_outfit` | Sunrise Exoskeleton | Free Stalkers | Protoexo | 224759 | 0.374 | 0.73 | 5 | 1.08 | 115.2 | 36 | `outfit_heavy` |

Reading the table: **`hit_fraction_actor` and `wound_protection` are different axes.** A
Nosorog's 0.17–0.31 BR is what stops bullets outright; `wound_protection` is the fraction
of damage that still gets through *after* the armour's own ballistic layer, which is why
the table's best `wound_protection` (IBAz ≈ 0.86) and its best BR class (Nosorog ≈ 0.17)
belong to different suits. Belt slots are the number of artefacts the suit can carry;
`artefact_count 0` suits cannot hold any.
