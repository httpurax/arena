#!/usr/bin/env python3
"""Offline tests for references/autocrafting-guide.md.

Stdlib-only and network-free: every case reads local files in the skill tree.

Covered:

  * the guide exists, is grounded in the named pack repository files at the pinned
    commit (e5e3d1d83e, pack 8.2, 2026-09-22), carries the same grounding rules as
    SKILL.md, and answers the beginner question it is written for;
  * the three Storage chapters it maps: verified chapter filenames/ids, quest counts
    and titled-quest counts, and the Storage group;
  * the AE2 autocrafting chain and the Refined Storage autocrafting chain, each in
    the config's dependency order, with every verified quest title and every config
    task item id;
  * the untitled quests: marked ``(no title in the config)`` in place, never given a
    derived title (the Molecular Assembler / crafting-CPU line, the RS Elite
    Autocrafter and disk line);
  * the Extended & Advanced AE scale-up quests (Assembler Matrix, Advanced Pattern
    Provider, Quantum Computer line, Quantum Crafter) with their quoted counts;
  * no-invented-names checks: plausible-but-absent item ids, quest titles, and mods
    must not appear, and recipe detail from the Quantum Ingredients descriptions
    must not be reproduced;
  * SKILL.md wiring: the new doc is linked and the version is bumped;
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
GUIDE_MD = SKILL_ROOT / "references" / "autocrafting-guide.md"

# The pinned snapshot every verified fact below was read from.
PINNED_COMMIT = "e5e3d1d83e"
PINNED_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"

# Pack-repository files the guide must name as its source.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
)

# The three Storage chapters, by config filename, with the quest counts the config
# states at the pinned commit and how many carry an explicit quest title.
CHAPTERS = (
    ("applied_energistics_2", "Applied Energistics 2", 74, 42),
    ("refined_storage", "Refined Storage", 72, 52),
    ("extended__advanced_ae", "Extended & Advanced AE", 56, 31),
)

# AE2 autocrafting chain titles in the config's dependency order (hub first).
AE2_CHAIN_TITLES = (
    "Auto-Crafting",
    "Patterns",
    "ME Level Emitter",
    "Redstone-Controlled ME",
)

# AE2 task item ids the chain's quests state, in table (dependency) order.
AE2_CHAIN_ITEMS = (
    "ae2:pattern_access_terminal",
    "ae2:pattern_encoding_terminal",
    "ae2:blank_pattern",
    "ae2:molecular_assembler",
    "ae2:1k_crafting_storage",
    "ae2:crafting_accelerator",
    "ae2:crafting_monitor",
    "ae2:speed_card",
    "ae2:level_emitter",
    "ae2:crafting_card",
)

# AE2 prerequisite task items (network before autocrafting).
AE2_PREREQ_ITEMS = (
    "ae2:charger",
    "ae2:inscriber",
    "ae2:meteorite_compass",
    "ae2:logic_processor",
    "ae2:calculation_processor",
    "ae2:engineering_processor",
    "ae2:certus_quartz_crystal",
    "ae2:fluix_crystal",
    "ae2:terminal",
    "ae2:crafting_terminal",
    "ae2:controller",
    "ae2:drive",
    "ae2:chest",
    "ae2:cell_component_1k",
    "ae2:energy_acceptor",
)

# Refined Storage autocrafting chain titles in dependency order.
RS_CHAIN_TITLES = (
    "Autocrafting",
    "Pattern Grid",
    "Autocrafter",
    "Monitoring Autocrafting",
    "Managing Autocrafters",
)

RS_CHAIN_ITEMS = (
    "refinedstorage:controller",
    "refinedstorage:disk_drive",
    "refinedstorage:storage_housing",
    "refinedstorage:cable",
    "refinedstorage:grid",
    "refinedstorage:crafting_grid",
    "refinedstorage:pattern",
    "refinedstorage:pattern_grid",
    "refinedstorage:autocrafter",
    "refinedstorage:autocrafting_monitor",
    "refinedstorage:autocrafter_manager",
    "refinedstorage:wireless_autocrafting_monitor",
    "refinedstorage:importer",
    "cabletiers:elite_autocrafter",
    "cabletiers:ultra_autocrafter",
    "cabletiers:mega_autocrafter",
)

# Extended & Advanced AE scale-up quest titles quoted by the guide.
EXTENDED_TITLES = (
    "Extended & Advanced AE",
    "Complex Crafter: The Crystal Assembler",
    "The Crystals of Space and Time: Entro Crystals",
    "Faster and Bigger: Extended Devices",
    "Many Assemblers In One: The Assembler Matrix",
    "Assembler Matrix Cores",
    "Specific Sided Patterns: The Advanced Pattern Provider",
    "Better Pattern Access: The Extended Pattern Access Terminal",
    "Quantum Ingredients",
    "Infinite Crafting Jobs: The Quantum Computer",
    "Massive Crafting Storage: The Quantum Computer Storage",
    "Co-Processing Oblivion: Quantum Computer Accelerator",
    "Heart of the Crafts: Quantum Computer Core",
    "Co-Processing To Infinity: Quantum Computer Multi-Threader",
    "Fully Automated Crafting: The Quantum Crafter",
    "The Ultimate Quantum Computer",
    "Reaction Efficency: The Reaction Chamber",
)

EXTENDED_ITEMS = (
    "extendedae:crystal_assembler",
    "extendedae:entro_crystal",
    "extendedae:ex_pattern_provider",
    "extendedae:assembler_matrix_frame",
    "extendedae:assembler_matrix_wall",
    "extendedae:assembler_matrix_glass",
    "extendedae:assembler_matrix_pattern",
    "extendedae:assembler_matrix_crafter",
    "extendedae:assembler_matrix_speed",
    "extendedae:ex_pattern_access_part",
    "advanced_ae:adv_pattern_encoder",
    "advanced_ae:shattered_singularity",
    "advanced_ae:quantum_alloy",
    "advanced_ae:quantum_processor",
    "advanced_ae:quantum_unit",
    "advanced_ae:quantum_structure",
    "advanced_ae:quantum_storage_128",
    "advanced_ae:quantum_storage_256",
    "advanced_ae:quantum_accelerator",
    "advanced_ae:quantum_core",
    "advanced_ae:quantum_multi_threader",
    "advanced_ae:quantum_crafter",
)

# Plausible names that are NOT in the three chapters' config and must never be
# presented as if they were: swapped namespaces, invented plain ids for filtered
# tasks, invented quest titles, and mods with no chapter in this mapping.
INVENTED_IDS = (
    "ae2:crafting_cpu",
    "ae2:crafting_unit",
    "`ae2:pattern_provider`",
    "refinedstorage:crafter",
    "refinedstorage:crafting_monitor",
    "refinedstorage:pattern_crafter",
    "extendedae:quantum_crafter",
    "extendedae:quantum_computer",
    "advanced_ae:assembler_matrix_frame",
    "megacells:quantum_crafter",
)

INVENTED_TITLES = (
    "Your First Autocraft",
    "Autocrafting 101",
    "ME Crafting CPU",
    "The Crafting CPU",
    "Refined Storage Autocrafting",
)

INVENTED_MODS = (
    "Botania",
    "Thermal Expansion",
    "LaserIO",
)


class TestAutocraftingGuide(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.guide = GUIDE_MD.read_text(encoding="utf-8") if GUIDE_MD.is_file() else ""
        cls.lower = cls.guide.lower()
        cls.flat = re.sub(r"\s+", " ", cls.guide)
        cls.flat_lower = cls.flat.lower()

    def section(self, marker: str) -> str:
        """The guide text from a section heading onward (for order checks)."""
        self.assertIn(marker, self.guide, f"missing section: {marker}")
        return self.guide.split(marker, 1)[1]

    # ------------------------------------------------------------------
    # existence, grounding, provenance
    # ------------------------------------------------------------------

    def test_guide_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.guide.strip()), 4000, "autocrafting-guide.md looks like a stub")

    def test_guide_answers_the_beginner_question(self) -> None:
        self.assertIn("how do I make the game craft things for me?", self.guide)
        self.assertIn("Applied Energistics 2", self.guide)
        self.assertIn("Refined Storage", self.guide)

    def test_guide_is_grounded_and_dated_to_the_pinned_commit(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lower, f"guide must state the {needle!r} rule")
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.lower, f"guide must name its source: {source}")
        self.assertIn(PINNED_COMMIT, self.guide)
        self.assertIn(PINNED_COMMIT_FULL, self.guide)
        self.assertIn("pack 8.2", self.guide)
        self.assertIn("8.x", self.guide)
        self.assertIn("2026-09-22", self.guide)
        self.assertIn("CHANGELOG.md", self.guide)
        self.assertIn("config/bcc-common.toml", self.guide)
        self.assertRegex(self.lower, r"never invented|not invented|never invent",
                         "guide must say its details were read, not invented")

    def test_guide_keeps_the_hedges(self) -> None:
        for needle in ("no recipes", "does not tell you", "approximate", "quest text",
                       "never a guess"):
            self.assertIn(needle, self.flat_lower, f"missing hedge: {needle}")
        self.assertIn("canvas, not as a numbered list", self.flat_lower)
        self.assertIn("in dependency order", self.flat_lower)

    def test_guide_names_the_three_chapters_and_quest_counts(self) -> None:
        self.assertIn("Storage", self.guide)
        for filename, title, quests, titled in CHAPTERS:
            self.assertIn(filename, self.guide, f"missing chapter id: {filename}")
            self.assertIn(title, self.guide, f"missing chapter title: {title}")
            self.assertIn(f"{quests} quests", self.guide,
                          f"guide must state the {filename} quest count")
            self.assertIn(str(titled), self.guide,
                          f"guide must state how many {filename} quests are titled")
        # The pre-network chapter is pointed at, not mapped as autocrafting.
        self.assertIn("Basic Storage", self.guide)
        self.assertIn("90 quests", self.guide)

    def test_guide_versions_the_mods_it_names(self) -> None:
        for needle in ("Applied Energistics 2 19.2.17", "Refined Storage 2.0.9",
                       "ExtendedAE 1.21-2.2.38-neoforge", "Advanced AE 1.6.12-1.21.1",
                       "MEGA Cells 4.11.0", "489 mod ids"):
            self.assertIn(needle, self.guide, f"missing verified mod version: {needle}")

    # ------------------------------------------------------------------
    # AE2 chain
    # ------------------------------------------------------------------

    def test_ae2_prerequisites_are_quoted(self) -> None:
        section = self.section("## AE2: the network you need before the first autocraft")
        for title in ("Applied Energistics 2", "First Things First", "Meteorite hunting",
                      "Processors", "Certus Quartz", "Fluix", "Basic Cabling", "Terminals",
                      "The Storage", "Creating your first Storage Cell"):
            self.assertIn(title, section, f"missing AE2 prerequisite quest: {title}")
        for item in AE2_PREREQ_ITEMS:
            self.assertIn(item, section, f"missing AE2 prerequisite item: {item}")
        # Quoted figures stay attributed to the quest text.
        self.assertIn("2:1 RF:AE", section)
        self.assertIn("8 channels", section)

    def test_ae2_autocrafting_chain_in_dependency_order(self) -> None:
        section = self.section("## AE2: the autocrafting chain, in dependency order")
        positions = [section.index(title) for title in AE2_CHAIN_TITLES]
        self.assertEqual(positions, sorted(positions),
                         "AE2 titled chain quests must stay in dependency order")
        item_positions = [section.index(item) for item in AE2_CHAIN_ITEMS]
        self.assertEqual(item_positions, sorted(item_positions),
                         "AE2 chain task items must stay in dependency order")
        for item in AE2_CHAIN_ITEMS:
            self.assertIn(item, section, f"missing AE2 chain item: {item}")
        # Filtered tasks are quoted as filters, with their lang task titles.
        self.assertIn("item_tag(ae2:pattern_provider)", section)
        self.assertIn("ME Pattern Provider", section)
        self.assertIn("Crafting Storage", section)
        # Quoted quest-text figures.
        self.assertIn("Up to 9 patterns", section)
        self.assertIn("Up to 6 MAs", section)
        self.assertIn("Control", self.guide)  # RS request quote lives in its own section

    def test_ae2_untitled_quests_are_marked_never_named(self) -> None:
        section = self.section("## AE2: the autocrafting chain, in dependency order")
        # Molecular Assembler, crafting CPU, co-processor, monitor, speed card,
        # crafting card: six untitled quests in the chain section alone (marked
        # with or without a subtitle, so match the shared prefix).
        self.assertGreaterEqual(section.count("(no title in the config"), 6,
                                "each untitled AE2 chain quest must be marked in place")
        for subtitle in ("Download more RAM", "Download more CPU cores",
                         "Download more VRAM", "Automation in upgrade form!"):
            self.assertIn(subtitle, section, f"missing verified subtitle: {subtitle}")


    # ------------------------------------------------------------------
    # Refined Storage chain
    # ------------------------------------------------------------------

    def test_rs_autocrafting_chain_in_dependency_order(self) -> None:
        section = self.section("## Refined Storage: the autocrafting chain, in dependency order")
        positions = [section.index(title) for title in RS_CHAIN_TITLES]
        self.assertEqual(positions, sorted(positions),
                         "RS chain quests must stay in dependency order")
        for item in RS_CHAIN_ITEMS:
            self.assertIn(item, self.guide, f"missing RS task item: {item}")
        # The book's own request method and processing example, quoted as quest text.
        self.assertIn("Control + Shift", self.guide)
        self.assertIn("Follow the Pattern", section)
        self.assertIn("Automated crafting!", section)

    def test_rs_crafter_tiers_quote_the_config(self) -> None:
        for needle in ("18 Pattern slots and works 2x faster",
                       "36 Pattern slots, works 5x faster",
                       "54 Pattern slots, works 8x faster",
                       "Speeding Everything Up!"):
            self.assertIn(needle, self.flat, f"missing quoted RS tier text: {needle}")
        # The Elite tier quest is untitled; the guide must mark it, not title it.
        section = self.section("### Processing patterns and the faster Autocrafters")
        self.assertIn("(no title in the config)", section)
        self.assertIn("cabletiers:elite_autocrafter", section)

    # ------------------------------------------------------------------
    # Extended & Advanced AE scale-up
    # ------------------------------------------------------------------

    def test_extended_scale_up_quests_and_items(self) -> None:
        section = self.section("## Extended & Advanced AE: the later AE2 scale-up (optional)")
        for title in EXTENDED_TITLES:
            self.assertIn(title, self.guide, f"missing Extended quest title: {title}")
        for item in EXTENDED_ITEMS:
            self.assertIn(item, section, f"missing Extended task item: {item}")
        # Quoted multiblock figures, attributed as quest text.
        for needle in ("3x3x3", "7x7x7", "36 pattern slots", "8928",
                       "256M crafting storage", "Won't accept crafting requests"):
            self.assertIn(needle, section, f"missing quoted Extended figure: {needle}")
        # Assembler Matrix task counts come from the config, not from prose.
        self.assertIn("×43", section)
        self.assertIn("×125", section)
        self.assertIn("×200", section)
        self.assertIn("×100", section)

    # ------------------------------------------------------------------
    # no invented names, no recipes
    # ------------------------------------------------------------------

    def test_no_invented_ids_titles_or_mods(self) -> None:
        for bad in INVENTED_IDS:
            self.assertNotIn(bad, self.guide, f"invented or mis-namespaced id present: {bad}")
        for bad in INVENTED_TITLES:
            self.assertNotIn(bad, self.guide, f"invented quest title present: {bad}")
        for bad in INVENTED_MODS:
            self.assertNotIn(bad, self.guide, f"unverified mod named as present: {bad}")

    def test_no_recipe_detail_is_reproduced(self) -> None:
        # The Quantum Ingredients descriptions do describe production; the guide
        # must list only their task items and defer the how to the book/JEI.
        for detail in ("Ender Dust", "Sky Stone Dust", "100 mB of Lava",
                       "Quantum Infused Dust"):
            self.assertNotIn(detail, self.guide,
                             f"recipe detail leaked into the guide: {detail}")
        self.assertIn("not reproduced here", self.flat)

    def test_manual_crafting_lookalikes_are_distinguished(self) -> None:
        # Crafting Terminal / Crafting Grid are hand crafting, not autocrafting;
        # the guide must say so instead of selling them as the answer.
        self.assertIn("ae2:crafting_terminal", self.guide)
        self.assertIn("refinedstorage:crafting_grid", self.guide)
        self.assertIn("not yet autocrafting", self.flat_lower)
        self.assertIn("still crafts", self.flat_lower)

    # ------------------------------------------------------------------
    # SKILL.md wiring
    # ------------------------------------------------------------------

    def test_skill_md_wires_the_new_doc_and_bumps_version(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/autocrafting-guide.md", skill,
                      "SKILL.md must point at the new guide")
        self.assertRegex(skill, re.compile(r"^version:\s*1\.6\.0\s*$", re.MULTILINE),
                         "SKILL.md version must be bumped to 1.6.0 for the new docs")

        self.assertIn("autocrafting", skill.lower())

    # ------------------------------------------------------------------
    # offline guarantee (this suite)
    # ------------------------------------------------------------------

    def test_this_suite_imports_no_network_module(self) -> None:
        network = {"socket", "urllib", "http", "requests", "ftplib", "smtplib",
                   "httpx", "aiohttp", "webbrowser", "subprocess"}
        found = set()
        for line in Path(__file__).read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        self.assertEqual(found & network, set())


if __name__ == "__main__":
    unittest.main()
