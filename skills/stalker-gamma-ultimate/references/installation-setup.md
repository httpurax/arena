# Installation & Setup

A complete guide to installing S.T.A.L.K.E.R. G.A.M.M.A. — Grok's "Gigantic Automated
Modular Modpack for Anomaly" — on Windows. The most up-to-date instructions are always
in the `#how-to-install` channel of the official GAMMA Discord (discord.gg/stalker-gamma)
and the [Stalker_GAMMA wiki](https://github.com/Grokitach/Stalker_GAMMA/wiki/Installing-GAMMA).

## Overview

G.A.M.M.A. is installed on top of S.T.A.L.K.E.R. Anomaly 1.5.3, a free standalone game
built on the XRay-Monolith 64-bit engine (a custom fork of the X-Ray engine). You do
not need to own any S.T.A.L.K.E.R. game for the standard install. The modpack itself is
managed through a Mod Organizer 2 (MO2) instance, and its installer (the G.A.M.M.A.
Launcher) downloads every addon directly from ModDB or GitHub.

## Requirements

### Software dependencies

Install these before anything else:

- **.NET Framework 3.5** (from Microsoft)
- **DirectX**, latest version (from Microsoft)
- **Visual C++ Redistributable**, latest supported version, x64 architecture (from Microsoft)
- **7-Zip** — required. WinRAR and the built-in Windows archive manager are known to
  corrupt large .7z extractions. Use 7-Zip for every archive in this guide.

### Disk space

- At least **150 GB free** to start and finish the installation; 175–200 GB is
  recommended to minimize the chance of errors.
- Approximate sizes: Anomaly 1.5.3 is ~9 GB to download (~16 GB installed);
  the GAMMA RC3 archive is ~11 GB (~27 GB installed); the mods fetched by the
  launcher add ~27 GB of downloads (~76 GB installed). The finished install totals
  roughly 130 GB.

### Folders

Create two folders — one for Anomaly, one for GAMMA — following these rules:

- They must be **two different folders**, not nested inside each other.
- They must be on the **same drive**.
- They must **not** be in restricted locations: not in your Users folder (this includes
  Documents), not on the Desktop, not in OneDrive, not in Program Files.
- They must **not** be on an external USB drive.
- Example: `F:/STALKER GAMMA/Anomaly` and `F:/STALKER GAMMA/GAMMA`.

### Antivirus

Put both folders in your antivirus exclusions **before** extracting or downloading
anything. MO2's folder-virtualization system is frequently flagged by antivirus
software. Known blockers of the GAMMA Launcher downloads include Norton, Avast, AVG,
and Malwarebytes (disable them fully during the launcher install, re-enable after).
Bitdefender also tends to block MO2 and the Anomaly executables — each `.exe` must be
excluded individually from Advanced Threat Defense.

## Preparation

1. Download the **Anomaly 1.5.3 archive** (full repack, standalone — unpack into an
   empty folder and play; do not install it over an older version or another
   S.T.A.L.K.E.R. game). Mirrors: the official torrent magnet link and the ModDB
   direct download.
2. Download the **GAMMA RC3 archive** (contains the modpack base files including
   Mod Organizer 2). Pick one mirror — Gofile, Mediafire, or MEGA — they all host
   the same file.
3. Optional but recommended: verify the downloads with SHA256 checksums. In
   PowerShell, run `CertUtil -hashfile "filename" SHA256` in the download folder and
   compare against the checksums published on the wiki.

## Steps

1. Extract the Anomaly 1.5.3 archive into your Anomaly folder using 7-Zip.
2. Run `AnomalyLauncher.exe`, click Play, wait until you reach the main menu, then
   exit the game. This generates the initial configuration the modpack expects.
3. Extract the GAMMA RC3 archive into your GAMMA folder using 7-Zip.
4. In the GAMMA folder, open the `.Grok's Modpack Installer` folder and run
   `G.A.M.M.A. Launcher.exe`. Confirm it reports v8.6 in the top-left corner; if
   not, update the launcher (see below) before continuing.
5. Click **First Install Initialization**. You only do this once.
6. When Mod Organizer 2 asks which game to manage, point it at your Anomaly folder
   (the one containing `AnomalyLauncher.exe`), then close the MO2 window.
7. Leave all GAMMA Launcher options on default and click **Install / Update GAMMA**.
   This downloads and installs every addon automatically — expect it to take a long
   time depending on your connection.
8. When the launcher's green window shows "Installation finished", click the Play
   button to open Mod Organizer 2.
9. In MO2, select **Anomaly (DX11)** in the top-right dropdown and click **Run**.

The launcher creates desktop shortcuts for both the G.A.M.M.A. Launcher and Mod
Organizer 2 for future use.

### Updating the GAMMA Launcher

If the launcher is older than v8.6, update it manually: download the v8.6 launcher
archive, extract its contents into `GAMMA/.Grok's Modpack Installer`, overwriting
existing files when asked.

## Verifying the Install

- The game should launch to the main menu via MO2 with "Anomaly (DX11)" selected.
- In MO2's mod list you should see the full GAMMA modlist enabled (hundreds of
  entries). If the count looks far lower than expected, see the troubleshooting doc:
  check antivirus exclusions, update the launcher, and click "Install / Update GAMMA"
  again.
- Start a new game and confirm you can move, open the inventory, and see GAMMA's
  UI additions before investing hours into a playthrough.

## Uninstalling

To remove everything, simply **delete the GAMMA and Anomaly folders**. Neither the
game nor the modpack stores anything outside of their own folders.

## Alternative: GOG One-Click Install

Since December 2025, G.A.M.M.A. has been available as a GOG One-click Mod — a fully
integrated install with no manual archives or external launchers. It is the simplest
method, but it requires owning either S.T.A.L.K.E.R.: Call of Pripyat or S.T.A.L.K.E.R. 2
on GOG specifically. See the GOG store page for S.T.A.L.K.E.R. G.A.M.M.A.
