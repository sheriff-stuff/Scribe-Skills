# Checks

- **Frontmatter** — required `title`, accepted `type` values, `epic` field semantics, list-field formats.
- **File naming** — kebab-case, named by subject (not generic like `feature.md` or `ticket-1.md`).
- **Template structure** — required sections of the appropriate template are present. Optional sections (e.g. User Story, Context when epic-linked) are not flagged when legitimately omitted.
- **Body Rules** — every Body Rule from the [Ticket Author](../Ticket-Author) skill.
- **Cross-ticket** — at most one `epic` file per batch; child tickets use `epic: auto` only when an epic file is present in the batch.
