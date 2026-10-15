import re
from pathlib import Path

DOC = Path(__file__).resolve().parents[1] / "references" / "git-basics.md"


def test_git_basics_content_and_format():
    text = DOC.read_text()
    lines = [l for l in text.splitlines() if l.strip().startswith("-")]
    assert len(lines) == 10
    for line in lines:
        assert re.match(r'^- `git [^`]+` — .+\.$', line.strip()), f"Bad format: {line}"
