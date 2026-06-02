# Ticket Vet

The ticket-vet skill reviews the ticket proposal files changed in a pull request and posts the findings as comments on the PR. It runs headless, for use in CI. The review is delegated to parallel agents; the skill gates the PR, runs the agents, validates their findings, and turns them into comments.

It is invoked as `/ticket-vet <PR>` to print findings, or `/ticket-vet <PR> --comment` to also post them.

## Sections

- [Triggers](Ticket-Vet/Triggers)
- [Review Agents](Ticket-Vet/Review-Agents)
- [Workflow](Ticket-Vet/Workflow)
- [Output](Ticket-Vet/Output)
