#!/usr/bin/env python3
"""Fixture script for tools/lint_skills.py: carries a fake credential on purpose.

Nothing here is real - the value below is a made-up string that exists so the linter's
secret scan has something it must flag. Do not copy this pattern into a real skill.
"""

# FAKE: the linter must report this line as secrets.api-key-literal.
api_key = "FAKE-fixture-api-key-not-a-real-secret"


def main() -> int:
    print("this fixture is never executed by the repository's own test suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
