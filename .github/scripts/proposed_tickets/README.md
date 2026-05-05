# proposed_tickets

CI helper that turns the markdown files written by the `ticket-author` skill into GitHub issues.

## What it does

- `python -m proposed_tickets.validate <dir>` — parses every `*.md` in `<dir>` and verifies each one would be accepted by the GitHub Issues API. Used by the **validate** workflow on every PR that touches `proposed-tickets/`. Pass `--offline` to skip the GitHub API calls (useful for local runs and unit tests).
- `python -m proposed_tickets.create <dir>` — re-validates, creates issues (and sub-issues for epics), and deletes the source file for each ticket whose issue was successfully created. Used by the **create** workflow when the PR merges.

Both entry points read `GITHUB_TOKEN` and `GITHUB_REPOSITORY` (`owner/repo`) from the environment for API access.

## What gets validated

Per-file:
- `title` is present and a non-empty string
- `type`, if set, is exactly `epic`
- `weight`, if set, is a non-negative integer
- `due_date`, if set, matches `YYYY-MM-DD`
- `labels` / `assignees` are lists of strings
- `milestone` is a string
- `epic`, if set, is `auto` or an integer

PR-wide:
- At most one `type: epic` file
- Any `epic: <int>` reference resolves to an existing issue

Remote (skipped with `--offline`):
- Every label in `labels` (plus the synthetic `weight:<N>` label) exists on the repo
- `milestone` resolves to an open milestone

What is **not** validated (intentionally — these belong to the skill or to GitHub itself):
- Filename shape
- Body presence
- Assignee existence

## GitLab → GitHub field mapping

| Frontmatter field | How it lands on GitHub                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------------------------- |
| `title`           | Issue title                                                                                             |
| `labels`          | Issue labels                                                                                            |
| `assignees`       | Issue assignees (silently dropped by GitHub if a username does not exist)                               |
| `milestone`       | Resolved by title to a milestone number                                                                 |
| `weight: N`       | Added to issue labels as `weight:N`                                                                     |
| `due_date`        | Appended to issue body as `**Due:** YYYY-MM-DD` (GitHub issues have no native due date)                 |
| `type: epic`      | Marks this ticket as the parent issue. Children with `epic: auto` are attached as native sub-issues.    |
| `epic: auto`      | Attaches this issue as a sub-issue of the `type: epic` file in the same PR. No-op if no epic in the PR. |
| `epic: <int>`     | Attaches this issue as a sub-issue of the existing GitHub issue with that number.                       |

## Idempotency

Each created issue body ends with a hidden marker comment `<!-- proposed-ticket: <filename> -->`. On a re-run, `create.py` searches for that marker before creating; if the issue already exists it is reused (no duplicate) but the source file is still deleted.

## Cleanup is per-file

A source markdown file is deleted only after its issue is successfully created on GitHub. If creation fails, the file stays on disk and the workflow exits non-zero so the PR shows red. A subsequent rerun will skip already-created tickets (via the marker) and retry just the failures.
