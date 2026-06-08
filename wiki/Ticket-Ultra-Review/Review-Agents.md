# Review Agents

The skill launches these agents in parallel. Each is told the PR title and description and returns a list of issues, each with the reason it was flagged. All run on sonnet.

ODD tickets are out of scope: any `proposed-tickets/*.md` file whose `labels` include `type::ODD` is excluded from the whole review — no agent reviews or flags it.

| Agent | Lens | Scope |
| --- | --- | --- |
| Ticket-reviewer, per ticket | [Ticket Reviewer](../Ticket-Reviewer) rules on one ticket | each ticket in [`proposed-tickets/`](../../proposed-tickets/) |
| Ticket-reviewer, whole batch | Cross-ticket rules ([Checks](../Ticket-Reviewer/Checks)) | the whole [`proposed-tickets/`](../../proposed-tickets/) batch |
| Implementability | Whether an LLM coding agent could deliver each non-epic ticket from its prompt and links, and whether an epic's children together deliver it without contradicting it or each other | the whole batch |

The epic-group judgement covers any epic in scope. An epic file in the batch brings its `epic: auto` children alongside it; a ticket under review with an integer `epic:` points at an epic whose other children live in the tracker, resolved from there — or the epic group is reported unchecked when the tracker cannot be read. A clash between children, or between a child and the epic, is flagged only when a ticket under review is one of the parties.

One preliminary agent runs before this parallel review: a haiku agent gates the PR (closed, draft, no review needed, or already commented).

The agents flag only high-signal issues: internal contradiction, ambiguity that hides what to build or when it is done, unverifiable acceptance criteria, missing or broken references, a ticket an LLM coding agent could not deliver without inventing an undecided choice, an epic its children cannot deliver, or children that contradict the epic or each other, and quotable ticket-author rule violations. Wording and style preferences, concerns that depend on information outside the ticket and the pull request, subjective suggestions, pre-existing issues, details a ticket correctly defers to a linked spec, and implementability complaints whose only fix would thicken a ticket past what [ticket-author](../Ticket-Author) allows — deferring spec detail to a linked source, naming behaviours instead of test cases, and leaving technical decisions to the wiki or code — are not flagged.
