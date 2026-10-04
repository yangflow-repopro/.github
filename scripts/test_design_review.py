#!/usr/bin/env python3
"""Self-test for design-review.py: python3 scripts/test_design_review.py"""
import importlib.util
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("design_review", HERE / "design-review.py")
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)

README = """<!-- template: design-README.md v2 -->
# Design mockups

## Screens

| Screen | Spec | Design file | Code dir | Status | Signed off | Accepted |
|---|---|---|---|---|---|---|
| Alpha | `docs/spec.md#alpha` | `screens/alpha.html` | `App/UI/Alpha/` | accepted | 2026-01-01 | 2026-01-02 |
| Beta | `docs/spec.md#beta` | `screens/beta.html` | | proposed | | |
"""
SPEC = "# Spec\n\n## Alpha\n\nAlpha text.\n\n### Sub\n\nsub text\n\n## Beta\n\nBeta text.\n"


class Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        for rel, text in {"design/README.md": README, "docs/spec.md": SPEC, "design/screens/alpha.html": "<p>alpha</p>",
                          "design/screens/beta.direction-a.html": "<p>a</p>"}.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        (self.repo / "design/screenshots/alpha").mkdir(parents=True)
        (self.repo / "design/screenshots/alpha/light.png").write_bytes(b"\x89PNG")
        self.srv = dr.serve(self.repo, 0)
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.srv.server_address[1]}"

    def tearDown(self):
        self.srv.shutdown()
        self.srv.server_close()
        self.tmp.cleanup()

    def get(self, path):
        return urllib.request.urlopen(self.base + path).read().decode("utf-8", "replace")

    def test_ledger_and_spec(self):
        self.assertEqual([r["key"] for r in dr.read_ledger(self.repo)], ["alpha", "beta"])
        self.assertEqual(dr.spec_section(self.repo, "docs/spec.md#alpha"), "## Alpha\n\nAlpha text.\n\n### Sub\n\nsub text")
        self.assertEqual(dr.check(self.repo), 0)

    def test_pages(self):
        home = self.get("/")
        self.assertIn("待审核 (proposed)", home)
        self.assertIn("/screen/alpha", home)
        alpha = self.get("/screen/alpha")
        self.assertIn("Alpha text.", alpha)
        self.assertIn("/design/screenshots/alpha/light.png", alpha)
        beta = self.get("/screen/beta")
        self.assertIn("beta.direction-a.html", beta)
        self.assertIn("通过 / Approve", beta)
        self.assertIn("<p>alpha</p>", self.get("/design/screens/alpha.html"))

    def test_decision_recorded_and_ignored(self):
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k):
                return None
        opener = urllib.request.build_opener(NoRedirect)
        data = urllib.parse.urlencode({"screen": "beta", "decision": "change", "text": "larger title"}).encode()
        with self.assertRaises(urllib.error.HTTPError) as cm:
            opener.open(self.base + "/decision", data)
        self.assertEqual(cm.exception.code, 303)
        self.assertIn("larger title", self.get("/screen/beta"))
        self.assertEqual(dr.decisions(self.repo, "beta")[0]["decision"], "change")
        status = subprocess.run(["git", "-C", str(self.repo), "status", "--porcelain"], capture_output=True, text=True).stdout
        self.assertNotIn(".design-review", status)

    def test_rejects(self):
        for body in ({"screen": "nope", "decision": "approve"}, {"screen": "beta", "decision": "change", "text": ""}):
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(self.base + "/decision", urllib.parse.urlencode(body).encode())
            self.assertEqual(cm.exception.code, 400)
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(self.base + "/design/../README.md")
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(self.base + "/design/%2e%2e/docs/spec.md")


if __name__ == "__main__":
    unittest.main()
