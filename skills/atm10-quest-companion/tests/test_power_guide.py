#!/usr/bin/env python3
"""Offline tests for the atm10-quest-companion power guide.

Stdlib-only and network-free: the guide is a Markdown document, so every case
here reads local files and checks them as text — existence, provenance and
grounding, the staged structure (early / mid / late / endgame), the verified
quest titles and task items each stage is built from, the power-system
relationships the pack's quests actually verify, and the discipline that keeps
the page honest (untitled quests marked, numbers only as attributed quest
text, recipes and unquoted figures refused).

The verified titles and ids below are the pack's own, read from the official
AllTheMods/ATM-10 quest config at main e5e3d1d83e (pack 8.2) — the same
snapshot the three endgame checklists use. If the pack moves on, refresh this
list from the new config instead of loosening a needle.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
POWER_GUIDE_MD = SKILL_ROOT / "references" / "power-guide.md"
PROGRESSION_MD = SKILL_ROOT / "references" / "progression.md"

# The pinned snapshot every endgame reference doc dates itself against.
PACK_COMMIT = "e5e3d1d83e"

# Pack-repository files the guide must name as its sources.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
    "config/bcc-common.toml",
)

# The Basic Power hub structure: the pack's own staging, by verified title.
POWER_HUB_TITLES = (
    "Basic Power",
    "All The Power!",
    "Early Game Power Options",
    "Starter Power",
    "Mid Game Power Options",
    "End Game Power Options",
    "More Power Than You'll Need",
    "Transferring Power",
    "Storing Power",
)

# Chapter 1's first-power line (the Main Questline's on-ramp to the hubs).
EARLY_TITLES = (
    "Wind Power",
    "Solar Power",
    "Lava Power",
    "Generators Galore",
    "Coal Generators",
    "Fossil Fuels",
    "Heat Generator",
    "Mekanism: Renewable Energy",
    "The Power of the Sun...",
)

# The mid-game menu the hubs route to, by verified title.
MID_TITLES = (
    "Mekanism: Gas-Burning Generator",
    "MELON POWER!",
    "More Powah!",
    "Extreme Reactors: Reactors",
    "Customizable Reactors!",
    "Our First Reactor",
    "Fueling our Passive Reactor",
    "The Energizing Orb",
    "8x What a deal!",
    "Bio Power",
    "Energy from moving things!",
    "Energy from Temperature",
    "Diesel Generator",
    "The Electric Age",
    "Electricity Generation",
    "LV Cables",
)

# The late/endgame lines, by verified title.
LATE_END_TITLES = (
    "Building An Actively Cooled Reactor",
    "To Make Steam!!",
    "Making Turbines",
    "The Turbine",
    "Fission Reactor",
    "Thermoelectric Boiler",
    "Making Energy with a Turbine",
    "Energized Induction Matrix",
    "Induction Cells",
    "Induction Providers",
    "Mekanism: Fusion Reactor",
    "Fusion Activate!",
    "Industrial Foregoing: Mycelial Reactor",
    "It's not Yourcelial Reactor",
    "Dyson Cube",
    "The power of the Sun, in the palm of your hand",
    "Draconic Evolution: Energy Core",
    "Basically Infinite Storage",
    "Energy Core Mulitblock",
    "What is Energy or as we call it, OP?",
)

# Powah's titled skeleton. Only 17 of its 109 quests carry a title in the
# config; the guide must quote this skeleton and mark the rest untitled.
POWAH_TITLED = (
    "Welcome to Powah!!!",
    "Starting with Dielectric Mats",
    "The Energizing Orb",
    "Tier: Tiny",
    "Tier: Basic",
    "Tier: Energized",
    "Tier: Blazing",
    "Tier: Niotic",
    "Tier: Spirited",
    "Tier: Nitro",
    "Reactor (Starter)",
    "Reactor (Basic)",
    "Reactor (Hardened)",
    "Reactor (Blazing)",
    "Reactor (Niotic)",
    "Reactor (Spirited)",
    "Reactor (Nitro)",
)

# Transfer, storage, and conversion quests — the "what connects to what" spine.
CONNECTIVITY_TITLES = (
    "Pipez: Energy Pipes",
    "Pipez: Upgrades",
    "Mekanism: Universal Cables",
    "Mekanism's Energy Transfer Pipe",
    "Mekanism: Quantum Entangloporter",
    "Mekanism: Energy Cubes",
    "More Power Storage",
    "RFTools Power: Powercells",
    "Integrated Dynamics: Energy Battery",
    "Batteries Included",
    "Flux Networks",
    "The Ultimate Wireless Power Solution",
    'The "Core" Crafting Materials',
    "Starting Your Network",
    "Becoming a Network Admin!",
    "Accessing Network Power",
    "Flux Storage",
    "Wireless Charging",
    "Automated Flux Dust",
    "Rotational Power",
    "Speed",
    "Stress",
    "Hand Crank",
    "Water Wheels",
    "Windmills",
    "Steam Engine",
    "Generating Pressure",
    "Generating Power",
    "Pressure from Power",
    "Pressure from the Sun",
    "Pressure from Liquids",
    "Pressure from Heat",
    "Pressure from Lightning",
    "Transfering Energy",  # spelled that way in the config (Oritech)
    "Storing Energy",
    "Power comes and goes through these",
)

# Task items the config states, across generation, storage, and transfer.
# Each id was read from a quest task at the pinned commit; a missing id means
# the guide stopped citing the verified build (or the pack moved — re-research).
TASK_ITEMS = (
    "minecraft:redstone",
    "minecraft:diamond",
    "minecraft:netherite_ingot",
    "mekanismgenerators:wind_generator",
    "mekanismgenerators:solar_generator",
    "mekanismgenerators:advanced_solar_generator",
    "mekanismgenerators:heat_generator",
    "mekanismgenerators:bio_generator",
    "mekanismgenerators:gas_burning_generator",
    "mekanismgenerators:fusion_reactor_controller",
    "mekanismgenerators:fission_reactor_casing",
    "mekanism:basic_energy_cube",
    "mekanism:basic_universal_cable",
    "mekanism:quantum_entangloporter",
    "mekanism:energy_tablet",
    "powah:uraninite_raw",
    "powah:dielectric_paste",
    "powah:energizing_orb",
    "powah:thermo_generator_starter",
    "powah:furnator_starter",
    "powah:solar_panel_starter",
    "powah:magmator_starter",
    "powah:reactor_starter",
    "powah:energy_cell_starter",
    "powah:player_transmitter_starter",
    "powah:player_transmitter_nitro",
    "powah:crystal_nitro",
    "generatorgalore:magmatic_generator",
    "generatorgalore:copper_generator",
    "bigreactors:basic_reactorcasing",
    "bigreactors:basic_reactorpowertapfe_active",
    "bigreactors:reinforced_reactorcasing",
    "bigreactors:insanite_block",
    "industrialforegoing:pitiful_generator",
    "industrialforegoing:mycelial_reactor",
    "justdirethings:generatort1",
    "actuallyadditions:coal_generator",
    "rftoolspower:coalgenerator",
    "rftoolspower:cell1",
    "pipez:energy_pipe",
    "fluxnetworks:flux_dust",
    "fluxnetworks:flux_plug",
    "fluxnetworks:flux_point",
    "fluxnetworks:basic_flux_storage",
    "fluxnetworks:flux_controller",
    "integrateddynamics:energy_battery",
    "draconicevolution:energy_core",
    "draconicevolution:crystal_binder",
    "dysoncubeproject:em_railejector_controller",
    "dysoncubeproject:ray_receiver_controller",
    "create:shaft",
    "create:water_wheel",
    "create:steam_engine",
    "create:stressometer",
    "modern_industrialization:bronze_boiler",
    "modern_industrialization:lv_steam_turbine",
    "modern_industrialization:lv_diesel_generator",
    "modern_industrialization:superconductor_cable",
    "modern_industrialization:nuclear_reactor",
    "pneumaticcraft:air_compressor",
    "pneumaticcraft:pneumatic_dynamo",
    "pneumaticcraft:flux_compressor",
    "immersiveengineering:dynamo",
    "immersiveengineering:thermoelectric_generator",
    "oritech:basic_generator_block",
    "oritech:energy_pipe",
    "ae2:energy_acceptor",
    "ae2:energy_cell",
    "powah:energy_cell_creative",
    "mekanism:creative_energy_cube",
    "integrateddynamics:energy_battery_creative",
    "ae2:creative_energy_cell",
)


class TestPowerGuideDoc(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = (
            POWER_GUIDE_MD.read_text(encoding="utf-8") if POWER_GUIDE_MD.is_file() else ""
        )
        cls.lower = cls.text.lower()
        cls.flat = re.sub(r"\s+", " ", cls.text)
        cls.flat_lower = cls.flat.lower()

    def test_power_guide_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(POWER_GUIDE_MD.is_file(), f"missing {POWER_GUIDE_MD}")
        self.assertGreater(
            len(self.text.strip()), 8000, "power-guide.md looks like a stub"
        )
        for heading in ("Provenance", "Grounding rules", "Cross-references",
                        "does not tell you"):
            self.assertIn(heading, self.text, f"missing section: {heading}")

    def test_provenance_names_the_pinned_snapshot(self) -> None:
        self.assertIn(PACK_COMMIT, self.text)
        self.assertIn("pack 8.2", self.text)
        self.assertIn("8.x", self.text)
        self.assertIn("CHANGELOG.md", self.text)
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.lower,
                          f"power-guide.md must name its source: {source}")
        # The four Power-group chapters and the snapshot's quest counts.
        for chapter in ("Basic Power", "Extreme Reactors", "Generators N Furnaces",
                        "Powah"):
            self.assertIn(chapter, self.text)
        for identifier in ("basic_power", "extreme_reactors", "generators", "powah"):
            self.assertIn(identifier, self.text,
                          f"the config filename {identifier} must be cited")

    def test_grounding_rules_are_carried_in_full(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lower,
                          f"power-guide.md must state the {needle!r} rule")
        self.assertRegex(self.lower, r"never invented|not invented|never invent",
                         "the guide must say its details were read, not invented")
        self.assertIn("no recipes", self.flat_lower)
        self.assertIn("does not tell you", self.flat_lower)

    def test_structure_covers_stages_systems_and_upgrade(self) -> None:
        """Key sections: the four stages in order, systems, transfer/storage."""
        stages = ("## Early game", "## Mid game", "## Late game", "## Endgame")
        positions = [self.text.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions),
                         "the stages must be written early -> mid -> late -> endgame")
        for stage in stages:
            self.assertIn("Generation to build", self.text)
            self.assertIn("When to upgrade", self.text)
        for system in ("The FE core", "Create: Rotational Power is not FE",
                       "Modern Industrialization: steam first",
                       "PneumaticCraft: pressure", "AE2: AE is converted from FE",
                       "Draconic Evolution: OP stays inside Draconic",
                       "Wireless transfer"):
            self.assertIn(system, self.text, f"missing system section: {system}")
        for heading in ("Storage to build", "Transfer to build"):
            self.assertIn(heading, self.text, f"missing section: {heading}")
        # The guide's "late" stage is its own interpolation and must say so.
        self.assertIn("the pack has no \"Late\" hub", self.text)
        self.assertIn("The short answer", self.text)

    def test_verified_hub_and_stage_titles_are_all_present(self) -> None:
        # Titles are checked against whitespace-flattened text, matching the
        # sibling endgame suites: a title may wrap across Markdown lines.
        for title in POWER_HUB_TITLES + EARLY_TITLES + MID_TITLES + LATE_END_TITLES:
            self.assertIn(title, self.flat,
                          f"missing a verified quest title: {title}")

    def test_powah_ladder_uses_only_its_titled_skeleton(self) -> None:
        self.assertEqual(len(POWAH_TITLED), 17)
        for title in POWAH_TITLED:
            self.assertIn(title, self.flat,
                          f"missing a titled Powah quest: {title}")
        self.assertIn("17 of its 109 quests carry an explicit title", self.flat)
        self.assertIn("32 of 34 in Basic Power", self.flat)
        # The reactor chain verifies the tier order; the guide must show it.
        chain = ("Reactor (Starter)", "Reactor (Basic)", "Reactor (Hardened)",
                 "Reactor (Blazing)", "Reactor (Niotic)", "Reactor (Spirited)",
                 "Reactor (Nitro)")
        spine = self.flat.index("The reactor dependency chain verifies the ladder order")
        positions = [self.flat.index(title, spine) for title in chain]
        self.assertEqual(positions, sorted(positions),
                         "the Powah reactors must stay in dependency order")

    def test_connectivity_titles_and_task_items_are_cited(self) -> None:
        for title in CONNECTIVITY_TITLES:
            self.assertIn(title, self.flat,
                          f"missing a verified transfer/storage title: {title}")
        for item in TASK_ITEMS:
            self.assertIn(item, self.text,
                          f"power-guide.md must cite the config's task item {item}")
        # The either/or structure is the book's, and the guide must name it.
        self.assertIn("smart_filter", self.text)
        self.assertIn("The choice is yours.", self.text)

    def test_untitled_quests_are_marked_never_titled(self) -> None:
        flat = self.flat
        # Powah's starter family, Chapter 1's two power quests, the Flux
        # network-admin quest, and MI's generator pair carry no config title.
        self.assertGreaterEqual(flat.count("(no title in the config)"), 6,
                                "untitled quests must be marked in place")
        self.assertIn("*(no title in the config; subtitle *Becoming a Network Admin!*",
                      flat)
        for item in ("powah:thermo_generator_starter", "oritech:basic_generator_block",
                     "modern_industrialization:lv_steam_turbine",
                     "modern_industrialization:bronze_boiler",
                     "ae2:energy_acceptor", "generatorgalore:culinary_generator"):
            self.assertIn(item, self.text,
                          f"the untitled quest for {item} must stay item-identified")

    def test_systems_relationships_keep_their_hedges(self) -> None:
        flat_lower = self.flat_lower
        # Verified bridges, quoted as quest text.
        self.assertIn("Mekanism uses FE", self.text)
        self.assertIn("turn your pressure in FE", self.text)
        self.assertIn("2:1 RF:AE", self.text)
        self.assertIn("does not have a way to generate power", flat_lower)
        # Unverified bridges must be refused, not assumed.
        for refusal in ("no quest in the chapters read offers a rotation-to-fe converter",
                        "do not list it as one",
                        "eu\u2194fe", "op\u2194fe"):
            self.assertIn(refusal, flat_lower,
                          f"missing the refusal hedge: {refusal}")
        # Ender IO is present in the modlist but unquested at this commit.
        self.assertIn("Ender IO", self.text)
        self.assertIn("present-but-unquested", flat_lower)

    def test_numbers_appear_only_as_attributed_quest_text(self) -> None:
        # Every output figure on the page is the quest author's, quoted.
        for figure in ("250k FE/t", "25MFE/t", "80MRF/t", "1GFE/t",
                       "9,223,372,036,854,775,808 FE", "256 EU/t"):
            self.assertIn(figure, self.text,
                          f"missing the quoted quest-text figure: {figure}")
        self.assertIn("quoted figures — the quest author's, verify in-game",
                      self.flat)
        self.assertIn("quoted exactly as written", self.flat)

    def test_the_guide_points_at_its_siblings(self) -> None:
        for sibling in ("progression.md", "key-mods.md", "atm-star-checklist.md",
                        "creative-checklist.md"):
            self.assertIn(sibling, self.text,
                          f"power-guide.md must point at {sibling}")


class TestPowerGuideSkillLinkage(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL_MD.read_text(encoding="utf-8") if SKILL_MD.is_file() else ""
        cls.progression = (
            PROGRESSION_MD.read_text(encoding="utf-8")
            if PROGRESSION_MD.is_file() else ""
        )

    def test_skill_md_documents_the_power_guide(self) -> None:
        self.assertTrue(SKILL_MD.is_file(), f"missing {SKILL_MD}")
        self.assertIn("references/power-guide.md", self.skill,
                      "SKILL.md must point at references/power-guide.md")
        for behaviour in ("which power", "when to upgrade"):
            self.assertIn(behaviour, self.skill.lower(),
                          f"SKILL.md must route the {behaviour!r} question")
        # The guide shares the endgame docs' pinned snapshot, and SKILL.md
        # must say so next to theirs.
        self.assertIn(PACK_COMMIT, self.skill)

    def test_progression_points_at_the_power_guide(self) -> None:
        self.assertIn("power-guide.md", self.progression,
                      "progression.md must point power questions at the guide")

    def test_this_suite_is_offline_and_stdlib_only(self) -> None:
        imported: set[str] = set()
        for line in Path(__file__).read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                imported.update(
                    part.strip().split()[0].split(".")[0]
                    for part in stripped[len("import "):].split(",")
                )
            elif stripped.startswith("from "):
                imported.add(stripped.split()[1].split(".")[0])
        network = {"socket", "urllib", "http", "requests", "ftplib", "smtplib",
                   "httpx", "aiohttp", "webbrowser", "subprocess"}
        self.assertEqual(imported & network, set(),
                         "this suite must stay offline: no network, no subprocesses")
        self.assertTrue(
            imported <= {"__future__", "re", "unittest", "pathlib"},
            f"unexpected import(s): {sorted(imported)}",
        )


if __name__ == "__main__":
    unittest.main()
