# Release

The pipeline is described in `../release.md`. The steps for the maintainer:

1. Everything for the release is merged; `docs/milestones/next.md` is complete and all acceptance items are
   ticked on a Mac.
2. Rename `next.md` to `v<X.Y>.md`; record the security walkthrough as `v<X.Y>-security.md`
   (`templates/security-walkthrough.md`).
3. `scripts/bump.sh <X.Y.Z>`; review the diff (version files, changelog sections); PR; merge.
4. `scripts/release.sh --check` locally if you can.
5. Tag and push: `git tag -a vX.Y.Z -m "<Name> X.Y.Z" && git push origin vX.Y.Z`. The release workflow builds,
   signs, notarizes, publishes and creates the GitHub Release.
6. Check the download page, the update feed and one real update from the previous build.
7. Merge the website changelog pull request the release opened.

## Files this touches

`Config/Version.xcconfig`, `CHANGELOG.md`, `CHANGELOG.zh.md`, `docs/milestones/`, website `changelog.json`.

## Check yourself

The launch checklist in `../release.md`.
