#!/usr/bin/env python3
"""Offline tests for ``references/troubleshooting.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. This page is
the one a session reaches for at 1 a.m. with a raid that will not start, so the tests hold
it to the four failure modes the user named -- the ``/client/locations`` hang, the
``TypeError: Cannot read properties of undefined`` family, the dual Donuts folder, and
config schema drift from old presets -- plus the isolation workflow that finds the culprit
among ~120 mods.

Covered:

  * grounding: exists, not a stub, the three tags, no invented versions, no dead domain;
  * evidence first: the server console is named as the place to look, with the client and
    Unity log paths alongside it;
  * failure 1: the ``/client/locations`` hang, its ranked causes, the TrueLive preset
    pattern, and a numbered response checklist;
  * failure 2: the TypeError, its three causes, and the regenerate-the-config fix;
  * failure 3: the dual Donuts folder, with the verified Donuts paths and a search command;
  * failure 4: schema drift, with the safe way to carry settings across an update;
  * the isolation workflow: backup first, bisect by halves (never one at a time), confirm,
    restore, and a worksheet;
  * a symptom to first-check table;
  * cross-references and the offline guarantee.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "troubleshooting.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

# Paths a session is told to open when something breaks.
EVIDENCE_PATHS = (
    "BepInEx\\LogOutput.log",
    "BepInEx\\config",
    "user\\mods",
    "SPT_Data\\Server\\configs",
    "AppData\\LocalLow\\Battlestate Games\\EscapeFromTarkov\\Player.log",
)

# The Donuts paths verified from Fika's headless-client docs and preset release notes.
DONUTS_PATHS = (
    "BepInEx\\plugins\\dvize.Donuts\\",
    "BepInEx\\plugins\\dvize.Donuts\\Config\\",
    "BepInEx\\plugins\\dvize.Donuts\\ScenarioConfig.json",
    "BepInEx\\config\\com.dvize.Donuts.cfg",
)

SWAG_PATHS = (
    "user\\mods\\SWAG\\config\\",
    "user\\mods\\SWAG\\config\\bosses\\",
    "user\\mods\\SWAG\\config\\bossConfig.json",
)

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")

VERIFIED_VERSIONS = {"3.10.5": "the user's SPT version"}

SIBLINGS_NAMED = ("load-order-guide.md", "performance-tuning.md", "backup-restore.md",
                  "mod-install-workflow.md", "server-config.md")


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
        self.assertGreater(len(self.text.splitlines()), 150)

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


class TestEvidenceFirst(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_server_console_is_the_first_place_to_look(self) -> None:
        self.assertIn("the **server console window**, not the game", self.flat)
        self.assertIn("first place to look", self.flat)

    def test_the_log_locations_are_quoted(self) -> None:
        for path in EVIDENCE_PATHS:
            self.assertIn(path, self.text, f"missing the evidence path {path}")

    def test_the_unknown_log_folder_is_flagged_not_guessed(self) -> None:
        self.assertIn("verify in-game", self.flat)
        self.assertIn("whether this install also drops a rolling server log", self.flat)


class TestLocationsHang(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_route_is_named_and_explained(self) -> None:
        self.assertIn("/client/locations", self.text)
        self.assertIn("## Failure 1", self.text)
        for phrase in ("client sits on a loading screen", "endless wait",
                       "server console"):
            self.assertIn(phrase, self.flat, f"missing the symptom detail {phrase!r}")

    def test_it_says_the_client_is_innocent(self) -> None:
        self.assertIn("The client is innocent", self.flat)

    def test_the_causes_are_ranked_in_a_table(self) -> None:
        self.assertIn("### What causes it, in the order to check", self.text)
        for cause in ("spawn preset that does not match", "Two spawn managers",
                      "sptVersion", "config schema mismatch"):
            self.assertIn(cause, self.flat, f"missing ranked cause {cause!r}")

    def test_the_swag_config_paths_are_quoted(self) -> None:
        for path in SWAG_PATHS:
            self.assertIn(path, self.text, f"missing the SWAG path {path}")

    def test_the_truelive_pattern_is_spelled_out(self) -> None:
        self.assertIn("TrueLive", self.text)
        self.assertIn("matsix", self.text)
        self.assertIn("preset pack", self.flat)
        self.assertIn("3.9", self.text, "the preset's target version must be named")
        self.assertIn("sandbox", self.text,
                      "the duplicated-map-name bug is the cautionary detail")

    def test_a_preset_is_called_a_code_change(self) -> None:
        self.assertIn("code change wearing a config's clothes", self.flat)

    def test_the_response_checklist_is_numbered_and_factory_first(self) -> None:
        self.assertIn("### First response checklist", self.text)
        for step in ("Read the **server console**", "Disable the **most recently changed**",
                     "Factory", "known-good backup"):
            self.assertIn(step, self.flat, f"missing checklist step {step!r}")


class TestTypeError(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_exact_error_string_is_quoted(self) -> None:
        self.assertIn("TypeError: Cannot read properties of undefined", self.text)

    def test_the_server_is_named_as_the_javascript_side(self) -> None:
        self.assertIn("Node/TypeScript", self.flat)

    def test_the_three_causes_are_given(self) -> None:
        for cause in ("config file missing a field", "A mod reading data another mod removed",
                      "A mod built for a different SPT version"):
            self.assertIn(cause, self.flat, f"missing TypeError cause {cause!r}")

    def test_the_three_step_fix_regenerates_the_config(self) -> None:
        self.assertIn("### The three-step fix", self.text)
        for step in ("Find the file", "Regenerate its config", "Re-apply edits one key"):
            self.assertIn(step, self.flat, f"missing fix step {step!r}")
        self.assertIn("writes a fresh default", self.flat)

    def test_it_says_to_capture_the_console_before_fixing(self) -> None:
        self.assertIn("Copy the whole console block", self.flat)


class TestDualDonutsFolder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_symptoms_are_listed(self) -> None:
        self.assertIn("## Failure 3", self.text)
        self.assertIn("do not stick", self.flat)
        self.assertIn("doubled", self.flat)

    def test_the_verified_donuts_paths_are_quoted(self) -> None:
        for path in DONUTS_PATHS:
            self.assertIn(path, self.text, f"missing the Donuts path {path}")

    def test_the_source_of_the_paths_is_stated(self) -> None:
        self.assertIn("Fika's headless-client documentation", self.flat)
        self.assertIn("preset-pack release notes", self.flat)

    def test_the_duplicate_folder_commit_is_cited_as_evidence(self) -> None:
        self.assertIn("Fix Duplicate Folders", self.flat,
                      "the commit name survives line-wrapping in the flattened text")
        self.assertIn("dvize/Donuts", self.text)

    def test_the_fix_moves_before_it_deletes(self) -> None:
        for step in ("Search the install for every Donuts directory", "**Move** the duplicates",
                     "Do not delete anything you have not backed up"):
            self.assertIn(step, self.flat, f"missing fix step {step!r}")
        self.assertIn("Get-ChildItem", self.text)
        self.assertIn("-Filter '*onuts*'", self.text)

    def test_it_verifies_you_are_editing_the_live_folder(self) -> None:
        self.assertIn("confirm it is still there after a reload", self.flat)


class TestSchemaDrift(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_failure_is_described_and_numbered(self) -> None:
        self.assertIn("## Failure 4", self.text)
        self.assertIn("config schema mismatch", self.flat)

    def test_the_six_step_carry_over_is_present(self) -> None:
        self.assertIn("### The safe way to carry settings across an update", self.text)
        for step in ("Back up the mod folder", "changelog", "Rename the old config",
                     "fresh default", "Re-apply your values by hand"):
            self.assertIn(step, self.flat, f"missing carry-over step {step!r}")

    def test_it_forbids_copying_the_old_file_back(self) -> None:
        self.assertIn("never by copying the old file back over it", self.flat)

    def test_a_preset_must_match_the_mod_major_version(self) -> None:
        self.assertIn("a preset must match the **major version**", self.flat)


class TestIsolationWorkflow(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_prerequisites_come_first(self) -> None:
        self.assertIn("### Before you start", self.text)
        self.assertIn("user\\profiles", self.text)
        self.assertIn("Stop the server and close the game", self.flat)

    def test_reproduce_on_factory(self) -> None:
        self.assertIn("### Step 1 — reproduce and capture", self.text)
        self.assertIn("Factory", self.text)

    def test_it_bisects_by_halves_not_one_at_a_time(self) -> None:
        self.assertIn("### Step 3 — bisect (do not disable one at a time)", self.text)
        self.assertIn("Disable **half**", self.flat)
        self.assertIn("6 rounds or fewer", self.flat)
        self.assertIn("testing one mod at a time is ~47 raids", self.flat)

    def test_confirmation_goes_both_ways(self) -> None:
        self.assertIn("### Step 4 — confirm and decide", self.text)
        self.assertIn("confirm the fault returns", self.flat)

    def test_the_install_is_put_back_and_a_backup_taken(self) -> None:
        self.assertIn("### Step 5 — put the install back", self.text)
        self.assertIn("known-good state", self.flat)

    def test_the_worksheet_is_shipped(self) -> None:
        self.assertIn("### The worksheet", self.text)
        for field in ("Symptom:", "Map used to test: Factory", "Culprit:", "Fix applied:"):
            self.assertIn(field, self.text, f"the worksheet must have {field!r}")


class TestSymptomTableAndCrossReferences(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)
        cls.skill = read(SKILL_MD)

    def test_the_quick_table_covers_the_named_symptoms(self) -> None:
        self.assertIn("## Symptom → first check", self.text)
        for symptom in ("Endless loading", "TypeError", "Donuts settings will not stick",
                        "Bosses never spawn", "Profile will not load"):
            self.assertIn(symptom, self.flat, f"the quick table must cover {symptom!r}")

    def test_required_sections_exist(self) -> None:
        for heading in ("# Troubleshooting", "## Log and evidence locations",
                        "## Failure 1", "## Failure 2", "## Failure 3", "## Failure 4",
                        "## The isolation workflow", "## Related pages",
                        "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_named_exists(self) -> None:
        for page in SIBLINGS_NAMED:
            self.assertIn(page, self.text)
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_broken_installs_here(self) -> None:
        self.assertIn("references/troubleshooting.md", self.skill)
        self.assertIn("/client/locations", self.skill)
        self.assertIn("TypeError: Cannot read properties of undefined", self.skill)
        self.assertIn("dual donuts", self.skill.lower())


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
