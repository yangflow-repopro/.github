# Release (self-hosted product)

The pipeline is described in `handbook/types/selfhosted/release.md`. The steps for the maintainer:

1. Everything for the release is merged; `docs/milestones/next.md` is complete and every acceptance item is ticked
   on the host it names.
2. Rename `next.md` to `v<X.Y>.md`; record the security walkthrough, covering every row of
   `docs/threat-model.md`, as `v<X.Y>-security.md`.
3. `scripts/bump.sh <X.Y.Z>`; review the diff (`VERSION`, every `package.json`, `macos/Config/Version.xcconfig`,
   changelog sections); PR; merge.
4. `scripts/release.sh --check` locally if you can.
5. Tag and push: `git tag -a vX.Y.Z -m "<Name> X.Y.Z" && git push origin vX.Y.Z`. The release workflow builds and
   publishes the image and the app.
6. Check: the download page, `latest.json`, the compose file's digest, one real Sparkle update from the previous
   build, and `docker compose pull && docker compose up -d` from the previous compose file on a Linux host.
7. Merge the website changelog pull request the release opened.

## Files this touches

`VERSION`, `package.json` files, `macos/Config/Version.xcconfig`, `CHANGELOG.md`, `CHANGELOG.zh.md`,
`docs/milestones/`, website `changelog.json`.

## Check yourself

The launch checklist in `handbook/types/selfhosted/release.md`.
