# Releases (MyGo native apps)

## Versions and artifacts

Use SemVer, `mygo.json` as the source, and `scripts/bump.py <version>` to update both changelogs.
The first public release is 1.0.0. Tags are `vX.Y.Z`; the tag must equal the configuration version.
Do not publish the template. `scripts/release.sh --check` runs local checks without publishing.
`go tool mygo build` packages the current platform. Its outputs are `.app` and `.dmg` on macOS,
`.exe` and an NSIS installer on Windows, and a desktop entry, archive and `.deb` on Linux.
Cross-compilation needs no cgo; macOS signing and DMG generation need macOS, and Windows installers need NSIS.

## Signing and updates

Use MyGo's signed update format, not Sparkle appcasts. Pure Go UI uses
`github.com/egoist/mygo/plugins/updater/native`, never the web update window.
The unconfigured template cannot check or install updates. Enable updates only after the product owns
its release settings: an Ed25519 public key, HTTPS download URL and signing process.
Generate keys outside the repository with `go tool mygo keygen`; keep the private key in a credential store.
Builds receive `MYGO_UPDATER_PRIVATE_KEY` from the protected environment, never from a tracked file.

Private source repositories must not be the client-facing GitHub update source. Use a public download
host such as `https://dl.<domain>`, backed by R2/S3, or a separate public release repository.
For R2 use MyGo's `updates.url` and `updates.s3`; keep credentials outside JSON.
Publish archives before manifests. Updates are per OS/architecture; keep previous archives for deltas.
Verify a real upgrade, a tampered archive rejection, cancellation and recovery before shipping.

macOS releases use Developer ID signing, notarization and stapling; Gatekeeper verification is required.
Windows public builds use Authenticode and a verified installer. Linux package behavior is tested on
supported distributions. Ad hoc or unsigned packages are development artifacts.

## Workflow boundary

The shared CI workflow only tests and builds. The template's manual packaging workflow stores artifacts,
with read-only repository permissions and no upload, signing secrets or release publication.
`scripts/release.sh` deliberately has no publishing command. Product-specific signing and publication
are added after maintainer approval and verified against a test destination. A reusable release workflow
must be exercised on a product branch before merge (`handbook/core/agents.md`).

The website download contract is recorded in `docs/website.md`; do not invent a `latest.json` writer
or Sparkle feed. Derive release notes from CHANGELOG, and never expose private repository links in clients.
