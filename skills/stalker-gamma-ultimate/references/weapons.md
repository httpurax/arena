# Weapons, parts and upgrades — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual articles **Ballistics System**
(`article_gamma_ballistics_text`), **Repairs for Guns** (`article_gamma_repgun_text`) and
**How To Progress**; the **NPE ammo tutorial** (`npe_gamma_tutorial_ammo.xml`, verbatim quotes
below); the pack's ammo spreadsheet `gamma_ammo_weapon_table.xlsx` (columns include
`ammo_k_ap`, `ammo_k_hit`, price per round, damage-per-Rouble, `Overpen damage factor`) and the
weapon doctrine working doc `good_weapons.txt` (shipped inside `G.A.M.M.A. Weapon Pack`);
`140- Weapon Parts Overhaul - arti` and its per-calibre cleaning/repair kit classes; the
Economy addon's `items/settings/part_prices.ltx`,
`mod_system_weapons_gamma_attachments_price.ltx`, `mod_system_weapons_kit_repair.ltx`;
`G.A.M.M.A. Mags Redux`/`Anomaly Magazines Redux`; the attachment and upgrade-kit keys in
`user.ltx`; and the shipped gameplay scripts `grok_weapon_jam`, `grok_weapon_fire_modes`,
`grok_weapon_drop_on_empty`, `mags_reload_unjam` (all listed in the repo's `modpack_data`).
Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. Guns are earned, not bought

> "Guns must be repaired to progress since **you can't buy them from traders** with GAMMA
> Economy. You can loot guns from stashes or dead stalkers though, and that's how you will make
> it to the North in one piece." — manual

So every weapon in GAMMA comes from one of three places:

| Source | Notes |
|---|---|
| **Looted from stalkers** | condition is bad by design; `outfit_drops`/weapon-drop chances scale with rank |
| **Marked stashes** | stash loot is map-tiered; better weapons further north |
| **Crafted / upgraded** | Gunsmith toolkit for ammo, mechanics for upgrade kits |
| **Black Market (optional)** | player-side MCM toggle that re-enables gear purchases |

The manual also fixes the *maintenance* frame: "**Gun condition represents how clean a gun
is**… **Jams are coming from the actual gun parts**. Repairing the gun condition will not
repair the gun's parts. Each part must be repaired individually… **The barrel changes the
damage the gun deals and the strength of ammo penetration.** A gun with a very bad barrel
condition will deal almost no damage, don't do that."

## 2. Parts, condition and jamming

GAMMA runs **Weapon Parts Overhaul**: every weapon has a **condition** (cleanliness, 0–100 %)
plus four **parts**, each with its own condition. The player-visible part types are
**barrel**, **bolt**, **bolt carrier**, and **trigger components/receiver** (the `prt_w_*`
families in the crafting tables: `prt_w_barrel_1…13`, `prt_w_bolt_1…9`,
`prt_w_bolt_carrier_1…11`, `prt_w_trigger_components_1…6`).

| What you observe | Mechanism |
|---|---|
| Gun jams constantly | **parts** are worn (bolt/bolt carrier/trigger components); each part contributes to jam chance |
| Gun does almost no damage | the **barrel** is worn — damage and penetration come from it |
| Gun loses parts condition while you shoot | **condition** (cleanliness) is what accelerates degradation; cleaning prevents it |
| Cleaning does nothing | cleaning only helps parts **above 60 %**; below that you must repair or replace |

**The 60 % rule (weapons).** From the manual, verbatim: "Collect parts **above 60 %
condition** and repair them with the appropriate tool to 100 % condition (**Ramrod,
Multitool, or File**). Then simply drag and drop the repaired parts on the gun." Below 60 %
the part cannot be repaired by hand tools — it needs a **repair kit** or must be swapped out
by *maintain parts*.

### The four repair-kit classes

`mod_system_weapons_kit_repair.ltx` splits weapons into four repair types, matching the Type
A–D cleaning/repair kit line (see `references/crafting-repairs.md` for their prices and
recipes):

| Repair type | Covered weapons (from the shipped file) | Kit class |
|---|---|---|
| `pistol` | all pistols/SMGs (9×18, 9×19, .45, 5.7, 9×21 …) | **Type A** (handgun calibres) |
| `shotgun` | 12×70, 12×76, 20×70, 23×75 (TOZ, BM-16, Saiga, KS-23, Mossberg, SPAS …) | **Type B** (shotguns, historic) |
| `rifle_5` | 5.45×39, 5.56×45, 7.62×39, 5.7×28, 5.45-class AK/RPK, ADAR, M4, AK5C, G36, SKS | **Type C** (standard military calibres and specific SMGs) |
| `rifle_7` | 7.62×54R, 7.62×51, 9×39, 12.7×55, .338 Lapua/Federal, the big LMGs | **Type D** (large calibre, complex) |

Alongside those, **upgrade kits are tiered T1 → T3** and their tier follows the item's repair
class: mechanics carry T1 kits for novice/light gear and Type A weapons, the higher tiers
arrive with better armour and rifle-class weapons. **Most calibre-conversion upgrades were
removed in 0.9.5**, and the prices of most weapon upgrade kits went *down*.

### Cleaning vs repair vs replace

| Situation | Do this | Cost |
|---|---|---|
| Part ≥ 60 % | buy a **cleaning kit** from a mechanic (available with **no toolkit unlocked**) and use *clean barrel* / *clean part* | kit use; cheap |
| Part < 60 % | **repair kit** of the right Type → *maintain parts* (replaces all parts with 100 % ones, including barrels) | **1 repair-kit use**; also improves gun condition |
| Any part, any condition, except barrel | drag-and-drop a looted same-type part (clean them first with the ramrod/multitool/file) | free, but dirties the gun |
| Barrel worn | repair kit *maintain parts*, or a looted barrel part | 1 kit use |

Jamming in GAMMA is implemented by **Weapon Parts Overhaul** (`140- Weapon Parts Overhaul -
arti`, `gamedata/scripts/arti_jamming.script`), which owns the `kb_unjam` keybind
(`custom22`, default **`R`** — see `references/keybinds-settings.md`), plays the unjam
animations, and reports failures with `ui_st_unjam_fail`. Related shipped scripts:
`shotgun_unjam_fix.script` (Mossberg 590 reanimation), `unjam_motion_mark.script` (Weapon Pack),
and `207- Mags Redux (Disable G.A.M.M.A. Unjam Reload)`, whose
`grok_reload_bind_checker.script` **rebinds `custom22` to `kF10`** so that the unjam action
follows the reload key instead — that is exactly why the addon's name warns you, and why you
must not stack two magazine/jam overhauls. GAMMA also ships *No Weapon Jam Chance at Full
Condition* and a "(Less Intense)" variant, and 0.9.5 notes "reduced green parts chance,
**reduced jam chance**", "**Jam Probability differs between weapons**", and "Less random
weapon parts degradation".

## 3. The weapon roster (WP / NATO / ANY)

`good_weapons.txt` is the pack's own working list, headed **"> VERIFY CALIBERS AND DEFINE
FINAL LIST BASED ON VARIANTS"** — treat it as doctrine, not gospel. Each line is
`wpn_<id>` + a tag: **WP**, **NATO**, or **ANY**. Parenthesised lines are variant/pending
entries. Highlights per block:

| Class | WP | NATO | ANY |
|---|---|---|---|
| **9×18 pistols** ("drastically reduce recoil") | `wpn_pm_custom`, `wpn_pb`, `wpn_fort17`, `wpn_aps`, `wpn_oc33` | — | — |
| **9×19 pistols** | `wpn_oc33`, `wpn_pl15_tan` | `wpn_beretta_camo`, `wpn_sig226`, `wpn_walther_p99`, `wpn_glock`, `wpn_glock17_m1`, `wpn_glock_modern`, `wpn_colt1911_custom` | — |
| **.357 / .45 / 5.7 / 9×21** | `wpn_mp412` (.357), `wpn_sr1m` (9×21, "reduce recoil a lot") | `wpn_colt1911_camo`, `wpn_desert_eagle`, `wpn_colt1911_n`, `wpn_sig220_n`, `wpn_usp_tac_45`, `wpn_fnp45`, `wpn_fnx45_custom`, `wpn_korth_custom`, `wpn_fn57` | — |
| **SMG, 9×19** | `wpn_vz61`, `wpn_vityaz`, `wpn_pp2000` | `wpn_aug_freedom`, `wpn_udp9`, `wpn_mp5`, `wpn_mp9`, `wpn_mp5sd`, `wpn_kriss_vector` | — |
| **SMG, 5.7** | — | `wpn_p90_gs`, `wpn_p90gamma`, `wpn_mp7` | — |
| **SMG, .45** | `wpn_thompson_m1a1` (untagged), `wpn_thompson_1921` | `wpn_mp5_nimble`, `wpn_ump45_custom` | — |
| **Shotguns 12×70** | `wpn_bm16`, `wpn_bm16_full`, `wpn_toz34`, `wpn_toz34_obrez`, `wpn_protecta`, `wpn_mp155`, `wpn_saiga12s_m1/m2`, `wpn_saiga12s_isg` (WP+ISG) | `wpn_remington870`, `wpn_wincheaster1300`, `wpn_ithacam37_mag`, `wpn_mossberg590_rail`, `wpn_ithacam37_trench`, `wpn_spas12`, `wpn_benelli_m1014` | `wpn_raptr`, `wpn_ithacam37_stakeout_20x70` (20×70) |
| **Shotguns 23×75** | `wpn_ks23`, `wpn_ks23_23_up`, `wpn_ks23_kaban`, `wpn_ksg23` | — | `wpn_toz34_mark4_23` |
| **5.45×39 rifles** | `wpn_ak74u`, `wpn_ak74`, `wpn_ak74m`, `wpn_ak74u_tac`, `wpn_ak105`, `wpn_ak74_pmc`, `wpn_ak74m_beard`, `wpn_aek`, `wpn_abakan_n`, `wpn_rpk74_16`, `wpn_ak12_m1`, `wpn_rpk74_16_drum`, `wpn_groza_nimble`, `wpn_ak74u_m1_isg` (WP+ISG), `wpn_ak74_isg` (WP+ISG) | — | — |
| **5.56×45 rifles** | `wpn_adar2_15`, `wpn_ak101` | `wpn_xm4`, `wpn_aug`, `wpn_aug_merc`, `wpn_l85_m2`, `wpn_m4a1_siber`, `wpn_sig550`, `wpn_ak5c_bas`, `wpn_m4_tac`, `wpn_sig550_custom`, `wpn_g36ka4_rwap`, `wpn_g36v_rwap`, `wpn_m4_ru556`, `wpn_m249`, `wpn_howa20`, `wpn_fn2000_nimble` | — |
| **7.62×39 rifles** | `wpn_sks_b`, `wpn_sks_molot`, `wpn_rpk`, `wpn_akms_alt`, `wpn_ak103`, `wpn_rpd`, `wpn_ak104_alfa`, `wpn_akm_alfa`, `wpn_akm_isg` (WP+ISG), `wpn_mk47` | `wpn_brn180` | — |
| **9×39** | `wpn_vintorez_n1`, `wpn_9a91`, `wpn_groza`, `wpn_val`, `wpn_vihr`, `wpn_amb17`, `wpn_vintorez_isg` (WP+ISG) | — | — |
| **7.92×33** | — | `wpn_k98`, `wpn_k98_mod` | — |
| **7.62×54R** | `wpn_mosin`, `wpn_sv98`, `wpn_svd_m1`, `wpn_svu`, `wpn_svds`, `wpn_svds_pmc`, `wpn_pkm_siber`, `wpn_pkp_siber` | — | — |
| **7.62×51** | `wpn_dvl10` | `wpn_steyr_scout_big`, `wpn_remington700`, `wpn_remington700_magpul_pro`, `wpn_fal_aus`, `wpn_ace52`, `wpn_scar_siber`, `wpn_fal_sa58_osw` | `wpn_dtmdr_black`, `wpn_sr25` |
| **12.7×55** | `wpn_eft_rsh12`, `wpn_vssk`, `wpn_ash12` | — | — |
| **.338 Federal** | `wpn_dvl10_m1` | `wpn_remington700_lapua700` | — |
| **.338 Lapua** | — | — | `wpn_l96a1m`, `wpn_m98b` |
| **Special** | — | — | `wpn_gauss`, `wpn_rpg7` |

**The faction doctrine table** (verbatim at the bottom of the same file, typos included):

```
stalker   WP        cleat sky  NATO      ecolog     ANY
bandit    WP        freedom    NATO      monolith   ANY
military  WP        merc       NATO      renagades  ANY
duty      WP                              ISG        ANY
sin       WP
```

That matches the manual's trader-doctrine list, with the important **ANY** group —
**Ecologists, Monolith, Renegades and UNISG use either bloc's weapons**, and Monolith
"have about 50 % chance to have a NATO or WP gun".

Beyond the doctrine file, the pack ships **additional weapon sets** that expand the roster:
*G.A.M.M.A. Weapon Pack* (BAS / Boomsticks & Sharpsticks), *Retrogue's Additional Weapons*,
*The Covenant Weapon Pack 3DSS*, *439- The Covenant Weapon Pack for DX9*, *355- Steyr Scout*,
*423- Mossberg 590 Reanimation*, *Trophy Weapons*, plus **Momopate's Detailed Weapon Stats**
for anyone who misses the raw numbers (0.9.5 removed the damage stat from the UI — see §7).

## 4. Ammunition: the values that actually matter

`gamma_ammo_weapon_table.xlsx` is the pack's own math sheet. Its header row:
`Ammo | Type | price | price/round | damage per Rouble | pen per Rouble | ammo_k_ap |
ammo_k_hit | gun power | total damage | in game displayed power | IRL Joules | IRL Speed |
Overpen damage factor | Joules multiplier to ref (7,62x51) | In game power based on Joules |
In game power adjusted by overpen factor`. Selected rows verbatim:

| Ammo | Type | price/round | `ammo_k_ap` | `ammo_k_hit` | total damage |
|---|---|---|---|---|---|
| `ammo_7.62x51_fmj` | Perf | 200 | 0.34 | 0.89 | 0.89 |
| `ammo_7.62x51_ap` | AP | 500 | 0.62 | 0.89 | 0.89 |
| `ammo_5.45x39_fmj` | Perf | 90 | 0.27 | 1.14 | 0.57 |
| `ammo_5.45x39_ep` | DMG | 106.67 | 0.10 | **1.75** | 0.875 |
| `ammo_5.45x39_ap` | AP | 340 | 0.47 | 1.10 | 0.55 |
| `ammo_5.56x45_fmj` | Perf | 100 | 0.29 | 1.05 | 0.525 |
| `ammo_5.56x45_ss190` | DMG | 106.67 | 0.13 | 1.57 | 0.785 |
| `ammo_5.56x45_ap` | AP | 366.67 | 0.52 | 1.05 | 0.525 |
| `ammo_7.62x39_fmj` | Perf | 130 | 0.31 | 1.17 | 0.679 |
| `ammo_7.62x39_ap` | AP | 393.33 | 0.55 | 1.17 | 0.679 |
| `ammo_9x39_pab9` | Perf | 106.67 | 0.34 | 1.04 | 0.645 |
| `ammo_9x39_ap` | AP | 346.67 | 0.55 | 1.04 | 0.645 |
| `ammo_357_hp_mag` | DMG | 200 | 0.30 | **2.60** | 1.56 |
| `ammo_9x18_fmj` | Perf | 37.33 | 0.14 | 0.76 | 0.342 |
| `ammo_9x18_pmm` | DMG | 76.67 | 0.08 | **1.40** | 0.63 |
| `ammo_9x19_fmj` | Perf | 43 | 0.17 | 0.70 | 0.315 |
| `ammo_9x19_pbp` | DMG | 75 | 0.10 | **1.35** | 0.608 |
| `ammo_11.43x23_hydro` | DMG | 101.79 | 0.10 | **1.64** | 0.902 |
| `ammo_7.62x25_p` | DMG | 54.69 | 0.08 | 1.001 | 0.450 |
| `ammo_7.62x25_ps` | AP | 60.94 | 0.25 | 0.70 | 0.315 |
| `ammo_5.7x28_ss190` | AP | 130 | 0.42 | 0.69 | 0.345 |
| `ammo_12x70_buck` | DMG | 75 | 0.27 | **3.78** | 3.024 |
| `ammo_12x76_zhekan` | Perf | 145 | 0.23 | **2.70** | 2.16 |
| `ammo_23x75_shrapnel` | DMG | 200 | 0.36 | **9.0** | 4.32 |
| `ammo_23x75_barrikada` | AP | 700 | 0.54 | 4.2 | 2.016 |
| `ammo_20x70_buck` | DMG | 60 | 0.27 | 2.70 | 2.16 |
| `ammo_pkm_100` | AP | 166.67 | 0.37 | 1.02 | 0.785 |
| `ammo_og-7b` (RPG) | EX | 416.33 | 0.37 | 3.0 | 9.0 |
| `ammo_338_federal` | DMG | 400 | 0.18 | **10.7** | 9.095 |
| `ammo_magnum_300` | AP | 1 700 | 1.4 | 1.26 | 1.512 |

Two lessons fall out of the table itself: **HP/DMG rounds have low `ammo_k_ap` and the
highest `ammo_k_hit`** (mutant killers), and **AP rounds double or triple `ammo_k_ap` while
keeping `ammo_k_hit` unchanged** (armour killers) — and the price-per-Rouble columns show you
are paying 3–5× more per round for that AP value.

## 5. Ammunition doctrine (the manual, verbatim structure)

**GROBBS** — "GAMMA uses **Grok's Balanced Overhaul Of Ballistic System**… it changes the
bullets and armor penetration **from PLAYER to NPCs** (not the other way around) using **EFT's
ammunition system** as an inspiration."

The rules, quoted:

- "**Ammo Armor Penetration (AP) power is compared to the limb armor of the opponent.**"
- "If **AP power > limb armor**, damage is applied. If **AP power is less than limb armor, no
  damage is applied and limb armor is reduced based on AP power.**"
- "**Leg and face armor are reduced.**"
- "FMJ and HP ammo will still work, but the enemy armor must be destroyed by many of these
  bullets to start doing damage."
- "**AP ammo**: expensive but will defeat any endgame heavily armored target… don't use them
  against lightly armored targets or you will waste money."
- "**FMJ**: cheap… use to kill lightly armored targets or as a cheaper and less effective
  replacement for AP ammo."
- "**HP**: a bit more expensive than FMJ and should be used to kill mutants since it has even
  less AP power than FMJ."
- "**Sniper ammo is actually very powerful**… **.338 Lapua will one shot most enemies with a
  hit to the chest** if you can afford it."
- "**Buckshot** will work as inexpensive early game ammo against stalkers… good for mutants,
  bad for exos. **Slugs** are good to kill mutants and stalkers alike. **AP Slugs are best
  against stalkers.**"
- "Some ammo is much more useful against mutants: **HP ammo, .357 magnum, .45 Hydrashock,
  buckshots, slugs, 7.62×25 Pst.**"

**BR classification** (in the manual and in every ammo description):

| BR class | Penetrates |
|---|---|
| BR1–BR2 | light armours |
| BR3–BR4 | middle-class armours |
| BR5 | heavy armours |
| BR6 | exo armours |

**Faction ammunition behaviour** (manual, verbatim): "**Monolith is only using AP ammo**.
**Sin is only using AP ammo, mainly using heavy machine guns, and much more resistant than a
normal human being.** **ISG members have very good gear, only use AP ammo and have a higher
ammo penetration resistance.** **Most Master and Legend stalkers use AP ammo.** Factions use
guns according to their trader type (WP or NATO)."

## 6. Attachments, magazines and fire modes

| System | Facts |
|---|---|
| **Mags/Magazines** | the pack ships *Anomaly Magazines Redux* and *G.A.M.M.A. Mags Redux*; the notes tell you to **disable GAMMA's unjam-reload bind** when using Mags Redux (`207- Mags Redux (Disable G.A.M.M.A. Unjam Reload) - RavenAscendant`). *Mags Buyable at Traders* re-enables magazine purchases, and *ATHI's Mags Redux Mod Madness* tweaks it further |
| **Attachment prices** | `mod_system_weapons_gamma_attachments_price.ltx` prices scopes, sights, suppressors and launchers; the **supply tables** gate which of them a trader will even show (supply 2 → optics, supply 3 → high-end optics, supply 4 → launchers, supply 5 → `gauss_sight`) |
| **UBGL (under-barrel launcher)** | rebound to **Left Alt** in 0.9.5 |
| **Fire modes** | `grok_weapon_fire_modes` runs the selector; 0.9.5 added the **G3 burst fire mode** as an upgrade, and *Retrogue's Additional Weapons* / *G.A.M.M.A. Weapon Pack* add more |
| **Cover tilt** | `235- Weapon Cover Tilt - Demonized` — "Weapon Cover Tilt" is a shipped aim-behaviour mod |
| **Weapon lowering** | `467- Lower Weapon Sprint Optimized - Spaicrab` |
| **Doom-like inspection** | `95- Doom-like weapon inspection - Grokitach` — the "inspect weapon" animation family |
| **Ammo wheel** | `Slugler's & Andtheherois's No old ammo in wheel` and `205- Old to ammo to new ammo converter` exist because GAMMA merged old/new ammo types; the **Y key** (default) cycles ammo types for the active gun |
| **Auto-holster/empty** | `grok_weapon_drop_on_empty`, `grok_weapon_autoreload` |

## 7. What changed in 0.9.5 for weapons

| Change | Detail (verbatim fragments from the patch notes) |
|---|---|
| **Gun overhaul** | "Guns have been improved noticeably based on the work of AndTheHeroIs through his **'GAMMA Immaculate Munition Pack' (GIMP)** and **3D Shader Scopes for GAMMA (3DSSG)** mods" |
| **New weapons** | "'Many new weapons have been added to GAMMA, like the **MAC10, MSBS Grot, HK23, SVT40**, and more.'" Plus *Billwa's Weapon Collection*, *SVT-40 'n AVT-40*, *MSBS Grot*, *Uzi family*, *BRN-180*, *Steyr Scout*, *Mossberg 590 Reanimation*, *Trophy Weapons*, *Covenant Weapon Pack* |
| **Shotguns / sawn-offs** | "Shotguns have been rebalanced a bit based on new models and animation sets, and **sawn-offs now fit pistol slots**" |
| **3D ballistics** | "**3D ballistics have been turned on by default**, meaning guns will shoot where the barrel is aiming, which puts more emphasis on using **lasers** for hip firing." A separate line: "3D ballistics activated by default now since 3DSSG now supports it" |
| **Lasers** | laser rendering reworked from **Borksy's Laser Settings** — "the laser size change and dim based on target distance" |
| **Handling** | "Weapon handling has been changed thanks to the work of Verdatim: **swapping to pistols is now much faster** than swapping to other guns, and aiming down sights plays a little **shouldering animation** with a speed depending on the gun type, handling stat, and weapon weight" (**Fast Pistol Swap**, **Non linear ADS**) |
| **Damage stat removed** | "**Removed damage stats from gun display**" and "removed weapon 'max range' stat"; ammo descriptions still carry the AP/DMG values, and **Momopate's Detailed Weapon Stats** is shipped for players who want the numbers back |
| **Upgrade kit overhaul** | "Upgrades kits needed overhaul based on armor, helmet and weapons **repair type**"; "**Reduced prices of most gun upgrade kits**"; "Most caliber change upgrade removed" / "Removal of ACE caliber change upgrade" / "Removed Kiparis upgrade to 9x19"; "Durability upgrades reduce armor degradation" |
| **Conversions that survived** | the flavour ones: "a simple **PM** pistol can turn into a fast-firing, low-recoil, large-magazine pistol with a laser module; the **Kiparis** can turn into a 50-round magazine beast; and the **AUG 9 mm** can have a long-range thermal scope for much cheaper than any other thermal kit" |
| **Gun repair types** | "**Gun repair types have been changed a bit**" — see §2 for the four classes |
| **Jamming** | "Jam Probability differs between weapons", "reduced jam chance", "Less random weapon parts degradation" |
| **UBGL** | "using a new engine feature, **UBGL usage is now tied to a specific key: Left Alt**" |
| **Ammo economy** | "**Ecologs sell Gauss Ammo at Supply Tier 4**", "Gauss Ammo alternative crafting recipes", "**Exo batteries craft recipe from gauss ammo**", "**Parts added to gunsmith and medic toolkits**", "Buffed 9x18 caliber (more damage, bit less pen)" |

## 8. Practical weapon progression

1. **South (Cordon/Swamps/Garbage):** a Toz-34, BM-16, SKS, Mosin, PPSH or a starter pistol.
   Ammo is cheap: 9×18 FMJ costs 37.33 RU/round, buckshot 75 RU/round.
2. **Garbage → Bar:** the AK/SKS/Saiga tier; buy the **Type A/B cleaning kits** as soon as a
   mechanic will sell them (no toolkit needed) so looted guns can be made usable.
3. **Mid Zone (Rostok/Yantar/Military):** 5.45/5.56 assault rifles, first scopes (supply 2),
   the first suppressors.
4. **North (Red Forest → Pripyat):** the 7.62×51/54R AP and .338 families; **Type D repair
   kits** and the expert toolkit that unlocks them; AP ammo is mandatory against
   Monolith/Sin/ISG.
5. **Everywhere:** loot parts off corpses and **disassemble every weapon you will not use** —
   parts feed both crafting and repair.

## 9. Quick answers

| Question | Answer |
|---|---|
| Can I buy guns? | No — traders sell supplies/accessories only; Black Market MCM toggle re-enables gear purchases. |
| Why does my gun jam? | Its **parts** (bolt, bolt carrier, trigger components) are worn; each part contributes to jam chance. |
| Why does my gun do no damage? | The **barrel** is worn — barrel condition sets damage and penetration. |
| What fixes a part above 60 %? | A **cleaning kit** from a mechanic (no toolkit required): right-click the gun → clean barrel/part. |
| What fixes a part below 60 %? | A **repair kit** of the weapon's Type (A pistol, B shotgun, C rifle-5, D rifle-7) → *maintain parts*; also replaces barrels. |
| Can I repair parts without kits? | Yes — clean parts above 60 % with the ramrod/multitool/file, then drag-and-drop them onto the gun (barrels excluded). |
| How often are repair kits consumable? | `max_uses = 3` per kit in the shipped balance. |
| How do I clean the gun itself? | Cleaning equipment or a mechanic; cleaning prevents parts degrading as you shoot, but does not repair parts. |
| Which ammo against armour? | AP (high `ammo_k_ap`); check the ammo's **BR class** — BR5 for heavy, BR6 for exo. |
| Which ammo against mutants? | HP/DMG rounds, .357 Magnum, .45 Hydrashock, buckshot, slugs, 7.62×25 Pst. |
| What do Monolith, Sin and ISG use? | AP ammo exclusively; Sin also fields heavy machine guns and is more resistant than a normal human. |
| Which faction uses NATO or WP guns? | Per `good_weapons.txt`: Loners, Bandits, Military, Duty, Sin = WP; Clear Sky, Freedom, Mercenaries = NATO; Ecologists, Monolith, Renegades, UNISG = ANY. |
| Where are the damage numbers? | In the ammo's description (AP + stopping power) and `gamma_ammo_weapon_table.xlsx`; the weapon stat was removed in 0.9.5. |
| How do I switch ammo types? | Default **Y** key for the active weapon. |
| How do I use the under-barrel launcher? | **Left Alt** (0.9.5 rebind). |

Cross-references: the BR system's armour side and damage maths →
`references/ballistics-damage.md`; kit prices, recipes and toolkit gating →
`references/crafting-repairs.md`; armour and helmet protection values →
`references/armor-outfits.md`; trader supply levels that gate attachments →
`references/trading-economy.md`; keybinds for unjam, ammo wheel and UBGL →
`references/keybinds-settings.md`.

---

## Appendix B — the complete gun list, by calibre class

The pack's own curated weapon roster, `modpack_addons/good_weapons.txt`, reproduced in full —
its section headers are kept verbatim apart from the file's `#########` decoration. The tag is
the **ammunition bloc the gun is meant to be fed from**: see `references/trading-economy.md` §4
for what that means at a trader, and the faction table at the end of this appendix for the
same file's bloc assignment per community.

**9x18 Pistols — drastically reduce recoil**

| Gun (item id) | Bloc |
|---|---|
| `wpn_pm_custom` | WP |
| `wpn_pb` | WP |
| `wpn_fort17` | WP |
| `wpn_aps` | WP |
| `wpn_oc33` | WP |

**9x19 Pistols**

| Gun (item id) | Bloc |
|---|---|
| `wpn_beretta_camo` | NATO |
| `wpn_oc33` | WP |
| `wpn_sig226` | NATO |
| `wpn_walther_p99` | NATO |
| `wpn_glock` | NATO |
| `wpn_glock17_m1` | NATO |
| `wpn_pl15_tan` | WP |
| `wpn_glock_modern` | NATO |
| `wpn_colt1911_custom` | NATO |

**7.62x25 Pistol**

| Gun (item id) | Bloc |
|---|---|
| `wpn_tt33_modern` | WP |

**.357 Pistols**

| Gun (item id) | Bloc |
|---|---|
| `wpn_mp412` | WP |
| `wpn_colt1911_camo` | NATO |
| `wpn_desert_eagle` | NATO |

**.45 Pistols**

| Gun (item id) | Bloc |
|---|---|
| `wpn_colt1911_n` | NATO |
| `wpn_sig220_n` | NATO |
| `wpn_usp_tac_45` | NATO |
| `wpn_fnp45` | NATO |
| `wpn_fnx45_custom` | NATO |
| `wpn_korth_custom` | NATO |

**5.7 Pistol — reduce recoil a lot**

| Gun (item id) | Bloc |
|---|---|
| `wpn_fn57` | NATO |

**9x21 Pistol — reduce recoil a lot**

| Gun (item id) | Bloc |
|---|---|
| `wpn_sr1m` | WP |

**7.62x25 SMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_ppsh41` | WP |

**9x18 SMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_kiparis` | WP |
| `wpn_bizon` | WP |

**9x19 SMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_vz61` | WP |
| `wpn_aug_freedom` | NATO |
| `wpn_udp9` | NATO |
| `wpn_vityaz` | WP |
| `wpn_mp5` | NATO |
| `wpn_pp2000` | WP |
| `wpn_mp9` | NATO |
| `wpn_mp5sd` | NATO |
| `wpn_kriss_vector` | NATO |

**.45 SMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_mp5_nimble` | NATO |
| `wpn_ump45_custom` | NATO |

**5.7 SMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_p90_gs` | NATO |
| `wpn_mp7` | NATO |
| `wpn_p90gamma` | NATO |

**9x21 SMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_sr2_veresk` | WP |
| `wpn_sr2_m1` | WP |

**12x70**

| Gun (item id) | Bloc |
|---|---|
| `wpn_bm16` | WP |
| `wpn_bm16_full` | WP |
| `wpn_toz34_obrez` | WP |
| `wpn_toz34` | WP |
| `wpn_remington870` | NATO |
| `wpn_wincheaster1300` | NATO |
| `wpn_ithacam37_mag` | NATO |
| `wpn_mossberg590_rail` | NATO |
| `wpn_ithacam37_trench` | NATO |
| `wpn_protecta` | WP |
| `wpn_mp155` | WP |
| `wpn_saiga12s_m1` | WP |
| `wpn_saiga12s_m2` | WP |
| `wpn_spas12` | NATO |
| `wpn_benelli_m1014` | NATO |
| `wpn_raptr` | ANY |

**20x70**

| Gun (item id) | Bloc |
|---|---|
| `wpn_toz106` | WP |
| `wpn_toz106_m1` | WP |
| `wpn_ithacam37_stakeout_20x70` | ANY |

**23x75**

| Gun (item id) | Bloc |
|---|---|
| `wpn_ks23` | WP |
| `wpn_ks23_23_up` | WP |
| `wpn_ks23_kaban` | WP |
| `wpn_toz34_mark4_23` | ANY |
| `wpn_ksg23` | WP |

**.357 Rifle**

| Gun (item id) | Bloc |
|---|---|
| `wpn_winchester1873` | NATO |

**5.45x39**

| Gun (item id) | Bloc |
|---|---|
| `wpn_ak74u` | WP |
| `wpn_ak74` | WP |
| `wpn_ak74m` | WP |
| `wpn_ak74u_tac` | WP |
| `wpn_ak105` | WP |
| `wpn_ak74_pmc` | WP |
| `wpn_ak74m_beard` | WP |
| `wpn_aek` | WP |
| `wpn_abakan_n` | WP |
| `wpn_rpk74_16` | WP |
| `wpn_ak12_m1` | WP |
| `wpn_rpk74_16_drum` | WP |
| `wpn_groza_nimble` | WP |

**5.56x45**

| Gun (item id) | Bloc |
|---|---|
| `wpn_adar2_15` | WP |
| `wpn_ak101` | WP |
| `wpn_xm4` | NATO |
| `wpn_aug` | NATO |
| `wpn_aug_merc` | NATO |
| `wpn_l85_m2` | NATO |
| `wpn_m4a1_siber` | NATO |
| `wpn_sig550` | NATO |
| `wpn_ak5c_bas` | NATO |
| `wpn_m4_tac` | NATO |
| `wpn_sig550_custom` | NATO |
| `wpn_g36ka4_rwap` | NATO |
| `wpn_g36v_rwap` | NATO |
| `wpn_m4_ru556` | NATO |
| `wpn_m249` | NATO |
| `wpn_howa20` | NATO |
| `wpn_fn2000_nimble` | NATO |

**7.62x39**

| Gun (item id) | Bloc |
|---|---|
| `wpn_sks_b` | WP |
| `wpn_sks_molot` | WP |
| `wpn_rpk` | WP |
| `wpn_akms_alt` | WP |
| `wpn_ak103` | WP |
| `wpn_rpd` | WP |
| `wpn_brn180` | NATO |
| `wpn_ak104_alfa` | WP |
| `wpn_akm_alfa` | WP |
| `wpn_mk47` | WP |

**9x39**

| Gun (item id) | Bloc |
|---|---|
| `wpn_vintorez_n1` | WP |
| `wpn_9a91` | WP |
| `wpn_groza` | WP |
| `wpn_val` | WP |
| `wpn_vihr` | WP |
| `wpn_amb17` | WP |

**7.92**

| Gun (item id) | Bloc |
|---|---|
| `wpn_k98` | NATO |
| `wpn_k98_mod` | NATO |

**7.62x54r**

| Gun (item id) | Bloc |
|---|---|
| `wpn_mosin` | WP |
| `wpn_sv98` | WP |
| `wpn_svd_m1` | WP |
| `wpn_svu` | WP |
| `wpn_svds` | WP |
| `wpn_svds_pmc` | WP |

**7.62x51**

| Gun (item id) | Bloc |
|---|---|
| `wpn_dvl10` | WP |
| `wpn_steyr_scout_big` | NATO |
| `wpn_remington700` | NATO |
| `wpn_remington700_magpul_pro` | NATO |
| `wpn_fal_aus` | NATO |
| `wpn_ace52` | NATO |
| `wpn_scar_siber` | NATO |
| `wpn_fal_sa58_osw` | NATO |
| `wpn_dtmdr_black` | ANY |
| `wpn_sr25` | ANY |

**12.7**

| Gun (item id) | Bloc |
|---|---|
| `wpn_eft_rsh12` | WP |
| `wpn_vssk` | WP |
| `wpn_ash12` | WP |

**.338 Federal**

| Gun (item id) | Bloc |
|---|---|
| `wpn_dvl10_m1` | WP |
| `wpn_remington700_lapua700` | NATO |

**.338 Lapua**

| Gun (item id) | Bloc |
|---|---|
| `wpn_l96a1m` | ANY |
| `wpn_m98b` | ANY |

**Special**

| Gun (item id) | Bloc |
|---|---|
| `wpn_gauss` | ANY |
| `wpn_rpg7` | ANY |

**7.62x54 LMG**

| Gun (item id) | Bloc |
|---|---|
| `wpn_pkm_siber` | WP |
| `wpn_pkp_siber` | WP |


### Faction blocs (verbatim from the same file)

| Community | Bloc |
|---|---|
| stalker | WP |
| bandit | WP |
| military | WP |
| duty | WP |
| sin | WP |
| freedom | NATO |
| merc | NATO |
| ecolog | ANY |
| monolith | ANY |
| renagades | ANY |
| ISG | ANY |
