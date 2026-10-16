#!/usr/bin/env python3
"""Offline regression checks for the ATM10 teleportation guide.

Reviewed against AllTheMods/ATM-10 at e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025
(pack 8.2, 2026-09-22): Welcome, Allthemodium, Mekanism and Just Dire Things quest
chapters and English lang files; waystones-common.toml; bcc-common.toml; modlist.json.
The expected data are frozen here, not fetched by the tests. These checks guard the
published snapshot and routing, not future pack/server updates.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references" / "teleportation-guide.md"
SKILL = ROOT / "SKILL.md"

# Explicit quest/task ids from the four named chapters. Never derive a quest title
# from an item's display name, especially for the four untitled JDT entries.
VERIFIED_ENTRY_IDS = {
    "7658C1C663394E85",  # Welcome: untitled quest, Useful Commands task
    "10A16F89D4AD238D",  # Welcome: Useful Commands task
    "07FDA46D83F8360D",  # Teleport Pad
    "201EE3566D4D3123",  # Allthemodium Ingot
    "2C4299D33D419AA0",  # Overworld
    "0CC0632E8276C787",  # The Nether
    "2EDE91023F7924FB",  # The End
    "7B0DFA55B4D8B16D",  # Custom Portals!
    "2EA0C74AE7366656",  # Portable Teleporter
    "16E02F671FBE9148",  # JDT Portal Gun task
    "4F9932477EDDCB8E",  # JDT Advanced Portal Gun task
    "0B9BBE2A764631BF",  # JDT Simple Swapper task
    "27FD46A8C958D259",  # JDT Totem of Death Recall task
}

# Task item ids and dimension ids actually used by the guide. These were read
# independently from the quest files and Waystones config at the pinned commit.
VERIFIED_NAMESPACED_IDS = {
    "allthemodium:teleport_pad", "allthemodium:mining",
    "allthemodium:the_other", "allthemodium:the_beyond",
    "minecraft:overworld", "minecraft:the_nether", "minecraft:the_end",
    "minecraft:wither",  # Waystones' entityDenyList, not a quest item
    "mekanism:teleporter_frame", "mekanism:teleporter",
    "mekanism:portable_teleporter",
    "justdirethings:portalgun", "justdirethings:portalgun_v2",
    "justdirethings:blockswappert1", "justdirethings:totem_of_death_recall",
}

# Chapter 2 quest title, quest id, description's destination, and dimension task.
PAD_ROUTES = (
    ("Overworld", "2C4299D33D419AA0", "Mining Dimension", "allthemodium:mining",
     "minecraft:overworld"),
    ("The Nether", "0CC0632E8276C787", "The Other", "allthemodium:the_other",
     "minecraft:the_nether"),
    ("The End", "2EDE91023F7924FB", "The Beyond", "allthemodium:the_beyond",
     "minecraft:the_end"),
)

JDT_TASKS = (
    ("16E02F671FBE9148", "justdirethings:portalgun"),
    ("4F9932477EDDCB8E", "justdirethings:portalgun_v2"),
    ("0B9BBE2A764631BF", "justdirethings:blockswappert1"),
    ("27FD46A8C958D259", "justdirethings:totem_of_death_recall"),
)


def section(text: str, heading: str) -> str:
    """Return a top-level Markdown section, without pulling in its neighbours."""
    marker = "## " + heading + "\n"
    start = text.index(marker)
    end = text.find("\n## ", start + len(marker))
    return text[start:end if end != -1 else None]


def flat(text: str) -> str:
    return " ".join(text.split())


class TestTeleportationGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = GUIDE.read_text(encoding="utf-8")
        cls.skill = SKILL.read_text(encoding="utf-8")

    def test_exists_and_has_the_same_structure_as_the_other_guides(self) -> None:
        self.assertGreater(len(self.text.splitlines()), 130)
        expected = (
            "Provenance — everything here was read, not remembered",
            "Grounding rules (read before repeating any of this)",
            "Choose the right kind of travel",
            "1. First trip home: the Welcome chapter's commands",
            "2. Waystones: repeatable stops, not guaranteed village loot",
            "3. The Teleport Pad is for three ATM dimensions",
            "4. Built destinations: Mekanism's powered Teleporters",
            "5. Other tracked travel tools (optional, later: judgement)",
            "If a teleport does not work", "Cross-references",
            "What this page deliberately does not tell you",
        )
        positions = [self.text.index("## " + heading + "\n") for heading in expected]
        self.assertEqual(positions, sorted(positions))

    def test_pinned_sources_and_limits_are_explicit(self) -> None:
        for needle in (
            "e5e3d1d83e", "2026-09-22", "pack 8.2", "modpackVersion = \"8.2\"",
            "config/ftbquests/quests/chapters/", "lang/en_us/chapters/",
            "config/waystones-common.toml", "config/crash_assistant/modlist.json",
            "config/bcc-common.toml", "FTB Essentials 2101.1.10",
            "Waystones 21.1.45", "Mekanism 10.7.19", "Just Dire Things 1.5.7",
            "JourneyMap 1.21.1-6.0.9", "per-world", "does **not** ship",
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.text)
        rules = section(self.text, "Grounding rules (read before repeating any of this)")
        for needle in ("in-game quest book (FTB Quests) and JEI are authoritative",
                       "quests are optional", "Mods are not gated", "judgement",
                       "not a quest title", "server/quest book"):
            self.assertIn(needle, flat(rules))

    def test_welcome_task_is_not_misnamed_a_quest(self) -> None:
        home = section(self.text, "1. First trip home: the Welcome chapter's commands")
        for needle in ("7658C1C663394E85", "10A16F89D4AD238D", "untitled quest",
                       "**task** title **Useful Commands**", "type `checkmark`",
                       "no dependencies", "/sethome farm", "/home farm", "/spawn",
                       "/rtp", "Overworld", "random location"):
            self.assertIn(needle, flat(home))
        self.assertLess(home.index("/sethome farm"), home.index("/home farm"))
        self.assertIn("saves/(name of save)/serverconfig/ftbessentials.snbt", home)
        self.assertIn("world/serverconfig/ftbessentials.snbt", home)
        self.assertIn("without giving any numbers", flat(home))
        self.assertIn("not settings shipped", flat(home))

    def test_waystones_settings_are_config_values_not_quest_promises(self) -> None:
        waystones = section(self.text,
                            "2. Waystones: repeatable stops, not guaranteed village loot")
        values = (
            '`spawnInVillages = "REGULAR"`', "some", "not every village",
            "`chunksBetweenWildWaystones = 25`", "approximate",
            "`wildWaystonesDimensionAllowList`", "`minecraft:overworld`",
            "`minecraft:the_nether`", "`minecraft:the_end`", "wild generation",
            "`enableCosts = false`", "not an active XP toll",
            "`enableCooldowns = true`", "`add_cooldown(inventory_button, 300)`",
            "not claim a 300-tick cooldown on every teleport",
            '`transportPets = "DISABLED"`', '`transportLeashed = "ENABLED"`',
            "`minecraft:wither`", "`journeyMap = true`", "activated",
            '`inventoryButton = ""`', "not a quest", "JEI",
        )
        for needle in values:
            with self.subTest(needle=needle):
                self.assertIn(needle, waystones)
        self.assertIn("it does not say where a placed stone can be used", flat(waystones))
        self.assertNotIn("Waystones quest", waystones)

    def test_pad_quests_are_distinct_from_destinations_and_home(self) -> None:
        pad = section(self.text, "3. The Teleport Pad is for three ATM dimensions")
        self.assertRegex(flat(pad),
                         r"\*\*Teleport Pad\*\* quest `07FDA46D83F8360D` asks for one "
                         r"`allthemodium:teleport_pad` and follows "
                         r"\*\*Allthemodium Ingot\*\* \(`201EE3566D4D3123`\)")
        self.assertIn("**two** pads", pad)
        self.assertIn("both main and offhand empty", pad)
        rows = [line for line in pad.splitlines() if line.startswith("| **")]
        self.assertEqual(len(rows), 3)
        for row, (name, quest, destination, dimension, task_dimension) in zip(rows, PAD_ROUTES):
            with self.subTest(quest=quest):
                self.assertEqual(row.split("|")[1].strip(), f"**{name}**")
                self.assertIn(f"`{quest}`", row)
                self.assertIn(f"{destination} (`{dimension}`)", row)
                self.assertIn(f"`{task_dimension}`", pad)
        self.assertIn("`dimension` tasks", pad)
        self.assertIn("not from those task payloads", flat(pad))
        self.assertIn("not a named-home Waystone", pad)

    def test_mekanism_network_dependency_and_power_are_not_conflated(self) -> None:
        mekanism = section(self.text, "4. Built destinations: Mekanism's powered Teleporters")
        for title, quest, parent, task in (
            ("Custom Portals!", "7B0DFA55B4D8B16D", "Metallurgic Infuser",
             "mekanism:teleporter_frame"),
            ("Portable Teleporter", "2EA0C74AE7366656", "Chargepad",
             "mekanism:portable_teleporter"),
        ):
            with self.subTest(quest=quest):
                row = next(line for line in mekanism.splitlines()
                           if line.startswith("| **" + title + "**"))
                self.assertIn(f"`{quest}`", row)
                self.assertIn(f"**{parent}**", row)
                self.assertIn(f"`{task}`", row)
        self.assertIn("9 `mekanism:teleporter_frame` and 1 `mekanism:teleporter`", mekanism)
        for needle in ("named network", "powered", "charge it", "owner",
                       "Portable Teleporter, it's an Item", "**not** *Custom Portals!*",
                       "no general energy budget", "unloaded base"):
            self.assertIn(needle, flat(mekanism))

    def test_optional_jdt_tasks_stay_untitled_and_described_only_from_quest_text(self) -> None:
        other = section(self.text, "5. Other tracked travel tools (optional, later: judgement)")
        self.assertIn("**None has a quest title in", other)
        rows = [line for line in other.splitlines() if line.startswith("| `")]
        self.assertEqual(len(rows), len(JDT_TASKS))
        for row, (quest, task) in zip(rows, JDT_TASKS):
            with self.subTest(quest=quest):
                self.assertTrue(row.startswith(f"| `{quest}` — `{task}` |"))
        for needle in ("left-click blue", "right-click orange", "power **and portal fluid**",
                       "**default** keybind", "Ferricore wrench", "**one-time use**",
                       "not a standing `/home`", "**not invented quest titles**"):
            self.assertIn(needle, flat(other))

    def test_all_quoted_ids_are_from_the_verified_snapshot(self) -> None:
        self.assertEqual(set(re.findall(r"`([0-9A-F]{16})`", self.text)), VERIFIED_ENTRY_IDS)
        ids = set(re.findall(r"`([a-z][a-z0-9_]*:[a-z0-9_./-]+)`", self.text))
        self.assertEqual(ids, VERIFIED_NAMESPACED_IDS)

    def test_no_invented_mechanics_and_sibling_links_exist(self) -> None:
        limits = section(self.text, "What this page deliberately does not tell you")
        for needle in ("No invented `/back`, `/tpa`", "No guaranteed Waystone",
                       "No arbitrary Teleport Pad destination", "not** a chunk loader",
                       "No coordinates, guessed recipes", "server's actual settings"):
            self.assertIn(needle, limits)
        links = set(re.findall(r"`references/([a-z0-9-]+\.md)`", self.text))
        self.assertEqual(links, {
            "first-hour-walkthrough.md", "getting-started.md", "dimension-guide.md",
            "flight-guide.md", "chunk-loading-guide.md", "power-guide.md",
        })
        for link in links:
            self.assertTrue((ROOT / "references" / link).is_file(), link)

    def test_skill_and_sibling_docs_route_the_question_to_this_page(self) -> None:
        name = "references/teleportation-guide.md"
        for heading in ("When to Use", "Research Grounding (read before advising)",
                        "Behaviors", "Completion Checklist"):
            with self.subTest(heading=heading):
                self.assertIn(name, section(self.skill, heading))
        for word in ("/home", "Waystones", "Teleport Pad", "Mekanism", "judgement",
                     "serverconfig", "powered destination"):
            self.assertIn(word, self.skill)
        self.assertIn("version: 1.5.0", self.skill)
        for sibling in ("getting-started.md", "progression.md", "dimension-guide.md"):
            with self.subTest(sibling=sibling):
                text = (ROOT / "references" / sibling).read_text(encoding="utf-8")
                self.assertIn(name, text)
        self.assertNotIn("Waystones from village loot",
                         (ROOT / "references/progression.md").read_text(encoding="utf-8"))

    def test_this_suite_is_network_free(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        imports = set(re.findall(r"^(?:from|import)\s+([a-zA-Z_][\w]*)", source, re.M))
        self.assertEqual(imports & {"socket", "urllib", "http", "requests", "subprocess",
                                    "ftplib", "smtplib", "webbrowser"}, set())


if __name__ == "__main__":
    unittest.main()
