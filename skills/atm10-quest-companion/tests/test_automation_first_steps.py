#!/usr/bin/env python3
"""Offline tests for references/automation-first-steps.md (the automation guide).

Stdlib-only and network-free: the suite reads the shipped markdown files and checks
them against a verified snapshot of the pack's quest config - every case here is a
fixed string, a regex over local text, or a pure function call. Nothing is fetched,
and no pack checkout is required at test time.

Covered:

  * provenance: the doc pins the pack repository, the exact commit (e5e3d1d83e),
    the changelog's pack 8.2 / 2026-09-22 stamp, and names the quest-config files it
    was read from;
  * grounding: the doc carries the skill's rules - in-game quest book and JEI
    authoritative, never invent, no recipes, hedges kept as approximate/judgement,
    formatting codes stripped, untitled quests marked instead of named;
  * the verified snapshot: every quest id the doc cites, its title, and its chapter
    (mirrored from the pack 8.2 config), plus every other config title, subtitle,
    and task item id the doc presents - each must appear in the doc;
  * the anchors table: every (title, quest id) row must match the mirrored snapshot,
    so a row can never drift from the config it was read from;
  * no-invented-names: every 16-hex quest id and every namespace:item id in the doc
    must be in the snapshot; every bold run must be a verified title or an
    allow-listed phrase; every claimed subtitle must be a config subtitle; no
    coordinates, y-levels, or placeholder markers;
  * structure: the five automations in the advertised impact order (ore processing ->
    power -> item transport -> storage -> farms), the ranking explicitly marked as
    judgement, and the short answer wired to its verified anchors;
  * representative quest-text quotes verified against the config are present,
    attributed as quest text;
  * SKILL.md wiring: version 1.7.0, the doc linked from When to Use / Research

    Grounding / Behaviors / Completion Checklist, the beginner question named;
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
DOC_PATH = SKILL_ROOT / "references" / "automation-first-steps.md"

# The pack snapshot the doc was read from: AllTheMods/ATM-10 main, pack 8.2.
PACK_REPO = "AllTheMods/ATM-10"
PACK_COMMIT = "e5e3d1d83e"
PACK_DATE = "2026-09-22"
PACK_VERSION = "8.2"

# (quest id, verified title, chapter config filename) - every quest whose id the doc
# cites, read from config/ftbquests/quests/{chapters,lang/en_us/chapters} at that
# commit. Titles are the config's with Minecraft '&' formatting codes stripped.
VERIFIED_QUESTS = (
    ("051E0C85E7B71CE0", "The Metal Age", "mainquestline_part_1"),
    ("0682DC1F2417DAEB", "Functional Storage", "storage"),
    ("08DDE018A804BFE7", "Enrichment Chamber", "mekanism"),
    ("109AD73F016D576B", "Your First Beehive", "productive_bees"),
    ("119BED334E331C25", "Enrich then Smelt", "mekanism"),
    ("13AA91D39A2CABF2", "Productive Bees!", "productive_bees"),
    ("1F81EA5E45424308", "Transferring Power", "basic_power"),
    ("2329AA0AFBEF1E13", "Pipez", "basic_logistics"),
    ("2CCAA7C0FEDEB573", "Wind Power", "mainquestline_part_1"),
    ("2FC15D3916DBF4E4", "Advanced Void Upgrade", "storage"),
    ("33433A443B65D252", "Fluid Pipez", "basic_logistics"),
    ("346860B8EBC4C28C", "Lava Power", "mainquestline_part_1"),
    ("36836AD948F96B9F", "Item Pipez", "basic_logistics"),
    ("3A1D07AED2A841E4", "Auto-Smelting Upgrade", "storage"),
    ("3B6F1BD64C0C570F", "Solar Power", "mainquestline_part_1"),
    ("418E57E34FFC19E1", "Laser Drill", "industrial_foregoing"),
    ("42D173B9FF8D16E4", "Early Game Power Options", "basic_power"),
    ("43021923E220CF68", "The Planter", "food_and_farming"),
    ("488DBE69595F38F8", "Energized Smelter", "mekanism"),
    ("4AB0DD227471FDBF", "Basic Power", "basic_power"),
    ("4E5238F00CEED8B2", "Basic Ore Doubling", "mainquestline_part_1"),
    ("4FBAB3A0FBF8CE2F", "Universal Pipez", "basic_logistics"),
    ("53EC96FA0E7C4ED4", "Energy Pipez", "basic_logistics"),
    ("54735C5FCD2077B3", "Mystical Agriculture!", "elmystical_agriculturerr"),
    ("5A94A2664BFDD7B9", "Basic Storage", "storage"),
    ("5E4BC0F59C90433A", "Sophisticated Storage", "storage"),
    ("5F1218CF8EFC607B", "Laser IO", "basic_logistics"),
    ("6C001E18093FC037", "Plants", "industrial_foregoing"),
    ("6CD7D99AA102A5C3", "Logistics", "basic_logistics"),
    ("6E05B62A40D5A891", "Integrated Dynamics", "basic_logistics"),
    ("72E1C19156633391", "Lava Bucket", "mainquestline_part_1"),
    ("76EA017B12E8F01B", "Storing Power", "basic_power"),
    ("790EC3EDC2DB1FB0", "Generators Galore", "mainquestline_part_1"),
    ("7AE502EDB73BD57A", "Crusher", "mekanism"),
    ("7E9E03274A88347D", "Stack Upgrade Tier 1", "storage"),
)

# Every other verified config title the doc presents by name (quest titles not cited
# by id, plus the chapter titles). Same source and rules as above.
VERIFIED_NAMES = (
    "Advanced Machine Frame",
    "Applied Energistics 2",
    "Auto-Smelting Upgrade",
    "Basic Logistics",
    "Basic Ore Doubling",
    "Basic Power",
    "Basic Storage",
    "Chapter 1: The Beginning",
    "Chemical Crystallizer",
    "Chemical Dissolution Chamber",
    "Chemical Injection Chamber",
    "Creating Loot",
    "Creating Sulfuric Acid",
    "Crush and Enrich our Clumps",
    "Crystal, Shard, Clump, ETC",
    "Early Game Power Options",
    "Enrich then Smelt",
    "Enrichment Chamber",
    "Extended & Advanced AE",
    "Fluids",
    "Food and Farming",
    "Fully Automated ATM Star",
    "Hostile Neural Networks",
    "Industrial Foregoing",
    "Inferium",
    "Inferium Growth Accelerator",
    "Infusion Altar",
    "Injecting Hydrogen Chloride",
    "Item Importing",
    "Item Pipez",
    "Laser Drill",
    "Lava Bucket",
    "Lava Power",
    "Learning Mobs",
    "Logistical Transporters",
    "Making Oxygen for Purifier",
    "Mechanical Pipes",
    "Mekanism",
    "Mekanism Logistics",
    "Mekanism: Reactors",
    "Melting Ores with Acid and Crystallizing them",
    "Modeling Mobs",
    "Mystical Agriculture",
    "Mystical Agriculture!",
    "Pipez",
    "Power",
    "Productive Bees",
    "Productive Bees!",
    "Prosperity Seed Base",
    "Prosperity Shards",
    "Purification Chamber",
    "Refined Storage",
    "Searching for Nests",
    "Shard, to Clump, to Dust, to Ingot",
    "Simple Machine Frame",
    "Simulating Deaths",
    "Solar Power",
    "Sophisticated Storage",
    "Storage",
    "The Data Center",
    "The Metal Age",
    "Welcome to Hostile Neural Networks!",
    "Wind Power",
)

# Subtitles the doc claims (config quest_subtitle values; quotes kept where the
# subtitle itself carries them).
VERIFIED_SUBTITLES = (
    '"Vanilla Chest"',
    "All The Power!",
    "Automatic",
    "Breaks Raw Ores into Dusts",
    "Creating Seeds",
    "Fluids",
    "It Crushes Things.",
    "Items",
    "Mekanism's Powered Furnace",
    "More Filtering Options",
    "Ore Processing: Step 1",
    "Ore Processing: Step 2",
    "Ore Processing: Step 3",
    "Range: 9 Blocks",
    "Starter Power",
    "Storage Drawers Distant Relative",
    "The Configurator",
    "The Learning HUD",
    "Tier 1 Ore Processing",
    "Tier 2 Ore Processing",
    "Tier 3 Ore Processing",
    "Tier 4 Ore Processing",
    "Tier: 1",
    "Void Miner",
    '"Wait until you get Machines for this..."',
)

# Every namespace:item id the doc cites - each is a real task item in the config.
VERIFIED_ITEM_IDS = (
    "hostilenetworks:blank_data_model",
    "hostilenetworks:deep_learner",
    "hostilenetworks:loot_fabricator",
    "hostilenetworks:prediction_matrix",
    "hostilenetworks:sim_chamber",
    "industrialforegoing:fluid_laser_base",
    "industrialforegoing:laser_drill",
    "industrialforegoing:ore_laser_base",
    "industrialforegoing:plant_gatherer",
    "industrialforegoing:plant_sower",
    "integrateddynamics:wrench",
    "laserio:logic_chip",
    "mekanism:configurator",
    "mekanism:crusher",
    "mekanism:energized_smelter",
    "mekanism:enrichment_chamber",
    "mekanismgenerators:wind_generator",
    "minecraft:copper_ingot",
    "minecraft:iron_ingot",
    "mysticalagriculture:inferium_growth_accelerator",
    "mysticalagriculture:infusion_altar",
    "mysticalagriculture:infusion_pedestal",
    "pipez:energy_pipe",
    "pipez:fluid_pipe",
    "pipez:item_pipe",
    "pipez:universal_pipe",
    "pipez:wrench",
    "productivebees:nest_locator",
    "sophisticatedbackpacks:auto_smelting_upgrade",
)

# Bold runs that are the doc's own prose (headings, rules, labels) rather than
# quest/chapter names - the only bold text allowed beyond the verified titles.
PROSE_BOLD = (
    "1",
    "2",
    "3",
    "4",
    "5",
    "8.2",
    "A digital storage network",
    "All the Mods 10",
    "Alternatives in the same chapter (pick one, the pack gates nothing):",
    "An official order.",
    "Anything not in the config.",
    "Anything uncertain is flagged approximate",
    "Applied Energistics 2 vs Refined Storage",
    "Automating the ATM Star itself",
    "Counts and numbers beyond quotes.",
    "Farms & renewable resources",
    "Food first if you haven't.",
    "If you only do one thing: automate ore processing first.",
    "Item ids below are quoted from config task entries, never invented",
    "Item transport",
    "Loot and resource scale-out",
    "Machine tiers, energy amounts, throughput, layouts, coordinates.",
    "No recipes, no counts, no layouts.",
    "Ore processing",
    "Other routes in the book (alternatives, not a sequence).",
    "Recipes.",
    "The Mekanism way",
    "The in-game quest book (FTB Quests) and JEI are authoritative.",
    "The ladder beyond Tier 1.",
    "The mid-game goal to keep in view:",
    "The ranking is judgement, not the pack's.",
    "The rest of the Mekanism ladder",
    "The verified trail.",
    "Then materials — three verified routes (alternatives, not a ladder):",
    "Titles are the config's, never invented.",
    "What this page is.",
    "Why this rank (judgement).",
    "bold",
    "ordered by impact for a beginner",
    "pack 8.2",
)

# Quest-text quotes (code-stripped) the doc must carry, attributed as quest text.
# Each was read from the lang files at the pinned commit; the doc quotes them.
VERIFIED_QUOTES = (
    "Smelting down raw ores in the beginning is necessary, but you are missing out on "
    "extra resources!",
    "These will break down 1 raw ore into 2 ore dust, which can be smelted into ingots, "
    "effectively doubling your ingot output!",
    "Want more per raw ore? Check out the mod Occultism!",
    "Congrats, you just Ore Processed!",
    "We can get 2 Dust from 1 Ore.",
    "Now that you have all this lava what will you do with it? More early game power!",
    "If you are like most this is the power you are after. All you do is place it as "
    "high as you can and get free power.",
    "This chapter is dedicated to all things power related!",
    "Pipez is the simplest Logistics Mod.",
    "That's what Logistics is for.",
    "Logistical Transporters will move Items and Blocks from one Inventory to another!",
    "Auto-smelt items in the Backpack.",
    "Sophisticated Storage allows you to upgrade your Chests and Barrels with metals to "
    "increase their storage!",
    "Mystical Agriculture is a resource generation mod that allows you to grow a large "
    "variety of vanilla and modded resources using Seeds.",
    "The Simulation Chamber is the main machine within HNN.",
    "The machine will remember your choice, so it can be automated.",
    "When supplied with Ether Gas, the Plant Gatherer will automatically replant crops.",
    "To get started with the mod, you'll first need to find some Honeycombs and Honey "
    "Bottles!",
    "Make sure to look them up in JEI if you need them!",
    "Wait until you get Machines for this...",
)

# The five ranked sections, in the advertised impact order (heading prefixes).
SECTION_HEADINGS = (
    "## 1. Ore processing",
    "## 2. Power",
    "## 3. Item transport",
    "## 4. Storage",
    "## 5. Farms & renewable resources",
)

# The summary table's rank rows, in order.
SUMMARY_ROWS = (
    "| **1** | **Ore processing**",
    "| **2** | **Power**",
    "| **3** | **Item transport**",
    "| **4** | **Storage**",
    "| **5** | **Farms & renewable resources**",
)

# Verified chapter quest counts the doc quotes (pack 8.2), with the context strings
# used to pin each one to its chapter.
CHAPTER_COUNT_STRINGS = (
    "(Main Questline, 36 quests)",
    "*Mekanism* (90 quests)",
    "(34 quests)",
    "(Logistics group, 40 quests)",
    "(Storage group, 90 quests)",
    "(Resources, 191 quests)",
    "(Resources, 50 quests)",
    "(Resources, 35 quests)",
    "(Resources, 252 quests)",
)

# The skill files the doc cross-references.
CROSS_REFERENCES = (
    "references/progression.md",
    "references/getting-started.md",
    "references/key-mods.md",
    "references/creative-checklist.md",
    # the logistics doc (guide #21) expands this page's #3 and must be linked back
    "references/logistics-guide.md",
)


def flatten(text: str) -> str:
    """Join wrapped lines so multi-line quotes and cells match as written."""
    return re.sub(r"\s*\n\s*", " ", text)


def strip_code_spans(text: str) -> str:
    """Blank out `inline code` so glob asterisks inside it can't read as markup."""
    return re.sub(r"`[^`]*`", " ", text)


class DocTestCase(unittest.TestCase):
    """Shared setup: load the doc once, plain and line-flattened."""

    @classmethod
    def setUpClass(cls) -> None:
        assert DOC_PATH.is_file(), f"missing {DOC_PATH}"
        cls.doc = DOC_PATH.read_text(encoding="utf-8")
        cls.flat = flatten(cls.doc)
        cls.quest_ids = {row[0] for row in VERIFIED_QUESTS}
        cls.quest_titles = {row[1] for row in VERIFIED_QUESTS}
        cls.allowed_names = cls.quest_titles | set(VERIFIED_NAMES)


# --------------------------------------------------------------------------------------
# provenance
# --------------------------------------------------------------------------------------

class TestProvenance(DocTestCase):

    def test_doc_exists_and_is_substantial(self) -> None:
        self.assertGreater(len(self.doc.strip()), 8000,
                           "automation-first-steps.md looks like a stub")

    def test_pins_repository_commit_version_and_date(self) -> None:
        for needle in (PACK_REPO, PACK_COMMIT, PACK_DATE, f"pack {PACK_VERSION}",
                       "CHANGELOG.md", "8.x", "examples/progress.example.json"):
            self.assertIn(needle, self.flat,
                          f"the doc must pin its source: {needle!r}")

    def test_names_the_quest_config_files_it_was_read_from(self) -> None:
        for needle in ("config/ftbquests/quests/chapters",
                       "lang/en_us/chapters",
                       "chapter_groups.snbt",
                       "config/ftbquests/quests/lang/en_us/chapter.snbt",
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
        self.assertIn("no recipes, no counts, no layouts", lowered)
        self.assertIn("read, not remembered", lowered)

    def test_hedges_stay_marked(self) -> None:
        self.assertIn("The ranking is judgement", self.flat)
        self.assertIn("approximate/judgement", self.flat)
        self.assertIn("judgement, not the pack's", self.flat)

    def test_untitled_quests_are_marked_not_named(self) -> None:
        self.assertIn("no title in the config", self.flat)

    def test_pinning_language(self) -> None:
        # The doc presents its snapshot as 8.2 state, not current truth.
        self.assertIn("This page is a snapshot of pack 8.2's config", self.flat)
        self.assertIn("If the player's book differs from anything here, his book wins",
                      self.flat)


# --------------------------------------------------------------------------------------
# verified snapshot: every mirrored name, id, subtitle, and item id is in the doc
# --------------------------------------------------------------------------------------

class TestVerifiedSnapshot(DocTestCase):

    def test_every_verified_quest_id_and_title_is_cited(self) -> None:
        for quest_id, title, _chapter in VERIFIED_QUESTS:
            self.assertIn(f"`{quest_id}`", self.doc,
                          f"missing quest id {quest_id} ({title})")
            self.assertIn(title, self.flat,
                          f"missing verified title {title!r}")

    def test_every_verified_name_is_present(self) -> None:
        for name in VERIFIED_NAMES:
            self.assertIn(name, self.flat, f"missing verified name {name!r}")

    def test_every_verified_subtitle_claim_is_present(self) -> None:
        for subtitle in VERIFIED_SUBTITLES:
            self.assertIn(subtitle, self.flat,
                          f"missing verified subtitle {subtitle!r}")

    def test_every_cited_task_item_id_is_present(self) -> None:
        for item_id in VERIFIED_ITEM_IDS:
            self.assertIn(f"`{item_id}`", self.doc,
                          f"missing task item id {item_id}")

    def test_verified_chapter_counts_are_quoted(self) -> None:
        for needle in CHAPTER_COUNT_STRINGS:
            self.assertIn(needle, self.flat, f"missing verified count context: {needle!r}")

    def test_quest_book_groups_are_named(self) -> None:
        for group in ("Main Questline", "Tech", "Resources", "Storage",
                      "Logistics", "Power", "Magic"):
            self.assertIn(group, self.flat, f"missing quest-book group {group!r}")


# --------------------------------------------------------------------------------------
# anchors table: rows can only repeat what the snapshot says
# --------------------------------------------------------------------------------------

class TestAnchorsTable(DocTestCase):

    def rows(self) -> "list[tuple[str, str]]":
        return re.findall(r"\*\*([^*]+)\*\* \| `([0-9A-F]{16})`", self.doc)

    def test_rows_exist_and_match_the_snapshot(self) -> None:
        rows = self.rows()
        self.assertGreaterEqual(len(rows), 21,
                                "the anchors table must list the cited quests")
        by_id = {quest_id: title for quest_id, title, _ in VERIFIED_QUESTS}
        for title, quest_id in rows:
            self.assertIn(quest_id, by_id,
                          f"anchors table cites unknown quest id {quest_id}")
            self.assertEqual(title, by_id[quest_id],
                             f"anchors table mis-titles {quest_id}: {title!r}")

    def test_every_id_backed_quest_has_a_row_or_inline_id(self) -> None:
        """Ids appear either in the anchors tables or inline - never both missing."""
        for quest_id, title, _chapter in VERIFIED_QUESTS:
            self.assertIn(f"`{quest_id}`", self.doc, f"{title} lost its id")


# --------------------------------------------------------------------------------------
# no-invented-names
# --------------------------------------------------------------------------------------

class TestNoInventedNames(DocTestCase):

    def test_no_quest_id_outside_the_snapshot(self) -> None:
        found = set(re.findall(r"\b[0-9A-F]{16}\b", self.doc))
        unknown = found - self.quest_ids
        self.assertEqual(unknown, set(),
                         f"quest ids not in the verified snapshot: {sorted(unknown)}")

    def test_no_item_id_outside_the_snapshot(self) -> None:
        found = set(re.findall(r"\b[a-z][a-z0-9_]*:[a-z0-9_]+\b", self.doc))
        unknown = found - set(VERIFIED_ITEM_IDS)
        self.assertEqual(unknown, set(),
                         f"item ids not in the verified snapshot: {sorted(unknown)}")

    def test_every_bold_run_is_a_verified_title_or_allowed_phrase(self) -> None:
        # Strip code spans first: `**bold**` inside code is the doc's own example.
        text = strip_code_spans(self.doc)
        runs = {re.sub(r"\s+", " ", run).strip()
                for run in re.findall(r"\*\*(.+?)\*\*", text, re.DOTALL)}
        allowed = self.allowed_names | set(PROSE_BOLD)
        unknown = runs - allowed
        self.assertEqual(unknown, set(),
                         f"bold names not verified against the config: {sorted(unknown)}")

    def test_every_claimed_subtitle_is_a_config_subtitle(self) -> None:
        claims = re.findall(r"subtitles?:?\s+\*([^*]+)\*", self.flat)
        claims += re.findall(r"subtitled\s+\*([^*]+)\*", self.flat)
        self.assertGreaterEqual(len(claims), 10, "subtitle claims should be pervasive")
        allowed = set(VERIFIED_SUBTITLES)
        for claim in claims:
            self.assertIn(claim, allowed,
                          f"claimed subtitle not in the verified snapshot: {claim!r}")

    def test_no_coordinates_y_levels_or_placeholders(self) -> None:
        self.assertNotRegex(self.doc, r"\b-?\d{1,5}\s+-?\d{1,5}\s+-?\d{1,5}\b",
                            "the doc must not carry coordinates")
        self.assertNotRegex(self.doc, r"\bY\s*-\d+",
                            "the doc must not carry y-levels")
        for marker in ("TODO", "TBD", "FIXME", "XXX"):
            self.assertNotIn(marker, self.doc, f"placeholder marker {marker} left in doc")


# --------------------------------------------------------------------------------------
# structure: five automations, in order, ranking marked as judgement
# --------------------------------------------------------------------------------------

class TestFiveAutomationsInOrder(DocTestCase):

    def test_section_headings_in_impact_order(self) -> None:
        positions = [self.flat.find(heading) for heading in SECTION_HEADINGS]
        for heading, position in zip(SECTION_HEADINGS, positions):
            self.assertGreaterEqual(position, 0, f"missing section {heading!r}")
        self.assertEqual(positions, sorted(positions),
                         "the five sections must appear in rank order")
        # ...and no duplicate numbered sections.
        numbered = re.findall(r"^## (\d)\. ", self.doc, re.MULTILINE)
        self.assertEqual(numbered, ["1", "2", "3", "4", "5"])

    def test_summary_table_ranks_in_order_with_anchors(self) -> None:
        positions = [self.flat.find(row) for row in SUMMARY_ROWS]
        for row, position in zip(SUMMARY_ROWS, positions):
            self.assertGreaterEqual(position, 0, f"missing summary row {row!r}")
        self.assertEqual(positions, sorted(positions),
                         "the summary table must list ranks 1..5 in order")
        # Each rank's short answer carries its verified anchor quest.
        table = self.flat[self.flat.find("| Rank |"):
                          self.flat.find("## 1. Ore processing")]
        for anchor in ("Basic Ore Doubling", "Early Game Power Options",
                       "Item Pipez", "Auto-Smelting Upgrade", "Mystical Agriculture!"):
            self.assertIn(anchor, table, f"short answer must anchor on {anchor!r}")

    def test_answers_the_beginner_question_verbatim(self) -> None:
        self.assertIn("what should I automate first?", self.flat)
        self.assertIn("ordered by impact for a beginner", self.flat)
        self.assertIn("If you only do one thing: automate ore processing first.",
                      self.flat)

    def test_ranking_is_marked_as_judgement_with_a_rationale_section(self) -> None:
        self.assertIn("## How the ranking was decided", self.flat)
        self.assertIn("Nothing in the quest config ranks automations", self.flat)
        self.assertIn("nothing in the pack ranks automations", self.flat)
        # Every section heading carries its hedge, on its own line in the source.
        lines = self.doc.splitlines()
        for heading in SECTION_HEADINGS:
            matches = [line for line in lines if line.startswith(heading)]
            self.assertEqual(len(matches), 1, f"expected exactly one {heading!r}")
            self.assertIn("judgement", matches[0],
                          f"{heading} must be marked judgement")

    def test_ore_processing_depends_on_the_metal_age_claim_is_flagged_verified(self) -> None:
        self.assertIn("(dependency verified in the config)", self.flat)


# --------------------------------------------------------------------------------------
# quotes: verified quest text is present and attributed
# --------------------------------------------------------------------------------------

class TestVerifiedQuotes(DocTestCase):

    def test_every_representative_quote_is_present(self) -> None:
        for quote in VERIFIED_QUOTES:
            self.assertIn(quote, self.flat, f"missing verified quote: {quote!r}")

    def test_quotes_are_presented_as_quest_text(self) -> None:
        self.assertIn("What the quest text says, quoted", self.flat)
        self.assertIn("quest text's own", self.flat)


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
        self.assertEqual(match.group(1), "1.7.0",
                         "adding a reference doc bumps the skill (1.7.0 as of the logistics doc)")


    def test_doc_is_linked_from_the_skill(self) -> None:
        self.assertGreaterEqual(
            self.skill.count("references/automation-first-steps.md"), 3,
            "SKILL.md must wire the doc from When to Use, Grounding, and Behaviors")

    def test_beginner_question_is_recognized(self) -> None:
        self.assertIn("what should i automate first", self.skill.lower())

    def test_grounding_bullet_dates_the_doc(self) -> None:
        self.assertIn("the automation doc date themselves", self.skill)
        self.assertIn(PACK_COMMIT, self.skill)
        self.assertIn("ranking marked as judgement", self.skill)

    def test_completion_checklist_covers_automation_answers(self) -> None:
        lowered = self.skill.lower()
        self.assertIn("automation answers quoted verified quest titles", lowered)

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
                          f"automation-first-steps.md must point at {sibling}")


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
