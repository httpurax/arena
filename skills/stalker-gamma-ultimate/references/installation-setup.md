# Installation, setup and maintenance — S.T.A.L.K.E.R. G.A.M.M.A.

Sources for this page: the official GAMMA wiki pages **Installing-GAMMA** and
**Technical-Support-FAQ** (snapshot of the wiki as of 2026-10-15), the GAMMA repository
`README.md` and `Patchnotes.md` at commit `ab0f743af42a3b3b0b0ee853b3676f5189f7f0d0`
(modpack 0.9.5, launcher 8.6, definition version 920), and the shipped launcher layout
(`G.A.M.M.A/modpack_data/modlist.txt`, `G.A.M.M.A_definition_version.txt`).

**The wiki says it plainly: "The most up-to-date and detailed version of these instructions
will always be on the GAMMA Discord's `#how-to-install` channel. This also goes for any
install links."** Treat the Discord announcement as newer than any page, including this one.

---

## 1. What you are actually installing

| Component | What it is | Version in this snapshot |
|---|---|---|
| **S.T.A.L.K.E.R. Anomaly** | Free standalone fan game (built on Call of Chernobyl / X-Ray). You do **not** need to own any S.T.A.L.K.E.R. game to play Anomaly or GAMMA. | 1.5.3 |
| **GAMMA RC3** | The core GAMMA release archive: launcher, Mod Organizer 2, base files. | RC3 (used with launcher v8.6) |
| **The mods** | ~385 addon folders plus third-party mods the launcher downloads itself. GAMMA's repo distributes little to no third-party copyrighted content: the launcher pulls each addon from ModDB/GitHub, which is why the install is a download-heavy, hours-long process. | modpack 0.9.5 |
| **Engine** | 0.9.5 ships the Multi-Threading test branch of the Anomaly engine by Demonized, `MT-TEST_2026.5.5`. | per `Patchnotes.md` |

The launcher also writes `G.A.M.M.A_definition_version.txt` (value **920** in this
snapshot) — the modpack definition number the launcher compares against to know what it
has installed.

## 2. Requirements

### Operating system and dependencies

The official guide covers **Windows x64**. It lists these dependencies:

- **.NET Framework 3.5** (Microsoft download)
- **DirectX, latest version** (Microsoft download)
- **Visual C++ Redistributable x64** (Microsoft download, "Latest supported redistributable
  version, X64 Architecture")

Other platforms (all **community**, linked from the official wiki — not maintained by
Grokitach):

| Platform | Path |
|---|---|
| Linux | Red's guide — https://github.com/Red007Master/Red-s-Guide-on-Installing-G.A.M.M.A.-on-Linux ; Discord has a Linux support thread |
| macOS | Discord thread (linked from the wiki) |
| Steam Deck | Discord thread (linked from the wiki) |
| Linux GUI front-ends | community launchers exist (e.g. `SSH-Kitty/STALKER-GAMMA-COMMANDER`, `FaithBeam/stalker-gamma-launcher-clone` for Wine/macOS) — use at your own risk, not official |

### Tooling

- **7-Zip** is required. The wiki says WinRAR and Windows' built-in archive manager "are
  known to cause issues when extracting large .7z files. Use 7-Zip for all file extraction
  when installing GAMMA."
- **Free disk space: at least 150 GB** to start and finish the installation — and you must
  have that space *before* you start. The wiki recommends **175–200 GB free** "to minimize
  the chance of errors."

### Download budget (the wiki's own table, rounded to the nearest GB)

| File(s) | Download size | Installed/extracted size |
|---|---|---|
| Anomaly 1.5.3 | 9 GB | 16 GB |
| GAMMA RC3 | 11 GB | 27 GB |
| GAMMA mods (via the launcher) | 27 GB | 76 GB |

Total installed GAMMA (not counting Anomaly) is **around 130 GB** — 27 GB from RC3, 27 GB of
downloaded mod files, 76 GB of installed mods, plus Git-pulled files and so on.

## 3. The two folders (this is where most installs go wrong)

Create a **_GAMMA folder_** and an **_Anomaly folder_**. They must be:

- two **different** folders, **not nested** in each other;
- **not** in a restricted location — the wiki explicitly excludes your `Users` folder
  (including `Documents`), the Desktop, **OneDrive**, and `Program Files`;
- on the **same drive**;
- **not** on an external/USB drive.

Example from the wiki: GAMMA at `F:/STALKER GAMMA/GAMMA` and Anomaly at
`F:/STALKER GAMMA/Anomaly`.

If you already have an Anomaly folder, it must be **clean, unmodded, and 1.5.3**. An old,
modded install is one of the classic causes of a broken GAMMA.

### Antivirus exclusions (mandatory, not optional)

Both folders go into your antivirus exclusions **before** you extract or download anything.
The reason given in the wiki: "Due to its folder virtualization system, MO2 is frequently
blocked by antivirus."

Known offenders from the official guide:

- **Norton, Avast, AVG, Malwarebytes** — known to block the *launcher downloads*; the wiki
  says you may need to disable them completely for the duration of the install and re-enable
  afterwards.
- **Bitdefender** — blocks MO2 *and* all Anomaly executables. Every one of those `.exe`
  files must be individually excluded from **Advanced Threat Defense**.

## 4. Installation, step by step (official order)

1. **Download the two key archives.** Anomaly 1.5.3 from the official torrent (magnet via
   the wiki's shortlink) or the ModDB direct download; GAMMA RC3.7z from **one** of the
   mirrors (Gofile / Mediafire / MEGA — they are the same file, pick one).
2. **Create the GAMMA and Anomaly folders** as described in §3, add the antivirus
   exclusions.
3. *(Optional but recommended)* **Verify the downloads.** Open PowerShell where the files
   are, run `CertUtil -hashfile "filename" SHA256`, and compare exactly. The wiki publishes:

   | File | SHA256 |
   |---|---|
   | `Anomaly-1.5.3-Full.2.7z` | `E564D9110E673EACFA5604B0837F6E6208EAE4CD46CD5682326ED59F931527AE` |
   | `GAMMA RC3.7z` | `2ceda1782b0b7737747c16974f1fe014bc1915caf1b08a1cba71e7950485192d` |

   (The checksum page carries its own "last updated" date — re-check it if a hash fails and
   the file is not obviously corrupt.)
4. **Extract Anomaly 1.5.3 into the Anomaly folder** with 7-Zip.
5. **Run `AnomalyLauncher.exe` and click Play until you reach the main menu, then exit.**
   This is the wiki's step 2 and it matters: it lets Anomaly generate its first-run files.
6. **Extract GAMMA RC3 into the GAMMA folder** with 7-Zip.
7. In the GAMMA folder open `.Grok's Modpack Installer` and run **`G.A.M.M.A. Launcher.exe`**.
   Confirm the window shows **launcher v8.6** in the top-left; if it does not, update it
   manually (§5).
8. Click **"First Install Initialization"** — you do this **once**.
9. When Mod Organizer asks which game to manage, **select your Anomaly folder** (the one
   containing `AnomalyLauncher.exe`). Then **close the Mod Organizer window**.
10. **Leave all GAMMA Launcher options on default** and click **"Install / Update GAMMA"**.
    This is the long part: 27 GB of downloads and 76 GB of extraction.
11. When the green "**Installation finished**" message appears, click **Play** to open Mod
    Organizer 2.
12. In MO2 choose **"Anomaly (DX11)"** in the top-right dropdown and click **Run**.

The launcher creates desktop shortcuts for itself and for MO2; from then on those are your
entry points.

## 5. Updating the GAMMA Launcher

If the launcher is not current (it must say **v8.6** for this snapshot):

1. Get the current launcher release (the wiki links GAMMA Launcher **v8.6** on Mediafire).
2. Extract its contents into `GAMMA/.Grok's Modpack Installer`, **overwriting** when asked.

Everything else in the GAMMA folder stays as it is.

## 6. Updating GAMMA itself

The short version from the wiki: **watch the Discord announcements channel and do what the
announcement says.** If two sources disagree, the announcement wins.

### The one rule everyone must know

> Every time you click **"Install / Update GAMMA"**, your **modlist, settings and mod
> settings reset**. This is *on purpose* — it is how the launcher repairs broken installs.

So: **back up first** (§7), always.

### Major version updates (version number changes)

- Announced in Discord; they generally change the modlist and settings, so **old backups
  are not useful** afterwards.
- **Save-game compatibility is never guaranteed** for major versions.
- Typical steps: update the launcher, leave options on default, click *Install / Update
  GAMMA*.

### Minor updates and hotfixes

- Usually no version bump; they **may or may not** change the modlist.
- Modlist/settings backups are *generally* fine to reuse; saves are *generally* compatible.
- Typical steps: update the launcher, **disable "Force git download" and "Force zip
  extraction"**, click *Install / Update GAMMA*. (Those two options force a full re-download
  / re-extract and are the reason a "small" update can take hours.)

### Do not chase ModDB addon updates

The FAQ is blunt: **do not update just because the launcher reports a moddb status update.**
"At worst, moddb addon updates can completely break your GAMMA install in a way that is not
fixable by you, the end user." ModDB's addon model makes rolling an update back impractical.
Watch the announcements channel instead.

## 7. Backups (do these before every update)

| What | How |
|---|---|
| **Anomaly settings** | back up `Anomaly/appdata/user.ltx` |
| **Saves** | back up `Anomaly/appdata/savedgames` (to move saves to another install, drop them back into that folder; create `savedgames` if missing) |
| **MCM settings** | find the mod **"G.A.M.M.A. MCM values - Rename to keep your personal changes"** in MO2 and *rename it*, e.g. "My MCM Backup". After the next update it will sit at the bottom of the modlist, disabled; re-enable it to load your old MCM values. |
| **Modlist profile** | in MO2 open the profile dropdown → **Manage…** → create a **copy** of the default `G.A.M.M.A.` profile, then switch to the copy. Make your own modlist changes on the copy, never on the default GAMMA profile. |

Two warnings from the FAQ:

- **MCM and modlist backups are snapshots — they never update.** They capture the moment
  you made them.
- Re-make both backups **after every major version update**, starting again from the GAMMA
  default, because major updates already changed the modlist and settings.

## 8. Moving an install to another drive/folder

1. Move the **GAMMA** and **Anomaly** folders to their new home.
2. In the GAMMA folder, find and **delete the file `ModOrganizer.ini`** — the
   *configuration* file with the **white** icon. **Do not delete `ModOrganizer.exe`** (the
   blue executable).
3. From the GAMMA folder, launch `ModOrganizer.exe`. It asks where Anomaly is; pick the
   **new** Anomaly folder location.

Everything else (mods, profiles, downloads) is path-relative and comes along.

## 9. Display setup

### Renderers (DX)

| Renderer | Verdict from the official wiki |
|---|---|
| **DX11** | "has the best mod compatibility and looks the best. We always recommend running DX11 if your PC can handle it." |
| **DX10** | "broken, do not run it" |
| **DX8 / DX9** | worse compatibility and visuals, better performance. To use them you **must** use the community **DX8/DX9 modlist**: https://github.com/veerserif/gamma-dx8-and-dx9 |

In MO2 the executable dropdown offers "Anomaly (DX11)", and that is what the install
instructions tell you to pick.

### Ultrawide and 16:10

Provided by the optional mod **Dynamic Aspect Ratio Tweaks**, which ships with GAMMA but is
**left disabled**: it sits after the **"End of List"** separator — search for it in MO2 (or
scroll) and enable it. It can also be downloaded separately from its Discord post.
**4:3 aspect ratios are not supported.**

### 2K / 4K and small fonts

- If changing resolution **crashes** the game, edit `Anomaly/appdata/user.ltx` directly:
  find the line `vid_mode 1920x1080` and set your width×height, save, then launch.
  (GAMMA's own patched default `user.ltx` ships this line as `vid_mode 1920x1080`.)
- If the font is too small at 1440p/4K, **enable the "Tactical Fonts for Anomaly" option**
  for your monitor (the FAQ names this togglable option).

## 10. Saving disk space (and what not to delete)

- Deleting the install archives saves roughly **20 GB**.
- You can also delete the mods inside the **"GAMMA Disabled (do not activate)"** and
  **"End of List"** categories in MO2 — those are shipped-but-disabled containers.
- Deleting archives from `GAMMA/downloads` is **"at your own risk"**: to repair the pack,
  update GAMMA or reinstall, the launcher must re-download **all** of those files, and the
  operation fails if there is not enough space for them.

## 11. Uninstalling

Delete the **GAMMA folder** and the **Anomaly folder**. Neither game writes anything outside
its own folder. (That also means: if you want to keep saves, copy
`Anomaly/appdata/savedgames` and `Anomaly/appdata/user.ltx` out first.)

## 12. Installing via GOG (one-click)

There is an official GOG release page for **S.T.A.L.K.E.R. GAMMA** that uses GOG's one-click
mod install system — the simplest installation path (the repo's README links it:
https://www.gog.com/en/game/stalker_gamma). **It requires owning one of the base games.**
Anomaly and the classic manual install remain 100 % free and require no purchase.

## 13. First-launch checklist

After the install finishes and you are in-game, verify these before playing for real:

- [ ] MO2 is running the **`G.A.M.M.A.`** profile and the game was started from the **"Anomaly
      (DX11)"** entry.
- [ ] **Options → Controls** shows GAMMA's keybinds (they are pre-loaded — see
      `references/keybinds-settings.md` for the full default table).
- [ ] The **PDA → Guide → GAMMA** section exists and opens; it carries the pack's own manual.
- [ ] **MCM** opens from the main menu (Mod Configuration Menu) — that is where all mod
      options live.
- [ ] Start a new game via the character-creation flow; GAMMA's default difficulty in the
      shipped `user.ltx` is `gd_veteran` (Veteran), on the *Tourist / Scavenger / Survivalist*
      economy axis chosen in character creation (see `references/keybinds-settings.md`).
- [ ] Take the **"Welcome"** tutorial prompts from NPE (GAMMA Tutorials) — they cover ammo,
      healing, artefacts, repair, tasks and vehicles, and they can be re-read later in
      **MCM → NPE**.

## 14. Quick diagnostics for a fresh install

| Symptom | First checks |
|---|---|
| Far fewer mods than expected | antivirus exclusions exist and are correct; antivirus disabled during install; launcher is v8.6+; press **Install / Update GAMMA** again |
| Launcher download errors | antivirus (Norton/Avast/AVG/Malwarebytes) blocking; try again after exclusions/disable |
| MO2 asks for the game again / wrong path | you moved folders — see §8 (delete `ModOrganizer.ini`) |
| Crash on start | wrong renderer (use DX11), missing VC++ redist / .NET 3.5 / DirectX, install on the same drive with no OneDrive redirection |
| Everything looks right but performance is awful | that's the performance page, not the installer: `references/performance-tuning.md` |

Cross-references: modlist internals and DLTX → `references/modding-guide.md`; update-induced
breakage, logs and crash triage → `references/troubleshooting.md`; performance and shaders →
`references/performance-tuning.md`; controls and MCM → `references/keybinds-settings.md`.
