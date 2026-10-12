#!/usr/bin/env python3
"""Offline, read-only lexical suggestions; never evidence of a user's qualifications."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys
import unicodedata

DEFAULT_CV = Path(__file__).resolve().parent.parent / "data" / "base-cv.md"
STOPWORDS = frozenset("""
    a an and are as at be been being but by can could did do does doing for from
    had has have having he her hers him his how i if in into is it its me more
    most my no nor not of on or our ours out over own s same she should so some
    such t than that the their theirs them themselves then there these they this
    those through to too under up us very was we were what when where which while
    who whom why will with would you your yours
    apply application candidate candidates company employer employment job jobs
    looking must preferred required requirements responsibilities role team work
""".split())
# Unicode letters/digits, optionally with language suffixes; underscores separate words.
WORD_RE = re.compile(r"[^\W_]+(?:\+\+|#)?", re.UNICODE)


def term_counts(text: str) -> Counter[str]:
    """Count meaningful unigrams and contiguous bi/trigrams within phrase boundaries."""
    text = unicodedata.normalize("NFKC", text).casefold()
    counts: Counter[str] = Counter()
    run: list[str] = []
    end = 0
    for match in WORD_RE.finditer(text):
        gap = text[end:match.start()]
        # Only horizontal whitespace and hyphens connect words into phrases.
        if any(char not in " \t-" for char in gap):
            run.clear()
        end = match.end()
        word = match.group()
        if word in STOPWORDS or not any(char.isalpha() for char in word):
            run.clear()
            continue
        run.append(word)
        run = run[-3:]
        for length in range(1, len(run) + 1):
            counts[" ".join(run[-length:])] += 1
    return counts


def missing_keywords(posting: str, cv: str, top: int = 20) -> list[tuple[str, int]]:
    """Sort missing terms by count, phrase length, then lexical order (stable ties)."""
    if top <= 0:
        raise ValueError("top must be a positive integer")
    covered = term_counts(cv)
    missing = [(term, count) for term, count in term_counts(posting).items()
               if term not in covered]
    missing.sort(key=lambda item: (-item[1], -len(item[0].split()), item[0]))
    return missing[:top]


def positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer") from None
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def read_input(raw_path: str, label: str) -> str:
    """Give actionable errors without printing private file contents."""
    try:
        return Path(raw_path).expanduser().read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise ValueError(f"{label} file not found: {raw_path}") from None
    except UnicodeError:
        raise ValueError(f"{label} must be UTF-8 text: {raw_path}") from None
    except (OSError, RuntimeError, ValueError):
        raise ValueError(f"cannot read {label} file: {raw_path}") from None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("posting", help="posting text file (UTF-8)")
    parser.add_argument("--cv", default=str(DEFAULT_CV), metavar="PATH",
                        help="base CV (default: this skill's data/base-cv.md)")
    parser.add_argument("--top", type=positive_int, default=20, metavar="N",
                        help="maximum suggestions, positive integer (default: 20)")
    args = parser.parse_args(argv)
    try:
        posting = read_input(args.posting, "posting")
        cv = read_input(args.cv, "CV")
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    results = missing_keywords(posting, cv, args.top)
    if not results:
        print("No missing keywords found.")
    for term, count in results:
        print(f"{count}\t{term}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
