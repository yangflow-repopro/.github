# Add a user-visible string

1. Write the English text where it is used: `String.loc("...")` in code, `Text("...")` in SwiftUI. The
   English text is the key.
2. Build; open `Resources/Localizable.xcstrings`; fill the other eight languages (state `translated`);
   keep placeholders (`%@`, `%lld`) identical in type and count.
3. Text that is not UI copy is `Text(verbatim:)`.
4. Run the two localization test suites.

## Files this touches

`Resources/Localizable.xcstrings`, the source file using the string.

## Check yourself

`LocalizationCatalogTests` and `UserVisibleStringsTests` pass.
