# Repository layout (macOS apps)

Every app repository has the same shape so that tooling, CI and people can move between them.

```
<Name>/                    App target
  App/                     @main, menu bar scene, updater, system services (language, login item…)
  UI/                      One directory per screen; views depend only on models
  Resources/               Localizable.xcstrings, Assets.xcassets, <Name>.icon, ThirdPartyLicenses/
<Name>Core/                Local SwiftPM package
  Package.swift            no third-party dependencies; default MainActor isolation per ADR (handbook/stacks/swift.md)
  Sources/<Name>Core/
    Domain/                nonisolated value types
    Services/              protocols + Live implementations (API clients, stores, engines, redactor, log)
    Design/                DesignTokens and shared design primitives
                           Mock, in-memory and preview-only types: inside #if DEBUG (never in Release)
<Name>Tests/               Swift Testing; @testable import of both modules
Config/
  Version.xcconfig         MARKETING_VERSION and CURRENT_PROJECT_VERSION; the only place they are written
  <Name>-Info.plist        Keys Xcode cannot generate (Sparkle feed, ATS exceptions)
project.yml                XcodeGen definition; references Config/Version.xcconfig
<Name>.xcodeproj           Generated; committed; CI checks it is up to date
design/
  README.md                Viewing · Screens (screen x state x light/dark) · Decision log · Maintenance
  tokens.html              Colors, type, spacing, radii, materials, motion; mirrors docs/design.md and the Core tokens
  screens/<screen>.html    One file per screen, named like UI/<Screen>/; states switched with ?state=...
  icon/                    icon.html, <name>-icon.js, export-icons.mjs, layers/
  screenshots/<screen>/{light,dark}.png   Exported from a Mac at acceptance
docs/
  spec.md  design.md  process.md (deltas only)  roadmap.md
  adr/README.md + NNNN-title.md
  milestones/v<X.Y>.md  v<X.Y>-security.md  next.md
  legal.md  website.md
scripts/
  bump.sh  release.sh  release-credentials.sh  test-release.sh
  scan_secrets.py  website-changelog.py  ax-audit.swift  export-website-shots.sh
.github/workflows/ci.yml   Calls the shared macos-ci.yml
.github/workflows/release.yml  Calls the shared macos-release.yml on tags
.swift-format  .gitignore  .editorconfig
README.md  AGENTS.md
CLAUDE.md  GEMINI.md  .github/copilot-instructions.md   (each contains only `@AGENTS.md`)
.repo-type  .docs-check.json   (repository type for check-docs; names that must not appear)
.claude/settings.json  .codex/config.toml   (swift-format hook; narrow permission allowlist)
CHANGELOG.md  CHANGELOG.zh.md  LICENSE (terms of service)  THIRD_PARTY.md  SECURITY.md (points here)
```

## Rules

- After changing `project.yml`, run `xcodegen generate` and commit the regenerated project with it.
- Core package API is `public`. A Core type the app constructs needs an explicit `public init` (the synthesized
  memberwise initializer is internal). Keep `lint-paths` in `ci.yml` and any source-scanning test in step
  with the directories.
- Bundle identifiers follow the product domain: `com.<product-domain>.app`, tests `.tests`.
- `AGENTS.md` is the tool-neutral brief for AI collaborators: what the project is, directory boundaries,
  common commands, project-specific rules and red lines. It links to this handbook instead of repeating it.
- `docs/process.md` in a product repository lists only its scopes/labels and anything that differs
  from `handbook/core/process.md`.
- Version numbers are never edited by hand; use `scripts/bump.sh` (see `handbook/types/app/release.md`).
- `THIRD_PARTY.md` lists every dependency with version and license; the license text ships in
  `Resources/ThirdPartyLicenses/`.
