# Workflow

1. Targets come only from explicit paths in the invocation message. The subagent does not infer targets from the skill name, prior conversation, or wiki layout. For folder paths, the subagent globs the `*.md` files directly inside.
2. If no paths were supplied, the subagent returns exactly the plain-text sentence `No paths supplied. Pass one or more wiki page paths to review.` (no blockquote, no code fences, no other markdown) and stops without globbing, reading, or reviewing anything.
3. Read the [page template](../../.claude/skills/wiki-page-author/assets/page-template.md) as the source of truth for required scaffolding and placeholder syntax.
4. Read every target file in full before producing any verdicts.
5. Read [`wiki/index.md`](../index) or [`wiki/home.md`](../home) (whichever exists) to verify each target page is linked from one of them.
6. Emit one verdict block per file, then a final summary block.
