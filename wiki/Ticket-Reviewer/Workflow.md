# Workflow

The steps the ticket-reviewer subagent follows to review a batch of ticket files.

1. Determine the set under review. If the dispatch names specific ticket files, that named set is under review; otherwise glob `proposed-tickets/*.md`. This set is the batch for the [cross-ticket checks](Checks) — when it holds a single file those checks cannot run and are marked `UNVERIFIED` for it.
2. Read every file in the set under review in full before producing any verdicts, so the whole set's state is known when applying the cross-ticket checks.
3. For every ticket type encountered in the batch, read its matching template from [`skills/ticket-author/assets/`](../../skills/ticket-author/assets/).
4. For every non-work-item URL appearing in any ticket, fetch it and read the linked page or file. The content is used to check the [Body Rule](../Ticket-Author/Body-Rules) **Don't duplicate spec detail from the source doc**. Work-item URLs (issues, MRs, PRs) are skipped — there is no spec to duplicate. When the consumer project's `CLAUDE.md` directs how a URL should be resolved — mapping a host or prefix to a local checkout, or directing that a host not be fetched — the subagent follows that instead of fetching. When a source cannot be read (the fetch fails, or project policy blocks it with no local alternative), the check is marked `UNVERIFIED` for the file that carries the URL and the URL is named in the batch NOTES line.
5. Draft a verdict for each file by applying every [check](Checks) — frontmatter fields from the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema), the [File Naming](../Ticket-Author/File-Naming) pattern, mandatory sections from each template, the [Body Rules](../Ticket-Author/Body-Rules), and the cross-ticket rules. Then re-walk every file with the draft in hand for violations the first pass missed or rules applied inconsistently, repeating until a walk produces no new findings. The iteration is internal and does not appear in the output.
6. Emit one verdict block per file, then a final summary block.

If the set under review is empty — no files were named and [`proposed-tickets/`](../../proposed-tickets/) is empty or absent — the subagent returns exactly `No tickets to review.`
