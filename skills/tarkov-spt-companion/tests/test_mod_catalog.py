#!/usr/bin/env python3
"""Offline tests for ``references/mod-catalog.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. The skill is a
document set about one SPT 3.10.5 install, so the tests hold each page to the rules the
user set for it -- real paths, no invented versions, no invented URLs, uncertainty marked --
rather than to facts about mods.

Covered here:

  * grounding: the page exists, is not a stub, and carries the provenance block that says
    where each claim came from (stated / verified / verify in-game);
  * the install profile: SPT 3.10.5, the install root, ~47 server mods, ~79 client plugins;
  * the core AI stack: all eight mods the user named, with the side of the install each
    lives on;
  * real paths only: every path the page quotes is one of the SPT 3.10.5 paths this skill
    uses, and every URL is on the two allowed hosts;
  * no invented versions: every X.Y.Z token on the page was verified from sp-mod.com or a
    GitHub repository, and the dead Forge domain is never named;
  * the enumeration commands: PowerShell that reads ``package.json`` out of ``user\\mods``;
  * friction pairs: AI Limit vs Questing Bots, one progression mod, SVM vs the spawn mods;
  * cross-references: SKILL.md routes here, and every sibling page named exists;
  * SKILL.md conformance: frontmatter keys, the hard rules, and the completion checklist;
  * offline guarantee: this suite imports no network or process module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "mod-catalog.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

# The eight mods the user named as the core of his AI stack.
CORE_STACK = (
    "SAIN", "BigBrain", "Waypoints", "Donuts", "SWAG",
    "Questing Bots", "Looting Bots", "ALP",
)

# Real SPT 3.10.5 paths. A path on the page that is not one of these (or a folder under one
# of them) is an invented path.
REAL_PATHS = (
    "user\\mods",
    "BepInEx\\plugins",
    "BepInEx\\patchers",
    "BepInEx\\config",
    "user\\profiles",
    "SPT_Data\\Server\\configs",
    "SPT_Data\\Server\\database",
    "user\\mods\\SWAG\\config\\config.json",
    "user\\mods\\SWAG\\config\\bossConfig.json",
    "BepInEx\\plugins\\dvize.Donuts\\ScenarioConfig.json",
    "user\\mods\\[SVM] ServerValueModifier",
    "user\\mods\\fika-server",
)

# Paths the page may also write with forward slashes, because that is how the upstream
# project prints them.
FORWARD_SLASH_PATHS = (
    "BepInEx/plugins/dvize.Donuts/Config",
    "user/mods/[SVM] ServerValueModifier",
)

# Paths inside the skill itself rather than inside the game install.
SKILL_PATHS = ("data\\",)

# URLs that appear on the page, all read from these two hosts during research.
ALLOWED_URLS = (
    "https://sp-mod.com",
    "https://github.com/dwesterwick/SPTQuestingBots",
    "https://github.com/dvize/Donuts",
    "https://github.com/Andrewgdewar/AlgorithmicLevelProgression",
    "https://github.com/GhostFenixx/svm-csharp",
    "https://github.com/sp-tarkov/wiki",
)

# Every X.Y.Z version token on the page, with the source that stated it.
VERIFIED_VERSIONS = {
    "3.10.5": "the user's SPT version",
    "1.2.0": "SWAG + Donuts 4.0.0 requires UnityToolkit V1.2.0 (sp-mod.com)",
    "1.5.0": "Questing Bots requires BigBrain 1.5.0+ (its README)",
    "1.9.0": "Questing Bots requires Waypoints 1.9.0+ (its README)",
    "4.5.0": "Questing Bots recommends SAIN 4.5.0+ (its README)",
    "1.8.0": "Questing Bots recommends Looting Bots 1.8.0+ (its README)",
    "4.0.0": "SWAG + Donuts 4.0.0 is marked SPT 3.10.5 compatible (sp-mod.com)",
}

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")
BACKTICKED_PATH_RE = re.compile(r"`([^`]+)`")

SIBLING_PAGES = (
    "load-order-guide.md",
    "troubleshooting.md",
    "performance-tuning.md",
    "backup-restore.md",
    "mod-install-workflow.md",
    "server-config.md",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def squashed(text: str) -> str:
    return re.sub(r"\s+", " ", text)


# --------------------------------------------------------------------------------------
# grounding
# --------------------------------------------------------------------------------------

class TestGrounding(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_page_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(DOC.is_file(), f"missing {DOC}")
        self.assertGreater(len(self.text.splitlines()), 120,
                           "the catalog is shorter than a real inventory page")

    def test_it_states_its_own_provenance(self) -> None:
        self.assertIn("## Provenance", self.text)
        for source in ("stated by the user", "https://sp-mod.com", "https://github.com/"):
            self.assertIn(source, self.text, f"provenance must name {source}")

    def test_it_carries_all_three_grounding_tags(self) -> None:
        for tag in ("**stated**", "**verified**", "**verify in-game**"):
            self.assertIn(tag, self.text, f"the grounding table must define {tag}")

    def test_uncertainty_is_marked_repeatedly(self) -> None:
        self.assertGreaterEqual(self.text.count("verify in-game"), 5,
                                "the catalog must keep flagging what it cannot confirm")

    def test_the_dead_forge_domain_is_never_named(self) -> None:
        self.assertNotIn("forge.sp-tarkov", self.text.lower())

    def test_every_url_is_on_the_allowed_hosts(self) -> None:
        for url in URL_RE.findall(self.text):
            self.assertTrue(url.startswith(("https://sp-mod.com", "https://github.com/")),
                            f"the catalog links somewhere it should not: {url}")

    def test_the_verified_repositories_are_cited(self) -> None:
        for url in ALLOWED_URLS:
            self.assertIn(url, self.text, f"the catalog must cite {url}")

    def test_no_invented_version_number(self) -> None:
        found = set(VERSION_RE.findall(self.text))
        unexpected = found - set(VERIFIED_VERSIONS)
        self.assertEqual(unexpected, set(),
                         f"version tokens with no verified source: {sorted(unexpected)}")
        self.assertIn("3.10.5", found, "the SPT version must be stated")


# --------------------------------------------------------------------------------------
# the install profile
# --------------------------------------------------------------------------------------

class TestInstallProfile(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_the_install_root_and_spt_version_are_quoted(self) -> None:
        self.assertIn(INSTALL_ROOT, self.text)
        self.assertIn("3.10.5", self.text)
        self.assertIn("3.10.x", self.text)

    def test_the_mod_counts_are_carried_from_the_user(self) -> None:
        self.assertIn("~47", self.text)
        self.assertIn("~79", self.text)

    def test_the_playstyle_is_recorded(self) -> None:
        for needle in ("alive raids", "gunplay", "looting", "light questing", "Softcore",
                       "16 GB"):
            self.assertIn(needle, self.text,
                          f"the catalog must record the playstyle: {needle}")


# --------------------------------------------------------------------------------------
# the core AI stack
# --------------------------------------------------------------------------------------

class TestCoreStack(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_all_eight_core_mods_are_named(self) -> None:
        for mod in CORE_STACK:
            self.assertIn(mod, self.text, f"the core stack is missing {mod}")

    def test_the_stack_table_names_each_mod_side(self) -> None:
        self.assertIn("| Mod | Side | Where it lives | What it does | Why it is here |",
                      self.text)
        self.assertIn("**server**", self.text)
        self.assertIn("| client |", self.text)

    def test_alp_is_expanded_once(self) -> None:
        self.assertIn("Algorithmic Level Progression", self.text)

    def test_the_dependency_mods_are_labelled_as_dependencies(self) -> None:
        self.assertIn("It is a **dependency**, not an option", self.text)
        self.assertIn("Hard dependency", self.text)


# --------------------------------------------------------------------------------------
# real paths only
# --------------------------------------------------------------------------------------

class TestRealPaths(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_the_key_install_paths_are_quoted(self) -> None:
        for path in REAL_PATHS:
            self.assertIn(path, self.text, f"the catalog must quote the real path {path}")

    def test_forward_slash_forms_of_upstream_paths_are_allowed(self) -> None:
        for path in FORWARD_SLASH_PATHS:
            self.assertIn(path, self.text, f"missing upstream path {path}")

    def test_every_backticked_path_is_one_this_skill_knows(self) -> None:
        """Every inline-code path on the page must be one this skill recognises.

        The scan is per line, so a fenced code block (whose ``` fence would otherwise pair
        with a later backtick) cannot swallow real paths into one token.
        """
        paths: "list[str]" = []
        for line in self.text.splitlines():
            for token in BACKTICKED_PATH_RE.findall(line):
                if "\\" in token or token.startswith(("user/", "BepInEx/", "SPT_Data/")):
                    paths.append(token)
        self.assertGreaterEqual(len(paths), 6, "the path scan found almost nothing")
        allowed = (tuple(REAL_PATHS) + tuple(FORWARD_SLASH_PATHS) + tuple(SKILL_PATHS)
                   + (INSTALL_ROOT,))
        for path in paths:
            self.assertTrue(
                any(path.startswith(known) or path.startswith(known.replace("\\", "/"))
                    for known in allowed),
                f"the catalog quotes a path this skill does not recognise: {path!r}",
            )


# --------------------------------------------------------------------------------------
# enumerating the real inventory
# --------------------------------------------------------------------------------------

class TestEnumeration(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_it_ships_powershell_that_reads_the_manifests(self) -> None:
        self.assertIn("```powershell", self.text)
        self.assertIn("Get-ChildItem", self.text)
        self.assertIn("package.json", self.text)
        self.assertIn("ConvertFrom-Json", self.text)

    def test_the_manifest_fields_it_reads_are_the_loaders_own(self) -> None:
        for field in ("sptVersion", "modDependencies", "loadAfter", "version", "name"):
            self.assertIn(field, self.text,
                          f"the enumeration must surface the manifest field {field}")

    def test_it_enumerates_the_client_plugins_too(self) -> None:
        self.assertIn("BepInEx\\plugins", self.text)
        self.assertIn("-Include *.dll", self.text)

    def test_it_checks_the_two_silent_folders(self) -> None:
        for needle in ("BepInEx\\patchers", "BepInEx\\config", "*.cfg"):
            self.assertIn(needle, self.text, f"the enumeration must cover {needle}")

    def test_dumps_go_to_the_ignored_data_folder(self) -> None:
        self.assertIn("data\\inventory-YYYYMMDD.txt", self.text)
        self.assertIn("gitignored", self.text)

    def test_the_counts_are_meant_to_be_reconciled(self) -> None:
        self.assertIn("## The counts to reconcile", self.text)
        self.assertIn("~47 server mods", self.text)
        self.assertIn("~79 client plugins", self.text)


# --------------------------------------------------------------------------------------
# friction pairs
# --------------------------------------------------------------------------------------

class TestFrictionPairs(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        self_text = read(DOC)
        cls.flat = squashed(self_text)

    def test_ai_limit_is_called_incompatible_with_questing_bots(self) -> None:
        self.assertIn("AI Limit", self.flat)
        self.assertIn("incompatible", self.flat)

    def test_only_one_progression_mod(self) -> None:
        self.assertIn("Two bot-progression mods", self.flat)
        self.assertIn("keep exactly one", self.flat)

    def test_only_one_spawn_manager(self) -> None:
        self.assertIn("Two spawn managers", self.flat)

    def test_svm_spawn_settings_lose_to_the_spawn_mod(self) -> None:
        self.assertIn("SVM spawn settings", self.flat)
        self.assertIn("overridden", self.flat)

    def test_old_presets_are_tied_to_the_locations_hang(self) -> None:
        self.assertIn("/client/locations", self.flat)
        self.assertIn("troubleshooting.md", self.flat)


# --------------------------------------------------------------------------------------
# structure and cross-references
# --------------------------------------------------------------------------------------

class TestStructureAndCrossReferences(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.skill = read(SKILL_MD)

    def test_required_sections_exist(self) -> None:
        for heading in ("# Mod catalog", "## Grounding", "## Provenance",
                        "## Tier A", "## Tier B", "## Tier C",
                        "## Filling in the worksheet", "## Known-friction pairs",
                        "## Related pages", "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_page_named_exists(self) -> None:
        for page in SIBLING_PAGES:
            self.assertIn(page, self.text, f"the catalog should point at {page}")
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_inventory_questions_here(self) -> None:
        self.assertIn("references/mod-catalog.md", self.skill)
        self.assertIn("mod-catalog.md", self.skill)

    def test_skill_md_states_the_install_profile_this_page_uses(self) -> None:
        for needle in (INSTALL_ROOT, "3.10.5", "~47", "~79"):
            self.assertIn(needle, self.skill,
                          f"SKILL.md must record the install profile: {needle}")


# --------------------------------------------------------------------------------------
# SKILL.md conformance (the linter's rules, asserted from the skill's own suite)
# --------------------------------------------------------------------------------------

class TestSkillMdConformance(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = read(SKILL_MD)

    def test_frontmatter_carries_every_required_key(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        for key in ("name: tarkov-spt-companion", "description:", "version:", "license:",
                    "platforms:", "category: gaming"):
            self.assertIn(key, frontmatter, f"frontmatter is missing {key}")
        match = re.search(r"^version:\s*(\d+\.\d+\.\d+)$", frontmatter, re.MULTILINE)
        self.assertIsNotNone(match, "version must be X.Y.Z")
        self.assertEqual(match.group(1), "1.0.0")

    def test_the_description_stays_under_the_listing_limit(self) -> None:
        match = re.search(r"^description:\s*(.+)$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertLessEqual(len(match.group(1).strip()), 60)

    def test_the_hard_rules_are_present(self) -> None:
        for needle in ("sp-mod.com", "server-side only", "user\\mods",
                       "Never extract an archive over an existing install",
                       "Never invent a mod version", "Factory first"):
            self.assertIn(needle, self.skill, f"SKILL.md must state the rule: {needle}")

    def test_the_dead_domain_is_banned_in_skill_md_too(self) -> None:
        self.assertNotIn("forge.sp-tarkov", self.skill.lower())

    def test_every_reference_page_is_indexed(self) -> None:
        for page in SIBLING_PAGES + ("mod-catalog.md",):
            self.assertIn(f"references/{page}", self.skill,
                          f"SKILL.md must index references/{page}")
            self.assertTrue((REFERENCES / page).is_file())

    def test_the_completion_checklist_exists(self) -> None:
        self.assertIn("## Completion Checklist", self.skill)
        checklist = self.skill.split("## Completion Checklist")[-1]
        for needle in ("verify in-game", "no new client DLL", "FPS number"):
            self.assertIn(needle, checklist, f"the checklist must mention {needle}")


# --------------------------------------------------------------------------------------
# offline guarantee
# --------------------------------------------------------------------------------------

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

    def test_the_guide_tells_a_session_to_read_not_fetch(self) -> None:
        text = read(DOC)
        for statement in ("git clone", "curl ", "Invoke-WebRequest"):
            self.assertNotIn(statement, text,
                             f"the guide should not tell a session to run {statement!r}")


if __name__ == "__main__":
    unittest.main()
