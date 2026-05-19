# Triggers

The subagent is invoked by name (e.g. `@ticket-reviewer`), or Claude delegates to it when a task matches its description.

Tools available to the subagent: `Read`, `Grep`, `Glob`. No write access.

The [Ticket Author](../Ticket-Author) skill is injected into the subagent's system prompt and is the source of truth for frontmatter schema, file naming, body rules, and templates.
