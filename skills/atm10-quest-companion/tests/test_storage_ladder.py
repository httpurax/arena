#!/usr/bin/env python3
"""Offline tests for ``references/storage-ladder.md``.

Stdlib-only and network-free, like the rest of this suite: the document under test is a
local file, and every fact asserted here is either read from that file, from the shipped
``examples/progress.example.json``, or from a constant transcribed below.

The constants are the verified snapshot, read out of the official pack repository
``AllTheMods/ATM-10`` at ``main`` commit ``e5e3d1d83e`` (pack 8.2, 2026-09-22). The files
that supplied them are ``config/ftbquests/quests`` (the four Storage-group chapter files,
their ``en_us`` lang files, ``chapter_groups.snbt``) and
``config/crash_assistant/modlist.json`` - the same snapshot the document cites. Nothing
here is fetched at test time; the offline guarantee at the bottom of this file enforces it.

Covered:

  * the document exists, is not a stub, and carries the skill's grounding rules (in-game
    quest book + JEI authoritative, uncertain details flagged approximate, nothing
    invented, no recipes) plus its provenance block (pinned commit, pack 8.2 / 8.x, the
    pack files it was read from);
  * structure: the H1, the required section headings, and the ``(no title in the config)``
    marker that keeps untitled quests from being given derived names;
  * the verified pack data: the four chapters' ids, titles, ``order_index`` values, quest
    counts, titled/untitled split, ``optional`` counts, and task-type counts;
  * completeness: every one of the 165 titled quests in those four chapters is named in
    the document, and every bold quest name in it is a verified title or known prose -
    no invented titles;
  * no invented ids: every backticked ``namespace:path`` in the document is one of the ids
    verified in the pack config at that commit;
  * the ladders: each tier chain appears in the config's dependency order, by item id -
    Sophisticated Storage chests, Sophisticated Backpacks, Functional Storage capacity
    upgrades, the Refined Storage item and fluid disk ladders (including the Extra Disks
    gate), and the AE2 storage-component ladder crossing into MEGA Cells;
  * the grounded quotes that carry the "when to upgrade" advice survive editing intact;
  * cross-references: the sibling reference docs, and the four chapter ids matching the
    shipped example file (group ``Storage``, stages ``early-game`` / ``tech``);
  * ``SKILL.md`` documents the new reference document;
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
DOC = SKILL_ROOT / "references" / "storage-ladder.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"
PROGRESSION_MD = SKILL_ROOT / "references" / "progression.md"
KEY_MODS_MD = SKILL_ROOT / "references" / "key-mods.md"
STAR_CHECKLIST_MD = SKILL_ROOT / "references" / "atm-star-checklist.md"
CREATIVE_CHECKLIST_MD = SKILL_ROOT / "references" / "creative-checklist.md"
BOSS_CHECKLIST_MD = SKILL_ROOT / "references" / "boss-checklist.md"

# --------------------------------------------------------------------------------------
# the verified snapshot: AllTheMods/ATM-10 @ e5e3d1d83e (pack 8.2)
# --------------------------------------------------------------------------------------

PACK_COMMIT = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
PACK_COMMIT_SHORT = "e5e3d1d83e"
PACK_VERSION = "8.2"
PACK_VERSION_STAMP = "8.x"

# The pack files the document must name as its sources (same list the endgame docs use,
# plus the two the Storage group needs on top of them).
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
    "chapter_groups.snbt",
    "config/ftbquests/quests/chapters/chapter_2_the_star.snbt",
)

STORAGE_GROUP_ID = "1AC60211DE7427FC"
STORAGE_GROUP_TITLE = "Storage"

# (identifier, chapter id, verified chapter title, order_index, quests, titled, untitled,
#  optional quests) - straight out of the four chapter files and their lang files.
CHAPTERS = (
    ("storage", "1DB294A8F8686321", "Basic Storage", 0, 90, 40, 50, 44),
    ("refined_storage", "15AAF17B6665223D", "Refined Storage", 2, 72, 52, 20, 5),
    ("applied_energistics_2", "07210DDF872160BA", "Applied Energistics 2", 1, 74, 42, 32, 4),
    ("extended__advanced_ae", "51A2FE60D8B76FC6", "Extended \\& Advanced AE", 2, 56, 31, 25, 3),
)
TOTAL_QUESTS = 292
TOTAL_TITLED = 165
TOTAL_UNTITLED = 127
TOTAL_TASKS = 351
ITEM_TASKS = 338
CHECKMARK_TASKS = 11
# one `advancement` task (ae2:main/presses) and one `observation` task (entro budding).
OTHER_TASK_TYPES = ("advancement", "observation")
PROGRESSION_MODE = "flexible"

UNTITLED_MARKER = "(no title in the config)"

# @@CONSTANTS-START@@
# Every quest title the four chapters' lang files give, at the pinned commit. The doc
# must name all of them: a title the doc drops is a rung a player cannot look up.
VERIFIED_TITLES = (
    "Iron Chest", "Gold Chest", "Diamond Chest", "Netherite Chest", "Sophisticated Storage",
    "Basic Storage", "Trash Cans", "Dimensional Storage", "Functional Storage",
    "Sophisticated Backpacks", "Copper Backpack", "Advanced Pickup Upgrade",
    "Advanced Filter Upgrade", "Advanced Magnet Upgrade", "Advanced Feeding Upgrade",
    "Advanced Compacting Upgrade", "Advanced Void Upgrade", "Advanced Restock Upgrade",
    "Advanced Deposit Upgrade", "Auto-Smelting Upgrade", "Auto-Smoking Upgrade",
    "Auto-Blasting Upgrade", "Stack Upgrade Tier 1", "Stack Upgrade Tier 2",
    "Stack Upgrade Tier 3", "Stack Upgrade Tier 4", "Advanced Tool Swapper Upgrade",
    "Advanced Pump Upgrade", "Experience Pump Upgrade", "Iron Backpack", "Gold Backpack",
    "Diamond Backpack", "Copper Upgrade", "Gold Upgrade", "Diamond Upgrade",
    "Netherite Upgrade", "Netherite Backpack", "Vanilla Storage", "Copper Chest",
    "Advanced Refill Upgrade", "Refined Storage", "1k Storage Part", "4k Storage Part",
    "16k Storage Part", "64k Storage Part", "65536k Storage Part", "256k Storage Part",
    "1024k Storage Part", "4096k Storage Part", "16384k Storage Part", "262m Storage Part",
    "1048m Storage Part", "Advanced Storage Housing", "Autocrafter", "Ultra Autocrafter",
    "Mega Autocrafter", "Cables", "Ultra Importer", "Ultra Destructor", "Ultra Constructor",
    "Ultra Exporter", "64B Fluid Storage Part", "256B Fluid Storage Part",
    "1024B Fluid Storage Part", "4096B Fluid Storage Part", "16384B Fluid Storage Part",
    "65536B Fluid Storage Part", "262kB Fluid Storage Part", "1048kB Fluid Storage Part",
    "Security Manager", "The Grid", "The Better Grid", "Pattern Grid", "Autocrafting",
    "Wireless Access", "Grid Networks", "Destructor Upgrades", "Speeding Everything Up!",
    "Increasing Wifi Range", "Regulator Upgrade", "Monitoring Autocrafting", "Wrench",
    "Managing Autocrafters", "Mega Constructor", "Mega Destructor", "Mega Importer",
    "Mega Exporter", "Interdimensional Wireless Transmitter", "Other Storage Parts",
    "Wireless Universal Grid", "Ultra Disk Interface", "Mega Disk Interface",
    "Applied Energistics 2", "First Things First", "Meteorite hunting", "Processors",
    "Fluix", "Basic Cabling", "Advanced Cabling", "Terminals", "The Storage", "The IO",
    "Auto-Crafting", "Quartz Wrench", "Network Tools", "Creating your first Storage Cell",
    "4k Storage Component", "16k Storage Component", "64k Storage Component",
    "256k Storage Component", "1M Storage Component", "4M Storage Component",
    "16M Storage Component", "64M Storage Component", "256M Storage Component",
    "Item Storage", "P2P Tunnels", "Forgot to Mention", "Patterns", "ME Level Emitter",
    "Redstone-Controlled ME", "Spatial IO", "Spatial Storage Cell", "Cable Anchor",
    "Color Applicator", "The... Weapons?", "Condensed Matter", "Wireless Terminals",
    "Infinity Booster", "Hyper-Condensed Matter", "Loosely Speaking",
    "Quantum Network Bridge", "Bulk Item Storage", "Certus Quartz", "ExtendedAE",
    "The Crystals of Space and Time: Entro Crystals",
    "Complex Crafter: The Crystal Assembler", "Faster and Bigger: Extended Devices",
    "Blocks to Circuits: The Circuit Slicer",
    "Connections across long distances: The Wireless Connector",
    "More Resources than you ever need: Infinity Cells",
    "Better Pattern Access: The Extended Pattern Access Terminal",
    "Can this Liquid: The ME Canner", "Many Assemblers In One: The Assembler Matrix",
    "Advanced AE", "Reaction Efficency: The Reaction Chamber",
    "Specific Sided Patterns: The Advanced Pattern Provider",
    "Infinite Crafting Jobs: The Quantum Computer", "Assembler Matrix Cores",
    "Massive Crafting Storage: The Quantum Computer Storage",
    "Co-Processing Oblivion: Quantum Computer Accelerator",
    "Heart of the Crafts: Quantum Computer Core",
    "Co-Processing To Infinity: Quantum Computer Multi-Threader",
    "Unnecessarily Large Storage: Quantum Data Entangler",
    "Fully Automated Crafting: The Quantum Crafter",
    "ME System As Armor: The Quantum Armor", "Upgrades for Quantum Armor",
    "Automating Entro Crystals", "Quantum Ingredients",
    "Matter Condenser in a Cell: The Void Cell",
    "Get-Yer-Crystals-Fixed: The Crystal Fixer", "Extended \\& Advanced AE",
    "Branches of Connections: The Wireless Hub",
    "Actively Placing From The Network: The Active Formation Plane",
    "The Ultimate Quantum Computer",
)

# Subtitles the config gives untitled quests; the doc quotes these as the book shows
# them, so they count as verified names too.
VERIFIED_SUBTITLES = (
    "\"I wonder what's in here?\"", "\"Vanilla Chest\"",
    "'COMIC #42: shearching 4 bobby [Fischer]'", "'S.M.R.T.'", "+10 Strength", "+2 Luck",
    "+20 Max HP", "+30% Evasion Chance", "+5 Attack Speed",
    "Adds a filter for items you want to auto-delete in the backpack.", "All Stocked up",
    "Allows the backpack to pick up items.", "Auto Compacts/Decompacts",
    "Automated crafting!", "Automatic", "Automation in upgrade form!",
    "Backpacks in your Backpacks?", "Better Signal", "Breaking Blocks!", "Bulk and cut",
    "Cell Workbench Wherever You Go", "Connecting the System", "Creative Flight",
    "Cut out the middleman", "Defragmentation", "Dimensional Drawer...",
    "Does exactly what you'd expect", "Don't go off the Grid", "Download more CPU cores",
    "Download more RAM", "Download more VRAM", "Exporting Items!", "First Things First",
    "Floppy Time!", "Follow the Pattern", "For more accuracy",
    "For when you can't deal with decay", "GET IN", "GET OUT", "GET OUT: Active Edition",
    "Getting Rid of The Excess", "Hyper-Condensed Matter",
    "I'm not writing the Toy Story line", "Importing Items!", "Inventories are too Small",
    "Iron Chests?", "Items as a file system", "Looking at you, Mekanism",
    "ME Storage Cells Drawers",
    "Many Molecular Assemblers and Pattern Providers in One Channel",
    "More Filtering Options", "No Flight Drift", "No more Manipulation!",
    "Now we're jammin", "OI, OI, OI!", "On-The-Go Grid", "Order up", "Placing Blocks!",
    "Plug in", "Secure your Grid!", "So much room for activities!", "Stacks on Stacks",
    "Storage Drawers Distant Relative", "Storing XP", "TLDR: Good Wifi", "The 21st Century",
    "The Base for Upgrades", "The Brain of the Drawers", "The Chest", "The First Upgrade",
    "The I", "The O", "The Sink but in cell form", "The first MEGAbyte.",
    "The first kilobyte.", "The remaining two IO cards", "The spare chest",
    "This has a use outside of crafting cables.", "This is what you're here for",
    "Too hot for the ATF", "Under the knife", "Up to +3 Jump Height",
    "Up to +3 Step Height", "Up to +5 Reach", "Version 2", "Virtual Storage System",
    "Wirelessly Connecting Networks", "Won't make you fully invincible",
    "You spin me right round'", "[Linux user joke goes here]",
    "not to be confused with the me caner", "not to be confused with time crystals",
    "x16 Storage Upgrade", "x24 Storage Upgrade", "x32 Storage Upgrade", "x4", "x4^2",
    "x4^3", "x4^4", "x8 Storage Upgrade",
)

# Every `namespace:path` the doc puts in backticks, each one verified to occur in the
# pack config at the pinned commit (chapter files, lang files, modlist). Adding an id
# to the doc without verifying it there fails test_every_backticked_id_is_verified.
# Categories: task items, smart-filter contents, item tags (`c:chests`), quest icons,
# advancement ids, reward items, and the chapters' canvas `images` paths.
VERIFIED_ITEM_IDS = (
    "advanced_ae:adv_pattern_encoder", "advanced_ae:adv_pattern_provider",
    "advanced_ae:data_entangler", "advanced_ae:quantum_accelerator",
    "advanced_ae:quantum_alloy", "advanced_ae:quantum_core", "advanced_ae:quantum_crafter",
    "advanced_ae:quantum_helmet", "advanced_ae:quantum_multi_threader",
    "advanced_ae:quantum_processor", "advanced_ae:quantum_storage_128",
    "advanced_ae:quantum_storage_256", "advanced_ae:quantum_structure",
    "advanced_ae:quantum_unit", "advanced_ae:quantum_upgrade_base",
    "advanced_ae:reaction_chamber", "advanced_ae:shattered_singularity",
    "ae2:1k_crafting_storage", "ae2:256k_crafting_storage", "ae2:annihilation_plane",
    "ae2:blank_pattern", "ae2:block/controller_lights", "ae2:cable_anchor",
    "ae2:calculation_processor", "ae2:capacity_card", "ae2:cell_component_16k",
    "ae2:cell_component_1k", "ae2:cell_component_256k", "ae2:cell_component_4k",
    "ae2:cell_component_64k", "ae2:cell_workbench", "ae2:certus_quartz_crystal",
    "ae2:charged_staff", "ae2:charger", "ae2:chest", "ae2:color_applicator",
    "ae2:condenser", "ae2:controller", "ae2:covered_cable", "ae2:covered_dense_cable",
    "ae2:crafting_accelerator", "ae2:crafting_card", "ae2:crafting_monitor",
    "ae2:creative_energy_cell", "ae2:dense_energy_cell", "ae2:drive", "ae2:ender_dust",
    "ae2:energy_acceptor", "ae2:energy_card", "ae2:energy_cell",
    "ae2:engineering_processor", "ae2:entropy_manipulator", "ae2:equal_distribution_card",
    "ae2:export_bus", "ae2:fluid_storage_cell_1k", "ae2:fluix_block", "ae2:fluix_crystal",
    "ae2:fluix_dust", "ae2:formation_plane", "ae2:fuzzy_card", "ae2:glass_cable",
    "ae2:growth_accelerator", "ae2:import_bus", "ae2:inscriber", "ae2:interface",
    "ae2:inverter_card", "ae2:io_port", "ae2:item_storage_cell_1k", "ae2:knife",
    "ae2:level_emitter", "ae2:logic_processor", "ae2:main/presses", "ae2:matter_ball",
    "ae2:matter_cannon", "ae2:me_p2p_tunnel", "ae2:memory_card", "ae2:meteorite_compass",
    "ae2:molecular_assembler", "ae2:name_press", "ae2:network_tool",
    "ae2:pattern_access_terminal", "ae2:pattern_encoding_terminal", "ae2:pattern_provider",
    "ae2:quantum_entangled_singularity", "ae2:quantum_link", "ae2:quantum_ring",
    "ae2:quartz_cluster", "ae2:quartz_fiber", "ae2:quartz_wrench", "ae2:redstone_card",
    "ae2:singularity", "ae2:smart_cable", "ae2:smart_dense_cable", "ae2:spatial_anchor",
    "ae2:spatial_io_port", "ae2:spatial_pylon", "ae2:spatial_storage_cell_2",
    "ae2:speed_card", "ae2:storage_bus", "ae2:tiny_tnt", "ae2:toggle_bus", "ae2:void_card",
    "ae2:wireless_access_point", "ae2:wireless_booster", "ae2:wireless_crafting_terminal",
    "ae2:wireless_terminal", "ae2wtlib:quantum_bridge_card",
    "ae2wtlib:wireless_universal_terminal", "aeinfinitybooster:dimension_card",
    "aeinfinitybooster:infinity_card", "allthetweaks:item/atm_star",
    "ars_nouveau:archwood_chest", "ars_nouveau:dowsing_rod",
    "atm:textures/questpics/storage/functional1.png", "c:chests",
    "cabletiers:elite_autocrafter", "cabletiers:elite_constructor",
    "cabletiers:elite_destructor", "cabletiers:elite_disk_interface",
    "cabletiers:elite_exporter", "cabletiers:elite_importer",
    "dimstorage:dimensional_chest", "dimstorage:dimensional_tank",
    "extendedae:active_formation_plane", "extendedae:assembler_matrix_frame",
    "extendedae:assembler_matrix_pattern", "extendedae:caner", "extendedae:circuit_cutter",
    "extendedae:crystal_assembler", "extendedae:crystal_fixer",
    "extendedae:entro_budding_fully", "extendedae:entro_crystal", "extendedae:entro_seed",
    "extendedae:ex_pattern_access_part", "extendedae:infinity_cobblestone_cell",
    "extendedae:infinity_water_cell", "extendedae:void_cell", "extendedae:wireless_connect",
    "extendedae:wireless_hub", "extendedae:wireless_tool",
    "extradisks:1024k_item_storage_part", "extradisks:1048576k_item_storage_part",
    "extradisks:16384b_fluid_storage_part", "extradisks:16384k_item_storage_part",
    "extradisks:256k_item_storage_part", "extradisks:262144k_item_storage_part",
    "extradisks:4096k_item_storage_part", "extradisks:65536k_item_storage_part",
    "extradisks:advanced_storage_housing", "ftbquests:custom_icon",
    "functionalstorage:collector_upgrade", "functionalstorage:compacting_drawer",
    "functionalstorage:configuration_tool", "functionalstorage:controller_extension",
    "functionalstorage:copper_upgrade", "functionalstorage:diamond_upgrade",
    "functionalstorage:drawer", "functionalstorage:ender_drawer",
    "functionalstorage:fluid_1", "functionalstorage:framed_storage_controller",
    "functionalstorage:gold_upgrade", "functionalstorage:iron_downgrade",
    "functionalstorage:linking_tool", "functionalstorage:netherite_upgrade",
    "functionalstorage:oak_4", "functionalstorage:puller_upgrade",
    "functionalstorage:pusher_upgrade", "functionalstorage:redstone_upgrade",
    "functionalstorage:simple_compacting_drawer", "functionalstorage:storage_controller",
    "functionalstorage:void_upgrade", "https://allthemods.github.io/alltheguides/mods/ae2/",
    "integratedterminals:terminal_storage_portable",
    "interdimensionalwirelesstransmitter:interdimensional_wireless_transmitter",
    "laserio:card_holder", "megacells:bulk_item_cell", "megacells:cell_component_16m",
    "megacells:cell_component_1m", "megacells:cell_component_256m",
    "megacells:cell_component_4m", "megacells:cell_component_64m",
    "megacells:portable_item_cell_256m", "minecraft:barrel", "minecraft:chest",
    "minecraft:chest_boats", "minecraft:chest_minecart", "minecraft:copper_ingot",
    "minecraft:enchanted_book", "minecraft:ender_chest", "minecraft:trapped_chest",
    "modern_industrialization:blastproof_casing", "mysticalagriculture:entro_seeds",
    "pipez:item_pipe", "pocketstorage:psu_1", "pocketstorage:psu_4",
    "productivebees:bee_type", "productivebees:entro", "refinedstorage:16k_storage_part",
    "refinedstorage:1k_storage_part", "refinedstorage:4k_storage_part",
    "refinedstorage:64b_fluid_storage_part", "refinedstorage:64k_storage_part",
    "refinedstorage:autocrafter", "refinedstorage:autocrafter_manager",
    "refinedstorage:autocrafting_monitor", "refinedstorage:autocrafting_upgrade",
    "refinedstorage:cable", "refinedstorage:constructor", "refinedstorage:controller",
    "refinedstorage:crafting_grid", "refinedstorage:creative_portable_grid",
    "refinedstorage:destructor", "refinedstorage:disk_drive",
    "refinedstorage:disk_interface", "refinedstorage:exporter",
    "refinedstorage:external_storage", "refinedstorage:grid", "refinedstorage:importer",
    "refinedstorage:network_receiver", "refinedstorage:network_transmitter",
    "refinedstorage:pattern", "refinedstorage:pattern_grid", "refinedstorage:portable_grid",
    "refinedstorage:range_upgrade", "refinedstorage:regulator_upgrade",
    "refinedstorage:security_manager", "refinedstorage:silk_touch_upgrade",
    "refinedstorage:speed_upgrade", "refinedstorage:stack_upgrade",
    "refinedstorage:storage_housing", "refinedstorage:storage_monitor",
    "refinedstorage:wireless_autocrafting_monitor", "refinedstorage:wireless_grid",
    "refinedstorage:wireless_transmitter", "refinedstorage:wrench",
    "refinedstorage_mekanism_integration:64b_chemical_storage_part",
    "refinedstorage_quartz_arsenal:wireless_crafting_grid",
    "refinedtypes:1k_soul_storage_part", "refinedtypes:64b_source_storage_part",
    "refinedtypes:64k_energy_storage_part", "sophisticatedbackpacks:backpack",
    "sophisticatedbackpacks:chipped/botanist_workbench_upgrade",
    "sophisticatedbackpacks:copper_backpack", "sophisticatedbackpacks:diamond_backpack",
    "sophisticatedbackpacks:gold_backpack", "sophisticatedbackpacks:iron_backpack",
    "sophisticatedbackpacks:netherite_backpack", "sophisticatedbackpacks:upgrade_base",
    "sophisticatedstorage:base_tier_wooden_storage",
    "sophisticatedstorage:basic_to_copper_tier_upgrade",
    "sophisticatedstorage:basic_to_iron_tier_upgrade", "sophisticatedstorage:controller",
    "sophisticatedstorage:diamond_to_netherite_tier_upgrade",
    "sophisticatedstorage:gold_to_diamond_tier_upgrade",
    "sophisticatedstorage:iron_to_gold_tier_upgrade",
    "sophisticatedstorage:item/packing_tape", "sophisticatedstorage:storage_link",
    "sophisticatedstorage:storage_tool", "sophisticatedstorage:upgrade_base",
    "trashcans:energy_trash_can", "trashcans:item_trash_can", "trashcans:liquid_trash_can",
    "trashcans:ultimate_trash_can", "universalgrid:wireless_universal_grid",
)

# Other verified names from the same snapshot: every chapter title in the book and
# every chapter-group title. The doc names chapters outside the Storage group when it
# cross-references them, and those names are the config's too.
OTHER_VERIFIED_NAMES = (
    "Apotheosis Gear", "Apothic Enchanting", "Apothic Spawners", "Applied Energistics 2",
    "Ars Nouveau", "Artifacts", "Auroral", "Basic Armor", "Basic Logistics", "Basic Power",
    "Basic Storage", "Basic Tools", "Bounty Board", "Building Tips", "Cataclysm",
    "Chapter 1: The Beginning", "Chapter 2: Allthemodium", "Chapter 3: The ATM Star",
    "Chapter 4: Creative", "Create", "Deeper and Darker", "Digital Age",
    "Draconic Evolution", "Electric Age: No more rookie", "End Game", "Eternal Starlight",
    "EvilCraft", "Exploration", "Extended \\& Advanced AE", "Extreme Reactors",
    "Food and Farming", "Forbidden \\& Arcanus", "Generators N Furnaces",
    "Hostile Neural Networks", "Ice and Fire", "Immersive Engineering",
    "Industrial Foregoing", "Integrated Dynamics", "Iron's Spells 'n Spellbooks",
    "Just Dire Things", "Logistics", "Magic", "Mahou Tsukai", "Main Questline", "Mekanism",
    "Mekanism: Reactors", "Modern Industrialization", "Modular Routers",
    "Mystical Agriculture", "Nature's Aura", "Neo Vitae", "Occultism", "Oritech",
    "PneumaticCraft", "Powah", "Power", "Productive Bees", "Productive Trees", "Pylons",
    "RailCraft", "Refined Storage", "Relics", "Resources", "Silent Gear",
    "Steam Age: New Beginnings", "Storage", "Tech", "The Aether", "The Bumblezone",
    "The Twilight Forest", "The Undergarden", "Theurgy", "Tips and Tricks",
    "Tools and Gear", "Welcome", "XyCraft",
)

# Bold spans in the doc that are prose, not quest names: rule headings, counts, and
# emphasis inside sentences. Anything bold that is NOT here and is not a verified
# title/subtitle/chapter name/modlist name fails test_no_bold_span_invents_a_quest_name.
BOLD_PROSE_ALLOWLIST = (
    "\"When to move up\" is either quoted or it is this skill's reading.",
    "23 quests hanging directly off it", "41 upgrade quests in total", "72", "74", "90",
    "Addon depth differs, and both are deep.", "All the Mods 10",
    "An order the book does not have.", "Anything not in the config.",
    "Both are full chapters in the same group",
    "Energy costs, channel budgets for a given build, throughput, or lag advice.",
    "Every number in quotation marks is quest text, not a measured fact.",
    "Item ids and counts below are quoted from the config, never invented.",
    "Logistics group", "No recipes.",
    "Nothing here was invented, and nothing is added from memory.",
    "Pocket Storage is the star's other storage ask", "Recipes.",
    "Rung numbers are this skill's reading, not the book's.",
    "Rungs 2a and 2b are alternatives, not steps.",
    "Slot counts for backpacks, chests, and drawers.", "Stay on rung 1",
    "The ATM Star line is AE2-family.",
    "The book lays chapters out on a canvas, not as a numbered list.",
    "The in-game quest book (FTB Quests) and JEI are authoritative.",
    "Titles are the config's.", "What the chapter says the mod is for",
    "What this page is.", "Which mod is better.",
    "`…` inside a quote marks an elision or a paragraph break in the config's own text",
    "advancement", "dependency order", "expanding the possibilities of end game systems",
    "from as early as you want to the very endgame", "observation", "pack 8.2",
)

# Modlist display names the doc bolds (config/crash_assistant/modlist.json).
MODLIST_NAMES = (
    "Advanced AE", "Applied Energistics 2", "ExtendedAE", "Functional Storage",
    "Industrial Foregoing", "Interdimensional Wireless Transmitter", "Refined Storage",
    "Sophisticated Backpacks", "Sophisticated Backpacks Create Integration",
    "Sophisticated Storage", "Sophisticated Storage In Motion", "Storage Delight",
    "Trash Cans",
)

# The tier chains, in the config's own dependency order, by task item id (or, for the
# Refined Storage fluid ladder, by verified quest title).
SOPHISTICATED_STORAGE_LADDER = (
    "sophisticatedstorage:base_tier_wooden_storage", "sophisticatedstorage:copper_chest",
    "sophisticatedstorage:iron_chest", "sophisticatedstorage:gold_chest",
    "sophisticatedstorage:diamond_chest", "sophisticatedstorage:netherite_chest",
)

SOPHISTICATED_BACKPACKS_LADDER = (
    "sophisticatedbackpacks:backpack", "sophisticatedbackpacks:copper_backpack",
    "sophisticatedbackpacks:iron_backpack", "sophisticatedbackpacks:gold_backpack",
    "sophisticatedbackpacks:diamond_backpack", "sophisticatedbackpacks:netherite_backpack",
)

FUNCTIONAL_STORAGE_UPGRADES = (
    "functionalstorage:copper_upgrade", "functionalstorage:gold_upgrade",
    "functionalstorage:diamond_upgrade", "functionalstorage:netherite_upgrade",
)

REFINED_STORAGE_ITEM_PARTS = (
    "refinedstorage:1k_storage_part", "refinedstorage:4k_storage_part",
    "refinedstorage:16k_storage_part", "refinedstorage:64k_storage_part",
    "extradisks:advanced_storage_housing", "extradisks:256k_item_storage_part",
    "extradisks:1024k_item_storage_part", "extradisks:4096k_item_storage_part",
    "extradisks:16384k_item_storage_part", "extradisks:65536k_item_storage_part",
    "extradisks:262144k_item_storage_part", "extradisks:1048576k_item_storage_part",
)

REFINED_STORAGE_FLUID_PARTS = (
    "64B Fluid Storage Part", "256B Fluid Storage Part", "1024B Fluid Storage Part",
    "4096B Fluid Storage Part", "16384B Fluid Storage Part", "65536B Fluid Storage Part",
    "262kB Fluid Storage Part", "1048kB Fluid Storage Part",
)

AE2_STORAGE_COMPONENTS = (
    "ae2:cell_component_1k", "ae2:cell_component_4k", "ae2:cell_component_16k",
    "ae2:cell_component_64k", "ae2:cell_component_256k", "megacells:cell_component_1m",
    "megacells:cell_component_4m", "megacells:cell_component_16m",
    "megacells:cell_component_64m", "megacells:cell_component_256m",
)

CABLE_TIERS_ITEMS = (
    "cabletiers:elite_importer", "cabletiers:elite_exporter",
    "cabletiers:elite_constructor", "cabletiers:elite_destructor",
    "cabletiers:elite_disk_interface", "cabletiers:elite_autocrafter",
)

CABLE_TIERS_TITLES = (
    "Ultra Importer", "Mega Importer", "Ultra Exporter", "Mega Exporter",
    "Ultra Constructor", "Mega Constructor", "Ultra Destructor", "Mega Destructor",
    "Ultra Disk Interface", "Mega Disk Interface", "Ultra Autocrafter", "Mega Autocrafter",
)

# Quotes that carry the doc's "when to upgrade" advice. Each one was checked
# against the pack's own en_us lang files at the pinned commit.
KEY_QUOTES = (
    "it is best to store them in Chests or Bags!",
    "If you can't make drives and have a bunch of chests everywhere, this is your best "
    "bet in creating a storage network!",
    "from as early as you want to the very endgame",
    "It is also an ingredient for the ATM Star.",
    "Increases stack size in the Backpack by 2", "Inventories are too Small",
    "all of the basic ways to store items without needing power",
    "There comes a point in any playthrough of a large modpack where even the highest "
    "standard tier of storage cell doesn't cut it",
    "In this modpack, quests are optional. Mods are not gated behind completing any quests!",
    "upgrade your Chests and Barrels with metals to increase their storage",
)
# @@CONSTANTS-END@@


def normalize(text: str) -> str:
    """Collapse whitespace so a title split across two wrapped lines still matches."""
    return re.sub(r"\s+", " ", text).strip()


class TestStorageLadderDoc(unittest.TestCase):
    """Existence, grounding, provenance, and structure."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = normalize(cls.text)
        cls.lowered = cls.text.lower()

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(DOC.is_file(), f"missing {DOC}")
        self.assertGreater(len(self.text.strip()), 2000, "storage-ladder.md looks like a stub")

    def test_doc_is_grounded_like_the_other_reference_docs(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lowered,
                          f"storage-ladder.md must state the {needle!r} rule")
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.lowered,
                          f"storage-ladder.md must name its source: {source}")
        self.assertIn(PACK_VERSION, self.text,
                      "the doc must date itself against the pack version it was read from")
        self.assertIn(PACK_VERSION_STAMP, self.text,
                      "the doc must tie that version to the skill's 8.x stamp")
        self.assertRegex(self.lowered, r"never invented|not invented|never invent",
                         "the doc must say its details were read, not invented")

    def test_doc_pins_the_commit_it_was_read_from(self) -> None:
        self.assertIn(PACK_COMMIT, self.text,
                      "the doc must pin the full commit it was read from")
        self.assertIn(PACK_COMMIT_SHORT, self.text)
        self.assertIn("2026-09-22", self.text, "the doc must date the snapshot")

    def test_doc_has_the_house_structure(self) -> None:
        self.assertTrue(self.text.startswith("# "), "the doc must start with an H1")
        headings = [normalize(line[3:]) for line in self.text.splitlines()
                    if line.startswith("## ")]
        for required in (
            "Provenance — everything here was read, not remembered",
            "Grounding rules (read before repeating any of this)",
            "The ladder at a glance",
            "Rung 1 — Basic Storage (`storage`, 90 quests)",
            "Rung 2a — Refined Storage (`refined_storage`, 72 quests)",
            "Rung 2b — Applied Energistics 2 (`applied_energistics_2`, 74 quests)",
            "Rung 3 — Extended \\& Advanced AE (`extended__advanced_ae`, 56 quests)",
            "When to upgrade — the pack's own signals",
            "Which one: Refined Storage or AE2",
            "Cross-references",
            "What this page deliberately does not tell you",
        ):
            self.assertIn(required, headings, f"missing section: {required}")
        # The four rungs must appear in the order the doc's own ladder claims.
        order = [headings.index(h) for h in headings if h.startswith("Rung ")]
        self.assertEqual(order, sorted(order), "the rung sections are out of ladder order")

    def test_doc_marks_untitled_quests_instead_of_naming_them(self) -> None:
        count = self.text.count(UNTITLED_MARKER)
        self.assertGreaterEqual(
            count, 35,
            "127 of the 292 quests carry no title; wherever the doc discusses one it must "
            f"use the marker, not a derived name (found {count} uses)")
        self.assertIn("never present a derived name as a verified title", self.lowered)

    def test_doc_refuses_recipes_and_invented_numbers(self) -> None:
        for needle in ("no recipes", "recipes.", "jei has the recipe"):
            self.assertIn(needle, self.lowered)
        self.assertIn("quest text, not a measured fact", self.lowered,
                      "quoted numbers must be labelled as the quests' own words")


class TestVerifiedChapterData(unittest.TestCase):
    """The chapter-level facts the doc states must match the pinned config."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = normalize(cls.text)

    def test_every_chapter_id_and_title_is_cited(self) -> None:
        self.assertIn(STORAGE_GROUP_ID, self.text)
        for identifier, chapter_id, title, _order, *_rest in CHAPTERS:
            self.assertIn(chapter_id, self.text, f"missing chapter id for {identifier}")
            self.assertIn(f"`{identifier}`", self.text, f"missing config id `{identifier}`")
            self.assertIn(normalize(title), self.flat, f"missing chapter title {title}")

    def test_quest_counts_are_cited(self) -> None:
        for identifier, _cid, _title, _order, quests, *_rest in CHAPTERS:
            self.assertIn(f"`{identifier}`, {quests} quests", self.text,
                          f"the doc must state {identifier}'s {quests} quests")
        self.assertIn(str(TOTAL_QUESTS), self.text, "the doc must total the group's quests")

    def test_titled_and_untitled_split_is_cited(self) -> None:
        self.assertIn(str(TOTAL_TITLED), self.text)
        self.assertIn(str(TOTAL_UNTITLED), self.text)
        for _identifier, _cid, _title, _order, _quests, titled, untitled, _opt in CHAPTERS:
            self.assertIn(f"{titled} / {untitled}", self.text,
                          "the at-a-glance table must give each chapter's titled/untitled split")

    def test_task_counts_are_cited(self) -> None:
        self.assertIn(str(TOTAL_TASKS), self.text)
        self.assertIn(str(ITEM_TASKS), self.text)
        self.assertIn(str(CHECKMARK_TASKS), self.text)
        for task_type in OTHER_TASK_TYPES:
            self.assertIn(task_type, self.text,
                          f"the doc must mention the chapter group's one {task_type} task")

    def test_optional_counts_are_cited(self) -> None:
        for _identifier, _cid, _title, _order, _quests, _titled, _untitled, optional in CHAPTERS:
            self.assertIn(f"| {optional} |", self.text,
                          "the at-a-glance table must give each chapter's optional count")

    def test_order_index_and_progression_mode_are_cited(self) -> None:
        self.assertIn(PROGRESSION_MODE, self.text)
        self.assertIn("`order_index`", self.text)
        for identifier, _cid, _title, order, *_rest in CHAPTERS:
            self.assertRegex(self.text, rf"`{identifier}`\)\s*\|\s*{order}\s*\|",
                             f"the doc must state {identifier}'s order_index ({order})")
        self.assertIn("ten groups", self.text,
                      "the doc must place the Storage group among the book's ten groups")


class TestNoInventedTitlesOrIds(unittest.TestCase):
    """The strongest guard: nothing in the doc that the config does not contain."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")
        cls.flat = normalize(cls.text)

    def test_every_verified_quest_title_is_named(self) -> None:
        missing = [title for title in VERIFIED_TITLES if normalize(title) not in self.flat]
        self.assertEqual(
            missing, [],
            "every titled quest in the four Storage chapters must be named in the doc: "
            f"{missing}")

    def test_title_list_is_the_verified_snapshot(self) -> None:
        self.assertEqual(len(VERIFIED_TITLES), TOTAL_TITLED)
        self.assertEqual(len(set(VERIFIED_TITLES)), len(VERIFIED_TITLES), "duplicate titles")

    def test_no_bold_span_invents_a_quest_name(self) -> None:
        """Bold text is how the doc writes quest titles, so every bold span is checked."""
        known = {normalize(t) for t in VERIFIED_TITLES} | {normalize(s) for s in VERIFIED_SUBTITLES}
        known |= {normalize(n) for n in OTHER_VERIFIED_NAMES} | set(MODLIST_NAMES)
        offenders = []
        for span in set(re.findall(r"\*\*(.+?)\*\*", self.text, flags=re.DOTALL)):
            flat = normalize(span)
            if flat in known or flat in BOLD_PROSE_ALLOWLIST:
                continue
            if any(flat in title for title in known):
                continue  # a verified title's own tail, e.g. "The Void Cell"
            offenders.append(flat)
        self.assertEqual(sorted(offenders), [],
                         "bold spans must be verified titles/subtitles or known prose")

    def test_every_backticked_id_is_verified(self) -> None:
        used = set(re.findall(r"`([a-z0-9_]+:[a-z0-9_./]+)`", self.text))
        unknown = sorted(used - set(VERIFIED_ITEM_IDS))
        self.assertEqual(
            unknown, [],
            "the doc cites an id that is not in the pinned pack config - verify it against "
            f"config/ftbquests/quests at {PACK_COMMIT_SHORT} and add it here: {unknown}")

    def test_id_list_is_sorted_and_unique(self) -> None:
        self.assertEqual(list(VERIFIED_ITEM_IDS), sorted(set(VERIFIED_ITEM_IDS)),
                         "VERIFIED_ITEM_IDS must stay sorted and duplicate-free")


class TestLadders(unittest.TestCase):
    """Each tier chain must appear in the config's own dependency order."""

    @classmethod
    def setUpClass(cls) -> None:
        # normalized: the doc wraps long titles across lines, and a ladder rung may be
        # written as a title in one place and as an item id in another.
        cls.text = normalize(DOC.read_text(encoding="utf-8"))

    def assert_in_order(self, ladder: "tuple[str, ...]", name: str) -> None:
        positions = []
        for item in ladder:
            index = self.text.find(item)
            self.assertGreaterEqual(index, 0, f"{name}: the doc never mentions {item}")
            positions.append(index)
        self.assertEqual(positions, sorted(positions),
                         f"{name} is out of order in the doc: {ladder}")

    def test_sophisticated_storage_chest_ladder(self) -> None:
        self.assert_in_order(SOPHISTICATED_STORAGE_LADDER, "the Sophisticated Storage tiers")
        for tier in ("copper", "iron", "gold", "diamond", "netherite"):
            self.assertIn(f"sophisticatedstorage:{tier}_barrel", self.text,
                          "each chest quest's filter also accepts the matching barrel")

    def test_sophisticated_backpack_ladder(self) -> None:
        self.assert_in_order(SOPHISTICATED_BACKPACKS_LADDER, "the Sophisticated Backpacks tiers")

    def test_functional_storage_capacity_ladder(self) -> None:
        self.assert_in_order(FUNCTIONAL_STORAGE_UPGRADES, "the Functional Storage upgrades")
        for multiplier in ("x8", "x16", "x24", "x32"):
            self.assertIn(multiplier, self.text,
                          f"the drawer upgrades' subtitles state {multiplier}")

    def test_refined_storage_item_disk_ladder(self) -> None:
        self.assert_in_order(REFINED_STORAGE_ITEM_PARTS, "the Refined Storage item parts")
        self.assertIn("extradisks:advanced_storage_housing", self.text,
                      "the Extra Disks gate must be named")

    def test_refined_storage_fluid_disk_ladder(self) -> None:
        self.assert_in_order(REFINED_STORAGE_FLUID_PARTS, "the Refined Storage fluid parts")

    def test_ae2_component_ladder_crosses_into_mega_cells(self) -> None:
        self.assert_in_order(AE2_STORAGE_COMPONENTS, "the AE2 storage components")
        self.assertIn("megacells", self.text)
        self.assertLess(self.text.find("ae2:cell_component_256k"),
                        self.text.find("megacells:cell_component_1m"),
                        "MEGA Cells is the rung after AE2's own top tier")

    def test_cable_tiers_families_are_all_present(self) -> None:
        for item in CABLE_TIERS_ITEMS:
            self.assertIn(item, self.text, f"missing Cable Tiers item {item}")
        for title in CABLE_TIERS_TITLES:
            self.assertIn(title, self.text, f"missing Cable Tiers quest title {title}")

    def test_extended_and_advanced_ae_are_kept_apart(self) -> None:
        for hub in ("ExtendedAE", "Advanced AE"):
            self.assertIn(hub, self.text)
        self.assertIn("extendedae:crystal_assembler", self.text)
        self.assertIn("advanced_ae:reaction_chamber", self.text)
        self.assertIn("advanced_ae:quantum_core", self.text)
        self.assertIn("advanced_ae:quantum_multi_threader", self.text)
        self.assertLess(self.text.find("extendedae:entro_seed"),
                        self.text.find("advanced_ae:reaction_chamber"),
                        "the ExtendedAE side is documented before the Advanced AE side")


class TestGroundedQuotes(unittest.TestCase):
    """The advice that tells a player when to move up must stay the pack's own words."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = normalize(DOC.read_text(encoding="utf-8"))

    def test_key_quotes_survive_editing(self) -> None:
        for quote in KEY_QUOTES:
            self.assertIn(normalize(quote), self.text, f"missing verified quote: {quote[:60]}")

    def test_the_elision_convention_is_documented(self) -> None:
        self.assertIn("elision", self.text.lower(),
                      "quotes use … for elisions and paragraph breaks; the doc must say so")

    def test_the_doc_defers_to_the_in_game_book(self) -> None:
        self.assertIn("the in-game quest book (ftb quests) and jei are authoritative",
                      self.text.lower())


class TestCrossReferences(unittest.TestCase):
    """The doc must fit the skill's other documents, and SKILL.md must point at it."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")
        cls.example = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        cls.chapters = {c["id"]: c for c in cls.example["chapters"]}

    def test_doc_links_the_sibling_reference_docs(self) -> None:
        for name in ("progression.md", "key-mods.md", "atm-star-checklist.md",
                     "creative-checklist.md"):
            self.assertIn(name, self.text, f"the doc must cross-reference {name}")
        for path in (PROGRESSION_MD, KEY_MODS_MD, STAR_CHECKLIST_MD, CREATIVE_CHECKLIST_MD,
                     BOSS_CHECKLIST_MD, EXAMPLE_DATA):
            self.assertTrue(path.is_file(), f"cross-referenced file is missing: {path}")

    def test_chapter_ids_match_the_shipped_example(self) -> None:
        for identifier, _cid, title, _order, *_rest in CHAPTERS:
            entry = self.chapters.get(identifier)
            self.assertIsNotNone(entry, f"{identifier} is missing from the example file")
            assert entry is not None
            self.assertEqual(entry["group"], STORAGE_GROUP_TITLE)
            self.assertEqual(normalize(entry["title"]), normalize(title))
            expected_stage = "early-game" if identifier == "storage" else "tech"
            self.assertEqual(entry["stage"], expected_stage,
                             f"{identifier}'s stage must match what the doc says")
            self.assertIn(f"stage `{expected_stage}`", self.text)

    def test_example_file_carries_the_pack_stamp(self) -> None:
        self.assertEqual(self.example["pack_version"], PACK_VERSION_STAMP)
        self.assertIn(PACK_VERSION, self.example["pack_version_source"])

    def test_skill_md_documents_the_storage_ladder(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/storage-ladder.md", skill,
                      "SKILL.md must point at references/storage-ladder.md")
        # Research Grounding, Behaviors, and the Completion Checklist must all cover it.
        for needle in ("The storage ladder is dated the same way",
                       "Storage questions go to `references/storage-ladder.md`",
                       "Storage answers quoted verified titles or ids"):
            self.assertIn(needle, skill, f"SKILL.md is missing the section: {needle}")
        # Adding a reference doc is a feature: the frontmatter version must have moved.
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md frontmatter must carry a semver version")
        assert match is not None
        self.assertGreaterEqual(tuple(int(part) for part in match.groups()), (1, 2, 0),
                                "SKILL.md documents the storage ladder: bump past 1.1.0")

    def test_sibling_docs_are_not_contradicted_on_the_storage_group(self) -> None:
        progression = PROGRESSION_MD.read_text(encoding="utf-8")
        self.assertIn("Basic Storage, Applied Energistics 2, Extended & Advanced AE",
                      normalize(progression).replace("\\&", "&"),
                      "progression.md lists the same four chapters in the Storage group")


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
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set(),
                         "this suite must stay offline")
        self.assertTrue(imported <= {"__future__", "json", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(imported)}")

    def test_the_doc_needs_no_network_to_be_used(self) -> None:
        text = DOC.read_text(encoding="utf-8").lower()
        self.assertIn("authoritative", text)
        self.assertNotIn("curl ", text)
        self.assertNotIn("wget ", text)


if __name__ == "__main__":
    unittest.main()
