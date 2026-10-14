#!/usr/bin/env python3
"""Offline tests for references/mob-farm-progression.md.

Stdlib-only and network-free: every check reads files that ship with the skill
(the reference doc, SKILL.md, examples/progress.example.json) and compares them
against constants transcribed from the AllTheMods/ATM-10 quest config at the
pinned commit e5e3d1d83e (pack 8.2, 2026-09-22) -- the same snapshot the
existing endgame reference docs are grounded in.

Mirrored verified data:

  * the Apothic Spawners chapter (id ``apotheosis_2``): its root quest, the
    *Blowing up Spawners* -> *Basic Modifications* -> rune split, the four
    Spawner Upgrade Runes with their quoted stats, the seven "Other Spawners"
    mod spawners and the spawn-egg routes, all by verified quest title,
    subtitle, or task item id;
  * the Hostile Neural Networks simulation line (7 titled quests, 37 untitled
    per-mob prediction quests, 5 untitled dimension-prediction quests);
  * the cross-chapter anchors: EvilCraft's *Mob Farms using Blood*, the
    Industrial Foregoing machines, *Routers for Mob Farms*, Mystical
    Agriculture's *Creating Mob Seeds*, the Bounty Board kill ladders, and
    Chapter 1's *Kill The Warden* / *Kill The Wither*;
  * no-invented-names checks: the doc must reject soul-shard-style shortcuts
    the config does not have, mark untitled quests in place, and never state a
    requirement the config does not carry;
  * SKILL.md wiring and the version bump;
  * the doc's stage claims match the shipped ``examples/progress.example.json``
    chapter list (offline stand-in for the pack checkout).
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
DOC_PATH = SKILL_ROOT / "references" / "mob-farm-progression.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# The snapshot this page was read from -- same commit the creative checklist pins.
PACK_COMMIT = "e5e3d1d83e"
PACK_VERSION = "8.2"
PACK_STAMP = "8.x"
PACK_DATE = "2026-09-22"

# Source files in the pack repo that supplied the page's data (same provenance
# set as the endgame docs, narrowed to the chapters actually read).
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters/apotheosis_2.snbt",
    "config/ftbquests/quests/chapters/hostile_neural_networks.snbt",
    "config/ftbquests/quests/lang/en_us/chapters/",
    "config/crash_assistant/modlist.json",
)

# Chapters the page names, with the stage/group the shipped example file gives
# them (offline mirror of the pack's chapter list at the pinned commit).
CHAPTERS_IN_DOC = {
    "apotheosis_2": ("Apothic Spawners", "Resources", "early-game"),
    "hostile_neural_networks": ("Hostile Neural Networks", "Resources", "tech"),
    "elmystical_agriculturerr": ("Mystical Agriculture", "Resources", "tech"),
    "industrial_foregoing": ("Industrial Foregoing", "Tech", "tech"),
    "evilcraft": ("EvilCraft", "Magic", "magic"),
    "modular_router": ("Modular Routers", "Logistics", "tech"),
    "apothic_enchanting": ("Apothic Enchanting", "Magic", "magic"),
    "natures_aura": ("Nature's Aura", "Magic", "magic"),
    "bounty_board": ("Bounty Board", "", "early-game"),
    "mainquestline_part_1": ("Chapter 1: The Beginning", "Main Questline", "early-game"),
}

# The Apothic Spawners chapter (36 quests): every quest title the page relies on,
# exactly as the chapter's en_us lang file gives it (formatting codes stripped).
APOTHIC_SPAWNERS_QUEST_COUNT = 36
APOTHIC_SPAWNERS_TITLED = (
    "Apothic Spawners",
    "Blowing up Spawners",
    "Ignore Light",
    "Youthful",
    "Spawn Range",
    "Redstone Active",
    "Health",
    "Burning",
    "Quiet down you'll wake up the mobs!",
    "Opposite Day",
    "No AI",
    "Ignore Players",
    "Ignore All Conditions",
    "Echoing",
)
# Quests the config leaves untitled but whose subtitle is verified; the page must
# use the subtitle, never a derived title.
APOTHIC_SPAWNERS_SUBTITLED = (
    "Basic Modifications",
    "Advanced Modifications",
    "Don't you despawn on me, Mobs",
    "That's no Spawn Egg!",
    "EnderIO's Spawner",
    "Draconic Evolution's Spawner",
    "PneumaticCraft's Spawner",
    "Mob Grinding Utils' Spawner",
    "Mystical Agriculture's Spawner",
    "Industrial Foregoing's Spawner",
    "Ars Nouveau's Spawner",
    "Capturing Books",  # task title on an untitled quest
    "Mob Charm Fragments",  # task title on an untitled quest
    "Spawn Eggs",  # task title on the hidden header quest
)

# Task item ids verified in chapters/apotheosis_2.snbt (and one enchantment id
# read from a smart-filter component). Every id the page prints in backticks
# from that chapter must be on this list.
APOTHIC_SPAWNERS_ITEM_IDS = (
    "minecraft:spawner",
    "minecraft:tnt",
    "minecraft:quartz",
    "apotheosis:spawner_chain",
    "apotheosis:spawner_rune",
    "apotheosis:infused_spawner_rune",
    "apotheosis:ignore_light_spawner_rune",
    "apotheosis:youthful_spawner_rune",
    "apotheosis:spawn_range_spawner_rune",
    "apotheosis:redstone_control_spawner_rune",
    "apotheosis:initial_health_spawner_rune",
    "apotheosis:burning_spawner_rune",
    "apotheosis:silent_spawner_rune",
    "apotheosis:no_ai_spawner_rune",
    "apotheosis:ignore_players_spawner_rune",
    "apotheosis:ignore_conditions_spawner_rune",
    "apotheosis:echoing_spawner_rune",
    "apotheosis:frontier_spawner_upgrade_rune",
    "apotheosis:ascent_spawner_upgrade_rune",
    "apotheosis:summit_spawner_upgrade_rune",
    "apotheosis:pinnacle_spawner_upgrade_rune",
    "apothic_spawners:capturing",
    "apothic_enchanting:occult_ender_lead",
    "reliquary:mob_charm_fragment",
    "reliquary:mob_charm_belt",
    "mob_grinding_utils:mob_swab",
    "mob_grinding_utils:gm_chicken_feed",
    "mob_grinding_utils:entity_spawner",
    "mob_grinding_utils:xpsolidifier",
    "mob_grinding_utils:solid_xp_mould_baby",
    "evilcraft:spirit_reanimator",
    "enderio:powered_spawner",
    "draconicevolution:stabilized_spawner",
    "pneumaticcraft:pressurized_spawner",
    "pneumaticcraft:spawner_agitator",
    "mysticalagriculture:soulium_spawner",
    "industrialforegoing:mob_duplicator",
    "ars_additions:source_spawner",
    "ftbfiltersystem:smart_filter",
)

# The Hostile Neural Networks chapter (50 quests): 7 titled quests, 37 untitled
# per-mob prediction quests, 5 untitled dimension-prediction quests + 1 hidden
# checkmark quest. Titles in the config's order.
HNN_QUEST_COUNT = 50
HNN_TITLED_QUEST_COUNT = 7
HNN_UNTITLED_PREDICTION_COUNT = 37
HNN_TITLED = (
    "Welcome to Hostile Neural Networks!",
    "Learning Mobs",
    "Modeling Mobs",
    "Simulating Deaths",
    "Leveling Up Data Models",
    "Creating Loot",
    "The Data Center",
)
HNN_ITEM_IDS = (
    "hostilenetworks:deep_learner",
    "hostilenetworks:blank_data_model",
    "hostilenetworks:sim_chamber",
    "hostilenetworks:prediction_matrix",
    "hostilenetworks:data_model",
    "hostilenetworks:loot_fabricator",
    "hostilenetworks:data_center",
    "hostilenetworks:data_center_io_port",
    "hostilenetworks:overworld_prediction",
    "hostilenetworks:nether_prediction",
    "hostilenetworks:end_prediction",
    "hostilenetworks:twilight_prediction",
    "kubejs:starlight_prediction",
)

# Cross-chapter verified quest titles the page quotes.
OTHER_CHAPTER_TITLES = (
    "Mob Farms using Blood",  # evilcraft
    "Revenge of the Spirits",  # evilcraft
    "Capturing Spirits",  # evilcraft
    "Creating Spawn Eggs",  # evilcraft
    "Garmonbozia",  # evilcraft
    "Creating Mob Seeds",  # Mystical Agriculture
    "Cognizant Dust",  # Mystical Agriculture
    "Infusing Spawner Runes",  # Apothic Enchanting (quest 4EE6824A970EEB35)
    "Occult Ender Lead",  # Apothic Enchanting
    "Altar of Birthing",  # Nature's Aura
    "Routers for Mob Farms",  # Modular Routers
    "Grid Networks",  # Refined Storage
    "Simple Magnets",  # Tips and Tricks
    "Kill The Warden",  # Chapter 1
    "Kill The Wither",  # Chapter 1
    "Overworld Bounty: Zombies",  # Bounty Board (formatting codes stripped)
    "The Nether Bounty: Blazes",  # Bounty Board (formatting codes stripped)
)

# Item ids outside the Apothic Spawners chapter that the page prints.
OTHER_ITEM_IDS = (
    "evilcraft:spirit_furnace",
    "evilcraft:dark_blood_brick",
    "evilcraft:vengeance_focus",
    "evilcraft:box_of_eternal_closure",
    "industrialforegoing:mob_crusher",
    "industrialforegoing:mob_slaughter_factory",
    "mysticalagriculture:soul_extractor",
    "modularrouters:vacuum_module",
    "modularrouters:void_module",
    "modularrouters:sender_module_1",
    "naturesaura:animal_spawner",
    "minecraft:warden",
    "minecraft:wither",
    "minecraft:wither_skeleton_skull",
    "minecraft:soul_sand",
)

# Numbers the page quotes from quest text / task counts, each verified against
# the pinned config.
VERIFIED_NUMBERS = (
    "36 quests",  # Apothic Spawners chapter
    "50 quests",  # Bounty Board chapter
    "87 kill tasks",  # Bounty Board chapter
    "5 / 10 / 50 / 100",  # the four kill-task tiers
    "48-57",  # Spawner Chains per *Blowing up Spawners* quest text
    "33 Dark Blood Bricks",  # *Mob Farms using Blood* task count
    "3x4x3",  # minimum spirit-furnace structure per quest text
    "70 Eterna",  # infused runes, per quest text
    "VII (7)",  # Capturing's highest level per quest text
    "0.5%",  # Capturing's per-level egg chance per quest text
    "7x7x7",  # Data Center multiblock per quest text
    "25 Self Aware Data Models",  # Data Center capacity per quest text
    "Faulty",  # first Data Model tier per quest text
    "150",  # Frontiersman's min spawn delay
    "600",  # Frontiersman's max spawn delay
    "100 / 400",  # Wayfarer's delays
    "50 / 200",  # Mountaineer's delays
    "20 / 20",  # Thundering delays
)

# Spawner Upgrade Rune names, exactly as each quest's description text names
# them (the quests themselves are untitled; the page must keep these hedges).
UPGRADE_RUNE_NAMES = (
    "Frontiersman's Spawner Upgrade Rune",
    "Wayfarer's Spawner Upgrade Rune",
    "Mountaineer's Spawner Upgrade Rune",
    "Thundering Spawner Upgrade Rune",
)

# Things the config does NOT contain; the page must say so rather than fill the
# gap from memory, and must never print an id for them.
ABSENT_FROM_CONFIG = (
    "soul shard",  # no Soul Shard item or quest in 8.2
    "dark room",  # no dark-room quest
)
FORBIDDEN_ID_FRAGMENTS = (
    "soul_shard",
    "soulshard",
    "cursed_earth",
    "mob_grinding_utils:fan",
)

# Sibling docs the page must cross-reference.
SIBLING_DOCS = (
    "progression.md",
    "key-mods.md",
    "boss-checklist.md",
    "atm-star-checklist.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


class TestMobFarmReferenceDoc(unittest.TestCase):
    """references/mob-farm-progression.md is grounded, complete, and wired up."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = read(DOC_PATH)
        cls.doc_lower = cls.doc.lower()
        cls.skill = read(SKILL_MD)
        cls.skill_lower = cls.skill.lower()

    # -- existence and grounding ------------------------------------------

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), f"missing {DOC_PATH}")
        self.assertGreater(len(self.doc.strip()), 8000, "the doc looks like a stub")

    def test_doc_names_its_provenance(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.doc_lower,
                          f"the doc must name its source: {source}")
        self.assertIn(PACK_COMMIT, self.doc, "the doc must pin the pack commit")
        self.assertIn(PACK_VERSION, self.doc, "the doc must date itself to pack 8.2")
        self.assertIn(PACK_STAMP, self.doc, "the doc must tie 8.2 to the skill's 8.x stamp")
        self.assertIn(PACK_DATE, self.doc, "the doc must carry the snapshot date")

    def test_doc_carries_the_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.doc_lower,
                          f"the doc must state the {needle!r} rule")
        self.assertRegex(self.doc_lower, r"nothing here was invented|never invent",
                         "the doc must say its details were read, not invented")

    def test_doc_marks_the_dark_room_as_general_knowledge(self) -> None:
        """The beginner default is vanilla mechanics -- no quest tracks it."""
        self.assertIn("general knowledge", self.doc_lower)
        self.assertIn("no quest", self.doc_lower)

    # -- verified quest titles ---------------------------------------------

    def test_doc_quotes_the_apothic_spawners_chapter(self) -> None:
        self.assertIn("Apothic Spawners", self.doc)
        self.assertIn("And Other Spawners", self.doc, "the chapter subtitle is verified")
        for title in APOTHIC_SPAWNERS_TITLED:
            self.assertIn(title, self.doc,
                          f"missing verified Apothic Spawners quest title: {title}")

    def test_doc_labels_subtitle_only_quests_as_subtitles(self) -> None:
        """The 'Other Spawners' quests have verified subtitles, not titles."""
        self.assertIn("subtitle", self.doc_lower)
        for subtitle in APOTHIC_SPAWNERS_SUBTITLED:
            self.assertIn(subtitle, self.doc,
                          f"missing verified subtitle/task title: {subtitle}")

    def test_doc_quotes_the_hnn_simulation_line(self) -> None:
        for title in HNN_TITLED:
            self.assertIn(title, self.doc, f"missing verified HNN quest title: {title}")

    def test_doc_quotes_the_cross_chapter_quests(self) -> None:
        for title in OTHER_CHAPTER_TITLES:
            self.assertIn(title, self.doc, f"missing verified quest title: {title}")

    def test_doc_names_the_chapters_it_reads(self) -> None:
        for chapter_id, (title, _group, _stage) in CHAPTERS_IN_DOC.items():
            self.assertIn(chapter_id, self.doc, f"missing chapter id: {chapter_id}")
            self.assertIn(title, self.doc, f"missing chapter title: {title}")

    # -- verified item ids --------------------------------------------------

    def test_doc_quotes_apothic_spawners_item_ids(self) -> None:
        for item_id in APOTHIC_SPAWNERS_ITEM_IDS:
            self.assertIn(item_id, self.doc, f"missing verified item id: {item_id}")

    def test_doc_quotes_hnn_item_ids(self) -> None:
        for item_id in HNN_ITEM_IDS:
            self.assertIn(item_id, self.doc, f"missing verified item id: {item_id}")

    def test_doc_quotes_other_item_ids(self) -> None:
        for item_id in OTHER_ITEM_IDS:
            self.assertIn(item_id, self.doc, f"missing verified item id: {item_id}")

    def test_doc_names_the_infusing_quest_id(self) -> None:
        # The one quest id the page cites (Apothic Enchanting's Infusing Spawner
        # Runes), transcribed from the lang file key.
        self.assertIn("4EE6824A970EEB35", self.doc)

    # -- verified numbers ---------------------------------------------------

    def test_doc_quotes_only_verified_numbers(self) -> None:
        for number in VERIFIED_NUMBERS:
            self.assertIn(number, self.doc, f"missing verified number: {number}")

    def test_doc_names_all_four_upgrade_runes_as_quest_text(self) -> None:
        for name in UPGRADE_RUNE_NAMES:
            self.assertIn(name, self.doc, f"missing rune name from quest text: {name}")
        self.assertIn("quest text", self.doc_lower,
                      "rune names must stay attributed to the quest text")

    def test_doc_marks_untitled_quests_in_place(self) -> None:
        """Untitled config quests must be marked untitled, never given a name."""
        self.assertIn("untitled", self.doc_lower)
        flat = re.sub(r"\s+", " ", self.doc)
        self.assertIn("Thirty-seven more\nuntitled quests", self.doc,
                      "the 37 per-mob prediction quests must be counted, not named")
        self.assertIn("37", flat)
        self.assertIn("no title in the config", flat,
                      "untitled quests must be marked in place")

    def test_doc_hedges_the_ladder_as_judgement(self) -> None:
        self.assertIn("judgement", self.doc_lower)
        self.assertIn("quests are optional", self.doc_lower,
                      "the Welcome chapter's own rule should anchor the hedge")

    # -- no invented names ---------------------------------------------------

    def test_doc_rejects_what_the_config_lacks(self) -> None:
        for topic in ABSENT_FROM_CONFIG:
            self.assertIn(topic, self.doc_lower,
                          f"the doc must address {topic!r} explicitly")
            self.assertRegex(
                self.doc_lower.replace("\n", " "),
                r"no [^.]*" + re.escape(topic) + r"[^.]*quest|not part of this pack",
                f"the doc must say the config has no {topic!r} content",
            )

    def test_doc_never_prints_an_id_for_config_absent_items(self) -> None:
        for fragment in FORBIDDEN_ID_FRAGMENTS:
            self.assertNotIn(fragment, self.doc_lower,
                             f"the doc must not print an id for absent content: {fragment}")

    def test_doc_flags_its_hnn_example_as_quest_flavor(self) -> None:
        # "Zombies for Iron" is the Loot Fabricator quest's own example text,
        # not a verified drop table; the page must attribute it as such.
        self.assertIn("Zombies for Iron", self.doc)
        self.assertRegex(self.doc, r"quest text, not a verified drop table")

    def test_doc_points_specifics_at_jei(self) -> None:
        self.assertIn("JEI", self.doc)
        self.assertIn("What this page deliberately does not tell you", self.doc)

    # -- wiring ---------------------------------------------------------------

    def test_doc_cross_references_its_siblings(self) -> None:
        for sibling in SIBLING_DOCS:
            self.assertIn(sibling, self.doc, f"the doc must link {sibling}")

    def test_skill_md_wires_the_doc(self) -> None:
        self.assertIn("mob-farm-progression.md", self.skill,
                      "SKILL.md must route mob-farm questions to the new doc")

    def test_skill_md_version_was_bumped(self) -> None:
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", self.skill, re.M)
        self.assertIsNotNone(match, "SKILL.md frontmatter must carry a semver version")
        version = tuple(int(part) for part in match.groups())
        self.assertGreaterEqual(version, (1, 2, 0),
                                "adding the doc is a feature: bump to at least 1.2.0")

    def test_doc_matches_the_shipped_chapter_list(self) -> None:
        """The doc's chapter ids/titles/stages mirror examples/progress.example.json."""
        data = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        by_id = {chapter["id"]: chapter for chapter in data["chapters"]}
        for chapter_id, (title, group, stage) in CHAPTERS_IN_DOC.items():
            self.assertIn(chapter_id, by_id, f"example file lacks chapter {chapter_id}")
            chapter = by_id[chapter_id]
            self.assertEqual(chapter["title"], title,
                             f"{chapter_id}: title drifted from the shipped list")
            self.assertEqual(chapter["group"], group,
                             f"{chapter_id}: group drifted from the shipped list")
            self.assertEqual(chapter["stage"], stage,
                             f"{chapter_id}: stage drifted from the shipped list")


class TestOfflineGuarantee(unittest.TestCase):
    """The new coverage stays stdlib-only and network-free."""

    def test_this_suite_imports_no_network_module(self) -> None:
        source = read(Path(__file__))
        for module in ("socket", "urllib", "http.client", "requests", "ftplib",
                       "smtplib", "subprocess", "asyncio"):
            self.assertNotRegex(source, rf"^\s*import {re.escape(module)}\b",
                                f"this suite must not import {module}")
            self.assertNotRegex(source, rf"^\s*from {re.escape(module)}\b",
                                f"this suite must not import {module}")


if __name__ == "__main__":
    unittest.main()
