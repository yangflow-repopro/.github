# Repository type: selfhosted

This is the self-hosted service documentation preset. Select only the stacks and components the project uses;
record its actual architecture and preset differences in its agent instructions and process document.

## What it is

A service the user runs on their own host. The current preset uses a container image and web UI; native shells,
agents and hosted support services are optional and may live in separate repositories. `.repo-type` is `selfhosted`.

## Stacks

`handbook/stacks/typescript.md` for the core, `shared/`, the web UI and services; `handbook/stacks/swift.md` for the
macOS shell; `handbook/stacks/python.md` for scripts.

## Pages

| Page | Covers |
|---|---|
| [layout.md](layout.md) | Directory tree, one version, module boundaries |
| [code.md](code.md) | Architecture, container image, macOS shell, web UI, localization, accessibility, logging, tests, CI |
| [release.md](release.md) | Image and app artifacts, pipeline, updates and migrations, launch checklist |
| [playbooks/](playbooks/add-screen.md) | Add a screen, a string, a language; bump a dependency; release |

The pages every repository follows are listed in [the handbook index](../../README.md).

## Templates

`handbook/templates/selfhosted/` (README, architecture, design language, milestone, third-party table, terms of
service, hosting, threat model) and the shared ones in `handbook/templates/common/`; `handbook/templates/manifest.json` maps each
required document to its template.

## Workflows

Projects provide their own service CI and release workflows. Shared `selfhosted-ci.yml` and
`selfhosted-release.yml` are not provided yet; see the CI expectations in `handbook/types/selfhosted/code.md`
and the release contract in `handbook/types/selfhosted/release.md`. `macos-ci.yml` applies to a shipped Swift
shell; `docs-check.yml` checks the declared documents.
