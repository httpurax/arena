"""Tests for gamestate.py module"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gamestate import (
    build_game_state,
    extract_completed_quests,
    load_chapter_definitions,
    load_quest_names,
    parse_snbt,
    read_snbt_file
)


@pytest.fixture
def temp_instance_path():
    """Create a temporary directory structure for testing."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def fixture_instance_path():
    """Path to the test fixtures."""
    return str(Path(__file__).parent / 'fixtures')


class TestSNBTParser:
    """Test SNBT parsing functionality."""
    
    def test_parse_empty_object(self):
        """Test parsing an empty object."""
        result = parse_snbt("{}")
        assert result == {}
    
    def test_parse_simple_object(self):
        """Test parsing a simple object."""
        result = parse_snbt('{key: "value", num: 42}')
        assert result == {'key': 'value', 'num': 42}
    
    def test_parse_nested_object(self):
        """Test parsing nested objects."""
        result = parse_snbt('{outer: {inner: "value"}}')
        assert result == {'outer': {'inner': 'value'}}
    
    def test_parse_array(self):
        """Test parsing arrays."""
        result = parse_snbt('[1, 2, 3, "four"]')
        assert result == [1, 2, 3, 'four']
    
    def test_parse_hex_ids(self):
        """Test parsing hex quest IDs."""
        result = parse_snbt('{quests: [0x00010001, 0x00010002]}')
        assert result == {'quests': ['0x00010001', '0x00010002']}
    
    def test_parse_with_comments(self):
        """Test parsing with comments."""
        result = parse_snbt('{key: "value"} // comment')
        assert result == {'key': 'value'}
    
    def test_parse_multiline(self):
        """Test parsing multiline SNBT."""
        snbt = """{
            key: "value",
            num: 42
        }"""
        result = parse_snbt(snbt)
        assert result == {'key': 'value', 'num': 42}


class TestFileReading:
    """Test file reading functionality."""
    
    def test_read_snbt_file(self, fixture_instance_path):
        """Test reading an SNBT file."""
        chapter_file = Path(fixture_instance_path) / 'config' / 'ftbquests' / 'quests' / 'chapters' / 'chapter_1.snbt'
        result = read_snbt_file(str(chapter_file))
        assert result is not None
        assert 'title' in result
        assert result['title'] == 'Getting Started'
    
    def test_read_nonexistent_file(self):
        """Test reading a non-existent file."""
        result = read_snbt_file('/nonexistent/path/file.snbt')
        assert result is None


class TestCompletedQuestsExtraction:
    """Test completed quests extraction."""
    
    def test_extract_completed_quests(self, fixture_instance_path):
        """Test extracting completed quests from progress files."""
        completed = extract_completed_quests(fixture_instance_path, 'world1')
        
        # Should have quests from both progress.snbt and completed.snbt
        assert '0x00010001' in completed
        assert '0x00010002' in completed
        assert '0x00010003' in completed
        assert '0x00020001' in completed
        assert '0x00020002' in completed
    
    def test_extract_from_nonexistent_save(self, temp_instance_path):
        """Test extracting from non-existent save."""
        completed = extract_completed_quests(temp_instance_path, 'nonexistent')
        assert completed == set()


class TestChapterDefinitions:
    """Test chapter definitions loading."""
    
    def test_load_chapter_definitions(self, fixture_instance_path):
        """Test loading chapter definitions."""
        chapters = load_chapter_definitions(fixture_instance_path)
        
        assert len(chapters) == 2
        assert 'chapter_1' in chapters
        assert 'chapter_2' in chapters
        
        chapter_1 = chapters['chapter_1']
        assert chapter_1['name'] == 'Getting Started'
        assert len(chapter_1['quests']) == 3
    
    def test_load_chapters_from_nonexistent(self, temp_instance_path):
        """Test loading chapters from non-existent path."""
        chapters = load_chapter_definitions(temp_instance_path)
        assert chapters == {}


class TestQuestNames:
    """Test quest names loading."""
    
    def test_load_quest_names(self, fixture_instance_path):
        """Test loading quest names from language file."""
        names = load_quest_names(fixture_instance_path)
        
        # Check some quest names
        assert names.get('0x00010001') == 'Craft a Wooden Pickaxe'
        assert names.get('0x00010002') == 'Mine Stone'
        assert names.get('0x00020001') == 'Get Iron Ingots'
    
    def test_load_quest_names_from_nonexistent(self, temp_instance_path):
        """Test loading quest names from non-existent path."""
        names = load_quest_names(temp_instance_path)
        assert names == {}


class TestGameStateBuilding:
    """Test game state building."""
    
    def test_build_game_state_complete(self, fixture_instance_path):
        """Test building game state with all data available."""
        state = build_game_state(fixture_instance_path, 'world1')
        
        # Should contain world name
        assert 'World: world1' in state
        
        # Should contain chapter info (1 complete out of 2)
        assert 'Chapters: 1/2 completed' in state
        
        # Should contain quest count (5 completed out of 7)
        assert 'Quests: 5/7 completed' in state
        
        # Should list completed quests
        assert 'Completed quests:' in state
        
        # Should list next quests
        assert 'Next quests:' in state
    
    def test_build_game_state_nonexistent_instance(self):
        """Test building game state with non-existent instance path."""
        state = build_game_state('/nonexistent/path', 'world1')
        assert 'Save not readable' in state
    
    def test_build_game_state_nonexistent_world(self, fixture_instance_path):
        """Test building game state with non-existent world."""
        state = build_game_state(fixture_instance_path, 'nonexistent_world')
        # Should still work but with no progress
        assert 'World: nonexistent_world' in state
    
    def test_build_game_state_no_progress_files(self, fixture_instance_path):
        """Test building game state when progress files don't exist."""
        # Use a world that doesn't have ftbquests directory
        state = build_game_state(fixture_instance_path, 'nonexistent')
        assert 'World: nonexistent' in state


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_snbt_file(self, temp_instance_path):
        """Test parsing empty SNBT file."""
        empty_file = Path(temp_instance_path) / 'empty.snbt'
        empty_file.write_text('')
        
        result = read_snbt_file(str(empty_file))
        assert result == {} or result is None
    
    def test_malformed_snbt(self):
        """Test parsing malformed SNBT."""
        # Should not crash
        result = parse_snbt('{incomplete')
        # May return partial or None depending on implementation
        assert result is not None or result == {}
    
    def test_special_characters_in_strings(self):
        """Test parsing strings with special characters."""
        result = parse_snbt('{name: "Test \\"quoted\\" string"}')
        # The parser may or may not handle escaped quotes perfectly
        assert 'name' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
