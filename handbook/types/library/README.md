# Repository type: library

This is the shared library or tool documentation preset. Select only the stacks and components the project uses;
record its actual architecture and preset differences in its agent instructions and process document.

## What it is

Shared code or tooling other repositories use, for example a generator vendored into product repositories.
`.repo-type` is `library`.

## Stacks

The stack of its code, named in its `AGENTS.md` (for example `handbook/stacks/python.md`).

## Pages

None beyond the pages every repository follows ([the handbook index](../../README.md)). A library's `AGENTS.md`
says how a change reaches the repositories that use it.

## Templates

`handbook/templates/library/` (README, design) and the shared ones in `handbook/templates/common/`.

## Workflows

`docs-check.yml`.
