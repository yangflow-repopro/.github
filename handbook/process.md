# Development process

How every yangflow-repopro project is built. Product repositories do not restate this file; their
`docs/process.md` only lists what differs.

## Language

- Everything except UI copy is English: code, comments, docs, scripts, logs, commits, PRs, CHANGELOG,
  release notes. UI copy is multilingual and lives in the String Catalog. `CHANGELOG.zh.md` is the one
  Chinese file per app; it feeds the Chinese website.
- Keep descriptions short: one necessary sentence beats a paragraph. Explain why, constraints and
  gotchas; do not restate the code.

## Roles

| Role | Who | Owns |
|---|---|---|
| Product and design decisions | Maintainer | Requirements, designs, final acceptance on a real Mac, merging |
| Implementation | AI collaborator | Spec drafts, mockups, code, tests, self-review, PRs |

The docs (`docs/`) are the only source of truth. When something is ambiguous, change the docs first,
then the code. If docs and code conflict, the docs win; point it out in the PR.

## Four steps per milestone

```
Spec ──► Design ──► Implement ──► Accept
 confirm   sign off   PR review     verify locally
```

1. **Spec**: scope, non-goals and acceptance checklist in `docs/milestones/<name>.md`.
2. **Design** (milestones with UI): high-fidelity mockups in `design/`, 2–3 directions per screen.
   **No UI code before sign-off.**
3. **Implement**: feature branches, small PRs (ideally under 400 changed lines). UI PRs attach
   screenshots or a recording (light + dark, every state) and tick the design acceptance checklist.
4. **Accept**: the maintainer runs it locally and ticks the checklist. Then merge.

## Branches and merging

- `main` always builds, runs and has green tests. Only the maintainer merges into `main`.
- Enforced by a ruleset on each product repository ("main protection"): changes go through a pull request
  with the CI check green (the check name is `ci / …` from the repository's `ci.yml`); no force-push, no
  deletion of `main`. Repository admins can bypass only through a pull request.
- Feature branches: `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `design/<topic>`, `build/<topic>`,
  `ci/<topic>`, `refactor/<topic>`; prefix the milestone when attached: `feat/m3-service-list`.
- PRs are squash-merged; the merged commit title is the PR title. Delete the branch after merging.
- No merge without green CI (see `handbook/code-standards.md`, CI).

## Commits (Conventional Commits)

```
<type>(<scope>): <title>

<body: why, not what; optional; wrap at 72>

<footer: Closes #n · BREAKING CHANGE: … · Co-Authored-By: …>
```

| Type | For |
|---|---|
| `feat` | new feature |
| `fix` | bug fix |
| `design` | mockups, icons, design tokens |
| `docs` | docs (spec, design, ADR, README, handbook) |
| `refactor` | behaviour-preserving change |
| `test` | tests only |
| `perf` | performance |
| `build` | project config, dependencies, signing |
| `ci` | CI config |
| `chore` | everything else |

- Title: English, imperative verb first, at most 50 characters, no trailing period.
- Scopes are defined per repository in its `docs/process.md` and mirrored as labels.
- One commit does one thing and can be reverted alone. Formatting and logic go in separate commits.
- Check the staged file list before committing; never `git add -A` / `git commit -a` on a dirty tree.
- AI-assisted commits carry a `Co-Authored-By` line.

## Pull requests

Every PR uses the organization template: what, why, screenshots, how to verify, checklist, known
limitations. `Closes #n` in the description closes the issue on merge. Changes touching credentials,
Keychain, network calls that carry a credential, or launch agents record a security walkthrough in the
PR (see `handbook/security.md`).

## Issues, milestones, labels

- One GitHub Milestone per development milestone, with one **tracking issue** (label `milestone`) whose
  body holds goal, scope, acceptance checklist and progress. Tasks are sub-issues of it.
- Split tasks only at that milestone's spec step; earlier findings change later approaches.
- File an issue as soon as something comes up; nothing lives only in chat. Untested technical
  assumptions get `unverified`; items awaiting the maintainer get `needs-decision`; post-1.0 work goes
  to a "Later" milestone.
- Shared labels are defined in `labels.yml` at the root of this repository and applied with
  `scripts/sync-labels.sh`. Type labels match commit types; status labels are `milestone`,
  `needs-decision`, `unverified`. Scope labels are per repository and never pruned by the sync.

## ADR

Key decisions become `docs/adr/NNNN-title.md` (status, date, context, decision, cost) and are listed in
`docs/adr/README.md`. A reversed decision keeps its file; write a new one and mark the old
"superseded by NNNN".

## Definition of Done

- [ ] Every acceptance item of the milestone spec is met
- [ ] CI is green on the PR
- [ ] Design acceptance checklist fully ticked, with screenshots
- [ ] Related docs (spec, design, ADR, CHANGELOG) updated
- [ ] The maintainer accepted it by running it locally
