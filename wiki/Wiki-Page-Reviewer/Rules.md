# Rules

- Output is the verdict blocks and the final summary block — nothing else. No preamble, no analysis text outside those blocks, no mid-stream self-corrections. If the subagent changes its mind, it re-emits only the corrected block.
- Offending text is quoted verbatim. Critique is never abstract.
- One verdict per file. `NEEDS WORK` if any violation is found, regardless of severity.
- The subagent does not rewrite pages. Fixes belong to the main conversation.
- A clean page gets an empty `VIOLATIONS:` list and `VERDICT: READY` — no praise.
- Batch-level observations (every page hedging, every page missing the H1 description comment) surface in the `NOTES:` line above the numeric summary.
- Body Rule citations use the rule number from the [Wiki Page Author](../Wiki-Page-Author) skill (e.g. `Body Rule 4`). Other violations use these category labels: `ODD`, `CAUTION`, `Naming`, `Template`, `Cross-page`, `Index sync`.
