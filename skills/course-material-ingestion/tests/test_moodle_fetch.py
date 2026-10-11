#!/usr/bin/env python3
"""Tests for moodle_fetch.py - stdlib unittest only, no external network.

The integration tests run a throwaway HTTP server on localhost that imitates the parts of
Moodle this skill depends on: view.php -> pluginfile.php redirects, Content-Disposition
filenames, a login redirect for missing cookies, and a 200-with-HTML error page.

    python -m unittest discover -s tests -v
"""

import hashlib
import importlib.util
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "moodle_fetch.py"
_spec = importlib.util.spec_from_file_location("moodle_fetch", SCRIPT)
mf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mf)

PDF = b"%PDF-1.4\n" + b"x" * 500 + b"\n%%EOF\n"
HTML = b"<!DOCTYPE html>\n<html><head><title>Log in to Moodle</title></head></html>"

COURSE_PAGE = """
<ul class="topics">
 <li class="activity resource modtype_resource" id="module-42">
   <a class="aalink" href="https://moodle.example.com/mod/resource/view.php?id=42">
     <span class="instancename">References<span class="accesshide"> File</span></span></a>
 </li>
 <li class="activity resource modtype_resource" id="module-43">
   <a class="aalink" href="https://moodle.example.com/mod/resource/view.php?id=43">
     <span class="instancename">U01 - Unit One<span class="accesshide"> File</span></span></a>
 </li>
 <li class="activity forum modtype_forum" id="module-77">
   <a class="aalink" href="https://moodle.example.com/mod/forum/view.php?id=77">
     <span class="instancename">Announcements</span></a>
 </li>
</ul>
"""

TILE_PAGE = """
<div class="course-content">
  <a class="aalink" href="/mod/resource/view.php?id=91&amp;forcedownload=1">
    <span class="instancename">Lecture 1</span></a>
  <a class="aalink" href="/mod/resource/view.php?id=92"><span>No title span here</span></a>
</div>
"""


class Handler(BaseHTTPRequestHandler):
    files = {
        "/pluginfile.php/1/mod_resource/content/0/References.pdf": PDF,
        "/pluginfile.php/1/mod_resource/content/0/U01 (2).pdf": b"%PDF-1.7\nunit one\n%%EOF\n",
        "/pluginfile.php/1/mod_resource/content/0/Slides.pptx": b"PK\x03\x04" + b"z" * 200,
    }
    redirects = {
        "/mod/resource/view.php?id=42": "/pluginfile.php/1/mod_resource/content/0/References.pdf",
        "/mod/resource/view.php?id=43": "/pluginfile.php/1/mod_resource/content/0/U01 (2).pdf",
        "/mod/resource/view.php?id=44": None,   # serves HTML error page
        "/mod/resource/view.php?id=45": "/mod/resource/view.php?id=42",  # two hops
        "/mod/resource/view.php?id=46": "/pluginfile.php/1/mod_resource/content/0/Slides.pptx",
    }

    def log_message(self, *a):
        pass

    def _auth(self):
        return "MoodleSession" in (self.headers.get("Cookie") or "")

    def do_GET(self):
        self.path = unquote(self.path)  # a real server decodes %20 before routing
        if self.path.startswith("/login"):
            body = HTML
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if not self._auth():
            self.send_response(302)
            self.send_header("Location", "/login/index.php")
            self.end_headers()
            return
        if self.path in self.redirects:
            target = self.redirects[self.path]
            if target is None:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(HTML)))
                self.end_headers()
                self.wfile.write(HTML)
                return
            self.send_response(302)
            self.send_header("Location", target)
            self.end_headers()
            return
        if self.path in self.files:
            body = self.files[self.path]
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            name = self.path.rsplit("/", 1)[-1]
            self.send_header("Content-Disposition", f'attachment; filename="{name}"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/course/view.php"):
            body = (TILE_PAGE if "tile=1" in self.path else COURSE_PAGE).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()


class ServerMixin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()


class FilenameTests(unittest.TestCase):
    def test_content_disposition_plain(self):
        h = {"Content-Disposition": 'attachment; filename="References.pdf"'}
        self.assertEqual(mf.filename_from_headers(h, "http://x/y/z"), "References.pdf")

    def test_content_disposition_rfc5987_utf8(self):
        h = {"Content-Disposition": "attachment; filename*=UTF-8''R%C3%A9f%C3%A9rences%20(1).pdf"}
        self.assertEqual(mf.filename_from_headers(h, "http://x/y/z"), "Références (1).pdf")

    def test_falls_back_to_redirect_path_not_view_php(self):
        h = {"Content-Type": "application/pdf"}
        name = mf.filename_from_headers(
            h, "http://moodle/mod/resource/view.php?id=42")
        self.assertEqual(name, "download.pdf")

    def test_uses_final_path_when_disposition_missing(self):
        h = {"Content-Type": "application/pdf"}
        self.assertEqual(
            mf.filename_from_headers(h, "http://m/pluginfile.php/1/mod_resource/content/0/U01%20(2).pdf"),
            "U01 (2).pdf")

    def test_sanitize_strips_windows_hostile_chars_and_keeps_accents(self):
        self.assertEqual(mf.sanitize('a:b*c?d"e<f>g|h.pdf'), "a_b_c_d_e_f_g_h.pdf")
        self.assertEqual(mf.sanitize("مقدمة في علم النفس.pdf"), "مقدمة في علم النفس.pdf")
        self.assertTrue(mf.sanitize("x" * 400 + ".pdf").endswith(".pdf"))
        self.assertLessEqual(len(mf.sanitize("x" * 400 + ".pdf")), 150)
        self.assertEqual(mf.sanitize("NUL.pdf"), "_NUL.pdf")


class SniffTests(unittest.TestCase):
    def test_pdf_ok(self):
        self.assertEqual(mf.sniff(PDF, ".pdf"), "ok")

    def test_html_saved_as_pdf_is_caught(self):
        self.assertEqual(mf.sniff(HTML, ".pdf"), "html")

    def test_ooxml_zip_signature(self):
        self.assertEqual(mf.sniff(b"PK\x03\x04rest", ".docx"), "ok")

    def test_docx_that_is_really_pdf_is_mismatch(self):
        self.assertEqual(mf.sniff(PDF, ".docx"), "mismatch")

    def test_m4a_marker_at_offset_4(self):
        self.assertEqual(mf.sniff(b"\x00\x00\x00\x18ftypM4A ", ".m4a"), "ok")

    def test_plain_text_is_unknown_not_failed(self):
        self.assertEqual(mf.sniff(b"hello", ".txt"), "unknown")


class UrlEncodingTests(unittest.TestCase):
    def test_raw_space_and_accent_are_encoded(self):
        self.assertEqual(
            mf.encode_unsafe("http://m/pluginfile.php/1/U01 (2) Réf.pdf"),
            "http://m/pluginfile.php/1/U01%20(2)%20R%C3%A9f.pdf")

    def test_existing_escapes_are_not_double_encoded(self):
        url = "http://m/pluginfile.php/1/U01%20(2).pdf"
        self.assertEqual(mf.encode_unsafe(url), url)

    def test_query_string_survives(self):
        self.assertEqual(mf.encode_unsafe("http://m/course/view.php?id=1&section=3"),
                         "http://m/course/view.php?id=1&section=3")


class DiscoverTests(unittest.TestCase):
    def test_titles_come_from_their_own_module_block(self):
        acts = mf.extract_activities(COURSE_PAGE, "https://moodle.example.com/course/view.php?id=1")
        by_id = {a["id"]: a for a in acts}
        self.assertEqual(by_id[42]["title"], "References")
        self.assertEqual(by_id[43]["title"], "U01 - Unit One")
        self.assertEqual(by_id[43]["url"], "https://moodle.example.com/mod/resource/view.php?id=43")

    def test_modtypes_filter(self):
        acts = mf.extract_activities(COURSE_PAGE, "https://m/", ["resource"])
        self.assertEqual([a["id"] for a in acts], [42, 43])

    def test_tile_page_relative_links_and_entities(self):
        acts = mf.extract_activities(TILE_PAGE, "https://m/course/view.php?id=2")
        self.assertEqual(acts[0]["url"], "https://m/mod/resource/view.php?id=91&forcedownload=1")
        self.assertEqual(acts[0]["title"], "Lecture 1")
        self.assertIsNone(acts[1]["title"])  # no instancename span -> honest None, not ""


class LinkSyncTests(unittest.TestCase):
    def _vault(self):
        tmp = Path(tempfile.mkdtemp())
        note = tmp / "Comprehension and Oral Expression 1.md"
        note.write_text(
            "# Course\n\n"
            "See [[Resource_2]] and [[Resource_4|the script]] and [[Resource_1#Grammar]].\n\n"
            "```\n[[Resource_99]] inside a fence must not be touched\n```\n\n"
            "Also [[Script I]].\n", encoding="utf-8")
        return tmp, note

    def test_dry_run_changes_nothing_and_reports_placeholders(self):
        tmp, note = self._vault()
        before = note.read_text(encoding="utf-8")
        rc = mf.cmd_sync_links(type("A", (), {
            "notes": str(tmp), "map": None, "manifest": None, "dry_run": True})())
        self.assertEqual(note.read_text(encoding="utf-8"), before)
        self.assertNotEqual(rc, 0)  # unresolved placeholders -> non-zero

    def test_rewrites_targets_keeps_alias_and_anchor_skips_code(self):
        tmp, note = self._vault()
        m = tmp / "map.json"
        m.write_text(json.dumps({"Resource_1": "Grammar and Pronunciation",
                                 "Resource_2": "Script I",
                                 "Resource_4": "Script II",
                                 "Script I": "Script I FINAL"}), encoding="utf-8")
        mf.cmd_sync_links(type("A", (), {
            "notes": str(tmp), "map": str(m), "manifest": None, "dry_run": False})())
        out = note.read_text(encoding="utf-8")
        self.assertIn("[[Script I]]", out)
        self.assertIn("[[Script II|the script]]", out)
        self.assertIn("[[Grammar and Pronunciation#Grammar]]", out)
        self.assertIn("[[Script I FINAL]]", out)
        self.assertIn("[[Resource_99]] inside a fence", out)  # fenced code untouched
        self.assertNotIn("[[Resource_2]]", out)


class IntegrationTests(ServerMixin):
    def _plan(self, ids, course="Comprehension and Oral Expression 1"):
        return [{"course": course,
                 "resources": [{"id": i, "url": f"{self.base}/mod/resource/view.php?id={i}",
                                "title": f"Resource {i}"} for i in ids]}]

    def _run_download(self, ids, cookie="MoodleSession=abc123"):
        dest = Path(tempfile.mkdtemp())
        plan = Path(tempfile.mkdtemp()) / "plan.json"  # kept out of dest on purpose
        plan.write_text(json.dumps(self._plan(ids)), encoding="utf-8")
        rc = mf.cmd_download(type("A", (), {
            "plan": str(plan), "dest": str(dest), "manifest": None, "update": False,
            "max_bytes": None, "cookie": cookie, "cookie_file": None,
            "timeout": 10, "insecure": False})())
        manifest = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
        return rc, dest, manifest, plan

    def test_resolve_reads_the_real_filename_off_the_redirect(self):
        info = mf.Fetcher("MoodleSession=abc123", timeout=10).resolve(
            f"{self.base}/mod/resource/view.php?id=42")
        self.assertEqual(info["filename"], "References.pdf")
        self.assertEqual(info["sniff"], "ok")
        self.assertEqual(info["declared_bytes"], len(PDF))
        self.assertEqual(len(info["redirects"]), 1)
        self.assertFalse(info["login_redirect"])

    def test_resolve_follows_multiple_hops(self):
        info = mf.Fetcher("MoodleSession=abc123", timeout=10).resolve(
            f"{self.base}/mod/resource/view.php?id=45")
        self.assertEqual(info["filename"], "References.pdf")
        self.assertEqual(len(info["redirects"]), 2)

    def test_expired_session_is_flagged_not_downloaded(self):
        info = mf.Fetcher("", timeout=10).resolve(f"{self.base}/mod/resource/view.php?id=42")
        self.assertTrue(info["login_redirect"])
        self.assertEqual(info["sniff"], "html")

    def test_download_writes_real_files_and_manifest(self):
        rc, dest, manifest, plan = self._run_download([42, 43])
        course = dest / "Comprehension and Oral Expression 1"
        self.assertTrue((course / "References.pdf").exists())
        self.assertTrue((course / "U01 (2).pdf").exists())
        self.assertEqual((course / "References.pdf").read_bytes(), PDF)
        statuses = {r["id"]: r["status"] for r in manifest["resources"]}
        self.assertEqual(statuses, {"42": "ok", "43": "ok"})
        entry = next(r for r in manifest["resources"] if r["id"] == "42")
        self.assertEqual(entry["sha256"], hashlib.sha256(PDF).hexdigest())
        self.assertEqual(rc, 0)

    def test_html_error_page_is_kept_as_bad_and_reported(self):
        rc, dest, manifest, plan = self._run_download([44])
        course = dest / "Comprehension and Oral Expression 1"
        self.assertEqual([r["status"] for r in manifest["resources"]], ["html_error"])
        self.assertTrue(list(course.glob("*.bad")), "HTML body should be quarantined as .bad")
        self.assertFalse(list(course.glob("download.pdf")))
        self.assertNotEqual(rc, 0)

    def test_expired_session_makes_download_fail_loudly(self):
        rc, dest, manifest, plan = self._run_download([42], cookie="")
        self.assertEqual([r["status"] for r in manifest["resources"]], ["error"])
        self.assertIn("login", manifest["resources"][0]["error"].lower())
        self.assertFalse(list((dest / "Comprehension and Oral Expression 1").glob("*.pdf")))
        self.assertNotEqual(rc, 0)

    def test_update_skips_unchanged_and_verify_passes(self):
        rc, dest, manifest, plan = self._run_download([42, 46])
        rc2 = mf.cmd_download(type("A", (), {
            "plan": str(plan), "dest": str(dest), "manifest": None, "update": True,
            "max_bytes": None, "cookie": "MoodleSession=abc123", "cookie_file": None,
            "timeout": 10, "insecure": False})())
        self.assertEqual(rc2, 0)
        m2 = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(m2["resources"]), 2)
        rc3 = mf.cmd_verify(type("A", (), {
            "manifest": str(dest / "manifest.json"), "root": str(dest), "notes": None})())
        self.assertEqual(rc3, 0)

    def test_verify_catches_a_tampered_file(self):
        rc, dest, manifest, plan = self._run_download([42])
        (dest / "Comprehension and Oral Expression 1" / "References.pdf").write_bytes(HTML)
        rc3 = mf.cmd_verify(type("A", (), {
            "manifest": str(dest / "manifest.json"), "root": str(dest), "notes": None})())
        self.assertNotEqual(rc3, 0)

    def test_verify_flags_dangling_wikilinks(self):
        rc, dest, manifest, plan = self._run_download([42])
        vault = Path(tempfile.mkdtemp())
        (vault / "Course.md").write_text("[[References]] and [[Resource_3]]\n", encoding="utf-8")
        rc3 = mf.cmd_verify(type("A", (), {
            "manifest": str(dest / "manifest.json"), "root": str(dest),
            "notes": str(vault)})())
        self.assertNotEqual(rc3, 0)  # [[Resource_3]] does not exist on disk


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=2))
