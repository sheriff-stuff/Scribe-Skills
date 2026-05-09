# Ticket Author

The ticket-author skill writes ticket proposal files to [`proposed-tickets/`](../proposed-tickets/). Each file becomes a GitLab issue (or epic) when the MR merges to main. The skill does not create branches, commits, or MRs.

## Triggers

- The user asks to create, draft, or write tickets.
- The user asks to break work into tickets, breakdown an epic, or plan work as GitLab issues.
- The user asks to write an epic, propose or scope work items, or create a spike or bug ticket.

## Ticket types

- Epic
- Feature
- Spike
- Bug

Each type has a template under [`.claude/skills/ticket-author/assets/`](../.claude/skills/ticket-author/assets/).

## Workflow

1. Clarify what the user wants to accomplish, how many tickets are needed, whether an epic is appropriate, and the type of each ticket.
2. Read what's already in the repo — wiki pages, code, documentation — and reuse existing terminology rather than inventing new names.
3. Decide the breakdown. Work that has multiple child tickets belonging together gets an epic file plus individual ticket files with `epic: auto`. Unrelated tickets stand alone. Each ticket represents an independently deliverable piece of work.
4. Batch-write every `.md` file to [`proposed-tickets/`](../proposed-tickets/), using the matching template as the structural basis.
5. Tell the user the files are ready for review.

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

## File naming

File names are lowercase kebab-case, named by subject. One epic file per MR maximum.

## Body rules

- Descriptions are actionable — acceptance criteria, context, and scope, written as a real issue.
- Technical decisions (class names, design patterns, library choices, file paths, route paths) are not inferred. They appear in a ticket only when the wiki, existing code, or the user supplies them.
- References to pages, code, or other projects use absolute URLs.
- Concepts that already have a name in the wiki or existing code keep that name.
- Implementation Approach orients the developer with patterns, existing implementations, and key decisions. It does not prescribe step-by-step instructions or copyable code.
- Rationale lives in the wiki, not in ticket bodies. Tickets link to the wiki page that holds the why; if no such page exists, the skill suggests creating one.
- Spec detail owned by a referenced doc is not duplicated. Tickets list scope only — names, structural decisions, enum or constant values, non-obvious gotchas — and link the source of truth.
- Each acceptance criterion is a falsifiable check a reviewer can perform. Restated scope, project-wide baselines (build, lint, test), and subjective judgements are not acceptance criteria.

## Related

- [Wiki Page Author](Wiki-Page-Author)
- [Home](home)
