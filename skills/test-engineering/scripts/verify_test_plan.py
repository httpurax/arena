#!/usr/bin/env python3
"""Validate the local test-plan manifest used by the test-engineering skill.

The verifier deliberately checks a small JSON contract instead of running tests. It makes a
reviewable test strategy machine-checkable: risks must map to tests, tests to local fixtures,
listed mock boundaries need a decision, and every plan carries an owned, expiring flaky-test
policy. It only reads the supplied local JSON file and uses the Python standard library.

Usage:
    python scripts/verify_test_plan.py path/to/test-plan.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

IMPACT_LEVELS = frozenset({"low", "medium", "high"})
TEST_LAYERS = frozenset({"unit", "integration", "e2e"})
FIXTURE_KINDS = frozenset({"factory", "local_file", "tempdir", "in_memory"})
FIXTURE_ISOLATION = frozenset({"per_test", "copy_on_write", "cleanup"})
MOCK_DECISIONS = frozenset({"mock", "real"})


def nonempty_text(value: Any) -> bool:
    """Return whether value is a non-empty string after surrounding whitespace is removed."""
    return isinstance(value, str) and bool(value.strip())


def add_required_text(record: dict[str, Any], field: str, location: str, errors: list[str]) -> None:
    """Add an error unless record[field] is a meaningful text value."""
    if not nonempty_text(record.get(field)):
        errors.append(f"{location}.{field} must be non-empty text")


def add_text_list(
    record: dict[str, Any], field: str, location: str, errors: list[str], *, minimum: int = 1
) -> list[str]:
    """Validate and return a list of non-empty text values, retaining valid entries only."""
    value = record.get(field)
    if not isinstance(value, list):
        errors.append(f"{location}.{field} must be a list")
        return []
    if len(value) < minimum:
        errors.append(f"{location}.{field} must contain at least {minimum} item(s)")
    valid: list[str] = []
    for index, item in enumerate(value):
        if not nonempty_text(item):
            errors.append(f"{location}.{field}[{index}] must be non-empty text")
        else:
            valid.append(item.strip())
    return valid


def records(value: Any, name: str, errors: list[str], *, minimum: int = 0) -> list[dict[str, Any]]:
    """Return mapping records from a top-level list while reporting malformed entries."""
    if not isinstance(value, list):
        errors.append(f"{name} must be a list")
        return []
    if len(value) < minimum:
        errors.append(f"{name} must contain at least {minimum} item(s)")
    output: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{name}[{index}] must be an object")
        else:
            output.append(item)
    return output


def plan_errors(plan: Any) -> list[str]:
    """Return every violation of the documented local test-plan JSON contract.

    A valid plan has a goal, named risks, tests that cover those risks using named local
    fixtures, documented mock boundaries, and an owned flaky-test policy. The function is
    pure so the unittest suite can exercise it without subprocesses, files, or a network.
    """
    if not isinstance(plan, dict):
        return ["plan must be a JSON object"]

    errors: list[str] = []
    add_required_text(plan, "goal", "plan", errors)

    risk_records = records(plan.get("risks"), "risks", errors, minimum=1)
    risk_ids: set[str] = set()
    for index, risk in enumerate(risk_records):
        location = f"risks[{index}]"
        risk_id = risk.get("id")
        if not nonempty_text(risk_id):
            errors.append(f"{location}.id must be non-empty text")
        elif risk_id.strip() in risk_ids:
            errors.append(f"{location}.id duplicates {risk_id.strip()!r}")
        else:
            risk_ids.add(risk_id.strip())
        add_required_text(risk, "behavior", location, errors)
        for field in ("impact", "likelihood"):
            value = risk.get(field)
            if value not in IMPACT_LEVELS:
                choices = ", ".join(sorted(IMPACT_LEVELS))
                errors.append(f"{location}.{field} must be one of: {choices}")

    fixture_records = records(plan.get("fixtures"), "fixtures", errors, minimum=1)
    fixture_ids: set[str] = set()
    for index, fixture in enumerate(fixture_records):
        location = f"fixtures[{index}]"
        fixture_id = fixture.get("id")
        if not nonempty_text(fixture_id):
            errors.append(f"{location}.id must be non-empty text")
        elif fixture_id.strip() in fixture_ids:
            errors.append(f"{location}.id duplicates {fixture_id.strip()!r}")
        else:
            fixture_ids.add(fixture_id.strip())
        kind = fixture.get("kind")
        if kind not in FIXTURE_KINDS:
            choices = ", ".join(sorted(FIXTURE_KINDS))
            errors.append(f"{location}.kind must be one of: {choices}")
        isolation = fixture.get("isolation")
        if isolation not in FIXTURE_ISOLATION:
            choices = ", ".join(sorted(FIXTURE_ISOLATION))
            errors.append(f"{location}.isolation must be one of: {choices}")

    test_records = records(plan.get("tests"), "tests", errors, minimum=1)
    test_ids: set[str] = set()
    covered_risks: set[str] = set()
    for index, test in enumerate(test_records):
        location = f"tests[{index}]"
        test_id = test.get("id")
        if not nonempty_text(test_id):
            errors.append(f"{location}.id must be non-empty text")
        elif test_id.strip() in test_ids:
            errors.append(f"{location}.id duplicates {test_id.strip()!r}")
        else:
            test_ids.add(test_id.strip())
        layer = test.get("layer")
        if layer not in TEST_LAYERS:
            choices = ", ".join(sorted(TEST_LAYERS))
            errors.append(f"{location}.layer must be one of: {choices}")
        add_required_text(test, "behavior", location, errors)

        referenced_risks = add_text_list(test, "risks", location, errors)
        for risk_id in referenced_risks:
            if risk_id not in risk_ids:
                errors.append(f"{location}.risks references unknown risk {risk_id!r}")
            else:
                covered_risks.add(risk_id)

        referenced_fixtures = add_text_list(test, "fixtures", location, errors)
        for fixture_id in referenced_fixtures:
            if fixture_id not in fixture_ids:
                errors.append(f"{location}.fixtures references unknown fixture {fixture_id!r}")

    for risk_id in sorted(risk_ids - covered_risks):
        errors.append(f"risk {risk_id!r} is not covered by any test")

    boundary_records = records(plan.get("mock_boundaries"), "mock_boundaries", errors)
    dependencies: set[str] = set()
    for index, boundary in enumerate(boundary_records):
        location = f"mock_boundaries[{index}]"
        dependency = boundary.get("dependency")
        if not nonempty_text(dependency):
            errors.append(f"{location}.dependency must be non-empty text")
        elif dependency.strip() in dependencies:
            errors.append(f"{location}.dependency duplicates {dependency.strip()!r}")
        else:
            dependencies.add(dependency.strip())
        decision = boundary.get("decision")
        if decision not in MOCK_DECISIONS:
            choices = ", ".join(sorted(MOCK_DECISIONS))
            errors.append(f"{location}.decision must be one of: {choices}")
        add_required_text(boundary, "reason", location, errors)

    flaky = plan.get("flaky_policy")
    if not isinstance(flaky, dict):
        errors.append("flaky_policy must be an object")
        return errors
    add_text_list(flaky, "diagnose", "flaky_policy", errors)
    quarantine = flaky.get("quarantine")
    if not isinstance(quarantine, dict):
        errors.append("flaky_policy.quarantine must be an object")
        return errors
    for field in ("owner", "tracking", "expires"):
        add_required_text(quarantine, field, "flaky_policy.quarantine", errors)
    expiry = quarantine.get("expires")
    if nonempty_text(expiry):
        try:
            date.fromisoformat(expiry.strip())
        except ValueError:
            errors.append("flaky_policy.quarantine.expires must be an ISO date (YYYY-MM-DD)")

    return errors


def load_plan(path: Path) -> tuple[Optional[Any], list[str]]:
    """Read one local JSON plan and return either its value or safe, actionable errors."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [f"could not read plan: {exc}"]
    try:
        return json.loads(text), []
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]


def verify(path: Path) -> list[str]:
    """Load and validate path without writing files or talking to a service."""
    plan, errors = load_plan(path)
    if errors:
        return errors
    return plan_errors(plan)


def report(path: Path, errors: Iterable[str]) -> int:
    """Print a concise, path-based report and return its process-style status code."""
    problem_list = list(errors)
    if problem_list:
        print(f"FAIL  {path}")
        for problem in problem_list:
            print(f"  - {problem}")
        return 1
    print(f"PASS  {path}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the command-line verifier for exactly one local JSON manifest."""
    parser = argparse.ArgumentParser(
        prog="verify_test_plan.py",
        description="Validate a local test-engineering JSON plan without network access.",
    )
    parser.add_argument("plan", type=Path, help="path to a test-plan JSON file")
    args = parser.parse_args(argv)
    return report(args.plan, verify(args.plan))


if __name__ == "__main__":
    sys.exit(main())
