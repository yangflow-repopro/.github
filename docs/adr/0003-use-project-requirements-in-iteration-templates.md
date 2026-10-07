<!-- template: adr.md v1 -->
# 0003 Use project requirements in iteration templates

- Status: accepted
- Date: 2026-10-08
- Related: [Documentation](../../handbook/core/docs.md), [Add a feature](../../handbook/playbooks/add-feature.md)

## Context

Common specification examples still assumed licensing and desktop updates. Iteration templates assumed release
versions, UI screens and a spec even for types that do not require one. The self-hosted guide required a shared
CI workflow that does not exist.

## Decision

Use the project's actual requirement document and shipped runtimes. Licensing, updates and screen fields apply
only when present. Keep existing product-specific requirements and completed history.
Upgrade common spec and the common, pipeline and self-hosted iteration templates to v2 with the same required H2s.
Allow dated iteration archives without introducing a version or release; preserve next.md and versioned names.
Keep marker checks strict and migrate consumer documents and pins together.
Describe existing project-local self-hosted CI and its responsibilities; extract shared workflows only for
current consumers after branch validation. Add no new configuration, dependency or service.

## Cost

Consumers must deliberately upgrade their markers and pinned handbook revision. Existing populated sections and
acceptance evidence are preserved; only project-inappropriate template instructions change.

## Revisit triggers

Add another shared template or workflow only when actual consumers need a distinct document set or reusable checks.
