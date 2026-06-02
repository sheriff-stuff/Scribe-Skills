# Workflow

The steps the ticket-author skill follows to produce a set of ticket files.

1. Understand the request and determine how many tickets are needed. The skill chooses each ticket's type by taking the first matching rule, top to bottom; epic is decided in step 4.
   1. **User named a type** (feature, spike, bug, chore, documentation, ODD, epic) — use it.
   2. **ODD** — never inferred; an ODD ticket originates only from an explicit request to resolve a wiki ODD.
   3. **Documentation** — the work only adds or changes wiki or docs, with no code change — use Documentation.
   4. **Spike, Bug, or Chore** — the request reads as an investigation, a defect fix, or maintenance with no user-facing behaviour change — ask the user before choosing one.
   5. **Otherwise** — use Feature.

2. Identify each ticket's [anchor](Ticket-Anchoring) — wiki-anchored or codebase-anchored. An anchor the skill cannot determine is settled with the user before drafting.
3. Read what's already in the repo — wiki pages, code, documentation — and reuse existing terminology rather than inventing new names. When a wiki page that informs a ticket carries a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block, the skill warns the user that the page is under investigation.
4. Decide the breakdown. Work that has multiple child tickets belonging together gets an epic file plus individual ticket files with `epic: auto`. Unrelated tickets stand alone. Each ticket represents an independently deliverable piece of work.
5. Batch-write every `.md` file to [`proposed-tickets/`](../../proposed-tickets/), using the matching template as the structural basis.
6. Delegate to the [ticket-reviewer](../Ticket-Reviewer) subagent, which reviews every file in [`proposed-tickets/`](../../proposed-tickets/). The loop is driven off each file's `VERDICT:` line rather than the summary count. A file marked `NEEDS WORK` either has each listed violation applied, or has a finding declined with a citation to the wiki, existing code, or the template — a finding is never silently dropped, and the citation is recorded in the reply to the user. After fixes, the reviewer runs again, and the loop stops as soon as every file reports `READY`. The loop is capped at three reviews: files still marked `NEEDS WORK` after the third, or a finding the author and reviewer deadlock on, are surfaced to the user with reasoning instead of re-reviewed. A `No tickets to review.` result stops the loop. URLs a `NOTES:` line reports as missing from `.claude/url-resolution.md` are listed to the user once.
7. The ticket set is reported as ready once every file reports `READY`. If the loop hits the cap with violations outstanding, those and the reasoning are reported instead — the set is not presented as ready.
