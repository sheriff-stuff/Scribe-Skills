# Checks

The checks the ticket-reviewer subagent applies to each file under review.

- **Frontmatter** — against the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema). A missing `type` field is flagged as a Frontmatter violation.
- **File naming** — against the [File Naming](../Ticket-Author/File-Naming) rule.
- **Template structure** — sections marked mandatory in the matching template are present. Conditional and optional sections, marked inline in the template, are not flagged when legitimately omitted.
- **Anchor** — each ticket is wiki-anchored or codebase-anchored and the body matches the [anchor](../Ticket-Author/Ticket-Anchoring). The choice is judged for correctness, not just consistency: a codebase-anchored ticket that would need a business case, user impact, or domain rationale to justify the work is mislabelled.
- **Body Rules** — every [Body Rule](../Ticket-Author/Body-Rules) from the [Ticket Author](../Ticket-Author) skill.
- **Risks** — entries name concrete exposure outside the ticket's control, not generic caveats. Applies when a Risks section is present.
- **ODD** — ODD tickets resolve an existing wiki ODD; the `Resolve [ODD-…]` line links the ODD ID to its owner wiki page.
- **Cross-ticket** — at most one `epic` file per batch; child tickets use `epic: auto` only when an epic file is present in the batch; no file sets both `type: epic` and `epic:`, since an epic is not a child of another epic.
