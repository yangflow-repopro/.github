#!/usr/bin/env python3
"""Check a repository's documentation against the organization's templates (handbook/docs.md).

    python3 check-docs.py [repo-root]

The repository declares its type in `.repo-type` (app, selfhosted, website, library, template, org). Optional
`.docs-check.json`:
    {"forbidden": ["other-product", ...],      names that must not appear anywhere (case-insensitive)
     "allow": ["path/glob", ...],              files exempt from the name check
     "ignore": ["path/glob", ...],             files exempt from the reference checks
     "external": ["docs/legal.md", ...],        paths that live in another repository (e.g. the app's)
     "pending": ["docs/design.md", ...],       required documents not written yet: no template check, and
                                               references to them are allowed (temporary, with a plan entry
                                               that removes it)
     "design_icons": ["icon.html", ...]}       extra top-level entries allowed in design/ (icon sources)

When design/README.md carries the `design-README.md v2` marker the ledger checks run (handbook/ui-workflow.md):
rows against design/screens, code dirs, status words, dates, screenshots, spec anchors, design/ whitelist.
Repositories still on v1 are not ledger-checked until they migrate.

Pull request checks run when PR_BASE is set (the base branch ref, e.g. origin/main) together with
PR_TITLE and PR_LABELS (comma separated):
  - a `feat` or `fix` PR that changes product code must change CHANGELOG.md (label `no-changelog` exempts)
  - when design/screens/ exists, a change to screen code (UI/<Screen>/; for selfhosted also web/src/screens/<screen>/)
    must change design/screens/
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
HANDBOOK = HERE.parent / "handbook"
TEMPLATES = HANDBOOK / "templates"
# A reference to a handbook file (handbook/<path>.md|json) in any document, comment or script of any repository.
HANDBOOK_REF = re.compile(r"(?<![\w.-])handbook/([\w./<>-]*[\w>-]\.(?:md|json))")
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
    if template_name.endswith("LICENSE"):
        want = re.findall(r"^\d+\. (.+)$", tmpl, re.M)
        have = re.findall(r"^\d+\. (.+)$", text, re.M)
        if want != have:
            err(rel, f"sections differ from the {template_name} template: expected {want}, found {have}")
        tag = re.search(r"\(template: \S+ v\d+\)", tmpl.split("\n")[0]).group(0)
        if tag not in text.split("\n")[0]:
            err(rel, f"first line must carry '{tag}'")
        return
    want_marker, have_marker = marker(tmpl), marker(text)
    if template_name == "common/design-README.md" and have_marker == (want_marker[0], 1):
        have_marker = want_marker  # v1 stays valid until the repository migrates (same H2 sections)
    if have_marker != want_marker:
        err(rel, f"first line must be '<!-- template: {want_marker[0]} v{want_marker[1]} -->' (found {have_marker})")
    have = h_lines(text, 2)
    if Path(template_name).name.startswith("CHANGELOG"):
        # Released versions follow Unreleased: "[X.Y.Z] - YYYY-MM-DD"
        released = [h for h in have[1:] if re.fullmatch(r"\[\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}", h)]
        if have[1:] != released:
            err(rel, "sections after [Unreleased] must be '[X.Y.Z] - YYYY-MM-DD'")
        have = have[:1]
    if h_lines(tmpl, 2) != have:
        err(rel, f"H2 sections differ from template {template_name}: expected {h_lines(tmpl, 2)}, found {have}")


TEXT_SUFFIXES = {".md", ".swift", ".py", ".sh", ".yml", ".yaml", ".html", ".js", ".json", ".mjs", ".plist", ".txt",
                 ".xcstrings", ".ts", ".tsx", ".mts", ".css"}
# Where a repository type keeps screen code (handbook/ui-workflow.md); a change there must change design/screens/.
SCREEN_CODE = {
    "selfhosted": r"^web/src/screens/[^/]+/.+\.(?:ts|tsx|css)$|(^|/)UI/[^/]+/.+\.swift$",
}
DEFAULT_SCREEN_CODE = r"(^|/)UI/[^/]+/.+\.swift$"
LEDGER_COLUMNS = ["screen", "spec", "design file", "code dir", "status", "signed off", "accepted"]
STATUSES = ["planned", "proposed", "signed-off", "in-review", "accepted"]
DESIGN_FIXED = {"README.md", "tokens.html", "check-tokens.py", "screens", "screenshots", ".DS_Store", "__pycache__"}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def ledger_rows(text):
    """Rows of the first table under '## Screens': (header, [cells])."""
    rows, in_section, header = [], False, None
    for line in text.split("\n"):
        if line.startswith("## "):
            in_section = line[3:].strip() == "Screens"
        elif in_section and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if header is None:
                header = [c.lower() for c in cells]
            elif not all(re.fullmatch(r":?-+:?", c) for c in cells):
                rows.append(cells)
    return header, rows


def check_ledger(config):
    readme = ROOT / "design/README.md"
    if not readme.is_file():
        return
    text = readme.read_text(encoding="utf-8")
    if not text.startswith("<!-- template: design-README.md v2 -->"):
        return
    rel = "design/README.md"
    header, rows = ledger_rows(text)
    if header != LEDGER_COLUMNS:
        err(rel, f"Screens table columns must be {LEDGER_COLUMNS}, found {header}")
        return
    strip = lambda c: c.strip().strip("`").strip()
    screens_dir = ROOT / "design/screens"
    files = sorted(p.name for p in screens_dir.glob("*.html")) if screens_dir.is_dir() else []
    directions = {}  # key -> direction files
    plain = set()
    for name in files:
        m = re.fullmatch(r"(.+)\.direction-[^.]+\.html", name)
        if m:
            directions.setdefault(m.group(1), []).append(name)
        else:
            plain.add(name[:-5])
    spec = ROOT / "docs/spec.md"
    spec_anchors = anchors(spec.read_text(encoding="utf-8")) if spec.is_file() else set()
    seen = {}
    for cells in rows:
        row = dict(zip(LEDGER_COLUMNS, [strip(c) for c in cells]))
        name = row["screen"]
        status = row["status"]
        m = re.fullmatch(r"screens/(.+)\.html", row["design file"])
        key = m.group(1) if m else name
        where = f"{rel} ({name})"
        if key in seen:
            err(where, f"duplicate ledger row for {key}")
        seen[key] = status
        if status not in STATUSES:
            err(where, f"status {status!r} must be one of {', '.join(STATUSES)}")
            continue
        sm = re.fullmatch(r"docs/spec\.md#([\w-]+)", row["spec"])
        if not sm:
            err(where, f"Spec cell must be docs/spec.md#anchor, found {row['spec']!r}")
        elif sm.group(1) not in spec_anchors:
            err(where, f"spec anchor {row['spec']} does not exist")
        if status != "planned":
            if not m:
                err(where, "Design file cell must be screens/<screen>.html")
            elif key not in plain and not (status == "proposed" and key in directions):
                err(where, f"design/screens/{key}.html does not exist")
        if status != "proposed" and key in directions:
            err(where, f"status {status} must not have direction files ({directions[key][0]}...): "
                       "rename the chosen one to <screen>.html and delete the rest")
        if status in ("in-review", "accepted"):
            code = row["code dir"]
            if not code or not (ROOT / code).is_dir():
                err(where, f"code dir {code!r} does not exist (required for {status})")
        if status in ("signed-off", "in-review", "accepted") and not DATE.fullmatch(row["signed off"]):
            err(where, f"status {status} needs a Signed off date (YYYY-MM-DD)")
        if status == "accepted":
            if not DATE.fullmatch(row["accepted"]):
                err(where, "status accepted needs an Accepted date (YYYY-MM-DD)")
            shots = ROOT / "design/screenshots" / key
            if not shots.is_dir() or not list(shots.glob("*.png")):
                err(where, f"status accepted needs device screenshots: design/screenshots/{key}/*.png")
        elif row["accepted"]:
            err(where, f"Accepted date is set but status is {status}")
    for key in sorted(plain | set(directions)):
        if key not in seen:
            err(f"design/screens/{key}.html", "no row in the design/README.md ledger")
    design = ROOT / "design"
    allowed = DESIGN_FIXED | set(config.get("design_icons", []))
    for p in sorted(design.iterdir()):
        if p.name not in allowed:
            err(f"design/{p.name}", "not on the design/ whitelist (README.md, tokens.html, check-tokens.py, screens/, "
                                    "screenshots/, icon sources listed in .docs-check.json design_icons)")


def main():
    type_file = ROOT / ".repo-type"
    if not type_file.is_file():
        err(".repo-type", "missing: declare one of " + ", ".join(json.loads((TEMPLATES / "manifest.json").read_text())["types"]))
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
    for rel, tname in manifest["types"][repo_type]["documents"].items():
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

    check_ledger(config)

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
        check_against(rel, manifest["patterns"]["docs/adr/NNNN-*.md"], text)
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
                check_against(rel, manifest["patterns"]["docs/milestones/v*-security.md"])
            elif re.fullmatch(r"v\d+\.\d+\.md|next\.md", p.name):
                check_against(rel, manifest["types"][repo_type]["milestone"])
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

    # 3c. third-party table versus package.json (exact versions only)
    manifests = [f for f in subprocess.run(["git", "-C", str(ROOT), "ls-files", "package.json", "*/package.json"], capture_output=True, text=True).stdout.split("\n") if f]
    if manifests:
        rows = [[c.strip().strip("`") for c in line.strip().strip("|").split("|")] for line in third.read_text().split("\n") if line.startswith("|")] if third.is_file() else []
        for f in manifests:
            pkg = json.loads((ROOT / f).read_text())
            for section in ("dependencies", "devDependencies", "optionalDependencies"):
                for name, spec in pkg.get(section, {}).items():
                    if spec.startswith("workspace:"):
                        continue
                    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[\w.]+)?", spec):
                        err(f, f"{name}: {spec!r} is not an exact version")
                        continue
                    row = next((r for r in rows if r[0].lower() == name.lower()), None)
                    if row is None:
                        err("THIRD_PARTY.md", f"{name} is in {f} but has no row")
                    elif spec not in row[1]:
                        err("THIRD_PARTY.md", f"{name} is {spec} in {f} but the row says {row[1]!r}")

    # 4. text scans: other products' names, ordinal references, references that must resolve
    files = [Path(f) for f in subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n") if f]
    texts = {}
    for rel in files:
        if rel.suffix in TEXT_SUFFIXES or rel.name in {"LICENSE", "Dockerfile"}:
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
        for m in HANDBOOK_REF.finditer(text):
            if "<" not in m.group(1) and not (HANDBOOK / m.group(1)).exists():
                line = text[: m.start()].count("\n") + 1
                err(f"{rel}:{line}", f"reference to handbook/{m.group(1)}, which does not exist in the organization handbook")
        if repo_type == "org" and rel.startswith("handbook/") and not rel.startswith("handbook/templates/") and rel.endswith(".md"):
            for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
                target = m.group(1)
                if not re.match(r"[a-z]+:", target) and not ((ROOT / rel).parent / target).exists():
                    line = text[: m.start()].count("\n") + 1
                    err(f"{rel}:{line}", f"link to {target}, which does not exist")
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
                if m.group(1) in config.get("external", []) + pending and not target.is_file():
                    continue  # lives in another repository, or is a required document not written yet
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
            and "/test/" not in f and ".test." not in f
            and not f.endswith((".md", ".json", ".xcodeproj/project.pbxproj", ".yml"))]
    if re.match(r"(feat|fix)(\(|:|!)", title) and code and "no-changelog" not in labels and "CHANGELOG.md" not in changed:
        err("CHANGELOG.md", "a feat/fix PR that changes product code must add a line under [Unreleased] (or label the PR no-changelog)")
    if (ROOT / "design/screens").is_dir() and "design-unchanged" not in labels:
        type_file = ROOT / ".repo-type"
        repo_type = type_file.read_text().strip() if type_file.is_file() else ""
        ui = [f for f in changed if re.search(SCREEN_CODE.get(repo_type, DEFAULT_SCREEN_CODE), f)]
        if ui and not any(f.startswith("design/screens/") for f in changed):
            err("design/screens", f"UI code changed ({ui[0]}...) without a change under design/screens/ (or label the PR design-unchanged)")


main()
pr_checks()
if errors:
    print("\n".join(errors))
    print(f"\n{len(errors)} problem(s)")
    sys.exit(1)
print("docs ok")
