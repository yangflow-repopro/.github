# Repository type: pipeline

## What it is

An automated pipeline the maintainer operates: a TypeScript command-line tool and the GitHub workflows that run it. It
reads from other repositories and external services and writes files or calls external services with the
maintainer's accounts. It has no UI of its own and is not distributed to users. Private. `.repo-type` is `pipeline`.

## Stacks

`handbook/stacks/typescript.md` for the packages and the command-line tool; `handbook/stacks/python.md` for the scripts
(the secret scan).

## Pages

| Page | Covers |
|---|---|
| [layout.md](layout.md) | Directory tree, module boundaries, exact versions |
| [code.md](code.md) | Architecture, side effects, untrusted content, secrets, command-line conventions, logging, tests, CI |
| [release.md](release.md) | No versions: what a merge to `main` means, rollout, rollback |
| [playbooks/](playbooks/bump-dependency.md) | Bump a dependency |

The pages every repository follows are listed in [the handbook index](../../README.md). A pipeline has no UI, so
`handbook/ui-workflow.md` does not apply and the repository has no `design/` and no `docs/design.md`.

## Templates

`handbook/templates/pipeline/` (README, spec, operations, threat model, milestone, third-party table) and the shared
ones in `handbook/templates/common/`; `handbook/templates/manifest.json` maps each required document to its template.

## Workflows

`pipeline-ci.yml` (added with the first pipeline code, see `handbook/types/pipeline/code.md`, CI) and
`docs-check.yml`. The pipeline's own workflows (one per trigger) are described in its `docs/operations.md`.
