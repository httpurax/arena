# Troubleshooting — the hang, the TypeError, the two Donuts, and the old preset

**What this page is.** The failure modes this install actually hits, in the order to check
them: the raid that never starts while the server sits on a `/client/locations` request,
the `TypeError: Cannot read properties of undefined` console spam, a Donuts install that
has grown a second config folder, configs that stopped matching what the mod expects, and
the isolation workflow that finds which of ~120 mods did it.

**Where to look first, every time:** the **server console window**, not the game. When the
client is stuck on a loading screen, the server is the side that has stopped answering.

---

## Grounding

| Tag | Meaning |
|---|---|
| **verified** | read from `https://sp-mod.com`, `https://github.com/dvize/Donuts`, `https://github.com/dwesterwick/SPTQuestingBots`, or the SPT wiki while this skill was built |
| **reported** | community reports (Reddit / mod-page comments) — real, but not reproduced here |
| **judgement** | the order this page suggests trying things in |
| **verify in-game** | confirm on his disk before acting |

No version numbers or URLs appear here that were not read from those sources.

## Log and evidence locations

| What | Where (relative to `C:\games\SPT-TARKOV-3105-COOP-LAN`) | Notes |
|---|---|---|
| Server console | the `SPT.Server.exe` window | **the first place to look**, always |
| Client plugin log | `BepInEx\LogOutput.log` | BepInEx writes every plugin load and exception here |
| Unity player log | `%USERPROFILE%\AppData\LocalLow\Battlestate Games\EscapeFromTarkov\Player.log` | crashes and hard locks |
| BepInEx configs | `BepInEx\config\*.cfg` | one file per plugin GUID |
| Server mod manifests | `user\mods\*\package.json` | `sptVersion` tells you if the mod belongs on 3.10.5 |
| Server configs | `SPT_Data\Server\configs\` | see `server-config.md` |

**verify in-game:** whether this install also drops a rolling server log file, and where —
check both `user\logs` and `logs` under the install root.

---

## Failure 1 — the `/client/locations` hang

### The shape of it

1. Pick a map, start the raid.
2. The client sits on a loading screen indefinitely — no crash, no error dialog, just an
   endless wait.
3. The server console shows the client's request for **`/client/locations`** and either an
   exception above it or nothing at all afterwards.

`/client/locations` is the request the client makes to get the map's generated data. Server
mods hook into that generation. So a hang there means: **a server mod threw, or is looping,
while the map is being prepared.** The client is innocent.

### What causes it, in the order to check

| # | Cause | How to confirm | Fix |
|---|---|---|---|
| 1 | A **spawn preset that does not match the installed SWAG build** (the TrueLive pattern) | the newest thing you changed was a preset pack; the console names a JSON file under `user\mods\SWAG\config\` | remove the preset, restore the SWAG config you had before, or reinstall SWAG clean |
| 2 | **Two spawn managers** both generating for the same map | two folders in `user\mods` that both manage spawns | keep one (see `load-order-guide.md`, Rule 1) |
| 3 | A server mod whose `sptVersion` is not 3.10.x | `user\mods\*\package.json` | remove that mod |
| 4 | A **config schema mismatch** — an edited JSON missing a field the new build reads | the console error names a property that does not exist in your file | delete the config and let the mod regenerate defaults (Failure 4) |
| 5 | Boss/other spawn JSONs carrying values the build no longer accepts | error names `user\mods\SWAG\config\bosses\` or `config\other\` | restore those files from a known-good backup |

### The TrueLive pattern, spelled out

**TrueLive** (by matsix) is a **Donuts + SWAG config preset pack**, not a mod: it is a
*dependency* of SWAG + Donuts, and installing it means overwriting the spawn configs with
someone else's. Two things about it matter here:

- The build that was published and discussed during research was written for **SPT 3.9.x**,
  with the author saying a 3.10 version would follow once Donuts for 3.10 shipped. **A
  3.9-era preset on a 3.10.5 install is exactly the mismatch that produces this hang** —
  and it is why the user's hard rule about checking the Versions tab exists.
- The same project shipped a real preset-level duplicate bug: two Ground Zero files were
  both named `sandbox` instead of one being `sandbox_high`, which **doubled the SCAV count**
  on that map. That is the class of bug "a preset I did not write" brings with it.

**Rule this page draws from that:** a preset pack is a *code change wearing a config's
clothes*. Treat it like a mod install — back up first, test on Factory, know how to undo it.

### First response checklist (do these in order)

1. Read the **server console** and copy the first error, not the last.
2. `Ctrl+C` out of the server, close the game.
3. Disable the **most recently changed** spawn-related mod by renaming its folder in
   `user\mods` (or its `package.json`) — do not delete it yet.
4. Start the server alone and watch for load errors.
5. Launch the game, raid **Factory**, same settings.
6. If it loads, the disabled mod is the culprit: restore *its* config from a known-good
   backup, or reinstall it clean (Failure 4).
7. If it still hangs, go to the isolation workflow below.

---

## Failure 2 — `TypeError: Cannot read properties of undefined`

The SPT server is a Node/TypeScript process, so server mods fail with JavaScript errors.
This one means: **the mod read a property off something that was not there.**

```
TypeError: Cannot read properties of undefined (reading 'someField')
```

In practice, on this install, it is one of three things:

| Cause | Tell | Fix |
|---|---|---|
| **A config file missing a field the current build expects** (old preset, hand-edited JSON, a config carried over from an older version) | the error appears right after the mod loads, or when a raid starts | **delete the config file and restart the server** — SPT server mods regenerate a default config on start. Then re-apply your edits one at a time. |
| **A mod reading data another mod removed or renamed** | it started right after a mod update | update or remove the older of the two; the error's stack trace names the file |
| **A mod built for a different SPT version** | `sptVersion` in `package.json` is not 3.10.x; the error names a server API that moved | remove the mod |

### The three-step fix that works most of the time

1. **Find the file.** The stack trace names a path under `user\mods\<ModFolder>\`. That
   folder is the suspect — not the game, not BepInEx.
2. **Regenerate its config.** Stop the server. Rename the mod's config file (or the whole
   `config` folder) to `*.bak`. Start the server: the mod writes a fresh default. If the
   error is gone, the config was the problem.
3. **Re-apply edits one key at a time**, restarting the server between each, until it breaks
   again. The last key you added is the one the build no longer accepts.

Copy the whole console block — including the stack — into `data\` before you start. When
the fix works, you will want to know what it said.

---

## Failure 3 — the dual Donuts folder

### What it looks like

- Donuts settings changed in the **F12** GUI do not stick, or the raid behaves as if your
  change never happened.
- Spawn numbers look **doubled** on one map.
- There are two folders that both look like Donuts, or a `Config` folder that nothing
  reads.

### Why it happens

Donuts is a **client** plugin whose data lives beside the DLL:

```
BepInEx\plugins\dvize.Donuts\                 # the plugin folder
BepInEx\plugins\dvize.Donuts\Config\          # its config folder
BepInEx\plugins\dvize.Donuts\ScenarioConfig.json   # scenario caps (PMC / SCAV per scenario)
BepInEx\config\com.dvize.Donuts.cfg           # the BepInEx .cfg
```

(The `...\dvize.Donuts\Config\` and `ScenarioConfig.json` paths are **verified** — Fika's
headless-client documentation says Donuts settings are stored in
`BepInEx/plugins/dvize.Donuts/Config`, and preset-pack release notes tell installers to
delete exactly that `Config` folder before an upgrade.)

Now add how things get installed: preset packs and older releases are zipped with their own
folder trees and are meant to be dropped on the install root. Do that twice, or from two
different versions, and you get **a second Donuts directory** — one the plugin loads and one
you are editing. The `dvize/Donuts` repository even carries a commit named *"Fix Duplicate
Folders"*, which tells you how common the shape is.

### The fix

1. Close the game **and** the server.
2. Search the install for every Donuts directory:

   ```powershell
   $root = 'C:\games\SPT-TARKOV-3105-COOP-LAN'
   Get-ChildItem -Path $root -Recurse -Directory -Filter '*onuts*' |
       Select-Object -ExpandProperty FullName
   ```

3. Expect exactly **one** plugin folder under `BepInEx\plugins\`. Anything else — a second
   Donuts folder in `BepInEx\plugins\`, a stray one under `user\mods\`, a leftover from an
   older release — is the duplicate.
4. **Move** the duplicates out of the install into a staging folder. Do not delete anything
   you have not backed up.
5. Start the game, open the F12 Donuts section, change one value, and confirm it is still
   there after a reload. If it is, you are editing the folder the plugin reads.
6. If a preset pack is the reason you have two: reinstall it the way its own instructions
   say (delete the target config folder first, then extract), never by merging.

---

## Failure 4 — config schema mismatch from an old preset

The same story as Failure 2, seen from the config's side. Symptom: a config file works
until a mod update, then the mod either ignores it or throws on it.

**Why keeping the old file is not neutral.** A mod that cannot read a key has three
options — use a default, throw, or hang. On this install all three have been seen.

### The safe way to carry settings across an update

1. Back up the mod folder: copy `user\mods\<ModFolder>` to your backup location.
2. Read the mod's **changelog** on its sp-mod.com page or GitHub releases — the breaking
   changes are listed there. If the changelog says "delete your config", believe it.
3. Rename the old config (`config.json` → `config.json.old`).
4. Start the server and let the mod write a **fresh default**.
5. Diff old against new. Re-apply your values by hand, key by key, into the **new** file —
   never by copying the old file back over it.
6. Keys present in the old file and gone from the new one are the ones the build dropped.
   Stop setting them.

Preset packs get the same treatment, with one extra rule: a preset must match the **major
version** of the mod it was written for. A preset written for an older SWAG/Donuts line is
not a config, it is a downgrade.

---

## The isolation workflow

Use this when the console does not name the culprit, or when two mods are plausible.

### Before you start

- [ ] Stop the server and close the game.
- [ ] Back up `user\profiles` (see `backup-restore.md`).
- [ ] Open a scratch file and write down today's date and what you are about to disable.

### Step 1 — reproduce and capture

Start the server, launch the game, and reproduce the fault **on Factory**. Copy the full
server console output and the tail of `BepInEx\LogOutput.log` into your scratch file.

### Step 2 — split the suspects

| Fault | Start with |
|---|---|
| Raid never starts / server error | `user\mods` (server side) |
| Crash, black screen, F12 menu missing | `BepInEx\plugins` (client side) |
| Both, or unsure | server side — it is faster to eliminate and the client cannot load without it |

### Step 3 — bisect (do not disable one at a time)

1. List the folders in `user\mods`.
2. Disable **half** of them by renaming the folders (`SWAG` → `SWAG.off`).
3. Test on Factory.
   - **Fixed?** the culprit is in the disabled half.
   - **Still broken?** the culprit is in the enabled half; re-enable the first half and
     disable the other.
4. Repeat, halving each time. ~47 server mods is **6 rounds or fewer**; ~79 client plugins
   is 7.

Bisecting is the whole trick: testing one mod at a time is ~47 raids, testing halves is 6.

### Step 4 — confirm and decide

- Re-enable everything except the one suspect and confirm the fault is gone.
- Re-enable the suspect alone and confirm the fault returns. Now you know.
- Decide: **reinstall it clean** (delete the folder, extract fresh — never over the top),
  **roll back a version**, or **drop it**. Record which.

### Step 5 — put the install back

Rename every `.off` folder back, start the server, and confirm the console lists the mod
count you expect. Then take a fresh backup — you now have a known-good state.

### The worksheet

```markdown
Date:
Symptom:
Map used to test: Factory
Server console (first error):
BepInEx\LogOutput.log (tail):
Round 1 — disabled: ...                     result: fixed / still broken
Round 2 — disabled: ...                     result: fixed / still broken
Culprit:
Fix applied:
Verified on (map, settings):
Backup taken after fix: yes / no
```

## Symptom → first check (quick table)

| Symptom | Look at first |
|---|---|
| Endless loading into a raid | server console, then the newest spawn mod/preset |
| `TypeError: Cannot read properties of undefined` | the named mod's config file |
| Donuts settings will not stick | duplicate Donuts folders |
| Double bots on one map | two spawn managers, or a preset with duplicated map entries |
| Bosses never spawn | a broken progression mod (community-reported for ALP) and `user\mods\SWAG\config\bossConfig.json` |
| Bots spawn in front of you | spawn-point data, and Questing Bots' minimum spawn distance |
| Stutter on raid start | `performance-tuning.md`, not this page |
| Profile will not load | `backup-restore.md` — a mod that was removed took its items with it |

## Related pages

- `load-order-guide.md` — how to disable a mod cleanly while bisecting.
- `performance-tuning.md` — when the symptom is stutter rather than a hang.
- `backup-restore.md` — the backup every step above assumes you took.
- `mod-install-workflow.md` — how the change that broke it should have been installed.
- `server-config.md` — the config files a fix may have to restore.

## Verify-in-game list

- Whether this install keeps a rolling server log file, and in which folder.
- The exact Donuts folder name the installed build uses before deleting a duplicate.
- Which SWAG version is installed, before trusting any preset pack's compatibility claim.
- Whether the error you are chasing is server-side (TypeScript/Node stack) or client-side
  (C# stack in `BepInEx\LogOutput.log`) — the two never mix.
