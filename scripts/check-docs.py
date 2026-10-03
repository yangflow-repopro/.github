#!/usr/bin/env python3
"""Check a repository's documentation against the organization's templates (handbook/docs.md).

    python3 check-docs.py [repo-root]

The repository declares its type in `.repo-type` (app, website, library, template, org). Optional
`.docs-check.json`:
    {"forbidden": ["other-product", ...],      names that must not appear anywhere (case-insensitive)
     "allow": ["path/glob", ...],              files exempt from the name check
     "ignore": ["path/glob", ...],             files exempt from the reference checks
     "external": ["docs/legal.md", ...],        paths that live in another repository (e.g. the app's)
     "pending": ["docs/design.md", ...]}       required documents whose template check is postponed
                                               (temporary, with a plan entry that removes it)

Pull request checks run when PR_BASE is set (the base branch ref, e.g. origin/main) together with
PR_TITLE and PR_LABELS (comma separated):
  - a `feat` or `fix` PR that changes product code must change CHANGELOG.md (label `no-changelog` exempts)
  - when design/screens/ exists, a change under a UI/<Screen>/ directory must change design/screens/
    (label `design-unchanged` exempts)

Exit status 1 when any check fails; every problem is printed as `path: message`.
"""
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "handbook/templates"
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
errors = []


def err(path, message):
    errors.append(f"{path}: {message}")


def h_lines(text, level):
    """Headings of the given level outside fenced code blocks."""
    out, fenced = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(rf"^{'#' * level} \S", line):
            out.append(line[level + 1:].strip())
    return out


def marker(text):
    m = re.match(r"<!-- template: (\S+) v(\d+) -->", text)
    return (m.group(1), int(m.group(2))) if m else None


def slug(heading):
    s = re.sub(r"`", "", heading.lower())
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    return s.strip().replace(" ", "-")


def anchors(text):
    found = set(re.findall(r'<a id="([^"]+)"', text))
    for level in range(1, 5):
        found |= {slug(h) for h in h_lines(text, level)}
    return found


def check_against(rel, template_name, text=None):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8") if text is None else text
    tmpl = (TEMPLATES / template_name).read_text(encoding="utf-8")
    if template_name == "LICENSE":
        want = re.findall(r"^\d+\. (.+)$", tmpl, re.M)
        have = re.findall(r"^\d+\. (.+)$", text, re.M)
        if want != have:
            err(rel, f"sections differ from the LICENSE template: expected {want}, found {have}")
        if "(template: LICENSE v1)" not in text.split("\n")[0]:
            err(rel, "first line must carry '(template: LICENSE v1)'")
        return
    want_marker, have_marker = marker(tmpl), marker(text)
    if have_marker != want_marker:
        err(rel, f"first line must be '<!-- template: {want_marker[0]} v{want_marker[1]} -->' (found {have_marker})")
    have = h_lines(text, 2)
    if template_name.startswith("CHANGELOG"):
        # Released versions follow Unreleased: "[X.Y.Z] - YYYY-MM-DD"
        released = [h for h in have[1:] if re.fullmatch(r"\[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}", h)]
        if have[1:] != released:
            err(rel, "sections after [Unreleased] must be '[X.Y.Z] - YYYY-MM-DD'")
        have = have[:1]
    if h_lines(tmpl, 2) != have:
        err(rel, f"H2 sections differ from template {template_name}: expected {h_lines(tmpl, 2)}, found {have}")


def main():
    type_file = ROOT / ".repo-type"
    if not type_file.is_file():
        err(".repo-type", "missing: declare app, website, library, template or org")
        return
    repo_type = type_file.read_text().strip()
    manifest = json.loads((TEMPLATES / "manifest.json").read_text())
    if repo_type not in manifest["types"]:
        err(".repo-type", f"unknown type {repo_type!r}")
        return
    config_file = ROOT / ".docs-check.json"
    config = json.loads(config_file.read_text()) if config_file.is_file() else {}

    # 1. required documents and their templates
    pending = config.get("pending", [])
    for rel, tname in manifest["types"][repo_type].items():
        if rel in pending:
            continue
        if not (ROOT / rel).is_file():
            err(rel, f"missing (required for type {repo_type})")
            continue
        check_against(rel, tname)
    for rel in manifest["pointers"]:
        p = ROOT / rel
        if not p.is_file():
            err(rel, "missing: pointer file containing only '@AGENTS.md'")
        elif p.read_text().strip() != "@AGENTS.md":
            err(rel, "must contain only the line '@AGENTS.md'")

    # 2. ADRs
    adr_dir = ROOT / "docs/adr"
    adrs = sorted(p for p in adr_dir.glob("*.md") if p.name != "README.md") if adr_dir.is_dir() else []
    index_text = (adr_dir / "README.md").read_text() if (adr_dir / "README.md").is_file() else ""
    for p in adrs:
        rel = str(p.relative_to(ROOT))
        m = re.fullmatch(r"(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md", p.name)
        if not m:
            err(rel, "ADR file names are NNNN-lowercase-title.md")
            continue
        text = p.read_text(encoding="utf-8")
        check_against(rel, "adr.md", text)
        h1 = h_lines(text, 1)
        if not h1 or not h1[0].startswith(m.group(1) + " "):
            err(rel, f"H1 must be '# {m.group(1)} <Title>'")
        elif f"[{m.group(1)}]({p.name}) | {h1[0][5:]} |" not in index_text:
            err(rel, "not listed in docs/adr/README.md with the same title as its H1")
    for linked in re.findall(r"\]\((\d{4}-[^)]+\.md)\)", index_text):
        if not (adr_dir / linked).is_file():
            err("docs/adr/README.md", f"lists {linked}, which does not exist")

    # 3. milestones
    ms_dir = ROOT / "docs/milestones"
    if ms_dir.is_dir():
        for p in sorted(ms_dir.glob("*.md")):
            rel = str(p.relative_to(ROOT))
            if re.fullmatch(r"v\d+\.\d+-security\.md", p.name):
                check_against(rel, "security-walkthrough.md")
            elif re.fullmatch(r"v\d+\.\d+\.md|next\.md", p.name):
                check_against(rel, "milestone.md")
            else:
                err(rel, "milestone files are v<X.Y>.md, v<X.Y>-security.md or next.md")

    # 3b. third-party table versus the resolved Swift packages
    third = ROOT / "THIRD_PARTY.md"
    resolved = [f for f in subprocess.run(["git", "-C", str(ROOT), "ls-files", "*Package.resolved"], capture_output=True, text=True).stdout.split("\n") if f]
    if third.is_file() and resolved:
        rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in third.read_text().split("\n") if line.startswith("|")]
        for f in resolved:
            for pin in json.loads((ROOT / f).read_text()).get("pins", []):
                ident, version = pin["identity"], pin.get("state", {}).get("version")
                row = next((r for r in rows if ident in r[0].lower()), None)
                if row is None:
                    err("THIRD_PARTY.md", f"{ident} is in {f} but has no row")
                elif version and version not in row[1]:
                    err("THIRD_PARTY.md", f"{ident} is {version} in {f} but the row says {row[1]!r}")

    # 4. text scans: other products' names, ordinal references, references that must resolve
    files = [Path(f) for f in subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n") if f]
    texts = {}
    for rel in files:
        if rel.suffix in {".md", ".swift", ".py", ".sh", ".yml", ".yaml", ".html", ".js", ".json", ".mjs", ".plist", ".txt", ".xcstrings"} or rel.name == "LICENSE":
            try:
                texts[str(rel)] = (ROOT / rel).read_text(encoding="utf-8")
            except (UnicodeDecodeError, FileNotFoundError):
                pass
    allow = config.get("allow", [])
    ignore = config.get("ignore", [])
    skip_dirs = ("public/", "build/", ".build/", "scripts/sitekit/", ".docs-check.json")
    forbidden = [re.compile(r"(?<![A-Za-z])" + re.escape(n) + r"(?![a-z])", re.I) for n in config.get("forbidden", [])]
    for rel, text in texts.items():
        if rel.startswith(skip_dirs) or rel.endswith(".xcodeproj/project.pbxproj"):
            continue
        if not any(fnmatch.fnmatch(rel, g) for g in allow):
            for rx in forbidden:
                m = rx.search(text)
                if m:
                    line = text[: m.start()].count("\n") + 1
                    err(f"{rel}:{line}", f"mentions {m.group(0)!r}: documents and code describe this product only")
        if any(fnmatch.fnmatch(rel, g) for g in ignore) or rel.startswith("CHANGELOG"):
            continue
        lines = text.split("\n")
        for m in re.finditer(r"§\s?\d|\bscenes?\s+\d|\bADR-\d+|(?<![\w.])M\d\b(?![\w-])", text):
            line = text[: m.start()].count("\n") + 1
            if m.group(0)[0] == "M" and not rel.endswith(".md") and not lines[line - 1].lstrip().startswith(("//", "#", "*", "///")):
                continue  # M<n> in code is only a milestone marker when it sits in a comment (SVG paths use it too)
            err(f"{rel}:{line}", f"numbered reference {m.group(0)!r}: link a stable anchor (docs/spec.md#slug), ADR file or screen instead")
        if True:
            for m in re.finditer(r"(?<![\w/.-])((?:docs|design)/[\w./-]*[\w-]\.(?:md|html))(#[\w-]+)?", text):
                target = ROOT / m.group(1)
                line = text[: m.start()].count("\n") + 1
                if m.group(1) in config.get("external", []) and not target.is_file():
                    continue
                if not target.is_file():
                    err(f"{rel}:{line}", f"reference to missing file {m.group(1)}")
                elif m.group(2) and m.group(2)[1:] not in anchors(target.read_text(encoding="utf-8")):
                    err(f"{rel}:{line}", f"reference to missing anchor {m.group(1)}{m.group(2)}")


def pr_checks():
    import os
    base = os.environ.get("PR_BASE")
    if not base:
        return
    title = os.environ.get("PR_TITLE", "")
    labels = {l.strip() for l in os.environ.get("PR_LABELS", "").split(",") if l.strip()}
    changed = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", f"{base}...HEAD"], capture_output=True, text=True).stdout.split()
    code = [f for f in changed if not f.startswith(("docs/", "scripts/", ".github/", "design/", ".claude/", ".codex/")) and "Tests/" not in f
            and not f.endswith((".md", ".json", ".xcodeproj/project.pbxproj", ".yml"))]
    if re.match(r"(feat|fix)(\(|:|!)", title) and code and "no-changelog" not in labels and "CHANGELOG.md" not in changed:
        err("CHANGELOG.md", "a feat/fix PR that changes product code must add a line under [Unreleased] (or label the PR no-changelog)")
    if (ROOT / "design/screens").is_dir() and "design-unchanged" not in labels:
        ui = [f for f in changed if re.search(r"(^|/)UI/[^/]+/", f) and f.endswith(".swift")]
        if ui and not any(f.startswith("design/screens/") for f in changed):
            err("design/screens", f"UI code changed ({ui[0]}...) without a change under design/screens/ (or label the PR design-unchanged)")


main()
pr_checks()
if errors:
    print("\n".join(errors))
    print(f"\n{len(errors)} problem(s)")
    sys.exit(1)
print("docs ok")
