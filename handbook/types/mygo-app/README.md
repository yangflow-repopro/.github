# Repository type: mygo-app

## What it is

A closed-source desktop app written in Go with MyGo native UI. There is no HTML frontend,
JavaScript runtime, WebView or Xcode project. `.repo-type` is `mygo-app`.

## Stacks

[Go](../../stacks/go.md) for the app and module-pinned CLI; [Python](../../stacks/python.md) for scripts.

## Pages

| Page | Covers |
|---|---|
| [layout.md](layout.md) | Module layout, configuration and initialization |
| [code.md](code.md) | Native views, state, localization and test evidence |
| [release.md](release.md) | Packaging, signing and native updates |

The common rules are in [the handbook index](../../README.md).

## Templates

`handbook/templates/mygo-app/` supplies the README, dependency table and terms of service.
The shared document sections and design language skeleton are mapped in
`handbook/templates/manifest.json`. Products fill every required section.

## Workflows

`mygo-ci.yml` and `docs-check.yml`. Packaging produces local or CI artifacts; publishing
and credentials are configured per product after maintainer approval.
Pin callers to one organization commit and pass that same SHA as `handbook-ref` to the docs workflow.
