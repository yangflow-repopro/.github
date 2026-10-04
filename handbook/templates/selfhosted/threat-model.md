<!-- template: selfhosted/threat-model.md v1 -->
<!-- docs/threat-model.md: what a self-hosted product protects and how. Each release's security walkthrough checks it. -->
# Threat model

## Assets

<What an attacker would want: credentials, sessions, user data, the host itself, the ability to act as the user.>

## Trust boundaries

<Where trusted and untrusted meet: the host and the container, the LAN, the internet, hosted services, model
providers, content the product reads.>

## Threats and mitigations

| Threat | Boundary | Mitigation | Verified by |
|---|---|---|---|
| <threat> | <boundary> | <what the code does> | <test, check or walkthrough item> |

## Accepted risks

<Risks we accept, each with the reason; or None.>

## Out of scope

<What this model does not cover; or None.>
