# Troubleshooting — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the official wiki pages *Installing-GAMMA* (its **Troubleshooting**
section, antivirus list, renderer notes) and *Technical-Support-FAQ*; GAMMA's `Patchnotes.md`
(0.9.5 **Bugfix** section — the authoritative "is this already fixed?" list, quoted by script
name); ZCP's `FAQs.txt` (the **"Not enough IDs"** crash, verbatim); the pack's crash-related
addons in the modlist; and the log/layout facts used throughout this skill (Anomaly writes its
errors to `<Anomaly>/appdata/logs/xray_*.log`, and the launcher drives MO2, whose profile is the
only supported modlist). Snapshot: GAMMA 0.9.5 @ `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`.

---

## 1. Triage order (do these in order, always)

1. **Which layer failed?** Installer/launcher → §2. Game start-up → §3. Crash while playing →
   §4/§5. Wrong content → §6. Not a bug at all → §7.
2. **Get the log.** `<Anomaly>/appdata/logs/xray_<user>.log` — read the **last `! ` / `[error]`
   block**, note the script and line number, then look that script up in §4 (known issues) and
   `references/modding-guide.md` §9 (which addon owns it).
3. **Check the version.** 0.9.5, launcher v8.6, engine `MT-TEST_2026.5.5`. Many 0.9.x-era
   crashes are *already fixed* — compare against §4 before doing anything clever.
4. **Check what changed.** A crash that started right after you enabled/added an addon is a
   modlist problem (§8). A crash that started right after an update is an update problem (§5).
5. **Do not** hand-edit files while the game runs (`user.ltx` is rewritten on exit), and **do
   not** copy loose files into `Anomaly/gamedata/`.

## 2. Installation and update problems

| Symptom | Cause / fix (wiki-sourced) |
|---|---|
| **Far fewer mods than expected** | Make sure Anomaly **and** GAMMA are in antivirus exclusions; temporarily disable antivirus during install; update the launcher; press **Install / Update GAMMA** again |
| Launcher downloads fail or stall | Known blocking AVs: **Norton, Avast, AVG, Malwarebytes**; **Bitdefender** also blocks MO2 and every Anomaly exe (exclude each from Advanced Threat Defense) |
| Launcher looks old | Must show **v8.6**; otherwise download the v8.6 launcher archive and extract into `GAMMA/.Grok's Modpack Installer`, overwriting |
| Install consumed all my disk | ≥150 GB free needed up front; ideally 175–200 GB. Deleting the `GAMMA/downloads` archives saves ~20 GB but breaks repair/reinstall (**at your own risk**) |
| "Update available" on ModDB | **Do not update just because the launcher says so** — moddb addon updates can break the install irreversibly for the end user; follow the Announcements channel instead |
| Metered connection | Budget: Anomaly 9 GB download / 16 GB extracted, GAMMA RC3 11 GB / 27 GB, mods 27 GB / 76 GB (≈130 GB installed total) |

## 3. Crashes on start-up (before the main menu)

| Symptom | First checks |
|---|---|
| Instant crash / black screen | Renderer: use **DX11** (`Anomaly (DX11)` in MO2). **DX10 is broken.** DX8/9 need the dedicated DX8/9 modlist |
| Missing DLL / `0xc000007b`-class errors | Install **.NET Framework 3.5**, latest **DirectX**, and the **VC++ Redistributable (x64)** |
| MO2 asks what game to manage / wrong path | You moved folders: delete `ModOrganizer.ini` (white icon — **not** `ModOrganizer.exe`) and re-pick the Anomaly folder |
| Game launches but MO2 did not apply mods | You launched `AnomalyLauncher.exe` directly instead of **Run** from MO2 (or you hand-copied files into `Anomaly/gamedata/`) |
| Crash changing resolution | Edit `vid_mode` in `Anomaly/appdata/user.ltx` by hand, save, relaunch |
| Install on OneDrive/Documents/Desktop/Program Files | Move it: installs must live in a normal folder (see `references/installation-setup.md` §3) and both folders must be on the **same drive** |

## 4. Known issues and their fixes in 0.9.5 (script-by-script)

The 0.9.5 Bugfix list is the most useful troubleshooting document GAMMA ships, because it names
the failing script. If your log shows one of these and you are not on 0.9.5+, **the fix is to
update**:

| What your log says | 0.9.5 status |
|---|---|
| `pda.script line 524` | fixed (twice, including a probable AlifePlus-debug cause) |
| `smart_terrain.script:1491` | fixed |
| `xr_meet.script(462)` | fixed — and trading was disabled for all NPCs in that path |
| `xr_danger` | "potential crash fix" |
| `ui_inventory:2201` | fixed |
| `task_functor:391`, `tasks_measure.se_target`, `get_jam_status`, `tasks_recover_item_on_corpse line 102` | fixed ("log spam error" for the last one) |
| `callbacks_gameobject` optimisation | crash fix shipped with the perf work |
| `smr_loot.script:345` | fixed |
| Rare crash when **Semenov** dies during his task | fixed |
| Crash after the **Afterglow** storyline | "Afterglow crash fix disabled by default to avoid issues" |
| Crash with **Useful Idiots** | "potential crash fix" |
| Infinite time-event loops | "prevent infinity time event loops" |
| `grok_bo.script` weapon-section identification | fixed |

Other 0.9.5 fixes worth knowing because they change behaviour rather than crashing:

- **Medics no longer drop trade inventories as loot.**
- **Sin's increased AP resistance fixed to 10 %.**
- **Nosorog despawn latency removed.**
- **"Stop other tools working as basickit"** (a bug where non-Basic toolkits behaved as a Basic
  kit).
- **"Disabled safe artifact melting since artefacts don't emit rads anymore"** — melting is no
  longer the radiation-safe workaround, because the problem no longer exists.
- **A "better seed system for loot stabilizer"** — loot variance is more consistent.
- **"Remove smart reticle by default"**, "Weapon Cover Tilt fix for activation after sprint and
  during sprint", "Fixed Sin increased AP res", "Fixed some north smart terrain spawns",
  "Starting locations text fixes", **"265- NPCs Die in Emissions for Real — Disabled"** (do not
  expect that addon to work).
- **AlifePlus debug** was implicated in a PDA crash; "Fast Autocomplete Tasks Enhanced" added by
  Priler in 0.9.5 "cancels bounty tasks in which you weren't involved".

## 5. Updates, saves and "my stuff reset"

- **Every launcher update resets the modlist, settings and MCM values on purpose** ("it helps
  repair broken installs"). Make backups **before** clicking *Install / Update GAMMA*:
  `Anomaly/appdata/user.ltx`, `Anomaly/appdata/savedgames`, a renamed copy of the
  *G.A.M.M.A. MCM values* mod, and a copied MO2 modlist profile.
- **Save compatibility:** "Save game compatibility is **never guaranteed** for major version
  updates." Minor updates and hotfixes are generally compatible.
- **Archives/backups are snapshots** — MCM and modlist backups never update themselves; recreate
  them after each major version.
- **Moving an install** is supported (§3) but requires deleting `ModOrganizer.ini`.
- **Uninstalling** is just deleting the GAMMA and Anomaly folders — nothing is written outside
  them.

## 6. Wrong content: "where is my stuff?"

| Symptom | Explanation (by design) |
|---|---|
| Stash is empty | **Unmarked stashes are almost always empty**; content is tied to the marked stash and to its map tier (`references/crafting-repairs.md`) |
| Can't find an Expert toolkit in the south | **Expert toolkits only spawn in the Red Forest or further north** (manual) |
| Artefact vanished | 0.9.5: **artefacts despawn after 5 in-game days** if not picked up |
| Traders won't sell me guns/armour | Traders sell supplies/accessories only; enable **Black Market** if you want gear trading |
| Trader has no AP ammo | Ammo is gated by **supply level** (goodwill 500/1 000/1 500/2 000) and by WP/NATO doctrine |
| A guide's map route is wrong | **The Agroprom Underground entrance is randomised** since 0.9.5 |
| Companions/NPCs behaving oddly | Check `grok_*` and companion addons; 0.9.5 reworked companions and task targeting |

## 7. Things that look like bugs but are not

- **Weapons jam a lot** — worn **parts**, not a bug; clean/repair them
  (`references/weapons.md`).
- **Guns do tiny damage** — worn **barrel**.
- **You cannot sleep** — you are not tired enough (`references/survival-mechanics.md`).
- **You cannot run** — stamina below `cant_sprint_power_begin = 0.08`, or you are overloaded.
- **The south feels emptier over time** — deliberate (population shifts north with the story).
- **Enemies tank your FMJ** — the GROBBS armour model; use AP
  (`references/ballistics-damage.md`).
- **Stutter after a few minutes** — performance, not a crash: `references/performance-tuning.md`.

## 8. "I broke it with an addon"

The safe bisect, and it is the only supported one:

1. Revert to the default **G.A.M.M.A.** MO2 profile (or your clean copy) — do not try to delete
   individual files out of `mods/`.
2. Re-enable your additions **one at a time**, launching between each.
3. When it breaks, check for the **mutually-exclusive pairs** the pack warns about, e.g.
   *Mags Redux* vs GAMMA's unjam-on-reload bind, or two mods that both rewrite the detector UI,
   jam logic or magazine logic (`references/modding-guide.md` §10).
4. Check load order: addons that patch others must load **after** their target.
5. If an addon came from "Disabled (DO NOT ACTIVATE)", put it back.
6. If the log points at a GAMMA script, re-read §4 — it may simply be a version problem.

## 9. The "Not enough IDs" crash

Verbatim from ZCP's FAQ:

> "The game engine assigns IDs to every stalker, mutant, item, and so on. **It has 65535 of such
> IDs available**, after that you will run into this error. ZCP alone — even on maxed out
> settings — will not exhaust all of these IDs. However, if you use other addons that spawn lots
> of stalkers/mutants/items, have unreasonably massive stashes, or such things, then that will all
> contribute to less available IDs."

Recommended remedies (identical in the FAQ):

1. **If it happened mid-game:** load an earlier save, **delete player stashes**, **trigger an
   emission** to kill off stalkers, then apply the measures below.
2. **Decrease mutant/stalker population, squad size and squad variance.**
3. **Disable other addons that spawn lots of stalkers, mutants and items.**

The FAQ is explicit that this is an engine limitation and that default GAMMA settings should
never hit it.

## 10. Reporting a problem usefully

A GAMMA crash report that someone can act on contains: **GAMMA version** (0.9.5), **launcher
version** (v8.6), **engine** (`MT-TEST_2026.5.5`), the **log excerpt** from
`appdata/logs/xray_*.log`, **what changed** (update? new addon? settings?), whether it happens on
a **new game** or only a save, and your **renderer**. The official support channels are the
Discord (install channel, announcements channel) and the repository's issue/PR process for
modpack development (`references/modding-guide.md` §8).

## 11. Quick answers

| Question | Answer |
|---|---|
| Where is the crash log? | `<Anomaly>/appdata/logs/xray_<user>.log`. |
| What should I read in it? | The last `! ` / `[error]` block: script and line. |
| First thing to try for any crash? | Confirm DX11, confirm 0.9.5 + launcher v8.6, then read §4. |
| My install is missing half the mods? | Antivirus exclusions, then re-run *Install / Update GAMMA*. |
| Can I delete `GAMMA/downloads`? | It saves ~20 GB but repair/reinstall will re-download everything, at your own risk. |
| Are my saves safe across updates? | Not across major updates; generally yes across minor ones and hotfixes. |
| Why did my settings reset after updating? | Reset is by design; restore from your `user.ltx`/MCM/modlist backups. |
| "Not enough IDs" fix? | Delete stashes, trigger an emission, lower populations/squad sizes, remove spawn-heavy addons. |
| Missing content vs bug? | Check §6 — stashes, toolkits, artefact despawn and trader stock are all rules. |
| Game still stutters? | That is the performance page, not a bug: `references/performance-tuning.md`. |

Cross-references: install/update/backup mechanics → `references/installation-setup.md`;
modlist ownership and the safe-add procedure → `references/modding-guide.md`; performance and
stutter → `references/performance-tuning.md`; MCM defaults and the settings that reset →
`references/keybinds-settings.md`; population systems behind the ID limit →
`references/mutants.md` and `references/anomalies.md`.
