<!-- template: selfhosted/architecture.md v1 -->
<!-- docs/architecture.md of a self-hosted product: the layers, what each owns and may not do, how it is extended. The spec says what to build; this says how the parts fit. Eight H2s, fixed. -->
# <Name> architecture

## Principles

<Five or fewer, each with the rule it implies for the code.>

## Layers

<The layers from the user down to the machine, one line each: what the layer owns. A diagram in a code block.>

## Components

<Table: component, layer, owns, may call, code directory (`handbook/types/selfhosted/layout.md`).>

## Boundaries

<What each layer may not do (reach past the layer below it, read another layer's storage, hold secrets, act without the
policy that applies). Each rule names the check or test that enforces it.>

## Extension points

<How each kind of extension is added without changing the layers around it: what to declare, where it plugs in, what
it is checked against. One subsection per kind.>

## Data flow

<The main paths through the layers, step by step: a user request, scheduled work, an approval.>

## Data and privacy

<What is stored where, what leaves the host and why, where secrets live, how export and erase work.>

## Evolution

<What the first working skeleton contains, and the order in which the rest is added on top of it.>
