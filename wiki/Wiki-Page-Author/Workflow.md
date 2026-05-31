# Workflow

1. Understand the request — a page to write, update, or remove; an inline `> [!ODD]` block to add or resolve; a page investigation caution to add or lift; or folder organisation.
2. Read [`home.md`](../home) and the pages topically related to the subject, plus the target page if it already exists, and reuse the terminology those pages establish.
3. Write the page from the [page template](../../skills/wiki-page-author/assets/page-template), holding every sentence to the [Body Rules](Body-Rules). An [Open Design Decision](Open-Design-Decision) or [Page Investigation Caution](Page-Investigation-Caution) block follows its own rule set.
4. Update [`home.md`](../home) for any page added or removed, and flag inconsistencies a change introduces on other pages rather than fixing them silently. See [Standing Instructions](Standing-Instructions).
5. Walk the [Validation](Validation) checklist against every page written or changed. Items that fail are fixed and the checklist re-run until every item passes.
6. Delegate to the [wiki-page-reviewer](../Wiki-Page-Reviewer) subagent, passing the path of every page written or changed; the reviewer acts only on the paths it is given. The skill waits for its verdicts before continuing.
7. Act on the review. Pages marked `NEEDS WORK` have their listed violations applied and the [Validation](Validation) checklist re-run, then return to the reviewer; this repeats until every page returns `READY` and the summary reports `M of M pages ready`. A `NOTES:` line reporting no wiki index, or a batch-level pattern only the user can resolve, is surfaced to the user once.
8. The work is reported as done once the reviewer returns all `READY` verdicts.
