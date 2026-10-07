<!-- template: adr.md v1 -->
# 0002 Record issue evidence before implementation

- Status: accepted
- Date: 2026-10-08
- Related: [Issue 13](https://github.com/yangflow-repopro/.github/issues/13), [Development process](../../handbook/core/process.md#issues-milestones-labels)

## Context

Shared issue forms need to describe findings and tasks across the repository presets. Environment details alone
do not distinguish reproduced behavior from assumptions, or explain which dependencies and rollback concerns matter.

## Decision

Preserve existing field identifiers, required fields and labels. Add an optional Bug evidence dropdown and
optional Task dependency, verification and impact fields. Request only relevant environment information and
exclude sensitive details. Early findings may be recorded before a spec; implementation tasks follow the
milestone spec step. A tracker is not scope approval. Label transitions need recorded evidence or a maintainer decision.
Prefer native issue relationships for actual blockers, with explicit links as the fallback.
Existing issues remain valid. GitHub issue forms have no documentation-template marker; document skeleton
versions and pinned consumer checks remain unchanged.

## Cost

Reporters may leave the new fields empty; maintainers still assess evidence and approve scope during triage.

## Revisit triggers

Make a field required only if actual reports show that leaving it optional repeatedly blocks useful triage.
