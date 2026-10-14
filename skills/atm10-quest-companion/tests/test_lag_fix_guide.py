#!/usr/bin/env python3
"""Offline tests for ``references/lag-fix-guide.md`` ("how do I fix lag?").

Stdlib-only and network-free: the guide is a snapshot of pack 8.2's config, so these
cases hold that snapshot's verified data as constants and assert the doc still carries
it — never the ~150 MB pack clone, and never the network.

Covered:

  * grounding: the guide exists, is not a stub, names the commit it was read from, dates
    itself against pack 8.2 / the skill's 8.x stamp, states that the in-game quest book
    and JEI are authoritative, flags approximate and judgement content, and says its
    details were read rather than invented;
  * provenance: every pack file the guide claims to quote is named in it;
  * verified quest titles and their exact lag/TPS/FPS sentences, the chapters they live
    in (cross-checked against the shipped 66-chapter list), and the four untitled quests
    kept untitled rather than given a derived name;
  * verified config keys and values: memory thresholds and the recommended-allocation
    table, ModernFix's two non-default lines, AllTheLeaks, spark, Iris, and the per-mod
    render, particle, tick-rate, and chunk-loading knobs;
  * verified mod names and versions from the pack's own modlist, including the fact that
    the renderer is Sodium and not Embeddium;
  * the video-settings claim is grounded in the Sodium option keys the pack ships
    translations for, not in a remembered settings screen;
  * no-invented-names guards: no config file, config key, command, mod, or frame-rate
    number that the pack does not state, every ``namespace:path`` id in the doc on the
    verified allowlist, and "Embeddium" mentioned only to correct the older doc;
  * SKILL.md and ``getting-started.md`` are wired to the guide (version bump, routing,
    grounding rules, checklist item, and the Embeddium → Sodium correction);
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
GUIDE_MD = SKILL_ROOT / "references" / "lag-fix-guide.md"
GETTING_STARTED_MD = SKILL_ROOT / "references" / "getting-started.md"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"

# --------------------------------------------------------------------------------------
# verified data — all of it read from AllTheMods/ATM-10 at main e5e3d1d83e (pack 8.2)
# --------------------------------------------------------------------------------------

PACK_COMMIT = "e5e3d1d83e"
PACK_COMMIT_FULL = "e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025"
MOD_COUNT = "493"

# The pack files the guide's provenance table must name.
SOURCE_FILES = (
    "config/bcc-common.toml",
    "config/memorysettings.json",
    "config/modernfix-mixins.properties",
    "config/alltheleaks.json",
    "config/spark/config.json",
    "config/iris.properties",
    "kubejs/assets/embeddium/lang/pt_br.json",
    "config/Mekanism/client.toml",
    "config/immersiveengineering-client.toml",
    "config/immersiveengineering-server.toml",
    "config/integrateddynamics-common.toml",
    "config/integratedtunnels-common.toml",
    "config/ae2-common.toml",
    "config/ars_nouveau-client.toml",
    "config/ftbultimine-server.snbt",
    "config/quarryplus.toml",
    "config/fluxnetworks-server.toml",
    "config/mahoutsukai-server.toml",
    "config/crashutilities-server.toml",
    "defaultconfigs/incontrol/spawn.json",
    "config/crash_assistant/modlist.json",
    "config/crash_assistant/config.toml",
    "config/fancymenu/options.txt",
    "MOD_ISSUES.md",
)

# Verified quest titles quoted by the guide, and the chapter each one lives in.
VERIFIED_QUEST_TITLES = (
    "Pipez",
    "Mekanism",
    "Integrated Dynamics",
    "Logic Cables",
    "Bio-Generator",
    "Simulated Hydroponic Bed",
    "Sea Prism",
    "Ancient Remnant",
    "Claiming Chunks",
    "Iesnium: Ore of the Otherworld",
)

# Chapters the guide cites; each must be a real chapter in the shipped 66-chapter list.
CITED_CHAPTERS = (
    "Basic Logistics",
    "Integrated Dynamics",
    "Mekanism",
    "Pylons",
    "Industrial Foregoing",
    "Chapter 4: Creative",
    "Cataclysm",
    "Modular Routers",
    "Occultism",
    "Welcome",
)

# Verified task item ids, quoted from the chapter config for the untitled quests.
VERIFIED_TASK_ITEMS = (
    "pipez:wrench",
    "mekanism:configurator",
    "integrateddynamics:wrench",
    "integrateddynamics:cable",
    "pylons:harvester_pylon",
    "modularrouters:fast_pickup_augment",
    "ae2:spatial_anchor",
)

# Verbatim quest text (Minecraft &-codes stripped), as the lang files carry it.
VERIFIED_QUEST_QUOTES = (
    "(Can be laggy when used in mass, still not as laggy as Mekanism pipes though)",
    "(These can cause a bit of lag when used in mass so be careful with them)",
    "(Least laggy pipe solution, these are recommended)",
    "skips a lotta lag",
    "That is because you buttheads keep making massive Melon Farms that eat Servers TPS!",
    "it can be a TPS eater",
    "Ever feel like the standard Hydroponic Bed is too laggy?",
    "Please don't make mass Turtle breeders and mass Guardian slaughter farms. "
    "TPS is important!",
    "His charge will hurt you and your FPS as it destroys every Block in his path.",
    "Very good for less lag!",
    "make sure your particle settings are turned on!",
    "To force load a chunk, shift-left click the chunk.",
    "simply functions as a chunk loader",
)

# Verified config keys and the values the pack ships for them.
VERIFIED_CONFIG_FACTS = (
    # config/memorysettings.json
    ("config/memorysettings.json", "`minimumClient` | `6000`"),
    ("config/memorysettings.json", "`maximumClient` | `32000`"),
    ("config/memorysettings.json", "`minimumServer` | `4096`"),
    ("config/memorysettings.json", "`maximumServer` | `128000`"),
    ("config/memorysettings.json", "`disableWarnings` | `false`"),
    ("config/memorysettings.json", "`warningTolerance` | `200`"),
    ("config/memorysettings.json", '"16000:8000"'),
    ("config/memorysettings.json", '"32000:12000"'),
    ("config/memorysettings.json", '"48000:12000"'),
    ("config/memorysettings.json", '"64000:12000"'),
    ("config/memorysettings.json", "apexminecrafthosting.com/how-to-allocate-more-ram/"),
    # config/modernfix-mixins.properties — the only two lines set beyond the defaults
    ("config/modernfix-mixins.properties", "mixin.perf.dynamic_resources=true"),
    ("config/modernfix-mixins.properties", "stability_level=BETA"),
    ("config/modernfix-mixins.properties", "require restarting the game to take effect"),
    ("config/modernfix-mixins.properties", "You may reset to defaults by deleting this file"),
    # config/alltheleaks.json
    ("config/alltheleaks.json", "ingredientDedupe: true"),
    ("config/alltheleaks.json", "skipTickingUnloadedFluxNetworks: true"),
    ("config/alltheleaks.json", "entitySectionCME"),
    ("config/alltheleaks.json", "disableEternalStarlightProgress"),
    # config/spark/config.json
    ("config/spark/config.json", "backgroundProfiler: false"),
    # config/iris.properties
    ("config/iris.properties", "enableShaders=true"),
    ("config/iris.properties", "shaderPack="),
    ("config/iris.properties", "maxShadowRenderDistance=32"),
    # config/Mekanism/client.toml
    ("config/Mekanism/client.toml", "berRange = 256"),
    ("config/Mekanism/client.toml", "machineEffects = true"),
    ("config/Mekanism/client.toml", "radiationParticleRadius = 30"),
    ("config/Mekanism/client.toml", "radiationParticleCount = 100"),
    # config/integrateddynamics-common.toml
    ("config/integrateddynamics-common.toml", "dynamicShape = true"),
    ("config/integrateddynamics-common.toml", "cacheCableModels = true"),
    ("config/integrateddynamics-common.toml", "partOverlayRenderdistance = 15"),
    ("config/integrateddynamics-common.toml", "ingredientNetworkObserverThreads = 4"),
    ("config/integrateddynamics-common.toml", "safeMode = false"),
    # config/integratedtunnels-common.toml
    ("config/integratedtunnels-common.toml", "worldInteractionEvents = true"),
    ("config/integratedtunnels-common.toml", "inventoryUnchangedTickTimeout = 10"),
    # config/immersiveengineering-*.toml
    ("config/immersiveengineering-server.toml", "particles = true"),
    ("config/immersiveengineering-server.toml", "enableWireDamage = true"),
    ("config/immersiveengineering-client.toml", "increasedTileRenderdistance = 1.5"),
    # config/ae2-common.toml
    ("config/ae2-common.toml", "formationPlaneEntityLimit = 128"),
    ("config/ae2-common.toml", "InterfaceMin = 5"),
    ("config/ae2-common.toml", "AnnihilationPlaneMax = 120"),
    ("config/ae2-common.toml", "non standard rates are not supported or tested"),
    # config/ars_nouveau-client.toml
    ("config/ars_nouveau-client.toml", "opaque_particles = false"),
    # chunk loading and bulk mining
    ("config/quarryplus.toml", "enableChunkLoader = true"),
    ("config/fluxnetworks-server.toml", "enableChunkLoading = false"),
    ("config/mahoutsukai-server.toml", "FAMILIAR_CHUNKLOADS = true"),
    ("config/ftbultimine-server.snbt", "max_blocks: 64"),
    # config/crashutilities-server.toml — the automatic item clear
    ("config/crashutilities-server.toml", "timer = 5"),
    ("config/crashutilities-server.toml", "maximum = 1000"),
    ("config/crashutilities-server.toml", "ITEMCLEAR INCOMING!"),
    ("config/crashutilities-server.toml", "ITEMCLEAR IN % SECONDS"),
    ("config/crashutilities-server.toml", "/spark heapdump"),
    # config/crash_assistant/config.toml
    ("config/crash_assistant/config.toml", "discord.gg/allthemods"),
)

# defaultconfigs/incontrol/spawn.json — all 11 shipped rules.
INCONTROL_RULES = (
    ("minecraft:zombie", "15"),
    ("minecraft:bat", "5"),
    ("minecraft:skeleton", "15"),
    ("minecraft:creeper", "15"),
    ("minecraft:spider", "15"),
    ("minecraft:enderman", "15"),
    ("minecraft:cave_spider", "15"),
    ("minecraft:drowned", "15"),
    ("irons_spellbooks:necromancer", "15"),
    ("creeperoverhaul:cave_creeper", "15"),
    ("creeperoverhaul:dripstone_creeper", "15"),
)

# Verified mod display names and versions, from config/crash_assistant/modlist.json.
VERIFIED_MODS = (
    ("ModernFix", "5.27.24+mc1.21.1"),
    ("Sodium", "0.8.13+mc1.21.1"),
    ("Sodium Extra", "0.9.4+mc1.21.1"),
    ("ImmediatelyFast", "1.6.14+1.21.1"),
    ("Invasive Optimizations", "1.0.24"),
    ("I'm Fast", "1.0.3"),
    ("Ferrite Core", "7.0.3"),
    ("All The Leaks", "1.1.13+1.21.1-neoforge"),
    ("spark", "1.10.124"),
    ("Observable", "5.4.4"),
    ("AI-Improvements", "0.5.3"),
    ("FlickerFix", "6.1.0"),
    ("Model Gap Fix", "1.21-1.10"),
    ("FastFurnace", "9.0.1"),
    ("Fast Workbench", "9.1.3"),
    ("Fast Suite", "6.0.7"),
    ("Iris", "1.8.14-beta.1+mc1.21.1"),
    ("Euphoria Patcher", "1.10.5-r5.9.3-neoforge"),
    ("Mekanism", "10.7.19"),
    ("IntegratedDynamics", "1.37.1"),
    ("Pylons", "5.4.2"),
    ("Modular Routers", "13.2.7"),
    ("Pipez", "1.21.1-1.2.31"),
    ("Industrial Foregoing", "1.21-3.6.39"),
    ("QuarryPlus", "21.1.164"),
    ("InControl", "1.21-10.3.0"),
    ("Crash Utilities", "9.0.4"),
    ("Crash Assistant", "1.11.12"),
)

# Sodium option keys the pack ships translations for in
# kubejs/assets/embeddium/lang/pt_br.json (74 keys in that file). The guide quotes the
# first group with their full key and the second without the `sodium.options.` prefix, as
# it says it does.
SODIUM_OPTION_KEYS_FULL = (
    "sodium.options.pages.quality",
    "sodium.options.pages.performance",
    "sodium.options.pages.advanced",
    "sodium.options.view_distance.tooltip",
    "sodium.options.simulation_distance.tooltip",
    "sodium.options.performance_impact_string",
    "sodium.console.broken_nvidia_driver",
)
SODIUM_OPTION_KEYS_SHORT = (
    "particle_quality",
    "graphics_quality",
    "clouds_quality",
    "weather_quality",
    "leaves_quality",
    "biome_blend",
    "entity_distance",
    "entity_shadows",
    "fps_limit",
    "use_entity_culling",
    "chunk_update_threads",
    "always_defer_chunk_updates",
)

# Every `namespace:path` id the guide is allowed to print. All are quoted from the pack
# config: quest task items, and the mob ids in defaultconfigs/incontrol/spawn.json. The
# last entry is the memorysettings description text, not an item id.
ALLOWED_IDS = frozenset(VERIFIED_TASK_ITEMS) | frozenset(
    mob for mob, _ in INCONTROL_RULES
) | {"memory:recommended"}

# Names, files, keys, and commands the pack does NOT ship. Printing any of them would be
# an invented detail, which is exactly what the skill's grounding rules forbid.
FORBIDDEN_TOKENS = (
    "optifine",
    "rubidium",
    "nvidium",
    "krypton",
    "lithium",
    "canary",
    "c2me",
    "threadtweak",
    "entityculling",
    "entity culling mod",
    "config/sodium.toml",
    "sodium-mixins.properties",
    "embeddium-mixins.properties",
    "config/options.txt",
    "options.txt (video",
    "maxEntityCramming",
    "max-entity-cramming",
    "config/embeddium/",
    "/spark profile",
    "/spark tps",
    "/spark sampler",
    "/spark health",
    "/observable",
    "fps = ",
    "config/sodium.toml",
    "config/sodium-extra.json",
    "config/embeddium.properties",
    "video_settings.toml",
    "options.toml",
)

# Context markers: "Embeddium" may appear only where the guide corrects the older doc or
# names the leftover language files it found in the repo.
EMBEDDIUM_CONTEXT = ("kubejs/assets/embeddium", "Sodium, not Embeddium",
                     "no Embeddium entry", 'saying "Embeddium"', "embeddium.*")


def guide_text() -> str:
    return GUIDE_MD.read_text(encoding="utf-8") if GUIDE_MD.is_file() else ""


def flat(text: str) -> str:
    """Collapse whitespace so assertions do not depend on the doc's line wrapping."""
    return re.sub(r"\s+", " ", text)


# --------------------------------------------------------------------------------------
# grounding and provenance
# --------------------------------------------------------------------------------------

class TestGuideIsGrounded(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = guide_text()
        cls.lower = cls.text.lower()
        cls.flat = flat(cls.text)

    def test_guide_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file(), f"missing {GUIDE_MD}")
        self.assertGreater(len(self.text.strip()), 12000,
                           "the lag guide looks like a stub")
        self.assertIn("how do i fix lag?", self.lower)

    def test_guide_dates_itself_against_the_pack_snapshot(self) -> None:
        for needle in (PACK_COMMIT, PACK_COMMIT_FULL, "8.2", "8.x", "AllTheMods/ATM-10",
                       "2026-09-22"):
            self.assertIn(needle, self.text, f"the guide must date itself with {needle!r}")
        self.assertIn(MOD_COUNT, self.text,
                      "the guide must say how many mods the modlist verifies")

    def test_guide_states_the_authority_and_hedging_rules(self) -> None:
        for needle in ("in-game quest book", "jei", "authoritative", "approximate",
                       "judgement"):
            self.assertIn(needle, self.lower, f"the guide must state the {needle!r} rule")
        self.assertRegex(self.lower, r"never invent|not invented|never guessed|not a guess",
                         "the guide must say its details were read, not invented")
        # The player's own config outranks the snapshot.
        self.assertIn("own `config/` folder", self.text)
        # Judgement is labelled rather than passed off as fact.
        self.assertIn("(judgement", self.text)

    def test_guide_names_every_pack_file_it_quotes(self) -> None:
        for source in SOURCE_FILES:
            self.assertIn(source, self.text, f"the provenance table is missing {source}")

    def test_guide_refuses_to_invent_settings_and_numbers(self) -> None:
        self.assertIn("does not tell you", self.lower)
        self.assertIn("any fps number", self.lower)
        self.assertIn("mods to install or remove", self.lower)
        # A frame-rate gain is never promised: no "<number> fps" anywhere in the doc.
        self.assertEqual(re.findall(r"(?i)\b\d+\s*(?:fps|frames per second)", self.text), [])

    def test_guide_cross_references_the_other_docs(self) -> None:
        for doc in ("getting-started.md", "key-mods.md", "progression.md",
                    "creative-checklist.md", "boss-checklist.md", "SKILL.md"):
            self.assertIn(doc, self.text, f"the guide must cross-reference {doc}")
            target = (SKILL_ROOT / doc) if doc == "SKILL.md" else \
                (SKILL_ROOT / "references" / doc)
            self.assertTrue(target.is_file(), f"cross-referenced doc does not exist: {target}")


# --------------------------------------------------------------------------------------
# verified quest titles, chapters, and quoted quest text
# --------------------------------------------------------------------------------------

class TestVerifiedQuestData(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = guide_text()
        cls.flat = flat(cls.text)

    def test_every_verified_quest_title_is_quoted(self) -> None:
        for title in VERIFIED_QUEST_TITLES:
            self.assertIn(title, self.text,
                          f"the guide is missing a verified quest title: {title}")

    def test_every_lag_quote_is_verbatim(self) -> None:
        for quote in VERIFIED_QUEST_QUOTES:
            self.assertIn(quote, self.flat,
                          f"the guide must quote this quest text verbatim: {quote!r}")

    def test_untitled_quests_stay_untitled(self) -> None:
        """Four of the cited quests carry no title in the config; the guide marks them."""
        self.assertGreaterEqual(self.flat.count("(no title in the config)"), 4,
                                "every untitled quest must be marked, not given a name")
        for item in ("integrateddynamics:cable", "pylons:harvester_pylon",
                     "modularrouters:fast_pickup_augment"):
            self.assertRegex(self.flat,
                             rf"\(no title in the config\)[^|]*{re.escape(item)}",
                             f"the untitled quest for {item} must stay untitled")

    def test_quoted_task_items_are_the_config_ids(self) -> None:
        for item in VERIFIED_TASK_ITEMS:
            self.assertIn(item, self.text,
                          f"the guide must cite the config's task item {item}")

    def test_cited_chapters_are_real_chapters(self) -> None:
        """Cross-check the chapters the guide names against the shipped chapter list."""
        import json
        chapters = {chapter["title"]
                    for chapter in json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))["chapters"]}
        self.assertEqual(len(chapters), 66, "the shipped chapter list is not the 8.2 list")
        for chapter in CITED_CHAPTERS:
            self.assertIn(chapter, chapters,
                          f"the guide cites a chapter the pack does not have: {chapter}")
            self.assertIn(chapter, self.text,
                          f"the guide should name the chapter a quest lives in: {chapter}")

    def test_mekanism_quote_keeps_its_sic(self) -> None:
        """The quest's own typo is quoted as written and marked, not silently fixed."""
        self.assertIn("recommened", self.text)
        self.assertIn("[sic]", self.text)


# --------------------------------------------------------------------------------------
# verified config values
# --------------------------------------------------------------------------------------

class TestVerifiedConfigValues(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = guide_text()
        cls.flat = flat(cls.text)

    def test_every_shipped_config_value_is_quoted(self) -> None:
        for source, fact in VERIFIED_CONFIG_FACTS:
            self.assertIn(source, self.text, f"the guide must name {source}")
            self.assertIn(fact, self.flat,
                          f"the guide must quote {source}'s shipped value: {fact!r}")

    def test_memory_table_matches_the_packs_recommendation(self) -> None:
        """16 GB → 8000 MB, 32/48/64 GB → 12000 MB, as config/memorysettings.json ships."""
        self.assertRegex(self.flat, r"16 GB machine\s*→\s*8000 MB")
        self.assertRegex(self.flat, r"32/48/64\s*GB machine\s*→\s*12000 MB")
        self.assertIn("8 GB on a 16 GB system", self.flat,
                      "the guide must agree with getting-started.md")

    def test_all_eleven_incontrol_rules_are_listed(self) -> None:
        self.assertIn("11 rules", self.flat)
        for mob, minimum in INCONTROL_RULES:
            self.assertIn(mob, self.text, f"missing In Control rule for {mob}")
        self.assertRegex(self.flat, r"`minecraft:bat` at `5`")
        self.assertIn("result", self.text)
        self.assertIn("deny", self.text)

    def test_item_clear_is_described_as_the_packs_own_behaviour(self) -> None:
        self.assertIn("Item Clear", self.text)
        self.assertIn("ITEMCLEAR", self.text)
        self.assertIn("the pack working, not a bug", self.flat)


# --------------------------------------------------------------------------------------
# verified mod list
# --------------------------------------------------------------------------------------

class TestVerifiedMods(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = guide_text()

    def test_every_mod_is_named_with_its_version(self) -> None:
        for name, version in VERIFIED_MODS:
            self.assertIn(name, self.text, f"the guide is missing the mod {name}")
            self.assertIn(version, self.text,
                          f"the guide must quote {name}'s modlist version {version}")

    def test_the_renderer_is_sodium_not_embeddium(self) -> None:
        self.assertIn("Sodium, not Embeddium", self.text)
        self.assertIn("no Embeddium entry", self.text)

    def test_nothing_needs_installing(self) -> None:
        self.assertRegex(self.text.lower(), r"nothing to (?:add|install)")


# --------------------------------------------------------------------------------------
# the video-settings claim is grounded, not remembered
# --------------------------------------------------------------------------------------

class TestVideoSettingsGrounded(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = guide_text()
        cls.flat = flat(cls.text)

    def test_the_settings_come_from_the_shipped_lang_keys(self) -> None:
        self.assertIn("kubejs/assets/embeddium/lang/pt_br.json", self.text)
        self.assertIn("74 keys", self.flat)
        self.assertIn("`sodium.options.<name>.tooltip`", self.text,
                      "the guide must say how the abbreviated option keys are formed")
        for key in SODIUM_OPTION_KEYS_FULL:
            self.assertIn(key, self.text,
                          f"the guide must ground that setting in the shipped key {key}")
        for key in SODIUM_OPTION_KEYS_SHORT:
            self.assertIn(key, self.text,
                          f"the guide must ground that setting in the shipped key {key}")

    def test_the_repo_is_said_to_ship_no_video_settings_file(self) -> None:
        self.assertIn("ships **no** Sodium or video-settings file", self.text)
        self.assertIn("config/fancymenu/options.txt", self.text)
        self.assertIn("default_gui_scale", self.text)
        self.assertIn("force_fullscreen", self.text)

    def test_the_two_translated_tooltips_are_marked_as_translations(self) -> None:
        self.assertEqual(self.flat.count("(translation"), 2,
                         "both quoted Sodium tooltips must be marked as translations")
        self.assertIn("simulation distance", self.flat)


# --------------------------------------------------------------------------------------
# no invented names
# --------------------------------------------------------------------------------------

class TestNoInventedNames(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = guide_text()
        cls.lower = cls.text.lower()

    def test_no_unverified_file_key_command_or_mod_is_named(self) -> None:
        for token in FORBIDDEN_TOKENS:
            self.assertNotIn(token, self.lower,
                             f"the guide names something the pack does not ship: {token!r}")

    def test_every_namespaced_id_is_on_the_verified_allowlist(self) -> None:
        found = {f"{ns}:{path}"
                 for ns, path in re.findall(r"\b([a-z][a-z0-9_]*):([a-z][a-z0-9_/]*)", self.text)}
        unexpected = found - ALLOWED_IDS
        self.assertEqual(unexpected, set(),
                         f"the guide prints ids that are not verified from the config: "
                         f"{sorted(unexpected)}")
        self.assertGreaterEqual(len(found), 15,
                                "the id scan found almost nothing — the regex drifted")

    def test_embeddium_is_mentioned_only_to_correct_the_older_doc(self) -> None:
        lines = [line for line in self.text.splitlines()
                 if "embeddium" in line.lower()]
        self.assertTrue(lines, "the guide should correct the Embeddium/Sodium mix-up")
        for line in lines:
            self.assertTrue(any(marker.lower() in line.lower()
                                for marker in EMBEDDIUM_CONTEXT),
                            f"Embeddium is mentioned outside the correction note: {line!r}")

    def test_no_invented_spark_or_observable_command(self) -> None:
        self.assertIn("this page invents none", self.text)
        self.assertIn("/spark heapdump", self.text,
                      "the one command quoted from the pack config must stay")
        self.assertRegex(self.text, r"its own in-game docs")

    def test_the_guide_says_the_player_config_wins(self) -> None:
        self.assertIn("his wins", self.text)


# --------------------------------------------------------------------------------------
# SKILL.md and getting-started.md are wired to the guide
# --------------------------------------------------------------------------------------

class TestSkillWiring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL_MD.read_text(encoding="utf-8")
        cls.started = GETTING_STARTED_MD.read_text(encoding="utf-8")

    def test_version_was_bumped(self) -> None:
        match = re.search(r"^version:\s*(\d+)\.(\d+)\.(\d+)$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md must carry an X.Y.Z version")
        self.assertGreaterEqual(tuple(int(part) for part in match.groups()), (1, 2, 0),
                                "adding a reference doc is a minor bump")

    def test_skill_md_routes_lag_questions_to_the_guide(self) -> None:
        self.assertIn("references/lag-fix-guide.md", self.skill)
        self.assertIn("how do i fix lag?", self.skill.lower())
        for needle in ("config/memorysettings.json", "FPS", "TPS", "Observable", "spark"):
            self.assertIn(needle, self.skill,
                          f"SKILL.md must describe the lag routing well enough: {needle}")
        self.assertIn("never promise a frame-rate gain", self.skill)

    def test_skill_md_grounding_covers_the_config_snapshot(self) -> None:
        self.assertIn("the lag guide quotes config, and the player's own config wins",
                      self.skill.lower())
        for needle in ("config/modernfix-mixins.properties", "config/alltheleaks.json",
                       "e5e3d1d83e"):
            self.assertIn(needle, self.skill, f"SKILL.md grounding must name {needle}")

    def test_completion_checklist_covers_lag_answers(self) -> None:
        checklist = self.skill.split("## Completion Checklist")[-1]
        self.assertIn("references/lag-fix-guide.md", checklist)
        self.assertIn("kind of lag", checklist)
        self.assertIn("frame-rate number", checklist)

    def test_getting_started_no_longer_names_embeddium_as_shipped(self) -> None:
        self.assertNotIn("Embeddium", self.started,
                         "getting-started.md must name the renderer the modlist ships")
        self.assertIn("Sodium", self.started)
        self.assertIn("references/lag-fix-guide.md", self.started)


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def test_this_suite_imports_no_network_module(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        imported: "set[str]" = set()
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                imported.update(part.strip().split()[0].split(".")[0]
                                for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                imported.add(stripped.split()[1].split(".")[0])
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set(),
                         f"this suite must stay offline: {sorted(imported)}")
        self.assertTrue(imported <= {"re", "unittest", "pathlib", "json", "__future__"},
                        f"unexpected import(s): {sorted(imported)}")

    def test_the_guide_needs_no_file_outside_the_skill(self) -> None:
        """The guide is a document: no script reads it, so nothing can reach the network."""
        text = guide_text()
        for statement in ("```bash", "```powershell", "python3 ", "curl ", "git clone"):
            self.assertNotIn(statement, text,
                             f"the guide should not tell a session to run {statement!r}")


if __name__ == "__main__":
    unittest.main()
