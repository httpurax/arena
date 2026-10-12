---
name: test-engineering
description: Plan robust tests beyond the red-green-refactor loop.
version: 1.0.0
author: Arena contributors
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: development
    tags: [testing, unittest, fixtures, test-strategy, reliability]
---

# Test Engineering

Use this skill to design and improve a test system, not just to make the next test pass. It
complements the built-in `test-driven-development` skill: TDD is an excellent implementation
loop for a small behavior, while this skill chooses the right behaviors, layers, data,
boundaries, and reliability controls for the whole change.

All examples use Python's standard-library `unittest` and local resources. Keep test work
portable: use relative project paths, temporary directories, and injected dependencies; do
not require credentials, an internet connection, or a live production service.

## When to Use

- A change crosses business logic, persistence, a CLI, a web handler, or another process and
  needs a deliberate unit/integration/end-to-end (E2E) split.
- Tests are slow, brittle, hard to understand, dependent on shared data, or intermittently
  fail in CI.
- A team needs reusable fixtures, representative data, or a documented mocking policy.
- A bug escaped despite existing tests and the test strategy needs to be repaired.
- A request asks what to test, not merely how to write one test.

## When Not to Use

- A tiny, isolated behavior already has a clear red-green-refactor path. Start with
  `test-driven-development` instead; return here if the change adds a boundary or systemic
  risk.
- The request is only to execute an existing suite or interpret one failure. Diagnose that
  failure first, then use this skill if it exposes a strategy or reliability gap.
- The user wants load, security, accessibility, or visual-regression testing as a specialty.
  Incorporate those risks in the strategy, but use the relevant specialist workflow for the
  detailed method.

## Core Workflow

### 1. State the observable contract and risks

Write a one-sentence outcome before naming a test. It should identify the actor, input or
event, observable result, and relevant failure mode. For example: “When an order total has a
fractional cent, checkout rounds using the published currency rule and records the exact
charged amount.”

Then make a compact risk list. Prioritize behaviors that could lose data or money, break a
public contract, bypass authorization, corrupt a state transition, or are difficult to undo.
For each risk, name:

- the behavior and its observable result;
- a representative normal case and an edge or failure case;
- impact and likelihood; and
- the cheapest test layer that can give meaningful confidence.

Test behavior and public contracts rather than private method calls, exact incidental log
messages, framework internals, or a mirror of the implementation's branches. A test that
would survive an internal refactor protects the user better.

### 2. Choose layers deliberately

Build a pyramid according to feedback cost, not a fixed percentage. Many fast unit tests
should cover rules, transformations, and state transitions; fewer integration tests should
prove the joins between components; a very small set of E2E tests should prove critical user
journeys. The exact shape changes with risk: an adapter-heavy feature needs more integration
coverage, and a compliance-critical checkout may justify more E2E coverage.

| Layer | Use it to prove | Keep it fast and trustworthy by | Avoid using it for |
|---|---|---|---|
| Unit | A rule, calculation, state transition, parser, or error mapping in isolation | Calling production code directly; injecting clock, random source, and collaborators | Proving wiring, serialization, or a real process boundary |
| Integration | A real join: repository plus schema, serializer plus handler, CLI plus files, or a client adapter plus a controllable local server | Using a temporary directory, `sqlite3` database, local subprocess, or in-process stdlib test server; resetting state | Repeating every domain edge case already covered by units |
| E2E | One valuable workflow across the deployed entry points | Using a stable local/test environment, explicit setup/cleanup, and observable completion | Exhaustively testing every validation branch or routine error |

For every important risk, choose **one primary layer**. Add another layer only when it proves a
different thing. For example, test a discount formula across dozens of values at unit level,
then use one integration test to prove JSON request/response wiring, and one E2E checkout
journey to prove the user-visible path. Do not duplicate every assertion at all three layers.

Use this decision order:

1. Can a unit test observe the behavior without lying about a boundary? Prefer it.
2. Could serialization, database semantics, filesystem behavior, process invocation, or an
   external protocol change the answer? Add a focused integration test.
3. Could configuration or a cross-component journey still fail while lower layers pass? Add a
   small E2E smoke test for that high-value journey.
4. Does the scenario need a real remote service to be meaningful? First test the client
   contract locally with a fake or recorded response. Run live checks only in an explicitly
   authorized environment with non-secret configuration; never make ordinary tests depend on
   the network.

### 3. Make test data local, readable, and isolated

Start with the smallest data that exposes the behavior. Give data domain names such as
`overdue_invoice` rather than opaque names such as `case_7`. Use a factory for normal cases
and override only the fields relevant to the assertion. Store large or format-sensitive inputs
under the test directory, read them as immutable source data, and copy them into a fresh
temporary workspace before a test mutates them.

Use `setUp` for a fresh fixture per test and register cleanup immediately after acquiring a
resource. The following is portable and needs neither a fixed path nor a service:

```python
import json
import tempfile
import unittest
from pathlib import Path


class ImportTests(unittest.TestCase):
    def setUp(self):
        self._temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self._temporary_directory.cleanup)
        self.workspace = Path(self._temporary_directory.name)

    def write_order(self, **changes):
        order = {"id": "order-1", "currency": "USD", "total_cents": 1250}
        order.update(changes)
        path = self.workspace / "order.json"
        path.write_text(json.dumps(order), encoding="utf-8")
        return path

    def test_import_preserves_a_valid_total(self):
        result = import_order(self.write_order())
        self.assertEqual(result.total_cents, 1250)

    def test_import_rejects_a_negative_total(self):
        with self.assertRaises(ValueError):
            import_order(self.write_order(total_cents=-1))
```

Apply these data rules:

- Do not mutate a module-level dictionary, class fixture, shared fixture file, or another
  test's database row. Make a new object, copy the source file, or reset the resource.
- Use `setUpClass` only for genuinely immutable, expensive data. Never let it carry mutable
  state from one test to another.
- Keep timestamps, random values, UUIDs, locale, timezone, environment variables, and current
  working directory under test control. Pass a clock or random generator to production code
  where possible instead of patching broad global state.
- Use `self.subTest(...)` for a compact table of independent cases. Keep each row small enough
  that a failure names the behavior, not just an index.
- Name fixture ownership and cleanup. A fixture is incomplete if a reader cannot tell who
  creates it, who may mutate it, and when it goes away.

### 4. Mock at boundaries, not at seams inside your own design

A mock is useful when it replaces a dependency whose real behavior is outside the unit's
responsibility, slow, costly, dangerous, nondeterministic, or unavailable locally. Typical
boundaries include payment providers, email gateways, clocks, random sources, process launch,
and remote HTTP clients. Prefer a small fake for a stable domain protocol when several tests
need realistic behavior; use a mock for a single interaction or failure.

Do **not** mock pure domain objects, value objects, the system under test, or collaborators
owned by the same unit merely to assert its implementation sequence. Calling mocks for every
internal helper turns refactors into test failures without proving a user outcome. Do not mock
an ORM or HTTP library just to imitate its internals; put that proof in a focused integration
test instead.

Patch the name where the system under test looks it up, and constrain mocks to the intended
interface. In `unittest`, `create_autospec` catches calls that the real collaborator would not
accept:

```python
import unittest
from unittest.mock import create_autospec


class ReceiptServiceTests(unittest.TestCase):
    def test_records_the_gateway_reference_after_a_successful_charge(self):
        gateway = create_autospec(PaymentGateway, instance=True)
        gateway.charge.return_value = ChargeResult(reference="charge-42")
        service = ReceiptService(gateway=gateway)

        receipt = service.charge(invoice(total_cents=1250))

        self.assertEqual(receipt.reference, "charge-42")
        gateway.charge.assert_called_once()
```

The assertion on `receipt.reference` is the outcome. The single mock assertion only protects
the boundary contract; it is not a substitute for an integration test of the real adapter.
When a test needs a clock, pass `now=lambda: fixed_time` (or a small clock object) rather than
sleeping or relying on the current time.

### 5. Diagnose, quarantine, and fix flakes

Treat a test as flaky when the same revision and intended environment produce different
outcomes without a behavior change. “It passed on retry” is evidence to investigate, not a
resolution.

**Identify and preserve evidence**

1. Record the full test id, revision, platform, Python/runtime version, attempt count, elapsed
   time, seed, relevant non-secret configuration, and failure output.
2. Re-run the single test in a clean process, then in a loop and alongside neighboring tests.
   Vary ordering, parallelism, timezone, locale, and constrained timing only one factor at a
   time.
3. Classify the cause: shared mutable state, order dependence, unawaited/background work,
   timing or polling, resource leak, port/file contention, random input, clock/timezone,
   external dependency, or an assertion that races an eventual result.

**Quarantine narrowly**

A quarantine is allowed only to keep a known non-deterministic test from blocking unrelated
work while it is repaired. Put it in a clearly named quarantined group or skip with a tracking
issue, an owner, a reason, and an expiry/review date. Keep the original test visible in reports.
Never silently delete it, mark a failure as expected forever, or add unlimited retries that
hide a real regression. If the test guards a critical payment, authorization, data-loss, or
security path, escalate rather than treating a quarantine as acceptable coverage.

**Fix the cause, then prove stability**

- Replace sleeps and fixed retry counts with an observable completion condition and a bounded,
  diagnostic timeout.
- Inject a clock and deterministic random source; report the seed for generated cases.
- Allocate ports and files per test, clean them with `addCleanup`, and wait for child processes
  to exit.
- Reset global state, restore environment changes, and make test order irrelevant.
- Replace a live remote dependency with a local fake at the boundary for ordinary tests.
- Run the repaired test repeatedly in a clean environment and restore it from quarantine only
  after the cause and evidence are recorded.

### 6. Record the plan and run a tight verification loop

For a reviewable plan, use the optional local manifest at
[examples/test-plan.json](examples/test-plan.json). It links risks to test layers, local
fixtures, boundary decisions, and flaky-test ownership. Validate it from the skill directory:

```bash
python3 scripts/verify_test_plan.py examples/test-plan.json
```

```powershell
python scripts/verify_test_plan.py examples/test-plan.json
```

The verifier reads one local JSON file and makes no network requests. It requires non-empty
risk coverage, local fixture declarations, an explicit mock/real decision for each listed
boundary, and a flaky-test policy with an owner, tracking reference, and valid expiry date.
It does not enforce a fixed unit/integration/E2E ratio: choose layers based on evidence and
risk.

For the implementation itself:

1. Make the smallest failing test at the selected layer.
2. Implement only enough to satisfy its observable contract.
3. Run the focused test, then the relevant suite, then the whole local suite required by the
   repository.
4. Inspect failures before adding a retry, sleep, or mock. Decide whether the failure is a
   product regression, bad test isolation, or an unmodeled boundary.
5. Report the behavior covered, layer, important omissions, fixture lifecycle, mocked
   boundaries, and any temporary quarantine.

## Completion Checklist

Before calling the work tested, confirm all of the following:

- Every high-risk behavior has at least one explicit test and the primary layer is justified.
- Unit tests cover rules and edge cases; integration tests prove each meaningful boundary; E2E
  tests cover only the few critical journeys that lower layers cannot prove.
- Test data is local, minimal, representative, and isolated from other tests.
- Time, randomness, environment, files, ports, and background work are controlled or cleaned.
- Each mock replaces a true boundary, has a stated reason, and is paired with real-adapter
  coverage where the boundary contract matters.
- No test relies on a live network service, production data, embedded credential, or a
  developer-specific absolute path.
- A flaky test has evidence and a root-cause fix, or a visible, owned, expiring quarantine.
- The focused, relevant, and required full suites all pass without hiding failures through
  unbounded retries.
