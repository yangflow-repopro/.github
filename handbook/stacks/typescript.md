# TypeScript

Applies to every TypeScript code base in the organization, whatever the repository type: servers, web UIs, tools and
services. A type's `handbook/types/<type>/code.md` adds its architecture, platform and UI rules on top.
Violations are bugs.

## Toolchain

| Setting | Value |
|---|---|
| Runtime | Node.js, the current Active LTS major, pinned in `.node-version`; anything else that names a Node.js version (a container base image, a CI setup step) must agree with it |
| Package manager | pnpm workspace; version pinned in the root `package.json` `packageManager` field; `pnpm install --frozen-lockfile` everywhere |
| Language | TypeScript, ES modules only. `tsconfig.base.json`: `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `verbatimModuleSyntax` |
| Formatting and lint | Biome, exact version in the root `package.json`; `biome.json` is a copy of `handbook/stacks/biome.json`, identical in every TypeScript repository; CI runs `biome ci --error-on-warnings`. Raising the Biome version updates that file first |
| Type check | `tsc --noEmit` per package; CI fails on any error |
| Dependencies | Exact versions only; `pnpm-lock.yaml` committed; every dependency in `THIRD_PARTY.md` (`check-docs.py` compares them and fails on a range) |
| Licenses | Shipped dependencies are MIT, BSD, ISC, Apache-2.0 or MPL-2.0. Anything else needs an ADR |

## Code

- **Boundaries are validated.** Every value that enters a process from outside (network messages, environment
  variables, files, responses from other services, content read from the web) is parsed by a schema before use. Types
  are derived from the schemas; there is no hand-written duplicate type.
- **Errors are typed.** A thrown error carries a stable `code`. User-facing copy is chosen from the code by the UI,
  never sent as a sentence from a server.
- **Every external client has an interface and two implementations**: the live one and a fake for tests. Fakes live
  under `test/` and never ship.
- **Time is UTC** in storage and logs (ISO 8601); local time only in a UI.
- No `any`, no non-null assertion on values that came from outside, no floating promises (Biome rules).

## Logging

- A server writes one JSON object per line to standard output: `time` (ISO 8601 UTC), `level`, `module`, `message`
  and structured fields. Nothing else writes to standard output.
- Logs never contain credentials, cookies or session tokens. Values that may carry them pass through the redactor
  first; a test feeds known secrets through every log path.

## Tests

- Vitest for every package. Service-level code covers at least the happy path and one error path. Fakes are local to
  the test that uses them unless they implement a shared interface.
- Live tests (real third-party services) are opt-in through environment variables and never run in CI. Fixtures
  never contain real credentials, cookies or personal data.
- In CI: `pnpm install --frozen-lockfile` · `biome ci` · `tsc --noEmit` · Vitest. A type's
  `handbook/types/<type>/code.md` adds its own jobs.
