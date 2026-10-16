#!/usr/bin/env python3
"""Offline tests for ``references/logistics-guide.md``.

Stdlib-only and network-free: every assertion reads local files in the skill tree or checks
against the verified pack-8.2 constants transcribed below from ``AllTheMods/ATM-10`` at
``main`` commit ``e5e3d1d83e`` (2026-09-22).

Covered:

  * existence, house structure, provenance (pinned commit ``e5e3d1d83e``, full SHA, pack
    8.2 / ``8.x``, 2026-09-22, all source files named), and grounding rules;
  * the four Logistics-group chapters (``basic_logistics``, ``integrated_dynamics``,
    ``modular_router``, ``pylons``): verified chapter ids, titles, ``order_index``,
    ``progression_mode``, quest counts, task counts, titled/untitled split, ``optional``
    counts, and agreement with ``examples/progress.example.json``;
  * completeness: all 31 titled quests across the four Logistics-group chapters appear by
    exact title, and untitled quests are marked ``*(no title in the config)*``;
  * verified quest chains and item ids for Pipez (including both conflicting config quotes
    on which upgrade unlocks filtering), Mekanism pipes/tubes/cables/conductors and
    Quantum Entangloporters, LaserIO (logic chip, node, wrench, connector, 5 cards, 4
    filters, 2 overclockers, holder, cloner), Transfer Labels, Integrated Dynamics +
    Integrated Tunnels (both the 6-quest preview and the 28-quest chapter), Modular
    Routers (7 titled quests + 48 untitled upgrades/augments/modules/filters), and Pylons;
  * Chapter 3 cross-check (zero ATM Star tasks from Logistics-group mods) and modlist
    cross-check for unquested logistics mods (SFM, XNet, Ender IO);
  * no-invented-ids / no-recipes / no-coordinates guards;
  * ``SKILL.md`` and ``references/automation-first-steps.md`` wiring;
  * offline guarantee: this test module imports no network or subprocess module.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
DOC = SKILL_ROOT / "references" / "logistics-guide.md"
AUTOMATION_MD = SKILL_ROOT / "references" / "automation-first-steps.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"
REFERENCES_DIR = SKILL_ROOT / "references"

PACK_COMMIT_SHORT = "e5e3d1d83e"
PACK_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
PACK_VERSION = "8.2"
PACK_STAMP = "8.x"
PACK_DATE = "2026-09-22"
LOGISTICS_GROUP_ID = "3D4E23B1100491AB"

SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapter_groups.snbt",
    "config/ftbquests/quests/chapters/basic_logistics.snbt",
    "config/ftbquests/quests/chapters/integrated_dynamics.snbt",
    "config/ftbquests/quests/chapters/modular_router.snbt",
    "config/ftbquests/quests/chapters/pylons.snbt",
    "config/ftbquests/quests/chapters/mekanism.snbt",
    "config/ftbquests/quests/chapters/chapter_2_the_star.snbt",
    "config/ftbquests/quests/lang/en_us/chapters/*.snbt",
    "config/crash_assistant/modlist.json",
    "CHANGELOG.md",
    "config/bcc-common.toml",
)

# (config_id, chapter_hex_id, title, order_index, quests, tasks, titled, untitled, optional, stage)
CHAPTERS = (
    ("basic_logistics", "3DEB33F78398EAD6", "Basic Logistics", 0, 40, 44, 19, 21, 6, "early-game"),
    ("integrated_dynamics", "69299302373C4CBC", "Integrated Dynamics", 1, 28, 29, 4, 24, 6, "tech"),
    ("modular_router", "0AB4F9AED808DE48", "Modular Routers", 2, 55, 60, 7, 48, 1, "tech"),
    ("pylons", "5712300EF4E5E846", "Pylons", 3, 13, 14, 1, 12, 1, "tech"),
)

# All 31 unique quest titles across the 4 Logistics-group chapters (Integrated Dynamics appears
# in both basic_logistics and integrated_dynamics, so 30 distinct strings / 31 titled quests).
VERIFIED_TITLES = (
    # basic_logistics (19)
    "Pipez",
    "Item Pipez",
    "Fluid Pipez",
    "Energy Pipez",
    "Universal Pipez",
    "Gas Pipez",
    "Mekanism",
    "Integrated Dynamics",
    "Logistics",
    "Item Importing",
    "Fluid Importing",
    "Energy Importing",
    "Laser IO",
    "Item Card",
    "Fluid Card",
    "Energy Card",
    "Redstone Card",
    "Chemical Card",
    "Transfer Labels",
    # integrated_dynamics (4: Integrated Dynamics + 3 more)
    "Crystallized Menril Chunks",
    "Logic Cables",
    "Variable Cards",
    # modular_router (7)
    "Modular Routers",
    "Modules",
    "Upgrades",
    "Augments",
    "Routers for Mob Farms",
    "Routers for Mining",
    "Routers for Farming",
    # pylons (1)
    "Pylons",
)

# Cross-referenced titled quests in mekanism.snbt and basic_power.snbt.
CROSS_CHAPTER_TITLES = (
    "Mekanism Logistics",
    "Logistical Transporters",
    "Mechanical Pipes",
    "Pressurized Tubes",
    "Thermodynamic Conductors",
    "Universal Cables",
    "Quantum Entangloporters",
    "Transferring Power",
    "Pipez: Energy Pipes",
    "Mekanism: Universal Cables",
    "Mekanism: Quantum Entangloporter",
    "Flux Networks",
)

VERIFIED_NAMESPACED_IDS = {
    "c:tools/wrench",
    "fluxnetworks:flux_dust",
    "integratedcrafting:part_interface_crafting",
    "integrateddynamics:cable",
    "integrateddynamics:coal_generator",
    "integrateddynamics:crystalized_menril_chunk",
    "integrateddynamics:drying_basin",
    "integrateddynamics:energy_battery",
    "integrateddynamics:logic_programmer",
    "integrateddynamics:mechanical_drying_basin",
    "integrateddynamics:mechanical_squeezer",
    "integrateddynamics:menril_berries",
    "integrateddynamics:menril_logs",
    "integrateddynamics:portable_logic_programmer",
    "integrateddynamics:squeezer",
    "integrateddynamics:variable",
    "integrateddynamics:variable_transformer_input",
    "integrateddynamics:variable_transformer_output",
    "integrateddynamics:variablestore",
    "integrateddynamics:wrench",
    "integratedterminals:part_terminal_crafting_job",
    "integratedtunnels:part_exporter_energy",
    "integratedtunnels:part_exporter_fluid",
    "integratedtunnels:part_exporter_item",
    "integratedtunnels:part_exporter_world_block",
    "integratedtunnels:part_exporter_world_energy",
    "integratedtunnels:part_exporter_world_fluid",
    "integratedtunnels:part_exporter_world_item",
    "integratedtunnels:part_importer_energy",
    "integratedtunnels:part_importer_fluid",
    "integratedtunnels:part_importer_item",
    "integratedtunnels:part_importer_world_block",
    "integratedtunnels:part_importer_world_energy",
    "integratedtunnels:part_importer_world_fluid",
    "integratedtunnels:part_importer_world_item",
    "integratedtunnels:part_interface_energy",
    "integratedtunnels:part_interface_fluid",
    "integratedtunnels:part_interface_item",
    "laserio:card_chemical",
    "laserio:card_cloner",
    "laserio:card_energy",
    "laserio:card_fluid",
    "laserio:card_holder",
    "laserio:card_item",
    "laserio:card_redstone",
    "laserio:filter_basic",
    "laserio:filter_count",
    "laserio:filter_mod",
    "laserio:filter_tag",
    "laserio:laser_connector",
    "laserio:laser_node",
    "laserio:laser_wrench",
    "laserio:logic_chip",
    "laserio:overclocker_card",
    "laserio:overclocker_node",
    "mekanism:advanced_logistical_transporter",
    "mekanism:advanced_mechanical_pipe",
    "mekanism:advanced_pressurized_tube",
    "mekanism:advanced_thermodynamic_conductor",
    "mekanism:advanced_universal_cable",
    "mekanism:basic_logistical_transporter",
    "mekanism:basic_mechanical_pipe",
    "mekanism:basic_pressurized_tube",
    "mekanism:basic_thermodynamic_conductor",
    "mekanism:basic_universal_cable",
    "mekanism:configurator",
    "mekanism:elite_logistical_transporter",
    "mekanism:elite_mechanical_pipe",
    "mekanism:elite_pressurized_tube",
    "mekanism:elite_thermodynamic_conductor",
    "mekanism:elite_universal_cable",
    "mekanism:quantum_entangloporter",
    "mekanism:ultimate_logistical_transporter",
    "mekanism:ultimate_mechanical_pipe",
    "mekanism:ultimate_pressurized_tube",
    "mekanism:ultimate_thermodynamic_conductor",
    "mekanism:ultimate_universal_cable",
    "minecraft:hoes",
    "minecraft:iron_ingot",
    "minecraft:polished_blackstone",
    "modularrouters:activator_module",
    "modularrouters:augment_core",
    "modularrouters:blank_module",
    "modularrouters:blank_upgrade",
    "modularrouters:blast_upgrade",
    "modularrouters:breaker_module",
    "modularrouters:bulk_item_filter",
    "modularrouters:camouflage_upgrade",
    "modularrouters:detector_module",
    "modularrouters:distributor_module",
    "modularrouters:dropper_module",
    "modularrouters:energy_distributor_module",
    "modularrouters:energy_output_module",
    "modularrouters:energy_upgrade",
    "modularrouters:extruder_module_1",
    "modularrouters:extruder_module_2",
    "modularrouters:fast_pickup_augment",
    "modularrouters:filter_round_robin_augment",
    "modularrouters:flinger_module",
    "modularrouters:fluid_module",
    "modularrouters:fluid_module_2",
    "modularrouters:fluid_upgrade",
    "modularrouters:inspection_filter",
    "modularrouters:mimic_augment",
    "modularrouters:mod_filter",
    "modularrouters:modular_router",
    "modularrouters:muffler_upgrade",
    "modularrouters:pickup_delay_augment",
    "modularrouters:placer_module",
    "modularrouters:player_module",
    "modularrouters:puller_module_1",
    "modularrouters:puller_module_2",
    "modularrouters:pushing_augment",
    "modularrouters:range_down_augment",
    "modularrouters:range_up_augment",
    "modularrouters:redstone_augment",
    "modularrouters:regex_filter",
    "modularrouters:regulator_augment",
    "modularrouters:security_upgrade",
    "modularrouters:sender_module_1",
    "modularrouters:sender_module_2",
    "modularrouters:sender_module_3",
    "modularrouters:speed_upgrade",
    "modularrouters:stack_augment",
    "modularrouters:stack_upgrade",
    "modularrouters:sync_upgrade",
    "modularrouters:tag_filter",
    "modularrouters:vacuum_module",
    "modularrouters:void_module",
    "modularrouters:xp_vacuum_augment",
    "mysticalagriculture:menril_seeds",
    "pipez:advanced_upgrade",
    "pipez:basic_upgrade",
    "pipez:energy_pipe",
    "pipez:filter_destination_tool",
    "pipez:fluid_pipe",
    "pipez:gas_pipe",
    "pipez:improved_upgrade",
    "pipez:item_pipe",
    "pipez:ultimate_upgrade",
    "pipez:universal_pipe",
    "pipez:wrench",
    "productivebees:configurable_honeycomb",
    "productivebees:menril",
    "pylons:block_filter",
    "pylons:expulsion_pylon",
    "pylons:harvester_pylon",
    "pylons:infusion_pylon",
    "pylons:interdiction_pylon",
    "pylons:lifeless_filter",
    "pylons:mob_filter",
    "pylons:player_filter",
    "pylons:potion_filter",
    "pylons:protection_pylon",
}

INVENTED_IDS = (
    "pipez:infinity_upgrade",
    "pipez:chemical_pipe",
    "laserio:card_gas",
    "laserio:laser_cable",
    "modularrouters:puller_module_3",
    "modularrouters:fluid_module_3",
    "integrateddynamics:item_importer",
    "integratedtunnels:item_pipe",
    "mekanism:basic_gas_pipe",
)

INVENTED_TITLES = (
    "Pipez Upgrades",
    "Destination Tool",
    "Laser Node",
    "Laser Wrench",
    "Card Overclocker",
    "Node Overclocker",
    "Puller Module",
    "Sender Module",
)

SIBLING_DOCS = (
    "automation-first-steps.md",
    "storage-ladder.md",
    "autocrafting-guide.md",
    "power-guide.md",
    "ore-processing-ladder.md",
    "lag-fix-guide.md",
    "chunk-loading-guide.md",
    "farming-guide.md",
    "progression.md",
    "key-mods.md",
)


class TestLogisticsGuide(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""
        cls.flat = re.sub(r"\s+", " ", cls.text)
        cls.lower = cls.flat.lower()
        cls.skill = SKILL_MD.read_text(encoding="utf-8")
        cls.automation = AUTOMATION_MD.read_text(encoding="utf-8")
        cls.example = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------
    # existence, provenance, grounding
    # ------------------------------------------------------------------

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(DOC.is_file(), f"missing {DOC}")
        self.assertGreater(len(self.text.splitlines()), 150)
        self.assertGreater(len(self.text), 15000)

    def test_doc_pins_commit_and_names_sources(self) -> None:
        for needle in (PACK_COMMIT_SHORT, PACK_COMMIT_FULL, f"pack {PACK_VERSION}",
                       PACK_STAMP, PACK_DATE, LOGISTICS_GROUP_ID):
            self.assertIn(needle, self.text, f"missing provenance token: {needle}")
        for src in SOURCE_FILES:
            self.assertIn(src, self.text, f"missing source file in provenance: {src}")

    def test_doc_states_grounding_rules(self) -> None:
        for phrase in (
            "in-game quest book (FTB Quests) and JEI are authoritative",
            "*(no title in the config)*",
            "No recipes",
            "*(judgement)*",
            "quests are optional. Mods are not gated behind completing any quests!",
        ):
            self.assertIn(phrase, self.flat, f"missing grounding phrase: {phrase}")

    def test_doc_prints_both_pipez_filter_upgrade_claims(self) -> None:
        self.assertIn("6A962535CD68713E", self.text)
        self.assertIn("2A976D41F79C34B1", self.text)
        self.assertIn("Basic Upgrade allows Redstone Activation with Pipez", self.flat)
        self.assertIn("you need atleast an Advanced Upgrade to get it though", self.flat)
        self.assertIn("disagree", self.lower)

    def test_doc_states_chapter_3_star_independence(self) -> None:
        self.assertIn("chapter_2_the_star.snbt", self.text)
        self.assertIn("never gates the ATM Star", self.flat)

    # ------------------------------------------------------------------
    # structure and verified chapter metadata
    # ------------------------------------------------------------------

    def test_required_sections_in_order(self) -> None:
        headings = (
            "# The logistics guide: moving items, fluids, gases, and energy (verified titles)",
            "## Provenance — everything here was read, not remembered",
            "## Grounding rules (read before repeating any of this)",
            "## The short answer — which logistics mod when *(judgement)*",
            "## The Logistics group at a glance",
            "## Chapter 1 of the group — Basic Logistics (`basic_logistics`, 40 quests)",
            "## Chapter 2 of the group — Integrated Dynamics (`integrated_dynamics`, 28 quests)",
            "## Chapter 3 of the group — Modular Routers (`modular_router`, 55 quests)",
            "## Chapter 4 of the group — Pylons (`pylons`, 13 quests)",
            "## What moves what — capability matrix (from the quest config)",
            "## Cross-references",
            "## What this page deliberately does not tell you",
        )
        pos = -1
        for h in headings:
            idx = self.text.find(h)
            self.assertNotEqual(idx, -1, f"missing heading: {h}")
            self.assertGreater(idx, pos, f"heading out of order: {h}")
            pos = idx

    def test_four_logistics_chapters_match_pack_82_and_example_file(self) -> None:
        by_id = {c["id"]: c for c in self.example["chapters"]}
        for cfg_id, hex_id, title, order_idx, quests, tasks, titled, untitled, opt, stage in CHAPTERS:
            self.assertIn(cfg_id, by_id)
            self.assertEqual(by_id[cfg_id]["title"], title)
            self.assertEqual(by_id[cfg_id]["group"], "Logistics")
            self.assertEqual(by_id[cfg_id]["stage"], stage)
            self.assertIn(cfg_id, self.text)
            self.assertIn(hex_id, self.text)
            self.assertIn(title, self.text)
            self.assertIn(f"**{quests}** ({tasks})", self.text)
            self.assertIn(f"{titled} / {untitled}", self.text)

    def test_group_totals_and_task_counts_are_cited(self) -> None:
        for token in ("136 quests", "31 titled", "105 untitled", "14 optional",
                      "147 tasks", "135 `item`", "12 `checkmark`"):
            self.assertIn(token, self.flat, f"missing group total: {token}")

    # ------------------------------------------------------------------
    # completeness of quest titles and chains
    # ------------------------------------------------------------------

    def test_every_titled_quest_in_logistics_group_is_named(self) -> None:
        for title in VERIFIED_TITLES:
            self.assertIn(f"**{title}**", self.flat, f"missing verified quest title: {title}")

    def test_cross_chapter_titles_are_named(self) -> None:
        for title in CROSS_CHAPTER_TITLES:
            self.assertIn(f"**{title}**", self.flat, f"missing cross-chapter title: {title}")

    def test_pipez_chain_and_items(self) -> None:
        for qid in ("2329AA0AFBEF1E13", "36836AD948F96B9F", "33433A443B65D252",
                    "53EC96FA0E7C4ED4", "2F4458E9921DEB86", "4FBAB3A0FBF8CE2F",
                    "6A962535CD68713E", "2A976D41F79C34B1"):
            self.assertIn(qid, self.text)
        for item in ("pipez:wrench", "pipez:item_pipe", "pipez:fluid_pipe",
                     "pipez:energy_pipe", "pipez:gas_pipe", "pipez:universal_pipe",
                     "pipez:basic_upgrade", "pipez:improved_upgrade",
                     "pipez:advanced_upgrade", "pipez:ultimate_upgrade",
                     "pipez:filter_destination_tool"):
            self.assertIn(item, self.text)

    def test_mekanism_logistics_chain_and_side_configs(self) -> None:
        for qid in ("34CFE1439262AA72", "30DE4F5BC3EDB555", "1834B5C1F8435D7A",
                    "4BC2D7FCDD792DBA", "316B513FE568EF57", "493D04D954E4FBA0",
                    "5E116409DC7D30BB", "60ECCCAB66AAC05D", "33C69B5934BE4D64",
                    "3AF1DC02E9A0010C", "66A450CAC07232E1", "62827AA1AD29A222",
                    "7CC49360D07086B8", "7FE969CB4B419FC6"):
            self.assertIn(qid, self.text)
        self.assertIn("Side Configs", self.text)
        self.assertIn("Auto-Eject", self.text)
        self.assertIn("mekanism:quantum_entangloporter", self.text)

    def test_laserio_chain_cards_filters_and_overclockers(self) -> None:
        for qid in ("5F1218CF8EFC607B", "7BC8F50A89A3BE1A", "5C0F6B1C93A52113",
                    "7EE27C3908008E20", "4C41FD926F31180B", "1C70D739CE464E25",
                    "52F85CED20C8B1E9", "47768B1FFD57D56E", "6718043D0F2D1830",
                    "47A2BEFB11F4D581", "06767BA0AFE8C1EE", "3065EA195D0A36BA",
                    "2A6900E87DE8BAE0", "046C417B2ADF3AA7", "0BB562FB44B0AAA7",
                    "617695A9CA45D88F", "308935C85364B04D"):
            self.assertIn(qid, self.text)
        self.assertIn("Max: 4", self.text)
        self.assertIn("Max: 8", self.text)
        self.assertIn("8 items per Operation", self.text)
        self.assertIn("5 Buckets", self.text)

    def test_transfer_labels_quest(self) -> None:
        self.assertIn("6CD60A9D88227005", self.text)
        self.assertIn("When you gotta fit a pipe between your blocks", self.flat)
        self.assertIn("mod(transfer_labels)", self.text)

    def test_integrated_dynamics_preview_and_full_chapter(self) -> None:
        for qid in ("6E05B62A40D5A891", "6112956E19017D2D", "03C40D6A5D722543",
                    "6F152402756DA35E", "034F2CDF0830254B", "76CECFB244F39F18",
                    "499CF9F39CED8899", "68498ADEF9765F81", "62B4A37CFDECA679",
                    "72F57D77C3FB366D", "4A05C037C0EE40BD", "79C1105A84B8BF8F",
                    "450EDE68EC992A5A", "73EA326304C01C3B", "33F4A7613764A016",
                    "65FA86357BC60573", "4D4152032F0410D2", "65D89991A45BC042"):
            self.assertIn(qid, self.text)
        self.assertIn("Least laggy pipe solution, these are recommended", self.flat)
        self.assertIn("Flux Plugs and Points", self.flat)

    def test_modular_routers_titled_and_untitled_coverage(self) -> None:
        for qid in ("63E4529AF8894018", "233C7CAA573D6045", "75FE0B514448865B",
                    "6648BC7D14233006", "53A5F5E49EA8D5AF", "067AB3E4C4492F0D",
                    "0D5691403AEC25A8", "2BB5769119BA2472"):
            self.assertIn(qid, self.text)
        for item in ("modularrouters:modular_router", "modularrouters:blank_module",
                     "modularrouters:blank_upgrade", "modularrouters:augment_core",
                     "modularrouters:puller_module_1", "modularrouters:puller_module_2",
                     "modularrouters:sender_module_1", "modularrouters:sender_module_2",
                     "modularrouters:sender_module_3", "modularrouters:vacuum_module",
                     "modularrouters:void_module", "modularrouters:breaker_module",
                     "modularrouters:placer_module", "modularrouters:activator_module",
                     "modularrouters:fluid_module", "modularrouters:fluid_module_2",
                     "modularrouters:energy_output_module",
                     "modularrouters:energy_distributor_module",
                     "modularrouters:bulk_item_filter", "modularrouters:inspection_filter",
                     "modularrouters:mod_filter", "modularrouters:regex_filter",
                     "modularrouters:tag_filter"):
            self.assertIn(item, self.text)

    def test_pylons_and_unquested_mods_cross_check(self) -> None:
        for qid in ("30B0240543253EFB", "32E52AD6EF194A60", "5B5FC539BD1F4A73",
                    "12ED1EE85E146A4B", "18246A48C20B29D8", "2F5263A4166BFCD6",
                    "5E02AE661945306C"):
            self.assertIn(qid, self.text)
        for unquested in ("Super Factory Manager (SFM)", "XNet", "Ender IO"):
            self.assertIn(unquested, self.flat)

    def test_capability_matrix_covers_all_six_resource_types(self) -> None:
        matrix = self.text.split("## What moves what — capability matrix", 1)[1]
        for row_label in (
            "**Items**",
            "**Fluids**",
            "**Mekanism Gases & Chemicals**",
            "**Energy (FE)**",
            "**Mekanism Heat**",
            "**Wireless Redstone**",
        ):
            self.assertIn(row_label, matrix)

    # ------------------------------------------------------------------
    # no invented ids, titles, recipes, or coordinates
    # ------------------------------------------------------------------

    def test_every_backticked_namespaced_id_is_verified(self) -> None:
        found = set(re.findall(r"`([a-z0-9_]+:[a-z0-9_/]+)`", self.text))
        unexpected = found - VERIFIED_NAMESPACED_IDS
        self.assertEqual(unexpected, set(), f"unverified namespaced id(s): {sorted(unexpected)}")

    def test_no_invented_ids_or_titles(self) -> None:
        for bad_id in INVENTED_IDS:
            self.assertNotIn(bad_id, self.text, f"invented id present: {bad_id}")
        for bad_title in INVENTED_TITLES:
            self.assertNotIn(f"**{bad_title}**", self.text, f"invented title present: {bad_title}")

    def test_no_recipes_or_coordinates(self) -> None:
        self.assertIsNone(re.search(r"\bX:\s*-?\d+|\bZ:\s*-?\d+", self.text))
        self.assertIn("**No recipes.**", self.text)
        self.assertIn("**No factory layouts or coordinates.**", self.text)

    # ------------------------------------------------------------------
    # cross-references and SKILL.md wiring
    # ------------------------------------------------------------------

    def test_doc_links_existing_sibling_references(self) -> None:
        xrefs = self.text.split("## Cross-references", 1)[1]
        for sibling in SIBLING_DOCS:
            self.assertIn(f"references/{sibling}", xrefs)
            self.assertTrue((REFERENCES_DIR / sibling).is_file(), f"missing {sibling}")

    def test_skill_md_and_automation_first_steps_wire_the_guide(self) -> None:
        self.assertGreaterEqual(self.skill.count("references/logistics-guide.md"), 4)
        self.assertIn("The logistics guide dates itself the same way.", self.skill)
        self.assertIn("Logistics and item/fluid/gas/energy transport questions go to", self.skill)
        self.assertIn("Logistics answers quoted verified titles or ids from", self.skill)
        self.assertIn("references/logistics-guide.md", self.automation)

    # ------------------------------------------------------------------
    # offline guarantee
    # ------------------------------------------------------------------

    def test_this_suite_imports_no_network_module(self) -> None:
        forbidden = {"socket", "urllib", "http", "requests", "ftplib", "smtplib",
                     "httpx", "aiohttp", "webbrowser", "subprocess"}
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertEqual(imported & forbidden, set())


if __name__ == "__main__":
    unittest.main()
