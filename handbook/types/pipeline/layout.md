# Repository layout (pipelines)

Every `pipeline` repository has this shape.

```
apps/<tool>/               The command-line tool: argument parsing and wiring, no rules of its own
  src/  test/  package.json
packages/<name>/           One package per module in docs/spec.md#modules
  src/index.ts             The package's only public entry
  src/                     Implementation
  test/                    Unit tests (Vitest) and the package's fakes
  package.json
<data>/                    Directories the pipeline reads or writes in this repository, one per kind of data;
                           declared in docs/spec.md#interfaces; the schema lives in the package that owns them
docs/
  spec.md  operations.md  threat-model.md  process.md  roadmap.md
  adr/README.md + NNNN-title.md
  milestones/v<X.Y>.md  next.md
scripts/                   Small scripts CI or the maintainer runs
.github/workflows/ci.yml   Calls the shared pipeline-ci.yml
.github/workflows/<trigger>.yml   One workflow per trigger, named in docs/operations.md
package.json  pnpm-workspace.yaml  pnpm-lock.yaml   Workspace root
tsconfig.base.json  biome.json  .node-version  .editorconfig  .gitignore
README.md  AGENTS.md
CLAUDE.md  GEMINI.md  .github/copilot-instructions.md   (each contains only `@AGENTS.md`)
.repo-type  .docs-check.json
THIRD_PARTY.md  SECURITY.md (points here)
```

## Rules

- **Modules meet at `index.ts`.** Code outside `packages/<name>/src/` imports only that package's `index.ts`; a test
  that scans imports enforces it. The dependency direction between packages is recorded in `docs/spec.md#modules`.
- **The domain package depends on nothing.** The package that defines the domain types and their schemas imports no
  other workspace package, so every other package can build on it.
- **Entry points are thin.** Anything under `apps/` that a test could want to call belongs in a package.
- **Exact dependency versions** in every `package.json` (no ranges); `pnpm-lock.yaml` is committed. Every dependency
  has a row in `THIRD_PARTY.md` (`check-docs.py` compares them). `biome.json` is a copy of
  `handbook/stacks/biome.json`.
- `docs/process.md` lists only the repository's scopes (one per package and per top-level data directory) and its
  differences from the handbook.
