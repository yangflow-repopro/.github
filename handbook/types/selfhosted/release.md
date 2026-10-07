# Releases (self-hosted products)

Apply each section only to components shipped by this project. Its documented architecture and release
contract decide whether it uses a container, a native shell, an agent or a separate client.

A self-hosted product ships two things that always carry the same version: a container image and a macOS app that
runs it. The image is published to a public registry so any host can pull it without an account; the app is
notarized and updated with Sparkle 2 like every macOS app (`handbook/types/app/release.md`). Downloads, feeds and
the compose file live on Cloudflare R2 behind `dl.<product-domain>`.

## Versions and tags

- SemVer. The first public release is `1.0.0`; nothing earlier is released or tagged.
- Only releases are tagged: `vX.Y.Z` on the squash commit that bumps the version.
- `VERSION` is the single source (`handbook/types/selfhosted/layout.md`). `scripts/bump.sh <version>` writes it to every
  manifest and to `macos/Config/Version.xcconfig`, raises the build number Sparkle compares, and moves the
  CHANGELOG "Unreleased" section under the new version with today's date.
- An app build pins the digest of the image built from the same commit and refuses to run any other.

## Changelog

As in `handbook/types/app/release.md`: `CHANGELOG.md` and `CHANGELOG.zh.md`, public wording only, linted by
`scripts/website-changelog.py`. One changelog covers the image and the app; an entry that concerns only one host
says so ("On Linux, …").

## Artifacts

| Artifact | Where | Verified by |
|---|---|---|
| Image `X.Y.Z`, `linux/arm64` and `linux/amd64` | `ghcr.io/yangflow-repopro/<name>` (public package) | Digest pinned in the app and in the compose file; signature (cosign, keyless, from the release workflow); SBOM attached |
| `compose.yaml` with the image pinned by digest | `https://dl.<domain>/compose.yaml` and `https://dl.<domain>/<X.Y.Z>/compose.yaml` | SHA-256 in `latest.json` |
| macOS app dmg | `https://dl.<domain>/` | Developer ID signature, notarization, Sparkle EdDSA signature |
| `latest.json` | `https://dl.<domain>/latest.json` | Version, dmg URL and SHA-256, image reference and digest, compose URL and SHA-256 |
| `appcast.xml` | `https://dl.<domain>/appcast.xml` | Sparkle |

A public image can be read by anyone. Nothing in it may depend on being secret: no keys, no hidden endpoints, no
licensing logic that only works while unread.

## Pipeline

```
bump.sh → PR → CI green → merge → git tag vX.Y.Z → push tag
   └─► selfhosted-release.yml (`release` environment)
         Linux runner:  build image (arm64 + amd64) → vulnerability scan → SBOM → push by digest
                        → cosign sign → write compose.yaml pinned to the digest
         macOS runner:  build app with the digest pinned → archive → scan app → sign → notarize → staple
                        → dmg → sign dmg → Gatekeeper check → Sparkle sign_update
         both:          upload dmg, compose.yaml, appcast.xml, latest.json to R2 → verify every hash
                        → GitHub Release (notes from CHANGELOG) → website changelog PR
```

- The image is pushed by digest first and tagged `X.Y.Z` only after the app is notarized, so a failed release never
  leaves a tag that points at an image without its app.
- Secrets are organization secrets bound to the `release` environment, as in `handbook/types/app/release.md`, plus the registry token.
  Image signing uses the workflow's identity; there is no signing key to store.
- `scripts/release.sh --check` is the dry run for both halves.
- The release refuses an image that contains test fakes, development routes (`/__states`), credential-like strings
  or build-machine paths, and an app that fails the checks in `handbook/types/app/release.md`.
- `selfhosted-release.yml` is added with the first release and rehearsed against a test bucket and a test package.

## Updates

- macOS: Sparkle updates the app; the new app pulls its pinned image, backs up the data directory's database, then
  starts the new image, which migrates forward.
- Linux: the web UI shows that a new version exists (from `latest.json`; the check can be turned off). The user runs
  `docker compose pull && docker compose up -d` with the new compose file. Nothing updates itself on Linux.
- Migrations run forward only, after an automatic backup. A data directory written by a newer version is refused
  with a message saying which version is needed. Downgrades are not supported (`docs/hosting.md`).

## Launch checklist (per product, before `v1.0.0`)

- [ ] CI green (check, image, shell); `check-version.sh` passes; image size and idle memory within the budgets in
      `docs/hosting.md`
- [ ] `release.sh --check` and `scan_secrets.py` (history, image filesystem, built app) pass
- [ ] Image: no fakes, no development routes, runs as non-root with a read-only root filesystem; vulnerability scan
      has no fixable high or critical finding; signature and SBOM verify
- [ ] A clean Mac and a clean Linux host each reach the first finished task by following only the website
- [ ] Upgrade from a data directory of every pre-release build the maintainer kept succeeds; a newer data directory
      is refused
- [ ] Sparkle: an actual update from a lower build number succeeds and pulls the new image
- [ ] The threat model's rows are each checked in `docs/milestones/v1.0-security.md`
- [ ] Hosted services the product depends on are running in production with monitoring
- [ ] Licensing, website, legal pages and in-app links as in `handbook/types/app/release.md`
- [ ] One full dry run of the tag-triggered release against a test bucket and a test package
