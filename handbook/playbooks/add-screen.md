# Add or change a screen

## Before you start

- The feature is in `docs/milestones/next.md`.

## Steps

1. Design: edit or create `design/screens/<screen>.html` named like the code directory `UI/<Screen>/`. Every
   state, light and dark. List the screen in `design/README.md` (Screens table).
2. Get the design signed off.
3. Code: `UI/<Screen>/` with the view, its model and small row views; the model depends only on protocols;
   a `#Preview` for every state. Tokens only, no magic numbers (`docs/design.md`).
4. Identifiers: every interactive element has `accessibilityIdentifier` `<screen>.<element>` and a label.
5. Strings: `add-string.md`.
6. In the PR: screenshots of every state, light and dark, and the design acceptance checklist ticked.

## Files this touches

`design/screens/<screen>.html`, `design/README.md`, `UI/<Screen>/`, `Resources/Localizable.xcstrings`,
tests for the model.

## Check yourself

Preview shows every state; the localization tests pass; `scripts/ax-audit.swift` finds no unnamed controls.
