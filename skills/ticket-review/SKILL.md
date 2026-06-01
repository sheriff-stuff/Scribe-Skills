---
name: ticket-review
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr list:*), WebFetch, mcp__github_inline_comment__create_inline_comment
description: Review the tickets in a pull request
---

Provide a ticket review for the given pull request.

**Agent assumptions (applies to all agents and subagents):**
- All tools are functional and will work without error. Do not test tools or make exploratory calls. Make sure this is clear to every subagent that is launched.
- Only call a tool if it is required to complete the task. Every tool call should have a clear purpose.

To do this, follow these steps precisely:

1. Launch a haiku agent to check if any of the following are true:
   - The pull request is closed
   - The pull request is a draft
   - The pull request does not need ticket review (e.g. automated PR, trivial change that is obviously correct)
   - Claude has already commented on this PR (check `gh pr view <PR> --comments` for comments left by claude)

   If any condition is true, stop and do not proceed.

Note: Still review Claude generated PR's.

2. Launch a haiku agent to return a list of file paths (not their contents) for all relevant CLAUDE.md files including:
   - The root CLAUDE.md file, if it exists
   - Any CLAUDE.md files in directories containing files modified by the pull request

3. Launch a sonnet agent to view the pull request and return a summary of the changes

4. Launch the following agents in parallel to independently review the changes. Each agent should return the list of issues, where each issue includes a description and the reason it was flagged (e.g. "CLAUDE.md adherence", "unclear ticket", "not implementable", "ticket-author rule violation"). The agents should do the following:

   Agent 1: sonnet objective-ticket agent (parallel subagent with the others)
   Read each changed ticket cold, as a first-time reader who does not know the ticket-author rules. Flag where it is contradictory, ambiguous, unactionable, or unverifiable — a self-conflicting scope, an undefined term, a goal you cannot tell how to meet, an untestable acceptance criterion, an unconfirmable done-state, or a missing or broken reference. Also audit it against any CLAUDE.md that shares its path or a parent. Flag only significant problems; ignore nitpicks. Leave the ticket-author rules to the ticket-reviewer agent.

   Agent 2: ticket-reviewer agent, one per ticket (parallel subagents with the others)
   For each changed ticket file, launch the ticket-reviewer agent once, passing it that one ticket as its target. These per-ticket runs cover the per-ticket rules and cannot run the cross-ticket checks (the whole-batch run does those), so ignore any cross-ticket `UNVERIFIED` they report. Each violation is an issue.

   Agent 3: ticket-reviewer agent, whole batch (parallel subagent with the others)
   Launch the ticket-reviewer agent once over the whole `proposed-tickets/` batch, passing no target set so it sees every ticket. Its unique contribution is the cross-ticket checks — at most one epic per batch, `epic:` references resolving; keep those findings as issues. Deduplicate its per-ticket findings against the per-ticket runs on file + rule + verbatim offending text.

   Agent 4: sonnet implementability agent, one per changed ticket (parallel subagents with the others)
   Launch one of these for each changed ticket, skipping any `type: epic` file — an epic is a grouping, not a unit of work to implement (the group implementability agent covers the epic with its children). A ticket is a prompt handed to an LLM coding agent that has the wiki and the codebase in context. Take that agent's position: read the ticket as your prompt and follow its links. Decide whether you could carry the ticket to a correct PR without inventing a decision the ticket left open. You are judging feasibility — do not make any changes. Flag the ticket where you would have to guess at an undecided choice, where the linked context does not resolve a detail the work needs, or where you could not tell when the work is done.

   Agent 5: sonnet implementability agent, the epic with its children as a group (parallel subagent with the others)
   Run this only when the batch contains an epic. Read the epic together with the child tickets that link to it, and judge the set as a whole: handed these tickets, could an LLM coding agent deliver the epic? Flag where the epic states scope that no child ticket implements, where children contradict each other or the epic, or where delivering every child would still leave the epic's goal unmet. You are judging feasibility — do not make any changes.

   **CRITICAL: We only want HIGH SIGNAL issues.** Flag issues where:
   - A ticket is internally contradictory, or so ambiguous a reader cannot tell what to build or when it is done
   - An acceptance criterion cannot be verified, or a referenced page, file, or ticket is missing or broken
   - Handed the ticket as a prompt, an LLM coding agent could not deliver it without inventing an undecided choice the ticket or its linked context leaves open
   - The epic and its child tickets, taken together, could not deliver the epic — scope the epic states is implemented by no child, or children that conflict with the epic or each other
   - Clear, unambiguous CLAUDE.md violations where you can quote the exact rule being broken
   - Clear, unambiguous ticket-author rule violations where you can quote the exact rule being broken

   Do NOT flag:
   - Wording or style preferences
   - Concerns that depend on information outside the ticket and the pull request
   - Subjective suggestions or improvements

   If you are not certain an issue is real, do not flag it. False positives erode trust and waste reviewer time.

   In addition to the above, each subagent should be told the PR title and description. This will help provide context regarding the author's intent.

5. For each issue found in the previous step, launch parallel subagents to validate the issue. These subagents should get the PR title and description along with a description of the issue. The agent's job is to review the issue to validate that the stated issue is truly an issue with high confidence. For a CLAUDE.md or ticket-author rule violation, the agent should validate that the rule that was violated is scoped for this file and is actually violated. For an objective-ticket or implementability issue, the agent should validate that the problem holds when the ticket and the context it links are read together. Use sonnet subagents to validate.

6. Filter out any issues that were not validated in step 5. This step will give us our list of high signal issues for our review.

7. Output a summary of the review findings to the terminal:
   - If issues were found, list each issue with a brief description.
   - If no issues were found, state: "No issues found. Checked for CLAUDE.md and ticket-author compliance, clarity, and implementability."

   If `--comment` argument was NOT provided, stop here. Do not post any GitHub comments.

   If `--comment` argument IS provided and NO issues were found, post a summary comment using `gh pr comment` and stop.

   If `--comment` argument IS provided and issues were found, continue to step 8.

8. Create a list of all comments that you plan on leaving. This is only for you to make sure you are comfortable with the comments. Do not post this list anywhere.

9. Post inline comments for each issue using `mcp__github_inline_comment__create_inline_comment` with `confirmed: true`. For each comment:
   - Provide a brief description of the issue
   - For small, self-contained fixes, include a committable suggestion block
   - For larger fixes (6+ lines, structural changes, or changes spanning multiple locations), describe the issue and suggested fix without a suggestion block
   - Never post a committable suggestion UNLESS committing the suggestion fixes the issue entirely. If follow up steps are required, do not leave a committable suggestion.

   **IMPORTANT: Only post ONE comment per unique issue. Do not post duplicate comments.**

10. Post a summary comment on the pull request using `gh pr comment`. Lead with the whole-batch ticket-reviewer run's `N of M tickets ready.` line, then list the issues you could not post inline (whole-file, structural, or cross-ticket findings with no diff line) with their file, rule, and why.

Use this list when evaluating issues in Steps 4 and 5 (these are false positives, do NOT flag):

- Pre-existing issues
- Something that appears to be a problem but is actually correct
- Pedantic nitpicks that a senior engineer would not flag
- A ticket detail the linked spec legitimately owns, where the ticket correctly defers to the link instead of restating it

Notes:

- Use the gh CLI to interact with GitHub (e.g., fetch pull requests, create comments).
- Create a todo list before starting.
- You must cite and link each issue in inline comments (e.g., if referring to a CLAUDE.md or ticket-author rule, include a link to it).
- If no issues are found and `--comment` argument is provided, post a comment with the following format:

---

## Ticket review

No issues found. Checked for CLAUDE.md and ticket-author compliance, clarity, and implementability.

---

- When linking to code in inline comments, follow the following format precisely, otherwise the Markdown preview won't render correctly: https://github.com/anthropics/claude-code/blob/c21d3c10bc8e898b7ac1a2d745bdc9bc4e423afe/package.json#L10-L15
  - Requires full git sha
  - You must provide the full sha. Commands like `https://github.com/owner/repo/blob/$(git rev-parse HEAD)/foo/bar` will not work, since your comment will be directly rendered in Markdown.
  - Repo name must match the repo you're reviewing
  - # sign after the file name
  - Line range format is L[start]-L[end]
  - Provide at least 1 line of context before and after, centered on the line you are commenting about (eg. if you are commenting about lines 5-6, you should link to `L4-7`)
