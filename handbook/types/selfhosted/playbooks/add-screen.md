# Add or change a screen (self-hosted product)

## Before you start

- The feature is in `docs/milestones/next.md` and its section in `docs/spec.md` names the screen. Read
  `handbook/ui-workflow.md`: the steps below are its stages, and the gates are the maintainer's.

## Steps

1. Spec: add the ledger row (`planned`) with the `docs/spec.md#anchor`.
2. Design: for a new screen draw 2 or 3 directions as `design/screens/<screen>.direction-<x>.html`, named like
   `web/src/screens/<screen>/`; every state at the phone and desktop viewports, light and dark. Row to `proposed`.
3. Review: the maintainer approves in the review tool. Never pick a direction yourself. On approval rename the
   chosen file to `<screen>.html`, delete the other directions, align the documents, row to `signed-off` with the
   date.
4. Code: `web/src/screens/<screen>/` composed from `web/src/components/`, with `states.ts` covering every state the
   design shows. Tokens only (`web/src/design/tokens.css`), no raw values. Data comes only through the API in
   `shared/`. Row to `in-review`, with the code dir. Do not start another screen's development before this one is
   accepted.
5. Identifiers: every interactive element has `data-testid="<screen>.<element>"` and an accessible name.
6. Strings: `handbook/types/selfhosted/playbooks/add-string.md`.
7. Tests: end-to-end coverage of the screen's flow and the accessibility check on every state.
8. Captures: `node scripts/capture-screens.mjs <screen>` against the running image writes
   `design/screenshots/<screen>/<state>-<viewport>-<scheme>.png`. Before asking for acceptance, start the image
   locally with demo data and tell the maintainer the address and which states to look at on a desktop browser, a
   phone and the macOS shell's window.
9. Merge only after the accepted gate. In the same PR the row becomes `accepted` with both dates.

A screen of the macOS shell itself follows `handbook/types/app/playbooks/add-screen.md`.

## Files this touches

`design/screens/<screen>.html`, `design/README.md` (ledger), `design/screenshots/<screen>/`,
`web/src/screens/<screen>/`, `web/src/i18n/*.json`, `web/e2e/`, maybe `shared/` and `web/src/components/`.

## Check yourself

Every state renders at `/__states/<screen>/<state>` at both viewports in both schemes; the localization tests and
the accessibility check pass; `python3 <org>/scripts/check-docs.py .` passes.
