"""
Game State Reader for Jinx Companion
Reads FTB Quests progress from Minecraft ATM10 save files and produces
a compact game state summary.

Two sources are used:

* Quest structure - ``<instance>/config/ftbquests/quests/``
  (chapter files, language files).  These are shared by every world of the
  instance and describe what the quest book *asks for*: quest names, task
  requirements and rewards.
* Quest progress - ``<instance>/saves/<world>/ftbquests/*.snbt``
  (one file per team).  These describe what the player has *already done*.

Player basics (experience level and current dimension) are read on a best
effort basis from ``saves/<world>/playerdata/*.dat`` (or ``level.dat``).
Those are gzipped NBT files, so a tiny read-only NBT parser lives below -
no third party dependency is used, and unreadable data is skipped silently.
"""

import gzip
import os
import re
import struct
import zlib
from pathlib import Path


# ---------------------------------------------------------------------------
# SNBT parsing
# ---------------------------------------------------------------------------

# Parsed quest book files are reused between chat requests: the quest book is
# a couple of megabytes and only changes when the pack is updated.  The cache
# is validated with mtime/size so edited files are always re-read.
_SNBT_CACHE = {}
_SNBT_CACHE_MAX = 512


def read_snbt_file(filepath):
    """Read and parse an SNBT file, returning a dict of the top-level structure."""
    try:
        stat = os.stat(filepath)
        cache_key = str(filepath)
        cached = _SNBT_CACHE.get(cache_key)
        if cached and cached[0] == stat.st_mtime_ns and cached[1] == stat.st_size:
            return cached[2]

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        result = parse_snbt(content)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError):
        return None

    if len(_SNBT_CACHE) >= _SNBT_CACHE_MAX:
        _SNBT_CACHE.clear()
    _SNBT_CACHE[cache_key] = (stat.st_mtime_ns, stat.st_size, result)
    return result


def parse_snbt(content):
    """
    Parse SNBT (Simplified NBT) content into a Python dict.
    Tolerant parser that handles the text format used by FTB Quests.
    """
    content = content.strip()
    if not content:
        return {}

    # Remove comments if any (but never inside quoted strings - item ids and
    # quest text contain '//' such as "https://discord.gg/allthemods").
    content = _strip_comments(content)
    content = content.strip()

    try:
        if content.startswith('{'):
            return _parse_snbt_object(content)
        elif content.startswith('['):
            return _parse_snbt_array(content)
        else:
            # Try to parse as a simple value
            return _parse_snbt_value(content)
    except (ValueError, IndexError):
        # Tolerant parsing: an unreadable file must never take the app down.
        return {}


def _strip_comments(content):
    """
    Remove ``//`` and ``/* */`` comments that are outside of quoted strings.

    A naive regex would truncate every line containing a URL, which is common
    in real quest book files (discord links, documentation links, ...).
    """
    out = []
    index = 0
    length = len(content)
    in_string = False
    string_char = None
    escaped = False

    while index < length:
        char = content[index]

        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == string_char:
                in_string = False
            index += 1
            continue

        if char in ('"', "'"):
            in_string = True
            string_char = char
            escaped = False
            out.append(char)
            index += 1
            continue

        if char == '/' and index + 1 < length:
            next_char = content[index + 1]
            if next_char == '/':
                newline = content.find('\n', index)
                if newline == -1:
                    break
                index = newline  # keep the newline itself
                continue
            if next_char == '*':
                end = content.find('*/', index + 2)
                if end == -1:
                    break
                index = end + 2
                continue

        out.append(char)
        index += 1

    return ''.join(out)


def _parse_snbt_object(content):
    """Parse an SNBT object/compound tag."""
    if not content.startswith('{'):
        raise ValueError("Expected object to start with {")

    result = {}
    # Remove outer braces
    inner = content[1:-1].strip()

    if not inner:
        return result

    # Split by commas *and* newlines at top level (FTB Quests omits commas
    # in generated files, e.g. "id: \"ABC\"\n type: \"item\"").
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

    # Split by commas and newlines at top level
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
        # String - require a closing quote, otherwise keep the raw text.
        quote = content[0]
        if len(content) >= 2 and content.endswith(quote):
            return content[1:-1]
        return content[1:]
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
                # Guard: hex ids such as 0x1E5 are identifiers, not numbers.
                if _HEX_ID_RE.match(content):
                    return content
                return float(content.rstrip('dDfF'))
            else:
                # Check for hex (FTB Quests uses hex quest IDs)
                if _HEX_ID_RE.match(content):
                    return content  # Keep as hex string
                if re.match(r'^[+-]?[0-9]+[LlSsBbYyZz]?$', content):
                    # NBT number suffixes
                    return int(content.rstrip('LlSsBbYyZz'))
                return int(content)
        except ValueError:
            # Return as string if not a number
            return content


def _split_top_level(content):
    """
    Split content into entries at the top level.

    Entries are separated by commas and/or newlines; neither may appear
    inside a quoted string or a nested compound/list.
    """
    parts = []
    current = []
    depth = 0
    in_string = False
    string_char = None
    escaped = False

    for char in content:
        if in_string:
            current.append(char)
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == string_char:
                in_string = False
            continue

        if char in ('"', "'"):
            in_string = True
            string_char = char
            escaped = False
            current.append(char)
        elif char == '{' or char == '[':
            depth += 1
            current.append(char)
        elif char == '}' or char == ']':
            depth = max(0, depth - 1)
            current.append(char)
        elif depth == 0 and (char == ',' or char == '\n'):
            parts.append(''.join(current))
            current = []
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
    escaped = False

    for i, char in enumerate(content):
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == string_char:
                in_string = False
            continue

        if char in ('"', "'"):
            in_string = True
            string_char = char
        elif char == '{' or char == '[':
            depth += 1
        elif char == '}' or char == ']':
            depth = max(0, depth - 1)
        elif char == ':' and depth == 0:
            return i

    return None


# ---------------------------------------------------------------------------
# Small text helpers
# ---------------------------------------------------------------------------

_HEX_ID_RE = re.compile(r'^0x[0-9a-fA-F]+$')
_QUEST_ID_RE = re.compile(r'^(?:0x[0-9a-fA-F]+|[0-9a-fA-F]{16})$')
_MC_FORMAT_RE = re.compile(r'&[0-9a-fk-orx]', re.IGNORECASE)
_LANG_KEY_RE = re.compile(
    r'^(?:ftbquests\.)?(quest|chapter|task|reward)\.([0-9A-Za-z_]+)'
    r'(?:\.(?:title|name))?$'
)


def normalize_quest_id(value):
    """
    Return a canonical form of a quest/chapter/task id so that ids read from
    chapter files ('0x00010001', '"28408BFAA54E4FC6"') can be compared with
    ids read from progress files.  Non-ids are returned upper-cased as-is.
    """
    if isinstance(value, bool) or value is None:
        return ''
    if isinstance(value, int):
        text = '0x%08X' % value
    else:
        text = str(value).strip().strip('"').strip("'").strip()
    if not text:
        return ''
    if text.lower().startswith('0x'):
        text = text[2:]
    return text.upper()


def _id_text(value):
    """Best effort conversion of an SNBT id value to text ('' when unusable)."""
    if isinstance(value, bool) or value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, int):
        return '0x%08X' % value
    return ''


def _clean_text(value):
    """
    Turn an SNBT language string into something readable for the model:
    unescape common escapes, drop Minecraft colour codes and collapse spaces.
    """
    if not isinstance(value, str):
        return ''
    text = value.replace('\\n', ' ').replace('\\"', '"')
    # Protect escaped ampersands (literal '&') from the colour-code stripper.
    text = text.replace('\\&', '\x00')
    text = _MC_FORMAT_RE.sub('', text)
    text = text.replace('\x00', '&')
    text = text.replace('\\\\', '\\')
    text = ' '.join(text.split())
    return text.strip()


def _friendly_dimension(dimension):
    """Map a dimension id to a short human readable name."""
    if not isinstance(dimension, str) or not dimension.strip():
        return ''
    key = dimension.strip().lower()
    names = {
        'minecraft:overworld': 'Overworld',
        'overworld': 'Overworld',
        'minecraft:the_nether': 'The Nether',
        'the_nether': 'The Nether',
        'nether': 'The Nether',
        'minecraft:the_end': 'The End',
        'the_end': 'The End',
        'end': 'The End',
    }
    return names.get(key, dimension.strip())


def _as_list(value):
    """Normalise an SNBT list-ish value to a list."""
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return list(value.values())
    if value is None:
        return []
    return [value]


def _as_number(value):
    """Best effort numeric conversion (handles '8L', 8.0 and plain ints)."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        text = value.strip().rstrip('LlSsBb')
        try:
            return int(float(text))
        except (TypeError, ValueError):
            return None
    return None


def _truncate(text, limit=80):
    """Keep a single description line short enough for a prompt."""
    if len(text) <= limit:
        return text
    return text[:limit - 1].rstrip() + '…'


# ---------------------------------------------------------------------------
# Quest progress (what the player has completed)
# ---------------------------------------------------------------------------

def extract_completed_quests(instance_path, world_name):
    """
    Extract completed quest IDs from FTB Quests progress files.
    Reads from <instance>/saves/<world>/ftbquests/*.snbt
    """
    completed = set()
    saves_dir = Path(instance_path) / 'saves' / world_name / 'ftbquests'

    if not saves_dir.exists():
        return completed

    for snbt_file in sorted(saves_dir.glob('*.snbt')):
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


def _add_quest_id(value, completed_set):
    """Add a quest id to the completed set if the value looks like one."""
    text = _id_text(value)
    if text and _QUEST_ID_RE.match(text):
        completed_set.add(text)


def _extract_quest_ids_from_data(data, completed_set):
    """Recursively extract quest IDs from parsed SNBT data."""
    if isinstance(data, dict):
        # Check for common FTB Quests progress patterns
        # Progress files often have structures like:
        # {progress: {quests: [hex_id, ...]}}
        # or {completed: [hex_id, ...]}
        # or individual quest entries with completed flags

        # Direct list of completed quests.  Modern FTB Quests (1.20+) writes
        # {completed: ["28408BFAA54E4FC6", ...]} while older versions used 0x ids.
        for key in ['completed', 'completed_quests', 'progress', 'quests']:
            value = data.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        _add_quest_id(item, completed_set)
                    elif isinstance(item, dict):
                        for id_key in ('id', 'quest', 'quest_id'):
                            if id_key in item:
                                _add_quest_id(item[id_key], completed_set)
                                break
            elif isinstance(value, dict):
                # {completed: {"<quest id>": <timestamp>}}
                for quest_id, quest_data in value.items():
                    if not _QUEST_ID_RE.match(_id_text(quest_id)):
                        continue
                    if isinstance(quest_data, dict):
                        if (quest_data.get('completed', False)
                                or quest_data.get('progress', 0) >= 100):
                            _add_quest_id(quest_id, completed_set)
                    else:
                        # Presence in the map means the quest was completed.
                        _add_quest_id(quest_id, completed_set)

        # Recurse into nested dicts
        for value in data.values():
            _extract_quest_ids_from_data(value, completed_set)

    elif isinstance(data, list):
        for item in data:
            _extract_quest_ids_from_data(item, completed_set)


# ---------------------------------------------------------------------------
# Quest definitions (chapter + language files)
# ---------------------------------------------------------------------------

def _iter_lang_files(instance_path):
    """
    Yield the English language files of the quest book.  FTB Quests has used
    both a single ``lang/en_us.snbt`` and a split ``lang/en_us/`` tree.
    """
    lang_dir = Path(instance_path) / 'config' / 'ftbquests' / 'quests' / 'lang'
    seen = set()

    candidates = [lang_dir / 'en_us.snbt']
    for sub in ('en_us', 'en_us/chapters'):
        directory = lang_dir / sub
        if directory.is_dir():
            candidates.extend(sorted(directory.glob('*.snbt')))

    for path in candidates:
        if not path.is_file():
            continue
        key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        yield path


def load_lang_strings(instance_path):
    """
    Load quest book language strings.

    Returns a dict with the keys ``quests``, ``chapters``, ``tasks`` and
    ``rewards``, each mapping a raw id to its display text.  Both the legacy
    ``ftbquests.quest.<id>`` keys and the modern ``quest.<id>.title`` keys
    are understood.
    """
    strings = {'quests': {}, 'chapters': {}, 'tasks': {}, 'rewards': {}}

    for lang_file in _iter_lang_files(instance_path):
        try:
            data = read_snbt_file(str(lang_file))
            if not isinstance(data, dict):
                continue
            _extract_lang_strings(data, strings)
        except Exception:
            # Tolerant parsing - a broken language file only loses names.
            continue

    return strings


def _extract_lang_strings(data, strings):
    """Recursively collect 'quest.<id>.title' style keys from language data."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                match = _LANG_KEY_RE.match(str(key))
                if match:
                    kind, object_id = match.group(1), match.group(2)
                    bucket = strings.get(kind + 's')
                    if bucket is not None:
                        bucket[object_id] = _clean_text(value)
            else:
                _extract_lang_strings(value, strings)
    elif isinstance(data, list):
        for item in data:
            _extract_lang_strings(item, strings)


def _extract_quest_names_from_data(data, names_dict):
    """Backwards-compatible helper: collect quest and chapter names."""
    strings = {'quests': names_dict, 'chapters': names_dict,
               'tasks': {}, 'rewards': {}}
    _extract_lang_strings(data, strings)


def load_quest_names(instance_path):
    """
    Load quest and chapter display names.
    Returns dict of id -> display_name (chapters first, then quests).
    """
    strings = load_lang_strings(instance_path)
    names = dict(strings.get('chapters', {}))
    names.update(strings.get('quests', {}))
    return names


def _normalized_lookup(mapping):
    """Return a copy of an id->text map keyed by normalised ids."""
    lookup = {}
    for raw_id, value in (mapping or {}).items():
        norm_id = normalize_quest_id(raw_id)
        if norm_id:
            lookup[norm_id] = value
    return lookup


def _load_chapter_file(snbt_file, lang=None):
    """
    Parse one chapter file into a chapter description.

    Returns a dict with the chapter id, display name, order index, the raw
    quest ids and one entry per quest (name, tasks, rewards, dependencies).
    Never raises: malformed files simply yield ``None``.
    """
    data = read_snbt_file(str(snbt_file))
    if not isinstance(data, dict) or not data:
        # Missing, unparsable or empty file: not a chapter definition.
        return None

    lang = lang or {}
    # Language files use the id as written in the pack; normalise both the
    # legacy '0x...' form and the modern 16 character hex form.
    chapter_names = _normalized_lookup(lang.get('chapters', {}))
    quest_names = _normalized_lookup(lang.get('quests', {}))
    task_titles = _normalized_lookup(lang.get('tasks', {}))
    reward_titles = _normalized_lookup(lang.get('rewards', {}))

    file_id = snbt_file.stem
    chapter_id = _id_text(data.get('id')) or file_id
    norm_chapter_id = normalize_quest_id(chapter_id)

    name = ''
    for key in ('title', 'name'):
        if isinstance(data.get(key), str) and data[key].strip():
            name = _clean_text(data[key])
            break
    if not name:
        name = chapter_names.get(norm_chapter_id) or chapter_names.get(
            normalize_quest_id(file_id)) or file_id

    order_index = data.get('order_index')
    if not isinstance(order_index, (int, float)) or isinstance(order_index, bool):
        order_index = None

    chapter_info = {
        'id': chapter_id,
        'name': name,
        'order_index': order_index,
        'quests': [],
        'quest_entries': [],
    }

    raw_quests = data.get('quests')
    if isinstance(raw_quests, dict):
        raw_quests = list(raw_quests.values())
    if not isinstance(raw_quests, list):
        # Chapter without a quest list (or with an unexpected shape).
        return chapter_info

    for raw_quest in raw_quests:
        entry = _build_quest_entry(
            raw_quest, chapter_info['name'],
            quest_names=quest_names,
            task_titles=task_titles,
            reward_titles=reward_titles,
        )
        if entry is None:
            continue
        chapter_info['quests'].append(entry['id'])
        chapter_info['quest_entries'].append(entry)

    return chapter_info


def _build_quest_entry(raw_quest, chapter_name, quest_names=None,
                       task_titles=None, reward_titles=None):
    """Turn one raw SNBT quest entry into a normalised quest description."""
    quest_names = quest_names or {}
    task_titles = task_titles or {}
    reward_titles = reward_titles or {}

    if isinstance(raw_quest, str):
        quest_data = {}
        quest_id = raw_quest
    elif isinstance(raw_quest, dict):
        quest_data = raw_quest
        quest_id = _id_text(
            quest_data.get('id', quest_data.get('quest_id')))
    else:
        return None

    if not quest_id:
        # Without an id the quest can never be matched to progress; skip it
        # rather than showing a quest that would never leave "up next".
        return None

    norm_id = normalize_quest_id(quest_id)

    dependencies = []
    for dep in _as_list(quest_data.get('dependencies')):
        dep_id = _id_text(dep)
        if dep_id:
            dependencies.append(dep_id)

    tasks = []
    first_task_title = ''
    first_item_id = ''
    for task in _as_list(quest_data.get('tasks')) + _as_list(quest_data.get('subtasks')):
        description = _describe_task(task, task_titles)
        if description:
            tasks.append(description)

        if isinstance(task, dict):
            if not first_task_title:
                first_task_title = _clean_text(task.get('title')) or task_titles.get(
                    normalize_quest_id(_id_text(task.get('id'))), '')
            if not first_item_id:
                first_item_id = _task_item_id(task)

    name = ''
    for key in ('title', 'name'):
        if isinstance(quest_data.get(key), str) and quest_data[key].strip():
            name = _clean_text(quest_data[key])
            break
    if not name:
        name = quest_names.get(norm_id)
    if not name:
        # FTB Quests hides the quest title behind the icon for many quests;
        # fall back to something recognisable instead of a bare hex id.
        name = first_task_title
    if not name:
        name = _icon_id(quest_data)
    if not name:
        name = first_item_id
    if not name:
        name = quest_id

    rewards = []
    for reward in _as_list(quest_data.get('rewards')):
        description = _describe_reward(reward, reward_titles)
        if description:
            rewards.append(description)

    return {
        'id': quest_id,
        'norm_id': norm_id,
        'name': name,
        'chapter': chapter_name,
        'optional': bool(quest_data.get('optional', False)),
        'invisible': bool(quest_data.get('invisible', False)),
        'dependencies': dependencies,
        'tasks': tasks,
        'rewards': rewards,
    }


def _icon_id(quest_data):
    """Return the icon item id of a raw quest entry ('' when absent)."""
    icon = quest_data.get('icon')
    if isinstance(icon, dict):
        return _clean_text(icon.get('id') or '')
    if isinstance(icon, str):
        return _clean_text(icon)
    return ''


def _task_item_id(task):
    """Return the item id a task asks for ('' when not an item task)."""
    if not isinstance(task, dict):
        return ''
    item = task.get('item')
    if isinstance(item, dict):
        return _clean_text(item.get('id') or '')
    if isinstance(item, str):
        return _clean_text(item)
    return _clean_text(task.get('item_id') or '')


def _item_filter_hint(item):
    """Short hint for item tasks that use a filter component (smart filters)."""
    if not isinstance(item, dict):
        return ''
    components = item.get('components')
    if not isinstance(components, dict):
        return ''
    for key, value in components.items():
        if isinstance(value, str) and 'filter' in str(key).lower():
            hint = _clean_text(value).replace('ftbfiltersystem:', '')
            return _truncate(hint, 40)
    return ''


def _describe_task(task, task_titles=None):
    """Build a short human readable description for an FTB Quests task."""
    task_titles = task_titles or {}

    if isinstance(task, str):
        return _clean_text(task)
    if not isinstance(task, dict):
        return ''

    title = _clean_text(task.get('title'))
    if not title:
        title = task_titles.get(normalize_quest_id(_id_text(task.get('id'))), '')

    task_type = _clean_text(task.get('type') or task.get('task') or '').lower()
    detail = ''

    if task_type == 'item' or 'item' in task_type and 'filter' not in task_type:
        detail = _describe_item_task(task)
    elif 'filter' in task_type:
        detail = _describe_item_task(task)
    elif task_type == 'kill':
        target = _clean_text(task.get('entity') or task.get('mob') or '')
        amount = _as_number(task.get('value') or task.get('count'))
        detail = ' '.join(part for part in (
            'Kill', (f'{amount}x' if amount else ''), target) if part)
    elif task_type == 'advancement':
        target = _clean_text(task.get('advancement') or '')
        detail = f'Advancement {target}' if target else ''
    elif task_type == 'dimension':
        target = _friendly_dimension(task.get('dimension'))
        detail = f'Visit {target}' if target else ''
    elif task_type == 'location':
        target = _friendly_dimension(task.get('dimension'))
        detail = f'Reach a location in {target}' if target else 'Reach a location'
    elif task_type == 'stat':
        target = _clean_text(task.get('stat') or '')
        amount = _as_number(task.get('value'))
        if target:
            detail = f'Stat {target}' + (f' = {amount}' if amount is not None else '')
    elif task_type == 'biome':
        target = _clean_text(task.get('biome') or '')
        detail = f'Find biome {target}' if target else ''
    elif task_type == 'structure':
        target = _clean_text(task.get('structure') or '')
        detail = f'Find structure {target}' if target else ''
    elif task_type == 'stage':
        target = _clean_text(task.get('stage') or '')
        detail = f'Unlock stage {target}' if target else ''
    elif task_type == 'fluid':
        target = _clean_text(task.get('fluid') or '')
        amount = _as_number(task.get('value') or task.get('amount'))
        if target:
            detail = 'Obtain ' + (f'{amount}mB ' if amount else '') + target
    elif task_type == 'energy':
        amount = _as_number(task.get('value') or task.get('energy'))
        detail = f'Charge {amount} FE' if amount else 'Charge energy'
    elif task_type in ('xp', 'experience'):
        amount = _as_number(task.get('value') or task.get('xp'))
        detail = f'Earn {amount} XP' if amount else 'Earn XP'
    elif task_type in ('xp_levels', 'xp_level'):
        amount = _as_number(task.get('value') or task.get('xp_levels'))
        if amount:
            detail = f'Reach {amount} XP ' + ('level' if amount == 1 else 'levels')
        else:
            detail = 'Reach an XP level'
    elif task_type == 'checkmark':
        detail = ''
    elif task_type == 'observation':
        detail = 'Observe the objective in game'

    if title and detail:
        description = f'{title} ({detail})'
    else:
        description = title or detail
    return _truncate(description)


def _describe_item_task(task):
    """Describe an item task ('Obtain 64x minecraft:stone')."""
    item = task.get('item')
    item_id = ''
    item_count = None
    if isinstance(item, dict):
        item_id = _clean_text(item.get('id') or '')
        item_count = _as_number(item.get('count'))
    elif isinstance(item, str):
        item_id = _clean_text(item)

    count = _as_number(task.get('count'))
    if count is None:
        count = item_count

    if not item_id:
        item_id = _clean_text(task.get('item_id') or '')
    if not item_id:
        return ''

    if count and count > 1:
        description = f'Obtain {count}x {item_id}'
    else:
        description = f'Obtain {item_id}'

    hint = _item_filter_hint(item)
    if hint:
        description = f'{description} [{hint}]'
    return description


def _describe_reward(reward, reward_titles=None):
    """Build a short human readable description for an FTB Quests reward."""
    reward_titles = reward_titles or {}

    if isinstance(reward, str):
        return _clean_text(reward)
    if not isinstance(reward, dict):
        return ''

    title = _clean_text(reward.get('title'))
    if not title:
        title = reward_titles.get(normalize_quest_id(_id_text(reward.get('id'))), '')

    reward_type = _clean_text(reward.get('type') or '').lower()
    detail = ''

    if reward_type == 'item':
        item = reward.get('item')
        item_id = ''
        item_count = None
        if isinstance(item, dict):
            item_id = _clean_text(item.get('id') or '')
            item_count = _as_number(item.get('count'))
        elif isinstance(item, str):
            item_id = _clean_text(item)
        count = _as_number(reward.get('count'))
        if count is None:
            count = item_count
        if item_id:
            detail = f'{count}x {item_id}' if count and count > 1 else item_id
    elif reward_type in ('xp', 'experience'):
        amount = _as_number(reward.get('xp'))
        detail = f'{amount} XP' if amount is not None else 'XP'
    elif reward_type in ('xp_levels', 'xp_level'):
        amount = _as_number(reward.get('xp_levels') or reward.get('xp'))
        if amount is None:
            detail = 'XP levels'
        else:
            detail = f'{amount} XP ' + ('level' if amount == 1 else 'levels')
    elif reward_type == 'command':
        command = _clean_text(reward.get('command') or '')
        detail = f'Command {command}' if command else 'Command'
    elif reward_type in ('random', 'choice', 'loot', 'all_table'):
        table = _id_text(reward.get('table_id') or '')
        detail = f'Reward table {table}' if table else 'Reward'
    elif reward_type == 'advancement':
        target = _clean_text(reward.get('advancement') or '')
        detail = f'Advancement {target}' if target else ''
    elif reward_type == 'toast':
        target = _clean_text(reward.get('description') or '')
        detail = target or ''
    elif reward_type == 'stage':
        target = _clean_text(reward.get('stage') or '')
        detail = f'Stage {target}' if target else ''
    elif reward_type:
        detail = _clean_text(reward_type)

    if title and detail:
        description = f'{title} ({detail})'
    else:
        description = title or detail
    return _truncate(description)


def load_chapter_definitions(instance_path, lang=None):
    """
    Load chapter definitions from <instance>/config/ftbquests/quests/chapters/*.snbt
    Returns dict of chapter_id -> {id, name, order_index, quests: [quest_id, ...],
    quest_entries: [...]}, in quest-book order.
    """
    chapters = {}
    chapters_dir = Path(instance_path) / 'config' / 'ftbquests' / 'quests' / 'chapters'

    if not chapters_dir.exists():
        return chapters

    if lang is None:
        lang = load_lang_strings(instance_path)

    loaded = []
    for snbt_file in sorted(chapters_dir.glob('*.snbt')):
        try:
            chapter_info = _load_chapter_file(snbt_file, lang)
        except Exception:
            # Tolerant parsing - a broken chapter must not hide the others.
            continue
        if chapter_info is not None:
            loaded.append((snbt_file.stem, chapter_info))

    # Sort by the pack's own chapter order when it is available.
    def sort_key(item):
        stem, info = item
        order = info.get('order_index')
        if isinstance(order, (int, float)) and not isinstance(order, bool):
            return (0, float(order), stem)
        return (1, 0.0, stem)

    for stem, chapter_info in sorted(loaded, key=sort_key):
        chapters[stem] = chapter_info

    return chapters


def load_quest_details(instance_path, chapters=None, lang=None):
    """
    Return every quest of the quest book as a flat list in quest-book order.

    Each item is a dict with:
    ``id``, ``norm_id``, ``name``, ``chapter``, ``optional``, ``invisible``,
    ``dependencies``, ``tasks`` (descriptions) and ``rewards`` (descriptions).
    """
    if chapters is None:
        chapters = load_chapter_definitions(instance_path, lang=lang)
    if lang is None:
        lang = load_lang_strings(instance_path)

    quests = []
    for chapter_info in chapters.values():
        quests.extend(chapter_info.get('quest_entries', []))
    return quests


def build_up_next_details(quest_details, completed_quests, limit=5):
    """
    Build the "Up next (details)" lines of the game state block.

    Quests that can be done right now (all dependencies completed) come first,
    followed by quests that are still locked.  Completed and hidden quests are
    skipped.  Returns an empty list when there is nothing to show.
    """
    completed_norm = {normalize_quest_id(q) for q in completed_quests}
    completed_norm.discard('')

    available = []
    locked = []
    for quest in quest_details or []:
        norm_id = quest.get('norm_id') or normalize_quest_id(quest.get('id'))
        if not norm_id or norm_id in completed_norm:
            continue
        if quest.get('invisible'):
            continue

        dependencies = [normalize_quest_id(dep) for dep in quest.get('dependencies', [])]
        dependencies = [dep for dep in dependencies if dep]
        if all(dep in completed_norm for dep in dependencies):
            available.append(quest)
        else:
            locked.append(quest)

    selected = available[:limit]
    if len(selected) < limit:
        selected.extend(locked[:limit - len(selected)])

    if not selected:
        return []

    lines = ['Up next (details):']
    for index, quest in enumerate(selected, start=1):
        markers = []
        if quest.get('optional'):
            markers.append('optional')
        if quest in locked:
            markers.append('locked')
        marker_text = f" [{' '.join(markers)}]" if markers else ''
        name = quest.get('name') or quest.get('id')
        chapter = quest.get('chapter') or ''
        chapter_text = f' ({chapter})' if chapter and chapter != name else ''
        lines.append(f"{index}. {name}{chapter_text}{marker_text}")

        # A checkmark task often repeats the quest title; do not say it twice.
        tasks = [task for task in quest.get('tasks') or []
                 if task.strip().lower() != name.strip().lower()]
        if tasks:
            lines.append('   Tasks: ' + _join_limited(tasks, 4))
        rewards = quest.get('rewards') or []
        if rewards:
            lines.append('   Rewards: ' + _join_limited(rewards, 3))

    return lines


def _join_limited(items, limit):
    """Join up to ``limit`` items with '; ', noting how many were dropped."""
    shown = [str(item) for item in items[:limit] if str(item).strip()]
    if len(items) > limit:
        shown.append(f'+{len(items) - limit} more')
    return '; '.join(shown)


# ---------------------------------------------------------------------------
# Player basics (experience level and dimension from the world save)
# ---------------------------------------------------------------------------
#
# Player saves are gzipped NBT.  Only the few primitive tags needed to reach
# XpLevel/Dimension are decoded; anything unexpected aborts parsing and the
# feature is skipped silently.

_NBT_END = 0
_NBT_BYTE = 1
_NBT_SHORT = 2
_NBT_INT = 3
_NBT_LONG = 4
_NBT_FLOAT = 5
_NBT_DOUBLE = 6
_NBT_BYTE_ARRAY = 7
_NBT_STRING = 8
_NBT_LIST = 9
_NBT_COMPOUND = 10
_NBT_INT_ARRAY = 11
_NBT_LONG_ARRAY = 12

_MAX_NBT_COLLECTION = 5_000_000


def _decompress_nbt(raw):
    """Return the decompressed payload of an NBT file (gzip/zlib/plain)."""
    if raw[:2] == b'\x1f\x8b':
        return gzip.decompress(raw)
    try:
        return zlib.decompress(raw)
    except zlib.error:
        return raw


def read_nbt_file(filepath):
    """
    Read a (possibly gzipped) NBT file into nested Python dicts/lists.
    Returns None when the file is missing, unreadable or not valid NBT.
    """
    try:
        raw = Path(filepath).read_bytes()
    except (OSError, ValueError):
        return None

    if not raw:
        return None

    try:
        payload = _decompress_nbt(raw)
    except (OSError, EOFError, zlib.error):
        return None

    for expect_name in (True, False):
        try:
            return _parse_nbt(payload, expect_name)
        except (ValueError, IndexError, struct.error, UnicodeDecodeError):
            continue
    return None


def _parse_nbt(data, expect_root_name=True):
    """Parse a single NBT document (see the tag ids above)."""
    position = [0]

    def read(length):
        start = position[0]
        end = start + length
        if length < 0 or end > len(data):
            raise ValueError('unexpected end of NBT data')
        position[0] = end
        return data[start:end]

    def u1():
        return read(1)[0]

    def i4():
        return struct.unpack('>i', read(4))[0]

    def string():
        length = struct.unpack('>H', read(2))[0]
        return read(length).decode('utf-8', 'replace')

    def payload(tag_id):
        if tag_id == _NBT_END:
            return None
        if tag_id == _NBT_BYTE:
            return struct.unpack('>b', read(1))[0]
        if tag_id == _NBT_SHORT:
            return struct.unpack('>h', read(2))[0]
        if tag_id == _NBT_INT:
            return i4()
        if tag_id == _NBT_LONG:
            return struct.unpack('>q', read(8))[0]
        if tag_id == _NBT_FLOAT:
            return struct.unpack('>f', read(4))[0]
        if tag_id == _NBT_DOUBLE:
            return struct.unpack('>d', read(8))[0]
        if tag_id == _NBT_BYTE_ARRAY:
            length = i4()
            if length < 0 or length > _MAX_NBT_COLLECTION:
                raise ValueError('implausible NBT byte array length')
            return read(length)
        if tag_id == _NBT_STRING:
            return string()
        if tag_id == _NBT_LIST:
            item_tag = u1()
            length = i4()
            if item_tag == _NBT_END or length <= 0:
                return []
            if length > _MAX_NBT_COLLECTION:
                raise ValueError('implausible NBT list length')
            return [payload(item_tag) for _ in range(length)]
        if tag_id == _NBT_COMPOUND:
            result = {}
            while True:
                child_tag = u1()
                if child_tag == _NBT_END:
                    return result
                name = string()
                result[name] = payload(child_tag)
        if tag_id == _NBT_INT_ARRAY:
            length = i4()
            if length < 0 or length > _MAX_NBT_COLLECTION:
                raise ValueError('implausible NBT int array length')
            return list(struct.unpack('>%di' % length, read(4 * length)))
        if tag_id == _NBT_LONG_ARRAY:
            length = i4()
            if length < 0 or length > _MAX_NBT_COLLECTION:
                raise ValueError('implausible NBT long array length')
            return list(struct.unpack('>%dq' % length, read(8 * length)))
        raise ValueError('unknown NBT tag %d' % tag_id)

    root_tag = u1()
    if root_tag == _NBT_END:
        return {}
    if expect_root_name:
        string()  # root compound name, usually empty
    return payload(root_tag)


def _find_player_record(data):
    """Locate the compound that holds XpLevel/Dimension in an NBT document."""
    if not isinstance(data, dict):
        return None

    for key in ('Player', 'player'):
        if isinstance(data.get(key), dict):
            return data[key]

    inner = data.get('Data')
    if isinstance(inner, dict):
        if isinstance(inner.get('Player'), dict):
            return inner['Player']
        if 'XpLevel' in inner or 'Dimension' in inner:
            return inner

    if 'XpLevel' in data or 'Dimension' in data:
        return data
    return None


def _player_data_candidates(world_dir):
    """Yield player save files, most recently written first."""
    playerdata_dir = Path(world_dir) / 'playerdata'
    candidates = []
    if playerdata_dir.is_dir():
        for path in playerdata_dir.glob('*.dat'):
            try:
                candidates.append((path.stat().st_mtime, path))
            except OSError:
                continue
    candidates.sort(key=lambda item: item[0], reverse=True)

    for _, path in candidates:
        yield path

    level_dat = Path(world_dir) / 'level.dat'
    if level_dat.is_file():
        yield level_dat


def read_player_basics(instance_path, world_name):
    """
    Best effort read of the player's experience level and dimension.

    Returns ``{'level': int or None, 'dimension': str or None}``.  When nothing
    is readable both values stay None and the caller simply omits the line.
    """
    info = {'level': None, 'dimension': None}

    world_dir = Path(instance_path) / 'saves' / world_name
    if not world_dir.is_dir():
        return info

    for candidate in _player_data_candidates(world_dir):
        record = _find_player_record(read_nbt_file(candidate))
        if not record:
            continue

        level = _as_number(record.get('XpLevel'))
        dimension = record.get('Dimension') or record.get('dimension')
        if level is not None and info['level'] is None:
            info['level'] = level
        if isinstance(dimension, str) and dimension.strip() and not info['dimension']:
            info['dimension'] = _friendly_dimension(dimension)

        if info['level'] is not None and info['dimension']:
            break

    return info


# ---------------------------------------------------------------------------
# Game state assembly
# ---------------------------------------------------------------------------

def _player_line(instance_path, world_name):
    """Build the optional 'Player: level X, dimension Y' line."""
    try:
        basics = read_player_basics(instance_path, world_name)
    except Exception:
        # Player basics are a nice-to-have; never fail the whole state.
        return None

    parts = []
    if basics.get('level') is not None:
        parts.append(f"level {basics['level']}")
    if basics.get('dimension'):
        parts.append(f"dimension {basics['dimension']}")
    if not parts:
        return None
    return 'Player: ' + ', '.join(parts)


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
        completed_norm = {normalize_quest_id(q) for q in completed_quests}
        completed_norm.discard('')

        # Load quest book definitions and language strings
        lang = load_lang_strings(instance_path)
        chapters = load_chapter_definitions(instance_path, lang=lang)
        quest_details = load_quest_details(instance_path, chapters=chapters, lang=lang)

        # Names of quests and chapters (chapters first, then quests)
        quest_names = dict(lang.get('chapters', {}))
        quest_names.update(lang.get('quests', {}))
        names_by_norm = {}
        for raw_id, name in quest_names.items():
            names_by_norm[normalize_quest_id(raw_id)] = name

        # Quest entries know fallbacks the language file does not (task titles,
        # icon ids), so prefer those names when available.
        for quest in quest_details:
            norm_id = quest.get('norm_id')
            if norm_id and quest.get('name'):
                names_by_norm[norm_id] = quest['name']

        # Build chapter completion info
        total_chapters = len(chapters)
        completed_chapters = 0

        for chapter_info in chapters.values():
            chapter_quests = chapter_info.get('quests', [])
            if not chapter_quests:
                continue

            # Count completed quests in this chapter
            completed_in_chapter = sum(
                1 for q in chapter_quests
                if normalize_quest_id(q) in completed_norm
            )

            if completed_in_chapter >= len(chapter_quests):
                completed_chapters += 1

        # Total quests
        all_quest_ids = set()
        for chapter_info in chapters.values():
            all_quest_ids.update(chapter_info.get('quests', []))
        all_quest_norm = {normalize_quest_id(q) for q in all_quest_ids}
        all_quest_norm.discard('')

        total_quests = len(all_quest_norm)
        total_completed = len(all_quest_norm & completed_norm)

        # Get completed quest names (up to 10)
        completed_with_names = sorted(
            names_by_norm.get(norm_id, norm_id) for norm_id in completed_norm
        )[:10]

        # Get incomplete quest names in quest-book order (up to 10)
        incomplete_with_names = []
        seen_incomplete = set()
        for quest in quest_details:
            norm_id = quest.get('norm_id') or normalize_quest_id(quest.get('id'))
            if not norm_id or norm_id in completed_norm or norm_id in seen_incomplete:
                continue
            if quest.get('invisible'):
                # Hidden quests (authors' placeholder entries) are not "next".
                seen_incomplete.add(norm_id)
                continue
            seen_incomplete.add(norm_id)
            incomplete_with_names.append(quest.get('name') or quest.get('id'))
        for norm_id in sorted(all_quest_norm):
            if norm_id in completed_norm or norm_id in seen_incomplete:
                continue
            seen_incomplete.add(norm_id)
            incomplete_with_names.append(names_by_norm.get(norm_id, norm_id))
        incomplete_with_names = incomplete_with_names[:10]

        # Build the game state text
        state_lines = []
        state_lines.append(f"World: {world_name}")

        player_line = _player_line(instance_path, world_name)
        if player_line:
            state_lines.append(player_line)

        state_lines.append(f"Chapters: {completed_chapters}/{total_chapters} completed")
        state_lines.append(f"Quests: {total_completed}/{total_quests} completed")

        if completed_with_names:
            state_lines.append(f"Completed quests: {', '.join(completed_with_names)}")

        if incomplete_with_names:
            state_lines.append(f"Next quests: {', '.join(incomplete_with_names)}")

        up_next_lines = build_up_next_details(quest_details, completed_quests)
        state_lines.extend(up_next_lines)

        return '\n'.join(state_lines)

    except Exception as e:
        return f"Save not readable: {str(e)}"


if __name__ == '__main__':
    # Test with sample paths
    print("Game State Reader - Test Mode")
    print("Use via build_game_state(instance_path, world_name)")
