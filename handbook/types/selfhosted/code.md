# Code (self-hosted products)

Apply each section only to components shipped by this project. Its documented architecture and release
contract decide whether it uses a container, a native shell, an agent or a separate client.

The core, `shared/`, the web UI and services follow `handbook/stacks/typescript.md`; the macOS shell follows
`handbook/stacks/swift.md`; scripts follow `handbook/stacks/python.md`. This page adds what is specific to a
self-hosted product. Violations are bugs.

## Architecture

- **The image is the product.** Anything a Linux user also needs lives in the core or the web UI; the macOS shell
  owns only what is native to the Mac (`handbook/types/selfhosted/layout.md`).
- **`shared/` is the contract.** The schemas for every API message live there; the core and the web UI derive their
  types from them.
- **The core owns behaviour; the web UI owns presentation.** The web UI holds no rule the core does not also enforce:
  a check in the UI is a convenience, the check in the core is the rule.
- **Values from the user's host are untrusted until parsed**: files in the data directory, model responses and
  content read from websites go through the schemas like network input.
- **Fakes never ship**: the image build fails if a fake module is reachable from the core's entry point.
- **Multi-step work is resumable.** A task interrupted by a restart continues or fails cleanly at its last recorded
  step; nothing is half-applied.

## Container image

- One image per product, built from `image/Dockerfile` for `linux/arm64` and `linux/amd64`. Base images are pinned
  by digest; the Node.js major agrees with `.node-version`.
- Multi-stage: build tools never reach the final stage. The final stage holds the built core, the built web UI and
  the runtimes the product needs, nothing else.
- Runs as a non-root user with a fixed UID. The root filesystem is read-only; the data directory (`/data`) and a
  `tmpfs` are the only writable paths.
- `HEALTHCHECK` calls the core's health endpoint.
- No secret in any layer, build argument or label.
- The compose file drops all capabilities the product does not need, sets `no-new-privileges`, and never mounts the
  container runtime's socket.
- The compose file publishes the web port on `127.0.0.1` only; exposing it to the LAN is a documented, explicit
  change (`docs/hosting.md`).
- Image size and idle memory are budgets in `docs/hosting.md`; CI reports both on every image build.

## macOS shell

- Deployment target macOS 26.0 on Apple silicon unless an ADR says otherwise.
- The shell runs the image in a lightweight virtual machine through the system's virtualization support; it never
  requires Docker.
- Its own native screens (menu bar, notifications, window chrome) follow the Localization, Design and Accessibility
  rules of `handbook/types/app/code.md`. The window that shows the web UI adds no UI of its own inside the page.

## Web UI

- The UI framework is a product decision recorded in an ADR. Whatever it is, the rules below hold.
- One directory per screen (`web/src/screens/<screen>/`). `states.ts` in it lists every state the design shows, with
  fixture data; development builds render each at `/__states/<screen>/<state>`. Production builds do not contain
  that route or the fixtures.
- Raw values (colors, sizes, spacing, radii, durations, breakpoints) appear only in `web/src/design/tokens.css`.
  Components and screens use the tokens.
- Light and dark follow the system preference, with an override in Settings.
- Every screen works at each viewport the product declares in `docs/spec.md#information-architecture` (sizes in
  `docs/design.md`); a viewport not declared yet is neither designed nor built. When a touch viewport is declared,
  touch targets meet the minimum in `docs/design.md`.
- The web UI is an installable PWA. It loads nothing from third parties at runtime: no fonts, scripts, styles, images
  or analytics from other origins. The core sets a strict Content Security Policy.
- Entrance animations play on first appearance only; `prefers-reduced-motion` turns motion off.

## Localization

`handbook/guides/localization.md` covers languages, the English source and the rules. In code: user-visible text is the
English literal passed to `t("…")`, which is also the key in `web/src/i18n/<code>.json`.

## Accessibility

- Semantic elements first; every interactive element has an accessible name and is reachable by keyboard in a
  logical order.
- Every interactive element carries `data-testid="<screen>.<element>"`.
- The end-to-end suite runs an automated accessibility check (axe-core) on every state of every screen; any
  violation fails.

## Logging

- On top of the stack's rules: logs never contain page content, email bodies or screenshots.
- Rotation: the compose file sets the container log driver to 10 MB per file, three files. The macOS shell writes the
  container's output to its log directory with the rotation rules of `handbook/stacks/swift.md`.

## Tests

- Playwright end-to-end tests run against the built image started with `image/compose.yaml`: the first-run flow,
  every screen state, and the accessibility check.
- Data migrations are tested by upgrading a data directory written by every previous released version.

## CI

Every PR runs the shared `selfhosted-ci.yml` reusable workflow on GitHub-hosted Linux runners:

| Job | Does |
|---|---|
| check | the TypeScript stack's CI steps · `check-version.sh` · `check-docs.py` · `scan_secrets.py` |
| image | build the image for `linux/amd64` · report size · start it with compose · Playwright end-to-end and accessibility · image vulnerability scan |
| shell | `macos-ci.yml` on `macos/` (`handbook/stacks/swift.md`, CI), only when the PR changes `macos/` |

Pushes to `main` also build `linux/arm64`. The workflow is added to this repository together with the first
`selfhosted` code and is tested from that repository's branch before it is merged, like every reusable workflow.
