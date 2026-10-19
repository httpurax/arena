#!/usr/bin/env python3
"""Checks that the boss guide honours the ATM10 quest-companion grounding rules.

`references/boss-guide.md` extends the boss inventory in
`references/boss-checklist.md` with a recommended fight order, arenas,
summoning gates, and the gear expectations the quest book itself states.
Every claim on that page was read out of the ATM-10 8.2 quest config
(AllTheMods/ATM-10, `main` commit `e5e3d1d83e`, 2026-09-22):

* `config/ftbquests/quests/chapters/*.snbt` — task types, entity/structure/
  dimension ids, `dependencies` links, and hidden-state bits;
* `config/ftbquests/quests/lang/en_us/chapters/*.snbt` — quest titles,
  subtitles, and the description text quoted on the page (Minecraft
  formatting codes stripped);
* `config/crash_assistant/modlist.json` — mod display names and versions.

The rules the page lives by, and that this suite enforces mechanically:

* only quest titles, quest ids, and item/entity/structure/dimension ids
  that appear in the config may appear on the page — anything else is an
  invented name and fails the run;
* a fight the book tracks by a trophy item, a drop item, or an
  `advancement` is never presented as a plain `kill`-task fight, and the
  fights the book does *not* implement are flagged as such;
* the Twilight Forest line is the one strict order (trophy dependencies);
  parallel lines stay parallel — claiming an order the config does not
  have is inventing a requirement;
* gear claims are either a config task, a tool tier quoted from quest
  text, or labelled *(judgement)*; no invented enchantment, weapon, or
  loadout may appear;
* "Hearts" figures are quest text and stay labelled as such;
* the only numbers resembling a location are the Chaos Islands hint
  quoted verbatim from its own quest.

Run with the standard library only, offline:

    python3 tests/test_boss_guide.py [-v]
"""

import re
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "boss-guide.md"
SKILL_MD = SKILL_DIR / "SKILL.md"

PINNED_COMMIT = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
UNTITLED_MARKER = "(no title in the config"

# Every quest id cited on the page, mapped to its English title and the
# chapter that contains it (config, `main` commit e5e3d1d83e, pack 8.2).
# "" records a quest with no title in the config; such a quest must be
# referred to by id only. Duplicated titles across chapters (there are
# several) are distinct quests — the id is the difference.
# Rows: quest id, English title, chapter.
VERIFIED_QUESTS = (
    ("00CB8D60E7831A57", 'Catacombs', "undergarden"),
    ("0107D516E038E0DB", 'Bring out your Dead', "twilight_forest"),
    ("0436DF3308681913", 'The Dead King', "iron_spells_and_spellbooks"),
    ("04440BB2EFFD6DD9", 'Mighty Meef Stroganoff', "twilight_forest"),
    ("0496E8E786262464", 'Overworld: Land of 3 4 5 bosses', "cataclysm"),
    ("0576C32B0FB360B0", 'Lunar Monstrosity', "eternal_starlight"),
    ("074EC1E636CD6605", 'Netherite Armor', "basic_armor"),
    ("07FDA46D83F8360D", 'Teleport Pad', "allthemodium"),
    ("08D1CC753F6B4283", 'Kill A Elder Guardian', "bounty_board"),
    ("08E4892F96828EC4", 'Sun Spirit', "aether"),
    ("09C82CDDA800D8C9", 'Kill The Wither', "bounty_board"),
    ("0B11EAB8D76529E0", 'Visit an Ancient City', "deeper_and_darker"),
    ("0B7F2B63D867D221", 'Necklace of the desert', "cataclysm"),
    ("0D2F07FC0F804223", 'Valkyrie Queen', "aether"),
    ("0ED7B25DC1AA767B", 'The Real Final Boss', "twilight_forest"),
    ("0F026D5A17CCCF51", 'Netherite Tier', "mainquestline_part_1"),
    ("0F3D51FFD2FE8DCB", 'To The Nether!', "mainquestline_part_1"),
    ("0F8F0F7880235BA2", 'Soul BlackSmith: Home of the Netherite Monstrosity', "cataclysm"),
    ("1054168AFD8520D4", 'Forgotten Guardian', "undergarden"),
    ("106D08542AAFA166", 'Locate and Destroy 14 Guardian Crystals', "draconic_evolution"),
    ("10AB188AC6FB24D3", 'Starlight Golem', "eternal_starlight"),
    ("13F77C38AC015E9F", 'Mountain Tower', "iron_spells_and_spellbooks"),
    ("144BB025516E0994", 'Vibranium Ingot', "allthemodium"),
    ("15FEA03A2CDBA33B", 'The Other', "allthemodium"),
    ("1682CED78D9D4BA7", 'Twilight Forest', "chapter_2_the_star"),
    ("17CA9D80D8EC3EF7", 'The Harbinger', "cataclysm"),
    ("17D7D34F519F7E5F", '', "ars_nouveau"),
    ("199932BF623A6785", 'Kill The Forgotten Guardian', "bounty_board"),
    ("1A23BBF444D17A63", 'Greater Dweller', "undergarden"),
    ("1C232674CD04024D", 'Welcome to the Undergarden!', "undergarden"),
    ("1C5EA7D62BAF2108", 'Abyssal Sacrifice', "cataclysm"),
    ("1EB04FE105ACA4BE", 'Heart of the Deep', "chapter_2_the_star"),
    ("201EE3566D4D3123", 'Allthemodium Ingot', "allthemodium"),
    ("21A0FD474FBB49F7", 'Ruined Citadel: Home of the Ender Guardian', "cataclysm"),
    ("24934231538B6492", 'Ancient Pyramid', "allthemodium"),
    ("24E124F12CFF2A50", 'The Slider', "aether"),
    ("26D6FC091B7A8B38", 'Silver Key', "aether"),
    ("2790EB2E347D28DE", '', "cataclysm"),
    ("27F62C4B42B16015", 'Aether Portal', "aether"),
    ("2951B1D7080C5EF9", 'Every Thorn has its Rose', "twilight_forest"),
    ("2A444F4CCC72545D", 'Abyssal Sacrifice', "chapter_2_the_star"),
    ("2B115519A21F9CB7", 'Ender Guardian', "cataclysm"),
    ("2CA9394459C24012", 'Kill A Rotbeast', "bounty_board"),
    ("2EC9668ED4EA47CB", 'Gearing Up', "mainquestline_part_1"),
    ("31BB7EB95CE73C1A", 'To the Snow Biomes!', "twilight_forest"),
    ("32992E3534B86521", 'Stage 1-3 Fire Dragon', "ice__fire"),
    ("33B1D3FD4C0B5514", 'Ancient Remnant', "cataclysm"),
    ("3531B28F14CF72A2", 'Evening The Scales', "twilight_forest"),
    ("36BCCF7395658A5C", 'Finding the Bosses', "eternal_starlight"),
    ("37355F60E45777FE", 'Orb of Prophecy', "eternal_starlight"),
    ("375F0A098589CF29", 'Golem Forge', "eternal_starlight"),
    ("3813F5C1760C3A79", 'Kill A Piglin Brute', "bounty_board"),
    ("392EAE8BE71510C1", 'End: Land of 1 lonely boss', "cataclysm"),
    ("395A33977B18B9AD", 'Ancient Knight', "iron_spells_and_spellbooks"),
    ("3D579A1F7EFEDD5C", 'Kill the Warden', "deeper_and_darker"),
    ("3DB036804AD70497", 'Bronze Key', "aether"),
    ("3DCF26B53AE1EBF6", 'The Dark Forest', "twilight_forest"),
    ("40786B63E2901D11", 'Cursed Garden', "eternal_starlight"),
    ("4193303999597249", 'Welcome to the Twilight Forest!', "twilight_forest"),
    ("420158B1736A1354", 'The Final Boss', "twilight_forest"),
    ("429785E8F64929CE", 'The Gatekeeper and The Gate', "eternal_starlight"),
    ("45EE60207C466D6C", 'Where is he?', "draconic_evolution"),
    ("4A079D40C0AF6BC3", 'Unobtainium Ingot', "allthemodium"),
    ("4A4C71C43519D5FE", 'Summoning The Wither', "mainquestline_part_1"),
    ("4B2146C9527C54E7", 'Allthemodium', "allthemodium"),
    ("4B95D48D7525FFAD", 'To the Swamps!', "twilight_forest"),
    ("4BD203AD481DDE8F", 'Meat Shredder', "chapter_2_the_star"),
    ("4BF7F82F1C8680B9", 'Bronze Dungeon', "aether"),
    ("4C23D7E3DC8327C2", 'Burn it!', "eternal_starlight"),
    ("4D822D92492E1F53", 'Aptrgangr', "cataclysm"),
    ("4DA0725E089D7C91", 'Ramification', "twilight_forest"),
    ("501A0AEEC73C0790", 'Piglich Heart Block', "chapter_2_the_star"),
    ("50C9CB8FB16E453D", 'Burning Arena: Home of the Ignis', "cataclysm"),
    ("52007C01B52F7295", '10 Victory Medals', "aether"),
    ("53154550397E9704", 'Netherite Monstrosity', "cataclysm"),
    ("55278DDC31951DA5", 'Strange Key', "cataclysm"),
    ("555ED1E39131D91B", 'Cryomancer', "iron_spells_and_spellbooks"),
    ("565376084F05ED6E", 'Nether: Land of 2 bosses', "cataclysm"),
    ("56DA46DC82F6665D", 'Kill The Wilden Chimera', "bounty_board"),
    ("573DD5834B321D0A", 'Acropolis: Home of Scylla', "cataclysm"),
    ("5825892699A8DCB7", 'The Aether', "aether"),
    ("58BD1063A19777DC", 'Visiting the Giants', "twilight_forest"),
    ("5900ADCC247CD5F9", 'Silver Dungeon', "aether"),
    ("5A5D4DFE4175FB42", 'Gold Dungeon', "aether"),
    ("5A955C0F53AED3ED", 'Chain of Souls', "chapter_2_the_star"),
    ("5B2FD54E425D5C9D", 'Void Forge', "chapter_2_the_star"),
    ("5BA986D7928BF09F", 'Piglich Boss', "allthemodium"),
    ("5C040191740A53C8", 'Your Highness', "bumblezone"),
    ("5C2CF51D28F84CBE", 'Kill the Chaos Guardian', "draconic_evolution"),
    ("5C6BA6BBEC75EB71", 'Gold Key', "aether"),
    ("5CBA8C89FE717B9C", 'Lamp of Cinders', "twilight_forest"),
    ("5DDC15AAFD2CAF47", 'Diamond Armor', "basic_armor"),
    ("5E287410EE969244", 'Shattered', "deeper_and_darker"),
    ("5E799B92358A8732", 'Ancient Metals', "mainquestline_part_1"),
    ("6187837A51BA09DC", 'Citadel', "iron_spells_and_spellbooks"),
    ("61C49BC2B384FB80", 'Finding The End', "mainquestline_part_1"),
    ("6314B892B569A0A5", 'Eternal Starlight', "eternal_starlight"),
    ("641888DC7BC40AA9", 'Evoker Fort', "iron_spells_and_spellbooks"),
    ("6800E0113DE9A4DB", 'Dragons and their Stages', "ice__fire"),
    ("688C911ECFB2F134", 'Tears of Fire', "twilight_forest"),
    ("689F32883C4E9502", 'Cataclysm', "cataclysm"),
    ("68B44B9E939F4228", 'Archevoker', "iron_spells_and_spellbooks"),
    ("69A517AB8A801939", 'Kill The Wither', "mainquestline_part_1"),
    ("6B8F2E05429C185F", 'Chaos Shard{s}', "draconic_evolution"),
    ("6C4B93FE64BD418D", 'The Undergarden', "undergarden"),
    ("6C5F9D0D447EFB9C", 'Allthemodium Armor', "basic_armor"),
    ("6D09511D64DDC282", 'Kill The Warden', "mainquestline_part_1"),
    ("6DB5732177AABB87", 'Catacombs', "iron_spells_and_spellbooks"),
    ("6E38CF6E7360E9CA", 'Heart of the Deep', "deeper_and_darker"),
    ("6E970CF05B96EB20", 'Powering down', "eternal_starlight"),
    ("6EDAB29FBD3C60A3", 'Visit The Deep Dark!', "mainquestline_part_1"),
    ("6EE5BE5693E8ACE4", 'The End', "mainquestline_part_1"),
    ("6F76DA3BBAE8337B", 'Unobtainium Armor', "basic_armor"),
    ("6FD41DF7704466A4", 'Clear Skies', "twilight_forest"),
    ("7026E46FD8B3A81D", 'Hydra Slayer', "twilight_forest"),
    ("70FD8856BFCD9AEE", 'Rotbeast', "undergarden"),
    ("71055E7BBB337C4D", 'Maledictus', "cataclysm"),
    ("713006AB89E43C6D", 'Scylla', "cataclysm"),
    ("728BE1816DA23DC0", 'Kill The Ender Dragon', "bounty_board"),
    ("72DDA413D73E3235", 'Vibranium Armor', "basic_armor"),
    ("734411D931A8CDBF", 'Kill A Ravager', "bounty_board"),
    ("746DE905D45A396C", 'The Leviathan', "cataclysm"),
    ("765CD913CC3896B2", 'Stage 4-5 Fire Dragon', "ice__fire"),
    ("76F14C2B866B4EAD", 'The Otherside', "deeper_and_darker"),
    ("774D61FEFABEFD9A", 'Shriek Worm', "deeper_and_darker"),
    ("792990DC06DB98F9", 'Eternal Starlight', "chapter_2_the_star"),
    ("7AED8FD7FB023AD8", 'Nether Star', "cataclysm"),
    ("7B21D2FAD5F3246A", 'Ice and Fire', "ice__fire"),
    ("7D1A27CBF1508712", 'Snow Queen Trophy', "chapter_2_the_star"),
    ("7D57A14810BC0CBE", 'Ignis', "cataclysm"),
    ("7F4963FCAE5337EC", 'Burning Ashes', "cataclysm"),
)

# Every quoted quest title is also a verified string.
VERIFIED_TITLES = frozenset(title for _, title, _ in VERIFIED_QUESTS if title)

# Every namespaced id the page may print: task items, kill targets,
# structure/dimension ids, and advancement ids from the config — values
# as they appear as config strings.
VERIFIED_IDS = frozenset({
    "aether:bronze_dungeon",
    "aether:bronze_dungeon_key",
    "aether:gold_dungeon",
    "aether:gold_dungeon_key",
    "aether:silver_dungeon",
    "aether:silver_dungeon_key",
    "aether:slider",
    "aether:sun_spirit",
    "aether:the_aether",
    "aether:valkyrie_queen",
    "aether:victory_medal",
    "allthemodium:allthemodium_ingot",
    "allthemodium:ancient_pyramid",
    "allthemodium:piglich_heart",
    "allthemodium:piglich_heart_block",
    "allthemodium:teleport_pad",
    "allthemodium:the_other",
    "ars_nouveau:archmage_spell_book",
    "ars_nouveau:wilden_boss",
    "cataclysm:abyssal_sacrifice",
    "cataclysm:acropolis",
    "cataclysm:ancient_factory",
    "cataclysm:aptrgangr",
    "cataclysm:burning_arena",
    "cataclysm:burning_ashes",
    "cataclysm:cursed_pyramid",
    "cataclysm:frosted_prison",
    "cataclysm:meat_shredder",
    "cataclysm:necklace_of_the_desert",
    "cataclysm:ruined_citadel",
    "cataclysm:soul_black_smith",
    "cataclysm:strange_key",
    "cataclysm:sunken_city",
    "cataclysm:void_forge",
    "deeperdarker:heart_of_the_deep",
    "deeperdarker:otherside",
    "deeperdarker:shattered",
    "deeperdarker:shriek_worm",
    "draconicevolution:chaos_shard",
    "draconicevolution:draconic_guardian",
    "draconicevolution:infused_obsidian",
    "eternal_starlight:chain_of_souls",
    "eternal_starlight:cursed_garden",
    "eternal_starlight:energy_block",
    "eternal_starlight:golem_forge",
    "eternal_starlight:lunar_monstrosity",
    "eternal_starlight:orb_of_prophecy",
    "eternal_starlight:portal_ruins",
    "eternal_starlight:saltpeter_matchbox",
    "eternal_starlight:seeking_eye",
    "eternal_starlight:starlight",
    "eternal_starlight:starlight_golem",
    "iceandfire:cyclops_cave",
    "iceandfire:dragonbone",
    "iceandfire:fire_dragon_blood",
    "iceandfire:fire_dragon_cave",
    "iceandfire:fire_dragon_roost",
    "iceandfire:gorgon_temple",
    "iceandfire:hydra_cave",
    "iceandfire:ice_dragon_cave",
    "iceandfire:ice_dragon_roost",
    "iceandfire:lightning_dragon_cave",
    "iceandfire:lightning_dragon_roost",
    "iceandfire:siren_island",
    "irons_spellbooks:archevoker",
    "irons_spellbooks:catacombs",
    "irons_spellbooks:citadel",
    "irons_spellbooks:citadel_keeper",
    "irons_spellbooks:cryomancer",
    "irons_spellbooks:dead_king",
    "irons_spellbooks:evoker_fort",
    "irons_spellbooks:mountain_tower",
    "minecraft:adventure/root",
    "minecraft:ancient_city",
    "minecraft:deep_dark",
    "minecraft:diamond",
    "minecraft:elder_guardian",
    "minecraft:end/dragon_egg",
    "minecraft:ender_dragon",
    "minecraft:ender_eye",
    "minecraft:flint_and_steel",
    "minecraft:glowstone",
    "minecraft:nether_star",
    "minecraft:netherite_ingot",
    "minecraft:obsidian",
    "minecraft:overworld",
    "minecraft:soul_sand",
    "minecraft:story/enter_the_nether",
    "minecraft:the_end",
    "minecraft:the_nether",
    "minecraft:warden",
    "minecraft:water_bucket",
    "minecraft:wither",
    "minecraft:wither_skeleton_skull",
    "the_bumblezone:the_queens_desire/the_beginning",
    "twilightforest:alpha_yeti_trophy",
    "twilightforest:blue_castle_door",
    "twilightforest:hydra_trophy",
    "twilightforest:knight_phantom_trophy",
    "twilightforest:lich_trophy",
    "twilightforest:maze_map",
    "twilightforest:minoshroom_trophy",
    "twilightforest:naga_trophy",
    "twilightforest:pink_castle_door",
    "twilightforest:quest_ram_trophy",
    "twilightforest:raw_meef",
    "twilightforest:root",
    "twilightforest:snow_queen_trophy",
    "twilightforest:thorn_rose",
    "twilightforest:ur_ghast_trophy",
    "twilightforest:violet_castle_door",
    "twilightforest:yellow_castle_door",
    "undergarden:catacombs",
    "undergarden:catalyst",
    "undergarden:forgotten_guardian",
    "undergarden:greater_dweller",
    "undergarden:rotbeast",
    "undergarden:undergarden",
})

# Bold runs that are prose (boss names, labels, asides), never quest
# titles in bold. Anything else bolded fails.
PROSE_BOLD = frozenset({
    '"Hearts" figures are quest text, quoted.',
    'A task gate (verified).',
    'A tool tier named in quest text (verified quote).',
    'All the Mods 10',
    'Alpha Yeti',
    'An explicit expectation sentence (verified quote).',
    'Auroral has no boss in the config.',
    'Bosses the book does not track.',
    "Cataclysm's eight last, in any order the player likes",
    'Chaos Guardian',
    'Coordinates, distances, and spawn chances.',
    'Drop tables and respawn rules.',
    'Ender Dragon — the End branch.',
    'Full fight mechanics.',
    'Gear means what the book states, not a loadout.',
    'How the list was built.',
    'Hydra',
    "Iron's Spells 'n Spellbooks",
    'Knight Phantoms',
    'Loadouts.',
    'Mid-game exploration, in any order',
    'Minoshroom',
    'Naga',
    'No coordinates, no recipes.',
    'Nothing here was invented, and nothing is added from memory.',
    'Order is verified only where a dependency link or quest sentence states it.',
    'Piglich',
    'Slider',
    'Snow Queen',
    'Tactics are quoted or labelled.',
    "The Aether's three dungeons, in any order",
    'The Bee Queen gives quests; she is not fought.',
    'The Final Boss is not a boss.',
    'The Gatekeeper is a gate, not a kill.',
    "The Other, once Chapter 2's Teleport Pad exists",
    'The Twilight Forest line, strictly in its own order',
    'The in-game quest book (FTB Quests) and JEI are authoritative.',
    "Titles and ids are the config's, quoted.",
    'Trader and villager "bounties" are jokes, not bosses.',
    'Twilight Lich',
    'Ur-Ghast',
    'Vanilla first',
    'Warden — the Deep Dark branch.',
    'What this page is.',
    'Wilden Chimera',
    'Wither — the summon-it-yourself branch.',
    'judgement',
    'pack 8.2',
    'verified',
    'yes — Chain of Souls',
    'yes — Dragon Soul',
    'yes — Oblivion Shard',
    'yes — Void Forge',
    'yes — Void Forge / Meat Shredder',
})

EXPECTED_SECTIONS = (
    "## Provenance — everything here was read, not remembered",
    "## Grounding rules (read before repeating any of this)",
    "## The short answer: fight them in this order",
    "## How to read \"the gear the book expects\"",
    "## The fight order at a glance",
    "## Vanilla first: Chapter 1's three branches",
    "## The Twilight Forest: the one strict order",
    "## The Aether: three dungeons, no order between them",
    "## Mid-game exploration: Undergarden, Eternal Starlight, Iron's Spells, and the Wilden Chimera",
    "## The Other: Piglich and Ice and Fire",
    "## Endgame: Cataclysm's eight and the Chaos Guardian",
    "## If you only want the ATM Star",
    "## Not a fight, not implemented, or not a boss",
    "## Related pages",
    "## What this page deliberately does not tell you",
)

# (chapter file, quest count) pairs the provenance and section headers cite.
CITED_CHAPTER_COUNTS = (
    ("mainquestline_part_1", 36), ("bounty_board", 50),
    ("twilight_forest", 56), ("aether", 73), ("cataclysm", 110),
    ("deeper_and_darker", 45), ("undergarden", 82),
    ("eternal_starlight", 193), ("allthemodium", 54),
    ("draconic_evolution", 140), ("iron_spells_and_spellbooks", 103),
    ("ars_nouveau", 130), ("ice__fire", 87), ("chapter_2_the_star", 128),
    ("basic_armor", 128),
)

# The Twilight trophy line, in the verified kill-order dependency chain
# (config, `main` commit e5e3d1d83e).
TWILIGHT_ORDER = (
    "3531B28F14CF72A2",  # Naga
    "0107D516E038E0DB",  # Twilight Lich
    "04440BB2EFFD6DD9",  # Minoshroom
    "7026E46FD8B3A81D",  # Hydra
    "3DCF26B53AE1EBF6",  # Knight Phantoms
    "688C911ECFB2F134",  # Ur-Ghast
    "31BB7EB95CE73C1A",  # Alpha Yeti
    "6FD41DF7704466A4",  # Snow Queen
)

# The Cataclysm eight in the page's stated (judgement) order: ascending
# quoted Hearts figure. Titles, not ids, because the detail section is
# prose.
CATACLYSM_HEARTS_ORDER = (
    "Ancient Remnant", "The Harbinger", "The Leviathan", "Ender Guardian",
    "Ignis", "Maledictus", "Scylla", "Netherite Monstrosity",
)

# Glance-table row number -> the quest id that tracks the fight.
GLANCE_ROWS = {
    1: "728BE1816DA23DC0", 2: "69A517AB8A801939", 3: "3D579A1F7EFEDD5C",
    4: "3531B28F14CF72A2", 5: "0107D516E038E0DB", 6: "04440BB2EFFD6DD9",
    7: "7026E46FD8B3A81D", 8: "3DCF26B53AE1EBF6", 9: "688C911ECFB2F134",
    10: "31BB7EB95CE73C1A", 11: "6FD41DF7704466A4", 12: "24E124F12CFF2A50",
    13: "0D2F07FC0F804223", 14: "08E4892F96828EC4", 15: "1054168AFD8520D4",
    16: "0576C32B0FB360B0", 17: "10AB188AC6FB24D3", 18: "0436DF3308681913",
    19: "56DA46DC82F6665D", 20: "5BA986D7928BF09F", 21: "765CD913CC3896B2",
    22: "33B1D3FD4C0B5514", 23: "17CA9D80D8EC3EF7", 24: "746DE905D45A396C",
    25: "2B115519A21F9CB7", 26: "7D57A14810BC0CBE", 27: "71055E7BBB337C4D",
    28: "713006AB89E43C6D", 29: "53154550397E9704", 30: "5C2CF51D28F84CBE",
}

# Glance-table row number -> Hearts cell text normalised for whitespace
# and citation noise. These are quotations of quest text.
GLANCE_HEARTS = {
    1: "200", 2: "300", 3: "500", 4: "—", 5: "—", 6: "—", 7: "—",
    8: "—", 9: "—", 10: "—", 11: "—", 12: "400", 13: "500", 14: "—",
    15: "80", 16: "200", 17: "220", 18: "500", 19: "—", 20: "9999",
    21: "as a Warden (quest text)", 22: "2,700", 23: "4,680",
    24: "6,400", 25: "6,660", 26: "7,200", 27: "8,400",
    28: "around 8658", 29: "up to 9,600",
    30: "two health bars (quest text)",
}

# Sentences quoted verbatim from quest descriptions in the config
# (formatting codes stripped when the page was written).
KEY_QUOTES = (
    "Here you'll need to follow a strict order of Bosses to kill and progress!",
    "There is no certain pattern of which bosses to kill first, but some are stronger than others, and some give loot that will help against the others.",
    "In this modpack, quests are optional. Mods are not gated behind completing any quests!",
    "This quest only requires you to make one Diamond tool or armor piece, but it's probably good to get a full set!",
    "probably some pretty good armor",
    "By now you should have Netherite and have killed all the bosses Minecraft has.",
    "You'll have to break the End Crystals on the pillars as they heal her, in order to kill her!",
    "She has 200 Hearts and can attack with Fireballs or ramming into you.",
    "When taken to half Health he will gain a shield against Projectiles and will need to be killed with a Sword or Axe.",
    "It explodes. A lot. Don't do this near your base.",
    "he is Blind. He can only find you with Sound, or Smell if you are close enough!",
    "The first boss you'll have to kill on your adventure in the Twilight Forest can be found within the Courtyard.",
    "To unlock the next area, you must eat it.",
    "Ranged attacks aren't as effective, meaning you'll need to get up close and personal.",
    "The Ur-Ghast is recommended to kill with a ranged weapon.",
    "You'll only be able to hit her top half, as she's protected by Ice.",
    "You'll need to kill the Alpha Yeti in order to enter the Glacier Biome.",
    "the easiest and simplest Dungeon.",
    "his Eyes will turn Red and he'll move faster",
    "They have 50 Hearts each and are Neutral until you Hit them.",
    "Hit the Ice Crystals at him to Freeze him! Once Frozen you can finally Hit him.",
    "you'll need a Pickaxe to deal Damage",
    "The better the Pickaxe the more Damage.",
    "The Forgotten Guardian is a massive Golem made of Forgotten Ingots.",
    "You'll need a Forgotten Pickaxe or Allthemodium Pickaxe to Mine the Dreadrock in the way.",
    "Careful, they are very tough.",
    "The Gatekeeper will also deem you worthy if you have defeated the Ender Dragon, and allow you to skip the duel.",
    "will only take 1 damage from each hit unless you use Fire.",
    "Right Click the Energy Blocks when they turn blue.",
    "He has 500 Hearts and has an actual Boss Bar (and music).",
    "He needs to be summoned through a ritual then fought!",
    "To create the final tier of your Spellbook, you'll need to have killed the Wilden Chimera.",
    "He has 9999 Hearts and currently has no attacks but trust me when he does they will be devastating!",
    "You'll need 9 of them dead to make a Block of it...",
    "Stages 1-3 will spawn in Roosts while Stage 4 and 5 spawn in Caves. Only 4 and 5 will Drop Eggs.",
    "If you want to fight these massive Dragons you will need the best Gear, Enchants, and Potions.",
    "a Pickaxe that is Netherite Tier or higher",
    "Right Click the Ancient Remnant with the Necklace of Desert to resurrect it!",
    "If you hit his Necklace he will be knocked down for a little bit",
    "To power up The Harbinger you'll need a Nether Star, which you get from killing the Wither.",
    "he is weak to the EMPs!",
    "invincible outside of Water",
    "his Mask will break",
    "He will regenerate Hearts when no Player is nearby.",
    "after a very difficult and long boss fight",
    "Go to the End at an X/Z coordinate that is a multiple of 10k.",
    "Destroying these crystals is no easy task without a Draconic weapon.",
    "he has two health bars both need to get taken to 0 to get the Chaos Shards.",
    "...is not implemented.",
    "Welcome to Ice and Fire! Now in The Other",
)

# Names that belong to other packs, other versions, or plausible-sounding
# gaps. If one is in the guide it was invented, because the config does
# not contain it. Checked as prose, case-sensitively where sensible.
FORBIDDEN_BOSSES_OR_MODS = (
    # bosses / dimensions from other packs or versions
    "Chaos Dragon", "Mutant Ender Dragon", "Wither Storm",
    "The Midnight", "The Betweenlands", "Blue Skies Dimension",
    "Angel Ring", "Elytra", "Totem of Undying", "Netherite Sword",
    "Dragon Heart", "Enchanted Apple",
    # invented dimension / structure ids the page must never print
    "twilightforest:twilight_forest", "minecraft:ocean_monument",
    "minecraft:stronghold", "cataclysm:altar_of_fire",
    "cataclysm:cursed_tombstone", "minecraft:woodland_mansion",
)

# Concrete gear the page must never prescribe; the config names none of
# it for these fights. Generic quoted words ("Sword or Axe") stay allowed.
FORBIDDEN_GEAR_PATTERNS = (
    r"\bCrossbow\b",
    r"\bTrident\b",
    r"\bFirework(s)?\b",
    r"\b(Golden|Enchanted Golden) Apple(s)?\b",
    r"\bProtection (IV|4|III|3)\b",
    r"\bSharpness (V|5|IV|4)\b",
    r"\b(Power|Infinity|Mending|Unbreaking) (V|5|IV|4|III|3)\b",
    r"\bbring a(n)? (sword|bow|axe|shield)\b",
)

ID_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_/:])([a-z][a-z0-9_]*:[a-z0-9_]+(?:/[a-z0-9_]+)*)"
    r"(?![A-Za-z0-9_/:-])"
)
QUEST_ID_TOKEN = re.compile(r"\b[0-9A-F]{16}\b")
BANNED_SUBSTRINGS = (
    "TODO", "TBD", "FIXME", "XXX",
    "as an AI", "language model",
    "session summary", "previous session",
)

# The three Cataclysm dimension-quest titles whose numbers are part of
# the title, not a boss count claim.
NUMBERY_TITLES = (
    "Nether: Land of 2 bosses", "Overworld: Land of 3 4 5 bosses",
    "End: Land of 1 lonely boss",
)


def flatten(text):
    return re.sub(r"\s+", " ", text)


def load(guide=True):
    path = DOC if guide else SKILL_MD
    text = path.read_text(encoding="utf-8")
    return text, flatten(text)


def glance_rows(text):
    """Numbered fight-order table rows: number -> list of cell strings."""
    rows = {}
    for line in text.splitlines():
        match = re.match(r"\| (\d+) \|", line)
        if match:
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows[int(match.group(1))] = cells
    return rows


class BossGuideGuardrailsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text, cls.flat = load()
        cls.skill, cls.skill_flat = load(guide=False)

    def test_doc_exists_and_is_substantial(self):
        self.assertTrue(DOC.is_file())
        self.assertGreater(len(self.text), 20000)

    def test_page_dates_and_sources_itself(self):
        for needle in (
            "AllTheMods/ATM-10",
            PINNED_COMMIT,
            "e5e3d1d83e",
            "pack 8.2",
            "8.x",
            'modpackVersion = "8.2"',
            "66 chapter files (4,790 quests)",
            "213 `kill` tasks",
            "config/ftbquests/quests/chapters/*.snbt",
            "config/ftbquests/quests/lang/en_us/chapters/*.snbt",
            "config/crash_assistant/modlist.json",
        ):
            self.assertIn(needle, self.flat)
        for chapter, count in CITED_CHAPTER_COUNTS:
            self.assertIn(f"`{chapter}`, {count} quests", self.flat)

    def test_grounding_rules_are_stated_up_front(self):
        self.assertIn("## Grounding rules (read before repeating any of this)",
                      self.text)
        for needle in (
            "The in-game quest book (FTB Quests) and JEI are authoritative",
            "If the player's book differs, his book wins",
            "Titles and ids are the config's, quoted.",
            "Tactics are quoted or labelled.",
            "Order is verified only where a dependency link or quest sentence states it.",
            "Gear means what the book states, not a loadout.",
            "No coordinates, no recipes.",
            "Nothing here was invented, and nothing is added from memory.",
            "never a plausible-sounding guess",
            "the in-game quest book is authoritative",
        ):
            self.assertIn(needle, self.flat)

    def test_expected_sections_in_order(self):
        positions = []
        for heading in EXPECTED_SECTIONS:
            index = self.text.find(heading)
            self.assertGreaterEqual(index, 0, f"missing section {heading!r}")
            positions.append(index)
        self.assertEqual(positions, sorted(positions))

    def test_every_verified_quest_is_cited_with_title_and_id(self):
        for quest_id, title, chapter in VERIFIED_QUESTS:
            where = f"{title!r} ({quest_id}, {chapter})"
            self.assertIn(quest_id, self.text, where)
            if title:
                self.assertIn(title, self.flat, where)

    def test_untitled_quests_are_marked_never_named(self):
        untitled = [qid for qid, t, _ in VERIFIED_QUESTS if not t]
        self.assertEqual(len(untitled), 2)
        for quest_id in untitled:
            index = self.text.index(quest_id)
            window = flatten(self.text[max(0, index - 200): index + 200])
            self.assertIn("untitled", window.lower(),
                          f"{quest_id}: not flagged as untitled near its id")

    def test_titles_never_appear_in_bold(self):
        no_code = re.sub(r"`[^`]*`", " ", self.text)
        for run in re.findall(r"\*\*(.+?)\*\*", no_code, re.DOTALL):
            run = flatten(run).strip()
            self.assertTrue(
                run in PROSE_BOLD or run in VERIFIED_TITLES,
                f"bold run {run!r} is neither prose nor a verified title",
            )

    def test_no_invented_quest_ids(self):
        cited = set(QUEST_ID_TOKEN.findall(self.text))
        known = {qid for qid, _, _ in VERIFIED_QUESTS}
        self.assertEqual(cited - known, set(),
                         "the page cites quest ids outside the verified set")

    def test_no_invented_namespaced_ids(self):
        found = {m.group(1) for m in ID_TOKEN.finditer(self.text)}
        invented = sorted(found - VERIFIED_IDS)
        self.assertEqual(invented, [],
                         "namespaced ids not present in the config: "
                         f"{invented}")

    def test_no_invented_bosses_mods_or_gear(self):
        for name in FORBIDDEN_BOSSES_OR_MODS:
            self.assertNotIn(name, self.text)
        for pattern in FORBIDDEN_GEAR_PATTERNS:
            self.assertIsNone(re.search(pattern, self.text), pattern)

    def test_no_coordinates_beyond_the_quoted_hint(self):
        self.assertEqual(
            self.flat.count("multiple of 10k"), 1,
            "the config's one numeric location hint is quoted exactly once",
        )
        self.assertIsNone(
            re.search(r"\b-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\b", self.text))
        self.assertIsNone(re.search(r"(?mi)^.*\bY\s+-?\d+\b", self.text))
        self.assertIsNone(re.search(r"(?i)\b\d+\s*blocks (away|north|south|east|west)\b", self.text))

    def test_no_invented_boss_count_claims(self):
        scan = self.flat
        for title in NUMBERY_TITLES:
            scan = scan.replace(title, " ")
        self.assertIsNone(re.search(r"(?i)\b\d+\s+bosses\b", scan))
        self.assertIsNone(
            re.search(r"(?i)\b(there are|exactly|a total of) \d+ (bosses|fights)\b",
                      scan))

    def test_glance_table_rows_are_sequential_and_verified(self):
        rows = glance_rows(self.text)
        self.assertEqual(sorted(rows), list(range(1, 31)))
        by_id = {qid: title for qid, title, _ in VERIFIED_QUESTS}
        for number, quest_id in GLANCE_ROWS.items():
            row = " | ".join(rows[number])
            self.assertIn(f"`{quest_id}`", row)
            self.assertIn(by_id[quest_id], row)

    def test_glance_table_hearts_match_the_config_quotes(self):
        rows = glance_rows(self.text)
        for number, expected in GLANCE_HEARTS.items():
            hearts = " ".join(rows[number][4].split())
            self.assertEqual(hearts, expected,
                             f"row {number}: Hearts cell")

    def test_twilight_line_is_presented_in_its_verified_order(self):
        positions = [self.text.index(f"`{qid}`") for qid in TWILIGHT_ORDER]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("strict order of Bosses to kill and progress", self.flat)
        self.assertIn("tracked by its trophy item, never by a `kill` task",
                      self.flat)

    def test_parallel_lines_are_not_given_a_false_order(self):
        for needle in (
            "no order between them",
            "in any order",
            "the book orders nothing here",
            "no certain pattern of which bosses to kill first",
        ):
            self.assertIn(needle, self.flat)

    def test_cataclysm_eight_follow_the_stated_hearts_order(self):
        section = self.flat.split("## Endgame:", 1)[1]
        positions = [section.index(f"**{title}**")
                     for title in CATACLYSM_HEARTS_ORDER]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Defeat all Cataclysm bosses", self.flat)
        self.assertIn("`2790EB2E347D28DE`", section)

    def test_fights_are_not_mislabelled_as_kill_tasks(self):
        for needle in (
            "tracked by `allthemodium:piglich_heart`, not a kill task",
            "whose task is the drop item `allthemodium:piglich_heart`, not a kill",
            "No quest tasks killing the Gatekeeper",
            "`advancement` is never rewritten as a `kill` task",
            "task `dimension eternal_starlight:starlight`",
        ):
            self.assertIn(needle, self.flat)
        # The Final Boss collects door blocks; the page says so plainly.
        self.assertIn("The Final Boss is not a boss.", self.flat)
        self.assertIn("...is not implemented.", self.flat)
        # The Bee Queen and Auroral stay in the not-a-fight section.
        self.assertIn("*Your Highness* (`5C040191740A53C8`)", self.flat)
        self.assertIn("no `kill` task at all", self.flat)

    def test_key_quotes_survive_verbatim(self):
        for quote in KEY_QUOTES:
            self.assertIn(quote, self.flat)

    def test_gear_claims_stay_inside_the_config(self):
        for needle in (
            "A task gate (verified).",
            "A tool tier named in quest text (verified quote).",
            "An explicit expectation sentence (verified quote).",
            "The book almost never requires armour for a boss.",
            "Never invent an enchantment, a weapon, or a protection level the config does not name.",
            "No armour task gates any of them",
            "No enchantment, weapon, or potion is recommended beyond the items and tool tiers the quests themselves name.",
        ):
            self.assertIn(needle, self.flat)
        self.assertGreaterEqual(self.flat.lower().count("(judgement)"), 8)
        self.assertGreaterEqual(self.flat.lower().count("*approximate*"), 3)

    def test_star_subset_is_the_verified_one(self):
        section = self.flat.split("## If you only want the ATM Star", 1)[1]
        section = section.split("## Not a fight", 1)[0]
        for needle in (
            "Snow Queen Trophy", "Heart of the Deep", "Chain of Souls",
            "Piglich Heart Block", "Abyssal Sacrifice", "Void Forge",
            "Meat Shredder", "Oblivion Shard", "Wither's Compass",
            "Dragon Soul",
        ):
            self.assertIn(needle, section)
        self.assertIn("does not need most of this page", section)

    def test_mod_versions_are_stated_as_in_the_pack(self):
        for needle in (
            "The Twilight Forest 4.8.3345",
            "The Aether 1.5.10",
            "The Undergarden 0.9.6",
            "Eternal Starlight 0.9.1",
            "Allthemodium 3.0.1",
            "Draconic Evolution 3.1.4.633",
            "Iron's Spells 'n Spellbooks 1.21.1-3.16.3",
            "Ars Nouveau 5.13.1",
            "Ice And Fire Community Edition 2.0-beta.17",
            "L_Ender's Cataclysm 1.21.1 3.33",
        ):
            self.assertIn(needle, self.flat)

    def test_cross_references_exist(self):
        for page in (
            "boss-checklist.md", "dimension-guide.md",
            "atm-star-checklist.md", "bounty-board-checklist.md",
            "armor-tools-ladder.md", "progression.md",
            "mob-farm-progression.md",
        ):
            self.assertIn(f"references/{page}", self.flat)

    def test_no_placeholders_or_session_leakage(self):
        for bad in BANNED_SUBSTRINGS:
            self.assertNotIn(bad, self.text)
        self.assertNotRegex(self.text, r"(?i)copyright|all rights reserved")

    def test_skill_md_wires_the_boss_guide(self):
        self.assertGreaterEqual(
            self.skill.count("references/boss-guide.md"), 3,
            "SKILL.md should reference the boss guide at least three times",
        )
        for needle in (
            "in what order",
            "references/boss-checklist.md",
            "Which boss, in what order, and with what gear?",
            "Boss-order",
            "The boss guide dates itself the same way",
            PINNED_COMMIT[:10],
        ):
            self.assertIn(needle, self.skill_flat)

    def test_skill_version_is_current(self):
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$",
                          self.skill, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertEqual(tuple(int(p) for p in match.groups()), (1, 6, 0))


if __name__ == "__main__":
    unittest.main()
