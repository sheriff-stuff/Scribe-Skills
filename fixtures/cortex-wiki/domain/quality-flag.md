---
title: Quality Flag
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Quality Flag

## Purpose

An automatic annotation produced by the Audio Quality Service that warns of issues affecting transcription accuracy. Flags are advisory, not blocking.

## Fields

- `id` — ULID.
- `recording_id` — FK.
- `kind` — one of `low_snr`, `overlap`, `silence`, `clipping`, `low_confidence`.
- `severity` — `info`, `warning`, `error`.
- `start_ms` / `end_ms` — bounded range within the Recording, inclusive of any later Utterance boundaries.
- `message` — short user-facing string.

## Where they appear

Quality Flags surface in the Notes Explorer as a small badge on affected Notes, and in the Transcript Viewer as inline highlights on the affected ranges.

## Related

- [Audio Quality Service](../services/audio-quality-service)
