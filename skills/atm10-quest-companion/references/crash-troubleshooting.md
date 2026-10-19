# Crash troubleshooting: "ATM10 won't start", "it just closes"

**What this page is.** The triage path for **All the Mods 10** when the game dies instead
of loading: the window vanishes with no Minecraft crash screen, the launcher reports an
exit code, `latest.log` stops mid-sentence, or Crash Assistant opens its own **Piracy
Warning** / **Too Many Changes** dialog. It exists so a session can answer *"why did my
ATM10 crash?"* by ordering the evidence **before** naming a mod — and so it never invents
a culprit the files do not name.

**What it is not.** A mod bug tracker, a GPU-driver guide, or a promise that a modified
instance can be fixed from one log. `references/lag-fix-guide.md` is for a game that
*runs* badly; this page is for one that does not run at all.

## Provenance — read, not remembered

Every pack value below was read from the official repository
[AllTheMods/ATM-10](https://github.com/AllTheMods/ATM-10) at `main` commit
[`e5e3d1d83e`](https://github.com/AllTheMods/ATM-10/commit/e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025)
(2026-09-22, pack **8.2**), or from the field report named in the next section:

| Source | What it supplied |
|---|---|
| `config/memorysettings.json` | the client minimum, maximum, and the per-system-memory recommended allocation quoted in Step 3 |
| `config/crash_assistant/config.toml` | where Crash Assistant keeps its own logs, and the pack's help link |
| `config/crash_assistant/modlist.json` | the shipped jar list (**497 jars / 493 mod ids** at 8.2), used to check "is this mod in the pack?" |
| `changelogs/CHANGELOG-ATM10-8.0-8.1.md` | the 8.0 → 8.1 mod moves quoted in Step 5 (Sodium, FancyMenu) |
| `changelogs/CHANGELOG-ATM10-8.1-8.2.md` | the 8.1 → 8.2 mod moves quoted in Step 5 (MineColonies) |
| `MOD_ISSUES.md` | the pack's own per-mod issue-tracker list, i.e. where a real mod bug is reported |

**The field report** this page was written from is one ATM10 **8.0** client
(Minecraft 1.21.1, NeoForge 21.1.247, Microsoft OpenJDK 21.0.7, Windows 10, 16 GB RAM,
Radeon RX 6600) whose launch ended with **exit code `-1073740791`** and a `latest.log`
that simply stopped. Its exact symptoms are quoted where they matter, and only there.

## Tags used here

| Tag | Meaning |
|---|---|
| **verified** | read from the pack repository, or from the file named next to the quote |
| **field report** | observed in that one 8.0 launch on 2026-10-19 — one instance, not the pack |
| **judgement** | the order this page suggests trying things in |
| **verify on disk** | confirm it in the player's own instance before acting |

No mod is named as "the cause" anywhere on this page unless a report or a log frame names
it. **A crash with no stack trace does not have a culprit yet** — it has suspects, and
the suspects are ranked by how much evidence points at them, not by reputation.

## Step 0 — collect the evidence before reading any of it

A `latest.log` that stops mid-loading is **not** a crash report. It stops because the
process died before it could write the closing lines. The files that matter are written
*around* the death, by the JVM, the launcher, and the OS.

All paths are relative to the **instance folder** — on a Windows launcher with a
per-version layout that is the folder holding `mods/`, `config/`, `logs/` and
`crash-reports/` (the field report's was
`%APPDATA%\.minecraft\versions\All the Mods 10 - ATM10 All the Mods 10-8.0\`).

| File | Written by | What it answers |
|---|---|---|
| `crash-reports/crash-<date>_<time>-client.txt` | Minecraft / NeoForge | a **mod threw**. The `Description:` line and the first frames under `StackTrace` are the lead. |
| `hs_err_pid<pid>.log` | the JVM itself | the **JVM or native code aborted**. Look for `Problematic frame`, `siginfo`, `Dynamic libraries` and the `-Xmx` line. |
| `logs/latest.log` **tail** | the game | how far loading got, and the last ERROR before silence. The tail, not the middle. |
| `logs/debug.log` | the game | the same run with more detail, including arguments |
| `logs/crash_assistant/` | Crash Assistant (pack ships it on) | its own app log — the window that says *"Log analysis is taking longer than expected"* is this app, and this is where it explains itself |
| `logs/stderr_stream.log` | Crash Assistant | **stderr**, which many launchers throw away — `config/crash_assistant/config.toml` ships `generate_own_launcher_log = true`, so the pack generates this file |

**Judgement:** look for `hs_err_pid*.log` and `crash-reports/` **first**. If
`hs_err_pid*.log` exists, skip straight to Step 2 and do not waste a round trip on the
mod list; the JVM has already named the frame it died in.

## Step 1 — decode the exit code, because it decides what evidence exists

Launchers print the Windows status as a **signed 32-bit decimal**, so the familiar
`0xC000…` codes arrive as large negative numbers. This part is Windows, not the pack
(**verified** against the NTSTATUS values, which are stable public constants):

| Decimal | Hex | Name | What it means for ATM10 |
|---|---|---|---|
| `0` | `0x0` | clean exit | the player quit — nothing crashed |
| `1` | `0x1` | general failure | a Java exception: the stack trace is in `crash-reports/` or `latest.log` |
| `255` / `-1` | `0xFF` | wrapper convention | usually a Java failure; read it exactly like `1` |
| `-1073741819` | `0xC0000005` | `STATUS_ACCESS_VIOLATION` | native code read or wrote bad memory — GPU driver, a DLL, or JNI. Look for `hs_err_pid*.log` |
| `-1073740791` | `0xC0000409` | `STATUS_STACK_BUFFER_OVERRUN` | Windows **fail-fast**: the process was aborted, not thrown. **No Java stack trace is written.** |
| `-1073741571` | `0xC00000FD` | `STATUS_STACK_OVERFLOW` | runaway recursion, often a mixin or a mod's world-gen; `hs_err` names the thread |
| `-1073740940` | `0xC0000374` | `STATUS_HEAP_CORRUPTION` | native heap damage — usually a DLL or driver |

**Field report** — the launch this page was written from ended with
`-1073740791` (`0xC0000409`), and its `latest.log` stops right after the sound engine
started and the texture atlas was built. That combination is the point of this whole
page: **`0xC0000409` is not a Minecraft exception.** There is no "Caused by" line to
find, and asking the player for a crash report he does not have wastes his time. What he
needs to look for is `hs_err_pid*.log`; what he needs to send is that file plus
`logs/crash_assistant/` and the tail of `latest.log`.

Two non-answers to rule out early (**judgement**):

- **A launcher dialog that says "Unexpected error occurred" with the same code** is the
  launcher reporting the child process it just lost, not a second crash.
- **Crash Assistant stuck on "Log analysis is taking longer than expected"** is the
  analyser, not the game. Its verdict is not evidence; the files above are.

## Step 2 — read the abort file, not the mod list

When `hs_err_pid*.log` exists, read it in this order:

1. **`#` header** — the `-Xmx` actually in force, the Java version, and the command line.
   Compare the heap with Step 3 before reading anything else; a heap far below the pack's
   minimum makes every later line noise.
2. **`Problematic frame`** — a `C`/`J`/`V` frame with a library name points at native
   code (driver, `lwjgl`, a mod's bundled `.dll`). A `j` frame points back at Java.
3. **`siginfo` and `Dynamic libraries`** — the signal and the loaded modules. On an AMD
   card, a `atio6axx.dll` / `amdxc64.dll` module in the crash path is a driver lead, not
   a mod lead.
4. **`Thread`** — `Render thread` means it died drawing; `main` means it died loading.

If there is no `hs_err_pid*.log` **and** no crash report, the process was killed from
outside the JVM: a fail-fast in a native library, a security product, or the OS. Check
Windows **Event Viewer → Windows Logs → Application** for an `Application Error` entry at
the same timestamp; it names the faulting module, which is the only place that name
appears.

## Step 3 — memory: the pack publishes the number, use it

`config/memorysettings.json` at 8.2 (**verified**) ships:

| Key | Shipped value | Meaning |
|---|---|---|
| `minimumClient` | `6000` | below this, the pack itself expects trouble (MB) |
| `maximumClient` | `32000` | above this, the pack warns: an oversized heap makes GC stutter worse |
| `recommendedMemory` | `16000:8000`, `32000:12000`, `48000:12000`, `64000:12000` | system RAM → allocation, in MB |

So on a **16 GB** machine the pack's own recommendation is **8 GB** for the client; the
floor is **6 GB**; do not go above ~10 GB on 16 GB total, because Windows, the browser
and Discord need the rest. `references/getting-started.md` says the same thing in the
setup steps — this table is the config it comes from.

**Field report** — that launch was running on a heap measured in the low hundreds of MB:
its own garbage-collector lines read `Starting garbage collector: 136 / 253 MB` and
`Garbage collector completed: 79 / 253 MB`, and then FancyMenu's title-screen preload
failed with `Could not load image: Out of memory` on a set of small PNGs. Small images
failing to allocate is not a texture problem — it is a heap that was already full.

**Fix, and how to confirm it took:** set the launcher's Java arguments to `-Xms8G -Xmx8G`
(the pack's table rounds that same allocation to 8000 MB; launchers that hide the field
expose it as a "Memory / Allocated RAM" slider), launch
once, then **verify** by finding the `-Xmx8G` in `latest.log`'s argument dump or in the
`hs_err` header. A launcher that ignores the field, or caps it, is the actual bug — and
that is common on the unsupported launchers Step 6 is about.

**Judgement, but cheap:** do not run a Windows "memory cleaner" / RAM optimizer while the
pack starts. These tools trim other processes' working sets; a JVM or GPU driver that
cannot get its pages back does not throw a Java exception, it fails fast — exactly the
`0xC0000409` class of death. Close it for the test, not forever.

## Step 4 — "Too Many Changes": the pack says it will not support that instance

Crash Assistant ships in the pack and compares the installed jars against
`config/crash_assistant/modlist.json`. When they differ it shows, **verbatim from the
field report's screenshot**:

> **Too Many Changes Warning**
> You've made too many changes to the modpack!
> Most likely, this issue is caused by your modifications.
> Clicking the "Update All" button in the launcher is also very likely to break things.
> If you haven't modified the modpack, most likely this is corrupted due to an incorrect
> update, and you should reinstall it.
> We won't provide support for that number of changes (n).
> Please revert all your changes, or you're on your own!

That dialog is the pack's own support policy, and the field report's instance showed
**Added 5, Removed 4, Updated 11**. Three consequences follow:

1. **The instance is not stock**, so no answer can be derived from the pack alone. Say so
   plainly instead of guessing which of the 20 changed jars did it.
2. **Use the app's own list, not a directory listing**: its panel has *Show mod list
   changes* / *Compare*, which names the exact jars. Ask the player to read them out (or
   send that panel's copied link) — that is the fastest path to a real answer.
3. **The supportable fix is a clean instance**: install ATM10 fresh through a supported
   launcher, launch it once untouched, and only then re-add the player's own mods one at
   a time. "Revert your changes" in the dialog means exactly this.

**Judgement:** reverting is also the fastest *diagnosis*. A clean 8.x instance that
launches proves the pack is fine and the changes are the cause; a clean instance that
still crashes proves the opposite, and turns the search toward Java, RAM and the driver.

## Step 5 — the three stacks that actually differ at startup

Check these before a mod bisect, because each is verifiable rather than remembered:

| Suspect | How to check it | What the pack says (**verified**) |
|---|---|---|
| **Distant Horizons** | is a `DistantHorizons-*.jar` / `distanthorizons` entry in `mods/`? | **not in the pack.** The 8.2 `modlist.json` (497 jars) contains no `distant` string at all, and neither the 8.0→8.1 nor the 8.1→8.2 changelog mentions it. Any DH build is a local addition, and it is the first thing to remove when testing. |
| **Sodium on 8.0** | the jar name | 8.0 shipped `0.8.13-beta.2`; 8.1 moved to stable `0.8.13` (`CHANGELOG-ATM10-8.0-8.1.md`: `Sodium (0.8.13-beta.2+mc1.21.1) -> (0.8.13+mc1.21.1)`). A player still on 8.0 is on the beta drop — updating the pack is a legitimate fix, not a mod hunt. |
| **Iris / shaders** | the jar name | `iris-neoforge-1.8.14-beta.1+mc1.21.1.jar` **is** the pack's own Iris at 8.2, so Iris itself is not "an added mod". Shaders and the `EuphoriaPatcher` that ships with it still change the render path: test with the shader pack set to **None** before blaming the game. |

The field report's own versions corroborate that its base was stock **8.0**: the
changelogs move `FancyMenu (3.9.9) -> (3.9.12)` in 8.1 and
`MineColonies (1.1.1374-1.21.1-snapshot) -> (1.1.1396-1.21.1-snapshot)` in 8.2, and the
report's FancyMenu `3.9.9`, MineColonies `1.1.1374-snapshot` and Sodium
`0.8.13-beta.2` are therefore the versions 8.0 shipped. Those three are **not** the
drift; the drift is whatever the Crash Assistant panel lists.

## Step 6 — offline mode and unsupported launchers: say it once, neutrally

Crash Assistant's other dialog, **verbatim from the field report**:

> **Piracy Warning (Crash Assistant)**
> You are using an unsupported launcher or offline mode.
> If you need help with this crash, please try installing a supported launcher (like
> Prism Launcher) or switching to online mode, then repeating the actions that led to the
> crash. ATM10 Support Channel community do not provide support for crashes that happen
> in offline mode.

What this changes in practice (**judgement**):

- **The pack's Discord/GitHub will not triage the log** — the pack's `help_link` is
  `https://discord.gg/allthemods`, and this warning is the gate in front of it. Do not
  send the player there with an offline log and expect an answer.
- **Unsupported launchers are the usual source of a tiny `-Xmx`.** Their defaults, not
  the pack's, decide the heap; that is why Step 3's "verify the running `-Xmx`" matters
  more than editing a config file.
- **Offline mode is not itself a crash cause** at this stage of loading — no Mojang
  session is needed to build a texture atlas. Do not tell the player that "being offline"
  broke his textures; tell him it removes his support path and may have set a bad heap.
- If he is offline for a legitimate reason (no connection, a child's machine), a
  **supported launcher in offline mode** is still an improvement: Prism/CurseForge give
  him a real Java-arguments field and a real log directory. The piracy warning clears
  when the launch is online.

## Step 7 — bisect, when Steps 3–6 are clean and it still dies

Do this only after a clean 8.x instance at 8 GB has been tried (**judgement**):

1. **Reproduce deterministically** — same world or a brand-new one? A crash at the title
   screen is a client-side load problem; a crash after "Joining world" is world/mod data.
2. **Halve `mods/`** — move half the jars out (not rename `.jar.disabled`: some launchers
   still scan those), launch, and keep the half that reproduces. Six or seven launches
   isolate one jar out of ~500.
3. **Read the added mod's own issue tracker** from the pack's `MOD_ISSUES.md` before
   reporting; the pack asks players not to send crashes straight to mod authors.
4. **Record the failing jar and its version** — a bug report without the exact jar name
   and the `hs_err` frame gets closed.

Prefer Step 4's clean-instance revert over this: a bisect on an instance that already
fails the pack's integrity check can find a jar that was never the problem.

## Traps in the log that are not the crash

The field report's `latest.log` is full of red that did **not** stop the launch. Naming
these as the cause is the easiest way to be confidently wrong.

| Line in the log | What it is | Verdict |
|---|---|---|
| `java.lang.IllegalStateException: Cannot get config value before config is loaded` repeated hundreds of times, from `minecolonies` → `ModEquipmentTypes.initRegisterEquipmentTiers` → `IItemStackExtension.getAttributeModifiers`, quoting `allthearcanistgear` and `justdirethings` armour classes | MineColonies' deferred equipment-tier registration reading another mod's config during the deferred work queue, i.e. before configs are loaded | **A real mod-timing bug, logged as ERROR, survived.** Loading continued past every line. Worth reporting to MineColonies; not the abort. |
| Two CC:Tweaked jars listed (`1.113.1` and `1.120.0`) | NeoForge aborts on two jars with the same mod id, so a launch that reached the title screen is loading **one** | Check the pack's own `modlist.json`: at 8.2 it lists **two** filenames too (`1.113.1` and `1.120.2`). Do not delete a jar on this evidence alone. |
| `Could not load image` / missing `*.png.mcmeta` / missing animation frames | FancyMenu and resource-pack metadata | Cosmetic — **unless** the message is `Out of memory`, which is Step 3 |
| `accesstransformer.cfg` missing for a mod | a mod shipping an AT without the file its loader expects | A warning; read the mod's own tracker if it matters |
| `mysticalagriculture` models missing for allthemodium / vibranium / unobtainium essences | ATM's datapack-driven additions without shipped models | Expected in this pack; cosmetic |
| `formations:template_editor` item absent | a mod item removed upstream | Cosmetic |

## Quick reference

| Symptom | First move |
|---|---|
| Window closes, launcher shows `-1073740791` | Step 1: there is no Java trace — find `hs_err_pid*.log` (Step 2) |
| Window closes, launcher shows `-1073741819` | Step 2: `Problematic frame`, then the GPU driver |
| Crash screen with a mod stack trace | a real mod crash: read `crash-reports/`, then `MOD_ISSUES.md` |
| "Too Many Changes" | Step 4: clean instance, then re-add one at a time |
| "Piracy Warning" | Step 6: supported launcher / online mode; do not send it to the pack's Discord |
| Loads, then stutters or lags | wrong page — `references/lag-fix-guide.md` |
| Dies only when joining a world | world-side: back up the world before anything else |

## What this page will not do

- **It will not name a culprit from a log with no stack trace.** If the player only has
  the tail of `latest.log`, the honest answer is "this file cannot identify the mod; send
  `hs_err_pid*.log` or the crash report".
- **It will not quote a config key the pack does not ship** — the memory numbers above
  come from `config/memorysettings.json`, not from a remembered launcher default.
- **It will not promise a frame-rate or stability gain.** Nothing here can measure the
  player's machine, and a clean instance changes different things on different hardware.
- **It will not tell the player to pirate-repair or to disable mods at random.** Reverting
  to a clean pack, then adding back deliberately, is both the supported path and the
  diagnosable one.
