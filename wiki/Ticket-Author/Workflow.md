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
6. Whether a reviewer pass runs automatically depends on the request. A file is an edit when the request names it by title or filename, points at an existing file in [`proposed-tickets/`](../../proposed-tickets/), or asks to fix, edit, update, or tweak it; anything else is a new ticket, and a request can mix the two. When the request includes new tickets, the skill dispatches the [ticket-reviewer](../Ticket-Reviewer) subagent over [`proposed-tickets/`](../../proposed-tickets/); for a request that only edits existing files, it first asks the user whether to run the reviewer and proceeds only on agreement. The skill fixes what the reviewer reports, then re-reviews — up to three times. Files still reporting `NEEDS WORK` after the third review are surfaced to the user rather than looped on further.
7. The ticket set is reported as ready once a reviewer pass shows every file at `READY`. Edits the user chose not to review are reported as written but unreviewed. Files still at `NEEDS WORK` after three reviews are reported with their outstanding violations rather than presented as ready.
