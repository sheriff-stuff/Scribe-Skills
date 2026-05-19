# Output Format

The subagent's entire response is the verdict blocks plus the final summary block. No preamble, no analysis text outside those blocks, no mid-stream self-corrections. If a verdict turns out wrong mid-output, the subagent re-emits only the corrected block.

One block per file:

```
FILE: <relative path>
VERDICT: READY | NEEDS WORK
VIOLATIONS:
  - Rule: <body rule name from the [Wiki Page Author](../Wiki-Page-Author) skill, or one of: ODD, CAUTION, Template, Cross-page, Index sync>
    Line: <line number, or range like 12-15; omitted for whole-file issues>
    Where: "<verbatim offending text, or section name if structural>"
    Why: <one sentence>
    Fix: <concrete, minimal>
```

A final summary block follows:

```
NOTES: <optional one-line batch-level observation, omit the line entirely if none>
N of M pages ready.
```

The numeric line is required and matches that exact format. The `NOTES:` line is emitted only when a batch-level pattern is worth flagging.

A clean page gets `VIOLATIONS: (none)` on a single line in place of the bulleted list, and `VERDICT: READY`.
