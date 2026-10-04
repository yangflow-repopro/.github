#!/usr/bin/env python3
"""Self-test for check-docs.py (ledger rules): python3 scripts/test_check_docs.py"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = json.loads((HERE.parent / "handbook/templates/manifest.json").read_text())

HEADER = ("<!-- template: design-README.md v2 -->\n# Design mockups\n\n## Viewing\n\nx\n\n## Screens\n\n"
          "| Screen | Spec | Design file | Code dir | Status | Signed off | Accepted |\n|---|---|---|---|---|---|---|\n")
FOOTER = "\n## Decision log\n\nNone.\n\n## Maintenance\n\nx\n"
GOOD_ROWS = [
    "| Alpha | `docs/spec.md#alpha` | `screens/alpha.html` | `App/UI/Alpha/` | accepted | 2026-01-01 | 2026-01-02 |",
    "| Beta | `docs/spec.md#beta` | `screens/beta.html` | `App/UI/Beta/` | in-review | 2026-01-03 | |",
    "| Gamma | `docs/spec.md#gamma` | `screens/gamma.html` | | signed-off | 2026-01-04 | |",
    "| Delta | `docs/spec.md#delta` | `screens/delta.html` | | proposed | | |",
    "| Eps | `docs/spec.md#eps` | | | planned | | |",
]
FILES = {
    "docs/spec.md": "# Spec\n\n## Alpha\n\n## Beta\n\n## Gamma\n\n## Delta\n\n## Eps\n",
    "design/tokens.html": "<p>t</p>", "design/check-tokens.py": "pass\n",
    "design/screens/alpha.html": "a", "design/screens/beta.html": "b", "design/screens/gamma.html": "g",
    "design/screens/delta.direction-a.html": "d", "design/screens/delta.direction-b.html": "d",
    "design/screenshots/alpha/light.png": "png", "App/UI/Alpha/View.swift": "x", "App/UI/Beta/View.swift": "x",
}


def make(rows=None, files=None, remove=(), config=None, readme=None):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    cfg = {"pending": list(MANIFEST["types"]["app"]), **(config or {})}
    all_files = {**FILES, **(files or {})}
    all_files["design/README.md"] = readme if readme is not None else HEADER + "\n".join(rows or GOOD_ROWS) + "\n" + FOOTER
    all_files[".repo-type"] = "app"
    all_files[".docs-check.json"] = json.dumps(cfg)
    for p in MANIFEST["pointers"]:
        all_files[p] = "@AGENTS.md\n"
    for rel in remove:
        all_files.pop(rel, None)
    for rel, text in all_files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    return tmp, root


def run(root):
    r = subprocess.run([sys.executable, str(HERE / "check-docs.py"), str(root)], capture_output=True, text=True)
    return r.returncode, r.stdout


class Test(unittest.TestCase):
    def fails(self, expect, **kw):
        tmp, root = make(**kw)
        with tmp:
            code, out = run(root)
        self.assertEqual(code, 1, out)
        self.assertIn(expect, out)

    def test_good_ledger(self):
        tmp, root = make()
        with tmp:
            self.assertEqual(run(root), (0, "docs ok\n"))

    def test_v1_not_checked(self):
        tmp, root = make(readme=HEADER.replace("v2", "v1") + "| junk | x |\n" + FOOTER, remove=["design/screens/alpha.html"])
        with tmp:
            self.assertEqual(run(root)[0], 0)

    def test_file_without_row(self):
        self.fails("no row in the design/README.md ledger", files={"design/screens/zeta.html": "z"})

    def test_row_without_file(self):
        self.fails("design/screens/gamma.html does not exist", remove=["design/screens/gamma.html"])

    def test_direction_ignored_while_proposed_but_not_after(self):
        self.fails("must not have direction files", files={"design/screens/gamma.direction-a.html": "g"})

    def test_code_dir_missing(self):
        self.fails("code dir 'App/UI/Beta/' does not exist", remove=["App/UI/Beta/View.swift"])

    def test_bad_status(self):
        self.fails("must be one of", rows=[GOOD_ROWS[2].replace("signed-off", "done")])

    def test_accepted_needs_png(self):
        self.fails("needs device screenshots", remove=["design/screenshots/alpha/light.png"])

    def test_whitelist(self):
        self.fails("design/mockup.html: not on the design/ whitelist", files={"design/mockup.html": "m"})

    def test_icon_whitelist_configurable(self):
        tmp, root = make(files={"design/icon.html": "i"}, config={"design_icons": ["icon.html"]})
        with tmp:
            self.assertEqual(run(root)[0], 0)

    def test_spec_anchor(self):
        self.fails("spec anchor docs/spec.md#nowhere does not exist", rows=[GOOD_ROWS[2].replace("#gamma", "#nowhere")])

    def test_dates(self):
        self.fails("needs a Signed off date", rows=[GOOD_ROWS[2].replace("2026-01-04", "")])
        self.fails("needs an Accepted date", rows=[GOOD_ROWS[0].replace("2026-01-02", "")])

    def test_columns(self):
        self.fails("columns must be", readme=HEADER.replace("| Accepted |", "| Done |") + FOOTER)


if __name__ == "__main__":
    unittest.main()
