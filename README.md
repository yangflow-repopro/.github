<!-- template: org/README.md v1 -->
# .github

Organization-wide defaults for yangflow-repopro.

## Contents

| Path | Purpose |
|---|---|
| `handbook/` | Mandatory `core/`, conditional `guides/`, language `stacks/` and repository `types/` |
| `handbook/templates/` | Templates for every kind of document, and `manifest.json` (which repository type needs which) |
| `.github/workflows/` | Reusable workflows for macOS, MyGo, websites, pipelines and document checks |
| `pull_request_template.md`, `ISSUE_TEMPLATE/` | Defaults for every repository that has none of its own |
| `SECURITY.md` | Vulnerability reporting |
| `labels.yml`, `scripts/sync-labels.sh` | Shared labels and the script that applies them |
| `scripts/check-docs.py` | Checks a repository's documents against the templates |
| `profile/README.md` | Organization profile |

## Visibility

This repository is public so GitHub applies the defaults to private repositories. It never contains product
code, credentials, internal hostnames or product names; examples use `<Name>` and `<domain>`.
