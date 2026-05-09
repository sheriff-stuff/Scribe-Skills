# Triggers

The subagent is invoked explicitly (e.g. `@wiki-page-reviewer <paths>`). It does not run automatically.

Tools available to the subagent: `Read`, `Grep`, `Glob`. No write access.

The [Wiki Page Author](../Wiki-Page-Author) skill is injected into the subagent's system prompt and is the source of truth for body rules, ODD and caution block rules, naming, and templates.
