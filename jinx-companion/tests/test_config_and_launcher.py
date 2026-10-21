"""Regression tests for the shipped config and the Windows launcher."""

import json
import sys
from pathlib import Path

APP_DIR = Path(__file__).parent.parent

sys.path.insert(0, str(APP_DIR))


class TestShippedConfig:
    """The shipped config.json points at the intended instance and world."""

    def test_instance_path_default(self):
        config = json.loads((APP_DIR / 'config.json').read_text(encoding='utf-8'))
        assert config['minecraft_instance_path'] == (
            'C:\\Users\\naddeer\\AppData\\Roaming\\.minecraft\\versions\\'
            'All the Mods 10 - ATM10 All the Mods 10-5.2'
        )

    def test_world_name_default(self):
        config = json.loads((APP_DIR / 'config.json').read_text(encoding='utf-8'))
        assert config['world_name'] == 'naders last'


class TestLauncher:
    """Exactly one browser tab is opened: by server.py, not by start.bat."""

    def test_start_bat_does_not_open_a_browser(self):
        content = (APP_DIR / 'start.bat').read_text(encoding='utf-8')
        browser_lines = [
            line.strip() for line in content.splitlines()
            if line.strip().lower().startswith('start ""')
        ]
        assert browser_lines == []
        assert 'http://127.0.0.1:8720"' not in content

    def test_start_bat_still_starts_the_server(self):
        content = (APP_DIR / 'start.bat').read_text(encoding='utf-8')
        assert 'server.py' in content

    def test_server_opens_exactly_one_browser_tab(self):
        content = (APP_DIR / 'server.py').read_text(encoding='utf-8')
        assert content.count('webbrowser.open(') == 1
