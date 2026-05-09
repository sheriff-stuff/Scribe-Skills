# Workflow

1. Glob `proposed-tickets/*.md` for files under review.
2. Read every globbed file in full before producing any verdicts.
3. For every ticket type encountered in the batch, read its matching template from [`.claude/skills/ticket-author/assets/`](../../.claude/skills/ticket-author/assets/).
4. Emit one verdict block per file, then a final summary block.

If [`proposed-tickets/`](../../proposed-tickets/) is empty or absent, the subagent returns exactly `No tickets to review.`
