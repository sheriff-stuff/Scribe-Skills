---
title: Note
category: domain
owners: [product-team]
last_updated: 2026-04-12
---

# Note

## Purpose

The user-facing artifact that brings together a Recording, its Transcript, and its Extraction. The Note is what the user opens, edits, and (in future) shares.

## Fields

- `id` — ULID.
- `recording_id` — FK.
- `transcript_id` — FK.
- `extraction_id` — FK.
- `template_version` — denormalised pin of the Template version used for this Note's Extraction.
- `title` — user-editable, defaults to the Extraction's first Topic title.
- `tags` — list of strings.
- `transcript_overlay` — JSON document holding user-applied edits to Transcript text.
- `created_at` / `updated_at`.

## Editing semantics

The Note is the only place where user edits land. Edits to Transcript text are stored as overlays so the original ASR output is preserved. Edits to Extraction content are first-class fields on the Note, not the Extraction (because re-running Extraction must not silently overwrite the user's manual changes).

## Related

- [Notes Service](../services/notes-service)
- [Notes Explorer](../frontend/notes-explorer)
- [Transcript Viewer](../frontend/transcript-viewer)
