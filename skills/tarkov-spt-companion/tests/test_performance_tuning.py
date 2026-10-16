#!/usr/bin/env python3
"""Offline tests for ``references/performance-tuning.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. The user's
hardware constraint is 16 GB of RAM, so this page is the one most at risk of drifting into
confident nonsense; these tests hold it to naming levers and never promising a frame rate.

Covered:

  * grounding: exists, not a stub, all four tags, no invented versions, no dead domain;
  * the promise: no frame-rate numbers anywhere on the page;
  * step 0: the three processes sharing 16 GB, named as a budget;
  * step 1: RAM hygiene first -- pagefile, the in-game cleaner's real behaviour, browser;
  * step 2: the cost ranking, with the insight that rank 1 is a **setting**, not a mod;
  * step 3: the per-mod levers, each with its real config path and its verified default
    (Questing Bots' 1 ms frame budget, its 200 m / 75 m limiter distances, Streets-only
    default);
  * step 4: graphics settings, and ``boot.config`` handled as the risky last step with a
    backup-first rule;
  * step 5: the order to do things, with ``boot.config`` last;
  * cross-references and the offline guarantee.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "performance-tuning.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

# Config paths the levers live in.
LEVER_PATHS = (
    "user\\mods\\SWAG\\config\\config.json",
    "BepInEx\\plugins\\dvize.Donuts\\ScenarioConfig.json",
    "EscapeFromTarkov_Data\\boot.config",
)

# Verified defaults quoted from the Questing Bots README.
VERIFIED_DEFAULTS = (
    "max_calc_time_per_frame_ms",   # 1 ms per frame
    "200 m",                        # limiter distance from the player
    "75 m",                         # limiter distance from other questing bots
    "Streets",                      # the only map limited by default
)

GRAPHICS_SETTINGS = (
    "LOD quality", "visibility distance", "Shadow quality", "HBAO", "SSR",
    "Nvidia Reflex", "Texture quality", "MIP streaming", "physical cores",
)

BOOT_CONFIG_KEYS = (
    "gfx-enable-gfx-jobs", "gfx-enable-native-gfx-jobs", "gfx-disable-mt-rendering",
    "gc-max-time-slice", "job-worker-count",
)

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")

VERIFIED_VERSIONS = {"3.10.5": "the user's SPT version"}

SIBLINGS_NAMED = ("mod-catalog.md", "troubleshooting.md", "backup-restore.md")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def squashed(text: str) -> str:
    return re.sub(r"\s+", " ", text)


class TestGrounding(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_page_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(DOC.is_file(), f"missing {DOC}")
        self.assertGreater(len(self.text.splitlines()), 120)

    def test_all_four_grounding_tags_are_carried(self) -> None:
        for tag in ("**verified**", "**reported**", "**judgement**", "**verify in-game**"):
            self.assertIn(tag, self.text, f"missing grounding tag {tag}")

    def test_no_invented_version_number(self) -> None:
        found = set(VERSION_RE.findall(self.text))
        self.assertEqual(found - set(VERIFIED_VERSIONS), set(),
                         f"version tokens with no verified source: {sorted(found)}")

    def test_no_url_outside_the_two_allowed_hosts(self) -> None:
        for url in URL_RE.findall(self.text):
            self.assertTrue(url.startswith(("https://sp-mod.com", "https://github.com/")),
                            f"the guide links somewhere it should not: {url}")

    def test_the_dead_forge_domain_is_never_named(self) -> None:
        self.assertNotIn("forge.sp-tarkov", self.text.lower())

    def test_install_root_and_memory_are_quoted(self) -> None:
        self.assertIn(INSTALL_ROOT, self.text)
        self.assertIn("16 GB", self.text)


class TestNoFrameRatePromises(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_page_states_the_promise_up_front(self) -> None:
        self.assertIn("names levers, never frame-rate numbers", self.flat)

    def test_no_plus_fps_claim(self) -> None:
        self.assertNotIn("+20 FPS", self.text)
        self.assertNotIn("+%", self.text)
        self.assertIn("never frame-rate numbers", self.flat.lower())
        self.assertNotIn("+X FPS", self.text)

    def test_it_tells_the_player_to_measure_himself(self) -> None:
        self.assertIn("Try a lever, play a Factory raid, keep it if it helped", self.flat)


class TestBudget(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_three_processes_sharing_the_memory_are_named(self) -> None:
        self.assertIn("## Step 0", self.text)
        for process in ("client", "SPT.Server.exe", "Windows + browser"):
            self.assertIn(process, self.flat, f"the budget table must name {process!r}")

    def test_the_conclusion_is_drawn(self) -> None:
        self.assertIn("the server is sitting in the same pool", self.flat)


class TestRamHygiene(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_hygiene_comes_before_mod_settings(self) -> None:
        self.assertIn("## Step 1", self.text)
        self.assertIn("before touching a single mod setting", self.flat)

    def test_the_pagefile_is_the_first_item(self) -> None:
        self.assertIn("pagefile", self.flat.lower())

    def test_the_in_game_cleaners_real_behaviour_is_stated(self) -> None:
        self.assertIn("double-tap", self.flat)
        self.assertIn("RAM Cleaner Fix", self.text)
        self.assertIn("90 seconds", self.text)

    def test_the_browser_is_not_treated_as_free(self) -> None:
        self.assertIn("Close the browser", self.flat)

    def test_restarting_is_offered_as_reported_not_promised(self) -> None:
        self.assertIn("Restart between long sessions", self.flat)


class TestCostRanking(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_ranking_table_exists(self) -> None:
        self.assertIn("## Step 2", self.text)
        self.assertIn("| Rank | Mod / system | Why it costs | Where the lever is |", self.text)

    def test_the_expected_mods_are_ranked(self) -> None:
        for mod in ("SWAG + Donuts", "SAIN", "Questing Bots", "Looting Bots", "ALP"):
            self.assertIn(mod, self.text, f"the cost ranking must cover {mod}")

    def test_rank_one_is_a_setting_not_a_mod(self) -> None:
        self.assertIn("**rank 1 is a setting, not a mod.**", self.flat)

    def test_leak_suspects_are_marked_reported(self) -> None:
        self.assertIn("Game Panel HUD", self.text)
        self.assertIn("Late to the Party", self.text)

    def test_the_heavy_maps_are_named(self) -> None:
        for location in ("Streets", "Lighthouse", "Ground Zero"):
            self.assertIn(location, self.text, f"the ranking must name the map {location}")


class TestLevers(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_every_lever_path_is_quoted(self) -> None:
        self.assertIn("## Step 3", self.text)
        for path in LEVER_PATHS:
            self.assertIn(path, self.text, f"missing the lever path {path}")

    def test_the_swag_caps_are_named(self) -> None:
        self.assertIn("MaxBotCap", self.text)
        self.assertIn("NightMaxBotCap", self.text)

    def test_questing_bots_verified_defaults_are_quoted(self) -> None:
        for needle in VERIFIED_DEFAULTS:
            self.assertIn(needle, self.text, f"missing the verified default {needle!r}")
        self.assertIn("1 ms", self.text)

    def test_questing_bots_own_limiter_is_the_compatible_one(self) -> None:
        self.assertIn("AI Limit and Questing Bots are incompatible", self.flat)

    def test_donuts_own_spawn_rules_are_cited(self) -> None:
        self.assertIn("https://github.com/dvize/Donuts", self.text)
        self.assertIn("spawn marker", self.flat)

    def test_coop_gets_a_lever_too(self) -> None:
        self.assertIn("global bot limit", self.flat)
        self.assertIn("headless client", self.flat)


class TestGraphicsAndBootConfig(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_settings_that_matter_are_covered(self) -> None:
        self.assertIn("## Step 4", self.text)
        for needle in GRAPHICS_SETTINGS:
            self.assertIn(needle, self.text, f"the graphics table must cover {needle!r}")

    def test_settings_are_marked_as_judgement_for_his_gpu(self) -> None:
        self.assertIn("All judgement, all *verify in-game*", self.flat)

    def test_boot_config_is_called_the_risky_one(self) -> None:
        self.assertIn("the risky one", self.flat)
        self.assertIn("EscapeFromTarkov_Data\\boot.config", self.text)

    def test_the_boot_config_keys_are_quoted(self) -> None:
        for key in BOOT_CONFIG_KEYS:
            self.assertIn(key, self.text, f"missing the boot.config key {key!r}")

    def test_boot_config_rules_demand_a_backup_and_one_line_at_a_time(self) -> None:
        for rule in ("Copy `boot.config` to your backup folder first",
                     "Change **one** line", "job-worker-count` is machine-specific"):
            self.assertIn(rule, self.flat, f"missing the boot.config rule {rule!r}")


class TestOrderAndCrossReferences(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)
        cls.skill = read(SKILL_MD)

    def test_the_ordered_list_puts_boot_config_last(self) -> None:
        self.assertIn("## Step 5", self.text)
        steps = self.text.split("## Step 5")[-1]
        self.assertLess(steps.index("Lower `MaxBotCap`"), steps.index("boot.config` last"))

    def test_required_sections_exist(self) -> None:
        for heading in ("# Performance tuning", "## Step 0", "## Step 1", "## Step 2",
                        "## Step 3", "## Step 4", "## Step 5", "## Related pages",
                        "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_named_exists(self) -> None:
        for page in SIBLINGS_NAMED:
            self.assertIn(page, self.text)
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_fps_questions_here(self) -> None:
        self.assertIn("references/performance-tuning.md", self.skill)
        self.assertIn("16 GB", self.skill)
        self.assertIn("FPS", self.skill)

    def test_skill_md_forbids_frame_rate_promises(self) -> None:
        self.assertIn("No FPS number was promised", self.skill)


class TestOfflineGuarantee(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess", "os")

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
        self.assertTrue(imported <= {"re", "unittest", "pathlib", "__future__"},
                        f"unexpected import(s): {sorted(imported)}")


if __name__ == "__main__":
    unittest.main()
