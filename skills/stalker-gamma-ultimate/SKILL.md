---
name: stalker-gamma-ultimate
description: Complete S.T.A.L.K.E.R. GAMMA knowledge skill.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: gaming
---

# S.T.A.L.K.E.R. G.A.M.M.A. — Ultimate Knowledge Skill

The largest skill in this repository: a complete, source-grounded knowledge base for
**S.T.A.L.K.E.R. G.A.M.M.A.** — *Grok's Automated Modular Modpack for Anomaly* — the
modpack built on top of the free standalone fan game **S.T.A.L.K.E.R. Anomaly 1.5.3**
(which is itself built on the X-Ray engine and the Call of Chernobyl mod).

This skill answers installation, configuration, gameplay-mechanics, modding, balance,
performance and crash questions about GAMMA from **verified primary sources** — the GAMMA
repository itself (configs, scripts, the in-game PDA manual, patch notes, the published mod
list), the official GAMMA wiki, and the pack's own in-game tutorials — and it is explicit
about what is *not* verifiable.

## Snapshot this skill was written against

| Fact | Value | Where it comes from |
|---|---|---|
| Pack version | **0.9.5** | `README.md` badge, `Patchnotes.md` header |
| Launcher version | **8.6** | `README.md` badge + official wiki "Installing GAMMA" |
| Modpack definition version | **920** | `G.A.M.M.A_definition_version.txt` |
| Repository | `github.com/Grokitach/Stalker_GAMMA` | README |
| Snapshot commit | `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0` | `git rev-parse HEAD` (2026-05-17, "Merge pull request #740 from Grokitach/dev2") |
| Base game | S.T.A.L.K.E.R. **Anomaly 1.5.3**, standalone, free | official wiki "Installing GAMMA" |
| Engine | Anomaly **MT-TEST_2026.5.5** (Multi-Threading, Demonized) for 0.9.5 | `Patchnotes.md`, `## Engine` of 0.9.5 |
| Addon folders shipped in the repo | **385** directories under `G.A.M.M.A/modpack_addons` | repository tree |
| Published mod entries with source links | **473 URLs / 492 lines** in `modpack_maker_list.txt` | repository file |
| Mod manager | **Mod Organizer 2** (shipped inside the GAMMA folder) | official wiki, `modlist.txt` |
| Default renderer | **DX11** (`renderer renderer_r4`) | `modpack_patches/appdata/user.ltx` |

Snapshot date: **2026-10-15**. If any of the numbers above disagree with the user's own
install, **the user's install wins** — every claim here was read from files, and every file
can be re-read.

## When to Use

- **Install / update / move / repair a GAMMA install** — "how do I install GAMMA?", "the
  launcher only installed half the mods", "can I move my install to another drive?", "do I
  have to update?", "can I play on DX8/DX9?", "how big is the download?" →
  `references/installation-setup.md`, and for the update/backup/troubleshooting FAQs
  `references/troubleshooting.md`.
- **Build or fix a modlist, add an addon, patch a conflict, edit DLTX configs** — "which
  addons are in GAMMA?", "can I add my own mod?", "load order?", "what is DLTX?", "why does
  updating reset my settings?" → `references/modding-guide.md`.
- **Guns** — "what's the best early rifle?", "why does my gun jam?", "why does my gun do no
  damage?", "how do repair kits / cleaning kits / weapon parts work?", "what does Type A/B/C/D
  mean?", "which weapons are NATO vs WP?" → `references/weapons.md`,
  `references/crafting-repairs.md`, `references/ballistics-damage.md`.
- **Damage, ammo, armor penetration** — "why does this stalker eat my bullets?", "FMJ vs AP
  vs HP?", "what is BR1–BR6?", "what is BRC?", "how do I kill exoskeletons?" →
  `references/ballistics-damage.md`.
- **Armor and outfits** — "which suit should I wear?", "why can't I move in an exo?",
  "how do I repair armor?", "cloth mask vs helmet?", "what are armor plates?" →
  `references/armor-outfits.md`.
- **Artefacts** — "how do I find artefacts?", "which detector do I need?", "how do I make
  artefacts better?", "what is the Artefact Melter?", "which artefact gives what?" →
  `references/artifacts.md`.
- **Crafting, cooking, repairs** — "what are the toolkits?", "what do I craft first?",
  "where do I find expert toolkits?", "how do I cook food?", "how do repair kits and
  maintenance kits differ?" → `references/crafting-repairs.md`.
- **Mutants, anomalies** — "how do I kill a pseudogiant / chimera / controller?",
  "how do I survive an emission?", "which anomaly is which?", "why did my artefact vanish?"
  → `references/mutants.md`, `references/anomalies.md`.
- **Quests and storylines** — "what storylines exist?", "how do I unlock the UNISG
  playthrough?", "how do I get north / open the Miracle Machine?", "what tasks pay best?"
  → `references/quests-storylines.md`, `references/trading-economy.md`.
- **Factions, reputation, disguise** — "who is a NATO trader?", "how do I raise goodwill?",
  "can I disguise as Monolith?" → `references/factions.md`,
  `references/trading-economy.md`.
- **Survival** — "how do I heal a broken leg / a bleed?", "why can't I sleep?", "why am I
  always tired?", "why is my stamina bar capped?", "how do campfire saves work?" →
  `references/survival-mechanics.md`.
- **Controls and settings** — "what is the unjam key?", "which key shows the detector?",
  "what MCM options should I change?", "how do I enable ultrawide / 1440p fonts?" →
  `references/keybinds-settings.md`.
- **Performance** — "I stutter / get low FPS", "which shaders?", "prefetcher?", "should I
  disable X?" → `references/performance-tuning.md`.
- **Crashes and broken installs** — "it crashes on load", "Not enough IDs", "missing
  stashes", "my saves don't load after updating" → `references/troubleshooting.md`.

## Non-negotiables (how this skill answers)

1. **Never invent an item, statistic, number, recipe, spawn or mechanic.** Everything this
   skill states was read from the GAMMA repository, the official wiki, or the pack's own
   documentation, and each guide names its sources at the top. If a value is not in any of
   those, the answer says so — "not verifiable from GAMMA's files; check in game" — instead
   of guessing.
2. **The user's live game overrides every document, including this one.** The GAMMA
   in-game manual lives at **PDA → Guide → GAMMA** (its content is
   `modpack_addons/Grulag's In-game G.A.M.M.A. Manual/gamedata/configs/text/eng/z_pda_gamma.xml`),
   the mod configuration lives in **MCM** (main menu or in-game), and every stat is visible
   on items. When the user's game disagrees with a guide, the game is right; say so.
3. **Version matters.** GAMMA changes fast; 0.9.5 rewrote armor stats, the BR class system,
   upgrade kits and the engine. A sentence in a 2022 YouTube comment is not a source.
   Mark anything that is version-sensitive as such.
4. **Never tell a user to break their install.** Adding mods, updating, deleting
   `GAMMA/downloads`, or editing `user.ltx` all have documented consequences (this skill
   lists them). Prefer reversible steps and back-ups first — see the backup section of
   `references/installation-setup.md`.
5. **Distinguish GAMMA from Anomaly and from the original games.** Many mechanics (limb
   health, repair kits, dynamic anomalies, no gear trading, the goodwill economy) are
   GAMMA's, not vanilla Anomaly's, and not the 2007–2010 trilogy's. Say which one a claim
   belongs to.

## Source hierarchy (use in this order)

| # | Source | Where it lives | Trust |
|---|---|---|---|
| 1 | The user's own install: live config, MCM, in-game item descriptions, PDA manual, logs | `<Anomaly>/appdata/`, `<GAMMA>/mods/`, `%GAMMA%/overwrite` | Authoritative |
| 2 | GAMMA's shipped configs and scripts | `G.A.M.M.A/modpack_addons/*/gamedata/…`, `G.A.M.M.A/modpack_patches/gamedata/…` | Authoritative for mechanics |
| 3 | GAMMA's in-game manual (Grulag) | `…/Grulag's In-game G.A.M.M.A. Manual/…/text/eng/z_pda_gamma.xml` | Authoritative prose |
| 4 | GAMMA's in-game tutorials (NPE) | `G.A.M.M.A. Tutorials/gamedata/configs/text/eng/*.xml` | Authoritative prose |
| 5 | `Patchnotes.md`, `README.md`, `G.A.M.M.A_definition_version.txt`, `modpack_maker_list.txt`, `modlist.txt` | repository root and `G.A.M.M.A/modpack_data/` | Authoritative for version facts |
| 6 | Official wiki: Installing GAMMA, Technical Support FAQ, Home | `github.com/Grokitach/Stalker_GAMMA/wiki` | Authoritative for install/support |
| 7 | GAMMA's own data tables (`artefacts_values.xlsx`, `gamma_ammo_weapon_table.xlsx`, `toolkits_chance.xlsx`, `good_weapons.txt`, `armor_values.tsv`) | inside addon folders | Authoritative, drafts — may drift |
| 8 | Established community material (official Discord guides, GSC/GOG store pages, community wikis and guides) | linked below | Mark as community/approximate |

Canonical links:

- Repository — https://github.com/Grokitach/Stalker_GAMMA
- Official wiki — https://github.com/Grokitach/Stalker_GAMMA/wiki
- Install guide — https://github.com/Grokitach/Stalker_GAMMA/wiki/Installing-GAMMA
- Technical support FAQ — https://github.com/Grokitach/Stalker_GAMMA/wiki/Technical-Support-FAQ
- Patch notes — https://github.com/Grokitach/Stalker_GAMMA/blob/main/Patchnotes.md
- Published mod list API — https://stalker-gamma.com/api/list
- Official Discord — https://discord.gg/stalker-gamma (the `#how-to-install` channel is the
  most current install source; the wiki says so explicitly)
- Linux port guide (community, wiki-linked) — https://github.com/Red007Master/Red-s-Guide-on-Installing-G.A.M.M.A.-on-Linux
- DX8/DX9 modlist (community, wiki-linked) — https://github.com/veerserif/gamma-dx8-and-dx9

## Reference index

| Guide | Answers |
|---|---|
| [`references/installation-setup.md`](references/installation-setup.md) | Requirements, downloads, folder layout, launcher workflow, sizes, checksums, backups, moving, uninstalling, DX8/9, Linux/macOS/Steam Deck, GOG one-click |
| [`references/modding-guide.md`](references/modding-guide.md) | MO2 modlist anatomy, addon numbering, GAMMA vs third-party addons, DLTX, load order, profiles, making patches, contributing upstream |
| [`references/weapons.md`](references/weapons.md) | Weapon classes, calibers, NATO/WP split, repair types A–D, parts, jamming, cleaning, upgrading, notable early/mid/late guns |
| [`references/armor-outfits.md`](references/armor-outfits.md) | Outfit classes (jacket → Nosorog), protection stats, armor parts, repair kits by class, helmets, exoskeletons, plates, speed/weight |
| [`references/ballistics-damage.md`](references/ballistics-damage.md) | GROBBS ballistic model, AP vs FMJ vs HP, BR1–BR6 scale, limb armor and BRC, hit zones, ammo-by-purpose, faction ammo behaviour |
| [`references/artifacts.md`](references/artifacts.md) | Artefact tiers and groups, spawn rules, quality/condition, detectors, empower/fuse/craft, melter, belt slots, perkifacts, pelts |
| [`references/crafting-repairs.md`](references/crafting-repairs.md) | The 6 toolkits, recipe books, repair kits and maintenance kits, workbench, cooking, disassembly, toolkit spawn tiers by map |
| [`references/mutants.md`](references/mutants.md) | Mutant roster, behaviour and counters, mutant loot and pelts, mutant tasks, populations and how they change |
| [`references/anomalies.md`](references/anomalies.md) | Anomaly types, fields vs mines, dynamic anomalies, artefacts in fields, psy/radiation zones, bolt technique, emissions |
| [`references/quests-storylines.md`](references/quests-storylines.md) | Storylines and how to start them, north gating (Miracle Machine / Brain Scorcher), task types, task boards, guides/fast travel |
| [`references/factions.md`](references/factions.md) | Faction list, relations, NATO vs WP doctrine, disguises, UNISG, Sin, Clear Sky↔Duty change |
| [`references/trading-economy.md`](references/trading-economy.md) | No gear trading, supply tiers and goodwill, price multipliers, what to sell, money sinks, black market, repairs at mechanics |
| [`references/survival-mechanics.md`](references/survival-mechanics.md) | Limb/main/psy health, bleeding, hunger, thirst, sleep and energy, radiation, weight, campfire saves, skills |
| [`references/keybinds-settings.md`](references/keybinds-settings.md) | GAMMA's default keybinds, GAMMA-added commands, MCM options, character creation, difficulty presets, graphics/audio defaults |
| [`references/performance-tuning.md`](references/performance-tuning.md) | Expected hardware behaviour, the MT engine, shaders, video options, the addons that exist to fix stutter, prefetcher, diagnostics |
| [`references/troubleshooting.md`](references/troubleshooting.md) | Install failures, antivirus, crashes (with the known fix list), save compatibility, log reading, missing content, "Not enough IDs" |

## GAMMA in one page (the state machine you are helping the user play)

GAMMA is a **survival-scavenging incremental game** wrapped around Anomaly's sandbox. The
loop, in the pack's own words (`article_gamma_progress_text` of the in-game manual):

1. **Do tasks and kill mutants** → collect mutant parts; the parts are wanted by stalkers'
   tasks. Goodwill with a faction unlocks better trader supply tiers.
2. **Collect stash coordinates** → visit marked stashes (white/green/yellow icons on the
   PDA map). **Toolkits come from marked stashes**, and the further north the map, the
   better the toolkit and the loot.
3. **Toolkits allow crafting/repair** → craft repair kits for the guns and armor you looted
   (you cannot buy weapons or armor in GAMMA).
4. **Better gear lets you go north** → the north is stronger stalkers, stronger mutants,
   deadlier anomalies and harsher radiation, with better rewards.
5. **The north is gated** behind the *Miracle Machine* and the *Brain Scorcher* storyline.

Three reinforcing design rules that explain most "why is this game like this?" questions:

- **No gear trading.** Traders sell supplies (ammo, meds, food, tools, attachments by
  faction type) and never weapons or armor. Gear is looted or crafted.
- **No random stash loot.** An unmarked stash is essentially empty; loot spawns only in
  marked stashes, and stash content is tied to the map it is in.
- **Condition is a resource.** Guns have both *condition* (cleanliness — drives jamming)
  and *part condition* (barrel drives damage/penetration); armor has condition plus parts
  and a repair class (Light/Medium/Heavy/Exo).

## Fast answers (the questions that arrive most often)

| Question | Short answer |
|---|---|
| What is GAMMA? | A free modpack for the free standalone game **S.T.A.L.K.E.R. Anomaly 1.5.3**; "Grok's Automated Modular Modpack for Anomaly". It installs itself with a launcher and MO2. |
| Do I need to own the S.T.A.L.K.E.R. games? | No. Anomaly is standalone and free. The GOG one-click installer is the only path that requires owning a base game. |
| Disk space? | At least **150 GB free** to install; ~175–200 GB recommended. Installed GAMMA (without Anomaly) is around 130 GB. |
| How long does install take? | Downloads: Anomaly 9 GB, GAMMA RC3 11 GB, mods 27 GB. Then MO2 extracts 76 GB of mods. Hours, not minutes. |
| Which renderer? | **DX11**. DX10 is broken and should not be used; DX8/9 need the community DX8/9 modlist. |
| Can I buy guns or armor? | No. That is intended. Buy supplies, loot gear, craft repairs. |
| Why do my bullets do nothing to some stalkers? | Armor penetration. See `references/ballistics-damage.md`: AP power must beat the hit limb's armor, otherwise you are only grinding armor down. |
| Where do I get toolkits? | From **marked** stashes; better maps give better toolkits (basic → advanced → expert). Expert toolkits only from the Red Forest and further north. |
| How do I repair a gun? | Clean parts ≥60 % with the right cleaning kit (Type A–D), repair/replace below that with the matching repair kit, and keep the gun itself clean. |
| How do I repair armor? | Swap parts with the class-matching repair kit (Light/Medium/Heavy/Exo) below 50 %, use maintenance items (sewing kits, glue) above that. |
| Best early money? | Tasks you can finish without a fight, mutant parts, artefacts to the Ecologists. |
| Why can't I sleep? | You must be tired enough; energy drinks/caffeine push tiredness away. Sleeping pills force sleep. |
| How do I find artefacts? | Equip a detector (default key **6**), walk anomaly fields; detectors are tier-limited (Echo→T1, Bear→T2, Grizzly→T4). |
| Why did my artefact disappear? | Capped: artefacts are intended to be found in the field, and 0.9.5 despawns unpicked artefacts after 5 in-game days. |
| Save system? | Quicksave/quickload (F5/F9 by default) and, in the modpack's default YACS configuration, campfire saves. Ironman/campfire modes are options. |
| Why did my MCM settings vanish after updating? | The launcher resets modlist/settings on purpose on every "Install / Update GAMMA". Back up first. |
| Where are my saves? | `Anomaly/appdata/savedgames`. Settings: `Anomaly/appdata/user.ltx`. |

## How to work with a user's install

When the user gives you access to their machine (or pastes files), these are the paths that
matter:

| Path | What it holds |
|---|---|
| `<GAMMA>/mods/` | the modlist the launcher installed (each addon is a folder) |
| `<GAMMA>/modlist.txt` | active/inactive mods and load order (`+` before, `-` disabled, `-End` stops MO2 from touching loose files) |
| `<GAMMA>/profiles/` | MO2 profiles (`G.A.M.M.A.` default, plus user copies) |
| `<GAMMA>/downloads/` | the downloaded archives — deleting these means re-downloading everything to repair |
| `<GAMMA>/.Grok's Modpack Installer/` | the GAMMA Launcher (`G.A.M.M.A. Launcher.exe`) |
| `<Anomaly>/appdata/user.ltx` | game settings and **all default keybinds** |
| `<Anomaly>/appdata/savedgames/` | save files |
| `<Anomaly>/appdata/logs/` | `xray_*.log` — the first file to read for a crash |
| `<Anomaly>/gamedata/configs/…` | loose Anomaly configs (GAMMA mostly overrides them through MO2) |

Reading a crash: get `xray_<user>.log`, find the last `! ` / `[error]` block, note the
script and line, then check `references/troubleshooting.md` for the known-issue list and
the addon that owns that script.

## Glossary

- **Anomaly** — the standalone free Stalker game GAMMA mods. Version 1.5.3.
- **GAMMA** — Grok's Automated Modular Modpack for Anomaly; the thing this skill is about.
- **MO2** — Mod Organizer 2, the virtual-file-system mod manager GAMMA ships and automates.
- **Addon** — one mod in the modlist. GAMMA's own addons are prefixed `G.A.M.M.A. …`;
  third-party ones are usually numbered (`197- New Storylines …`).
- **DLTX** — a config-patching framework that lets an addon edit another mod's `.ltx`
  values without replacing the file (used heavily by GAMMA).
- **Toolkit** — Basic / Advanced / Expert / Medical / Gunsmith / Artefact Melter; unlocks
  crafting and lets mechanics sell you repair kits. Found in marked stashes.
- **Repair kit vs cleaning kit** — repair kits replace parts (and are consumed); cleaning
  kits restore *parts* ≥60 % to 100 % (Type A–D, one per weapon repair type).
- **Maintenance kit** — armor-side equivalent (sewing kits, glues) used at ≥65 % condition.
- **BR class (BRC)** — the armour-penetration class of armour, running from **0.17**
  (Nosorog) to **0.80** (7.62×54R AP, which defeats everything); a bullet whose AP is below
  the armour's class only damages the armour. See `references/ballistics-damage.md`.
- **PDA manual** — PDA → Guide → GAMMA, the pack's own in-game manual (Grulag).
- **Perkifact** — a belt artefact that grants procedural perks instead of protection
  (Perk-Based Artefacts addon); spawns at 100 % efficiency and decays while equipped.
- **Pelts** — skinned mutant hides used as belt items with bonuses; only one at a time.
- **YACS** — "Yet Another Campfire Saving" mod: campfire saves, configured by GAMMA.

## Guardrails

- Don't claim a specific **spawn chance, price, damage or protection number** unless it is
  in the guides with a source. GAMMA's tables are drafts and the game is the truth.
- Don't recommend **DX10**; the wiki says it is broken.
- Don't recommend **deleting `GAMMA/downloads`** as routine cleanup without the warning.
- Don't advise mixing **DX8/9** without the community modlist.
- Don't treat **moddb "update available"** notices as safe to apply — the FAQ explicitly
  warns against it.
- Don't confuse **Anomaly's** mechanics with **GAMMA's**; when in doubt, name the source.
- Don't promise save compatibility across **major** versions; the FAQ says it is never
  guaranteed.
