"""Offline contract for guide #21, verified against ATM-10 pack 8.2.

The fixture freezes selected quest records from chapters/{basic_logistics,mekanism}
.snbt and their lang/en_us counterparts at e5e3d1d83e. It is a snapshot, not a live
compatibility test. Tests require neither a pack checkout nor network access.
"""

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "references/logistics-guide.md"
FIXTURE = ROOT / "tests/fixtures/logistics_quests.json"
COMMIT = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"

# Independently reviewed explicit titles, with Minecraft formatting removed.
TITLES = {
    "6CD7D99AA102A5C3": "Logistics",
    "2329AA0AFBEF1E13": "Pipez",
    "36836AD948F96B9F": "Item Pipez",
    "33433A443B65D252": "Fluid Pipez",
    "53EC96FA0E7C4ED4": "Energy Pipez",
    "4FBAB3A0FBF8CE2F": "Universal Pipez",
    "2F4458E9921DEB86": "Gas Pipez",
    "5E116409DC7D30BB": "Mekanism Logistics",
    "60ECCCAB66AAC05D": "Logistical Transporters",
    "33C69B5934BE4D64": "Mechanical Pipes",
    "3AF1DC02E9A0010C": "Pressurized Tubes",
    "5F1218CF8EFC607B": "Laser IO",
    "4C41FD926F31180B": "Item Card",
    "1C70D739CE464E25": "Fluid Card",
    "6E05B62A40D5A891": "Integrated Dynamics",
    "6F152402756DA35E": "Item Importing",
    "034F2CDF0830254B": "Fluid Importing",
}
UNTITLED = {
    "2A976D41F79C34B1", "6A962535CD68713E", "5C0F6B1C93A52113",
    "47A2BEFB11F4D581", "6112956E19017D2D", "03C40D6A5D722543",
}


def plain(text):
    """Normalize only formatting and whitespace, never wording or punctuation."""
    text = re.sub(r"&[0-9a-fk-or]", "", text)
    text = text.replace("\\n", " ").replace("**", "").replace("`", "")
    return " ".join(text.split())


class TestLogisticsGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = GUIDE.read_text(encoding="utf-8")
        cls.flat = plain(cls.text)
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.records = {q["id"]: q for q in cls.fixture["quests"]}
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    def row(self, quest_id):
        rows = [line for line in self.text.splitlines()
                if line.startswith("|") and f"`{quest_id}`" in line]
        self.assertEqual(len(rows), 1, f"expected one table row for {quest_id}")
        return rows[0]

    def test_snapshot_and_source_paths(self):
        self.assertEqual(self.fixture["commit"], COMMIT)
        self.assertEqual(self.fixture["pack_version"], "8.2")
        for needle in (COMMIT, "2026-09-22", "pack 8.2", "config/bcc-common.toml"):
            self.assertIn(needle, self.text)
        for chapter in ("basic_logistics", "mekanism"):
            for directory in ("chapters", "lang/en_us/chapters"):
                self.assertIn(f"config/ftbquests/quests/{directory}/{chapter}.snbt",
                              self.text)

    def test_fixture_and_guide_contain_only_reviewed_ids(self):
        expected = set(TITLES) | UNTITLED
        self.assertEqual(set(self.records), expected)
        self.assertEqual(len(self.fixture["quests"]), len(expected))
        # The additional id is the verified prerequisite of Mekanism Logistics.
        self.assertEqual(set(re.findall(r"`([0-9A-F]{16})`", self.text)),
                         expected | {"4B35C01F5D0AAC58"})

    def test_explicit_titles_are_attached_to_correct_ids(self):
        for quest_id, title in TITLES.items():
            with self.subTest(quest_id=quest_id):
                self.assertEqual(plain(self.records[quest_id]["title"]), title)
                if title == "Logistics":
                    self.assertRegex(self.text, r"\*\*Logistics\*\* root\s+"
                                               r"\(`6CD7D99AA102A5C3`\)")
                else:
                    self.assertIn(f"**{title}**", self.row(quest_id))

    def test_untitled_quests_are_not_renamed_as_verified_titles(self):
        for quest_id in UNTITLED:
            with self.subTest(quest_id=quest_id):
                self.assertIsNone(self.records[quest_id]["title"])
                self.assertIn("*(no explicit title)*", self.row(quest_id))

    def test_direct_task_ids_and_filtered_tasks(self):
        for quest_id, q in self.records.items():
            for task in q["tasks"]:
                item = task["item"]
                if item["id"] == "ftbfiltersystem:smart_filter":
                    if quest_id != "6CD7D99AA102A5C3":
                        self.assertIn("filtered", self.row(quest_id))
                        self.assertIn("ftbfiltersystem:filter", item["components"])
                else:
                    self.assertIn(f"`{item['id']}`", self.row(quest_id))

    def test_all_block_quotes_are_exact_snapshot_excerpts(self):
        descriptions = [plain(line) for q in self.records.values()
                        for line in q["descriptions"]]
        quotes = [line[2:] for line in self.text.splitlines() if line.startswith("> ")]
        self.assertEqual(len(quotes), 6)
        for quote in quotes:
            with self.subTest(quote=quote):
                self.assertTrue(any(plain(quote) in desc for desc in descriptions),
                                f"unverified or altered quote: {quote}")

    def test_pipez_dependencies_not_a_linear_upgrade_ladder(self):
        self.assertEqual(set(self.records["4FBAB3A0FBF8CE2F"]["dependencies"]),
                         {"36836AD948F96B9F", "33433A443B65D252", "53EC96FA0E7C4ED4"})
        self.assertIn("depends on Item Pipez, Fluid Pipez, and Energy Pipez",
                      self.row("4FBAB3A0FBF8CE2F"))
        self.assertEqual(self.records["2F4458E9921DEB86"]["dependencies"],
                         ["2329AA0AFBEF1E13"])
        self.assertIn("depends on Pipez", self.row("2F4458E9921DEB86"))

    def test_other_branch_dependency_shapes(self):
        self.assertEqual(self.records["5E116409DC7D30BB"]["dependencies"],
                         ["4B35C01F5D0AAC58"])
        for quest_id in ("60ECCCAB66AAC05D", "33C69B5934BE4D64", "3AF1DC02E9A0010C"):
            self.assertEqual(self.records[quest_id]["dependencies"],
                             ["5E116409DC7D30BB"])
        for quest_id in ("6F152402756DA35E", "034F2CDF0830254B"):
            self.assertEqual(set(self.records[quest_id]["dependencies"]),
                             {"6112956E19017D2D", "03C40D6A5D722543"})
        self.assertIn("not on each other", self.flat)
        self.assertIn("both the cable quest and the variable-card quest", self.flat)
        for quest_id in ("5C0F6B1C93A52113", "4C41FD926F31180B", "1C70D739CE464E25",
                         "47A2BEFB11F4D581"):
            self.assertEqual(self.records[quest_id]["dependencies"],
                             ["5F1218CF8EFC607B"])

    def test_pipez_conflict_is_quoted_not_silently_resolved(self):
        self.assertIn("you need atleast an Advanced Upgrade", self.text)
        self.assertIn("Basic Upgrade allows Redstone Activation", self.text)
        self.assertIn("Do not resolve this contradiction", self.flat)
        self.assertIn("guarantee a minimum filtering tier", self.flat)
        self.assertIn("installed extraction GUI", self.flat)

    def test_resource_types_and_setup_caveats_are_preserved(self):
        for needle in ("do not extend that list to chemicals", "Extract", "Insert",
                       "Side Configs", "Auto-Eject", "Variable Card",
                       "doesn't move Sources of Fluid", "only moves Fluids from one Tank",
                       "Wrench mode is described as dropping", "NBT matching"):
            self.assertIn(needle, self.flat)
        universal = self.row("4FBAB3A0FBF8CE2F")
        self.assertNotIn("gas_pipe", universal)

    def test_grounding_and_deliberate_limits(self):
        for needle in ("## Grounding rules", "## Provenance", "## Cross-references",
                       "## What this page deliberately does not tell you",
                       "No recipes", "JEI are authoritative", "judgement",
                       "not a mandatory progression", "compatibility tests or benchmarks",
                       "Cross-dimensional links", "no throughput table"):
            self.assertIn(needle, self.text)
        self.assertNotRegex(self.text, r"\b\d+\s*(?:FE/t|mB/t|items/t)\b")
        self.assertNotIn("git clone", self.text)
        self.assertNotIn("python3 scripts/", self.text)

    def test_checklist_covers_failure_modes_without_default_disposal(self):
        checklist = self.text.split("## 5.", 1)[1].split("## What", 1)[0]
        for needle in ("Source and destination", "Resource type", "Extraction and insertion",
                       "Routing controls", "Network-specific parts", "Destination full",
                       "Only stops when you leave", "Moves, but slowly",
                       "Do not solve", "voiding", "both endpoints"):
            self.assertIn(needle, checklist)

    def test_skill_routes_topic_in_all_relevant_sections(self):
        sections = (
            ("## When to Use", "## When Not to Use"),
            ("## Research Grounding", "## Setup"),
            ("### 2.", "### 3."),
            ("## Completion Checklist", None),
        )
        for start, end in sections:
            text = self.skill.split(start, 1)[1]
            if end:
                text = text.split(end, 1)[0]
            self.assertIn("references/logistics-guide.md", text)
        self.assertIn("filter-tier conflict", self.skill)

    def test_sibling_links_exist_and_point_back(self):
        for name in ("getting-started.md", "key-mods.md", "progression.md",
                     "automation-first-steps.md"):
            self.assertIn("references/logistics-guide.md",
                          (ROOT / "references" / name).read_text(encoding="utf-8"))
            self.assertIn(f"references/{name}", self.text)
        for link in re.findall(r"`(references/[a-z0-9-]+\.md)`", self.text):
            self.assertTrue((ROOT / link).is_file(), f"broken reference: {link}")


if __name__ == "__main__":
    unittest.main()
