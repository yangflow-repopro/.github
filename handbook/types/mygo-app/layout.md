# Repository layout (MyGo native apps)

```text
main.go                         lifecycle, native window and native updater
internal/ui/<screen>/           view, state and headless interaction tests
mygo.json                       name, reverse-DNS identifier, version and packaging
.go-version                     matches go.mod's exact Go version
go.mod, go.sum                 one module, pinned MyGo and CLI tool
resources/ThirdPartyLicenses/   license notices shipped with each app
resources/icon.png              optional neutral icon; replace before shipping
scripts/                        check.sh, bump.py, release.sh
.template/                      product README and AGENTS (template only)
docs/, design/                  required documents and design ledger
.github/workflows/              thin callers of shared CI and docs checks
```

Use `go tool mygo dev` and `go tool mygo build`. Configuration is JSON, never TypeScript.
Use `main: "."` and `out: "build"`; ignore `build/` and `.mygo/`.
The identifier follows the reversed domain plus `.app` and never changes after release.
Version is written only in `mygo.json`; `scripts/bump.py <version>` updates it and both changelogs.

The template starts with Template and example.com. `scripts/init.sh <Name> <domain> [--repo <name>]`
rewrites the product and module, sets `.repo-type` to `mygo-app`, installs the product docs,
and removes template-only scripts and planning notes. It validates before writing and never commits.
`--repo` defaults to the lowercase product name under the organization.
Run its tests on disposable copies, including rejected input and a second invocation.
A neutral demonstration is a template fixture, not a product screen approval; real products
must replace its spec and design and follow `handbook/guides/ui-workflow.md`.
