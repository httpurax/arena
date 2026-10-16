#!/usr/bin/env python3
"""Offline tests for ``references/mod-install-workflow.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. This page is
the gate a new mod has to pass before it touches a ~120-mod install, so the tests hold it to
the user's two hard rules -- **sp-mod.com and GitHub releases only**, and **server-side
only, no new BepInEx client DLLs** -- and to a workflow that can actually be undone.

Covered:

  * grounding: exists, not a stub, the tags, no invented versions, no dead domain;
  * the two rules, stated up front;
  * step 0 source check: the two allowed hosts, and repacks as an auto-reject;
  * step 1 version check: the Versions tab as the authority, 3.10.x, and the
    ``package.json`` → ``sptVersion`` confirmation on disk;
  * step 2 side check: how to read an archive, and the verdict for each shape it can have;
  * step 3 dependencies, including the recurring ones for this stack;
  * step 4 conflict check against the friction table;
  * step 5 backup, step 6 replace-never-merge install, step 7 the Factory test protocol;
  * step 8 recording it in the catalog;
  * rollback: three levels, and the warning that rollback needs the backup;
  * red flags, the worksheet, cross-references, and the offline guarantee.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "mod-install-workflow.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

# The two hosts a mod may come from.
ALLOWED_HOSTS = ("https://sp-mod.com", "GitHub releases")

# The recurring dependencies for this stack.
STACK_DEPENDENCIES = ("BigBrain", "Waypoints", "UnityToolkit")

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")

VERIFIED_VERSIONS = {
    "3.10.5": "the user's SPT version",
    "1.2.0": "SWAG + Donuts requires UnityToolkit V1.2.0 (sp-mod.com)",
    "4.0.0": "SWAG + Donuts 4.0.0 is marked SPT 3.10.5 compatible (sp-mod.com)",
}

SIBLINGS_NAMED = ("backup-restore.md", "load-order-guide.md", "mod-catalog.md",
                  "troubleshooting.md", "performance-tuning.md")

FACTORY_CHECKS = (
    "Raid **loads**",
    "Server console is clean",
    "Bots spawn",
    "You can extract",
    "Profile saved",
    "Frame time",
)


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
        self.assertGreater(len(self.text.splitlines()), 130)

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


class TestTheTwoRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_both_rules_are_stated_up_front(self) -> None:
        self.assertIn("**New mods are server-side only.**", self.text)
        self.assertIn("**Sources are `https://sp-mod.com` and GitHub releases only.**",
                      self.text)

    def test_no_new_client_dlls_is_spelled_out(self) -> None:
        self.assertIn("No new BepInEx client DLLs", self.flat)

    def test_the_dead_domain_is_called_dead(self) -> None:
        self.assertIn("The old Forge domain is dead", self.flat)


class TestSourceCheck(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_step_zero_lists_the_checks(self) -> None:
        self.assertIn("## Step 0 — source check", self.text)
        for host in ALLOWED_HOSTS:
            self.assertIn(host, self.text, f"the source check must name {host}")

    def test_repacks_are_an_auto_reject(self) -> None:
        self.assertIn("Repacks", self.text)
        self.assertIn("auto-rejects", self.flat)

    def test_it_rejects_mods_that_do_not_name_3_10(self) -> None:
        self.assertIn("SPT 3.10.x", self.text)
        self.assertIn("3.9.x", self.text)


class TestVersionCheck(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_versions_tab_is_the_authority(self) -> None:
        self.assertIn("## Step 1", self.text)
        self.assertIn("**Versions** tab", self.flat)
        self.assertIn("the authority", self.flat)

    def test_it_wants_a_3_10_x_build(self) -> None:
        self.assertIn("3.10.x", self.text)
        self.assertIn("3.10.5", self.text)
        self.assertIn('"3.10.x ONLY"', self.text)

    def test_the_manifest_is_the_final_check(self) -> None:
        self.assertIn("package.json", self.text)
        self.assertIn("sptVersion", self.text)
        self.assertIn("it beats any web page", self.flat)

    def test_it_refuses_to_invent_a_version(self) -> None:
        self.assertIn("Never invent or assume a version", self.flat)


class TestSideCheck(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_archive_is_opened_before_extracting(self) -> None:
        self.assertIn("## Step 2", self.text)
        self.assertIn("Open the archive **before** extracting anything", self.flat)

    def test_all_four_archive_shapes_are_judged(self) -> None:
        for shape in ("user\\mods\\<Folder>\\", "BepInEx\\plugins\\*.dll", "Both",
                      "Just a `config` folder"):
            self.assertIn(shape, self.text, f"the side check must judge {shape!r}")

    def test_a_client_only_mod_is_rejected(self) -> None:
        self.assertIn("**client plugin** — reject by this install's rule", self.flat)

    def test_a_preset_pack_is_called_a_config_not_a_mod(self) -> None:
        self.assertIn("**a preset/config pack**, not a mod", self.flat)

    def test_the_official_split_is_quoted(self) -> None:
        self.assertIn("https://github.com/sp-tarkov/wiki", self.text)
        for path in ("user\\mods", "BepInEx\\plugins", "BepInEx\\patchers"):
            self.assertIn(path, self.text, f"missing the split path {path}")


class TestDependencyAndConflictChecks(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_recurring_dependencies_are_named(self) -> None:
        self.assertIn("## Step 3", self.text)
        for dep in STACK_DEPENDENCIES:
            self.assertIn(dep, self.text, f"the dependency check must name {dep}")

    def test_missing_dependencies_are_visible_not_subtle(self) -> None:
        self.assertIn("modDependencies", self.text)
        self.assertIn("the server prints it and skips the mod", self.flat)

    def test_the_conflict_check_lists_the_four_jobs(self) -> None:
        self.assertIn("## Step 4", self.text)
        for job in ("second bot-progression mod", "second spawn manager", "AI limiter",
                    "SVM or the spawn mods already own"):
            self.assertIn(job, self.flat, f"missing conflict check {job!r}")

    def test_questing_bots_auto_disable_is_respected(self) -> None:
        self.assertIn("Questing Bots auto-disables its own initial-PMC", self.flat)


class TestInstallAndTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_step_five_requires_a_backup(self) -> None:
        self.assertIn("## Step 5", self.text)
        self.assertIn("user\\profiles", self.text)
        self.assertIn("full snapshot", self.flat)

    def test_step_six_replaces_and_never_merges(self) -> None:
        self.assertIn("## Step 6 — install (replace, never merge)", self.text)
        for step in ("staging folder outside the install", "**delete or rename** the target folder",
                     "**Copy** the staged folder", "read the console"):
            self.assertIn(step, self.flat, f"missing install step {step!r}")

    def test_step_seven_is_the_factory_test(self) -> None:
        self.assertIn("## Step 7 — the Factory test", self.text)
        for check in FACTORY_CHECKS:
            self.assertIn(check, self.text, f"the Factory test must check {check!r}")

    def test_it_demands_a_second_bigger_map(self) -> None:
        self.assertIn("one bigger map", self.flat)
        self.assertIn("Factory is too small", self.flat)

    def test_step_eight_records_the_mod(self) -> None:
        self.assertIn("## Step 8 — record it", self.text)
        self.assertIn("mod-catalog.md", self.text)


class TestRollback(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_three_levels_are_tabled(self) -> None:
        self.assertIn("## Rollback", self.text)
        for level in ("**1. Disable**", "**2. Reset the config**",
                      "**3. Remove and restore**"):
            self.assertIn(level, self.text, f"missing rollback level {level!r}")

    def test_the_cheapest_level_loses_nothing(self) -> None:
        self.assertIn("nothing — settings survive", self.flat)

    def test_rollback_depends_on_the_backup(self) -> None:
        self.assertIn("**Rollback is only real if Step 5 happened.**", self.text)


class TestRedFlagsAndWorksheet(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)
        cls.skill = read(SKILL_MD)

    def test_the_reject_list_is_present(self) -> None:
        self.assertIn("## Red flags — reject without testing", self.text)
        for flag in ("Any new client DLL", "sptVersion` is not 3.10.x",
                     "promises a frame-rate number"):
            self.assertIn(flag, self.text, f"missing red flag {flag!r}")

    def test_the_worksheet_is_shipped(self) -> None:
        self.assertIn("## The worksheet", self.text)
        for field in ("Versions tab -> SPT build chosen:", "Server-side only?",
                      "Factory raid:", "Rolled back?", "Catalog row added:"):
            self.assertIn(field, self.text, f"the worksheet must have {field!r}")

    def test_required_sections_exist(self) -> None:
        for heading in ("# Mod install workflow", "## Step 0", "## Step 1", "## Step 2",
                        "## Step 3", "## Step 4", "## Step 5", "## Step 6", "## Step 7",
                        "## Step 8", "## Rollback", "## Red flags", "## The worksheet",
                        "## Related pages", "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_named_exists(self) -> None:
        for page in SIBLINGS_NAMED:
            self.assertIn(page, self.text)
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_new_mod_questions_here(self) -> None:
        self.assertIn("references/mod-install-workflow.md", self.skill)
        self.assertIn("Versions tab", self.skill)
        self.assertIn("Factory", self.skill)


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
