# Repository type: selfhosted

## What it is

A product the user runs on their own host: one container image with a web UI that every client uses, a native macOS
shell that runs the image on Macs, Docker Compose on Linux, and services the organization operates for the product
when it needs them. Closed source. `.repo-type` is `selfhosted`.

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

`handbook/templates/selfhosted/` (README, design language, milestone, third-party table, terms of service, hosting,
threat model) and the shared ones in `handbook/templates/common/`; `handbook/templates/manifest.json` maps each
required document to its template.

## Workflows

`selfhosted-ci.yml` and `selfhosted-release.yml` (added with the first code and the first release, see
`handbook/types/selfhosted/code.md` and `handbook/types/selfhosted/release.md`), `macos-ci.yml` for the shell,
`docs-check.yml`.
