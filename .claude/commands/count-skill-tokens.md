---
description: Count tokens for a SKILL.md file via the Anthropic API
argument-hint: <path-to-SKILL.md>
allowed-tools: Bash(python:*)
---

Run `python .claude/commands/scripts/count-skill-tokens.py "$ARGUMENTS"` and report the token count to the user. The path is quoted so Windows backslash paths (e.g. `C:\Users\PC\work\Skills\skills\ticket-ultra-review\SKILL.md`) survive the shell.
