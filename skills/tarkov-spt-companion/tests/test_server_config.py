#!/usr/bin/env python3
"""Offline tests for ``references/server-config.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. The page
documents the SPT 3.10.5 server config folder, so the tests hold it to: the real folder, the
real file names, the two ``core.json`` switches that rescue a profile, LAN co-op addressing
that actually works, and SVM as a **server** mod with its real preset layout.

Covered:

  * grounding: exists, not a stub, the tags, no invented versions, no dead domain;
  * the config folder, the stop-the-server-first rule, and the keep-a-copy rule;
  * the nine config files, with their responsibilities hedged where they were not verified;
  * ``http.json``: ``ip`` / ``backendIp`` / ``port``, the default port, and the LAN co-op
    guidance that distinguishes binding from what the client is told;
  * ``core.json``: ``sptVersion``, ``serverName``, and the two profile-cleaning switches;
  * SVM: the mod folder, the presets folder, ``loader.json``, ``Greed.exe``, and the
    uninstall note about its optional CSM client file;
  * the who-overrides-whom table, including that the spawn mods beat SVM's spawn settings;
  * a playstyle section mapping wants to files rather than to invented values;
  * editing rules (stop, copy, one change, test, restore the .bak);
  * cross-references and the offline guarantee.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "server-config.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

CONFIG_DIR = "SPT_Data\\Server\\configs"

# The nine files, as documented for SPT's server configs.
CONFIG_FILES = {
    "core.json": "core server settings",
    "http.json": "backendIp",
    "gameplay.json": "gameplay",
    "inraid.json": "in-raid",
    "insurance.json": "insurance",
    "location.json": "per-map",
    "ragfair.json": "flea",
    "trader.json": "trader",
    "weather.json": "weather",
}

HTTP_KEYS = ("ip", "backendIp", "port")

CORE_KEYS = ("sptVersion", "serverName", "removeModItemsFromProfile",
             "removeInvalidTradersFromProfile")

SVM_PATHS = (
    "user\\mods\\[SVM] ServerValueModifier\\",
    "user\\mods\\[SVM] ServerValueModifier\\Presets\\*.json",
    "user\\mods\\[SVM] ServerValueModifier\\loader.json",
)

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")

VERIFIED_VERSIONS = {"3.10.5": "the user's SPT version"}

SIBLINGS_NAMED = ("backup-restore.md", "load-order-guide.md", "performance-tuning.md",
                  "mod-catalog.md")


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

    def test_the_three_grounding_tags_are_carried(self) -> None:
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

    def test_install_root_is_quoted(self) -> None:
        self.assertIn(INSTALL_ROOT, self.text)


class TestConfigFolder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_3_10_folder_is_named_and_hedged(self) -> None:
        self.assertIn(CONFIG_DIR, self.text)
        self.assertIn("**verify in-game**", self.text,
                      "the folder location must be flagged for confirmation")

    def test_the_old_path_is_called_gone(self) -> None:
        self.assertIn("Aki_Data", self.text)
        self.assertIn("is gone", self.flat)

    def test_stop_the_server_before_editing(self) -> None:
        self.assertIn("**The server must be stopped before editing any of these files.**",
                      self.text)

    def test_keep_a_copy_beside_each_file(self) -> None:
        self.assertIn("**Keep a copy beside each file you edit.**", self.text)


class TestConfigFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_all_nine_files_are_listed(self) -> None:
        for name, responsibility in CONFIG_FILES.items():
            self.assertIn(name, self.text, f"the file table must list {name}")
            self.assertIn(responsibility, self.text,
                          f"{name}'s row must say something about {responsibility}")

    def test_uncertain_rows_are_hedged(self) -> None:
        self.assertIn("**verify in-game** against the installed file", self.text)
        self.assertIn("verify each file exists", self.text)


class TestHttpJson(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_keys_are_quoted(self) -> None:
        for key in HTTP_KEYS:
            self.assertIn(key, self.text, f"http.json coverage must name the key {key}")

    def test_the_default_port_is_stated(self) -> None:
        self.assertIn("6969", self.text)

    def test_lan_coop_gets_its_own_row(self) -> None:
        self.assertIn("LAN co-op", self.text)
        self.assertIn("0.0.0.0", self.text)

    def test_binding_is_distinguished_from_what_the_client_is_told(self) -> None:
        self.assertIn("it is a bind setting, not a client setting", self.flat)
        self.assertIn("launcher's server URL", self.flat)

    def test_it_says_to_confirm_from_the_other_machine(self) -> None:
        self.assertIn("confirm from the **other** machine", self.flat)


class TestCoreJson(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_all_four_keys_are_documented(self) -> None:
        for key in CORE_KEYS:
            self.assertIn(key, self.text, f"core.json coverage must name the key {key}")

    def test_sptversion_should_read_the_install_version(self) -> None:
        self.assertIn("should read **3.10.5** here", self.text)

    def test_the_profile_switches_point_at_the_restore_guide(self) -> None:
        self.assertIn("backup-restore.md", self.text)


class TestSvm(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_svm_is_called_a_server_mod(self) -> None:
        self.assertIn("SVM is a **server** mod", self.text)

    def test_every_svm_path_is_quoted(self) -> None:
        for path in SVM_PATHS:
            self.assertIn(path, self.text, f"missing the SVM path {path}")

    def test_greed_lives_beside_the_server_executable(self) -> None:
        self.assertIn("Greed.exe", self.text)
        self.assertIn("SPT.Server.exe", self.text)

    def test_the_source_repository_is_cited(self) -> None:
        self.assertIn("https://github.com/GhostFenixx/svm-csharp", self.text)

    def test_the_workflow_saves_a_named_preset(self) -> None:
        self.assertIn("save it as a named preset", self.flat)
        self.assertIn("Confirm `loader.json` points at the preset you just saved", self.flat)

    def test_the_csm_note_is_a_removal_note_only(self) -> None:
        self.assertIn("HideSpecialIcon.dll", self.text)
        self.assertIn("not a licence to add new client DLLs", self.flat)


class TestWhoOverridesWhom(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_table_covers_the_four_layers(self) -> None:
        self.assertIn("## Who overrides whom", self.text)
        for row in ("Spawn numbers", "Bot gear / progression",
                    "Raid timers, extracts, insurance, flea, skills", "Everything, in co-op"):
            self.assertIn(row, self.text, f"the override table must cover {row!r}")

    def test_the_spawn_mods_beat_svm(self) -> None:
        self.assertIn("SVM spawn/bot settings are overridden", self.flat)
        self.assertIn("user\\mods\\SWAG\\config\\config.json", self.text)
        self.assertIn("BepInEx\\plugins\\dvize.Donuts\\ScenarioConfig.json", self.text)

    def test_it_warns_against_setting_one_value_twice(self) -> None:
        self.assertIn("**do not set the same value in two places.**", self.text)


class TestPlaystyleAndEditingRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)
        cls.skill = read(SKILL_MD)

    def test_the_playstyle_section_maps_wants_to_files(self) -> None:
        self.assertIn("## For this playstyle", self.text)
        for want in ("Longer/shorter raids", "More loot", "Insurance", "Extracts always"):
            self.assertIn(want, self.text, f"the playstyle table must cover {want!r}")

    def test_the_editing_rules_are_five_numbered_steps(self) -> None:
        self.assertIn("## Editing rules", self.text)
        for rule in ("**Stop the server.**", "**Copy the file first**",
                     "trailing comma", "Change **one** thing", "restore the `.bak`"):
            self.assertIn(rule, self.text, f"missing editing rule {rule!r}")

    def test_required_sections_exist(self) -> None:
        for heading in ("# Server config", "## The config files", "## `http.json`",
                        "## `core.json`", "## SVM", "## Who overrides whom",
                        "## For this playstyle", "## Editing rules", "## Related pages",
                        "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_named_exists(self) -> None:
        for page in SIBLINGS_NAMED:
            self.assertIn(page, self.text)
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_server_settings_here(self) -> None:
        self.assertIn("references/server-config.md", self.skill)
        self.assertIn("SVM", self.skill)
        self.assertIn("raid settings", self.skill.lower())


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
