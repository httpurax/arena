---
name: tarkov-spt-companion
description: SPT 3.10.5 mod, config and FPS companion.
version: 1.0.0
license: MIT
platforms: [windows]
metadata:
  hermes:
    category: gaming
---

# Tarkov SPT Companion

A maintenance companion for **one specific single-player Escape from Tarkov install**: SPT
**3.10.5** at `C:\games\SPT-TARKOV-3105-COOP-LAN`, running roughly 120 mods (about 47
server mods under `user\mods` plus about 79 BepInEx client plugins), built around the
**SAIN / BigBrain / Waypoints / Donuts / SWAG / Questing Bots / Looting Bots / ALP** AI
stack. The player wants raids that feel alive, gunplay and looting over questing, a
Softcore profile, and playable frame rates on **16 GB of RAM**.

This skill does **not** migrate the install. 3.10.5 is the destination, not a waypoint, and
every recommendation here is written for that exact server version.

## When to Use

- The user asks what a mod in his install does, why it is there, or whether two of his mods
  fight each other — start at `references/mod-catalog.md`.
- The user asks about **load order**: which BepInEx plugin wins, how the SPT server orders
  `user\mods`, or how to disable one mod without deleting it →
  `references/load-order-guide.md`.
- Something is **broken**: the raid never starts and the server sits on a
  `/client/locations` request, the console prints
  `TypeError: Cannot read properties of undefined`, Donuts settings will not stick, or an
  old preset made a config stop matching → `references/troubleshooting.md`.
- The user asks about **FPS, stutter, or memory** on his 16 GB machine →
  `references/performance-tuning.md`.
- The user wants to **back up or restore** a profile, a mod set, or the whole install →
  `references/backup-restore.md`.
- The user wants to **add a new mod** (or asks "is this mod safe for 3.10.5?") →
  `references/mod-install-workflow.md`.
- The user asks about **server settings** — raid timers, loot, traders, flea, SVM, LAN
  addresses → `references/server-config.md`.

## When Not to Use

- The user is on a different SPT version (3.9.x, 3.11.x, 4.x). The paths, config keys, and
  mod builds here are 3.10.5's; say so and do not extrapolate.
- The user wants a **new BepInEx client DLL**. That is off the table for this install by
  his own rule — new mods go to `user\mods` only.
- The user wants hardware, driver, or Windows tuning beyond what
  `references/performance-tuning.md` covers; that page stops at graphics settings and RAM
  hygiene on purpose.
- The user asks for a download link. Point him at `https://sp-mod.com` and the mod's GitHub
  releases page; this skill never invents a URL.

## Install profile (the facts this skill is built on)

| Fact | Value | Source |
|---|---|---|
| SPT version | **3.10.5** — staying, no migration | stated by the user |
| Install root | `C:\games\SPT-TARKOV-3105-COOP-LAN` | stated by the user |
| Server mods | **~47** folders under `user\mods` | stated by the user (recount with `mod-catalog.md`) |
| Client plugins | **~79** DLLs under `BepInEx\plugins` | stated by the user (recount with `mod-catalog.md`) |
| Core AI stack | SAIN, BigBrain, Waypoints, Donuts, SWAG, Questing Bots, Looting Bots, ALP | stated by the user |
| Playstyle | alive raids, gunplay + looting, light questing | stated by the user |
| Profile type | Softcore | stated by the user |
| Hardware constraint | 16 GB RAM, FPS-conscious | stated by the user |

Paths used throughout, all relative to the install root:

```
C:\games\SPT-TARKOV-3105-COOP-LAN\
├── SPT.Server.exe                  # the server
├── BepInEx\plugins\                # client plugins (.dll + their own folders)
├── BepInEx\patchers\               # prepatchers (rare, load before plugins)
├── BepInEx\config\                 # BepInEx .cfg files, one per plugin GUID
├── user\mods\                      # SERVER mods, one folder each, each with package.json
├── user\profiles\                  # the save files — *.json, one per profile
├── SPT_Data\Server\configs\        # core.json, http.json, gameplay.json, ...
└── SPT_Data\Server\database\       # items, traders, locations, globals
```

## Hard rules (never break these)

1. **Sources are `https://sp-mod.com` and GitHub releases only.** The old Forge domain
   is dead — do not send the user there, do not quote it, do not accept a link to it.
2. **New mods are server-side only.** They land in `user\mods\<ModFolder>\`; no new
   BepInEx client DLLs are added to this install.
3. **Never extract an archive over an existing install.** Extract to a staging folder,
   delete or rename the target folder in the install, then copy the staged files in
   (`references/backup-restore.md`, `references/mod-install-workflow.md`).
4. **Never invent a mod version, a build number, or a URL.** If a version is not verified,
   say "check the Versions tab on sp-mod.com" and mark the line *verify in-game*.
5. **Test every change on Factory first.** Smallest map, fastest load, quickest verdict.
6. **Back up before you touch anything at all**, at minimum `user\profiles`.

## Research grounding (read before advising)

- **The install on the user's disk wins.** Mod folder names, config file names, and which
  of the ~120 mods are actually present are things only his disk knows. Where this skill
  names a path it is quoting a documented layout or the user's own description; where it
  guesses, the line carries **verify in-game**.
- **Verified vs. judgement.** *Verified* = stated by the user, or read from sp-mod.com /
  a GitHub repository during this skill's research. *Judgement* = an inference (ranking,
  "this costs more than that", "try this first"). Keep the label when repeating it.
- **No frame-rate promises.** `performance-tuning.md` names levers, never "this gives you
  +20 FPS".
- **Uncertain = marked.** Anything version-sensitive, folder-name-sensitive, or user
  dependent is flagged rather than smoothed over.

## Reference index

| Reference | Answers |
|---|---|
| `references/mod-catalog.md` | installed inventory (server + client), what each does, why it is there, and how to enumerate the real one |
| `references/load-order-guide.md` | BepInEx plugin order, `user\mods` priority, `package.json` ordering fields, conflict resolution |
| `references/troubleshooting.md` | the `/client/locations` hang, `TypeError: Cannot read properties of undefined`, dual Donuts folders, old-preset schema drift, isolation workflow |
| `references/performance-tuning.md` | 16 GB RAM budgeting, which mods cost the most, graphics and boot-config levers |
| `references/backup-restore.md` | profile backup, full mod backup, safe restore, never extract over an install |
| `references/mod-install-workflow.md` | evaluate → version-check → install → Factory test → rollback |
| `references/server-config.md` | `SPT_Data\Server\configs\`, SVM + Greed, raid settings, LAN addresses |

## Three workflows, in one line each

- **Adding a mod:** check the Versions tab for a 3.10.x build → confirm it is server-side →
  back up → factory-test on Factory → roll back by deleting the folder you added.
- **Raid won't start:** read the *server console*, not the game → bisect `user\mods` →
  suspect the newest spawn preset first.
- **Before any of it:** copy `user\profiles` somewhere that is not the install.

## Completion Checklist

Before telling the user an answer is finished:

- The answer came from one of the seven references, and the reference was named.
- Every path quoted is a real SPT 3.10.5 path; nothing was invented to fill a gap.
- No version number or URL was stated that this skill did not verify.
- The hard rules held: sp-mod.com / GitHub only, no new client DLL, no extract-over-install,
  Factory first, backup first.
- Anything uncertain was handed back to the user as **verify in-game** rather than asserted.
- No FPS number was promised.
