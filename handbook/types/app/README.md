# Repository type: app

## What it is

A native macOS app, closed source, distributed as a notarized download from its website and updated in-app with
Sparkle. `.repo-type` is `app`.

## Stacks

`handbook/stacks/swift.md` for the app and its Core package; `handbook/stacks/python.md` for its scripts.

## Pages

| Page | Covers |
|---|---|
| [layout.md](layout.md) | Directory tree and file set |
| [code.md](code.md) | Platform, architecture, localization, design, accessibility |
| [captures.md](captures.md) | How device captures are made; what counts as acceptance evidence |
| [release.md](release.md) | Versions, tags, changelog, release pipeline, launch checklist |
| [playbooks/](playbooks/add-screen.md) | Add a screen, a string, a language; bump a dependency; release |

The pages every repository follows are listed in [the handbook index](../../README.md).

## Templates

`handbook/templates/app/` (README, design language, third-party table, terms of service) and the shared ones in
`handbook/templates/common/`; `handbook/templates/manifest.json` maps each required document to its template.

## Workflows

`macos-ci.yml` (`handbook/stacks/swift.md`, CI), `macos-release.yml` (`handbook/types/app/release.md`),
`docs-check.yml`.
