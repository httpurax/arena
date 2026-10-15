#!/usr/bin/env python3
"""Grounding checks for `references/trading-economy.md`.

Trade is data: `items/trade/trade_*.ltx` per trader, `presets/trade_presets.ltx`
and the `gamma_wp_preset.ltx` / `gamma_nato_preset.ltx` supply ladders, plus the
Economy addon's price patches and `part_prices.ltx`. This suite pins the trader
files, the condition factors and exponents and the headline price figures.

Run with the standard library only, offline:

    python3 tests/test_trading_economy.py [-v]
"""

import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DOC = SKILL_DIR / "references" / "trading-economy.md"


class TradingEconomyDoc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_exists_and_names_its_sources(self):
        self.assertTrue(DOC.is_file())
        for source in (
            "trade_presets.ltx",
            "gamma_wp_preset.ltx",
            "gamma_nato_preset.ltx",
            "part_prices.ltx",
        ):
            with self.subTest(source=source):
                self.assertIn(source, self.text)

    def test_trader_files_are_named(self):
        for trader in (
            "trade_stalker_sidorovich.ltx",
            "trade_generic_mechanic.ltx",
            "trade_bandit.ltx",
            "trade_csky_spore.ltx",
        ):
            with self.subTest(trader=trader):
                self.assertIn(trader, self.text)

    def test_condition_factors_and_exponents(self):
        for value in (
            "buy_item_condition_factor = 0.05",
            "buy_item_condition_factor = 0.01",
            "buy_item_exponent = 2.25",
            "buy_item_exponent = 1.75",
            "sell_item_exponent = 0.75",
        ):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_mechanic_toolkit_gate(self):
        self.assertIn("toolkit_task_done", self.text)
        self.assertIn("drugkit_task_done", self.text)

    def test_classifier_groups_are_documented(self):
        for group in (
            "[merchant]",
            "[barman]",
            "[medic]",
            "[scientist]",
            "[mechanic]",
            "[common_stock]",
        ):
            with self.subTest(group=group):
                self.assertIn(group, self.text)

    def test_bloc_map_comes_from_the_trader_files(self):
        for value in ("trade_greh", "trade_monolith", "supply_1_nato", "supply_1_wp", "upgr_w_1_internal"):
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_headline_kit_prices(self):
        self.assertIn("150 000", self.text)
        self.assertIn("45 000", self.text)

    def test_supply_ladder_and_no_gear_rule(self):
        self.assertIn("supplies_5", self.text)
        self.assertIn("sell_item_exponent", self.text)

    def test_pointer_to_the_other_guides(self):
        for sibling in (
            "references/factions.md",
            "references/weapons.md",
            "references/crafting-repairs.md",
            "references/artifacts.md",
        ):
            with self.subTest(sibling=sibling):
                self.assertIn(sibling, self.text)


if __name__ == "__main__":
    unittest.main()
