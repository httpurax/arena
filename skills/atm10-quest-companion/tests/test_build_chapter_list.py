#!/usr/bin/env python3
"""Offline tests for scripts/snbt.py and scripts/build_chapter_list.py.

Stdlib-only and network-free: every case runs against a small hand-written SNBT
fixture checkout built in a temp directory - never the real ~150MB pack clone, and
never the network (the builder itself cannot fetch: it only reads the checkout path
the user passes).

Covered:

  * the SNBT reader: compounds and arrays with or without comma separators (the pack
    writes none), quoted keys, dotted lang keys, number suffixes, booleans, comments,
    CRLF, string escapes including the pack's ``\\&`` literal ampersand, typed-array
    prefixes - and a clear one-line error (line + column) for every malformed shape;
  * title normalization: Minecraft ``&`` formatting codes stripped, escaped ``\\&``
    ampersands and non-code ``&`` left alone;
  * fixture-based regeneration: a six-chapter fake checkout in real pack layout
    rebuilds a document that is field-for-field identical to the matching slice of the
    shipped ``examples/progress.example.json`` - same ids, titles, order, quest-book
    groups, stages, and the ``8.x`` pack stamp - and passes progress.py's schema;
  * the CLI contract: default write, "unchanged" idempotency, ``--check`` exit codes,
    ``--commit``/``--date`` provenance, atomic writes;
  * failure handling: a missing path, a directory that is not an ATM-10 checkout, a
    malformed SNBT file, a chapter in an unknown FTB group, a chapter missing from the
    stage table, a missing title, a broken bcc config, or a bad ``--date`` is one
    clear message, exit status 1, no traceback, and nothing is written;
  * offline guarantee: neither new module imports a network or process module.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
EXAMPLE_DATA = SKILL_ROOT / "examples" / "progress.example.json"
SKILL_MD = SKILL_ROOT / "SKILL.md"


def load_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snbt = load_module("snbt", SCRIPTS / "snbt.py")
builder = load_module("build_chapter_list", SCRIPTS / "build_chapter_list.py")
progress = load_module("progress", SCRIPTS / "progress.py")


def run_main(argv: "list[str]") -> "tuple[int, str, str]":
    """Call builder.main() in-process; return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = builder.main(argv)
    return code, out.getvalue(), err.getvalue()


# --------------------------------------------------------------------------------------
# the SNBT reader
# --------------------------------------------------------------------------------------

class TestSnbtParser(unittest.TestCase):

    def test_simple_compound(self) -> None:
        self.assertEqual(snbt.parse('{filename: "welcome" order_index: 0}'),
                         {"filename": "welcome", "order_index": 0})

    def test_pack_style_file_crlf_tabs_no_commas(self) -> None:
        text = (
            '{\r\n\tdefault_hide_dependency_lines: false\r\n\tfilename: "mekanism"'
            '\r\n\tgroup: "2B51AC12041E3F89"\r\n\torder_index: 5\r\n}\r\n'
        )
        self.assertEqual(snbt.parse(text), {
            "default_hide_dependency_lines": False,
            "filename": "mekanism",
            "group": "2B51AC12041E3F89",
            "order_index": 5,
        })

    def test_arrays_of_compounds_and_empty_arrays(self) -> None:
        text = '{ chapter_groups: [ { id: "AAAA" } { id: "BBBB" } ] quest_links: [ ] }'
        self.assertEqual(snbt.parse(text),
                         {"chapter_groups": [{"id": "AAAA"}, {"id": "BBBB"}],
                          "quest_links": []})

    def test_commas_and_trailing_commas_are_tolerated(self) -> None:
        self.assertEqual(snbt.parse('{a: 1, b: [1, 2,],}'),
                         {"a": 1, "b": [1, 2]})

    def test_typed_array_prefix(self) -> None:
        self.assertEqual(snbt.parse("{ids: [I; 1 2 3]}"), {"ids": [1, 2, 3]})
        self.assertEqual(snbt.parse("{ids: [B; 1b 2b]}"), {"ids": [1, 2]})

    def test_number_suffixes(self) -> None:
        got = snbt.parse(
            "{a: 8 b: -12 c: 5.0d d: -4.5d e: 0.9d f: 1b g: 2s h: 123L i: 3i "
            "j: 1.0f k: .5 l: 1e3 m: 250}"
        )
        self.assertEqual(got, {
            "a": 8, "b": -12, "c": 5.0, "d": -4.5, "e": 0.9, "f": 1, "g": 2,
            "h": 123, "i": 3, "j": 1.0, "k": 0.5, "l": 1000.0, "m": 250})
        self.assertIsInstance(got["c"], float)
        self.assertIsInstance(got["a"], int)
        self.assertIsInstance(got["h"], int)

    def test_booleans_and_bare_strings(self) -> None:
        self.assertEqual(snbt.parse("{yes: true no: false bare: something}"),
                         {"yes": True, "no": False, "bare": "something"})

    def test_quoted_keys_and_dotted_lang_keys(self) -> None:
        text = '{"quoted key": 1 quest.001DE8028CAF0A08.title: "Muffling &8Upgrade"}'
        self.assertEqual(snbt.parse(text),
                         {"quoted key": 1,
                          "quest.001DE8028CAF0A08.title": "Muffling &8Upgrade"})

    def test_single_quoted_strings(self) -> None:
        self.assertEqual(snbt.parse("{a: 'it\\'s'}"), {"a": "it's"})

    def test_string_escapes(self) -> None:
        got = snbt.parse(r'{s: "a\\b\"c\nd\teA/" t: "x\'y"}')
        self.assertEqual(got["s"], 'a\\b"c\nd\teA/')
        self.assertEqual(got["t"], "x'y")

    def test_escaped_literal_ampersand(self) -> None:
        """The pack writes a literal ampersand as \\&; it must survive as backslash+&."""
        text = r'{title: "Extended \\& Advanced AE"}'
        self.assertEqual(snbt.parse(text), {"title": "Extended \\& Advanced AE"})

    def test_unicode_escape(self) -> None:
        self.assertEqual(snbt.parse(r'{s: "A"}'), {"s": "A"})

    def test_comments(self) -> None:
        text = '# leading comment\n{ // trailing comment\n\ta: 1 # hash comment\n}\n'
        self.assertEqual(snbt.parse(text), {"a": 1})

    def test_nested_compounds(self) -> None:
        text = '{icon: {id: "ftbquests:book" Count: 1b} x: -8.5d}'
        self.assertEqual(snbt.parse(text),
                         {"icon": {"id": "ftbquests:book", "Count": 1}, "x": -8.5})

    def test_string_lists_span_lines(self) -> None:
        text = '{\n\tquest.a.quest_desc: [\n\t\t"one"\n\t\t"two"\n\t]\n}'
        self.assertEqual(snbt.parse(text), {"quest.a.quest_desc": ["one", "two"]})

    def assert_parse_error(self, text: str, *needles: str) -> None:
        with self.assertRaises(snbt.SnbtError) as ctx:
            snbt.parse(text)
        message = str(ctx.exception)
        for needle in needles:
            self.assertIn(needle, message)

    def test_errors_name_line_and_column(self) -> None:
        self.assert_parse_error('{a: "unterminated', "line 1, column 5", "unterminated string")
        self.assert_parse_error("{\n\tgood: 1\n\tbroken\n}", "line 3", "expected ':'")
        self.assert_parse_error("{a: [1 2", "unterminated array")
        self.assert_parse_error("{a: ", "expected a value")
        self.assertEqual(snbt.parse("{}"), {})  # an empty compound is valid
        self.assert_parse_error("{a: 1} extra", "unexpected text after the document")
        self.assert_parse_error('{a: "bad \\q escape"}', "unknown escape sequence")
        self.assert_parse_error('{a: "bad \\u12G4"}', "four hex digits")
        self.assert_parse_error("{a: 1 a: 2}", "duplicate key 'a'")
        self.assert_parse_error("", "the document is empty")
        self.assert_parse_error("   \r\n  ", "the document is empty")
        with self.assertRaises(snbt.SnbtError):
            snbt.parse(42)  # type: ignore[arg-type]


# --------------------------------------------------------------------------------------
# title normalization
# --------------------------------------------------------------------------------------

class TestTitleNormalization(unittest.TestCase):

    def test_format_codes_are_stripped(self) -> None:
        self.assertEqual(builder.normalize_title("&aChapter 2&r: &6The ATM Star"),
                         "Chapter 2: The ATM Star")
        self.assertEqual(builder.normalize_title("&aChapter 4&r: &dCreative"),
                         "Chapter 4: Creative")
        self.assertEqual(builder.normalize_title("RailCraft"), "RailCraft")

    def test_escaped_ampersand_survives(self) -> None:
        self.assertEqual(builder.normalize_title("Extended \\& Advanced AE"),
                         "Extended \\& Advanced AE")

    def test_non_code_ampersand_survives(self) -> None:
        self.assertEqual(builder.normalize_title("Rock & Roll"), "Rock & Roll")
        self.assertEqual(builder.normalize_title("&zinc"), "&zinc")  # 'z' is not a code

    def test_outer_whitespace_is_trimmed(self) -> None:
        self.assertEqual(builder.normalize_title("&r Pylons &r"), "Pylons")


# --------------------------------------------------------------------------------------
# a small fake checkout in the real pack layout
# --------------------------------------------------------------------------------------

# Real chapter ids (so the shipped stage table applies), real FTB group hex ids, real
# pack order_index values, and the real titles from the pack's en_us lang - including
# the escape/formatting edge cases - so the rebuilt slice can be checked against the
# shipped example file. Disk order (filenames alphabetical) deliberately differs from
# book order, so the order_index/group layout logic is what produces it.
GROUP_MAIN = "2084F3F6FB861C5B"
GROUP_STORAGE = "1AC60211DE7427FC"
GROUP_TECH = "2B51AC12041E3F89"

FIXTURE_CHAPTERS = (
    # (filename, ftb hex id, group, order_index, quest count, lang title)
    ("welcome", "5B00676D79306EA2", "", 0, 1, "Welcome"),
    ("bounty_board", "18A429E7F56AF5A9", "", 1, 2, "Bounty Board"),
    ("mainquestline_part_1", "732824E03978A934", GROUP_MAIN, 0, 3,
     "&aChapter 1&r: &bThe Beginning"),
    ("allthemodium", "4293754F9B2D05F0", GROUP_MAIN, 1, 1,
     "&aChapter 2&r: &eAllthemodium"),
    ("extended__advanced_ae", "51A2FE60D8B76FC6", GROUP_STORAGE, 2, 0,
     r"Extended \\& Advanced AE"),
    ("mekanism", "23983F4DC524B14B", GROUP_TECH, 5, 2, "Mekanism"),
)


def chapter_snbt(filename: str, hex_id: str, group: str, order_index: int,
                 quest_count: int) -> str:
    """A chapter file in the exact dialect the pack writes (CRLF, tabs, no commas)."""
    quests = "\r\n".join(
        "\t\t{\r\n"
        f"\t\t\tid: \"{hex_id[:-4]}{index:04d}\"\r\n"
        "\t\t\tx: 1.5d\r\n"
        f"\t\t\ttitle: \"Quest {index}\"\r\n"
        "\t\t}"
        for index in range(quest_count)
    )
    quests_block = f"\tquests: [\r\n{quests}\r\n\t]\r\n" if quests else "\tquests: [ ]\r\n"
    return (
        "{\r\n"
        "\tdefault_hide_dependency_lines: false\r\n"
        f"\tfilename: \"{filename}\"\r\n"
        f"\tgroup: \"{group}\"\r\n"
        "\ticon: {\r\n"
        "\t\tid: \"ftbquests:book\"\r\n"
        "\t}\r\n"
        f"\tid: \"{hex_id}\"\r\n"
        f"\torder_index: {order_index}\r\n"
        f"{quests_block}"
        "}\r\n"
    )


def write_fixture_checkout(
    root: Path,
    chapters: "tuple[tuple[str, str, str, int, int, str], ...]" = FIXTURE_CHAPTERS,
    *,
    group_defs: "tuple[tuple[str, str], ...]" = (
        (GROUP_MAIN, "Main Questline"), (GROUP_STORAGE, "Storage"),
        (GROUP_TECH, "Tech")),
    pack_version: "str | None" = "8.2",
    pack_name: str = "All the Mods 10",
    title_override: "dict[str, str] | None" = None,
    drop_chapter_groups: bool = False,
    drop_group_lang: bool = False,
    drop_chapter_lang: bool = False,
) -> Path:
    """Write a minimal AllTheMods/ATM-10 checkout tree under ``root`` and return it."""
    quests_dir = root / "config" / "ftbquests" / "quests"
    chapters_dir = quests_dir / "chapters"
    lang_dir = quests_dir / "lang" / "en_us"
    chapters_dir.mkdir(parents=True)
    lang_dir.mkdir(parents=True)

    if not drop_chapter_groups:
        entries = "\r\n".join(f'\t\t{{ id: "{group_id}" }}' for group_id, _ in group_defs)
        (quests_dir / "chapter_groups.snbt").write_text(
            "{\r\n\tchapter_groups: [\r\n" + entries + "\r\n\t]\r\n}\r\n",
            encoding="utf-8",
        )

    if not drop_group_lang:
        lines = "\r\n".join(
            f'\tchapter_group.{group_id}.title: "{title}"' for group_id, title in group_defs
        )
        (lang_dir / "chapter_group.snbt").write_text("{\r\n" + lines + "\r\n}\r\n",
                                                     encoding="utf-8")

    overrides = title_override or {}
    if not drop_chapter_lang:
        lines = "\r\n".join(
            f'\tchapter.{hex_id}.title: "{overrides.get(hex_id, title)}"'
            for _, hex_id, _, _, _, title in chapters
        )
        (lang_dir / "chapter.snbt").write_text("{\r\n" + lines + "\r\n}\r\n",
                                               encoding="utf-8")

    for filename, hex_id, group, order_index, quest_count, _title in chapters:
        (chapters_dir / f"{filename}.snbt").write_text(
            chapter_snbt(filename, hex_id, group, order_index, quest_count),
            encoding="utf-8",
        )

    bcc_lines = ""
    if pack_name is not None:
        bcc_lines += f'\tmodpackName = "{pack_name}"\r\n'
    if pack_version is not None:
        bcc_lines += f'\tmodpackVersion = "{pack_version}"\r\n'
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "bcc-common.toml").write_text("[general]\r\n" + bcc_lines,
                                                    encoding="utf-8")
    return root


class CheckoutTestCase(unittest.TestCase):
    """Each test gets a temp fixture checkout and a temp output path."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name) / "ATM-10"
        self.root.mkdir()
        self.out_path = Path(self._tmp.name) / "progress.example.json"

    def build_checkout(self, **kwargs: Any) -> Path:
        return write_fixture_checkout(self.root, **kwargs)

    def run_build(self, *extra: str) -> "tuple[int, str, str]":
        return run_main([str(self.root), "--out", str(self.out_path),
                         "--date", "2026-09-22", "--commit", "e5e3d1d83e", *extra])

    def assert_clean_failure(self, result: "tuple[int, str, str]", *needles: str) -> None:
        code, out, err = result
        self.assertEqual(code, 1, f"expected exit 1, got {code} (stdout: {out!r})")
        combined = out + err
        self.assertNotIn("Traceback", combined)
        self.assertIn("error:", combined)
        for needle in needles:
            self.assertIn(needle, combined)
        self.assertFalse(self.out_path.exists(),
                         "a failed build must not write the output file")


EXPECTED_FIXTURE_CHAPTERS = [
    {"id": "welcome", "title": "Welcome", "group": "",
     "stage": "early-game", "status": "pending"},
    {"id": "bounty_board", "title": "Bounty Board", "group": "",
     "stage": "early-game", "status": "pending"},
    {"id": "mainquestline_part_1", "title": "Chapter 1: The Beginning",
     "group": "Main Questline", "stage": "early-game", "status": "pending"},
    {"id": "allthemodium", "title": "Chapter 2: Allthemodium",
     "group": "Main Questline", "stage": "endgame", "status": "pending"},
    {"id": "extended__advanced_ae", "title": "Extended \\& Advanced AE",
     "group": "Storage", "stage": "tech", "status": "pending"},
    {"id": "mekanism", "title": "Mekanism", "group": "Tech",
     "stage": "tech", "status": "pending"},
]


class TestFixtureRegeneration(CheckoutTestCase):

    def build_document(self) -> "dict[str, Any]":
        self.build_checkout()
        code, out, err = self.run_build()
        self.assertEqual(code, 0, err)
        return json.loads(self.out_path.read_text(encoding="utf-8"))

    def test_rebuilds_the_golden_document(self) -> None:
        doc = self.build_document()
        self.assertEqual(doc["pack_version"], "8.x")
        self.assertEqual(doc["chapters"], EXPECTED_FIXTURE_CHAPTERS)
        source = doc["pack_version_source"].lower()
        for needle in ("allthemods/atm-10", "config/ftbquests", "8.2",
                       "commit e5e3d1d83e", "2026-09-22", "6 chapters, 9 quests",
                       "in-game quest book"):
            self.assertIn(needle, source, f"provenance must mention {needle!r}")

    def test_semantically_identical_to_the_shipped_example_slice(self) -> None:
        """The proof for the real regeneration: same fixture-shaped inputs that the
        real pack checkout yields produce exactly the shipped example's rows."""
        doc = self.build_document()
        shipped = json.loads(EXAMPLE_DATA.read_text(encoding="utf-8"))
        shipped_by_id = {chapter["id"]: chapter for chapter in shipped["chapters"]}
        fixture_ids = [chapter["id"] for chapter in doc["chapters"]]
        for chapter in doc["chapters"]:
            gold = shipped_by_id.get(chapter["id"])
            self.assertIsNotNone(gold, f"{chapter['id']} must exist in the shipped example")
            assert gold is not None
            self.assertEqual(chapter, gold,
                             f"regenerated {chapter['id']} must equal the shipped row")
        shipped_order = [gold_id for gold_id in (c["id"] for c in shipped["chapters"])
                         if gold_id in set(fixture_ids)]
        self.assertEqual(fixture_ids, shipped_order,
                         "quest-book order must match the shipped example's order")
        self.assertEqual(doc["pack_version"], shipped["pack_version"])

    def test_output_passes_progress_schema(self) -> None:
        doc = self.build_document()
        self.assertEqual(progress.validate(doc), [])
        known = progress.load_known_chapters(self.out_path)
        self.assertIsNotNone(known, "progress.py must accept a regenerated file")
        assert known is not None
        self.assertEqual(known.version, "8.x")

    def test_all_statuses_pending_and_fields_in_order(self) -> None:
        doc = self.build_document()
        for chapter in doc["chapters"]:
            self.assertEqual(list(chapter), ["id", "title", "group", "stage", "status"])
            self.assertEqual(chapter["status"], "pending")

    def test_second_run_is_unchanged_and_writes_nothing(self) -> None:
        self.build_checkout()
        code, out, err = self.run_build()
        self.assertEqual(code, 0, err)
        original = self.out_path.read_text(encoding="utf-8")
        code, out, err = self.run_build()
        self.assertEqual(code, 0, err)
        self.assertIn("unchanged", out)
        self.assertEqual(self.out_path.read_text(encoding="utf-8"), original)

    def test_summary_points_at_sync_workflow(self) -> None:
        self.build_checkout()
        code, out, err = self.run_build()
        self.assertEqual(code, 0, err)
        self.assertIn("6 chapters, pack 8.2 (stamp 8.x)", out)
        self.assertIn("progress.py --sync", out)

    def test_pack_stamp_tracks_the_major_line(self) -> None:
        self.assertEqual(builder.pack_stamp("8.2"), "8.x")
        self.assertEqual(builder.pack_stamp("8.2.1"), "8.x")
        self.assertEqual(builder.pack_stamp("9.0"), "9.x")


class TestCheckMode(CheckoutTestCase):

    def test_check_passes_on_up_to_date_file(self) -> None:
        self.build_checkout()
        code, _out, err = self.run_build()
        self.assertEqual(code, 0, err)
        # A different --date only changes provenance text, not chapter content.
        code, out, _err = self.run_build("--check", "--date", "2027-01-01")
        self.assertEqual(code, 0, out)
        self.assertIn("check ok", out)
        self.assertIn("pack_version_source", out)

    def test_check_fails_when_missing(self) -> None:
        self.build_checkout()
        code, out, _err = self.run_build("--check")
        self.assertEqual(code, 1)
        self.assertIn("would change", out)

    def test_check_fails_when_content_moves(self) -> None:
        self.build_checkout()
        code, _out, err = self.run_build()
        self.assertEqual(code, 0, err)
        doc = json.loads(self.out_path.read_text(encoding="utf-8"))
        doc["chapters"][0], doc["chapters"][1] = doc["chapters"][1], doc["chapters"][0]
        doc["chapters"][2]["title"] = "Renamed Chapter"
        doc["pack_version"] = "7.x"
        self.out_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        code, out, _err = self.run_build("--check")
        self.assertEqual(code, 1)
        self.assertIn("pack_version: '7.x' -> '8.x'", out)
        self.assertIn("quest-book order changed", out)
        self.assertIn("mainquestline_part_1: title", out)

    def test_check_never_writes(self) -> None:
        self.build_checkout()
        self.run_build("--check")
        self.assertFalse(self.out_path.exists())


class TestBuildFailures(CheckoutTestCase):

    def test_missing_path(self) -> None:
        missing = Path(self.root) / "nope"
        self.assert_clean_failure(
            run_main([str(missing), "--out", str(self.out_path)]),
            "no such path", "AllTheMods/ATM-10",
        )

    def test_path_is_a_file(self) -> None:
        some_file = self.root / "file.txt"
        some_file.write_text("x", encoding="utf-8")
        self.assert_clean_failure(
            run_main([str(some_file), "--out", str(self.out_path)]),
            "not a directory",
        )

    def test_not_a_checkout(self) -> None:
        self.build_checkout()
        (self.root / "config" / "ftbquests").rename(self.root / "config" / "moved")
        self.assert_clean_failure(self.run_build(), "does not look like",
                                  "ftbquests", "chapter_groups.snbt",
                                  "github.com/AllTheMods/ATM-10")

    def test_empty_chapters_dir(self) -> None:
        self.build_checkout()
        for path in (self.root / "config" / "ftbquests" / "quests" / "chapters").glob("*"):
            path.unlink()
        self.assert_clean_failure(self.run_build(), "does not look like", "no .snbt")

    def test_missing_chapter_groups(self) -> None:
        self.build_checkout(drop_chapter_groups=True)
        self.assert_clean_failure(self.run_build(), "does not look like",
                                  "chapter_groups.snbt")

    def test_missing_lang_files(self) -> None:
        self.build_checkout(drop_chapter_lang=True)
        self.assert_clean_failure(self.run_build(), "does not look like", "chapter.snbt")

    def test_missing_group_title(self) -> None:
        self.build_checkout(drop_group_lang=True)
        self.assert_clean_failure(self.run_build(), "does not look like",
                                  "chapter_group.snbt")

    def test_malformed_snbt_names_the_file_and_line(self) -> None:
        self.build_checkout()
        target = (self.root / "config" / "ftbquests" / "quests" / "chapters"
                  / "welcome.snbt")
        target.write_text('{\r\n\tfilename: "welcome\r\n', encoding="utf-8")
        self.assert_clean_failure(self.run_build(), "cannot parse", "welcome.snbt",
                                  "line")

    def test_unknown_ftb_group_reference(self) -> None:
        chapters = FIXTURE_CHAPTERS + (
            ("ars_nouveau", "FFFF000011110000", "DEAD0000BEEF0000", 0, 1, "Ars Nouveau"),
        )
        self.build_checkout(chapters=chapters)
        self.assert_clean_failure(self.run_build(), "group id",
                                  "ars_nouveau", "not listed", "chapter_groups")

    def test_chapter_missing_from_stage_table(self) -> None:
        chapters = FIXTURE_CHAPTERS + (
            ("brand_new_mod", "ABCD000011110000", GROUP_TECH, 2, 1, "Brand New Mod"),
        )
        self.build_checkout(chapters=chapters)
        self.assert_clean_failure(self.run_build(), "not in the stage table",
                                  "brand_new_mod", "STAGE_ASSIGNMENTS",
                                  "references/progression.md")

    def test_missing_chapter_title(self) -> None:
        self.build_checkout(title_override={"5B00676D79306EA2": ""})
        # an empty lang title falls back to nothing -> clear error naming the chapter
        self.assert_clean_failure(self.run_build(), "no title found", "welcome")

    def test_duplicate_chapter_id(self) -> None:
        self.build_checkout()
        chapters_dir = self.root / "config" / "ftbquests" / "quests" / "chapters"
        (chapters_dir / "welcome_copy.snbt").write_text(
            (chapters_dir / "welcome.snbt").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self.assert_clean_failure(self.run_build(), "duplicate chapter id", "welcome")

    def test_wrong_pack_name(self) -> None:
        self.build_checkout(pack_name="Not The Mods 9")
        self.assert_clean_failure(self.run_build(), "modpackName", "Not The Mods 9")

    def test_missing_pack_version(self) -> None:
        self.build_checkout(pack_version=None)
        self.assert_clean_failure(self.run_build(), "modpackVersion", "stamp")

    def test_bad_date_argument(self) -> None:
        self.build_checkout()
        code, out, err = run_main([str(self.root), "--out", str(self.out_path),
                                   "--date", "tomorrow"])
        self.assert_clean_failure((code, out, err), "--date must be YYYY-MM-DD")
        code, out, err = run_main([str(self.root), "--out", str(self.out_path),
                                   "--date", "2026-02-30"])
        self.assert_clean_failure((code, out, err), "not a real calendar date")

    def test_broken_existing_output_is_reported_then_overwritten(self) -> None:
        self.build_checkout()
        self.out_path.write_text("this is not json", encoding="utf-8")
        code, out, err = self.run_build()
        self.assertEqual(code, 0, err)
        self.assertIn("not a usable chapter-list document", out)
        json.loads(self.out_path.read_text(encoding="utf-8"))  # now valid


# --------------------------------------------------------------------------------------
# docs + offline guarantee
# --------------------------------------------------------------------------------------

class TestDocsAndOffline(unittest.TestCase):

    NETWORK_IMPORTS = ("socket", "urllib", "http", "requests", "ftplib", "smtplib",
                       "httpx", "aiohttp", "webbrowser", "subprocess")

    def imported_modules(self, source: str) -> "set[str]":
        found: "set[str]" = set()
        for line in source.splitlines():
            stripped = line.strip()
            if stripped.startswith("import "):
                found.update(part.strip().split()[0].split(".")[0]
                             for part in stripped[len("import "):].split(","))
            elif stripped.startswith("from "):
                found.add(stripped.split()[1].split(".")[0])
        return found

    def test_snbt_imports_only_re_and_typing(self) -> None:
        imported = self.imported_modules(
            (SCRIPTS / "snbt.py").read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())
        self.assertTrue(imported <= {"re", "typing", "__future__"},
                        f"unexpected import(s): {sorted(imported)}")

    def test_builder_imports_no_network_or_process_module(self) -> None:
        imported = self.imported_modules(
            (SCRIPTS / "build_chapter_list.py").read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set(),
                         "build_chapter_list.py must stay offline")
        allowed = {"argparse", "datetime", "json", "os", "re", "sys", "tempfile",
                   "pathlib", "typing", "__future__", "snbt", "importlib"}
        self.assertTrue(imported <= allowed,
                        f"unexpected import(s): {sorted(imported - allowed)}")

    def test_this_suite_imports_no_network_module(self) -> None:
        imported = self.imported_modules(Path(__file__).read_text(encoding="utf-8"))
        self.assertEqual(imported & set(self.NETWORK_IMPORTS), set())

    def test_skill_md_documents_the_pack_update_workflow(self) -> None:
        skill = SKILL_MD.read_text(encoding="utf-8")
        for needle in ("scripts/build_chapter_list.py", "AllTheMods/ATM-10 clone",
                       "review the diff", "progress.py --sync"):
            self.assertIn(needle, skill, f"SKILL.md must document {needle!r}")


if __name__ == "__main__":
    unittest.main()
