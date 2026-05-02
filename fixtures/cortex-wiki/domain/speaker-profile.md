---
title: Speaker Profile
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Speaker Profile

## Purpose

A persistent identity that an Utterance can be attributed to. Speaker Profiles span Recordings — naming `Tag-1` as 'Priya' once should let Cortex auto-resolve Priya's voice in subsequent Recordings.

## Fields

- `id` — ULID.
- `display_name` — user-supplied.
- `voice_embedding` — fixed-length vector used to match new Speaker Tags to known Profiles.
- `embedding_version` — model version that produced the embedding.
- `created_at` / `updated_at`.

## Resolution

When a new Transcript arrives, the Notes Service compares each Speaker Tag's voice embedding to existing Speaker Profiles. Matches above the configured similarity threshold are auto-resolved; below it the Tag is left unresolved and surfaced for the user to name.

## Related

- [Utterance](utterance)
- [Diarization Service](../services/diarization-service)
- [Notes Service](../services/notes-service)
