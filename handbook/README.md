# Handbook

Start with the mandatory core, then read only the guides, stacks and type preset that fit the project.
Project decisions specify actual components and may override presets; core security and maintainer approval remain mandatory.

## Every repository

| File | Covers |
|---|---|
| [core/process.md](core/process.md) | Collaboration, branches, commits, review and acceptance |
| [core/docs.md](core/docs.md) | Required documents, project sections and explicit version migrations |
| [core/agents.md](core/agents.md) | AI collaborators and maintainer authority |
| [core/security.md](core/security.md) | Credential protection, trust boundaries and external actions |

## Read when applicable

| Guide | Applies when |
|---|---|
| [guides/ui-workflow.md](guides/ui-workflow.md) | A product has interactive screens |
| [guides/localization.md](guides/localization.md) | A project translates UI or generated content |
| [guides/security.md](guides/security.md) | Runtime security, credentials, network services or publishing are involved |
| [guides/legal.md](guides/legal.md) | A commercial product uses the terms-of-service preset |
| [playbooks/](playbooks/add-feature.md) | Adding a feature or recording a decision |

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

Changing a rule: open a PR here, then migrate consumers in separate PRs with a pinned handbook revision.
Old root-level guide paths remain compatibility entry points, including their heading anchors.
