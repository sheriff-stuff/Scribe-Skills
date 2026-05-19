# Checks

- **Frontmatter** — against the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema).
- **File naming** — against the [File Naming](../Ticket-Author/File-Naming) rule.
- **Template structure** — sections marked mandatory in the matching template are present. Conditional and optional sections, marked inline in the template, are not flagged when legitimately omitted.
- **Body Rules** — every [Body Rule](../Ticket-Author/Body-Rules) from the [Ticket Author](../Ticket-Author) skill.
- **Cross-ticket** — at most one `epic` file per batch; child tickets use `epic: auto` only when an epic file is present in the batch.
