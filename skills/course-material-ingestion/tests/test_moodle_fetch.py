#!/usr/bin/env python3
"""Tests for moodle_fetch.py - stdlib unittest only, no external network.

The integration tests run a throwaway HTTP server on localhost that imitates the parts of
Moodle this skill depends on: view.php -> pluginfile.php redirects, Content-Disposition
filenames, a login redirect for missing cookies, and a 200-with-HTML error page.

    python -m unittest discover -s tests -v
"""

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import unquote
from unittest import mock

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
    file_requests = []
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
            type(self).file_requests.append(self.path)
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


class ExpiredSessionHandler(Handler):
    """A Moodle whose session dies in the middle of a run.

    `Handler` answers every cookie-carrying request, which cannot model a session that times
    out with half a plan still to fetch. This one revokes the session at a chosen point and
    answers everything after that with the login redirect, which is what Moodle does when the
    `MoodleSession` cookie it was given has expired.

    Two ways to choose that point, whichever the test is about:

    * `expire_on` - a substring of the request path; the session dies on that request.
    * `expire_at` - the number of authenticated requests the session survives; the next one
      is answered with the login page. Used to expire *between* two steps of one resource.

    `requested` records every path the client asked for, so a test can prove a stopped run
    did not go on to fire a doomed request per remaining resource.
    """

    expire_on = None
    expire_at = None
    expired = False
    valid_requests = 0
    requested = []

    @classmethod
    def reset(cls, expire_on=None, expire_at=None):
        cls.expire_on = expire_on
        cls.expire_at = expire_at
        cls.expired = False
        cls.valid_requests = 0
        cls.requested = []

    def _auth(self):
        cls = type(self)
        if cls.expired:
            return False
        if not super()._auth():
            return False            # no cookie at all: a login redirect, as before
        if cls.expire_at is not None and cls.valid_requests >= cls.expire_at:
            cls.expired = True
            return False
        if cls.expire_on and cls.expire_on in self.path:
            cls.expired = True
            return False
        cls.valid_requests += 1
        return True

    def do_GET(self):
        type(self).requested.append(unquote(self.path))
        return super().do_GET()


class ServerMixin(unittest.TestCase):
    handler = Handler  # a subclass with a less cooperative Moodle replaces this

    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), cls.handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def setUp(self):
        # An ambient cookie must never change what another test asked for, so every
        # networked test starts from a clean environment and puts it back afterwards.
        self._saved_cookie_env = os.environ.pop("MOODLE_SESSION_COOKIE", None)
        self.handler.file_requests = []

    def tearDown(self):
        os.environ.pop("MOODLE_SESSION_COOKIE", None)
        if self._saved_cookie_env is not None:
            os.environ["MOODLE_SESSION_COOKIE"] = self._saved_cookie_env

    # -- download helpers, shared by the integration and dead-session tests -------------

    def _plan(self, ids, course="Comprehension and Oral Expression 1"):
        return [{"course": course,
                 "resources": [{"id": i, "url": f"{self.base}/mod/resource/view.php?id={i}",
                                "title": f"Resource {i}"} for i in ids]}]

    def _run_download(self, ids, cookie="MoodleSession=abc123"):
        """`download` in-process: (returncode, dest, manifest, plan)."""
        rc, dest, manifest, plan, _output = self._run_download_captured(ids, cookie)
        return rc, dest, manifest, plan

    def _run_download_captured(self, ids, cookie="MoodleSession=abc123"):
        """The same run, plus everything it printed.

        When a session dies the message *is* the fix, so the tests read what the run said
        instead of trusting the exit code to carry it.
        """
        dest = Path(tempfile.mkdtemp())
        plan = Path(tempfile.mkdtemp()) / "plan.json"  # kept out of dest on purpose
        plan.write_text(json.dumps(self._plan(ids)), encoding="utf-8")
        with capture_output() as buf:
            rc = mf.cmd_download(fake_args(
                plan=str(plan), dest=str(dest), manifest=None, update=False, max_bytes=None,
                cookie=cookie, cookie_file=None, timeout=10, insecure=False))
        manifest = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
        return rc, dest, manifest, plan, buf.getvalue()

    def _run_update(self, dest, plan, cookie="MoodleSession=abc123"):
        with capture_output() as buf:
            rc = mf.cmd_download(fake_args(
                plan=str(plan), dest=str(dest), manifest=None, update=True, max_bytes=None,
                cookie=cookie, cookie_file=None, timeout=10, insecure=False))
        manifest = json.loads((dest / "manifest.json").read_text(encoding="utf-8"))
        return rc, manifest, buf.getvalue()


def fake_args(**kw):
    """An argparse namespace look-alike; unknown flags stay absent, like real ones."""
    base = {"cookie": None, "cookie_file": None, "cookie_env": None}
    base.update(kw)
    return type("A", (), base)()


@contextlib.contextmanager
def capture_output():
    """stdout and stderr in one string - that is how the user sees a run."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        yield buf


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

    def test_expired_session_stops_instead_of_downloading(self):
        """A login redirect stops the run now - see DeadSessionTests for the whole contract."""
        rc, dest, manifest, plan = self._run_download([42], cookie="")
        self.assertEqual([r["status"] for r in manifest["resources"]], ["session_expired"])
        self.assertIn("login", manifest["resources"][0]["error"].lower())
        self.assertFalse(list((dest / "Comprehension and Oral Expression 1").glob("*.pdf")))
        self.assertNotEqual(rc, 0)

    def test_update_skips_identical_recorded_file_without_redownload_or_warning(self):
        rc, dest, manifest, plan = self._run_download([42])
        self.assertEqual(rc, 0)
        before = len(self.handler.file_requests)

        rc2, m2, output = self._run_update(dest, plan)

        self.assertEqual(rc2, 0, output)
        # The update still resolves the URL once, but does not open the file for the
        # second, streaming download.
        self.assertEqual(len(self.handler.file_requests) - before, 1)
        self.assertIn("(unchanged)", output)
        self.assertNotIn("WARN", output)
        self.assertEqual(len(m2["resources"]), 1)

    def test_update_redownloads_same_size_file_with_different_bytes(self):
        rc, dest, manifest, plan = self._run_download([42])
        self.assertEqual(rc, 0)
        entry = manifest["resources"][0]
        recorded = Path(entry["path"])
        tampered = bytearray(PDF)
        tampered[10] = ord("Y")
        recorded.write_bytes(tampered)
        before = len(self.handler.file_requests)

        rc2, m2, output = self._run_update(dest, plan)

        self.assertEqual(rc2, 0, output)
        self.assertEqual(len(self.handler.file_requests) - before, 2,
                         "a changed file must be resolved and downloaded again")
        self.assertNotIn("(unchanged)", output)
        refreshed = m2["resources"][0]
        refreshed_path = Path(refreshed["path"])
        self.assertEqual(refreshed_path.read_bytes(), PDF)
        self.assertEqual(refreshed["sha256"], hashlib.sha256(PDF).hexdigest())
        self.assertNotEqual(refreshed_path, recorded)

    def test_update_uses_the_manifest_path_when_the_recorded_file_is_deleted(self):
        rc, dest, manifest, plan = self._run_download([42])
        self.assertEqual(rc, 0)
        recorded = Path(manifest["resources"][0]["path"])
        recorded.unlink()
        before = len(self.handler.file_requests)

        rc2, m2, output = self._run_update(dest, plan)

        self.assertEqual(rc2, 0, output)
        self.assertEqual(len(self.handler.file_requests) - before, 2)
        self.assertNotIn("(unchanged)", output)
        self.assertEqual(Path(m2["resources"][0]["path"]).read_bytes(), PDF)

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


class DeadSessionMessageTests(unittest.TestCase):
    """The stop message is the whole point of the feature, so it is asserted on directly."""

    def test_names_the_login_page_the_count_and_the_way_back(self):
        msg = mf.dead_session_report("https://moodle.example.com/login/index.php",
                                     remaining=7, had_cookie=True)
        self.assertIn("https://moodle.example.com/login/index.php", msg)
        self.assertIn("7 resource(s)", msg)
        self.assertIn("re-authenticate", msg.lower())

    def test_carries_the_caller_s_resume_hint(self):
        # Only `download` has a run to resume, so only it asks for the --update line.
        msg = mf.dead_session_report("https://m/login/index.php", remaining=1, had_cookie=True,
                                     resume_hint="re-run with --update")
        self.assertIn("--update", msg)
        self.assertNotIn("--update", mf.dead_session_report(
            "https://m/login/index.php", remaining=1, had_cookie=True))

    def test_says_nothing_about_cookies_when_one_was_supplied(self):
        msg = mf.dead_session_report("https://m/login/index.php", remaining=1, had_cookie=True)
        self.assertNotIn("no cookie was supplied", msg)

    def test_names_the_cookie_flags_when_none_was_supplied(self):
        # The commonest cause of a "dead" session is that no cookie was passed at all.
        msg = mf.dead_session_report("https://m/login/index.php", remaining=1, had_cookie=False)
        self.assertIn("no cookie was supplied", msg)
        self.assertIn("--cookie-env", msg)

    def test_a_discover_stop_does_not_pretend_a_manifest_was_written(self):
        # discover writes no manifest, so the download-specific lines must stay out of it.
        msg = mf.dead_session_report("https://m/login/index.php", remaining=0, had_cookie=True)
        self.assertNotIn("manifest.json", msg)

    def test_is_login_url_matches_moodle_login_and_sso_paths(self):
        self.assertTrue(mf.is_login_url("https://moodle.example.com/login/index.php"))
        self.assertTrue(mf.is_login_url("https://moodle.example.com/login"))
        self.assertTrue(mf.is_login_url("https://moodle.example.com/auth/oidc/"))
        self.assertFalse(mf.is_login_url("https://moodle.example.com/course/view.php?id=1"))
        self.assertFalse(mf.is_login_url(
            "https://moodle.example.com/pluginfile.php/1/mod_resource/content/0/References.pdf"))


class DeadSessionTests(ServerMixin):
    """A session that dies mid-plan stops the run once - it does not fail item by item.

    Each test decides how the session dies; `ExpiredSessionHandler` does the rest.
    """

    handler = ExpiredSessionHandler

    def setUp(self):
        super().setUp()
        ExpiredSessionHandler.reset()

    def test_stopping_at_the_first_login_redirect_keeps_what_was_downloaded(self):
        ExpiredSessionHandler.reset(expire_on="id=43")
        rc, dest, manifest, plan, output = self._run_download_captured([42, 43, 44])

        # 42 finished before the session died, so its bytes are still on disk...
        course = dest / "Comprehension and Oral Expression 1"
        self.assertEqual((course / "References.pdf").read_bytes(), PDF)
        # ...and nothing was written for 43, whose request is the one that proved it dead.
        self.assertEqual(sorted(p.name for p in course.iterdir()), ["References.pdf"])

        statuses = {r["id"]: r["status"] for r in manifest["resources"]}
        self.assertEqual(statuses, {"42": "ok", "43": "session_expired", "44": "session_expired"})
        self.assertEqual(manifest["stopped_reason"], "session_expired")
        self.assertNotEqual(rc, 0)

    def test_the_rest_of_the_plan_is_never_requested(self):
        ExpiredSessionHandler.reset(expire_on="id=43")
        self._run_download_captured([42, 43, 44])
        self.assertNotIn("/mod/resource/view.php?id=44", ExpiredSessionHandler.requested,
                         "once the session is known to be dead, do not probe item by item")

    def test_the_message_says_how_to_resume(self):
        ExpiredSessionHandler.reset(expire_on="id=43")
        rc, dest, manifest, plan, output = self._run_download_captured([42, 43, 44])
        self.assertIn("login", output.lower())
        self.assertIn("re-authenticate", output.lower())
        self.assertIn("--update", output)
        self.assertIn("1 resource(s) in the plan were not attempted", output)
        self.assertIn("manifest.json", output)

    def test_a_stopped_run_leaves_a_manifest_verify_can_read(self):
        ExpiredSessionHandler.reset(expire_on="id=43")
        rc, dest, manifest, plan, output = self._run_download_captured([42, 43, 44])
        self.assertTrue((dest / "manifest.json").exists())
        with capture_output() as buf:
            rc2 = mf.cmd_verify(fake_args(manifest=str(dest / "manifest.json"),
                                          root=str(dest), notes=None))
        self.assertNotEqual(rc2, 0)
        self.assertIn("session_expired", buf.getvalue())

    def test_a_missing_cookie_is_called_out(self):
        # No cookie at all is the commonest "dead session"; the message says so instead of
        # leaving the user to wonder why every request bounced.
        rc, dest, manifest, plan, output = self._run_download_captured([42], cookie="")
        self.assertIn("no cookie was supplied", output)
        self.assertIn("--cookie-env", output)

    def test_an_expiry_between_resolve_and_fetch_never_saves_the_login_page(self):
        # resolve costs two authenticated requests (view.php -> pluginfile.php), so allowing
        # exactly two kills the session right before the body fetch of the same resource:
        # what arrives is the login page under the file's own name.
        ExpiredSessionHandler.reset(expire_at=2)
        rc, dest, manifest, plan, output = self._run_download_captured([42])
        course = dest / "Comprehension and Oral Expression 1"
        self.assertEqual(list(course.glob("*")), [],
                         "no .part file and no login page saved under a .pdf name")
        entry = manifest["resources"][0]
        self.assertEqual(entry["status"], "session_expired")
        self.assertIn("login", entry["error"].lower())
        self.assertNotEqual(rc, 0)

    def test_only_a_login_page_stops_the_run(self):
        # A resource that is simply broken must not be mistaken for an expired session.
        rc, dest, manifest, plan, output = self._run_download_captured([44, 42])
        statuses = [r["status"] for r in manifest["resources"]]
        self.assertEqual(statuses, ["html_error", "ok"])
        self.assertNotIn("session_expired", statuses)
        self.assertNotIn("STOP", output)

    def test_a_healthy_session_runs_to_the_end_untouched(self):
        rc, dest, manifest, plan, output = self._run_download_captured([42, 46])
        self.assertEqual(rc, 0, output)
        self.assertEqual({r["status"] for r in manifest["resources"]}, {"ok"})
        self.assertNotIn("STOP", output)
        self.assertNotIn("stopped_reason", manifest)

    def test_discover_reports_a_dead_session_instead_of_an_empty_course(self):
        # A login page renders zero activities; reporting that as "this course has no files"
        # is worse than no answer at all.
        with capture_output() as buf:
            rc = mf.cmd_discover(fake_args(
                course_url=f"{self.base}/course/view.php?id=1", section=None,
                modtypes="resource,folder,page,url,book,file", cookie="", cookie_file=None,
                timeout=10, insecure=False))
        output = buf.getvalue()
        self.assertNotEqual(rc, 0)
        self.assertIn("re-authenticate", output.lower())
        self.assertNotIn('"activities"', output)


# Two different resources, one filename. The A/B pair has the same size and different bytes:
# the case that used to be overwritten silently. Same-size identical bytes and a size mismatch
# cover the other two branches of the collision rule.
SAME_SIZE_A = b"%PDF-1.4\n" + b"A" * 300 + b"\n%%EOF\n"
SAME_SIZE_B = b"%PDF-1.4\n" + b"B" * 300 + b"\n%%EOF\n"
SHORTER = b"%PDF-1.4\n" + b"C" * 10 + b"\n%%EOF\n"
assert len(SAME_SIZE_A) == len(SAME_SIZE_B) and len(SHORTER) != len(SAME_SIZE_A)


class CollisionHandler(Handler):
    """A Moodle where several resources are all served as `Notes.pdf`."""

    files = {
        **Handler.files,
        "/pluginfile.php/7/mod_resource/content/0/Notes.pdf": SAME_SIZE_A,
        "/pluginfile.php/8/mod_resource/content/0/Notes.pdf": SAME_SIZE_B,
        "/pluginfile.php/9/mod_resource/content/0/Notes.pdf": SAME_SIZE_A,
        "/pluginfile.php/10/mod_resource/content/0/Notes.pdf": SAME_SIZE_A,
        "/pluginfile.php/11/mod_resource/content/0/Notes.pdf": SAME_SIZE_A,
        "/pluginfile.php/12/mod_resource/content/0/Notes.pdf": SHORTER,
    }
    redirects = {
        **Handler.redirects,
        "/mod/resource/view.php?id=70": "/pluginfile.php/7/mod_resource/content/0/Notes.pdf",
        "/mod/resource/view.php?id=71": "/pluginfile.php/8/mod_resource/content/0/Notes.pdf",
        "/mod/resource/view.php?id=72": "/pluginfile.php/9/mod_resource/content/0/Notes.pdf",
        "/mod/resource/view.php?id=73": "/pluginfile.php/10/mod_resource/content/0/Notes.pdf",
        "/mod/resource/view.php?id=74": "/pluginfile.php/11/mod_resource/content/0/Notes.pdf",
        "/mod/resource/view.php?id=75": "/pluginfile.php/12/mod_resource/content/0/Notes.pdf",
    }


def _warnings(output):
    return [line for line in output.splitlines() if line.startswith("WARN")]


class CollisionTests(ServerMixin):
    """Same filename inside one course: size decides whether a hash is needed at all."""

    handler = CollisionHandler
    COURSE = "Comprehension and Oral Expression 1"

    def _download_into(self, dest, ids):
        """A second run into an existing folder - the re-run case."""
        plan = Path(tempfile.mkdtemp()) / "plan.json"
        plan.write_text(json.dumps(self._plan(ids)), encoding="utf-8")
        with capture_output() as buf:
            rc = mf.cmd_download(fake_args(
                plan=str(plan), dest=str(dest), manifest=None, update=False, max_bytes=None,
                cookie="MoodleSession=abc123", cookie_file=None, timeout=10, insecure=False))
        return rc, buf.getvalue()

    def test_same_name_same_size_different_bytes_keeps_both_files(self):
        rc, dest, manifest, plan, output = self._run_download_captured([70, 71])
        course = dest / self.COURSE
        self.assertEqual(sorted(p.name for p in course.iterdir()), ["Notes (2).pdf", "Notes.pdf"])
        self.assertEqual((course / "Notes.pdf").read_bytes(), SAME_SIZE_A)
        self.assertEqual((course / "Notes (2).pdf").read_bytes(), SAME_SIZE_B)

        by_id = {r["id"]: r for r in manifest["resources"]}
        self.assertEqual(sorted(by_id), ["70", "71"])
        self.assertEqual({r["status"] for r in by_id.values()}, {"ok"})
        self.assertEqual(Path(by_id["70"]["path"]).name, "Notes.pdf")
        self.assertEqual(Path(by_id["71"]["path"]).name, "Notes (2).pdf")
        self.assertEqual(by_id["70"]["sha256"], hashlib.sha256(SAME_SIZE_A).hexdigest())
        self.assertEqual(by_id["71"]["sha256"], hashlib.sha256(SAME_SIZE_B).hexdigest())

        warnings = _warnings(output)
        self.assertEqual(len(warnings), 1, output)
        self.assertIn("Notes.pdf", warnings[0])
        self.assertIn("Notes (2).pdf", warnings[0])
        self.assertEqual(rc, 0, output)

    def test_same_name_same_size_identical_bytes_is_one_file_without_warning(self):
        rc, dest, manifest, plan, output = self._run_download_captured([72, 73])
        course = dest / self.COURSE
        self.assertEqual([p.name for p in course.iterdir()], ["Notes.pdf"])
        self.assertEqual((course / "Notes.pdf").read_bytes(), SAME_SIZE_A)
        self.assertEqual(_warnings(output), [])
        # Both resources resolve to the one file on disk; no suffixed copy is recorded.
        self.assertEqual({Path(r["path"]).name for r in manifest["resources"]}, {"Notes.pdf"})
        self.assertEqual(rc, 0, output)

    def test_update_uses_b_recorded_suffix_not_a_requested_name(self):
        rc, dest, manifest, plan, output = self._run_download_captured([70, 71])
        self.assertEqual(rc, 0, output)
        by_id = {r["id"]: r for r in manifest["resources"]}
        b_path = Path(by_id["71"]["path"])
        self.assertEqual(b_path.name, "Notes (2).pdf")
        # A owns the requested name Notes.pdf. Corrupt only B's recorded copy with
        # same-sized bytes: checking Notes.pdf would falsely call B unchanged.
        b_path.write_bytes(SAME_SIZE_A)
        before = len(self.handler.file_requests)

        rc2, m2, output2 = self._run_update(dest, plan)

        self.assertEqual(rc2, 0, output2)
        self.assertEqual(len(self.handler.file_requests) - before, 3,
                         "A resolves only; B resolves and is downloaded again")
        updated_b = next(r for r in m2["resources"] if r["id"] == "71")
        updated_b_path = Path(updated_b["path"])
        self.assertEqual(updated_b_path.read_bytes(), SAME_SIZE_B)
        self.assertEqual(updated_b_path.name, "Notes (3).pdf")
        self.assertEqual((dest / self.COURSE / "Notes.pdf").read_bytes(), SAME_SIZE_A)
        self.assertEqual((dest / self.COURSE / "Notes (2).pdf").read_bytes(), SAME_SIZE_A)

    def test_identical_rerun_takes_the_fast_path_silently(self):
        dest = Path(tempfile.mkdtemp())
        self._download_into(dest, [70])
        rc, output = self._download_into(dest, [70])
        self.assertEqual(rc, 0, output)
        self.assertEqual([p.name for p in (dest / self.COURSE).iterdir()], ["Notes.pdf"])
        self.assertEqual(_warnings(output), [])

    def test_size_mismatch_keeps_the_suffix_and_never_hashes(self):
        # Sizes differ, so the bytes differ: the suffix rule applies without a hash compare.
        with mock.patch.object(mf, "sha256_file", wraps=mf.sha256_file) as hashed:
            rc, dest, manifest, plan, output = self._run_download_captured([74, 75])
        self.assertEqual(hashed.call_count, 0)
        course = dest / self.COURSE
        self.assertEqual((course / "Notes.pdf").read_bytes(), SAME_SIZE_A)
        self.assertEqual((course / "Notes (2).pdf").read_bytes(), SHORTER)
        self.assertEqual(_warnings(output), [])
        self.assertEqual(rc, 0, output)

    def test_same_size_collision_does_not_pile_up_copies_on_rerun(self):
        dest = Path(tempfile.mkdtemp())
        self._download_into(dest, [70, 71])
        rc, output = self._download_into(dest, [70, 71])
        course = dest / self.COURSE
        self.assertEqual(sorted(p.name for p in course.iterdir()), ["Notes (2).pdf", "Notes.pdf"],
                         "the second run must reuse the copy it already has")
        self.assertEqual((course / "Notes (2).pdf").read_bytes(), SAME_SIZE_B)
        self.assertEqual(rc, 0, output)


class PickDestinationTests(unittest.TestCase):
    """The naming rule on its own, against real files in a scratch folder."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.target = self.dir / "Notes.pdf"

    def _digest(self, data):
        return hashlib.sha256(data).hexdigest()

    def test_free_name_is_used_as_is(self):
        self.assertEqual(mf.pick_destination(self.target, 10, self._digest(b"x" * 10)),
                         (self.target, None))

    def test_identical_file_under_the_name_is_the_fast_path(self):
        self.target.write_bytes(SAME_SIZE_A)
        self.assertEqual(mf.pick_destination(self.target, len(SAME_SIZE_A),
                                             self._digest(SAME_SIZE_A)),
                         (self.target, None))

    def test_different_size_takes_the_next_free_suffix_without_hashing(self):
        self.target.write_bytes(SAME_SIZE_A)
        with mock.patch.object(mf, "sha256_file", wraps=mf.sha256_file) as hashed:
            dest, clash = mf.pick_destination(self.target, len(SHORTER), self._digest(SHORTER))
        self.assertEqual(hashed.call_count, 0)
        self.assertEqual((dest.name, clash), ("Notes (2).pdf", None))

    def test_same_size_different_bytes_is_a_clash_and_gets_a_suffix(self):
        self.target.write_bytes(SAME_SIZE_A)
        dest, clash = mf.pick_destination(self.target, len(SAME_SIZE_B), self._digest(SAME_SIZE_B))
        self.assertEqual((dest.name, clash), ("Notes (2).pdf", self.target))

    def test_walks_past_other_files_to_an_identical_copy_or_a_free_name(self):
        # Notes.pdf and Notes (3).pdf are same-size clashes with the download; the copy at
        # Notes (2).pdf has another size and is skipped without being read.
        other = b"%PDF-1.4\n" + b"D" * 300 + b"\n%%EOF\n"
        self.assertEqual(len(other), len(SAME_SIZE_A))
        self.target.write_bytes(SAME_SIZE_B)
        self.dir.joinpath("Notes (2).pdf").write_bytes(SHORTER)
        self.dir.joinpath("Notes (3).pdf").write_bytes(SAME_SIZE_A)

        dest, clash = mf.pick_destination(self.target, len(SAME_SIZE_A), self._digest(SAME_SIZE_A))
        self.assertEqual((dest.name, clash.name), ("Notes (3).pdf", "Notes.pdf"))

        dest, clash = mf.pick_destination(self.target, len(other), self._digest(other))
        self.assertEqual((dest.name, clash.name), ("Notes (4).pdf", "Notes.pdf"))


# A value distinctive enough that "the secret is absent" means something: a short or
# common string could pass a substring check by coincidence.
SECRET = "zQ7-s3cr3t-moodle-session-value-a1b2c3"
COOKIE = f"MoodleSession={SECRET}"

NETSCAPE_FILE = (
    "# Netscape HTTP Cookie File\n"
    "# https://curl.se/docs/http-cookies.html\n"
    "moodle.example.com\tFALSE\t/\tTRUE\t0\tMoodleSession\t" + SECRET + "\n"
    "moodle.example.com\tFALSE\t/\tFALSE\t0\tMoodleSessionTest\tnotasecret\n"
)

# What curl actually writes: HttpOnly cookies are commented out behind #HttpOnly_.
NETSCAPE_HTTPONLY_FILE = (
    "# Netscape HTTP Cookie File\n"
    "#HttpOnly_moodle.example.com\tFALSE\t/\tTRUE\t0\tMoodleSession\t" + SECRET + "\n"
)


class CookieSourceTests(unittest.TestCase):
    """Cookie source precedence: an explicit flag always beats the ambient environment."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        saved = {k: os.environ.get(k) for k in
                 ("MOODLE_SESSION_COOKIE", "MF_TEST_COOKIE")}
        for k in saved:
            os.environ.pop(k, None)
        self.addCleanup(self._restore, saved)

    @staticmethod
    def _restore(saved):
        for k, v in saved.items():
            os.environ.pop(k, None)
            if v is not None:
                os.environ[k] = v

    def _file(self, text, name="cookies.txt"):
        p = self.tmp / name
        p.write_text(text, encoding="utf-8")
        return p

    # -- precedence ----------------------------------------------------------

    def test_cookie_flag_beats_every_other_source(self):
        os.environ["MOODLE_SESSION_COOKIE"] = "MoodleSession=ambient"
        os.environ["MF_TEST_COOKIE"] = "MoodleSession=from-env"
        args = fake_args(cookie="MoodleSession=explicit",
                         cookie_file=str(self._file("MoodleSession=from-file")),
                         cookie_env="MF_TEST_COOKIE")
        self.assertEqual(mf.resolve_cookie(args), ("MoodleSession=explicit", "--cookie"))

    def test_cookie_file_beats_cookie_env_and_ambient(self):
        os.environ["MOODLE_SESSION_COOKIE"] = "MoodleSession=ambient"
        os.environ["MF_TEST_COOKIE"] = "MoodleSession=from-env"
        args = fake_args(cookie_file=str(self._file("MoodleSession=from-file")),
                         cookie_env="MF_TEST_COOKIE")
        value, source = mf.resolve_cookie(args)
        self.assertEqual(value, "MoodleSession=from-file")
        self.assertTrue(source.startswith("--cookie-file"))

    def test_cookie_env_beats_ambient(self):
        os.environ["MOODLE_SESSION_COOKIE"] = "MoodleSession=ambient"
        os.environ["MF_TEST_COOKIE"] = "MoodleSession=from-env"
        args = fake_args(cookie_env="MF_TEST_COOKIE")
        self.assertEqual(mf.resolve_cookie(args),
                         ("MoodleSession=from-env", "--cookie-env MF_TEST_COOKIE"))

    def test_ambient_env_is_picked_up_when_no_flag_is_given(self):
        os.environ["MOODLE_SESSION_COOKIE"] = "MoodleSession=ambient"
        value, source = mf.resolve_cookie(fake_args())
        self.assertEqual(value, "MoodleSession=ambient")
        self.assertEqual(source, "$MOODLE_SESSION_COOKIE (ambient)")

    def test_blank_ambient_env_is_not_a_cookie(self):
        os.environ["MOODLE_SESSION_COOKIE"] = "   "
        self.assertEqual(mf.resolve_cookie(fake_args()), ("", "none"))

    def test_no_source_at_all_is_reported_as_none(self):
        self.assertEqual(mf.resolve_cookie(fake_args()), ("", "none"))

    def test_cookie_env_pointing_at_an_unset_variable_is_an_error(self):
        with self.assertRaises(SystemExit) as cm:
            mf.resolve_cookie(fake_args(cookie_env="MF_TEST_COOKIE"))
        self.assertIn("MF_TEST_COOKIE", str(cm.exception))

    def test_read_cookie_returns_just_the_value(self):
        self.assertEqual(mf.read_cookie(fake_args(cookie="a=b")), "a=b")

    # -- Netscape parsing ----------------------------------------------------

    def test_netscape_file_parses_name_value_pairs_in_order(self):
        value = mf.cookie_from_text(NETSCAPE_FILE, "test")
        self.assertEqual(value, f"MoodleSession={SECRET}; MoodleSessionTest=notasecret")

    def test_netscape_httponly_row_is_not_skipped(self):
        # The row everybody needs is HttpOnly, and curl comments those rows out.
        self.assertEqual(mf.cookie_from_text(NETSCAPE_HTTPONLY_FILE, "test"), COOKIE)

    def test_netscape_detection(self):
        self.assertTrue(mf.is_netscape(NETSCAPE_FILE))
        self.assertTrue(mf.is_netscape(NETSCAPE_HTTPONLY_FILE))
        self.assertFalse(mf.is_netscape(COOKIE))
        self.assertFalse(mf.is_netscape("MoodleSession=x; Other=y"))

    def test_raw_cookie_header_is_left_alone(self):
        self.assertEqual(mf.cookie_from_text("MoodleSession=abc; Other=1", "test"),
                         "MoodleSession=abc; Other=1")

    def test_wrapped_cookie_header_is_joined(self):
        self.assertEqual(mf.cookie_from_text("MoodleSession=abc;\nOther=1\n", "test"),
                         "MoodleSession=abc; Other=1")

    def test_banner_with_no_rows_is_empty_not_silently_ok(self):
        with self.assertRaises(SystemExit):
            mf.cookie_from_text("# Netscape HTTP Cookie File\n", "test")

    def test_malformed_netscape_row_does_not_echo_the_row(self):
        # The row holds a credential, so the error must describe it, not quote it.
        with self.assertRaises(SystemExit) as cm:
            mf.parse_netscape("example.com\tFALSE\t/\tMoodleSession\t" + SECRET + "\n")
        message = str(cm.exception)
        self.assertNotIn(SECRET, message)
        self.assertIn("7 tab-separated fields", message)

    def test_netscape_file_through_the_flag_path(self):
        p = self._file(NETSCAPE_FILE)
        value, source = mf.resolve_cookie(fake_args(cookie_file=str(p)))
        self.assertEqual(value, f"MoodleSession={SECRET}; MoodleSessionTest=notasecret")
        self.assertEqual(source, f"--cookie-file {p}")

    # -- stdin ---------------------------------------------------------------

    def test_cookie_file_dash_reads_stdin(self):
        with mock.patch.object(sys, "stdin", io.StringIO(COOKIE + "\n")):
            self.assertEqual(mf.resolve_cookie(fake_args(cookie_file="-")),
                             (COOKIE, "--cookie-file - (stdin)"))

    def test_cookie_file_dash_reads_a_netscape_file_from_stdin(self):
        with mock.patch.object(sys, "stdin", io.StringIO(NETSCAPE_FILE)):
            value, _ = mf.resolve_cookie(fake_args(cookie_file="-"))
            self.assertEqual(value, f"MoodleSession={SECRET}; MoodleSessionTest=notasecret")

    def test_cookie_file_dash_refuses_to_read_a_terminal(self):
        terminal = type("T", (), {"isatty": staticmethod(lambda: True),
                                  "read": staticmethod(lambda: ""),
                                  "buffer": None})()
        with mock.patch.object(sys, "stdin", terminal):
            with self.assertRaises(SystemExit) as cm:
                mf.resolve_cookie(fake_args(cookie_file="-"))
        self.assertIn("terminal", str(cm.exception))

    def test_cookie_file_dash_decodes_non_utf8_bytes(self):
        class Pipe(io.BytesIO):
            buffer = property(lambda self: self)
        with mock.patch.object(sys, "stdin", Pipe(COOKIE.encode("cp1252", "replace"))):
            self.assertEqual(mf.resolve_cookie(fake_args(cookie_file="-"))[0], COOKIE)


class CookieLeakTests(ServerMixin):
    """The invariant: a cookie goes on the wire and nowhere else."""

    def _plan_file(self):
        plan = Path(tempfile.mkdtemp()) / "plan.json"
        plan.write_text(json.dumps([{
            "course": "Comprehension and Oral Expression 1",
            "resources": [{"id": 42,
                           "url": f"{self.base}/mod/resource/view.php?id=42"}]}]),
            encoding="utf-8")
        return plan

    def _download(self, extra_env=None, extra_args=None, stdin=None):
        """Run `download` in-process, returning (rc, all output, manifest text, dest)."""
        dest = Path(tempfile.mkdtemp())
        plan = self._plan_file()
        args = {"plan": str(plan), "dest": str(dest), "manifest": None, "update": False,
                "max_bytes": None, "cookie": None, "cookie_file": None, "cookie_env": None,
                "timeout": 10, "insecure": False}
        args.update(extra_args or {})
        buf, saved_env = io.StringIO(), dict(os.environ)
        try:
            if extra_env:
                os.environ.update(extra_env)
            ctx = (mock.patch.object(sys, "stdin", io.StringIO(stdin))
                   if stdin is not None else contextlib.nullcontext())
            with ctx, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                rc = mf.cmd_download(fake_args(**args))
        finally:
            os.environ.clear()
            os.environ.update(saved_env)
        return rc, buf.getvalue(), (dest / "manifest.json").read_text(encoding="utf-8"), dest

    def _assert_clean(self, rc, output, manifest_text, label):
        self.assertEqual(rc, 0, f"{label}: download failed ->\n{output}")
        self.assertNotIn(SECRET, output, f"{label}: cookie value appeared on stdout/stderr")
        self.assertNotIn(SECRET, manifest_text, f"{label}: cookie value in manifest.json")
        self.assertNotIn("Cookie", manifest_text, f"{label}: cookie header in manifest.json")

    def test_cookie_never_reaches_manifest_or_output_for_any_source(self):
        netscape = Path(tempfile.mkdtemp()) / "cookies.txt"
        netscape.write_text(NETSCAPE_FILE, encoding="utf-8")
        cases = [
            ("--cookie", {"cookie": COOKIE}, None, None),
            ("--cookie-env", {"cookie_env": "MF_TEST_COOKIE"},
             {"MF_TEST_COOKIE": COOKIE}, None),
            ("--cookie-file -", {"cookie_file": "-"}, None, COOKIE + "\n"),
            ("--cookie-file <netscape>", {"cookie_file": str(netscape)}, None, None),
            ("$MOODLE_SESSION_COOKIE", {}, {"MOODLE_SESSION_COOKIE": COOKIE}, None),
        ]
        for label, extra_args, extra_env, stdin in cases:
            with self.subTest(source=label):
                self._assert_clean(*self._download(extra_env, extra_args, stdin)[:3], label)

    def test_ambient_pickup_is_announced_without_the_value(self):
        rc, output, manifest_text, _ = self._download({"MOODLE_SESSION_COOKIE": COOKIE})
        self.assertEqual(rc, 0, output)
        self.assertIn("MOODLE_SESSION_COOKIE", output)   # the source is safe to print
        self.assertNotIn(SECRET, output)                 # the value is not

    def test_no_cookie_file_is_written_when_the_cookie_came_from_a_pipe(self):
        _, _, _, dest = self._download(extra_args={"cookie_file": "-"}, stdin=COOKIE + "\n")
        self.assertEqual(list(dest.glob("**/*cookies*")), [],
                         "a piped cookie must not be persisted into the destination")

    def test_cli_download_does_not_leak_the_cookie_either(self):
        """Same invariant, through the real command line instead of in-process calls."""
        dest = Path(tempfile.mkdtemp())
        plan = self._plan_file()
        env = dict(os.environ, MOODLE_SESSION_COOKIE=COOKIE)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "download", str(plan), "--dest", str(dest)],
            env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90)
        blob = proc.stdout.decode("utf-8", "replace") + proc.stderr.decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 0, blob)
        self.assertNotIn(SECRET, blob, "cookie value appeared in CLI output")
        self.assertNotIn(SECRET, (dest / "manifest.json").read_text(encoding="utf-8"),
                         "cookie value appeared in manifest.json")


if __name__ == "__main__":
    sys.exit(unittest.main(verbosity=2))
