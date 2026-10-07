# Add a language

See `handbook/guides/localization.md`, "Add a language". Steps in order:

1. App: add to the String Catalog (all keys), to the language type (`AppLanguage`), to the catalog test's
   language list.
2. Website: `i18n/languages.json`, `i18n/<code>.json` translated from English, screenshots if the site has a
   carousel.
3. `scripts/sitekit/check_i18n.py`, `scripts/build.py`, `scripts/sitekit/check_site.py`.
4. Update the language table in `handbook/guides/localization.md`.

## Files this touches

App: catalog, language type, tests. Website: `i18n/`, `public/` (generated), screenshots.

## Check yourself

Both repositories' CI; the language appears in the app's Settings and in the website's language menu.
