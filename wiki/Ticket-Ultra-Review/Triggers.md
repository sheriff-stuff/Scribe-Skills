# Triggers

Runs on a request to ultra-review the tickets in a pull request — a user invoking `/ticket-ultra-review`, or Claude selecting it (interactive or headless `claude -p`) when a prompt asks to lint or ultra-review the proposed tickets in a PR. The `description` scopes selection to ticket ultra-review intent, so general code-review or PR-mention prompts do not select it. In headless `claude -p`, only this model-driven selection applies — slash commands run in interactive mode — and the installed marketplace plugin must be enabled for the run to discover it.
