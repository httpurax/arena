# Certus Quartz Ore

A tiny NeoForge **1.21.1** mod that puts **AE2's certus quartz ore back in the world**, for
All the Mods 10 (and any other 1.21.1 pack running Applied Energistics 2).

* Mod id: `certusore`
* Requires: Minecraft 1.21.1, NeoForge 21.1+, Applied Energistics 2 (`ae2` 19.0.0+)
* Side: client **and** server (it is a worldgen/registry mod — both sides need it)

### Why the ore vanished

Applied Energistics 2 replaced certus quartz mining with the vanilla-amethyst style
budding/growth system in 1.19 (`Certus Quartz Rework`, AE2 #6380). `ae2:quartz_ore`
and `ae2:charged_quartz_ore` no longer exist — certus quartz now comes from
**budding certus quartz with clusters**, which spawns inside **meteorites** and has to be
grown like amethyst.

This mod does *not* touch any of that. It just adds the four ore blocks back, plus the
worldgen to place them, so you can go mining for certus again.

### What it adds

| Block | Drops | Vanilla-ish Y range |
|---|---|---|
| Certus Quartz Ore | 1 certus quartz crystal (Fortune works) | −48 … 56 |
| Deepslate Certus Quartz Ore | 1 certus quartz crystal | −48 … 56 (deepslate areas) |
| Charged Certus Quartz Ore | 1 **charged** certus quartz crystal | −64 … 8 |
| Deepslate Charged Certus Quartz Ore | 1 **charged** certus quartz crystal | −64 … 8 (deepslate areas) |

* Silk Touch drops the ore block itself, so it works with a Silk Touch pickaxe in a
  pulverizer/grinder/crusher from other mods.
* Iron pickaxe or better is required to get drops.
* Registered in the AE2 item tags the old ore used (`c:ores/certus_quartz`,
  `c:ores`, plus `minecraft:mineable/pickaxe` and `needs_iron_tool`) so other mods'
  ore-processing recipes that target certus quartz can see them.
* Also shown in the creative **Natural Blocks** tab.
* New chunks only: worldgen never retro-gens existing terrain.

Ore textures are freshly drawn 16×16 originals (`tools/generate_textures.py`), not
copied from AE2, so this mod's assets stay MIT.

### Tuning the ore (no config file needed)

Worldgen is plain data, so you tune it with a tiny datapack instead of a config file —
that is also the only way a datapack-driven ore can be tuned, since the numbers are baked
into the worldgen JSON when the world loads.

Create `saves/<world>/datapacks/certusore-tweak/` with a `pack.mcmeta`:

```json
{ "pack": { "pack_format": 48, "description": "certusore tweak" } }
```

…and `data/certusore/worldgen/placed_feature/certus_quartz_ore.json` (this file
*overrides* the mod's, because the namespace matches):

```json
{
  "feature": "certusore:certus_quartz_ore",
  "placement": [
    { "type": "minecraft:count", "count": 3 },
    { "type": "minecraft:in_square" },
    { "type": "minecraft:height_range", "height": {
        "type": "minecraft:trapezoid",
        "min_inclusive": { "absolute": -48 },
        "max_inclusive": { "absolute": 56 } } },
    { "type": "minecraft:biome" }
  ]
}
```

Useful knobs: `count` (veins attempted per chunk — `0` disables the ore),
`height_range`, and `size` in
`data/certusore/worldgen/configured_feature/certus_quartz_ore.json` (blocks per vein,
default 9). Same trick works for `charged_certus_quartz_ore.json` (default 1 vein,
Y −64…8). Run `/reload`, then generate new chunks.

### Installing

1. Drop `certusore-1.0.0.jar` into the pack instance's `mods/` folder
   (Prism/ATLauncher/CurseForge instance).
2. Restart, then fly/walk into terrain you have never loaded before, or start a new world.
3. Branch-mine between **Y −48 and 56** (deepslate areas included) for certus quartz, and
   below **Y 8** for the charged variant — or just look for the cyan flecks in cave walls.

On a server, install it on the server too — client-only gets you a "missing registry
entries" disconnect.

### Building from source

Java 21 required.

```bash
cd minecraft-mods/certus-quartz-ore
./gradlew build          # jar lands in build/libs/
./gradlew runClient      # dev client with the mod loaded
# or: gradle build, if you already have Gradle 8.8+ installed
```

GitHub Actions builds it too: `.github/workflows/certus-quartz-ore.yml`
(manual dispatch, or by pushing a `certusore-v*` tag → attaches the jar to a release).

### Notes / gotchas

* AE2's own meteorites and budding certus still generate. This is additive — no
  meteorite removal, no recipe changes, no quest changes. If a pack (like ATM10)
  deliberately gated certus behind meteorites for balance, this makes early AE2 easier;
  that is the point, but it is a balance change you are opting into.
* If you also run a mod that adds its own certus ore (e.g. *Better Certus Quartz*),
  you will get both blocks. Disable one of them (see tuning above).
* Deepslate variants appear wherever the stone/deepslate ore-replaceable tags apply, so
  this works in modded biomes too.

MIT licensed. Not affiliated with the Applied Energistics 2 team.
