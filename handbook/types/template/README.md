# Repository type: template

## What it is

A GitHub template repository that new repositories of another type are created from. It carries that type's code,
documents and workflows in a form that builds from the first commit. `.repo-type` is `template`.

## Stacks

The stacks of the type it starts; `handbook/stacks/swift.md` for macOS apps, `handbook/stacks/go.md` for MyGo native apps,
and `handbook/stacks/python.md` for scripts.

## Pages

The pages of the type it starts (`handbook/types/app/README.md` or `handbook/types/mygo-app/README.md`), and [the handbook index](../../README.md).

## Templates

`handbook/templates/template/README.md` and the shared ones in `handbook/templates/common/`. The documents it hands
to a new product follow that product's type.

## Workflows

Those of the type it starts, and `docs-check.yml`.
