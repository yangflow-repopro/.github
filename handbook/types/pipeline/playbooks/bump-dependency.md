# Bump a dependency (pipeline)

1. Set the new exact version in the `package.json` that uses it and run `pnpm install` so `pnpm-lock.yaml` changes
   with it. When the Node.js major changes, change `.node-version` and every CI setup step that names it.
2. Read the dependency's changelog for breaking changes and license changes; a license outside the allowed list in
   `handbook/stacks/typescript.md` needs an ADR.
3. Update `THIRD_PARTY.md`: version (must equal `package.json`), license, package, whether it runs in production, where
   its notice is.
4. Run the repository's CI commands (`AGENTS.md`, Commands) locally.
5. Add a `build` commit: `build: bump <dependency> to <version>`.

## Files this touches

`package.json`, `pnpm-lock.yaml`, `.node-version`, `THIRD_PARTY.md`.

## Check yourself

`check-docs.py` compares `THIRD_PARTY.md` with every `package.json` and fails on a version range.
