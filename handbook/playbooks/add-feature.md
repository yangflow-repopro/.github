# Add a feature

The only way a feature starts. Do not write code first.

## Before you start

- The idea is an issue (type `feat`); if it needs the maintainer's call, label it `needs-decision`.

## Steps

1. Put the feature in the iteration: edit `docs/milestones/next.md` (Goal, Scope, Non-goals, Decisions,
   Acceptance checklist). Link the existing document that owns the requirement: a spec for a product or pipeline,
   a library design document, website content/design, or an organization rule. Update that document first when
   behavior changes. Do not create an otherwise unused spec solely to satisfy this playbook.
2. If it has interactive product UI: describe it in the project's spec with its screen and follow the add-screen
   playbook where the type has one; otherwise follow `handbook/guides/ui-workflow.md`: design, maintainer
   sign-off, code, device acceptance. No UI code before sign-off; no merge of UI code
   before the maintainer has accepted the screen on a device. Update the ledger in `design/README.md` in the
   same PR.
3. If it changes an established way of working: write the ADR (`handbook/playbooks/write-adr.md`).
4. Implement in small PRs on a `feat/<topic>` branch. If the change has translated copy, follow the project's
   localization rules. Static websites use their type's design and preview checks. Each PR says what, why and
   how to verify, with screenshots for UI changes.
5. If the repository declares a changelog, add its user-facing line under `## [Unreleased]`; update the
   translated changelog only when the project requires it. Pipelines record rollout and rollback instead.

## Files this touches

`docs/milestones/next.md`, the project's requirement document, `design/screens/`, `design/README.md` (ledger), code and tests, `CHANGELOG.md`,
`CHANGELOG.zh.md`, maybe `docs/adr/`.

## Check yourself

`python3 <org>/scripts/check-docs.py .` and the repository's CI commands (`AGENTS.md`, Commands).
