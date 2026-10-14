#!/usr/bin/env python3
"""Offline tests for references/farming-guide.md (atm10-quest-companion).

Stdlib-only and network-free: every case reads a file shipped in this skill. Each constant
below mirrors the pack's own quest config - AllTheMods/ATM-10 at main commit e5e3d1d83e,
pack 8.2 (2026-09-22) - exactly as it was read when the guide was written, and the tests
check that the guide still says that, and nothing invented:

  * grounding: the guide exists, carries the skill's grounding rules (in-game quest book
    and JEI authoritative, approximate flagged, nothing invented) and its provenance
    (repository, pinned commit, pack 8.2 / the 8.x stamp, the config files read), and its
    "what should I set up farming first?" answer is present and labelled as judgement;
  * Mystical Agriculture: the entry quests' verified titles and quest ids, the essence
    tiers in the config's order (Tier: 1 to Tier: 6, the awakened tier, Creative), the
    growth-accelerator ranges, and all 125 seed quests in the right Tier: row;
  * the other farming systems: chapter ids, groups and quest counts, the Apothic Spawners
    upgrade-rune ladder, the Industrial Foregoing frame ladder, the Hostile Neural
    Networks spine and its three named data-model tiers, the Productive Bees lines, the
    Food and Farming chains, and the bridges the config states between them;
  * no invented names: every backticked id in the guide is in a frozen allowlist read
    from the config, every bold name in its tables is a verified title, no
    resource-chicken mod is named, and no growth-acceleration pylon is claimed;
  * wiring: SKILL.md (version 1.5.0) points at the guide and routes farming questions to

    it, and the sibling reference docs link it and no longer claim a growth pylon;
  * offline guarantee: this suite imports no network or process module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
FARMING_MD = REFERENCES / "farming-guide.md"
PROGRESSION_MD = REFERENCES / "progression.md"
KEY_MODS_MD = REFERENCES / "key-mods.md"
GETTING_STARTED_MD = REFERENCES / "getting-started.md"

PINNED_COMMIT = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
SKILL_VERSION = "1.5.0"


SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "lang/en_us/chapter.snbt",
    "lang/en_us/chapter_group.snbt",
    "config/crash_assistant/modlist.json",
)

# chapter id (the config's filename) -> (book title, book group, quests, titled quests)
FARMING_CHAPTERS = {
    "apotheosis_2": ("Apothic Spawners", "Resources", 36, 14),
    "food_and_farming": ("Food and Farming", "Resources", 35, 31),
    "hostile_neural_networks": ("Hostile Neural Networks", "Resources", 50, 7),
    "elmystical_agriculturerr": ("Mystical Agriculture", "Resources", 191, 53),
    "productive_bees": ("Productive Bees", "Resources", 252, 195),
    "productive_trees": ("Productive Trees", "Resources", 167, 5),
    "industrial_foregoing": ("Industrial Foregoing", "Tech", 78, 24),
    "pylons": ("Pylons", "Logistics", 13, 1),
}

# Mystical Agriculture's two entry lines: verified title -> quest id.
MA_ENTRY_QUESTS = (
    ("Mystical Agriculture!", "54735C5FCD2077B3"),
    ("Inferium", "1CC4F8570A7A99EB"),
    ("Inferium Farmland", "7DFF18CFEB0B8DBE"),
    ("Infusion Crystal", "217DB12EA32E1724"),
    ("Prosperity Shards", "2DDA04088C8220D2"),
    ("Prosperity Seed Base", "1E0F92F07FDD162E"),
    ("Infusion Altar", "0B37355262121DD5"),
)

# The essence tiers, in the config's order: (subtitle, verified title, quest id, task item).
MA_TIERS = (
    ("Tier: 1", "Inferium", "1CC4F8570A7A99EB", "mysticalagriculture:inferium_essence"),
    ("Tier: 2", "Prudentium", "73350AD668200E99", "mysticalagriculture:prudentium_essence"),
    ("Tier: 3", "Tertium", "2C9C9CB71941DC01", "mysticalagriculture:tertium_essence"),
    ("Tier: 4", "Imperium", "66C52B137A4FF869", "mysticalagriculture:imperium_essence"),
    ("Tier: 5", "Supremium", "67DBE6C59C0D9D1B", "mysticalagriculture:supremium_essence"),
    ("Tier: 5 - Awakened", "Awakened Supremium", "7A103577EAE7B3F1",
     "mysticalagriculture:awakened_supremium_essence"),
    ("Tier: 6", "Insanium", "202B1F54D3F06DAB", "mysticalagradditions:insanium_essence"),
    ("Tier: Creative", "Creative Essence", "6D0A876D4E4D35AB",
     "mysticalagradditions:creative_essence"),
)

# Growth-accelerator quests and their "Range: N Blocks" subtitles, lowest tier first.
MA_ACCELERATORS = (
    ("Inferium Growth Accelerator", 9),
    ("Prudentium Growth Accelerator", 18),
    ("Tertium Growth Accelerator", 27),
    ("Imperium Growth Accelerator", 36),
    ("Supremium Growth Accelerator", 45),
    ("Awakened Supremium Growth Accelerator", 54),
)

# Every seed quest: (Tier: subtitle, the gate quest besides Infusion Altar, seed names).
# A seed's id is mysticalagriculture:<name>_seeds.
SEED_ROWS = (
    ("Tier: 1", "Inferium Farmland",
     ("air", "deepslate", "dirt", "earth", "fire", "ice", "stone", "water", "wood")),
    ("Tier: 2", "Prudentium Farmland",
     ("aluminum", "amethyst", "coal", "coral", "dye", "grains_of_infinity", "honey", "kivi",
      "limestone", "menril", "nature", "nether", "rubber", "saltpeter", "silicon", "sulfur",
      "unexplored_wood")),
    ("Tier: 2", "Creating Mob Seeds",
     ("armadillo", "chicken", "cow", "fish", "pig", "sheep", "slime", "squid", "turtle")),
    ("Tier: 3", "Tertium Farmland",
     ("azure_silver", "black_quartz", "brass", "bronze", "certus_quartz", "conductive_alloy",
      "copper", "copper_alloy", "crimson_iron", "darkstone", "glowstone", "graphite", "iron",
      "ironwood", "lead", "nether_quartz", "obsidian", "prismarine", "quartz_enriched_iron",
      "redstone", "redstone_alloy", "silver", "sky_stone", "steeleaf", "tin",
      "xychorium_gem", "zinc")),
    ("Tier: 3", "Tertium",
     ("creeper", "phantom", "rabbit", "skeleton", "spider", "zombie")),
    ("Tier: 4", "Imperium Farmland",
     ("blazing_crystal", "compressed_iron", "constantan", "dark_steel", "electrum", "end",
      "energetic_alloy", "energized_steel", "fiery_ingot", "fluix", "fluorite", "gold",
      "hop_graphite", "invar", "knightmetal", "lapis_lazuli", "nickel", "osmium", "peridot",
      "pulsating_alloy", "refined_glowstone", "refined_obsidian", "ruby", "sapphire",
      "soularium", "soulium", "steel", "uranium")),
    ("Tier: 4", "Imperium",
     ("blaze", "breeze", "enderman", "experience", "ghast")),
    ("Tier: 5", "Supremium Farmland",
     ("cyanite", "diamond", "draconium", "emerald", "end_steel", "enderium", "entro",
      "iridium", "netherite", "niotic_crystal", "platinum", "sky_steel", "spirited_crystal",
      "uraninite", "vibrant_alloy", "yellorium")),
    ("Tier: 5", "Supremium", ("wither_skeleton",)),
    ("Tier: 6", "Insanium Farmland",
     ("awakened_draconium", "dragon_egg", "nether_star", "nitro_crystal")),
    ("Tier: Magical", "Insanium Farmland", ("allthemodium", "unobtainium", "vibranium")),
)
SEED_TOTAL = 125

# Apothic Spawners: the 14 titled quests, and the upgrade-rune ladder in rank order
# (name in the quest text, task item, the quest it needs, quoted stats).
APOTHIC_TITLES = (
    "Apothic Spawners", "Blowing up Spawners", "Burning", "Health", "Youthful", "Spawn Range",
    "Ignore Light", "Redstone Active", "Opposite Day", "Quiet down you'll wake up the mobs!",
    "Echoing", "Ignore Players", "Ignore All Conditions", "No AI",
)
UPGRADE_RUNES = (
    ("Frontiersman's Spawner Upgrade Rune", "apotheosis:frontier_spawner_upgrade_rune",
     "Basic Modifications", "150 / 600 | 7 | 12 | 24"),
    ("Wayfarer's Spawner Upgrade Rune", "apotheosis:ascent_spawner_upgrade_rune",
     "Basic Modifications", "100 / 400 | 10 | 18 | 32"),
    ("Mountaineer's Spawner Upgrade Rune", "apotheosis:summit_spawner_upgrade_rune",
     "Advanced Modifications", "50 / 200 | 13 | 24 | 40"),
    ("Thundering Spawner Upgrade Rune", "apotheosis:pinnacle_spawner_upgrade_rune",
     "Advanced Modifications", "20 / 20 | 16 | 32 | 48"),
)
OTHER_SPAWNERS = (
    ("EnderIO's Spawner", "enderio:powered_spawner"),
    ("Draconic Evolution's Spawner", "draconicevolution:stabilized_spawner"),
    ("Ars Nouveau's Spawner", "ars_additions:source_spawner"),
    ("Mob Grinding Utils' Spawner", "mob_grinding_utils:entity_spawner"),
    ("Mystical Agriculture's Spawner", "mysticalagriculture:soulium_spawner"),
    ("PneumaticCraft's Spawner", "pneumaticcraft:pressurized_spawner"),
    ("Industrial Foregoing's Spawner", "industrialforegoing:mob_duplicator"),
)

# Industrial Foregoing's frame ladder, in order: (verified title, Tier: subtitle).
IF_FRAMES = (
    ("Industrial Foregoing", "Tier: 1"),
    ("Simple Machine Frame", "Tier: 2"),
    ("Advanced Machine Frame", "Tier: 3"),
    ("Supreme Machine Frame", "Tier: 4"),
)

# Hostile Neural Networks: the seven titled quests, and the only data-model tiers its text
# names, in order.
HNN_TITLES = (
    "Welcome to Hostile Neural Networks!", "Learning Mobs", "Modeling Mobs",
    "Leveling Up Data Models", "Simulating Deaths", "Creating Loot", "The Data Center",
)
HNN_MODEL_TIERS = ("Faulty", "Basic", "Self Aware")

# Productive Bees: the opening spine in order, the bee lines, and the ATM-metal ladder.
BEES_SPINE = ("Productive Bees!", "Capturing Bees!", "Your First Beehive", "Advanced Beehive",
              "Expansion Box")
BEE_LINES = (
    ("Iron Bee", "Ashy Mining + Crystalline"),
    ("Gold Bee", "Crystalline + Mason"),
    ("Coal Bee", "Magmatic + Leafcutter"),
    ("Redstone Bee", "Glowing + Chocolate Mining"),
    ("Lapis Bee", "Redstone + Blue Banded"),
    ("Diamond Bee", "Ender + Lapis"),
    ("Emerald Bee", "Diamond Bee + Slimy Bee"),
    ("Ancient Bee", "Feed Diamond Bee a Block of Netherite"),
)
ATM_BEE_LADDER = ("Ancient Bee", "Allthemodium Bee", "Vibranium Bee", "Unobtainium Bee")
ESSENCE_BEES = ("Inferium Bee", "Prudentium Bee", "Tertium Bee", "Imperium Bee",
                "Supremium Bee", "Insanium Bee", "Awakened Supremium Bee")

# Food and Farming chains, each in dependency order.
WHEAT_LINE = ("The Planter", "Punch the Grass", "Wheat", "The Bread of Life")
FISHING_LINE = ("The Start of a Fisher", "Iron Fishing Rod", "Golden Fishing Rod",
                "Diamond Fishing Rod", "Neptunium Fishing Rod")

# The five pylons the Pylons chapter has (none accelerates growth).
PYLON_IDS = frozenset(("pylons:harvester_pylon", "pylons:infusion_pylon",
                       "pylons:expulsion_pylon", "pylons:interdiction_pylon",
                       "pylons:protection_pylon"))

# Resource chickens are absent from pack 8.2: these are the chicken-related quest items
# the config does have, and names of chicken mods it does not (never to be claimed).
CHICKEN_ITEMS_IN_CONFIG = ("mysticalagriculture:chicken_seeds", "hostilenetworks:chicken",
                           "mob_grinding_utils:gm_chicken_feed", "minecraft:chicken",
                           "minecraft:egg")
INVENTED_CHICKEN_NAMES = ("roost", "hatchery", "more chickens", "morechickens",
                          "resourceful chickens", "resourcefulchickens", "chicken roost",
                          "chickens mod", "productive chickens", "productivechickens",
                          "chickenroost")
INVENTED_CHICKEN_NAMESPACES = ("chickens", "roost", "morechickens", "resourcefulchickens",
                               "productivechickens", "chickenroost", "hatchery")

# Every backticked id the guide may use - each one read from the pack config at the pinned
# commit (item ids, item tags, data-model ids, and the enchantment id). Adding an id to the
# guide means verifying it against the config first, then adding it here.
VERIFIED_ITEM_IDS = frozenset((
    # allthetweaks
    "allthetweaks:mini_exit",
    # apotheosis
    "apotheosis:ascent_spawner_upgrade_rune", "apotheosis:frontier_spawner_upgrade_rune",
    "apotheosis:infused_spawner_rune", "apotheosis:pinnacle_spawner_upgrade_rune",
    "apotheosis:spawner_chain", "apotheosis:spawner_rune",
    "apotheosis:summit_spawner_upgrade_rune",
    # apothic_enchanting
    "apothic_enchanting:occult_ender_lead",
    # apothic_spawners
    "apothic_spawners:capturing",
    # aquaculture
    "aquaculture:diamond_fishing_rod", "aquaculture:gold_fishing_rod",
    "aquaculture:iron_fishing_rod", "aquaculture:neptunium_fishing_rod",
    # ars_additions
    "ars_additions:source_spawner",
    # c
    "c:crops", "c:seeds",
    # cookingforblockheads
    "cookingforblockheads:cooking_table",
    # cucumber
    "cucumber:scythes",
    # draconicevolution
    "draconicevolution:stabilized_spawner",
    # enderio
    "enderio:powered_spawner",
    # evilcraft
    "evilcraft:spirit_reanimator",
    # farmingforblockheads
    "farmingforblockheads:market",
    # gateways
    "gateways:gate_pearl",
    # generatorgalore
    "generatorgalore:honey_generator",
    # hostilenetworks
    "hostilenetworks:allthemodium/piglich", "hostilenetworks:blank_data_model",
    "hostilenetworks:chicken", "hostilenetworks:data_center",
    "hostilenetworks:data_center_io_port", "hostilenetworks:data_model",
    "hostilenetworks:deep_learner", "hostilenetworks:end_prediction",
    "hostilenetworks:loot_fabricator", "hostilenetworks:nether_prediction",
    "hostilenetworks:overworld_prediction", "hostilenetworks:prediction",
    "hostilenetworks:prediction_matrix", "hostilenetworks:sim_chamber",
    "hostilenetworks:twilight_prediction",
    # immersiveengineering
    "immersiveengineering:cloche",
    # industrialforegoing
    "industrialforegoing:animal_baby_separator", "industrialforegoing:animal_feeder",
    "industrialforegoing:animal_rancher", "industrialforegoing:hydroponic_bed",
    "industrialforegoing:hydroponic_simulation_processor",
    "industrialforegoing:machine_frame_pity", "industrialforegoing:marine_fisher",
    "industrialforegoing:mob_crusher", "industrialforegoing:mob_duplicator",
    "industrialforegoing:mob_slaughter_factory", "industrialforegoing:plant_fertilizer",
    "industrialforegoing:plant_gatherer", "industrialforegoing:plant_sower",
    "industrialforegoing:plastic", "industrialforegoing:sewage_bucket",
    "industrialforegoing:sewage_composter", "industrialforegoing:sewer",
    "industrialforegoing:simulated_hydroponic_bed",
    # kubejs
    "kubejs:magical_soil", "kubejs:starlight_prediction",
    # minecraft
    "minecraft:beehive", "minecraft:bread", "minecraft:chicken", "minecraft:egg",
    "minecraft:feather", "minecraft:fishing_rod", "minecraft:honey_bottle",
    "minecraft:honeycomb", "minecraft:lead", "minecraft:leather",
    "minecraft:polished_blackstone", "minecraft:quartz", "minecraft:redstone",
    "minecraft:spawner", "minecraft:sugar", "minecraft:sugar_cane", "minecraft:tnt",
    "minecraft:wheat", "minecraft:wheat_seeds",
    # mob_grinding_utils
    "mob_grinding_utils:entity_spawner", "mob_grinding_utils:gm_chicken_feed",
    "mob_grinding_utils:mob_swab", "mob_grinding_utils:solid_xp_mould_baby",
    "mob_grinding_utils:xpsolidifier",
    # mysticalagradditions
    "mysticalagradditions:awakened_draconium_crux", "mysticalagradditions:creative_essence",
    "mysticalagradditions:dragon_egg_crux", "mysticalagradditions:insanium_coal_block",
    "mysticalagradditions:insanium_essence", "mysticalagradditions:insanium_farmland",
    "mysticalagradditions:nether_star_crux", "mysticalagradditions:nitro_crystal_crux",
    # mysticalagriculture
    "mysticalagriculture:awakened_supremium_essence",
    "mysticalagriculture:awakened_supremium_ingot_block",
    "mysticalagriculture:awakened_supremium_upgrade", "mysticalagriculture:awakening_altar",
    "mysticalagriculture:awakening_pedestal", "mysticalagriculture:chicken_seeds",
    "mysticalagriculture:cognizant_dust", "mysticalagriculture:compressed_iron_seeds",
    "mysticalagriculture:essence_vessel", "mysticalagriculture:experience_capsule",
    "mysticalagriculture:harvester", "mysticalagriculture:imperium_essence",
    "mysticalagriculture:imperium_upgrade", "mysticalagriculture:inferium_essence",
    "mysticalagriculture:inferium_farmland", "mysticalagriculture:inferium_seeds",
    "mysticalagriculture:inferium_upgrade", "mysticalagriculture:infusion_altar",
    "mysticalagriculture:infusion_crystal", "mysticalagriculture:infusion_pedestal",
    "mysticalagriculture:master_infusion_crystal",
    "mysticalagriculture:mystical_fertilizer", "mysticalagriculture:prosperity_seed_base",
    "mysticalagriculture:prosperity_shard", "mysticalagriculture:prudentium_essence",
    "mysticalagriculture:prudentium_upgrade", "mysticalagriculture:seed_reprocessor",
    "mysticalagriculture:soul_extractor", "mysticalagriculture:soul_jar",
    "mysticalagriculture:soulium_dagger", "mysticalagriculture:soulium_spawner",
    "mysticalagriculture:supremium_essence", "mysticalagriculture:supremium_upgrade",
    "mysticalagriculture:tertium_essence", "mysticalagriculture:tertium_upgrade",
    "mysticalagriculture:wand", "mysticalagriculture:watering_can",
    # pneumaticcraft
    "pneumaticcraft:crop_support", "pneumaticcraft:pressurized_spawner",
    "pneumaticcraft:spawner_agitator",
    # productivebees
    "productivebees:advanced_beehives", "productivebees:bee_cage",
    "productivebees:expansion_boxes", "productivebees:honey_treat",
    "productivebees:spawn_egg_configurable_bee",
    # productivelib
    "productivelib:upgrade_pollen_sieve",
    # pylons
    "pylons:expulsion_pylon", "pylons:harvester_pylon", "pylons:infusion_pylon",
    "pylons:interdiction_pylon", "pylons:protection_pylon",
    # reliquary
    "reliquary:mob_charm_fragment",
    # silentgear
    "silentgear:flax_seeds", "silentgear:flax_string",
))

# Every bold name inside the guide's tables is one of these verified quest/chapter titles
# (or the connective "and").
VERIFIED_TABLE_TITLES = frozenset((
    "Allthemodium Bee", "Ancient Bee", "Animals", "Apothic Spawners", "Automated Flux Dust",
    "Automating Awakened Supremium", "Awakened Supremium", "Coal Bee", "Craftable flowers",
    "Creating Loot", "Creative Essence", "Diamond Bee", "Emerald Bee", "Food and Farming",
    "Gold Bee", "Honey Generator", "Hostile Neural Networks", "I'm not gonna make an Egg pun",
    "Imperium", "Industrial Foregoing", "Inferium", "Inferium Farmland", "Infusion Altar",
    "Infusion Crystal", "Insanium", "Iron Bee", "Lapis Bee", "Learning Mobs",
    "Leveling Up Data Models", "Modeling Mobs", "Mystical Agriculture",
    "Mystical Agriculture!", "Mystical Fertilizer", "Plants", "Productive Bees",
    "Productive Trees", "Prosperity Seed Base", "Prosperity Shards", "Prudentium", "Pylons",
    "Redstone Bee", "Sewer", "Simulated Hydroponic Bed", "Simulating Deaths", "Supremium",
    "Tertium", "The Chickens Must Go", "The Data Center", "Unobtainium Bee", "Vibranium Bee",
    "Welcome to Hostile Neural Networks!",
))


def read(path: Path) -> str:
    """Read a shipped text file as UTF-8 (universal newlines keep Windows checkouts equal)."""
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    """Return the body of the `## heading` section, up to the next `## ` heading."""
    start = text.find(heading)
    if start < 0:
        return ""
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end < 0 else text[start:end]


def table_rows(text: str) -> "list[str]":
    return [line for line in text.splitlines() if line.startswith("|")]


class FarmingGuideTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(FARMING_MD) if FARMING_MD.is_file() else ""
        cls.lower = cls.text.lower()
        # Prose wrapped across lines, joined back so phrases can be matched whole.
        cls.flat = re.sub(r"\s*\n\s*", " ", cls.text)

    # unittest's own messages repr the whole container - here a 45 KB reference doc, full
    # of non-ASCII arrows a Windows console may not encode. Report long-text misses briefly.
    LONG_TEXT = 300

    def assertIn(self, member, container, msg=None):  # noqa: N802 - unittest's name
        if isinstance(container, str) and len(container) > self.LONG_TEXT:
            if member not in container:
                self.fail(msg or f"{member!r} not found in the {len(container)}-character text")
            return
        super().assertIn(member, container, msg)

    def assertRegex(self, text, expected_regex, msg=None):  # noqa: N802 - unittest's name
        if isinstance(text, str) and len(text) > self.LONG_TEXT:
            pattern = (expected_regex if isinstance(expected_regex, re.Pattern)
                       else re.compile(expected_regex))
            if not pattern.search(text):
                self.fail(msg or f"regex {pattern.pattern!r} did not match the "
                                 f"{len(text)}-character text")
            return
        super().assertRegex(text, expected_regex, msg)

    def assert_in_order(self, haystack: str, needles: "tuple[str, ...]", what: str) -> None:
        positions = []
        for needle in needles:
            index = haystack.find(needle)
            self.assertGreaterEqual(index, 0, f"{what}: {needle!r} is missing")
            positions.append(index)
        self.assertEqual(positions, sorted(positions),
                         f"{what} must appear in the config's order: {needles}")


# --------------------------------------------------------------------------------------
# grounding and provenance
# --------------------------------------------------------------------------------------

class TestFarmingGuideGrounding(FarmingGuideTestCase):

    def test_the_guide_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(FARMING_MD.is_file(), f"missing {FARMING_MD}")
        self.assertGreater(len(self.text.strip()), 20000, "farming-guide.md looks like a stub")
        self.assertTrue(self.text.startswith("# Farming guide"))

    def test_it_carries_the_skill_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "no recipes", "(no title in the config)"):
            self.assertIn(needle, self.lower, f"the guide must state the {needle!r} rule")
        self.assertRegex(self.lower, r"never invented|not invented|never invent")
        self.assertIn("## Grounding rules", self.text)
        self.assertIn("## What this page deliberately does not tell you", self.text)

    def test_it_names_its_sources_commit_and_pack_version(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.lower, f"the guide must name its source: {source}")
        self.assertIn(PINNED_COMMIT, self.text, "the guide must pin the full commit")
        self.assertIn("`e5e3d1d83e`", self.text)
        self.assertIn("2026-09-22", self.text)
        self.assertIn("**pack 8.2**", self.text, "the guide must date itself against pack 8.2")
        self.assertIn("8.x", self.text, "the guide must tie 8.2 to the skill's 8.x stamp")
        self.assertIn("scripts/snbt.py", self.text)

    def test_the_what_first_answer_is_present_and_labelled_as_judgement(self) -> None:
        answer = section(self.text, "## What should I set up farming first?")
        self.assertTrue(answer, "the guide must answer 'what should I set up farming first?'")
        lowered = answer.lower()
        self.assertGreaterEqual(lowered.count("judgement"), 3,
                                "the 'what first' order must be labelled as judgement")
        flat = re.sub(r"\s*\n\s*", " ", answer)
        # The two ordering claims the pack itself makes (Inferium Farmland, Productive Trees).
        self.assertIn("You'll want to start growing Inferium as soon as you can!", flat)
        self.assertIn("For Pollen you need Bees.", flat)
        for system in ("Food and Farming", "Mystical Agriculture", "Inferium", "Apothic Spawners",
                       "Industrial Foregoing", "Hostile Neural Networks", "Productive", "chickens"):
            self.assertIn(system, flat, f"the 'what first' answer must cover {system}")
        # Steps in the recommended order: food, Inferium, harvest, mobs, bees, chickens.
        self.assert_in_order(flat, ("**Food, on day one", "**Mystical Agriculture's Inferium",
                                    "**Automate the harvest", "**Mob drops", "**Bees, then Trees",
                                    "**Resource chickens"), "the 'what first' steps")

    def test_the_chapter_table_matches_the_config(self) -> None:
        for chapter_id, (title, group, quests, titled) in FARMING_CHAPTERS.items():
            pattern = (rf"^\| \*\*{re.escape(title)}\*\*[^|]*\| `{chapter_id}` \| {group} \| "
                       rf"{quests} \| {titled} \|")
            self.assertRegex(self.text, re.compile(pattern, re.MULTILINE),
                             f"chapter row for {chapter_id} must read {title}/{group}/"
                             f"{quests} quests/{titled} titled")
        self.assertIn("And Other Spawners", self.text)


# --------------------------------------------------------------------------------------
# Mystical Agriculture
# --------------------------------------------------------------------------------------

class TestMysticalAgricultureTiers(FarmingGuideTestCase):

    def test_entry_quests_carry_their_verified_ids(self) -> None:
        rows = table_rows(section(self.text, "## Mystical Agriculture"))
        for title, quest_id in MA_ENTRY_QUESTS:
            matching = [row for row in rows if row.startswith(f"| **{title}** | `{quest_id}` |")]
            self.assertTrue(matching, f"entry quest {title} must sit with quest id {quest_id}")

    def test_essence_tiers_are_listed_in_the_config_order(self) -> None:
        found = re.findall(r"^\| `(Tier: [^`]+)` \| \*\*(.+?)\*\* \| `([0-9A-F]{16})` \| "
                           r"`([a-z_]+:[a-z_]+)` \|", self.text, re.MULTILINE)
        self.assertEqual(tuple(found), MA_TIERS,
                         "the essence-tier table must list the eight tiers, with their quest "
                         "ids and items, in the config's order")

    def test_the_tier_numbers_ascend(self) -> None:
        numbers = [int(sub.split(": ")[1].split()[0]) for sub, *_ in MA_TIERS[:-1]]
        self.assertEqual(numbers, sorted(numbers))
        self.assertEqual(numbers[0], 1)
        self.assertEqual(numbers[-1], 6)
        # Prudentium through Supremium each hang off the tier before them.
        for (_, earlier, *_), (_, later, *_) in zip(MA_TIERS[1:5], MA_TIERS[2:5]):
            row = next((r for r in table_rows(self.text) if r.startswith("| `Tier: ")
                        and f"| **{later}** |" in r), "")
            self.assertTrue(row, f"the essence-tier table has no {later} row")
            self.assertIn(f"| {earlier} |", row, f"{later} must need {earlier}")

    def test_growth_accelerator_ranges_grow_by_tier(self) -> None:
        ranges = [int(n) for n in re.findall(r"Growth Accelerator \(\*Range: (\d+) Blocks\*\)",
                                             self.text)]
        self.assertEqual(ranges, [blocks for _, blocks in MA_ACCELERATORS])
        for title, blocks in MA_ACCELERATORS:
            self.assertIn(f"{title} (*Range: {blocks} Blocks*)", self.text)

    def test_every_seed_sits_in_its_verified_tier_row(self) -> None:
        rows = re.findall(r"^\| `(Tier: [^`]+)` \| (\d+) \| ([^|]+?) \| ([a-z_, ]+) \|$",
                          self.text, re.MULTILINE)
        self.assertEqual(len(rows), len(SEED_ROWS), "the seed table must have one row per gate")
        total = 0
        for (subtitle, count, gate, names), (want_sub, want_gate, want_names) in zip(rows,
                                                                                    SEED_ROWS):
            listed = tuple(name.strip() for name in names.split(","))
            self.assertEqual((subtitle, gate.strip()), (want_sub, want_gate))
            self.assertEqual(listed, want_names, f"{subtitle} / {want_gate} seeds differ")
            self.assertEqual(int(count), len(want_names), f"{subtitle} / {want_gate} count")
            total += int(count)
        self.assertEqual(total, SEED_TOTAL)
        self.assertIn(f"all {SEED_TOTAL} seed quests", self.text)

    def test_no_seed_is_listed_in_two_tiers(self) -> None:
        seen: "dict[str, str]" = {}
        for subtitle, _, names in SEED_ROWS:
            for name in names:
                self.assertNotIn(name, seen, f"{name} is in both {seen.get(name)} and {subtitle}")
                seen[name] = subtitle
        self.assertEqual(len(seen), SEED_TOTAL)
        self.assertEqual(seen["iron"], "Tier: 3")
        self.assertEqual(seen["diamond"], "Tier: 5")
        self.assertEqual(seen["air"], "Tier: 1")

    def test_tier_six_and_magical_requirements_are_quoted(self) -> None:
        for crux in ("awakened_draconium", "dragon_egg", "nether_star", "nitro_crystal"):
            self.assertIn(f"`mysticalagradditions:{crux}_crux`", self.text)
        self.assertIn("`kubejs:magical_soil`", self.text)
        self.assertIn("To grow Tier 6 or Magical Seeds you need to have a certain Crux placed "
                      "directly below the Farmland they are growing on.", self.flat)

    def test_the_supremium_description_typo_is_flagged_not_fixed(self) -> None:
        self.assertIn("This is the Tier 4 Essence, made by combining 4 Imperium", self.flat)
        self.assertIn("typo", self.lower)

    def test_mystical_agriculture_star_links_are_cross_referenced(self) -> None:
        self.assertIn("Creative Essence is needed to craft the ATM Star.", self.flat)
        self.assertIn("references/atm-star-checklist.md", self.text)


# --------------------------------------------------------------------------------------
# mob farms, bees, trees, crops
# --------------------------------------------------------------------------------------

class TestOtherFarmingSystems(FarmingGuideTestCase):

    def test_apothic_spawners_titles_and_rune_ladder(self) -> None:
        for title in APOTHIC_TITLES:
            self.assertIn(f"**{title}**", self.flat, f"missing Apothic Spawners quest: {title}")
        self.assert_in_order(self.text, tuple(name for name, *_ in UPGRADE_RUNES),
                             "the spawner upgrade-rune ladder")
        rows = table_rows(self.text)
        for name, item, needs, stats in UPGRADE_RUNES:
            row = next((r for r in rows if f"| {name} |" in r), "")
            self.assertIn(f"`{item}`", row, f"{name} must carry its task item")
            self.assertIn(f"| {needs} |", row, f"{name} must need {needs}")
            self.assertIn(f"| {stats} |", row, f"{name} stats must match the quest text")

    def test_other_spawners_are_listed_by_their_subtitles(self) -> None:
        rows = table_rows(self.text)
        for subtitle, item in OTHER_SPAWNERS:
            row = next((r for r in rows if r.startswith(f"| *{subtitle}* |")), "")
            self.assertIn(f"`{item}`", row, f"{subtitle} must ask for {item}")

    def test_industrial_foregoing_frames_ascend(self) -> None:
        self.assert_in_order(self.flat, tuple(f"**{title}** (`{tier}`" for title, tier in IF_FRAMES),
                             "Industrial Foregoing's frame ladder")
        for machine in ("mob_slaughter_factory", "mob_crusher", "mob_duplicator", "plant_gatherer",
                        "hydroponic_bed", "simulated_hydroponic_bed"):
            self.assertIn(f"`industrialforegoing:{machine}`", self.text)

    def test_hostile_neural_networks_spine_and_model_tiers(self) -> None:
        for title in HNN_TITLES:
            self.assertIn(f"**{title}**", self.text, f"missing HNN quest: {title}")
        start = self.flat.find("### Hostile Neural Networks")
        hnn = self.flat[start:self.flat.find("### Gateways", start)]
        self.assertTrue(hnn, "the guide must have a Hostile Neural Networks section")
        self.assert_in_order(hnn, HNN_MODEL_TIERS, "HNN's named data-model tiers")
        self.assertIn("three, no more", self.flat)
        self.assertIn("37 mob-prediction quests", self.flat)
        self.assertIn("33 are optional", self.flat)
        self.assertIn("`hostilenetworks:allthemodium/piglich`", self.text)

    def test_productive_bees_lines_and_tree_dependency(self) -> None:
        self.assert_in_order(self.flat, tuple(f"**{title}**" for title in BEES_SPINE),
                             "the Productive Bees opening spine")
        rows = table_rows(self.text)
        for title, subtitle in BEE_LINES:
            self.assertIn(f"| **{title}** | *{subtitle}* |", "\n".join(rows),
                          f"{title} must carry its verified subtitle")
        self.assert_in_order("\n".join(rows), tuple(f"| **{t}** |" for t in ATM_BEE_LADDER),
                             "the ATM-metal bee ladder")
        for bee in ESSENCE_BEES:
            self.assertIn(f"**{bee}**", self.text)
        self.assertIn("Productive Trees is a sister Mod to Productive Bees.", self.flat)

    def test_food_and_farming_chains_in_dependency_order(self) -> None:
        crops = section(self.text, "## Crops and food")
        flat = re.sub(r"\s*\n\s*", " ", crops)
        self.assert_in_order(flat, tuple(f"**{t}**" for t in WHEAT_LINE), "the wheat line")
        self.assert_in_order(flat, tuple(f"**{t}**" for t in FISHING_LINE), "the fishing line")
        self.assertIn("`minecraft:wheat_seeds` ×8", flat)

    def test_bridges_are_only_the_ones_the_config_states(self) -> None:
        bridges = section(self.text, "## How the farming systems connect")
        self.assertTrue(bridges)
        rows = [r for r in table_rows(bridges)[2:] if "→" in r.split("|")[1]]
        self.assertEqual(len(rows), 10, "the bridge table lists exactly the ten verified bridges")
        for quote in ("Awakened Supremium and other tiered essences can be farmed using the "
                      "Productive Bees mod.", "2 tall flowers can be crafted with MA Essence",
                      "Flux Dust can be automated using Productive Bees!"):
            self.assertIn(quote, re.sub(r"\s*\n\s*", " ", bridges))


# --------------------------------------------------------------------------------------
# no invented names
# --------------------------------------------------------------------------------------

class TestNoInventedNames(FarmingGuideTestCase):

    def test_every_backticked_id_is_one_the_config_contains(self) -> None:
        used = set(re.findall(r"`([a-z0-9_.-]+:[a-z0-9_./-]+)`", self.text))
        unknown = sorted(used - VERIFIED_ITEM_IDS)
        self.assertEqual(unknown, [], "ids not verified against the pack config: "
                                      f"{unknown}")
        self.assertGreaterEqual(len(used), 140, "the guide should quote the config's ids")

    def test_every_quest_id_is_a_verified_one(self) -> None:
        known = {quest_id for _, quest_id in MA_ENTRY_QUESTS} | {t[2] for t in MA_TIERS}
        used = set(re.findall(r"`([0-9A-F]{16})`", self.text))
        self.assertEqual(used - known, set(), "unverified FTB quest ids in the guide")
        self.assertEqual(used, known, "every verified Mystical Agriculture quest id is quoted")

    def test_bold_names_in_tables_are_verified_titles(self) -> None:
        bold = {name for row in table_rows(self.text) for name in re.findall(r"\*\*(.+?)\*\*", row)}
        self.assertEqual(sorted(bold - VERIFIED_TABLE_TITLES - {"and"}), [],
                         "a bold name in a table is not a verified quest or chapter title")

    def test_resource_chickens_are_reported_absent(self) -> None:
        chickens = section(self.text, "## Resource chickens")
        self.assertTrue(chickens, "the guide must have a Resource chickens section")
        flat = re.sub(r"\s*\n\s*", " ", chickens)
        self.assertIn("not in ATM10 8.2", flat)
        self.assertIn("no resource-chicken mod and no chicken quest line", flat)
        self.assertIn("CodeChicken Lib", flat)
        for item in CHICKEN_ITEMS_IN_CONFIG:
            self.assertIn(item, flat, f"the chicken section must cite the verified {item}")

    def test_no_resource_chicken_mod_is_named(self) -> None:
        for name in INVENTED_CHICKEN_NAMES:
            self.assertFalse(name in self.lower,
                             f"{name!r} is not in pack 8.2's modlist; the guide must not name it")
        namespaces = set(re.findall(r"`([a-z0-9_]+):", self.text))
        self.assertEqual(namespaces & set(INVENTED_CHICKEN_NAMESPACES), set(),
                         "the guide cites an item from a chicken mod pack 8.2 does not have")

    def test_no_growth_pylon_is_claimed(self) -> None:
        pylons = {i for i in re.findall(r"`(pylons:[a-z_]+)`", self.text)}
        self.assertEqual(pylons, PYLON_IDS, "the guide must cite exactly the chapter's five pylons")
        self.assertFalse("growth pylon" in self.lower, "the guide must not claim a growth pylon")
        self.assertIn("None of them is a growth accelerator", self.flat)

    def test_mods_without_quests_are_not_given_quest_steps(self) -> None:
        nobooks = section(self.text, "### In the modlist, but no quest teaches them")
        for mod in ("BotanyPots", "BotanyPots-Mystical", "BotanyTrees", "ModularBees"):
            self.assertIn(mod, nobooks)
        self.assertFalse("`botanypots:" in self.text, "no quest asks for a Botany Pots item")


# --------------------------------------------------------------------------------------
# wiring into SKILL.md and the sibling docs
# --------------------------------------------------------------------------------------

class TestSkillWiring(FarmingGuideTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.skill = read(SKILL_MD)

    def test_skill_version_is_bumped(self) -> None:
        self.assertRegex(self.skill, re.compile(rf"^version: {re.escape(SKILL_VERSION)}$",
                                                re.MULTILINE))

    def test_skill_md_routes_farming_questions_to_the_guide(self) -> None:
        self.assertIn("references/farming-guide.md", self.skill)
        self.assertIn("Farming questions go to `references/farming-guide.md`.", self.skill)
        flat = re.sub(r"\s*\n\s*", " ", self.skill)
        self.assertIn("what to set up farming first", flat)
        self.assertIn("resource chickens", flat)
        self.assertIn("never name a chicken mod", flat)
        # The grounding note dates the guide to the same commit, and the completion
        # checklist holds farming answers to it.
        self.assertIn("**So does the farming guide.**", self.skill)
        checklist = section(self.skill, "## Completion Checklist")
        self.assertIn("references/farming-guide.md", checklist)

    def test_sibling_docs_link_the_guide(self) -> None:
        for path in (PROGRESSION_MD, KEY_MODS_MD, GETTING_STARTED_MD):
            self.assertIn("farming-guide.md", read(path), f"{path.name} must link the guide")
        for sibling in ("atm-star-checklist.md", "boss-checklist.md", "creative-checklist.md",
                        "progression.md", "key-mods.md", "getting-started.md"):
            self.assertIn(f"references/{sibling}", self.text,
                          f"the guide must cross-reference {sibling}")

    def test_sibling_docs_no_longer_claim_a_growth_pylon(self) -> None:
        for path in (PROGRESSION_MD, KEY_MODS_MD, GETTING_STARTED_MD):
            lowered = read(path).lower()
            for claim in ("growth pylon", "harvest/growth pylon", "growth acceleration, chunk",
                          "harvest pylon for mystical agriculture"):
                self.assertFalse(claim in lowered, f"{path.name} still claims {claim!r}")

    def test_key_mods_tier_order_agrees_with_the_config(self) -> None:
        row = next((line for line in read(KEY_MODS_MD).splitlines()
                    if line.startswith("| **Mystical Agriculture**")), "")
        self.assertTrue(row, "key-mods.md must keep its Mystical Agriculture row")
        self.assert_in_order(row.lower(), tuple(title.lower() for _, title, *_ in MA_TIERS[:5]),
                             "key-mods.md's Mystical Agriculture tiers")


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_or_process_module(self) -> None:
        found: "set[str]" = set()
        for line in read(Path(__file__)).splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from ") and " import " in stripped:
                found.add(stripped.split()[1].split(".")[0])
        self.assertEqual(found & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(found <= {"__future__", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(found)}")


if __name__ == "__main__":
    unittest.main()
