# Security

## Red lines

- Never write a token, API key, customer license key or any other credential into a PR, issue, log,
  report, chat or other external channel; refer to it by file path and line.
- Sending anything to an external service needs the maintainer's confirmation each time.
- Never modify a user's dotfiles or global Git configuration.
- Never tell the maintainer a project is "secure" or "risk-free" without a complete scan or walkthrough.
  If a scan is incomplete or has unresolved findings, report that faithfully; the PR does not merge.

## Walkthroughs

Changes that touch credentials, Keychain, network requests that carry a credential, launch agents or
code signing get a manual security walkthrough before merging. The conclusion is recorded in the PR
description. Each app keeps a `docs/milestones/<release>-security.md` with the pre-release walkthrough.

## Tooling

- `scripts/scan_secrets.py` scans the whole git history, or a built app with `--path`, for
  credential-like strings and prints redacted findings. It runs before every release and in CI.
- `scripts/release.sh` scans the built app for credential-like strings, build-machine paths and debug
  entitlements and refuses to ship them.
- Credentials used by the app are stored in the user's Keychain only, never in preferences or files.
  Secrets in subprocess output are redacted before they reach logs.

## Reporting

See `SECURITY.md` at the root of this repository.
