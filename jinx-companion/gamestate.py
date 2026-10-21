"""
Game State Reader for Jinx Companion
Reads FTB Quests progress from Minecraft ATM10 save files and produces
a compact game state summary.
"""

import os
import re
import json
from pathlib import Path


def read_snbt_file(filepath):
    """Read and parse an SNBT file, returning a dict of the top-level structure."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return parse_snbt(content)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError):
        return None


def parse_snbt(content):
    """
    Parse SNBT (Simplified NBT) content into a Python dict.
    Tolerant parser that handles the text format used by FTB Quests.
    """
    content = content.strip()
    if not content:
        return {}
    
    # Remove comments if any
    content = re.sub(r'//.*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = content.strip()
    
    if content.startswith('{'):
        return _parse_snbt_object(content)
    elif content.startswith('['):
        return _parse_snbt_array(content)
    else:
        # Try to parse as a simple value
        return _parse_snbt_value(content)


def _parse_snbt_object(content):
    """Parse an SNBT object/compound tag."""
    if not content.startswith('{'):
        raise ValueError("Expected object to start with {")
    
    result = {}
    # Remove outer braces
    inner = content[1:-1].strip()
    
    if not inner:
        return result
    
    # Split by commas at top level (not inside nested structures)
    parts = _split_top_level(inner)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Find the first colon that's not inside quotes or nested structures
        colon_idx = _find_top_level_colon(part)
        if colon_idx is None:
            continue
        
        key = part[:colon_idx].strip()
        # Remove quotes from key if present
        key = key.strip('"').strip("'")
        
        value_str = part[colon_idx + 1:].strip()
        value = _parse_snbt_value(value_str)
        
        result[key] = value
    
    return result


def _parse_snbt_array(content):
    """Parse an SNBT array/list tag."""
    if not content.startswith('['):
        raise ValueError("Expected array to start with [")
    
    result = []
    # Remove outer brackets
    inner = content[1:-1].strip()
    
    if not inner:
        return result
    
    # Split by commas at top level
    parts = _split_top_level(inner)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        value = _parse_snbt_value(part)
        result.append(value)
    
    return result


def _parse_snbt_value(content):
    """Parse a single SNBT value (primitive, object, or array)."""
    content = content.strip()
    
    if not content:
        return None
    
    if content.startswith('{'):
        return _parse_snbt_object(content)
    elif content.startswith('['):
        return _parse_snbt_array(content)
    elif content.startswith('"') or content.startswith("'"):
        # String
        return content[1:-1]
    elif content.lower() == 'true':
        return True
    elif content.lower() == 'false':
        return False
    elif content.lower() == 'null' or content.lower() == '':
        return None
    else:
        # Try to parse as number
        try:
            if '.' in content or 'e' in content.lower() or 'E' in content:
                return float(content)
            else:
                # Check for hex (FTB Quests uses hex quest IDs)
                if re.match(r'^0x[0-9a-fA-F]+$', content):
                    return content  # Keep as hex string
                if re.match(r'^[0-9]+[LlSsBbYyZz]?$', content):
                    # NBT number suffixes
                    return int(content.rstrip('LlSsBbYyZz'))
                return int(content)
        except ValueError:
            # Return as string if not a number
            return content


def _split_top_level(content):
    """Split content by commas at the top level (not inside nested structures)."""
    parts = []
    current = []
    depth = 0
    in_string = False
    string_char = None
    
    for char in content:
        if char in ('"', "'") and (not in_string or char == string_char):
            in_string = not in_string
            if in_string:
                string_char = char
            else:
                string_char = None
            current.append(char)
        elif not in_string:
            if char == '{' or char == '[':
                depth += 1
                current.append(char)
            elif char == '}' or char == ']':
                depth -= 1
                current.append(char)
            elif char == ',' and depth == 0:
                parts.append(''.join(current))
                current = []
            else:
                current.append(char)
        else:
            current.append(char)
    
    if current:
        parts.append(''.join(current))
    
    return parts


def _find_top_level_colon(content):
    """Find the first colon at top level (not inside nested structures or strings)."""
    depth = 0
    in_string = False
    string_char = None
    
    for i, char in enumerate(content):
        if char in ('"', "'") and (not in_string or char == string_char):
            in_string = not in_string
            if in_string:
                string_char = char
            else:
                string_char = None
        elif not in_string:
            if char == '{' or char == '[':
                depth += 1
            elif char == '}' or char == ']':
                depth -= 1
            elif char == ':' and depth == 0:
                return i
    
    return None


def extract_completed_quests(instance_path, world_name):
    """
    Extract completed quest IDs from FTB Quests progress files.
    Reads from <instance>/saves/<world>/ftbquests/*.snbt
    """
    completed = set()
    saves_dir = Path(instance_path) / 'saves' / world_name / 'ftbquests'
    
    if not saves_dir.exists():
        return completed
    
    for snbt_file in saves_dir.glob('*.snbt'):
        try:
            data = read_snbt_file(str(snbt_file))
            if data is None:
                continue
            
            # Look for completed quests in various possible structures
            # FTB Quests stores progress with quest IDs
            _extract_quest_ids_from_data(data, completed)
        except Exception:
            # Tolerant parsing - skip files that fail
            continue
    
    return completed


def _extract_quest_ids_from_data(data, completed_set):
    """Recursively extract quest IDs from parsed SNBT data."""
    if isinstance(data, dict):
        # Check for common FTB Quests progress patterns
        # Progress files often have structures like:
        # {progress: {quests: [hex_id, ...]}}
        # or {completed: [hex_id, ...]}
        # or individual quest entries with completed flags
        
        # Direct list of completed quests
        for key in ['completed', 'completed_quests', 'progress', 'quests']:
            if key in data and isinstance(data[key], list):
                for item in data[key]:
                    if isinstance(item, str) and re.match(r'^0x[0-9a-fA-F]+$', item):
                        completed_set.add(item)
        
        # Check for nested structures
        if 'progress' in data and isinstance(data['progress'], dict):
            if 'quests' in data['progress'] and isinstance(data['progress']['quests'], list):
                for quest in data['progress']['quests']:
                    if isinstance(quest, str) and re.match(r'^0x[0-9a-fA-F]+$', quest):
                        completed_set.add(quest)
            elif 'quests' in data['progress'] and isinstance(data['progress']['quests'], dict):
                for quest_id, quest_data in data['progress']['quests'].items():
                    if isinstance(quest_id, str) and re.match(r'^0x[0-9a-fA-F]+$', quest_id):
                        # Check if quest is completed
                        if isinstance(quest_data, dict):
                            if quest_data.get('completed', False) or quest_data.get('progress', 0) >= 100:
                                completed_set.add(quest_id)
                        else:
                            completed_set.add(quest_id)
        
        # Recurse into nested dicts
        for value in data.values():
            _extract_quest_ids_from_data(value, completed_set)
    
    elif isinstance(data, list):
        for item in data:
            _extract_quest_ids_from_data(item, completed_set)


def load_chapter_definitions(instance_path):
    """
    Load chapter definitions from <instance>/config/ftbquests/quests/chapters/*.snbt
    Returns dict of chapter_id -> {name, quests: [quest_id, ...]}
    """
    chapters = {}
    chapters_dir = Path(instance_path) / 'config' / 'ftbquests' / 'quests' / 'chapters'
    
    if not chapters_dir.exists():
        return chapters
    
    for snbt_file in sorted(chapters_dir.glob('*.snbt')):
        try:
            data = read_snbt_file(str(snbt_file))
            if data is None:
                continue
            
            chapter_id = snbt_file.stem
            chapter_info = {'id': chapter_id, 'name': chapter_id, 'quests': []}
            
            # Extract chapter name
            if 'title' in data:
                chapter_info['name'] = data['title']
            elif 'name' in data:
                chapter_info['name'] = data['name']
            
            # Extract quests
            if 'quests' in data and isinstance(data['quests'], list):
                for quest in data['quests']:
                    if isinstance(quest, str):
                        chapter_info['quests'].append(quest)
                    elif isinstance(quest, dict) and 'id' in quest:
                        chapter_info['quests'].append(quest['id'])
            
            chapters[chapter_id] = chapter_info
        except Exception:
            continue
    
    return chapters


def load_quest_names(instance_path):
    """
    Load quest display names from <instance>/config/ftbquests/quests/lang/en_us.snbt
    Returns dict of quest_id -> display_name
    """
    quest_names = {}
    lang_file = Path(instance_path) / 'config' / 'ftbquests' / 'quests' / 'lang' / 'en_us.snbt'
    
    if not lang_file.exists():
        return quest_names
    
    try:
        data = read_snbt_file(str(lang_file))
        if data is None:
            return quest_names
        
        # Language files typically have structure like:
        # {"ftbquests.quest.<id>": "Display Name", ...}
        _extract_quest_names_from_data(data, quest_names)
    except Exception:
        pass
    
    return quest_names


def _extract_quest_names_from_data(data, names_dict):
    """Recursively extract quest names from language file data."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                # Check for quest name patterns
                # ftbquests.quest.<hex_id> or similar
                match = re.match(r'ftbquests\.quest\.(0x[0-9a-fA-F]+)', key)
                if match:
                    quest_id = match.group(1)
                    names_dict[quest_id] = value
                # Also check for chapter names
                match = re.match(r'ftbquests\.chapter\.(0x[0-9a-fA-F]+)', key)
                if match:
                    chapter_id = match.group(1)
                    names_dict[chapter_id] = value
            else:
                _extract_quest_names_from_data(value, names_dict)
    elif isinstance(data, list):
        for item in data:
            _extract_quest_names_from_data(item, names_dict)


def build_game_state(instance_path, world_name):
    """
    Build a compact game state text from the save files.
    Returns a string describing the game state or an error message.
    """
    try:
        # Check if instance path exists
        if not Path(instance_path).exists():
            return "Save not readable: Instance path does not exist"
        
        # Get completed quests
        completed_quests = extract_completed_quests(instance_path, world_name)
        
        # Load chapter definitions
        chapters = load_chapter_definitions(instance_path)
        
        # Load quest names
        quest_names = load_quest_names(instance_path)
        
        # Build chapter completion info
        total_chapters = len(chapters)
        completed_chapters = 0
        chapter_status = []
        
        for chapter_id, chapter_info in chapters.items():
            chapter_quests = chapter_info.get('quests', [])
            if not chapter_quests:
                continue
            
            # Count completed quests in this chapter
            completed_in_chapter = sum(
                1 for q in chapter_quests if q in completed_quests
            )
            
            is_complete = completed_in_chapter >= len(chapter_quests)
            if is_complete:
                completed_chapters += 1
            
            chapter_status.append({
                'id': chapter_id,
                'name': chapter_info.get('name', chapter_id),
                'total_quests': len(chapter_quests),
                'completed': completed_in_chapter,
                'is_complete': is_complete
            })
        
        # Total quests
        all_quest_ids = set()
        for chapter_info in chapters.values():
            all_quest_ids.update(chapter_info.get('quests', []))
        
        total_quests = len(all_quest_ids)
        total_completed = len([q for q in all_quest_ids if q in completed_quests])
        
        # Get completed quest names (up to 10)
        completed_with_names = []
        for quest_id in completed_quests:
            if quest_id in quest_names:
                completed_with_names.append(quest_names[quest_id])
            else:
                completed_with_names.append(quest_id)
        
        # Sort and limit to 10
        completed_with_names = sorted(completed_with_names)[:10]
        
        # Get incomplete quest names (up to 10)
        incomplete_quests = all_quest_ids - completed_quests
        incomplete_with_names = []
        for quest_id in incomplete_quests:
            if quest_id in quest_names:
                incomplete_with_names.append(quest_names[quest_id])
            else:
                incomplete_with_names.append(quest_id)
        
        incomplete_with_names = sorted(incomplete_with_names)[:10]
        
        # Build the game state text
        state_lines = []
        state_lines.append(f"World: {world_name}")
        state_lines.append(f"Chapters: {completed_chapters}/{total_chapters} completed")
        state_lines.append(f"Quests: {total_completed}/{total_quests} completed")
        
        if completed_with_names:
            state_lines.append(f"Completed quests: {', '.join(completed_with_names)}")
        
        if incomplete_with_names:
            state_lines.append(f"Next quests: {', '.join(incomplete_with_names)}")
        
        return '\n'.join(state_lines)
    
    except Exception as e:
        return f"Save not readable: {str(e)}"


if __name__ == '__main__':
    # Test with sample paths
    print("Game State Reader - Test Mode")
    print("Use via build_game_state(instance_path, world_name)")
