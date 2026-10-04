# Releases (macOS apps)

Apps are closed source, notarized, shipped from the product website and updated in-app with Sparkle 2.
The appcast and downloads live on Cloudflare R2 behind `dl.<product-domain>`.

## Versions and tags

- SemVer. The first public release is `1.0.0`; nothing earlier is released or tagged.
- Only releases are tagged: `vX.Y.Z` on the squash commit that bumps the version. Milestones are not
  tagged.
- `MARKETING_VERSION` is the user-facing version; `CURRENT_PROJECT_VERSION` is a monotonically increasing
  integer and is what Sparkle compares. Both live in `Config/Version.xcconfig` only.
- `scripts/bump.sh <version>` sets both (build number +1), moves the CHANGELOG "Unreleased" section
  under the new version with today's date, and prints the tag command. Nothing else edits them.
- A Pro license covers every 1.x version; a major version bump is a commercial decision recorded in an ADR.

## Changelog

- `CHANGELOG.md` follows Keep a Changelog. `CHANGELOG.zh.md` mirrors it in Chinese.
- The text is public: no issue or PR numbers, hashes, repository names, local paths, tooling words or
  security wording that was not written deliberately. `scripts/website-changelog.py` lints it and
  refuses on any hit.
- GitHub Release notes and the website changelog entry are both derived from these files; nothing is
  written twice.

## Pipeline

```
bump.sh → PR → CI green → merge → git tag vX.Y.Z → push tag
   └─► macos-release.yml (GitHub-hosted macOS runner, `release` environment)
         archive → scan app → sign (Developer ID, timestamp) → notarize → staple
         → dmg → sign dmg → Gatekeeper check → Sparkle sign_update
         → upload dmg + appcast.xml + latest.json to R2 → verify download hash
         → GitHub Release (notes from CHANGELOG) → website changelog PR
```

- The release workflow runs on a GitHub-hosted macOS runner. Everything it needs is an organization
  secret bound to the `release` environment: the Developer ID certificate (`.p12`, base64) and its
  password, an App Store Connect API key for `notarytool`, the Sparkle EdDSA private key, and the R2
  write credentials. The workflow imports the certificate and the Sparkle key into a temporary
  keychain that is deleted when the job ends; nothing is written to the repository or to logs.
- Local releases remain possible: `scripts/release-credentials.sh` keeps the same values in the
  maintainer's login keychain for `scripts/release.sh`.
- Secrets are rotated when a maintainer leaves and after any suspected exposure.
- `scripts/release.sh --check` is the dry run; `scripts/test-release.sh` tests the script itself and runs
  in CI on every PR that touches it.
- `release.sh` refuses to publish a build number that already exists in the appcast, a binary that
  contains mock or debug symbols, `get-task-allow`, credential-like strings or build-machine paths.
- The website's download button reads `latest.json` (version, URL, SHA-256); release history is a
  page on the website, not in the appcast.

## Launch checklist (per app, before `v1.0.0`)

- [ ] CI green (main + compat); `xcodegen` produces no diff; format lint passes
- [ ] `release.sh --check`, `test-release.sh --full` and `scan_secrets.py` (history and built app) pass
- [ ] Release binary contains no mock/in-memory/preview symbols
- [ ] Sparkle: public key in the bundle, private key in the keychain, appcast signature verifies, an
      actual update from a lower build number succeeds
- [ ] Licensing: activate, deactivate and offline grace tested against both test and live endpoints
- [ ] Website: all languages pass the checks; download button shows version and hash; legal pages
      match the in-app terms; support mailbox receives mail
- [ ] In-app links to terms, privacy and refund resolve to the website paths
- [ ] One full dry run of the tag-triggered release against a test bucket
