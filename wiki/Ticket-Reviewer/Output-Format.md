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

The `UNVERIFIED:` block is emitted only when a check could not be run for that file — for example, the **Don't duplicate spec detail from the source doc** check when one of the ticket's linked sources could not be read, or the cross-ticket checks when the set under review is a single file. When every check ran, the block is omitted. A `VERDICT: READY` alongside an `UNVERIFIED:` line means no violations among the checks that could run — not that the file was fully verified.

A final summary block follows:

```
NOTES: <optional one-line batch-level observation, omit the line entirely if none>
N of M tickets ready.
```

The numeric line is required and matches that exact format. `N` is the count of `VERDICT: READY` files and `M` the total reviewed, both derived from the verdicts above so the tally cannot contradict them. The `NOTES:` line is emitted when:

- a batch-level pattern emerges — for example, multiple tickets violating the same Body Rule or cross-ticket structural issues, or
- a URL in the batch could not be read — the fetch failed, or project policy blocked it with no local alternative — and the unreadable URLs are named so they can be checked by hand.

A clean ticket gets an empty `VIOLATIONS:` list and `VERDICT: READY`.
