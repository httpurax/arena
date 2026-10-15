# Crafting, repairs and toolkits — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual articles **Crafting** (`article_gamma_crafting_text`),
**Cooking** (`article_gamma_cooking_text`), **Repairs for Guns** (`article_gamma_repgun_text`)
and **Repairs for Armor** (`article_gamma_reparm_text`), plus the **Inventory** article
(`article_gamma_inventory_text`, which carries the disassembly rules); the **NPE weapon and
armour repair tutorials**; GAMMA's crafting database `items/settings/craft.ltx` (with its annotated recipe
book table) and `mod_system_grok_recipes.ltx`; the Economy addon's
`mod_system_GAMMA_repair_kits_uses.ltx` and `mod_system_GAMMA_items_repair_quantity.ltx`; the
Type A–D kit descriptions in
`G.A.M.M.A. Repair Kit Renaming/gamedata/configs/text/eng/st_items_repair_new.xml`; the
pack's toolkit-by-map table `toolkits_chance.xlsx`; and `Patchnotes.md` 0.9.5 (Crafting and
Economy sections). Snapshot: GAMMA 0.9.5 @
`ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

Crafting is the spine of GAMMA's progression. The manual's *How To Progress* says it in
order: do tasks → collect stash coordinates → **use the toolkits to craft repair kits for the
guns and armour you found** → gear up → go north.

---

## 1. The six toolkits

Verbatim from the manual: "There are **6 types of toolkits: Basic, Advanced, Expert, Medical,
Gunsmith and the Artefact Melter.**" 0.9.5 made two of them craftable ("Craftable Medic and
Ammo toolkits + increased base items recipes costs").

| Toolkit | What it unlocks (players' understanding, from the recipes) | How to get it |
|---|---|---|
| **Basic** | the entry tier: basic weapon/armour repair kits, cleaning kits, basic equipment, basic electronics, basic upgrades, most cooking | marked stashes on the southern maps |
| **Advanced** | advanced equipment/electronics/upgrades, the **Grizzly detector**, `af_*` tech-item upgrades, medium/heavy repair-kit lines | mid maps |
| **Expert** | expert-tier repairs and upgrades; expert crafting | **Red Forest and further north** (manual: "Expert toolkits can only be found in the Red Forest or further North") |
| **Medical** (`itm_drugkit`) | medical crafting | craftable since 0.9.5: `itm_basickit ×2 + medkit_scientic ×3 + rebirth ×1 + drug_anabiotic ×1` |
| **Gunsmith / ammo** (`itm_ammokit`) | ammo crafting, gunsmith work | craftable since 0.9.5: `itm_basickit ×2 + powder_3 ×6 + bullet_r7_ap ×6 + prt_i_copper ×8` |
| **Artefact Melter** (`itm_artefactskit`) | fuse/empower/craft artefacts | bought from **Sakharov or Hermann** (Ecologists); also rarely in white stashes (NPE) |

There is also an intermediate container the recipes use: `itm_advancedkit` is crafted from
`itm_basickit ×5 + prt_i_scrap ×5` (i.e. you climb the toolkit ladder by crafting, not only by
looting).

### Using a toolkit

> "**Right click any toolkit to open a portable workbench** to start crafting and repairing or
> upgrading your gear." — manual

That is the whole interface: right-click a toolkit → portable workbench. "Crafting tools
don't weight much and you can right click them to 'open workbench' and start crafting
on-the-go" (inventory article). The pack even ships an optional **"G.A.M.M.A. Crafting Tools
Weight Reduce"** addon and **"Serious Workshop optimization"** for people who craft a lot.

### Where toolkits actually spawn

`toolkits_chance.xlsx` is the pack's own table — its header says: **"Chances to get tools in
RARE STASHES (white ones have 0 %)"**. Per map it lists the tool tiers present and the
computed chance columns (Basic kits / Advanced / Expert / Drug / Ammo). Selected rows
verbatim:

| Map | Basic | Advanced | Expert | Drug | Ammo |
|---|---|---|---|---|---|
| `y04_pole` | 25 % | 0 | 0 | 37.5 % | 37.5 % |
| `k00_marsh` | 40 % | 0 | 0 | 30 % | 30 % |
| `l01_escape` | 40 % | 0 | 0 | 30 % | 30 % |
| `l02_garbage` | 42.6 % | 4.5 % | 0 | 26.4 % | 26.4 % |
| `k02_trucks_cemetery` | 26.6 % | 50.6 % | 0 | 11.4 % | 11.4 % |
| `l06_rostok` | 40.3 % | 24.7 % | 0 | 17.5 % | 17.5 % |
| `l07_military` | 27.3 % | 50.9 % | 0 | 10.9 % | 10.9 % |
| `l08_yantar` | 33.9 % | 37.2 % | 0 | 14.5 % | 14.5 % |
| `l10_limansk` | 17.0 % | 56.8 % | 12.5 % | 6.8 % | 6.8 % |
| `l10_red_forest` | 0 | **87.5 %** | **12.5 %** | 0 | 0 |
| `l10_radar` | 3.8 % | 68.2 % | **25 %** | 1.5 % | 1.5 % |
| `zaton` / `jupiter` | 18.2 % | 47.3 % | 20 % | 7.3 % | 7.3 % |
| `pripyat` | 5.7 % | 39.8 % | **50 %** | 2.3 % | 2.3 % |
| `l11_hospital` / `l11_pripyat` | 0 | 50 % | **50 %** | 0 | 0 |
| `l12_stancia` / `l12_stancia_2` | 0 | 37.5 % | **62.5 %** | 0 | 0 |
| `l13_generators` | 0 | 30 % | **70 %** | 0 | 0 |

**Reading:** basic kits dominate the south; advanced kits become the common result from the
Garbage/Trucks Cemetery/Rostok/Military/Yantar band; **expert kits only show up from Limansk,
Red Forest, Radar, Zaton/Jupiter, Pripyat, the Hospital and the northern endgame maps**, at
odds that climb from 12.5 % to 70 %. This matches the manual's sentence and the NPE tutorial's
advice ("The more to the north of the Zone [you go, the better the stashes]").

**Restating the critical rule** (manual, *Stashes*): "**Unmarked stashes are almost always
empty. Stashes must be marked to contain anything of value, especially toolkits.**" Stash
content is tied to the map, and northern stashes are better.

## 2. The crafting menu structure

`craft.ltx` numbers its menus (the file's own section keys are `[1]`, `[2]`, `[3]`, …) with
titles like `st_ui_craft_device` (devices), `st_ui_craft_equipment` (equipment),
`st_ui_craft_repair` (repair). Recipes are written as
`x_item = count, recipe_book, ingredient, amount, ingredient, amount, ingredient, amount` —
i.e. **each recipe declares which recipe book unlocks it** (`recipe_basic_0` /
`recipe_advanced_0` / `recipe_expert_0` are the always-available defaults).

The annotated recipe-book table in the file's header comments:

| Recipe book | Unlocks | Price | Sold by |
|---|---|---|---|
| `recipe_basic_1` | Basic equipment | 2 000 RU | Mechanics |
| `recipe_advanced_1` | Advanced equipment | 6 000 RU | Mechanics |
| `recipe_expert_1` | Expert equipment | 18 000 RU | Mechanics |
| `recipe_basic_2` | Basic electronics (detectors, NVGs, containers…) | 4 000 RU | Mechanics |
| `recipe_advanced_2` | Advanced electronics | 12 000 RU | Mechanics |
| `recipe_expert_2` | Expert electronics | 36 000 RU | Mechanics |
| `recipe_basic_3` | Basic upgrades | 1 000 RU | Mechanics |
| `recipe_advanced_3` | Advanced upgrades | 3 000 RU | Mechanics |
| `recipe_expert_3` | Expert upgrades | 9 000 RU | Mechanics |
| `recipe_basic_4` | Tier 2 artefacts | 4 000 RU | Ecologists |
| `recipe_advanced_4` | Tier 3 artefacts | 12 000 RU | Ecologists |
| `recipe_expert_4` | Special artefacts | 36 000 RU (0.9.5: raised to 99 000) | Ecologists |

`mod_system_grok_recipes.ltx` carries the actually-loaded costs (basic 1 000–6 000, advanced
3 000–36 000, expert 7 000–48 000, plus `recipe_ammo_4` at 65 000) — read the file in your own
install for the current numbers.

## 3. Weapon repairs — the full decision tree

| Situation | Tool needed | Action | Cost |
|---|---|---|---|
| Part ≥ 60 % | **Cleaning kit** of the gun's Type (A/B/C/D) | right-click gun → *maintenance* → *clean part* → 100 %; or double-click the kit in inventory and pick the part | kit consumption (kits are cheap; only Type A is at mechanics from the start) |
| Part < 60 % | **Repair kit** of the gun's Type | right-click gun → *maintenance* → *repair part* → 100 % | **one repair-kit use** (kits ship with `max_uses = 3`) |
| Any part, any condition, **except the barrel** | nothing | drag and drop a looted part of the same type onto the gun | free, but dirties the gun |
| Barrel, any condition | Repair kit's **maintain parts** | right-click gun → *maintain parts* → automatically replaces parts with 100 % ones | one use; can replace barrels |
| Cleanliness (the gun itself) | cleaning equipment, or a mechanic | clean the gun so parts stop degrading while you shoot | small fee / kit use |

If you loot a "destroyed" gun, this order applies: **swap or repair the barrel first** (damage
and penetration), then the internal parts (jamming), then clean it (slows future degradation).
Optional addons that change these rules exist and are shipped disabled:
"G.A.M.M.A. Guns Have No Condition", "G.A.M.M.A. Guns easier cleaning",
"No Weapon Jam Chance at Full Condition".

## 4. Armour repairs — the full decision tree

| Situation | Tool needed | Action |
|---|---|---|
| Condition **< 50 %** | **Armour Repair Kit** of the class (Light / Medium / Heavy / Exo) + **Spare Parts** | use at a workbench (or the portable one) and swap parts. Resulting condition = **average of all parts**. **Swapping parts does not consume kit charges** |
| Condition **≥ 65 %** | **Maintenance kit** — sewing kits and glues | right-click apply; can be boosted with **Supportive Materials** |
| Spare parts themselves | the part's matching repair item | right-click the repair item and pick the part (the game highlights the item you need) |
| 50–65 % band | parts swapping until above 65 %, then maintenance | — |

Additional armour-repair facts:

- **Mechanics cannot repair armour.** ("In GAMMA, mechanics cannot repair armor.")
- The **Light / Medium / Heavy / Exo** repair kits are the armour counterpart of the weapon
  kits — matched to the class shown on the armour's icon.
- 0.9.5 raised the top-end costs: "Increased cost and crafting cost of Type D cleaning kit and
  repair kit", "Increase exo and heavy repair kits costs and crafting costs".
- The recipes for the armour line (from `craft.ltx`, section "repair"), read literally:

```
x_light_repair_kit    = glue_a ×2, glue_b ×2, sewing_thread ×4, swiss_knife ×3
x_medium_repair_kit   = sewing_kit_b ×3, heavy_sewing_thread ×2, glue_b ×3, grooming ×2
x_heavy_repair_kit    = sewing_kit_a ×8, heavy_sewing_thread ×4, glue_e ×6, armor_repair_fa ×4
x_exo_repair_kit      = heavy_repair_kit ×10, sewing_kit_h ×4, sewing_kit_a ×8, sewing_kit_b ×8
```

and for weapons (same section, annotated with the pack's own price notes):

```
x_cleaning_kit_p  = gun_oil_ru ×3, swiss_knife, grooming ×2, prt_i_fasteners   ; 2390 / 3941 RU
x_toolkit_p       = cleaning_kit_p ×4, gun_oil_ru_d ×3, grooming ×4, steel_wool ; 6006 / 10660 RU
x_cleaning_kit_s  = gun_oil_ru_d ×3, grooming ×2, rasp_tool ×2, prt_i_fasteners ×4 ; 3590 / 4562 RU
x_toolkit_s       = cleaning_kit_s ×4, gun_oil ×3, ramrod_tool ×4, steel_wool ×2  ; 11384 / 20660 RU
x_cleaning_kit_r5 = gun_oil ×3, rasp_tool ×2, steel_wool, prt_i_fasteners ×4    ; 4191 / 5028 RU
x_toolkit_r5      = cleaning_kit_r5 ×4, solvent ×5, ramrod_tool ×4, steel_wool ×3 ; 14204 / 25420 RU
x_cleaning_kit_r7 = gun_oil ×4, rasp_tool ×5, steel_wool ×3, prt_i_scrap ×3     ; 8928 / 10500 RU
x_toolkit_r7      = cleaning_kit_r7 ×20, solvent ×7, ramrod_tool ×6, steel_wool ×4 ; 57706 / 75000 RU
```

(Read `x_… =` lines as "yields the item on the left from the ingredients on the right". The
annotated prices are the pack's own notes: crafting cost vs trader value.)

Also from the shipped `mod_system_GAMMA_items_repair_quantity.ltx`, **tarpaulin** carries
`repair_part_bonus = 0.10` — a supportive material that raises the condition a repair action
produces. The file further lists which items each maintenance consumable may be applied to
(`glue_b`, `glue_a`, `glue_e`, `armor_repair_fa`, `sewing_kit_b/a/h`, `light/medium/heavy/exo
repair_kit` each with their own `repair_parts_sections` lists — fabrics, boots, ropes,
helmets, plates and so on). That is the "Supportive Materials" mechanic from the NPE tutorial,
in data form.

## 5. Other repair items you will meet

The manual names the gun-part tools directly: "Collect parts above 60 % condition and repair
them with the appropriate tool to 100 % condition (**Ramrod, Multitool, or File**)."
In the shipped recipes and price lists the same family appears as `ramrod_tool`, `rasp_tool`
(a file/rasp), `swiss_knife`, `grooming`, `steel_wool`, `solvent`, `gun_oil`, `gun_oil_ru`,
`gun_oil_ru_d`, `duct_tape`, `tarpaulin`, `sewing_thread`, `heavy_sewing_thread`, `glue_b/a/e`
and `armor_repair_fa`. 0.9.5 rebalanced exactly this economy: "Glowsticks and tarpaulin give
plastic. Fieldcooker gives more scraps", "Less plastic needed for medkits, no plastic for
stimpaks, syringe etc", "Metal mags give much more paper", "Increased wood parts from items
disassembly (easier hideout furniture crafting)".

## 6. Disassembly: where your crafting materials come from

The manual's inventory article is the best brief on this: "Ammunition can be quite heavy, but
**disassembled ammo parts are very lightweight**. Keep these parts and craft ammo with your
gunsmith toolkit on-the-go. **Be sure to disassemble all unnecessary ammo.**" And "Disassemble
the gear you find will allow you to retrieve crafting parts. Some of these items are valuable,
like broken detectors, so be sure to keep those if you need extra cash."

Material families visible throughout the recipes:

| Family | Examples |
|---|---|
| Electronics | `prt_i_resistors`, `prt_i_transistors`, `prt_i_capacitors`, `prt_i_copper`, `prt_i_plastic` |
| Mechanical | `prt_i_scrap`, `prt_i_fasteners`, `prt_i_wood`, `ball_hammer`, `steel_wool`, `rope`, `synthrope` |
| Fabrics/clothing | `prt_o_fabrics_1…4`, `sewing_thread`, `duct_tape`, `tarpaulin` |
| Ballistic/armour parts | `prt_o_ballistic_5…20`, `prt_o_retardant_1…18` (used for the `af_*` protection tech items and plates) |
| Gun parts | `prt_w_barrel_1…13`, `prt_w_bolt_1…9`, `prt_w_bolt_carrier_1…11`, `prt_w_trigger_components_1…6` (see `references/weapons.md`) |
| Ammo parts | powder and bullet components (`powder_3`, `bullet_r7_ap`, …) |

**Junk items that feed crafting are marked with a hammer-and-pincer icon** — the manual says
to keep them ("'Junk' items that are necessary for crafting recipes are indicated by a hammer
and pincer icon. Keep those."). The same icon marks the **armour parts** used in the plate
upgrade chain.

## 7. Cooking

From the manual's *Cooking* article — one of GAMMA's most-loved systems:

- "**All cooking recipes are available from the start.**"
- "Cooking is essential, it will provide high calorie food for cheap."
- "Using the **basic cooking kit near bonfires** will allow you to cook **without the need for
  charcoal**."
- "The **advanced cooking kit needs liquid fuel** to work. However, it is able to cook **high
  tier meals which provide useful long lasting buffs**."

Crafting side: `x_cooking = cutlery ×2 + prt_i_scrap ×2` (basic), and
`x_fieldcooker = cooking ×5 + explo_balon_gas ×1 + prt_i_scrap ×10 + prt_i_fasteners ×5`
(advanced, 2 × `recipe_advanced_1`). Food and drink items are part of the same systems as
survival — see `references/survival-mechanics.md`, which covers hunger, thirst and how meals
interact with tiredness.

Related shipped addons: **"G.A.M.M.A. Cooking Overhaul"**, **"G.A.M.M.A. Books Pass Time"**
(reading books to pass time), **"SaloEater's Remember HFE's Stove Slot"**, and the hideout
furniture family that adds stoves and storage.

## 8. The workbench, upgrading, and where crafting meets guns

- **Right-click any toolkit → portable workbench.** At the workbench you craft, repair, and
  (with the appropriate upgrade kits) install upgrades.
- **Upgrade kits are tiered by the item's repair class** since 0.9.5 (T1 → T3 as you go from
  novice/light gear and Type A weapons up to Exos and Type D weapons), and most calibre
  conversions were removed. Prices of most gun upgrade kits were **reduced** in 0.9.5.
- **Upgrade kits are among the recipes themselves**: `recipe_basic_3 / advanced_3 / expert_3`
  gate which upgrade recipes you can perform ("Basic / Advanced / Expert upgrades" in the
  header table above).
- Custom upgrades from the same patch show what GAMMA expects: durability upgrades that
  reduce armour degradation, and weapon conversions that keep a weapon's identity (PM → fast
  low-recoil laser pistol, Kiparis → 50-round gun, 9 mm AUG → cheap thermal-scope host).

## 9. Crafting economy in one table

| Want | Cheapest route |
|---|---|
| Stay alive early | craft bandages/medkits and cook your own food; buy only what you cannot craft |
| Fix a pistol/SMG | Type A cleaning kit from a mechanic (available from the start) → then a Type A repair kit |
| Fix a rifle | Type C kit line: craft cleaning-kit-r5 → toolkit-r5 (needs `solvent`, `ramrod_tool`, `steel_wool`) |
| Fix a sniper/LMG | Type D line: the toolkit-r7 recipe is a *large* investment (the pack's own note: ≈57 700 RU of materials, ~75 000 RU value) |
| Fix armour | Light kits are cheap (glues + thread); Exo kits need a Heavy Repair Kit ×10 |
| Get a Grizzly detector | advanced toolkit + `detector_advanced` + 14/14/14 electronics |
| Get into artefacts | Melter from the Ecologists, then fuse/empower (see `references/artifacts.md`) |

**Money-saving rule that follows from the data:** repairs are cheaper than replacements, and
the pack made the top two repair tiers **more** expensive in 0.9.5 on purpose — so good armour
in each tier plus upgrade kits beats jumping tiers on broken gear.

## 10. Quick answers

| Question | Answer |
|---|---|
| What are the toolkits? | Basic, Advanced, Expert, Medical, Gunsmith, Artefact Melter. |
| Where do I get them? | Marked stashes (Basic→south, Advanced→mid, Expert→Red Forest and north); Medical and Gunsmith are craftable since 0.9.5; the Melter is bought from Sakharov/Hermann. |
| How do I open a workbench? | Right-click a toolkit in your inventory. |
| Do repair kits have uses? | Yes — `max_uses = 3` for the four weapon kits in the shipped balance. |
| How do I fix a part below 60 %? | Repair kit of the gun's type: right-click → maintenance → repair part. |
| How do I fix a part above 60 %? | Cleaning kit of the gun's type: right-click → maintenance → clean part. |
| How do I fix armour below 50 %? | Swap parts with the class-matching armour repair kit at a workbench. Parts swapping does not consume kit charges. |
| How do I fix armour above 65 %? | Maintenance kits (sewing kits/glues), optionally with supportive materials. |
| Who repairs my armour? | You do — mechanics repair guns and sell kits, but not armour. |
| Why is my rifle still jam-prone after cleaning? | Cleaning fixes parts ≥60 % and prevents degradation; worn internal parts below 60 % must be repaired or replaced. |
| Why can't I craft X? | Most recipes are available from the start, but "some recipes are locked, these are mainly advanced exos PSUs recipes. You can get them from Lv5 supply Mercenary and Ecologist traders" (manual). |
| Where do I get cooking gear? | Craft a basic cooking kit (cutlery + scrap); use it at a bonfire; upgrade to the field cooker (advanced) for buff meals. |

Cross-references: gun parts, types and jamming → `references/weapons.md`; armour classes and
maintenance items → `references/armor-outfits.md`; artefact recipes and the melter →
`references/artifacts.md`; what traders charge and stock → `references/trading-economy.md`;
what the difficulty presets do to repair prices → `references/keybinds-settings.md`.
