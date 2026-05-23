# Workflow

1. Understand the request and determine how many tickets are needed. The skill chooses each ticket's type using this decision table; epic is decided in step 3.

   | User named type? | Type is ODD? | Type is Spike/Bug/Chore? | Action                                            |
   | ---------------- | ------------ | ------------------------ | ------------------------------------------------- |
   | Yes              | —            | —                        | Use the named type                                |
   | No               | Yes          | —                        | Ask the user (ODD must be explicit)               |
   | No               | No           | Yes                      | Ask the user before choosing Spike, Bug, or Chore |
   | No               | No           | No                       | Use Feature                                       |

2. Read what's already in the repo — wiki pages, code, documentation — and reuse existing terminology rather than inventing new names. When a wiki page that informs a ticket carries a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block, the skill stops, surfaces the caution to the user, and waits for instruction. Spike and Bug tickets are exempt — a Spike's purpose is to investigate unresolved design, and a Bug targets existing behaviour rather than committing to the cautioned design.
3. Decide the breakdown. Work that has multiple child tickets belonging together gets an epic file plus individual ticket files with `epic: auto`. Unrelated tickets stand alone. Each ticket represents an independently deliverable piece of work.
4. Batch-write every `.md` file to [`proposed-tickets/`](../../proposed-tickets/), using the matching template as the structural basis.
5. Walk the [Validation](Validation) checklist against each ticket. Items that fail are fixed and the checklist re-run on the revised ticket. Failures that depend on information only the user can provide are surfaced in one message rather than asked piecemeal.
