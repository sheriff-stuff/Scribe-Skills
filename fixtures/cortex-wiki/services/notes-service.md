---
title: Notes Service
category: services
owners: [product-team]
last_updated: 2026-04-12
---

# Notes Service

## Responsibility

Assembles, edits, queries, and (eventually) shares Notes. The only writer to Note rows. Resolves Speaker Tags to Speaker Profiles.

## Operations

- `assemble(recording_id)` — composes a Note from the Recording, its latest Transcript, and its latest Extraction.
- `update_note(id, fields...)` — partial update of user-editable fields (title, tags, transcript overlay, edited Extraction items).
- `list_notes(query)` — paginated listing with filters (date range, tag, speaker).
- `delete_note(id)` — deletes the Note **and** its underlying Recording, Transcript, Extraction, and media file.

## Speaker resolution

On Note assembly, the service walks each unresolved Speaker Tag and compares its embedding to all known Speaker Profiles. Matches above the configured similarity threshold (default 0.85) auto-resolve to the Profile; the Tag remains unresolved otherwise.

## Search

The Notes Service does not yet support full-text search. The current `list_notes` implementation filters by tag and date only.

## Related

- [Note](../domain/note)
- [Speaker Profile](../domain/speaker-profile)
