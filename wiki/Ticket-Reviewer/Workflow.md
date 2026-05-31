# Workflow

The steps the ticket-reviewer subagent follows to review a batch of ticket files.

1. Read `.claude/url-resolution.md` from the project root. The file maps remote URLs (or URL prefixes) to local checkout paths, in a format the subagent can pattern-match against — there is no fixed schema. If the file is absent, URL-content checks are skipped, the missing file is surfaced in the batch NOTES line, and the **Don't duplicate spec detail from the source doc** check is marked `UNVERIFIED` for every file whose source it would have read.
2. Glob `proposed-tickets/*.md` for files under review.
3. Read every globbed file in full before producing any verdicts, so batch-wide state is known when applying [cross-ticket checks](Checks).
4. For every ticket type encountered in the batch, read its matching template from [`skills/ticket-author/assets/`](../../skills/ticket-author/assets/).
5. For every URL appearing in any ticket, resolve it against the mappings from step 1 and read the local file. The content is used to check the [Body Rule](../Ticket-Author/Body-Rules) **Don't duplicate spec detail from the source doc**. The subagent never fetches the URL itself. Work-item URLs (issues, MRs, PRs) are skipped — they have no local equivalent. Any URL with no mapping is collected for the batch NOTES line, and the check is marked `UNVERIFIED` for the file that carries it.
6. Draft a verdict for each file by applying every [check](Checks) — frontmatter fields from the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema), the [File Naming](../Ticket-Author/File-Naming) pattern, mandatory sections from each template, the [Body Rules](../Ticket-Author/Body-Rules), and the cross-ticket rules. Then re-walk every file with the draft in hand for violations the first pass missed or rules applied inconsistently, repeating until a walk produces no new findings. The iteration is internal and does not appear in the output.
7. Emit one verdict block per file, then a final summary block.

If [`proposed-tickets/`](../../proposed-tickets/) is empty or absent, the subagent returns exactly `No tickets to review.`
