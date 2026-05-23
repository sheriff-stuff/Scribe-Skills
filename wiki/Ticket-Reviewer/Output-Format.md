# Output Format

One block per file:

```
FILE: <relative path>
VERDICT: READY | NEEDS WORK
VIOLATIONS:
  - Rule: <body rule name from the [Ticket Author](../Ticket-Author) skill, or one of: Frontmatter, Naming, Template, Cross-ticket>
    Line: <line number or range; omitted for whole-file issues>
    Where: "<verbatim offending text, or section name if structural>"
    Why: <one sentence>
    Fix: <minimal pointer to the problem; fixes are suggestions only and belong to the main conversation>
```

Within each file block, violations are listed in this order: Frontmatter, Naming, Template, Body Rules, Cross-ticket.

A final summary block follows:

```
NOTES: <optional one-line batch-level observation, omit the line entirely if none>
N of M tickets ready.
```

The numeric line is required and matches that exact format. The `NOTES:` line is emitted only when a batch-level pattern emerges — for example, multiple tickets violating the same Body Rule or cross-ticket structural issues.

A clean ticket gets an empty `VIOLATIONS:` list and `VERDICT: READY`.
