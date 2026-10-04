<!-- template: pipeline/README.md v1 -->
<!-- Pipeline README. Replace every <...>. Keep the H2 list and order. Delete this comment; keep the marker line above. -->
# <Name>

<One paragraph: what the pipeline does, for whom, on what input. Present tense, no marketing adjectives.>

## Status

<State in two lines: what runs today, what does not. Link to the roadmap.>

## What it does

<Five bullets at most: the commands and what each turns into what.>

## Run it

<Locally: requirements and the one command per task, with `--dry-run`. In workflows: which triggers run it (details in
`docs/operations.md`). Which secrets it needs, by name only.>

## Development

<Requirements; the install, lint, typecheck and test commands copied from `AGENTS.md`; link to the handbook.>

## Documentation

| Document | Contents |
|---|---|
| [docs/spec.md](docs/spec.md) | What to build |
| [docs/operations.md](docs/operations.md) | Triggers, secrets, services, failure, switches, cost |
| [docs/threat-model.md](docs/threat-model.md) | Assets, boundaries, threats |
| [docs/roadmap.md](docs/roadmap.md) | What comes next |
| [docs/adr/](docs/adr/README.md) | Decisions |
| [AGENTS.md](AGENTS.md) | Brief for AI collaborators |

## License

<One sentence: private, all rights reserved; third-party software in `THIRD_PARTY.md`.>
