# Keybinds and Settings

Where every control and option lives in S.T.A.L.K.E.R. G.A.M.M.A., and how to adapt
them to your setup. Note: GAMMA ships hundreds of mods, and many add their own
keys — always confirm the exact default binding in-game rather than trusting memory,
because mod updates can change them.

## First-Launch Setup

Before installing the modpack (per the official wiki):

1. Extract Anomaly 1.5.3, run `AnomalyLauncher.exe`, press Play, and reach the
   main menu once. This generates the base configuration files.
2. Only then install GAMMA on top. Skipping the first launch means the modpack
   inherits no baseline config, which causes subtle settings bugs.

After the modpack is installed, launch through Mod Organizer 2 (dropdown set to
Anomaly (DX11), then Run) — never by double-clicking the game executable, or none
of the mods load.

## Remapping Controls

- **In-game Controls menu**: the standard Options > Controls screen covers
  movement, weapons, inventory, and interaction. Click a binding, press the new
  key. This is the only safe place to remap vanilla-style actions.
- **Avoid double-binding**: if a key does two things, one of them came from a mod.
  Decide which action keeps the key and rebind or clear the other.
- **Back up before experimenting**: MO2 profiles also store control settings, so
  switching to a test profile keeps your main bindings untouched.

## GAMMA-Specific Keys and the MCM

Most features GAMMA adds on top of Anomaly — HUD toggles, quick-access menus,
sorting hotkeys, mask/helmet visor controls, artifact container handling — register
their keys through the **Mod Configuration Menu (MCM)** rather than the vanilla
Controls screen:

1. Open the MCM from the pause menu / options.
2. Find the mod's page; its keybind section lists every action with the current
   binding.
3. Change bindings there, not by editing config files — MCM writes them in the
   format the mod actually reads.

If a GAMMA feature "does nothing" when you press its key, the cause is almost
always one of: the key was never bound (check MCM), another mod stole the binding,
or the feature's master toggle in MCM is off.

## Launcher Settings

`AnomalyLauncher.exe` (run once during setup, and available afterwards) holds the
engine-level options:

- **Renderer**: DirectX 8, 9, 10, or 11 — must match what you run from MO2. DX11 is
  the pack's target; DX10 is broken; DX8/9 need the dedicated modlist.
- **AVX toggle**: enable only on a powerful modern CPU; disable it if you get
  startup crashes.

## Settings Files and Profiles

- Game settings live in the Anomaly user files (created on first launch) and in
  MO2's profile-specific INI handling. Because MO2 virtualizes the file system,
  per-profile settings do not leak between profiles.
- Prefer changing settings through the in-game menus and MCM. Hand-editing INI
  files works but is overwritten without warning by launcher updates that touch
  the same files — and a typo in an INI can prevent the game from starting with
  no useful error message.
- If settings ever behave inexplicably (options not saving, controls resetting),
  check that the Anomaly and GAMMA folders are still in your antivirus exclusions:
  security software quarantining config writes is a classic cause.

## Recommended First Adjustments

For a new player, the highest-value settings pass after installation:

1. Set the renderer correctly (DX11) and confirm the game launches through MO2.
2. Walk through the MCM pages once to see what is configurable — you do not need
   to change anything yet, but knowing where difficulty, HUD, and survival options
   live saves hours later.
3. Adjust mouse sensitivity and invert settings in Controls before your first real
   session.
4. Tune graphics only after gameplay settings feel right (see the performance
   tuning doc) — one category at a time.
