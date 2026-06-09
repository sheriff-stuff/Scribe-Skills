# Output Format

The subagent's entire response is the verdict blocks plus the final summary block. No preamble, no analysis text outside those blocks, no mid-stream self-corrections. If a verdict turns out wrong mid-output, the subagent re-emits only the corrected block.

One block per file:

```
FILE: <relative path>
VERDICT: READY | NEEDS WORK
VIOLATIONS:
  - Rule: <body rule name from the [Wiki Page Author](../Wiki-Page-Author) skill, or one of: ODD, CAUTION, Naming, Template, Cross-page, Index sync>
    Line: <line number, or range like 12-15; omitted for whole-file issues>
    Where: "<verbatim offending text, or section name if structural>"
    Why: <one sentence>
    Fix: <concrete, minimal>
UNVERIFIED:
  - <check name> — <why it could not be run for this file>
```

The `UNVERIFIED:` block is emitted only when a check could not be run for that file — the [Cross-page check](Checks) when an owner page behind a pointer could not be read, or the [Index sync check](Checks) when the wiki index could not be located. When every check ran, the block is omitted. A `VERDICT: READY` alongside an `UNVERIFIED:` line means no violations among the checks that could run — not that the page was fully verified.

A final summary block follows:

```
NOTES: <optional one-line batch-level observation, omit the line entirely if none>
N of M pages ready.
```

The numeric line is required and matches that exact format. `N` is the count of `VERDICT: READY` files and `M` the total reviewed, both derived from the verdicts above. The `NOTES:` line is emitted when a batch-level pattern is worth flagging, or when a target's owner page or the wiki index could not be read — each named so it can be checked by hand.

A clean page gets `VIOLATIONS: (none)` on a single line in place of the bulleted list, and `VERDICT: READY`.
