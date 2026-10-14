#!/usr/bin/env python3
"""Offline tests for references/allthemodium-mining-guide.md (atm10-quest-companion).

Stdlib-only and network-free: the page is a static Markdown file, so every case reads it
from disk and checks it against constants transcribed from the pack's own config at the
pinned commit (AllTheMods/ATM-10 ``main`` @ e5e3d1d83e, pack 8.2, 2026-09-22) and against
the skill's shipped example file.

Covered:

  * existence and grounding: the page is not a stub, states the skill's grounding rules
    (in-game quest book + JEI authoritative, uncertain details approximate, nothing
    invented), names every pack file it was read from, and dates itself to the pinned
    commit, ``CHANGELOG.md``, pack 8.2, and the skill's 8.x stamp;
  * structure: the required sections in order; one at-a-glance row per ore (3), in
    progression order, with the verified ore ids, dimension, spawn biome, pickaxe and
    harvest tier; three numbered per-ore sections each carrying *Ore ids / Dimension /
    Where it spawns / Mined by / Harvest tier / Tracked by / The pack's own words*; the
    six-rung harvest tier ladder; the pickaxe-to-tier table;
  * key content: every ore, biome, dimension, raw-material and ore-tag id read from the
    config; the eight verbatim tooltip lines the pack installs on the ore blocks; the
    verified quest titles, quest ids, and quoted quest descriptions; the mod jar the ores
    come from; the chapter ids, titles and quest counts, cross-checked against
    ``examples/progress.example.json``;
  * grounding guards: every namespaced id on the page is on the config-verified list, no
    coordinates and no ore levels, no recipe reproduced, the one disagreement between two
    pack sources is printed rather than smoothed over, in-page anchors resolve, and the
    sibling docs the page points at exist;
  * the rest of the skill points at the page (SKILL.md, resource-farming-guide.md), and
    this suite imports no network module.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
GUIDE_MD = REFERENCES / "allthemodium-mining-guide.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
RESOURCE_FARMING_MD = REFERENCES / "resource-farming-guide.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# Where the page was read from: the pack's own quest config, worldgen tags, tooltip script,
# potion config and mod list, at the same pinned commit as the sibling docs.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "kubejs/client_scripts/tooltips.js",
    "kubejs/data/atm10/tags/worldgen/biome/allthemodium_spawnable.json",
    "config/ftbquests/quests/chapters/allthemodium.snbt",
    "config/ftbquests/quests/lang/en_us/chapters/allthemodium.snbt",
    "config/ftbquests/quests/chapters/basic_tools.snbt",
    "config/potionsmaster/allthemodium.json",
    "config/potionsmaster/vibranium.json",
    "config/potionsmaster/unobtainium.json",
    "laser_drill_ore/raw_materials",
    "config/crash_assistant/modlist.json",
)
PINNED_COMMIT = "e5e3d1d83e"
PINNED_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"

# The three ores, in the page's order: (name, task-item id the book tracks).
ORES = (
    "Allthemodium",
    "Vibranium",
    "Unobtainium",
)

# Config-verified ore block ids, raw ids and ore tags (tooltips.js, potionsmaster,
# modern_industrialization quarry recipes, industrialforegoing laser-drill recipes).
ORE_BLOCK_IDS = {
    "Allthemodium": ("allthemodium:allthemodium_ore", "allthemodium:allthemodium_slate_ore"),
    "Vibranium": ("allthemodium:vibranium_ore", "allthemodium:other_vibranium_ore"),
    "Unobtainium": ("allthemodium:unobtainium_ore",),
}
RAW_IDS = {
    "Allthemodium": "allthemodium:raw_allthemodium",
    "Vibranium": "allthemodium:raw_vibranium",
    "Unobtainium": "allthemodium:raw_unobtainium",
}
ORE_TAGS = (
    "c:ores/allthemodium",
    "c:ores/vibranium",
    "c:ores/unobtainium",
)

# The dimension each ore is in, and the biome tag (with its values) that gates generation.
# Biome tags are kubejs/data/atm10/tags/worldgen/biome/*.json at the commit.
DIMENSION_IDS = {
    "Allthemodium": ("minecraft:overworld", "allthemodium:mining"),
    "Vibranium": ("minecraft:the_nether", "allthemodium:the_other"),
    "Unobtainium": ("minecraft:the_end",),
}
SPAWN_BIOME_TAGS = {
    "Allthemodium": ("atm10:allthemodium_spawnable", ("minecraft:deep_dark",)),
    "Vibranium": ("atm10:vibranium_spawnable",
                  ("minecraft:crimson_forest", "minecraft:warped_forest")),
    "Unobtainium": ("atm10:unobtainium_spawnable", ("minecraft:end_highlands",)),
}
# The dimension explicitly ruled out for unobtainium by its own quest text.
NOT_THE_BEYOND = "allthemodium:the_beyond"

# Needed pickaxe and harvest tier, per ore. Tiers come from the `Tier: N` quest subtitles in
# the Basic Tools chapter, not from this skill.
NEEDED_PICKAXE = {
    "Allthemodium": "Netherite or better",
    "Vibranium": "Allthemodium or better",
    "Unobtainium": "Vibranium or better",
}
HARVEST_TIER = {"Allthemodium": "5", "Vibranium": "6", "Unobtainium": "6"}

# The eight tooltip lines the pack installs on the ore blocks (kubejs/client_scripts/
# tooltips.js, Minecraft § colour codes stripped). Two per ore, three for allthemodium's
# second location.
TOOLTIP_LINES = (
    "Needs at least Netherite to be mined",
    "Found in the Deep Dark Biome and will always spawn air exposed",
    "Also found in the Deep Slate Layer of Mining Dimension",
    "Needs at least AllTheModium to be mined",
    "Found in any Nether biome",
    "Also found in The Other",
    "Needs at least Vibranium to be mined",
    "Found in the End Highlands",
)

# The six-rung Harvest Tier ladder (chapter `basic_tools`): tier -> (quest id, task item,
# description). Every field read from the chapter file and its en_us lang entry.
TIER_LADDER = (
    ("1", "57F47BA495B27F83", "minecraft:cobblestone",
     "Tier 1 Harvest Level is the lowest pickaxe level, needing a pickaxe. Any pickaxe can "
     "mine these. Items that are Tier 1 would be like Stone, Furnace, and Coal Ore."),
    ("2", "3917DECAEF56A06A", "minecraft:raw_iron",
     "Tier 2 is the stone pickaxe level. It's almost only for mining Iron items."),
    ("3", "6601450C63FEEE61", "minecraft:diamond",
     "Tier 3 is Iron Pickaxe level, it mines most ores like Diamond, Emerald, and Gold."),
    ("4", "17FE0C7748DD65CA", "minecraft:ancient_debris",
     "Tier 4 is Diamond tool level, used to get Obsidian and Netherite. Also some modded "
     "ores like Uranium and Platinum."),
    ("5", "03E05018D64DDEE1", "allthemodium:raw_allthemodium",
     "Tier 5 is basically just for Allthemodium Ore, not much else."),
    ("6", "09733948CBCB3FB9", "allthemodium:raw_unobtainium",
     "Tier 6 is the highest tier, anything that is breakable can be mined with it, "
     "including Vibranium and Unobtainium."),
)
TIER_QUEST_TITLES = {
    tier: f"Harvest Tier {tier}" for tier, _quest_id, _item, _desc in TIER_LADDER
}

# Pickaxe -> tier, from the Basic Tools chapter's `Tier: N` quest subtitles.
PICKAXE_TIERS = (
    ("minecraft:netherite_pickaxe", "5", "299F56B753286D0C"),
    ("mekanismtools:refined_obsidian_pickaxe", "5", "512396B331108BAF"),
    ("allthemodium:allthemodium_pickaxe", "6", "609D03E335CF32E2"),
    ("allthemodium:vibranium_pickaxe", "6", "609D03E335CF32E2"),
    ("allthemodium:unobtainium_pickaxe", "6", "609D03E335CF32E2"),
    ("allthemodium:alloy_pick", "6", "609D03E335CF32E2"),
    ("mysticalagriculture:supremium_pickaxe", "6", "58DDD32F849940A0"),
    ("mysticalagriculture:awakened_supremium_pickaxe", "6", "58DDD32F849940A0"),
)

# Chapter ids, titles and quest counts, cross-checked against examples/progress.example.json.
CHAPTERS = {
    "allthemodium": ("Chapter 2: Allthemodium", "4293754F9B2D05F0", 54, "endgame",
                     "Main Questline"),
    "basic_tools": ("Basic Tools", "4B9D26E0087CD163", 77, "early-game", "Tools and Gear"),
}

# Verified quest titles and ids in Chapter 2: Allthemodium, with the quoted description text.
QUEST_IDS = {
    "Allthemodium": "4B2146C9527C54E7",
    "Ancient City": "111E4ACF7D570EE8",
    "Allthemodium Ingot": "201EE3566D4D3123",
    "Teleport Pad": "07FDA46D83F8360D",
    "Mining Dimension": "6D738730B371B152",
    "The Nether": "0CC0632E8276C787",
    "Overworld": "2C4299D33D419AA0",
    "The End": "2EDE91023F7924FB",
    "The Other": "15FEA03A2CDBA33B",
    "The Beyond": "11E957CDEFA0CAAB",
    "Vibranium Ingot": "144BB025516E0994",
    "Unobtainium Ingot": "4A079D40C0AF6BC3",
    "Allthemodium Pickaxes": "609D03E335CF32E2",
}
# The untitled quarry-warning follow-up: no `title` in the lang file, only a quest_desc.
UNTITLED_QUEST = "18FAD56CDE05646A"

# Quest descriptions quoted verbatim on the page (en_us lang file, pack 8.2).
QUEST_QUOTES = (
    "Only the hardest Structure in Vanilla Minecraft. So of course that's where you'll have "
    "to look for Allthemodium! You can find the Ore in the walls of Caves around the "
    "Ancient Cities, it's Glowing so it'll be easy to spot just very rare! You will also be "
    "able to locate it in any Deep Dark Biome.",
    "To mine Allthemodium you'll need a Pickaxe that is Netherite Tier or higher!",
    "I recommend making 2 Teleport Pads with the Nuggets! You can use those to get to the "
    "Mining Dimension to find more Allthemodium or The Other to find other adventures.",
    "Vibranium is the next ore after Allthemodium, so of course it requires Allthemodium "
    "Pickaxe (or the same tier) to mine it. You can find it rarely in The Nether or "
    "abundantly in The Other.",
    "It is also recommend to Ore Process it to get more.",
    "No it isn't found in The Beyond. You can find Unobtainium Ore very rarely in End "
    "Highlands Biomes. Those are usually where End Cities spawn as well! You'll need a "
    "Vibranium Pickaxe (or same Tier) to Mine the Ore. Do I need to still tell you to Ore "
    "process it?",
    "There's nothing here! You might want an Angel Block.",
    "Ore spawns differ for the Y Level and layer in the Mining Dimension.",
    "You can also mine for Vibranium (and other ores!) or find it and better in the "
    "structures!",
    "You can't set up Quarries for many blocks in The Other though, no cheesing anything "
    "here.",
    "Now it will Mine Allthemodium but Void the drops... might want to be careful with your "
    "Quarries now!",
    "I recommend Mining with Ore Sight Potions if you are looking strictly for Allthemodium!",
    "Place the Teleport Pad in the Overworld to go to the Mining Dimension.",
    "Place the Teleport Pad in The Nether to go to The Other.",
    "Below the surface is almost every single Ore.",
)

# The mod jar the ores come from (config/crash_assistant/modlist.json at the commit).
MOD_JAR = "allthemodium-3.0.1_mc_1.21.1.jar"
MOD_VERSION = "Allthemodium 3.0.1"

# Every namespaced id the page may print -- each one read from the pack config at the
# commit (tooltips.js, biome tags, quest task items/values, potionsmaster, laser-drill
# recipes, modlist). A new id on the page must be verified against the config and added
# here on purpose: nothing is invented.
VERIFIED_IDS = frozenset({
    # ore blocks
    "allthemodium:allthemodium_ore",
    "allthemodium:allthemodium_slate_ore",
    "allthemodium:vibranium_ore",
    "allthemodium:other_vibranium_ore",
    "allthemodium:unobtainium_ore",
    # raw materials
    "allthemodium:raw_allthemodium",
    "allthemodium:raw_vibranium",
    "allthemodium:raw_unobtainium",
    # ore tags (potionsmaster oretag fields)
    "c:ores/allthemodium",
    "c:ores/vibranium",
    "c:ores/unobtainium",
    # spawn-biome tags (kubejs/data/atm10/tags/worldgen/biome)
    "atm10:allthemodium_spawnable",
    "atm10:vibranium_spawnable",
    "atm10:unobtainium_spawnable",
    # biome ids
    "minecraft:deep_dark",
    "minecraft:crimson_forest",
    "minecraft:warped_forest",
    "minecraft:end_highlands",
    # dimension ids
    "minecraft:overworld",
    "minecraft:the_nether",
    "minecraft:the_end",
    "allthemodium:mining",
    "allthemodium:the_other",
    "allthemodium:the_beyond",
    # structure
    "minecraft:ancient_city",
    # tier-ladder task items
    "minecraft:cobblestone",
    "minecraft:raw_iron",
    "minecraft:diamond",
    "minecraft:ancient_debris",
    # pickaxes
    "minecraft:netherite_pickaxe",
    "mekanismtools:refined_obsidian_pickaxe",
    "allthemodium:allthemodium_pickaxe",
    "allthemodium:vibranium_pickaxe",
    "allthemodium:unobtainium_pickaxe",
    "allthemodium:alloy_pick",
    "mysticalagriculture:supremium_pickaxe",
    "mysticalagriculture:awakened_supremium_pickaxe",
    # ore-sight potion (quoted from a quest reward; the other two are not quoted as ids)
    "potionsmaster:allthemodium",
})

# Recipes the page must never reproduce: the Teleport Pad's craft and the pad's pad count.
NOT_REPRODUCED = (
    "4 Allthemodium Nuggets",
    "Nuggets and an Ender Pearl",
    "4x5 Glowstone",
)

COORDINATE_PATTERNS = (
    re.compile(r"\b[xyz]\s*[=:]\s*-?\d", re.IGNORECASE),            # x=100, y: 64
    re.compile(r"\by\s*(?:level\s*)?-?\d+\b", re.IGNORECASE),        # Y -40, Y Level 0
    re.compile(r"-?\d+\s*,\s*-?\d+\s*,\s*-?\d+"),                    # 100, 64, -200
    re.compile(r"\b\d+\s*k\b", re.IGNORECASE),                       # 10k
    re.compile(r"\bx\s*/\s*z\b", re.IGNORECASE),                     # X/Z
    re.compile(r"multiple of", re.IGNORECASE),                       # "a multiple of 10k"
)

EXPECTED_SECTIONS = (
    "Provenance",
    "Grounding rules",
    "The three ores at a glance",
    "Ore by ore",
    "What mines them: the harvest tier ladder",
    "Getting more per ore",
    "Related pages",
    "What this page deliberately does not tell you",
    "Using this page in a session",
)
AT_A_GLANCE_COLUMNS = ("Ore", "Ore block id(s)", "Dimension", "Spawns in", "Needed pickaxe",
                       "Harvest tier", "Tracked by")
FIELDS = ("**Ore ids:**", "**Dimension:**", "**Where it spawns:**", "**Mined by:**",
          "**Harvest tier:**", "**Tracked by:**", "**The pack's own words")
SIBLING_DOCS = ("resource-farming-guide.md", "ore-processing-ladder.md",
                "armor-tools-ladder.md", "dimension-guide.md", "atm-star-checklist.md",
                "progression.md")

ID_TOKEN = re.compile(r"#?\b[a-z0-9_]+:[a-z0-9_./]*[a-z0-9_]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def flatten(text: str) -> str:
    """Collapse wrapped Markdown lines so multi-line sentences can be matched whole."""
    return re.sub(r"\s+", " ", text)


def strip_quotes(text: str) -> str:
    """Drop Markdown '> ' blockquote markers so quoted quest text matches as one sentence."""
    return "\n".join(re.sub(r"^\s*>\s?", "", line) for line in text.splitlines())


def h2_sections(text: str) -> "list[tuple[str, str]]":
    """[(heading, body)] for every '## ' section, in document order."""
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def section(text: str, heading_prefix: str) -> str:
    for heading, body in h2_sections(text):
        if heading.startswith(heading_prefix):
            return body
    return ""


def h3_sections(body: str) -> "list[tuple[str, str]]":
    parts = re.split(r"^### (.+)$", body, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def table_rows(body: str) -> "list[list[str]]":
    """Data rows of the first Markdown table in ``body``, as stripped cells."""
    rows: "list[list[str]]" = []
    in_table = False
    for line in body.splitlines():
        if line.startswith("|"):
            in_table = True
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append(cells)
        elif in_table:
            break
    # rows[0] is the header, rows[1] the |---| separator.
    return rows


def github_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    return slug.replace(" ", "-")


class GuideTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(GUIDE_MD)
        cls.lower = cls.text.lower()
        cls.flat = flatten(strip_quotes(cls.text))
        cls.flat_lower = cls.flat.lower()


# --------------------------------------------------------------------------------------
# existence, provenance, grounding rules
# --------------------------------------------------------------------------------------

class TestExistenceAndGrounding(GuideTestCase):

    def test_page_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.text.strip()), 15000,
                           "allthemodium-mining-guide.md looks like a stub")
        self.assertTrue(self.text.startswith("# Allthemodium mining guide"),
                        "the page must open with its '# Allthemodium mining guide' title")

    def test_states_the_skill_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "nothing here was invented"):
            self.assertIn(needle, self.lower, f"must state the {needle!r} rule")
        self.assertIn("his game wins", self.flat_lower)

    def test_says_the_book_gates_nothing(self) -> None:
        self.assertIn(
            "In this modpack, quests are optional. Mods are not gated behind completing any "
            "quests!", self.flat)

    def test_names_its_sources_and_dates_itself(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.lower, f"must name its source: {source}")
        self.assertIn(PINNED_COMMIT, self.text)
        self.assertIn(PINNED_COMMIT_FULL, self.text, "the commit link must be the full SHA")
        self.assertIn("CHANGELOG.md", self.text)
        self.assertIn("pack 8.2", self.text)
        self.assertIn("8.x", self.text, "must tie the version read to the skill's 8.x stamp")
        self.assertIn("2026-09-22", self.text)
        self.assertIn('modpackVersion = "8.2"', self.text, "must cite bcc-common.toml")

    def test_names_the_mod_the_ores_come_from(self) -> None:
        self.assertIn(MOD_JAR, self.text)
        self.assertIn(MOD_VERSION, self.flat)

    def test_credits_the_tooltip_script_as_the_strongest_source(self) -> None:
        provenance = section(self.text, "Provenance")
        self.assertIn("tooltips.js", provenance)
        self.assertIn("in-game tooltip lines", provenance)
        rules = flatten(section(self.text, "Grounding rules"))
        self.assertIn("strongest source here", rules)
        self.assertIn("still a snapshot", rules)


# --------------------------------------------------------------------------------------
# structure
# --------------------------------------------------------------------------------------

class TestStructure(GuideTestCase):

    def test_required_sections_in_order(self) -> None:
        headings = [heading for heading, _ in h2_sections(self.text)]
        self.assertEqual(len(headings), len(EXPECTED_SECTIONS), headings)
        for heading, expected in zip(headings, EXPECTED_SECTIONS):
            self.assertTrue(heading.startswith(expected), f"{heading!r} != {expected!r}")

    def test_at_a_glance_table_has_one_row_per_ore_in_order(self) -> None:
        rows = table_rows(section(self.text, "The three ores at a glance"))
        header, data = rows[0], rows[2:]
        for column in AT_A_GLANCE_COLUMNS:
            self.assertTrue(any(cell.startswith(column) for cell in header),
                            f"at-a-glance table needs a {column!r} column: {header}")
        self.assertEqual(len(data), len(ORES))
        for cells, name in zip(data, ORES):
            self.assertEqual(cells[0], name)
            for ore_id in ORE_BLOCK_IDS[name]:
                self.assertIn(f"`{ore_id}`", cells[1], f"{name}: missing {ore_id}")
            for dimension_id in DIMENSION_IDS[name]:
                self.assertIn(f"`{dimension_id}`", cells[2], f"{name}: missing {dimension_id}")
            self.assertEqual(cells[4], NEEDED_PICKAXE[name])
            self.assertEqual(cells[5], HARVEST_TIER[name])
            self.assertTrue(cells[6].startswith("Chapter 2: Allthemodium"), cells[6])

    def test_three_numbered_ore_sections_with_all_the_fields(self) -> None:
        sections = [(heading, body) for heading, body
                    in h3_sections(section(self.text, "Ore by ore"))
                    if re.match(r"\d+\. ", heading)]
        self.assertEqual(len(sections), len(ORES))
        for index, ((heading, body), name) in enumerate(zip(sections, ORES), 1):
            self.assertTrue(heading.startswith(f"{index}. {name}"), heading)
            self.assertIn(f"`{ORE_BLOCK_IDS[name][0]}`", heading)
            for field in FIELDS:
                self.assertIn(field, body, f"{heading!r} is missing {field}")
            for ore_id in ORE_BLOCK_IDS[name]:
                self.assertIn(f"`{ore_id}`", body, f"{heading!r} must name {ore_id}")
            for dimension_id in DIMENSION_IDS[name]:
                self.assertIn(f"`{dimension_id}`", body, f"{heading!r} must name {dimension_id}")
            tag, biomes = SPAWN_BIOME_TAGS[name]
            self.assertIn(f"`{tag}`", body, f"{heading!r} must name {tag}")
            for biome in biomes:
                self.assertIn(f"`{biome}`", body, f"{heading!r} must name {biome}")
            self.assertIn(f"`{RAW_IDS[name]}`", body, f"{heading!r} must name {RAW_IDS[name]}")
            self.assertIn(f"**{HARVEST_TIER[name]}.**", flatten(body),
                          f"{heading!r} must state harvest tier {HARVEST_TIER[name]}")
            self.assertIn(NEEDED_PICKAXE[name], flatten(body),
                          f"{heading!r} must state the needed pickaxe")

    def test_unobtainium_section_rules_out_the_beyond(self) -> None:
        body = dict((heading, body) for heading, body
                    in h3_sections(section(self.text, "Ore by ore")))
        uno = [b for h, b in body.items() if h.startswith("3. Unobtainium")]
        self.assertEqual(len(uno), 1)
        self.assertIn(f"`{NOT_THE_BEYOND}`", uno[0])
        self.assertIn("No it isn't found in The Beyond.", flatten(uno[0]))

    def test_harvest_tier_ladder_has_six_rungs_in_order(self) -> None:
        rows = table_rows(section(self.text, "What mines them: the harvest tier ladder"))[2:]
        self.assertEqual(len(rows), len(TIER_LADDER))
        for cells, (tier, quest_id, item, description) in zip(rows, TIER_LADDER):
            self.assertEqual(cells[0], tier)
            self.assertIn(f"*{TIER_QUEST_TITLES[tier]}*", cells[1])
            self.assertIn(f"`{quest_id}`", cells[2], f"tier {tier} must cite its quest id")
            self.assertIn(f"`{item}`", cells[3], f"tier {tier} must name its task item")
            self.assertIn(description, flatten(cells[4]), f"tier {tier} description mismatch")

    def test_pickaxe_tier_table_lists_every_pickaxe_at_its_tier(self) -> None:
        body = section(self.text, "What mines them: the harvest tier ladder")
        pick = [b for heading, b in h3_sections(body)
                if heading.startswith("Which pickaxe sits at which tier")]
        self.assertEqual(len(pick), 1, "the pickaxe table must exist exactly once")
        joined = flatten(pick[0])
        for pickaxe, tier, quest_id in PICKAXE_TIERS:
            row = [line for line in pick[0].splitlines() if f"`{pickaxe}`" in line]
            self.assertEqual(len(row), 1, f"{pickaxe} must appear on exactly one row")
            cells = [cell.strip() for cell in row[0].strip().strip("|").split("|")]
            self.assertEqual(cells[1], tier, f"{pickaxe} must be listed at tier {tier}")
            self.assertIn(f"`{quest_id}`", cells[2], f"{pickaxe} must cite {quest_id}")
        self.assertIn("all three ATM picks plus the alloy pick", joined)


# --------------------------------------------------------------------------------------
# key content
# --------------------------------------------------------------------------------------

class TestKeyContent(GuideTestCase):

    def test_every_ore_raw_and_tag_id_is_covered(self) -> None:
        for name in ORES:
            for ore_id in ORE_BLOCK_IDS[name]:
                self.assertIn(f"`{ore_id}`", self.text, f"missing {ore_id}")
            self.assertIn(f"`{RAW_IDS[name]}`", self.text, f"missing {RAW_IDS[name]}")
        for tag in ORE_TAGS:
            self.assertIn(f"`{tag}`", self.text, f"missing {tag}")

    def test_every_spawn_biome_tag_and_value_is_covered(self) -> None:
        for tag, biomes in SPAWN_BIOME_TAGS.values():
            self.assertIn(f"`{tag}`", self.text, f"missing {tag}")
            for biome in biomes:
                self.assertIn(f"`{biome}`", self.text, f"missing {biome}")

    def test_the_pack_tooltip_lines_are_quoted_verbatim(self) -> None:
        for line in TOOLTIP_LINES:
            self.assertIn(line, self.flat, f"missing tooltip line: {line!r}")

    def test_quest_titles_and_ids(self) -> None:
        for title, quest_id in QUEST_IDS.items():
            self.assertIn(f"*{title}*", self.flat, f"missing quest title: {title}")
            self.assertIn(f"`{quest_id}`", self.text, f"missing quest id for {title}")
        self.assertIn(f"`{UNTITLED_QUEST}`", self.text)
        self.assertIn("(no title in the config)", self.flat)

    def test_key_quest_text_is_quoted_verbatim(self) -> None:
        for quote in QUEST_QUOTES:
            self.assertIn(quote, self.flat, f"missing quest-text quote: {quote!r}")

    def test_chapter_ids_titles_counts_and_stages_match_the_example_file(self) -> None:
        example = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        by_id = {chapter["id"]: chapter for chapter in example["chapters"]}
        for chapter_id, (title, hex_id, count, stage, group) in CHAPTERS.items():
            self.assertIn(chapter_id, by_id, f"{chapter_id} is not a shipped chapter")
            self.assertEqual(by_id[chapter_id]["title"], title)
            self.assertEqual(by_id[chapter_id]["stage"], stage)
            self.assertEqual(by_id[chapter_id]["group"], group)
            self.assertIn(f"`{chapter_id}`", self.text, f"missing chapter id {chapter_id}")
            self.assertIn(f"`{hex_id}`", self.text, f"missing chapter hex id for {chapter_id}")
            self.assertIn(title, self.text)
            self.assertIn(f"**{count} quests**", self.flat,
                          f"{chapter_id} must be cited with its pack-8.2 quest count")

    def test_the_hedged_points_stay_hedged(self) -> None:
        rules = flatten(section(self.text, "Grounding rules"))
        self.assertIn("A biome tag proves", rules)
        self.assertIn("do not say the same thing", rules)
        self.assertIn("not smooth it over", self.text)
        self.assertIn("judgement", self.flat_lower)
        self.assertIn("the pack's own adverbs", self.flat_lower)

    def test_the_two_pack_sources_that_disagree_are_both_printed(self) -> None:
        rules = flatten(section(self.text, "Grounding rules"))
        self.assertIn("Found in any Nether biome", rules)
        self.assertIn("atm10:vibranium_spawnable", rules)
        vib = dict((heading, body) for heading, body
                   in h3_sections(section(self.text, "Ore by ore")))
        body = [b for h, b in vib.items() if h.startswith("2. Vibranium")][0]
        self.assertIn("These two config sources do not agree", flatten(body))
        self.assertIn("will not smooth it over", flatten(body))


# --------------------------------------------------------------------------------------
# grounding guards
# --------------------------------------------------------------------------------------

class TestGroundingGuards(GuideTestCase):

    def test_every_namespaced_id_is_config_verified(self) -> None:
        found = {token for token in ID_TOKEN.findall(self.text)
                 if not token.startswith(("https:", "http:"))}
        unverified = sorted(found - VERIFIED_IDS)
        self.assertEqual(unverified, [], "ids not verified against the pack config: "
                         f"{unverified} -- verify them and add them to VERIFIED_IDS")

    def test_no_coordinates(self) -> None:
        for pattern in COORDINATE_PATTERNS:
            match = pattern.search(self.text)
            self.assertIsNone(match, f"coordinate-like text: {match and match.group(0)!r}")

    def test_no_ore_level_is_published(self) -> None:
        withheld = flatten(section(self.text, "What this page deliberately does not tell you"))
        self.assertIn("No ore levels.", withheld)
        self.assertIn("the pack declines to publish them", withheld)
        self.assertIn("the drill's setting, not a spawn range", withheld)
        self.assertIn("does not repeat it as an ore level", self.flat)

    def test_no_recipe_is_reproduced(self) -> None:
        for phrase in NOT_REPRODUCED:
            self.assertNotIn(phrase.lower(), self.flat_lower,
                             f"recipe text must stay in JEI: {phrase}")
        self.assertIn("**No recipes**", self.flat)

    def test_in_page_anchors_resolve(self) -> None:
        slugs = {github_slug(heading)
                 for heading in re.findall(r"^#{1,6} (.+)$", self.text, flags=re.MULTILINE)}
        anchors = re.findall(r"\]\(#([^)]+)\)", self.text)
        self.assertTrue(anchors, "the at-a-glance intro links the per-ore sections")
        for anchor in anchors:
            self.assertIn(anchor, slugs, f"broken in-page anchor: #{anchor}")

    def test_sibling_docs_are_linked_and_exist(self) -> None:
        related = section(self.text, "Related pages")
        for sibling in SIBLING_DOCS:
            self.assertIn(f"references/{sibling}", related, f"must point at {sibling}")
            self.assertTrue((REFERENCES / sibling).is_file(), f"{sibling} is missing")

    def test_untitled_quests_are_marked_never_renamed(self) -> None:
        # 18FAD56CDE05646A has no `title` key in the lang file: the page must say so rather
        # than invent a name for it.
        index = self.text.index(f"`{UNTITLED_QUEST}`")
        window = flatten(self.text[max(0, index - 400):index + 200])
        self.assertIn("no title in the config", window)


# --------------------------------------------------------------------------------------
# the rest of the skill points at the page
# --------------------------------------------------------------------------------------

class TestCrossReferences(unittest.TestCase):

    def test_skill_md_routes_mining_questions_to_the_page(self) -> None:
        skill = flatten(read(SKILL_MD))
        self.assertIn("references/allthemodium-mining-guide.md", skill)
        self.assertIn("Allthemodium-ore questions go to", skill)
        checklist = flatten(section(read(SKILL_MD), "Completion Checklist"))
        self.assertIn("references/allthemodium-mining-guide.md", checklist)
        self.assertIn("allthemodium-mining-guide.md",
                      flatten(section(read(SKILL_MD), "Research Grounding")))

    def test_resource_farming_guide_points_at_the_page(self) -> None:
        farming = read(RESOURCE_FARMING_MD)
        self.assertIn("references/allthemodium-mining-guide.md", farming,
                      "resource-farming-guide.md must point at the mining guide")


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestOffline(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_module(self) -> None:
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        imported: "set[str]" = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(imported <= {"__future__", "ast", "json", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(imported)}")


if __name__ == "__main__":
    unittest.main()
