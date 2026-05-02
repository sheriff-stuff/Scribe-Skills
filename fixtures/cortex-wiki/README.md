# Cortex Wiki — fixture

This is a **mock wiki** built for evaluating skills that operate on wiki-like input — currently the [`ticket-creator`](../../ticket-creator/SKILL.md) skill.

## What this is

A fictional, forward-looking design corpus for "Cortex", a local meeting-transcription app loosely modelled on Otter.ai. The wiki describes Cortex as if it were a real internal project: architecture, domain glossary, service responsibilities, ADRs, runbooks, and process docs.

The content is generated from `_generator/outline.py` by `_generator/generate.py`. Editing the generated `.md` files directly is fine for one-off tweaks but the next regeneration will overwrite them — make durable changes in the outline.

## Why it exists

Skills like `ticket-creator` rely on a real wiki to ground their output (pick up existing terminology, defer to source docs, link with absolute URLs, write outcome-based acceptance criteria). Without a wiki the skill has nothing to read, and evals can't exercise the rules that matter most.

Real wikis aren't always shareable or stable, so this fixture stands in. It is deliberately:

- **Internally consistent** — single canonical glossary, no contradictory pages, no deprecated content. The wiki itself is *not* what's being tested; ticket generation is. A messy wiki would noise up the eval signal.
- **Forward-looking** — describes a target system (some built, some not), the same shape as the real workflow these skills are designed for.
- **Skill-agnostic** — sits outside any single skill folder so future skills (wiki-page writer, doc summarizer, etc.) can reuse it.

## How eval prompts use it

Eval prompts reference the fixture by absolute path, the same way they would a real wiki:

> "Cortex's wiki is at `C:\Users\PC\work\Skills\fixtures\cortex-wiki\`. Read it, then draft tickets to add full-text search across notes."

Within an eval run, the wiki is treated as authoritative source-of-truth. If a ticket and the wiki disagree on a term or scope, the wiki wins — that's a deliberate rule from the `ticket-creator` skill (Body Rule 7).

## Layout

```
cortex-wiki/
├── README.md                  # this file
├── _generator/
│   ├── generate.py            # renders the wiki from outline.py
│   └── outline.py             # canonical spec — all pages, glossary, links live here
├── index.md                   # landing page with TOC
├── glossary.md                # canonical vocabulary
├── architecture/              # system shape
├── domain/                    # entities and schemas
├── services/                  # backend service responsibilities
├── frontend/                  # web app structure
├── ops/                       # runbooks, deploy, on-call
├── process/                   # ticket conventions, release process
└── adrs/                      # architectural decision records
```

Internal cross-links are relative paths without the `.md` extension — `[Label](../folder/page)` from a subfolder, `[Label](folder/page)` from the wiki root. The generator rewrites a sentinel inside `outline.py` (`@@WIKI@@/<slug>`) into the correct relative path for each linking page, so editing the outline doesn't require knowing the source page's location.

## Regenerating

From this directory:

```
python _generator/generate.py
```

The generator validates internal links, checks glossary coverage, and writes all markdown files. It is idempotent — running it twice produces identical output.

## Cortex (the real project)

There is a real project called Cortex at `C:\Users\PC\projects\Meeting`. This wiki is loosely shaped by what's there (Python/FastAPI backend, React frontend, two-phase pipeline, Ollama default) but does **not** reuse real file paths, class names, or implementation details. The wiki has its own clean vocabulary (e.g., `Utterance`, `Speaker Profile`, `Extraction`); the real codebase has its own (e.g., `Segment`, `MeetingItem`). Any resemblance is coincidental and intentional only in spirit.
