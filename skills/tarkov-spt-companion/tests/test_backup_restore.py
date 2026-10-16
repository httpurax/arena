#!/usr/bin/env python3
"""Offline tests for ``references/backup-restore.md``.

Stdlib-only and network-free: every check reads files shipped with the skill. The user's
rule is "never extract over an existing install", and this page is where that rule lives, so
the tests hold it to: real paths, a staged-restore workflow, and a restore that never
destroys the thing it is replacing before the new one is proven.

Covered:

  * grounding: exists, not a stub, the tags, no invented versions, no dead domain;
  * the one rule: never extract over a working install, with the reason (merging leaves
    stale files behind) and the mod authors' own "delete first" notes as evidence;
  * the backup table: profiles, mod folders, configs, plugins, patchers, ``.cfg`` files,
    SVM presets, and an explicit list of what is *not* worth backing up;
  * three tiers: profile-only, full snapshot with a ``mod-versions.txt`` manifest, and a
    whole-install copy for the irreversible cases;
  * rotation: a labelled known-good snapshot plus the recent ones;
  * restore: profile restore that renames rather than deletes, the mod-set-changed trap and
    the two ``core.json`` switches, and a single-mod restore that replaces rather than
    merges;
  * the post-restore verification checklist;
  * cross-references and the offline guarantee.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
REFERENCES = SKILL_ROOT / "references"
DOC = REFERENCES / "backup-restore.md"

INSTALL_ROOT = "C:\\games\\SPT-TARKOV-3105-COOP-LAN"

# Everything worth backing up, with the path this page must quote.
BACKUP_PATHS = (
    "user\\profiles\\*.json",
    "user\\mods\\",
    "SPT_Data\\Server\\configs\\",
    "BepInEx\\plugins\\",
    "BepInEx\\patchers\\",
    "BepInEx\\config\\",
    "SPT_Data\\Server\\database\\",
    "user\\mods\\[SVM] ServerValueModifier\\Presets\\",
)

# Generated folders that rebuild themselves -- the page must say not to bother.
NOT_WORTH_BACKING_UP = ("BepInEx\\cache", "BepInEx\\interop")

# The two core.json switches for rescuing a profile whose mods are gone.
CORE_JSON_SWITCHES = ("removeModItemsFromProfile", "removeInvalidTradersFromProfile")

# The nine server config files, as server-config.md lists them.
SERVER_CONFIG_FILES = ("core.json", "http.json", "gameplay.json", "inraid.json",
                       "insurance.json", "location.json", "ragfair.json", "trader.json",
                       "weather.json")

VERSION_RE = re.compile(r"(?<![\d.])(\d+\.\d+\.\d+)(?![\d.])")
URL_RE = re.compile(r"https?://[^\s)`\]|>]+")

VERIFIED_VERSIONS = {"3.10.5": "the user's SPT version"}

SIBLINGS_NAMED = ("troubleshooting.md", "mod-install-workflow.md", "server-config.md")


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


class TestTheOneRule(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_the_rule_is_a_heading_and_a_sentence(self) -> None:
        self.assertIn("## The one rule: never extract over an existing install", self.text)
        self.assertIn("merges", self.flat)

    def test_the_reason_is_stale_files(self) -> None:
        self.assertIn("stale files", self.flat)
        self.assertIn("TypeError: Cannot read properties of undefined", self.flat)

    def test_mod_authors_own_delete_first_notes_are_the_evidence(self) -> None:
        self.assertIn("uninstall and delete all its files first", self.flat)
        self.assertIn("delete the target config folder", self.flat)

    def test_the_six_step_sequence_is_given(self) -> None:
        for step in ("Stop the server and close the game", "**Delete or rename the target folder**",
                     "staging folder", "**Copy** the staged files in", "Factory"):
            self.assertIn(step, self.flat, f"missing install step {step!r}")


class TestWhatToBackUp(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_every_path_worth_backing_up_is_quoted(self) -> None:
        for path in BACKUP_PATHS:
            self.assertIn(path, self.text, f"the backup table must quote {path}")

    def test_the_nine_server_config_files_are_listed(self) -> None:
        for name in SERVER_CONFIG_FILES:
            self.assertIn(name, self.text, f"the backup table must name {name}")

    def test_generated_folders_are_excluded(self) -> None:
        self.assertIn("**Not worth backing up:**", self.text)
        for folder in NOT_WORTH_BACKING_UP:
            self.assertIn(folder, self.text, f"the page must exclude {folder}")

    def test_profiles_are_called_the_only_irreplaceable_thing(self) -> None:
        self.assertIn("user\\profiles", self.text)
        self.assertIn("nothing else on this list is irreplaceable", self.flat)

    def test_svm_loader_json_is_named(self) -> None:
        self.assertIn("loader.json", self.text)


class TestTiers(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_tier_one_is_profile_only_and_is_tied_to_every_change(self) -> None:
        self.assertIn("### Tier 1", self.text)
        self.assertIn("Run this before **every** mod change", self.flat)

    def test_tier_two_snapshots_the_manifest_versions(self) -> None:
        self.assertIn("### Tier 2", self.text)
        self.assertIn("mod-versions.txt", self.text)
        self.assertIn("package.json", self.text)
        self.assertIn("ConvertFrom-Json", self.text)

    def test_tier_three_is_reserved_for_the_irreversible(self) -> None:
        self.assertIn("### Tier 3", self.text)
        self.assertIn("something I cannot undo", self.flat)

    def test_every_tier_stops_the_server_first(self) -> None:
        self.assertIn("Stop the server and close the game", self.flat)


class TestRotation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)

    def test_a_labelled_known_good_snapshot_is_kept(self) -> None:
        self.assertIn("## Rotation", self.text)
        self.assertIn("KNOWN-GOOD", self.text)
        self.assertIn("never overwrite it", self.text)

    def test_the_recent_snapshots_are_bounded(self) -> None:
        self.assertIn("3 most recent", self.text)

    def test_a_layout_is_shown(self) -> None:
        self.assertIn("D:\\SPT-backups\\", self.text)
        self.assertIn("profile-", self.text)


class TestRestore(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.flat = squashed(cls.text)

    def test_profile_restore_renames_before_it_deletes(self) -> None:
        self.assertIn("user\\profiles.broken", self.text)
        self.assertIn("do not delete it until the restore is confirmed working", self.flat)
        self.assertIn("Stop the server and close the game", self.flat)

    def test_the_mod_set_trap_is_named(self) -> None:
        self.assertIn("### The trap: restoring a profile under a changed mod set", self.text)
        self.assertIn("SPT_Data\\Server\\configs\\core.json", self.text)

    def test_both_core_json_switches_are_quoted(self) -> None:
        for switch in CORE_JSON_SWITCHES:
            self.assertIn(switch, self.text, f"the restore path must name {switch}")

    def test_the_preference_order_is_explicit(self) -> None:
        for line in ("**Best:** restore the mod set **and** the profile from the same snapshot",
                     "**Acceptable:** flip those two keys on",
                     "**Last resort:** restore an older profile"):
            self.assertIn(line, self.flat, f"missing restore option {line!r}")

    def test_mod_set_restore_never_merges(self) -> None:
        self.assertIn("Do not extract the backup archive over the install", self.flat)
        self.assertIn("user\\mods.old", self.text)
        self.assertIn("BepInEx\\plugins.old", self.text)

    def test_single_mod_restore_is_a_replace(self) -> None:
        self.assertIn("the operation is *replace*, never *merge*", self.flat)


class TestVerificationAndCrossReferences(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(DOC)
        cls.skill = read(SKILL_MD)

    def test_the_verification_checklist_is_shipped(self) -> None:
        self.assertIn("## After any restore", self.text)
        for item in ("Server console lists the expected number of mods",
                     "A Factory raid loads and finishes",
                     "The profile opens", "One bigger map loads",
                     "A **fresh backup** of the now-working state exists"):
            self.assertIn(item, self.text, f"the checklist must include {item!r}")

    def test_required_sections_exist(self) -> None:
        for heading in ("# Backup and restore", "## The one rule", "## Backup procedure",
                        "## Rotation", "## Restore", "## After any restore",
                        "## Related pages", "## Verify-in-game list"):
            self.assertIn(heading, self.text, f"missing section {heading!r}")

    def test_every_sibling_named_exists(self) -> None:
        for page in SIBLINGS_NAMED:
            self.assertIn(page, self.text)
            self.assertTrue((REFERENCES / page).is_file(), f"{page} does not exist")

    def test_skill_md_routes_backup_questions_here(self) -> None:
        self.assertIn("references/backup-restore.md", self.skill)
        self.assertIn("never extract", self.skill.lower())
        self.assertIn("Back up before you touch anything at all", self.skill)


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
