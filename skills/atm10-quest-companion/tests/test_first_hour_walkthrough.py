#!/usr/bin/env python3
"""Offline tests for references/first-hour-walkthrough.md (the first-hour route).

Stdlib-only and network-free: the suite reads the shipped markdown files and checks
them against a verified snapshot of the pack's quest config - every case here is a
fixed string, a regex over local text, or a pure function call. Nothing is fetched,
and no pack checkout is required at test time.

Covered:

  * provenance: the doc pins the pack repository, the exact commit (e5e3d1d83e),
    the pack 8.2 / 2026-09-22 stamp, and names the quest-config files it was read
    from;
  * grounding: the doc carries the skill's rules - in-game quest book and JEI
    authoritative, never invent, no recipes, no coordinates, hedges kept as
    approximate/judgement, formatting codes stripped, untitled quests marked
    rather than renamed;
  * the verified snapshot: every quest id the doc cites, its title, and its
    chapter (mirrored from the pack 8.2 config), plus every config title, task
    title, subtitle, item id, and filter tag the doc presents - each must appear
    in the doc;
  * the opening chain: Welcome -> Putting the Craft in Minecraft -> Our First
    Pick -> Stone Age -> The Metal Age -> An Iron Pick, in dependency order, and
    the Welcome chapter's five player-visible quests with their 10 XP payouts;
  * the first-hour route table: anchored on the verified chain ids, in order, and
    explicitly marked judgement;
  * no-invented-names: every 16-hex quest/chapter id and every namespace:item
    token in the doc must be in the snapshot; every bold run must be a verified
    title or an allow-listed phrase; no coordinates, y-levels, or placeholder
    markers;
  * SKILL.md wiring: version 1.6.0, the doc linked from When to Use / Research

    Grounding / Behaviors / Completion Checklist, the beginner question named;
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
DOC_PATH = SKILL_ROOT / "references" / "first-hour-walkthrough.md"

# The pack snapshot the doc was read from: AllTheMods/ATM-10 main, pack 8.2.
PACK_REPO = "AllTheMods/ATM-10"
PACK_COMMIT = "e5e3d1d83e"
PACK_DATE = "2026-09-22"
PACK_VERSION = "8.2"
SKILL_VERSION = "1.6.0"


# (quest id, verified title, chapter config filename) - every titled quest whose id
# the doc cites, read from config/ftbquests/quests/{chapters,lang/en_us/chapters} at
# that commit. Titles are the config's with Minecraft '&' formatting codes stripped.
VERIFIED_QUESTS = (
    ("698A959C9E449592", "An Iron Pick", "mainquestline_part_1"),
    ("3ADCAD65EA6900BA", "Archaeology!", "mainquestline_part_1"),
    ("4E5238F00CEED8B2", "Basic Ore Doubling", "mainquestline_part_1"),
    ("378BF828DC931F0C", "Crafting, but on a Stick", "mainquestline_part_1"),
    ("0790D3BB481162A6", "Crafting... on a Stick!", "tips_and_tricks"),
    ("7EC01E7DB045DB05", "Furnace Augments", "mainquestline_part_1"),
    ("2AEBE3F28996A6ED", "Furnace Upgrades!", "mainquestline_part_1"),
    ("790EC3EDC2DB1FB0", "Generators Galore", "mainquestline_part_1"),
    ("72E1C19156633391", "Lava Bucket", "mainquestline_part_1"),
    ("346860B8EBC4C28C", "Lava Power", "mainquestline_part_1"),
    ("7975C7145572C438", "Our First Pick", "mainquestline_part_1"),
    ("282CE3A088AE5CFB", "Putting the Craft in Minecraft", "mainquestline_part_1"),
    ("4DE1158931F84F22", "Redstone", "mainquestline_part_1"),
    ("3B6F1BD64C0C570F", "Solar Power", "mainquestline_part_1"),
    ("7D38BC3DB3406F51", "Stone Age", "mainquestline_part_1"),
    ("051E0C85E7B71CE0", "The Metal Age", "mainquestline_part_1"),
    ("76406EFFF8CBA6B4", "We've Struck Diamonds!", "mainquestline_part_1"),
    ("3BC0A50886A3222B", "Welcome to All The Mods 10!", "welcome"),
    ("5CF320E9C4C1B1E1", "Welcome to Getting Started!", "mainquestline_part_1"),
    ("2CCAA7C0FEDEB573", "Wind Power", "mainquestline_part_1"),
)

# Cited quests that carry NO quest title in the config - the book shows them by their
# task title. The doc must mark these, never rename them.
UNTITLED_QUESTS = (
    ("0C93D7A607AB8B83", "welcome"),
    ("24C9BA6DC32CFAD9", "mainquestline_part_1"),
    ("3708A4780ACEB34E", "welcome"),
    ("4869C413646CC4CC", "mainquestline_part_1"),
    ("49EDAA2F57D3BF1D", "welcome"),
    ("5792CC9E3AFAB229", "mainquestline_part_1"),
    ("5AC1BE754210429E", "welcome"),
    ("672134A1A620EEAB", "mainquestline_part_1"),
    ("7658C1C663394E85", "welcome"),
)

# Chapter and group ids the doc names (same source; not quest ids).
VERIFIED_CHAPTER_IDS = (
    "1BE666F01EFFC00D",  # Tips and Tricks
    "2084F3F6FB861C5B",  # Main Questline group
    "5B00676D79306EA2",  # Welcome
    "732824E03978A934",  # Chapter 1: The Beginning
)

# Every other verified config name the doc presents (task titles, the two random
# reward tables, the chapter and group titles).
VERIFIED_NAMES = (
    "AllRightsReserved",
    "Archaeology!",
    "Chapter 1: The Beginning",
    "Claiming Chunks",
    "Coal",
    "Creating a Team",
    "Generators Galore",
    "Main Questline",
    "Power Cables",
    "Power Storage",
    "Quests",
    "Reward: Common",
    "Reward: Uncommon",
    "Smelt your logs",
    "Tips and Tricks",
    "Useful Commands",
    "Welcome",
)

# Subtitle claims the doc makes (config quest_subtitle values; the quotes are kept
# where the subtitle itself carries them, as in the doc).
VERIFIED_SUBTITLES = ('"Smelt your logs"',)

# Task item / reward item / dimension ids the doc cites. Every one is a real id in
# the pack 8.2 config at the pinned commit - a task entry, a reward entry, a chapter
# icon, or a filter component.
VERIFIED_ITEM_IDS = (
    "alltheores:copper_dust",
    "alltheores:iron_dust",
    "crafting_on_a_stick:crafting_table",
    "ftbquests:book",
    "generatorgalore:copper_generator",
    "generatorgalore:enchantment_generator",
    "generatorgalore:halitosis_generator",
    "generatorgalore:magmatic_generator",
    "generatorgalore:netherstar_generator",
    "generatorgalore:potion_generator",
    "ironfurnaces:augment_blasting",
    "ironfurnaces:augment_factory",
    "ironfurnaces:augment_fuel",
    "ironfurnaces:augment_generator",
    "ironfurnaces:augment_smoking",
    "ironfurnaces:augment_speed",
    "ironfurnaces:copper_furnace",
    "ironfurnaces:iron_furnace",
    "ironfurnaces:upgrade_copper",
    "ironfurnaces:upgrade_iron",
    "mekanism:basic_energy_cube",
    "mekanism:basic_fluid_tank",
    "mekanism:basic_universal_cable",
    "mekanism:ultimate_universal_cable",
    "mekanismgenerators:solar_generator",
    "mekanismgenerators:wind_generator",
    "minecraft:brush",
    "minecraft:bucket",
    "minecraft:coal_block",
    "minecraft:cooked_beef",
    "minecraft:copper_ingot",
    "minecraft:crafting_table",
    "minecraft:crying_obsidian",
    "minecraft:diamond",
    "minecraft:furnace",
    "minecraft:iron_ingot",
    "minecraft:iron_pickaxe",
    "minecraft:lava_bucket",
    "minecraft:oak_log",
    "minecraft:obsidian",
    "minecraft:overworld",
    "minecraft:redstone",
    "minecraft:redstone_block",
    "minecraft:torch",
    "minecraft:wooden_pickaxe",
    "pipez:energy_pipe",
    "powah:energy_cable_basic",
    "powah:energy_cell_starter",
    "powah:magmator_basic",
    "powah:magmator_starter",
    "powah:solar_panel_basic",
)

# Tag ids that appear inside the config's own smart-filter task definitions.
VERIFIED_FILTER_TAGS = (
    "alltheores:ore_hammers",
    "c:cobblestones",
    "minecraft:coals",
    "minecraft:logs",
)

# Ids the doc quotes from config/ftbultimine-server.snbt (merge_tags) - config values,
# not quest tasks.
VERIFIED_ULTIMINE_TOKENS = (
    "integrateddynamics:menril_logs",
    "minecraft:base_stone_overworld",
)

# Config keys/values the doc quotes verbatim from config/ftbquests/quests/data.snbt.
VERIFIED_DATA_KEYS = (
    "default_autoclaim_rewards",
    "default_consume_items",
    "detection_delay",
    "emergency_items_cooldown",
)

# The opening chain, in dependency order (verified in the config).
OPENING_CHAIN = (
    "5CF320E9C4C1B1E1",  # Welcome to Getting Started!      (chapter root)
    "282CE3A088AE5CFB",  # Putting the Craft in Minecraft   (dep: root)
    "7975C7145572C438",  # Our First Pick                   (dep: above)
    "7D38BC3DB3406F51",  # Stone Age                        (dep: above)
    "051E0C85E7B71CE0",  # The Metal Age                    (dep: above)
    "698A959C9E449592",  # An Iron Pick                     (dep: above)
)

# The Welcome chapter's five player-visible quests, each paying 10 XP.
WELCOME_QUESTS = (
    "3BC0A50886A3222B",
    "3708A4780ACEB34E",
    "7658C1C663394E85",
    "0C93D7A607AB8B83",
    "5AC1BE754210429E",
)

# The route table's anchors, in the order the table walks them.
ROUTE_ANCHORS = (
    "3708A4780ACEB34E",
    "5CF320E9C4C1B1E1",
    "282CE3A088AE5CFB",
    "7975C7145572C438",
    "7D38BC3DB3406F51",
    "051E0C85E7B71CE0",
    "698A959C9E449592",
    "378BF828DC931F0C",
)

# Quest-text quotes (code-stripped) the doc must carry, attributed as quest text.
VERIFIED_QUOTES = (
    "ATM10 is a kitchensink pack that allows you to explore the world of modded "
    "Minecraft in your own way!",
    "In this modpack, quests are optional. Mods are not gated behind completing any "
    "quests!",
    "To claim chunks, open up your map using M, then click the Claimed Chunks icon in "
    "the top left.",
    "To claim a chunk, left click and drag to claim.",
    "To force load a chunk, shift-left click the chunk. If done properly, you'll see "
    "lines across the chunk.",
    "If you want to create a team for you and your friends, use the command /ftbteams "
    "party create (name of team) to create the team!",
    "Note: These commands have cooldowns and limits.",
    "ATM10 is a Kitchensink pack, meaning you are free to explore and play the modpack "
    "any way that you want!",
    "However, there is an endgame goal: Making the ATM Star!",
    "This questline serves as a guide for all players, whether you are brand new to "
    "Minecraft or you've played through previous ATM packs.",
    "Just like almost every modpack, gather some wood to get started!",
    "Pickaxes allow you to break most stone and metal blocks. This wooden one won't "
    "last long, so make sure to gather some Cobblestone with it!",
    "Cobblestone unlocks the next part of progression by allowing you to craft a "
    "Furnace to smelt our ores.",
    "You'll also want to upgrade your pickaxe to stone to mine better ores like Iron!",
    "Copper is abundant and has plenty of uses for things like Ore Hammers or Drawer "
    "Upgrades, so make sure to grab plenty of it!",
    "Iron is probably one of the most important ores you'll want to get every time you "
    "run into it. The world of modded MC pretty much runs on Iron.",
    "The next step of progression is to make an Iron Pickaxe.",
    "This pickaxe can mine some of the rarer ores in the game, including Diamond!",
    "Once you have an Iron or better tier Pickaxe, you'll be able to mine Redstone.",
    "Smelting down raw ores in the beginning is necessary, but you are missing out on "
    "extra resources!",
    "These will break down 1 raw ore into 2 ore dust, which can be smelted into ingots, "
    "effectively doubling your ingot output!",
    "Want more per raw ore? Check out the mod Occultism!",
    "Coal is your first real source of power. If you are running low and can't find any "
    "Coal, an alternative would be to use Charcoal.",
    "Buckets and Tanks are a great early way to move around lava.",
    "Personally, I hate having to run to a block just to craft. That's where the "
    "Crafting Table on a Stick comes in!",
    "This item works as a Portable Crafting Table!",
    "With our new metals, we can upgrade our Furnace using the mod Iron Furnaces!",
    "Now that you have all this lava what will you do with it? More early game power!",
    "If you are like most this is the power you are after. All you do is place it as "
    "high as you can and get free power.",
    "Just like wind generation this will give you lots of power without giving it any "
    "resources. The only downside here is it has to be daytime.",
    "As was mentioned before, this mod adds a ton of fun ways to generate power that "
    "require specific builds.",
    "Transferring power out of your generators is probably a good idea, but how can you "
    "do it?",
    "Note: You only have to make one of the items to complete the quest.",
    "a must have in the early game",
)

# Bold runs that are the doc's own prose (headings, rules, table labels, mod names)
# rather than quest/chapter titles - the only bold text allowed beyond the verified
# names, table-column labels, and the mod/id runs quoted from config text.
# Bold runs that are the doc's own prose (headings, rules, table labels, section
# titles) rather than quest/chapter names - the only bold text allowed beyond the
# verified names above. Generated from the doc and checked exactly.
PROSE_BOLD = (
    '10 XP',
    '8.2',
    'A keybind the config does not name.',
    'All the Mods 10',
    'An official first-hour order.',
    'Anything uncertain is flagged approximate.',
    'Controls',
    'Coordinates, y-levels, ore heights, biome lists, or where to walk.',
    'Counts beyond the quoted ones.',
    "Don't build a storage network.",
    "Don't chase the ATM Star.",
    "Don't grind Mystical Agriculture yet.",
    "Don't leave the quest book closed.",
    "Don't pick a tech line yet.",
    'FTB Ultimine is in the pack and configured generously.',
    'Item ids below are quoted from config task entries, never invented',
    'No recipes, no coordinates, no seed tricks, no layouts.',
    "One of them is the pack's only chunk-loading tutorial.",
    'Open the quest book first — before you build anything.',
    'Recipes.',
    'Stop at the iron pickaxe and look around.',
    'Take the cheap side quests as you pass them',
    'The first quest completes on its own.',
    'The in-game quest book (FTB Quests) and JEI are authoritative.',
    'The map is on',
    'The minute-by-minute split is judgement',
    'The other four are self-declared checkmarks.',
    "The pack's config does not name the keybind",
    "The route order is the config's; the timing is judgement.",
    'The untitled coal entry',
    'The wiring quests sit right behind them',
    'Then start Chapter 1: The Beginning',
    'This is the pack\'s own "what do I do first".',
    "Titles are the config's, never invented.",
    'Titles for quests that have none.',
    'What this page is.',
    'no quest title in the config',
    'not',
    'or',
    'pack 8.2',
    'without taking it',
)

# The skill files the doc cross-references.
CROSS_REFERENCES = (
    "references/automation-first-steps.md",
    "references/chunk-loading-guide.md",
    "references/getting-started.md",
    "references/key-mods.md",
    "references/ore-processing-ladder.md",
    "references/progression-roadmap.md",
)


def flatten(text: str) -> str:
    """Join wrapped lines so multi-line quotes and cells match as written."""
    return re.sub(r"\s*\n\s*", " ", text)


def strip_code_spans(text: str) -> str:
    """Blank out `inline code` so markup inside it cannot read as prose markup."""
    return re.sub(r"`[^`]*`", " ", text)


class DocTestCase(unittest.TestCase):
    """Shared setup: load the doc once, plain and line-flattened."""

    @classmethod
    def setUpClass(cls) -> None:
        assert DOC_PATH.is_file(), f"missing {DOC_PATH}"
        cls.doc = DOC_PATH.read_text(encoding="utf-8")
        cls.flat = flatten(cls.doc)
        cls.quest_ids = {row[0] for row in VERIFIED_QUESTS}
        cls.untitled_ids = {row[0] for row in UNTITLED_QUESTS}


# --------------------------------------------------------------------------------------
# provenance
# --------------------------------------------------------------------------------------

class TestProvenance(DocTestCase):

    def test_doc_exists_and_is_substantial(self) -> None:
        self.assertGreater(len(self.doc.strip()), 8000,
                           "first-hour-walkthrough.md looks like a stub")

    def test_pins_repository_commit_version_and_date(self) -> None:
        for needle in (PACK_REPO, PACK_COMMIT, PACK_DATE, f"pack {PACK_VERSION}",
                       "CHANGELOG.md", "8.x", "examples/progress.example.json"):
            self.assertIn(needle, self.flat,
                          f"the doc must pin its source: {needle!r}")

    def test_names_the_quest_config_files_it_was_read_from(self) -> None:
        for needle in ("config/ftbquests/quests/chapters/welcome.snbt",
                       "config/ftbquests/quests/chapters/mainquestline_part_1.snbt",
                       "lang/en_us/chapters",
                       "chapter_groups.snbt",
                       "data.snbt",
                       "config/bcc-common.toml",
                       "config/ftbultimine-server.snbt",
                       "config/crash_assistant/modlist.json",
                       "CHANGELOG.md"):
            self.assertIn(needle, self.flat, f"missing named source: {needle!r}")

    def test_says_titles_and_quotes_are_code_stripped(self) -> None:
        self.assertIn("formatting codes stripped", self.flat)


# --------------------------------------------------------------------------------------
# grounding rules
# --------------------------------------------------------------------------------------

class TestGroundingRules(DocTestCase):

    def test_book_and_jei_stay_authoritative(self) -> None:
        lowered = self.flat.lower()
        self.assertIn("in-game quest book", lowered)
        self.assertIn("jei", lowered)
        self.assertIn("authoritative", lowered)

    def test_never_invent_and_no_recipes(self) -> None:
        lowered = self.flat.lower()
        self.assertIn("never invented", lowered)
        self.assertIn("no recipes", lowered)
        self.assertIn("read, not remembered", lowered)

    def test_hedges_stay_marked(self) -> None:
        self.assertIn("timing is judgement", self.flat)
        self.assertIn("(judgement)", self.flat)
        self.assertIn("judgement —", self.flat)
        self.assertIn("verify in-game", self.flat)

    def test_untitled_quests_are_marked_not_named(self) -> None:
        self.assertIn("no title in the config", self.flat)

    def test_pinning_language(self) -> None:
        self.assertIn("This page is a snapshot of pack 8.2's config", self.flat)
        self.assertIn("If the player's book differs from anything here, his book wins",
                      self.flat)

    def test_says_the_pack_gates_nothing(self) -> None:
        self.assertIn("quests are optional. Mods are not gated behind completing any "
                      "quests!", self.flat)


# --------------------------------------------------------------------------------------
# verified snapshot: every mirrored name, id, subtitle, and item id is in the doc
# --------------------------------------------------------------------------------------

class TestVerifiedSnapshot(DocTestCase):

    def test_every_verified_quest_id_and_title_is_cited(self) -> None:
        for quest_id, title, _chapter in VERIFIED_QUESTS:
            self.assertIn(f"`{quest_id}`", self.doc,
                          f"missing quest id {quest_id} ({title})")
            self.assertIn(title, self.flat, f"missing verified title {title!r}")

    def test_every_untitled_quest_id_is_cited(self) -> None:
        for quest_id, _chapter in UNTITLED_QUESTS:
            self.assertIn(f"`{quest_id}`", self.doc,
                          f"missing untitled quest id {quest_id}")

    def test_chapter_and_group_ids_are_cited(self) -> None:
        for chapter_id in VERIFIED_CHAPTER_IDS:
            self.assertIn(f"`{chapter_id}`", self.doc,
                          f"missing chapter/group id {chapter_id}")

    def test_every_verified_name_is_present(self) -> None:
        for name in VERIFIED_NAMES:
            self.assertIn(name, self.flat, f"missing verified name {name!r}")

    def test_every_verified_subtitle_claim_is_present(self) -> None:
        for subtitle in VERIFIED_SUBTITLES:
            self.assertIn(subtitle, self.flat,
                          f"missing verified subtitle {subtitle!r}")

    def test_every_cited_item_id_is_present(self) -> None:
        for item_id in VERIFIED_ITEM_IDS + VERIFIED_FILTER_TAGS:
            self.assertIn(item_id, self.doc, f"missing item id {item_id}")

    def test_every_ultimine_config_token_is_present(self) -> None:
        for token in VERIFIED_ULTIMINE_TOKENS:
            self.assertIn(token, self.doc, f"missing ultimine token {token}")

    def test_the_two_reward_tables_are_named_not_numbered(self) -> None:
        # The doc names the tables by their verified titles and never prints the
        # numeric table ids (which would be a bare count with no title context).
        self.assertIn("**Reward: Common**", self.doc)
        self.assertIn("**Reward: Uncommon**", self.doc)
        self.assertNotIn("487623848494439020", self.doc)
        self.assertNotIn("4196188979167302596", self.doc)

    def test_quotes_the_pack_wide_quest_config_switches(self) -> None:
        for key in VERIFIED_DATA_KEYS:
            self.assertIn(key, self.doc, f"missing data.snbt key {key}")
        self.assertIn('"disabled"', self.flat)
        self.assertIn("false", self.flat)


# --------------------------------------------------------------------------------------
# the opening chain and the Welcome chapter
# --------------------------------------------------------------------------------------

class TestOpeningChain(DocTestCase):

    def test_chain_appears_in_dependency_order(self) -> None:
        positions = [self.doc.find(f"`{quest_id}`") for quest_id in OPENING_CHAIN]
        for quest_id, position in zip(OPENING_CHAIN, positions):
            self.assertGreaterEqual(position, 0,
                                    f"the chain must cite {quest_id}")
        self.assertEqual(positions, sorted(positions),
                         "the opening chain must be presented in dependency order")

    def test_chain_table_states_its_dependencies(self) -> None:
        # The first link is the chapter root; every other link names its predecessor.
        self.assertIn("(chapter root)", self.flat)
        chain_table = self.flat[
            self.flat.find("| # | Verified quest title |"):
            self.flat.find("**This is the pack's own")]
        for predecessor in ("#1", "#2", "#3", "#4", "#5"):
            self.assertIn(predecessor, chain_table,
                          f"chain table must name dependency {predecessor}")

    def test_welcome_chapter_quests_are_listed_with_their_payout(self) -> None:
        welcome_table = self.flat[
            self.flat.find("| Book entry (as the config titles it) |"):
            self.flat.find("Three things matter about that table")]
        for quest_id in WELCOME_QUESTS:
            self.assertIn(f"`{quest_id}`", welcome_table,
                          f"Welcome chapter quest {quest_id} must be in its table")
        self.assertIn("10 XP", welcome_table)

    def test_welcome_first_quest_completes_on_its_own(self) -> None:
        self.assertIn("dimension` task for `minecraft:overworld`", self.doc)
        self.assertIn("is satisfied by being in the Overworld", self.flat)

    def test_chain_root_pays_the_first_hour_resources(self) -> None:
        self.assertIn("4 × `minecraft:torch`, 4 × `minecraft:cooked_beef`", self.doc)


# --------------------------------------------------------------------------------------
# the first-hour route table
# --------------------------------------------------------------------------------------

class TestRouteTable(DocTestCase):

    def route_section(self) -> str:
        start = self.flat.find("## A route you can actually run in an hour")
        self.assertGreaterEqual(start, 0, "missing the first-hour route section")
        return self.flat[start:self.flat.find("## What is", start)]

    def test_route_section_is_marked_judgement(self) -> None:
        section = self.route_section()
        self.assertIn("judgement", section.lower())
        self.assertIn("dependencies below are verified in the config", section)

    def test_route_anchors_appear_in_order(self) -> None:
        section = self.route_section()
        positions = [section.find(f"`{quest_id}`") for quest_id in ROUTE_ANCHORS]
        for quest_id, position in zip(ROUTE_ANCHORS, positions):
            self.assertGreaterEqual(position, 0,
                                    f"route table must anchor on {quest_id}")
        self.assertEqual(positions, sorted(positions),
                         "route anchors must appear in the order the route walks them")

    def test_route_ends_before_the_generators(self) -> None:
        # Hour one stops at the iron pick; the generators are named as hour two.
        section = self.route_section()
        self.assertNotIn("`346860B8EBC4C28C`", section,
                         "Lava Power is hour two, not hour one")

    def test_answers_the_beginner_question(self) -> None:
        self.assertIn("what do I do first?", self.flat)
        self.assertIn("## The short answer", self.flat)
        self.assertIn("Open the quest book first", self.flat)


# --------------------------------------------------------------------------------------
# no-invented-names
# --------------------------------------------------------------------------------------

class TestNoInventedNames(DocTestCase):

    def test_no_quest_id_outside_the_snapshot(self) -> None:
        allowed = (self.quest_ids | self.untitled_ids | set(VERIFIED_CHAPTER_IDS))
        found = set(re.findall(r"\b[0-9A-F]{16}\b", self.doc))
        unknown = found - allowed
        self.assertEqual(unknown, set(),
                         f"ids not in the verified snapshot: {sorted(unknown)}")

    def test_no_item_id_outside_the_snapshot(self) -> None:
        # Anchor the match so a URL scheme (https://) and a glob (c:ores/*) cannot
        # read as an item id.
        pattern = (r"(?<![A-Za-z0-9_/:])"
                   r"([a-z][a-z0-9_]*:[a-z0-9_]+(?:/[a-z0-9_]+)*)"
                   r"(?![A-Za-z0-9_/:-])")
        found = set(re.findall(pattern, self.doc))
        allowed = (set(VERIFIED_ITEM_IDS) | set(VERIFIED_FILTER_TAGS)
                   | set(VERIFIED_ULTIMINE_TOKENS))
        unknown = found - allowed
        self.assertEqual(unknown, set(),
                         f"item-like tokens not in the verified snapshot: "
                         f"{sorted(unknown)}")

    def test_every_bold_run_is_a_verified_title_or_allowed_phrase(self) -> None:
        text = strip_code_spans(self.doc)
        runs = {re.sub(r"\s+", " ", run).strip()
                for run in re.findall(r"\*\*(.+?)\*\*", text, re.DOTALL)}
        titles = ({row[1] for row in VERIFIED_QUESTS} | set(VERIFIED_NAMES))
        allowed = titles | set(PROSE_BOLD)
        unknown = runs - allowed
        self.assertEqual(unknown, set(),
                         f"bold names not verified against the config: "
                         f"{sorted(unknown)}")

    def test_every_claimed_subtitle_is_a_config_subtitle(self) -> None:
        claims = re.findall(r"subtitles?:?\s+\*([^*]+)\*", self.flat)
        allowed = set(VERIFIED_SUBTITLES)
        for claim in claims:
            self.assertIn(claim, allowed,
                          f"claimed subtitle not in the verified snapshot: {claim!r}")

    def test_no_coordinates_y_levels_or_placeholders(self) -> None:
        self.assertNotRegex(self.doc, r"\b-?\d{1,5}\s+-?\d{1,5}\s+-?\d{1,5}\b",
                            "the doc must not carry coordinates")
        self.assertNotRegex(self.doc, r"\bY\s*-?\s*\d+",
                            "the doc must not carry y-levels")
        for marker in ("TODO", "TBD", "FIXME", "XXX"):
            self.assertNotIn(marker, self.doc, f"placeholder marker {marker} left in doc")

    def test_does_not_promise_a_recipe_or_a_keybind(self) -> None:
        lowered = self.flat.lower()
        self.assertIn("the pack's config does not name the keybind", lowered)
        self.assertIn("check the **controls** screen".lower(), lowered)


# --------------------------------------------------------------------------------------
# quotes: verified quest text is present and attributed
# --------------------------------------------------------------------------------------

class TestVerifiedQuotes(DocTestCase):

    def test_every_representative_quote_is_present(self) -> None:
        for quote in VERIFIED_QUOTES:
            self.assertIn(quote, self.flat, f"missing verified quote: {quote!r}")

    def test_quotes_are_presented_as_quest_text(self) -> None:
        self.assertIn("What its text says, quoted", self.flat)
        self.assertIn("What the rest of the chapter's text says, quoted", self.flat)
        self.assertIn("in the config's own words", self.flat)


# --------------------------------------------------------------------------------------
# SKILL.md wiring
# --------------------------------------------------------------------------------------

class TestSkillWiring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL_MD.read_text(encoding="utf-8")

    def test_version_bumped(self) -> None:
        match = re.search(r"^version:\s*(\S+)\s*$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md frontmatter has no version")
        assert match is not None
        self.assertEqual(match.group(1), SKILL_VERSION,
                         f"adding the first-hour doc bumps the skill to {SKILL_VERSION}")

    def test_doc_is_linked_from_the_skill(self) -> None:
        self.assertGreaterEqual(
            self.skill.count("references/first-hour-walkthrough.md"), 3,
            "SKILL.md must wire the doc from When to Use, Grounding, and Behaviors")

    def test_beginner_question_is_recognized(self) -> None:
        self.assertIn("what do i do first", self.skill.lower())

    def test_grounding_bullet_dates_the_doc(self) -> None:
        self.assertIn("first-hour doc dates itself", self.skill)
        self.assertIn(PACK_COMMIT, self.skill)
        self.assertIn("walkthrough", self.skill.lower())

    def test_completion_checklist_covers_first_hour_answers(self) -> None:
        lowered = self.skill.lower()
        self.assertIn("first-hour answers quoted verified quest titles", lowered)

    def test_existing_grounding_rules_survive_the_edit(self) -> None:
        lowered = self.skill.lower()
        for needle in ("in-game quest book", "jei", "authoritative",
                       "never invent", "approximate"):
            self.assertIn(needle, lowered, f"SKILL.md lost the {needle!r} rule")


# --------------------------------------------------------------------------------------
# cross-references and offline guarantee
# --------------------------------------------------------------------------------------

class TestCrossReferences(DocTestCase):

    def test_doc_points_at_its_sibling_references(self) -> None:
        for sibling in CROSS_REFERENCES:
            self.assertIn(sibling, self.flat,
                          f"first-hour-walkthrough.md must point at {sibling}")


class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def imported_modules(self, source: str) -> "set[str]":
        found: "set[str]" = set()
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        return found

    def test_this_suite_imports_no_network_module(self) -> None:
        imported = self.imported_modules(Path(__file__).read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(imported <= {"re", "unittest", "pathlib", "__future__"},
                        f"unexpected import(s): {sorted(imported)}")


if __name__ == "__main__":
    unittest.main()
