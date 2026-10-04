#!/usr/bin/env python3
"""Local design review server (handbook/ui-workflow.md). Standard library only.

    python3 design-review.py <product-repo> [--port 8800]
    python3 design-review.py <product-repo> --check      render every page once, print a summary, exit

Reads the ledger (the Screens table of <repo>/design/README.md, template design-README.md v2) and serves:
  /               screens grouped by status
  /screen/<name>  spec section, the design file, device screenshots, recorded decisions, the two buttons
Decisions ("Approve" / "Request change" + text) are appended to <repo>/.design-review/decisions.jsonl, which
is kept out of Git through .git/info/exclude. The server never edits tracked files; the agent applies the
recorded decisions to the ledger afterwards. The server listens on 127.0.0.1 only.
"""
import argparse
import html
import json
import mimetypes
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

# Interface text (the maintainer reads Chinese); English status words stay in brackets.
LABELS = {
    "title": "设计审核",
    "home": "返回首页",
    "empty": "(无)",
    "proposed": "待审核 (proposed)",
    "in-review": "已开发,待真机验收 (in-review)",
    "signed-off": "已通过,待开发 (signed-off)",
    "accepted": "已验收 (accepted)",
    "planned": "待设计 (planned)",
    "spec": "Spec 段落",
    "spec_missing": "找不到 spec 段落",
    "design": "设计稿",
    "directions": "方向稿",
    "screenshots": "真机截图",
    "decisions": "已记录的决定",
    "approve": "通过 / Approve",
    "change": "改成… / Request change",
    "change_hint": "写下要改成什么",
    "note": "记录只写入本机 .design-review/decisions.jsonl;Agent 之后据此更新台账。",
    "recorded": "已记录",
    "approved": "通过",
    "changed": "要求修改",
    "need_text": "「改成…」需要填写内容",
    "open": "单独打开",
}
GROUPS = ["proposed", "in-review", "signed-off", "accepted", "planned"]
STATUSES = set(GROUPS)
DIRECTION = re.compile(r"^(?P<stem>.+)\.direction-[^.]+\.html$")


def slug(heading):
    s = re.sub(r"`", "", heading.lower())
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    return s.strip().replace(" ", "-")


def cell(text):
    return text.strip().strip("`").strip()


def read_ledger(repo):
    """Rows of the Screens table: dicts keyed by column name (lowercase), plus 'key' (design file stem or Screen)."""
    readme = repo / "design/README.md"
    if not readme.is_file():
        raise SystemExit(f"{readme}: missing")
    lines, in_section, rows, header = readme.read_text(encoding="utf-8").split("\n"), False, [], None
    for line in lines:
        if line.startswith("## "):
            in_section = line[3:].strip() == "Screens"
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
        elif not all(re.fullmatch(r":?-+:?", c) for c in cells):
            row = dict(zip(header, cells))
            df = cell(row.get("design file", ""))
            m = re.fullmatch(r"(?:screens/)?(.+?)\.html", df)
            row["key"] = m.group(1) if m else cell(row.get("screen", ""))
            row["status"] = cell(row.get("status", ""))
            rows.append(row)
    return rows


def spec_section(repo, spec_cell):
    """Text of the heading section of docs/spec.md named by `docs/spec.md#anchor`, or None."""
    m = re.search(r"#([\w-]+)", spec_cell)
    spec = repo / "docs/spec.md"
    if not m or not spec.is_file():
        return None
    anchor, lines, start, level, fenced = m.group(1), spec.read_text(encoding="utf-8").split("\n"), None, 0, False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fenced = not fenced
            continue
        h = None if fenced else re.match(r"^(#{1,6}) (\S.*)", line)
        if start is None:
            if (h and slug(h.group(2)) == anchor) or f'<a id="{anchor}"' in line:
                start, level = i, (len(h.group(1)) if h else 6)
        elif h and len(h.group(1)) <= level:
            return "\n".join(lines[start:i]).strip()
    return "\n".join(lines[start:]).strip() if start is not None else None


def decisions(repo, screen=None):
    f = repo / ".design-review/decisions.jsonl"
    out = []
    if f.is_file():
        for line in f.read_text(encoding="utf-8").split("\n"):
            if line.strip():
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                if screen is None or d.get("screen") == screen:
                    out.append(d)
    return out


def record(repo, screen, decision, text):
    d = repo / ".design-review"
    d.mkdir(exist_ok=True)
    entry = {"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "screen": screen, "decision": decision, "text": text}
    with open(d / "decisions.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def ensure_ignored(repo):
    """Keep .design-review/ out of Git without touching tracked files: .git/info/exclude."""
    r = subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-path", "info/exclude"], capture_output=True, text=True)
    if r.returncode != 0:
        return
    p = Path(r.stdout.strip())
    p = p if p.is_absolute() else repo / p
    gi = repo / ".gitignore"
    if gi.is_file() and ".design-review" in gi.read_text():
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.is_file() or ".design-review/" not in p.read_text():
        with open(p, "a", encoding="utf-8") as f:
            f.write("\n.design-review/\n")


CSS = """body{font:15px/1.5 -apple-system,system-ui,sans-serif;margin:0;padding:24px;max-width:1400px}
h1{margin-top:0}h2{margin-top:28px;border-bottom:1px solid #8884;padding-bottom:4px}
.row{padding:6px 0}.tag{font-size:12px;padding:1px 8px;border-radius:9px;background:#8883}
iframe{width:100%;height:760px;border:1px solid #8886;border-radius:6px}
pre.spec{white-space:pre-wrap;background:#8881;padding:12px;border-radius:6px}
.shots img{max-width:420px;margin:0 8px 8px 0;border:1px solid #8886;border-radius:6px}
button{font-size:15px;padding:6px 16px;margin-right:8px}textarea{width:100%;height:70px;font:inherit}
.dec{padding:4px 0;border-bottom:1px solid #8883}"""


def page(title, body):
    return (f"<!doctype html><meta charset=utf-8><title>{html.escape(title)}</title>"
            f"<style>{CSS}</style><body>{body}</body>")


def screen_files(repo, key):
    screens = repo / "design/screens"
    directions = sorted(p.name for p in screens.glob(f"{key}.direction-*.html")) if screens.is_dir() else []
    main = (screens / f"{key}.html").is_file()
    shots_dir = repo / "design/screenshots" / key
    shots = sorted(p.name for p in shots_dir.glob("*.png")) if shots_dir.is_dir() else []
    return main, directions, shots


def home_page(repo):
    rows = read_ledger(repo)
    body = [f"<h1>{LABELS['title']}</h1>"]
    for status in GROUPS:
        group = [r for r in rows if r["status"] == status]
        body.append(f"<h2>{html.escape(LABELS[status])} · {len(group)}</h2>")
        if not group:
            body.append(f"<div class=row>{LABELS['empty']}</div>")
        for r in group:
            body.append(f"<div class=row><a href='/screen/{quote(r['key'])}'>{html.escape(r['key'])}</a></div>")
    other = [r for r in rows if r["status"] not in STATUSES]
    for r in other:
        body.append(f"<div class=row>? {html.escape(r['key'])}: {html.escape(r['status'])}</div>")
    return page(LABELS["title"], "".join(body))


def screen_page(repo, key):
    row = next((r for r in read_ledger(repo) if r["key"] == key), None)
    if row is None:
        return None
    main, directions, shots = screen_files(repo, key)
    status = row["status"]
    label = LABELS.get(status, status)
    k = html.escape(key)
    body = [f"<p><a href='/'>{LABELS['home']}</a></p><h1>{k} <span class=tag>{html.escape(label)}</span></h1>"]
    body.append(f"<h2>{LABELS['spec']}</h2>")
    section = spec_section(repo, row.get("spec", ""))
    body.append(f"<pre class=spec>{html.escape(section)}</pre>" if section else f"<p>{LABELS['spec_missing']}: {html.escape(row.get('spec', ''))}</p>")
    if main:
        body.append(f"<h2>{LABELS['design']}</h2><p><a href='/design/screens/{quote(key)}.html' target=_blank>{LABELS['open']}</a></p>"
                    f"<iframe src='/design/screens/{quote(key)}.html'></iframe>")
    if directions and status == "proposed":
        body.append(f"<h2>{LABELS['directions']}</h2>")
        for d in directions:
            body.append(f"<p><a href='/design/screens/{quote(d)}' target=_blank>{html.escape(d)}</a></p>"
                        f"<iframe src='/design/screens/{quote(d)}'></iframe>")
    if shots:
        body.append(f"<h2>{LABELS['screenshots']}</h2><div class=shots>")
        body += [f"<a href='/design/screenshots/{quote(key)}/{quote(s)}' target=_blank><img src='/design/screenshots/{quote(key)}/{quote(s)}' title='{html.escape(s)}'></a>" for s in shots]
        body.append("</div>")
    body.append(f"<h2>{LABELS['decisions']}</h2>")
    ds = decisions(repo, key)
    for d in ds:
        word = LABELS["approved"] if d.get("decision") == "approve" else LABELS["changed"]
        body.append(f"<div class=dec>{html.escape(d.get('time', ''))} · <b>{word}</b> {html.escape(d.get('text', ''))}</div>")
    if not ds:
        body.append(f"<div class=row>{LABELS['empty']}</div>")
    body.append(f"<h2>?</h2><form method=post action='/decision'><input type=hidden name=screen value='{k}'>"
                f"<p><button name=decision value=approve>{LABELS['approve']}</button></p>"
                f"<p><textarea name=text placeholder='{LABELS['change_hint']}'></textarea></p>"
                f"<p><button name=decision value=change>{LABELS['change']}</button></p></form>"
                f"<p><small>{LABELS['note']}</small></p>")
    return page(key, "".join(body))


def make_handler(repo):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, ctype="text/html; charset=utf-8", extra=None):
            data = body if isinstance(body, bytes) else body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path = unquote(urlparse(self.path).path)
            try:
                if path == "/":
                    return self.send(200, home_page(repo))
                if path.startswith("/screen/"):
                    p = screen_page(repo, path[len("/screen/"):])
                    return self.send(200, p) if p else self.send(404, "not found")
                if path.startswith("/design/"):
                    base = (repo / "design").resolve()
                    f = (base / path[len("/design/"):]).resolve()
                    if base in f.parents and f.is_file():
                        return self.send(200, f.read_bytes(), mimetypes.guess_type(f.name)[0] or "application/octet-stream")
                return self.send(404, "not found")
            except SystemExit as e:
                return self.send(500, str(e))

        def do_POST(self):
            if urlparse(self.path).path != "/decision":
                return self.send(404, "not found")
            size = int(self.headers.get("Content-Length") or 0)
            form = {k: v[0] for k, v in parse_qs(self.rfile.read(size).decode("utf-8")).items()}
            screen, decision, text = form.get("screen", ""), form.get("decision", ""), form.get("text", "").strip()
            if screen not in {r["key"] for r in read_ledger(repo)} or decision not in ("approve", "change"):
                return self.send(400, "bad request")
            if decision == "change" and not text:
                return self.send(400, LABELS["need_text"])
            record(repo, screen, decision, text)
            self.send(303, "", extra={"Location": f"/screen/{quote(screen)}"})
    return Handler


def serve(repo, port):
    ensure_ignored(repo)
    return ThreadingHTTPServer(("127.0.0.1", port), make_handler(repo))


def check(repo):
    rows = read_ledger(repo)
    if not rows:
        print("no ledger rows found in design/README.md (Screens table)")
        return 1
    bad = [r for r in rows if r["status"] not in STATUSES]
    home_page(repo)
    for r in rows:
        screen_page(repo, r["key"])
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in GROUPS}
    print(f"{len(rows)} screens: " + ", ".join(f"{s} {n}" for s, n in counts.items()))
    for r in bad:
        print(f"{r['key']}: unknown status {r['status']!r}")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description="Local design review server")
    ap.add_argument("repo")
    ap.add_argument("--port", type=int, default=8800)
    ap.add_argument("--check", action="store_true", help="render all pages once and exit")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    if a.check:
        sys.exit(check(repo))
    srv = serve(repo, a.port)
    print(f"design review: http://127.0.0.1:{srv.server_address[1]}/  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
