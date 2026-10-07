# Handbook

The single source of truth for how yangflow-repopro projects are built and shipped. Product repositories link here
and record only their differences. It has three layers: rules every repository follows, rules per language, and rules
per repository type.

## Every repository

| File | Covers |
|---|---|
| [process.md](process.md) | Roles, milestones, branches, commits, PRs, issues, labels, Definition of Done |
| [docs.md](docs.md) | The documentation system: map, repository types, rules, names, lifecycle |
| [agents.md](agents.md) | Working rules for AI collaborators |
| [ui-workflow.md](ui-workflow.md) | Screen lifecycle, gates, ledger, `design/` whitelist, review tool, merge rule |
| [localization.md](localization.md) | Languages, adding a string, adding a language |
| [security.md](security.md) | Red lines, walkthroughs, scanning |
| [legal.md](legal.md) | Legal pages: one source per fact, skeletons, fixed wording |
| [playbooks/](playbooks/add-feature.md) | Add a feature, write an ADR |

## Languages

| File | Covers |
|---|---|
| [stacks/go.md](stacks/go.md) | Toolchain, code, tests and CI for Go |
| [stacks/swift.md](stacks/swift.md) | Toolchain, concurrency, errors, logging, tests, CI for Swift |
| [stacks/typescript.md](stacks/typescript.md) | Toolchain, code, logging, tests for TypeScript |
| [stacks/python.md](stacks/python.md) | Toolchain, scripts, tests for Python |

## Repository types

Each type has a directory with the same index (`README.md`: what it is, stacks, pages, templates, workflows).

| Type | Index |
|---|---|
| `mygo-app` | [types/mygo-app/](types/mygo-app/README.md) |
| `app` | [types/app/](types/app/README.md) |
| `selfhosted` | [types/selfhosted/](types/selfhosted/README.md) |
| `pipeline` | [types/pipeline/](types/pipeline/README.md) |
| `website` | [types/website/](types/website/README.md) |
| `library` | [types/library/](types/library/README.md) |
| `template` | [types/template/](types/template/README.md) |
| `org` | [types/org/](types/org/README.md) |

## Templates

[templates/](templates/manifest.json): `common/` for documents every type shares, one directory per type for the
rest; `manifest.json` says which repository type needs which document from which template.

Changing a rule: open a PR here, link it from the product PR that needs it.
