# Body Rules

- Descriptions are actionable — acceptance criteria, context, and scope, written as a real issue.
- Technical decisions (class names, design patterns, library choices, file paths, route paths) are not inferred. They appear in a ticket only when the wiki, existing code, or the user supplies them.
- References to pages, code, or other projects use absolute URLs. References to a sibling ticket created in the same branch use the sibling's planned title as plain text, since no URL exists yet.
- Concepts that already have a name in the wiki or existing code keep that name.
- File references identify locations by content (symbol name, string, or section heading) and link to the file. Line-number anchors (`#L104`, `#L3-6`) are not used.
- Implementation Approach orients the developer with patterns, existing implementations, and key decisions referenced by concrete anchors (files, classes, wiki pages). It does not prescribe imperative steps, whether numbered or bulleted. Bullets that carry structural facts about layout or shape are fine. Every Scope item is reachable from the Approach.
- A reference to an existing implementation names what to take from it and what to change. Single verbs (mirror, match, follow, reference) are not used — they leave the executing agent guessing how closely to copy. Class names follow the class's role: infrastructure names (base classes, configs, converters) come with the borrowed structure; domain names (entities, repositories, services) are renamed to the ticket's domain.
- Rationale lives in the wiki, not in ticket bodies. Tickets link to the wiki page that holds the why; if no such page exists, the skill suggests creating one.
- Spec detail owned by a referenced doc is not duplicated. Tickets list scope only — names, structural decisions, enum or constant values — and link the source of truth.
- Material from a wiki page carrying a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block does not appear in Scope, Implementation Approach, or Acceptance Criteria. It is routed to `Out of Scope` when the ticket has no dependency on it, or to `Risks` when the ticket still has exposure to the cautioned design.
- Each acceptance criterion is a falsifiable check a reviewer can perform. Restated scope, project-wide baselines (build, lint, test), and subjective judgements are not acceptance criteria.
- Risks entries point at concrete exposure outside the ticket's control — a dependency on unconfirmed design, an upstream migration with no fixed date, or a cautioned wiki page whose outcome could change scope. Material fully excluded via Out of Scope does not appear in Risks.
- Testing sections name behaviours that must have coverage, not specific cases, edges, frameworks, or file paths. Bug tickets always include a regression for the reproduction case.
- ODD tickets request resolution of an existing wiki ODD. They close when the wiki ODD is [resolved](../Wiki-Page-Author/Open-Design-Decision#resolving-an-open-design-decision).
