# Add or change a screen

## Before you start

- The feature is in `docs/milestones/next.md` and its section in `docs/spec.md` names the screen. Read
  `handbook/ui-workflow.md`: the steps below are its stages, and the gates are the maintainer's.

## Steps

1. Spec: add the ledger row (`planned`) with the `docs/spec.md#anchor`.
2. Design: for a new screen draw 2 or 3 directions as `design/screens/<screen>.direction-<x>.html`, named like
   the code directory `UI/<Screen>/`; every state, light and dark. Row to `proposed`.
3. Review: the maintainer approves in the review tool. Never pick a direction yourself. On approval rename the
   chosen file to `<screen>.html`, delete the other directions, align the documents, row to `signed-off` with the
   date.
4. Code: `UI/<Screen>/` with the view, its model and small row views; the model depends only on protocols;
   a `#Preview` for every state. Tokens only, no magic numbers (`docs/design.md`). Row to `in-review`, with the
   code dir. Do not start another screen's development before this one is accepted.
5. Identifiers: every interactive element has `accessibilityIdentifier` `<screen>.<element>` and a label.
6. Strings: `handbook/types/app/playbooks/add-string.md`.
7. Device acceptance: export light and dark captures of every state from the real app into
   `design/screenshots/<screen>/` (device captures only, no design renders). The maintainer compares and accepts.
8. Merge only after the accepted gate. In the same PR the row becomes `accepted` with both dates.

## Files this touches

`design/screens/<screen>.html`, `design/README.md` (ledger), `design/screenshots/<screen>/`, `UI/<Screen>/`,
`Resources/Localizable.xcstrings`, tests for the model.

## Check yourself

Preview shows every state; the localization tests pass; `scripts/ax-audit.swift` finds no unnamed controls;
`python3 <org>/scripts/check-docs.py .` passes (it checks the ledger against the files and code).
