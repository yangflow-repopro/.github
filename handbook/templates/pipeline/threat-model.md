<!-- template: pipeline/threat-model.md v1 -->
<!-- docs/threat-model.md: what a pipeline that acts with the maintainer's accounts protects and how. Update it in the PR that adds a boundary. -->
# Threat model

## Assets

<What an attacker would want: the accounts the pipeline posts or pays with, the secrets, the reputation of what is
published, the repositories it can write to.>

## Trust boundaries

<Where trusted and untrusted meet: content read from other repositories and websites, model providers and their
responses, the services the pipeline calls, pull requests from forks, workflow runners.>

## Threats and mitigations

| Threat | Boundary | Mitigation | Verified by |
|---|---|---|---|
| <threat> | <boundary> | <what the code or the workflow does> | <test, check or walkthrough item> |

## Accepted risks

<Risks we accept, each with the reason; or None.>

## Out of scope

<What this model does not cover; or None.>
