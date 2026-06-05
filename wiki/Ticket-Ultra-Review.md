# Ticket Ultra Review

The ticket-ultra-review skill runs an ultra review of the ticket proposal files changed in a pull request and posts the findings as comments on the PR. It runs headless, for use in CI. The review is delegated to parallel agents; the skill gates the PR, runs the agents, validates their findings, and turns them into comments.

It is invoked as `/ticket-ultra-review <PR>` to print findings, or `/ticket-ultra-review <PR> --comment` to also post them.

## Sections

- [Triggers](Ticket-Ultra-Review/Triggers)
- [Review Agents](Ticket-Ultra-Review/Review-Agents)
- [Workflow](Ticket-Ultra-Review/Workflow)
- [Output](Ticket-Ultra-Review/Output)
