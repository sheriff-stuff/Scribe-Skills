# Triggers

Runs on an explicit request for an ultra review of the tickets in a pull request — a CI job prompting Claude to ultra-review a PR's tickets, or a developer invoking `/ticket-ultra-review <PR>` locally. Pass `--comment` to post the findings to the PR; without it the review only prints. The `description` scopes model selection to explicit ultra-review intent, so a generic ticket-review or lint request, a code-review request, or a bare PR mention does not select it. The installed marketplace plugin must be enabled for the run to discover the skill.
