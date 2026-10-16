# Load order guide — BepInEx plugins, server mods, and who wins

**What this page is.** How the two independent loaders in this install decide what runs
when, what to do when two mods want the same thing, and how to take a mod out of the
picture without losing it. SPT 3.10.5 at `C:\games\SPT-TARKOV-3105-COOP-LAN`.

The one sentence to remember: **there are two loaders and they never see each other.**
`BepInEx` loads client plugins inside the game process. The SPT server loads
`user\mods` separately when `SPT.Server.exe` starts. Nothing you do to one changes the
other's order.

---

## Grounding

| Tag | Meaning |
|---|---|
| **verified** | from `https://github.com/sp-tarkov/wiki` (the official mod split), `https://sp-mod.com`, or a mod's GitHub repository |
| **judgement** | an inference — which conflict to suspect first, what order to try fixes in |
| **verify in-game** | confirm on his disk before acting |

- Server mods live in `user\mods`, client mods in `BepInEx\plugins`, and the rare
  prepatcher in `BepInEx\patchers` (verified: the official SPT wiki's `Mod_Types.md`).
- **No version numbers or URLs are invented here.** Where a version matters, this page names
  the file that states it (`package.json`, the mod page's Versions tab) rather than a number.

---

## Part 1 — the client side: BepInEx

### The order, as BepInEx 5 runs it

1. **`BepInEx\patchers\`** — prepatchers. They run *before* plugins and touch assemblies
   before plugin code exists. Very few mods ship one; if a mod does, it must stay there.
2. **`BepInEx\plugins\`** — the ~79 client plugins.
3. **Dependency order inside `plugins`.** BepInEx 5 sorts plugins by their
   `[BepInDependency]` declarations: a plugin that declares a dependency is loaded after
   the plugin it names. Dependency-less plugins fall back to the order the loader walks the
   directory in.

**There is no user-editable load-order file.** You cannot rename a plugin to `aaa-mod.dll`
and make it load first — that is a myth that survives because renaming *sometimes* appears
to work. Mod managers such as SSPTMM (on sp-mod.com) read the same `[BepInDependency]`
data straight out of the DLLs, which is the only reliable way to see the graph.

### What "load order" actually controls on the client

| Symptom | What it really is |
|---|---|
| A plugin's feature silently does nothing | it loaded but its dependency did not, or another plugin patched the same method later |
| The **F12** menu is missing an expected section | that plugin did not load — check `BepInEx\LogOutput.log` |
| Two mods both change the HUD and one "wins" inconsistently | two patches on the same method; which one lands is not something you can fix by reordering |
| Game hangs at the splash screen after adding a plugin | the new plugin, or a prepatcher placed in the wrong folder |

### Taking a client plugin out without deleting it

```
C:\games\SPT-TARKOV-3105-COOP-LAN\BepInEx\plugins\<PluginFolder>\
```

- **A lone DLL:** rename `ModName.dll` → `ModName.dll.disabled`. BepInEx only loads files
  ending in `.dll`.
- **A plugin folder:** rename the folder, or move it to a staging folder *outside* the
  install (never into another BepInEx subfolder — a stray DLL under `BepInEx\plugins` is
  still loaded).
- **A prepatcher:** same trick, in `BepInEx\patchers\`.

Leave `BepInEx\config\*.cfg` alone while a plugin is disabled; when you re-enable it, its
settings are still there.

## Part 2 — the server side: `user\mods`

### The order, as the SPT server runs it

Every server mod is a folder in `user\mods` containing a `package.json`. The loader reads
those manifests, then:

1. **resolves `modDependencies`** — a mod whose dependency is missing or too old is
   reported in the server console and skipped;
2. **applies `loadBefore` / `loadAfter`** — the two `package.json` fields that set relative
   order (verified from the loader behaviour described by SPT mod managers, which read
   `modDependencies` for server mods and `[BepInDependency]` for client mods);
3. loads everything else in whatever order the manifest walk produces.

**Watch the server console.** It prints the mods it found and the ones it refused. That
output is the ground truth for "did my mod load", not the mod list in the launcher.

### Reading one manifest

`user\mods\<ModFolder>\package.json` is the mod's identity card. The fields that matter for
ordering:

| Field | What it does |
|---|---|
| `name` | the loader's name for the mod |
| `version` | the **mod's** version — not SPT's |
| `sptVersion` | the SPT version the mod was built for. On 3.10.5 this should be a **3.10.x** string. |
| `modDependencies` | other server mods that must be present, and the version range |
| `loadBefore` / `loadAfter` | relative ordering hints |
| `main` | the entry file the loader executes |

A mod whose `sptVersion` is not `3.10.x` does not belong in this install — that is the
check in `mod-install-workflow.md`, step 2.

### Taking a server mod out without deleting it

Rename its folder (`SWAG` → `SWAG.off`) **or** rename its `package.json`
(`package.json` → `package.json.off`). Either one stops the loader from seeing a loadable
mod. Renaming the folder is the safer of the two, because it also stops the mod's other
files from being read.

---

## Part 3 — conflict resolution

### Rule 1: one mod per job

| Job | Keep exactly one | What happens with two |
|---|---|---|
| Bot spawn management | SWAG + Donuts **or** MOAR **or** Better Spawns Plus | double spawns, or a raid that never finishes loading |
| Bot gear progression | ALP **or** APBS **or** Valen's Progression | contradictory loadouts; community reports also tie a broken ALP to bosses not spawning |
| AI limiting | Questing Bots' own limiter **or** AI Limit | **AI Limit is documented as incompatible with Questing Bots** — it disables bots that are mid-quest. Use Questing Bots' built-in limiter. |
| Raid/server values | SVM | overlapping edits from two value mods are invisible until something is wrong |

### Rule 2: the built-in auto-disable is a feature, not a bug

Questing Bots **turns off its own initial-PMC spawning when it detects SWAG + Donuts**
(verified in its README). If someone "fixes" that by forcing `initial_PMC_spawns.enabled`
back on, the map gets two spawn systems fighting. Leave it off.

### Rule 3: when two mods claim the same setting, the more specific one wins

| Setting | Who wins | Consequence |
|---|---|---|
| Bot counts / spawn waves | the spawn mod (SWAG's `config.json`, Donuts' `ScenarioConfig.json`) | spawn numbers set in **SVM are overridden** (community-reported; verify in-game) |
| Bot gear | the progression mod (ALP) | SVM gear settings are cosmetic next to it |
| Bot behaviour in a fight | SAIN | brain-layer priorities decide what a bot does when two mods want a say |
| Loot on bots/containers | the loot mod (Looting Bots) plus whatever generates the loot server-side | — |
| Raid timers, extracts, flea, insurance | SVM / `SPT_Data\Server\configs\` | — |

### Rule 4: Fika (co-op) sits above both

Co-op settings — including a **global bot limit** — are applied by the Fika server mod, and
they cap whatever the spawn mods asked for (community-reported; **verify in-game** on the
Fika build in this install). If bot counts make no sense in co-op, look at Fika before
blaming SWAG.

---

## Part 4 — the practical order to try things

1. **Read the console before changing anything.** Server console for `user\mods`,
   `BepInEx\LogOutput.log` for client plugins. A refused dependency is usually one line.
2. **Disable, do not delete.** Rename the folder or the `package.json`.
3. **Change one thing, then re-test the same raid.** Factory, same settings, same time of
   day. Two changes at once teaches you nothing.
4. **If the raid will not start at all**, it is almost always a *server* mod — the client
   cannot finish loading while the server is stuck. Go to `troubleshooting.md`.
5. **Only after it works**, delete the `.off` folder or fix the config.

## Related pages

- `mod-catalog.md` — the inventory this ordering applies to.
- `troubleshooting.md` — when a load problem turns into a raid that will not start.
- `mod-install-workflow.md` — the dependency check that runs before a mod is installed.

## Verify-in-game list

- Which of the ~79 client plugins declare `[BepInDependency]` on each other — read it from
  the DLLs with a manager, not from memory.
- Whether the installed SWAG/Donuts build puts `loadBefore`/`loadAfter` in its
  `package.json`, and what it names.
- Whether Fika in this install exposes a global bot limit in its own F12 section.
- The exact `sptVersion` string in each `user\mods\*\package.json` — a single non-3.10.x
  entry is a latent break.
