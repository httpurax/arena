"""Tests for the quest-book detail features of gamestate.py.

Covers the "Up next (details)" section (task and reward descriptions), the
tolerant handling of missing chapter/task/reward fields and the best effort
player basics (experience level / dimension).  Everything runs offline
against local fixtures or temporary directories.
"""

import gzip
import shutil
import struct
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gamestate import (
    build_game_state,
    build_up_next_details,
    extract_completed_quests,
    load_chapter_definitions,
    load_lang_strings,
    load_quest_details,
    normalize_quest_id,
    parse_snbt,
    read_nbt_file,
    read_player_basics,
)

DETAILS_FIXTURE = Path(__file__).parent / 'fixtures' / 'details'


@pytest.fixture
def details_instance():
    """Path to the quest-book fixtures with tasks and rewards."""
    return str(DETAILS_FIXTURE)


@pytest.fixture
def temp_instance():
    """Create an empty temporary instance directory."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


def write_chapter(instance_path, filename, content):
    """Write a chapter file into a temporary instance."""
    chapters = (Path(instance_path) / 'config' / 'ftbquests' / 'quests' / 'chapters')
    chapters.mkdir(parents=True, exist_ok=True)
    (chapters / filename).write_text(content, encoding='utf-8')


def write_progress(instance_path, world_name, content):
    """Write an FTB Quests progress file into a temporary instance."""
    progress = Path(instance_path) / 'saves' / world_name / 'ftbquests'
    progress.mkdir(parents=True, exist_ok=True)
    (progress / 'team.snbt').write_text(content, encoding='utf-8')


def up_next_lines(state):
    """Return only the 'Up next (details)' block of a game state string."""
    lines = state.splitlines()
    if 'Up next (details):' not in lines:
        return []
    start = lines.index('Up next (details):')
    block = [lines[start]]
    for line in lines[start + 1:]:
        if line and not line[0].isdigit() and not line.startswith(' '):
            break
        block.append(line)
    return block


class TestRealWorldSNBT:
    """FTB Quests writes SNBT without commas and with '//' inside strings."""

    def test_newline_separated_fields(self):
        result = parse_snbt(
            '{\n\tfilename: "alpha"\n\tid: "AAAA000000000001"\n'
            '\tquest_links: [ ]\n}'
        )
        assert result['filename'] == 'alpha'
        assert result['id'] == 'AAAA000000000001'
        assert result['quest_links'] == []

    def test_double_slash_inside_string_is_not_a_comment(self):
        result = parse_snbt(
            '{\n\tclick: "https://discord.gg/allthemods"\n\tid: "ABC"\n}'
        )
        assert result['click'] == 'https://discord.gg/allthemods'
        assert result['id'] == 'ABC'

    def test_real_comment_still_removed(self):
        result = parse_snbt('{\n\t// a comment\n\tid: "ABC" // trailing\n}')
        assert result == {'id': 'ABC'}

    def test_crlf_chapter_file(self, temp_instance):
        write_chapter(
            temp_instance, 'windows.snbt',
            '{\r\n\tid: "DDDD000000000001"\r\n\torder_index: 2\r\n'
            '\tquests: [ ]\r\n}\r\n',
        )
        chapters = load_chapter_definitions(temp_instance)
        assert chapters['windows']['id'] == 'DDDD000000000001'
        assert chapters['windows']['order_index'] == 2

    def test_numeric_suffixes(self):
        result = parse_snbt('{value: 5L, size: 1.5d, xp_levels: 2}')
        assert result['value'] == 5
        assert result['xp_levels'] == 2
        # Unknown numeric type suffix is kept as text but must not crash.
        assert result['size'] == pytest.approx(1.5)

    def test_nested_inline_item(self):
        result = parse_snbt(
            '{tasks: [{id: "T1", item: { count: 1, id: "minecraft:stone" }, '
            'type: "item"}]}'
        )
        task = result['tasks'][0]
        assert task['item'] == {'count': 1, 'id': 'minecraft:stone'}


class TestQuestDetailsLoading:
    """Chapter, quest, task and reward data is loaded from the fixture pack."""

    def test_chapters_are_in_quest_book_order(self, details_instance):
        chapters = load_chapter_definitions(details_instance)
        assert list(chapters.keys()) == ['alpha', 'beta']
        assert chapters['alpha']['name'] == 'Alpha Chapter'
        assert chapters['beta']['order_index'] is None

    def test_chapter_name_falls_back_to_language_file(self, details_instance):
        chapters = load_chapter_definitions(details_instance)
        assert chapters['beta']['name'] == 'Beta Chapter'

    def test_quest_names_come_from_language_file(self, details_instance):
        quests = {q['id']: q for q in load_quest_details(details_instance)}
        # Colour codes are stripped for the prompt.
        assert quests['AAAA00000000000A']['name'] == 'Gather Wood'
        assert quests['AAAA00000000000B']['name'] == 'Fight the Night'

    def test_task_descriptions(self, details_instance):
        quests = {q['id']: q for q in load_quest_details(details_instance)}

        # Item task with an outer total count takes precedence over item.count
        assert 'Obtain 64x minecraft:stone' in quests['AAAA00000000000C']['tasks']
        # Kill task
        assert 'Kill 5x minecraft:zombie' in quests['AAAA00000000000B']['tasks']
        # Dimension task uses a friendly name
        assert 'Visit The Nether' in quests['AAAA00000000000E']['tasks']
        # Checkmark task uses the lang task title
        assert 'Say hello' in quests['AAAA00000000000A']['tasks']

    def test_reward_descriptions(self, details_instance):
        quests = {q['id']: q for q in load_quest_details(details_instance)}
        assert quests['AAAA00000000000A']['rewards'] == ['2 XP levels']
        assert quests['AAAA00000000000B']['rewards'] == ['16x minecraft:bread']
        assert quests['AAAA00000000000E']['rewards'] == ['50 XP']

    def test_quest_without_tasks_or_rewards(self, details_instance):
        quests = {q['id']: q for q in load_quest_details(details_instance)}
        assert quests['BBBB00000000000A']['tasks'] == []
        assert quests['BBBB00000000000B']['tasks'] == []
        assert quests['BBBB00000000000B']['rewards'] == []

    def test_quest_without_id_is_skipped(self, details_instance):
        chapters = load_chapter_definitions(details_instance)
        beta = chapters['beta']
        # The fixture has five raw quest entries, one of which has no id.
        assert len(beta['quests']) == 4
        assert 'Quest without an id' not in [q['name'] for q in beta['quest_entries']]

    def test_name_falls_back_to_quest_id(self, details_instance):
        quests = {q['id']: q for q in load_quest_details(details_instance)}
        assert quests['BBBB00000000000B']['name'] == 'BBBB00000000000B'

    def test_name_falls_back_to_task_title(self, details_instance):
        quests = {q['id']: q for q in load_quest_details(details_instance)}
        assert quests['BBBB00000000000C']['name'] == 'Smelt some iron'

    def test_lang_strings_are_structured(self, details_instance):
        lang = load_lang_strings(details_instance)
        assert lang['quests']['AAAA00000000000B'] == 'Fight the Night'
        assert lang['chapters']['BBBB000000000001'] == 'Beta Chapter'
        assert lang['tasks']['AAAA0000000000A2'] == 'Say hello'


class TestUpNextDetails:
    """The 'Up next (details)' section of the GAME STATE block."""

    def test_section_is_present(self, details_instance):
        state = build_game_state(details_instance, 'worldA')
        assert 'Up next (details):' in state

    def test_lists_incomplete_quests_with_tasks_and_rewards(self, details_instance):
        state = build_game_state(details_instance, 'worldA')
        block = up_next_lines(state)

        assert block[0] == 'Up next (details):'
        assert '1. Fight the Night (Alpha Chapter)' in block
        assert '   Tasks: Kill 5x minecraft:zombie' in block
        assert '   Rewards: 16x minecraft:bread' in block

    def test_completed_quests_are_not_listed(self, details_instance):
        state = build_game_state(details_instance, 'worldA')
        block = '\n'.join(up_next_lines(state))
        assert 'Gather Wood' not in block

    def test_invisible_quests_are_not_listed(self, details_instance):
        state = build_game_state(details_instance, 'worldA')
        assert 'Hidden Placeholder' not in state

    def test_at_most_five_quests_are_listed(self, details_instance):
        state = build_game_state(details_instance, 'worldA')
        numbered = [line for line in up_next_lines(state) if line[:1].isdigit()]
        assert len(numbered) == 5

    def test_optional_and_locked_markers(self, details_instance):
        state = build_game_state(details_instance, 'worldA')
        block = '\n'.join(up_next_lines(state))
        assert '2. Stockpile Stone (Alpha Chapter) [optional]' in block

        details = load_quest_details(details_instance)
        completed = extract_completed_quests(details_instance, 'worldA')
        extended = '\n'.join(build_up_next_details(details, completed, limit=10))
        assert '7. Into the Nether (Alpha Chapter) [locked]' in extended

    def test_quest_without_tasks_only_has_a_header_line(self, details_instance):
        details = load_quest_details(details_instance)
        completed = extract_completed_quests(details_instance, 'worldA')
        lines = build_up_next_details(details, completed, limit=10)
        index = lines.index('3. Beta Starter (Beta Chapter)')
        assert lines[index + 1].startswith(('4. ', 'Up next'))

    def test_many_tasks_and_rewards_are_capped(self, temp_instance):
        tasks = '\n'.join(
            '\t\t\t\t{\n\t\t\t\t\tid: "EEEE0000000000%02X"\n'
            '\t\t\t\t\titem: { count: 1, id: "minecraft:item_%d" }\n'
            '\t\t\t\t\ttype: "item"\n\t\t\t\t}' % (i, i)
            for i in range(6)
        )
        rewards = '\n'.join(
            '\t\t\t\t{\n\t\t\t\t\tid: "FFFF0000000000%02X"\n'
            '\t\t\t\t\ttype: "xp"\n\t\t\t\t\txp: %d\n\t\t\t\t}' % (i, 10 * i)
            for i in range(5)
        )
        write_chapter(temp_instance, 'many.snbt', (
            '{\n\tid: "EEEE000000000001"\n\torder_index: 0\n'
            '\tquests: [{\n\t\tid: "EEEE00000000000A"\n'
            '\t\ttasks: [\n' + tasks + '\n\t\t]\n'
            '\t\trewards: [\n' + rewards + '\n\t\t]\n\t}]\n}'
        ))

        lines = build_up_next_details(load_quest_details(temp_instance), set())
        tasks_line = next(line for line in lines if line.startswith('   Tasks:'))
        rewards_line = next(line for line in lines if line.startswith('   Rewards:'))
        assert tasks_line.count('minecraft:item_') == 4
        assert '+2 more' in tasks_line
        assert rewards_line.count(' XP') == 3
        assert '+2 more' in rewards_line

    def test_no_section_when_nothing_is_incomplete(self, temp_instance):
        write_chapter(temp_instance, 'small.snbt', (
            '{\n\tid: "CCCC000000000001"\n'
            '\tquests: [{ id: "CCCC00000000000A" }]\n}'
        ))
        write_progress(temp_instance, 'worldC',
                       '{ completed: ["CCCC00000000000A"] }')
        state = build_game_state(temp_instance, 'worldC')
        assert 'Up next (details):' not in state
        assert 'Quests: 1/1 completed' in state


class TestGracefulDegradation:
    """Missing chapters, tasks, rewards or language data must never crash."""

    def test_no_chapters_directory(self, temp_instance):
        write_progress(temp_instance, 'worldA',
                       '{ completed: ["AAAA00000000000A"] }')
        state = build_game_state(temp_instance, 'worldA')
        assert 'World: worldA' in state
        assert 'Up next (details):' not in state

    def test_chapter_without_quests_key(self, temp_instance):
        write_chapter(temp_instance, 'gamma.snbt',
                      '{ id: "CCCC000000000001", filename: "gamma" }')
        chapters = load_chapter_definitions(temp_instance)
        assert chapters['gamma']['quests'] == []
        state = build_game_state(temp_instance, 'worldA')
        assert 'Chapters: 0/1 completed' in state

    def test_malformed_chapter_does_not_hide_good_ones(self, temp_instance):
        write_chapter(temp_instance, 'broken.snbt', '{ this is not valid snbt')
        write_chapter(temp_instance, 'good.snbt', (
            '{\n\tid: "DDDD000000000001"\n\torder_index: 0\n'
            '\tquests: [{\n\t\tid: "DDDD00000000000A"\n'
            '\t\ttasks: [{ id: "DDDD0000000000A1", type: "checkmark" }]\n\t}]\n}'
        ))
        chapters = load_chapter_definitions(temp_instance)
        assert list(chapters.keys()) == ['good']

        state = build_game_state(temp_instance, 'worldA')
        assert 'Up next (details):' in state
        assert 'DDDD00000000000A' in state

    def test_chapter_quests_is_not_a_list(self, temp_instance):
        write_chapter(temp_instance, 'odd.snbt',
                      '{ id: "DDDD000000000001", quests: "nope" }')
        chapters = load_chapter_definitions(temp_instance)
        assert chapters['odd']['quests'] == []

    def test_quest_tasks_is_a_dict(self, temp_instance):
        write_chapter(temp_instance, 'odd.snbt', (
            '{\n\tid: "DDDD000000000001"\n\tquests: [{\n'
            '\t\tid: "DDDD00000000000A"\n'
            '\t\ttasks: { one: { id: "T1", type: "checkmark" } }\n'
            '\t\trewards: "none"\n\t}]\n}'
        ))
        state = build_game_state(temp_instance, 'worldA')
        assert 'Up next (details):' in state

    def test_missing_language_files(self, temp_instance):
        write_chapter(temp_instance, 'alpha.snbt', (
            '{\n\tid: "AAAA000000000001"\n'
            '\tquests: [{\n\t\tid: "AAAA00000000000A"\n'
            '\t\ttasks: [{ id: "AAAA0000000000A1", item: '
            '{ count: 1, id: "minecraft:oak_log" }, type: "item" }]\n\t}]\n}'
        ))
        state = build_game_state(temp_instance, 'worldA')
        # Without a language file the quest falls back to its first item id.
        assert '1. minecraft:oak_log (alpha)' in state
        assert 'Tasks: Obtain minecraft:oak_log' in state

    def test_task_without_type_is_ignored(self, temp_instance):
        write_chapter(temp_instance, 'alpha.snbt', (
            '{\n\tid: "AAAA000000000001"\n'
            '\tquests: [{\n\t\tid: "AAAA00000000000A"\n'
            '\t\ttasks: [{ id: "AAAA0000000000A1" }, {}]\n'
            '\t\trewards: [{ id: "AAAA0000000000A2" }]\n\t}]\n}'
        ))
        state = build_game_state(temp_instance, 'worldA')
        assert 'Up next (details):' in state
        assert '1. AAAA00000000000A' in state


class TestIdNormalisation:
    """Chapter ids and progress ids use different spellings."""

    def test_ids_match_with_and_without_prefix(self, temp_instance):
        write_chapter(temp_instance, 'alpha.snbt', (
            '{\n\tid: "AAAA000000000001"\n'
            '\tquests: [{\n\t\tid: "AAAA00000000000A"\n'
            '\t\ttasks: [{ id: "T1", type: "checkmark" }]\n\t}]\n}'
        ))
        # Old style progress file (0x prefix, lower case).
        write_progress(temp_instance, 'worldA',
                       '{ progress: { quests: [0x00010001] } }')
        assert normalize_quest_id('0x00010001') == '00010001'
        assert normalize_quest_id('"AAAA00000000000A"') == 'AAAA00000000000A'

        state = build_game_state(temp_instance, 'worldA')
        assert 'Up next (details):' in state  # AAAA... is still incomplete
        assert 'Quests: 0/1 completed' in state


# ---------------------------------------------------------------------------
# Best effort player basics
# ---------------------------------------------------------------------------

def _nbt_string(value):
    encoded = value.encode('utf-8')
    return struct.pack('>H', len(encoded)) + encoded


def _nbt_int(value):
    return struct.pack('>i', value)


def _nbt_compound(entries):
    body = b''
    for tag_id, name, payload in entries:
        body += bytes([tag_id]) + _nbt_string(name) + payload
    return body + b'\x00'


def _write_nbt(path, payload, compress=True):
    document = b'\x0a' + _nbt_string('') + payload
    if compress:
        document = gzip.compress(document)
    Path(path).write_bytes(document)


def write_player(instance_path, world_name, level=12,
                 dimension='minecraft:the_nether', compress=True):
    """Write a minimal playerdata/<uuid>.dat file."""
    playerdata = Path(instance_path) / 'saves' / world_name / 'playerdata'
    playerdata.mkdir(parents=True, exist_ok=True)
    payload = _nbt_compound([
        (3, 'XpLevel', _nbt_int(level)),
        (8, 'Dimension', _nbt_string(dimension)),
        (3, 'XpTotal', _nbt_int(1234)),
    ])
    _write_nbt(playerdata / '00000000-0000-0000-0000-000000000001.dat',
               payload, compress=compress)


class TestPlayerBasics:
    """Experience level and dimension are read when the save allows it."""

    def test_reads_level_and_dimension(self, temp_instance):
        write_player(temp_instance, 'worldA', level=12,
                     dimension='minecraft:the_nether')
        basics = read_player_basics(temp_instance, 'worldA')
        assert basics['level'] == 12
        assert basics['dimension'] == 'The Nether'

    def test_player_line_in_game_state(self, temp_instance):
        write_player(temp_instance, 'worldA', level=7,
                     dimension='minecraft:overworld')
        state = build_game_state(temp_instance, 'worldA')
        assert 'Player: level 7, dimension Overworld' in state

    def test_level_dat_player_tag(self, temp_instance):
        world = Path(temp_instance) / 'saves' / 'worldB'
        world.mkdir(parents=True)
        player = _nbt_compound([
            (3, 'XpLevel', _nbt_int(3)),
            (8, 'Dimension', _nbt_string('minecraft:the_end')),
        ])
        _write_nbt(world / 'level.dat',
                   _nbt_compound([(10, 'Player', player)]))
        basics = read_player_basics(temp_instance, 'worldB')
        assert basics['level'] == 3
        assert basics['dimension'] == 'The End'

    def test_uncompressed_playerdata(self, temp_instance):
        write_player(temp_instance, 'worldC', level=4,
                     dimension='minecraft:overworld', compress=False)
        assert read_player_basics(temp_instance, 'worldC')['level'] == 4

    def test_missing_save_is_silent(self, temp_instance):
        state = build_game_state(temp_instance, 'worldA')
        assert 'Player:' not in state

    def test_corrupt_playerdata_is_silent(self, temp_instance):
        playerdata = Path(temp_instance) / 'saves' / 'worldA' / 'playerdata'
        playerdata.mkdir(parents=True)
        (playerdata / 'broken.dat').write_bytes(b'this is not nbt')
        assert read_player_basics(temp_instance, 'worldA') == {
            'level': None, 'dimension': None}
        assert 'Player:' not in build_game_state(temp_instance, 'worldA')

    def test_read_nbt_file_missing(self, temp_instance):
        assert read_nbt_file(Path(temp_instance) / 'nope.dat') is None
