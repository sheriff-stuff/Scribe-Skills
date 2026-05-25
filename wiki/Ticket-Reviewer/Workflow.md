# Workflow

1. Read `.claude/url-resolution.md` from the project root. The file maps remote URLs (or URL prefixes) to local checkout paths, in a format the subagent can pattern-match against — there is no fixed schema. If the file is absent, URL-content checks are skipped and the missing file is surfaced in the batch NOTES line.
2. Glob `proposed-tickets/*.md` for files under review.
3. Read every globbed file in full before producing any verdicts, so batch-wide state is known when applying [cross-ticket checks](Checks).
4. For every ticket type encountered in the batch, read its matching template from [`skills/ticket-author/assets/`](../../skills/ticket-author/assets/).
5. For every URL appearing in any ticket, resolve it against the mappings from step 1 and read the local file. The content is used to check the [Body Rule](../Ticket-Author/Body-Rules) **Don't duplicate spec detail from the source doc**. The subagent never fetches the URL itself. Work-item URLs (issues, MRs, PRs) are skipped — they have no local equivalent. Any URL with no mapping is collected for the batch NOTES line.
6. Construct a unified mental checklist — frontmatter fields from the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema), the [File Naming](../Ticket-Author/File-Naming) pattern, mandatory sections from each template, the [Body Rules](../Ticket-Author/Body-Rules), and the cross-ticket rules — and apply it to each file before writing any verdict.
7. Emit one verdict block per file, then a final summary block.

If [`proposed-tickets/`](../../proposed-tickets/) is empty or absent, the subagent returns exactly `No tickets to review.`

If the `ticket-author` SKILL.md cannot be read (missing or permission error) or is empty, the subagent halts and returns exactly `Review blocked: ticket-author SKILL.md is unavailable. No verdicts produced.`
