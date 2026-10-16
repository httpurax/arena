# Server config — `SPT_Data\Server\configs`, SVM, and raid settings

**What this page is.** The server-side knobs that matter for this SPT **3.10.5** install:
which file holds what, the two `core.json` switches that rescue a profile, how LAN co-op
addressing works, and how **SVM** (Server Value Modifier) fits on top of all of it.

Paths are relative to `C:\games\SPT-TARKOV-3105-COOP-LAN`.

---

## Grounding

| Tag | Meaning |
|---|---|
| **verified** | read from `https://github.com/GhostFenixx/svm-csharp`, SPT server tooling, or the SPT wiki |
| **reported** | community / hosting-provider documentation |
| **judgement** | this page's advice on which file to open first |
| **verify in-game** | confirm the file and key exist in this install before editing |

- **Server configs live in `SPT_Data\Server\configs\`** on 3.10.x. (Later SPT versions moved
  them; the 3.x `Aki_Data` path is gone. **verify in-game** that the folder is where this
  page says on his install.)
- **The server must be stopped before editing any of these files.** The server reads them at
  start; an edit made while it runs is either ignored or overwritten when it writes back.
- **Keep a copy beside each file you edit.** SPT tooling does exactly this — it writes the
  new value while leaving the original next to it. It is the cheapest insurance in this
  document.

## The config files

| File | What it holds | Notes |
|---|---|---|
| `core.json` | core server settings: the SPT version string, server name, and the profile-cleaning switches below | the one to open when a **profile will not load** |
| `http.json` | `ip`, `backendIp`, `port` — the addresses the server binds and the client is told to use | the one to open for **LAN co-op** |
| `gameplay.json` | gameplay-side modifiers | *reported* as holding raid-time and extraction-style settings — **verify in-game** against the installed file |
| `inraid.json` | in-raid behaviour, including save behaviour | **verify in-game** |
| `insurance.json` | insurance return times and chances | — |
| `location.json` | per-map settings | *reported* to carry raid timers and loot multipliers per location — **verify in-game** |
| `ragfair.json` | flea market: prices, offer behaviour | — |
| `trader.json` | trader restock and purchasing | — |
| `weather.json` | weather and time of day | — |

(The file list and rough responsibilities are as documented by SPT hosting documentation and
server tooling; **verify each file exists** in this install before editing — a version's file
set is not guaranteed.)

## `http.json` — LAN co-op addressing

The install is named `...-COOP-LAN`, so the server has to be reachable from another machine
on the LAN. The keys are `ip`, `backendIp`, and `port`.

| Situation | What to set |
|---|---|
| Solo, single machine | leave the loopback defaults alone |
| **LAN co-op** | `ip` and `backendIp` set to the host machine's **LAN address** (or `0.0.0.0` to listen on every interface), and the client pointed at that address |

- The default server port is **6969** (verified from SPT server tooling).
- Setting the bind address to `0.0.0.0` is what server containers do to listen on all
  interfaces — it is a bind setting, not a client setting. The **client still has to be told
  the real LAN address**, in the launcher's server URL.
- After changing this: restart the server, then confirm from the **other** machine, not the
  host. Both machines must run the same mod set for co-op to behave.

## `core.json` — the two switches that matter most

| Key | What it does |
|---|---|
| `sptVersion` | the SPT version the server is — the value server tooling checks before it will touch anything. It should read **3.10.5** here. |
| `serverName` | the name shown to clients |
| `removeModItemsFromProfile` | when `true`, the server **removes items from removed mods** out of profiles as they load |
| `removeInvalidTradersFromProfile` | when `true`, it drops **traders belonging to missing mods** |

Those last two are the recovery path for "my profile will not load since I took a mod out"
(verified from the descriptions published for these keys by SPT tooling; **verify in-game**
that both keys are present under those names in this install).

Workflow: back up `user\profiles` first, flip both to `true`, start the server once, let it
clean the profile, confirm it loads, then decide whether to leave them on. Details and the
safer alternatives are in `backup-restore.md`.

## SVM — Server Value Modifier

SVM is a **server** mod, which is why it survives this install's server-side-only rule.

| Path | What it is |
|---|---|
| `user\mods\[SVM] ServerValueModifier\` | the mod (verified from `https://github.com/GhostFenixx/svm-csharp`) |
| `user\mods\[SVM] ServerValueModifier\Presets\*.json` | the saved presets — this is where the settings actually live |
| `user\mods\[SVM] ServerValueModifier\loader.json` | names the **active** preset |
| `Greed.exe` (install root, beside `SPT.Server.exe`) | the Windows app that edits the presets |

How to use it:

1. Stop the server. Run `Greed.exe` from the install root.
2. Change what you want, **save it as a named preset** (do not overwrite the only preset you
   have), and apply it.
3. Confirm `loader.json` points at the preset you just saved.
4. Start the server and read the console.
5. Test on Factory.

SVM's own uninstall note (from its repository) is worth knowing: deleting the mod folder is
not always the whole job — if its optional **CSM** component was used, that also placed
`HideSpecialIcon.dll` in `BepInEx\plugins`. That is a **removal** note for an existing file,
not a licence to add new client DLLs.

## Who overrides whom

| Setting | Winner | Consequence |
|---|---|---|
| **Spawn numbers** | the spawn mod | SVM spawn/bot settings are overridden by SWAG + Donuts (*reported*; **verify in-game**). Change spawn counts in `user\mods\SWAG\config\config.json` and `BepInEx\plugins\dvize.Donuts\ScenarioConfig.json`, not in SVM. |
| **Bot gear / progression** | the progression mod (ALP) | SVM gear-side settings will not show through |
| **Raid timers, extracts, insurance, flea, skills** | SVM / the config files | this is SVM's home turf |
| **Everything, in co-op** | Fika's co-op settings | co-op-level limits cap what the mods below asked for |

Practical rule: **do not set the same value in two places.** If you set it in SVM, do not
also hand-edit it in `SPT_Data\Server\configs\` — you will not be able to tell which one won.

## For this playstyle (alive raids, gunplay + looting, light questing)

All judgement, all *verify in-game* — the point is where to look, not what to pick:

| Want | Where |
|---|---|
| Longer/shorter raids, extract availability | SVM, or `location.json` per map (**verify in-game**) |
| More loot on the map | the loot multipliers in the location/loot server config (SVM may expose them) |
| Loot that matters without grinding the flea | `ragfair.json` / SVM's flea section |
| Insurance that comes back | `insurance.json` / SVM |
| Fewer loading screens between raids | `performance-tuning.md` — that is a memory problem, not a config one |
| Extracts always available | SVM's extraction settings |

## Editing rules

1. **Stop the server.** Every time.
2. **Copy the file first** (`core.json` → `core.json.bak`).
3. Edit JSON carefully: **a trailing comma or a smart quote stops the server from starting**,
   and the error will not point at your typo.
4. Change **one** thing, restart, test on Factory.
5. If the server will not start after an edit, restore the `.bak` before debugging anything
   else.

## Related pages

- `backup-restore.md` — the profile-recovery path behind the two `core.json` switches.
- `load-order-guide.md` — why the spawn mods beat SVM's spawn settings.
- `performance-tuning.md` — raid settings that look like performance problems and are not.
- `mod-catalog.md` — where SVM and the spawn stack sit in the inventory.

## Verify-in-game list

- That `SPT_Data\Server\configs\` is the live config folder on this install, and which of
  the nine files are actually present.
- That `core.json` carries `removeModItemsFromProfile` and `removeInvalidTradersFromProfile`
  under those exact names.
- The installed SVM version's preset layout, and which preset `loader.json` currently names.
- Whether the co-op server mod in this install adds its own config folder alongside these
  (Fika's server config lives under its own `user\mods\fika-server\` folder in some
  installs — **verify in-game**).
