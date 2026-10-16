# Mod catalog — what is installed, what it does, why it is here

**What this page is.** The inventory for one SPT **3.10.5** install at
`C:\games\SPT-TARKOV-3105-COOP-LAN`: what the mods are, which side of the install they live
on, which config file actually controls them, and why a player who wants *alive raids,
gunplay plus looting, light questing* keeps them.

It is also honest about its own limits: the skill knows the **eight core mods by name**
because the user named them, and it knows the **shape** of the rest. The full 47 + 79 list
lives on his disk, and this page ships the exact commands to pull it out.

---

## Grounding — read before repeating any of this

| Tag | Meaning |
|---|---|
| **stated** | the user told this skill directly (install path, SPT version, core stack, mod counts) |
| **verified** | read from `https://sp-mod.com` or a GitHub repository while this skill was built |
| **verify in-game** | the folder name, config file name, or presence of the mod must be confirmed on his disk before anyone acts on it |

### The layout this page uses

Paths below are relative to the install root `C:\games\SPT-TARKOV-3105-COOP-LAN`:

```
user\mods\                # SERVER mods, one folder each, each with a package.json
BepInEx\plugins\          # client plugins (.dll + their own folders)
BepInEx\patchers\         # prepatchers (rare, load before plugins)
BepInEx\config\           # BepInEx .cfg files, one per plugin GUID
user\profiles\            # the save files — *.json, one per profile
SPT_Data\Server\configs\  # core.json, http.json, gameplay.json, ...
SPT_Data\Server\database\ # items, traders, locations, globals
```

Rules that follow from that table:

- **No invented versions.** A mod version appears here only when it was read from
  sp-mod.com or a GitHub repository during research. Everything else says *verify
  in-game*, or tells the player to look at the mod's own `package.json` in
  `user\mods\<ModFolder>\package.json`.
- **No invented URLs.** Only two hosts are ever named: `https://sp-mod.com` and
  `https://github.com/...`. The old Forge domain is dead and is never linked.
- **The disk wins.** If a folder name here does not match his install, his install is
  right — rename in your head, and correct this page.

## Provenance

| Source | What it supplied |
|---|---|
| stated by the user | install root, SPT 3.10.5, ~47 server mods, ~79 client plugins, the eight-mod core stack, Softcore profile, 16 GB RAM |
| `https://sp-mod.com` (The Forge) | SWAG + Donuts 4.0.0 is marked **SPT 3.10.5 Compatible** and **SPT 3.10.x ONLY**; its required dependency (UnityToolkit V1.2.0, Waypoints); the SWAG config paths (`user\mods\SWAG\config\config.json`, `user\mods\SWAG\config\bossConfig.json`, and the per-boss folders `user\mods\SWAG\config\bosses\`, `user\mods\SWAG\config\other\`, `user\mods\SWAG\config\custom\`) |
| `https://github.com/dwesterwick/SPTQuestingBots` | Questing Bots' requirements (BigBrain 1.5.0+, Waypoints 1.9.0+; SAIN 4.5.0+ and Looting Bots 1.8.0+ recommended) and its real config keys |
| `https://github.com/dvize/Donuts` | Donuts' spawn rules (same-level spawn markers, radius, one marker per group) |
| `https://github.com/Andrewgdewar/AlgorithmicLevelProgression` | ALP is *Algorithmic Level Progression* — randomized loadouts, bots level with the player |
| `https://github.com/GhostFenixx/svm-csharp` | SVM is a **server** mod: `user/mods/[SVM] ServerValueModifier` plus `Greed.exe` at the install root |
| `https://github.com/sp-tarkov/wiki` | the official mod split: server mods in `user\mods`, client mods in `BepInEx\plugins`, prepatchers in `BepInEx\patchers` |

---

## Tier A — the core AI stack (stated by the user)

Every row here is in the install. **Why it is there** is judgement from what the mod does
and what the player asked for (alive raids, gunplay, looting, light questing).

| Mod | Side | Where it lives | What it does | Why it is here |
|---|---|---|---|---|
| **SAIN** (Solarint's AI Modifications) | client | `BepInEx\plugins\` (**verify in-game**: exact folder name) | Replaces bot combat AI — decisions, suppression, cover, grenades, hearing. Configured from its in-game **F12** menu; per-bot-type presets are written into the plugin folder. | This is what makes gunplay feel like a fight instead of a shooting gallery. It is the single biggest quality difference in a raid. |
| **BigBrain** | client | `BepInEx\plugins\DrakiaXYZ-BigBrain\` (**verify in-game**) | Lets other mods add custom "brain layers" to bots — the plumbing SAIN, Questing Bots and Looting Bots all stand on. | It is a **dependency**, not an option: SAIN, Questing Bots and Looting Bots all need it. |
| **Waypoints** | client | `BepInEx\plugins\DrakiaXYZ-Waypoints\` (**verify in-game**) | Feeds navmesh/door waypoint data to the other AI mods so bots can path and open doors properly. | Hard dependency for SAIN and Questing Bots, and it is what stops bots from getting stuck in doorways. |
| **SWAG** | **server** | `user\mods\SWAG\` | Owns the map's spawn data: waves, spawn points, boss configuration. Config at `user\mods\SWAG\config\config.json` (with `MaxBotCap` / `NightMaxBotCap`), `user\mods\SWAG\config\bossConfig.json`, and the per-boss JSONs under `user\mods\SWAG\config\bosses\`, `user\mods\SWAG\config\other\`, `user\mods\SWAG\config\custom\`. | Server-side spawn data means every client sees the same raid — and it is the first place to cap bot counts when FPS hurts. |
| **Donuts** | client | `BepInEx\plugins\dvize.Donuts\` (verified: Fika's headless-client docs put Donuts settings in `BepInEx/plugins/dvize.Donuts/Config`) | Spawns and despawns bots **during** the raid around the player; scenario caps live in `BepInEx\plugins\dvize.Donuts\ScenarioConfig.json`. | This is what makes a raid feel *inhabited* instead of pre-seeded: waves arrive while you play. |
| **Questing Bots** | **server** | `user\mods\` (**verify in-game**: exact folder name) | Gives bots objectives (real quests, extracts, looting breaks) and can spawn initial PMCs / PScavs. Auto-disables its own initial-PMC spawning when SWAG + Donuts is detected. | Alive raids = bots with somewhere to be. Its own AI limiter is the clean way to stop paying for bots across the map. |
| **Looting Bots** | client | `BepInEx\plugins\` (**verify in-game**: exact folder name) | Makes bots loot containers and corpses, and lets other mods drive that behaviour through its interop. | Looting is half the playstyle; it also makes dead PMCs worth checking. |
| **ALP** (Algorithmic Level Progression) | **server** | `user\mods\` (**verify in-game**: exact folder name) | Randomized bot loadouts that scale with the player's level — the "wipe progression" mod. | Keeps gear fights honest: bots wear what the wipe would make them wear. **One bot-progression mod only** — see friction pairs below. |

## Tier B — supporting mods a stack like this normally carries

These were **not** confirmed present by the user. Treat each as "check whether it is in
your `user\mods` / `BepInEx\plugins`" before acting.

| Mod | Side | What it does | Why it would be here | Status |
|---|---|---|---|---|
| **SVM** (Server Value Modifier) | **server** | Edits server values (skills, extracts, flea, insurance, raid settings) from a Windows app. Lives at `user\mods\[SVM] ServerValueModifier\`, presets in `user\mods\[SVM] ServerValueModifier\Presets\`, active preset named in `loader.json`, configured with `Greed.exe` in the install root (verified from `https://github.com/GhostFenixx/svm-csharp`). | One UI for raid settings nobody wants to hand-edit in JSON. | verify in-game |
| **Fika** | both (`user\mods\fika-server\` server-side) | Co-op. The install is named `...-COOP-LAN`, so a co-op server mod is expected. | LAN co-op is in the folder name. | verify in-game |
| **UnityToolkit** | client | Shared library. SWAG + Donuts 4.0.0 lists **UnityToolkit V1.2.0** as required (verified on sp-mod.com). | Dependency of the spawn stack. | verify in-game |
| **RAM Cleaner Fix** | client | Forces the memory cleanup the in-game option only does in the menu. Community standard on 16 GB. | 16 GB RAM budget. | verify in-game |
| **Performance Improvements** | client | Community reports of smoother AI-spawn frames on 3.10. | Same 16 GB reason. | verify in-game |
| **Late to the Party** | client | Re-spawns bosses/raiders later in a raid. | Alive raids. | verify in-game — **also reported as a memory-leak suspect**; see `performance-tuning.md` |
| **Item/UI QoL** (MoreCheckmarks, Better Keys NG, and friends) | client | Inventory and quest readability. | Light questing. | verify in-game |

## Tier C — the other ~110 mods: enumerate them from disk

This is the part only his machine can answer. Run these in **PowerShell** with the server
and game **closed**, and keep the output in the skill's ignored `data\` folder.

Server mods, with the version fields the loader itself reads:

```powershell
$root = 'C:\games\SPT-TARKOV-3105-COOP-LAN'
Get-ChildItem -Path "$root\user\mods" -Directory | ForEach-Object {
    $pkg = Join-Path $_.FullName 'package.json'
    if (Test-Path $pkg) {
        $json = Get-Content $pkg -Raw | ConvertFrom-Json
        [pscustomobject]@{
            Folder    = $_.Name
            Name      = $json.name
            Version   = $json.version
            SptVer    = $json.sptVersion
            Deps      = ($json.modDependencies.PSObject.Properties.Name -join ', ')
            LoadAfter = ($json.loadAfter -join ', ')
        }
    } else {
        [pscustomobject]@{ Folder = $_.Name; Name = '(no package.json - not a server mod)'
                           Version = ''; SptVer = ''; Deps = ''; LoadAfter = '' }
    }
} | Sort-Object Name | Format-Table -AutoSize
```

Client plugins:

```powershell
$root = 'C:\games\SPT-TARKOV-3105-COOP-LAN'
Get-ChildItem -Path "$root\BepInEx\plugins" -Recurse -Include *.dll |
    Select-Object @{n='Plugin';e={$_.FullName.Replace("$root\",'')}},
                  @{n='KB';e={[math]::Round($_.Length/1KB,1)}} |
    Sort-Object Plugin | Format-Table -AutoSize
```

Prepatchers and BepInEx configs, the two places that silently break things:

```powershell
$root = 'C:\games\SPT-TARKOV-3105-COOP-LAN'
Get-ChildItem -Path "$root\BepInEx\patchers" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
Get-ChildItem -Path "$root\BepInEx\config" -Filter *.cfg | Select-Object -ExpandProperty Name
```

Save the output next to this skill as `data\inventory-YYYYMMDD.txt` — `data\` is gitignored,
so a dump of someone's install never lands in the repository.

### The counts to reconcile

| What the user said | What the enumeration should show |
|---|---|
| ~47 server mods | the number of `user\mods` sub-folders that contain a `package.json` |
| ~79 client plugins | the number of `.dll` files under `BepInEx\plugins` |

If the numbers disagree, the difference is usually one of: a mod that ships **both** sides
(counted once as a mod, twice as files), a leftover folder with no `package.json`, or a
plugin folder holding more than one DLL.

---

## Filling in the worksheet

Once the inventory is on disk, each mod gets one row. Copy this block per mod:

```markdown
| <Mod name> | server \| client | <install path> | <one-line job> | <why he keeps it> | <version or *verify in-game*> | <config path or "F12 menu"> |
```

Order the rows by **blast radius**, not alphabetically:

1. spawn managers (SWAG, Donuts, and anything else that touches spawns),
2. bot brains (SAIN, Questing Bots, Looting Bots, BigBrain, Waypoints),
3. progression/loot (ALP, loot mods),
4. server values (SVM, raid-setting mods),
5. co-op (Fika),
6. UI/QoL,
7. everything else.

## Known-friction pairs (check these first when something feels wrong)

| Pair | What happens | Rule |
|---|---|---|
| Two bot-progression mods (Valen's / APBS / ALP) | bots get contradictory loadouts; community reports also name ALP as a **boss-spawn** breaker | keep exactly one — the SPT wiki says so too |
| Two spawn managers (SWAG + Donuts vs. MOAR vs. Better Spawns Plus) | double spawns, or a map that never finishes loading | keep exactly one |
| **AI Limit + Questing Bots** | AI Limit freezes bots that are mid-quest | Questing Bots documents this as incompatible; use its own AI limiter instead |
| **SVM spawn settings + SWAG/Donuts** | spawn changes made in SVM are overridden by the spawn mod | change spawn numbers in the spawn mod |
| **Old preset pack + newer SWAG build** | configs missing fields the new build reads → the `/client/locations` hang in `troubleshooting.md` | a preset must match the SWAG major version it was written for |
| **Client HUD mods + 16 GB RAM** | reported memory leaks that page the system | see `performance-tuning.md` |

## Related pages

- `load-order-guide.md` — who wins when two of these mods want the same setting.
- `troubleshooting.md` — what to do when a preset pack breaks the raid.
- `performance-tuning.md` — which of these mods cost the most frame time.
- `backup-restore.md` — how to snapshot this inventory before changing it.
- `mod-install-workflow.md` — the gate a new mod has to pass to join this list.
- `server-config.md` — where SVM and the server configs sit in the same picture.

## Verify-in-game list

- The exact folder names in `user\mods` and `BepInEx\plugins` for all eight core mods.
- Whether `user\mods\SWAG\config\config.json` carries per-map `MaxBotCap` /
  `NightMaxBotCap` in the installed SWAG version.
- Whether Donuts in this install keeps its scenario caps in
  `BepInEx\plugins\dvize.Donuts\ScenarioConfig.json` (verified by the Fika wiki and
  community posts) or elsewhere.
- The real server-mod and client-plugin counts, once the enumeration above has run.
- Which bot-progression mod is installed, and that only one is.
