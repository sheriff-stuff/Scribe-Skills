# Output Format

The subagent returns one verdict block per file, then a final summary block.

Each file block:

```
FILE: <relative path>
VERDICT: READY | NEEDS WORK
VIOLATIONS:
  - Rule: <body rule name from the [Ticket Author](../Ticket-Author) skill, or one of: Frontmatter, Naming, Template, Cross-ticket>
    Line: <line number or range; omitted for whole-file issues>
    Where: "<verbatim offending text, or section name if structural>"
    Why: <one sentence>
    Fix: <minimal pointer to the problem; fixes are suggestions only and belong to the main conversation>
UNVERIFIED:
  - <check name> — <why it could not be run for this file>
```

Within each file block, violations are listed in this order: Frontmatter, Naming, Template, Body Rules, Cross-ticket.

The `UNVERIFIED:` block is emitted only when a check could not be run for that file — for example, the **Don't duplicate spec detail from the source doc** check when the file's source URL has no mapping in `.claude/url-resolution.md`. When every check ran, the block is omitted. A `VERDICT: READY` alongside an `UNVERIFIED:` line means no violations among the checks that could run — not that the file was fully verified.

A final summary block follows:

```
NOTES: <optional one-line batch-level observation, omit the line entirely if none>
N of M tickets ready.
```

The numeric line is required and matches that exact format. The `NOTES:` line is emitted when:

- a batch-level pattern emerges — for example, multiple tickets violating the same Body Rule or cross-ticket structural issues, or
- the consumer project's `.claude/url-resolution.md` is missing — the note prompts the user to create one to enable URL-content checks, or
- URLs in the batch have no mapping in `.claude/url-resolution.md` — the unresolved URLs are named so the mapping can be extended.

A clean ticket gets an empty `VIOLATIONS:` list and `VERDICT: READY`.
