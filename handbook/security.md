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

## Self-hosted products

A `selfhosted` product runs a server on the user's host, holds the user's credentials and sessions, and may be
reachable from the network. On top of the rules above:

- **Threat model.** `docs/threat-model.md` lists assets, trust boundaries and each threat with its mitigation and
  how it is verified. A change that adds a boundary (a new port, a hosted service, a new kind of content the product
  reads) updates it in the same PR. Each release's walkthrough checks every row.
- **No unauthenticated mode.** Every API request and WebSocket is authenticated, including from localhost; the macOS
  shell passes its token to the web view. Requests are checked for origin; the core sets a strict Content Security
  Policy.
- **Network exposure is opt-in.** The image's port is published on `127.0.0.1` by default; LAN or internet exposure
  is a documented change in `docs/hosting.md`.
- **Secrets at rest.** On a Mac host, credentials live in the Keychain and reach the core at start. On a Linux host,
  they live in a file in the data directory readable only by the core's user. They never appear in environment
  variables baked into the image, in the web UI in clear text after entry, or in logs.
- **Container hardening** as in `handbook/types/selfhosted/code.md`: non-root, read-only root filesystem, dropped
  capabilities, `no-new-privileges`, never the container runtime's socket.
- **Supply chain.** Base images pinned by digest, exact dependency versions, a committed lockfile, an image
  vulnerability scan in CI and at release, an SBOM and a signature on every released image.
- **Hosted services** the product depends on never receive user content in clear text; a walkthrough covers their
  key handling before the first release.
- `scripts/scan_secrets.py` also runs on the image's exported filesystem before every release.

## Pipelines

A `pipeline` product acts with the maintainer's accounts and may publish or spend without a person watching. On top
of the rules above:

- **Threat model.** `docs/threat-model.md` lists assets, trust boundaries and each threat with its mitigation and how
  it is verified. A change that adds a boundary (a new outside service, a new account, a new kind of content read)
  updates it in the same PR.
- **No outward action without a recorded approval** in the repository, set by a person or by a policy written in an
  ADR (`handbook/types/pipeline/code.md`, Side effects). A new channel or account needs the maintainer's confirmation.
- **Untrusted content is data.** Content from other repositories, websites and models never reaches a shell, a workflow
  expression or a model call that holds a credential.
- **Least privilege.** Each secret belongs to the environment or job that needs it; workflows start from
  `contents: read`; third-party actions are pinned by commit; dependencies are exact, locked, and their install scripts
  are off unless listed.
- **A way to stop.** `docs/operations.md` names the switch that halts every outward action and says how it was tested.
- `scripts/scan_secrets.py` runs in CI.

## Reporting

See `SECURITY.md` at the root of this repository.
