#!/usr/bin/env python3
"""Offline tests for scripts/jinx_link.py — the PC-side Jinx Talk service.

Stdlib-only, network-free and game-free, like every other suite in this skill:

  * ``jinx_link.py`` imports ``ai_service`` — the helper module that ships next
    to it on the PC (SNBT readers, chapter status, the inbox writer), which is
    not part of this repository. The suite therefore injects a minimal
    stand-in into ``sys.modules`` before loading the module under test, so
    nothing here needs a Minecraft save, a KubeJS instance or a running LLM.
  * ``ask_llm`` and ``speak`` are monkeypatched per test: no request ever
    leaves the process, and no TTS engine is touched (``speak`` is a no-op off
    Windows anyway).
  * the HTTP API is exercised for real — ``start_http_server`` binds
    127.0.0.1 on an ephemeral port inside this process and the tests talk to
    it over a socket, which is exactly the "throwaway localhost server" the CI
    workflow describes. Nothing binds a non-loopback address.

Covered:

  * GET /health -> {"ok": true}; unknown paths -> a JSON 404 (GET and POST);
  * POST /chat -> the reply is built the same way the file flow builds it
    (persona first, the live CONTEXT block from the quest context, the short
    chat history, ``clean_reply`` cleaning), on a 20-second LLM timeout, is
    spoken, is appended to the shared history, and is returned in the response
    body *without* ever being written to kubejs/ai/inbox.json; a failing or
    empty LLM answer yields the quest-aware ``fallback_reply`` with the same
    200 status; the second call in a conversation carries the first exchange;
  * POST /event -> {"announce": "Chapter complete: <quest>! Nice work."} with
    the quest title from the body used verbatim and spoken; any other event
    type -> {} and no speech;
  * GET /cues -> drains: every queued cue is handed out exactly once and the
    next call returns an empty list; the sync's newly completed chapters each
    produce one {"kind": "chat", ...} cue naming the next quest (or "check the
    quest book"); the queue is capped, dropping the oldest cue rather than
    growing without a reader;
  * robustness: malformed JSON, an empty body, a non-object body, a missing
    message, a missing quest title -> 400 JSON with an "error"; a byte stream
    that is not even HTTP is logged on stderr and the server still answers the
    next request; a busy port or a non-loopback --http-host degrades to the
    file flow (start_http_server returns None) instead of raising;
  * the pre-existing file flow is untouched: answer_one still chunks into the
    inbox with the "[Jinx] " prefix on the 90-second timeout, outbox offsets
    and partial/corrupt lines behave as before, state round-trips, and the CLI
    keeps every old flag while adding --http-host/--http-port/--no-http;
  * run() itself: one loop iteration starts the HTTP server on a daemon
    thread, runs the sync, queues the cues, answers the outbox line into the
    inbox and persists the state file.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import http.client
import importlib.util
import inspect
import io
import json
import socket
import sys
import tempfile
import threading
import types
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
JINX_LINK_PY = SCRIPTS / "jinx_link.py"


# ---------------------------------------------------------------------------
# ai_service stand-in (the real one ships next to jinx_link.py on the PC)
# ---------------------------------------------------------------------------

def make_fake_ai_service() -> types.ModuleType:
    """A mutable stand-in for the ``ai_service`` module jinx_link.py imports.

    Only the helpers jinx_link.py actually calls exist here. Canned progress
    data lives on the module so a test can reshape it, and every side effect
    (inbox write, sync call) is recorded instead of touching a game install.
    """
    mod = types.ModuleType("ai_service")

    # canned quest data (gather_quest_ctx reads all of these)
    mod.team_path = None            # set per test: a real file on disk
    mod.completed: "list[str]" = ["1111", "2222", "3333"]
    mod.chapters: "dict[str, dict]" = {
        "welcome": {"id": "welcome"},
        "mekanism": {"id": "mekanism"},
        "create": {"id": "create"},
    }
    mod.titles: "dict[str, str]" = {"mekanism": "Mekanism", "welcome": "Welcome"}
    mod.status: "dict[str, dict]" = {
        "welcome": {"state": "done", "done": 9, "total": 9},
        "mekanism": {"state": "partial", "done": 12, "total": 40},
        "create": {"state": "partial", "done": 3, "total": 30},
    }
    mod.next_list: "list[dict]" = [
        {"title": "Digital Miner", "chapter_title": "Mekanism"},
        {"title": "Quarry", "chapter_title": "Create"},
    ]
    mod.sync_result: "tuple" = (None, [], [])

    # recorded side effects
    mod.inbox_writes: "list[tuple]" = []
    mod.sync_calls: "list[tuple]" = []

    def find_world(saves, world):
        return world or str(Path(saves or ".") / "world")

    def find_team_file(world_dir):
        if mod.team_path is None:
            raise FileNotFoundError("no team file configured in the test fake")
        return mod.team_path

    def extract_completed_ids(text):
        return list(mod.completed)

    def load_chapters(chapters_dir):
        return dict(mod.chapters)

    def load_titles(lang_file):
        return dict(mod.titles)

    def chapter_status(chapters, completed):
        return dict(mod.status)

    def next_quests(chapters, status, completed, titles, limit=5):
        return list(mod.next_list)[:limit]

    def write_inbox(instance_dir, directives):
        mod.inbox_writes.append((instance_dir, directives))
        return True

    def sync(world, chapters, lang, out_dir, instance, state_path):
        mod.sync_calls.append((world, chapters, lang, out_dir, instance, state_path))
        return mod.sync_result

    mod.find_world = find_world
    mod.find_team_file = find_team_file
    mod.extract_completed_ids = extract_completed_ids
    mod.load_chapters = load_chapters
    mod.load_titles = load_titles
    mod.chapter_status = chapter_status
    mod.next_quests = next_quests
    mod.write_inbox = write_inbox
    mod.sync = sync
    return mod


FAKE_AI_SERVICE = make_fake_ai_service()


def load_jinx_link(fake_ai_service: types.ModuleType):
    """Import scripts/jinx_link.py with ``ai_service`` resolved to the fake."""
    saved = sys.modules.get("ai_service")
    sys.modules["ai_service"] = fake_ai_service
    try:
        spec = importlib.util.spec_from_file_location("jinx_link_under_test", JINX_LINK_PY)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if saved is None:
            sys.modules.pop("ai_service", None)
        else:
            sys.modules["ai_service"] = saved
    return module


jl = load_jinx_link(FAKE_AI_SERVICE)

# A quest context of the shape gather_quest_ctx() returns, reused by the HTTP
# tests so they exercise the endpoints without any save-file reading.
CTX = {
    "chapters_done": 2,
    "chapters_total": 66,
    "quests_done": 41,
    "in_progress": [{"title": "Mekanism", "done": 12, "total": 40}],
    "suggested_next": [{"quest": "Digital Miner", "chapter": "Mekanism"}],
}

CHAT_BODY = {
    "player": "Nader",
    "message": "what should I do next?",
    "pos": [100, 64, -200],
    "dim": "minecraft:overworld",
    "ts": 1_760_000_000_000,
}

_UNSET = object()


# ---------------------------------------------------------------------------
# HTTP client helper (stdlib only, loopback only)
# ---------------------------------------------------------------------------

def http_call(port: int, method: str, path: str, payload=_UNSET, raw: "bytes | None" = None,
              timeout: float = 15.0) -> "tuple[int, object]":
    """One request to the in-process server -> (status, decoded JSON body)."""
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=timeout)
    try:
        if raw is not None:
            body: "bytes | str | None" = raw
        elif payload is _UNSET:
            body = None
        else:
            body = json.dumps(payload)
        conn.request(method, path, body=body, headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        data = resp.read()
        return resp.status, (json.loads(data.decode("utf-8")) if data else None)
    finally:
        conn.close()


class JinxLinkTestCase(unittest.TestCase):
    """Common fixture: quiet streams, patched speak(), clean fake recorders."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.tmp_path = Path(self.tmp.name)

        # the service prints one line per answer and logs requests on stderr;
        # keep both out of the CI log, and readable for the assertions below.
        self.captured_err = io.StringIO()
        self.captured_out = io.StringIO()
        for redirect in (contextlib.redirect_stderr(self.captured_err),
                         contextlib.redirect_stdout(self.captured_out)):
            redirect.__enter__()
            self.addCleanup(redirect.__exit__, None, None, None)

        FAKE_AI_SERVICE.inbox_writes.clear()
        FAKE_AI_SERVICE.sync_calls.clear()
        FAKE_AI_SERVICE.team_path = None
        FAKE_AI_SERVICE.sync_result = (None, [], [])

        self.spoken: "list[tuple[str, bool]]" = []
        self._patch(jl, "speak",
                    lambda text, enabled: self.spoken.append((text, enabled)) or True)

        self.instance = str(self.tmp_path / "instance")
        self.args = self.make_args()

    # -- helpers --------------------------------------------------------

    def _patch(self, obj, name, value):
        self.addCleanup(setattr, obj, name, getattr(obj, name))
        setattr(obj, name, value)

    def make_args(self, **overrides):
        """An argparse.Namespace with every attribute jinx_link.py reads."""
        values = {
            "world": str(self.tmp_path / "world"),
            "saves": None,
            "chapters": str(self.tmp_path / "chapters"),
            "lang": None,
            "instance": self.instance,
            "out": str(self.tmp_path / "out"),
            "llm_url": "http://localhost:8080/v1",
            "model": "local-model",
            "interval": 0,
            "sync_interval": 15,
            "voice": True,
            "http_host": "127.0.0.1",
            "http_port": 0,          # ephemeral: never fight CI over a port
            "no_http": False,
            "selftest": False,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def make_hub(self, ctx=None, state=None, **arg_overrides):
        args = self.make_args(**arg_overrides) if arg_overrides else self.args
        return jl.LinkHub(args, CTX if ctx is None else ctx,
                          {"offset": 0, "history": []} if state is None else state)

    def serve(self, hub) -> int:
        """Start the real server on an ephemeral loopback port -> the port."""
        httpd = jl.start_http_server(hub, "127.0.0.1", 0)
        self.assertIsNotNone(httpd, "the server refused an ephemeral loopback port")
        self.addCleanup(jl.stop_http_server, httpd)
        port = httpd.server_address[1]
        self.assertNotEqual(port, 0)
        return port

    def patch_llm(self, reply=None, error=None):
        """Replace ask_llm with a recorder -> the list of calls it received."""
        calls: "list[dict]" = []

        def fake_ask_llm(base_url, model, api_key, messages, timeout=90):
            calls.append({"base_url": base_url, "model": model, "api_key": api_key,
                          "messages": messages, "timeout": timeout})
            if error is not None:
                raise error
            return reply

        self._patch(jl, "ask_llm", fake_ask_llm)
        return calls

    def write_team_file(self) -> Path:
        """A stand-in team .snbt so gather_quest_ctx() can open something real."""
        path = self.tmp_path / "team.snbt"
        path.write_text('{ completed: [ "1111", "2222" ] }', encoding="utf-8")
        FAKE_AI_SERVICE.team_path = str(path)
        return path


# ---------------------------------------------------------------------------
# /health and routing
# ---------------------------------------------------------------------------

class TestHealthAndRouting(JinxLinkTestCase):
    def test_health_reports_ok(self):
        port = self.serve(self.make_hub())
        status, body = http_call(port, "GET", "/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"ok": True})

    def test_health_needs_no_body_and_no_llm(self):
        calls = self.patch_llm(reply="never used")
        port = self.serve(self.make_hub())
        self.assertEqual(http_call(port, "GET", "/health")[0], 200)
        self.assertEqual(calls, [])

    def test_unknown_path_is_a_json_404(self):
        port = self.serve(self.make_hub())
        for method, payload in (("GET", _UNSET), ("POST", {"message": "hi"})):
            status, body = http_call(port, method, "/nope", payload=payload)
            self.assertEqual(status, 404, method)
            self.assertIsInstance(body, dict)
            self.assertIn("error", body)

    def test_query_string_does_not_change_routing(self):
        port = self.serve(self.make_hub())
        status, body = http_call(port, "GET", "/health?probe=1")
        self.assertEqual((status, body), (200, {"ok": True}))

    def test_unsupported_method_never_crashes_the_server(self):
        port = self.serve(self.make_hub())
        status, body = http_call(port, "PUT", "/chat", payload=CHAT_BODY)
        self.assertEqual(status, 404)
        self.assertIn("error", body)
        self.assertEqual(http_call(port, "GET", "/health"), (200, {"ok": True}))


# ---------------------------------------------------------------------------
# POST /chat
# ---------------------------------------------------------------------------

class TestHttpChat(JinxLinkTestCase):
    def test_reply_is_returned_and_never_written_to_the_inbox(self):
        calls = self.patch_llm(reply="Grab the Digital Miner, then set up power.")
        hub = self.make_hub()
        port = self.serve(hub)

        status, body = http_call(port, "POST", "/chat", payload=CHAT_BODY)

        self.assertEqual(status, 200)
        self.assertEqual(body, {"reply": "Grab the Digital Miner, then set up power."})
        self.assertEqual(FAKE_AI_SERVICE.inbox_writes, [],
                         "an HTTP reply goes back to the mod, never into inbox.json")
        self.assertEqual(len(calls), 1)

    def test_llm_prompt_matches_the_file_flow(self):
        calls = self.patch_llm(reply="ok")
        port = self.serve(self.make_hub())
        http_call(port, "POST", "/chat", payload=CHAT_BODY)

        messages = calls[0]["messages"]
        self.assertEqual(messages[0], {"role": "system", "content": jl.PERSONA})
        prompt = messages[-1]["content"]
        self.assertEqual(messages[-1]["role"], "user")
        self.assertIn("CONTEXT (from the save files, trust this):", prompt)
        self.assertIn("Quest chapters complete: 2 of 66. Quests done: 41.", prompt)
        self.assertIn("In progress: Mekanism (12/40 quests).", prompt)
        self.assertIn("Suggested next quest: Digital Miner (chapter: Mekanism).", prompt)
        self.assertIn("Player Nader is at [100, 64, -200] in minecraft:overworld.", prompt)
        self.assertTrue(prompt.endswith("Nader asks: what should I do next?"))
        self.assertEqual(calls[0]["base_url"], "http://localhost:8080/v1")
        self.assertEqual(calls[0]["model"], "local-model")

    def test_http_path_uses_the_short_20_second_timeout(self):
        calls = self.patch_llm(reply="ok")
        port = self.serve(self.make_hub())
        http_call(port, "POST", "/chat", payload=CHAT_BODY)
        self.assertEqual(jl.HTTP_LLM_TIMEOUT, 20)
        self.assertEqual(calls[0]["timeout"], jl.HTTP_LLM_TIMEOUT)

    def test_file_flow_keeps_the_long_timeout(self):
        # the mod stops reading after ~25s; the outbox poller has no such deadline.
        self.assertEqual(jl.LLM_TIMEOUT, 90)
        self.assertEqual(inspect.signature(jl.ask_llm).parameters["timeout"].default, 90)
        calls = self.patch_llm(reply="still 90s for the file flow")
        jl.answer_one(dict(CHAT_BODY), CTX, {"offset": 0, "history": []}, self.args)
        self.assertEqual(calls[0]["timeout"], 90)

    def test_reply_is_cleaned_like_the_file_flow(self):
        hub = self.make_hub()
        port = self.serve(hub)
        cases = [
            ("```\nGo get the miner.\n```", "Go get the miner."),   # fences unwrapped
            ("Jinx: Go get the miner.", "Go get the miner."),        # name prefix dropped
            ("ASSISTANT:   two   spaces\nand a newline", "ASSISTANT: two spaces and a newline"
             .replace("ASSISTANT: ", "")),                           # whitespace collapsed
            ("x" * 900, "x" * 600),                                  # still capped at 600
        ]
        for raw, expected in cases:
            self.patch_llm(reply=raw)
            status, body = http_call(port, "POST", "/chat", payload=CHAT_BODY)
            self.assertEqual(status, 200, raw)
            self.assertEqual(body["reply"], expected, raw)
            self.assertEqual(body["reply"], jl.clean_reply(raw),
                             "the HTTP path cleans exactly like the file path")

    def test_reply_is_spoken_and_remembers_in_the_shared_history(self):
        self.patch_llm(reply="Build the miner first.")
        hub = self.make_hub()
        port = self.serve(hub)
        http_call(port, "POST", "/chat", payload=CHAT_BODY)

        self.assertEqual(self.spoken, [("Build the miner first.", True)])
        self.assertEqual(hub.state["history"], [
            {"role": "user", "content": "what should I do next?"},
            {"role": "assistant", "content": "Build the miner first."},
        ])
        self.assertEqual(hub.history(), hub.state["history"])

    def test_voice_off_still_answers_but_says_nothing(self):
        self.patch_llm(reply="silent answer")
        hub = self.make_hub(voice=False)
        port = self.serve(hub)
        _, body = http_call(port, "POST", "/chat", payload=CHAT_BODY)
        self.assertEqual(body["reply"], "silent answer")
        self.assertEqual(self.spoken, [("silent answer", False)])

    def test_second_chat_carries_the_first_exchange(self):
        calls: "list[dict]" = []
        replies = iter(["first answer", "second answer"])

        def fake_ask_llm(base_url, model, api_key, messages, timeout=20):
            calls.append(messages)
            return next(replies)

        self._patch(jl, "ask_llm", fake_ask_llm)
        hub = self.make_hub()
        port = self.serve(hub)
        self.assertEqual(http_call(port, "POST", "/chat", payload=CHAT_BODY)[1],
                         {"reply": "first answer"})
        self.assertEqual(http_call(port, "POST", "/chat",
                                   payload=dict(CHAT_BODY, message="and then?"))[1],
                         {"reply": "second answer"})

        self.assertEqual([m["role"] for m in calls[0]], ["system", "user"])
        self.assertEqual([m["role"] for m in calls[1]],
                         ["system", "user", "assistant", "user"],
                         "the short history travels with the next question")
        self.assertEqual(calls[1][1]["content"], "what should I do next?")
        self.assertEqual(calls[1][2]["content"], "first answer")
        self.assertTrue(calls[1][3]["content"].endswith("Nader asks: and then?"))
        self.assertEqual(hub.state["history"], [
            {"role": "user", "content": "what should I do next?"},
            {"role": "assistant", "content": "first answer"},
            {"role": "user", "content": "and then?"},
            {"role": "assistant", "content": "second answer"},
        ])
        self.assertEqual(hub.history(), hub.state["history"])

    def test_llm_failure_falls_back_with_a_quest_aware_answer(self):
        self.patch_llm(error=OSError("connection refused"))
        hub = self.make_hub()
        port = self.serve(hub)

        status, body = http_call(port, "POST", "/chat", payload=CHAT_BODY)

        expected = jl.fallback_reply(CTX, CHAT_BODY["message"])
        self.assertEqual(status, 200, "a fallback reply beats a timeout for the mod")
        self.assertEqual(body, {"reply": expected})
        self.assertIn("chapters 2/66 done", body["reply"])
        self.assertIn("mid-way through Mekanism (12/40)", body["reply"])
        self.assertIn("Suggested next: Digital Miner", body["reply"])
        self.assertIn("LLM error", self.captured_err.getvalue())
        self.assertEqual(FAKE_AI_SERVICE.inbox_writes, [])
        self.assertEqual(self.spoken, [(expected, True)])
        self.assertEqual(hub.state["history"][-1]["content"], expected[:300])

    def test_empty_llm_reply_also_falls_back(self):
        self.patch_llm(reply="```")
        port = self.serve(self.make_hub())
        _, body = http_call(port, "POST", "/chat", payload=CHAT_BODY)
        self.assertEqual(body["reply"], jl.fallback_reply(CTX, CHAT_BODY["message"]))

    def test_chat_uses_the_live_context_the_loop_refreshed(self):
        hub = self.make_hub()
        port = self.serve(hub)
        calls = self.patch_llm(reply="ok")
        hub.set_ctx(dict(CTX, chapters_done=9, quests_done=120))
        http_call(port, "POST", "/chat", payload=CHAT_BODY)
        self.assertIn("Quest chapters complete: 9 of 66. Quests done: 120.",
                      calls[0]["messages"][-1]["content"])
        self.assertEqual(hub.get_ctx()["chapters_done"], 9)

    def test_missing_or_empty_message_is_a_400(self):
        calls = self.patch_llm(reply="never used")
        port = self.serve(self.make_hub())
        for body in ({"player": "Nader"},
                     {"player": "Nader", "message": "   "},
                     {"player": "Nader", "message": 42}):
            status, payload = http_call(port, "POST", "/chat", payload=body)
            self.assertEqual(status, 400, body)
            self.assertIn("message", payload["error"])
        self.assertEqual(calls, [], "a rejected body must not reach the LLM")

    def test_position_and_dimension_are_optional(self):
        calls = self.patch_llm(reply="ok")
        port = self.serve(self.make_hub())
        status, body = http_call(port, "POST", "/chat",
                                 payload={"player": "Nader", "message": "hi"})
        self.assertEqual((status, body), (200, {"reply": "ok"}))
        self.assertNotIn("is at", calls[0]["messages"][-1]["content"])


# ---------------------------------------------------------------------------
# POST /event
# ---------------------------------------------------------------------------

class TestHttpEvent(JinxLinkTestCase):
    def test_quest_completed_is_announced_verbatim_and_spoken(self):
        port = self.serve(self.make_hub())
        status, body = http_call(port, "POST", "/event", payload={
            "type": "quest_completed", "quest": "Mekanism", "player": "Nader"})
        self.assertEqual(status, 200)
        self.assertEqual(body, {"announce": "Chapter complete: Mekanism! Nice work."})
        self.assertEqual(self.spoken, [("Chapter complete: Mekanism! Nice work.", True)])
        self.assertEqual(FAKE_AI_SERVICE.inbox_writes, [])

    def test_quest_title_is_used_exactly_as_sent(self):
        port = self.serve(self.make_hub())
        quest = "Chapter 2: Allthemodium & The Other  "
        _, body = http_call(port, "POST", "/event",
                            payload={"type": "quest_completed", "quest": quest})
        self.assertEqual(body["announce"], "Chapter complete: %s! Nice work." % quest)

    def test_voice_off_does_not_speak_the_announce(self):
        hub = self.make_hub(voice=False)
        port = self.serve(hub)
        http_call(port, "POST", "/event",
                  payload={"type": "quest_completed", "quest": "Create"})
        self.assertEqual(self.spoken, [("Chapter complete: Create! Nice work.", False)])

    def test_any_other_event_type_is_an_empty_200(self):
        port = self.serve(self.make_hub())
        for payload in ({"type": "player_died", "player": "Nader"},
                        {"type": ""},
                        {"type": "quest_started", "quest": "Mekanism"},
                        {"player": "Nader"}):
            status, body = http_call(port, "POST", "/event", payload=payload)
            self.assertEqual(status, 200, payload)
            self.assertEqual(body, {}, payload)
        self.assertEqual(self.spoken, [])

    def test_quest_completed_without_a_title_is_a_400(self):
        port = self.serve(self.make_hub())
        for payload in ({"type": "quest_completed"},
                        {"type": "quest_completed", "quest": "  "}):
            status, body = http_call(port, "POST", "/event", payload=payload)
            self.assertEqual(status, 400, payload)
            self.assertIn("quest", body["error"])
        self.assertEqual(self.spoken, [])


# ---------------------------------------------------------------------------
# GET /cues — drain semantics, and the sync that fills the queue
# ---------------------------------------------------------------------------

class TestCueQueue(JinxLinkTestCase):
    def test_cues_are_drained_exactly_once(self):
        hub = self.make_hub()
        port = self.serve(hub)
        hub.enqueue_cue({"kind": "chat", "text": "Chapter complete: Mekanism."})
        hub.enqueue_cue({"kind": "chat", "text": "Chapter complete: Create."})

        status, body = http_call(port, "GET", "/cues")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"cues": [
            {"kind": "chat", "text": "Chapter complete: Mekanism."},
            {"kind": "chat", "text": "Chapter complete: Create."},
        ]})

        self.assertEqual(http_call(port, "GET", "/cues"), (200, {"cues": []}))
        self.assertEqual(http_call(port, "GET", "/cues"), (200, {"cues": []}))

    def test_new_cues_arrive_after_a_drain(self):
        hub = self.make_hub()
        port = self.serve(hub)
        self.assertEqual(http_call(port, "GET", "/cues")[1], {"cues": []})
        hub.enqueue_cue({"kind": "chat", "text": "later"})
        self.assertEqual(http_call(port, "GET", "/cues")[1], {"cues": [{"kind": "chat",
                                                                       "text": "later"}]})

    def test_draining_is_thread_safe_under_concurrent_readers(self):
        hub = self.make_hub()
        port = self.serve(hub)
        for i in range(40):
            hub.enqueue_cue({"kind": "chat", "text": "cue %d" % i})

        seen: "list[dict]" = []
        lock = threading.Lock()

        def reader():
            _, body = http_call(port, "GET", "/cues")
            with lock:
                seen.extend(body["cues"])

        threads = [threading.Thread(target=reader) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(15)
        self.assertEqual(len(seen), 40, "every cue is handed to exactly one reader")
        self.assertEqual(len({c["text"] for c in seen}), 40)

    def test_the_queue_is_capped_and_drops_the_oldest(self):
        hub = self.make_hub()
        for i in range(jl.MAX_CUES + 5):
            hub.enqueue_cue({"kind": "chat", "text": "cue %d" % i})
        cues = hub.drain_cues()
        self.assertEqual(len(cues), jl.MAX_CUES)
        self.assertEqual(cues[0]["text"], "cue 5")
        self.assertEqual(cues[-1]["text"], "cue %d" % (jl.MAX_CUES + 4))

    def test_newly_completed_chapters_each_queue_one_cue(self):
        hub = self.make_hub()
        jl.announce_new_chapters(["mekanism", "create"],
                                 [{"title": "Digital Miner"}],
                                 {"mekanism": "Mekanism", "create": "Create"},
                                 self.args, hub)
        self.assertEqual(hub.drain_cues(), [
            {"kind": "chat", "text": "Chapter complete: Mekanism. Suggested next: Digital Miner"},
            {"kind": "chat", "text": "Chapter complete: Create. Suggested next: Digital Miner"},
        ])
        self.assertEqual([text for text, enabled in self.spoken],
                         ["Chapter complete: Mekanism. Suggested next: Digital Miner",
                          "Chapter complete: Create. Suggested next: Digital Miner"],
                         "the spoken line and the cue say the same thing")
        self.assertEqual([enabled for _, enabled in self.spoken], [True, True])

    def test_without_a_next_quest_the_cue_points_at_the_quest_book(self):
        hub = self.make_hub()
        jl.announce_new_chapters(["unknown_id"], [], {}, self.args, hub)
        self.assertEqual(hub.drain_cues(), [{
            "kind": "chat",
            "text": "Chapter complete: unknown_id. Suggested next: check the quest book",
        }])

    def test_no_new_chapters_means_no_cues_and_no_speech(self):
        hub = self.make_hub()
        jl.announce_new_chapters([], [{"title": "Digital Miner"}], {}, self.args, hub)
        self.assertEqual(hub.drain_cues(), [])
        self.assertEqual(self.spoken, [])


# ---------------------------------------------------------------------------
# Robustness: bad bodies, junk bytes, unbindable sockets
# ---------------------------------------------------------------------------

class TestRobustness(JinxLinkTestCase):
    def test_malformed_json_body_is_a_400_with_an_error(self):
        calls = self.patch_llm(reply="never used")
        hub = self.make_hub()
        port = self.serve(hub)
        for raw in (b"{not json at all", b'{"message": "unclosed', b"\xff\xfe\x00binary"):
            status, body = http_call(port, "POST", "/chat", raw=raw)
            self.assertEqual(status, 400, raw)
            self.assertIsInstance(body, dict)
            self.assertIn("error", body)
            self.assertTrue(body["error"], "the 400 must say what was wrong")
        self.assertEqual(calls, [])
        self.assertEqual(hub.state["history"], [])
        self.assertEqual(http_call(port, "GET", "/health"), (200, {"ok": True}),
                         "a bad body must not take the server down")

    def test_empty_and_non_object_bodies_are_400s(self):
        port = self.serve(self.make_hub())
        self.assertEqual(http_call(port, "POST", "/chat")[0], 400)         # no body at all
        self.assertEqual(http_call(port, "POST", "/event")[0], 400)
        status, body = http_call(port, "POST", "/chat", payload=[1, 2, 3])
        self.assertEqual(status, 400)
        self.assertIn("JSON object", body["error"])
        status, body = http_call(port, "POST", "/chat", payload="just a string")
        self.assertEqual(status, 400)
        self.assertIn("JSON object", body["error"])

    def test_small_bodies_work_and_oversized_ones_are_refused(self):
        port = self.serve(self.make_hub())
        self.patch_llm(reply="ok")
        self.assertEqual(http_call(port, "POST", "/chat",
                                   payload={"message": "x" * 64})[0], 200,
                         "an ordinary body is served")
        # lie about a huge length: the handler refuses before allocating it
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=15)
        self.addCleanup(conn.close)
        conn.putrequest("POST", "/chat")
        conn.putheader("Content-Type", "application/json")
        conn.putheader("Content-Length", str(jl.MAX_BODY_BYTES + 1))
        conn.endheaders(message_body=b'{"message": "hi"}')
        resp = conn.getresponse()
        payload = json.loads(resp.read().decode("utf-8"))
        self.assertEqual(resp.status, 400)
        self.assertIn("too large", payload["error"])

    def test_a_lying_content_length_is_a_400(self):
        port = self.serve(self.make_hub())
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=15)
        self.addCleanup(conn.close)
        conn.putrequest("POST", "/chat")
        conn.putheader("Content-Length", "not-a-number")
        conn.endheaders()
        resp = conn.getresponse()
        payload = json.loads(resp.read().decode("utf-8"))
        self.assertEqual(resp.status, 400)
        self.assertIn("Content-Length", payload["error"])

    def test_a_request_that_is_not_even_http_is_logged_and_survived(self):
        port = self.serve(self.make_hub())
        with socket.create_connection(("127.0.0.1", port), timeout=10) as sock:
            sock.sendall(b"GARBAGE THAT IS NOT HTTP\r\n\r\n")
            try:
                sock.recv(4096)
            except OSError:
                pass
        with socket.create_connection(("127.0.0.1", port), timeout=10) as sock:
            sock.sendall(b"POST /chat HTTP/1.1\r\nHost: x\r\nContent-Length: 999\r\n\r\n")
            sock.close()          # hangs up mid-body: the handler must cope
        self.assertEqual(http_call(port, "GET", "/health"), (200, {"ok": True}),
                         "broken requests must never stop the service")
        self.assertIn("http:", self.captured_err.getvalue())

    def test_a_handler_crash_answers_500_and_keeps_serving(self):
        hub = self.make_hub()
        port = self.serve(hub)

        def boom(_hub):
            raise RuntimeError("synthetic handler failure")

        self._patch(jl.LinkHub, "drain_cues", boom)
        status, body = http_call(port, "GET", "/cues")
        self.assertEqual(status, 500)
        self.assertIn("error", body)
        self.assertIn("synthetic handler failure", self.captured_err.getvalue())
        self._patch(jl.LinkHub, "drain_cues", lambda _hub: [])
        self.assertEqual(http_call(port, "GET", "/health"), (200, {"ok": True}))

    def test_a_non_loopback_host_is_refused_not_bound(self):
        hub = self.make_hub()
        for host in ("0.0.0.0", "192.168.1.50", "::", "example.com", ""):
            self.assertIsNone(jl.start_http_server(hub, host, 0), host)
        self.assertIn("localhost only", self.captured_err.getvalue())

    def test_loopback_detection(self):
        for host in ("127.0.0.1", "127.0.0.2", "::1", "localhost"):
            self.assertTrue(jl.is_loopback_host(host), host)
        for host in ("0.0.0.0", "192.168.1.50", "10.0.0.1", "::", "example.com"):
            self.assertFalse(jl.is_loopback_host(host), host)

    def test_a_busy_port_degrades_to_the_file_flow(self):
        hub = self.make_hub()
        first = jl.start_http_server(hub, "127.0.0.1", 0)
        self.assertIsNotNone(first)
        self.addCleanup(jl.stop_http_server, first)
        busy_port = first.server_address[1]
        self.assertIsNone(jl.start_http_server(hub, "127.0.0.1", busy_port))
        self.assertIn("cannot listen", self.captured_err.getvalue())
        self.assertEqual(http_call(busy_port, "GET", "/health"), (200, {"ok": True}),
                         "the first server is untouched by the failed bind")

    def test_stop_http_server_tolerates_none(self):
        jl.stop_http_server(None)          # --no-http / a refused bind: nothing to do


# ---------------------------------------------------------------------------
# The pre-existing file flow must behave exactly as before
# ---------------------------------------------------------------------------

class TestFileFlowUnchanged(JinxLinkTestCase):
    def test_answer_one_writes_chunked_inbox_directives_and_speaks(self):
        calls = self.patch_llm(reply="Go get the Digital Miner.")
        state = {"offset": 0, "history": []}
        jl.answer_one(dict(CHAT_BODY), CTX, state, self.args)

        self.assertEqual(len(FAKE_AI_SERVICE.inbox_writes), 1)
        instance, directives = FAKE_AI_SERVICE.inbox_writes[0]
        self.assertEqual(instance, self.instance)
        self.assertEqual(directives, [{"kind": "chat", "prefix": "[Jinx] ",
                                       "message": "Go get the Digital Miner."}])
        self.assertEqual(calls[0]["timeout"], 90)
        self.assertEqual(self.spoken, [("Go get the Digital Miner.", True)])
        self.assertEqual(state["history"], [
            {"role": "user", "content": "what should I do next?"},
            {"role": "assistant", "content": "Go get the Digital Miner."},
        ])
        self.assertIn("answered Nader", self.captured_out.getvalue())

    def test_answer_one_falls_back_into_the_inbox_when_the_llm_is_down(self):
        self.patch_llm(error=OSError("no route to host"))
        state = {"offset": 0, "history": []}
        jl.answer_one(dict(CHAT_BODY), CTX, state, self.args)
        expected = jl.fallback_reply(CTX, CHAT_BODY["message"])
        directives = FAKE_AI_SERVICE.inbox_writes[0][1]
        self.assertEqual(" ".join(d["message"] for d in directives), expected,
                         "the fallback is chunked into the inbox, exactly as before")
        self.assertTrue(all(d["prefix"] == "[Jinx] " for d in directives))
        self.assertEqual(state["history"][-1]["content"], expected[:300])

    def test_long_replies_still_chunk_to_four_chat_safe_pieces(self):
        text = "word " * 400
        chunks = jl.chunk_text(text)
        self.assertEqual(len(chunks), 4)
        self.assertTrue(all(len(c) <= 170 for c in chunks))
        self.assertEqual(jl.chunk_text("short answer"), ["short answer"])

    def test_outbox_offsets_partial_lines_and_corrupt_lines(self):
        outbox = self.tmp_path / "outbox.jsonl"
        msgs, offset = jl.read_new_outbox(str(outbox), 0)
        self.assertEqual((msgs, offset), ([], 0), "a missing outbox is not an error")

        line = json.dumps({"player": "Nader", "message": "hi"}) + "\n"
        outbox.write_text(line + "{corrupt\n" + '{"player": "N", "message": "half',
                          encoding="utf-8")
        msgs, offset = jl.read_new_outbox(str(outbox), 0)
        self.assertEqual([m["message"] for m in msgs], ["hi"], "the corrupt line is skipped")
        consumed = line + "{corrupt\n"
        self.assertEqual(offset, len(consumed.encode("utf-8")),
                         "the corrupt line is consumed (and dropped), not re-read forever")
        self.assertEqual(jl.read_new_outbox(str(outbox), offset)[0], [],
                         "the half-written line waits for its newline")

        with outbox.open("a", encoding="utf-8") as fh:
            fh.write('"}\n' + json.dumps({"message": "second"}) + "\n")
        msgs, offset2 = jl.read_new_outbox(str(outbox), offset)
        self.assertEqual([m.get("message") for m in msgs], ["half", "second"])
        self.assertGreater(offset2, offset)

        outbox.write_text("", encoding="utf-8")
        self.assertEqual(jl.read_new_outbox(str(outbox), offset2), ([], 0),
                         "a truncated outbox rewinds the offset")

    def test_state_round_trips_through_disk(self):
        path = self.tmp_path / ".jinx_link_state.json"
        self.assertEqual(jl.load_state(str(path)), {"offset": 0, "history": []})
        state = {"offset": 128, "history": [{"role": "user", "content": "hi"}]}
        jl.save_state(str(path), state)
        self.assertEqual(jl.load_state(str(path)), state)
        path.write_text("{not json", encoding="utf-8")
        self.assertEqual(jl.load_state(str(path)), {"offset": 0, "history": []})

    def test_hub_snapshot_keeps_the_persisted_shape(self):
        hub = self.make_hub()
        hub.state["offset"] = 42
        hub.state["history"] = [{"role": "user", "content": "hi"}]
        snapshot = hub.snapshot_state()
        self.assertEqual(snapshot, {"offset": 42, "history": [{"role": "user", "content": "hi"}]})
        snapshot["history"].append({"role": "assistant", "content": "mutated"})
        self.assertEqual(len(hub.state["history"]), 1, "the snapshot is a copy")

    def test_gather_quest_ctx_reads_progress_through_ai_service(self):
        self.write_team_file()
        ctx = jl.gather_quest_ctx("world", "chapters", "en_us.snbt")
        self.assertEqual(ctx["chapters_done"], 1)          # only Welcome is "done"
        self.assertEqual(ctx["chapters_total"], 3)
        self.assertEqual(ctx["quests_done"], 3)
        self.assertEqual(ctx["in_progress"][0]["title"], "Mekanism",
                         "the closest-to-finished partial chapter comes first")
        self.assertEqual(ctx["suggested_next"], [
            {"quest": "Digital Miner", "chapter": "Mekanism"},
            {"quest": "Quarry", "chapter": "Create"},
        ])
        self.assertIn("Quest chapters complete: 1 of 3.", jl.context_block(ctx, CHAT_BODY))


# ---------------------------------------------------------------------------
# CLI + run() wiring
# ---------------------------------------------------------------------------

class TestCliAndRunWiring(JinxLinkTestCase):
    def parse_cli(self, argv):
        captured = {}
        self._patch(jl, "run", lambda args: captured.update(vars(args)))
        self._patch(sys, "argv", ["jinx_link.py"] + argv)
        jl.main()
        return captured

    def test_old_flags_still_parse_and_the_new_ones_default_correctly(self):
        args = self.parse_cli(["--chapters", "C", "--instance", "I", "--world", "W",
                               "--lang", "en_us.snbt", "--llm-url", "http://localhost:8080/v1",
                               "--model", "local-model", "--interval", "2",
                               "--sync-interval", "15"])
        self.assertEqual((args["chapters"], args["instance"], args["world"]), ("C", "I", "W"))
        self.assertEqual(args["lang"], "en_us.snbt")
        self.assertEqual((args["interval"], args["sync_interval"]), (2, 15))
        self.assertTrue(args["voice"])
        self.assertFalse(args["selftest"])
        self.assertEqual(args["http_host"], "127.0.0.1")
        self.assertEqual(args["http_port"], 8712)
        self.assertFalse(args["no_http"])

    def test_http_flags_can_be_overridden_and_disabled(self):
        args = self.parse_cli(["--chapters", "C", "--instance", "I",
                               "--http-host", "127.0.0.5", "--http-port", "9001",
                               "--no-http", "--no-voice"])
        self.assertEqual(args["http_host"], "127.0.0.5")
        self.assertEqual(args["http_port"], 9001)
        self.assertTrue(args["no_http"])
        self.assertFalse(args["voice"])

    def test_required_flags_are_still_required(self):
        self._patch(jl, "run", lambda args: None)
        self._patch(sys, "argv", ["jinx_link.py"])
        with self.assertRaises(SystemExit) as raised:
            jl.main()          # argparse complains on stderr, which setUp captures
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--chapters", self.captured_err.getvalue())

    def test_selftest_prints_the_context_and_pings_without_serving(self):
        self.write_team_file()
        started = []
        self._patch(jl, "start_http_server",
                    lambda *a, **k: started.append(a) or None)
        ran = []
        self._patch(jl, "run", lambda args: ran.append(args))
        calls = self.patch_llm(reply="link ok")
        self._patch(sys, "argv", ["jinx_link.py", "--chapters", "C", "--instance", "I",
                                  "--world", "W", "--selftest"])
        jl.main()
        out = self.captured_out.getvalue()
        self.assertIn("quest context:", out)
        self.assertIn("LLM ping: 'link ok'", out)
        self.assertEqual(calls[0]["timeout"], 30)
        self.assertEqual(started, [], "--selftest must not open a port")
        self.assertEqual(ran, [], "--selftest must not enter the loop")

    def test_selftest_survives_an_unreachable_llm(self):
        self.write_team_file()
        self.patch_llm(error=OSError("refused"))
        self._patch(jl, "run", lambda args: self.fail("--selftest must not run the loop"))
        self._patch(sys, "argv", ["jinx_link.py", "--chapters", "C", "--instance", "I",
                                  "--world", "W", "--selftest"])
        jl.main()
        self.assertIn("LLM ping FAILED", self.captured_out.getvalue())

    def test_run_starts_the_http_server_and_keeps_the_file_flow(self):
        """One full loop iteration: sync -> cues, outbox -> inbox, HTTP serving."""
        self.write_team_file()
        outbox = Path(self.instance) / "kubejs" / "ai" / "outbox.jsonl"
        outbox.parent.mkdir(parents=True, exist_ok=True)
        outbox.write_text(json.dumps(dict(CHAT_BODY, message="loop question")) + "\n",
                          encoding="utf-8")
        FAKE_AI_SERVICE.sync_result = (None, [{"title": "Digital Miner"}], ["mekanism"])
        self.patch_llm(reply="answer from the loop")

        started: "list" = []
        real_start = jl.start_http_server

        def spy_start(hub, host, port):
            httpd = real_start(hub, host, port)
            started.append((hub, httpd))
            return httpd

        self._patch(jl, "start_http_server", spy_start)

        class OneShotClock:
            """Lets exactly one loop iteration run, then ends run().

            time() has to look like "long after startup" so the sync branch is
            due (the loop compares against last_sync = 0.0), and sleep() ends
            the iteration instead of blocking the suite.
            """
            def time(self):
                return 1000.0

            def sleep(self, _seconds):
                raise StopIteration("end of the iteration under test")

        self._patch(jl, "time", OneShotClock())
        args = self.make_args(lang="en_us.snbt", http_port=0)
        with self.assertRaises(StopIteration):
            jl.run(args)

        self.assertEqual(len(started), 1, "run() starts the HTTP server exactly once")
        hub, httpd = started[0]
        self.assertIsNotNone(httpd)
        self.addCleanup(jl.stop_http_server, httpd)
        servers = [t for t in threading.enumerate() if t.name == "jinx-link-http"]
        self.assertEqual(len(servers), 1, "the server runs on one background thread")
        self.assertTrue(servers[0].daemon, "it must never hold the process open")
        port = httpd.server_address[1]

        # the loop answered the outbox line into the file inbox, as always ...
        self.assertEqual(len(FAKE_AI_SERVICE.inbox_writes), 1)
        self.assertEqual(FAKE_AI_SERVICE.inbox_writes[0][1][0]["message"],
                         "answer from the loop")
        # ... the sync queued a cue for the mod to drain over HTTP ...
        status, body = http_call(port, "GET", "/cues")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"cues": [{
            "kind": "chat",
            "text": "Chapter complete: Mekanism. Suggested next: Digital Miner"}]})
        self.assertEqual(http_call(port, "GET", "/cues")[1], {"cues": []})
        self.assertEqual(http_call(port, "GET", "/health")[1], {"ok": True})
        # ... and the state file persisted the new offset and history.
        saved = json.loads((Path(args.out) / ".jinx_link_state.json").read_text("utf-8"))
        self.assertEqual(saved["offset"], outbox.stat().st_size)
        self.assertEqual(saved["history"][-1]["content"], "answer from the loop")
        self.assertEqual(len(FAKE_AI_SERVICE.sync_calls), 1)

    def test_run_honours_no_http(self):
        self.write_team_file()
        started = []
        self._patch(jl, "start_http_server",
                    lambda *a, **k: started.append(a) or None)
        FAKE_AI_SERVICE.sync_result = (None, [], [])

        class OneShotClock:
            def time(self):
                return 1000.0

            def sleep(self, _seconds):
                raise StopIteration

        self._patch(jl, "time", OneShotClock())
        with self.assertRaises(StopIteration):
            jl.run(self.make_args(no_http=True))
        self.assertEqual(started, [], "--no-http must not open a port")
        self.assertIn("disabled", self.captured_out.getvalue())

    def test_run_survives_a_failing_sync_and_a_failing_outbox(self):
        self.write_team_file()

        def broken_sync(*a):
            raise RuntimeError("save file locked")

        self._patch(FAKE_AI_SERVICE, "sync", broken_sync)

        def broken_outbox(*a):
            raise OSError("disk on fire")

        self._patch(jl, "read_new_outbox", broken_outbox)
        started = []
        self._patch(jl, "start_http_server",
                    lambda hub, host, port: started.append(hub) or None)

        class OneShotClock:
            def time(self):
                return 1000.0

            def sleep(self, _seconds):
                raise StopIteration

        self._patch(jl, "time", OneShotClock())
        with self.assertRaises(StopIteration):
            jl.run(self.make_args(lang=None))
        err = self.captured_err.getvalue()
        self.assertIn("sync error (retrying): save file locked", err)
        self.assertIn("outbox error (retrying): disk on fire", err)


# ---------------------------------------------------------------------------
# Hygiene: stdlib only, loopback only, no game writes
# ---------------------------------------------------------------------------

class TestModuleHygiene(JinxLinkTestCase):
    def parsed_source(self):
        return ast.parse(JINX_LINK_PY.read_text(encoding="utf-8"))

    def test_no_third_party_imports(self):
        source = JINX_LINK_PY.read_text(encoding="utf-8")
        stdlib = {"argparse", "ipaddress", "json", "os", "queue", "re", "socket",
                  "subprocess", "sys", "threading", "time", "urllib.error",
                  "urllib.request", "http.server"}
        imported = set()
        for node in ast.walk(self.parsed_source()):
            if getattr(node, "col_offset", 0) != 0:
                continue                    # function-local imports are checked below
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        self.assertIn("http.server", imported)
        self.assertIn("ai_service", imported)
        foreign = {m for m in imported if m not in stdlib and m != "ai_service"}
        self.assertEqual(foreign, set(),
                         "jinx_link.py must stay stdlib-only (ai_service ships beside it)")
        # pyttsx3 stays an optional, function-local Windows extra, as before.
        self.assertIn("import pyttsx3", source)
        self.assertNotIn("pyttsx3", imported)

    def test_it_still_never_writes_to_a_game_file(self):
        """READ-ONLY on saves: the only write-mode open() is this service's own state."""
        writes = []
        for node in ast.walk(self.parsed_source()):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id == "open"):
                mode = node.args[1].value if len(node.args) > 1 and isinstance(
                    node.args[1], ast.Constant) else "r"
                if any(c in str(mode) for c in "wxa+"):
                    writes.append((node.lineno, mode))
        self.assertEqual(len(writes), 1, writes)
        self.assertEqual(writes[0][1], "w")          # save_state's temp file under --out
        self.assertIn("READ-ONLY on game files", JINX_LINK_PY.read_text(encoding="utf-8"))
        self.assertIn("ai_service.write_inbox", JINX_LINK_PY.read_text(encoding="utf-8"),
                      "the inbox is still written through ai_service, and only there")

    def test_defaults_are_the_documented_localhost_and_port(self):
        self.assertEqual(jl.DEFAULT_HTTP_HOST, "127.0.0.1")
        self.assertEqual(jl.DEFAULT_HTTP_PORT, 8712)
        self.assertEqual(jl.HTTP_LLM_TIMEOUT, 20)
        self.assertTrue(issubclass(jl.JinxLinkHTTPServer, ThreadingHTTPServer))
        self.assertTrue(jl.JinxLinkHTTPServer.daemon_threads)
        self.assertTrue(jl.is_loopback_host(jl.DEFAULT_HTTP_HOST))


if __name__ == "__main__":
    unittest.main()
