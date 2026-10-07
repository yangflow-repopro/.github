# MyGo native application code

## Baseline

Pin MyGo and its CLI together in `go.mod`. The initial baseline is MyGo v0.2.16 and Go 1.27.1.
Run on macOS 12+, Windows 10/11 and Linux with GTK 3. Production uses `CGO_ENABLED=0`.
Support amd64 and arm64 only when the product documents and verifies both.
There is no Bun, Node, npm dependency or web asset in this type.

## Views and state

Use `mygo.NewWindow` with `Content: ui.View(view)`. The main thread owns view state.
A view handles input and draws from that state. Blocking services run outside the view,
then deliver their result to the main thread and request `Window.Update()`.
Do not create service interfaces, a separate core module or a store for a trivial counter.
Use MyGo theme colors and native controls. GPU-rendered native UI does not automatically
provide every operating-system widget or accessibility behavior; verify those on devices.

## Localization and accessibility

Ship all nine languages in `handbook/localization.md`, using its app codes as JSON catalog names.
Embed catalogs with `go:embed`, resolve the system locale via `App.Locale()`, and fall back to English.
A product may expose an explicit language picker; tests pass the locale directly, never change system settings.
Translations must have identical keys and formatting placeholders. Label symbol-only buttons.
Test localized actions using `ui.NewTester`, including a long translation and light/dark state.
Follow `handbook/ui-workflow.md`: spec, mockup, sign-off, implementation, device acceptance.

## Tests and evidence

Use `ui.NewTester` for clicks, keyboard actions, resize and appearance changes. It runs without a window.
Keep stable labels or `ID` values and pin dimensions and locale. Headless rendering is unit-test evidence,
not a device screenshot or accessibility acceptance. Capture the packaged app on each declared OS,
including minimum and default window sizes, all states, light/dark, keyboard traversal and screen reader use.
Store real captures as `design/screenshots/<screen>/<state>-<os>-<scheme>.png`.
Never mark a screen signed-off or accepted without the maintainer's explicit decision.

## Local checks

`gofmt`, `go mod tidy`, `go vet ./...`, `go test ./...`, script tests and document checks.
Compile each declared platform with `CGO_ENABLED=0 GOOS=<os> GOARCH=<arch> go build` into a temporary
output. Then package on the platform with `go tool mygo build`; cross-compilation alone does not verify
installers or a working device UI. Shared CI runs the same checks and six-target compilation.
