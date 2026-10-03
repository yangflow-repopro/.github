# .github

Organization-wide defaults for yangflow-repopro.

| Path | Purpose |
|---|---|
| `handbook/` | How projects are built and shipped; product repositories link here |
| `.github/workflows/` | Reusable workflows: `macos-ci.yml`, `site-ci.yml` (release workflow follows) |
| `pull_request_template.md`, `ISSUE_TEMPLATE/` | Defaults for every repository that has none of its own |
| `SECURITY.md` | Vulnerability reporting |
| `labels.yml`, `scripts/sync-labels.sh` | Shared labels and the script that applies them |
| `profile/README.md` | Organization profile |

This repository is public so GitHub applies the defaults to private repositories. It never contains
product code, credentials or internal hostnames.
