---
title: Transcript
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Transcript

## Purpose

A speaker-attributed record of speech in a Recording, represented as an ordered list of Utterances.

## Fields

- `id` — ULID.
- `recording_id` — FK to Recording.
- `language` — auto-detected ISO 639-1 code.
- `model_version` — ASR model version used.
- `created_at` — when transcription completed.
- `utterances` — ordered list of Utterance rows.

## Lifecycle

Created by the Transcription Service after ASR completes. Utterances are appended (not edited) by the Diarization Service in a follow-up step. After diarization the Transcript is sealed; subsequent edits go through the Notes Service and produce a new revision rather than mutating the Transcript in place.

## Editing model

User edits to Transcript text are stored as overlays owned by the Note. The original Transcript is preserved verbatim so that re-running Extraction always sees the model's output, not the user's.

## Related

- [Utterance](utterance)
- [Transcription Service](../services/transcription-service)
- [Diarization Service](../services/diarization-service)
