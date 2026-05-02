---
title: Ingest Service
category: services
owners: [platform-team]
last_updated: 2026-04-12
---

# Ingest Service

## Responsibility

Owns Recording intake: validation, deduplication, and persistence of the original media file. The only writer to Recording rows.

## Inputs

An uploaded media file plus optional user-supplied metadata (title hint, recorded-at timestamp, tags).

## Outputs

A Recording row plus a media file written to the configured media directory. Emits a `recording.created` event consumed by the Job Orchestrator to queue the transcription Job.

## Validation rules

- Rejects unsupported formats.
- Rejects files larger than the configured limit (default 1 GB).
- Detects duplicates by content hash and returns the existing Recording instead of creating a new one. Duplicate detection is opt-out per upload.

## Failure modes

Validation failures surface synchronously as HTTP errors. Storage failures (out of disk, permission denied) surface as HTTP 500 with a user-actionable message in the body.

## Related

- [Recording](../domain/recording)
- [Job Orchestrator](job-orchestrator)
