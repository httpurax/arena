# Certus Budding Ore — datapack

A **zero-install alternative** to the `certus-quartz-ore` mod: instead of adding ore
*items*, this datapack generates **`ae2:flawed_budding_quartz`** underground, so certus
quartz regrows where you find it — no meteorite hunting, and no mod jar to install.

* Works on Minecraft 1.21.1 + NeoForge (uses `neoforge:add_features`, so vanilla
  Fabric/Forge without NeoForge will not load it).
* Does not add any new blocks, items or textures — it only adds worldgen.

### Install

Single player:

```
<instance>/saves/<world>/datapacks/certus_budding_ore_1.21.1.zip
```

Server:

```
<server>/world/datapacks/certus_budding_ore_1.21.1.zip
```

Then in game run `/reload` (or restart), check `/datapack list` shows it enabled, and
explore **newly generated chunks**. Optional: `/gamerule doMobSpawning` etc. not needed;
just remember worldgen is not retroactive.

### What it generates

| Feature | Frequency | Y range | Result |
|---|---|---|---|
| `certusbud:certus_budding_ore` | 3 veins × up to 5 blocks per chunk | −48 … 40 | Flawed budding certus quartz veins in stone/deepslate |

Every one of those blocks **grows certus clusters** on random ticks, exactly like the
budding blocks in meteorites — and because they are *flawed*, they slowly decay to
chipped → damaged → plain quartz block as they grow. Silk Touch keeps them at their
current stage; a normal pickaxe knocks them down a stage.

That means: mine one with Silk Touch → you have a renewable certus farm without ever
touching Spatial IO. That is a bigger balance change than the ore mod, so pick one:

* **Use the ore mod** if you want *mining* certus (closest to pre-1.19 AE2).
* **Use this datapack** if you want *renewable* certus and hate meteorite hunting.
* Using both is fine, but you will get plenty of certus.

### Tuning

Edit the JSON and re-zip (or just point the world at the `src/` folder during testing):

* `data/certusbud/worldgen/placed_feature/certus_budding_ore.json` → `count` (veins per
  chunk), the `height_range` min/max.
* `data/certusbud/worldgen/configured_feature/certus_budding_ore.json` → `size` (blocks
  per vein), and swap `ae2:flawed_budding_quartz` for `ae2:damaged_budding_quartz`,
  `ae2:chipped_budding_quartz` or `ae2:flawless_budding_quartz` for a stronger/weaker
  vein (flawless never decays — that is basically creative mode certus).

`pack.mcmeta` declares `pack_format` 48 with `supported_formats` 48–64, i.e. 1.21 through
1.21.8; the worldgen JSON here is unchanged across those versions, so it keeps loading.
