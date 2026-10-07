# Documentation

Each repository selects the document set for its purpose, with templates as a required baseline. This file is
the map and the rules; the templates are in `handbook/templates/`, the check that enforces them is
`scripts/check-docs.py`. Product names appear only in the product's own repository: this handbook and the
templates use `<Name>` and `<domain>`.

## The map

Each document answers one question. The template column names the template in `handbook/templates/common/` or, for
`<type>/…`, the one in that type's directory.

| Document | Answers | Template |
|---|---|---|
| `README.md` | What is this, what state is it in, how do I build it, where is everything | `<type>/README.md` |
| `AGENTS.md` | What must an AI collaborator know before changing anything | `AGENTS.md` |
| `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md` | (pointers) | one line: `@AGENTS.md` |
| `docs/spec.md` | What to build and what not; data, modules, flows, acceptance | `spec.md`, or `pipeline/spec.md` |
| `docs/architecture.md` | How a self-hosted product's parts fit: layers, boundaries, extension points, data flow, privacy | `selfhosted/architecture.md` |
| `docs/design.md` | The design language: tokens, components, motion, copy tone, accessibility | `<type>/design.md` |
| `design/README.md` | How to read the mockups; the ledger of screens and their status (`handbook/guides/ui-workflow.md`) | `design-README.md` |
| `docs/roadmap.md` | The order of work after the baseline | `roadmap.md` |
| `docs/milestones/v<X.Y>.md` | One iteration: goal, scope, decisions, tests, acceptance | `milestone.md`, or `<type>/milestone.md` where a type has its own |
| `docs/milestones/v<X.Y>-security.md` | The security walkthrough recorded for a release | `security-walkthrough.md` |
| `docs/adr/NNNN-title.md` and `docs/adr/README.md` | One decision each, and their index | `adr.md`, `adr-index.md` |
| `docs/legal.md` | Where each legal fact lives and which code it must match | `legal.md` |
| `docs/website.md` | What the product depends on from its website (paths, feeds, download copy) | `website.md` |
| `docs/content.md` | Where each piece of a website's copy comes from | `website/content.md` |
| `docs/hosting.md` | What the product needs from and promises to the user's host: ports, data, resources, upgrades | `selfhosted/hosting.md` |
| `docs/threat-model.md` | What the product protects, where the trust boundaries are, how each threat is mitigated | `selfhosted/threat-model.md`, `pipeline/threat-model.md` |
| `docs/operations.md` | What a pipeline needs to run and how to stop it: triggers, secrets, outside services, failure, switches, cost | `pipeline/operations.md` |
| `docs/process.md` | Only what differs from the handbook for this repository | `process.md` |
| `CHANGELOG.md`, `CHANGELOG.zh.md` | User-facing changes (Keep a Changelog) | `CHANGELOG.md`, `CHANGELOG.zh.md` |
| `THIRD_PARTY.md` | Every dependency: version, license, shipped or not, where its notice is | `<type>/THIRD_PARTY.md` |
| `SECURITY.md` | Where to report a vulnerability | `SECURITY.md` |
| `LICENSE` | The terms of service, which are also the license agreement | `<type>/LICENSE` |

## Repository types

Which documents a repository needs, and from which template, depends on its type, declared in `.repo-type` at the
repository root. `handbook/templates/manifest.json` holds the table; `scripts/check-docs.py` enforces it. Each type
is described in `handbook/types/<type>/README.md`.

| Type | What it is | Templates of its own (`handbook/templates/<type>/`) |
|---|---|---|
| `mygo-app` | A Go desktop app with MyGo native UI | README, design, THIRD_PARTY, LICENSE |
| `app` | A native macOS app distributed as a notarized download | README, design, THIRD_PARTY, LICENSE |
| `selfhosted` | A service the user runs on their own host, with optional clients or agents | README, architecture, design, milestone, THIRD_PARTY, LICENSE, hosting, threat-model |
| `pipeline` | A TypeScript command-line tool and the workflows that run it, acting with the maintainer's accounts; no UI, not distributed | README, spec, operations, threat-model, milestone, THIRD_PARTY |
| `website` | A product's static website | README, design, content, THIRD_PARTY |
| `library` | Shared code or tooling used by other repositories | README, design |
| `template` | A repository other repositories are created from | README |
| `org` | This repository | README |

Types are documentation and lifecycle presets, not a requirement to use every component in their example layout.
A project records its actual stack, platforms, distribution and differences in its agent instructions and process
document. Use the existing preset when its document set fits; a new language or optional client alone needs no new type.
Add a type only when a current project needs a different document set or lifecycle. A template lives in `common/` only when
every one of its sections fits every type that uses it. Rules about a language go to `handbook/stacks/`, never into
a type's pages, so every type that uses the language shares them.

## Rules

1. **One template per kind of document.** A product document fills the template; it does not change the
   skeleton. Every H2 of the template is required exactly once, in the template's order.
   A project may add sections between them. A required section with nothing to say says `None`; it is not deleted.
   Changelogs and legal license section lists keep their dedicated strict checks.
   An architecture override does not waive required documents; describe non-applicable sections as `None`.
2. **The first line is the template marker**, `<!-- template: <name> v<N> -->`, copied from the template. When
   the template changes, its version number goes up and every document using it is rewritten from the new
   template as an explicit migration; the check fails until it is.
   Pin the reusable docs workflow and its `handbook-ref` input to the same organization commit SHA.
   The checker, manifest and templates then come from one revision; changes on `main` do not silently migrate a project.
   Unpinned callers remain supported during migration. Upgrade the SHA, documents and references together in a PR.
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
- Screens: `design/screens/<screen>.html`, named like the screen's code directory (`handbook/guides/ui-workflow.md`, Code
  directories and captures).

## Lifecycle of an iteration

`Issue` (the tracking issue) → `docs/milestones/next.md` (goal, scope, decisions) → design (`design/screens/`)
→ implementation PRs → acceptance on the project's declared runtime or devices.
Versioned products rename `next.md` to `v<X.Y>.md`, update their changelog and tag the release.
Pipelines follow their rollout and rollback rules; they do not acquire release tags or changelogs from this lifecycle. The playbooks in `playbooks/` list the steps and the files each touches.

The lifecycle of a screen, the ledger in `design/README.md` and the `design/` whitelist are in
`handbook/guides/ui-workflow.md`.

## Pointers for AI tools

Only `AGENTS.md` carries instructions. `CLAUDE.md`, `GEMINI.md` and `.github/copilot-instructions.md` contain
the single line `@AGENTS.md`.
