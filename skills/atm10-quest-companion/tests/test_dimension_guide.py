#!/usr/bin/env python3
"""Offline tests for references/dimension-guide.md (atm10-quest-companion).

Stdlib-only and network-free: the page is a static Markdown file, so every case reads it
from disk and checks it against constants transcribed from the pack's quest config at the
pinned commit (AllTheMods/ATM-10 ``main`` @ e5e3d1d83e, pack 8.2) and against the skill's
own shipped example file.

Covered:

  * existence and grounding: the page is not a stub, states the skill's grounding rules
    (in-game quest book + JEI authoritative, uncertain details approximate, nothing
    invented), names the pack-repository files it was read from, and dates itself to the
    pinned commit, ``CHANGELOG.md``, pack 8.2, and the skill's 8.x stamp;
  * structure: the required sections in order; the at-a-glance table has one row per
    destination (13), in the recommended order, with the verified dimension id, an unlock
    quest, and a stage tag that matches ``examples/progress.example.json``; the 13
    numbered per-dimension sections each carry *Unlocked by / Chapter / stage / Roughly
    when / Go there for*; the Teleport Pad routing table; an eight-step visit order whose
    steps are each marked verified or approximate;
  * key content: all 12 dimension ids the config's 28 ``dimension`` tasks name; the
    Twilight Forest tracked by ``twilightforest:root`` with no invented dimension id; the
    verified unlock quest titles, chapter ids, quest counts, mod versions, and quotes; the
    star-component cross-links;
  * grounding guards: every namespaced id on the page is on the config-verified list,
    no coordinates, no portal crafting recipe reproduced, in-page anchors resolve, and
    the sibling docs the page points at exist;
  * the rest of the skill points at the page (SKILL.md, progression.md, key-mods.md,
    boss-checklist.md), and this suite imports no network module.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_ROOT / "references"
GUIDE_MD = REFERENCES / "dimension-guide.md"
SKILL_MD = SKILL_ROOT / "SKILL.md"
PROGRESSION_MD = REFERENCES / "progression.md"
KEY_MODS_MD = REFERENCES / "key-mods.md"
BOSS_CHECKLIST_MD = REFERENCES / "boss-checklist.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# Where the page was read from: the same four sources as the endgame docs, at the same
# pinned commit as the Chapter 4 checklist.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
)
PINNED_COMMIT = "e5e3d1d83e"
PINNED_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"

# The 12 dimension ids named by the config's 28 `dimension` tasks (15 chapters, pack 8.2).
CONFIG_DIMENSION_IDS = (
    "minecraft:overworld",
    "minecraft:the_nether",
    "minecraft:the_end",
    "aether:the_aether",
    "undergarden:undergarden",
    "the_bumblezone:the_bumblezone",
    "deeperdarker:otherside",
    "eternal_starlight:starlight",
    "allthemodium:mining",
    "allthemodium:the_other",
    "allthemodium:the_beyond",
    "neovitae:dungeon",
)

# The 13 destinations in the page's recommended order: (name, dimension id or None).
# The Twilight Forest has no `dimension` task; its chapter tracks entry with the
# advancement `twilightforest:root`.
DESTINATIONS = (
    ("Overworld", "minecraft:overworld"),
    ("The Nether", "minecraft:the_nether"),
    ("The Twilight Forest", None),
    ("The End", "minecraft:the_end"),
    ("The Bumblezone", "the_bumblezone:the_bumblezone"),
    ("The Aether", "aether:the_aether"),
    ("The Undergarden", "undergarden:undergarden"),
    ("The Otherside", "deeperdarker:otherside"),
    ("The Starlight", "eternal_starlight:starlight"),
    ("Mining Dimension", "allthemodium:mining"),
    ("The Other", "allthemodium:the_other"),
    ("The Beyond", "allthemodium:the_beyond"),
    ("Neo Vitae's realm", "neovitae:dungeon"),
)
VANILLA = frozenset({"Overworld", "The Nether", "The End"})

# Verified quest titles on the way into each dimension (en_us lang files, pack 8.2).
UNLOCK_QUESTS = {
    "Overworld": ("Welcome to All The Mods 10!",),
    "The Nether": ("To The Nether!", "We've Struck Diamonds!"),
    "The Twilight Forest": ("Welcome to the Twilight Forest!",),
    "The End": ("Finding The End", "The End"),
    "The Bumblezone": ("The Bumblezone!", "Into the Hive"),
    "The Aether": ("Aether Portal", "The Aether"),
    "The Undergarden": ("The Undergarden", "Welcome to the Undergarden!"),
    "The Otherside": ("Visit an Ancient City", "Kill the Warden", "Heart of the Deep",
                      "The Otherside"),
    "The Starlight": ("The Gatekeeper and The Gate", "Eternal Starlight", "Orb of Prophecy"),
    "Mining Dimension": ("Teleport Pad", "Overworld", "Mining Dimension"),
    "The Other": ("Teleport Pad", "The Nether", "The Other", "Ice and Fire"),
    "The Beyond": ("Teleport Pad", "The End", "The Beyond"),
    "Neo Vitae's realm": ("Tier III: The Master's Orb", "Highway to Hell",
                          "Breaching the Veil"),
}

# Chapter config ids each destination belongs to, with the chapter's title and quest count
# in pack 8.2 (cross-checked against the shipped example file below).
DESTINATION_CHAPTERS = {
    "Overworld": ("welcome",),
    "The Nether": ("mainquestline_part_1",),
    "The Twilight Forest": ("twilight_forest",),
    "The End": ("mainquestline_part_1",),
    "The Bumblezone": ("bumblezone",),
    "The Aether": ("aether",),
    "The Undergarden": ("undergarden",),
    "The Otherside": ("deeper_and_darker",),
    "The Starlight": ("eternal_starlight",),
    "Mining Dimension": ("allthemodium",),
    "The Other": ("allthemodium", "ice__fire"),
    "The Beyond": ("allthemodium",),
    "Neo Vitae's realm": ("neo_vitae",),
}
CHAPTER_QUEST_COUNTS = {
    "welcome": ("Welcome", 6),
    "mainquestline_part_1": ("Chapter 1: The Beginning", 36),
    "twilight_forest": ("The Twilight Forest", 56),
    "bumblezone": ("The Bumblezone", 114),
    "aether": ("The Aether", 73),
    "undergarden": ("The Undergarden", 82),
    "deeper_and_darker": ("Deeper and Darker", 45),
    "eternal_starlight": ("Eternal Starlight", 193),
    "allthemodium": ("Chapter 2: Allthemodium", 54),
    "ice__fire": ("Ice and Fire", 87),
    "neo_vitae": ("Neo Vitae", 49),
}

# Mod display names and versions from config/crash_assistant/modlist.json at the commit.
MOD_VERSIONS = (
    "The Twilight Forest 4.8.3345",
    "The Bumblezone 7.16.1",
    "The Aether 1.5.10",
    "The Undergarden 0.9.6",
    "Deeper and Darker 1.4.1",
    "Eternal Starlight 0.9.1",
    "Allthemodium 3.0.1",
    "Ice And Fire Community Edition 2.0-beta.17",
    "Neo Vitae 1.1.26",
)

# Every namespaced id the page may print -- each one read from the config at the commit
# (task item/entity/dimension/structure/biome/advancement values). A new id on the page
# must be verified against the config and added here on purpose: nothing is invented.
VERIFIED_IDS = frozenset({
    # dimensions
    *CONFIG_DIMENSION_IDS,
    # advancements
    "twilightforest:root",
    "minecraft:story/enter_the_nether",
    "minecraft:story/follow_ender_eye",
    "minecraft:end/dragon_egg",
    "the_bumblezone:the_queens_desire/the_beginning",
    # structures
    "minecraft:ancient_city",
    "#eternal_starlight:portal_ruins",
    "allthemodium:ancient_pyramid",
    "undergarden:catacombs",
    # biomes (The Other's own, as Ice and Fire's biome quests name them)
    "allthemodium:soul_sand_valley",
    "allthemodium:warped_forest",
    "allthemodium:desert",
    "allthemodium:crimson_forest",
    # entity
    "minecraft:warden",
    # task items
    "minecraft:obsidian",
    "minecraft:diamond",
    "minecraft:ender_eye",
    "minecraft:netherite_ingot",
    "minecraft:glowstone",
    "minecraft:water_bucket",
    "twilightforest:snow_queen_trophy",
    "undergarden:catalyst",
    "deeperdarker:heart_of_the_deep",
    "eternal_starlight:orb_of_prophecy",
    "eternal_starlight:seeking_eye",
    "eternal_starlight:chain_of_souls",
    "allthemodium:teleport_pad",
    "allthemodium:piglich_heart",
    "neovitae:blood_orb_master",
    "neovitae:ritual_diviner_dusk",
    "neovitae:standard_key",
    "neovitae:mine_entrance_key",
    "neovitae:mine_key",
})

# Sentences quoted from the quest descriptions (verbatim, pack 8.2).
KEY_QUOTES = (
    "In this modpack, quests are optional. Mods are not gated behind completing any quests!",
    "also allow you to visit new dimensions like the Twilight Forest!",
    "make a 2x2 hole in the ground and fill it with water. Surround the edges of the hole "
    "with flowers, and throw a Diamond into the water.",
    "Place the Teleport Pad in the Overworld to go to the Mining Dimension.",
    "Place the Teleport Pad in The Nether to go to The Other.",
    "Place the Teleport Pad in The End to go to The Beyond.",
    "To teleport you need to shift right click with your main and offhand empty!",
    "The Gatekeeper will also deem you worthy if you have defeated the Ender Dragon, and "
    "allow you to skip the duel.",
    "We can use the Heart of the Deep on a frame of Reinforced Deepslate to get our Portal "
    "to the Otherside.",
    "Once formed, you can activate it by using the Catalyst on it.",
    "Then you'll need to either throw an Enderpearl into it or have a Piston push you into it!",
    "Welcome to Ice and Fire! Now in The Other",
    "You can find it rarely in The Nether or abundantly in The Other.",
    "There's nothing here!",
    "No it isn't found in The Beyond.",
    "The Highway to Hell ritual opens a permanent gate into the Endless Realm.",
    "Only the Antechamber, past the veil, grows this strange fruit.",
)

# Chapter 3 / Chapter 4 tasks and the star component each feeds (config dependency links).
STAR_LINKS = (
    ("Snow Queen Trophy", "Oblivion Shard"),
    ("Heart of the Deep", "Wither's Compass"),
    ("Chain of Souls", "Dragon Soul"),
    ("Piglich Heart Block", "Dragon Soul"),
    ("Soul Lava Bee Spawn Egg", "Dragon Soul"),
    ("Soul Binding Crystal", "Top ATM Star part"),
    ("Abyssal Sacrifice", "Dragon Soul"),
    ("Void Forge", "Oblivion Shard"),
    ("Meat Shredder", "Oblivion Shard"),
)

# Quest text the page must never reproduce: the Teleport Pad quest's crafting recipe
# (recipes are JEI's) and the Aether portal quest's joke, which is not the frame.
NOT_REPRODUCED = (
    "4 Allthemodium Nuggets",
    "Nuggets and an Ender Pearl",
    "4x5 Glowstone",
)

COORDINATE_PATTERNS = (
    re.compile(r"\b[xyz]\s*[=:]\s*-?\d", re.IGNORECASE),            # x=100, y: 64
    re.compile(r"\by\s*(?:level\s*)?-?\d+\b", re.IGNORECASE),        # Y -40, Y Level 0
    re.compile(r"-?\d+\s*,\s*-?\d+\s*,\s*-?\d+"),                    # 100, 64, -200
    re.compile(r"\b\d+\s*k\b", re.IGNORECASE),                       # 10k
    re.compile(r"\bx\s*/\s*z\b", re.IGNORECASE),                     # X/Z
    re.compile(r"multiple of", re.IGNORECASE),                       # "a multiple of 10k"
)

EXPECTED_SECTIONS = (
    "Provenance",
    "Grounding rules",
    "The dimensions at a glance",
    "Dimension by dimension",
    "The recommended visit order",
    "Where the dimensions meet the ATM Star",
    "Related pages",
    "What this page deliberately does not tell you",
)
SIBLING_DOCS = ("boss-checklist.md", "atm-star-checklist.md", "creative-checklist.md",
                "progression.md", "key-mods.md")
STAGE_IDS = ("early-game", "tech", "magic", "endgame")
FIELDS = ("**Unlocked by:**", "**Chapter / stage:**", "**Roughly when:**", "**Go there for:**")

ID_TOKEN = re.compile(r"#?\b[a-z0-9_]+:[a-z0-9_./]*[a-z0-9_]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def flatten(text: str) -> str:
    """Collapse wrapped Markdown lines so multi-line sentences can be matched whole."""
    return re.sub(r"\s+", " ", text)


def h2_sections(text: str) -> "list[tuple[str, str]]":
    """[(heading, body)] for every '## ' section, in document order."""
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def section(text: str, heading_prefix: str) -> str:
    for heading, body in h2_sections(text):
        if heading.startswith(heading_prefix):
            return body
    return ""


def h3_sections(body: str) -> "list[tuple[str, str]]":
    parts = re.split(r"^### (.+)$", body, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def table_rows(body: str) -> "list[list[str]]":
    """Data rows of the first Markdown table in ``body``, as stripped cells."""
    rows: "list[list[str]]" = []
    in_table = False
    for line in body.splitlines():
        if line.startswith("|"):
            in_table = True
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append(cells)
        elif in_table:
            break
    # rows[0] is the header, rows[1] the |---| separator.
    return rows


def github_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\- ]", "", slug)
    return slug.replace(" ", "-")


class GuideTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(GUIDE_MD)
        cls.lower = cls.text.lower()
        cls.flat = flatten(cls.text)
        cls.flat_lower = cls.flat.lower()


# --------------------------------------------------------------------------------------
# existence, provenance, grounding rules
# --------------------------------------------------------------------------------------

class TestExistenceAndGrounding(GuideTestCase):

    def test_page_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.text.strip()), 15000, "dimension-guide.md looks like a stub")
        self.assertTrue(self.text.startswith("# Dimension guide"),
                        "the page must open with its '# Dimension guide' title")

    def test_states_the_skill_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lower, f"must state the {needle!r} rule")
        self.assertRegex(self.lower, r"never invented|not invented|never invent",
                         "must say its details were read, not invented")
        self.assertIn("approximate by construction", self.flat_lower)

    def test_names_its_sources_and_dates_itself(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source.lower(), self.lower, f"must name its source: {source}")
        self.assertIn(PINNED_COMMIT, self.text)
        self.assertIn(PINNED_COMMIT_FULL, self.text, "the commit link must be the full SHA")
        self.assertIn("CHANGELOG.md", self.text)
        self.assertIn("pack 8.2", self.text)
        self.assertIn("8.x", self.text, "must tie the version read to the skill's 8.x stamp")

    def test_says_how_the_list_was_built(self) -> None:
        for needle in ("66 chapter files", "4,790 quests", "**28**", "15 chapters",
                       "**12 dimension ids**", "**13 destinations**"):
            self.assertIn(needle, self.flat, f"provenance must state {needle!r}")

    def test_the_book_gates_nothing_and_portals_are_quoted_not_reconstructed(self) -> None:
        self.assertIn("The book gates nothing.", self.flat)
        self.assertIn("**No portal recipes:**", self.flat)
        self.assertIn("**No coordinates.**", self.flat)
        self.assertIn("never filled in from memory", self.flat)
        self.assertIn("does not tell you", self.flat_lower)


# --------------------------------------------------------------------------------------
# structure
# --------------------------------------------------------------------------------------

class TestStructure(GuideTestCase):

    def test_required_sections_in_order(self) -> None:
        headings = [heading for heading, _ in h2_sections(self.text)]
        self.assertEqual(len(headings), len(EXPECTED_SECTIONS), headings)
        for heading, expected in zip(headings, EXPECTED_SECTIONS):
            self.assertTrue(heading.startswith(expected), f"{heading!r} != {expected!r}")

    def test_at_a_glance_table_has_one_row_per_destination_in_order(self) -> None:
        rows = table_rows(section(self.text, "The dimensions at a glance"))
        header, data = rows[0], rows[2:]
        for column in ("Dimension", "Dimension id", "Unlocked by", "Chapter", "Stage tag",
                       "Roughly when", "Go there for"):
            self.assertTrue(any(cell.startswith(column) for cell in header),
                            f"at-a-glance table needs a {column!r} column: {header}")
        self.assertEqual(len(data), len(DESTINATIONS))
        for index, (cells, (name, dimension_id)) in enumerate(zip(data, DESTINATIONS), 1):
            number, dimension, id_cell, unlocked, _chapter, stage, when, purpose = cells
            self.assertEqual(number, str(index))
            self.assertTrue(dimension.startswith(name), f"row {index}: {dimension!r}")
            if dimension_id is None:
                self.assertIn("twilightforest:root", id_cell)
                self.assertTrue(id_cell.startswith("none"), id_cell)
            else:
                self.assertEqual(id_cell, f"`{dimension_id}`")
            self.assertTrue(any(f"*{title}*" in unlocked for title in UNLOCK_QUESTS[name]),
                            f"row {index} must name a verified unlock quest: {unlocked!r}")
            self.assertRegex(stage, r"^`(%s)`$" % "|".join(STAGE_IDS))
            self.assertTrue(when and purpose, f"row {index} has an empty cell")

    def test_stage_tags_match_the_shipped_example_file(self) -> None:
        example = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        stages = {chapter["id"]: chapter["stage"] for chapter in example["chapters"]}
        titles = {chapter["id"]: chapter["title"] for chapter in example["chapters"]}
        rows = table_rows(section(self.text, "The dimensions at a glance"))[2:]
        for cells, (name, _) in zip(rows, DESTINATIONS):
            chapter_cell, stage_cell = cells[4], cells[5].strip("`")
            for chapter_id in DESTINATION_CHAPTERS[name]:
                self.assertIn(chapter_id, stages, f"{chapter_id} is not a known chapter")
                self.assertTrue(f"`{chapter_id}`" in chapter_cell
                                or titles[chapter_id] in chapter_cell,
                                f"{name}: chapter cell must name {chapter_id}")
                self.assertEqual(stage_cell, stages[chapter_id],
                                 f"{name}: stage tag must match the example file")

    def test_thirteen_numbered_dimension_sections_with_the_four_fields(self) -> None:
        sections = [(heading, body) for heading, body
                    in h3_sections(section(self.text, "Dimension by dimension"))
                    if re.match(r"\d+\. ", heading)]
        self.assertEqual(len(sections), len(DESTINATIONS))
        for index, ((heading, body), (name, dimension_id)) in enumerate(
                zip(sections, DESTINATIONS), 1):
            self.assertTrue(heading.startswith(f"{index}. {name}"), heading)
            if dimension_id is None:
                self.assertNotIn("`", heading, "the Twilight Forest has no dimension id")
            else:
                self.assertIn(f"`{dimension_id}`", heading)
            for field in FIELDS:
                self.assertIn(field, body, f"section {heading!r} is missing {field}")
            if name not in VANILLA:
                self.assertIn("**Star relevance:**", body, heading)
            for title in UNLOCK_QUESTS[name]:
                self.assertIn(f"*{title}*", flatten(body), f"{heading!r} must name *{title}*")
            for chapter_id in DESTINATION_CHAPTERS[name]:
                chapter_note = (f"`{chapter_id}`" in body
                                or CHAPTER_QUEST_COUNTS[chapter_id][0] in body)
                self.assertTrue(chapter_note, f"{heading!r} must name chapter {chapter_id}")

    def test_teleport_pad_table_routes_each_vanilla_dimension(self) -> None:
        body = section(self.text, "Dimension by dimension")
        pad = [b for heading, b in h3_sections(body) if heading.startswith("The Teleport Pad")]
        self.assertEqual(len(pad), 1, "the Teleport Pad block must exist exactly once")
        rows = table_rows(pad[0])[2:]
        expected = (("the Overworld", "Mining Dimension", "allthemodium:mining"),
                    ("the Nether", "The Other", "allthemodium:the_other"),
                    ("the End", "The Beyond", "allthemodium:the_beyond"))
        self.assertEqual(len(rows), 3)
        for cells, (placed_in, leads_to, dimension_id) in zip(rows, expected):
            self.assertEqual(cells[0], placed_in)
            self.assertEqual(cells[2], leads_to)
            self.assertIn(f"`{dimension_id}`", cells[3])
        self.assertIn("The pad's recipe is JEI's.", flatten(pad[0]))

    def test_visit_order_has_eight_marked_steps_in_order(self) -> None:
        body = section(self.text, "The recommended visit order")
        steps = re.split(r"^\d+\. ", body, flags=re.MULTILINE)[1:]
        self.assertEqual(len(steps), 8)
        for number, step in enumerate(steps, 1):
            self.assertTrue("**verified**" in step or "*approximate*" in step,
                            f"step {number} must say what is verified or approximate")
        ordered = ("the Nether", "Twilight Forest", "The End", "Bumblezone", "Otherside",
                   "Eternal Starlight", "Mining Dimension", "The Other", "The Beyond",
                   "Neo Vitae")
        listed = "".join(steps)
        positions = []
        for name in ordered:
            pattern = r"\bThe Other\b(?!side)" if name == "The Other" else re.escape(name)
            match = re.search(pattern, listed)
            self.assertIsNotNone(match, f"the visit order must mention {name}")
            positions.append(match.start())
        self.assertEqual(positions, sorted(positions), "visit order is out of sequence")
        self.assertIn("I only want the star", body)


# --------------------------------------------------------------------------------------
# key content
# --------------------------------------------------------------------------------------

class TestKeyContent(GuideTestCase):

    def test_every_config_dimension_id_is_covered(self) -> None:
        for dimension_id in CONFIG_DIMENSION_IDS:
            self.assertIn(f"`{dimension_id}`", self.text, f"missing {dimension_id}")

    def test_twilight_forest_is_tracked_by_its_advancement_not_an_invented_id(self) -> None:
        self.assertIn("`twilightforest:root`", self.text)
        self.assertIn("no `dimension` task", self.flat)
        twilight_ids = {token for token in ID_TOKEN.findall(self.text)
                        if token.startswith("twilightforest:")}
        self.assertEqual(twilight_ids, {"twilightforest:root", "twilightforest:snow_queen_trophy"})

    def test_chapter_ids_and_quest_counts(self) -> None:
        for chapter_id, (_title, count) in CHAPTER_QUEST_COUNTS.items():
            self.assertIn(f"(`{chapter_id}`, {count} quests", self.text,
                          f"{chapter_id} must be cited with its pack-8.2 quest count")

    def test_chapter_titles_agree_with_the_example_file(self) -> None:
        example = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        titles = {chapter["id"]: chapter["title"] for chapter in example["chapters"]}
        for chapter_id, (title, _count) in CHAPTER_QUEST_COUNTS.items():
            self.assertEqual(titles.get(chapter_id), title)
            self.assertIn(title, self.text)

    def test_mod_versions_from_the_modlist(self) -> None:
        for mod in MOD_VERSIONS:
            self.assertIn(mod, self.flat, f"missing verified mod version: {mod}")

    def test_key_quest_text_is_quoted_verbatim(self) -> None:
        for quote in KEY_QUOTES:
            self.assertIn(quote, self.flat, f"missing quest-text quote: {quote!r}")

    def test_star_component_links(self) -> None:
        rows = table_rows(section(self.text, "Where the dimensions meet the ATM Star"))[2:]
        self.assertGreaterEqual(len(rows), 6)
        joined = [" | ".join(cells) for cells in rows]
        for task, feeds in STAR_LINKS:
            self.assertTrue(any(f"*{task}*" in row and feeds in row for row in joined),
                            f"{task} -> {feeds} must share a row of the star table")
        for sibling in ("atm-star-checklist.md", "creative-checklist.md"):
            self.assertIn(sibling, section(self.text, "Where the dimensions meet the ATM Star"))

    def test_the_hedged_points_stay_hedged(self) -> None:
        self.assertIn("*approximate*: how far to push before moving on", self.flat)
        self.assertIn("the quest text and the dependency links disagree", self.flat)
        self.assertIn("JEI may show other sources", self.flat)
        self.assertIn("do not guess the frame", self.flat)
        self.assertGreaterEqual(self.text.count("**verified**"), 10)
        self.assertGreaterEqual(self.text.count("*approximate*"), 8)


# --------------------------------------------------------------------------------------
# grounding guards
# --------------------------------------------------------------------------------------

class TestGroundingGuards(GuideTestCase):

    def test_every_namespaced_id_is_config_verified(self) -> None:
        found = {token for token in ID_TOKEN.findall(self.text)
                 if not token.startswith(("https:", "http:"))}
        unverified = sorted(found - VERIFIED_IDS)
        self.assertEqual(unverified, [], "ids not verified against the pack config: "
                         f"{unverified} -- verify them and add them to VERIFIED_IDS")

    def test_no_coordinates(self) -> None:
        for pattern in COORDINATE_PATTERNS:
            match = pattern.search(self.text)
            self.assertIsNone(match, f"coordinate-like text: {match and match.group(0)!r}")

    def test_no_portal_recipe_is_reproduced(self) -> None:
        for phrase in NOT_REPRODUCED:
            self.assertNotIn(phrase.lower(), self.flat_lower,
                             f"recipe/frame text must stay in the quest entry and JEI: {phrase}")
        self.assertIn("the Catalyst's recipe is JEI's", self.flat)

    def test_in_page_anchors_resolve(self) -> None:
        slugs = {github_slug(heading)
                 for heading in re.findall(r"^#{1,6} (.+)$", self.text, flags=re.MULTILINE)}
        anchors = re.findall(r"\]\(#([^)]+)\)", self.text)
        self.assertTrue(anchors, "the at-a-glance intro links the visit-order section")
        for anchor in anchors:
            self.assertIn(anchor, slugs, f"broken in-page anchor: #{anchor}")

    def test_sibling_docs_are_linked_and_exist(self) -> None:
        related = section(self.text, "Related pages")
        for sibling in SIBLING_DOCS:
            self.assertIn(f"references/{sibling}", related, f"must point at {sibling}")
            self.assertTrue((REFERENCES / sibling).is_file(), f"{sibling} is missing")


# --------------------------------------------------------------------------------------
# the rest of the skill points at the page
# --------------------------------------------------------------------------------------

class TestCrossReferences(unittest.TestCase):

    def test_skill_md_routes_dimension_questions_to_the_page(self) -> None:
        skill = flatten(read(SKILL_MD))
        self.assertIn("Dimension questions go to `references/dimension-guide.md`.", skill)
        self.assertIn("which dimension to open next", skill)
        self.assertIn("the dimension guide, `references/dimension-guide.md`", skill)
        checklist = flatten(section(read(SKILL_MD), "Completion Checklist"))
        self.assertIn("references/dimension-guide.md", checklist)

    def test_reference_docs_point_at_the_page(self) -> None:
        for path in (PROGRESSION_MD, KEY_MODS_MD, BOSS_CHECKLIST_MD):
            self.assertIn("references/dimension-guide.md", read(path),
                          f"{path.name} must point at the dimension guide")
        guidance = flatten(section(read(PROGRESSION_MD), "Using this document in a session"))
        self.assertIn("dimension-guide.md", guidance)


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestOffline(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_module(self) -> None:
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        imported: "set[str]" = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(imported <= {"__future__", "ast", "json", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(imported)}")


if __name__ == "__main__":
    unittest.main()
