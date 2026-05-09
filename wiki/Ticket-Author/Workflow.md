# Workflow

1. Clarify what the user wants to accomplish, how many tickets are needed, whether an epic is appropriate, and the type of each ticket.
2. Read what's already in the repo — wiki pages, code, documentation — and reuse existing terminology rather than inventing new names. When a wiki page that informs a ticket carries a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block, the skill stops, surfaces the caution to the user, and offers to route the page's material into `Out of Scope` or `Risks` (each with a link back to the cautioned page). The rule applies to Epic, Feature, Chore, and Spike tickets; Spikes and bugs are exempt.
3. Decide the breakdown. Work that has multiple child tickets belonging together gets an epic file plus individual ticket files with `epic: auto`. Unrelated tickets stand alone. Each ticket represents an independently deliverable piece of work.
4. Batch-write every `.md` file to [`proposed-tickets/`](../../proposed-tickets/), using the matching template as the structural basis.
