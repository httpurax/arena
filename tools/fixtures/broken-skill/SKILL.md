---
name: broken-skill
version: 1.0
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: testing
---

# Broken skill (linter fixture)

This is not a real skill and is never installed. It exists only so
`tools/test_lint_skills.py` can prove that `tools/lint_skills.py` rejects a non-conforming
skill. Three violations are deliberate, and the self-test asserts each rule by name:

- `description` is missing entirely (`frontmatter.description`).
- `version: 1.0` is not X.Y.Z (`frontmatter.version`).
- The code block below carries an obviously fake credential (`secrets.password-literal`).

```python
password = "fixture-password-not-a-real-credential"
```
