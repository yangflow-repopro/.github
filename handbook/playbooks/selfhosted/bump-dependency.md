# Bump a dependency (self-hosted product)

1. npm package: set the new exact version in the `package.json` that uses it and run `pnpm install` so
   `pnpm-lock.yaml` changes with it. Base image: change the pinned digest in `image/Dockerfile` (and
   `.node-version` when the Node.js major changes; they must agree). Swift package in the shell: as in
   `../bump-dependency.md`.
2. Read the dependency's changelog for breaking changes and license changes; a license outside the allowed list in
   `code-standards-selfhosted.md` needs an ADR.
3. Update `THIRD_PARTY.md`: version (must equal `package.json` or `Package.resolved`), license, part, whether it
   ships, where its notice is.
4. Run the `check` and `image` jobs locally; for a base image or runtime change also compare image size and idle
   memory with `docs/hosting.md`.
5. Add a `build` commit: `build: bump <dependency> to <version>`.

## Files this touches

`package.json`, `pnpm-lock.yaml`, `image/Dockerfile`, `.node-version`, `THIRD_PARTY.md`, notice files.

## Check yourself

`check-docs.py` compares `THIRD_PARTY.md` with every `package.json` and fails on a version range.
