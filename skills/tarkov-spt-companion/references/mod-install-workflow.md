# Mod install workflow — evaluate, verify, install, Factory-test, roll back

**What this page is.** The gate every **new** mod has to pass before it touches
`C:\games\SPT-TARKOV-3105-COOP-LAN`. It exists because this install is already ~120 mods
deep: at that size, adding one wrong thing costs hours, and the cost is paid in
troubleshooting time rather than in download time.

**The two rules that shape the whole page:**

1. **New mods are server-side only.** They go in `user\mods`. No new BepInEx client DLLs.
2. **Sources are `https://sp-mod.com` and GitHub releases only.** The old Forge domain is
   dead; anything else — repacks, re-uploads, video descriptions, "mirror" links — is out.

---

## Grounding

| Tag | Meaning |
|---|---|
| **verified** | read from `https://sp-mod.com`, `https://github.com/sp-tarkov/wiki`, or a mod's GitHub repository |
| **reported** | community practice |
| **judgement** | this page's ordering and its reject list |
| **verify in-game** | confirm on his disk / in the game |

## Step 0 — source check (30 seconds, kills most bad mods)

| ✔ | Check | Reject if |
|---|---|---|
| ☐ | Downloaded from **sp-mod.com** or the mod's **GitHub releases** page | anywhere else. **Repacks and "all-in-one" archives are auto-rejects** — you cannot audit what is inside them, and they are built for someone else's install. |
| ☐ | The page names **SPT 3.10.x** compatibility | it only lists 3.9.x, 3.11.x, or 4.x |
| ☐ | The page has a maintainer and a changelog | it is a re-upload with no author and no history |
| ☐ | The file is the author's release, not a re-zipped copy | the archive contains files the mod does not need |

## Step 1 — version check: the Versions tab is the whole test

On sp-mod.com each mod has a **Versions** tab listing every published build with the SPT
version it targets. That tab is the authority — not the mod's title, not a compatibility
note in a comment, not the date.

- Pick the build whose **SPT version is 3.10.x**, ideally explicitly **3.10.5**.
- "3.10.x ONLY" means do not carry it forward — which is fine here, 3.10.5 is the
  destination.
- A mod whose newest build predates 3.10 is **not** a candidate. Waiting is a valid outcome.
- **Never invent or assume a version.** If the Versions tab does not show a 3.10.x build,
  the answer is "not yet", and the line you give the user is *verify in-game* / check back
  later.

Then confirm it on disk after install: `user\mods\<ModFolder>\package.json` →
`sptVersion` should read **3.10.x**. That manifest is what the loader believes, and it beats
any web page.

## Step 2 — side check: is it server-side only?

Open the archive **before** extracting anything.

| Archive contains | Verdict |
|---|---|
| `user\mods\<Folder>\` with a `package.json` at its root | **server mod** — this is what you want |
| `BepInEx\plugins\*.dll` (and nothing under `user\mods`) | **client plugin** — reject by this install's rule |
| Both | **reject**, unless the client half is a dependency the user already has installed and is simply being re-shipped. A mod that needs a new client DLL is not a server-side mod. |
| Just a `config` folder and JSON files | **a preset/config pack**, not a mod — it goes through the preset rules in `troubleshooting.md` (Failure 4) and is tested like a mod |

The official split, for the avoidance of doubt (verified from the SPT wiki's
`Mod_Types.md`): server mods → `user\mods`, client mods → `BepInEx\plugins`, prepatchers →
`BepInEx\patchers`.

## Step 3 — dependency check

- Read **Required Dependencies** on the mod page. For this stack, the recurring ones are
  **BigBrain**, **Waypoints**, and (for SWAG + Donuts) **UnityToolkit** — SWAG + Donuts 4.0.0
  lists UnityToolkit V1.2.0 and Waypoints as required.
- After install, `package.json`'s `modDependencies` tells the loader the same thing. A
  missing dependency is not a subtle bug: the server prints it and skips the mod.
- If a dependency is a **client** mod you do not already have, stop — that is Step 2's rule
  again, wearing a different hat.

## Step 4 — conflict check against the stack

Run the new mod against the friction table in `mod-catalog.md`:

- Is it a **second bot-progression mod**? (ALP is the one in this install.)
- Is it a **second spawn manager**?
- Is it an **AI limiter**? (incompatible with Questing Bots)
- Does it claim settings SVM or the spawn mods already own? (`load-order-guide.md`, Rule 3)

One more, specific to this install: **Questing Bots auto-disables its own initial-PMC
spawning when it detects SWAG + Donuts** (verified in its README). A new mod that also wants
to spawn bots is stepping on that.

## Step 5 — back up

Minimum: `user\profiles` (Tier 1 in `backup-restore.md`). If the mod touches spawning or
server values, take a **full snapshot** (Tier 2) so you have a real way back.

## Step 6 — install (replace, never merge)

1. Stop the server and close the game.
2. Extract the archive to a **staging folder outside the install** — never on top of it.
3. In the install, **delete or rename** the target folder if one exists.
4. **Copy** the staged folder into `user\mods\`.
5. Start `SPT.Server.exe` and **read the console**: mod found, dependencies satisfied, no
   `TypeError`.
6. Launch the game and check the mod's F12 section exists (server mods with a client-facing
   menu) or that its config folder was generated.

## Step 7 — the Factory test

Factory is the smallest map and the fastest load, so it gives the quickest verdict on the
thing that actually matters: *does the server still build a raid?*

| ✔ | Check |
|---|---|
| ☐ | Raid **loads** (no `/client/locations` hang — `troubleshooting.md`, Failure 1) |
| ☐ | Server console is clean for the whole raid |
| ☐ | Bots spawn, and the count looks like what the mod promised |
| ☐ | You can extract, and the raid **ends** |
| ☐ | Profile saved afterwards without errors |
| ☐ | Frame time is still acceptable (16 GB — watch it, per `performance-tuning.md`) |

Then repeat on **one bigger map** he actually plays. A mod can pass Factory and still fall
over on a map with more spawn data.

## Step 8 — record it

Add a row to the catalog worksheet in `mod-catalog.md`: folder, side, version from
`package.json`, config path, why it is there, and the date. Six months later this row is the
only thing that will tell him why the mod is installed.

## Rollback — three levels, cheapest first

| Level | When | How | Cost |
|---|---|---|---|
| **1. Disable** | you are not sure yet | rename the mod folder in `user\mods` (or its `package.json`) | nothing — settings survive |
| **2. Reset the config** | the mod loads but misbehaves | rename its config file/folder, restart the server so it regenerates a default, re-apply edits one key at a time | your tuning |
| **3. Remove and restore** | the install is broken | delete the mod folder, then restore `user\mods` (and if needed `user\profiles`) from the snapshot in Step 5 | back to the pre-install state |

**Rollback is only real if Step 5 happened.** No backup, no rollback — just recovery.

## Red flags — reject without testing

- **Any new client DLL** for this install (the user's rule, not a suggestion).
- A build whose `sptVersion` is not 3.10.x.
- A mod that requires you to **overwrite files you did not back up**.
- A preset pack whose own instructions say "delete X first" and you have not backed up X.
- Two mods that both manage spawning, both manage bot progression, or both limit AI.
- A "performance" mod that promises a frame-rate number. Nobody can promise that about
  someone else's machine.

## The worksheet

```markdown
Mod:
Source (sp-mod.com / GitHub releases URL):
Versions tab -> SPT build chosen:
Server-side only? yes / no   (reject if no)
package.json sptVersion after install:
Dependencies:                Satisfied? yes / no
Conflicts checked against:   progression / spawning / AI limit / SVM
Backup taken:                profile only / full snapshot  (path:)
Installed to:                user\mods\<folder>
Factory raid:                load / bots / extract / console  -> pass / fail
Second map (name):           pass / fail
FPS / memory note (judgement, no numbers promised):
Rolled back?                 no / level 1 / 2 / 3
Catalog row added:           yes / no
```

## Related pages

- `backup-restore.md` — Steps 5 and 9, and the rollback levels, in full.
- `load-order-guide.md` — the one-mod-per-job rules used by the conflict check.
- `mod-catalog.md` — where a mod that passes gets recorded.
- `troubleshooting.md` — what to do when the Factory test fails.
- `performance-tuning.md` — judging the FPS/mem line in the worksheet honestly.

## Verify-in-game list

- The exact `sptVersion` string in the installed `package.json` — the page can be wrong, the
  manifest is what the loader reads.
- Whether the mod's F12 section exists in this install (server mods vary).
- Bot counts on the second map, not just Factory — Factory is too small to prove much.
- Whether the mod wrote a config folder on first start, and where.
