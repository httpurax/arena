#!/usr/bin/env python3
"""Offline contract for references/item-fluid-transport-guide.md (guide #21).

Stdlib-only and network-free. The reviewed fixture was extracted from
AllTheMods/ATM-10 e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025 (pack 8.2,
2026-09-22): basic_logistics and mekanism quest SNBT and their English lang
files. Explicit titles have only Minecraft formatting codes stripped; absent
ones are null, not inferred from task item names. Dependencies and task filter
components preserve the config's semantics. No external pack checkout is needed.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references" / "item-fluid-transport-guide.md"
FIXTURE = ROOT / "tests" / "fixtures" / "transport_quests.json"
PIN = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
SECTIONS = (
    "## Provenance — everything here was read, not remembered",
    "## Grounding rules (read before repeating any of this)",
    "## The choices at a glance",
    "## 1. Pipez — a first connection and its filters",
    "## 2. Mekanism — transport type and machine sides are separate checks",
    "## 3. Laser IO — nodes, extract cards, and insert cards",
    "## 4. Integrated Dynamics — importers, interfaces, and Variable Cards",
    "## When nothing moves — a diagnostic order (judgement)",
    "## Cross-references",
    "## What this page deliberately does not tell you",
)


class TestItemFluidTransportGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUIDE.read_text(encoding="utf-8")
        cls.flat = re.sub(r"\s+", " ", cls.text)
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.quests = cls.fixture["quests"]
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def section(self, heading):
        return self.text.split(heading, 1)[1].split("\n## ", 1)[0]

    def test_structure_and_substance(self):
        self.assertTrue(self.text.startswith("# Item and fluid transport in ATM10:"))
        self.assertIn("**What this page is.**", self.text)
        self.assertGreater(len(self.text.split()), 1500, "guide must not be a stub")
        positions = [self.text.index(heading) for heading in SECTIONS]
        self.assertEqual(positions, sorted(positions))
        for heading in SECTIONS[3:7]:
            section = self.section(heading)
            for marker in ("### Verified quest trail", "**Verified dependencies:**",
                           "**The pack's own words.**", "**What to do first (judgement).**"):
                self.assertIn(marker, section)

    def test_snapshot_and_source_paths(self):
        self.assertEqual(self.fixture["commit"], PIN)
        self.assertEqual(self.fixture["pack_version"], "8.2")
        self.assertEqual(self.fixture["date"], "2026-09-22")
        for value in (PIN, "e5e3d1d83e", "pack 8.2", "2026-09-22",
                      "AllTheMods/ATM-10", "examples/progress.example.json", '"8.x"'):
            self.assertIn(value, self.text)
        for path in self.fixture["source_files"]:
            self.assertIn(path, self.text)
        example = json.loads((ROOT / "examples" / "progress.example.json").read_text())
        self.assertIn("8.x", json.dumps(example))

    def test_verified_quest_rows_exactly_match_fixture(self):
        expected = []
        for quest in self.quests:
            title = (f"**{quest['title']}**" if quest["title"]
                     else "*No explicit quest title*")
            items = ", ".join(f"`{item}`" for item in quest["task_items"])
            row = f"| {title} | `{quest['id']}` | {items} |"
            expected.append(row)
            self.assertEqual(self.text.count(row), 1, quest["id"])
        actual = re.findall(r"^\| .*? \| `[0-9A-F]{16}` \| .*? \|$",
                            self.text, re.MULTILINE)
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), 20)
        self.assertEqual(len({quest["id"] for quest in self.quests}), 20)

    def test_no_unverified_quest_or_item_ids(self):
        ids = set(re.findall(r"`([0-9A-F]{16})`", self.text))
        self.assertEqual(ids, {quest["id"] for quest in self.quests})
        items = set(re.findall(r"\b[a-z][a-z0-9_]*:[a-z][a-z0-9_/]*", self.text))
        self.assertEqual(items, {item for quest in self.quests for item in quest["task_items"]})

    def test_quoted_sentences_match_reviewed_source(self):
        quoted = [quest for quest in self.quests if "quote" in quest]
        self.assertEqual(len(quoted), 8)
        for quest in quoted:
            with self.subTest(quest=quest["id"]):
                self.assertIn(quest["quote"], self.flat)

    def test_untitled_entries_are_never_renamed(self):
        untitled = [quest for quest in self.quests if quest["title"] is None]
        self.assertEqual(len(untitled), 6)
        for quest in untitled:
            self.assertIn(f"| *No explicit quest title* | `{quest['id']}` |", self.text)
        self.assertIn("device names are not replacement titles", self.flat)

    def test_dependency_branches_not_a_false_linear_ladder(self):
        by_id = {quest["id"]: quest for quest in self.quests}
        branches = (
            ("2329AA0AFBEF1E13", ("36836AD948F96B9F", "33433A443B65D252",
                                  "2F4458E9921DEB86", "2A976D41F79C34B1")),
            ("5E116409DC7D30BB", ("60ECCCAB66AAC05D", "33C69B5934BE4D64",
                                  "3AF1DC02E9A0010C")),
            ("5F1218CF8EFC607B", ("7BC8F50A89A3BE1A", "5C0F6B1C93A52113",
                                  "4C41FD926F31180B", "1C70D739CE464E25",
                                  "47A2BEFB11F4D581")),
        )
        for parent, children in branches:
            for child in children:
                self.assertEqual(by_id[child]["dependencies"], [parent])
        for child in ("6112956E19017D2D", "03C40D6A5D722543"):
            self.assertEqual(by_id[child]["dependencies"], ["6E05B62A40D5A891"])
        for child in ("6F152402756DA35E", "034F2CDF0830254B"):
            self.assertEqual(by_id[child]["dependencies"],
                             ["6112956E19017D2D", "03C40D6A5D722543"])
        for phrase in ("alternatives, not a mandatory progression ladder",
                       "They are sibling branches", "They are alternatives for different contents",
                       "all five entries after", "**both** of those untitled entries"):
            self.assertIn(phrase, self.flat)

    def test_smart_filter_tasks_keep_their_semantics(self):
        filtered = [quest for quest in self.quests
                    if quest["task_items"] == ["ftbfiltersystem:smart_filter"]]
        self.assertEqual(len(filtered), 3)
        for quest in filtered:
            expression = quest["task_components"][0]["ftbfiltersystem:filter"]
            self.assertTrue(expression.startswith("or("))
            self.assertEqual(len(re.findall(r"item\(", expression)), 4)
        self.assertIn("**they do not ask you to craft a generic smart filter**", self.flat)
        self.assertIn("across tiers", self.text)

    def test_operating_caveats_are_preserved(self):
        for phrase in ("Advanced Upgrade", "Whitelist or Blacklist", "NBT",
                       "Side Configs", "Auto-Eject", "Extract", "Insert",
                       "Variable Card", "not move fluid source blocks",
                       "Fluid is not a synonym", "not a measured sustainable transfer rate"):
            self.assertIn(phrase, self.flat)
        self.assertIn("The task is the destination tool", self.text)

    def test_grounding_and_deliberate_omissions(self):
        for phrase in ("in-game quest book (FTB Quests) and JEI are authoritative",
                       "his book wins", "Never invent", "approximate/judgement",
                       "not a quest requirement", "not recipes",
                       "not a requirement to finish every preceding mod"):
            self.assertIn(phrase, self.flat)
        omissions = self.section(SECTIONS[-1])
        for phrase in ("Recipes", "Transfer rates", "A mandatory mod order",
                       "Guaranteed wireless or cross-dimensional transport", "Unverified fixes"):
            self.assertIn(phrase, omissions)
        self.assertNotRegex(self.text, r"\b\d+(?:\.\d+)?\s*(?:FE/t|mB/t|items/t)\b")
        self.assertNotRegex(self.text, r"\b[XYZ]\s*=\s*-?\d+")

    def test_diagnostic_order_and_scope(self):
        diagnostic = self.section(SECTIONS[7])
        steps = re.findall(r"^\d\. \*\*([^*]+)\*\*", diagnostic, re.MULTILINE)
        self.assertEqual(steps, ["What are you moving?", "Is extraction actually configured?",
                                "Can the destination accept it?", "Is a filter excluding it?",
                                "Does it stop only when you leave?",
                                "Does it move, but the game stalls?"])
        for phrase in ("Transport is not chunk loading", "FPS from TPS",
                       "never promise", "ask for the pack version"):
            self.assertIn(phrase, re.sub(r"\s+", " ", diagnostic))

    def test_cross_references_exist_and_sibling_links_back(self):
        paths = set(re.findall(r"`(references/[a-z0-9-]+\.md)`", self.text))
        self.assertGreaterEqual(len(paths), 7)
        for path in paths:
            self.assertTrue((ROOT / path).is_file(), path)
        sibling = (ROOT / "references" / "automation-first-steps.md").read_text()
        self.assertIn("references/item-fluid-transport-guide.md", sibling)

    def test_skill_routes_and_grounding_are_wired(self):
        for start, end in (("## When to Use", "## When Not to Use"),
                           ("## Research Grounding", "## Setup"),
                           ("## Behaviors", "### 3."),
                           ("## Completion Checklist", None)):
            section = self.skill.split(start, 1)[1]
            if end:
                section = section.split(end, 1)[0]
            self.assertIn("references/item-fluid-transport-guide.md", section)
        for phrase in ("Which pipes should I use?", "how do I filter outputs?",
                       "why does nothing move?", "fluids are not chemicals"):
            self.assertIn(phrase, self.skill)
        version = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)$", self.skill, re.MULTILINE)
        self.assertIsNotNone(version)
        self.assertGreaterEqual(tuple(map(int, version.groups())), (1, 6, 0))
        description = re.search(r"^description:\s*(.*)$", self.skill, re.MULTILINE)
        self.assertIsNotNone(description)
        self.assertLess(len(description.group(1)), 60)

    def test_suite_is_offline_and_document_needs_no_commands(self):
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split(".")[0])
        self.assertLessEqual(imports, {"__future__", "ast", "json", "re", "unittest", "pathlib"})
        for command in ("git clone", "curl ", "python3 scripts/", "```bash"):
            self.assertNotIn(command, self.text)


if __name__ == "__main__":
    unittest.main()
