# Body Rules

- Descriptions are actionable — acceptance criteria, context, and scope, written as a real issue.
- Technical decisions (class names, design patterns, library choices, file paths, route paths) are not inferred. They appear in a ticket only when the wiki, existing code, or the user supplies them.
- References to pages, code, or other projects use absolute URLs.
- Concepts that already have a name in the wiki or existing code keep that name.
- File references identify locations by content (symbol name, string, or section heading) and link to the file. Line-number anchors (`#L104`, `#L3-6`) are not used.
- Implementation Approach orients the developer with patterns, existing implementations, and key decisions. It does not prescribe step-by-step instructions or copyable code. Approaches use _mirror_, not _copy_, and every Scope item is reachable from the Approach.
- Rationale lives in the wiki, not in ticket bodies. Tickets link to the wiki page that holds the why; if no such page exists, the skill suggests creating one.
- References to supporting docs are inline at the point of mention. Epics additionally carry a mandatory Source Documentation section at the top, listing the wiki page(s) or spec(s) driving the epic.
- Spec detail owned by a referenced doc is not duplicated. Tickets list scope only — names, structural decisions, enum or constant values, non-obvious gotchas — and link the source of truth.
- Material from a wiki page carrying a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block does not appear in Scope, Implementation Approach, or Acceptance Criteria. By default it is routed to `Out of Scope` or `Risks` with a link back to the cautioned page. Treating a cautioned page as ground truth requires explicit user authorization.
- Each acceptance criterion is a falsifiable check a reviewer can perform. Restated scope, project-wide baselines (build, lint, test), and subjective judgements are not acceptance criteria.
- Testing sections name behaviours that must have coverage, not specific cases, edges, frameworks, or file paths. Bug tickets always include a regression for the reproduction case.
- References to a sibling ticket created in the same branch use the sibling's planned title from its frontmatter, not a generic phrase ("another ticket", "a separate ticket", "a follow-up ticket").
- ODD tickets request resolution of an existing wiki ODD. They close when the wiki ODD is [resolved](../Wiki-Page-Author/Open-Design-Decision#resolving-an-open-design-decision).
