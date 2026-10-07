# Localization

## Languages

Apps, self-hosted products and websites ship the same nine languages. The language code differs between them.

| Language | App code (String Catalog) | Self-hosted web UI file | Website code and path |
|---|---|---|---|
| English (source) | `en` | `en.json` | `en`, `/` |
| Chinese, simplified | `zh-Hans` | `zh-Hans.json` | `zh`, `/zh` |
| Chinese, traditional | `zh-Hant` | `zh-Hant.json` | `zh-hant`, `/zh-hant` |
| Japanese | `ja` | `ja.json` | `ja`, `/ja` |
| Korean | `ko` | `ko.json` | `ko`, `/ko` |
| French | `fr` | `fr.json` | `fr`, `/fr` |
| German | `de` | `de.json` | `de`, `/de` |
| Spanish | `es` | `es.json` | `es`, `/es` |
| Portuguese (Brazil) | `pt-BR` | `pt-BR.json` | `pt`, `/pt` |

MyGo native apps use the app codes in embedded JSON catalogs; see `handbook/types/mygo-app/code.md`.

A self-hosted product's macOS shell uses the app codes in its own String Catalog.

A pipeline has no UI copy. The languages of the content it generates are listed per product in the pipeline's
configuration, with the app codes.

## Rules

- **English is the source and the only reference.** Translators and AI translate from English. Chinese is not
  a second reference.
- **Only UI copy is multilingual.** Logs, diagnostics, error summaries for developers, exported files, script
  output, code comments, docs, commits, PRs and release notes are English. `CHANGELOG.zh.md` is the one
  Chinese file of an app or a self-hosted product.
- Keep copy short: one necessary sentence beats a paragraph. Error copy says what happened and what to do.
- No em or en dashes in website copy (`check_i18n` fails on them).

## Add a string (app)

1. Write the English text at the use site: `String.loc("Publish")` for code-built text, `Text("Publish")` for
   SwiftUI. The English text is the catalog key.
2. Build once; Xcode adds the key to `Resources/Localizable.xcstrings`. Fill all nine languages, state
   `translated`. Placeholders (`%@`, `%lld`) keep their types and count.
3. Run the two localization test suites (`LocalizationCatalogTests`, `UserVisibleStringsTests`). They fail on a
   missing language, a left-over English copy in a CJK language, mismatched placeholders, a UI literal that is
   not in the catalog, and a catalog key no code uses.
4. Text that is not UI copy (an example URL, a keyboard hint) is `Text(verbatim:)`.

## Add a string (self-hosted web UI)

1. Write the English text at the use site as `t("Publish")`; values go in as named placeholders:
   `t("Signed in to {site}", { site })`. The English text is the key.
2. Add the key to `web/src/i18n/en.json` and translate it in the other eight files. Placeholders keep their names
   and count.
3. Error copy is keyed by the error's `code`, never by text the core sent (`handbook/types/selfhosted/code.md`).
4. Run the web UI's localization tests. They fail on a key missing from any language, a CJK value equal to the
   English, mismatched placeholders, a text node or user-visible attribute (`title`, `aria-label`, `placeholder`,
   `alt`) not passed through `t`, and a key no code uses.
5. Text that is not UI copy (an example URL, a keyboard hint) is marked `verbatim` and is not in the files.
6. The UI language follows the browser's preferred languages until the user picks one in Settings; switching
   applies without a reload.

## Add a language

1. App: add the language to the String Catalog (all keys), to the language list type in the app
   (`AppLanguage`), and to the catalog test's language list.
2. Self-hosted product: add `web/src/i18n/<code>.json` (every key), add the code to the web UI's language list and
   to its localization tests, and add the language to the macOS shell's String Catalog as for an app.
3. Website: add it to `i18n/languages.json` (path, HTML `lang`, browser language prefixes), copy
   `i18n/en.json` to `i18n/<code>.json` and translate, add screenshots if the site has a carousel.
4. Run `scripts/sitekit/check_i18n.py`, `scripts/build.py`, `scripts/sitekit/check_site.py`.
5. Add the language to the table above in the same PR.

## Website copy

Strings may contain HTML; `{{root}}` in a link becomes the language's path prefix. Every language file has the
same structure, the same HTML tags in the same order, the same link targets and placeholders as `en.json`
(`check_i18n.py`). Legal pages carry a translation notice in every non-English language (see `handbook/legal.md`).
