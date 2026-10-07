# Go

Applies to every Go module in the organization. Repository types add architecture and platform rules.

## Toolchain

- Pin the exact Go patch in `go.mod`; CI reads it with `go-version-file: go.mod`.
- Commit `go.sum`. Pin tools with a `tool` directive and run them with `go tool <name>`.
- Format with `gofmt`; `go vet ./...` and `go test ./...` must pass. Run `go test -race ./...`
  on a host with a C toolchain; production builds use `CGO_ENABLED=0` unless an ADR permits cgo.
- After a dependency change, run `go mod tidy`; it must leave no diff on the next run.
- List every module in `go.mod` (direct and indirect) in `THIRD_PARTY.md`, with the exact version
  and license. Ship the required notices under `resources/ThirdPartyLicenses/`.
- MIT, BSD, ISC, Apache-2.0 and MPL-2.0 dependencies are allowed; others require an ADR.

## Code

Use one module until there is a real consumer for another. Start with `main.go` and `internal/`;
extract packages for coherent responsibilities, not test convenience. Follow Go naming and error conventions.

- Return errors; wrap with `%w` when adding context. Use `errors.Is` or `errors.As` for decisions.
- Validate values at file, environment, network and IPC boundaries before using them.
- Pass `context.Context` to work that can block; honor cancellation and bound timeouts and sizes.
- Keep state ownership clear. No goroutine leaks or unbounded channels. The UI thread owns UI state.
- Add an interface at a real external boundary when substitution is useful; no interface per struct.
- Avoid `panic` for recoverable failures. Keep package initialization free of network and disk writes.

## Logging

Use standard `log/slog`, UTC timestamps and stable structured fields. Do not log credentials,
customer data or whole request/response bodies. User-facing errors are localized separately.

## Tests and CI

Use the standard `testing` package, table tests where helpful, and `t.TempDir()` for files.
Test observable behavior and failure paths. Real service tests are opt-in, never required in CI.
Tests pin locale, time zone and external inputs and never write a user's saved settings.
CI verifies format, tidy, vet, tests and production compilation for supported targets.
