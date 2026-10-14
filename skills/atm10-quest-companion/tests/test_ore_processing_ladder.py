#!/usr/bin/env python3
"""Offline tests for references/ore-processing-ladder.md and its SKILL.md wiring.

Stdlib-only and network-free: every case mirrors pack data that was *read* from the
official AllTheMods/ATM-10 repository at commit ``e5e3d1d83e`` (pack 8.2, 2026-09-22) --
``config/ftbquests/quests/chapters/*.snbt`` for tasks and dependencies and
``config/ftbquests/quests/lang/en_us/`` for the titles, subtitles, and description text
quoted below. The pack clone is not shipped and is never fetched here; the constants in
this file are the verified snapshot the doc under test must reproduce.

Covered:

  * the doc exists, is no stub, and carries the skill's grounding rules (in-game quest
    book / JEI authoritative, approximate flagged, sources named, "never invented");
  * every verified quest id, title, and subtitle of the ore-processing ladder appears --
    Chapter 1's Ore Hammer quest, Mekanism's four tier quests and their machine quests,
    Occultism's crusher line, the three untitled Industrial Foregoing steps, Oritech,
    Create, Immersive Engineering, RailCraft, and Modern Industrialization;
  * every quoted sentence appears verbatim (whitespace-normalized; the pack's ``&`` /
    ``&#RRGGBB`` formatting codes stripped, which is how the doc renders them);
  * no invented item ids: every ``namespace:name`` token in the doc is one the config
    actually writes, and no plausible-but-unverified machine name (SAG Mill, Thermal
    Centrifuge, Ore Washer, ...) appears anywhere;
  * the untitled quests are marked as untitled, never given a derived name;
  * the community "doubling/tripling/quadrupling" naming is flagged as shorthand, with
    the config's own labels (Tier 1-4, 2x-5x) presented as the verified ones;
  * SKILL.md points at the new doc and its version was bumped;
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
LADDER_MD = SKILL_ROOT / "references" / "ore-processing-ladder.md"

# The commit the doc must date itself against; pack 8.2 per the repo's CHANGELOG.md and
# config/bcc-common.toml, matching examples/progress.example.json's "8.x" stamp.
COMMIT = "e5e3d1d83e"

# Pack-repository files the doc must name as its source.
SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
)

# The chapters the ladder touches: config filename -> (book title, group, order_index,
# quest count). Filenames are how the skill itself tracks chapters.
CHAPTER_FACTS = {
    "mainquestline_part_1": ("Chapter 1: The Beginning", "Main Questline", 0, 36),
    "mekanism": ("Mekanism", "Tech", 5, 90),
    "industrial_foregoing": ("Industrial Foregoing", "Tech", 3, 78),
    "oritech": ("Oritech", "Tech", 7, 56),
    "create": ("Create", "Tech", 0, 89),
    "immersive_engineering": ("Immersive Engineering", "Tech", 2, 127),
    "railcraft": ("RailCraft", "Tech", 10, 52),
    "occultism": ("Occultism", "Magic", 7, 64),
    "mi_steam": ("Steam Age: New Beginnings", "Modern Industrialization", 0, 30),
}

# Verified quests of the ore-processing ladder: (quest id, chapter file, plain-text title
# or None, subtitle or None). Titles/subtitles are the lang file's with ``&`` codes
# stripped; ``None`` means the config gives no title, and the book then shows the task
# item's name.
ORE_QUESTS = (
    ("4E5238F00CEED8B2", "mainquestline_part_1.snbt", "Basic Ore Doubling", None),
    ("051E0C85E7B71CE0", "mainquestline_part_1.snbt", "The Metal Age", None),
    ("119BED334E331C25", "mekanism.snbt", "Enrich then Smelt", "Tier 1 Ore Processing"),
    ("445CC9AAA6F8AAB6", "mekanism.snbt", "Making Oxygen for Purifier",
     "Tier 2 Ore Processing"),
    ("67E7A9A65B14C933", "mekanism.snbt", "Crush and Enrich our Clumps",
     "Tier 2 Ore Processing"),
    ("7485BCBE366501DF", "mekanism.snbt", "Making Chlorine", "Tier 3 Ore Processing"),
    ("0E175356D43E6A10", "mekanism.snbt", "Injecting Hydrogen Chloride",
     "Tier 3 Ore Processing"),
    ("0095422BC87AA135", "mekanism.snbt", "Shard, to Clump, to Dust, to Ingot",
     "Tier 3 Ore Processing"),
    ("75E4751F7A802A44", "mekanism.snbt", "Creating Sulfuric Acid", "Tier 4 Ore Processing"),
    ("77FB313845779AED", "mekanism.snbt", "Melting Ores with Acid and Crystallizing them",
     "Tier 4 Ore Processing"),
    ("6DC1E08D019FD543", "mekanism.snbt", "Making more Hydrogen Chloride",
     "Tier 4 Ore Processing"),
    ("7934873E784C4B3C", "mekanism.snbt", "Crystal, Shard, Clump, ETC",
     "Tier 4 Ore Processing"),
    ("08DDE018A804BFE7", "mekanism.snbt", "Enrichment Chamber", "Breaks Raw Ores into Dusts"),
    ("488DBE69595F38F8", "mekanism.snbt", "Energized Smelter", "Mekanism's Powered Furnace"),
    ("7AE502EDB73BD57A", "mekanism.snbt", "Crusher", "It Crushes Things."),
    ("33415CB421F7620A", "mekanism.snbt", "Purification Chamber", None),
    ("27512B0434531195", "mekanism.snbt", "Chemical Injection Chamber", None),
    ("6B8040401B512E50", "mekanism.snbt", "Chemical Dissolution Chamber", None),
    ("60B52705049D1BA5", "mekanism.snbt", "Chemical Washer", None),
    ("602A6CF9D5B66AD3", "mekanism.snbt", "Chemical Crystallizer", None),
    ("2A793B35FE25003C", "mekanism.snbt", "Chemical Oxidizer", None),
    ("18783C62009934DB", "mekanism.snbt", "Electrolytic Separator", None),
    ("376532CD98D39781", "mekanism.snbt", "Chemical Infuser", None),
    ("603BEDD49070ECAD", "mekanism.snbt", "Rotary Condensentrator", None),
    ("120572510F525930", "mekanism.snbt", "Thermal Evaporation Plant", None),
    ("21D8B88155648EA6", "mekanism.snbt", "Machines", None),
    ("6263A27182B2CE3D", "mekanism.snbt", "Better Machines", None),
    ("71CF9E59F8F0B4A6", "mekanism.snbt", "Even better Machines!", None),
    ("1ABD22AA58E093A6", "mekanism.snbt", "Some of the best Machines!", None),
    ("0F326EEEC2EBE4E5", "mekanism.snbt", "Enriched Items", "Enrich your items first!"),
    ("47F38E606AD3FF53", "mekanism.snbt", "Crushed to Dust!", None),
    ("0B35172E47705205", "industrial_foregoing.snbt", None, "Ore Processing: Step 1"),
    ("1684D52FDAAC894B", "industrial_foregoing.snbt", None, "Ore Processing: Step 2"),
    ("34AA079FFAFC64BD", "industrial_foregoing.snbt", None, "Ore Processing: Step 3"),
    ("4F35D04721DFC9FF", "occultism.snbt", "Our First Ritual", "Aviar's Circle"),
    ("5FE507DAEE770507", "occultism.snbt", "Ophyx' Calling", "An alternate path for light blue"),
    ("2AD68066C1948C90", "occultism.snbt", "Fatma's Incentivized Attraction", "Maximum Summon"),
    ("33106E24A3B5DDD8", "occultism.snbt", "Iesnium: Ore of the Otherworld", None),
    ("3DD27DED791C6A0B", "oritech.snbt", "Ore Processing", "Maximum output"),
    ("4EAD06B0B3AD7D6E", "oritech.snbt", "Clumps", "Fragment raw ores"),
    ("3F02EF19112D23BE", "create.snbt", "Crushing Wheels", None),
    ("32384DE59539557D", "immersive_engineering.snbt", "Crusher", None),
    ("21693C4DE6531D73", "railcraft.snbt", "Crusher", None),
    ("0DAF5D42694EA8C9", "mi_steam.snbt", "Forge Hammer", None),
    ("62622137648A4F56", "artifacts.snbt", "Pickaxe Heater", "Hands"),
    ("144BB025516E0994", "allthemodium.snbt", "Vibranium Ingot", None),
)

# Quest ids whose lang entry carries no title at all; the doc must mark each one as
# untitled (the book shows the task item's own name instead).
UNTITLED_QUEST_IDS = (
    "0B35172E47705205",
    "1684D52FDAAC894B",
    "34AA079FFAFC64BD",
    "175509632CBF8631",
    "310FA9380CB3E0BB",
    "164EA8EE10CA1583",
)

# Sentences the doc quotes from the config, with ``&``/``&#RRGGBB`` codes stripped and
# whitespace collapsed -- the exact shape in which the doc presents them. Each one was
# read from the chapter's lang file at the pinned commit.
QUOTED_SENTENCES = (
    # Chapter 1, the beginner answer.
    "Smelting down raw ores in the beginning is necessary, but you are missing out on extra resources!",
    "These will break down 1 raw ore into 2 ore dust, which can be smelted into ingots, effectively doubling your ingot output!",
    "Want more per raw ore? Check out the mod Occultism!",
    "Copper is abundant and has plenty of uses for things like Ore Hammers or Drawer Upgrades, so make sure to grab plenty of it!",
    # Mekanism tiers.
    "The very first and simplest Ore Processing is just 2 Machines! Enrichers and Smelters!",
    "We can use Ore Blocks to get twice the Dust or Raw Ore to get 1/3 more. So 3 Raw Ore to get 4 Dust.",
    "We can get 2 Dust from 1 Ore.",
    "Now that the Purifier has Oxygen, we can place our Ores into it to get 3 Ore Clumps from Ore Blocks or 2 Ore Clumps from Raw Ore.",
    "To start, Crush each Clump to get 2 Dirty Ore Dust.",
    "Pipe that Hydrogen Chloride into a Chemical Injection Chamber to Inject Ores to get Shards.",
    "Ore Blocks will get 4 Ore Shards while 3 Raw Ores will get 8 Ore Shards.",
    "3 Raw Ore will give 2 Buckets of Ore Slurry and 1 Ore Block will give 1 Bucket of Ore Slurry.",
    "Every 5mb of Dirty Slurry will be turned into 3mb of Ore Slurry.",
    "Each 200mb of Ore Slurry is equal to 1 Crystal.",
    "With our Chemical Injector, we can Inject the Crystals with Hydrogen Chloride to get 2 Ore Shards from each Ore Crystal.",
    "The Chemical Washer is only for Ore Processing.",
    "And most important, using Hydrogen Chloride into Ore Blocks to get Ore Shards for Processing!",
    # Occultism's crusher demons.
    "For our first ritual, we want to summon a Foliot Crusher Demon. This Demon will crush items for us, which is something we'll need to make some of the higher level Chalks!",
    "Djinnis are able to crush ores more efficiently than Foliots, but not as efficiently as Afrits or Marids.",
    "what if I told you that you could summon a demon that gives you 6 dusts per raw ore it crushes?",
    "Since you can't break this ore down into double the dusts using the standard methods, try using your Foliot Crusher to double your ingots per raw ore!",
    # Industrial Foregoing's numbered modes.
    "Yes, Industrial Foregoing has ore processing too. This one uses Liquid Meat to convert an ore into Raw Ore Meat.",
    "2x ore processing rate, 5 seconds to process.",
    "3x ore processing rate, 45 seconds to process.",
    "4x ore processing rate, 120 seconds to process.",
    "5x ore processing rate, 300 seconds to process.",
    # The other routes.
    "To process ores using Oritech, you need to use a Centrifuge with a Fluid Addon and a Pulveriser or Fragment Forge.",
    "Improves yield on all pulverisation recipes.",
    "This can be very helpful especially with taking Raw Ores into Dust.",
    "It can crush blocks to get the crafting materials, like bricks from a brick staircase, or dusts from ingots.",
    "Forge Hammer is the beginning of your journey. It has a lot of uses like getting a better output out of your ores to making components for future crafts.",
    "The Forge Hammer will allow you to easily crush Copper Ingots or Ore forms into its Dusts.",
    "It is also recommend to Ore Process it to get more.",
    "Might want to be careful with it if you want Ore Processing.",
    "In this modpack, quests are optional. Mods are not gated behind completing any quests!",
)

# The pack's own ladder labels -- the four Mekanism subtitles plus the two places the
# config prints doubling/2x language for ore processing.
CONFIG_LADDER_LABELS = (
    "Tier 1 Ore Processing",
    "Tier 2 Ore Processing",
    "Tier 3 Ore Processing",
    "Tier 4 Ore Processing",
    "Basic Ore Doubling",
    "effectively doubling your ingot output",
)

# Plausible-sounding ore machines the pack's en_us quest text never mentions (checked
# against every en_us lang file at the pinned commit). The doc must not smuggle any of
# them in from memory: if it is not in the config, the answer is the quest book and JEI.
UNVERIFIED_NAMES = (
    "SAG Mill",
    "Thermal Centrifuge",
    "Ore Washer",
    "Elite Purification Chamber",
    "Purification Factory",
    "Ore Doubling Machine",
    "Tier 5 Ore Processing",
    "Enrichment Factory",
)

# Every item id the doc is allowed to write, each one read from the config's quest tasks
# or from the smart filters' item tags. A "namespace:name" token outside this set fails
# the suite.
VERIFIED_ITEM_IDS = frozenset((
    # Chapter 1 task tag.
    "alltheores:ore_hammers",
    # Mekanism tier and machine tasks.
    "mekanism:enrichment_chamber",
    "mekanism:basic_enriching_factory",
    "mekanism:energized_smelter",
    "mekanism:purification_chamber",
    "mekanism:crusher",
    "mekanism:electric_pump",
    "mekanism:electrolytic_separator",
    "mekanism:chemical_infuser",
    "mekanism:chemical_injection_chamber",
    "mekanism:chemical_dissolution_chamber",
    "mekanism:chemical_washer",
    "mekanism:chemical_crystallizer",
    "mekanism:chemical_oxidizer",
    "mekanism:rotary_condensentrator",
    "mekanism:thermal_evaporation_block",
    "mekanism:thermal_evaporation_controller",
    "mekanism:thermal_evaporation_valve",
    "mekanism:steel_casing",
    "mekanism:advanced_control_circuit",
    "mekanism:elite_control_circuit",
    "mekanism:ultimate_control_circuit",
    "alltheores:sulfur",
    # Smart-filter item tags the config's tasks use.
    "mekanism:enriched",
    "ftbfiltersystem:item_tag",
    "c:dusts",
    # Other mods' ore quests.
    "industrialforegoing:washing_factory",
    "industrialforegoing:fermentation_station",
    "industrialforegoing:fluid_sieving_machine",
    "oritech:fragment_forge_block",
    "oritech:machine_fluid_addon",
    "create:crushing_wheel",
    "railcraft:crusher",
    "modern_industrialization:bronze_macerator",
    "alltheores:copper_dust",
))

# "namespace:name" as the doc writes config ids; the name must start with a letter so
# URLs and prose are not mistaken for an id.
ITEM_ID_RE = re.compile(r"(?<![\w:/])([a-z][a-z0-9_]{0,30}):([a-z][a-z0-9_/]{1,60})")

# The pack's formatting codes: &#RRGGBB colours first, then single-character codes.
HEX_CODE_RE = re.compile(r"&#[0-9A-Fa-f]{6}")
FORMAT_CODE_RE = re.compile(r"&[0-9a-fk-orA-FK-OR]")


def strip_codes(text: str) -> str:
    """Strip the pack's formatting codes; the doc quotes text this way."""
    return FORMAT_CODE_RE.sub("", HEX_CODE_RE.sub("", text))


def flatten(text: str) -> str:
    """Flatten markdown so line wrapping and blockquote markers cannot hide a quote.

    Every run of whitespace collapses to one space and a line-leading ``>`` (a markdown
    blockquote continuation) is dropped, so a quoted sentence wrapped across lines still
    reads as the config's own text.
    """
    unquoted = re.sub(r"(?m)^[ \t]*>[ \t]?", " ", text)
    return re.sub(r"\s+", " ", unquoted)


class DocTestCase(unittest.TestCase):
    """Assertion helpers that keep a failure short even for a ~30 kB document."""

    def assert_contains(self, haystack: str, needle: str, message: str) -> None:
        if needle not in haystack:
            self.fail(f"{message} — missing: {needle!r}")

    def assert_absent(self, haystack: str, needle: str, message: str) -> None:
        if needle in haystack:
            self.fail(f"{message} — found: {needle!r}")


class TestOreProcessingLadderDoc(DocTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LADDER_MD.read_text(encoding="utf-8") if LADDER_MD.is_file() else ""
        cls.flat = flatten(cls.text)
        cls.lowered = cls.flat.lower()

    # -- existence and grounding rules -------------------------------------------------

    def test_doc_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(LADDER_MD.is_file(), f"missing {LADDER_MD}")
        self.assertGreater(len(self.text.strip()), 8000,
                           "ore-processing-ladder.md looks like a stub")

    def test_doc_carries_the_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assert_contains(self.lowered, needle, f"the doc must state the {needle!r} rule")
        self.assertTrue(re.search(r"never invented|not invented|never invent", self.lowered),
                        "the doc must say its details were read, not invented")
        self.assert_contains(self.lowered, "no recipes", "the doc must refuse to give recipes")

    def test_doc_names_its_sources_and_dates_itself(self) -> None:
        for source in SOURCE_FILES:
            self.assert_contains(self.lowered, source.lower(),
                                 f"the doc must name its source {source!r}")
        self.assert_contains(self.text, COMMIT, "the doc must pin the commit it was read from")
        self.assert_contains(self.text, "8.2", "the doc must date itself against pack 8.2")
        self.assert_contains(self.text, "8.x",
                             "the doc must tie that version to the skill's 8.x stamp")
        self.assert_contains(self.text, "CHANGELOG.md", "the doc must name the changelog")
        for chapter_file in sorted({chapter for _, chapter, _, _ in ORE_QUESTS}):
            self.assert_contains(self.text, chapter_file,
                                 f"the doc must name the chapter file {chapter_file!r}")

    def test_doc_chapter_table_matches_the_config(self) -> None:
        for chapter_file, (title, group, order, count) in CHAPTER_FACTS.items():
            row = f"| `{chapter_file}` | {title} | {group} | {order} | {count} |"
            self.assert_contains(self.text, row, f"missing chapter-table row for {chapter_file}")

    # -- verified quest ids, titles, and subtitles -------------------------------------

    def test_every_verified_quest_id_is_quoted(self) -> None:
        for quest_id, _, title, subtitle in ORE_QUESTS:
            self.assert_contains(self.text, quest_id,
                                 f"the doc must cite quest id {quest_id} "
                                 f"({title or subtitle})")

    def test_every_verified_title_and_subtitle_is_quoted(self) -> None:
        for quest_id, _, title, subtitle in ORE_QUESTS:
            if title is not None:
                self.assert_contains(self.flat, strip_codes(title).strip(),
                                     f"the doc must carry the verified title {title!r} "
                                     f"({quest_id})")
            if subtitle is not None:
                self.assert_contains(self.flat, strip_codes(subtitle).strip(),
                                     f"the doc must carry the verified subtitle "
                                     f"{subtitle!r} ({quest_id})")

    def test_untitled_quests_are_marked_not_named(self) -> None:
        for quest_id in UNTITLED_QUEST_IDS:
            line = next((line for line in self.text.splitlines() if quest_id in line), "")
            self.assertTrue(line, f"the doc must mention untitled quest {quest_id}")
            self.assert_contains(line, "(no title in the config)",
                                 f"{quest_id} carries no title in the config")
        self.assertGreaterEqual(self.text.count("(no title in the config)"),
                                len(UNTITLED_QUEST_IDS),
                                "every untitled quest must be marked in place")

    # -- quotes are real, and nothing invented -----------------------------------------

    def test_quoted_sentences_are_verbatim_from_the_config(self) -> None:
        for quote in QUOTED_SENTENCES:
            self.assert_contains(self.flat, flatten(strip_codes(quote)),
                                 "the doc must quote the config's own sentence")

    def test_no_invented_item_ids(self) -> None:
        found = {"%s:%s" % (namespace, name) for namespace, name in ITEM_ID_RE.findall(self.text)}
        unexpected = sorted(found - VERIFIED_ITEM_IDS)
        self.assertEqual(unexpected, [],
                         f"the doc cites item id(s) the config does not: {unexpected}")

    def test_no_unverified_machine_names(self) -> None:
        for name in UNVERIFIED_NAMES:
            self.assert_absent(self.text, name,
                               f"the doc names an unverified machine {name!r}")

    # -- the ladder's labels and hedges ------------------------------------------------

    def test_the_configs_own_ladder_labels_are_present(self) -> None:
        for label in CONFIG_LADDER_LABELS:
            self.assert_contains(self.flat, label,
                                 f"the doc must carry the config's label {label!r}")

    def test_community_multiplier_names_are_flagged_as_shorthand(self) -> None:
        for word in ("doubling", "tripling", "quadrupling"):
            self.assert_contains(self.lowered, word,
                                 f"the doc must address the community term {word!r}")
        self.assert_contains(self.lowered, "community shorthand",
                             "the community tier names must be marked as shorthand")
        self.assert_contains(self.lowered, 'never says "tripling"',
                             "the doc must say which of those words the config never uses")
        self.assert_contains(self.lowered, "verify",
                             "the hedge must send the player to the book / JEI")

    def test_doc_refuses_to_compute_per_ore_totals(self) -> None:
        self.assert_contains(self.lowered, "per-step",
                             "the doc must say the config's numbers are per-step")
        self.assert_contains(self.lowered, "does not tell you",
                             "the doc must keep a 'does not tell you' section")

    def test_doc_cross_references_its_siblings(self) -> None:
        for sibling in ("progression.md", "key-mods.md", "getting-started.md",
                        "creative-checklist.md", "atm-star-checklist.md"):
            self.assert_contains(self.text, sibling, f"the doc must point at {sibling}")


class TestSkillWiring(DocTestCase):
    """SKILL.md must advertise the new doc and carry a bumped version."""

    def setUp(self) -> None:
        self.skill = SKILL_MD.read_text(encoding="utf-8")

    def test_skill_md_points_at_the_ladder_doc(self) -> None:
        self.assert_contains(self.skill, "references/ore-processing-ladder.md",
                             "SKILL.md must wire the new reference doc")

    def test_version_was_bumped(self) -> None:
        match = re.search(r"^version:\s*(\d+\.\d+\.\d+)\s*$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md must keep an X.Y.Z version")
        assert match is not None
        self.assertGreaterEqual(tuple(int(part) for part in match.group(1).split(".")),
                                (1, 2, 0),
                                "adding the ore-processing doc must bump the skill version")

    def test_skill_md_still_documents_the_grounding_rule(self) -> None:
        lowered = self.skill.lower()
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "never invent"):
            self.assert_contains(lowered, needle, f"SKILL.md must keep the {needle!r} rule")


class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_module(self) -> None:
        imported: "set[str]" = set()
        for line in Path(__file__).read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                imported.update(part.strip().split()[0].split(".")[0]
                                for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                imported.add(stripped.split()[1].split(".")[0])
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set(),
                         "the suite must stay offline: no network, no subprocesses")


if __name__ == "__main__":
    unittest.main()
