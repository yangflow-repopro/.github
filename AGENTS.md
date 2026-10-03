<!-- template: AGENTS.md v1 -->
# AGENTS.md

## What it is

The organization defaults repository: the handbook, the document templates, the shared labels, issue and PR
templates, and the reusable CI workflows used by every product repository.

## Sources of truth

`handbook/` is the single source for how repositories are structured, documented, built and released.
`handbook/templates/manifest.json` says which repository type needs which documents. If a rule here and a
product repository disagree, this repository wins.

## Directory boundaries

```
handbook/              rules; templates/ and playbooks/ below it
.github/workflows/     reusable workflows (workflow_call), called from product repositories
scripts/               check-docs.py, sync-labels.sh
profile/               organization profile page
```

Nothing product-specific lives here; use `<Name>` and `<domain>` in examples.

## Commands

```bash
python3 scripts/check-docs.py .        # documents against the templates
scripts/sync-labels.sh <owner/repo>    # apply labels.yml
```

## Project rules

- A change to a template raises its version (`<!-- template: <name> v<N> -->`) and every product repository
  is rewritten from it (`handbook/docs.md`).
- A change to a reusable workflow is tested from a product repository's branch before it is merged.

## Red lines

This repository is public: no credentials, no internal hostnames, no product names. See `handbook/agents.md`.
