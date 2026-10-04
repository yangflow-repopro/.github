# Bump a dependency

1. Update the version (Swift package: the requirement in `project.yml`, then `xcodegen generate` and let
   `Package.resolved` change).
2. Read the dependency's changelog for breaking changes and license changes.
3. Update `THIRD_PARTY.md`: version (must equal `Package.resolved`), license, whether it ships, where its
   notice text is, whether About credits it. Replace the notice text file if the license text changed.
4. Build and run all tests.
5. Add a `build` commit: `build: bump <dependency> to <version>`.

## Files this touches

`project.yml`, `Package.resolved`, `THIRD_PARTY.md`, the notice file, the About credits.

## Check yourself

`check-docs.py` compares `THIRD_PARTY.md` with `Package.resolved`.
