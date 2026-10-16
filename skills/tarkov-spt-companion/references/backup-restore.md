# Backup and restore — profiles, mod sets, and never extracting over an install

**What this page is.** What to copy before touching a ~120-mod SPT **3.10.5** install,
where each thing lives, how often, and how to put it back without turning a small problem
into a reinstall. The rule that gives the page its name: **you never extract an archive over
a working install.**

---

## Grounding

| Tag | Meaning |
|---|---|
| **verified** | read from `https://github.com/sp-tarkov/wiki`, `https://sp-mod.com`, or a mod's GitHub repository |
| **reported** | community practice |
| **judgement** | this page's suggested schedule and layout |
| **verify in-game** | confirm the path exists on his disk |

Paths are relative to `C:\games\SPT-TARKOV-3105-COOP-LAN`.

| Thing | Path | Why back it up |
|---|---|---|
| **Profiles** | `user\profiles\*.json` | the save files. Everything he has earned is in here, and nothing else on this list is irreplaceable. |
| **Server mods** | `user\mods\` | ~47 folders, each with a hand-tuned config. Re-downloading them is easy; re-tuning them is not. |
| **Server configs** | `SPT_Data\Server\configs\` | `core.json`, `http.json`, `gameplay.json`, `inraid.json`, `insurance.json`, `location.json`, `ragfair.json`, `trader.json`, `weather.json` |
| **Client plugins** | `BepInEx\plugins\` | ~79 DLLs plus the folders that hold their F12 presets and configs |
| **Prepatchers** | `BepInEx\patchers\` | rare, and easy to forget — a missing prepatcher looks exactly like a broken plugin |
| **BepInEx configs** | `BepInEx\config\` | one `.cfg` per plugin GUID: the settings the F12 menus wrote |
| **Edited database files** | `SPT_Data\Server\database\` | only if he edited them by hand |
| **SVM** | `user\mods\[SVM] ServerValueModifier\Presets\` + `loader.json` | the preset is the configuration; `loader.json` says which one is live (verified from `https://github.com/GhostFenixx/svm-csharp`) |

**Not worth backing up:** `BepInEx\cache\`, `BepInEx\interop\`, and other generated folders —
they rebuild themselves.

## The one rule: never extract over an existing install

Extracting a mod archive on top of a live install does not replace the target — it **merges**
into it. Whatever the new version removed stays behind as a stale file, and stale files are
how you get a second config folder, an old DLL that still loads, and the
`TypeError: Cannot read properties of undefined` family of errors in `troubleshooting.md`.

Mod authors say this in their own install notes: the SWAG + Donuts release notes tell you to
**uninstall and delete all its files first**, and preset packs tell you to **delete the
target config folder** before extracting. That is not pedantry, it is the fix.

**The correct sequence, every time:**

1. Stop the server and close the game.
2. Back up whatever you are about to touch (`user\profiles` at minimum).
3. **Delete or rename the target folder** in the install — do not merge into it.
4. Extract the new files to a **staging folder** outside the install.
5. **Copy** the staged files in.
6. Start the server, read the console, then test on Factory.

## Backup procedure

### Tier 1 — profile only (30 seconds, before any change)

```powershell
$root  = 'C:\games\SPT-TARKOV-3105-COOP-LAN'
$dest  = 'D:\SPT-backups'
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
New-Item -ItemType Directory -Path "$dest\profile-$stamp" -Force | Out-Null
Copy-Item "$root\user\profiles\*" -Destination "$dest\profile-$stamp\" -Recurse -Force
```

Run this before **every** mod change. It is the only backup that is never a waste.

### Tier 2 — full mod backup (before anything structural)

```powershell
$root  = 'C:\games\SPT-TARKOV-3105-COOP-LAN'
$dest  = 'D:\SPT-backups'
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
$snap  = "$dest\full-$stamp"

New-Item -ItemType Directory -Path $snap -Force | Out-Null
foreach ($p in 'user\mods', 'user\profiles', 'SPT_Data\Server\configs',
                'BepInEx\plugins', 'BepInEx\patchers', 'BepInEx\config') {
    $target = Join-Path $snap $p
    New-Item -ItemType Directory -Path $target -Force | Out-Null
    Copy-Item "$root\$p\*" -Destination $target -Recurse -Force
}

Get-ChildItem "$root\user\mods" -Directory | ForEach-Object {
    $pkg = Join-Path $_.FullName 'package.json'
    if (Test-Path $pkg) {
        $j = Get-Content $pkg -Raw | ConvertFrom-Json
        "{0}`t{1}`t{2}" -f $_.Name, $j.name, $j.version
    }
} | Out-File "$snap\mod-versions.txt" -Encoding utf8
```

`mod-versions.txt` is the part that pays off later: after an update breaks something, it is
the list of exactly what you had, not what you remember having.

### Tier 3 — whole install (rare, and worth it before a big change)

Copy the entire install folder to another drive. It is large and slow, so this is for "I am
about to do something I cannot undo" — not for routine changes.

## Rotation (judgement)

| Keep | Why |
|---|---|
| The **last known-good** full snapshot | the one you can always go back to — label it, and never overwrite it |
| The **3 most recent** full snapshots | enough history to find when something changed |
| Profile snapshots | keep them all until the drive complains; they are small |

Layout:

```
D:\SPT-backups\
├── KNOWN-GOOD-2026-10-01\
├── full-20261016-1430\
├── full-20261009-2010\
└── profile-20261016-1400\
```

## Restore — the safe workflow

### Restoring a profile

1. Stop the server and close the game. **Both.** Restoring under a running server is how
   profiles get half-written.
2. Rename the current `user\profiles` to `user\profiles.broken` — do not delete it until the
   restore is confirmed working.
3. Copy the profile JSONs from the backup into `user\profiles\`.
4. Start the server and watch the console. Load the profile in the launcher.
5. Check: stash contents, money, trader standing, quest states.
6. Only then delete `user\profiles.broken`.

### The trap: restoring a profile under a changed mod set

A profile that contains **items from a mod that is no longer installed** can fail to load.
The SPT server has switches for exactly this in **`SPT_Data\Server\configs\core.json`**:

| Key | What it does |
|---|---|
| `removeModItemsFromProfile` | when `true`, the server strips items belonging to mods that are no longer installed |
| `removeInvalidTradersFromProfile` | when `true`, it drops traders from missing mods |

(Verified from the descriptions published for these keys by SPT tooling; **verify in-game**
that both keys are present in this install's `core.json` before relying on them.)

Order of preference:

1. **Best:** restore the mod set **and** the profile from the same snapshot, so they match
   again.
2. **Acceptable:** flip those two keys on, start the server once, let it clean the profile,
   then consider turning them back off.
3. **Last resort:** restore an older profile and lose the progress since.

### Restoring a mod set

1. Stop the server and close the game.
2. **Do not extract the backup archive over the install.** Extract it to a staging folder.
3. In the install, **rename** `user\mods` → `user\mods.old` (and `BepInEx\plugins` →
   `BepInEx\plugins.old` if you are restoring client plugins too).
4. Copy the staged folders in.
5. Start the server, read the console, confirm the mod count.
6. Raid **Factory**. Then delete the `.old` folders.

### Restoring a single mod

Never restore one mod by merging its folder back in. Delete the installed folder first, then
copy the backed-up folder in. Same rule as installing: the operation is *replace*, never
*merge*.

## After any restore — the verification checklist

- [ ] Server console lists the expected number of mods, with no refusal lines.
- [ ] A Factory raid loads and finishes.
- [ ] The profile opens: stash, money, traders, quests all present.
- [ ] One bigger map loads (whatever he plays most).
- [ ] The F12 menus for SAIN / Donuts / Questing Bots open and show values.
- [ ] A **fresh backup** of the now-working state exists.

## Related pages

- `troubleshooting.md` — the errors that make a restore necessary in the first place.
- `mod-install-workflow.md` — the install rule that this page's "never extract over" comes from.
- `server-config.md` — the config files worth backing up, and the two `core.json` switches.

## Verify-in-game list

- That `user\profiles` really is where this install keeps its saves (it is the SPT 3.10
  layout — confirm before trusting a backup that was never restored).
- Which drive and folder he wants backups on. `D:\SPT-backups` above is a placeholder.
- That `core.json` in this install carries both cleaning keys under those exact names.
- The size of a full snapshot on his disk, before scheduling one nightly.
