# Python

Applies to every Python script and tool in the organization: repository scripts (`scripts/*.py`), the website
generator and its checks, and the organization's own checks. Violations are bugs.

## Toolchain

| Setting | Value |
|---|---|
| Interpreter | `python3` as installed on the maintainer's Mac and on the GitHub-hosted runner; no virtual environment |
| Dependencies | Standard library only. A script that needs a package is rewritten or becomes an ADR |
| Network | No network access at build or check time |

## Scripts

- Every module starts with a docstring that says what it does; an executable script also starts with
  `#!/usr/bin/env python3` and its docstring says how to run it.
- Output is English. A finding is one line, `path: message` (or `path:line: message`); the exit status is 1 when
  anything failed.
- A script that publishes or deletes something has a dry run (`--check`) and refuses on any unexpected state.
- Secrets are never printed; values that may carry them are redacted first.

## Tests

`unittest`, in a `test_<script>.py` next to the script, run with `python3 scripts/test_<script>.py`. A script that
other repositories depend on has tests for every rule it enforces.
