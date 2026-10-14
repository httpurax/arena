#!/usr/bin/env python3
"""snbt.py - a small, strict-enough SNBT (stringified NBT) parser, stdlib-only.

ATM10's FTB Quests config (``config/ftbquests/quests/**.snbt``) is SNBT with one
non-standard relaxation: compound and array entries are separated by newlines
instead of commas, so the files carry no commas at all. This parser accepts both
comma- and whitespace-separated entries (and a trailing comma), ``#`` and ``//``
line comments, single- and double-quoted strings with the usual backslash escapes,
and NBT number suffixes (``b``, ``s``, ``l``, ``i`` -> int; ``f``, ``d`` -> float).

The result is plain Python data: compounds are ``dict``, arrays are ``list``,
strings are ``str``, integers and floats are ``int``/``float`` (suffix dropped),
and ``true``/``false`` are ``bool``. Bare (unquoted) values that are neither
numbers nor booleans are returned as strings, matching Mojang's lenient reader.

Every failure raises :class:`SnbtError` with a one-line message that names the
line and column and quotes the offending source, so callers can show it to a
user as-is. Nothing here touches the network, the filesystem, or ``import``s
beyond the standard library's ``re``.

Example (after importing this module as ``snbt``)::

    data = snbt.parse(path.read_text(encoding="utf-8-sig"))
    print(data["filename"], data["group"], len(data["quests"]))
"""

from __future__ import annotations

import re
from typing import Any, Optional

__all__ = ["SnbtError", "parse", "loads"]


class SnbtError(ValueError):
    """A malformed SNBT document. The message is a single user-facing line."""


# Whitespace per the SNBT grammar (the pack's files use CRLF and tabs).
_WHITESPACE = " \t\r\n"

# Number forms: an optional sign, then an integer/decimal/exponent body, then an
# optional single-letter NBT suffix. `\d+f` is accepted as a float (Mojang
# writes floats that way); the `i` suffix is accepted for symmetry with `bls`.
_NUMBER_RE = re.compile(
    r"^[+-]?(?:"
    r"(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?[fFdD]?"
    r"|\d+[eE][+-]?\d+[fFdD]?"
    r"|\d+[fFdDbBsSiIlL]?"
    r")$"
)
_INT_SUFFIXES = frozenset("bBsSiIlL")
_FLOAT_SUFFIXES = frozenset("fFdD")

# Characters that end a bare (unquoted) token: every other character - letters,
# digits, '.', '/', ':', '$', '+', '-', '_' - is allowed inside one, because lang
# keys look like ``quest.00AB12CD34EF56AB.title`` and values can be bare
# ``minecraft:stone``-style identifiers.
_TOKEN_BREAKS = _WHITESPACE + "{}[],:"

# Backslash escapes inside quoted strings. An escaped backslash yields one
# literal backslash, which is why ``"Extended \\& Advanced AE"`` parses to the
# three characters ``\&`` in front of "Advanced": that is the pack's own way of
# writing a literal ampersand that Minecraft must not read as a formatting code.
_ESCAPES = {
    "\\": "\\",
    '"': '"',
    "'": "'",
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "b": "\b",
    "f": "\f",
    "/": "/",
}


def _describe(text: str, position: int) -> str:
    """Render ``line X, column Y`` plus a quoted excerpt of the offending line."""
    line = text.count("\n", 0, position) + 1
    line_start = text.rfind("\n", 0, position) + 1
    line_end = text.find("\n", position)
    if line_end == -1:
        line_end = len(text)
    column = position - line_start + 1
    excerpt = text[line_start:line_end].strip()
    if len(excerpt) > 60:
        excerpt = excerpt[:57] + "..."
    return f"line {line}, column {column}: {excerpt!r}"


class _Parser:
    """A cursor over one SNBT document. Never reused."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.position = 0

    def error(self, message: str, position: Optional[int] = None) -> SnbtError:
        where = _describe(self.text, self.position if position is None else position)
        return SnbtError(f"{message} at {where}")

    # ------------------------------------------------------------------
    # whitespace and comments
    # ------------------------------------------------------------------

    def skip_ignored(self) -> None:
        """Skip whitespace and ``#`` / ``//`` line comments."""
        text, end = self.text, len(self.text)
        while self.position < end:
            char = text[self.position]
            if char in _WHITESPACE:
                self.position += 1
                continue
            if char == "#":
                self.position = text.find("\n", self.position)
                if self.position == -1:
                    self.position = end
                continue
            if char == "/" and text.startswith("//", self.position):
                self.position = text.find("\n", self.position)
                if self.position == -1:
                    self.position = end
                continue
            break

    def at_end(self) -> bool:
        self.skip_ignored()
        return self.position >= len(self.text)

    def peek(self) -> str:
        return self.text[self.position] if self.position < len(self.text) else ""

    # ------------------------------------------------------------------
    # grammar
    # ------------------------------------------------------------------

    def parse_document(self) -> Any:
        """Parse one top-level value and require clean end-of-input after it."""
        value = self.parse_value()
        self.skip_ignored()
        if self.position < len(self.text):
            raise self.error(
                f"unexpected text after the document ends ({self.peek()!r}); "
                f"a SNBT file holds exactly one value"
            )
        return value

    def parse_value(self) -> Any:
        self.skip_ignored()
        char = self.peek()
        if char == "":
            raise self.error("expected a value but reached the end of the document")
        if char == "{":
            return self.parse_compound()
        if char == "[":
            return self.parse_array()
        if char in "\"'":
            return self.parse_quoted_string()
        return self.parse_bare_token()

    def parse_compound(self) -> "dict[str, Any]":
        """``{ key: value key2: value2 }`` - separators (commas) optional."""
        self.position += 1  # consume '{'
        result: "dict[str, Any]" = {}
        while True:
            self.skip_ignored()
            char = self.peek()
            if char == "":
                raise self.error("unterminated compound: expected another key or '}'")
            if char == "}":
                self.position += 1
                return result
            if char == ",":  # tolerate a separator or trailing comma
                self.position += 1
                continue
            start = self.position
            key = self.parse_key()
            self.skip_ignored()
            if self.peek() != ":":
                raise self.error(
                    f"expected ':' after the key {key!r}", start
                )
            self.position += 1  # consume ':'
            if key in result:
                raise self.error(f"duplicate key {key!r}", start)
            result[key] = self.parse_value()

    def parse_array(self) -> "list[Any]":
        """``[ value value ]`` - commas optional, a ``[I; ...]`` typed prefix slipped."""
        start = self.position
        self.position += 1  # consume '['
        self.skip_ignored()
        # A typed-array prefix ([B; [I; [L;) is legal NBT; treat the items as ints.
        char = self.peek()
        if char and char in "bBlLiI":
            letter_position = self.position
            self.position += 1
            self.skip_ignored()
            if self.peek() == ";":
                self.position += 1
            else:
                self.position = letter_position  # not a type letter after all
        items: "list[Any]" = []
        while True:
            self.skip_ignored()
            char = self.peek()
            if char == "":
                raise self.error("unterminated array: expected another value or ']'", start)
            if char == "]":
                self.position += 1
                return items
            if char == ",":
                self.position += 1
                continue
            items.append(self.parse_value())

    def parse_key(self) -> str:
        """A quoted string or one bare token (dots and digits included)."""
        if self.peek() in "\"'":
            return self.parse_quoted_string()
        return self.parse_bare_token(what="a key")

    def parse_quoted_string(self) -> str:
        quote = self.peek()
        start = self.position
        self.position += 1
        out: "list[str]" = []
        text, end = self.text, len(self.text)
        while self.position < end:
            char = text[self.position]
            if char == "\\":
                if self.position + 1 >= end:
                    break
                nxt = text[self.position + 1]
                if nxt == "u":
                    digits = text[self.position + 2:self.position + 6]
                    if len(digits) != 4 or not all(d in "0123456789abcdefABCDEF" for d in digits):
                        raise self.error(
                            f"\\u must be followed by exactly four hex digits (got {digits!r})"
                        )
                    out.append(chr(int(digits, 16)))
                    self.position += 6
                    continue
                if nxt not in _ESCAPES:
                    raise self.error(f"unknown escape sequence \\{nxt}; use \\\\ for a backslash")
                out.append(_ESCAPES[nxt])
                self.position += 2
                continue
            if char == quote:
                self.position += 1
                return "".join(out)
            out.append(char)
            self.position += 1
        raise self.error(f"unterminated string starting here (missing closing {quote})", start)

    def parse_bare_token(self, what: str = "a value") -> Any:
        start = self.position
        text, end = self.text, len(self.text)
        while self.position < end and text[self.position] not in _TOKEN_BREAKS:
            self.position += 1
        token = text[start:self.position]
        if not token:
            raise self.error(
                f"expected {what} but found {self.peek()!r}"
            )
        if token == "true":
            return True
        if token == "false":
            return False
        if _NUMBER_RE.match(token):
            return self._to_number(token)
        return token

    def _to_number(self, token: str) -> Any:
        suffix = token[-1]
        if suffix in _FLOAT_SUFFIXES:
            return float(token[:-1])
        if suffix in _INT_SUFFIXES:
            return int(token[:-1])
        body, _, fraction = token.partition(".")
        if fraction or "e" in token.lower():
            return float(token)
        try:
            return int(body)
        except ValueError:  # a bare '+' or lone digits guard; cannot happen per regex
            raise self.error(f"malformed number {token!r}")


def parse(text: str) -> Any:
    """Parse one SNBT document given as text; raise SnbtError on any problem."""
    if not isinstance(text, str):
        raise SnbtError(f"snbt.parse expects a str, got {type(text).__name__}")
    if text.startswith("\ufeff"):  # a stray BOM is invisible noise, drop it
        text = text[1:]
    if not text.strip():
        raise SnbtError("the document is empty: expected a value")
    return _Parser(text).parse_document()


def loads(text: str) -> Any:
    """Alias for :func:`parse`, mirroring the ``json`` module's naming."""
    return parse(text)
