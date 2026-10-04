<!-- template: pipeline/spec.md v1 -->
<!-- Final specification of a pipeline. Headings are stable names (no numbers); other documents link docs/spec.md#<slug>. -->
# <Name> specification

## Decisions

<What the pipeline is and is not; the choices that shape everything else, each one line with its reason; what is out of
scope.>

## Interfaces

<Every way in or out: commands with the files they read and write, pull requests and labels, workflows and their
triggers, the directories in this repository that hold data.>

## Data model

<Entities, fields, states and transitions, where each is stored, and each format's `version` and migration.>

## Modules

<The packages, what each owns, and which packages each may import.>

## Key flows

<One H3 per flow: trigger, steps, what is written, what can fail and how it recovers.>

## Technical baseline

<Runtime, language, dependencies, limits, how the tool reaches the workflows that run it.>

## Acceptance checklist

- [ ] <Observable requirement>
