# Repository layout (macOS apps)

Every app repository has the same shape so that tooling, CI and people can move between them.

```
<Name>/                    App target
  App/                     @main, menu bar scene, updater, system services (language, login item…)
  UI/                      One directory per screen; views depend only on models
  Resources/               Localizable.xcstrings, Assets.xcassets, <Name>.icon, ThirdPartyLicenses/
<Name>Core/                Local SwiftPM package
  Package.swift            defaultIsolation(MainActor.self); no third-party dependencies
  Sources/<Name>Core/
    Domain/                nonisolated value types
    Services/              protocols + Live implementations (API clients, stores, engines, redactor, log)
    Design/                DesignTokens and shared design primitives
  Sources/<Name>CoreTestSupport/   Mock and in-memory implementations (tests and DEBUG previews only)
<Name>Tests/               Swift Testing; @testable import of both modules
Config/
  Version.xcconfig         MARKETING_VERSION and CURRENT_PROJECT_VERSION; the only place they are written
  <Name>-Info.plist        Keys Xcode cannot generate (Sparkle feed, ATS exceptions)
project.yml                XcodeGen definition; references Config/Version.xcconfig
<Name>.xcodeproj           Generated; committed; CI checks it is up to date
design/                    High-fidelity mockups (HTML), icon source, exported icon layers, screenshots
docs/
  spec.md  design.md  process.md (deltas only)  roadmap.md
  adr/README.md + NNNN-title.md
  milestones/<name>.md
scripts/
  bump.sh  release.sh  release-credentials.sh  test-release.sh
  scan_secrets.py  website-changelog.py  ax-audit.swift  export-website-shots.sh
.github/workflows/ci.yml   Calls the shared macos-ci.yml
.github/workflows/release.yml  Calls the shared macos-release.yml on tags
.swift-format  .gitignore  .editorconfig
README.md  AGENTS.md  CLAUDE.md (contains only `@AGENTS.md`)
CHANGELOG.md  CHANGELOG.zh.md  LICENSE (terms of service)  THIRD_PARTY.md  SECURITY.md (points here)
```

## Rules

- After changing `project.yml`, run `xcodegen generate` and commit the regenerated project with it.
- Bundle identifiers follow the product domain: `com.<product-domain>.app`, tests `.tests`.
- `AGENTS.md` is the tool-neutral brief for AI collaborators: what the project is, directory boundaries,
  common commands, project-specific rules and red lines. It links to this handbook instead of repeating it.
- `docs/process.md` in a product repository lists only its scopes/labels and anything that differs
  from `handbook/process.md`.
- Version numbers are never edited by hand; use `scripts/bump.sh` (see `handbook/release.md`).
- `THIRD_PARTY.md` lists every dependency with version and license; the license text ships in
  `Resources/ThirdPartyLicenses/`.
