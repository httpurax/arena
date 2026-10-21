#!/usr/bin/env python3
"""
Jinx Link — chat with Jinx inside ATM10, with voice, reading live game data.

Flow:
    In Minecraft you type:   !jinx <question>      (also !ai / !j)
    ai_bridge.js appends it to  kubejs/ai/outbox.jsonl
    (player, message, position, dimension, timestamp).

    jinx_link.py reads new outbox lines, builds context from the save
    files (FTB Quests progress via ai_service helpers, plus the player
    snapshot the bridge captured), asks the local LLM, then:
      -> writes the reply to kubejs/ai/inbox.json  (the bridge prints
         it in game chat, chunked, prefixed "[Jinx] ")
      -> speaks the reply through the PC speakers (Windows TTS)

    It also runs ai_service.sync() on a slower cadence, so the
    chapter-complete toasts keep working from this ONE process, and
    speaks chapter completions when voice is on.
    => Run jinx_link.py OR ai_service.py --watch. Not both.

    python jinx_link.py --world "<path>" --chapters "<...>"
        --instance "<instance dir>" [--lang en_us.snbt]
        [--llm-url http://localhost:8080/v1] [--model local-model]
        [--voice | --no-voice] [--interval 2] [--sync-interval 15]
        [--http-host 127.0.0.1] [--http-port 8712] [--no-http]

HTTP API (the Jinx Talk mod posts here instead of going through the files):
    GET  /health -> {"ok": true}
    POST /chat   -> body {"player": ..., "message": ..., "pos": [x, y, z],
                          "dim": ..., "ts": <epoch millis>}
                    answer {"reply": "<text>"} sent straight back to the mod.
                    Same persona, same live quest context, same short history,
                    same cleaning and same fallback as the file flow — but the
                    reply is NEVER written to kubejs/ai/inbox.json, and the LLM
                    gets 20s (the mod stops reading after ~25s, so a fallback
                    reply always beats a timeout).
    POST /event  -> body {"type": "quest_completed", "quest": "<title>",
                          "player": ...}
                    answer {"announce": "Chapter complete: <quest>! Nice work."}
                    (spoken when voice is on). Any other type -> {}.
    GET  /cues   -> {"cues": [...]} DRAINS the cue queue: every cue is handed
                    out exactly once, so a second call returns [] until the
                    quest sync pushes more. The sync queues one
                    {"kind": "chat", "text": "Chapter complete: ... Suggested
                    next: ..."} cue per newly completed chapter; its file-inbox
                    toasts are unchanged.
    Malformed JSON -> 400 {"error": ...}, unknown path -> 404 JSON. A broken
    request is logged on stderr and never stops the main loop.

    Listens on 127.0.0.1:8712 by default, localhost only (a non-loopback
    --http-host is refused, not bound), on a daemon thread next to the
    file-based main loop. --no-http keeps the file flow alone.

Env: JINX_LINK_API_KEY — only if the LLM endpoint requires one.

If the LLM is unreachable the chat still answers with a quest-aware
fallback (progress + suggested next quest) instead of going silent.

READ-ONLY on game files. Always. Never writes to saves.
"""

import argparse
import ipaddress
import json
import os
import queue
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import ai_service  # same folder: SNBT helpers, chapters, titles, inbox writer


# --------------------------------------------------------------------------
# Persona
# --------------------------------------------------------------------------

PERSONA = (
    "You are Jinx, the AI companion on Nader's PC, now talking to him "
    "inside Minecraft (All the Mods 10, 1.21.1, NeoForge). Be casual, "
    "direct and brief — answers appear in game chat, so plain text only, "
    "no markdown, no lists, max ~3 short sentences unless he asks for "
    "detail. You know ATM10 well: Mekanism, Create, AE2, Ars Nouveau, "
    "the ATM Star endgame. A CONTEXT block is attached to each message "
    "with his REAL quest progress and position from the save files — "
    "trust it, use it, and never invent quest names, chapters or "
    "progress that are not in it."
)

# --------------------------------------------------------------------------
# Quest context (live, from the save files)
# --------------------------------------------------------------------------

def gather_quest_ctx(world_dir, chapters_dir, lang_file):
    """-> dict describing real progress, straight from the team .snbt."""
    team_path = ai_service.find_team_file(world_dir)
    with open(team_path, encoding="utf-8", errors="replace") as fh:
        completed = ai_service.extract_completed_ids(fh.read())
    chapters = ai_service.load_chapters(chapters_dir)
    titles = ai_service.load_titles(lang_file) if lang_file else {}
    status = ai_service.chapter_status(chapters, completed)
    nxt = ai_service.next_quests(chapters, status, completed, titles, limit=5)
    partials = [
        {"title": titles.get(cid, cid),
         "done": s["done"], "total": s["total"]}
        for cid, s in status.items() if s["state"] == "partial"
    ]
    partials.sort(key=lambda p: (-p["done"] / p["total"] if p["total"] else 0))
    return {
        "chapters_done": sum(1 for s in status.values() if s["state"] == "done"),
        "chapters_total": len(chapters),
        "quests_done": len(completed),
        "in_progress": partials[:4],
        "suggested_next": [
            {"quest": n["title"], "chapter": n["chapter_title"]} for n in nxt
        ],
    }


def context_block(ctx, msg):
    lines = ["CONTEXT (from the save files, trust this):"]
    lines.append("Quest chapters complete: %d of %d. Quests done: %d."
                 % (ctx["chapters_done"], ctx["chapters_total"], ctx["quests_done"]))
    for p in ctx["in_progress"]:
        lines.append("In progress: %s (%d/%d quests)." % (p["title"], p["done"], p["total"]))
    for n in ctx["suggested_next"][:3]:
        lines.append("Suggested next quest: %s (chapter: %s)." % (n["quest"], n["chapter"]))
    if msg.get("pos"):
        lines.append("Player %s is at %s in %s."
                     % (msg.get("player", "?"), msg["pos"], msg.get("dim", "?")))
    return "\n".join(lines)


# --------------------------------------------------------------------------
# LLM (OpenAI-compatible; default = his local llama-server on :8080)
# --------------------------------------------------------------------------

LLM_TIMEOUT = 90        # the file flow can afford to wait: nobody is blocking on it
HTTP_LLM_TIMEOUT = 20   # the mod stops reading after ~25s: a fallback beats a timeout


def ask_llm(base_url, model, api_key, messages, timeout=LLM_TIMEOUT):
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {"model": model, "messages": messages,
               "temperature": 0.7, "max_tokens": 260}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("Authorization", "Bearer " + api_key)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body["choices"][0]["message"]["content"].strip()


def clean_reply(text):
    # Unwrap code fences (keep the text) instead of deleting fenced blocks:
    # if the whole reply is fenced, deleting would leave silence.
    text = re.sub(r"^(Jinx|Assistant|AI)\s*:\s*", "", str(text).strip(), flags=re.IGNORECASE)
    text = text.replace("```", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:600]


def fallback_reply(ctx, question):
    """Quest-aware canned answer when the LLM is down. Never silence."""
    base = ("My brain (local LLM on :8080) isn't answering right now, "
            "but here's your save data: chapters %d/%d done."
            % (ctx["chapters_done"], ctx["chapters_total"]))
    if ctx["in_progress"]:
        p = ctx["in_progress"][0]
        base += " You're mid-way through %s (%d/%d)." % (p["title"], p["done"], p["total"])
    if ctx["suggested_next"]:
        base += " Suggested next: %s." % ctx["suggested_next"][0]["quest"]
    base += " Start llama-server for full chat."
    return base


# --------------------------------------------------------------------------
# Chat delivery (inbox chunks) + voice
# --------------------------------------------------------------------------

def chunk_text(text, limit=170):
    """Split into chat-safe chunks at word boundaries."""
    text = re.sub(r"\s+", " ", str(text)).strip()
    chunks = []
    while len(text) > limit:
        cut = text.rfind(" ", 0, limit)
        if cut <= 0:
            cut = limit
        chunks.append(text[:cut].strip())
        text = text[cut:].strip()
    if text:
        chunks.append(text)
    return chunks[:4]  # never flood the chat


def deliver(instance_dir, text, prefix="[Jinx] "):
    directives = [{"kind": "chat", "prefix": prefix, "message": c}
                  for c in chunk_text(text)]
    if directives:
        ai_service.write_inbox(instance_dir, directives)


_tts_engine = None
_tts_lock = threading.Lock()


def speak(text, enabled):
    """Speak via Windows TTS on the PC. No-op off Windows / when disabled."""
    if not enabled or sys.platform != "win32":
        return False
    text = re.sub(r"[^A-Za-z0-9 .,;:!?'\-]", " ", str(text))[:280].strip()
    if not text:
        return False

    def _say_pyttsx3():
        global _tts_engine
        import pyttsx3
        with _tts_lock:
            if _tts_engine is None:
                _tts_engine = pyttsx3.init()
                _tts_engine.setProperty("rate", 175)
            _tts_engine.say(text)
            _tts_engine.runAndWait()

    def _say_sapi():
        ps = ("Add-Type -AssemblyName System.Speech; "
              "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
              "$s.Rate = 1; $s.Speak('%s')" % text.replace("'", ""))
        subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                       timeout=60, check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _worker():
        try:
            _say_pyttsx3()
        except Exception:
            try:
                _say_sapi()
            except Exception:
                pass

    threading.Thread(target=_worker, daemon=True).start()
    return True


# --------------------------------------------------------------------------
# Outbox (game -> service), offset-tracked JSON lines
# --------------------------------------------------------------------------

def read_new_outbox(outbox_path, offset):
    """-> (messages, new_offset). Only complete lines are consumed."""
    if not os.path.exists(outbox_path):
        return [], 0
    size = os.path.getsize(outbox_path)
    if offset > size:  # file was recreated/truncated
        offset = 0
    if size == offset:
        return [], offset
    with open(outbox_path, "rb") as fh:
        fh.seek(offset)
        data = fh.read()
    if not data.endswith(b"\n"):
        last_nl = data.rfind(b"\n")
        if last_nl < 0:
            return [], offset  # partial line only; wait for the rest
        data = data[:last_nl + 1]
    new_offset = offset + len(data)
    msgs = []
    for raw in data.decode("utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            msgs.append(json.loads(raw))
        except ValueError:
            pass  # half-written/corrupt line: skip, never crash
    return msgs, new_offset


# --------------------------------------------------------------------------
# State (outbox offset + short chat history)
# --------------------------------------------------------------------------

def load_state(path):
    try:
        with open(path, encoding="utf-8") as fh:
            s = json.load(fh)
        return {"offset": int(s.get("offset", 0)),
                "history": s.get("history", [])[-12:]}
    except (OSError, ValueError):
        return {"offset": 0, "history": []}


def save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh)
    os.replace(tmp, path)


# --------------------------------------------------------------------------
# Shared state: the main loop and the HTTP handlers run in different threads
# --------------------------------------------------------------------------

MAX_CUES = 256  # the mod polls /cues; if it never does, drop the oldest, never grow


class LinkHub:
    """The quest context + chat history + cue queue, guarded by one lock.

    The file flow (main loop) and the HTTP handlers share all three, so every
    read and write goes through this object. The LLM call itself happens
    OUTSIDE the lock: it can take 20s, and holding the lock that long would
    stall the other path.
    """

    def __init__(self, args, ctx, state):
        self.args = args
        self.state = state            # {"offset": int, "history": [...]}
        self._lock = threading.Lock()
        self._ctx = ctx
        self._cues = queue.Queue(maxsize=MAX_CUES)

    # -- quest context --------------------------------------------------

    def get_ctx(self):
        with self._lock:
            return self._ctx

    def set_ctx(self, ctx):
        with self._lock:
            self._ctx = ctx

    # -- chat history ---------------------------------------------------

    def history(self):
        with self._lock:
            return list(self.state.get("history", []))

    def snapshot_state(self):
        """-> a copy of the persisted state, safe to serialize off-thread."""
        with self._lock:
            return {"offset": int(self.state.get("offset", 0)),
                    "history": list(self.state.get("history", []))}

    # -- replies --------------------------------------------------------

    def reply_to(self, msg, timeout=HTTP_LLM_TIMEOUT):
        """Answer one HTTP chat: speak it, remember it, return it.

        Deliberately does NOT touch kubejs/ai/inbox.json — the mod prints the
        HTTP response itself, so writing it too would double-post in chat.
        """
        with self._lock:
            ctx = self._ctx
            history = list(self.state.get("history", []))
        reply = compose_reply(msg, ctx, history, self.args, timeout=timeout)
        speak(reply, self.args.voice)
        with self._lock:
            remember(self.state, msg, reply)
        return reply

    # -- cues -----------------------------------------------------------

    def enqueue_cue(self, cue):
        """Queue one cue for the mod's next GET /cues. Never blocks, never grows."""
        while True:
            try:
                self._cues.put_nowait(cue)
                return
            except queue.Full:
                try:
                    self._cues.get_nowait()  # drop the oldest: nobody is reading them
                except queue.Empty:
                    pass

    def drain_cues(self):
        """-> every queued cue, emptying the queue (each cue is handed out once)."""
        cues = []
        while True:
            try:
                cues.append(self._cues.get_nowait())
            except queue.Empty:
                return cues


def compose_reply(msg, ctx, history, args, timeout=LLM_TIMEOUT):
    """-> the reply text for one message. Shared by the file and HTTP flows.

    Same persona, same live CONTEXT block, same short history, same cleaning,
    same quest-aware fallback when the LLM is down or answers with nothing.
    """
    messages = [{"role": "system", "content": PERSONA}]
    messages.extend(history)
    messages.append({"role": "user",
                     "content": context_block(ctx, msg) + "\n\nNader asks: " + msg["message"]})
    try:
        reply = clean_reply(ask_llm(args.llm_url, args.model,
                                    os.environ.get("JINX_LINK_API_KEY", ""),
                                    messages, timeout=timeout))
        if not reply:
            raise RuntimeError("empty LLM reply")
    except Exception as e:
        print("LLM error (%s) -> fallback reply" % e, file=sys.stderr)
        reply = fallback_reply(ctx, msg["message"])
    return reply


def remember(state, msg, reply):
    """Append the exchange to the short chat history (caller holds the lock)."""
    state["history"] = (state.get("history", []) + [
        {"role": "user", "content": str(msg.get("message", ""))[:300]},
        {"role": "assistant", "content": reply[:300]},
    ])[-12:]


# --------------------------------------------------------------------------
# HTTP API (mod -> service): the Jinx Talk mod's direct line
# --------------------------------------------------------------------------

DEFAULT_HTTP_HOST = "127.0.0.1"
DEFAULT_HTTP_PORT = 8712
MAX_BODY_BYTES = 1 << 20  # one chat message is a few hundred bytes; be generous anyway


class BadRequest(ValueError):
    """The request body cannot be used; answered as 400 with the reason."""


def is_loopback_host(host):
    """True only for addresses that are certainly this machine.

    Jinx Link reads the player's save files and speaks on his PC: it has no
    business being reachable from the LAN, so anything that is not verifiably
    loopback is refused instead of bound.
    """
    if host in ("localhost", "localhost.localdomain"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False  # some other hostname: we cannot prove it resolves to loopback


def make_handler(link_hub):
    """-> a request handler class bound to this hub (one hub per process).

    The parameter is not called ``hub``: inside the class body, ``hub = hub``
    would resolve the right-hand side against the class namespace being built
    and raise NameError instead of capturing the closure value.
    """

    class JinxLinkHandler(BaseHTTPRequestHandler):
        # HTTP/1.1 so the mod can keep one connection warm; every response
        # carries an exact Content-Length and then closes, so a half-handled
        # request can never leave a client waiting for bytes that will not come.
        protocol_version = "HTTP/1.1"
        server_version = "JinxLink/1"
        sys_version = ""
        hub = link_hub

        # -- plumbing ---------------------------------------------------

        def log_message(self, fmt, *fmt_args):
            # self.path / self.command may not exist yet when a request line
            # could not be parsed at all - logging must never raise.
            sys.stderr.write("http: %s %s %s\n"
                             % (self.address_string(),
                                getattr(self, "command", "-"), fmt % fmt_args))

        def _send_json(self, code, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True
            try:
                self.wfile.write(body)
            except OSError as e:
                print("http: client vanished before the answer (%s)" % e, file=sys.stderr)

        def _internal_error(self, exc):
            print("http: %s %s failed: %r"
                  % (getattr(self, "command", "-"), getattr(self, "path", "-"), exc),
                  file=sys.stderr)
            try:
                self._send_json(500, {"error": "internal error"})
            except Exception:
                pass  # nothing left to say to a dead socket

        def _read_json(self):
            """-> the JSON object body, or BadRequest with a reason to show."""
            raw_length = self.headers.get("Content-Length")
            try:
                length = int(raw_length or 0)
            except ValueError:
                raise BadRequest("Content-Length must be a number, got %r" % raw_length)
            if length <= 0:
                raise BadRequest("empty body: expected a JSON object")
            if length > MAX_BODY_BYTES:
                raise BadRequest("body too large (%d bytes, limit %d)"
                                 % (length, MAX_BODY_BYTES))
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8", errors="replace"))
            except ValueError as e:
                raise BadRequest("malformed JSON body: %s" % e)
            if not isinstance(payload, dict):
                raise BadRequest("body must be a JSON object, got %s"
                                 % type(payload).__name__)
            return payload

        # -- routes -----------------------------------------------------

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            try:
                if path == "/health":
                    self._send_json(200, {"ok": True})
                elif path == "/cues":
                    self._send_json(200, {"cues": self.hub.drain_cues()})
                else:
                    self._send_json(404, {"error": "unknown path: %s" % path})
            except Exception as e:
                self._internal_error(e)

        def do_POST(self):
            path = self.path.split("?", 1)[0]
            try:
                body = self._read_json()
                if path == "/chat":
                    self._send_json(200, {"reply": self._chat(body)})
                elif path == "/event":
                    self._send_json(200, self._event(body))
                else:
                    self._send_json(404, {"error": "unknown path: %s" % path})
            except BadRequest as e:
                print("http: bad request for %s: %s" % (path, e), file=sys.stderr)
                self._send_json(400, {"error": str(e)})
            except Exception as e:
                self._internal_error(e)

        # Any other method that carries no meaning here is answered like an
        # unknown path — a JSON 404, never a traceback. (HEAD is left to the
        # base class' 501: a JSON body on a HEAD reply would be a lie.)
        do_PUT = do_DELETE = do_PATCH = do_GET

        def _chat(self, body):
            message = body.get("message")
            if not isinstance(message, str) or not message.strip():
                raise BadRequest("missing or empty 'message'")
            msg = {"player": body.get("player") or "?",
                   "message": message,
                   "pos": body.get("pos"),
                   "dim": body.get("dim"),
                   "ts": body.get("ts")}
            reply = self.hub.reply_to(msg)  # spoken, remembered, never inboxed
            print("answered %s (http): %r -> %r"
                  % (msg["player"], message[:60], reply[:80]))
            return reply

        def _event(self, body):
            if body.get("type") != "quest_completed":
                return {}  # anything we do not act on is acknowledged, silently
            quest = body.get("quest")
            if not isinstance(quest, str) or not quest.strip():
                raise BadRequest("quest_completed needs a 'quest' title")
            announce = "Chapter complete: %s! Nice work." % quest
            speak(announce, self.hub.args.voice)
            print("event quest_completed (http): %r" % quest[:60])
            return {"announce": announce}

    return JinxLinkHandler


class JinxLinkHTTPServer(ThreadingHTTPServer):
    """Threading server that treats a broken request as noise, not as failure."""

    daemon_threads = True      # never hold the process open on a stuck client
    allow_reuse_address = True
    request_queue_size = 16

    def handle_error(self, request, client_address):
        # socketserver calls this for anything raised while handling a request.
        # Log it on stderr and carry on: the file-based main loop must survive
        # every malformed line, dead socket and aborted upload the mod sends.
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionError, socket.timeout, OSError)):
            print("http: dropped %s (%s)" % (client_address, exc), file=sys.stderr)
        else:
            print("http: handler error from %s: %r" % (client_address, exc),
                  file=sys.stderr)


def start_http_server(hub, host=DEFAULT_HTTP_HOST, port=DEFAULT_HTTP_PORT):
    """Serve the mod's HTTP API on a daemon thread -> the server, or None.

    Returns None (and says why on stderr) instead of raising, so a busy port or
    a non-loopback --http-host degrades to the file flow rather than killing the
    service the in-game chat depends on.
    """
    if not is_loopback_host(host):
        print("http: refusing to bind %r — Jinx Link listens on localhost only "
              "(file flow continues)" % host, file=sys.stderr)
        return None
    try:
        httpd = JinxLinkHTTPServer((host, port), make_handler(hub))
    except OSError as e:
        print("http: cannot listen on %s:%s (%s) — file flow continues"
              % (host, port, e), file=sys.stderr)
        return None
    # poll_interval well under the 0.5s default: it only bounds how long
    # shutdown() waits, and an idle select() wakeup costs nothing.
    threading.Thread(target=httpd.serve_forever, kwargs={"poll_interval": 0.05},
                     name="jinx-link-http", daemon=True).start()
    print("http: listening on http://%s:%d — GET /health, POST /chat, POST /event, "
          "GET /cues" % (host, httpd.server_address[1]))
    return httpd


def stop_http_server(httpd):
    """Shut a server from start_http_server down (tests, and a clean exit)."""
    if httpd is None:
        return
    httpd.shutdown()
    httpd.server_close()


# --------------------------------------------------------------------------
# Main service
# --------------------------------------------------------------------------

def answer_one(msg, ctx, state, args):
    """The file flow: answer one outbox line into the inbox, and speak it."""
    reply = compose_reply(msg, ctx, state["history"], args)
    deliver(args.instance, reply)
    speak(reply, args.voice)
    remember(state, msg, reply)
    print("answered %s: %r -> %r" % (msg.get("player"), msg["message"][:60], reply[:80]))


def announce_new_chapters(new_done, nxt, titles, args, hub):
    """Speak every chapter the sync just completed, and queue a cue per chapter.

    The file-inbox toasts are ai_service.sync()'s job and stay as they were;
    this adds the /cues payload the mod polls for, plus the spoken line.
    """
    for cid in new_done:
        name = titles.get(cid, cid)
        nxt_title = nxt[0]["title"] if nxt else "check the quest book"
        text = "Chapter complete: %s. Suggested next: %s" % (name, nxt_title)
        hub.enqueue_cue({"kind": "chat", "text": text})
        speak(text, args.voice)


def run(args):
    world = ai_service.find_world(args.saves, args.world)
    out_dir = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(out_dir, exist_ok=True)
    state_path = os.path.join(out_dir, ".jinx_link_state.json")
    sync_state_path = os.path.join(out_dir, ".jinx_link_sync_state.json")
    state = load_state(state_path)
    outbox_path = os.path.join(args.instance, "kubejs", "ai", "outbox.jsonl")

    titles = ai_service.load_titles(args.lang) if args.lang else {}
    print("Jinx Link up. world=%s" % world)
    print("chat: type  !jinx <question>  in game. LLM=%s model=%s voice=%s"
          % (args.llm_url, args.model, args.voice))

    hub = LinkHub(args, gather_quest_ctx(world, args.chapters, args.lang), state)
    httpd = None
    if args.no_http:
        print("http: disabled (--no-http), file flow only")
    else:
        httpd = start_http_server(hub, args.http_host, args.http_port)

    last_sync = 0.0
    while True:
        now = time.time()
        if now - last_sync >= args.sync_interval:
            last_sync = now
            try:
                _, nxt, new_done = ai_service.sync(
                    world, args.chapters, args.lang, out_dir,
                    args.instance, sync_state_path)
                hub.set_ctx(gather_quest_ctx(world, args.chapters, args.lang))
                announce_new_chapters(new_done, nxt, titles, args, hub)
            except Exception as e:
                print("sync error (retrying): %s" % e, file=sys.stderr)
        try:
            msgs, state["offset"] = read_new_outbox(outbox_path, state["offset"])
            for msg in msgs:
                if msg.get("message"):
                    answer_one(msg, hub.get_ctx(), state, args)
            if msgs:
                save_state(state_path, hub.snapshot_state())
        except Exception as e:
            print("outbox error (retrying): %s" % e, file=sys.stderr)
        time.sleep(args.interval)


def main():
    ap = argparse.ArgumentParser(description="Jinx Link — in-game chat + voice for ATM10")
    ap.add_argument("--world", help="path to the world folder")
    ap.add_argument("--saves", help="path to the instance saves/ dir (auto-detect world)")
    ap.add_argument("--chapters", required=True,
                    help="config/ftbquests/quests/chapters dir")
    ap.add_argument("--lang", default=None, help="en_us.snbt for titles")
    ap.add_argument("--instance", required=True,
                    help="instance dir (holds kubejs/ai/inbox.json + outbox.jsonl)")
    ap.add_argument("--out", default=None, help="output dir (default: ./out)")
    ap.add_argument("--llm-url", default="http://localhost:8080/v1",
                    help="OpenAI-compatible base URL (default: local llama-server)")
    ap.add_argument("--model", default="local-model")
    ap.add_argument("--interval", type=int, default=2, help="outbox poll seconds")
    ap.add_argument("--sync-interval", type=int, default=15, help="quest sync seconds")
    ap.add_argument("--voice", dest="voice", action="store_true", default=True,
                    help="speak replies through the PC speakers (default)")
    ap.add_argument("--no-voice", dest="voice", action="store_false",
                    help="chat only, no speech")
    ap.add_argument("--http-host", default=DEFAULT_HTTP_HOST,
                    help="loopback address for the mod's HTTP API (default: %(default)s; "
                         "anything non-loopback is refused)")
    ap.add_argument("--http-port", type=int, default=DEFAULT_HTTP_PORT,
                    help="port for the mod's HTTP API (default: %(default)s)")
    ap.add_argument("--no-http", action="store_true",
                    help="serve only the file outbox/inbox flow, no HTTP API")
    ap.add_argument("--selftest", action="store_true",
                    help="print quest context + ping the LLM, then exit")
    args = ap.parse_args()

    if args.selftest:
        world = ai_service.find_world(args.saves, args.world)
        ctx = gather_quest_ctx(world, args.chapters, args.lang)
        print("quest context: %s" % json.dumps(ctx, indent=2))
        try:
            ping = ask_llm(args.llm_url, args.model,
                           os.environ.get("JINX_LINK_API_KEY", ""),
                           [{"role": "user", "content": "Reply with exactly: link ok"}],
                           timeout=30)
            print("LLM ping: %r" % ping)
        except Exception as e:
            print("LLM ping FAILED: %s (fallback replies will be used)" % e)
        return

    run(args)


if __name__ == "__main__":
    main()
