# Localization

## Languages

Apps and websites ship the same nine languages. The language code differs between the two.

| Language | App code (String Catalog) | Website code and path |
|---|---|---|
| English (source) | `en` | `en`, `/` |
| Chinese, simplified | `zh-Hans` | `zh`, `/zh` |
| Chinese, traditional | `zh-Hant` | `zh-hant`, `/zh-hant` |
| Japanese | `ja` | `ja`, `/ja` |
| Korean | `ko` | `ko`, `/ko` |
| French | `fr` | `fr`, `/fr` |
| German | `de` | `de`, `/de` |
| Spanish | `es` | `es`, `/es` |
| Portuguese (Brazil) | `pt-BR` | `pt`, `/pt` |

## Rules

- **English is the source and the only reference.** Translators and AI translate from English. Chinese is not
  a second reference.
- **Only UI copy is multilingual.** Logs, diagnostics, error summaries for developers, exported files, script
  output, code comments, docs, commits, PRs and release notes are English. `CHANGELOG.zh.md` is the one
  Chinese file of an app.
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

## Add a language

1. App: add the language to the String Catalog (all keys), to the language list type in the app
   (`AppLanguage`), and to the catalog test's language list.
2. Website: add it to `i18n/languages.json` (path, HTML `lang`, browser language prefixes), copy
   `i18n/en.json` to `i18n/<code>.json` and translate, add screenshots if the site has a carousel.
3. Run `scripts/sitekit/check_i18n.py`, `scripts/build.py`, `scripts/sitekit/check_site.py`.
4. Add the language to the table above in the same PR.

## Website copy

Strings may contain HTML; `{{root}}` in a link becomes the language's path prefix. Every language file has the
same structure, the same HTML tags in the same order, the same link targets and placeholders as `en.json`
(`check_i18n.py`). Legal pages and the FAQ carry a translation notice in every non-English language
(see `legal.md`).
