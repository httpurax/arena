#!/usr/bin/env python3
"""Offline tests for the test-engineering plan contract.

The skill's verifier is intentionally stdlib-only and only reads a local JSON file. These tests
exercise its documented rules with an independent valid fixture plus deliberately malformed
plans, mirroring the contract-focused coverage used by the study-flashcards skill. No test
requires a service, credentials, a fixed filesystem location, or a network connection.
"""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
EXAMPLE_PLAN = SKILL_ROOT / "examples" / "test-plan.json"
VERIFIER_PATH = SKILL_ROOT / "scripts" / "verify_test_plan.py"

_spec = importlib.util.spec_from_file_location("verify_test_plan", VERIFIER_PATH)
assert _spec is not None and _spec.loader is not None
verifier = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verifier)


def valid_plan() -> dict[str, object]:
    """Return a fresh valid plan covering every supported part of the contract."""
    return {
        "goal": "Keep local invoice imports correct and deterministic.",
        "risks": [
            {
                "id": "rounding",
                "behavior": "A fractional value follows the currency rounding rule.",
                "impact": "high",
                "likelihood": "medium",
            },
            {
                "id": "bad-input",
                "behavior": "An invalid amount receives a domain error.",
                "impact": "medium",
                "likelihood": "low",
            },
        ],
        "fixtures": [
            {"id": "invoice-factory", "kind": "factory", "isolation": "per_test"},
            {"id": "workspace", "kind": "tempdir", "isolation": "cleanup"},
        ],
        "tests": [
            {
                "id": "unit-rounding",
                "layer": "unit",
                "behavior": "The rounding rule returns the documented amount.",
                "risks": ["rounding"],
                "fixtures": ["invoice-factory"],
            },
            {
                "id": "integration-rejection",
                "layer": "integration",
                "behavior": "A local input file surfaces an invalid amount as a domain error.",
                "risks": ["bad-input"],
                "fixtures": ["invoice-factory", "workspace"],
            },
            {
                "id": "e2e-receipt",
                "layer": "e2e",
                "behavior": "The local command produces a receipt for a valid invoice.",
                "risks": ["rounding"],
                "fixtures": ["invoice-factory", "workspace"],
            },
        ],
        "mock_boundaries": [
            {
                "dependency": "payment provider",
                "decision": "mock",
                "reason": "Units must not contact a remote payment provider.",
            },
            {
                "dependency": "local filesystem",
                "decision": "real",
                "reason": "The integration test verifies local file behavior.",
            },
        ],
        "flaky_policy": {
            "diagnose": [
                "Record the seed and attempt output.",
                "Vary ordering and timing one factor at a time.",
            ],
            "quarantine": {
                "owner": "quality-team",
                "tracking": "TEST-42",
                "expires": "2028-01-31",
            },
        },
    }


class TestPlanVerifierTests(unittest.TestCase):
    def test_bundled_example_is_valid(self) -> None:
        self.assertTrue(EXAMPLE_PLAN.is_file())
        self.assertEqual([], verifier.verify(EXAMPLE_PLAN))

    def test_all_supported_layers_can_be_used(self) -> None:
        self.assertEqual([], verifier.plan_errors(valid_plan()))

    def test_a_plan_does_not_need_an_artificial_e2e_layer(self) -> None:
        plan = valid_plan()
        plan["tests"] = [
            {
                "id": "unit-rounding",
                "layer": "unit",
                "behavior": "The rounding rule returns the documented amount.",
                "risks": ["rounding"],
                "fixtures": ["invoice-factory"],
            },
            {
                "id": "unit-rejection",
                "layer": "unit",
                "behavior": "The domain rule rejects invalid input.",
                "risks": ["bad-input"],
                "fixtures": ["invoice-factory"],
            },
        ]
        self.assertEqual([], verifier.plan_errors(plan))

    def test_risks_must_be_known_and_covered(self) -> None:
        plan = valid_plan()
        plan["tests"][0]["risks"] = ["unknown-risk"]
        plan["tests"][2]["risks"] = ["bad-input"]
        errors = verifier.plan_errors(plan)
        self.assertIn("tests[0].risks references unknown risk 'unknown-risk'", errors)
        self.assertIn("risk 'rounding' is not covered by any test", errors)

    def test_tests_require_unique_ids_known_fixtures_and_valid_layers(self) -> None:
        plan = valid_plan()
        plan["tests"][1]["id"] = "unit-rounding"
        plan["tests"][1]["layer"] = "smoke"
        plan["tests"][1]["fixtures"] = ["not-a-fixture"]
        errors = verifier.plan_errors(plan)
        self.assertIn("tests[1].id duplicates 'unit-rounding'", errors)
        self.assertIn("tests[1].layer must be one of: e2e, integration, unit", errors)
        self.assertIn("tests[1].fixtures references unknown fixture 'not-a-fixture'", errors)

    def test_fixture_contract_rejects_duplicate_and_nonisolated_data(self) -> None:
        plan = valid_plan()
        plan["fixtures"][1]["id"] = "invoice-factory"
        plan["fixtures"][1]["kind"] = "remote-service"
        plan["fixtures"][1]["isolation"] = "shared"
        errors = verifier.plan_errors(plan)
        self.assertIn("fixtures[1].id duplicates 'invoice-factory'", errors)
        self.assertIn("fixtures[1].kind must be one of: factory, in_memory, local_file, tempdir", errors)
        self.assertIn("fixtures[1].isolation must be one of: cleanup, copy_on_write, per_test", errors)

    def test_mock_boundaries_require_a_reason_and_a_decision(self) -> None:
        plan = valid_plan()
        plan["mock_boundaries"][0]["decision"] = "sometimes"
        plan["mock_boundaries"][0]["reason"] = " "
        errors = verifier.plan_errors(plan)
        self.assertIn("mock_boundaries[0].decision must be one of: mock, real", errors)
        self.assertIn("mock_boundaries[0].reason must be non-empty text", errors)

    def test_flaky_policy_requires_diagnosis_owner_tracking_and_an_iso_expiry(self) -> None:
        plan = valid_plan()
        plan["flaky_policy"]["diagnose"] = []
        plan["flaky_policy"]["quarantine"] = {
            "owner": "",
            "tracking": "",
            "expires": "next release",
        }
        errors = verifier.plan_errors(plan)
        self.assertIn("flaky_policy.diagnose must contain at least 1 item(s)", errors)
        self.assertIn("flaky_policy.quarantine.owner must be non-empty text", errors)
        self.assertIn("flaky_policy.quarantine.tracking must be non-empty text", errors)
        self.assertIn(
            "flaky_policy.quarantine.expires must be an ISO date (YYYY-MM-DD)", errors
        )

    def test_verifier_handles_invalid_json_without_network_or_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            plan_path = Path(temporary_directory) / "broken.json"
            plan_path.write_text("{not JSON", encoding="utf-8")
            errors = verifier.verify(plan_path)
        self.assertTrue(errors)
        self.assertIn("invalid JSON at line 1", errors[0])

    def test_command_reports_pass_and_failure_for_relative_local_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            good_path = root / "good.json"
            good_path.write_text(json.dumps(valid_plan()), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = verifier.main([str(good_path)])
            self.assertEqual(0, result)
            self.assertIn(f"PASS  {good_path}", output.getvalue())

            bad_path = root / "bad.json"
            bad_plan = copy.deepcopy(valid_plan())
            bad_plan["goal"] = ""
            bad_path.write_text(json.dumps(bad_plan), encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = verifier.main([str(bad_path)])
            self.assertEqual(1, result)
            self.assertIn("plan.goal must be non-empty text", output.getvalue())


class SkillDocumentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = SKILL_MD.read_text(encoding="utf-8")

    def test_frontmatter_is_portable_and_has_the_requested_identity(self) -> None:
        self.assertIn("name: test-engineering", self.skill_text)
        self.assertIn("version: 1.0.0", self.skill_text)
        self.assertIn("platforms: [linux, macos, windows]", self.skill_text)
        self.assertIn("category: development", self.skill_text)
        description = next(
            line.split(":", 1)[1].strip()
            for line in self.skill_text.splitlines()
            if line.startswith("description:")
        )
        self.assertLess(len(description), 60)
        self.assertNotIn("/home/", self.skill_text)
        self.assertNotIn("C:\\", self.skill_text)

    def test_required_engineering_guidance_and_local_unittest_fixture_are_present(self) -> None:
        for heading in (
            "### 1. State the observable contract and risks",
            "### 2. Choose layers deliberately",
            "### 3. Make test data local, readable, and isolated",
            "### 4. Mock at boundaries, not at seams inside your own design",
            "### 5. Diagnose, quarantine, and fix flakes",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.skill_text)
        self.assertIn("tempfile.TemporaryDirectory()", self.skill_text)
        self.assertIn("self.addCleanup", self.skill_text)
        self.assertIn("create_autospec", self.skill_text)
        self.assertIn("unbounded retries", self.skill_text)


if __name__ == "__main__":
    unittest.main()
