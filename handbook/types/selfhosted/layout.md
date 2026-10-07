# Repository layout (self-hosted products)

A self-hosted product (`.repo-type` `selfhosted`) is one container image that holds the whole product, a web UI
that every client uses, a native macOS shell that runs the image on Macs, and, when the product needs one, a
service the organization operates. This is the default layout, not a required set of components.
Projects declare included components and their real paths in AGENTS.md and record deviations in docs/process.md;
a client may live in another repository and a native shell is optional.

```
core/                      The server inside the image (TypeScript on Node.js)
  src/<module>/            One directory per module in docs/spec.md#modules; index.ts is its only public entry
  src/migrations/          Forward-only data migrations, numbered
  test/                    Unit tests (Vitest)
  package.json
shared/                    The API contract between core and web: types and schemas, no other runtime code
  src/
  package.json
web/                       The web UI, built to static files that the core serves
  src/screens/<screen>/    One directory per screen, named like design/screens/<screen>.html; states.ts lists
                           every state
  src/components/          Shared components; screens compose them
  src/design/tokens.css    Design tokens as CSS custom properties; the only place raw values live
  src/i18n/<code>.json     UI copy; en.json is the source
  public/                  PWA manifest and icons
  test/                    Unit tests (Vitest)
  e2e/                     End-to-end tests and screen captures against the built image (Playwright)
  package.json
image/
  Dockerfile               The one image: core, built web UI, runtimes; multi-stage, arm64 and x86_64
  compose.yaml             What Linux hosts run; development uses it too
macos/                     The native macOS shell, laid out as in handbook/types/app/layout.md:
  <Name>/                  App/, UI/, Resources/ (its String Catalog)
  <Name>Tests/
  Config/Version.xcconfig  Written by scripts/bump.sh only
  Config/<Name>-Info.plist
  project.yml  <Name>.xcodeproj
<service>/                 A service the organization operates for the product, one directory each (own package.json,
                           own deploy configuration); omitted when there is none
design/                    As in ui-workflow.md
docs/
  spec.md  design.md  hosting.md  threat-model.md  process.md  roadmap.md  legal.md  website.md
  adr/README.md + NNNN-title.md
  milestones/v<X.Y>.md  v<X.Y>-security.md  next.md
scripts/
  bump.sh                  Writes the version everywhere (below)
  check-version.sh         Fails when any manifest disagrees with VERSION
  capture-screens.mjs      Screen captures for design acceptance (ui-workflow.md)
  release.sh  scan_secrets.py  website-changelog.py
VERSION                    The product version; the single source
package.json  pnpm-workspace.yaml  pnpm-lock.yaml   Workspace root: core, shared, web, services
tsconfig.base.json  biome.json  .node-version
.github/workflows/ci.yml   Calls the shared selfhosted-ci.yml
.github/workflows/release.yml
.swift-format  .gitignore  .editorconfig  .dockerignore
README.md  AGENTS.md
CLAUDE.md  GEMINI.md  .github/copilot-instructions.md   (each contains only `@AGENTS.md`)
.repo-type  .docs-check.json
CHANGELOG.md  CHANGELOG.zh.md  LICENSE (terms of service)  THIRD_PARTY.md  SECURITY.md (points here)
```

## Rules

- **The image is the product.** Anything a Linux user also needs lives in `core/` or `web/`. The macOS shell owns
  only what is native to the Mac: running the image, the Keychain, the menu bar, notifications, launch at login and
  its own updates.
- **Modules meet at `index.ts`.** Code outside `core/src/<module>/` imports only that module's `index.ts`; a test
  that scans imports enforces it. The dependency direction between modules is recorded in `docs/spec.md#modules`.
- **`shared/` is the only contract** between core and web. The web UI never imports from `core/`; the core never
  imports from `web/`.
- **One version.** `VERSION` holds it. `scripts/bump.sh <version>` writes it to every `package.json`, to
  `macos/Config/Version.xcconfig` (with the build number +1) and moves the CHANGELOG section;
  `scripts/check-version.sh` runs in CI. Nothing else edits a version.
- **Exact dependency versions** in every `package.json` (no ranges); `pnpm-lock.yaml` is committed. Every dependency
  has a row in `THIRD_PARTY.md` (`check-docs.py` compares them).
- After changing `macos/project.yml`, run `xcodegen generate` and commit the regenerated project with it.
- Bundle identifiers of the shell follow the product domain: `com.<product-domain>.app`, tests `.tests`.
- `docs/process.md` lists only the repository's scopes (one per top-level directory above) and its differences
  from the handbook.
