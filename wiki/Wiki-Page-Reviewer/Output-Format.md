# Output Format

One block per file:

```
FILE: <relative path>
VERDICT: READY | NEEDS WORK
VIOLATIONS:
  - Rule: <Body Rule N | ODD | CAUTION | Naming | Template | Cross-page | Index sync>
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
