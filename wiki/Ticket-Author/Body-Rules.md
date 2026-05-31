# Body Rules

These apply to the body of every ticket:

- Descriptions are actionable — acceptance criteria, context, and scope, written as a real issue.
- Technical decisions (class names, design patterns, library choices, file paths, route paths) are not inferred. They appear in a ticket only when the wiki, existing code, or the user supplies them.
- References to pages, code, or other projects use absolute URLs. References to a sibling ticket created in the same branch use the sibling's planned title as plain text, since no URL exists yet.
- Concepts that already have a name in the wiki or existing code keep that name.
- File references identify locations by content (symbol name, string, or section heading) and link to the file. Line-number anchors (`#L104`, `#L3-6`) are not used.
- Implementation Approach orients the developer with patterns, existing implementations, and key decisions referenced by concrete anchors (files, classes, wiki pages). It does not prescribe imperative steps, whether numbered or bulleted. Bullets that carry structural facts about layout or shape are fine. Every Scope item is reachable from the Approach.
- A reference to an existing implementation names what to take from it and what to change. Single verbs (mirror, match, follow, reference) are not used. Class names follow the class's role: infrastructure names (base classes, configs, converters) come with the borrowed structure; domain names (entities, repositories, services) are renamed to the ticket's domain.
- What a ticket body carries depends on its [anchor](Ticket-Anchoring). A wiki-anchored ticket links the wiki page that holds the why and carries no motivational rationale — business case, user impact, or strategic priority; if no such page exists, the skill suggests creating one. A codebase-anchored ticket carries causal-mechanical detail — sequencing constraints, invariants, and the dependencies the executing agent needs — and no motivational rationale; a ticket that needs business case or user impact to make sense is wiki-anchored.
- Spec detail owned by a referenced source is not duplicated. Tickets list scope only — names, structural decisions, enum or constant values — and link the source of truth: the wiki page for a wiki-anchored ticket, another ticket or a code file for a codebase-anchored one.
- Material from a wiki page carrying a top-of-page [`> [!CAUTION]`](../Wiki-Page-Author/Page-Investigation-Caution) block does not appear in Scope, Implementation Approach, or Acceptance Criteria. It is routed to `Out of Scope` when the ticket has no dependency on it, or to `Risks` when the ticket still has exposure to the cautioned design.
- Each acceptance criterion is a falsifiable check a reviewer can perform. Restated scope, project-wide baselines (build, lint, test), and subjective judgements are not acceptance criteria.
- Risks entries point at concrete exposure outside the ticket's control — a dependency on unconfirmed design, an upstream migration with no fixed date, or a cautioned wiki page whose outcome could change scope. Material fully excluded via Out of Scope does not appear in Risks.
- Testing sections name behaviours that must have coverage, not specific cases, edges, frameworks, or file paths. Bug tickets always include a regression for the reproduction case.
- ODD tickets request resolution of an existing wiki ODD, and are always wiki-anchored. They close when the wiki ODD is [resolved](../Wiki-Page-Author/Open-Design-Decision#resolving-an-open-design-decision).
