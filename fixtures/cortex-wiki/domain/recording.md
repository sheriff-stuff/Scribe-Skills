---
title: Recording
category: domain
owners: [platform-team]
last_updated: 2026-04-12
---

# Recording

## Purpose

A Recording wraps an audio source ingested into Cortex along with its metadata. It is the entry point for the Pipeline.

## Fields

- `id` — ULID.
- `media_path` — absolute path to the original media file on disk.
- `media_hash` — SHA-256 of the original media. Detects duplicates on re-upload.
- `duration_seconds` — measured at ingest, not user-supplied.
- `format` — container format (mp3, m4a, wav, mp4, webm).
- `sample_rate_hz` — measured.
- `channels` — measured.
- `recorded_at` — user-supplied timestamp; defaults to file mtime.
- `created_at` — ingest time.

## Lifecycle

Recordings are created by the Ingest Service and are **immutable** after creation. User-visible fields such as title and tags live on the associated Note, not on the Recording.

## Related

- [Ingest Service](../services/ingest-service)
- [Transcript](transcript) — one per Recording.
- [Note](note) — one per Recording, user-facing.
