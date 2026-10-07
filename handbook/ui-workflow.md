# UI workflow

How a screen goes from an idea to an accepted, shipped view. It applies to every repository with a UI (`app`, `mygo-app` and
`selfhosted`; a `pipeline` has no UI and skips it); a repository's
`docs/process.md` records only differences. `scripts/check-docs.py` and `scripts/design-review.py` enforce and
support it.

## Roles

| Who | Decides | Does not decide |
|---|---|---|
| Maintainer | Whether each screen design passes; which features are in `docs/spec.md`; whether a screen passes device acceptance; which of spec, design and code wins when they disagree | Token values, implementation details |
| Agent | How a design is drawn; the design tokens (recorded in `docs/design.md`); the code; keeping the documents in sync | Any "approved" or "accepted" verdict; choosing a direction for the maintainer |

## Lifecycle of a screen

```
spec -> design -> review -> develop -> device acceptance -> archive
 ^                                                              |
 +------------------- next screen / iteration <-----------------+
```

| Stage | What happens | Output | Gate (exit condition) | Status |
|---|---|---|---|---|
| 1 Spec | The feature is written into `docs/spec.md` and names its screen | A spec section with a stable anchor | Maintainer accepts the feature scope | `planned` |
| 2 Design | A new screen gets 2 or 3 directions; a redesign gets before and after; a small change to an existing screen changes the file only | `design/screens/<screen>.direction-<x>.html` | The file shows every state, light and dark | `proposed` |
| 3 Review | The maintainer looks at each screen (`design-review.py`) and answers "approve" or "change to ..." | Ledger row with the date and the chosen direction | The maintainer says approve for that screen. A blanket "go with your suggestion" counts only for what was shown | `signed-off` |
| 3b Sync | Right after approval: rename the chosen file to `<screen>.html`, delete the other directions, align spec, `docs/design.md` and the README | One documentation PR | `check-docs.py` passes; no `direction` file is left | `signed-off` |
| 4 Develop | One PR per screen: the screen's code directory, model, tests, every state renderable, identifiers, strings in every language (see Code directories and captures) | A PR | Local checks pass (below). The PR is **not merged** | `in-review` |
| 5 Device acceptance | Capture every state from the real product as the repository type defines; the maintainer compares them with the design and checks the screen where the type says | `design/screenshots/<screen>/` (real captures only) | The maintainer says the screen is accepted. Only then does the PR merge | `accepted` |
| 6 Archive | Merge, delete the branch, ledger row to `accepted`, one line in the decision log | `main` | Ledger, files and code directory agree | `accepted` |

## Iron rules

1. One screen at a time through develop and acceptance. The next screen's development does not start until the
   previous one is accepted. Design of several screens can run in parallel.
2. Whenever spec, design and code disagree: stop and ask the maintainer which wins. Default: the document wins;
   change the document first, then the code.
3. Changing an accepted screen goes back to stage 2.
4. A status moves forward in the order above only. Moving back needs a reason in the decision log.
5. Only the maintainer's explicit words move a screen to `signed-off` or `accepted`. An agent records them; it
   never infers them.

## Code directories and captures

| | `app` | `selfhosted` |
|---|---|---|
| Screen code | `<Name>/UI/<Screen>/` | `web/src/screens/<screen>/`; native shell screens in `macos/<Name>/UI/<Screen>/` |
| Every state renderable | A `#Preview` per state | `states.ts` per screen, rendered at `/__states/<screen>/<state>` in development builds |
| Identifiers | `accessibilityIdentifier` `<screen>.<element>` | `data-testid="<screen>.<element>"` |
| Captures | Exported from the running app on a Mac: every state, light and dark (`handbook/types/app/captures.md`) | `scripts/capture-screens.mjs` against the running image: every state at each viewport the product declares in `docs/spec.md`, light and dark, named `<state>-<viewport>-<scheme>.png`; shell screens as for apps |
| Where the maintainer accepts | On a Mac | Wherever each declared viewport is used: the macOS shell's window, a desktop browser, a real phone |
| Automated UI checks | `scripts/ax-audit.swift` | The accessibility check in the end-to-end suite (`handbook/types/selfhosted/code.md`) |

### MyGo native apps

Screen code lives in `internal/ui/<screen>/`. Use localized control labels and stable IDs,
with `ui.NewTester` covering each state. Device captures, keyboard and screen reader checks
are required on every supported OS (`handbook/types/mygo-app/code.md`). All design gates and
ledger rules apply; headless images do not substitute for device captures.

## Status vocabulary

Exactly five words, in the ledger's Status column: `planned`, `proposed`, `signed-off`, `in-review`, `accepted`.
Anything else fails `check-docs.py`.

## The ledger

The Screens table of `design/README.md` (template `handbook/templates/common/design-README.md` v2) is the single
source of truth:

| Screen | Spec | Design file | Code dir | Status | Signed off | Accepted |
|---|---|---|---|---|---|---|

- Spec is `docs/spec.md#anchor`, so a feature leads to its screen and a screen to its feature.
- The ledger changes in the same PR as the change it records.
- `check-docs.py` (for repositories whose `design/README.md` carries the v2 marker) requires: every
  `design/screens/*.html` has a row and every row has its file (`.direction-` files are ignored while the row is
  `proposed`, and forbidden in any later status); the code directory exists for `in-review` and `accepted`;
  `accepted` has at least one png in `design/screenshots/<screen>/`; the Signed off date is present from
  `signed-off` on and the Accepted date for `accepted`; every Spec anchor exists.

## The `design/` directory

Allowed at the top level, nothing else:

```
design/
  README.md              ledger, how to view, decision log
  tokens.html            token page, kept in step with the code tokens; check-tokens.py verifies it
  check-tokens.py
  screens/               <screen>.html; temporarily <screen>.direction-<x>.html while proposed
  screenshots/<screen>/  device captures only
  <icon sources>         listed in .docs-check.json as "design_icons" (for example icon.html, a layers directory)
```

No history is kept in the tree: no `mockup.html`, `reference/`, `archive/`, old milestone screenshots or design
renders. History is in Git.

### Screenshots

Only captures from the real product, produced in stage 5 as Code directories and captures defines, are committed.
Renders of the design files are not.

**Latest captures.** When a screen's code or design changes after review, re-capture and commit the new images in
the same PR, so `design/screenshots/<screen>/` always shows the latest state. Delete stale images.

**Before asking for acceptance**, launch the product locally with demo data in the state to check, and tell the
maintainer exactly which window and state to look at. Say what was not verified (a screenshot not opened, a key
press not sent).

## Review tool

`python3 <org>/scripts/design-review.py <repo> [--port 8800]` starts a local server (standard library only) on
`http://127.0.0.1:8800/`. The home page lists screens by status: waiting for review (`proposed`), built and
waiting for device acceptance (`in-review`), signed off, accepted. A screen page shows the spec section, the
design file (all states, light and dark), the device captures beside it when they exist, and for proposed
screens the direction files. Two buttons, "Approve" and "Request change" (with a text box), record the maintainer's
answer in `<repo>/.design-review/decisions.jsonl`. That file is not tracked (the tool adds it to
`.git/info/exclude`); the agent reads it and applies the decisions to the ledger and the files. `--check` renders
every page once and exits, for tests. The interface labels are Chinese by design, with the English status word in
brackets.

## Merging and CI

- Checks run locally and must pass. `app`: formatter, tests, `check-docs.py`, `check-tokens.py`; hosted CI is not
  used for macOS minutes. `selfhosted`: the `check` and `image` jobs of `handbook/types/selfhosted/code.md` (CI) and
  `check-tokens.py`, run locally; a merge does not wait for hosted CI.
- A UI code PR also needs the maintainer's device acceptance (stage 5). Documentation and fix PRs merge once the
  local checks pass.
- Stage explicit paths only; never `git add -A` or `git commit -a`.
- `app`: noise the build writes to `Localizable.xcstrings` (entries marked `stale`) is not committed.

## Who owns which document

| Document | Owns | Changed by |
|---|---|---|
| `docs/spec.md` | What to build: features, data, flows, acceptance; every feature names its screen | The agent, after the maintainer accepts |
| `docs/design.md` | The design language and token decisions | The agent |
| `design/README.md` | The ledger and the decision log | The agent, in the same PR as every status change |
| `docs/process.md` | Differences from the handbook for this repository | The agent |
| `handbook/ui-workflow.md` | This process | Only after the maintainer approves |
