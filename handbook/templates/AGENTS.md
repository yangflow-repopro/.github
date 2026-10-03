<!-- template: AGENTS.md v1 -->
<!-- AGENTS.md for any repository. Six H2s in this order. Each section ends with a link to the handbook where one exists; do not restate the handbook. -->
# AGENTS.md

## What it is

<Two or three sentences: product, platform, stack, how it is distributed.>

## Sources of truth

<Which document answers what: spec, design, legal, ADRs. Docs win over code. Link `docs/...#anchor`.>

How we work: the organization handbook (`https://github.com/yangflow-repopro/.github/tree/main/handbook`);
rules for AI collaborators: `handbook/agents.md`.

## Directory boundaries

<The tree, one line per directory, and the dependency rule between layers. Link `handbook/repo-layout.md`.>

## Commands

<The exact commands CI runs: generate, lint, build, test, bump, release check.>

## Project rules

<Only what is specific to this repository; each rule one or two lines. Link the handbook for the rest.>

## Red lines

Credentials never appear in PRs, issues, logs, reports or chat. Signing, release and anything sent to an
external service need the maintainer's confirmation. No blind staging. See `handbook/agents.md`.
