# Triggers

The subagent is invoked explicitly (e.g. `@ticket-reviewer`). It does not run automatically.

Tools available to the subagent: `Read`, `Grep`, `Glob`. No write access.

The [Ticket Author](../Ticket-Author) skill is injected into the subagent's system prompt and is the source of truth for frontmatter schema, file naming, body rules, and templates.
