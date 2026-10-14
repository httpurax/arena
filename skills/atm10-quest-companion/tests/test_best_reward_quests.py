"""Stdlib-only, zero-network regression checks for the reward guide.

The fixture is a reviewed extraction from AllTheMods/ATM-10 main commit
 e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025 (8.2, 2026-09-22):
chapters/<key>.snbt and lang/en_us/chapters/<key>.snbt under
config/ftbquests/quests/. Preserve raw titles, tasks, dependencies, full rewards
and descriptions, not inferred item display names. No pack checkout is needed.
These checks detect guide drift against the snapshot, not upstream pack changes.
"""

import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "references/best-reward-quests.md"
FIXTURE = ROOT / "tests/fixtures/best_reward_quests.json"
spec = importlib.util.spec_from_file_location(
    "reward_title_builder", ROOT / "scripts/build_chapter_list.py"
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

# Independently reviewed ids and normalized titles; keep punctuation/case exact.
TITLES = {
    '5CF320E9C4C1B1E1': 'Welcome to Getting Started!',
    '637981B64BBE0D92': 'Charging Gadgets',
    '378C95C18798D413': 'Tool Belt',
    '36836AD948F96B9F': 'Item Pipez',
    '33433A443B65D252': 'Fluid Pipez',
    '53EC96FA0E7C4ED4': 'Energy Pipez',
    '58514FDE153FD971': 'Iron Chest',
    '3E33730DC2115D26': 'Gold Chest',
    '485D5664A17E16DF': 'Copper Upgrade',
    '1E1EB7DC19DDCFB7': 'Netherite Template',
    '4A4C71C43519D5FE': 'Summoning The Wither',
    '201EE3566D4D3123': 'Allthemodium Ingot',
    '07FDA46D83F8360D': 'Teleport Pad',
    '46D756F4DC6CC894': 'Netherite Backpack',
    '6B2027DA7AA6FF34': 'Welcome to Powah!!!',
    '67D40A1A9332C03D': 'Legendary Ink',
    '7408CCF998D9CD37': 'Ancient Codex',
    '445C21949ADA1FE3': 'Allthemodium Spell Book',
    '4A01C5F5DCF32C19': 'Soul Elytra',
    '0D2F07FC0F804223': 'Valkyrie Queen',
    '73201E591C2A40CC': 'Star Shards',
    '5436157FDFC9633E': 'Fully Automated ATM Star',
    '2A976D41F79C34B1': None,
    '6D09511D64DDC282': 'Kill The Warden',
    '051E0C85E7B71CE0': 'The Metal Age',
    '76406EFFF8CBA6B4': "We've Struck Diamonds!",
}


def fixed_payoff(quest):
    """Render only item rewards; outer reward count takes precedence."""
    result = []
    for reward in quest['rewards']:
        if reward['type'] != 'item':
            continue
        stack = reward['item']
        item = stack['id'] if isinstance(stack, dict) else stack
        count = reward.get('count', stack.get('count', 1)
                           if isinstance(stack, dict) else 1)
        rendered = '`{}` ×{}'.format(item, count)
        if isinstance(stack, dict) and stack.get('components'):
            rendered += '; components: `' + json.dumps(
                stack['components'], separators=(',', ':'), sort_keys=True) + '`'
        result.append(rendered)
    return '<br>'.join(result)


def table_rows(text):
    rows = []
    for line in text.splitlines():
        if line.startswith('| `'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) != 5:
                raise ValueError('Malformed reward row')
            rows.append(cells)
    return rows


def validate_rows(text, verified):
    """Reject unknown ids, invented/derived titles, wrong chapter or payoff."""
    seen = set()
    for chapter, title, qid, payoff, why in table_rows(text):
        qid = qid.strip('`')
        if qid not in verified or qid in seen:
            raise ValueError('Unknown or duplicate quest id')
        seen.add(qid)
        entry = verified[qid]
        raw = entry['title_raw']
        expected = ('**' + builder.normalize_title(raw) + '**' if raw
                    else '*(no explicit title in config)*')
        if title != expected:
            raise ValueError('Unverified quest title')
        if chapter != '`' + entry['chapter'] + '`':
            raise ValueError('Wrong chapter')
        if payoff != fixed_payoff(entry['quest']):
            raise ValueError('Unverified reward/count/components')
        if not why:
            raise ValueError('Missing judgement')
    return seen


class TestBestRewardQuests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding='utf-8')
        cls.fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
        cls.verified = {q['quest']['id']: q for q in cls.fixture['quests']}

    def test_pinned_provenance(self):
        self.assertEqual(self.fixture['commit'],
                         'e5e3d1d83ec6885bb9a5e9fb309fb8e9730db025')
        self.assertEqual(self.fixture['pack_version'], '8.2')
        self.assertEqual(self.fixture['date'], '2026-09-22')
        for value in ('e5e3d1d83e', self.fixture['commit'], '2026-09-22',
                      'pack 8.2', 'config/ftbquests/quests/chapters/',
                      'config/ftbquests/quests/lang/en_us/chapters/'):
            self.assertIn(value, self.text)

    def test_verified_titles_and_ids(self):
        self.assertEqual(set(self.verified), set(TITLES))
        self.assertEqual(len(self.fixture['quests']), len(TITLES))
        for qid, expected in TITLES.items():
            raw = self.verified[qid]['title_raw']
            self.assertEqual(builder.normalize_title(raw) if raw else None, expected)
            self.assertIn('`' + qid + '`', self.text)
            if expected:
                self.assertIn('**' + expected + '**', self.text)

    def test_chapter_titles_are_verified_and_findable(self):
        chapters = {q['chapter']: builder.normalize_title(q['chapter_title_raw'])
                    for q in self.fixture['quests']}
        self.assertEqual(len(chapters), 10)
        for key, title in chapters.items():
            self.assertIn('- `{}` → **{}**.'.format(key, title), self.text)

    def test_no_invented_names_in_emphasized_prose(self):
        # Named entries are bold in both prose and tables. Only these non-name
        # emphasis labels are exempt; a new plausible quest name must fail.
        labels = {
            '2026-09-22', 'All the Mods 10', 'pack 8.2', 'What this page is.',
            'Beginner answer (judgement):',
            'All priority order, “worth it” reasoning, and beginner/later groupings are judgement (approximate)',
            'Every named quest title below is quoted from the config',
            'It does not reward an Allthemodium ingot in this snapshot.',
            'The in-game quest book (FTB Quests) is authoritative.',
            'and', 'fixed `item` rewards only', 'judgement (approximate)',
            'not', 'task item id',
        }
        allowed = labels | {title for title in TITLES.values() if title}
        allowed |= {builder.normalize_title(q['chapter_title_raw'])
                    for q in self.fixture['quests']}

        def unknown_names(text):
            emphasized = {' '.join(x.split()) for x in
                          re.findall(r'\*\*(.*?)\*\*', text, re.DOTALL)}
            return emphasized - allowed

        self.assertFalse(unknown_names(self.text))
        self.assertEqual(unknown_names(self.text + '\nTry **Free ATM Starter Kit**.'),
                         {'Free ATM Starter Kit'})

    def test_complete_pick_list_and_exact_fixed_rewards(self):
        seen = validate_rows(self.text, self.verified)
        caution_only = {'6D09511D64DDC282', '051E0C85E7B71CE0', '76406EFFF8CBA6B4'}
        self.assertEqual(seen, set(TITLES) - caution_only)
        self.assertGreaterEqual(len({self.verified[q]['chapter'] for q in seen}), 9)

    def test_no_invented_title_or_id_in_tables(self):
        for old, new in [
            ('**Item Pipez**', '**Free Pipe Starter Kit**'),
            ('*(no explicit title in config)*', '**Pipez Advanced Upgrade Quest**'),
            ('`36836AD948F96B9F`', '`0000000000000000`'),
            ('`pipez:item_pipe` ×16', '`pipez:item_pipe` ×64'),
            ('`pipez:item_pipe` ×16', '`pipez:imaginary_pipe` ×16'),
        ]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                validate_rows(self.text.replace(old, new), self.verified)

    def test_no_unknown_ids_or_namespaced_identifiers_anywhere(self):
        ids = set(re.findall(r'`([0-9A-F]{16})`', self.text))
        self.assertEqual(ids, set(TITLES))
        identifiers = set(re.findall(r'\b[a-z][a-z0-9_]*:[a-z][a-z0-9_/]*', self.text))
        source = json.dumps(self.fixture)
        allowed = set(re.findall(r'\b[a-z][a-z0-9_]*:[a-z][a-z0-9_/]*', source))
        self.assertFalse(identifiers - allowed, identifiers - allowed)

    def test_critical_rewards_are_not_confused_with_tasks(self):
        cube = self.verified['637981B64BBE0D92']['quest']
        self.assertEqual(cube['tasks'][0]['item']['id'], 'charginggadgets:charging_station')
        reward = next(r for r in cube['rewards'] if r['type'] == 'item')
        self.assertEqual(reward['item']['id'], 'mekanism:basic_energy_cube')
        self.assertEqual(reward['item']['components']['mekanism:energy'],
                         {'energy_containers': [4000000]})
        warden = self.verified['6D09511D64DDC282']['quest']
        items = [r['item'] for r in warden['rewards'] if r['type'] == 'item']
        self.assertEqual(items, [{'count': 1, 'id': 'minecraft:potion', 'components': {
            'minecraft:potion_contents': {'potion': 'potionsmaster:allthemodium'}}}])
        self.assertIn('**It does not reward an Allthemodium ingot in this snapshot.**', self.text)
        self.assertEqual(self.verified['2A976D41F79C34B1']['quest']['tasks'][0]['item']['id'],
                         'pipez:filter_destination_tool')

    def test_random_and_loot_cautions_match_config(self):
        for qid, reward_type in [('637981B64BBE0D92', 'random'),
                                 ('051E0C85E7B71CE0', 'loot'),
                                 ('76406EFFF8CBA6B4', 'loot')]:
            reward = next(r for r in self.verified[qid]['quest']['rewards']
                          if r['type'] == reward_type)
            self.assertTrue(reward['exclude_from_claim_all'])
            self.assertIn('table_id', reward)
        self.assertIn('This page does not evaluate their', self.text)
        self.assertIn('reward-table contents or claim odds', self.text)

    def test_dependencies_not_free_first_items(self):
        for qid in ('201EE3566D4D3123', '1E1EB7DC19DDCFB7',
                    '73201E591C2A40CC', '5436157FDFC9633E'):
            self.assertTrue(self.verified[qid]['quest']['dependencies'])
        terminal = self.verified['5436157FDFC9633E']['quest']
        self.assertEqual(len(terminal['dependencies']), 10)
        self.assertEqual(terminal['tasks'][0]['item']['id'], 'allthetweaks:atm_star')
        self.assertNotIn('allthetweaks:atm_star',
                         [r['item']['id'] for r in terminal['rewards'] if r['type'] == 'item'])

    def test_grounding_and_skill_wiring(self):
        for phrase in ('**The in-game quest book (FTB Quests) is authoritative.**',
                       'judgement (approximate)', 'No recipes, coordinates, dimension routes',
                       'not a quest title or a reward', 'JEI', 'not the complete reward list'):
            self.assertIn(phrase, self.text)
        skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('version: 1.4.0', skill)

        self.assertIn('references/best-reward-quests.md', skill)
        self.assertIn('which quests are worth doing for their rewards', skill)


if __name__ == '__main__':
    unittest.main()
