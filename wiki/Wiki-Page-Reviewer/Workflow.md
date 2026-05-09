# Workflow

1. Resolve the paths supplied in the invocation. For folders, glob the `*.md` files directly inside.
2. If no paths were supplied, return the sentence `No paths supplied. Pass one or more wiki page paths to review.` as plain text (no blockquote, no code fences, no other markdown) and stop.
3. Read every target file in full before producing any verdicts.
4. For every `> [!ODD]` or `> [!CAUTION]` pointer block in the targets, read the owner page so the anchor and (for ODDs) the `Affects:` line can be verified.
5. Read [`wiki/index.md`](../index) or [`wiki/home.md`](../home) (whichever exists) to verify each target page is linked from one of them.
6. Emit one verdict block per file, then a final summary block.
