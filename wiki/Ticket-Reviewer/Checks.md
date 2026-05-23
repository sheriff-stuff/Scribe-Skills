# Checks

- **Frontmatter** — against the [Frontmatter Schema](../Ticket-Author/Frontmatter-Schema). A missing or unrecognised `type` field is flagged as a Frontmatter violation.
- **File naming** — against the [File Naming](../Ticket-Author/File-Naming) rule.
- **Template structure** — sections marked mandatory in the matching template are present. Conditional and optional sections, marked inline in the template, are not flagged when legitimately omitted. When the type is unrecognised and no matching template exists, Template checks are skipped for that file and the verdict carries `Where: "Template checks skipped: unknown type"`.
- **Body Rules** — every [Body Rule](../Ticket-Author/Body-Rules) from the [Ticket Author](../Ticket-Author) skill.
- **Cross-ticket** — at most one `epic` file per batch; child tickets use `epic: auto` only when an epic file is present in the batch.
