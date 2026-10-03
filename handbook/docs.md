# Documentation

Every repository documents itself with the same set of documents, each built from one template. This file is
the map and the rules; the templates are in `templates/`, the check that enforces them is
`scripts/check-docs.py`. Product names appear only in the product's own repository: this handbook and the
templates use `<Name>` and `<domain>`.

## The map

Each document answers one question.

| Document | Answers | Template |
|---|---|---|
| `README.md` | What is this, what state is it in, how do I build it, where is everything | `README.md` |
| `AGENTS.md` | What must an AI collaborator know before changing anything | `AGENTS.md` |
| `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` | (pointers) | one line: `@AGENTS.md` |
| `docs/spec.md` | What to build and what not; data, modules, flows, acceptance | `spec.md` |
| `docs/design.md` | The design language: tokens, components, materials, motion, copy tone, accessibility | `design.md` |
| `design/README.md` | How to read the mockups, which screens exist, why they look so | `design-README.md` |
| `docs/roadmap.md` | The order of work after the baseline | `roadmap.md` |
| `docs/milestones/v<X.Y>.md` | One iteration: goal, scope, decisions, tests, acceptance | `milestone.md` |
| `docs/milestones/v<X.Y>-security.md` | The security walkthrough recorded for a release | `security-walkthrough.md` |
| `docs/adr/NNNN-title.md` and `docs/adr/README.md` | One decision each, and their index | `adr.md` |
| `docs/legal.md` | Where each legal fact lives and which code it must match | `legal.md` |
| `docs/website.md` | What the app depends on from the website (paths, feeds, download copy) | `website.md` |
| `docs/process.md` | Only what differs from the handbook for this repository | `process.md` |
| `CHANGELOG.md`, `CHANGELOG.zh.md` | User-facing changes (Keep a Changelog) | `CHANGELOG.md`, `CHANGELOG.zh.md` |
| `THIRD_PARTY.md` | Every dependency: version, license, shipped or not, where its notice is | `THIRD_PARTY.md` |
| `SECURITY.md` | Where to report a vulnerability | `SECURITY.md` |
| `LICENSE` | The terms of service, which are also the license agreement | `LICENSE` |

Which documents a repository needs depends on its type, declared in `.repo-type` at the repository root
(`app`, `website`, `library`, `template`, `org`). `scripts/check-docs.py` holds the table.

## Rules

1. **One template per kind of document.** A product document fills the template; it does not change the
   skeleton. Every H2 of the template is required, in the template's order. A section with nothing to say
   says `None`; it is not deleted.
2. **The first line is the template marker**, `<!-- template: <name> v<N> -->`, copied from the template. When
   the template changes, its version number goes up and every document using it is rewritten from the new
   template; the check fails until it is.
3. **Rewrite, do not patch.** A document that no longer matches its template is rewritten from the template,
   moving the content over, not edited in place into shape.
4. **Headings are stable names, not numbers.** Other documents and code link to
   `docs/spec.md#licensing`, never to "section 4.9" or "scene 17". Renaming a heading, a file or an ADR
   includes fixing every reference in the same pull request. References that are numbered (`§4.9`, `M4`,
   `scene 3`, `ADR-0004`) are not allowed.
5. **Documents describe their own product only.** No comparisons with other products, no "same as X", no old
   names. What products have in common is written here in the handbook, once.
6. **English everywhere except UI copy.** `CHANGELOG.zh.md` is the one Chinese file of an app (it feeds the
   Chinese website).
7. **Docs win.** If a document and the code disagree, fix the document first, then the code.

## Names

- Milestone documents: `v<X.Y>.md` (the release they describe) and `v<X.Y>-security.md`. Work in progress for
  the next release lives in `docs/milestones/next.md` and is renamed when the version is chosen. Internal
  numbered milestones are not kept after the release that finished them.
- ADRs: `NNNN-title.md`, four digits, lowercase hyphenated title; the index lists every file once, with the
  same title as the file's H1.
- Screens: `design/screens/<screen>.html`, named like the code directory `UI/<Screen>/`.

## Lifecycle of an iteration

`Issue` (the tracking issue) → `docs/milestones/next.md` (goal, scope, decisions) → design (`design/screens/`)
→ implementation PRs → acceptance on a Mac → `next.md` becomes `v<X.Y>.md`, `CHANGELOG.md` gets its dated
section, the release is tagged. The playbooks in `playbooks/` list the steps and the files each touches.

## Pointers for AI tools

Only `AGENTS.md` carries instructions. `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` contain
the single line `@AGENTS.md`.
