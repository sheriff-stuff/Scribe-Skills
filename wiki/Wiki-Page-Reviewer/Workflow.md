# Workflow

1. Targets come only from explicit paths in the invocation message. The subagent does not infer targets from the skill name, prior conversation, or wiki layout. For folder paths, the subagent globs the `*.md` files directly inside.
2. If no paths were supplied, the subagent returns exactly the plain-text sentence `No paths supplied. Pass one or more wiki page paths to review.` (no blockquote, no code fences, no other markdown) and stops without globbing, reading, or reviewing anything.
3. Read every target file in full before producing any verdicts.
4. For every pointer `> [!ODD]` block in the targets, follow its link to the owner page and read it so the owner ODD and its `Affects:` list can be verified.
5. Walking up from the directory containing any target page, find the first ancestor directory containing `index.md`, `home.md`, or both — that is the wiki root. Whichever of the two files exist there are read. Each target page is linked from one of them. If no ancestor directory contains either file, a batch-level `NOTES:` entry records that no wiki index was found and the Index sync check is skipped.
6. The checks are walked at least twice before any verdict is emitted. The first pass drafts verdicts internally. The second pass re-walks every rule in [Checks](Checks) against every target with the draft in hand, looking for violations the first pass missed, rules applied inconsistently across the batch, and interactions between rules (e.g. a sentence that is both a hedge and a rationale; a pointer block whose owner page is also a target). Passes continue until a full walk produces no new findings. Iteration is internal — none of it appears in the output.
7. Emit one verdict block per file, then a final summary block.
