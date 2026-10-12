#!/usr/bin/env python3
"""Offline tests for the study-deck data contract.

These tests use only the Python standard library. They parse the bundled template's
JSON-compatible example data and exercise a small Python mirror of the validation
rules in scripts/verify-deck.js, so the suite does not require Node or a network.
"""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_ROOT / "assets" / "flashcard-quiz-app.html"
MARK_START = "const STUDY_DATA = "
MARK_END = "/* ==================== END STUDY DATA"


def extract_data_block(html: str) -> str:
    """Extract the data expression from the bundled HTML template."""
    start = html.find(MARK_START)
    end = html.find(MARK_END)
    if start < 0 or end < 0 or end < start:
        raise ValueError("STUDY DATA markers not found")
    block = html[start + len(MARK_START):end].strip()
    if block.endswith(";"):
        block = block[:-1].rstrip()
    return block


def data_block_errors(block: str) -> list[str]:
    """Return inline-script hazards prohibited by the skill's data-block contract."""
    errors = []
    if "<" in block:
        errors.append('raw "<" inside the data block')
    if "</script" in block:
        errors.append("literal </script> inside the data block")
    if "<!--" in block:
        errors.append("literal <!-- inside the data block")
    return errors


def deck_errors(deck: Any) -> list[str]:
    """Mirror the bundled verifier's documented shape and quiz-answer checks."""
    errors: list[str] = []
    if not isinstance(deck, dict):
        return ["STUDY_DATA is not an object"]
    if not isinstance(deck.get("title"), str) or not deck["title"].strip():
        errors.append("title is missing or empty")

    flashcards = deck.get("flashcards")
    quiz = deck.get("quiz")
    if not isinstance(flashcards, list):
        errors.append("flashcards is not an array")
        flashcards = []
    if not isinstance(quiz, list):
        errors.append("quiz is not an array")
        quiz = []

    ids = [card.get("id") if isinstance(card, dict) else None for card in flashcards]
    if any(value == previous for index, value in enumerate(ids) for previous in ids[:index]):
        errors.append("flashcard ids are not unique")
    for index, card in enumerate(flashcards, start=1):
        if not isinstance(card, dict):
            errors.append(f"flashcard {index} is not an object")
            continue
        for field in ("id", "front", "back"):
            value = card.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f'flashcard {index} field "{field}" is missing or empty')

    for index, item in enumerate(quiz, start=1):
        if not isinstance(item, dict):
            errors.append(f"quiz {index} is not an object")
            continue
        question = item.get("question")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"quiz {index} question is missing")
        item_type = item.get("type")
        if item_type not in ("mc", "tf", "short"):
            errors.append(f'quiz {index} has unknown type "{item_type}"')
            continue
        answer = item.get("answer")
        if item_type == "mc":
            options = item.get("options")
            if not isinstance(options, list) or len(options) != 4:
                errors.append(f"quiz {index} must have exactly 4 options")
            elif type(answer) is not int or answer < 0 or answer >= len(options):
                errors.append(f"quiz {index} answer is not a valid option index")
        elif item_type == "tf":
            if type(answer) is not bool:
                errors.append(f"quiz {index} tf answer must be a boolean")
        elif not isinstance(answer, str) or not answer.strip():
            errors.append(f"quiz {index} short answer must be non-empty text")

    return errors


def valid_deck() -> dict[str, Any]:
    """Minimal valid fixture covering each supported quiz type."""
    return {
        "title": "Offline fixture",
        "flashcards": [{"id": "c1", "front": "Question", "back": "Answer"}],
        "quiz": [
            {
                "id": "q1",
                "type": "mc",
                "question": "Choose the answer",
                "options": ["A", "B", "C", "D"],
                "answer": 0,
            },
            {"id": "q2", "type": "tf", "question": "A statement", "answer": True},
            {"id": "q3", "type": "short", "question": "Explain", "answer": "A concise answer"},
        ],
    }


class DeckContractTests(unittest.TestCase):
    def test_bundled_template_data_is_safe_and_valid(self) -> None:
        block = extract_data_block(TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual([], data_block_errors(block))
        deck = json.loads(block)
        self.assertEqual([], deck_errors(deck))

    def test_flashcard_ids_must_be_unique(self) -> None:
        deck = valid_deck()
        deck["flashcards"].append(copy.deepcopy(deck["flashcards"][0]))
        self.assertIn("flashcard ids are not unique", deck_errors(deck))

    def test_multiple_choice_requires_four_options_and_an_in_range_integer(self) -> None:
        deck = valid_deck()
        deck["quiz"][0]["answer"] = 4
        self.assertTrue(any("valid option index" in error for error in deck_errors(deck)))

        deck = valid_deck()
        deck["quiz"][0]["options"].pop()
        self.assertIn("quiz 1 must have exactly 4 options", deck_errors(deck))

        deck = valid_deck()
        deck["quiz"][0]["answer"] = True
        self.assertTrue(any("valid option index" in error for error in deck_errors(deck)))

    def test_true_false_answer_must_be_a_boolean(self) -> None:
        deck = valid_deck()
        deck["quiz"][1]["answer"] = 1
        self.assertIn("quiz 2 tf answer must be a boolean", deck_errors(deck))

    def test_short_answer_must_be_nonempty_text(self) -> None:
        deck = valid_deck()
        deck["quiz"][2]["answer"] = "  "
        self.assertIn("quiz 3 short answer must be non-empty text", deck_errors(deck))

    def test_inline_data_block_rejects_raw_less_than_and_breakout_markers(self) -> None:
        for unsafe in ('{"front":"a < b"}', '{"value":"</script>"}', '{"value":"<!--"}'):
            with self.subTest(unsafe=unsafe):
                self.assertTrue(data_block_errors(unsafe))

        escaped = json.dumps({"front": "a < b"}).replace("<", r"\u003c")
        self.assertEqual([], data_block_errors(escaped))


if __name__ == "__main__":
    unittest.main()
