# Add a feature

The only way a feature starts. Do not write code first.

## Before you start

- The idea is an issue (type `feat`); if it needs the maintainer's call, label it `needs-decision`.

## Steps

1. Put the feature in the iteration: edit `docs/milestones/next.md` (Goal, Scope, Non-goals, Decisions,
   Acceptance checklist). If it changes what the product is, edit `docs/spec.md` first.
2. If it has UI: add or change `design/screens/<screen>.html` (all states, light and dark) and get it signed
   off. No UI code before sign-off. See `add-screen.md`.
3. If it changes an established way of working: write the ADR (`write-adr.md`).
4. Implement in small PRs on a `feat/<topic>` branch. Strings follow `add-string.md`. Each PR description
   says what, why, how to verify, and carries screenshots for UI.
5. Add the user-facing line under `## [Unreleased]` in `CHANGELOG.md` (and `CHANGELOG.zh.md`).

## Files this touches

`docs/milestones/next.md`, maybe `docs/spec.md`, `design/screens/`, code and tests, `CHANGELOG.md`,
`CHANGELOG.zh.md`, maybe `docs/adr/`.

## Check yourself

`python3 <org>/scripts/check-docs.py .` and the repository's CI commands (`AGENTS.md`, Commands).
