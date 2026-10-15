# Trading and economy — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual articles **Traders Progression**
(`article_gamma_traders_text`), **Money** and **How To Progress**; the Economy addon's
`items/trade/` tree — `presets/trade_presets.ltx` (buy/sell classifier groups),
`presets/trade_discounts.ltx` (referenced by every trader through a `#include`, but **not
present in the repository snapshot**, so the `discount_*` tables cannot be read here),
`presets/gamma_wp_preset.ltx` and
`presets/gamma_nato_preset.ltx` (`supply_1…5` ladders), the individual `trade_*.ltx` files
(Sidorovich, Barman, mechanics, Sakharov, Hermann, faction traders, flea-market/night variants)
— plus its price patches `mod_system_zzzzzzzzzzzzzzzzzzz_GAMMA_items_price.ltx`,
`items/settings/part_prices.ltx`, `mod_system_mutant_parts_price_gamma.ltx` and
`mod_system_weapons_gamma_attachments_price.ltx`; the economy presets in
`G.A.M.M.A. Difficulty Presets Rebalance/…/difficulty.ltx`; the toolkit-by-map table
`toolkits_chance.xlsx`; and `Patchnotes.md` 0.9.5 (**Economy**, **Crafting**). Snapshot:
GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. The two rules that define GAMMA's economy

> "Traders will mostly sell **supplies and some accessories**. **You won't be able to buy or
> sell armors and guns at traders.** You can increase traders supply level by doing tasks for
> the trader's faction. **The goodwill thresholds are: 500, 1000, 1500 and 2000 goodwill.**
> This is a reliable way to secure a steady income of quality ammunitions." — manual

> "Money is of the essence, especially in the beginning. There are fast ways to make cash,
> namely **doing tasks without picking fights**, **selling mutant parts** or **selling artefacts
> to the ecologists**… In the mid game, you'll inevitably get loads of money. This can be used
> to **upgrade your equipment**, or **invest in expensive AP ammo**… **Maintaining an
> exoskeleton armor will also be a money sink since you often need to buy expensive exo
> batteries.**" — manual

Everything else on this page follows from those two paragraphs.

## 2. Who trades what

| Trader file | Type | Notable stock / behaviour |
|---|---|---|
| `trade_stalker_sidorovich.ltx` | Loner | the classic Cordon start; `buy_item_condition_factor = 0.05`, `buy_item_exponent = 2.25`, `sell_item_exponent = 0.75` |
| `trade_generic_barman.ltx` | Loner (Bar) | the bar economy — food, drink, supplies |
| `trade_generic_mechanic.ltx` | Mechanic | `buy_item_condition_factor = 0.01`, `buy_item_exponent = 1.75`; **the only sale route for tools, and the seller of upgrade recipes**; supplies gated on `toolkit_task_done(1..3)` rather than goodwill |
| `trade_generic_medic.ltx` | Medic | medical stock |
| `trade_ecolog_sakharov.ltx` | Ecologist | `[trade_generic_buy]:scientist,artefacts_h,furnitures_low`; sells `trading_computer`, `recipe_basic_4` at supply 1, detectors, medkits; **`supplies_5` adds `recipe_exo_1/2/3`** |
| `trade_ecolog_hermann.ltx` | Ecologist | second artefact/tech hub (Jupiter) |
| `trade_bandit.ltx`, `trade_bandit_basic.ltx` | Bandit | `[supplies_1]:common_stock,supply_1_wp` |
| `trade_duty.ltx`, `trade_freedom.ltx`, `trade_freedom_ashot.ltx` | Duty/Freedom | WP and NATO flavours respectively |
| `trade_csky_spore.ltx` | Clear Sky | `[supplies_1]:common_stock,supply_1_nato` |
| `trade_military.ltx`, `trade_military_esc.ltx` | Military | |
| `trade_mercenary.ltx`, `_basic`, `_meeker` | Mercenary | |
| `trade_monolith.ltx`, `_basic` | Monolith | |
| `trade_isg.ltx`, `_light`, `_mission` | UNISG | |
| `trade_renegade.ltx` | Renegade | |
| `trade_stalker_owl/loris/nimble/flea_market/flea_market_night/butcher` | Specialists | `flea_market` has a **night** variant — the market changes after dark |
| `trade_ithaca/*.ltx` | Overrides | a parallel set of trader files (one per faction) |
| `trade_melee_rework/*.ltx` | Overrides | melee-focused rework set |

**Classifiers** come from `trade_presets.ltx`, which is a big item dictionary grouped by
category: `[pistols]`, `[rifles]`, `[ammo]`, `[ammo_bad]`, `[ammo_damaged]`, `[w_addons]`,
`[explosives]`, `[melee]`, `[headgear]`, `[outfits]`, `[outfits_ecolog]`, `[backpacks]`,
`[artefacts]`, `[drugs]`, `[cigs]`, `[drinks]`, `[food]`, `[fuels]`, `[misc]`, `[devices]`,
`[mutant_parts]`, `[trash]`, `[tools]`, `[repair_kits]`, `[upgrade_items]`, `[unused]`,
`[parts]`, `[camping]`, `[money]`, `[furnitures_low]`, `[toolkits_h]`, `[artefacts_h]`,
`[common_stock]`, and composites
`[weapons]:pistols,rifles`, `[weapons_else]:ammo,ammo_bad,ammo_damaged,w_addons,explosives,melee,backpacks`,
`[outfits_all]:headgear,outfits,outfits_ecolog`,
`[consumables]:drugs,cigs,drinks,food`,
`[cooking_stuff]:camping,fuels`, and finally
`[none]:unused,money,parts,weapons,weapons_else,outfits_all,consumables,artefacts,cooking_stuff,misc,devices,mutant_parts,trash,tools,repair_kits,upgrade_items`
and `[supplier]:unused,money,parts,ammo_bad,ammo_damaged,trash,weapons,outfits_all`.
That `[none]` line is the mechanical expression of "traders don't sell guns and armour".

The remaining composites are the **per-trader-type whitelists** a `[trader]` block inherits
through `buy_condition` / `sell_condition` — verbatim from the file:

```
[merchant]:unused,money,parts,ammo_damaged,trash,weapons,outfits_all
[trasher] :unused,money,parts,weapons,outfits_all
[barman]  :unused,money,parts,weapons,weapons_else,outfits_all,drugs,artefacts,cooking_stuff,misc,devices,trash,tools,repair_kits,upgrade_items
[medic]   :unused,money,parts,weapons,weapons_else,outfits_all,cigs,drinks,food,artefacts,cooking_stuff,misc,devices,mutant_parts,trash,tools,repair_kits,upgrade_items
[scientist]:unused,money,parts,headgear,outfits,backpacks,cigs,drinks,food,cooking_stuff,misc,trash,tools,repair_kits,weapons,weapons_else,outfits_all
[mechanic]:unused,money,weapons,weapons_else,outfits_all,consumables,artefacts,misc,trash,devices,mutant_parts
```

Note what each one *excludes*: a mechanic does **not** buy or sell food and drink, a barman
does **not** touch devices or mutant parts, and every one of them keeps `weapons` and
`outfits_all` in its `[unused]`-style exclusion set — i.e. guns and armour are inedible to the
whole trader network, in both directions. The file also carries two comments worth quoting:
`[common_stock] ;-- items all traders will sell` and
`[unused] ;-- technical items should be listed here so traders don't sell/buy them`.

### 2.1 Which traders are actually WP and which are NATO (from the files, not the manual)

The manual's bloc list and the `good_weapons.txt` faction table do not agree with each other,
so the shipped trader files are the tiebreaker for *purchasing*. Grep-verified result:

| Bloc | Traders whose supply ladders use it |
|---|---|
| **WP** (`supply_*_wp`) | Bandit (`trade_bandit`, `_basic`), Duty, Military (`trade_military`, `_esc`), Renegade, all Loner shopkeepers (`trade_stalker_sidorovich/loris/owl/basic`) |
| **NATO** (`supply_*_nato`) | Clear Sky (`trade_csky_spore`), Freedom (`trade_freedom`, `_ashot`), Mercenary (`trade_mercenary`, `_basic`, `_meeker`), UNISG/ISG (`trade_isg`, `_light`) |
| **Both** | Monolith (`trade_monolith`, `_basic`) and Greh (`trade_greh`) — a double inventory, consistent with the manual's "Monolith NPCs have about 50 % chance to have a NATO or WP gun" |
| **Neither** | Ecologists (`trade_ecolog_sakharov/_hermann` — they sell their own science stock: detectors, the Melter, `recipe_exo_*`), the generic Barman/Medic/Mechanic service traders, and the specialist Loner files (`trade_stalker_nimble`, `_butcher`, `_flea_market`, `_flea_market_night`, `trade_isg_mission`) |

Compare with the in-game manual (*Traders Progression*), which puts **Renegades and Monolith in
WP** and **UNISG in NATO**, and with `good_weapons.txt`, whose FACTIONS block says `ecolog`,
`monolith`, `renagades` and `ISG` are `ANY` (and `sin` is `WP`). The three sources disagree on
the ANY/NATO/WP edge cases; when the question is "**can I buy this calibre here?**", follow the
trader files above — that is what the game evaluates.

## 3. Supply levels (the progression dial)

Every trader's `[trader]` block reads `buy_supplies = {…}` with conditions evaluated in order;
the first match wins. The canonical shape (Sidorovich, verbatim):

```
buy_supplies = {=actor_goodwill_ge(stalker:2000)} supplies_5, {=heavy_pockets_functor()} supplies_5,
               {=actor_goodwill_ge(stalker:1500)} supplies_4, {=actor_goodwill_ge(stalker:1000)} supplies_3,
               {=actor_goodwill_ge(stalker:500)}  supplies_2, supplies_1
```

So the ladder is:

| Goodwill with that faction | Supply level | What it means (WP example) |
|---|---|---|
| 0 (default) | `supplies_1` | ammunition basics in pistol calibres, a knife, starter accessories |
| **500** | `supplies_2` | optics/sights, `af_kevlar`, kevlar/upgrade kits, intermediate rifle calibres |
| **1 000** | `supplies_3` | high-end glass (PSO/1P29/SUSAT class) and gun kits |
| **1 500** | `supplies_4` | thermal/RMR-class sights, **grenade launchers**, heavy suppressors |
| **2 000** | `supplies_5` | `wpn_knife6`, **`recipe_exo_1/2/3`** (exoskeleton PSU recipes), `gauss_sight` |
| — | `heavy_pockets_functor()` | an alternative route to level 5: have deep pockets rather than friends |

Mechanics use a **different** gate — `{=toolkit_task_done(1)} supplies_2`, `(2) supplies_3`,
`(3) supplies_4` — i.e. the mechanic's stock improves as you finish his toolkit tasks. Medics
use a third one: `buy_supplies = {=drugkit_task_done()} supplies_2, supplies_1`, so the drug
stock you can buy is literally a reward for his drug-toolkit task. The two service traders are
also the ones who ignore faction standing entirely — no goodwill, no supplies.

What the mechanic's `[supplies_2]` (basic tools delivered) actually adds is worth reading in
full, because it is the game's only shop-shelf for upgrades:

```
[supplies_2]:supplies_1        ;-- basic tools delivered
trading_computer    = 1, 1
upgr_o_1_physical   = 1,0.30     upgr_o_1_magical = 1,0.30   upgr_o_1_utility = 1,0.30
upgr_o_2_physical   = 1,0.15     …                            …
upgr_o_3_physical   = 1,0.05     …
upgr_w_1_internal   = 1,0.35     upgr_w_1_external = 1,0.35  upgr_w_1_optical = 1,0.35
upgr_w_2_*          = 1,0.20     upgr_w_3_*        = 1,0.05
;-- Grok's Craft and Repair Overhaul
grooming            = 4, 1
steel_wool          = 5, 1
```

(Read `= 1, 0.30` as *one item at a 30 % chance per restock*.) So **armour and weapon upgrade
kits come from the mechanic once you have handed in toolkit task 1**, and the deeper tiers get
rarer, not more plentiful — the same shape as the artefact recipe economy. His buy/sell groups
are `[trade_generic_buy]:craft_repair_overhaul,mechanic,toolkits_h` and
`[trade_generic_sell]:mechanic, toolkits_h`.

The manual's summary: "Some traders sell very specific items, like **Prof. Sakharov and
Hermann sell the Artefacts Melter**… They also sell **exoskeletons' PSU recipes at Supplies
Lv 5**."

## 4. WP vs NATO: trader doctrine

> "Traders are either of the WP (Warsaw Pact) or NATO type. This will influence the kind of
> supplies they sell (ammo and attachments mostly). **NATO factions: Mercenaries, Clear Sky,
> Freedom, UNISG. WP factions: Military, Loner, Duty, Bandits, Renegades, Monolith.** This
> also influences NPCs loadouts of factions, ie: **Monolith NPCs have about 50 % chance to have
> a NATO or WP gun.**" — manual

The two preset files mirror each other section by section
(`supply_1_nato` … `supply_5_nato` vs `supply_1_wp` … `supply_5_wp`), so a faction's trader
sells *its* calibres and *its* optics. Practically:

- **You cannot buy your way into the other bloc's ammo.** A Loner who finds a NATO rifle must
  loot ammo, buy from a Mercenary/Clear Sky/Freedom/UNISG trader, or **craft it** with the
  gunsmith toolkit (see `references/crafting-repairs.md`).
- **The `good_weapons.txt` doctrine table** gives the per-gun tag (WP / NATO / ANY) the pack
  actually enforces — reproduced in `references/weapons.md` §3.

## 5. Prices: what things actually cost

### Personal gear prices (verbatim from `mod_system_zzzzzzzzzzzzzzzzzzz_GAMMA_items_price.ltx`)

| Item | Cost | Item | Cost |
|---|---|---|---|
| `wpn_knife` | 1 000 | `device_glowstick` (each colour) | 400 |
| `headlamp` | 1 200 | `radio` | 1 200 |
| `flashlight_broken` | 1 500 | `broken_detector` | 2 000 |
| `itm_drugkit` (Medical toolkit) | 3 500 | `itm_ammokit` (Gunsmith toolkit) | 3 850 |
| `device_light_altar` | 5 360 | `cutlery` | 810 |
| `cards` | 1 100 | `porn` / `porn2` | 750 / 950 |
| `guitar_a` | 5 000 | `mod9` | 6 000 |
| `pl15_scolaz` | 12 000 | `cleaning_kit_r7` | 10 500 |
| `heavy_repair_kit` | 45 000 | **`exo_repair_kit`** | **150 000** |
| `recipe_exo_1/2/3` | **68 500 each** | `itm_artefactskit` (Melter) | 15 000 |

### Faction patches

`csky 650`, `ecolog 550`, `bandit 550`, `stalker 700`, `renegade 800`, `freedom 850`,
`dolg 850`, `army 850`, `killer 850`, `monolith 1 000`, `greh 1 300`, `isg 1 500`.

### Parts, kits and attachments

- **Gun parts** (`part_prices.ltx`): barrels **2 625–8 250**, trigger components **3 900–7 125**,
  bolt carriers **3 750–6 750**, bolts **4 875–7 125**. (See `references/weapons.md`.)
- **Repair kits**: `x_cleaning_kit_p` ≈ 2 390 RU of materials vs 3 941 RU trader value, up to
  `x_toolkit_r7` ≈ **57 706 RU of materials vs 75 000 RU value** (the pack's own annotations in
  `craft.ltx`).
- **Attachments**: `mod_system_weapons_gamma_attachments_price.ltx` prices scopes, suppressors and
  launchers; the supply tables also cap availability by goodwill.

### Mutants and artefacts

- **Mutant parts**: `mutant_part_heart_chimera = 5 250`, `mutant_part_lurker_meat = 608`
  (and everything between). Parts are loot-table drops — see `references/mutants.md`.
- **Artefacts**: the Melter (15 000 RU) plus fusion costs (7 / 12 / 23 mS by tier) and the
  recipe books (T2 4 000, T3 12 000→ higher in 0.9.5, special 36 000 → **99 000** in 0.9.5).
  See `references/artifacts.md`.

### The traders' spread

Every trader sets a **buy condition factor** and exponents that decide what they pay for used
gear: Sidorovich pays `0.05 ×` value for items at low condition, a mechanic pays `0.01 ×`;
`buy_item_exponent` (2.25 for general traders, 1.75 for mechanics) further punishes worn items,
and `sell_item_exponent 0.75` discounts what they charge you. **Conclusion: a broken gun is
nearly worthless to a trader** — disassemble it instead, or repair it first. In the generic sell
table, standard medical stock sits at `0.83,0.83` (i.e. traders buy and sell the same class of
item on a fixed margin).

## 6. The economy presets (what difficulty does to money)

From `difficulty.ltx`, verbatim multiplier sets (`[econ_1]` = Tourist, `[econ_2]` =
Scavenger, `[econ_3]` = Survivalist):

| Value | econ_1 (Tourist) | econ_2 (Scavenger) | econ_3 (Survivalist) | Meaning (file's own comment) |
|---|---|---|---|---|
| `goodwill` | **1.4** | 1.2 | 1.0 | goodwill earned from quests |
| `rewards` | 1.25 | 1.1 | 0.9 | money earned from quests |
| `repair` | 1.0 | 1.3 | 1.7 | cost of **repair services** by mechanics |
| `upgrade` | 1.3 | 1.6 | 2.0 | cost of **upgrading** by mechanics |
| `buy` | 1.25 | 1.0 | 0.75 | prices of items sold to other traders/stalkers |
| `sell` | 0.75 | 1.0 | 1.25 | prices of items bought from traders/stalkers |
| `loots` | 1.5 | 1.0 | 1.0 | chance of finding items on corpses |
| `money_loots` | 1.0 | 0.75 | 0.5 | money looted from corpses |
| `stash_chance` | **0.4** | 0.3 | **0.2** | chance of discovering a stash per corpse |
| `weapon_degradation` | 0.5 | 0.75 | 1.0 | how fast weapons degrade |
| `battery_consumption` | 0.5 | 0.75 | 1.0 | device power consumption |
| `random_items` | 0.5 | 0.4 | 0.3 | fraction of dynamic items spawned |
| `scope_chance` | 0.10 | 0.05 | 0.02 | chance a stalker's weapon has a scope |
| `arty_chance` | 0.30 | 0.25 | 0.20 | artefact spawn chance |
| `restock` | **24** | **48** | **48** | hours for a trader to restock |
| `limited_bolts` | true | true | true | bolts are a resource in every preset |
| `outfit_drops` | 2 (progressive) | 2 | 2 | armour drops depend on player rank |

Note the counter-intuitive pair: Tourist difficulty gives **more** sell income for *you*
(`buy 1.25` = what traders pay for your goods) and **cheaper restock timers**, while
Survivalist flips it (`buy 0.75`, `sell 1.25`). Also note `repair` and `upgrade` are the
multipliers that the manual's "repairs cost money" advice is measured against.

## 7. Money sinks, in order of size

| Sink | Cost (verified) |
|---|---|
| Exoskeleton upkeep — **exo batteries** + exo maintenance | `exo_repair_kit` 150 000 RU (manual: "you often need to buy expensive exo batteries") |
| Heavy armour maintenance | `heavy_repair_kit` 45 000 RU |
| Exoskeleton PSU recipes | `recipe_exo_1/2/3` at 68 500 each, sold by Sakharov/Hermann at supply 5 |
| Sniper-tier repair toolkits | `x_toolkit_r7` ≈ 57 706 RU of materials |
| Detectors | Melter 15 000; `detector_grizzly` 27 560 (see `references/artifacts.md`) |
| AP ammunition | the manual's explicit mid-game advice: "invest in expensive AP ammo" |
| Repair services | multiplied by `repair`/`upgrade` per economy preset |
| Healing items | "You'll find yourself often spending money on healing items and that's intended" |

## 8. Money sources, in order of reliability

1. **Tasks that do not require fighting** — manual's first recommendation; rewards are also
   **scaled by the target map** since 0.9.5 (see `references/quests-storylines.md`).
2. **Mutant parts** — a full loot table per mutant, with chimera hearts at 5 250 RU.
3. **Artefacts to the Ecologists** — manual's third recommendation; the Ecologists also buy
   `artefacts_h` (high-tier) selectively.
4. **Corpse money** — `misc_high` and general loot pools drop `roubles` (e.g. `roubles, 8, 0.08`
   in the high pool), scaled by `money_loots`.
5. **Patch trading** — bandit/renegade patches are bought at `1.5,1.5`.
6. **Junk that is not junk** — disassemble rather than sell (see §9).
7. **Black Market (optional MCM toggle)** — allows buying gear; the pack's own folder name
   calls this out: "G.A.M.M.A. Economy (don't disable, turn on Black Market to buy gear)".

## 9. Selling vs disassembling (the actual optimisation)

| Item you looted | Sell it | Disassemble it |
|---|---|---|
| Worn weapon | `buy_item_condition_factor` 0.01–0.05 → basically nothing | **parts**: barrels 2 625–8 250, bolts 4 875–7 125 (see `references/crafting-repairs.md`) |
| Ammunition you cannot use | small | **very light** — "disassembled ammo parts are very lightweight… Be sure to disassemble all unnecessary ammo" (manual) |
| Mutant corpse | parts + pelt | parts feed crafting (fabrics, tech items) |
| Meds you over-stocked | 0.83 margin | — |
| Junk with the hammer-and-pincer icon | sells for pennies | **do not sell** — it is a crafting input |

The 0.9.5 patch notes pulled several levers here: "**Increased cost of glowsticks and
flashlights**… Fixed rubbish to cables recipes", "**Metal mags give much more paper**",
"**Glowsticks and tarpaulin give plastic**… Increased wood parts from items disassembly",
"**Less plastic needed for medkits**, no plastic for stimpaks, syringe etc", and "**Increased
cost and crafting cost of Type D cleaning kit and repair kit**".

## 10. Quick answers

| Question | Answer |
|---|---|
| Can I buy guns or armour? | No — traders sell supplies and accessories only (unless the player enables the **Black Market** MCM option). |
| How do I get better trader stock? | Faction goodwill 500 / 1 000 / 1 500 / 2 000 → supply levels 2 / 3 / 4 / 5; mechanics instead gate on `toolkit_task_done`; or `heavy_pockets_functor` for level 5. |
| Where do I buy the Melter? | Sakharov or Hermann (Ecologists) for 15 000 RU. |
| Where do I buy exo PSU recipes? | Sakharov/Hermann at supply level 5 (2 000 ecolog goodwill), 68 500 RU each. |
| Do all traders sell the same ammo? | No — WP traders (Military, Loner, Duty, Bandits, Renegades, Monolith) vs NATO traders (Mercenaries, Clear Sky, Freedom, UNISG). |
| Why is my looted rifle worth nothing? | `buy_item_condition_factor` 0.01 (mechanic) / 0.05 (general) times the value, then `buy_item_exponent` 1.75–2.25 applied — worn gear is near-worthless by design. |
| Fastest money? | Non-combat tasks (map-scaled rewards), mutant parts, artefacts to Ecologists. |
| Biggest money sink? | Exoskeleton maintenance: exo batteries, a 150 000 RU exo repair kit, and 68 500 RU PSU recipes. |
| Does trader stock refresh? | Yes — `restock` is 24 h on Tourist and 48 h on Scavenger/Survivalist. |
| How many bolts do I get? | `limited_bolts = true` on every preset — bolts are stock, buy `bolts_pack`. |
| Where is the night market? | `trade_stalker_flea_market.ltx` and `trade_stalker_flea_market_night.ltx` — the flea market has a night inventory. |

Cross-references: repair-kit costs and crafting routes → `references/crafting-repairs.md`;
goodwill, factions and trader-gating → `references/factions.md`; ammo types and their prices →
`references/weapons.md` and `references/ballistics-damage.md`; artefact sale routes →
`references/artifacts.md`; task rewards and map scaling → `references/quests-storylines.md`;
economy multipliers per preset → `references/keybinds-settings.md`.
