# Swift

Applies to every Swift code base in the organization, whatever the repository type. A type's
`handbook/types/<type>/code.md` adds the platform, architecture and UI rules on top. Violations are bugs.

## Toolchain

| Setting | Value |
|---|---|
| Xcode | Current release (CI main job); previous major in the compatibility job |
| Swift language mode | `SWIFT_VERSION = 6.0` (strict concurrency), `SWIFT_TREAT_WARNINGS_AS_ERRORS = YES` |
| Project definition | XcodeGen `project.yml`; the generated `.xcodeproj` is committed; CI fails if regenerating changes it |
| Dependencies | SwiftPM only; `Package.resolved` is committed and matches `THIRD_PARTY.md` (`check-docs.py`) |
| Formatting | `xcrun swift-format` (the copy bundled with Xcode) with the shared `.swift-format`, identical in every repository; CI runs `lint --strict` |

## Concurrency

- The app target is `MainActor`-isolated by default (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`). A local package
  sets `defaultIsolation(MainActor.self)` when it is mostly main-actor services; a package that is mostly `Sendable`
  value types and background engines leaves the default and annotates `@MainActor` explicitly. Record the choice in
  an ADR.
- Domain value types are `nonisolated` so engines can read them from any execution domain.
- A MainActor-isolated protocol cannot be implemented by an actor; test doubles are `final class`.
- Multi-step remote operations are idempotent; each flow is tested for success, mid-way failure and retry.

## Errors

- Never force-unwrap user input; throw typed errors.
- User-facing error messages are localizable and say what happened and what to do.

## Logging

- One implementation per log kind. App log: one entry per line, `ISO8601 [level] category: message`, 1 MB rotation,
  two rotated files kept, entries older than 7 days removed at launch.
- Logs never contain credentials; outputs that may carry them pass through the redactor first.

## Tests

- Swift Testing (`@Test`, `#expect`). Service-level code covers at least the happy path and one error path. Test
  doubles are `private` to the test file; mocks are not shared across test files.
- No XCUITest. UI quality relies on all-state previews, screenshots on every UI PR and the maintainer's acceptance
  (`handbook/ui-workflow.md`).
- Tests run with `-testLanguage en -testRegion US`; assert English text or pass an explicit locale.
- Live integration tests are opt-in through environment variables and skipped in CI.
- Tests that need real sockets, a local HTTP server or WebKit carry
  `.enabled(if: !TestEnvironment.isCompatibilityRun)`: the compatibility job sets `COMPAT_RUN=1`
  (`TEST_RUNNER_COMPAT_RUN` on the xcodebuild command) because the hosted macOS 26 image is unreliable for them. The
  main job runs everything. Timing assertions leave headroom for a loaded machine: prove "did not wait for the
  limit" with a generous limit, not with a tight wall-clock bound.

## CI

Swift code is built and tested by the shared `macos-ci.yml` reusable workflow:

| Job | Runner | Does |
|---|---|---|
| main | GitHub-hosted `xcode-27` (current Xcode) | `xcodegen generate` + no diff · `swift-format lint --strict` · build (Release) · test |
| compat | GitHub-hosted `macos-26`, previous Xcode | build (Release) · test; runs on push to `main` only |

The compatibility job exists to catch APIs that are newer than the deployment target. All jobs run on GitHub-hosted
runners; macOS minutes on private repositories are billed at 10×, so the compatibility job is limited to pushes to
`main`.
