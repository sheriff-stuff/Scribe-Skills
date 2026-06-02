# Workflow

The steps the ticket-vet skill follows to review the tickets in a pull request.

1. Gate the PR; stop if it is closed, a draft, needs no review, or Claude has already commented. Claude-generated PRs are still reviewed.
2. Gather the relevant CLAUDE.md file paths.
3. Summarise the pull request.
4. Run the [review agents](Review-Agents) in parallel; each flags only high-signal issues.
5. Deduplicate the whole-batch reviewer's per-ticket findings against the per-ticket runs, keeping its cross-ticket findings.
6. Validate each issue with a parallel sonnet subagent; an issue that does not hold is dropped.
7. Keep the validated issues.
8. Print the findings to the terminal. Without `--comment`, stop. With `--comment` and no issues, post a clean summary comment and stop.
9. Plan the comments.
10. Post one inline comment per issue that maps to a changed line.
11. Post a summary comment carrying the whole-batch run's `N of M tickets ready.` line and the issues that have no diff line to attach to.
