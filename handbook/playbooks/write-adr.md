# Write an ADR

Write one when a PR changes an established way of working, or a decision would otherwise exist only in a
conversation.

1. Next number: the highest in `docs/adr/` plus one. File `docs/adr/NNNN-lowercase-title.md` from
   `handbook/templates/common/adr.md`: H1 `# NNNN Title`, Status, Date, Related, then Context, Decision, Cost, Revisit
   triggers (`None` allowed).
2. Add the row to `docs/adr/README.md` with the same title as the H1.
3. If it supersedes another, set that file's Status to `superseded by NNNN`.
4. Write only this product's reasons. Where the reason is an organization standard, link the handbook file.
5. Tick "this PR changes an established way of working" in the PR and name the ADR.

## Files this touches

`docs/adr/NNNN-title.md`, `docs/adr/README.md`.

## Check yourself

`check-docs.py` (index and H1 agree, H2s match).
