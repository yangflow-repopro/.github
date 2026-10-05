<!-- template: pipeline/operations.md v1 -->
<!-- docs/operations.md: what the pipeline needs to run and how to stop it. Every value here is a fact the workflows must match. -->
# Operations

## Triggers

<Each workflow: file, trigger (schedule, dispatch from another repository, merge), what it runs, what it may change.>

## Secrets and permissions

| Secret | Held in | Used by | Scope | Rotation |
|---|---|---|---|---|
| <NAME> | <GitHub Secrets / environment> | <workflow, job> | <what it can do> | <how and how often> |

<The permissions each workflow requests, and why.>

## External services

<Each service the pipeline calls: purpose, quota or rate limit, cost, what the pipeline does when it is down.>

## Failure and recovery

<How a failed run shows itself, what is safe to re-run, how to withdraw each kind of outside effect (a published post, a
scheduled item, a paid call).>

## Switches

<The switch that halts every outward action, where it is set, how it was tested; other switches, or None.>

## Cost

<What a month of normal use costs and what bounds it.>
