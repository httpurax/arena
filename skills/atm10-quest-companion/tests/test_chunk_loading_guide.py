#!/usr/bin/env python3
"""Offline tests for references/chunk-loading-guide.md.

Stdlib-only and network-free: this suite never touches the ~150MB pack clone and never
opens a socket. It mirrors the verified slice of the AllTheMods/ATM-10 config that the
page was read from - quest titles, quest and task ids, item ids, config keys and values,
changelog lines, and mod-list versions, all at ``main`` commit ``e5e3d1d83e`` (pack 8.2,
2026-09-22) - and then holds the page to it.

The point of the constants below is the *reverse* checks. A doc test that only asserts
"the page mentions X" cannot catch a page that also invents Y, so three scans walk the
page and require every token of a given shape to be one this suite already knows:

  * every ``namespace:path`` id in the page must be in ``VERIFIED_ITEM_IDS`` (or be the
    ``item:`` prefix of the EMI removal-list entries quoted verbatim);
  * every 16-hex-digit quest/task id must be in ``VERIFIED_QUEST_AND_TASK_IDS``;
  * every ``key = value`` pair must be in ``VERIFIED_CONFIG``.

An invented chunk loader, an invented quest id, or an invented force-load limit therefore
fails the suite rather than shipping.

Covered:

  * provenance: the page names the pack repo, the pinned commit, pack 8.2 / the skill's
    ``8.x`` stamp, the snapshot date, and every source file it was read from;
  * grounding: the in-game quest book + JEI are authoritative, nothing was invented,
    uncertain detail is flagged ``approximate`` / ``judgement``, and bundled non-English
    localization is flagged as a ``translation`` rather than quoted as an English name;
  * the beginner question is actually answered: the Welcome chapter's verified
    *Claiming Chunks* steps (M, the Claimed Chunks icon, drag to claim, shift-left-click
    to force load, the lines across the chunk), and the ordered answer a session can give;
  * verified quest titles are quoted as the config gives them, and the quests that carry
    no title are marked ``(no title in the config)`` next to their id instead of being
    given a derived name;
  * the pack's negative facts survive: the four chunk-loading switches it ships **off**,
    the three chunk loaders it hides from the EMI index, the FTB Chunks config it does
    **not** ship (so no limit may be quoted), and Modular Machinery Reborn's chunkloader
    being gone since pack 5.0;
  * the forbidden list: no claim/force-load limit, no command syntax, no recipe, no
    coordinate, and no chunk loader from another pack;
  * wiring: SKILL.md points at the page and bumps its version, and the sibling references
    point back at it.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
GUIDE_MD = SKILL_ROOT / "references" / "chunk-loading-guide.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
GETTING_STARTED_MD = SKILL_ROOT / "references" / "getting-started.md"
KEY_MODS_MD = SKILL_ROOT / "references" / "key-mods.md"
PROGRESSION_MD = SKILL_ROOT / "references" / "progression.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# --------------------------------------------------------------------------------------
# the pinned snapshot the page was read from
# --------------------------------------------------------------------------------------

PACK_REPO = "AllTheMods/ATM-10"
PACK_COMMIT = "e5e3d1d83e"
PACK_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
PACK_VERSION = "8.2"          # config/bcc-common.toml -> modpackVersion = "8.2"
PACK_STAMP = "8.x"            # what examples/progress.example.json is stamped with
PACK_DATE = "2026-09-22"      # the pinned commit's date
CHAPTER_COUNT = 66            # config/ftbquests/quests/chapters/*.snbt at that commit
MODLIST_ENTRIES = 493         # config/crash_assistant/modlist.json at that commit

# Pack-repo paths the page must name as its sources.
SOURCE_FILES = (
    PACK_REPO,
    "config/ftbquests/quests/chapters/welcome.snbt",
    "config/ftbquests/quests/lang/en_us/chapters/welcome.snbt",
    "config/ftbquests/quests/chapters/applied_energistics_2.snbt",
    "config/ftbquests/quests/lang/en_us/chapter.snbt",
    "chapter_group.snbt",
    "chapter_groups.snbt",
    "config/crash_assistant/modlist.json",
    "config/Mekanism/general.toml",
    "config/ae2-common.toml",
    "config/pneumaticcraft-common.toml",
    "config/pylons-server.toml",
    "config/quarryplus.toml",
    "config/mahoutsukai-server.toml",
    "config/iceandfire/iaf-common.json",
    "config/fluxnetworks-server.toml",
    "config/hyperbox-common.toml",
    "config/crashutilities-server.toml",
    "kubejs/assets/emi/index/stacks/removals.json",
    "kubejs/server_scripts/Tweaks/tags.js",
    "MOD_ISSUES.md",
)

# --------------------------------------------------------------------------------------
# verified quest titles, exactly as the en_us lang files give them at that commit
# --------------------------------------------------------------------------------------

# Minecraft `&` formatting codes stripped, the way scripts/build_chapter_list.py does it:
# `&dWelcome to All The Mods 10!` -> `Welcome to All The Mods 10!`, `&lPylons` -> `Pylons`.
VERIFIED_QUEST_TITLES = (
    # Welcome (`welcome`, chapter id 5B00676D79306EA2, standalone, order_index 0)
    "Welcome to All The Mods 10!",
    "Claiming Chunks",     # task.103C42C743E2A2DB.title - the pack's chunk-loading lesson
    "Useful Commands",     # task.10A16F89D4AD238D.title
    "Creating a Team",     # task.4F13A02FB0055A62.title
    "Quests",              # task.52BB142F044075B4.title
    # Applied Energistics 2 (`applied_energistics_2`, group Storage)
    "Spatial IO",          # quest.01F3F0C25BA72BDA.title
    # Apothic Spawners (`apotheosis_2`, group Resources)
    "Apothic Spawners",    # quest.310969B8FE0A94DE.title - the chapter hub
    "Blowing up Spawners",  # quest.321C15EBBE2D3D30.title
    "Ignore Players",      # quest.30EB438C66324213.title - the Rune of Solitude quest
    "Ignore Light", "Youthful", "Spawn Range", "Redstone Active", "Opposite Day",
    "Health", "Burning",   # the basic-rune siblings of 17C87EB8ED8A27AB
    "No AI", "Ignore All Conditions", "Echoing",   # infused-rune siblings of Ignore Players
    # Draconic Evolution (`draconic_evolution`, group Tech)
    "Quantum Energy Tunnel",  # quest.4B9FF9E972B0E530.title
    "Wireless Energy Link",   # quest.20D8DA523E900A52.title
    "Modules!",               # quest.4EFFE300EC781C3E.title
    # Pylons (`pylons`, group Logistics, 13 quests)
    "Pylons",              # quest.30B0240543253EFB.title (`&lPylons` in the config)
    "Hoes",                # task.616C07AFBAFA7AE4.title
    # Neo Vitae (`neo_vitae`, group Magic)
    "The Aura Between Worlds",   # quest.298458E916F65407.title
    # Productive Bees (`productive_bees`, group Resources)
    "Quarry Bee",          # task.471F062B01D0DDA1.title
)

# Chapter titles and the quest-book group each sits in, from lang/en_us/chapter.snbt and
# chapter_group.snbt (the skill's own examples/progress.example.json carries the same).
VERIFIED_CHAPTERS = {
    "welcome": ("Welcome", "", 6),
    "applied_energistics_2": ("Applied Energistics 2", "Storage", 74),
    "apotheosis_2": ("Apothic Spawners", "Resources", 36),
    "pylons": ("Pylons", "Logistics", 13),
    "neo_vitae": ("Neo Vitae", "Magic", 49),
}

# Quests the config gives NO title at all - neither `quest.<id>.title` nor a
# `task.<id>.title`. The page must mark each one instead of naming it.
UNTITLED_QUEST_IDS = (
    "3708A4780ACEB34E",   # Welcome - Quests (task-titled; no quest title)
    "7658C1C663394E85",   # Welcome - Useful Commands (task-titled)
    "5AC1BE754210429E",   # Welcome - Creating a Team (task-titled)
    "49EDAA2F57D3BF1D",   # Welcome - the hidden AllRightsReserved notice
    "2897FA291E5A38D8",   # AE2 - the Spatial Anchor quest
    "18DFB25DC48D8BF7",   # AE2 - the Spatial Pylon quest
    "1102B27CBF564127",   # Apothic Spawners - the Spawner Agitator quest
    "17C87EB8ED8A27AB",   # Apothic Spawners - the basic-rune quest
    "503AC506720FC59E",   # Apothic Spawners - the infused-rune quest
    "18246A48C20B29D8",   # Pylons - the Infusion Pylon quest
    "12ED1EE85E146A4B",   # Pylons - the Harvester Pylon quest
    "32E52AD6EF194A60",   # Pylons - the Expulsion Pylon quest
    "5B5FC539BD1F4A73",   # Pylons - the Interdiction Pylon quest
    "5C2C29ECA67F9B49",   # Pylons - the Lifeless Filter quest
    "034A9FBCA6D79BB6",   # Pylons - the Hoes quest (task-titled)
    "6E093D16B12E12B3",   # Productive Bees - the Quarry Bee quest (task-titled)
)

UNTITLED_MARKER = "(no title in the config)"
UNTITLED_MARKER_VARIANTS = (UNTITLED_MARKER, "(no quest title in the config)")

# Every 16-hex-digit id the page may cite: chapter ids, quest ids, task ids.
VERIFIED_QUEST_AND_TASK_IDS = (
    # chapter ids
    "5B00676D79306EA2",   # welcome
    "07210DDF872160BA",   # applied_energistics_2
    "0E81CBCD6B1D1895",   # apotheosis_2
    "5712300EF4E5E846",   # pylons
    # Welcome quests and tasks
    "3BC0A50886A3222B", "3708A4780ACEB34E", "7658C1C663394E85", "0C93D7A607AB8B83",
    "5AC1BE754210429E", "49EDAA2F57D3BF1D",
    "103C42C743E2A2DB",   # the `Claiming Chunks` checkmark task
    "10A16F89D4AD238D", "4F13A02FB0055A62", "52BB142F044075B4",
    # AE2
    "01F3F0C25BA72BDA", "18DFB25DC48D8BF7", "2897FA291E5A38D8", "68A36AB341CC016D",
    "0EFC322997906572", "4E0C5E3A98293C08", "40A7CC56DACC2623",
    # Apothic Spawners
    "310969B8FE0A94DE", "321C15EBBE2D3D30", "17C87EB8ED8A27AB", "503AC506720FC59E",
    "30EB438C66324213", "1102B27CBF564127", "0F0E227FC3EC0D90",
    "5225548C5219E0C6", "211FBEB0E4FF1FD6", "3839A67493B2E5C3",
    # Draconic Evolution
    "4B9FF9E972B0E530", "20D8DA523E900A52", "4EFFE300EC781C3E", "7634D5C19B7C8904",
    "6263FF7F49AAC2E5",
    # Pylons
    "30B0240543253EFB", "18246A48C20B29D8", "12ED1EE85E146A4B", "32E52AD6EF194A60",
    "5B5FC539BD1F4A73", "5C2C29ECA67F9B49", "034A9FBCA6D79BB6",
    "576428EF1CDDEF96", "6C593196779DD911", "2F7ABC9758AAC23E", "3644DD329B1CF04B",
    "525BAD815438BF4C", "5E3CBC6340E0D0AE", "616C07AFBAFA7AE4",
    # Neo Vitae, Productive Bees
    "298458E916F65407", "64771006538ED238", "11F6669733F1420B",
    "6E093D16B12E12B3", "471F062B01D0DDA1", "17419401147B5C02",
)

# --------------------------------------------------------------------------------------
# verified item / block / dimension / texture ids
# --------------------------------------------------------------------------------------

VERIFIED_ITEM_IDS = (
    # the one chunk loader the quest book tracks, and its Spatial IO lineage
    "ae2:spatial_anchor", "ae2:spatial_pylon", "ae2:spatial_io_port",
    # Mekanism's two, named by config/Mekanism/general.toml's own comment
    "mekanism:upgrade_anchor", "mekanism:dimensional_stabilizer",
    # Apothic Spawners runes (namespace `apotheosis`, Apotheosis 8.8.0)
    "apotheosis:ignore_players_spawner_rune", "apotheosis:infused_spawner_rune",
    "apotheosis:no_ai_spawner_rune", "apotheosis:ignore_conditions_spawner_rune",
    "apotheosis:echoing_spawner_rune", "apotheosis:spawner_chain",
    # the Apothic Spawners chapter's other spawner task items
    "pneumaticcraft:spawner_agitator", "pneumaticcraft:pressurized_spawner",
    "enderio:powered_spawner", "draconicevolution:stabilized_spawner",
    "ars_additions:source_spawner", "mysticalagriculture:soulium_spawner",
    "industrialforegoing:mob_duplicator", "mob_grinding_utils:entity_spawner",
    "mob_grinding_utils:xpsolidifier", "mob_grinding_utils:solid_xp_mould_baby",
    # Draconic Evolution energy links
    "draconicevolution:item_draconic_energy_link",
    "draconicevolution:item_wyvern_energy_link",
    # Pylons
    "pylons:infusion_pylon", "pylons:harvester_pylon", "pylons:expulsion_pylon",
    "pylons:interdiction_pylon", "pylons:lifeless_filter",
    # vanilla and utility ids the config itself uses
    "minecraft:spawner", "minecraft:tnt", "minecraft:polished_blackstone",
    "minecraft:overworld", "minecraft:hoes",
    "ftbfiltersystem:smart_filter", "ftbfiltersystem:item_tag",
    # FTB Chunks' own ids, from the Welcome chapter and the pack's tag tweak
    "ftbchunks:interact_whitelist", "ftbchunks:textures/waypoint_home.png",
    "ftbquests:custom_icon", "ftbquests:icon",
    # QuarryPlus - the only quarryplus id anywhere in the quest config (a quest icon)
    "quarryplus:quarry",
    # Neo Vitae
    "neovitae:vas_maleficum",
    # the four ids that exist ONLY in the pack's bundled pt_br/ru_ru localization
    "naturesaura:chunk_loader", "immersiveengineering:chunk_loader",
    "pneumaticcraft:chunkloader_upgrade", "ars_additions:ritual_chunk_loading",
    # the one the pack removed in 5.0 - named only to date it
    "modular_machinery_reborn:chunkloader",
    # Pylons' expulsionAllowedDimensions list (config/pylons-server.toml)
    "allthemodium:the_beyond", "eternal_starlight:starlight",
    "compactmachines:compact_world",
)

# `kubejs/assets/emi/index/stacks/removals.json` entries are quoted verbatim, so the page
# carries their `item:` prefix. Only the two prefixes of the three chunk loaders may appear.
EMI_INDEX_PREFIXES = ("item:ae2", "item:mekanism")

LOCALIZATION_ONLY_IDS = (
    "naturesaura:chunk_loader",
    "immersiveengineering:chunk_loader",
    "pneumaticcraft:chunkloader_upgrade",
    "ars_additions:ritual_chunk_loading",
)

# --------------------------------------------------------------------------------------
# verified config keys and values, each with the file that ships it
# --------------------------------------------------------------------------------------

VERIFIED_CONFIG = {
    # switch ON in this pack
    "allowChunkloading": ("true", "config/Mekanism/general.toml"),
    "spatialAnchorEnableRandomTicks": ("true", "config/ae2-common.toml"),
    "enableChunkLoader": ("true", "config/quarryplus.toml"),
    "chunk_marker": ("true", "config/quarryplus.toml"),
    "quarry": ("true", "config/quarryplus.toml"),
    "flexible_marker": ("true", "config/quarryplus.toml"),
    "removeCommonMaterialsByChunkDestroyer": ("true", "config/quarryplus.toml"),
    "infusionChunkloads": ("true", "config/pylons-server.toml"),
    "teamSupportEnabled": ("true", "config/pylons-server.toml"),
    "harvesterRequiresTool": ("true", "config/pylons-server.toml"),
    "FAMILIAR_CHUNKLOADS": ("true", "config/mahoutsukai-server.toml"),
    # switch OFF in this pack
    "adv_quarry": ("false", "config/quarryplus.toml"),
    "enableChunkLoading": ("false", "config/fluxnetworks-server.toml"),
    "auto_force_hyperbox_chunks": ("false", "config/hyperbox-common.toml"),
    "allow_navigate_to_unloaded_chunks": ("false", "config/pneumaticcraft-common.toml"),
    "chunkLoggerTrace": ("false", "config/ae2-common.toml"),
    "harvesterCanBeAutomated": ("false", "config/pylons-server.toml"),
    "harvesterRequiresPower": ("false", "config/pylons-server.toml"),
    "expulsionPylonCanExplode": ("false", "config/pylons-server.toml"),
    # numbers the pack ships
    "chunkload_offline_time": ("300", "config/pneumaticcraft-common.toml"),
    "days": ("7", "config/crashutilities-server.toml"),
    "harvesterWorkDelay": ("20", "config/pylons-server.toml"),
    "harvesterPowerCost": ("5", "config/pylons-server.toml"),
    "expulsionPylonMaxRadius": ("2", "config/pylons-server.toml"),
    "expulsionWorldSpawnRadius": ("1", "config/pylons-server.toml"),
    "yield": ("38400", "config/immersiveengineering-server.toml"),
}

# Quoted whole, because a truncated list would be a different claim.
VERIFIED_CONFIG_LINES = (
    'expulsionAllowedDimensions = ["minecraft:overworld", "allthemodium:the_beyond", '
    '"eternal_starlight:starlight", "compactmachines:compact_world"]',
    'modpackVersion = "8.2"',
    '["Ftb Chunks"]',
)

# The four switches the pack ships disabled - the page must keep them negative.
DISABLED_SWITCHES = (
    ("enableChunkLoading", "config/fluxnetworks-server.toml"),
    ("auto_force_hyperbox_chunks", "config/hyperbox-common.toml"),
    ("allow_navigate_to_unloaded_chunks", "config/pneumaticcraft-common.toml"),
    ('["Ftb Chunks"]', "config/crashutilities-server.toml"),
)

# The three chunk-loading items hidden from the EMI item index.
EMI_HIDDEN_CHUNK_LOADERS = (
    "item:ae2:spatial_anchor",
    "item:mekanism:upgrade_anchor",
    "item:mekanism:dimensional_stabilizer",
)

# --------------------------------------------------------------------------------------
# verified mod-list names and versions (config/crash_assistant/modlist.json)
# --------------------------------------------------------------------------------------

VERIFIED_MODS = {
    "FTB Chunks": "2101.1.22",
    "FTB Teams": "2101.1.11",
    "FTB Ranks": "2101.1.5",
    "FTB Essentials": "2101.1.10",
    "FTB Library": "2101.1.36",
    "FTB Quests": "2101.1.36",
    "Journeymap": "1.21.1-6.0.9",
    "Applied Energistics 2": "19.2.17",
    "Mekanism": "10.7.19",
    "QuarryPlus": "21.1.164",
    "Pylons": "5.4.2",
    "Flux Networks": "8.0.0",
    "PneumaticCraft: Repressurized": "8.2.23",
    "Mahou Tsukai": "1.21.1-v1.36.28",
    "Ice And Fire Community Edition": "2.0-beta.17",
    "NaturesAura": "41.10",
    "Ars Additions": "1.21.1-21.3.0",
    "Apotheosis": "8.8.0",
    "Apothic Spawners": "1.4.0",
    "Immersive Engineering": "12.4.2-194",
    "Draconic Evolution": "3.1.4.633",
    "Neo Vitae": "1.1.26",
    "Waystones": "21.1.45",
    "Crash Utilities": "9.0.4",
}

# --------------------------------------------------------------------------------------
# changelog and MOD_ISSUES lines the page quotes
# --------------------------------------------------------------------------------------

VERIFIED_CHANGELOG_LINES = (
    "Disable Fluxnet Chunkloading",                      # CHANGELOG-ATM10-2.31-2.32.md
    "fix: remove modular machinery",                     # CHANGELOG-ATM10-4.15-5.0.md
    "Modular Machinery Reborn (2.3.2)",                  # CHANGELOG-ATM10-4.15-5.0.md
    "Modular Machinery Reborn ArsNouveau (2.0.3)",
    "Modular Machinery Reborn Mekanism (2.0.6)",
    "FTB Chunks (2101.1.21) -> (2101.1.22)",             # CHANGELOG-ATM10-8.1-8.2.md
    "Updated PT_BR Localizations (#4389)",               # CHANGELOG-ATM10-8.1-8.2.md
    "FTB Chunks (Forge)",                                # MOD_ISSUES.md
)

# --------------------------------------------------------------------------------------
# what must NOT appear: invented limits, commands, recipes, or other packs' loaders
# --------------------------------------------------------------------------------------

FORBIDDEN_INVENTIONS = (
    # FTB Chunks / FTB Ranks limit keys - the pack ships no such config, so a value for
    # any of these would be invented.
    "max_claimed", "max_force_loaded", "maxClaimed", "maxForceLoaded", "force_load_radius",
    # command syntax the repo never states
    "/forceload", "/ftbchunks", "/chunkload", "/claim",
    # chunk-loading mods and blocks ATM10 does not ship (other packs' favourites)
    "ChickenChunks", "Chunk Loaders", "Dark Utilities", "Forcecraft", "TelePastries",
    "chunkloader block from Mekanism", "RailCraft chunk loader", "Create chunk loader",
    # a limit stated as a fact
    "you can force-load 25 chunks", "up to 50 chunks",
)

# The page must say these things rather than fill the gaps.
REQUIRED_REFUSALS = (
    "no claim or force-load limit is quoted",
    "ships no FTB Chunks config",
    "Never invent a limit",
    "not stated in the repo",
)

ID_RE = re.compile(r"\b([a-z][a-z0-9_]+):([a-z][a-z0-9_/.\-]*)")
HEX16_RE = re.compile(r"\b([0-9A-F]{16})\b")
CONFIG_PAIR_RE = re.compile(
    r"`?([A-Za-z_][A-Za-z0-9_]{2,})`?\s*=\s*`?(-?[A-Za-z0-9_.]+)`?")


def flatten(text: str) -> str:
    """One line, with blockquote gutters removed so a quoted paragraph stays searchable."""
    lines = [re.sub(r"^\s*>\s?", "", line) for line in text.splitlines()]
    return re.sub(r"\s+", " ", "\n".join(lines)).replace("\n", " ")


def deparen(text: str) -> str:
    """`flatten` plus markdown emphasis removed, for prose phrase checks."""
    return flatten(text).replace("**", "").replace("*", "")


class GuideTestCase(unittest.TestCase):
    """Loads the page once for the suite, in three views."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = GUIDE_MD.read_text(encoding="utf-8") if GUIDE_MD.is_file() else ""
        cls.flat = flatten(cls.text)          # markup kept, one line
        cls.plain = deparen(cls.text)         # markup stripped, one line
        cls.lower = cls.plain.lower()         # for case-insensitive prose checks

    def window(self, needle: str, size: int = 600, view: str = "plain") -> str:
        """The page around a token, so a caveat can be tied to the thing it qualifies."""
        hay = getattr(self, view)
        index = hay.lower().find(needle.lower())
        self.assertGreaterEqual(index, 0, f"the page never mentions {needle!r}")
        return hay[index:index + size]

    def any_window(self, needle: str, size: int = 800, view: str = "plain") -> "list[str]":
        """Every window around every occurrence of a token."""
        hay = getattr(self, view)
        low = hay.lower()
        target = needle.lower()
        out, start = [], low.find(target)
        while start >= 0:
            out.append(hay[start:start + size])
            start = low.find(target, start + 1)
        self.assertTrue(out, f"the page never mentions {needle!r}")
        return out

    def section(self, heading: str, view: str = "plain") -> str:
        """The page from one `##` heading to the next."""
        hay = getattr(self, view)
        start = hay.index(heading)
        rest = hay[start + len(heading):]
        match = re.search(r"\n?## ", rest)
        return hay[start:start + len(heading) + (match.start() if match else len(rest))]


# --------------------------------------------------------------------------------------
# the page exists and dates itself
# --------------------------------------------------------------------------------------

class TestGuideExistsAndIsGrounded(GuideTestCase):

    def test_guide_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.text.strip()), 12000,
                           "chunk-loading-guide.md looks like a stub")

    def test_it_names_the_pack_repo_and_pinned_commit(self) -> None:
        self.assertIn(PACK_REPO, self.text)
        self.assertIn(PACK_COMMIT, self.text)
        self.assertIn(PACK_COMMIT_FULL, self.text)
        self.assertIn(PACK_DATE, self.text)

    def test_it_dates_itself_to_pack_8_2_and_the_skill_stamp(self) -> None:
        self.assertIn(f"pack {PACK_VERSION}", self.text)
        self.assertIn(PACK_STAMP, self.text,
                      "the page must tie 8.2 to the skill's 8.x stamp")
        self.assertIn('modpackVersion = "8.2"', self.text)
        self.assertIn("examples/progress.example.json", self.text)
        # The shipped example carries the same stamp; the two must not drift apart.
        self.assertIn(f'"pack_version": "{PACK_STAMP}"',
                      EXAMPLE_DATA.read_text(encoding="utf-8"))

    def test_it_names_every_source_file(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source, self.text, f"the page must name its source: {source}")

    def test_it_states_the_read_not_remembered_rule(self) -> None:
        self.assertRegex(self.lower, r"read, not remembered|never invented|not invented")
        self.assertIn("nothing is added from memory", self.lower)

    def test_it_defers_to_the_in_game_book_and_jei(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lower, f"missing the {needle!r} rule")
        self.assertIn("ftb quests", self.lower)

    def test_it_flags_judgement_and_translation_separately_from_quotes(self) -> None:
        self.assertIn("judgement", self.lower,
                      "anything not quoted must be flagged as judgement")
        self.assertIn("translation", self.lower,
                      "pt_br/ru_ru strings must be flagged as translations")
        self.assertIn("pt_br", self.text)
        self.assertIn("ru_ru", self.text)
        self.assertIn("no `en_us` name", self.flat,
                      "the page must say the repo carries no English name for those ids")

    def test_it_says_formatting_codes_were_stripped(self) -> None:
        self.assertIn("formatting codes", self.lower)
        self.assertIn("&6M&r", self.text,
                      "the page must show the raw form it stripped, so the quote is checkable")

    def test_it_quotes_the_pack_scale_it_relied_on(self) -> None:
        self.assertIn(f"{CHAPTER_COUNT} chapters", self.flat)
        self.assertIn(f"{MODLIST_ENTRIES} entries", self.flat)


# --------------------------------------------------------------------------------------
# the beginner question is actually answered
# --------------------------------------------------------------------------------------

class TestTheBeginnerQuestionIsAnswered(GuideTestCase):

    def test_the_question_itself_is_on_the_page(self) -> None:
        self.assertIn("how do i keep my farm running while i'm away?", self.lower)
        self.assertIn("## Answering the beginner question", self.text)

    def test_the_short_answer_is_the_claim_and_force_load_steps(self) -> None:
        self.assertIn("## The short answer", self.text)
        short = self.flat[self.flat.index("## The short answer"):
                          self.flat.index("## Step 1")]
        for needle in ("Claim the chunks", "force-load", "shift-left-click",
                       "Claimed Chunks", "left-click and drag"):
            self.assertIn(needle.lower(), short.lower(),
                          f"the short answer must give the {needle!r} step")

    def test_the_verified_claiming_chunks_instructions_are_quoted(self) -> None:
        """The Welcome chapter's own words, code-stripped, are the whole tutorial."""
        for line in ("To claim chunks, open up your map using M, then click the Claimed "
                     "Chunks icon in the top left.",
                     "To claim a chunk, left click and drag to claim.",
                     "To force load a chunk, shift-left click the chunk. If done properly, "
                     "you'll see lines across the chunk."):
            self.assertIn(line, self.plain, f"missing the quoted step: {line[:50]}...")

    def test_the_claiming_chunks_quest_is_cited_by_id_and_task(self) -> None:
        self.assertIn("0C93D7A607AB8B83", self.text)     # the quest
        self.assertIn("103C42C743E2A2DB", self.text)     # its checkmark task
        self.assertIn("checkmark", self.lower)
        self.assertIn("5B00676D79306EA2", self.text)     # the Welcome chapter id
        self.assertIn("order_index", self.text)

    def test_claiming_is_distinguished_from_force_loading(self) -> None:
        self.assertIn("LOADED not Claimed Chunks", self.text,
                      "the pack's own Crash Utilities wording is the distinction")
        self.assertIn("Claiming alone is not enough", self.flat)

    def test_the_ordered_answer_covers_the_cases_a_session_meets(self) -> None:
        answer = self.flat[self.flat.index("## Answering the beginner question"):]
        for needle in ("Force-load the farm's chunks", "Ask what kind of farm",
                       "Mob farm?", "AE2 network", "check the switches",
                       "Never state a limit"):
            self.assertIn(needle.lower(), answer.lower(), f"missing step: {needle}")
        # The two follow-ups that change the answer.
        self.assertIn("singleplayer or server?", answer.lower())
        self.assertIn("how big is the farm, in chunks?", answer.lower())

    def test_the_troubleshooting_section_is_grounded_only(self) -> None:
        trouble = self.flat[self.flat.index("## When it still does not work"):]
        self.assertIn("lines across the chunk", trouble.lower())
        self.assertIn("chunk border", trouble.lower())
        self.assertIn("MOD_ISSUES.md", trouble)
        self.assertIn("FTBTeam/FTB-Mods-Issues", trouble)
        self.assertIn("ATM discord", trouble)


# --------------------------------------------------------------------------------------
# verified quest titles, and the untitled ones left untitled
# --------------------------------------------------------------------------------------

class TestVerifiedQuestTitles(GuideTestCase):

    def test_every_verified_title_is_quoted(self) -> None:
        for title in VERIFIED_QUEST_TITLES:
            self.assertIn(title, self.plain,
                          f"the page is missing a verified quest title: {title}")

    def test_the_claiming_chunks_title_is_attributed_to_the_task(self) -> None:
        """The config puts that title on the task, not the quest - the page must say so."""
        self.assertIn("task.103C42C743E2A2DB.title", self.text)
        window = self.window("0C93D7A607AB8B83", 900)
        self.assertIn("absent", window,
                      "the page must record that the quest itself has no title key")
        self.assertIn("Task title (verified)", self.text)
        self.assertRegex(self.lower, r"puts the title on the task, not the quest")

    def test_chapter_titles_groups_and_quest_counts_are_the_config_s(self) -> None:
        for filename, (title, group, quests) in VERIFIED_CHAPTERS.items():
            self.assertIn(filename, self.text, f"missing chapter filename: {filename}")
            self.assertIn(title, self.text, f"missing chapter title: {title}")
            self.assertIn(f"{quests} quests", self.text,
                          f"the {title} chapter has {quests} quests in the config")
            if group:
                self.assertIn(group, self.text, f"missing group for {title}: {group}")

    def test_untitled_quests_are_marked_not_named(self) -> None:
        for quest_id in UNTITLED_QUEST_IDS:
            windows = [w.lower() for w in self.any_window(quest_id, 800)]
            self.assertTrue(any(any(m in w for m in UNTITLED_MARKER_VARIANTS)
                                for w in windows),
                            f"quest {quest_id} carries no title in the config and must be "
                            f"marked {UNTITLED_MARKER!r} next to its id")

    def test_the_marker_convention_matches_the_sibling_docs(self) -> None:
        self.assertGreaterEqual(self.lower.count(UNTITLED_MARKER), 10,
                                "every untitled quest the page cites must be marked")

    def test_no_derived_name_is_presented_as_a_verified_title(self) -> None:
        """Local names for untitled quests must be tied to their quest text."""
        for phrase in ("the Spatial Anchor quest", "the Spawner Agitator quest",
                       "the Infusion Pylon quest", "the Harvester Pylon quest",
                       "the Expulsion Pylon quest", "the Interdiction Pylon quest",
                       "the Claiming Chunks quest"):
            if phrase in ("the Infusion Pylon quest", "the Harvester Pylon quest",
                          "the Expulsion Pylon quest", "the Interdiction Pylon quest"):
                continue  # the Pylons table names those by their config item, not a quest
            self.assertIn(phrase, self.plain, f"missing the local name {phrase!r}")
        self.assertRegex(self.lower, r"called the spatial anchor quest here, after its own text")
        self.assertRegex(self.lower,
                         r"do not present a derived name as a verified quest title")


# --------------------------------------------------------------------------------------
# no invented ids: the reverse scans
# --------------------------------------------------------------------------------------

class TestNoInventedIds(GuideTestCase):

    def cited_ids(self) -> "set[str]":
        found = set()
        for match in ID_RE.finditer(self.text):
            token = f"{match.group(1)}:{match.group(2)}".rstrip(".,;:")
            found.add(token)
        return found

    def test_every_id_on_the_page_is_verified(self) -> None:
        allowed = set(VERIFIED_ITEM_IDS) | set(EMI_INDEX_PREFIXES)
        unknown = sorted(self.cited_ids() - allowed)
        self.assertEqual(unknown, [],
                         "the page cites an id that is not in this pack's config "
                         "(invented item/block/dimension id): " + ", ".join(unknown))

    def test_the_scan_actually_finds_the_ids_it_should(self) -> None:
        """Guard the guard: if the regex stops matching, the test above goes vacuous."""
        cited = self.cited_ids()
        self.assertGreater(len(cited), 40, "the id scan found suspiciously few ids")
        for expected in ("ae2:spatial_anchor", "mekanism:upgrade_anchor",
                         "apotheosis:ignore_players_spawner_rune", "pylons:harvester_pylon",
                         "naturesaura:chunk_loader"):
            self.assertIn(expected, cited)

    def test_every_quest_id_on_the_page_is_verified(self) -> None:
        cited = set(HEX16_RE.findall(self.text))
        unknown = sorted(cited - set(VERIFIED_QUEST_AND_TASK_IDS))
        self.assertEqual(unknown, [],
                         "the page cites a 16-hex id that is not a chapter, quest, or task "
                         "id in this pack's config: " + ", ".join(unknown))

    def test_the_hex_scan_actually_finds_the_ids_it_should(self) -> None:
        cited = set(HEX16_RE.findall(self.text))
        self.assertGreater(len(cited), 30, "the quest-id scan found suspiciously few ids")
        self.assertIn("0C93D7A607AB8B83", cited)
        self.assertIn("2897FA291E5A38D8", cited)

    def test_the_key_ids_are_present(self) -> None:
        for item in ("ae2:spatial_anchor", "mekanism:upgrade_anchor",
                     "mekanism:dimensional_stabilizer", "pylons:infusion_pylon",
                     "pylons:harvester_pylon", "apotheosis:ignore_players_spawner_rune",
                     "pneumaticcraft:spawner_agitator", "ftbchunks:interact_whitelist"):
            self.assertIn(item, self.text, f"missing verified id: {item}")

    def test_the_dimension_ids_come_from_the_pylons_config(self) -> None:
        for line in VERIFIED_CONFIG_LINES:
            self.assertIn(line, self.plain, f"missing quoted config line: {line[:60]}")
        self.assertIn("the only ones this page names", self.lower)


# --------------------------------------------------------------------------------------
# no invented config values: the reverse scan
# --------------------------------------------------------------------------------------

class TestNoInventedConfigValues(GuideTestCase):

    def cited_pairs(self) -> "dict[str, str]":
        found = {}
        for match in CONFIG_PAIR_RE.finditer(self.flat):
            key, value = match.group(1), match.group(2)
            if key in VERIFIED_CONFIG or key in ("modpackVersion", "enabled"):
                found[key] = value
        return found

    def test_every_config_pair_on_the_page_matches_the_pack(self) -> None:
        wrong = []
        for key, value in self.cited_pairs().items():
            if key == "modpackVersion":
                if value.strip('"') != PACK_VERSION:
                    wrong.append(f"{key} = {value}")
                continue
            if key == "enabled":
                continue  # scoped to the ["Ftb Chunks"] section, checked below
            expected = VERIFIED_CONFIG[key][0]
            if value.strip('"') != expected:
                wrong.append(f"{key} = {value} (pack ships {expected})")
        self.assertEqual(wrong, [],
                         "the page states a config value the pack does not ship: "
                         + "; ".join(wrong))

    def test_the_pair_scan_actually_finds_the_pairs_it_should(self) -> None:
        pairs = self.cited_pairs()
        self.assertGreater(len(pairs), 15, "the config scan found suspiciously few pairs")
        for key in ("allowChunkloading", "enableChunkLoading", "chunkload_offline_time",
                    "infusionChunkloads", "auto_force_hyperbox_chunks"):
            self.assertIn(key, pairs)

    def test_every_key_is_attributed_to_its_file(self) -> None:
        for key, (_value, path) in VERIFIED_CONFIG.items():
            self.assertIn(key, self.text, f"missing config key: {key}")
            self.assertIn(path, self.text,
                          f"the page must name the file that ships {key}: {path}")

    def test_the_four_disabled_switches_stay_disabled(self) -> None:
        for key, path in DISABLED_SWITCHES:
            window = self.window(key, 400)
            self.assertIn(path, self.text)
            if key.startswith("["):
                self.assertIn("false", window,
                              'the ["Ftb Chunks"] purge must stay `enabled = false`')
            else:
                self.assertIn("false", window,
                              f"{key} ships false in this pack; the page must not flip it")
        self.assertIn("what the pack turned off", self.lower)

    def test_the_enabled_switches_are_listed_for_contrast(self) -> None:
        for key in ("allowChunkloading", "spatialAnchorEnableRandomTicks",
                    "enableChunkLoader", "FAMILIAR_CHUNKLOADS", "infusionChunkloads"):
            window = self.window(f"{key} = true", 300)
            self.assertTrue(window, f"{key} = true must appear on the page")

    def test_the_offline_cap_is_quoted_with_its_own_comment(self) -> None:
        self.assertIn("chunkload_offline_time = 300", self.plain)
        self.assertIn("Time in seconds after a player logs out", self.plain)
        self.assertIn("Set to 0 to allow indefinite offline chunkloading", self.plain)
        self.assertIn("five minutes", self.lower,
                      "300s must be rendered as a duration a beginner can use")

    def test_the_infusion_pylon_online_caveat_survives(self) -> None:
        self.assertIn("while the player is online", self.lower)
        self.assertIn("limited to one pylon per player", self.lower)
        self.assertIn("not an away-farm answer", self.lower)


# --------------------------------------------------------------------------------------
# the EMI index removals, and the localization-only ids
# --------------------------------------------------------------------------------------

class TestTheHiddenAndTheThinlySourced(GuideTestCase):

    def test_the_three_hidden_chunk_loaders_are_quoted(self) -> None:
        for entry in EMI_HIDDEN_CHUNK_LOADERS:
            self.assertIn(entry, self.text, f"missing EMI removal-list entry: {entry}")
        self.assertIn("kubejs/assets/emi/index/stacks/removals.json", self.text)

    def test_hiding_is_not_overstated_as_disabling(self) -> None:
        """The file hides index entries; whether the items still work is judgement."""
        self.assertRegex(self.lower, r"hidden from the item browser|index removal")
        self.assertIn("judgement", self.lower)
        self.assertRegex(self.lower, r"is not stated by this file")

    def test_localization_only_ids_are_flagged_where_they_appear(self) -> None:
        for item in LOCALIZATION_ONLY_IDS:
            self.assertIn(item, self.text, f"missing localization-only id: {item}")
        self.assertIn("non-english localization", self.lower)
        self.assertRegex(self.lower, r"found only in `?kubejs/assets")
        self.assertIn("evidence that an id exists, not of its english name", self.lower)
        # Each of the four must sit next to its own caveat.
        for item, caveat in (("naturesaura:chunk_loader", "en_us"),
                             ("immersiveengineering:chunk_loader", "translation"),
                             ("pneumaticcraft:chunkloader_upgrade", "pt_br"),
                             ("ars_additions:ritual_chunk_loading", "translation")):
            window = self.window(item, 1400).lower()
            self.assertIn(caveat.lower(), window,
                          f"{item} must carry its {caveat!r} caveat next to it")

    def test_the_pt_br_drone_tiers_are_marked_as_a_translation(self) -> None:
        window = self.window("cardinal cross", 500).lower()
        self.assertIn("one upgrade keeps the drone's own chunk loaded", self.lower)
        self.assertIn("translation", window,
                      "the drone tiers come from a pt_br string and must stay flagged")

    def test_the_immersive_engineering_config_is_not_misread(self) -> None:
        """Its 19 chunk mentions are all worldgen - the page must say so."""
        self.assertIn("19 times", self.plain)
        self.assertIn("worldgen or retrogen", self.lower)
        self.assertIn("retrogen_excavator_veins", self.text)
        self.assertIn("attempts_per_chunk", self.text)

    def test_the_waystones_tag_tweak_is_quoted_and_hedged(self) -> None:
        self.assertIn("allthemods.add('ftbchunks:interact_whitelist', ['@waystones'])",
                      self.text)
        self.assertIn("kubejs/server_scripts/Tweaks/tags.js", self.text)
        window = self.window("allthemods.add(", 900).lower()
        self.assertIn("not defined in this repo", window)
        self.assertIn("judgement", window)


# --------------------------------------------------------------------------------------
# the forbidden list: nothing invented to fill a gap
# --------------------------------------------------------------------------------------

class TestNothingIsInventedToFillAGap(GuideTestCase):

    def test_no_forbidden_invention_appears(self) -> None:
        """Scoped to the body: the closing refusals section names these to refuse them."""
        refusals = self.plain.index("## What this page deliberately does not tell you")
        body = self.plain[:refusals]
        for needle in FORBIDDEN_INVENTIONS:
            self.assertNotIn(needle, body,
                             f"the page invents {needle!r}; it is not in this pack's config")

    def test_the_refusals_section_is_where_those_names_may_appear(self) -> None:
        refusals = self.section("## What this page deliberately does not tell you")
        for needle in ("/forceload", "/ftbchunks"):
            self.assertIn(needle, refusals,
                          f"the refusal to give {needle} syntax belongs in the closing "
                          f"section, and only there")

    def test_the_page_says_what_it_refuses_to_state(self) -> None:
        for refusal in REQUIRED_REFUSALS:
            self.assertIn(refusal.lower(), self.lower, f"missing refusal: {refusal}")

    def test_no_ftb_chunks_config_means_no_limit(self) -> None:
        self.assertIn("no ftb chunks config file at all", self.lower)
        self.assertIn("ftbultimine-server.snbt", self.text,
                      "the page must name the FTB configs the pack *does* ship")
        self.assertRegex(self.lower, r"never invent a limit|never state a limit")

    def test_no_recipe_or_cost_is_given(self) -> None:
        self.assertIn("## What this page deliberately does not tell you", self.plain)
        refusals = self.section("## What this page deliberately does not tell you",
                                view="flat")
        for needle in ("Recipes and costs", "Command syntax", "Farm designs",
                       "A claim or force-load limit", "English names for the four"):
            self.assertIn(needle, refusals, f"missing the {needle!r} refusal")

    def test_only_the_welcome_chapter_s_commands_are_quoted(self) -> None:
        for command in ("/sethome", "/home", "/spawn", "/rtp", "/ftbteams party create"):
            self.assertIn(command, self.plain)
        self.assertIn("the only commands quoted anywhere on this page", self.lower)

    def test_the_removed_mod_chunkloader_is_dated_not_recommended(self) -> None:
        self.assertIn("modular_machinery_reborn:chunkloader", self.text)
        self.assertIn("Not available in 8.2", self.plain)
        for line in VERIFIED_CHANGELOG_LINES:
            self.assertIn(line, self.plain, f"missing changelog line: {line}")
        self.assertIn("CHANGELOG-ATM10-4.15-5.0.md", self.text)
        self.assertIn("Removed (3)", self.text)

    def test_the_hyperbox_modlist_gap_is_flagged(self) -> None:
        """The config file ships, but the mod is not in modlist.json at this commit."""
        window = self.window("auto_force_hyperbox_chunks", 2000).lower()
        self.assertIn("hyperbox` entry", window)
        self.assertIn("unverified", window)

    def test_no_coordinates_or_energy_numbers_are_invented(self) -> None:
        self.assertNotRegex(self.text, r"\b[XY] = -?\d+",
                            "the page must not print world coordinates")
        # The only chunk-count figures allowed are the config's own pylon areas.
        for allowed in ("1x1", "3x3", "5x5", "7x7", "9x9", "25x25"):
            self.assertIn(allowed, self.text)
        self.assertRegex(self.plain, r"(?i)\d+x\d+ chunks?\b",
                         "chunk areas must be quoted, and only from the config")


# --------------------------------------------------------------------------------------
# the AE2 and spawner content, which is the substance of steps 2 and 3
# --------------------------------------------------------------------------------------

class TestTheTwoDocumentedAlternatives(GuideTestCase):

    def test_the_spatial_anchor_quest_is_quoted_in_full(self) -> None:
        for line in ("The Spatial Anchor is a companion device from the Spatial IO lineage "
                     "that simply functions as a chunk loader.",
                     "the Anchor will force-load all the chunks occupied by the ME network "
                     "across all cables and devices, excluding subnetworks, as long as the "
                     "network remains powered."):
            self.assertIn(line, self.plain, "missing the Spatial Anchor quote")
        self.assertIn("optional", self.lower)
        self.assertIn("5871764666515020368", self.text, "the reward table id is verified")

    def test_it_is_presented_as_the_only_tracked_chunk_loader(self) -> None:
        self.assertRegex(self.plain,
                         r"Across all 66 chapters, exactly one quest has a chunk loader as "
                         r"its task item")

    def test_the_ignore_players_rune_keeps_its_chunk_loaded_condition(self) -> None:
        self.assertIn("A Rune of Solitude will do part what the Spawner Upgrade Runes do "
                      "but much better.", self.plain)
        self.assertIn("As long as its chunk-loaded it will spawn.", self.plain)
        self.assertIn("Players no longer need to be near the spawner.", self.plain)
        self.assertIn("partner for step 1, not a replacement", self.lower)

    def test_the_rune_dependency_chain_is_in_config_order(self) -> None:
        chain = ("310969B8FE0A94DE", "321C15EBBE2D3D30", "17C87EB8ED8A27AB",
                 "503AC506720FC59E", "30EB438C66324213")
        table = self.section("Its place in the chapter", view="flat")
        self.assertIn("| # | Quest id |", table, "the chain must be a table")
        positions = [table.index(q) for q in chain]
        self.assertEqual(positions, sorted(positions),
                         "the rune line must stay in the config's dependency order")
        self.assertIn("at least 70 Eterna, 30% Quanta, and 50% Arcana", self.plain)

    def test_the_spawner_agitator_is_not_sold_as_a_chunk_loader(self) -> None:
        self.assertIn("it won't change that but rather will keep spawned mobs from "
                      "despawning incase you leave the chunks", self.plain)
        self.assertIn("does not make the spawner work without a player", self.lower)
        self.assertIn("do not sell it as a chunk loader", self.lower)

    def test_the_other_spawners_are_listed_without_inferred_behaviour(self) -> None:
        self.assertIn("0F0E227FC3EC0D90", self.text)
        self.assertRegex(self.lower,
                         r"the repo says nothing about whether any of these runs without a "
                         r"player")
        self.assertIn("Do not infer it from the names", self.flat)

    def test_the_draconic_cross_dimension_caveat_is_quoted(self) -> None:
        self.assertIn("just make sure the other side is chunkloaded", self.plain)
        self.assertIn("Quantum Energy Tunnel", self.text)
        self.assertIn("both** ends", self.text.replace("**both**", "both**"))

    def test_chunk_areas_are_separated_from_chunk_loading(self) -> None:
        self.assertIn("Chunk *areas* that are not chunk loading", self.text)
        self.assertIn("loads nothing", self.lower)
        self.assertIn("it chunkloads only itself", self.lower)
        self.assertIn("Neo Vitae's per-chunk Spiritus", self.text)
        self.assertIn("resource unit", self.lower)


# --------------------------------------------------------------------------------------
# wiring: SKILL.md and the sibling references
# --------------------------------------------------------------------------------------

class TestWiring(GuideTestCase):

    def test_skill_md_points_at_the_new_page(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("references/chunk-loading-guide.md", skill)

    def test_skill_md_routes_the_beginner_question_to_it(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertRegex(skill.lower(), r"keep (my|your|his|a) farm running")
        self.assertIn("chunk-loading", skill.lower())

    def test_skill_md_version_was_bumped(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)\s*$", skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md frontmatter has no version")
        assert match is not None
        version = tuple(int(g) for g in match.groups())
        self.assertGreaterEqual(version, (1, 2, 0),
                                "adding a reference doc must bump the minor version")

    def test_skill_md_description_stays_under_the_listing_limit(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        match = re.search(r"^description:\s*(.+?)\s*$", skill, re.MULTILINE)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertLess(len(match.group(1)), 60,
                        "Hermes truncates long descriptions in listings")

    def test_the_sibling_references_point_back(self) -> None:
        for path in (GETTING_STARTED_MD, KEY_MODS_MD, PROGRESSION_MD):
            self.assertIn("chunk-loading-guide.md", path.read_text(encoding="utf-8"),
                          f"{path.name} must point at the new page")

    def test_the_page_points_at_its_siblings(self) -> None:
        self.assertIn("## Cross-references", self.text)
        for sibling in ("getting-started.md", "key-mods.md", "progression.md",
                        "creative-checklist.md"):
            self.assertIn(sibling, self.text, f"the page must point at {sibling}")

    def test_the_key_mods_claim_about_pylons_is_true(self) -> None:
        """The page says key-mods.md calls the Pylons helpers 'chunk-ish' - keep it honest."""
        key_mods = deparen(KEY_MODS_MD.read_text(encoding="utf-8"))
        self.assertIn("chunk-area helpers that are not chunk loaders", key_mods)
        self.assertIn("chunk-loading-guide.md", key_mods)


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

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

    def test_this_suite_imports_no_network_or_process_module(self) -> None:
        imported = self.imported_modules(Path(__file__).read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set(),
                         "this suite must stay offline: no network, no subprocesses")
        self.assertTrue(imported <= {"re", "unittest", "pathlib", "__future__"},
                        f"unexpected import(s): {sorted(imported)}")

    def test_the_page_needs_no_script_and_no_network(self) -> None:
        text = GUIDE_MD.read_text(encoding="utf-8")
        self.assertNotIn("python3 scripts/", text,
                         "the page is a reference doc; it must not tell anyone to run a "
                         "script that fetches pack data")
        self.assertNotRegex(text, r"git clone")


if __name__ == "__main__":
    unittest.main()
