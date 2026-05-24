# Workflow

1. Glob `proposed-tickets/*.md` for files under review.
2. Read every globbed file in full before producing any verdicts, so batch-wide state is known when applying [cross-ticket checks](Checks).
3. For every ticket type encountered in the batch, read its matching template from [`skills/ticket-author/assets/`](../../skills/ticket-author/assets/).
4. Construct a unified mental checklist — frontmatter fields from the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema), the [File Naming](../Ticket-Author/File-Naming) pattern, mandatory sections from each template, the [Body Rules](../Ticket-Author/Body-Rules), and the cross-ticket rules — and apply it to each file before writing any verdict.
5. Emit one verdict block per file, then a final summary block.

If [`proposed-tickets/`](../../proposed-tickets/) is empty or absent, the subagent returns exactly `No tickets to review.`

If the `ticket-author` SKILL.md cannot be read (missing or permission error) or is empty, the subagent halts and returns exactly `Review blocked: ticket-author SKILL.md is unavailable. No verdicts produced.`
