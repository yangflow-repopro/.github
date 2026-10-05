# Releases (pipelines)

A pipeline is not released. `main` is what runs, from the moment a pull request merges; there is no version number,
no tag and no changelog file. The history of squash-merged pull requests is the record of changes.

## Data formats

Every file format the pipeline writes carries a `version` field and has a schema in the package that owns it. A
change to a format is a forward migration that reads every older version, listed in `docs/spec.md#data-model`; the
pipeline never writes a format it cannot read back.

## Rolling out a change

- A change to a workflow or to a step with outside effects is tried first on its branch, with the tool's `--dry-run`
  (`handbook/types/pipeline/code.md`), and the dry-run output is pasted into the pull request.
- A change that adds an outside channel, an account, a secret or a permission needs the maintainer's confirmation
  and updates `docs/operations.md` and `docs/threat-model.md` in the same pull request.

## Rolling back

Revert the pull request. Work the pipeline already did outside the repository (a published post, a call to a paid
service) is not undone by a revert; `docs/operations.md` says how to withdraw each kind.
