#!/usr/bin/env python3
"""Self-test for check-docs.py (ledger rules, selfhosted type): python3 scripts/test_check_docs.py"""
import json
import re
import os
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


def make(rows=None, files=None, remove=(), config=None, readme=None, repo_type="app"):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    cfg = {"pending": list(MANIFEST["types"][repo_type]["documents"]), **(config or {})}
    all_files = {**FILES, **(files or {})}
    all_files["design/README.md"] = readme if readme is not None else HEADER + "\n".join(rows or GOOD_ROWS) + "\n" + FOOTER
    all_files[".repo-type"] = repo_type
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


def run(root, env=None):
    r = subprocess.run([sys.executable, str(HERE / "check-docs.py"), str(root)], capture_output=True, text=True,
                       env={**os.environ, **(env or {})})
    return r.returncode, r.stdout


def template(name):
    return (HERE.parent / "handbook/templates" / name).read_text()


def git(root, *args):
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", *args], check=True,
                   capture_output=True)


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



class SelfhostedTest(unittest.TestCase):
    def check(self, **kw):
        tmp, root = make(repo_type="selfhosted", **kw)
        with tmp:
            return run(root)

    def without_pending(self, *rels):
        return {"pending": [r for r in MANIFEST["types"]["selfhosted"]["documents"] if r not in rels]}

    def test_good(self):
        self.assertEqual(self.check(), (0, "docs ok\n"))

    def test_templates(self):
        rels = ("LICENSE", "THIRD_PARTY.md", "docs/hosting.md", "docs/threat-model.md", "docs/design.md")
        files = {rel: template(MANIFEST["types"]["selfhosted"]["documents"][rel]) for rel in rels}
        self.assertEqual(self.check(files=files, config=self.without_pending(*rels)), (0, "docs ok\n"))

    def test_app_license_is_rejected(self):
        code, out = self.check(files={"LICENSE": template("app/LICENSE")}, config=self.without_pending("LICENSE"))
        self.assertEqual(code, 1)
        self.assertIn("(template: selfhosted/LICENSE v1)", out)

    def test_milestone_template(self):
        code, out = self.check(files={"docs/milestones/next.md": template("common/milestone.md")})
        self.assertEqual(code, 1)
        self.assertIn("selfhosted/milestone.md", out)
        ok = self.check(files={"docs/milestones/next.md": template("selfhosted/milestone.md")})
        self.assertEqual(ok, (0, "docs ok\n"))

    def test_package_versions(self):
        third = template("selfhosted/THIRD_PARTY.md").replace(
            "| <Name> | <x.y.z, matches package.json or Package.resolved> |", "| `lib` | 1.2.3 |")
        files = {"THIRD_PARTY.md": third, "core/package.json": json.dumps({"dependencies": {"lib": "1.2.3"}})}
        self.assertEqual(self.check(files=files)[0], 0)
        code, out = self.check(files={**files, "core/package.json": json.dumps({"dependencies": {"lib": "^1.2.3"}})})
        self.assertIn("is not an exact version", out)
        code, out = self.check(files={**files, "web/package.json": json.dumps({"devDependencies": {"other": "2.0.0"}})})
        self.assertIn("other is in web/package.json but has no row", out)
        code, out = self.check(files={**files, "core/package.json": json.dumps({"dependencies": {"lib": "1.2.4"}})})
        self.assertIn("lib is 1.2.4", out)

    def test_names_in_typescript(self):
        code, out = self.check(files={"core/src/a.ts": "// like Rival does\n"}, config={"forbidden": ["rival"]})
        self.assertEqual(code, 1)
        self.assertIn("core/src/a.ts:1: mentions 'Rival'", out)

    def test_screen_code_needs_design_change(self):
        tmp, root = make(repo_type="selfhosted")
        with tmp:
            git(root, "commit", "-q", "-m", "base")
            git(root, "branch", "base")
            (root / "web/src/screens/alpha").mkdir(parents=True)
            (root / "web/src/screens/alpha/view.tsx").write_text("x")
            git(root, "add", ".")
            git(root, "commit", "-q", "-m", "change")
            code, out = run(root, {"PR_BASE": "base", "PR_TITLE": "refactor: x", "PR_LABELS": ""})
            self.assertEqual(code, 1)
            self.assertIn("UI code changed (web/src/screens/alpha/view.tsx", out)



class HandbookTest(unittest.TestCase):
    def test_reference_to_missing_handbook_file(self):
        gone = "handbook/" + "no-such-page.md"  # split so this file does not reference it itself
        tmp, root = make(files={"AGENTS.md": f"See `{gone}` and `handbook/agents.md`.\n"})
        with tmp:
            code, out = run(root)
        self.assertEqual(code, 1)
        self.assertIn(f"AGENTS.md:1: reference to {gone}", out)
        self.assertNotIn("handbook/agents.md,", out)

    def test_reference_to_pending_document_is_allowed(self):
        tmp, root = make(files={"docs/roadmap.md": "Writes `docs/legal.md` after pricing.\n"})
        with tmp:
            self.assertEqual(run(root), (0, "docs ok\n"))
        tmp, root = make(files={"docs/roadmap.md": "Writes `docs/nowhere.md`.\n"})
        with tmp:
            self.assertIn("reference to missing file docs/nowhere.md", run(root)[1])

    def test_placeholder_reference_is_not_checked(self):
        tmp, root = make(files={"AGENTS.md": "See `handbook/types/<type>/code.md`.\n"})
        with tmp:
            self.assertEqual(run(root), (0, "docs ok\n"))

    def test_every_type_is_complete(self):
        handbook = HERE.parent / "handbook"
        for name, t in MANIFEST["types"].items():
            self.assertTrue((handbook / "types" / name / "README.md").is_file(), name)
            for stack in t["stacks"]:
                self.assertTrue((handbook / "stacks" / f"{stack}.md").is_file(), stack)
            for tname in [*t["documents"].values(), t["milestone"]]:
                self.assertTrue((handbook / "templates" / tname).is_file(), tname)
        for tname in MANIFEST["patterns"].values():
            self.assertTrue((handbook / "templates" / tname).is_file(), tname)

    def test_template_markers_follow_paths(self):
        templates = HERE.parent / "handbook/templates"
        for p in sorted(templates.rglob("*")):
            if not p.is_file() or p.name == "manifest.json":
                continue
            rel = str(p.relative_to(templates))
            name = rel.removeprefix("common/")
            first = p.read_text().split("\n")[0]
            self.assertRegex(first, rf"(<!-- template: |\(template: ){re.escape(name)} v\d+", rel)


if __name__ == "__main__":
    unittest.main()
