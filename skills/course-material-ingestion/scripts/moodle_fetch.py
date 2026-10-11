#!/usr/bin/env python3
"""moodle_fetch.py - ingest Moodle course files with their real names, then keep notes in sync.

Commands
    resolve     follow redirects for one URL; report the real filename, type, size
    discover    list activity links on a course page (server-rendered HTML)
    download    fetch a plan of resources into one folder per course + manifest.json
    verify      check files on disk against a manifest (size, sha256, HTML sniff)
    sync-links  rewrite Obsidian [[wikilinks]] to point at names that exist on disk

Stdlib only, Python 3.8+. No network is touched except by resolve/discover/download.

Cookie sources, highest precedence first (an explicit flag always beats the ambient
environment):

    --cookie VALUE       raw Cookie header on the command line
    --cookie-file PATH   file with a Cookie header or Netscape cookies.txt;
                         `-` reads the cookie from stdin and keeps it off disk
    --cookie-env VAR     read the value out of $VAR
    (no flag given)      $MOODLE_SESSION_COOKIE, if it happens to be set

The session cookie is a credential. It goes on the wire and nowhere else: it is never
printed, never logged, never written into manifest.json, and error messages about a
malformed cookie file describe the line count rather than quoting the line.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import ssl
import sys
import unicodedata
from datetime import datetime, timezone
from email.message import Message
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urljoin, urlparse, urlsplit, urlunsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPSHandler

DEFAULT_UA = "moodle-fetch/1.0 (+hermes course-material-ingestion)"
MAX_REDIRECTS = 12
CHUNK = 262144
MAX_NAME = 150

# ---------------------------------------------------------------------------
# signatures / sniffing
# ---------------------------------------------------------------------------

SIGNATURES = {
    ".pdf": [b"%PDF"],
    ".docx": [b"PK\x03\x04"], ".pptx": [b"PK\x03\x04"], ".xlsx": [b"PK\x03\x04"],
    ".odt": [b"PK\x03\x04"], ".ods": [b"PK\x03\x04"], ".odp": [b"PK\x03\x04"],
    ".zip": [b"PK\x03\x04"], ".epub": [b"PK\x03\x04"],
    ".doc": [b"\xd0\xcf\x11\xe0"], ".ppt": [b"\xd0\xcf\x11\xe0"], ".xls": [b"\xd0\xcf\x11\xe0"],
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"], ".jpeg": [b"\xff\xd8\xff"],
    ".gif": [b"GIF87a", b"GIF89a"],
    ".mp3": [b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2", b"\xff\xfa"],
    ".opus": [b"OggS"], ".ogg": [b"OggS"], ".oga": [b"OggS"],
    ".wav": [b"RIFF"],
    ".webm": [b"\x1aE\xdf\xa3"], ".mkv": [b"\x1aE\xdf\xa3"],
    ".flac": [b"fLaC"],
    ".rtf": [b"{\\rtf"],
}

# containers whose marker sits at offset 4
OFFSET4 = {".m4a": b"ftyp", ".mp4": b"ftyp", ".mov": b"ftyp", ".3gp": b"ftyp"}

CT_EXT = {
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.ms-excel": ".xls",
    "application/zip": ".zip",
    "application/x-zip-compressed": ".zip",
    "text/plain": ".txt",
    "text/html": ".html",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "audio/mpeg": ".mp3",
    "audio/ogg": ".opus",
    "audio/mp4": ".m4a",
    "video/mp4": ".mp4",
    "video/webm": ".webm",
}

HTML_HEAD_RE = re.compile(rb"^\s*(<!doctype\s+html|<!--.*?-->\s*<html|<html|<head|<body)", re.I | re.S)


def sniff(head: bytes, ext: str) -> str:
    """Return one of: html, ok, mismatch, unknown."""
    if ext != ".html" and ext != ".htm" and HTML_HEAD_RE.match(head):
        return "html"
    if b"<title>" in head[:2048] and b"<html" in head[:4096].lower():
        return "html"
    if ext in OFFSET4:
        return "ok" if head[4:12].startswith(OFFSET4[ext]) else "mismatch"
    sigs = SIGNATURES.get(ext)
    if not sigs:
        return "unknown"
    return "ok" if any(head.startswith(s) for s in sigs) else "mismatch"


# ---------------------------------------------------------------------------
# filenames
# ---------------------------------------------------------------------------

WINDOWS_BAD = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
            *(f"LPT{i}" for i in range(1, 10))}


def sanitize(name: str) -> str:
    name = unicodedata.normalize("NFC", name or "")
    name = WINDOWS_BAD.sub("_", name).strip()
    name = re.sub(r"\s+", " ", name)
    stem, dot, ext = name.rpartition(".")
    if not dot:
        stem, ext = name, ""
    stem = stem.rstrip(". ")
    if stem.upper() in RESERVED:
        stem = "_" + stem
    name = (stem + dot + ext) if dot else stem
    if not name:
        name = "download"
    if len(name) > MAX_NAME:
        keep = MAX_NAME - len(ext) - 1
        name = name[:max(keep, 1)].rstrip(". ") + (("." + ext) if ext else "")
    return name


def filename_from_headers(headers, final_url: str, fallback: str = "") -> str:
    cd = headers.get("Content-Disposition") or ""
    cand = ""
    if cd:
        msg = Message()
        msg["content-disposition"] = cd
        cand = msg.get_filename() or ""
        if not cand:
            m = re.search(r"filename\*=\s*([^;]+)", cd, re.I)
            if m:
                raw = m.group(1).strip().strip('"')
                parts = raw.split("'", 2)
                payload = parts[2] if len(parts) == 3 else raw
                cand = unquote(payload)
    if not cand:
        seg = unquote(urlparse(final_url).path.rstrip("/").rsplit("/", 1)[-1])
        if seg and not re.match(r"^(view|index|pluginfile|file|download)\.php$", seg, re.I):
            cand = seg
    if not cand:
        cand = fallback or "download"
    # A title or a bare URL segment carries no extension; the response tells us the type.
    if not Path(cand).suffix:
        ct = (headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ct in CT_EXT:
            cand += CT_EXT[ct]
    return sanitize(cand)


# ---------------------------------------------------------------------------
# http
# ---------------------------------------------------------------------------

class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # observe the redirect instead of following it invisibly


def encode_unsafe(url: str) -> str:
    """Percent-encode characters a server left raw in a Location header.

    Moodle happily emits `Location: .../U01 (2).pdf`; a raw space or a non-ASCII
    character in the request line makes some servers answer 400 or drop the
    connection. Existing escapes are preserved, so `%20` is never double-encoded.
    """
    parts = urlsplit(url)
    path = quote(parts.path, safe="/%:@!$&'()*+,;=~-._")
    query = quote(parts.query, safe="=&%:@!$'()*+,;/?~-._")
    return urlunsplit((parts.scheme, parts.netloc, path, query, parts.fragment))


class Fetcher:
    def __init__(self, cookie=None, timeout=30, insecure=False, ua=DEFAULT_UA):
        self.cookie = (cookie or "").strip()
        ctx = ssl._create_unverified_context() if insecure else None
        handlers = [_NoRedirect()]
        if ctx is not None:
            handlers.append(HTTPSHandler(context=ctx))
        self.opener = build_opener(*handlers)
        self.timeout = timeout
        self.ua = ua

    def _request(self, url, method="GET"):
        req = Request(url, method=method)
        req.add_header("User-Agent", self.ua)
        req.add_header("Accept", "*/*")
        if self.cookie:
            req.add_header("Cookie", self.cookie)
        return req

    def open(self, url, method="GET"):
        """Return (final_url, headers, stream, chain). Raises URLError/HTTPError on 4xx/5xx."""
        chain = []
        current = url
        for _ in range(MAX_REDIRECTS):
            try:
                resp = self.opener.open(self._request(current, method), timeout=self.timeout)
            except HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    loc = e.headers.get("Location")
                    chain.append({"url": current, "status": e.code, "location": loc})
                    e.close()
                    if not loc:
                        raise URLError(f"{current}: {e.code} with no Location header")
                    current = encode_unsafe(urljoin(current, loc))
                    continue
                detail = ""
                try:
                    detail = e.read(200).decode("utf-8", "replace")
                except Exception:
                    pass
                raise HTTPError(e.url, e.code, f"{e.reason} {detail[:120]}", e.headers, None)
            if resp.status in (301, 302, 303, 307, 308):
                loc = resp.headers.get("Location")
                chain.append({"url": current, "status": resp.status, "location": loc})
                resp.close()
                if not loc:
                    raise URLError(f"{current}: {resp.status} with no Location header")
                current = encode_unsafe(urljoin(current, loc))
                continue
            chain.append({"url": current, "status": resp.status, "location": None})
            return current, resp.headers, resp, chain
        raise URLError(f"{url}: more than {MAX_REDIRECTS} redirects")

    def resolve(self, url):
        """Return dict describing what url actually serves (body is not consumed)."""
        final_url, headers, stream, chain = self.open(url)
        try:
            head = stream.read(4096)
        finally:
            stream.close()
        ct = (headers.get("Content-Type") or "").split(";")[0].strip().lower()
        name = filename_from_headers(headers, final_url)
        ext = Path(name).suffix.lower()
        return {
            "source_url": url,
            "final_url": final_url,
            "filename": name,
            "extension": ext,
            "content_type": ct,
            "declared_bytes": _int_or_none(headers.get("Content-Length")),
            "content_disposition": headers.get("Content-Disposition"),
            "sniff": sniff(head, ext),
            "head_hex": head[:8].hex(),
            "redirects": chain[:-1],
            "login_redirect": bool(re.search(r"/(login|auth)/", urlparse(final_url).path, re.I)),
        }


def _int_or_none(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# session cookie
# ---------------------------------------------------------------------------

#: Read automatically when no cookie flag is given. The value is the full
#: `MoodleSession=...` pair, i.e. exactly what a `Cookie:` header expects.
DEFAULT_COOKIE_ENV = ("MOODLE_SESSION_COOKIE",)

NETSCAPE_HEADER_RE = re.compile(r"^#\s*Netscape HTTP Cookie File", re.I | re.M)
HTTPONLY_PREFIX = "#HttpOnly_"


def _stdin_is_a_terminal() -> bool:
    try:
        return bool(sys.stdin is not None and sys.stdin.isatty())
    except (AttributeError, ValueError):
        return False


def _read_stdin() -> str:
    """Read stdin as text, tolerating a pipe that delivers non-UTF-8 bytes."""
    stream = getattr(sys.stdin, "buffer", sys.stdin)
    data = stream.read()
    if isinstance(data, bytes):
        data = data.decode("utf-8", "replace")
    return data


def parse_netscape(text: str):
    """Parse a Netscape cookies.txt into a list of `name=value` strings.

    `#HttpOnly_` rows count as data. Tools that write cookies.txt comment those rows
    out - the prefix is how curl marks an HttpOnly cookie - and `MoodleSession` is
    HttpOnly, so the one row everybody needs is exactly the row a naive reader skips.

    Errors name the line number and the field count; they never quote the row, because
    the row holds a credential.
    """
    pairs = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith(HTTPONLY_PREFIX):
            line = line[len(HTTPONLY_PREFIX):]
        elif line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 7:
            raise SystemExit(
                f"cookie file line {lineno}: expected 7 tab-separated fields "
                f"(Netscape cookies.txt), found {len(fields)}")
        if fields[5]:
            pairs.append(f"{fields[5]}={fields[6]}")
    if not pairs:
        raise SystemExit("cookie file: no cookies parsed "
                         "(expected a Cookie header or Netscape cookies.txt)")
    return pairs


def is_netscape(text: str) -> bool:
    """True when `text` is a cookies.txt rather than a raw `Cookie:` header.

    A raw Cookie header is one line of `a=b; c=d` and carries no tab, so a
    tab-separated 7-field row - or the canonical banner - settles it.
    """
    if NETSCAPE_HEADER_RE.search(text):
        return True
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(HTTPONLY_PREFIX):
            line = line[len(HTTPONLY_PREFIX):]
        elif line.startswith("#"):
            continue
        if len(line.split("\t")) >= 7:
            return True
    return False


def cookie_from_text(text: str, source: str = "cookie source") -> str:
    """Turn the contents of a cookie file (or of stdin) into a Cookie header value."""
    if not text.strip():
        raise SystemExit(f"{source}: empty - no session cookie found")
    if is_netscape(text):
        return "; ".join(parse_netscape(text))
    lines = [ln.strip().rstrip(";").strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("#")]
    if not lines:
        raise SystemExit(f"{source}: no cookies parsed "
                         "(expected a Cookie header or Netscape cookies.txt)")
    return "; ".join(lines)


def resolve_cookie(args):
    """Return `(cookie_header_value, source_label)`.

    The value is a credential and is never printed. The label is safe to print and
    tells the operator where the cookie came from - which matters most in the ambient
    case, where the cookie arrived without being asked for.

    Precedence, highest first - an explicit flag always beats the ambient environment:

        --cookie VALUE        raw Cookie header on the command line
        --cookie-file PATH    a file, or `-` to read stdin
        --cookie-env VAR      read $VAR
        no flag at all        $MOODLE_SESSION_COOKIE, if it is set
    """
    explicit = getattr(args, "cookie", None)
    if explicit and explicit.strip():
        return explicit.strip(), "--cookie"

    path = getattr(args, "cookie_file", None)
    if path:
        if path == "-":
            if _stdin_is_a_terminal():
                raise SystemExit("--cookie-file -: stdin is a terminal, so there is nothing "
                                 "to read; pipe the cookie in, or use --cookie-env")
            return (cookie_from_text(_read_stdin(), "--cookie-file - (stdin)"),
                    "--cookie-file - (stdin)")
        p = Path(path).expanduser()
        text = p.read_text(encoding="utf-8", errors="replace")
        return cookie_from_text(text, str(p)), f"--cookie-file {p}"

    var = getattr(args, "cookie_env", None)
    if var:
        value = os.environ.get(var)
        if not value or not value.strip():
            raise SystemExit(f"--cookie-env {var}: ${var} is unset or empty")
        return value.strip(), f"--cookie-env {var}"

    for name in DEFAULT_COOKIE_ENV:
        value = os.environ.get(name)
        if value and value.strip():
            return value.strip(), f"${name} (ambient)"
    return "", "none"


def read_cookie(args) -> str:
    """The session cookie for this run, or "" when none was supplied.

    Announces *where* the cookie came from - never its value. The ambient case is the
    one that needs saying out loud, because the operator never asked for it.
    """
    value, source = resolve_cookie(args)
    if source.endswith("(ambient)"):
        print(f"cookie   : picked up from {source} (value not printed)", file=sys.stderr)
    elif source == "none":
        print("cookie   : none supplied - requests will hit the login redirect",
              file=sys.stderr)
    return value


def human(n):
    if n is None:
        return "?"
    for unit in ("B", "K", "M", "G"):
        if n < 1024 or unit == "G":
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}B"
        n /= 1024.0


# ---------------------------------------------------------------------------
# discover
# ---------------------------------------------------------------------------

MOD_RE = re.compile(r'href="([^"]*?/mod/([a-z]+)/view\.php\?[^"]*?\bid=(\d+)[^"]*)"', re.I)
HIDE_RE = re.compile(r'<span[^>]*class="[^"]*accesshide[^"]*"[^>]*>.*?</span>', re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
# A module link or an activity title, whichever comes first, in document order.
TOKEN_RE = re.compile(
    r'href="([^"]*?/mod/([a-z]+)/view\.php\?[^"]*?\bid=(\d+)[^"]*)"'
    r'|<span[^>]*class="[^"]*instancename[^"]*"[^>]*>(.*?)</span>',
    re.I | re.S)


def _clean(html_fragment: str) -> str:
    text = HIDE_RE.sub(" ", html_fragment)
    text = TAG_RE.sub(" ", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'")
    return re.sub(r"\s+", " ", text).strip()


def _scan(html, base_url, modtypes, found, order):
    """Walk links and titles in document order; a title attaches to the link before it."""
    pending = None
    for m in TOKEN_RE.finditer(HIDE_RE.sub(" ", html)):
        if m.group(1) is not None:
            pending = _record(found, order, m.group(3), m.group(2), m.group(1),
                              base_url, modtypes)
        elif pending is not None:
            title = _clean(m.group(4) or "")
            if title and not pending["title"]:
                pending["title"] = title


def extract_activities(html: str, base_url: str, modtypes=None) -> list:
    """Pull {id, modtype, url, title} out of a rendered Moodle course page.

    Every activity is wrapped in an `id="module-<n>"` block, so when those blocks are
    present each is scanned on its own - a title can only attach to the link inside its
    own block. Collapsed and tile-format pages that render no blocks fall back to a
    document-order scan, where a title attaches to the nearest preceding link; those
    titles are a best guess, which is why the real name always comes from `resolve`.
    """
    modtypes = {m.lower() for m in (modtypes or [])} or None
    found, order = {}, []

    parts = re.split(r'id="module-(\d+)"', html)
    blocks = [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2) if MOD_RE.search(parts[i + 1])]
    if blocks:
        for _mid, chunk in blocks:
            _scan(chunk, base_url, modtypes, found, order)
    else:
        _scan(html, base_url, modtypes, found, order)

    return [found[mid] for mid in order]


def _record(found, order, mid, mtype, href, base_url, modtypes):
    mtype = mtype.lower()
    if modtypes and mtype not in modtypes:
        return None
    if mid not in found:
        order.append(mid)
    return found.setdefault(mid, {"id": int(mid), "modtype": mtype, "title": None,
                                  "url": urljoin(base_url, href.replace("&amp;", "&"))})


def cmd_discover(args):
    f = Fetcher(read_cookie(args), args.timeout, args.insecure)
    url = args.course_url
    if args.section is not None:
        url = f"{url}{'&' if '?' in url else '?'}section={args.section}"
    final_url, headers, stream, chain = f.open(url)
    html = stream.read().decode("utf-8", "replace")
    stream.close()
    modtypes = [m.strip() for m in args.modtypes.split(",") if m.strip()]
    activities = extract_activities(html, final_url, modtypes)
    missing_titles = sum(1 for a in activities if not a["title"])
    print(json.dumps({
        "course_url": args.course_url,
        "final_url": final_url,
        "section": args.section,
        "activity_count": len(activities),
        "activities": activities,
        "note": (f"{missing_titles} activity title(s) not rendered - this is normal for "
                 "collapsed/tile formats. Run `resolve <url>` for each of those; the real "
                 "filename comes from the redirect target, not from the page."
                 if missing_titles else
                 "titles came from the page; still confirm each one with `resolve`."),
    }, indent=2, ensure_ascii=False))
    return 0


# ---------------------------------------------------------------------------
# download
# ---------------------------------------------------------------------------

def load_plan(path):
    data = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    plans = data if isinstance(data, list) else [data]
    out = []
    for p in plans:
        course = p.get("course") or p.get("course_name") or "Unsorted"
        for r in p.get("resources", []):
            url = r["url"]
            rid = str(r.get("id") or _id_from_url(url) or hashlib.sha1(url.encode()).hexdigest()[:10])
            out.append({"course": course, "id": rid, "url": url,
                        "title": r.get("title") or ""})
    return out


def _id_from_url(url):
    m = re.search(r"[?&]id=(\d+)", url)
    return m.group(1) if m else None


def cmd_download(args):
    items = load_plan(args.plan)
    dest_root = Path(args.dest).expanduser()
    manifest_path = Path(args.manifest).expanduser() if args.manifest else dest_root / "manifest.json"
    manifest = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "dest_root": str(dest_root), "resources": []}
    if manifest_path.exists() and args.update:
        try:
            old = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["resources"] = [r for r in old.get("resources", [])]
        except Exception:
            pass
    by_id = {r["id"]: r for r in manifest["resources"]}
    f = Fetcher(read_cookie(args), args.timeout, args.insecure)

    failures = 0
    for item in items:
        prev = by_id.get(item["id"])
        try:
            info = f.resolve(item["url"])
            course_dir = dest_root / sanitize(item["course"])
            course_dir.mkdir(parents=True, exist_ok=True)
            name = info["filename"]
            target = course_dir / name

            if info["login_redirect"]:
                raise RuntimeError(f"redirected to a login page ({info['final_url']}) - session expired?")

            if args.update and prev and prev.get("status") in ("ok", "suspect") and target.exists():
                if target.stat().st_size == prev.get("bytes"):
                    print(f"skip  {item['course']}/{name} (unchanged)")
                    continue

            if info["declared_bytes"] and args.max_bytes and info["declared_bytes"] > args.max_bytes:
                print(f"SKIP  {item['course']}/{name}: {human(info['declared_bytes'])} exceeds --max-bytes")
                manifest["resources"].append(_entry(item, info, None, None, 0, "too_large"))
                failures += 1
                continue

            final_url, headers, stream, chain = f.open(item["url"])
            tmp = course_dir / (name + ".part")
            h, n = hashlib.sha256(), 0
            with open(tmp, "wb") as fh:
                while True:
                    chunk = stream.read(CHUNK)
                    if not chunk:
                        break
                    h.update(chunk)
                    n += len(chunk)
                    fh.write(chunk)
                stream.close()
            sha = h.hexdigest()
            with open(tmp, "rb") as fh:
                head = fh.read(4096)
            kind = sniff(head, Path(name).suffix.lower())
            declared = _int_or_none(headers.get("Content-Length")) or info["declared_bytes"]

            if kind == "html":
                bad = target.with_name(name + ".bad")
                tmp.replace(bad)
                status = "html_error"
                failures += 1
                print(f"FAIL  {item['course']}/{name}: server returned an HTML page, kept as {bad.name}")
            else:
                if target.exists() and target.stat().st_size != n:
                    k = 2
                    while True:
                        alt = target.with_name(f"{Path(name).stem} ({k}){Path(name).suffix}")
                        if not alt.exists():
                            target = alt
                            break
                        k += 1
                tmp.replace(target)
                status = "ok" if kind in ("ok", "unknown") else "suspect"
                if status == "suspect":
                    failures += 1
                    print(f"WARN  {item['course']}/{name}: bytes do not match the {Path(name).suffix} "
                          f"signature (saved as {status})")
                else:
                    print(f"ok    {item['course']}/{name}  {human(n)}")

            entry = _entry(item, info, target if status != "html_error" else None, sha, n, status)
            if declared and n and declared != n and status == "ok":
                entry["status"] = "truncated"
                failures += 1
                print(f"WARN  {item['course']}/{name}: got {n}B of {declared}B")
            manifest["resources"] = [r for r in manifest["resources"] if r["id"] != item["id"]]
            manifest["resources"].append(entry)
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                     encoding="utf-8")
        except (HTTPError, URLError, RuntimeError, OSError) as e:
            failures += 1
            print(f"FAIL  {item['course']}#{item['id']}: {e}", file=sys.stderr)
            manifest["resources"] = [r for r in manifest["resources"] if r["id"] != item["id"]]
            manifest["resources"].append({"id": item["id"], "course": item["course"],
                                          "title": item["title"], "source_url": item["url"],
                                          "status": "error", "error": str(e)[:300]})
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                     encoding="utf-8")

    ok = [r for r in manifest["resources"] if r.get("status") == "ok"]
    print(f"\n{len(ok)} ok / {len(manifest['resources'])} resources -> {manifest_path}")
    if failures:
        print(f"{failures} problem(s): run `verify` and read the manifest before reporting success.")
    return 1 if failures else 0


def _entry(item, info, path, sha, n, status):
    return {
        "id": item["id"], "course": item["course"], "title": item["title"],
        "source_url": item["url"], "final_url": info.get("final_url"),
        "filename": info.get("filename"), "path": str(path) if path else None,
        "content_type": info.get("content_type"), "bytes": n, "sha256": sha, "status": status,
    }


# ---------------------------------------------------------------------------
# verify
# ---------------------------------------------------------------------------

LINK_RE = re.compile(r"\[\[([^\[\]|#]+?)(#[^\[\]|]*)?(\|[^\[\]]*)?\]\]")


def iter_notes(root: Path):
    for p in sorted(root.rglob("*.md")):
        yield p


def strip_code(text: str) -> str:
    """Blank out fenced code blocks while preserving the line count, so reported line
    numbers still match the file on disk."""
    out, fence = [], None
    for line in text.splitlines(keepends=True):
        m = re.match(r"\s*(```+|~~~+)", line)
        if m:
            fence = None if fence else m.group(1)[0]
            out.append("\n")
            continue
        out.append("\n" if fence else line)
    return "".join(out)


def wikilink_targets(notes_root: Path):
    """Yield (path, lineno, target, raw) for every wikilink outside code fences."""
    for p in iter_notes(notes_root):
        text = strip_code(p.read_text(encoding="utf-8", errors="replace"))
        for i, line in enumerate(text.splitlines(), 1):
            for m in LINK_RE.finditer(line):
                yield p, i, m.group(1).strip(), m.group(0)


def cmd_verify(args):
    manifest = json.loads(Path(args.manifest).expanduser().read_text(encoding="utf-8"))
    root = Path(args.root).expanduser() if args.root else Path(manifest.get("dest_root", ".")).expanduser()
    problems, known = [], set()
    for r in manifest.get("resources", []):
        status = r.get("status")
        if status not in ("ok", "suspect", "truncated"):
            problems.append(f"[{status}] {r['course']}#{r['id']} {r.get('error') or r.get('filename') or ''}")
            continue
        p = Path(r["path"]) if r.get("path") else None
        if p is None or not p.exists():
            problems.append(f"[missing] {r['filename']}")
            continue
        known.add(p.name.lower())
        known.add(Path(p.name).stem.lower())
        size = p.stat().st_size
        if size != r.get("bytes"):
            problems.append(f"[size] {p.name}: {size} on disk vs {r.get('bytes')} in manifest")
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(CHUNK), b""):
                h.update(chunk)
        if r.get("sha256") and h.hexdigest() != r["sha256"]:
            problems.append(f"[sha256] {p.name}: content changed since download")
        with open(p, "rb") as fh:
            head = fh.read(4096)
        kind = sniff(head, p.suffix.lower())
        if kind == "html":
            problems.append(f"[html] {p.name}: HTML served under a document name")
        elif kind == "mismatch":
            problems.append(f"[magic] {p.name}: bytes do not match {p.suffix}")

    orphans = []
    manifest_paths = {os.path.abspath(str(r.get("path"))) for r in manifest.get("resources", [])
                      if r.get("path")}
    for p in root.rglob("*"):
        if p.is_file() and os.path.abspath(str(p)) not in manifest_paths \
                and p.name != "manifest.json" and not p.name.endswith(".part"):
            orphans.append(str(p.relative_to(root)))

    dangling = []
    if args.notes:
        notes_root = Path(args.notes).expanduser()
        for p, line, target, raw in wikilink_targets(notes_root):
            if target.lower() not in known:
                dangling.append(f"{p.name}:{line} {raw}")

    print(f"checked {len(manifest.get('resources', []))} manifest entries under {root}")
    for x in problems:
        print("  PROBLEM " + x)
    if orphans:
        print(f"  {len(orphans)} file(s) on disk are not in the manifest (first 10):")
        for x in orphans[:10]:
            print("    " + x)
    if args.notes:
        print(f"  {len(dangling)} dangling wikilink(s)"
              + ("" if not dangling else " (first 10):"))
        for x in dangling[:10]:
            print("    " + x)
    if not problems and not dangling and not orphans:
        print("all good")
    return 1 if (problems or dangling) else 0


# ---------------------------------------------------------------------------
# sync-links
# ---------------------------------------------------------------------------

def build_map_from_manifest(manifest):
    m = {}
    for r in manifest.get("resources", []):
        if not r.get("filename"):
            continue
        fn = Path(r["filename"])
        new = fn.stem
        for key in {r.get("title") or "", fn.name, fn.stem,
                    Path(r.get("final_url") or "").name, r.get("previous_filename") or ""}:
            k = Path(key).stem if key and Path(key).suffix else key
            if k and k != new:
                m[k] = new
    return m


def cmd_sync_links(args):
    notes_root = Path(args.notes).expanduser()
    rename = {}
    if args.map:
        rename.update(json.loads(Path(args.map).expanduser().read_text(encoding="utf-8")))
    if args.manifest:
        rename.update(build_map_from_manifest(
            json.loads(Path(args.manifest).expanduser().read_text(encoding="utf-8"))))
    lower = {k.lower(): v for k, v in rename.items()}

    changes, placeholders = [], []
    for p in iter_notes(notes_root):
        original = p.read_text(encoding="utf-8", errors="replace")
        lines = original.splitlines(keepends=True)
        out, touched = [], False
        for line in lines:
            def sub(m):
                nonlocal touched
                target, anchor, alias = (m.group(1).strip(), m.group(2) or "", m.group(3) or "")
                new = rename.get(target) or lower.get(target.lower())
                if not new:
                    if re.match(r"^(Resource[ _-]?\d+|view\.php|File|Script|Untitled)$", target, re.I) \
                            or target.lower().endswith(".php"):
                        placeholders.append(f"{p.name} {m.group(0)}")
                    return m.group(0)
                touched = True
                return f"[[{new}{anchor}{alias}]]"
            out.append(LINK_RE.sub(sub, line))
        if touched:
            new_text = "".join(out)
            if args.dry_run:
                for a, b in zip(original.splitlines(), new_text.splitlines()):
                    if a != b:
                        changes.append(f"{p.name}: {a.strip()}  ->  {b.strip()}")
            else:
                p.write_text(new_text, encoding="utf-8")
                changes.append(f"{p.name}: updated")

    mode = "would change" if args.dry_run else "changed"
    print(f"{len(changes)} file(s) {mode}; {len(placeholders)} placeholder link(s) still unresolved")
    for x in changes[:40]:
        print("  " + x)
    if placeholders:
        print("  unresolved placeholders (need a --map entry):")
        for x in placeholders[:10]:
            print("    " + x)
    return 1 if placeholders else 0


# ---------------------------------------------------------------------------
# cli
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Cookie sources, highest precedence first: --cookie, --cookie-file, "
               "--cookie-env, then $MOODLE_SESSION_COOKIE when no flag is given. The cookie "
               "goes on the wire and nowhere else: it is never printed, never logged, and "
               "never written into manifest.json.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("--cookie", metavar="VALUE",
                       help="raw Cookie header value, e.g. 'MoodleSession=...' "
                            "(credential - never echoed)")
        p.add_argument("--cookie-file", metavar="PATH",
                       help="file with a Cookie header or a Netscape cookies.txt; "
                            "'-' reads the cookie from stdin and keeps it off disk")
        p.add_argument("--cookie-env", metavar="VAR",
                       help="read the cookie from $VAR (the variable name is echoed, "
                            "its value never is)")
        p.add_argument("--timeout", type=int, default=30)
        p.add_argument("--insecure", action="store_true", help="skip TLS verification (campus certs)")

    p = sub.add_parser("resolve", help="follow redirects; report real filename/type/size")
    p.add_argument("url")
    p.add_argument("--json", action="store_true")
    add_common(p)

    p = sub.add_parser("discover", help="list activity links on a course page")
    p.add_argument("course_url")
    p.add_argument("--section", type=int, default=None)
    p.add_argument("--modtypes", default="resource,folder,page,url,book,file")
    add_common(p)

    p = sub.add_parser("download", help="download a plan into per-course folders + manifest")
    p.add_argument("plan")
    p.add_argument("--dest", required=True)
    p.add_argument("--manifest")
    p.add_argument("--update", action="store_true", help="skip ids whose file is unchanged")
    p.add_argument("--max-bytes", type=int, default=None, help="refuse files larger than this")
    add_common(p)

    p = sub.add_parser("verify", help="check files on disk against a manifest")
    p.add_argument("--manifest", required=True)
    p.add_argument("--root")
    p.add_argument("--notes", help="also check that every [[wikilink]] resolves to a file")
    add_common(p)

    p = sub.add_parser("sync-links", help="rewrite [[wikilinks]] to names on disk")
    p.add_argument("notes")
    p.add_argument("--map", help='JSON {"old name": "new name"}')
    p.add_argument("--manifest")
    p.add_argument("--dry-run", action="store_true")
    add_common(p)

    args = ap.parse_args(argv)
    # `read_cookie` announces the cookie's source (never its value) on every network
    # command, so the CLI and a direct call to `cmd_download` behave the same way.
    if args.cmd == "resolve":
        info = Fetcher(read_cookie(args), args.timeout, args.insecure).resolve(args.url)
        if args.json:
            print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            print(f"final url : {info['final_url']}")
            print(f"filename  : {info['filename']}")
            print(f"type      : {info['content_type'] or '?'}")
            print(f"size      : {human(info['declared_bytes'])}")
            print(f"sniff     : {info['sniff']}")
            if info["login_redirect"]:
                print("WARNING   : ended on a login page - the session is not valid")
        return 1 if info["sniff"] == "html" or info["login_redirect"] else 0
    if args.cmd == "discover":
        return cmd_discover(args)
    if args.cmd == "download":
        return cmd_download(args)
    if args.cmd == "verify":
        return cmd_verify(args)
    if args.cmd == "sync-links":
        return cmd_sync_links(args)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
