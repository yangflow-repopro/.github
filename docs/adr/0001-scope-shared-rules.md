<!-- template: adr.md v1 -->
# 0001 Scope shared rules

- Status: accepted
- Date: 2026-10-07
- Related: [Documentation](../../handbook/docs.md)

## Context

The handbook began with native macOS products. New stacks and project purposes inherited platform,
commercial and deployment assumptions, while checks required identical document outlines and followed main.

## Decision

Separate mandatory collaboration and documentation rules from guides selected by project needs.
Keep language rules in stacks and concrete layout and release conventions in repository types.
Existing type identifiers remain supported; they select documentation presets, not mandatory architectures.
A project records its actual platforms, stack, languages, distribution and exceptions in its agent instructions and process document.
Allow project sections while requiring each template section once in order; keep legal and changelog checks strict.
Pin the reusable docs workflow and handbook-ref to the same commit and migrate consumers in separate PRs.
Move canonical rules into core/ and guides/, preserving old paths and heading anchors as compatibility entry points.
Do not change product architectures, licensing terms, supported languages or release workflows in this migration.

## Cost

Compatibility entry points stay until consumers migrate. Each project must deliberately upgrade its handbook pin.
Existing type names retain historical specificity; shared guidance avoids adding a new type for each stack combination.

## Revisit triggers

Extract another shared rule only when multiple current projects need it. Remove compatibility entry points only
when all maintained consumers and external references have an agreed migration.
