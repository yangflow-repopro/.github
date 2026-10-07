# Add a language (self-hosted product)

See `handbook/guides/localization.md`, "Add a language". Steps in order:

1. Web UI: `web/src/i18n/<code>.json` with every key translated from English; the code in the web UI's language
   list and in its localization tests.
2. macOS shell: the language in its String Catalog (all keys), its language type and its catalog test.
3. Website: as in `handbook/types/app/playbooks/add-language.md`.
4. Update the language table in `handbook/guides/localization.md`.

## Files this touches

`web/src/i18n/`, the web UI's language list and tests, the shell's catalog and tests, the website's `i18n/`.

## Check yourself

The web UI's and the shell's localization tests pass; the language appears in Settings in the web UI and is used
by the shell's menu.
