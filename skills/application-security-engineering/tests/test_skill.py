"""Stdlib-only tests for the application-security-engineering skill.

Covers offline-testable structure only — no network, no node:
- frontmatter name matches the directory
- every references/, profiles/, recipes/, templates/, checklists/ file
  named in SKILL.md exists on disk
- eval tasks 001–016 are all present with Setup/Expected/Failure sections
- templates/finding.md contains the finding-contract headings
- checklist files are non-empty
- both scripts are non-empty with correct shebangs
"""

from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_MD = SKILL_DIR / "SKILL.md"
README_MD = SKILL_DIR / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestFrontmatter(unittest.TestCase):
    """SKILL.md frontmatter basics."""

    def test_frontmatter_name_matches_directory(self):
        text = _read(SKILL_MD)
        m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(m, "no frontmatter found")
        fm = m.group(1)
        name_match = re.search(r"^name:\s*(.+)", fm, re.MULTILINE)
        self.assertIsNotNone(name_match, "no name in frontmatter")
        self.assertEqual(name_match.group(1).strip(),
                         SKILL_DIR.name)

    def test_required_keys_present(self):
        text = _read(SKILL_MD)
        m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(m)
        fm = m.group(1)
        for key in ("name", "description", "version", "author",
                     "license", "platforms", "metadata"):
            self.assertRegex(fm, rf"(?m)^{re.escape(key)}:",
                             f"missing key: {key}")

    def test_version_is_xyz(self):
        text = _read(SKILL_MD)
        m = re.search(r"^version:\s*(.+)", text, re.MULTILINE)
        self.assertIsNotNone(m)
        self.assertRegex(m.group(1).strip(), r"^\d+\.\d+\.\d+$")

    def test_description_under_60_chars(self):
        text = _read(SKILL_MD)
        m = re.search(r"^description:\s*(.+)", text, re.MULTILINE)
        self.assertIsNotNone(m)
        self.assertLessEqual(len(m.group(1).strip()), 60)

    def test_license_is_unlicensed(self):
        text = _read(SKILL_MD)
        m = re.search(r"^license:\s*(.+)", text, re.MULTILINE)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1).strip(), "UNLICENSED")


class TestReferencesExist(unittest.TestCase):
    """Every references/ file pointed to by SKILL.md exists on disk."""

    EXPECTED = [
        "references/api-security.md",
        "references/attack-surface-mapping.md",
        "references/authentication-authorization-session.md",
        "references/business-logic-and-race-conditions.md",
        "references/cryptography-secrets-and-data-protection.md",
        "references/error-handling-and-security-logging.md",
        "references/exceptional-conditions-and-resource-limits.md",
        "references/file-handling.md",
        "references/frontend-browser-security.md",
        "references/input-encoding-and-injection.md",
        "references/multi-tenancy-and-isolation.md",
        "references/remediation-and-regression.md",
        "references/scope-and-rules-of-engagement.md",
        "references/secure-code-review.md",
        "references/security-orchestration.md",
        "references/security-requirements-and-threat-modeling.md",
        "references/security-testing-and-validation.md",
        "references/ssrf-and-outbound-network.md",
        "references/standards-map.md",
        "references/supply-chain-and-dependencies.md",
        "references/vulnerability-reporting-and-severity.md",
    ]

    def test_all_references_exist(self):
        for rel in self.EXPECTED:
            path = SKILL_DIR / rel
            self.assertTrue(path.is_file(), f"missing: {rel}")


class TestProfilesExist(unittest.TestCase):
    """Every profiles/ file pointed to by SKILL.md exists on disk."""

    EXPECTED = [
        "profiles/api-service.md",
        "profiles/authentication-identity.md",
        "profiles/file-upload-processing.md",
        "profiles/high-impact-business-flow.md",
        "profiles/high-risk-internet-facing.md",
        "profiles/library-and-supply-chain.md",
        "profiles/multi-tenant-saas.md",
        "profiles/web-application.md",
        "profiles/white-box-repository.md",
    ]

    def test_all_profiles_exist(self):
        for rel in self.EXPECTED:
            path = SKILL_DIR / rel
            self.assertTrue(path.is_file(), f"missing: {rel}")


class TestRecipesExist(unittest.TestCase):
    """Every recipes/ file pointed to by SKILL.md exists on disk."""

    EXPECTED = [
        "recipes/access-control-review.md",
        "recipes/api-endpoint-review.md",
        "recipes/auth-flow-review.md",
        "recipes/business-logic-review.md",
        "recipes/dependency-review.md",
        "recipes/file-upload-review.md",
        "recipes/finding-validation.md",
        "recipes/outbound-request-review.md",
        "recipes/race-condition-review.md",
        "recipes/regression-test-from-finding.md",
        "recipes/security-code-review.md",
        "recipes/threat-model.md",
    ]

    def test_all_recipes_exist(self):
        for rel in self.EXPECTED:
            path = SKILL_DIR / rel
            self.assertTrue(path.is_file(), f"missing: {rel}")


class TestTemplatesExist(unittest.TestCase):
    """Every templates/ file pointed to by SKILL.md exists on disk."""

    EXPECTED = [
        "templates/asvs-tailoring.md",
        "templates/attack-surface-inventory.md",
        "templates/finding.md",
        "templates/security-review-plan.md",
        "templates/threat-model.md",
    ]

    def test_all_templates_exist(self):
        for rel in self.EXPECTED:
            path = SKILL_DIR / rel
            self.assertTrue(path.is_file(), f"missing: {rel}")


class TestChecklistsExist(unittest.TestCase):
    """Every checklists/ file pointed to by SKILL.md exists on disk."""

    EXPECTED = [
        "checklists/feature-security.md",
        "checklists/finding-report.md",
        "checklists/release-security.md",
        "checklists/secure-code-review.md",
        "checklists/security-review-definition-of-done.md",
    ]

    def test_all_checklists_exist(self):
        for rel in self.EXPECTED:
            path = SKILL_DIR / rel
            self.assertTrue(path.is_file(), f"missing: {rel}")


class TestEvalsPresent(unittest.TestCase):
    """Eval tasks 001–016 are all present with required sections."""

    def _eval_path(self, n: int) -> Path:
        return SKILL_DIR / "evals" / "tasks" / f"{n:03d}-*.md"

    def _find_eval(self, n: int) -> Path:
        matches = sorted((SKILL_DIR / "evals" / "tasks").glob(f"{n:03d}-*.md"))
        self.assertTrue(matches, f"eval {n:03d} not found")
        return matches[0]

    def test_all_16_evals_present(self):
        for n in range(1, 17):
            path = self._find_eval(n)
            self.assertTrue(path.is_file(), f"eval {n:03d} missing")

    def test_evals_have_required_sections(self):
        for n in range(1, 17):
            path = self._find_eval(n)
            text = _read(path)
            for section in ("Setup", "Expected", "Failure"):
                self.assertIn(f"## {section}", text,
                              f"eval {n:03d} missing ## {section}")


class TestFindingTemplate(unittest.TestCase):
    """templates/finding.md contains the finding-contract headings."""

    REQUIRED_HEADINGS = [
        "Title", "Severity", "Affected Component", "Preconditions",
        "Security Property Violated", "Evidence", "Expected Behavior",
        "Actual Behavior", "Demonstrated Impact", "Root Cause",
        "Standards Mapping", "Remediation", "Regression Test",
        "Fix Verification", "Notes / Residual Risk",
    ]

    def test_finding_template_has_contract_headings(self):
        text = _read(SKILL_DIR / "templates" / "finding.md")
        for heading in self.REQUIRED_HEADINGS:
            self.assertIn(f"## {heading}", text,
                          f"missing heading: ## {heading}")


class TestChecklistsNonEmpty(unittest.TestCase):
    """Every checklist file is non-empty."""

    def test_checklists_are_non_empty(self):
        for path in sorted((SKILL_DIR / "checklists").glob("*.md")):
            text = _read(path).strip()
            self.assertTrue(text, f"empty checklist: {path.name}")


class TestScripts(unittest.TestCase):
    """Both scripts are non-empty with correct shebangs."""

    def test_run_security_baseline_shebang(self):
        path = SKILL_DIR / "scripts" / "run-security-baseline"
        self.assertTrue(path.is_file(), "run-security-baseline missing")
        text = _read(path)
        self.assertTrue(text.strip(), "run-security-baseline is empty")
        self.assertTrue(text.startswith("#!/usr/bin/env bash"),
                        "run-security-baseline missing bash shebang")

    def test_security_project_audit_shebang(self):
        path = SKILL_DIR / "scripts" / "security-project-audit"
        self.assertTrue(path.is_file(), "security-project-audit missing")
        text = _read(path)
        self.assertTrue(text.strip(), "security-project-audit is empty")
        self.assertTrue(text.startswith("#!/usr/bin/env node"),
                        "security-project-audit missing node shebang")


if __name__ == "__main__":
    unittest.main(verbosity=2)