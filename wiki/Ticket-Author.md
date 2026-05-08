# Ticket Author

The ticket-author skill writes ticket proposal files to [`proposed-tickets/`](../proposed-tickets/). Each file becomes a GitLab issue (or epic) when the MR merges to main. The skill does not create branches, commits, or MRs.

Each ticket is a prompt for Claude Code: combined with the wiki and the codebase, it drives an LLM agent to produce code and a PR.

## Triggers

- The user asks to create, draft, or write tickets.
- The user asks to break work into tickets, breakdown an epic, or plan work as GitLab issues.
- The user asks to write an epic, propose or scope work items, or create a spike, bug, or chore ticket.

## Ticket types

- Epic
- Feature
- Spike
- Bug
- Chore

Each type has a template under [`.claude/skills/ticket-author/assets/`](../.claude/skills/ticket-author/assets/).

## Workflow

1. Clarify what the user wants to accomplish, how many tickets are needed, whether an epic is appropriate, and the type of each ticket.
2. Read what's already in the repo — wiki pages, code, documentation — and reuse existing terminology rather than inventing new names. When a wiki page that informs a ticket carries a top-of-page [`> [!CAUTION]`](Wiki-Page-Author/Page-Investigation-Caution) block, the skill stops, surfaces the caution to the user, and offers to route the page's material into `Out of Scope` or `Risks` (each with a link back to the cautioned page). The rule applies to Epic, Feature, Chore, and Spike tickets; Spikes and bugs are exempt.
3. Decide the breakdown. Work that has multiple child tickets belonging together gets an epic file plus individual ticket files with `epic: auto`. Unrelated tickets stand alone. Each ticket represents an independently deliverable piece of work.
4. Batch-write every `.md` file to [`proposed-tickets/`](../proposed-tickets/), using the matching template as the structural basis.

## Frontmatter schema

| Field       | Required | Type                | Notes                                                                           |
| ----------- | -------- | ------------------- | ------------------------------------------------------------------------------- |
| `title`     | Yes      | string              | Non-empty                                                                       |
| `type`      | No       | string              | Only accepted value is `epic`                                                   |
| `labels`    | No       | list                | Each label must already exist in the project                                    |
| `assignees` | No       | list                | GitLab usernames                                                                |
| `milestone` | No       | string              | Milestone title or ID                                                           |
| `weight`    | No       | integer             | Non-negative                                                                    |
| `due_date`  | No       | string              | `YYYY-MM-DD`                                                                    |
| `epic`      | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same MR |

List fields (`labels`, `assignees`) accept YAML inline `[a, b]` or block format.

## Labels

Labels follow GitLab's scoped-label convention (`scope::value`). Every ticket carries:

- `type::<kind>` — set by the template (`type::feature`, `type::bug`, `type::spike`, `type::chore`, `type::epic`).
- `area::<name>` — the part of the system the work touches (`area::backend`, `area::frontend`, `area::infra`). Areas reuse names already in use in the project; new ones are not invented when a matching label exists.

Bug tickets additionally carry `severity::*`, `env::*`, and `network::*` scoped labels.

## File naming

File names are lowercase kebab-case, named by subject. One epic file per MR maximum.

## Body rules

- Descriptions are actionable — acceptance criteria, context, and scope, written as a real issue.
- Technical decisions (class names, design patterns, library choices, file paths, route paths) are not inferred. They appear in a ticket only when the wiki, existing code, or the user supplies them.
- References to pages, code, or other projects use absolute URLs.
- Concepts that already have a name in the wiki or existing code keep that name.
- File references identify locations by content (symbol name, string, or section heading) and link to the file. Line-number anchors (`#L104`, `#L3-6`) are not used.
- Implementation Approach orients the developer with patterns, existing implementations, and key decisions. It does not prescribe step-by-step instructions or copyable code. Approaches use _mirror_, not _copy_, and every Scope item is reachable from the Approach.
- Rationale lives in the wiki, not in ticket bodies. Tickets link to the wiki page that holds the why; if no such page exists, the skill suggests creating one.
- References to supporting docs are inline at the point of mention. Epics additionally carry a mandatory Source Documentation section at the top, listing the wiki page(s) or spec(s) driving the epic.
- Spec detail owned by a referenced doc is not duplicated. Tickets list scope only — names, structural decisions, enum or constant values, non-obvious gotchas — and link the source of truth.
- Material from a wiki page carrying a top-of-page [`> [!CAUTION]`](Wiki-Page-Author/Page-Investigation-Caution) block does not appear in Scope, Implementation Approach, or Acceptance Criteria. By default it is routed to `Out of Scope` or `Risks` with a link back to the cautioned page. Treating a cautioned page as ground truth requires explicit user authorization.
- Each acceptance criterion is a falsifiable check a reviewer can perform. Restated scope, project-wide baselines (build, lint, test), and subjective judgements are not acceptance criteria.
- Testing sections name behaviors that must have coverage, not specific cases, edges, frameworks, or file paths. Bug tickets always include a regression for the reproduction case.

## Related

- [Wiki Page Author](Wiki-Page-Author)
- [Home](home)
