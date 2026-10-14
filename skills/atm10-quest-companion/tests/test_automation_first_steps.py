#!/usr/bin/env python3
"""Offline tests for references/automation-first-steps.md (atm10-quest-companion).

Stdlib-only and network-free, like the rest of this suite: the reference doc is a
snapshot of the AllTheMods/ATM-10 quest config at the pinned commit, so every case
here is a string check against data mirrored below from that snapshot.

Covered:

  * the doc exists, is not a stub, carries the skill's grounding rules (in-game
    quest book + JEI authoritative, approximate details flagged, nothing invented),
    and dates itself to commit ``e5e3d1d83e`` / pack 8.2 / the skill's 8.x stamp;
  * every verified quest title and tier subtitle the doc uses is mirrored here from
    the pack config (chapters ``mainquestline_part_1``, ``mekanism``, ``create``,
    ``oritech``, ``mi_steam``, ``basic_power``, ``generators``, ``basic_logistics``,
    ``pylons``, ``elmystical_agriculturerr``, ``productive_bees``,
    ``industrial_foregoing``, ``applied_energistics_2``, ``refined_storage``,
    ``hostile_neural_networks``, ``occultism``, ``allthemodium``);
  * the five automations appear, in the doc's own stated order, and the ordering is
    explicitly flagged as judgement rather than pack data;
  * the key quest-text quotes appear verbatim (whitespace-normalized);
  * no invented names: every ``namespace:path`` id the doc cites is in the verified
    allowlist below, untitled quests stay marked ``(no title in the config)``, and the
    doc never claims a "Tier 5 Ore Processing" subtitle the config does not have;
  * SKILL.md wires the doc in and its version was bumped for it;
  * this suite itself imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = SKILL_ROOT / "references" / "automation-first-steps.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"

# The pinned snapshot: AllTheMods/ATM-10 main at e5e3d1d83e (2026-09-22), pack 8.2.
PINNED_COMMIT = "e5e3d1d83e"

# --------------------------------------------------------------------------------------
# verified pack data the doc must reproduce (read from the config at the pinned commit)
# --------------------------------------------------------------------------------------

# Quest titles, exactly as the en_us lang files state them (color codes stripped).
VERIFIED_TITLES = (
    # Chapter 1: The Beginning (mainquestline_part_1)
    "Basic Ore Doubling", "The Metal Age", "Furnace Upgrades!", "Furnace Augments",
    "Lava Power", "Wind Power", "Solar Power", "Generators Galore",
    # Mekanism
    "Mekanism", "Enrich then Smelt", "Enrichment Chamber", "Energized Smelter",
    "Making Oxygen for Purifier", "Crush and Enrich our Clumps",
    "Making Chlorine", "Injecting Hydrogen Chloride",
    "Shard, to Clump, to Dust, to Ingot",
    "Creating Sulfuric Acid", "Melting Ores with Acid and Crystallizing them",
    "Making more Hydrogen Chloride", "Crystal, Shard, Clump, ETC",
    "Thermal Evaporation Plant", "Logistical Transporters", "Mekanism Logistics",
    # Create
    "Crushing Wheels", "Millstone", "Encased Fan", "Item Logistics", "Andesite Funnel",
    "Mechanical Harvester", "Mechanical Crafter",
    # Oritech
    "Oritech Beginnings", "Refining Ores", "Clumps", "Ore Processing",
    # Modern Industrialization: Steam Age
    "Forge Hammer",
    # Basic Power
    "Basic Power", "Early Game Power Options", "Mid Game Power Options",
    "End Game Power Options", "Transferring Power", "Storing Power",
    "Pipez: Energy Pipes", "Mekanism: Universal Cables",
    "Mekanism: Quantum Entangloporter", "Mekanism: Energy Cubes",
    "RFTools Power: Powercells", "Integrated Dynamics: Energy Battery",
    "Automated Flux Dust",
    # Generators N Furnaces
    "The Furnace", "Copper Generator", "Iron Generator", "Gold Generator",
    "Diamond Generator", "Augment: Factory",
    # Basic Logistics
    "Logistics", "Pipez", "Item Pipez",
    # Mystical Agriculture (elmystical_agriculturerr)
    "Mystical Agriculture!", "Inferium", "Inferium Farmland", "Infusion Altar",
    "Infusion Crystal", "Inferium Growth Accelerator", "Prudentium", "Tertium",
    "Prudentium Farmland", "Tertium Farmland",
    # Productive Bees
    "Capturing Bees!", "Your First Beehive", "Advanced Beehive",
    # Industrial Foregoing
    "Plants",
    # AE2 / Refined Storage
    "Auto-Crafting", "Patterns", "Autocrafting", "Autocrafter", "Pattern Grid",
    "Monitoring Autocrafting", "Managing Autocrafters",
    # later-stage signposts
    "Simulating Deaths", "Creating Loot", "Demon Mining", "Mining Dimension",
)

# Quest subtitles the doc quotes, exactly as the lang files state them.
VERIFIED_SUBTITLES = (
    "The Start of Your Own Factory",
    "Tier 1 Ore Processing", "Tier 2 Ore Processing",
    "Tier 3 Ore Processing", "Tier 4 Ore Processing",
    "Breaks Raw Ores into Dusts", "Mekanism's Powered Furnace",
    "Starter Power", "More Power Than You'll Need", "Batteries Included",
    "Mekanism's Energy Transfer Pipe", "Doesn't just work for Power",
    "Items", "The Configurator",
    "Order up", "Follow the Pattern", "Automated crafting!", "GET IN",
    "No more shearing.", "Processing Honeycombs", "Recycling!",
    "Infinite Resources", "It all starts here",
    "Tier: 1", "Tier: 2", "Tier: 3", "Range: 9 Blocks", "Creating Seeds",
    "Find nickel ore to find begin your journey",  # sic - spelled that way in the config
    "Turning one into more", "Fragment raw ores", "Maximum output", "This blows!",
)

# Every namespace:path id the doc is allowed to cite, mirrored from task items,
# task filters, and reward tables in the chapters' .snbt files at the pinned commit.
VERIFIED_ITEM_IDS = frozenset((
    "ae2:annihilation_plane",
    "ae2:blank_pattern",
    "ae2:growth_accelerator",
    "ae2:pattern_access_terminal",
    "ae2:pattern_encoding_terminal",
    "alltheores:copper_dust",
    "alltheores:iron_dust",
    "alltheores:ore_hammers",  # item tag, from the Basic Ore Doubling task filter
    "appflux:charged_redstone_block",
    "create:belt_connector",
    "create:crushing_wheel",
    "generatorgalore:copper_generator",
    "industrialforegoing:fluid_transporter_type",
    "industrialforegoing:item_transporter_type",
    "industrialforegoing:plant_gatherer",
    "industrialforegoing:plant_sower",
    "ironfurnaces:augment_factory",
    "ironfurnaces:copper_furnace",
    "ironfurnaces:iron_furnace",
    "ironfurnaces:upgrade_copper",
    "ironfurnaces:upgrade_iron",
    "mekanism:energized_smelter",
    "mekanism:enrichment_chamber",
    "mekanism:thermal_evaporation_block",
    "mekanismgenerators:wind_generator",
    "minecraft:beehive",
    "minecraft:diamond",
    "modern_industrialization:forge_hammer",
    "modern_industrialization:steam_quarry",
    "modern_industrialization:steel_machine_casing",
    "mysticalagriculture:certus_quartz_seeds",
    "mysticalagriculture:inferium_essence",
    "mysticalagriculture:inferium_farmland",
    "mysticalagriculture:inferium_growth_accelerator",
    "mysticalagriculture:inferium_seeds",
    "mysticalagriculture:infusion_altar",
    "mysticalagriculture:infusion_crystal",
    "mysticalagriculture:infusion_pedestal",
    "mysticalagriculture:iron_seeds",
    "mysticalagriculture:redstone_seeds",
    "mysticalagriculture:seed_reprocessor",
    "oritech:copper_gem",
    "oritech:gold_gem",
    "oritech:iron_gem",
    "oritech:nickel_gem",
    "oritech:platinum_gem",
    "oritech:uranium_gem",
    "pipez:energy_pipe",
    "pipez:item_pipe",
    "pipez:wrench",
    "productivebees:spawn_egg_configurable_bee",
    "pylons:harvester_pylon",
    "refinedstorage:autocrafter",
    "refinedstorage:pattern",
    "refinedstorage:pattern_grid",
    "xycraft_machines:extractor",
))

# Quest-text quotes the doc must carry verbatim (whitespace-normalized).
VERIFIED_QUOTES = (
    "Smelting down raw ores in the beginning is necessary, but you are missing out on "
    "extra resources!",
    "These will break down 1 raw ore into 2 ore dust, which can be smelted into ingots, "
    "effectively doubling your ingot output!",
    "Want more per raw ore? Check out the mod Occultism!",
    "The very first and simplest Ore Processing is just 2 Machines! Enrichers and Smelters!",
    "Congrats, you just Ore Processed!",
    "make automation easier by allowing you to auto-pull or push from the sides using "
    "the config on the left of the interface.",
    "These don't produce a ton of power, but they are typically easy or cheap to get in "
    "the early game!",
    "Harvester Pylons work as a very simple Auto-Farm.",
    "You'll want to start growing Inferium as soon as you can!",
    "a resource generation mod that allows you to grow a large variety of vanilla and "
    "modded resources using Seeds.",
    "getting a Powered Centrifuge soon after is a must.",
    "AE2's auto-crafting system begins with the ME Pattern Provider.",
    "Once a recipe is placed into the machine, you'll be able to 'Request' an item to be "
    "crafted from your Grid.",
    "The Quarry is a multiblock to generate resources. It requires Drills and Steam to "
    "function.",
    "I recommend setting up a Quarry.",
)

# The five automations, by the anchor of each numbered section, in the doc's order.
FIVE_STEPS = (
    "1. Ore doubling",
    "2. Power you can walk away from",
    "3. Moving items",
    "4. Farms",
    "5. Auto-crafting from your storage network",
)


def flatten(text: str) -> str:
    """Normalize markdown for substring checks: drop blockquote markers, fold
    line wraps (the doc hard-wraps at ~90 columns, mid-title and mid-quote)."""
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text)


class DocTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = DOC_PATH.read_text(encoding="utf-8") if DOC_PATH.is_file() else ""
        cls.flat = flatten(cls.doc)
        cls.lower = cls.doc.lower()
        cls.flat_lower = flatten(cls.lower)


class TestDocExistsAndIsGrounded(DocTestCase):

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(DOC_PATH.is_file(), f"missing {DOC_PATH}")
        self.assertGreater(len(self.doc.strip()), 8000, "the doc looks like a stub")

    def test_doc_states_the_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "judgement"):
            self.assertIn(needle, self.lower, f"the doc must state the {needle!r} rule")
        self.assertRegex(self.lower, r"never invented|read, not remembered",
                         "the doc must say its details were read, not invented")
        self.assertIn("no recipes", self.lower)

    def test_doc_dates_itself_to_the_pinned_snapshot(self) -> None:
        self.assertIn(PINNED_COMMIT, self.doc)
        self.assertIn("AllTheMods/ATM-10", self.doc)
        self.assertIn("pack 8.2", self.doc)
        self.assertIn("8.x", self.doc)
        self.assertIn("2026-09-22", self.doc)
        self.assertIn("config/ftbquests/quests/chapters", self.doc)
        self.assertIn("lang/en_us/chapters", self.doc)

    def test_doc_answers_the_beginner_question(self) -> None:
        self.assertIn("what should i automate first?", self.flat_lower)


class TestVerifiedQuestTitles(DocTestCase):

    def test_every_verified_title_appears(self) -> None:
        for title in VERIFIED_TITLES:
            self.assertIn(title, self.flat,
                          f"the doc is missing a verified quest title: {title}")

    def test_every_verified_subtitle_appears(self) -> None:
        for subtitle in VERIFIED_SUBTITLES:
            self.assertIn(subtitle, self.flat,
                          f"the doc is missing a verified quest subtitle: {subtitle}")

    def test_mekanism_tier_counts_match_the_config(self) -> None:
        # The mekanism chapter's lang file carries the tier subtitles on exactly
        # 1 + 2 + 3 + 4 quests; the doc states those counts.
        self.assertIn("Tier 1 Ore Processing** (1 quest)", self.flat)
        self.assertIn("Tier 2 Ore Processing** (2 quests)", self.flat)
        self.assertIn("Tier 3 Ore Processing** (3 quests)", self.flat)
        self.assertIn("Tier 4 Ore Processing** (4 quests)", self.flat)

    def test_untitled_quests_stay_marked(self) -> None:
        # Five quests the doc leans on carry no title in the config: the Pylons
        # harvester, the AE2 annihilation plane, the AE2 growth accelerator, the
        # Productive Bees centrifuge, and the MI steam quarry. The doc must mark
        # them rather than derive names.
        self.assertGreaterEqual(self.flat.count("(no title in the config)"), 5,
                                "untitled quests must be marked, not renamed")

    def test_no_tier_5_is_claimed(self) -> None:
        # The config has no "Tier 5 Ore Processing" subtitle; the doc may only
        # mention it to say it does not exist.
        self.assertIn('no "Tier 5 Ore Processing" subtitle anywhere in the chapter',
                      self.flat)
        occurrences = self.flat.count("Tier 5 Ore Processing")
        self.assertEqual(occurrences, 1,
                         "Tier 5 Ore Processing may appear only in the denial sentence")


class TestVerifiedQuotes(DocTestCase):

    def test_key_quest_text_quotes_are_verbatim(self) -> None:
        for quote in VERIFIED_QUOTES:
            self.assertIn(quote, self.flat,
                          f"the doc must quote this quest text verbatim: {quote[:60]}...")


class TestNoInventedNames(DocTestCase):

    ID_RE = re.compile(r"`([a-z][a-z0-9_]*:[a-z0-9_/.]+)`")

    def test_every_cited_id_is_verified(self) -> None:
        cited = set(self.ID_RE.findall(self.flat))
        self.assertGreater(len(cited), 40,
                           "the doc should cite the config's task items by id")
        invented = sorted(cited - VERIFIED_ITEM_IDS)
        self.assertEqual(invented, [],
                         f"the doc cites ids not present in the pinned config: {invented}")

    def test_allowlist_itself_has_no_duplicates_or_junk(self) -> None:
        self.assertEqual(len(VERIFIED_ITEM_IDS), 56)
        for item in VERIFIED_ITEM_IDS:
            self.assertRegex(item, r"^[a-z][a-z0-9_]*:[a-z0-9_/.]+$")

    def test_no_coordinates_or_dimensions_are_invented(self) -> None:
        # The doc must not state Y levels, biome coordinates, or dimension portals
        # that the config does not carry; it defers to the book instead.
        self.assertNotRegex(self.doc, r"\bY[ =-]?\d+\b")
        self.assertIn("never a guess", self.flat_lower)


class TestFiveStepsAndOrder(DocTestCase):

    def test_the_five_steps_appear_in_order(self) -> None:
        positions = []
        for step in FIVE_STEPS:
            index = self.flat.find(step)
            self.assertNotEqual(index, -1, f"missing the numbered section: {step}")
            positions.append(index)
        self.assertEqual(positions, sorted(positions),
                         "the five automations must stay in the doc's impact order")

    def test_ordering_is_flagged_as_judgement(self) -> None:
        self.assertIn("ordering and the impact reasoning are this skill's judgement",
                      self.flat_lower)
        self.assertIn("The five-item ordering is judgement, not pack data", self.flat)

    def test_alternatives_are_never_a_required_path(self) -> None:
        self.assertIn("never invent a \"required\" path", self.flat_lower)
        self.assertIn("alternatives, not a required path", self.flat_lower)

    def test_doc_defers_to_the_book_for_specifics(self) -> None:
        self.assertIn("open that quest in the book / look it up in JEI", self.flat)
        self.assertIn("quest entries and jei", self.flat_lower)


class TestDocWiring(DocTestCase):

    def test_doc_cross_references_its_siblings(self) -> None:
        for sibling in ("getting-started.md", "progression.md", "key-mods.md",
                        "creative-checklist.md"):
            self.assertIn(sibling, self.doc, f"the doc must point at {sibling}")

    def test_skill_md_wires_the_doc_in(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/automation-first-steps.md", skill,
                      "SKILL.md must point at the new reference doc")
        self.assertIn("automation-first-steps", skill.lower())

    def test_skill_md_version_was_bumped(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", skill, re.M)
        self.assertIsNotNone(match, "SKILL.md frontmatter must carry a version")
        version = tuple(int(part) for part in match.groups())
        self.assertGreaterEqual(version, (1, 2, 0),
                                "adding a reference doc must bump the skill version")


class TestOffline(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_module(self) -> None:
        found: "set[str]" = set()
        for line in Path(__file__).read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        self.assertEqual(found & set(self.NETWORK_IMPORTS), set())


if __name__ == "__main__":
    unittest.main()
