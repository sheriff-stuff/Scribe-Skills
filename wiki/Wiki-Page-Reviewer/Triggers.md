# Triggers

The subagent is invoked by name with the wiki page paths to review (e.g. `@wiki-page-reviewer <paths>`), or Claude delegates to it when the user asks to review, audit, lint, validate, or check a wiki page, and after the [Wiki Page Author](../Wiki-Page-Author) skill writes or updates a page.

Tools available to the subagent: `Read`, `Grep`, `Glob`. No write access.

The [Wiki Page Author](../Wiki-Page-Author) skill is injected into the subagent's system prompt and is the source of truth for body rules, ODD and caution block rules, naming, and templates.
