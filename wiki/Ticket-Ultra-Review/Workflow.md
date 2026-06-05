# Workflow

The steps the ticket-ultra-review skill follows to ultra-review the tickets in a pull request.

1. Gate the PR; stop if it is closed, a draft, needs no review, or Claude has already commented. Claude-generated PRs are still reviewed.
2. Run the [review agents](Review-Agents) in parallel; each flags only high-signal issues. Deduplicate the whole-batch reviewer's per-ticket findings against the per-ticket runs, keeping its cross-ticket findings.
3. Validate each issue with a parallel sonnet subagent; an issue that does not hold is dropped.
4. Keep the validated issues.
5. Print the findings to the terminal. Without `--comment`, stop. With `--comment` and no issues, post a clean summary comment and stop.
6. Plan the comments.
7. Post one inline comment per issue that maps to a line in the PR diff.
8. Post a summary comment carrying the whole-batch run's `N of M tickets ready.` line and the issues that have no diff line to attach to.
