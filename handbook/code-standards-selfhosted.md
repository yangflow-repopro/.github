# Code standards (self-hosted products)

Applies to every `selfhosted` repository. The macOS shell under `macos/` follows `code-standards.md` (macOS apps)
in full; everything else follows this file. Violations are bugs.

## Toolchain

| Setting | Value |
|---|---|
| Runtime | Node.js, the current Active LTS major; pinned in `.node-version` and in the image's base, which must agree |
| Package manager | pnpm workspace; version pinned in the root `package.json` `packageManager` field; `pnpm install --frozen-lockfile` everywhere |
| Language | TypeScript, ES modules only. `tsconfig.base.json`: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax` |
| Formatting and lint | Biome with the shared `biome.json`, identical in every `selfhosted` repository; CI runs `biome ci`. Warnings are errors |
| Type check | `tsc --noEmit` per package; CI fails on any error |
| Dependencies | Exact versions only; `pnpm-lock.yaml` committed; every dependency in `THIRD_PARTY.md` |
| Licenses | Shipped dependencies are MIT, BSD, ISC, Apache-2.0 or MPL-2.0. Anything else needs an ADR |

## Architecture

- **Boundaries are validated.** Every value that enters a process from outside (HTTP and WebSocket messages,
  environment variables, files in the data directory, model responses, content read from websites) is parsed by a
  schema before use. Types come from the schemas in `shared/`; there is no hand-written duplicate type.
- **The core owns behaviour; the web UI owns presentation.** The web UI holds no rule the core does not also
  enforce: a check in the UI is a convenience, the check in the core is the rule.
- **Every external client has an interface and two implementations**: the live one and a fake for tests. Fakes live
  under `test/` and never ship; the image build fails if a fake module is reachable from the core's entry point.
- **Errors are typed.** A thrown error carries a stable `code`. The web UI turns codes into localized copy; the
  core never sends user-facing sentences.
- **Multi-step work is resumable.** A task interrupted by a restart continues or fails cleanly at its last
  recorded step; nothing is half-applied.
- **Time is UTC** in storage and logs (ISO 8601); local time only in the UI.
- No `any`, no non-null assertion on values that came from outside, no floating promises (Biome rules).

## Container image

- One image per product, built from `image/Dockerfile` for `linux/arm64` and `linux/amd64`. Base images are pinned
  by digest.
- Multi-stage: build tools never reach the final stage. The final stage holds the built core, the built web UI and
  the runtimes the product needs, nothing else.
- Runs as a non-root user with a fixed UID. The root filesystem is read-only; the data directory (`/data`) and a
  `tmpfs` are the only writable paths.
- `HEALTHCHECK` calls the core's health endpoint.
- No secret in any layer, build argument or label.
- The compose file drops all capabilities the product does not need, sets `no-new-privileges`, and never mounts
  the container runtime's socket.
- The compose file publishes the web port on `127.0.0.1` only; exposing it to the LAN is a documented, explicit
  change (`docs/hosting.md`).
- Image size and idle memory are budgets in `docs/hosting.md`; CI reports both on every image build.

## Web UI

- The UI framework is a product decision recorded in an ADR. Whatever it is, the rules below hold.
- One directory per screen (`web/src/screens/<screen>/`). `states.ts` in it lists every state the design shows,
  with fixture data; development builds render each at `/__states/<screen>/<state>`. Production builds do not
  contain that route or the fixtures.
- Raw values (colors, sizes, spacing, radii, durations, breakpoints) appear only in `web/src/design/tokens.css`.
  Components and screens use the tokens.
- Light and dark follow the system preference, with an override in Settings.
- Every screen works at the phone and desktop viewports defined in `docs/design.md`; touch targets meet its
  minimum.
- The web UI is an installable PWA. It loads nothing from third parties at runtime: no fonts, scripts, styles,
  images or analytics from other origins. The core sets a strict Content Security Policy.
- Entrance animations play on first appearance only; `prefers-reduced-motion` turns motion off.

## Localization

`localization.md` covers languages, the English source and the rules. In code: user-visible text is the English
literal passed to `t("…")`, which is also the key in `web/src/i18n/<code>.json`.

## Accessibility

- Semantic elements first; every interactive element has an accessible name and is reachable by keyboard in a
  logical order.
- Every interactive element carries `data-testid="<screen>.<element>"`.
- The end-to-end suite runs an automated accessibility check (axe-core) on every state of every screen; any
  violation fails.

## Logging

- The core writes one JSON object per line to standard output: `time` (ISO 8601 UTC), `level`, `module`, `message`
  and structured fields. Nothing else writes to standard output.
- Logs never contain credentials, cookies, session tokens, page content, email bodies or screenshots. Values that
  may carry them pass through the redactor first; a test feeds known secrets through every log path.
- Rotation: the compose file sets the container log driver to 10 MB per file, three files. The macOS shell writes
  the container's output to its log directory with the rotation rules of `code-standards.md`.

## Tests

- Vitest for `core`, `shared`, `web` and services. Service-level code covers at least the happy path and one error
  path. Fakes are local to the test that uses them unless they implement an interface from `shared/`.
- Playwright end-to-end tests run against the built image started with `image/compose.yaml`: the first-run flow,
  every screen state, and the accessibility check.
- Data migrations are tested by upgrading a data directory written by every previous released version.
- Live tests (a real model provider, real websites) are opt-in through environment variables and never run in CI.
  Fixtures never contain real credentials, cookies or personal data.

## CI

Every PR runs the shared `selfhosted-ci.yml` reusable workflow on GitHub-hosted Linux runners:

| Job | Does |
|---|---|
| check | `pnpm install --frozen-lockfile` · `biome ci` · `tsc --noEmit` · Vitest · `check-version.sh` · `check-docs.py` · `scan_secrets.py` |
| image | build the image for `linux/amd64` · report size · start it with compose · Playwright end-to-end and accessibility · image vulnerability scan |
| shell | `macos-ci.yml` on `macos/`, only when the PR changes `macos/` (macOS minutes are billed at 10×) |

Pushes to `main` also build `linux/arm64`. The workflow is added to this repository together with the first
`selfhosted` code and is tested from that repository's branch before it is merged, like every reusable workflow.
