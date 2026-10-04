<!-- template: selfhosted/README.md v1 -->
<!-- Self-hosted product README (container image, web UI, optional macOS shell). Replace every <...>. Keep the H2 list and order. Delete this comment; keep the marker line above. -->
# <Name>

<One paragraph: what the product does for whom. Present tense, no marketing adjectives.>

## Status

<Version and state in two lines. Host requirements: macOS version and chip for the app; Linux with Docker Compose.
Link to the roadmap.>

## Product

<Five bullets at most: what it does. Plans and prices go to `docs/spec.md`, not here.>

## Install

<macOS: where to download the app, how to verify the download. Linux: where the compose file is, the one command
that starts it, how to verify the image.>

## Development

<Requirements; the build/test/lint commands for the core, the web UI and the macOS shell, copied from `AGENTS.md`;
how the version is bumped; link to the handbook.>

## Documentation

| Document | Contents |
|---|---|
| [docs/spec.md](docs/spec.md) | What to build |
| [docs/design.md](docs/design.md) | Design language |
| [docs/roadmap.md](docs/roadmap.md) | What comes after the baseline |
| [docs/adr/](docs/adr/README.md) | Decisions |
| [CHANGELOG.md](CHANGELOG.md) | Changes |
| [AGENTS.md](AGENTS.md) | Brief for AI collaborators |

## License

<One sentence: closed source, `LICENSE` is the terms of service, same text as `https://<domain>/terms`; third-party software in `THIRD_PARTY.md`.>
