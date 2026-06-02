# Ticket Vet

The ticket-vet skill reviews the ticket proposal files changed in a pull request and posts the findings as comments on the PR. It runs headless, for use in CI. The review is delegated to parallel agents; the skill gates the PR, runs the agents, validates their findings, and turns them into comments.

It is invoked as `/ticket-vet <PR>` to print findings, or `/ticket-vet <PR> --comment` to also post them.

## Triggers

Reviewing the tickets in a pull request, or a CI step that gates ticket quality on a PR.

## Review agents

The skill launches these agents in parallel. Each is told the PR title and description and returns a list of issues, each with the reason it was flagged. All run on sonnet.

| Agent | Lens | Scope |
| --- | --- | --- |
| Objective-ticket | Reads each ticket cold for contradiction, ambiguity, and unverifiability, and audits it against the project CLAUDE.md | each changed ticket |
| Ticket-reviewer, per ticket | [Ticket Reviewer](Ticket-Reviewer) rules on one ticket | each changed ticket |
| Ticket-reviewer, whole batch | Cross-ticket rules ([Checks](Ticket-Reviewer/Checks)) | the whole [`proposed-tickets/`](../proposed-tickets/) batch |
| Implementability, per ticket | Whether an LLM coding agent could deliver the ticket from its prompt and links; epics are skipped | each changed non-epic ticket |
| Implementability, group | Whether the epic and its children, taken together, deliver the epic | the epic with its children |

Two checks bracket these: a haiku agent gates the PR (closed, draft, no review needed, or already commented), and a sonnet agent summarises the changes.

## Workflow

1. Gate the PR; stop if it is closed, a draft, needs no review, or Claude has already commented.
2. Gather the relevant CLAUDE.md file paths.
3. Summarise the pull request.
4. Run the review agents in parallel; each flags only high-signal issues.
5. Validate each issue with a parallel sonnet subagent; an issue that does not hold is dropped.
6. Keep the validated issues.
7. Print the findings to the terminal. Without `--comment`, stop. With `--comment` and no issues, post a clean summary comment and stop.
8. Plan the comments.
9. Post one inline comment per issue that maps to a changed line.
10. Post a summary comment carrying the whole-batch run's `N of M tickets ready.` line and the issues that have no diff line to attach to.

## Output

Findings print to the terminal. With `--comment`, each issue on a changed line becomes an inline comment, and whole-file, structural, and cross-ticket findings go into one summary comment. When no issues are found, a single comment records that the tickets were checked. Every posted comment opens with a `🤖 Generated with Claude Code` line.
