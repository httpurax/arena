#!/usr/bin/env python3
"""Offline tests for ``references/load-order-guide.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. The page
describes how two independent loaders order ~120 mods, so these tests hold it to what can
actually be known from the install itself -- the manifest fields, the folder split, the
disabling techniques -- and keep it from inventing an ordering mechanism that does not
exist.

Covered:

  * grounding: the page exists, is not a stub, and carries the verified / judgement /
    verify-in-game tags;
  * the two loaders: BepInEx for client plugins, the SPT server for ``user\\mods``, with the
    official folder split quoted from the SPT wiki;
  * no myth-making: the guide must say plainly that there is **no** user-editable
    load-order file, so no one is told to rename a DLL to make it load first;
  * the server side: ``package.json`` and the ordering fields it carries, with the console
    named as the ground truth;
  * disabling, not deleting: renaming a folder, a ``package.json``, or a ``.dll``;
  * conflict rules: one mod per job, Questing Bots' auto-disable left alone, the more
    specific mod wins, co-op on top;
  * cross-references and the offline guarantee.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "load-order-guide.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

# The official split, as the SPT wiki states it.
SPLIT_PATHS = (
    "user\\mods",
    "BepInEx\\plugins",
    "BepInEx\\patchers",
)

# ``package.json`` fields the SPT server loader actually reads.
MANIFEST_FIELDS = (
    "name", "version", "sptVersion", "modDependencies", "loadBefore", "loadAfter", "main",
)

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")

VERIFIED_VERSIONS = {"3.10.5": "the user's SPT version"}

SIBLINGS_NAMED = ("mod-catalog.md", "troubleshooting.md", "mod-install-workflow.md")


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
        self.assertGreater(len(self.text.splitlines()), 100)

    def test_it_carries_the_three_grounding_tags(self) -> None:
        for tag in ("**verified**", "**judgement**", "**verify in-game**"):
            self.assertIn(tag, self.text, f"missing grounding tag {tag}")

    def test_the_official_source_is_cited(self) -> None:
        self.assertIn("https://github.com/sp-tarkov/wiki", self.text)
        self.assertIn("Mod_Types.md", self.text)

    def test_no_url_outside_the_two_allowed_hosts(self) -> None:
        for url in URL_RE.findall(self.text):
            self.assertTrue(url.startswith(("https://sp-mod.com", "https://github.com/")),
                            f"the guide links somewhere it should not: {url}")

    def test_the_dead_forge_domain_is_never_named(self) -> None:
        self.assertNotIn("forge.sp-tarkov", self.text.lower())

    def test_no_invented_version_number(self) -> None:
        found = set(VERSION_RE.findall(self.text))
        self.assertEqual(found - set(VERIFIED_VERSIONS), set(),
                         f"version tokens with no verified source: {sorted(found)}")

    def test_install_root_is_quoted(self) -> None:
        self.assertIn(INSTALL_ROOT, self.text)
        self.assertIn("3.10.5", self.text)


class TestTwoLoaders(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_both_loaders_are_named_and_separated(self) -> None:
        self.assertIn("two independent loaders", self.flat)
        self.assertIn("BepInEx", self.text)
        self.assertIn("SPT.Server.exe", self.text)

    def test_the_official_folder_split_is_quoted(self) -> None:
        for path in SPLIT_PATHS:
            self.assertIn(path, self.text, f"missing the real path {path}")

    def test_the_client_order_is_described_as_dependency_driven(self) -> None:
        self.assertIn("[BepInDependency]", self.text)
        self.assertIn("BepInEx\\patchers", self.text)
        self.assertIn("plugins", self.text)

    def test_it_says_plainly_that_there_is_no_order_file(self) -> None:
        self.assertIn("no user-editable load-order file", self.flat.lower())
        self.assertIn("myth", self.flat.lower(),
                      "the guide must head off the rename-your-DLL myth explicitly")

    def test_the_server_console_is_the_ground_truth_for_loading(self) -> None:
        self.assertIn("server console", self.flat.lower())
        self.assertIn("ground truth", self.flat.lower())


class TestServerModManifest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_every_ordering_field_is_documented(self) -> None:
        for field in MANIFEST_FIELDS:
            self.assertIn(field, self.text,
                          f"the manifest table must document the field {field}")

    def test_sptversion_is_the_compatibility_check(self) -> None:
        self.assertIn("3.10.x", self.text)
        self.assertIn("does not belong in this install", self.text)

    def test_it_points_at_the_install_workflow_for_that_check(self) -> None:
        self.assertIn("mod-install-workflow.md", self.text)


class TestDisablingNotDeleting(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_all_three_disabling_techniques_are_given(self) -> None:
        self.assertIn(".dll.disabled", self.text)
        self.assertIn("package.json.off", self.text)
        self.assertIn("Rename its folder", self.text)

    def test_it_warns_that_a_stray_dll_still_loads(self) -> None:
        self.assertIn("still loaded", self.text)

    def test_bepinex_configs_are_left_alone_while_disabled(self) -> None:
        self.assertIn("BepInEx\\config", self.text)
        self.assertIn("Leave", self.text)


class TestConflictRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_one_mod_per_job_is_the_first_rule(self) -> None:
        self.assertIn("### Rule 1: one mod per job", self.text)

    def test_the_job_table_covers_the_four_contested_jobs(self) -> None:
        for job in ("Bot spawn management", "Bot gear progression", "AI limiting",
                    "Raid/server values"):
            self.assertIn(job, self.text, f"the job table must cover {job}")

    def test_ai_limit_is_documented_as_incompatible(self) -> None:
        self.assertIn("AI Limit is documented as incompatible with Questing Bots", self.flat)

    def test_questing_bots_auto_disable_is_left_alone(self) -> None:
        self.assertIn("turns off its own initial-PMC spawning", self.flat)
        self.assertIn("Leave it off", self.flat)

    def test_the_more_specific_mod_wins_table_exists(self) -> None:
        self.assertIn("### Rule 3", self.text)
        for setting in ("Bot counts / spawn waves", "Bot gear", "Raid timers"):
            self.assertIn(setting, self.text, f"the who-wins table must cover {setting}")

    def test_svm_spawn_settings_are_said_to_lose(self) -> None:
        self.assertIn("SVM are overridden", self.flat)
        self.assertIn("verify in-game", self.flat)

    def test_coop_sits_above_both(self) -> None:
        self.assertIn("### Rule 4", self.text)
        self.assertIn("global bot limit", self.flat)


class TestPracticalOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_read_the_console_before_changing_anything(self) -> None:
        self.assertIn("Read the console before changing anything", self.flat)

    def test_one_change_then_the_same_raid(self) -> None:
        self.assertIn("Change one thing", self.flat)
        self.assertIn("Factory", self.text)

    def test_a_hung_raid_is_called_a_server_problem(self) -> None:
        self.assertIn("server mod", self.flat)
        self.assertIn("troubleshooting.md", self.text)


class TestCrossReferences(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.skill = read(SKILL_MD)

    def test_required_sections_exist(self) -> None:
        for heading in ("# Load order guide", "## Part 1", "## Part 2", "## Part 3",
                        "## Part 4", "## Related pages", "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_named_exists(self) -> None:
        for page in SIBLINGS_NAMED:
            self.assertIn(page, self.text)
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_order_questions_here(self) -> None:
        self.assertIn("references/load-order-guide.md", self.skill)
        self.assertIn("load order", self.skill.lower())


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
