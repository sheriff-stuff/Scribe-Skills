# Workflow

1. Understand the request and determine how many tickets are needed. The skill chooses each ticket's type using this decision table; epic is decided in step 4.

   | User named type? | Type is ODD? | Type is Spike/Bug/Chore? | Action                                            |
   | ---------------- | ------------ | ------------------------ | ------------------------------------------------- |
   | Yes              | —            | —                        | Use the named type                                |
   | No               | Yes          | —                        | Ask the user (ODD must be explicit)               |
   | No               | No           | Yes                      | Ask the user before choosing Spike, Bug, or Chore |
   | No               | No           | No                       | Use Feature                                       |

2. Identify each ticket's [anchor](Ticket-Anchoring) — wiki-anchored or codebase-anchored. An anchor the skill cannot determine is settled with the user before drafting.
3. Read what's already in the repo — wiki pages, code, documentation — and reuse existing terminology rather than inventing new names. When a wiki page that informs a ticket carries a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block, the skill stops, surfaces the caution to the user, and waits for instruction. Spike and Bug tickets are exempt — a Spike's purpose is to investigate unresolved design, and a Bug targets existing behaviour rather than committing to the cautioned design.
4. Decide the breakdown. Work that has multiple child tickets belonging together gets an epic file plus individual ticket files with `epic: auto`. Unrelated tickets stand alone. Each ticket represents an independently deliverable piece of work.
5. Batch-write every `.md` file to [`proposed-tickets/`](../../proposed-tickets/), using the matching template as the structural basis.
6. Walk the [Validation](Validation) checklist against each ticket. Items that fail are fixed and the checklist re-run on the revised ticket until every item passes.
7. Delegate to the [ticket-reviewer](../Ticket-Reviewer) subagent, which reviews every file in [`proposed-tickets/`](../../proposed-tickets/). The skill waits for its verdicts before continuing.
8. Act on the review. Files marked `NEEDS WORK` have their listed violations applied and the [Validation](Validation) checklist re-run, then return to the reviewer; this repeats until every file returns `READY` and the summary reports `M of M tickets ready`. A `No tickets to review.` result stops the loop. URLs a `NOTES:` line reports as missing from `.claude/url-resolution.md` are listed to the user once.
9. The ticket set is reported as ready once the reviewer returns all `READY` verdicts.
