---
title: Utterance
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Utterance

## Purpose

The smallest indexable unit of transcribed speech. All citations from an Extraction back into the Transcript reference Utterances by ID.

## Fields

- `id` — ULID.
- `transcript_id` — FK.
- `index` — ordinal within the Transcript (0-based).
- `start_ms` / `end_ms` — timestamps relative to the Recording start.
- `text` — the transcribed text.
- `speaker_tag` — provisional label assigned by diarization.
- `speaker_profile_id` — FK to Speaker Profile, nullable until resolved.
- `confidence` — ASR confidence score, 0.0–1.0.

## Granularity

An Utterance is roughly one continuous spoken phrase, typically 1–15 seconds. It is not a sentence and not a single word — it is whatever the ASR engine emits as a contiguous segment with a single speaker.

## Related

- [Transcript](transcript)
- [Speaker Profile](speaker-profile)
