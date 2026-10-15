import re
from pathlib import Path

DOC = Path(__file__).resolve().parents[1] / "references" / "git-push-troubleshooting.md"


def test_git_push_troubleshooting_content_and_format():
    text = DOC.read_text()
    sections = re.findall(r'^## \d+\. .+', text, re.MULTILINE)
    assert len(sections) == 5
    assert text.count("- Cause:") == 5
    assert text.count("- Fix:") == 5
