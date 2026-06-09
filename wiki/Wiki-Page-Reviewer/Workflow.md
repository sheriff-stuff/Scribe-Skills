# Workflow

The steps the wiki-page-reviewer subagent follows to review the pages passed to it.

1. Targets come only from explicit paths in the invocation message — the subagent does not infer them from the skill name, prior conversation, or wiki layout. For folder paths it globs the `*.md` files directly inside. When no paths are supplied, it reads nothing, calls no tool, and returns exactly the plain-text sentence `No paths supplied. Pass one or more wiki page paths to review.`
2. Read every target file in full before producing any verdicts, so cross-page rules can be applied across the batch.
3. For every pointer `> [!ODD]` block in the targets, follow its link to the owner page and read it, so the owner ODD and its `Affects:` list can be verified. When an owner page cannot be read, the [Cross-page check](Checks) is marked `UNVERIFIED` for the file carrying that pointer.
4. Locate the wiki index by walking up from a target to the nearest directory containing `index.md`, `home.md`, or both, and confirm each target is linked from it. When no such directory exists, the [Index sync check](Checks) is marked `UNVERIFIED` and named in the batch `NOTES:` line.
5. Draft a verdict for each target by applying every [check](Checks), then re-walk every check against every target with the draft in hand — looking for violations the first pass missed, rules applied inconsistently across the batch, and interactions between rules (e.g. a sentence that is both a hedge and a rationale; a pointer block whose owner page is also a target). Iteration continues until a walk produces no new findings and is internal — none of it appears in the output.
6. Emit one verdict block per file, then a final summary block.
