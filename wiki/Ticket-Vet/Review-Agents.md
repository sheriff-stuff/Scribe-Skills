# Review Agents

The skill launches these agents in parallel. Each is told the PR title and description and returns a list of issues, each with the reason it was flagged. All run on sonnet.

| Agent | Lens | Scope |
| --- | --- | --- |
| Ticket-reviewer, per ticket | [Ticket Reviewer](../Ticket-Reviewer) rules on one ticket | each changed ticket |
| Ticket-reviewer, whole batch | Cross-ticket rules ([Checks](../Ticket-Reviewer/Checks)) | the whole [`proposed-tickets/`](../../proposed-tickets/) batch |
| Implementability | Whether an LLM coding agent could deliver each non-epic ticket from its prompt and links, and whether the epic and its children together deliver the epic (when the batch contains an epic) | the whole batch |

One preliminary agent runs before this parallel review: a haiku agent gates the PR (closed, draft, no review needed, or already commented).

The agents flag only high-signal issues: internal contradiction, ambiguity that hides what to build or when it is done, unverifiable acceptance criteria, missing or broken references, a ticket an LLM coding agent could not deliver without inventing an undecided choice, an epic its children cannot deliver, and quotable ticket-author rule violations. Wording and style preferences, concerns that depend on information outside the ticket and the pull request, subjective suggestions, pre-existing issues, details a ticket correctly defers to a linked spec, and implementability complaints whose only fix would thicken a ticket past what [ticket-author](../Ticket-Author) allows — deferring spec detail to a linked source, naming behaviours instead of test cases, and leaving technical decisions to the wiki or code — are not flagged.
