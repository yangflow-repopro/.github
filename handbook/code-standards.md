# Code standards (macOS apps)

Applies to every Swift app in the organization. Violations are bugs.

## Toolchain

| Setting | Value |
|---|---|
| Xcode | Current release (CI main job); previous major in the compatibility job |
| Swift language mode | `SWIFT_VERSION = 6.0` (strict concurrency), `SWIFT_TREAT_WARNINGS_AS_ERRORS = YES` |
| Deployment target | macOS 26.0 unless an ADR says otherwise |
| Project definition | XcodeGen `project.yml`; the generated `.xcodeproj` is committed; CI fails if regenerating changes it |
| Dependencies | SwiftPM only; `Package.resolved` is committed |
| Formatting | `xcrun swift-format` (the copy bundled with Xcode) with the shared `.swift-format`; CI runs `lint --strict` |

## Concurrency

- The app target is `MainActor`-isolated by default (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`); the
  Core package sets `defaultIsolation(MainActor.self)`.
- Domain value types are `nonisolated` so engines can read them from any execution domain.
- A MainActor-isolated protocol cannot be implemented by an actor; test doubles are `final class`.
- Multi-step remote operations are idempotent; each flow is tested for success, mid-way failure and
  retry.

## Architecture

- `View → Model/Coordinator → protocol`. Views depend only on observable models; models depend only on
  protocols. Every external client (API, license, store) has a Live and a Mock implementation.
- Shared logic lives in the Core package with an explicit `public` API; the app target holds UI and
  macOS-specific system services only. See `handbook/repo-layout.md`.
- Mock, in-memory and preview-only code never ships: it lives in a test-support product or behind
  `#if DEBUG`. The release script fails if such symbols are found in the built app.
- Never force-unwrap user input; throw typed errors; user-facing error messages are localizable and
  say what happened and what to do.

## Localization

- User-visible text is an English literal that is also the String Catalog key:
  `String.loc("Publish")`. Translations live in `Resources/Localizable.xcstrings`.
- UI languages: en (source), zh-Hans, zh-Hant, ja, ko, fr, de, es, pt-BR; switchable in Settings and
  applied without restart. Every key carries every language; unit tests enforce it.
- Language boundary: everything that is not UI copy (logs, diagnostics, developer error summaries,
  exported files, script output, comments) is English and is not in the catalog.
- Tests run with `-testLanguage en -testRegion US`; assert English text or pass an explicit locale.
- UI copy keeps one necessary sentence and never uses infrastructure terms the user did not choose.

## Design

- Colors, spacing, radii, motion and window sizes come from the design tokens in Core; no magic
  numbers in views.
- Every SwiftUI view has a `#Preview` covering all its states; previews are part of design acceptance.
- Glass materials are for the navigation layer only and are never stacked.
- Entrance animations play on first appearance only, never on redraw.

## Accessibility

- Every interactive element has an `accessibilityIdentifier` named `<screen>.<element>` and a label
  VoiceOver can read; decorative elements use `accessibilityHidden(true)`.
- `scripts/ax-audit.swift` flags unnamed controls and untranslated text in the running app.

## Logging

- One implementation per log kind. App log: one entry per line, `ISO8601 [level] category: message`,
  1 MB rotation, two rotated files kept, entries older than 7 days removed at launch.
- Logs never contain credentials; outputs that may carry them pass through the redactor first.

## Tests

- Swift Testing (`@Test`, `#expect`). Service-level code covers at least the happy path and one error
  path. Test doubles are `private` to the test file; mocks are not shared across test files.
- No XCUITest. UI quality relies on all-state previews, screenshots on every UI PR and the
  maintainer's manual acceptance.
- Live integration tests are opt-in through environment variables and skipped in CI.
- Tests that need real sockets, a local HTTP server or WebKit carry
  `.enabled(if: !TestEnvironment.isCompatibilityRun)`: the compatibility job sets `COMPAT_RUN=1`
  (`TEST_RUNNER_COMPAT_RUN` on the xcodebuild command) because the hosted macOS 26 image is unreliable
  for them. The main job runs everything. Timing assertions leave headroom for a loaded machine: prove
  "did not wait for the limit" with a generous limit, not with a tight wall-clock bound.

## CI

Every PR runs the shared `macos-ci.yml` reusable workflow:

| Job | Runner | Does |
|---|---|---|
| main | GitHub-hosted `xcode-27` (current Xcode) | `xcodegen generate` + no diff · `swift-format lint --strict` · build (Release) · test |
| compat | GitHub-hosted `macos-26`, previous Xcode | build (Release) · test; runs on push to `main` only |

The compatibility job exists to catch APIs that are newer than the deployment target.

All jobs run on GitHub-hosted runners; there are no self-hosted machines. macOS minutes on private
repositories are billed at 10×, so the compatibility job is limited to pushes to `main`.
