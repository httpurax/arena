#!/usr/bin/env python3
"""Offline tests for the flight guide (``references/flight-guide.md``).

Stdlib-only and network-free: every check reads files shipped with the skill. The
verified data below was read from the official ``AllTheMods/ATM-10`` repository at the
same pinned commit as the endgame docs (``e5e3d1d83e``, pack 8.2) -- the quest chapters,
their English lang files, the pack's Iron Jetpacks tier files, and the modlist -- and
these tests hold the page to it.

Covered:

  * grounding: the page exists, is not a stub, names its source files (including
    ``config/ironjetpacks/jetpacks``), pins the commit and pack version, and carries the
    skill's rules (in-game quest book + JEI authoritative, approximate flagged, nothing
    invented, quests optional);
  * the answer itself: the cheapest reliable path (Tips and Tricks' dependency-free
    *Iron Jetpacks* and *Charging Gadgets*) leads the page, and the at-a-glance ladder
    keeps its verified order from the Wood jetpack to the Creative Jetpack;
  * verified data: every quest title, task item, dependency chain, upstream count, and
    quoted sentence the page relies on, and the pack config's jetpack tiers;
  * no invented names: every namespaced id on the page is on the verified list, every
    bold title in a table and every member of a dependency chain is a verified quest
    title, and each untitled quest stays marked *(no title in the config)*;
  * absences: no Angel Ring, flight totem, or vanilla-Elytra quest is presented as part
    of the 8.2 book, and the Ritual of Flight's undescribed effect is not filled in;
  * hedges: timing is labelled *(judgement)*, recipes and numbers go to JEI;
  * wiring: SKILL.md is bumped to 1.6.0 and routes flight questions to the page, and

    ``progression.md`` points at it;
  * offline guarantee: this suite imports no network or process module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
FLIGHT_MD = SKILL_ROOT / "references" / "flight-guide.md"
PROGRESSION_MD = SKILL_ROOT / "references" / "progression.md"

SKILL_VERSION = "1.6.0"

FLIGHT_COMMIT = "e5e3d1d83e"
FLIGHT_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"

SOURCE_FILES = (
    "AllTheMods/ATM-10",
    "config/ftbquests/quests/chapters",
    "lang/en_us/chapters",
    "config/crash_assistant/modlist.json",
    "config/ironjetpacks/jetpacks",
    "config/bcc-common.toml",
    "CHANGELOG.md",
)

# Every quest title the page cites, exactly as the en_us lang files give it at the pinned
# commit (formatting codes stripped; the config's escaped "\&" rendered as "&", as the
# sibling docs do). A bold title in a table or a member of a dependency chain that is not
# in this list is a derived name, not a verified one.
FLIGHT_VERIFIED_TITLES = (
    # Tips and Tricks + Basic Power: the first flight and keeping it charged
    "Iron Jetpacks", "Charging Gadgets", "Mekanism: Energy Cubes", "Flux Networks",
    "Wireless Charging",
    # Mekanism: the hydrogen jetpack chain
    "Mekanism", "Osmium", "Metallurgic Infuser", "Infused Alloy", "Power!", "Chargepad",
    "Jetpack",
    # Mekanism: Reactors: the MekaSuit modules and the gate in front of the Bodyarmor
    "Modification Station", "Jetpack Unit", "Elytra Unit", "Gravitational Modulating Unit",
    "Gravitational Modulating Additional Unit", "MekaSuit Bodyarmor",
    "Super-Critical Phase Shifter",
    # Chapter 3 / Chapter 4
    "Nexium Emitter", "Creative Jetpack", "Fully Automated ATM Star",
    # PneumaticCraft
    "Pneumatic Armor",
    # Just Dire Things
    "Armor Upgrades", "Ferricore", "Eclipse Alloy",
    # Extended & Advanced AE / Basic Armor
    "Extended & Advanced AE", "Advanced AE", "Reaction Efficency: The Reaction Chamber",
    "Quantum Ingredients", "ME System As Armor: The Quantum Armor",
    "Upgrades for Quantum Armor", "Quantum Armor (AE2)",
    # Draconic Evolution
    "Draconic Evolution", "Modules!", "Wyvern Flight Module", "Draconic Flight Module",
    "Chaotic Flight Module", "Wyvern Tier", "Draconic Tier", "Chaotic Tier",
    "Wyvern Chestplate", "Draconic Chestplate", "Chaotic Chestplate",
    # Elytra and gliding
    "Ignitium Elytra Chestplate", "Ignitium Armor", "Mechanical Fusion Anvil",
    "Soul Elytra", "Ancient Hoops", "Allthemodium Armor", "Kinetic Belt",
    # Short hops and mounts
    "Valkyrie Armor", "Silver Key", "Enchanting Apparatus", "Cloud in a Bottle",
    "Rule the Skys with the Hippogryph", "Taming the Amphithere", "Commanding your Dragon",
    "Beehemoth",
    # Cross-referenced from Chapter 1
    "Kill The Warden",
)

# Quests the config leaves untitled: (task item, subtitle or None). The page must mark
# each one *(no title in the config)* where it cites it, never derive a name for it.
FLIGHT_UNTITLED_QUESTS = (
    ("xycraft_machines:stake", "Up!"),
    ("pneumaticcraft:jet_boots_upgrade_1", "Max: 1"),
    ("pneumaticcraft:elytra_upgrade", "Max: 1"),
    ("justdirethings:upgrade_flight", None),
    ("justdirethings:upgrade_elytra", None),
    ("advanced_ae:flight_card", "Creative Flight"),
    ("advanced_ae:flight_drift_card", "No Flight Drift"),
    ("ars_nouveau:glyph_glide", None),
    ("ars_nouveau:belt_of_levitation", None),
    ("ars_nouveau:ritual_flight", None),
    ("silentgear:elytra_blueprint", None),
    ("mekanism:pellet_antimatter", None),
    ("the_bumblezone:bumble_bee_chestplate_1", None),
    ("the_bumblezone:bumble_bee_chestplate_2", None),
)

# The flight items' task ids (and the jetpack tier components) the page must cite.
FLIGHT_TASK_ITEMS = (
    "ironjetpacks:jetpack", "ironjetpacks:jetpack_id", "ironjetpacks:wood",
    "ironjetpacks:creative", "charginggadgets:charging_station", "xycraft_machines:stake",
    "mekanism:jetpack", "mekanism:chargepad", "pneumaticcraft:jet_boots_upgrade_1",
    "pneumaticcraft:elytra_upgrade", "justdirethings:upgrade_flight",
    "justdirethings:upgrade_elytra", "justdirethings:eclipsealloy_chestplate",
    "advanced_ae:flight_card", "advanced_ae:flight_drift_card",
    "advanced_ae:quantum_upgrade_base", "draconicevolution:item_wyvern_flight",
    "draconicevolution:item_draconic_flight", "draconicevolution:item_chaotic_flight",
    "mekanism:module_gravitational_modulating_unit",
    "gmut:module_gravitational_modulating_additional_unit", "mekanism:module_jetpack_unit",
    "mekanism:module_elytra_unit", "mekanism:pellet_antimatter",
    "cataclysm:ignitium_elytra_chestplate", "deeperdarker:soul_elytra",
    "ars_nouveau:glyph_glide", "ars_nouveau:belt_of_levitation", "ars_nouveau:ritual_flight",
    "silentgear:elytra_blueprint", "the_bumblezone:bumble_bee_chestplate_1",
    "the_bumblezone:bumble_bee_chestplate_2",
)

# Every other namespaced id the page may show: rewards, quest-task structures and
# advancements, components, the Wood tier's crafting-material tag, and the ids it quotes
# while saying what is *not* a flight item. ``minecraft:elytra`` is here only because the
# page cites it as absent from the quest config (checked separately below).
FLIGHT_OTHER_IDS = (
    "tag:minecraft:planks", "mekanism:basic_energy_cube", "minecraft:potion",
    "apothic_attributes:levitation", "mekanism:basic_chemical_tank", "mekanism:hydrogen",
    "the_bumblezone:ancient_hoops", "iceandfire:iceandfire/tame_hippogryph",
    "advanced_ae:quantum_helmet", "advanced_ae:quantum_chestplate",
    "advanced_ae:quantum_leggings", "advanced_ae:quantum_boots", "ars_nouveau:ritual_brazier",
    "utilitarian:angel_block", "constructionstick:template_angel", "aether:angelic_stone",
    "artifacts:chorus_totem", "minecraft:totem_of_undying",
    "justdirethings:totem_of_death_recall", "undergarden:denizen_totem", "minecraft:elytra",
)
VERIFIED_IDS = frozenset(FLIGHT_TASK_ITEMS + FLIGHT_OTHER_IDS)

# The at-a-glance ladder: (the "roughly when" label, the task item the row must cite), in
# the order the page lists them -- earliest first.
LADDER = (
    ("Early game", "ironjetpacks:wood"),
    ("Early game", "xycraft_machines:stake"),
    ("Early tech", "mekanism:jetpack"),
    ("Mid tech", "pneumaticcraft:jet_boots_upgrade_1"),
    ("Mid, after the Warden", "justdirethings:upgrade_flight"),
    ("Mid to late tech", "advanced_ae:flight_card"),
    ("Late", "draconicevolution:item_draconic_flight"),
    ("Endgame, star tier", "mekanism:module_gravitational_modulating_unit"),
    ("After the star", "ironjetpacks:creative"),
)

# Dependency chains read from the config's ``dependencies`` lists, root first.
MEKANISM_JETPACK_CHAIN = ("Mekanism", "Osmium", "Metallurgic Infuser", "Infused Alloy",
                          "Power!", "Chargepad", "Jetpack")
QUANTUM_ARMOR_CHAIN = ("Extended & Advanced AE", "Advanced AE",
                       "Reaction Efficency: The Reaction Chamber", "Quantum Ingredients",
                       "ME System As Armor: The Quantum Armor", "Upgrades for Quantum Armor")
DRACONIC_FLIGHT_CHAIN = ("Modules!", "Wyvern Flight Module", "Draconic Flight Module",
                         "Chaotic Flight Module")

# Transitive-dependency counts computed from the config: the jet boots upgrade (24), the
# Quantum Armor flight card (6), the MekaSuit Bodyarmor (17).
UPSTREAM_COUNTS = ("24 quests upstream", "6 quests upstream", "17 quests upstream")

# The pack's Iron Jetpacks tiers (``config/ironjetpacks/jetpacks/*.json``): 17 files,
# none disabled; the creative one is tier -1.
JETPACK_TIERS = {
    0: {"wood"},
    1: {"stone", "copper"},
    2: {"iron", "bronze", "silver"},
    3: {"gold", "electrum", "invar", "steel"},
    4: {"diamond", "platinum"},
    5: {"emerald"},
    6: {"allthemodium"},
    7: {"vibranium"},
    8: {"unobtainium"},
    -1: {"creative"},
}

# Sentences quoted verbatim from the quest text (formatting codes stripped).
VERIFIED_QUOTES = (
    "In this modpack, quests are optional. Mods are not gated behind completing any quests!",
    "The Charging Station is a very helpful Early Game Block.",
    "Either Pipe in Energy or use Furnace Fuel to make Energy in the form of FE.",
    "To start making them you'll need to start with a Wood Jetpack! This can be upgraded "
    "all the way to a Creative Jetpack.",
    "All of them also need FE to work, you can use any Item Charger to charge them! They "
    "will use FE to fly and yes you will drop if you run out of Energy.",
    "To fly you'll need to turn on your Engine (V), then when you hold Space you'll fly up "
    "and drop when you let go.",
    "You can even charge your Jetpacks while you are flying with this mod.",
    "The Balloon on a Stick is an early and restrictive source of Creative Flight.",
    "Go too far and you'll get detached and fall.",
    "The Mekanism Jetpack works similar to Iron Jetpacks just with different Modes and it "
    "requires Hydrogen as Fuel instead of Energy!",
    "Allows you to fly like Iron Man.",
    "Allows you to use an Elytra while still having your Pneumatic Chestplate on.",
    "Grants the player creative flight.",
    "Shadowpulse Goo is the fourth and final tier of goo added by JDT and requires Ancient "
    "City and Warden materials to craft.",
    "acquired by performing Goo Spread on Netherite Blocks using tier four goo",
    "Okay now this ones give both Gliding and actual Flying, Creative Flight to be more "
    "exact.",
    "I don't like to call it flying, rather 'falling with style'.",
    "Literally just Creative Flight.",
    "You won't be able to use this Unit while you have the Gravitational Modulating Unit on.",
    "This Module, when put into the MekaSuit Chestplate, will give you Creative Flight. You "
    "only need some of the most expensive Items in the game to craft it!",
    "Well you'll neever need to worry about that again!",
    "You might need to make every Jetpack before it, an ATM Star, plus more expensive Items "
    "but hey it is worth it!",
    "Just combine an Ignitium Chestplate with an Elytra... that simple!",
    "When wearing all 5 parts of it you can hold Space to Fly! Only for a short time though.",
    "While wearing it you can hold Space Bar to fly for a little.",
    "This belt allows you to levitate.",
    "check out each of them using the Worn Notebook",
)

ABSENCE_HEADING = "## Not in the 8.2 book (searched, and absent)"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def flatten(text: str) -> str:
    """Collapse the page's line wrapping so a quote can be found across line breaks."""
    return re.sub(r"\s+", " ", text)


def blocks(text: str) -> "list[str]":
    """The page as table rows, list items, headings, and paragraphs, each on one line."""
    out: "list[str]" = []
    current: "list[str]" = []

    def flush() -> None:
        if current:
            out.append(" ".join(current))
            current.clear()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            flush()
        elif stripped.startswith("|"):
            flush()
            out.append(stripped)
        else:
            if stripped.startswith(("- ", "#")) or re.match(r"\d+\. ", stripped):
                flush()
            current.append(stripped)
    flush()
    return out


def italic_spans(block: str) -> "list[str]":
    """Single-star emphasis spans in one block, paired left to right.

    Inline code (which may hold a literal ``*``, as in ``chapters/*.snbt``) and bold runs
    are blanked first, so a closing star can never pair with the next opening one.
    """
    plain = re.sub(r"`[^`]*`", "`code`", block)
    plain = re.sub(r"\*\*.+?\*\*", "B", plain)
    return [match.group(1) for match in re.finditer(r"\*([^*]+)\*", plain)]


def section(text: str, heading: str) -> str:
    """Everything under ``heading`` up to the next heading of the same or higher level."""
    lines = text.splitlines()
    start = lines.index(heading)
    level = len(heading) - len(heading.lstrip("#"))
    body: "list[str]" = []
    for line in lines[start + 1:]:
        if line.startswith("#") and len(line) - len(line.lstrip("#")) <= level:
            break
        body.append(line)
    return "\n".join(body)


def table_rows(text: str, heading: str) -> "list[list[str]]":
    """The data rows (header and separator dropped) of the first table under ``heading``."""
    rows: "list[str]" = []
    for line in section(text, heading).splitlines():
        if line.startswith("|"):
            rows.append(line)
        elif rows:
            break
    return [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in rows[2:]]


class FlightGuideCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(FLIGHT_MD)
        cls.lower = cls.text.lower()
        cls.flat = flatten(cls.text)
        cls.flat_lower = cls.flat.lower()
        cls.blocks = blocks(cls.text)


# --------------------------------------------------------------------------------------
# grounding
# --------------------------------------------------------------------------------------

class TestFlightGuideGrounding(FlightGuideCase):

    def test_the_page_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(FLIGHT_MD.is_file(), f"missing {FLIGHT_MD}")
        self.assertGreater(len(self.text.strip()), 2000, "flight-guide.md looks like a stub")
        self.assertTrue(self.text.startswith("# Flight in ATM10"))
        self.assertIn("when can I fly?", self.text)

    def test_it_carries_the_skills_grounding_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate"):
            self.assertIn(needle, self.lower, f"flight-guide.md must state the {needle!r} rule")
        self.assertRegex(self.lower, r"never invented|not invented|never invent")
        self.assertIn("nothing here was invented", self.lower)
        self.assertIn("read, not remembered", self.lower)

    def test_it_names_every_source_file(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source, self.text, f"flight-guide.md must name its source: {source}")

    def test_it_dates_itself_to_the_pinned_commit_and_pack_version(self) -> None:
        self.assertIn(FLIGHT_COMMIT, self.text)
        self.assertIn(FLIGHT_COMMIT_FULL, self.text, "the commit link must use the full hash")
        self.assertIn("pack 8.2", self.text)
        self.assertIn("8.x", self.text, "the page must tie 8.2 to the skill's 8.x stamp")
        self.assertIn("2026-09-22", self.text)
        self.assertIn('modpackVersion = "8.2"', self.text)

    def test_it_says_quests_guide_rather_than_gate(self) -> None:
        self.assertIn("Quests guide, they do not gate.", self.text)
        self.assertIn(VERIFIED_QUOTES[0], self.flat)

    def test_it_says_how_absence_was_established(self) -> None:
        self.assertIn("How it was searched.", self.text)
        self.assertIn("All 66 chapter files", self.flat)
        self.assertIn("scripts/snbt.py", self.text)
        self.assertIn("searched for and not found", self.flat)


# --------------------------------------------------------------------------------------
# the answer: cheapest reliable path first, then the ladder in order
# --------------------------------------------------------------------------------------

class TestFlightGuideAnswer(FlightGuideCase):

    def test_the_short_answer_leads_with_the_cheapest_reliable_path(self) -> None:
        short = flatten(section(self.text, "## The short answer"))
        for needle in ("Tips and Tricks", "Iron Jetpacks", "Charging Gadgets",
                       "no dependencies", "Wood", "cheapest reliable path"):
            self.assertIn(needle, short, f"the short answer must mention {needle!r}")
        first_item = short.split("2. ")[0]
        self.assertIn("early game", first_item, "the first answer must say flight is early")
        self.assertIn("(judgement", first_item, "the recommendation must be marked judgement")
        self.assertLess(self.text.index("## The short answer"), self.text.index("## Provenance"),
                        "the beginner's answer comes before the provenance")

    def test_the_tips_and_tricks_pair_is_dependency_free_and_cited_exactly(self) -> None:
        rows = table_rows(self.text, "## 1. The cheapest reliable path: Tips and Tricks")
        self.assertEqual([row[0] for row in rows], ["**Charging Gadgets**", "**Iron Jetpacks**"])
        self.assertIn("`charginggadgets:charging_station`", rows[0][1])
        self.assertIn("Charging Gadgets 1.14.1", rows[0][2])
        self.assertIn("`ironjetpacks:jetpack_id` = `ironjetpacks:wood`", rows[1][1])
        self.assertIn("Iron Jetpacks 8.0.11", rows[1][2])
        tips = flatten(section(self.text, "## 1. The cheapest reliable path: Tips and Tricks"))
        self.assertIn("neither has a dependency", tips)
        self.assertIn("standalone chapter (no chapter group, 23 quests", tips)
        self.assertIn("`tag:minecraft:planks`", tips)
        self.assertIn('subtitle *"Complete all the tips!"*', tips)

    def test_the_ladder_keeps_its_verified_order(self) -> None:
        rows = table_rows(self.text, "## The ladder at a glance")
        self.assertEqual(len(rows), len(LADDER), "one ladder row per verified flight item")
        for row, (when, item) in zip(rows, LADDER):
            self.assertEqual(row[0], when)
            self.assertIn(f"`{item}`", row[2], f"the {when!r} row must cite {item}")
        self.assertIn("nothing — no dependencies", rows[0][4])
        self.assertIn("*Fully Automated ATM Star*", rows[-1][4])

    def test_the_mid_game_choice_is_presented_as_alternatives(self) -> None:
        mid = flatten(section(self.text, "## 6. Mid-game creative flight: Just Dire Things or "
                                         "Advanced AE"))
        self.assertIn("does not order these two against each other", mid)
        self.assertIn("pick the line you already run", mid)


# --------------------------------------------------------------------------------------
# verified data
# --------------------------------------------------------------------------------------

class TestFlightGuideVerifiedData(FlightGuideCase):

    def test_every_verified_title_is_cited(self) -> None:
        self.assertEqual(len(FLIGHT_VERIFIED_TITLES), len(set(FLIGHT_VERIFIED_TITLES)))
        for title in FLIGHT_VERIFIED_TITLES:
            self.assertIn(title, self.flat, f"flight-guide.md is missing a verified title: {title}")

    def test_every_flight_task_item_is_cited(self) -> None:
        for item in FLIGHT_TASK_ITEMS:
            self.assertIn(f"`{item}`", self.text, f"flight-guide.md must cite {item}")

    def test_the_dependency_chains_are_in_config_order(self) -> None:
        for chain in (MEKANISM_JETPACK_CHAIN, QUANTUM_ARMOR_CHAIN, DRACONIC_FLIGHT_CHAIN):
            self.assertIn(" → ".join(chain), self.flat, f"chain out of order: {chain[0]} ...")
        self.assertIn("six-quest chain", self.flat)
        for count in UPSTREAM_COUNTS:
            self.assertIn(count, self.flat)

    def test_the_jetpack_tiers_mirror_the_pack_config(self) -> None:
        rows = table_rows(self.text, "### The jetpack ladder (pack config)")
        found: "dict[int, set[str]]" = {}
        for cell_tier, cell_names in rows:
            tier = int(re.match(r"-?\d+", cell_tier).group(0))
            found[tier] = {name.strip() for name in cell_names.split(",")}
        self.assertEqual(found, JETPACK_TIERS)
        self.assertEqual(sum(len(names) for names in found.values()), 17)
        self.assertEqual([tier for tier in found if tier >= 0], list(range(9)),
                         "tiers 0-8 must be listed in ascending order")
        self.assertIn('`"creative": true`', rows[-1][0])
        ladder = flatten(section(self.text, "### The jetpack ladder (pack config)"))
        self.assertIn("defines 17 jetpacks", ladder)
        self.assertIn('`"disable": false` in every file', ladder)
        self.assertIn("a higher `tier` always has a larger `capacity` and a larger `usage`",
                      ladder)

    def test_quotes_are_verbatim(self) -> None:
        for quote in VERIFIED_QUOTES:
            self.assertIn(quote, self.flat, f"quote missing or altered: {quote[:60]}...")
        # The pack's own typo stays, and is flagged rather than corrected.
        self.assertIn("neever need to worry about that again!\"* (sic)", self.flat)

    def test_the_gates_behind_creative_flight_are_the_configs(self) -> None:
        self.assertIn("only the Eclipse Alloy chestplate takes it", self.flat)
        self.assertIn("Only the Eclipse Alloy chestplate's list", self.flat)
        self.assertIn("the Ferricore and Blazegold chestplates list neither", self.flat)
        self.assertIn("upgrade to the Unobtainium chestplate", self.flat)
        self.assertIn("as an input of **Nexium Emitter**", self.flat)
        self.assertIn("has one dependency, **Fully Automated ATM Star**", self.flat)
        self.assertIn("one of the four XyCraft quests with no dependencies", self.flat)

    def test_mod_versions_come_from_the_modlist(self) -> None:
        for mod in ("Iron Jetpacks 8.0.11", "Charging Gadgets 1.14.1", "XyCraft Machines 0.7.53",
                    "Mekanism 10.7.19", "Just Dire Things 1.5.7", "Advanced AE 1.6.12-1.21.1",
                    "Draconic Evolution 3.1.4.633",
                    "Gravitational Modulating Additional Unit 6.4", "489 mods"):
            self.assertIn(mod, self.flat)


# --------------------------------------------------------------------------------------
# no invented names
# --------------------------------------------------------------------------------------

class TestFlightGuideNoInventedNames(FlightGuideCase):

    def test_every_namespaced_id_is_a_verified_one(self) -> None:
        cited = set(re.findall(r"`([^`\s]+:[^`\s]+)`", self.text))
        self.assertEqual(cited - VERIFIED_IDS, set(),
                         "flight-guide.md cites ids that were not verified in the config")
        self.assertEqual(VERIFIED_IDS - cited, set(), "a verified id dropped off the page")

    def test_bold_titles_in_tables_are_verified_titles(self) -> None:
        verified = set(FLIGHT_VERIFIED_TITLES)
        for row in (block for block in self.blocks if block.startswith("|")):
            for title in re.findall(r"\*\*(.+?)\*\*", row):
                self.assertIn(title, verified, f"unverified title in a table row: {title!r}")

    def test_every_chain_member_is_a_verified_title(self) -> None:
        verified = set(FLIGHT_VERIFIED_TITLES)
        chains = [span for block in self.blocks for span in italic_spans(block) if "→" in span]
        self.assertEqual(len(chains), 5, "the page writes five dependency chains in italics")
        for chain in chains:
            for member in (part.strip() for part in chain.split("→")):
                if member:
                    self.assertIn(member, verified, f"unverified chain member: {member!r}")

    def test_untitled_quests_stay_untitled(self) -> None:
        marker = "(no title in the config)"
        for item, subtitle in FLIGHT_UNTITLED_QUESTS:
            hits = [block for block in self.blocks if f"`{item}`" in block]
            self.assertTrue(hits, f"{item} is not cited")
            marked = [block for block in hits if marker in block]
            self.assertTrue(marked, f"{item} must be marked {marker!r} where it is cited")
            if subtitle is not None:
                self.assertTrue(any(f'subtitle *"{subtitle}"*' in block for block in marked),
                                f"{item} must carry its config subtitle {subtitle!r}")
        self.assertIn("its own *(no title in the config)* quest", self.flat,
                      "the Chapter 3 copy of the module is untitled too")

    def test_untitled_quests_get_no_bold_name(self) -> None:
        for item, _ in FLIGHT_UNTITLED_QUESTS:
            for block in (b for b in self.blocks if b.startswith("|") and f"`{item}`" in b):
                first_cells = block.strip("|").split("|")[:2]
                self.assertNotIn("**", " ".join(first_cells),
                                 f"a table row gives the untitled {item} a bold name")


# --------------------------------------------------------------------------------------
# absences
# --------------------------------------------------------------------------------------

class TestFlightGuideAbsences(FlightGuideCase):

    def test_the_absent_section_lists_what_the_book_lacks(self) -> None:
        absent = flatten(section(self.text, ABSENCE_HEADING))
        for needle in ("**Angel Ring.**", "**Flight totems.**", "**A vanilla Elytra quest.**",
                       "**A fly command.**", "**What the Ritual of Flight does.**"):
            self.assertIn(needle, absent)
        self.assertIn("no angel-ring mod is in `modlist.json`", absent)
        self.assertIn("none of them a ring, none described as giving flight", absent)
        self.assertIn("`minecraft:elytra` appears nowhere in the quest config", absent)

    def test_the_vanilla_elytra_is_never_cited_as_a_task(self) -> None:
        for row in (block for block in self.blocks if block.startswith("|")):
            self.assertNotIn("minecraft:elytra`", row, "no table may cite a vanilla Elytra task")
        for block in (b for b in self.blocks if "`minecraft:elytra`" in b):
            self.assertIn("appears nowhere", block,
                          "minecraft:elytra may only be cited to say it is absent")

    def test_angel_rings_and_flight_totems_are_only_ever_absent(self) -> None:
        # Inside the absent section every bullet is itself the absence statement; anywhere
        # else, a mention must point at that section or say it was searched for.
        absent_blocks = set(blocks(section(self.text, ABSENCE_HEADING)))
        mentions = 0
        for block in self.blocks:
            lowered = block.lower()
            if block in absent_blocks or not ("angel ring" in lowered
                                              or "flight totem" in lowered):
                continue
            mentions += 1
            self.assertTrue(
                any(word in lowered for word in ("not in the 8.2 book", "absent",
                                                 "searched for")),
                f"an Angel Ring / flight totem is mentioned without saying it is absent: "
                f"{block[:90]}...")
        self.assertGreaterEqual(mentions, 1, "the short answer must say they are absent")
        cited = set(re.findall(r"`([^`\s]+:[^`\s]+)`", self.text))
        for token in cited:
            self.assertNotRegex(token, r"angel_?ring|flight_?totem")

    def test_the_ritual_of_flight_effect_is_not_filled_in(self) -> None:
        ritual = [b for b in self.blocks if "`ars_nouveau:ritual_flight`" in b]
        self.assertEqual(len(ritual), 1)
        self.assertIn("has no description", ritual[0])
        self.assertIn("Worn Notebook", ritual[0])
        self.assertNotIn("creative flight", ritual[0].lower(),
                         "the config never says what the ritual does")


# --------------------------------------------------------------------------------------
# hedges
# --------------------------------------------------------------------------------------

class TestFlightGuideHedges(FlightGuideCase):

    def test_timing_is_labelled_judgement(self) -> None:
        self.assertGreaterEqual(self.lower.count("(judgement"), 6)
        self.assertIn("Roughly when *(judgement)*", self.text)
        self.assertIn("not what it costs", self.flat)

    def test_recipes_and_numbers_go_to_jei(self) -> None:
        for needle in ("no recipes", "does not tell you", "jei's to show",
                       "not given here", "players rebind"):
            self.assertIn(needle, self.flat_lower, f"missing hedge: {needle}")
        self.assertIn("not a crafting guide", self.flat_lower)
        self.assertIn("tether's range is not in the config", self.flat_lower)

    def test_the_page_cross_references_its_siblings(self) -> None:
        for sibling in ("progression.md", "key-mods.md", "boss-checklist.md",
                        "atm-star-checklist.md", "creative-checklist.md"):
            self.assertIn(sibling, self.text, f"flight-guide.md must point at {sibling}")


# --------------------------------------------------------------------------------------
# wiring: SKILL.md and progression.md
# --------------------------------------------------------------------------------------

class TestFlightGuideWiring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read(SKILL_MD)
        cls.skill_flat = flatten(cls.skill)

    def test_skill_version_is_bumped(self) -> None:
        frontmatter = self.skill.split("---")[1]
        self.assertRegex(frontmatter, rf"(?m)^version: {re.escape(SKILL_VERSION)}$")

    def test_skill_md_routes_flight_questions_to_the_page(self) -> None:
        self.assertIn("references/flight-guide.md", self.skill)
        when_to_use = self.skill.split("## When to Use")[1].split("## When Not to Use")[0]
        self.assertIn("when can I fly?", when_to_use)
        self.assertIn("**Flight questions go to `references/flight-guide.md`.**", self.skill)
        self.assertIn("**The flight guide dates itself too.**", self.skill)
        self.assertIn("config/ironjetpacks/jetpacks/*.json", self.skill)

    def test_skill_md_keeps_the_pages_hedges(self) -> None:
        routing = self.skill_flat.split("**Flight questions go to")[1][:900]
        for needle in ("cheapest reliable path", "*(judgement)* labels", "JEI",
                       "does not have"):
            self.assertIn(needle, routing)
        checklist = self.skill.split("## Completion Checklist")[1]
        self.assertIn("references/flight-guide.md", checklist)
        self.assertIn("no Angel Ring", flatten(checklist))

    def test_progression_points_at_the_page(self) -> None:
        progression = flatten(read(PROGRESSION_MD))
        self.assertIn("references/flight-guide.md", progression)
        self.assertIn("Tips and Tricks' *Iron Jetpacks* quest has no dependencies", progression)


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestFlightGuideOffline(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_or_process_module(self) -> None:
        found: "set[str]" = set()
        for line in Path(__file__).read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        self.assertEqual(found & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(found <= {"__future__", "re", "unittest", "pathlib"},
                        f"unexpected import(s): {sorted(found)}")


if __name__ == "__main__":
    unittest.main()
