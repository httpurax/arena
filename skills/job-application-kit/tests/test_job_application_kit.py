"""Stdlib-only offline tests using fictional strings and temporary files only."""

import contextlib
import importlib.util
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "posting_keywords.py"
spec = importlib.util.spec_from_file_location("posting_keywords", SCRIPT)
keywords = importlib.util.module_from_spec(spec)
spec.loader.exec_module(keywords)


class SkillContractTests(unittest.TestCase):
    def setUp(self):
        self.doc = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    def test_exact_frontmatter_and_directory_name(self):
        expected = """---
name: job-application-kit
description: Tailor your CV and cover letter to each job posting.
version: 1.0.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: productivity
---
"""
        self.assertTrue(self.doc.startswith(expected))
        self.assertEqual(re.search(r"^name: (.+)$", self.doc, re.M)[1], SKILL.name)

    def test_examples_are_fictional_without_contact_markers(self):
        for name in ("base-cv.example.md", "posting.example.md"):
            with self.subTest(name=name):
                text = (SKILL / "examples" / name).read_text(encoding="utf-8")
                self.assertIn("fictional", text.lower())
                self.assertNotRegex(text, r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
                self.assertNotRegex(text, r"(?<!\w)\+?\d[\d ().-]{7,}\d(?!\w)")
                self.assertNotRegex(text, r"(?i)\b\d+\s+(?:[\w.-]+\s+){1,4}"
                                         r"(?:street|st|road|rd|avenue|ave|lane|ln|drive|dr|boulevard|blvd)\b")
                self.assertNotRegex(text, r"(?i)\bp\.?\s*o\.?\s+box\s+\d+")

    def test_honesty_and_user_only_answers(self):
        flat = " ".join(self.doc.split())
        for rule in (
            "Rephrase and select from the base CV only",
            "Never invent employers, job titles, dates, degrees, certificates, or skills",
            "say so plainly", "never bridge the gap with fiction",
            "Legal attestations, signatures, and anything only the user can answer",
            "never filled in", "The user reviews every tailored document",
            "Nothing is sent automatically", "review before sending",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, flat)

    def test_setup_outputs_and_privacy_documented(self):
        for fragment in (
            "First-run setup", "paste their base CV once", "data/base-cv.md",
            "output/<slug>-cv.md", "output/<slug>-cover-letter.md",
            "gitignored", "never committed", "posting_keywords.py", "--cv", "--top",
            "```bash", "```powershell",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.doc)

    def test_private_directories_ignored(self):
        rules = (SKILL / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("/data/", rules)
        self.assertIn("/output/", rules)
        self.assertFalse(any(line.startswith("!") for line in rules))


class RankingTests(unittest.TestCase):
    def test_fixed_ranking_missing_phrases_and_covered_terms(self):
        posting = "Customer support. Ticket triage. Ticket triage. React. The and with."
        cv = "CUSTOMER SUPPORT."
        self.assertEqual(keywords.missing_keywords(posting, cv), [
            ("ticket triage", 2), ("ticket", 2), ("triage", 2), ("react", 1),
        ])

    def test_trigrams_and_deterministic_ties(self):
        self.assertEqual(keywords.missing_keywords("Zebra. Alpha. Data quality review.", ""), [
            ("data quality review", 1), ("data quality", 1), ("quality review", 1),
            ("alpha", 1), ("data", 1), ("quality", 1), ("review", 1), ("zebra", 1),
        ])

    def test_frequency_precedes_phrase_length(self):
        self.assertEqual(keywords.missing_keywords("React. React. Data quality review.", "", 1),
                         [("react", 2)])

    def test_stopwords_and_punctuation_do_not_create_phrases(self):
        self.assertEqual(keywords.term_counts("React and CSS. Python\nHTML; JavaScript"),
                         {"react": 1, "css": 1, "python": 1, "html": 1, "javascript": 1})

    def test_covered_phrase_excluded_with_case_and_hyphens(self):
        self.assertEqual(keywords.missing_keywords("Ticket-triage", "TICKET TRIAGE"), [])

    def test_whole_tokens_not_substrings(self):
        self.assertEqual(keywords.missing_keywords("Java. React.", "JavaScript. Reactive."),
                         [("java", 1), ("react", 1)])

    def test_covered_words_can_form_a_new_phrase(self):
        self.assertEqual(keywords.missing_keywords("Data quality", "Data. Quality."),
                         [("data quality", 1)])

    def test_unicode_and_programming_language_tokens(self):
        self.assertEqual(keywords.missing_keywords("C++. C#. CAFÉ. Ｒｅａｃｔ.",
                                                   "c++. Cafe\u0301. React."), [("c#", 1)])

    def test_empty_stopword_only_and_numeric_inputs(self):
        for text in ("", "The and a with required team", "123 456"):
            self.assertEqual(keywords.missing_keywords(text, ""), [])

    def test_top_limits_results_and_rejects_nonpositive(self):
        self.assertEqual(keywords.missing_keywords("Beta. Alpha.", "", 1), [("alpha", 1)])
        for top in (0, -1):
            with self.assertRaises(ValueError):
                keywords.missing_keywords("Alpha", "", top)


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.posting = self.root / "posting with spaces.md"
        self.cv = self.root / "cv.md"
        self.posting.write_text("Ticket triage. Ticket triage. React.", encoding="utf-8")
        self.cv.write_text("React", encoding="utf-8")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                              cwd=self.root, capture_output=True, text=True, timeout=10)

    def assert_graceful_error(self, proc, message):
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn(message, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertEqual(proc.stdout, "")

    def test_cli_ranking_and_top_read_only(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        proc = self.run_cli(self.posting, "--cv", self.cv, "--top", "2")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "2\tticket triage\n2\tticket\n")
        self.assertEqual(proc.stderr, "")
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_missing_posting(self):
        self.assert_graceful_error(self.run_cli(self.root / "absent", "--cv", self.cv),
                                   "posting file not found")

    def test_missing_cv(self):
        self.assert_graceful_error(self.run_cli(self.posting, "--cv", self.root / "absent"),
                                   "CV file not found")

    def test_directory_instead_of_file(self):
        self.assert_graceful_error(self.run_cli(self.root, "--cv", self.cv),
                                   "cannot read posting file")

    def test_invalid_utf8_never_echoes_contents(self):
        self.cv.write_bytes(b"private-canary\xff")
        proc = self.run_cli(self.posting, "--cv", self.cv)
        self.assert_graceful_error(proc, "CV must be UTF-8")
        self.assertNotIn("private-canary", proc.stderr)

    def test_bom_and_no_missing_message(self):
        self.cv.write_text(self.posting.read_text(encoding="utf-8"), encoding="utf-8-sig")
        proc = self.run_cli(self.posting, "--cv", self.cv)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "No missing keywords found.\n")

    def test_invalid_top_and_missing_argument(self):
        for value in ("0", "-3", "two", "1.5"):
            with self.subTest(value=value):
                self.assert_graceful_error(
                    self.run_cli(self.posting, "--cv", self.cv, "--top", value),
                    "positive integer")
        self.assert_graceful_error(self.run_cli(), "required")

    def test_default_cv_is_skill_relative(self):
        self.assertEqual(keywords.DEFAULT_CV, SKILL / "data" / "base-cv.md")
        with patch.object(keywords, "read_input", return_value="React") as read:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(keywords.main([str(self.posting)]), 0)
        self.assertEqual(read.call_args_list[1].args, (str(keywords.DEFAULT_CV), "CV"))

    def test_tilde_expansion(self):
        with patch.dict(os.environ, {"HOME": str(self.root), "USERPROFILE": str(self.root)}):
            self.assertEqual(keywords.read_input("~/cv.md", "CV"), "React")

    def test_permission_error_is_concise(self):
        with patch.object(Path, "read_text", side_effect=PermissionError):
            with self.assertRaisesRegex(ValueError, "cannot read CV file"):
                keywords.read_input(str(self.cv), "CV")


if __name__ == "__main__":
    unittest.main()
