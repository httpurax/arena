# Quests, tasks and storylines — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the PDA manual articles **Storylines & Missions**
(`article_gamma_story_text`), **How To Progress** (`article_gamma_progress_text`), **Stashes**,
**Money** and **Hidden Radio Emitting Packages** (`article_gamma_rfpacks_text`); the **NPE
task tutorial** (`npe_gamma_tutorial_task.xml`); the New Storylines addon
(`197- New Storylines (DLTX minimodpack) - Demonized/…/mod_system_storylines.ltx`); the
task-related addons and fixes in the shipped modlist (`293- PDA Taskboard`, `403- New Tasks`,
`450- Useful Idiots`, `463- Tasks QoL Pack`, `G.A.M.M.A. Dynamic Tasks Balance`,
`G.A.M.M.A. Quests Rebalance`, `G.A.M.M.A. Additional Storylines fixes`, `Catspaw's Timed
Tutorial Prompts`, `AlphaLion's Reworked Stash Quest and Map Markers`); the pack's
character-creation keys in `axr_options.ltx` (`[character_creation]`); and `Patchnotes.md`
0.9.5 (**Progression**, **Gameplay**, **Bugfix**). Snapshot: GAMMA 0.9.5 @
`ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. The storylines GAMMA ships (verbatim list)

The in-game manual's *Storylines & Missions* article is the authoritative catalogue:

| Storyline | How it starts | Who can play it |
|---|---|---|
| **Lost to the Zone** | "Available at your **faction leader in your starting base** with these factions: Loner, Clear Sky, Duty, Freedom, Mercenary, Ecologist" | the six listed factions |
| **Mission Afterglow** | "Available at the start of the **UNISG playthrough** (type **`isg`** in char creation to unlock faction)" | UNISG only |
| **Artefact Hunters** | "talk to any NPC among the 'Artefact Hunters', ie; **Kovalev in church in the swamps** or their representative, named **Sarik the Twilight in the Cordon Village**" | "Available to **Ecologist Allies**: Loner, Clear Sky, Duty, Freedom, Military, Mercenary, Ecologist" |
| **Last Dawn** | "Talk to **Spire in the Swamps Clear Sky base**" | "Available to **Clear Sky Allies**: Loner, Clear Sky, Duty, Freedom, Mercenary, Ecologist" |
| **Operation Monolith Retribution** | "Available from **Colonel Kuzentsov** and help the Military take control of the centre of the Zone" | "Available to **Military Allies**: Military, Ecologist" |
| **Dr.X Questline** | — | "Available to **all factions**, not really story oriented" |

Practical consequences:

- **The `isg` trick is a real, documented character-creation entry** — typing `isg` into the
  character-creation flow unlocks the **UNISG** faction and with it the *Mission Afterglow*
  storyline. GAMMA also ships `[character_creation]` keys in its MCM defaults
  (`new_game_faction`, `new_game_story_mode`, `new_game_conditions_mode`, …), so story mode and
  faction are both first-class creation choices.
- **The two "big" campaign spines are Lost to the Zone (your faction) and the north gates.**
  Beyond that, GAMMA's progression is task-driven, not cutscene-driven.
- **New Storylines (3.0)** is the addon that supplies much of the modern story content; its
  config (`mod_system_storylines.ltx`) defines story artefacts such as `af_ah_o1` / `af_ah_o2`
  (`class = SCRPTART`, `af_rank = 0`, `cost = 4000`, **`can_trade = false`** — quest items you
  cannot sell). `G.A.M.M.A. Additional Storylines fixes` patches it.

## 2. The north gates

GAMMA's geography is locked, and the README states the rule plainly:

> "**Access to the North of the Zone is locked behind completing the Miracle Machine and the
> Brain Scorcher.**"

Between those two gates and normal tasking, the practical progression chain a player
experiences is:

1. **Southern maps** (Cordon, Swamps, Garbage, Dark Valley, Agroprom, Darkscape, Truck
   Cemetery) — basic toolkits, low-tier mutants, WP/NATO starter ammo.
2. **Mid maps** (Bar/Rostok, Military, Yantar, Dead City, Limansk) — advanced toolkits become
   common (see the toolkit by-map table in `references/crafting-repairs.md`), first real
   armour.
3. **The gates** — Miracle Machine and Brain Scorcher, normally along your faction's main
   storyline (Lost to the Zone / your faction leader) or Dr.X's chain.
4. **North** (Red Forest, Radar, Zaton/Jupiter, Pripyat, Hospital, Stancia, Generators) —
   expert toolkits, AP-only factions, the best artefacts, and the endgame.

0.9.5 changed two things that touch this chain:

- **"Randomized Agroprom Underground entrance"** (oleh5230) — the entrance to the underground
  is randomised per playthrough, so old guides' route descriptions do not always hold.
- **"South / North population balance upon receiving the psy helmet"** — the Zone
  repopulates as you progress: "as you progress with the story, the **south will progressively
  become emptier as the north gets more populated**, which should improve the tasking shifts as
  well." Expect easier south roaming and harder north work after that milestone.

## 3. Task types (what a task can be)

GAMMA's task pool, as described by the patch notes and manual:

| Task type | Detail |
|---|---|
| **Fetch / delivery** | item hand-ins; 0.9.5 reworked "RF/delivery package loot", removed multiple weapon fetch tasks, and made **fetch quests not pick belt artefacts** |
| **Elimination / assault** | kill targets; **assault tasks now target squads of 2 or more** rather than lone NPCs, and rewards scale with the target map's danger |
| **Capture enemy documents** | "Capture enemy document tasks cannot be on the same map as the task giver" |
| **Loot a stash / mark stashes** | stash-discovery tasks; stash content is map-tiered (see `references/crafting-repairs.md`) |
| **Anomalous study / measurement** | measurement tasks in anomalies, now with a **failure penalty** since 0.9.5 |
| **RF receiver hidden packages** | radio packages — see §4 |
| **Eliminate apex predator** | a new rare task added in 0.9.5 |
| **Artefact Hunters jobs** | artefact-oriented, with **increased money rewards** in 0.9.5 |
| **Bounty / squad contracts** | the Bounty Squads family (GAMMA ships optional "Bounty Squads Rework"/"Bounty Squad Kill" addons) |
| **Guide jobs (fast travel)** | paying NPCs to take you across the Zone — see §6 |

Two rules the 0.9.5 patch notes made explicit because they were previously unfair:

- **"Tasks can no longer be 'stolen' by other stalkers"** — "the task is canceled without
  penalty because someone else took the bounty faster than you".
- **"Avoid quest stashes to be on the same level as actor"** — quest stash spawns are not
  placed on the map you are standing in, so you actually travel for them.

And one that changes the feel of the early game: **"Tasks money rewards depend on targeted
map"** — south tasks pay less, north tasks pay more. That is the intended incentive to push
north (and it is why the manual's money article calls tasks out as a fast income source).

## 4. Hidden radio-emitting packages (a GAMMA signature task)

From `article_gamma_rfpacks_text`, in the manual's own steps:

1. "You'll get random messages that are telling you to find some packages in certain maps."
2. "To find them, **equip your RF Receiver and press the detector key**. **Put your weapon
   away** and **change the frequency of your RF Receiver to match the one from the message**
   (check keymap for more details)."
3. "Follow the strong beeps, **the faster they are, the closer** you are to the package."
4. "You can hold the **Use button (F)** to display the package text and more easily find and
   grab it."
5. **"It's actually an item laying on the ground** or hidden in barrels etc. It is **NOT a
   stash** you have to interact with."
6. "You can then right click the package in your inventory and **open it** to get its
   contents."
7. "Packages range from random stuff to **artefacts or toolkits**."

Supporting addons in the list: **`332- QoL Patch to Tweak_Breeki's RF Receiver Hidden
Packages`**, **`254- Better RF Receiver sound`**, **`SaloEater's Use Package Only Once`**,
**`Oleh's Package Loot Rework`** (0.9.5 explicitly credits "RF/delivery package loot rework -
oleh5230").

## 5. Stashes (the actual progression currency)

`article_gamma_stashes_text` is short and every line matters:

- "**Stashes are the main source of toolkits**, which are the most critical items you need to
  progress."
- "**Unmarked stashes are almost always empty.**" / "**Stashes must be marked to contain
  anything of value, especially toolkits.**"
- "**Stash content is tied to the map they spawn in.**"
- "The more to the north a stash is in the Zone, the better the loot."
- "**Expert toolkits can only be found in the Red Forest or further North.**"
- "**Storing stuff in stashes is safe: it won't be looted by NPCs.**"
- "Even if the stash is marked at some point, content will spawn in the stash **on top of what
  you previously stored**."

How you mark stashes: tasks, looting NPCs (`stash_chance` in `difficulty.ltx` is 0.4 / 0.3 /
0.2 across the three economy presets), PDA map markers, and this shipped design decision from
the README: "**GAMMA removes random stash loot, so you can't just run to the meta stashes and
have endgame equipment instantly.**" 0.9.5 also added "Bit less armors in stashes" and "Proper
armors stash tiers with the rebalance" plus "Slightly easier expert tools in the north".

## 6. Travel, guides and PDA conveniences

| System | Facts |
|---|---|
| **Guides / fast travel** | pay an NPC to move you; 0.9.5 changed cheap swamp guide routes: "Cheap Swamp guide routes to **Yantar and Jupiter** instead of **Bar and Agroprom**", plus "Marsh guide text edits". The pack ships `G.A.M.M.A. Fast Travel Limiter Rebalance` to tune cost/limits |
| **PDA Taskboard** | `293- PDA Taskboard` (iTheon) adds a task board to the PDA; GAMMA ships `478- Custom iTheon's PDA Taskboard` and patched it for long-task scrolling and overlapping text in 0.9.5 |
| **Guiding tasks on the map** | 0.9.5: "guiding tasks are now visible on the map thanks to SaloEater" |
| **Map markers** | `AlphaLion's Reworked Stash Quest and Map Markers`, `466- PDA Map Location Labels and Faction Icons` |
| **Companions** | `G.A.M.M.A. Companions Rework`, `132- Companion anti awol`, `G_FLAT's Individualy Recruitable Companions`, companion wheel keybind (`custom18`, default **C**) |
| **New tasks** | `403- New Tasks` (iTheon), `463- Tasks QoL Pack`, `450- Useful Idiots` (escort/task NPC behaviour) |
| **Task fixes** | `Oleh's Tasks Crash Fixes`, `FishWings XR Reach Task Script Fix`, `G_FLAT's Gavrilenko Tasks Fix`, `G_FLAT's More Measurement Task Maps` |

## 7. Hideout content (new in 0.9.5, and it *is* progression)

0.9.5's patch notes describe two hideout items with mechanical value:

- **Trading computer** — "a trading computer that you can buy from the **Ecologists and
  Mechanics** allows you to access **traders allied to your true faction in a 150 m radius**".
  (Also listed under Economy: "trading_computer added to several traders including mechanics".)
- **Artifact harvester** — "allows you to **place an artifact in it, which is then degraded to
  passively generate items**, with results depending on the artifact. Outcomes range from wood
  parts to mutant meat to ammo crafting materials, up to… other artifacts."

Supporting modlist entries: `245- Hideout Furniture`, `349- Hideout Furniture Expansion`,
`385- Even More Hideout Furnitures`, `470- Gadgets for Hideout Furniture`,
`Veerserif's Hideout Furniture Craft and Trade`, `SixSloth's & Veerserif's Hideout Furnitures
2.2.1 GAMMA patch`.

## 8. North-side quest pitfalls and the fixes GAMMA applied (0.9.5 Bugfix list)

Reading the bugfix list is the fastest way to know which quest bugs are *already solved* in
0.9.5 (so you should not advise workarounds):

- "Fixed rare crash when semenov dies during his task"
- "Fixed medics dropping trade inventories as loot", "fixed xr_meet.script(462) crash and
  disabled trading for all NPCs"
- "Afterglow crash fix disabled by default to avoid issues"
- "Tasks 123 124 125 text fix", "simulation tasks 122-126 text fixes"
- "Fixed log spam error tasks_recover_item_on_corpse", "task_functor:391 tentative crash fix",
  "tasks_measure.se_target tentative crash fix"
- "Better Artefacts Hunter Russian text by demyanich", "special character ' fix in certain
  st_quests_general.xml dialogues"
- "Fixed Dolg <> Csky relations for actor and drx questline honcho pick"

These are worth quoting to a user who reports an old crash: **if their GAMMA is not 0.9.5+,
the answer may be "update"** (with the warnings in `references/installation-setup.md` §6 about
how updates reset their settings).

## 9. Tasking-loop advice (derived from the mechanics above)

1. **Talk to everyone in your starting base first** — faction leader for the storyline spine,
   traders for supply, mechanics for the first Type A repair kit.
2. **Mark stashes relentlessly.** Stash coordinates come from tasks and corpse looting;
   `stash_chance` is 20–40 % per corpse depending on economy preset.
3. **Take map-appropriate tasks.** Rewards scale with the target map, so an "easy" northern
   fetch can be worth more than a southern firefight — and 0.9.5 made assaults target *squads*,
   which is a real change in difficulty.
4. **Do the North gating storylines deliberately.** Miracle Machine and Brain Scorcher are hard
   locks; nothing else opens the north.
5. **Bank goodwill while tasking** — task completion is the main goodwill source
   (`goodwill` multiplier 1.4/1.2/1.0 across economy presets) and goodwill is what unlocks
   trader supply tiers (see `references/trading-economy.md`).
6. **Use the Artefact Hunters and Dr.X chains as money engines** — Artefact Hunters rewards
   were buffed, and Dr.X is available to every faction.
7. **If you play UNISG, type `isg`** at character creation, or you will never see *Mission
   Afterglow*.

## 10. Quick answers

| Question | Answer |
|---|---|
| How do I start a storyline? | Faction leader in your starting base (Lost to the Zone); Kovalev (swamps church) or Sarik the Twilight (Cordon) for Artefact Hunters; Spire (Swamps, Clear Sky base) for Last Dawn; Colonel Kuznetsov for Operation Monolith Retribution; Dr.X for everyone. |
| How do I unlock UNISG? | Type `isg` in character creation (manual's own instruction). |
| How do I open the north? | Complete **Miracle Machine** and **Brain Scorcher**. |
| Where are the best stashes? | Further north; stash content is tied to the map, expert toolkits only from Red Forest and beyond. |
| Do unmarked stashes have loot? | Essentially never; only marked stashes hold anything. |
| Can NPCs loot my stash? | No — stash storage is safe by design, and marked stashes *add* content on top of what you stored. |
| Why is my task gone? | Since 0.9.5 tasks can be taken by other stalkers — the task is cancelled without penalty. |
| Why did my fetch task ask for something strange? | Fetch tasks no longer pick belt artefacts, but they can still ask for anything else in your pack — read the task before accepting. |
| Is there a quest log? | Yes — the PDA, plus the PDA Taskboard addon and the active-jobs keybind (`active_jobs`, default **CAPS LOCK**). |
| Where is my task reward? | Tasks pay by map tier; the money lands via the giver, and the reputation/goodwill effect is separate (see `references/factions.md`). |

Cross-references: task rewards and goodwill economics → `references/trading-economy.md`;
faction availability and allies → `references/factions.md`; stash toolkit tiers →
`references/crafting-repairs.md`; north-side threats → `references/mutants.md` and
`references/anomalies.md`; difficulty presets that change task rewards →
`references/keybinds-settings.md`; task/quest crashes and the scripts behind them
(`task_functor:391` and friends) → `references/troubleshooting.md`.
