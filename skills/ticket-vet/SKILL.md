---
name: ticket-vet
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr list:*), WebFetch, mcp__github_inline_comment__create_inline_comment
description: Vets the proposed tickets in a pull request for clarity, implementability, and ticket-author compliance, optionally posting findings as PR comments. Use only when the user explicitly asks to vet, lint, or review the tickets (not the code) in a PR — for example vet the tickets, ticket-vet this PR, or review the proposed tickets in a PR. Do NOT use for code review, for general review-this-PR requests, or when a PR is merely mentioned.
---

Provide a ticket review for the given pull request.

**ODD tickets are out of scope.** Any `proposed-tickets/*.md` file whose `labels` include `type::ODD` is excluded from the whole review — no step or agent below reviews or flags it.

**Agent assumptions (applies to all agents and subagents):**
- All tools are functional and will work without error. Do not test tools or make exploratory calls. Make sure this is clear to every subagent that is launched.
- Only call a tool if it is required to complete the task. Every tool call should have a clear purpose.

**Every comment posted to the PR — inline, summary, no-issues note — leads with `🤖 Generated with Claude Code` on its own line.**

To do this, follow these steps precisely:

1. Launch a haiku agent to check if any of the following are true:
   - The pull request is closed
   - The pull request is a draft
   - The pull request does not need ticket review (e.g. automated PR, trivial change that is obviously correct)
   - Claude has already commented on this PR (check `gh pr view <PR> --comments` for comments left by claude)

   If any condition is true, stop and do not proceed.

Note: Still review Claude-generated PRs.

2. Launch the following agents in parallel to independently review the changes. Each agent should return the list of issues, where each issue includes a description and the reason it was flagged (e.g. "unclear ticket", "not implementable", "ticket-author rule violation"). The agents should do the following:

   Agent 1: ticket-reviewer agent, one per ticket (parallel subagents with the others)
   For each changed non-ODD ticket file, launch the ticket-reviewer agent once, passing it that one ticket as its target. These per-ticket runs cover the per-ticket rules and cannot run the cross-ticket checks (the whole-batch run does those), so ignore any cross-ticket `UNVERIFIED` they report. Each violation is an issue.

   Agent 2: ticket-reviewer agent, whole batch (parallel subagent with the others)
   Launch the ticket-reviewer agent once over the whole non-ODD batch — every non-ODD ticket in `proposed-tickets/`, not only the changed ones — so it sees the whole batch at once. Its unique contribution is the cross-ticket checks — at most one epic per batch, `epic:` references resolving; keep those findings as issues.

   Agent 3: sonnet implementability agent, whole batch (parallel subagent with the others)
   Read every changed non-ODD ticket in one pass and judge it at two levels.
   - Per ticket (skip `type: epic` files): following the ticket's links, could an LLM coding agent with the wiki and codebase in context deliver this ticket without inventing an undecided choice, and could it tell when the work is done?
   - Epic group (only when the batch contains an epic): read the epic with its child tickets — does the set, taken together, deliver the epic's stated scope, and do any children contradict each other or the epic?

   **CRITICAL: We only want HIGH SIGNAL issues.** Flag issues where:
   - A ticket is internally contradictory, or so ambiguous a reader cannot tell what to build or when it is done
   - An acceptance criterion cannot be verified, or a referenced page, file, or ticket is missing or broken
   - Handed the ticket as a prompt, an LLM coding agent could not deliver it without inventing an undecided choice the ticket or its linked context leaves open
   - The epic and its child tickets, taken together, could not deliver the epic — scope the epic states is implemented by no child, or children that conflict with the epic or each other
   - Clear, unambiguous ticket-author rule violations where you can quote the exact rule being broken (these come from the ticket-reviewer agents, which carry the rules)

   Do NOT flag:
   - Wording or style preferences
   - Concerns that depend on information outside the ticket and the pull request
   - Subjective suggestions or improvements

   If you are not certain an issue is real, do not flag it. False positives erode trust and waste reviewer time.

   In addition to the above, each subagent should be told the PR title and description. This will help provide context regarding the author's intent.

   Once every agent above has returned, deduplicate the whole-batch reviewer's per-ticket findings against the per-ticket runs on file + rule + verbatim offending text, keeping its cross-ticket findings. The parallel agents cannot see each other's output, so this dedup happens here, after they all return — not inside any agent.

3. For each issue found in the previous step, launch parallel subagents to validate the issue. These subagents should get the PR title and description along with a description of the issue. The agent's job is to review the issue to validate that the stated issue is truly an issue with high confidence. For a ticket-author rule violation, the agent should validate that the rule that was violated is scoped for this file and is actually violated. For an implementability issue, the agent should validate that the problem holds when the ticket and the context it links are read together. Use sonnet subagents to validate.

4. Filter out any issues that were not validated in step 3. This step will give us our list of high signal issues for our review.

5. Output a summary of the review findings to the terminal:
   - If issues were found, list each issue with a brief description.
   - If no issues were found, state: "No issues found. Checked for ticket-author compliance, clarity, and implementability."

   If `--comment` argument was NOT provided, stop here. Do not post any GitHub comments.

   If `--comment` argument IS provided and NO issues were found, post a summary comment using `gh pr comment` and stop.

   If `--comment` argument IS provided and issues were found, continue to step 6.

6. Create a list of all comments that you plan on leaving. This is only for you to make sure you are comfortable with the comments. Do not post this list anywhere.

7. Post inline comments for each issue using `mcp__github_inline_comment__create_inline_comment` with `confirmed: true`. For each comment:
   - Provide a brief description of the issue
   - For small, self-contained fixes, include a committable suggestion block
   - For larger fixes (6+ lines, structural changes, or changes spanning multiple locations), describe the issue and suggested fix without a suggestion block
   - Never post a committable suggestion UNLESS committing the suggestion fixes the issue entirely. If follow up steps are required, do not leave a committable suggestion.

   **IMPORTANT: Only post ONE comment per unique issue. Do not post duplicate comments.**

8. Post a summary comment on the pull request using `gh pr comment`. Lead with the whole-batch ticket-reviewer run's `N of M tickets ready.` line, then list the issues you could not post inline (whole-file, structural, or cross-ticket findings with no diff line) with their file, rule, and why.

Use this list when evaluating issues in Steps 2 and 3 (these are false positives, do NOT flag):

- Pre-existing issues
- Something that appears to be a problem but is actually correct
- Pedantic nitpicks that a senior engineer would not flag
- A ticket detail the linked spec legitimately owns, where the ticket correctly defers to the link instead of restating it
- An implementability complaint whose only fix would thicken the ticket past what `skills/ticket-author/SKILL.md` allows — a ticket may defer spec detail to a linked source, name behaviours instead of enumerating test cases, and leave technical decisions to the wiki or code

Notes:

- Use the gh CLI to interact with GitHub (e.g., fetch pull requests, create comments).
- Create a todo list before starting.
- You must cite and link each issue in inline comments (e.g., if referring to a ticket-author rule, include a link to it).
- If no issues are found and `--comment` argument is provided, post a comment with the following format:

---

## Ticket review

No issues found. Checked for ticket-author compliance, clarity, and implementability.

---

- When linking to code in inline comments, follow this format precisely, otherwise the Markdown preview won't render correctly: https://github.com/anthropics/claude-code/blob/c21d3c10bc8e898b7ac1a2d745bdc9bc4e423afe/package.json#L10-L15
  - Requires full git sha
  - You must provide the full sha. Commands like `https://github.com/owner/repo/blob/$(git rev-parse HEAD)/foo/bar` will not work, since your comment will be directly rendered in Markdown.
  - Repo name must match the repo you're reviewing
  - # sign after the file name
  - Line range format is L[start]-L[end]
  - Provide at least 1 line of context before and after, centered on the line you are commenting about (eg. if you are commenting about lines 5-6, you should link to `L4-7`)
