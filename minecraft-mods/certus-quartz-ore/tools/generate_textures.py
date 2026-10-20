#!/usr/bin/env python3
"""
Generates the original 16x16 ore textures (and the mod logo) for the
"Certus Quartz Ore" NeoForge mod.

Run from the repo root:

    python3 minecraft-mods/certus-quartz-ore/tools/generate_textures.py

Everything is drawn from scratch with Pillow - no assets are copied from
Applied Energistics 2 - so the mod textures stay MIT licensed.
"""

from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw

MOD_ROOT = Path(__file__).resolve().parents[1]
TEXTURE_DIR = MOD_ROOT / "src/main/resources/assets/certusore/textures/block"
LOGO_PATH = MOD_ROOT / "src/main/resources/certusore.png"

# ---------------------------------------------------------------- palettes ---
# Base rock noise (low, high)
STONE = (118, 146)
DEEPSLATE = (66, 92)

# Certus crystal: outline / body / highlight
CERTUS = ((64, 108, 124), (154, 214, 226), (226, 249, 255))
# Charged certus: same shape language, warm glow
CHARGED = ((112, 96, 40), (238, 214, 122), (255, 248, 206))

VARIANTS = 4
SEED = 20261020


def rock_pixel(rng: random.Random, lo: int, hi: int) -> tuple[int, int, int, int]:
    v = rng.randint(lo, hi)
    # Slight cool tint so the rock reads as "stone" rather than "mud"
    return (v - 2, v, v + 3, 255)


def paint_rock(img: Image.Image, rng: random.Random, lo: int, hi: int) -> None:
    for y in range(16):
        for x in range(16):
            img.putpixel((x, y), rock_pixel(rng, lo, hi))


def crystal_sites(rng: random.Random) -> list[tuple[int, int]]:
    """Pick non-overlapping centres for the crystal blobs."""
    sites: list[tuple[int, int]] = []
    attempts = 0
    while len(sites) < rng.randint(4, 5) and attempts < 200:
        attempts += 1
        x = rng.randint(2, 13)
        y = rng.randint(2, 13)
        if all(abs(x - sx) + abs(y - sy) >= 5 for sx, sy in sites):
            sites.append((x, y))
    return sites


def paint_crystal(
    img: Image.Image,
    cx: int,
    cy: int,
    rng: random.Random,
    outline: tuple[int, int, int],
    body: tuple[int, int, int],
    shine: tuple[int, int, int],
) -> None:
    """Draw one chunky diamond-ish crystal, Minecraft-ore style."""
    r = rng.choice((1, 2, 2, 3))
    for dy in range(-r - 1, r + 2):
        for dx in range(-r - 1, r + 2):
            x, y = cx + dx, cy + dy
            if not (0 <= x < 16 and 0 <= y < 16):
                continue
            # Squashed diamond mask gives the classic ore blob silhouette
            if abs(dx) + abs(dy) > r + 1:
                continue
            if abs(dx) + abs(dy) == r + 1:
                img.putpixel((x, y), (*outline, 255))
            elif dx + dy * 2 <= -r:  # upper-left facet catches the light
                img.putpixel((x, y), (*shine, 255))
            else:
                img.putpixel((x, y), (*body, 255))


def make_ore(
    name: str,
    variant: int,
    rock: tuple[int, int],
    crystal: tuple[tuple[int, int, int], ...],
    rng: random.Random,
) -> None:
    img = Image.new("RGBA", (16, 16))
    paint_rock(img, rng, *rock)
    outline, body, shine = crystal
    for cx, cy in crystal_sites(rng):
        paint_crystal(img, cx, cy, rng, outline, body, shine)
    out = TEXTURE_DIR / f"{name}_{variant}.png"
    img.save(out)
    print(f"  wrote {out.relative_to(MOD_ROOT)}")


def make_logo() -> None:
    """128x128 mod logo: the stone ore texture blown up with a dark frame."""
    src = Image.open(TEXTURE_DIR / "certus_quartz_ore_0.png").convert("RGBA")
    big = src.resize((112, 112), Image.NEAREST)
    logo = Image.new("RGBA", (128, 128), (24, 30, 36, 255))
    logo.paste(big, (8, 8))
    draw = ImageDraw.Draw(logo)
    draw.rectangle((7, 7, 120, 120), outline=(154, 214, 226, 255), width=2)
    logo.save(LOGO_PATH)
    print(f"  wrote {LOGO_PATH.relative_to(MOD_ROOT)}")


def main() -> None:
    TEXTURE_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating ore textures:")
    rng = random.Random(SEED)
    for variant in range(VARIANTS):
        make_ore("certus_quartz_ore", variant, STONE, CERTUS, rng)
    for variant in range(VARIANTS):
        make_ore("deepslate_certus_quartz_ore", variant, DEEPSLATE, CERTUS, rng)
    for variant in range(VARIANTS):
        make_ore("charged_certus_quartz_ore", variant, STONE, CHARGED, rng)
    for variant in range(VARIANTS):
        make_ore("deepslate_charged_certus_quartz_ore", variant, DEEPSLATE, CHARGED, rng)
    print("Generating logo:")
    make_logo()


if __name__ == "__main__":
    main()
