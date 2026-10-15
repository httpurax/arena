# Factions, relations and standing — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the pack's **relations table** `creatures/game_relations.ltx`
(`[game_relations]` rank/reputation/goodwill ladders and the full `[communities_relations]`
matrix, as shipped by `G.A.M.M.A. Economy`); the **starting locations** plugin
`G.A.M.M.A. Starting Locations/gamedata/configs/plugins/new_game_start_locations.ltx`; the
**starting loadouts** `G.A.M.M.A. Starting Loadouts/…/new_game_loadouts.ltx`; the faction keys
in `109- MCM Mod Configuration Menu` (`ui_main_menu.script` → `character_creation`
`new_game_faction`, `new_game_loadout`, `new_game_difficulty`, `new_game_economy`); the
per-faction trader files under `G.A.M.M.A. Economy/…/items/trade/`; the faction patch prices in
`mod_system_zzzzzzzzzzzzzzzzzzz_GAMMA_items_price.ltx`; the manual's *Storylines & Missions*,
*Trading* and *Money* articles; the faction column of the pack's own outfit table
(`G.A.M.M.A. Outfits Balances/tools/armor_values.tsv`); and the faction doctrine table at the
end of `good_weapons.txt`. Snapshot: GAMMA 0.9.5 @
`ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. The communities GAMMA defines

`game_relations.ltx` numbers the communities in this order (verbatim from the
`communities =` line): `actor 0, monster 1, trader 2, army_npc 3, greh_npc 4, bandit 5,
dolg 6, ecolog 7, freedom 8, killer 9, army 10, monolith 11, greh 12, stalker 13, zombied 14,
csky 15, isg 16, renegade 17` — plus one entry per player faction (`actor_stalker` … 
`actor_renegade`) and `arena_enemy`.

Decoded, and matched against the faction names used everywhere else in GAMMA:

| Engine name | GAMMA's name | Notes |
|---|---|---|
| `stalker` | **Loners / Free Stalkers** | the default player faction |
| `bandit` | **Bandits** | allied to Renegades |
| `dolg` | **Duty** | |
| `freedom` | **Freedom** | Duty's enemy |
| `ecolog` | **Ecologists** | Sakharov, Hermann; artefacts economy |
| `army` | **Military** | allied to `army_npc` (2000) |
| `killer` | **Mercenaries** | Dead City; the pack also ships trader files for them |
| `monolith` | **Monolith** | allied to Sin and to zombies |
| `greh` | **Sin** | neutral to monsters (0) — and the pack ships a *Sin and Mutants are Allies* patch |
| `csky` | **Clear Sky** | Swamps base |
| `isg` | **UNISG** | unlockable by typing `isg` in character creation |
| `renegade` | **Renegades** | allied to Bandits |
| `zombied` | **Zombified** | a playable start (`abandoned_sawmill`, Zaton) |

## 2. Relations: who is actually at war

Rules of the table (verbatim header): **">999 = Ally, 0 = Neutral, <-999 = Enemy"**, and the
engine thresholds `attitude_neutal_threshold = -999`, `attitude_friend_threshold = 999`, with
standing constants `goodwill_enemy = -1000`, `goodwill_neutal = 0`, `goodwill_friend = 1000`.

Reading the shipped matrix row by row (a value of **300** means "neutral-plus, self/kin",
**±2000** means the extreme):

| Faction | Allied with (≥ 999) | Neutral with (between) | Hostile to (≤ −999) |
|---|---|---|---|
| **Loners** (`stalker`) | — (self 300) | trader; `army_npc`, `greh_npc`; **Duty, Ecologists, Freedom, Clear Sky** | Bandits, Mercenaries, Military, Monolith, Sin, Zombified, UNISG, Renegades |
| **Bandits** | **Renegades** (300) | `greh_npc`; **Freedom, Mercenaries** | Duty, Ecologists, Military, Monolith, Sin, Loners, Zombified, Clear Sky, UNISG |
| **Duty** (`dolg`) | — | `army_npc`, `greh_npc`; **Military, Ecologists, Loners** | **Freedom**, Bandits, Mercenaries, Monolith, Sin, Zombified, Clear Sky, UNISG, Renegades |
| **Freedom** | — | `army_npc`, `greh_npc`; **Bandits, Ecologists, Mercenaries, Loners, Clear Sky** | **Duty**, Military, Monolith, Sin, Zombified, UNISG, Renegades |
| **Ecologists** | — | `army_npc`, `greh_npc`; **Duty, Freedom, Mercenaries, Military, Loners, Clear Sky** | Bandits, Monolith, Sin, Zombified, UNISG, Renegades |
| **Military** (`army`) | **`army_npc`** (2000) | **Duty, Ecologists** | Bandits, Freedom, Mercenaries, Monolith, Sin, Loners, Zombified, Clear Sky, UNISG, Renegades |
| **Mercenaries** (`killer`) | — | `army_npc`, `greh_npc`; **Bandits, Ecologists, Freedom, Clear Sky, UNISG** | Duty, Military, Monolith, Sin, **Loners**, Zombified, Renegades |
| **Monolith** | self 2000; **`greh_npc` (300), Sin (300), Zombified (300)** | — | everyone else (all −2000) |
| **Sin** (`greh`) | **`greh_npc` (300), Monolith (300), Zombified (300)** | **monsters (0)**, trader | everyone else |
| **Clear Sky** (`csky`) | — | `army_npc`, `greh_npc`; **Ecologists, Freedom, Mercenaries, Loners** | **Bandits, Duty**, Military, Monolith, Sin, Zombified, UNISG, Renegades |
| **UNISG** (`isg`) | — | **Mercenaries (0)** | literally everyone else, including all four "neutral" NPC communities |
| **Renegades** | **Bandits (300)** | `army_npc`, `greh_npc` | everyone else |
| **Zombified** | `greh_npc` (300), Monolith, Sin | **traders (1)** | everyone else |

Three structural facts fall out of this table that a player should internalise:

1. **Duty ↔ Freedom is the only true two-sided faction war at the top.** They are −2000 to
   each other while both being neutral (or better) with Loners, Ecologists and Mercenaries.
2. **UNISG is at war with the entire Zone** — its only non-hostile relation is with the
   Mercenaries. Playing UNISG (via `isg`) means a completely different diplomacy game.
3. **Monolith and Sin are a bloc** — with each other, with the Monolith-flavoured
   `greh_npc` community, and with zombies; Sin is even neutral toward monsters, which is what
   the shipped *Sin and Mutants are Allies* patch formalises.

## 3. Standing: rank, reputation and goodwill

From the same file, verbatim value ladders:

| Meter | Ladder |
|---|---|
| **Rank** (`rating`) | `novice` (≤ 3 999) → `trainee` (5 999) → `experienced` (9 999) → `professional` (15 999) → `veteran` (23 999) → `expert` (34 999) → `master` (49 999) → `legend`. The file's comment: "Requirements for each rank increase by an additional multiple of 500 points with each rank. Rookie → Trainee: 500 (+500), Trainee → Experienced: 1500 (+1000), Experienced → Professional: 3000 (+1500)…" |
| **Monster rating** | `weak` (≤ 40), `normal` (80), `strong` |
| **Reputation** | `terrible` (−1 999), `really_bad` (−1 499), `very_bad` (−999), `bad` (−499), `neutral` (499), `good` (999), `very_good` (1 499), `really_good` (1 999), `excellent` |
| **Goodwill vs a faction** | `st_goodwill_enemy` (0), `st_goodwill_indifferent` (1 000), `st_goodwill_friendly` |

The file also spells out how an NPC's attitude to you is computed:
`attitude = personal_goodwill + community_goodwill + community_to_community + reputation_goodwill + rank_goodwill` — i.e. **your faction's relations change how individuals see you**, which is why joining Duty makes Freedom's rank and file shoot on sight even though your personal goodwill is zero.

GAMMA exposes **rank/relationship cheats and protections** in its addon list — e.g.
`Ranks and Relationship Cheat - Emper`, `Clear Sky Changes`, and the goal-tracking
`G.A.M.M.A. Guide faction` — so players who want to see the ladders in-game have tooling for
it.

## 4. Goodwill is how traders unlock stock

This is the mechanic that makes goodwill matter beyond diplomacy. In every faction trader file
the supply line is gated on **faction** goodwill (examples verbatim):

```
; Sidorovich (Loner trader)
buy_supplies = {=actor_goodwill_ge(stalker:2000)} supplies_5, {=heavy_pockets_functor()} supplies_5,
               {=actor_goodwill_ge(stalker:1500)} supplies_4, {=actor_goodwill_ge(stalker:1000)} supplies_3,
               {=actor_goodwill_ge(stalker:500)} supplies_2, supplies_1

; Sakharov (Ecologists)
buy_supplies = {=actor_goodwill_ge(ecolog:2000)} supplies_5, {=heavy_pockets_functor()} supplies_5, …
```

So: **500 goodwill → supply level 2, 1 000 → 3, 1 500 → 4, 2 000 → 5**, plus an alternative
route for rich players (`heavy_pockets_functor()`, i.e. "carry enough money"). Supply sections
chain upward (`[supplies_2]:supplies_1`), so each step *adds* to the previous level's stock.

Which factions have goodwill-gated traders in the shipped files: **loner (`stalker`)**,
`bandit`, `dolg`, `ecolog`, `freedom`, `army` (Military), `killer` (Mercenaries), `csky`,
`monolith`, `isg`, `greh` (Sin). Faction traders therefore always sell a mix of
**supplies/consumables/accessories** and **faction-specific supplies**:

| Supply level (WP preset, verbatim items) | What it adds |
|---|---|
| `supply_1_wp` | starter gear: `wpn_sil_sr1m`, `wpn_sil_aps`, `lazup_pl15`, `pl15_scolaz`, `sr1upgr1`, `ammo_7.62x54_7h1` ×3, `ammo_9x19_fmj`/`ammo_9x18_fmj`/`ammo_7.62x25_ps` ×6, `wpn_knife`, `wpn_sil_9mm` |
| `supply_2_wp` | scopes/sights (`ekp8_02`, `ekp8_18`, `kobra`, `eot`, `okp`, `0kp2`, `rakurs`, `1p63`, `pka`, `p1x42`, `pk6`), `af_kevlar`, `gurza_up`, `vitup`, and calibres `ammo_5.45x39_fmj`, `ammo_9x39_pab9`, `ammo_23x75_shrapnel` (0.70), `ammo_12.7x55_fmj` (0.50) |
| `supply_3_wp` | high-end optics (`1p29`, `1p78gs`, `pn23`, `ps01`, `pso1m21`, `pso2`, `susat`, `pgo7gs`, `wpn_addon_scope_po4x34`) and **kits** (`sr2_upkit`, `23_up`, `kab_up`, `sup`, `kp_sr2`) |
| `supply_4_wp` | `kashtan_rmr`, `pritseldob`, `1p59`, **grenade launchers** (`wpn_addon_grenade_launcher`, `…_monolit`), `wpn_sil_rotor`, `wpn_sil_tgpv`, `wpn_sil_kzrzp` |
| `supply_5_wp` | `wpn_knife6`, **`recipe_exo_1/2/3`** and `gauss_sight` |

The NATO preset mirrors this structure (`supply_1_nato` … `supply_5_nato` in
`gamma_nato_preset.ltx`), and each faction trader file picks the flavour: e.g.
`[supplies_1]:common_stock,supply_1_wp` in `trade_bandit.ltx` / `trade_duty.ltx`, versus
`[supplies_1]:common_stock,supply_1_nato` in `trade_csky_spore.ltx`.

Related facts: **`trade_presets.ltx` also defines the buy/sell classifier groups** —
`[weapons]`, `[outfits_all]`, `[consumables]`, `[artefacts]`, `[tools]`, `[repair_kits]`,
`[upgrade_items]`, `[mutant_parts]`, and a `[none]` group that contains weapons, outfits and
scripts items, i.e. the classes most traders are configured not to trade. That is the data
behind the manual's flat statement that traders "**sell only supplies and accessories, never
weapons or armour**" (Black Market toggle aside).

## 5. Starting a new game as a faction

`new_game_start_locations.ltx` lists the **spawn points per faction**; the second field in each
line is a `story_only` boolean (true = only available in story mode). Verbatim extracts:

| Faction | Starting locations (`section = map`) |
|---|---|
| `stalker_start_locations` | `rookie_village = l01_escape`, `hidden_base = k00_marsh`, `lodging_house = l05_bar` |
| `bandit_start_locations` | `northern_factory = l04_darkvalley`, `car_park = l01_escape`, `train_hangar = l02_garbage`, `abandoned_school = l09_deadcity`, `truck_cemetery_bandits_post = k02_trucks_cemetery`, `tuzla_outpost = k00_marsh`, `pole_bandit_base = l01_escape` |
| `dolg_start_locations` | `makeshift_barracks = l05_bar` (single option) |
| `freedom_start_locations` | `military_base = l07_military`, `abandoned_school = l09_deadcity`, `truck_cemetery_bandits_post = k02_trucks_cemetery` |
| `ecolog_start_locations` | `sakharovs_bunker = l08_yantar`, `research_institute = l03_agroprom` |
| `army_start_locations` | `research_institute = l03_agroprom`, `tc_central_tower = k02_trucks_cemetery`, `eastern_factory = l04_darkvalley`, `machine_yard = k00_marsh`, `southern_checkpoint = l01_escape`, `village_ruins = k00_marsh` |
| `csky_start_locations` | `hidden_base = k00_marsh`, `rookie_village = l01_escape` |
| `killer_start_locations` | `sports_center = l09_deadcity`, `construction_site = l06_rostok`, `sakharovs_bunker = l08_yantar` |
| `monolith_start_locations` | `cultural_center = l11_pripyat`, `brain_scorcher = l10_radar`, `power_station = l12_stancia` (no `story_only` flag → available outside story mode too), `river_port = pripyat`, `kbo_monolith = pripyat`, `yanov_depo_monolith = jupiter`, `l13_generators = l12_stancia`, `bridge_red_forest_mon = l10_red_forest` |
| `greh_start_locations` (Sin) | `red_forest_old_mine = l10_red_forest`, `brain_scorcher = l10_radar`, `river_port = pripyat`, `l13_generators = l12_stancia`, `kbo_monolith = pripyat` |
| `isg_start_locations` (UNISG) | `dasc_sawwill = l01_escape` (single option) |
| `renegade_start_locations` | `tuzla_outpost = k00_marsh`, `pole_bandit_base = l01_escape` |
| `zombied_start_locations` | `abandoned_sawmill = zaton`, `kopachy_village = jupiter`, `river_port = pripyat`, `tunnel_entrance = jupiter` |

Notice the design: **the hostile-but-playable factions start in the north** (Monolith, Sin),
which is a self-imposed hard mode, while Loners/Bandits/Clear Sky/Renegades start south.

### Loadouts

`new_game_loadouts.ltx` gives every faction a shared base plus faction weapons and outfits,
bought with a **points budget**: `total_points_eco_1 = 1700`, `total_points_eco_2 = 1400`,
`total_points_eco_3 = 1100` (three economy tiers — the same values that appear as shop
budgets). Items are written `section = can_choose, amount, points [, max_difficulty]`, e.g.
`wpn_mosin = true,1,800`, `wpn_sks_b = true,1,1000,1` (locked to difficulty 1 and above).

Shared items every faction always receives (verbatim selection): `cash`, `device_pda_1`,
`bandage ×3`, `jgut`, `batteries_dead ×2`, `flask`, `vodka`, `tushonka`, `box_matches ×4`,
`swiss_knife`, `grooming`, `itm_actor_backpack`, `itm_backpack`, `detector_simple`,
`detector_radio`, `wpn_knife`, `bolts_pack ×2`, and a `picture_woman`.

Faction flavour examples:

| Faction | Headgear | Signature choices |
|---|---|---|
| **Loner** | `helm_resp` (50) | `wpn_ithacam37_stakeout_20x70` (550), `wpn_sks_b` (1000), `wpn_mosin` (800), `wpn_ppsh41` (650), `wpn_vityaz` (500), `wpn_kiparis` (300), `wpn_toz34_obrez` (550, diff ≤2), `wpn_toz106_m1` (375) + pistols; `novice_outfit` (50), `stalker_salamander_outfit` (500); `joint`, `ammo_9x18_ap` |
| **Bandit** | `helm_cloth_mask` (50) | `wpn_eft_mts_255` (600); `bandit_novice_outfit` (50), `banditmerc_outfit` (500); `ammo_9x18_pmm` |
| **Ecologist** | `helm_resp` (50) | `wpn_k98` (750), `wpn_mp5` (500), `wpn_vz61` (375), `wpn_bm16` (550, diff ≤2); `novice_outfit_camo` (50), `ghillie_outfit` (650); `stimpack_scientic` |
| **UNISG** | — | `wpn_udp9` (650) — a single smg line in `mod_new_game_loadouts_udp9.ltx` |

(For the ammo-doctrine side of faction identity — WP vs NATO vs ANY — see
`references/weapons.md` §3 and `references/ballistics-damage.md` §3.)

## 6. Faction identity in the world

| Faction | Where you meet them | What they are for |
|---|---|---|
| **Loners** | Cordon, Bar, everywhere | default faction; the loosest network of the Zone |
| **Bandits** | Garbage, Dark Valley, Truck Cemetery | hostile to Loners; allied to Renegades |
| **Duty** | Bar (Rostok) | anti-mutant/anti-Monolith dogma; wars with Freedom |
| **Freedom** | Army Warehouses, Dead City | anarchist; wars with Duty |
| **Ecologists** | Yantar (Sakharov), Jupiter (Hermann) | artefact/melting/technology hub — the melter, T3+ recipe books, psy helmets |
| **Military** | Agroprom, Truck Cemetery, Cordon checkpoint | the "Operation Monolith Retribution" storyline; hostile to Loners |
| **Mercenaries** | Dead City | neutral to Bandits, Freedom, Clear Sky, UNISG, Ecologists; hostile to Loners/Duty/Military |
| **Monolith** | Pripyat, Radar, north | a bloc with Sin and zombies |
| **Sin** | Red Forest, Jupiter, Pripyat | Monolith-aligned; the pack makes them friendly with mutants |
| **Clear Sky** | Swamps | *Last Dawn* storyline; in GAMMA they are pushed toward the north rather than the old swamp campaign |
| **UNISG** | Cordon (`dasc_sawwill`) | single-war-all campaign; *Mission Afterglow* |
| **Renegades** | Swamps, Cordon | Bandit-aligned low-tier enemy |
| **Zombified** | Zaton, Jupiter, Pripyat | playable "zombie" start with its own loadout inheritance (`[zombied_loadout]:shared,stalker_loadout`) |

**Faction patches** are tradable identity items; the pack's own price file lists them
verbatim: `csky_patch 650`, `freedom_patch 850`, `stalker_patch 700`, `ecolog_patch 550`,
`bandit_patch 550`, `dolg_patch 850`, `monolith_patch 1000`, `army_patch 850`,
`killer_patch 850`, `isg_patch 1500` (dearest), `greh_patch 1300`, `renegade_patch 800`.
Bandit and Renegade patches sit at `1.5,1.5` in the generic buy table — i.e. traders pay a
premium for them.

The pack's outfit table shows where each faction's production pipeline lands: **Duty 25
outfit entries, Mercenary 23, Free Stalkers 18, Freedom 14, Clear Sky 13, Bandit 12, UNISG 11,
Monolith 11, Ecologist 9, Military 8, Sin 5, Renegade 3** (plus 9 "Unknown"), out of 161
outfits. If you want faction-specific armour variety, Duty and the Mercenaries are the deep
trees.

## 7. Storyline availability (faction-gated)

Verbatim from the manual (`article_gamma_story_text`), cross-referenced with §2:

| Storyline | Available to |
|---|---|
| **Lost to the Zone** | Loner, Clear Sky, Duty, Freedom, Mercenary, Ecologist (from your faction leader at your starting base) |
| **Mission Afterglow** | UNISG only (unlock with `isg` at character creation) |
| **Artefact Hunters** | "Ecologist Allies: Loner, Clear Sky, Duty, Freedom, Military, Mercenary, Ecologist" — i.e. everyone the Ecologists are not at war with |
| **Last Dawn** | "Clear Sky Allies: Loner, Clear Sky, Duty, Freedom, Mercenary, Ecologist" |
| **Operation Monolith Retribution** | "Military Allies: Military, Ecologist" |
| **Dr.X Questline** | all factions, "not really story oriented" |

The correspondence with §2 is exact: **"Ecologist Allies" = the neutral-or-better set in the
Ecologists' row**, which is why Duty, Freedom, Military, Mercenaries and Clear Sky all appear
even though several of them hate each other.

## 8. Quick answers

| Question | Answer |
|---|---|
| Which factions can I play? | Loner, Bandit, Duty, Freedom, Ecologist, Military, Mercenary, Clear Sky, Monolith, Sin, UNISG, Renegade, Zombified — 13 starting-location sets in `new_game_start_locations.ltx`. |
| How do I play UNISG? | Type `isg` during character creation (manual), then pick the `dasc_sawwill` (Cordon) start. |
| Who is at war with whom? | Duty ↔ Freedom; UNISG vs everybody; Monolith + Sin + Zombies as a bloc; Bandits + Renegades allied; Military + `army_npc` allied at 2000. Full table above. |
| Why do Duty members shoot me? | `attitude = personal_goodwill + community_goodwill + community_to_community + reputation_goodwill + rank_goodwill` — your faction's relations count against you. |
| How do I unlock better trader stock? | Faction goodwill: 500 → supply 2, 1 000 → 3, 1 500 → 4, 2 000 → 5 (or pay via `heavy_pockets_functor`). |
| Which traders are goodwill-gated? | Loner, Bandit, Duty, Ecologist, Freedom, Military, Mercenary, Clear Sky, Monolith, UNISG, Sin trader files all carry `actor_goodwill_ge` gates. |
| What are the rank names? | novice, trainee, experienced, professional, veteran, expert, master, legend (thresholds 3999/5999/9999/15999/23999/34999/49999). |
| What are the reputation names? | terrible, really_bad, very_bad, bad, neutral, good, very_good, really_good, excellent. |
| Where do I start as Monolith/Sin? | Pripyat, Radar, Red Forest, Generators — GAMMA deliberately starts hostile factions deep in the north. |
| How much do faction patches cost? | 550 (bandit/ecolog) up to 1 500 (UNISG); see the price list in §6. |
| Does GAMMA change faction relations? | Yes — relations, spawn tables and alliances are patched (e.g. Sin and Mutants are Allies); the pack also ships relation-tuning addons. |

Cross-references: who sells what and how goodwill converts to stock →
`references/trading-economy.md`; faction ammunition doctrine and weapon types →
`references/weapons.md`; faction armour trees → `references/armor-outfits.md`; storyline starts
and north gating → `references/quests-storylines.md`; faction-populated maps and spawn weight
changes → `references/mutants.md`; the difficulty presets that multiply the goodwill you earn
(`goodwill = 1.4 / 1.2 / 1.0` across Tourist / Scavenger / Survivalist) and therefore how fast
you reach the 500 / 1 000 / 1 500 / 2 000 supply thresholds → `references/keybinds-settings.md`.
