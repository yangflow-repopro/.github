# Add a user-visible string (self-hosted web UI)

1. Write the English text where it is used: `t("...")`, values as named placeholders (`{site}`). The English
   text is the key.
2. Add it to `web/src/i18n/en.json` and translate it in the other eight files; placeholders keep their names and
   count.
3. Error copy is keyed by the error `code`, never by text from the core.
4. Text that is not UI copy is marked `verbatim`.
5. Run the web UI's localization tests.

A string in the macOS shell follows `handbook/types/app/playbooks/add-string.md`.

## Files this touches

`web/src/i18n/*.json`, the source file using the string.

## Check yourself

The localization tests pass (`handbook/localization.md`, Add a string (self-hosted web UI)).
