# Review Agents

The skill launches these agents in parallel. Each is told the PR title and description and returns a list of issues, each with the reason it was flagged. All run on sonnet.

| Agent | Lens | Scope |
| --- | --- | --- |
| Objective-ticket | Reads each ticket cold for contradiction, ambiguity, and unverifiability, and audits it against the project CLAUDE.md | each changed ticket |
| Ticket-reviewer, per ticket | [Ticket Reviewer](../Ticket-Reviewer) rules on one ticket | each changed ticket |
| Ticket-reviewer, whole batch | Cross-ticket rules ([Checks](../Ticket-Reviewer/Checks)) | the whole [`proposed-tickets/`](../../proposed-tickets/) batch |
| Implementability, per ticket | Whether an LLM coding agent could deliver the ticket from its prompt and links; epics are skipped | each changed non-epic ticket |
| Implementability, group | Whether the epic and its children, taken together, deliver the epic; runs only when the batch contains an epic | the epic with its children |

Three preliminary agents run before this parallel review: a haiku agent gates the PR (closed, draft, no review needed, or already commented), a haiku agent gathers the relevant CLAUDE.md file paths, and a sonnet agent summarises the changes.

The agents flag only high-signal issues: internal contradiction, ambiguity that hides what to build or when it is done, unverifiable acceptance criteria, missing or broken references, a ticket an LLM coding agent could not deliver without inventing an undecided choice, an epic its children cannot deliver, and quotable CLAUDE.md or ticket-author rule violations. Wording and style preferences, concerns that depend on information outside the ticket and the pull request, subjective suggestions, pre-existing issues, and details a ticket correctly defers to a linked spec are not flagged.
