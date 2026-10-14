#!/usr/bin/env python3
"""Offline tests for references/enchanting-guide.md (Apothic Enchanting, pack 8.2).

Stdlib-only and network-free: every check reads files shipped in this skill. The verified
data below was read - not remembered - from the official pack repository AllTheMods/ATM-10
at ``main`` commit e5e3d1d83e (2026-09-22; CHANGELOG.md lists it as pack 8.2), parsed with
the skill's own SNBT reader (``scripts/snbt.py``):

  * ``config/ftbquests/quests/chapters/apothic_enchanting.snbt`` and its en_us lang file -
    the chapter's 58 quest ids, titles, dependencies, task items, and reward items;
  * ``config/ftbquests/quests/chapters/apotheosis_gear.snbt`` and its en_us lang file - the
    World Tier quests the chapter links to and depends on;
  * the en_us lang files of the other chapters the guide quotes (Chapter 3, Chapter 4,
    Apothic Spawners, Tips and Tricks, Industrial Foregoing);
  * ``config/apotheosis/enchantments.cfg`` - every enchantment's configured levels.

After a pack update, rebuild these constants from a fresh clone of the new release (the
same way SKILL.md's "Pack updates" workflow rebuilds the chapter list) - never edit them by
hand from memory, and never loosen a check to make an invented detail pass.

Covered:

  * provenance and grounding: the guide names the pack repository, the pinned commit, the
    files it was read from, pack 8.2 / the skill's 8.x stamp, and carries the skill's
    grounding rules (in-game quest book and JEI authoritative, approximate, nothing
    invented, no recipes);
  * verified quests: the embedded chapter data is self-consistent (58 quests, 57 titled,
    an acyclic dependency graph, four starting points, four cross-chapter World Tier
    dependencies, two either-or gates), and the guide lists every verified title, every
    task item, the chapter's shape, and the one untitled quest - marked, never named;
  * the two Eterna ceilings: World Tier caps (30/45/60/75/100) tied to the right quests and
    advancements, each shelf's own maximum, the spine in dependency order, the finished
    set-up's five tasks, and the quoted infusion windows next to the right quests;
  * configured levels: every vanilla and Apothic Enchanting row of the guide's tables
    matches ``enchantments.cfg``, and the summary claims (117 entries, 84 raised, 32 kept,
    one lowered, loot levels at the original cap, the level-13 holders) are recomputed;
  * no invented names: every namespaced id in the guide is on the verified allowlist, every
    title column holds only verified titles (or the untitled marker), chapter names are
    verified, and task titles are never dressed up as quest titles;
  * wiring: SKILL.md (version bumped to 1.2.0 or later) routes enchanting questions to the
    guide, the sibling docs point at it, and the guide's chapter claims match the shipped
    ``examples/progress.example.json``;
  * offline guarantee: this suite imports no network or process module.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
GUIDE_MD = REFERENCES / "enchanting-guide.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"
PROGRESSION_MD = REFERENCES / "progression.md"
KEY_MODS_MD = REFERENCES / "key-mods.md"
SIBLING_DOCS = ("progression.md", "key-mods.md", "boss-checklist.md",
                "atm-star-checklist.md", "creative-checklist.md")

PACK_COMMIT = "e5e3d1d83e"
PACK_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
CHAPTER_ID = "apothic_enchanting"
UNTITLED_MARKER = "(no title in the config)"

# --------------------------------------------------------------------------------------
# verified data: the Apothic Enchanting chapter (apothic_enchanting.snbt + en_us lang)
# --------------------------------------------------------------------------------------

# Every quest in the chapter, in config order: quest id -> en_us title (Minecraft `&`
# formatting codes stripped), or None where the lang file gives the quest no title.
# Dependencies: quest id -> the quest ids it needs (config `dependencies`, in order). Ids
# outside ENCHANTING_QUESTS belong to the Apotheosis Gear chapter (GEAR_QUEST_LINKS).
ENCHANTING_QUESTS = {
    "1FAFDB20F504688E": "Apothic Enchanting",
    "79AF63E77AD70A93": "Vanilla Max is just the start",
    "6C2C135B9B7B9402": "Infusing",
    "31E7F7464D79F881": "Other Infusion Items",
    "24C757B8AA6841F6": "Making a real Trident",
    "6884E25641A1020C": "Enchantment Library",
    "42746659C66CF17F": "Library of Alexandria",
    "78FEDE6FA4845585": "Negative amounts",
    "0A3C464EF7CDD5F6": "Hellshelves",
    "45161821C221EF0B": "Infused Hellshelves",
    "60850E717C747A78": "Enchanting Clues",
    "51E554305FFEBA1D": "Blazing Hellshelf",
    "7C758209D06ED0E3": "Glowing Hellshelf",
    "235E3C386E8D36A3": "Deepshelf",
    "6852BEFDD4DE4E4B": "Soul-Touched Deepshelf",
    "24FCFF18296ED907": "Soul-Touched Sculkshelf",
    "0518551637F76C50": "Echoing Deepshelf",
    "2EC2FA680076C07D": "Echoing Sculkshelf",
    "1873205CF5247E3E": "Endshelves",
    "523DC411241B470A": "Negative Enchantments Removal",
    "5DE45BC0258D1B0B": "Pearlescent Endshelf",
    "148A33CC36B2563A": "Draconic Endshelf",
    "7C9D9D1C054874A7": "Best Enchanting set-up",
    "6A07D09831428CB9": "Seashelves",
    "24391162F4FF0587": "Infused Seashelf",
    "5C73247A48E72FB3": "Remove Enchantments from Pool",
    "70D2C5FAC661E01A": "Heart-Forged Seashelf",
    "191A7F3C9FBA4C13": "Crystalline Seashelf",
    "62D39F68DE6E44A4": "Arcana",
    "0F3A0A4DC18E5E55": "Eterna",
    "586D5DE28EEC8014": "Quanta",
    "158F872A3A2C3650": "Infused Dragon's Breath",
    "001A348054127235": "Making Budding Amethyst",
    "78E66F1DE42C747A": "Infinite Echo Shards?",
    "6220EDE42C813C1B": "Unbreakable Charms",
    "105442DA79829777": "Tome of Scrapping",
    "4E895C54651A3CB3": "Tomes",
    "377D6CF86BC1C64F": "Tome of Superior Scrapping",
    "3D31B94CC42BCE43": None,
    "224716A537F2FFA0": "Armor Tomes",
    "516E66BE01EE5B31": "Weapon Tomes",
    "43167C59036E79A7": "Tool Tomes",
    "6C57D64518FF22C0": "ETC. Tomes",
    "695889817162EFC7": "Crafting EXP?",
    "784466C3813AA506": "Flimsy Ender Lead",
    "78BFDD3A9B996655": "Ender Lead",
    "61217D80BFF8A858": "Occult Ender Lead",
    "37E556B4A730E5AA": "The Frontier Calls",
    "091957223C32B094": "Ascent to 60",
    "1F748ACA3976A92F": "A Gate",
    "18AA64DF63F68762": "Another Gate",
    "1113BF457DB7F1DE": "To reach the Summit",
    "73E09ED46A94B812": "Ahh, Pinnacle, at last",
    "4EE6824A970EEB35": "Infusing Spawner Runes",
    "7F007C888C23EC42": "Gem Case",
    "06F70F6CA37168CC": "Gem Case of House Fabergé",
    "1617C1935F22FBD1": "God-Fused Pearl",
    "3311B79A8F6C6ADD": "Enchanting Table of the Raven",
}
ENCHANTING_DEPENDENCIES = {
    "79AF63E77AD70A93": ("1FAFDB20F504688E",),
    "6C2C135B9B7B9402": ("79AF63E77AD70A93",),
    "31E7F7464D79F881": ("6C2C135B9B7B9402",),
    "24C757B8AA6841F6": ("31E7F7464D79F881", "37E556B4A730E5AA"),
    "42746659C66CF17F": ("6884E25641A1020C", "31E7F7464D79F881", "73E09ED46A94B812"),
    "78FEDE6FA4845585": ("62D39F68DE6E44A4", "586D5DE28EEC8014", "0F3A0A4DC18E5E55"),
    "0A3C464EF7CDD5F6": ("6C2C135B9B7B9402",),
    "45161821C221EF0B": ("0A3C464EF7CDD5F6", "37E556B4A730E5AA"),
    "60850E717C747A78": ("45161821C221EF0B",),
    "51E554305FFEBA1D": ("45161821C221EF0B",),
    "7C758209D06ED0E3": ("45161821C221EF0B",),
    "235E3C386E8D36A3": ("091957223C32B094",),
    "6852BEFDD4DE4E4B": ("235E3C386E8D36A3",),
    "24FCFF18296ED907": ("6852BEFDD4DE4E4B",),
    "0518551637F76C50": ("235E3C386E8D36A3",),
    "2EC2FA680076C07D": ("0518551637F76C50",),
    "1873205CF5247E3E": ("158F872A3A2C3650",),
    "523DC411241B470A": ("6C2C135B9B7B9402",),
    "5DE45BC0258D1B0B": ("1873205CF5247E3E",),
    "148A33CC36B2563A": ("1873205CF5247E3E",),
    "7C9D9D1C054874A7": ("148A33CC36B2563A",),
    "6A07D09831428CB9": ("6C2C135B9B7B9402",),
    "24391162F4FF0587": ("6A07D09831428CB9", "37E556B4A730E5AA"),
    "5C73247A48E72FB3": ("24391162F4FF0587",),
    "70D2C5FAC661E01A": ("24391162F4FF0587",),
    "191A7F3C9FBA4C13": ("24391162F4FF0587",),
    "62D39F68DE6E44A4": ("6C2C135B9B7B9402",),
    "0F3A0A4DC18E5E55": ("6C2C135B9B7B9402",),
    "586D5DE28EEC8014": ("6C2C135B9B7B9402",),
    "158F872A3A2C3650": ("523DC411241B470A", "73E09ED46A94B812"),
    "001A348054127235": ("31E7F7464D79F881", "091957223C32B094"),
    "78E66F1DE42C747A": ("31E7F7464D79F881", "1113BF457DB7F1DE"),
    "6220EDE42C813C1B": ("31E7F7464D79F881", "73E09ED46A94B812"),
    "105442DA79829777": ("4E895C54651A3CB3",),
    "4E895C54651A3CB3": ("6C2C135B9B7B9402",),
    "377D6CF86BC1C64F": ("31E7F7464D79F881", "105442DA79829777", "37E556B4A730E5AA"),
    "3D31B94CC42BCE43": ("31E7F7464D79F881", "377D6CF86BC1C64F", "091957223C32B094"),
    "224716A537F2FFA0": ("4E895C54651A3CB3",),
    "516E66BE01EE5B31": ("4E895C54651A3CB3",),
    "43167C59036E79A7": ("4E895C54651A3CB3",),
    "6C57D64518FF22C0": ("4E895C54651A3CB3",),
    "695889817162EFC7": ("31E7F7464D79F881",),
    "78BFDD3A9B996655": ("31E7F7464D79F881", "784466C3813AA506", "37E556B4A730E5AA"),
    "61217D80BFF8A858": ("31E7F7464D79F881", "78BFDD3A9B996655", "1113BF457DB7F1DE"),
    "37E556B4A730E5AA": ("2A032EC573B5316C", "1F748ACA3976A92F"),
    "091957223C32B094": ("1D1FAA2F86695781", "18AA64DF63F68762"),
    "1F748ACA3976A92F": ("6A07D09831428CB9", "0A3C464EF7CDD5F6"),
    "18AA64DF63F68762": ("7C758209D06ED0E3", "191A7F3C9FBA4C13"),
    "1113BF457DB7F1DE": ("097FDC136BC843A7",),
    "73E09ED46A94B812": ("2EC2FA680076C07D", "24FCFF18296ED907", "7EF873DCEB3B9D48"),
    "4EE6824A970EEB35": ("31E7F7464D79F881", "1113BF457DB7F1DE"),
    "06F70F6CA37168CC": ("7F007C888C23EC42", "73E09ED46A94B812"),
    "1617C1935F22FBD1": ("148A33CC36B2563A",),
    "3311B79A8F6C6ADD": ("1617C1935F22FBD1",),
}
ENCHANTING_TASK_ITEMS = (
    "apotheosis:ender_gem_case",
    "apotheosis:gem_case",
    "apotheosis:god_fused_pearl",
    "apotheosis:infused_spawner_rune",
    "apothic_enchanting:apothic_enchanting_table",
    "apothic_enchanting:beeshelf",
    "apothic_enchanting:blazing_hellshelf",
    "apothic_enchanting:boots_tome",
    "apothic_enchanting:bow_tome",
    "apothic_enchanting:chestplate_tome",
    "apothic_enchanting:crystal_seashelf",
    "apothic_enchanting:deepshelf",
    "apothic_enchanting:draconic_endshelf",
    "apothic_enchanting:echoing_deepshelf",
    "apothic_enchanting:echoing_sculkshelf",
    "apothic_enchanting:ender_lead",
    "apothic_enchanting:ender_library",
    "apothic_enchanting:endshelf",
    "apothic_enchanting:extraction_tome",
    "apothic_enchanting:filtering_shelf",
    "apothic_enchanting:fishing_tome",
    "apothic_enchanting:flimsy_ender_lead",
    "apothic_enchanting:geode_shelf",
    "apothic_enchanting:glowing_hellshelf",
    "apothic_enchanting:heart_seashelf",
    "apothic_enchanting:hellshelf",
    "apothic_enchanting:helmet_tome",
    "apothic_enchanting:improved_scrap_tome",
    "apothic_enchanting:inert_trident",
    "apothic_enchanting:infused_breath",
    "apothic_enchanting:infused_hellshelf",
    "apothic_enchanting:infused_seashelf",
    "apothic_enchanting:leggings_tome",
    "apothic_enchanting:library",
    "apothic_enchanting:melonshelf",
    "apothic_enchanting:occult_ender_lead",
    "apothic_enchanting:other_tome",
    "apothic_enchanting:pearl_endshelf",
    "apothic_enchanting:pickaxe_tome",
    "apothic_enchanting:raven_enchanting_table",
    "apothic_enchanting:scrap_tome",
    "apothic_enchanting:seashelf",
    "apothic_enchanting:sightshelf",
    "apothic_enchanting:sightshelf_t2",
    "apothic_enchanting:soul_touched_deepshelf",
    "apothic_enchanting:soul_touched_sculkshelf",
    "apothic_enchanting:stoneshelf",
    "apothic_enchanting:treasure_shelf",
    "apothic_enchanting:weapon_tome",
    "minecraft:book",
    "minecraft:budding_amethyst",
    "minecraft:echo_shard",
    "minecraft:enchanting_table",
    "minecraft:honey_bottle",
    "minecraft:lapis_lazuli",
)
ENCHANTING_REWARD_ITEMS = (
    "apotheosis:gem",
    "apotheosis:godforged_pearl",
    "apothic_enchanting:basic_bookshelf",
    "apothic_enchanting:blazing_hellshelf",
    "apothic_enchanting:deepshelf",
    "apothic_enchanting:dormant_deepshelf",
    "apothic_enchanting:draconic_endshelf",
    "apothic_enchanting:ender_lead",
    "apothic_enchanting:endshelf",
    "apothic_enchanting:flimsy_ender_lead",
    "apothic_enchanting:heart_seashelf",
    "apothic_enchanting:hellshelf",
    "apothic_enchanting:infused_hellshelf",
    "apothic_enchanting:infused_seashelf",
    "apothic_enchanting:seashelf",
    "apothic_enchanting:warden_tendril",
    "minecraft:amethyst_shard",
    "minecraft:anvil",
    "minecraft:blaze_rod",
    "minecraft:book",
    "minecraft:budding_amethyst",
    "minecraft:dragon_breath",
    "minecraft:dragon_head",
    "minecraft:echo_shard",
    "minecraft:enchanted_book",
    "minecraft:end_stone_bricks",
    "minecraft:ender_pearl",
    "minecraft:experience_bottle",
    "minecraft:lapis_block",
    "minecraft:lapis_lazuli",
    "minecraft:sculk",
    "minecraft:spawner",
    "minecraft:stick",
    "naturescompass:naturescompass",
)

# The one untitled quest: its subtitle and its only task item (the book shows the item's
# own name; the guide must mark it, not name it).
UNTITLED_QUEST_ID = "3D31B94CC42BCE43"
UNTITLED_SUBTITLE = "All Enchantments, doesn't break"
UNTITLED_TASK_ITEM = "apothic_enchanting:extraction_tome"

# Quests with `dependency_requirement: "one_completed"` - the chapter's either-or gates.
ONE_COMPLETED_GATES = ("1F748ACA3976A92F", "18AA64DF63F68762")

# The chapter's 65 tasks by type, and the non-item task targets.
TASK_TYPE_COUNTS = {"item": 58, "advancement": 5, "dimension": 2}
ENCHANTING_TASK_TAGS = ("c:bookshelves", "curios:charm")
ENCHANTING_TASK_ADVANCEMENTS = (
    "apotheosis:progression/ascent",
    "apotheosis:progression/frontier",
    "apotheosis:progression/pinnacle",
    "apotheosis:progression/summit",
    "minecraft:story/enchant_item",
)
ENCHANTING_TASK_DIMENSIONS = ("minecraft:overworld",)

# The chapter's six `quest_links`: Apotheosis Gear quests shown on this canvas.
GEAR_QUEST_LINKS = {
    "196312DF0D2E2CB6": "Invaders/Bosses and World Tiers",
    "377A41499D8218C9": "World Tier: Haven",
    "2A032EC573B5316C": "World Tier: Frontier",
    "1D1FAA2F86695781": "World Tier: Ascent",
    "097FDC136BC843A7": "World Tier: Summit",
    "7EF873DCEB3B9D48": "World Tier: Pinnacle",
}

# World Tier -> (Max Eterna per the quest text, its advancement task, this chapter's quest
# that depends on it, that quest's subtitle). Haven has no dependent quest here.
WORLD_TIERS = (
    ("World Tier: Haven", 30, "apotheosis:progression/haven", None, None),
    ("World Tier: Frontier", 45, "apotheosis:progression/frontier",
     "The Frontier Calls", "Why is my Eterna capped to 30?"),
    ("World Tier: Ascent", 60, "apotheosis:progression/ascent",
     "Ascent to 60", "Max Eterna to 60"),
    ("World Tier: Summit", 75, "apotheosis:progression/summit",
     "To reach the Summit", "Max Eterna to 75"),
    ("World Tier: Pinnacle", 100, "apotheosis:progression/pinnacle",
     "Ahh, Pinnacle, at last", "Max Eterna to 100"),
)

# The max-enchanting spine, in dependency order; a step with two titles is the pack's
# Hellshelf / Seashelf either-or (or a pair that both lead on).
SPINE = (
    ("Apothic Enchanting",),
    ("Vanilla Max is just the start",),
    ("Infusing",),
    ("Hellshelves", "Seashelves"),
    ("A Gate",),
    ("The Frontier Calls",),
    ("Infused Hellshelves", "Infused Seashelf"),
    ("Glowing Hellshelf", "Crystalline Seashelf"),
    ("Another Gate",),
    ("Ascent to 60",),
    ("Deepshelf",),
    ("Soul-Touched Deepshelf", "Echoing Deepshelf"),
    ("Soul-Touched Sculkshelf", "Echoing Sculkshelf"),
    ("Ahh, Pinnacle, at last",),
    ("Infused Dragon's Breath",),
    ("Endshelves",),
    ("Draconic Endshelf",),
    ("Best Enchanting set-up",),
)
RAVEN_TAIL = ("Draconic Endshelf", "God-Fused Pearl", "Enchanting Table of the Raven")

# Each shelf's own maximum Eterna, as its quest text words it.
SHELF_MAXIMUM_QUOTES = (
    ("Vanilla Max is just the start", "a max of 30"),
    ("Infused Hellshelves", "5 Eterna with a max of 60 Eterna"),
    ("Infused Seashelf", "more Eterna at 5 with a max of 60"),
    ("Soul-Touched Deepshelf", "increases max Eterna to 75"),
    ("Echoing Deepshelf", "raising the max Eterna to 75"),
    ("Soul-Touched Sculkshelf", "a max Eterna of 80"),
    ("Endshelves", "But their max Eterna of 90 is incredible!"),
    ("Pearlescent Endshelf", "max Eterna 90, but this isn't what we want for max Enchanting"),
    ("Draconic Endshelf", "it has the max Eterna of 100"),
)

# Best Enchanting set-up: its five tasks, in config order, with required counts.
BEST_SETUP_TASKS = (
    ("apothic_enchanting:soul_touched_sculkshelf", 5),
    ("apothic_enchanting:echoing_sculkshelf", 5),
    ("apothic_enchanting:draconic_endshelf", 1),
    ("apothic_enchanting:geode_shelf", 1),
    ("apothic_enchanting:treasure_shelf", 1),
)

# Infusion windows, quoted from each quest's own text.
INFUSION_WINDOWS = (
    ("Making a real Trident", "between 40 Eterna, 20%-50% Quanta, and atleast 35% Arcana"),
    ("Ender Lead", "at least 45 Eterna, 25% Quanta, and 40% Arcana"),
    ("Making Budding Amethyst", "60 Eterna, between 30% and 50% Quanta, and 50% Arcana"),
    ("Infinite Echo Shards?", "70 Eterna, 50% Quanta, and 50% Arcana"),
    ("Infusing Spawner Runes", "at least 70 Eterna, 30% Quanta, and 50% Arcana"),
    ("Occult Ender Lead", "at least 75 Eterna, 85% Quanta, and between 60-85% Arcana"),
    ("Unbreakable Charms",
     "100 Eterna, between 8.5% and 13.5% Quanta, and between 32.5% and 37.5% Arcana"),
    ("Deepshelf", "60 Eterna, 40% Quanta, and 40% Arcana"),
    ("Infused Dragon's Breath", "80 Eterna, 25% Quanta and 100% Arcana"),
)
GOD_FUSED_PEARL_WINDOW = "100 Eterna, 9.65-11.00% Quanta, and 58.75-60.0% Arcana"

# The chapter's reward tables sum to this many XP levels (`xp_levels` rewards).
XP_LEVELS_TOTAL = 311

# Task titles from the lang files - task labels, never quest titles.
TASK_TITLES = ("Enchanting Tables", "Bookshelves", "Permanent Charms", "Armor Tomes",
               "Weapon Tomes", "Tool Tomes", "Capturing Books", "Apothic Gateways",
               "Disenchantment Methods")

# --------------------------------------------------------------------------------------
# verified data: the other chapters the guide quotes
# --------------------------------------------------------------------------------------

# Chapter titles (lang/en_us/chapter.snbt) the guide names.
VERIFIED_CHAPTER_TITLES = ("Apothic Enchanting", "Apotheosis Gear", "Apothic Spawners",
                           "Chapter 3: The ATM Star", "Chapter 4: Creative",
                           "Tips and Tricks", "Industrial Foregoing")

# Quest titles from other chapters that the guide uses as titles.
OTHER_CHAPTER_TITLES = (
    "Godforged Pearl",               # apotheosis_gear
    "Apothic Mods",                  # chapter_2_the_star (hub, task minecraft:bookshelf)
    "Infused Dragon's Breath",       # chapter_2_the_star (same title as this chapter's)
    "Runic Enchanter",               # achapter_2r_6the_atm_star
    "Disenchanting Methods",         # tips_and_tricks
)

# Namespaced ids the guide cites from other chapters' tasks.
OTHER_CHAPTER_IDS = (
    "apotheosis:progression/haven",              # apotheosis_gear: World Tier: Haven
    "gateways:gate_pearl",                       # apotheosis_gear: "Apothic Gateways" task
    "minecraft:bookshelf",                       # chapter_2_the_star: Apothic Mods
    "allthetweaks:mini_nether",                  # chapter_2_the_star (untitled)
    "allthetweaks:mini_end",                     # chapter_2_the_star (untitled)
    "allthetweaks:mini_exit",                    # chapter_2_the_star (untitled)
    "modern_industrialization:runic_enchanter",  # achapter_2r_6the_atm_star
    "industrialforegoing:enchantment_factory",   # industrial_foregoing (untitled)
    "minecraft:enchanted_book",                  # apotheosis_2: "Capturing Books" task
) + (
    # tips_and_tricks: Disenchanting Methods accepts any of these (with the three tomes
    # and minecraft:anvil, which are already verified above)
    "disenchanting_table:disenchanting_table",
    "draconicevolution:disenchanter",
    "tombstone:book_of_disenchantment",
    "actuallyadditions:lens_of_disenchanting",
    "industrialforegoing:enchantment_extractor",
    "evilcraft:purifier",
    "evilcraft:blook",
)
DISENCHANTING_METHOD_ITEMS = OTHER_CHAPTER_IDS[-7:] + (
    "apothic_enchanting:scrap_tome",
    "apothic_enchanting:improved_scrap_tome",
    "apothic_enchanting:extraction_tome",
    "minecraft:anvil",
)

# --------------------------------------------------------------------------------------
# verified data: config/apotheosis/enchantments.cfg
# --------------------------------------------------------------------------------------

# Every configured enchantment: id -> (original max level per the cfg comment,
# "Max Level", "Max Loot Level"). "Forced Level Cap" is -1 and both power functions are
# empty for every entry.
ENCHANTMENT_LEVELS = {
    "apothic_enchanting:berserkers_fury": (3, 3, 3),
    "apothic_enchanting:boon_of_the_earth": (5, 5, 5),
    "apothic_enchanting:chainsaw": (1, 1, 1),
    "apothic_enchanting:chromatic": (1, 1, 1),
    "apothic_enchanting:crescendo_of_bolts": (5, 5, 5),
    "apothic_enchanting:endless_quiver": (1, 1, 1),
    "apothic_enchanting:growth_serum": (1, 1, 1),
    "apothic_enchanting:icy_thorns": (3, 5, 3),
    "apothic_enchanting:infusion": (1, 1, 1),
    "apothic_enchanting:knowledge_of_the_ages": (3, 3, 3),
    "apothic_enchanting:life_mending": (3, 3, 3),
    "apothic_enchanting:miners_fervor": (5, 1, 1),
    "apothic_enchanting:natures_blessing": (3, 7, 3),
    "apothic_enchanting:rebounding": (3, 5, 3),
    "apothic_enchanting:reflective_defenses": (5, 7, 5),
    "apothic_enchanting:scavenger": (3, 3, 3),
    "apothic_enchanting:shield_bash": (4, 7, 4),
    "apothic_enchanting:stable_footing": (1, 1, 1),
    "apothic_enchanting:tempting": (1, 1, 1),
    "apothic_enchanting:worker_exploitation": (1, 1, 1),
    "apothic_spawners:capturing": (3, 7, 3),
    "ars_elemental:mirror_shield": (3, 7, 3),
    "ars_elemental:soulbound": (1, 1, 1),
    "ars_nouveau:mana_boost": (3, 7, 3),
    "ars_nouveau:mana_regen": (3, 7, 3),
    "ars_nouveau:reactive": (4, 8, 4),
    "deeperdarker:catalysis": (3, 5, 3),
    "deeperdarker:sculk_smite": (5, 10, 5),
    "dungeons_arise:discharge": (3, 5, 3),
    "dungeons_arise:ensnaring": (4, 6, 4),
    "dungeons_arise:lolths_curse": (1, 1, 1),
    "dungeons_arise:purification": (3, 4, 3),
    "dungeons_arise:voltaic_shot": (1, 1, 1),
    "eternal_starlight:fearless": (2, 6, 2),
    "eternal_starlight:poisoning": (4, 8, 4),
    "eternal_starlight:soul_snatcher": (3, 5, 3),
    "evilcraft:breaking": (3, 8, 3),
    "evilcraft:life_stealing": (3, 6, 3),
    "evilcraft:poison_tip": (3, 7, 3),
    "evilcraft:unusing": (1, 1, 1),
    "evilcraft:vengeance": (3, 8, 3),
    "farmersdelight:backstabbing": (3, 8, 3),
    "forbidden_arcanus:soul_looting": (3, 8, 3),
    "minecolonies:raider_damage_enchant": (2, 6, 2),
    "minecraft:aqua_affinity": (1, 1, 1),
    "minecraft:bane_of_arthropods": (5, 10, 5),
    "minecraft:binding_curse": (1, 1, 1),
    "minecraft:blast_protection": (4, 9, 4),
    "minecraft:breach": (4, 8, 4),
    "minecraft:channeling": (1, 1, 1),
    "minecraft:density": (5, 10, 5),
    "minecraft:depth_strider": (3, 7, 3),
    "minecraft:efficiency": (5, 9, 5),
    "minecraft:feather_falling": (4, 11, 4),
    "minecraft:fire_aspect": (2, 5, 2),
    "minecraft:fire_protection": (4, 9, 4),
    "minecraft:flame": (1, 1, 1),
    "minecraft:fortune": (3, 8, 3),
    "minecraft:frost_walker": (2, 7, 2),
    "minecraft:impaling": (5, 10, 5),
    "minecraft:infinity": (1, 1, 1),
    "minecraft:knockback": (2, 5, 2),
    "minecraft:looting": (3, 8, 3),
    "minecraft:loyalty": (3, 9, 3),
    "minecraft:luck_of_the_sea": (3, 8, 3),
    "minecraft:lure": (3, 8, 3),
    "minecraft:mending": (1, 1, 1),
    "minecraft:multishot": (1, 1, 1),
    "minecraft:piercing": (4, 8, 4),
    "minecraft:power": (5, 9, 5),
    "minecraft:projectile_protection": (4, 11, 4),
    "minecraft:protection": (4, 8, 4),
    "minecraft:punch": (2, 5, 2),
    "minecraft:quick_charge": (3, 5, 3),
    "minecraft:respiration": (3, 7, 3),
    "minecraft:riptide": (3, 9, 3),
    "minecraft:sharpness": (5, 9, 5),
    "minecraft:silk_touch": (1, 1, 1),
    "minecraft:smite": (5, 10, 5),
    "minecraft:soul_speed": (3, 7, 3),
    "minecraft:sweeping_edge": (3, 8, 3),
    "minecraft:swift_sneak": (3, 5, 3),
    "minecraft:thorns": (3, 5, 3),
    "minecraft:unbreaking": (3, 8, 3),
    "minecraft:vanishing_curse": (1, 1, 1),
    "minecraft:wind_burst": (3, 8, 3),
    "mysticalagriculture:mystical_enlightenment": (5, 9, 5),
    "mysticalagriculture:soul_siphoner": (5, 9, 5),
    "quarryplus:quarry_pickaxe": (1, 1, 1),
    "railcraft:destruction": (3, 7, 3),
    "railcraft:implosion": (5, 10, 5),
    "railcraft:smack": (4, 9, 4),
    "railcraft:wrecking": (5, 9, 5),
    "reliquary:severing": (5, 9, 5),
    "supplementaries:stasis": (1, 1, 1),
    "the_bumblezone:comb_cutter": (2, 3, 2),
    "the_bumblezone:neurotoxins": (2, 13, 2),
    "the_bumblezone:potent_poison": (3, 11, 3),
    "tombstone:blessing": (10, 13, 10),
    "tombstone:curse_of_bones": (10, 13, 10),
    "tombstone:decrepitude": (10, 13, 10),
    "tombstone:frostbite": (10, 13, 10),
    "tombstone:incurable_wounds": (10, 13, 10),
    "tombstone:magic_siphon": (10, 13, 10),
    "tombstone:plague_bringer": (10, 13, 10),
    "tombstone:ruthless_strike": (10, 13, 10),
    "tombstone:sanctified": (10, 13, 10),
    "tombstone:soulbound": (1, 1, 1),
    "tombstone:spectral_bite": (10, 13, 10),
    "tombstone:spectral_conjurer": (10, 13, 10),
    "twilightforest:chill_aura": (3, 8, 3),
    "twilightforest:destruction": (3, 8, 3),
    "twilightforest:fire_react": (3, 8, 3),
    "twilightforest:renewal": (1, 1, 1),
    "undergarden:longevity": (3, 7, 3),
    "undergarden:ricochet": (3, 7, 3),
    "undergarden:self_sling": (1, 1, 1),
}

# The examples the guide's short answer quotes.
SHORT_ANSWER_LEVELS = (
    ("minecraft:sharpness", 9),
    ("minecraft:efficiency", 9),
    ("minecraft:fortune", 8),
    ("minecraft:looting", 8),
    ("minecraft:unbreaking", 8),
    ("minecraft:mending", 1),
)

VERIFIED_IDS = frozenset(
    ENCHANTING_TASK_ITEMS + ENCHANTING_TASK_TAGS + ENCHANTING_TASK_ADVANCEMENTS
    + ENCHANTING_TASK_DIMENSIONS + ENCHANTING_REWARD_ITEMS + tuple(ENCHANTMENT_LEVELS)
    + OTHER_CHAPTER_IDS
)
VERIFIED_TITLES = frozenset(
    tuple(title for title in ENCHANTING_QUESTS.values() if title)
    + tuple(GEAR_QUEST_LINKS.values()) + OTHER_CHAPTER_TITLES
)


# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def flatten(text: str) -> str:
    """Collapse whitespace so wrapped Markdown lines compare as one line."""
    return re.sub(r"\s+", " ", text)


def section(text: str, heading: str) -> str:
    """The body of the `## heading` section (up to the next `## ` heading)."""
    match = re.search(r"^## " + re.escape(heading) + r"[^\n]*\n(.*?)(?=^## |\Z)",
                      text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def markdown_tables(text: str) -> "list[tuple[list[str], list[list[str]]]]":
    """Every pipe table in `text` as (header cells, body rows of cells)."""
    tables: "list[tuple[list[str], list[list[str]]]]" = []
    block: "list[str]" = []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            block.append(line)
            continue
        if len(block) >= 2 and re.match(r"^\|[-| ]+\|$", block[1]):
            cells = [[cell.strip() for cell in row.strip().strip("|").split("|")]
                     for row in block]
            tables.append((cells[0], cells[2:]))
        block = []
    return tables


def column(text: str, header_test) -> "list[str]":
    """All body cells under every table header that satisfies `header_test`."""
    cells: "list[str]" = []
    for header, rows in markdown_tables(text):
        for index, name in enumerate(header):
            if header_test(name):
                cells.extend(row[index] for row in rows if index < len(row))
    return cells


def bold_spans(text: str) -> "list[str]":
    return re.findall(r"\*\*(.+?)\*\*", text)


def italic_spans(text: str) -> "list[str]":
    """Single-asterisk spans that are not quotes (`*"..."*`) and not bold."""
    return re.findall(r'(?<![*\w])\*(?![*"\s])([^*"]+?)(?<!\s)\*(?![*\w])', text)


def title_of(quest_id: str) -> str:
    title = ENCHANTING_QUESTS.get(quest_id) or GEAR_QUEST_LINKS.get(quest_id)
    assert title, f"no verified title for {quest_id}"
    return title


ID_BY_TITLE = {title: quest_id for quest_id, title in ENCHANTING_QUESTS.items() if title}


# --------------------------------------------------------------------------------------
# the embedded verified data is internally consistent
# --------------------------------------------------------------------------------------

class TestVerifiedChapterData(unittest.TestCase):
    """Guards the constants themselves, so a bad edit cannot slip a fact past the doc tests."""

    def test_quest_ids_and_titles(self) -> None:
        self.assertEqual(len(ENCHANTING_QUESTS), 58)
        for quest_id in list(ENCHANTING_QUESTS) + list(GEAR_QUEST_LINKS):
            self.assertRegex(quest_id, r"^[0-9A-F]{16}$")
        titled = [title for title in ENCHANTING_QUESTS.values() if title]
        self.assertEqual(len(titled), 57)
        self.assertEqual(len(set(titled)), 57, "verified titles are unique in the chapter")
        self.assertEqual([quest_id for quest_id, title in ENCHANTING_QUESTS.items()
                          if not title], [UNTITLED_QUEST_ID])

    def test_dependencies_point_at_known_quests_and_form_a_dag(self) -> None:
        known = set(ENCHANTING_QUESTS) | set(GEAR_QUEST_LINKS)
        for quest_id, needs in ENCHANTING_DEPENDENCIES.items():
            self.assertIn(quest_id, ENCHANTING_QUESTS)
            for need in needs:
                self.assertIn(need, known, f"{quest_id} needs an unknown quest {need}")
        # Kahn's algorithm over the in-chapter edges must visit every quest.
        indegree = {quest_id: sum(1 for need in ENCHANTING_DEPENDENCIES.get(quest_id, ())
                                  if need in ENCHANTING_QUESTS)
                    for quest_id in ENCHANTING_QUESTS}
        ready = [quest_id for quest_id, count in indegree.items() if count == 0]
        visited = 0
        while ready:
            current = ready.pop()
            visited += 1
            for quest_id, needs in ENCHANTING_DEPENDENCIES.items():
                if current in needs:
                    indegree[quest_id] -= 1
                    if indegree[quest_id] == 0:
                        ready.append(quest_id)
        self.assertEqual(visited, 58, "the chapter's dependency graph must be acyclic")

    def test_starting_points_gates_and_cross_chapter_edges(self) -> None:
        starts = sorted(title_of(quest_id) for quest_id in ENCHANTING_QUESTS
                        if quest_id not in ENCHANTING_DEPENDENCIES)
        self.assertEqual(starts, ["Apothic Enchanting", "Enchantment Library",
                                  "Flimsy Ender Lead", "Gem Case"])
        cross = {title_of(quest_id): title_of(need)
                 for quest_id, needs in ENCHANTING_DEPENDENCIES.items()
                 for need in needs if need in GEAR_QUEST_LINKS}
        expected = {tier_quest: tier for tier, _, _, tier_quest, _ in WORLD_TIERS if tier_quest}
        self.assertEqual(cross, expected,
                         "exactly the four tier quests depend on the Gear chapter's tiers")
        self.assertEqual([title_of(gate) for gate in ONE_COMPLETED_GATES],
                         ["A Gate", "Another Gate"])
        self.assertEqual({title_of(need) for need in ENCHANTING_DEPENDENCIES["1F748ACA3976A92F"]},
                         {"Seashelves", "Hellshelves"})
        self.assertEqual({title_of(need) for need in ENCHANTING_DEPENDENCIES["18AA64DF63F68762"]},
                         {"Glowing Hellshelf", "Crystalline Seashelf"})
        self.assertEqual(sum(TASK_TYPE_COUNTS.values()), 65)

    def test_the_spine_follows_the_dependency_graph(self) -> None:
        """Every spine quest directly needs a quest from the step before it."""
        for previous, step in zip(SPINE, SPINE[1:]):
            for title in step:
                needs = {title_of(need) for need in ENCHANTING_DEPENDENCIES[ID_BY_TITLE[title]]}
                self.assertTrue(needs & set(previous),
                                f"{title!r} does not depend on any of {previous!r}")
        for previous, title in zip(RAVEN_TAIL, RAVEN_TAIL[1:]):
            needs = {title_of(need) for need in ENCHANTING_DEPENDENCIES[ID_BY_TITLE[title]]}
            self.assertIn(previous, needs)
        # Pinnacle waits for both Sculkshelves (and the Gear chapter's Pinnacle tier).
        pinnacle = {title_of(need) for need in ENCHANTING_DEPENDENCIES["73E09ED46A94B812"]}
        self.assertEqual(pinnacle, {"Echoing Sculkshelf", "Soul-Touched Sculkshelf",
                                    "World Tier: Pinnacle"})

    def test_configured_levels_are_consistent(self) -> None:
        self.assertEqual(len(ENCHANTMENT_LEVELS), 117)
        raised = [key for key, (orig, top, _) in ENCHANTMENT_LEVELS.items() if top > orig]
        kept = [key for key, (orig, top, _) in ENCHANTMENT_LEVELS.items() if top == orig]
        lowered = [key for key, (orig, top, _) in ENCHANTMENT_LEVELS.items() if top < orig]
        self.assertEqual((len(raised), len(kept), lowered),
                         (84, 32, ["apothic_enchanting:miners_fervor"]))
        loot_off_original = [key for key, (orig, _, loot) in ENCHANTMENT_LEVELS.items()
                             if loot != orig]
        self.assertEqual(loot_off_original, ["apothic_enchanting:miners_fervor"])
        highest = max(top for _, top, _ in ENCHANTMENT_LEVELS.values())
        holders = [key for key, (_, top, _) in ENCHANTMENT_LEVELS.items() if top == highest]
        self.assertEqual(highest, 13)
        self.assertEqual(len(holders), 12)
        self.assertEqual(sum(1 for key in holders if key.startswith("tombstone:")), 11)
        self.assertIn("the_bumblezone:neurotoxins", holders)
        self.assertEqual(len([key for key in ENCHANTMENT_LEVELS
                              if key.startswith("minecraft:")]), 42)
        self.assertEqual(len([key for key in ENCHANTMENT_LEVELS
                              if key.startswith("apothic_enchanting:")]), 20)
        for enchantment, level in SHORT_ANSWER_LEVELS:
            self.assertEqual(ENCHANTMENT_LEVELS[enchantment][1], level)

    def test_task_and_reward_ids_are_namespaced(self) -> None:
        self.assertEqual(len(ENCHANTING_TASK_ITEMS), 55)
        self.assertEqual(len(ENCHANTING_REWARD_ITEMS), 34)
        for identifier in VERIFIED_IDS:
            self.assertRegex(identifier, r"^[a-z0-9_]+:[a-z0-9_/]+$")
        for identifier in DISENCHANTING_METHOD_ITEMS:
            self.assertIn(identifier, VERIFIED_IDS)
        self.assertEqual(len(DISENCHANTING_METHOD_ITEMS), 11)
        self.assertIn(UNTITLED_TASK_ITEM, ENCHANTING_TASK_ITEMS)


# --------------------------------------------------------------------------------------
# the guide: provenance and grounding rules
# --------------------------------------------------------------------------------------

class GuideTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(GUIDE_MD)
        cls.flat = flatten(cls.text)
        cls.lower = cls.flat.lower()


class TestGuideProvenanceAndGrounding(GuideTestCase):

    def test_guide_exists_and_is_substantial(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.text.strip()), 2000, "enchanting-guide.md looks like a stub")
        self.assertTrue(self.text.startswith("# Apothic Enchanting"))

    def test_guide_answers_the_beginner_question_first(self) -> None:
        headings = re.findall(r"^## (.+)$", self.text, re.MULTILINE)
        self.assertTrue(headings, "the guide has no sections")
        self.assertEqual(headings[0], "The short answer: how do I get the best enchants?")
        for heading in ("Provenance — everything here was read, not remembered",
                        "Grounding rules (read before repeating any of this)",
                        "How the chapter is shaped",
                        "Ceiling 1 — your World Tier caps Eterna",
                        "Ceiling 2 — the shelf ladder, in dependency order",
                        "Cross-references",
                        "What this page deliberately does not tell you"):
            self.assertIn(heading, headings)

    def test_guide_names_its_sources_and_pins_the_commit(self) -> None:
        for source in ("AllTheMods/ATM-10", "config/ftbquests/quests/chapters",
                       "lang/en_us/chapters", "config/crash_assistant/modlist.json",
                       "config/apotheosis/enchantments.cfg",
                       "config/ftbquests/quests/chapters/apothic_enchanting.snbt",
                       "config/ftbquests/quests/chapters/apotheosis_gear.snbt",
                       "CHANGELOG.md", "config/bcc-common.toml"):
            self.assertIn(source, self.text, f"the guide must name its source: {source}")
        self.assertIn(PACK_COMMIT, self.text)
        self.assertIn(PACK_COMMIT_FULL, self.text, "the commit link must use the full hash")
        self.assertIn("2026-09-22", self.text)
        self.assertIn("pack 8.2", self.text)
        self.assertIn("8.x", self.text, "the guide must tie 8.2 to the skill's 8.x stamp")

    def test_guide_carries_the_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "no recipes", "does not tell you", "never a guess",
                       "canvas, not as a numbered list", "in dependency order",
                       "stat figures are quest text, not formulas"):
            self.assertIn(needle, self.lower, f"missing grounding rule: {needle!r}")
        self.assertRegex(self.lower, r"never invented|not invented|never invent")
        self.assertIn("(To know the Levels needed you can check JEI or follow these Quests)",
                      self.flat, "the chapter's own pointer to JEI must be quoted")
        # Each rule must sit in the rules section itself, not just somewhere on the page.
        rules = flatten(section(self.text, "Grounding rules (read before repeating any of this)"))
        for rule in ("**The in-game quest book (FTB Quests) and JEI are authoritative.**",
                     "**Item ids and counts below are quoted from the config, never invented.**",
                     "**Stat figures are quest text, not formulas.**",
                     "**No recipes.**",
                     "**Titles are the config's.**",
                     "**Nothing here was invented, and nothing is added from memory.**"):
            self.assertIn(rule, rules, f"the grounding rules section must state {rule}")

    def test_guide_names_the_mods_from_the_modlist(self) -> None:
        for mod in ("Apotheosis 8.8.0", "Apothic Enchanting 1.6.2", "Apothic Attributes 2.10.1",
                    "Apothic Spawners 1.4.0", "Gateways To Eternity 5.1.0",
                    "Dis-Enchanting Table 5.0.2"):
            self.assertIn(mod, self.flat)


# --------------------------------------------------------------------------------------
# the guide: verified quests, the chapter's shape, the untitled quest
# --------------------------------------------------------------------------------------

class TestGuideQuests(GuideTestCase):

    def test_every_verified_title_is_listed(self) -> None:
        for title in ENCHANTING_QUESTS.values():
            if title:
                self.assertIn(title, self.flat, f"missing verified quest title: {title}")
        for title in GEAR_QUEST_LINKS.values():
            self.assertIn(title, self.flat, f"missing linked Gear quest: {title}")

    def test_every_task_item_tag_and_advancement_is_cited(self) -> None:
        for identifier in (ENCHANTING_TASK_ITEMS + ENCHANTING_TASK_TAGS
                           + ENCHANTING_TASK_ADVANCEMENTS):
            self.assertIn(f"`{identifier}`", self.text,
                          f"the guide must cite the config's task target {identifier}")
        for dimension in ENCHANTING_TASK_DIMENSIONS:
            self.assertIn(f"`dimension {dimension}`", self.text,
                          f"the guide must cite the dimension task {dimension}")

    def test_the_chapter_shape_matches_the_config(self) -> None:
        self.assertIn("| Quests in the chapter | **58** |", self.flat)
        self.assertIn("| Tasks in total | 65 (58 `item`, 5 `advancement`, 2 `dimension`) |",
                      self.flat)
        self.assertIn("4 — *Apothic Enchanting*, *Enchantment Library*, *Flimsy Ender Lead*, "
                      "*Gem Case*", self.flat)
        self.assertIn("57 of the 58 quests carry an explicit title", self.flat)
        self.assertIn('`dependency_requirement: "one_completed"`', self.flat)
        self.assertIn("2 — *A Gate*, *Another Gate*", self.flat)
        self.assertIn("6 — *Invaders/Bosses and World Tiers* and the five *World Tier:* quests",
                      self.flat)
        self.assertIn("group **Magic**", self.flat)
        self.assertIn("`order_index` 0", self.flat)

    def test_the_untitled_quest_is_marked_not_named(self) -> None:
        row = next((line for line in self.text.splitlines()
                    if f"`{UNTITLED_TASK_ITEM}`" in line and line.startswith("|")), "")
        self.assertTrue(row.startswith(f"| *{UNTITLED_MARKER}* |"),
                        "the untitled quest's row must carry the untitled marker")
        self.assertIn(UNTITLED_SUBTITLE, row)
        # The derived name may appear only inside the quest's own quoted text.
        self.assertNotIn("Tome of Extraction", bold_spans(self.flat))
        self.assertNotIn("Tome of Extraction", italic_spans(self.flat))
        self.assertIn('*"The Tome of Extraction is the Tome we are looking for!', self.flat)

    def test_the_spine_is_written_in_dependency_order(self) -> None:
        bullet = re.search(r"- \*\*The spine\*\*(.*?)(?=\n- \*\*)", self.text, re.DOTALL)
        self.assertIsNotNone(bullet, "the shape section must spell out the spine")
        assert bullet is not None
        spine_text = flatten(bullet.group(1))
        positions = []
        for step in SPINE:
            for title in step:
                self.assertIn(f"*{title}*", spine_text, f"the spine is missing {title!r}")
            positions.append(min(spine_text.index(f"*{title}*") for title in step))
        self.assertEqual(positions, sorted(positions), "the spine must stay in dependency order")
        tail = [spine_text.rindex(f"*{title}*") for title in RAVEN_TAIL]
        self.assertEqual(tail, sorted(tail))

    def test_the_ladder_table_follows_the_spine(self) -> None:
        ladder = section(self.text, "Ceiling 2 — the shelf ladder, in dependency order")
        rows = [row for header, body in markdown_tables(ladder) if header[0] == "Step"
                for row in body]
        self.assertEqual([row[0] for row in rows], [str(number) for number in range(1, 19)])
        for row, step in zip(rows, SPINE):
            for title in step:
                self.assertIn(f"**{title}**", row[1], f"ladder step {row[0]} must be {step}")

    def test_each_shelf_maximum_is_quoted(self) -> None:
        for title, quote in SHELF_MAXIMUM_QUOTES:
            self.assertIn(title, self.flat)
            self.assertIn(quote, self.flat, f"missing {title!r} maximum: {quote!r}")


# --------------------------------------------------------------------------------------
# the guide: World Tiers, the finished set-up, infusion windows
# --------------------------------------------------------------------------------------

class TestGuideCeilingsAndSetups(GuideTestCase):

    def test_world_tier_caps_are_tied_to_the_right_quests(self) -> None:
        tiers = section(self.text, "Ceiling 1 — your World Tier caps Eterna")
        for tier, cap, advancement, quest, subtitle in WORLD_TIERS:
            row = next((line for line in tiers.splitlines()
                        if line.startswith(f"| **{tier}** |")), "")
            self.assertTrue(row, f"missing World Tier row: {tier}")
            self.assertTrue(row.startswith(f"| **{tier}** | {cap} |"),
                            f"{tier} must cap Eterna at {cap}")
            if quest:
                self.assertIn(f'**{quest}** — *"{subtitle}"*', row)
            self.assertIn(f"`{advancement}`", tiers)
        short = section(self.text, "The short answer: how do I get the best enchants?")
        self.assertIn("30 on Haven, 45 on Frontier, 60 on Ascent, 75 on Summit, 100 on Pinnacle",
                      flatten(short))

    def test_the_gear_dependency_is_stated_precisely(self) -> None:
        self.assertIn("forcing the Frontier World Tier quest from Apotheosis Gear", self.flat)
        self.assertIn("its first steps do not; its World Tier gates do", self.flat)
        self.assertIn("This one is not required for the main shelf progression", self.flat)

    def test_the_best_setup_lists_its_five_tasks_in_order(self) -> None:
        finish = section(self.text, "The finish line")
        positions = []
        for item, count in BEST_SETUP_TASKS:
            row = f"| `{item}` | {count} |"
            self.assertIn(row, finish, f"Best Enchanting set-up must list {item} x{count}")
            positions.append(finish.index(row))
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Without the Enchanting Table of the Raven", finish)
        self.assertIn("every stat maxed out, every good Enchantment available", flatten(finish))
        self.assertIn("optional *for the set-up*", flatten(finish),
                      "the optional-vs-task mismatch must be flagged, not smoothed over")
        self.assertIn(GOD_FUSED_PEARL_WINDOW, flatten(finish))
        self.assertIn("without the need for shelves", flatten(finish))

    def test_infusion_windows_sit_next_to_their_quests(self) -> None:
        rows = [line for line in self.text.splitlines() if line.startswith("|")]
        for title, window in INFUSION_WINDOWS:
            matching = [row for row in rows if f"**{title}**" in row and window in row]
            self.assertTrue(matching, f"{title!r} must be quoted with its window {window!r}")

    def test_conflicting_setups_are_both_quoted_and_flagged(self) -> None:
        self.assertIn("2 Soul-Touched Sculkshelves, 3 Heart-Forged Seashelves, 8 Normal "
                      "Bookshelves, and 1 Geode-Encased Bookshelf of Stability", self.flat)
        self.assertIn("4 Echoing + 4 Soul-Touched Sculkshelves + 6 Geode shelves", self.flat)
        self.assertIn("two quests even suggest different set-ups for the same infusion",
                      self.flat)

    def test_steering_and_library_rules_are_quoted(self) -> None:
        for quote in ("by clicking the ? in the Top Right of the Enchantment Table's GUI",
                      "it will get rid of the increased chances of worse Enchantments",
                      "this Enchantment won't show up on Items or Books",
                      "Each Enchanting Clue will tell you 1 Enchantment",
                      "like Mending!",
                      "The max Level of Enchanted Book is determined by the highest Level of "
                      "Book you've put in.",
                      "1.1 Billion Points of each Book!"):
            self.assertIn(quote, self.flat)
        self.assertIn(f"**{XP_LEVELS_TOTAL} XP levels**", self.flat)


# --------------------------------------------------------------------------------------
# the guide: configured enchantment levels
# --------------------------------------------------------------------------------------

class TestGuideConfiguredLevels(GuideTestCase):

    def expected_row(self, enchantment: str) -> str:
        original, top, loot = ENCHANTMENT_LEVELS[enchantment]
        shown = f"**{top}**" if top != original else str(top)
        return f"| `{enchantment}` | {original} | {shown} | {loot} |"

    def test_every_vanilla_row_matches_the_config(self) -> None:
        for enchantment in ENCHANTMENT_LEVELS:
            if enchantment.startswith("minecraft:"):
                self.assertIn(self.expected_row(enchantment), self.text,
                              f"the {enchantment} row must match enchantments.cfg")

    def test_every_apothic_enchanting_row_matches_the_config(self) -> None:
        for enchantment in ENCHANTMENT_LEVELS:
            if enchantment.startswith("apothic_enchanting:"):
                self.assertIn(self.expected_row(enchantment), self.text,
                              f"the {enchantment} row must match enchantments.cfg")

    def test_no_level_row_disagrees_with_the_config(self) -> None:
        """Any `| \\`id\\` | n | n | n |` row in the guide must be exactly the config's."""
        for match in re.finditer(r"^\| `([a-z0-9_]+:[a-z0-9_]+)` \| (\d+) \| (\*\*)?(\d+)(\*\*)? "
                                 r"\| (\d+) \|$", self.text, re.MULTILINE):
            enchantment = match.group(1)
            self.assertIn(enchantment, ENCHANTMENT_LEVELS, f"unknown enchantment {enchantment}")
            self.assertEqual((int(match.group(2)), int(match.group(4)), int(match.group(6))),
                             ENCHANTMENT_LEVELS[enchantment], enchantment)

    def test_the_summary_claims_match_the_config(self) -> None:
        for claim in ("**117**", "**84 of the 117**", "**32** keep it",
                      "exactly **one** is lowered",
                      "`apothic_enchanting:miners_fervor`, originally 5, set to `Max Level` 1 "
                      "and `Max Loot Level` 1",
                      "`Max Loot Level` equals the original cap for every other entry",
                      "`Forced Level Cap` is `-1` (disabled) for every entry",
                      "13, held by twelve entries — eleven Corail Tombstone enchantments and "
                      "`the_bumblezone:neurotoxins`",
                      "Every vanilla (`minecraft:`) entry — 42",
                      "Apothic Enchanting's own 20 entries"):
            self.assertIn(claim, self.flat, f"missing or changed config claim: {claim!r}")
        short = flatten(section(self.text, "The short answer: how do I get the best enchants?"))
        for enchantment, level in SHORT_ANSWER_LEVELS:
            self.assertIn(f"`{enchantment}`", short)
        self.assertIn("`minecraft:sharpness` goes to **9** (originally 5)", short)
        self.assertIn("`minecraft:mending` stays **1**", short)

    def test_capturing_cross_check(self) -> None:
        self.assertEqual(ENCHANTMENT_LEVELS["apothic_spawners:capturing"], (3, 7, 3))
        self.assertIn("`apothic_spawners:capturing` is originally 3 with `Max Level` 7", self.flat)
        self.assertIn("the highest level you can normally get is VII (7).", self.flat)

    def test_the_guide_disclaims_formulas(self) -> None:
        self.assertIn("which eterna — or which shelves — the table needs before it offers a "
                      "given level", self.lower)
        self.assertIn("**Formulas.**", self.flat)


# --------------------------------------------------------------------------------------
# the guide: no invented names
# --------------------------------------------------------------------------------------

class TestGuideInventsNothing(GuideTestCase):

    def test_every_namespaced_id_is_verified(self) -> None:
        cited = set(re.findall(r"`([a-z0-9_]+:[a-z0-9_/.]+)`", self.text))
        self.assertGreater(len(cited), 100, "the id scan found suspiciously few ids")
        unverified = sorted(cited - VERIFIED_IDS)
        self.assertEqual(unverified, [], f"ids not verified against the pack config: {unverified}")

    def test_every_apothic_enchanting_id_is_a_task_reward_or_enchantment(self) -> None:
        cited = set(re.findall(r"`(apothic_enchanting:[a-z0-9_]+)`", self.text))
        allowed = (set(ENCHANTING_TASK_ITEMS) | set(ENCHANTING_REWARD_ITEMS)
                   | {key for key in ENCHANTMENT_LEVELS if key.startswith("apothic_enchanting:")})
        self.assertEqual(sorted(cited - allowed), [])

    def test_title_columns_hold_only_verified_titles(self) -> None:
        cells = column(self.text, lambda name: "verified" in name.lower()
                       and not name.startswith("Needs")
                       and ("title" in name.lower() or "quest" in name.lower()))
        cells += column(self.text, lambda name: name == "This chapter's quest that waits for it")
        self.assertGreater(len(cells), 40, "the title-column scan found too few cells")
        for cell in cells:
            names = bold_spans(cell)
            if not names:
                self.assertTrue(cell.startswith(f"*{UNTITLED_MARKER}*") or cell.startswith("—"),
                                f"title cell without a verified title or the marker: {cell!r}")
            for name in names:
                self.assertIn(name, VERIFIED_TITLES, f"unverified quest title: {name!r}")

    def test_needs_columns_name_exactly_the_configured_dependencies(self) -> None:
        """Every Needs cell names each configured dependency - and nothing else."""
        filler = re.compile(r"\(Apotheosis Gear\)|\bboth\b|\bnothing\b|a starting point|"
                            r"\band\b|\bor\b|[\s,/*()]")
        checked = 0
        for header, rows in markdown_tables(self.text):
            if "Verified quest title" not in header:
                continue
            needs = [index for index, name in enumerate(header)
                     if name.startswith("Needs") or name == "Also needs"]
            if not needs:
                continue
            title_index, needs_index = header.index("Verified quest title"), needs[0]
            for row in rows:
                titles = bold_spans(row[title_index])
                quest_ids = ([ID_BY_TITLE[title] for title in titles] if titles
                             else [UNTITLED_QUEST_ID])
                expected = {title_of(need) for quest_id in quest_ids
                            for need in ENCHANTING_DEPENDENCIES.get(quest_id, ())}
                if header[needs_index] == "Also needs":
                    expected.discard("Other Infusion Items")  # stated above that table
                cell = row[needs_index]
                for title in expected:
                    self.assertIn(title, cell, f"{titles or 'untitled'} must name {title!r}")
                remainder = cell
                for title in sorted(expected, key=len, reverse=True):
                    remainder = remainder.replace(title, "")
                self.assertEqual(filler.sub("", remainder), "",
                                 f"{titles or 'untitled'}: unverified text in {cell!r}")
                checked += 1
        self.assertGreaterEqual(checked, 30, "the Needs scan found too few rows")

    def test_chapter_column_holds_only_verified_chapters(self) -> None:
        cells = column(self.text, lambda name: name == "Chapter (verified)")
        self.assertTrue(cells)
        for cell in cells:
            name = cell.replace("**", "")
            self.assertIn(name, VERIFIED_CHAPTER_TITLES + ("Chapter 3",),
                          f"unverified chapter name: {cell!r}")

    def test_italic_titles_in_the_spine_and_tier_table_are_verified(self) -> None:
        spine = re.search(r"- \*\*The spine\*\*(.*?)(?=\n- \*\*)", self.text, re.DOTALL)
        assert spine is not None
        spans = italic_spans(flatten(spine.group(1)))
        spans += [span for cell in column(self.text, lambda name: name.startswith(
            "Shelf quests this chapter opens")) for span in italic_spans(cell)]
        self.assertGreater(len(spans), 30)
        for span in spans:
            self.assertIn(span, VERIFIED_TITLES, f"unverified quest title in italics: {span!r}")

    def test_task_titles_are_never_dressed_up_as_quest_titles(self) -> None:
        styled = set(bold_spans(self.flat)) | set(italic_spans(self.flat))
        for task_title in TASK_TITLES:
            if task_title in VERIFIED_TITLES:
                continue  # also a real quest title (e.g. "Armor Tomes")
            self.assertNotIn(task_title, styled,
                             f"task title {task_title!r} must not be styled as a quest title")

    def test_untitled_quests_elsewhere_stay_untitled(self) -> None:
        rows = [line for line in self.text.splitlines() if line.startswith("|")]
        for identifier in ("allthetweaks:mini_nether", "allthetweaks:mini_end",
                           "allthetweaks:mini_exit", "industrialforegoing:enchantment_factory"):
            row = next((line for line in rows if f"`{identifier}`" in line), "")
            self.assertIn(f"*{UNTITLED_MARKER}*", row, f"the {identifier} quest is untitled")
        self.assertGreaterEqual(self.flat.count(UNTITLED_MARKER), 8)


# --------------------------------------------------------------------------------------
# wiring: SKILL.md, sibling docs, the shipped example file
# --------------------------------------------------------------------------------------

class TestGuideWiring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read(SKILL_MD)
        cls.guide = read(GUIDE_MD)

    def test_skill_version_was_bumped(self) -> None:
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md frontmatter has no X.Y.Z version")
        assert match is not None
        self.assertGreaterEqual(tuple(int(part) for part in match.groups()), (1, 2, 0),
                                "adding the enchanting guide bumps the skill to 1.2.0+")

    def test_skill_md_routes_enchanting_questions_to_the_guide(self) -> None:
        path = "references/enchanting-guide.md"
        for heading in ("When to Use", "Research Grounding", "Behaviors",
                        "Completion Checklist"):
            self.assertIn(path, section(self.skill, heading),
                          f"SKILL.md's {heading!r} section must point at {path}")
        flat = flatten(self.skill)
        self.assertIn("config/apotheosis/enchantments.cfg", flat)
        self.assertIn("how do I get the best enchants?", flat)
        self.assertIn(PACK_COMMIT, flat)

    def test_sibling_docs_point_at_the_guide(self) -> None:
        for path in (PROGRESSION_MD, KEY_MODS_MD):
            self.assertIn("enchanting-guide.md", read(path),
                          f"{path.name} must point at the enchanting guide")
        for sibling in SIBLING_DOCS:
            self.assertIn(f"references/{sibling}", self.guide,
                          f"the guide must cross-reference {sibling}")

    def test_chapter_claims_match_the_shipped_example_file(self) -> None:
        chapters = {chapter["id"]: chapter for chapter in
                    json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))["chapters"]}
        expected = {
            "apothic_enchanting": ("Apothic Enchanting", "Magic", "magic"),
            "apotheosis_gear": ("Apotheosis Gear", "Tools and Gear", "early-game"),
            "apotheosis_2": ("Apothic Spawners", "Resources", "early-game"),
        }
        for chapter_id, (title, group, stage) in expected.items():
            chapter = chapters[chapter_id]
            self.assertEqual((chapter["title"], chapter["group"], chapter["stage"]),
                             (title, group, stage))
            self.assertIn(f"`{chapter_id}`", self.guide)
            self.assertIn(f"stage `{stage}`", self.guide)
        magic = [chapter_id for chapter_id, chapter in chapters.items()
                 if chapter["group"] == "Magic"]
        self.assertEqual(magic[0], CHAPTER_ID, "the guide calls it the Magic group's first chapter")
        self.assertIn("the first chapter of the Magic group", flatten(self.guide))


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_only_offline_stdlib_modules(self) -> None:
        found: "set[str]" = set()
        for line in Path(__file__).read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        self.assertEqual(found & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(found <= {"__future__", "json", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(found)}")


if __name__ == "__main__":
    unittest.main()
