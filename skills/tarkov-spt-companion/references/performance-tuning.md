# Performance tuning — 16 GB, alive raids, and the mods that cost the most

**What this page is.** How to keep raids feeling alive on **16 GB of RAM** with the ~120-mod
SPT **3.10.5** install at `C:\games\SPT-TARKOV-3105-COOP-LAN`: where the memory actually
goes, which mods cost the most, the settings worth touching, and the ones that are not worth
the risk.

**One promise up front: this page names levers, never frame-rate numbers.** Nobody can
measure this install from a document. Try a lever, play a Factory raid, keep it if it
helped.

---

## Grounding

| Tag | Meaning |
|---|---|
| **verified** | read from `https://sp-mod.com`, `https://github.com/dwesterwick/SPTQuestingBots`, `https://github.com/DeadLeavez/MISC` while this skill was built |
| **reported** | what SPT players report in community threads — real experience, not measured here |
| **judgement** | this page's ranking and the order to try things |
| **verify in-game** | confirm on his disk / his settings screen before changing |

## Step 0 — know what is sharing the 16 GB

This install runs **three** things on one machine at once:

| Process | Rough share (judgement) | Notes |
|---|---|---|
| The EFT **client** | the biggest single consumer | the game itself leaks; that is base EFT, not SPT |
| The **SPT server** (`SPT.Server.exe`) | a further slice, plus more for every bot it tracks | a second PC can host it (see the Fika note below) |
| Windows + browser + Discord/voice | the part everyone forgets | a browser with a few tabs open is not free on 16 GB |

That is the whole problem in one table: the game wants more than 16 GB, and the server is
sitting in the same pool. Everything below is either **give the system somewhere to spill**
or **ask for fewer bots**.

---

## Step 1 — RAM hygiene first (cheapest wins, no gameplay cost)

Do these before touching a single mod setting.

1. **Make sure the Windows pagefile is enabled.** The most common 16 GB fix: with no
   pagefile, raids on the bigger maps fail to load at all rather than merely stuttering.
   *reported* widely; the size is your call — half to twice the RAM is the usual advice.
2. **Use the in-game RAM cleaner, and know what it actually does.** The built-in option is
   reported to fire mainly in the menu, not in a raid — which is why players double-tap
   `Esc` every few minutes. That is not a superstition; the pause triggers a cleanup.
3. **Consider the RAM Cleaner Fix mod** (community staple, find it on sp-mod.com) — it makes
   the cleanup run on a timer, commonly set around **90 seconds**. *reported*.
4. **Close the browser before a session.** On 16 GB this is not optional advice, it is the
   cheapest GB you will ever reclaim.
5. **Restart between long sessions.** Several players report that no cleaner fully replaces
   restarting after a few big-map raids. *reported*.
6. **Optional external tool:** Intelligent Standby List Cleaner (ISLC, wagnardsoft) clears
   the standby list. *reported*. Use it or don't — it is a system tool, not a mod, and this
   page takes no position beyond noting it exists.

## Step 2 — the mods that cost the most (judgement ranking)

Ranked by what they do to a 16 GB box, not by how visible they are.

| Rank | Mod / system | Why it costs | Where the lever is |
|---|---|---|---|
| 1 | **Bot count** — i.e. the spawn stack (SWAG + Donuts) | every live bot is CPU and memory, and the cost is multiplied by whatever else is reading them | `user\mods\SWAG\config\config.json` (`MaxBotCap`, `NightMaxBotCap`) and `BepInEx\plugins\dvize.Donuts\ScenarioConfig.json` |
| 2 | **SAIN** | per-bot combat logic on every bot in range — cost scales with the bot count above | SAIN's **F12** menu; presets live in the plugin folder (**verify in-game**) |
| 3 | **Questing Bots** | per-frame quest-selection work; capped at **1 ms per frame** by default (verified: `questing.quest_selection.max_calc_time_per_frame_ms` in its README) | its F12 / config; its own AI limiter |
| 4 | **The map itself** | Streets, Lighthouse and Ground Zero are the heavy ones | pick the map; use the low-resolution texture option where the game offers one |
| 5 | **Looting Bots** | bots evaluating containers and corpses | plugin config / F12 |
| 6 | **ALP** | generates randomized loadouts — server-side work concentrated around spawns | the mod folder in `user\mods` (**verify in-game**) |
| 7 | **Client HUD / UI mods** — EFT API + Game Panel HUD are named repeatedly | memory leaks that no in-raid cleaner keeps up with | *reported*; if memory climbs all session, try a raid without them |
| 8 | **Late to the Party** | named by several players as a leak source when combined with a spawn mod | *reported*; disable and test if memory climbs |
| 9 | Everything else | — | bisect per `troubleshooting.md` if something specific is suspected |

Note the shape of that table: **rank 1 is a setting, not a mod.** Before removing anything,
lower the bot counts — that single change reduces the cost of ranks 2, 3, 5 and 6 at once.

## Step 3 — the levers, per mod

### SWAG — `user\mods\SWAG\config\config.json`

- `MaxBotCap` and `NightMaxBotCap`: the per-map bot ceilings, found at the bottom of the
  file (verified from the Fika/SWAG performance write-up at
  `https://github.com/DeadLeavez/MISC`). **This is the first number to lower.**
- The same file carries the general SWAG options, including a **disable-all-spawns** switch
  named on the mod's sp-mod.com page — the fastest way to prove whether spawning is your
  problem at all.

### Donuts — `BepInEx\plugins\dvize.Donuts\ScenarioConfig.json`

- Per-scenario PMC and SCAV caps. *reported* community practice: lower the caps, raise the
  **spawn cooldown** (one commonly quoted value is 360 seconds) for breathing room between
  waves, and enable the **despawn / hard-cap** options so dead bots stop being your problem.
- Donuts' own rules (verified from `https://github.com/dvize/Donuts`): bots spawn at the
  spawn marker's level, within a radius of it, one marker per group. Spawn point quality, not
  just quantity, is part of how heavy a raid feels.

### Questing Bots — server-side

- `questing.quest_selection.max_calc_time_per_frame_ms` — **1 ms by default** (verified).
  Leave it alone unless you know why you are changing it; raising it trades frame time for
  faster quest selection.
- **Its own AI limiter** (verified from its README): it must be enabled explicitly in the F12
  menu, and per map; by default questing bots are only disabled on **Streets**. Bots are
  only put to sleep beyond a distance from you (**200 m** default) and from other questing
  bots (**75 m** default).
- Its AI limiter exists precisely because **AI Limit and Questing Bots are incompatible** —
  a generic AI limiter freezes bots mid-quest.

### Fika (co-op)

- A **global bot limit** in the Fika F12 section is reported to cap everything the spawn mods
  asked for. *reported* — verify the section exists in the installed Fika build.
- **verify in-game:** whether Fika's headless client is in play or worth setting up. Running
  the bots/server on a second machine takes that load off the 16 GB box entirely; it is the
  only change on this page that adds capacity instead of spending less.

## Step 4 — graphics settings that matter

In the game's **Settings → Graphics** screen. All judgement, all *verify in-game* — the
right value depends on his GPU, and this page will not guess it.

| Setting | Why it is on this list | Suggested direction (judgement) |
|---|---|---|
| **LOD quality** | reported to hit **both** CPU and GPU — the rare setting that costs on the side this build is short of | low end (~2–2.5 is a commonly quoted range) |
| **Overall visibility distance** | same family as LOD; drives how much is drawn at all | lower if the map feels heavy |
| **Shadow quality / shadows** | large cost, small readability gain in a firefight | low–medium |
| **HBAO / SSR** | repeatedly described as a bad visual-to-performance trade | off |
| **Nvidia Reflex** | *reported* as on by default and, for at least one player, the single biggest fix for stutter once disabled | try off; use the driver's low-latency mode instead if you want it |
| **Texture quality** | pure VRAM: high textures on a card with less than ~8 GB is a stutter generator | medium on <8 GB VRAM |
| **MIP streaming** | keeps texture memory from peaking | on |
| **Anti-aliasing** | TAA is softer and cheaper than supersampling; FXAA/other options are a taste call | TAA, or the cheapest option you can stand |
| **Grass shadows, chromatic aberration, noise** | free quality-of-life removals | off |
| **"Only use physical cores"** | *reported* to matter, and it interacts with the `boot.config` below | try both, keep the winner |

### `boot.config` — the risky one

*Reported* by players tweaking SPT 3.10 performance. The file sits in the game's data
folder — **`EscapeFromTarkov_Data\boot.config`** (**verify in-game**: confirm the exact
folder name in this install). Values seen in the wild:

```
gfx-enable-gfx-jobs=1
gfx-enable-native-gfx-jobs=1
gfx-disable-mt-rendering=1
wait-for-native-debugger=0
vr-enabled=0
hdr-display-enabled=0
gc-max-time-slice=10
job-worker-count=7
```

Rules if you go here:

1. **Copy `boot.config` to your backup folder first.** It is one file; there is no excuse.
2. Change **one** line, test a Factory raid, write down the result.
3. `job-worker-count` is machine-specific — one player reported the best result at
   (virtual core count − 1) with "only physical cores" **unchecked**. *reported*.
4. If the game stops launching, restore the copy. Nothing on this page is worth a
   non-starting install.

## Step 5 — the order to do all of this

1. Pagefile on, browser closed, in-game RAM cleaner on. (no gameplay cost)
2. Lower `MaxBotCap` / `NightMaxBotCap`, then the Donuts scenario caps. (the big one)
3. Turn on Questing Bots' own AI limiter for the maps you play.
4. Graphics: LOD, visibility, shadows, HBAO/SSR off, Reflex off, textures to your VRAM.
5. Only then consider dropping a mod — and if memory climbs all session, suspect the HUD/UI
   mods and Late to the Party first.
6. `boot.config` last, one line at a time, with a backup.

## Related pages

- `mod-catalog.md` — what each mod in the cost ranking actually does.
- `troubleshooting.md` — bisect with this when the cost looks like a leak, not a setting.
- `backup-restore.md` — back up `boot.config` and the SWAG/Donuts configs before editing.

## Verify-in-game list

- His actual GPU and VRAM — everything in Step 4 is calibrated against them, and this page
  does not know them.
- The names of the bot-cap keys in the **installed** SWAG and Donuts versions (both files
  have been reorganised across versions).
- Whether the installed Fika build exposes a global bot limit.
- Whether the HUD/UI mods in his ~79 plugins are the ones the leak reports name — check the
  actual plugin folder, not a list on the internet.
- The exact data-folder name holding `boot.config` in this install.
