#!/usr/bin/env python3
"""Offline contract for ``references/crash-troubleshooting.md`` ("why did ATM10 die?").

Stdlib-only and network-free: the page is a snapshot of pack 8.2's shipped config plus
one field report, so these cases freeze that data as constants and assert the doc still
carries it — never the ~150 MB pack clone, and never the network.

Covered:

  * grounding: the page exists, is not a stub, names the commit and date it was read
    from, separates itself from ``lag-fix-guide.md``, and says a log without a stack
    trace cannot name a culprit;
  * verified pack values: the memory table from ``config/memorysettings.json``, Crash
    Assistant's log settings and help link from ``config/crash_assistant/config.toml``,
    the 8.2 jar/id counts from ``modlist.json``;
  * the Windows exit-code table, including every code the field report could plausibly
    show, with ``0xC0000409`` marked as "no Java stack trace";
  * the two verified 8.0 → 8.1 → 8.2 mod moves quoted in the page, and the
    Distant-Horizons-is-not-in-the-pack claim;
  * the "traps" section: MineColonies' config spam and the two CC:Tweaked jars are named
    as non-fatal, not as the culprit;
  * no-fiction guards: no username, UUID, access token, or launcher-specific path from
    the field report leaks into the public doc, and every URL is on the allowlist;
  * SKILL.md wiring: the page is linked, the version is bumped to 1.6.0, "When to Use"
    routes crashes to it, and "When Not to Use" no longer disclaims all installation
    troubleshooting;
  * offline guarantee: this suite imports no network module.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
GUIDE_MD = SKILL_ROOT / "references" / "crash-troubleshooting.md"

PACK_COMMIT = "e5e3d1d83e"
PACK_DATE = "2026-09-22"
SKILL_VERSION = "1.6.0"

# --------------------------------------------------------------------------------------
# verified data — read from AllTheMods/ATM-10 at main e5e3d1d83e (pack 8.2)
# --------------------------------------------------------------------------------------

# config/memorysettings.json
MEMORY_VALUES = (
    "`minimumClient`", "`6000`",
    "`maximumClient`", "`32000`",
    "`16000:8000`", "`32000:12000`", "`48000:12000`", "`64000:12000`",
)

# config/crash_assistant/config.toml
CRASH_ASSISTANT_VALUES = (
    "generate_own_launcher_log = true",
    "logs/stderr_stream.log",
    "logs/crash_assistant/",
    "https://discord.gg/allthemods",
)

# config/crash_assistant/modlist.json
MODLIST_JARS = "497"
MODLIST_IDS = "493"

# The exit codes the page must explain, with the name Windows gives them.
EXIT_CODES = (
    ("0", None, None),
    ("1", None, None),
    ("-1073741819", "0xC0000005", "STATUS_ACCESS_VIOLATION"),
    ("-1073740791", "0xC0000409", "STATUS_STACK_BUFFER_OVERRUN"),
    ("-1073741571", "0xC00000FD", "STATUS_STACK_OVERFLOW"),
    ("-1073740940", "0xC0000374", "STATUS_HEAP_CORRUPTION"),
)

# changelogs/CHANGELOG-ATM10-8.0-8.1.md and ...-8.1-8.2.md
CHANGELOG_QUOTES = (
    "Sodium (0.8.13-beta.2+mc1.21.1) -> (0.8.13+mc1.21.1)",
    "FancyMenu (3.9.9) -> (3.9.12)",
    "1.1.1374-1.21.1-snapshot",
    "1.1.1396-1.21.1-snapshot",
    "iris-neoforge-1.8.14-beta.1+mc1.21.1.jar",
)

ALLOWED_URL_PREFIXES = (
    "https://github.com/AllTheMods/ATM-10",
    "https://discord.gg/allthemods",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def flatten(text: str) -> str:
    """Collapse markdown wrapping so assertions survive re-flowing."""
    return re.sub(r"\s+", " ", text)


def section(text: str, heading_prefix: str) -> str:
    """Return the body of the first ``## `` section whose heading starts with prefix."""
    lines = text.splitlines()
    out: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip().startswith(heading_prefix)
            continue
        if inside:
            out.append(line)
    return "\n".join(out)


class TestCrashTroubleshootingGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = read(GUIDE_MD)
        cls.flat = flatten(cls.text)
        cls.skill = read(SKILL_MD)

    # -- grounding ---------------------------------------------------------------------

    def test_the_page_exists_and_is_not_a_stub(self) -> None:
        self.assertTrue(GUIDE_MD.is_file())
        self.assertGreaterEqual(len(self.text.splitlines()), 150)
        self.assertIn(PACK_COMMIT, self.text)
        self.assertIn(PACK_DATE, self.text)
        self.assertIn("pack **8.2**", self.text)

    def test_it_is_the_crash_page_not_the_lag_page(self) -> None:
        self.assertIn("references/lag-fix-guide.md", self.text)
        self.assertIn("does not run at all", self.flat)
        self.assertIn("A crash with no stack trace does not have a culprit yet", self.flat)

    def test_it_never_names_a_mod_as_the_cause_from_the_field_report(self) -> None:
        # The field log has no stack trace, so the page must not claim one mod did it.
        for phrase in ("is the crash", "caused the crash", "the culprit is",
                       "blame the mod", "definitely the cause"):
            self.assertNotIn(phrase, self.flat)
        self.assertIn("not the abort", self.flat)

    # -- verified pack data ------------------------------------------------------------

    def test_memory_table_matches_the_shipped_config(self) -> None:
        for needle in MEMORY_VALUES:
            self.assertIn(needle, self.text)
        self.assertIn("config/memorysettings.json", self.text)
        self.assertIn("-Xms8G -Xmx8G", self.text)
        self.assertIn("**8 GB**", self.flat)

    def test_crash_assistant_paths_and_help_link_match_the_shipped_config(self) -> None:
        for needle in CRASH_ASSISTANT_VALUES:
            self.assertIn(needle, self.text)
        self.assertIn("config/crash_assistant/config.toml", self.text)

    def test_modlist_counts_match_the_8_2_snapshot(self) -> None:
        self.assertIn(MODLIST_JARS, self.text)
        self.assertIn(MODLIST_IDS, self.text)
        self.assertIn("config/crash_assistant/modlist.json", self.text)

    def test_changelog_quotes_are_exact(self) -> None:
        for quote in CHANGELOG_QUOTES:
            self.assertIn(quote, self.text)
        self.assertIn("CHANGELOG-ATM10-8.0-8.1.md", self.text)
        self.assertIn("CHANGELOG-ATM10-8.1-8.2.md", self.text)

    def test_distant_horizons_is_marked_as_not_shipped(self) -> None:
        self.assertIn("Distant Horizons", self.text)
        self.assertIn("**not in the pack.**", self.text)
        self.assertIn("no `distant` string", self.text)

    # -- exit codes --------------------------------------------------------------------

    def test_every_exit_code_is_explained_with_its_windows_name(self) -> None:
        for decimal, hex_code, name in EXIT_CODES:
            with self.subTest(code=decimal):
                self.assertIn(f"`{decimal}`", self.text)
                if hex_code:
                    self.assertIn(f"`{hex_code}`", self.text)
                if name:
                    self.assertIn(name, self.text)

    def test_the_fail_fast_code_is_called_out_as_trace_free(self) -> None:
        self.assertIn("**No Java stack trace is written.**", self.text)
        self.assertIn("hs_err_pid*.log", self.text)
        self.assertIn("Problematic frame", self.text)

    # -- the traps in the field log ----------------------------------------------------

    def test_minecolonies_spam_is_called_a_survivable_bug(self) -> None:
        self.assertIn("Cannot get config value before config is loaded", self.text)
        self.assertIn("initRegisterEquipmentTiers", self.text)
        self.assertIn("survived", self.flat)

    def test_cc_tweaked_pair_is_not_blamed(self) -> None:
        self.assertIn("1.113.1", self.text)
        self.assertIn("1.120.0", self.text)
        self.assertIn("1.120.2", self.text)
        self.assertIn("Do not delete a jar on this evidence alone", self.flat)

    def test_cosmetic_errors_are_labeled_cosmetic(self) -> None:
        for needle in ("mysticalagriculture", "accesstransformer.cfg",
                       "formations:template_editor", "Cosmetic"):
            self.assertIn(needle, self.text)

    # -- privacy and link hygiene ------------------------------------------------------

    def test_no_field_report_identity_leaks(self) -> None:
        lowered = self.text.lower()
        for leak in ("naddeer", "34dbf481", "accesstoken", "--username", "--uuid",
                     "c:\\users\\"):
            self.assertNotIn(leak, lowered)

    def test_every_url_is_on_the_allowlist(self) -> None:
        urls = set(re.findall(r"https?://[^\s)\]>]+", self.text))
        self.assertTrue(urls, "the page must link its provenance")
        for url in urls:
            with self.subTest(url=url):
                self.assertTrue(url.startswith(ALLOWED_URL_PREFIXES),
                                f"unverified URL in the guide: {url}")

    def test_no_network_imports(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        for module in ("requests", "urllib.request", "http.client", "socket"):
            self.assertNotIn(f"import {module}", source)

    # -- SKILL.md wiring ---------------------------------------------------------------

    def test_skill_links_the_page_and_bumps_the_version(self) -> None:
        self.assertIn("references/crash-troubleshooting.md", self.skill)
        match = re.search(r"^version:\s*(\S+)\s*$", self.skill, re.MULTILINE)
        self.assertIsNotNone(match, "SKILL.md frontmatter has no version")
        assert match is not None
        self.assertEqual(match.group(1), SKILL_VERSION)

    def test_when_to_use_routes_crashes_to_the_page(self) -> None:
        body = flatten(section(self.skill, "When to Use")).lower()
        self.assertIn("crash", body)
        self.assertIn("references/crash-troubleshooting.md", body)
        for symptom in ("won't start", "exit code", "latest.log"):
            self.assertIn(symptom, body)

    def test_when_not_to_use_no_longer_disclaims_installation_troubleshooting(self) -> None:
        body = flatten(section(self.skill, "When Not to Use")).lower()
        self.assertNotIn("beyond the setup notes", body)
        self.assertIn("crash-troubleshooting", body)

    def test_research_grounding_dates_the_page(self) -> None:
        body = flatten(section(self.skill, "Research Grounding"))
        self.assertIn("crash-troubleshooting.md", body)
        self.assertIn("8.2", body)
        self.assertIn("2026-09-22", body)

    def test_completion_checklist_has_a_crash_item(self) -> None:
        body = flatten(section(self.skill, "Completion Checklist")).lower()
        self.assertIn("crash-troubleshooting.md", body)
        self.assertIn("hs_err", body)


if __name__ == "__main__":
    unittest.main()
