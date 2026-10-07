# Code (macOS apps)

An app follows `handbook/stacks/swift.md` and `handbook/stacks/python.md` (its scripts). This page adds what is
specific to a macOS app. Violations are bugs.

## Platform

Deployment target macOS 26.0 unless an ADR says otherwise.

## Architecture

- `View → Model/Coordinator → protocol`. Views depend only on observable models; models depend only on protocols.
  Every external client (API, license, store) has a Live and a Mock implementation.
- Shared logic lives in the Core package with an explicit `public` API; the app target holds UI and macOS-specific
  system services only. See `handbook/types/app/layout.md`.
- Mock, in-memory and preview-only code never ships: it lives in a test-support product or behind `#if DEBUG`. The
  release script fails if such symbols are found in the built app.

## Localization

- User-visible text is an English literal that is also the String Catalog key: `String.loc("Publish")`.
  Translations live in `Resources/Localizable.xcstrings`.
- UI languages are the nine in `handbook/guides/localization.md`, switchable in Settings and applied without restart. Every
  key carries every language; unit tests enforce it.
- UI copy keeps one necessary sentence and never uses infrastructure terms the user did not choose.

## Design

- Colors, spacing, radii, motion and window sizes come from the design tokens in Core; no magic numbers in views.
- Every SwiftUI view has a `#Preview` covering all its states; previews are part of design acceptance.
- Glass materials are for the navigation layer only and are never stacked.
- Entrance animations play on first appearance only, never on redraw.

## Accessibility

- Every interactive element has an `accessibilityIdentifier` named `<screen>.<element>` and a label VoiceOver can
  read; decorative elements use `accessibilityHidden(true)`.
- `scripts/ax-audit.swift` flags unnamed controls and untranslated text in the running app.
