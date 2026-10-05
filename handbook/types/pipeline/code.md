# Code (pipelines)

Packages and the command-line tool follow `handbook/stacks/typescript.md`. This page adds what is specific to a
pipeline. Violations are bugs.

## Architecture

- **State is files.** The pipeline keeps its state in this repository (or in what an external service holds), never in
  a database. Every format it writes has a schema and a `version` (`handbook/types/pipeline/release.md`).
- **Compute and act are separate.** A step that decides what to do returns a plan as data; a step that touches the
  outside world carries the plan out. Both are tested separately.
- **The domain package defines the contract.** Other packages take their types from its schemas
  (`handbook/types/pipeline/layout.md`).
- **Configuration is data.** What differs between the things the pipeline works on (products, projects, accounts) is
  read from files and validated by a schema; no such name appears in code.

## Side effects

- Every command that has an outside effect (posting, publishing, deleting, pushing, spending money) accepts
  `--dry-run`: it prints what it would do and touches nothing.
- Every outside effect is **idempotent**: look up before creating, so a second run, or a retry after a crash, leaves
  the outside world as one run would. Each flow is tested for success, failure half-way and retry.
- An outward-facing action reads a recorded approval from the repository (for example a draft in the state
  `approved`) and refuses to run without it. The pipeline never acts on its own authority.

## Untrusted content

- Content read from other repositories or websites, and every model response, is untrusted until a schema has parsed
  it. It is written to files as data and never executed, evaluated, or placed in a shell command or a workflow
  expression.
- A model call that reads untrusted content holds no credential and no tool with an outside effect; its output is data
  that the code then checks.

## Secrets

- Secrets arrive as environment variables from GitHub Secrets (`docs/operations.md` lists each one). They are never
  read from a file in the repository and never taken as a command-line argument.
- A command checks at start that every secret it needs is set and names the missing variable, never a value.

## Command-line conventions

- The result of a command is written to standard output; everything else goes to standard error.
- Exit status: `0` success, `1` the work failed, `2` invalid arguments or configuration.
- `--help` of every command lists its inputs (arguments, files read, environment variables) and its outputs (files
  written, outside effects).

## Logging

- On top of the stack's rules: logs are JSON lines on standard error, and record that a call happened (service,
  operation, duration, outcome), not its content: no page text, no model prompt or response.

## Tests

- Tests run offline and need no secret. Every external client has a fake that implements the same interface and lives
  in `test/`; fakes never ship.
- Anything a model produces is tested with recorded fixtures and checks on the output's structure, never with a live
  call. Live checks are opt-in through environment variables and never run in CI.
- A test scans every package's imports and fails when one reaches past another package's `index.ts`.

## CI

Every PR runs the shared `pipeline-ci.yml` reusable workflow on a GitHub-hosted Linux runner:

| Job | Does |
|---|---|
| check | the TypeScript stack's CI steps · the repository's `scripts/scan_secrets.py` over the whole history |

Documents are checked by `docs-check.yml`, which the repository's `docs.yml` calls.

Workflows declare `permissions: contents: read` and raise it per job; third-party actions are pinned by commit. The
workflow is added to this repository together with the first `pipeline` code and is tested from that repository's
branch before it is merged, like every reusable workflow.
