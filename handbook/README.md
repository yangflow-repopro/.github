# Handbook

The single source of truth for how yangflow-repopro projects are built and shipped. Product
repositories link here and record only their differences.

| File | Covers |
|---|---|
| [process.md](process.md) | Roles, milestones, branches, commits, PRs, issues, labels, Definition of Done |
| [code-standards.md](code-standards.md) | macOS apps: toolchain, concurrency, architecture, localization, design, accessibility, tests, CI |
| [code-standards-selfhosted.md](code-standards-selfhosted.md) | Self-hosted products: toolchain, architecture, container image, web UI, accessibility, logging, tests, CI |
| [repo-layout.md](repo-layout.md) | Standard directory tree and file set for an app repository |
| [repo-layout-selfhosted.md](repo-layout-selfhosted.md) | Standard directory tree and file set for a self-hosted product |
| [release.md](release.md) | macOS apps: versions, tags, changelog, release pipeline, launch checklist |
| [release-selfhosted.md](release-selfhosted.md) | Self-hosted products: one version, image and app artifacts, pipeline, updates, launch checklist |
| [security.md](security.md) | Red lines, walkthroughs, scanning |
| [website.md](website.md) | Static websites: generator, rules, checks, deploy |
| [docs.md](docs.md) | The documentation system: map, rules, names, lifecycle |
| [ui-workflow.md](ui-workflow.md) | Screen lifecycle, gates, ledger, `design/` whitelist, review tool, merge rule |
| [localization.md](localization.md) | Languages, adding a string, adding a language |
| [legal.md](legal.md) | Legal pages: one source per fact, skeletons, fixed wording |
| [agents.md](agents.md) | Working rules for AI collaborators |
| [playbooks/](playbooks/add-feature.md) | Step lists: feature, screen, string, language, ADR, release, dependency |
| [templates/](templates/manifest.json) | Templates for every document and which repository type needs which |

Changing a rule: open a PR here, link it from the product PR that needs it.
