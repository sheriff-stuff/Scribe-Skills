---
title: Service Map
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Service Map

## Purpose

Names every backend service, what it owns, and what it depends on. If a responsibility doesn't fit into one of the services listed here, that is a sign the shape needs revisiting — discuss before adding a new service.

## Services

- [Ingest Service](../services/ingest-service) — owns Recording intake and validation.
- [Transcription Service](../services/transcription-service) — produces a Transcript from a Recording.
- [Diarization Service](../services/diarization-service) — assigns Speaker Tags to Utterances.
- [Extraction Service](../services/extraction-service) — produces an Extraction from a Transcript.
- [Template Service](../services/template-service) — owns Template CRUD and version pinning.
- [Notes Service](../services/notes-service) — assembles, edits, and queries Notes.
- [Job Orchestrator](../services/job-orchestrator) — queues, runs, and reports Jobs.
- [Audio Quality Service](../services/audio-quality-service) — annotates Recordings with Quality Flags.

## Dependency rules

- The Job Orchestrator is the only service permitted to call Transcription, Diarization, Extraction, and Audio Quality Services directly. Other services must go through it.
- The Notes Service is the sole writer to Note records. Other services may read, but never mutate.
- The Ingest Service is the sole writer to Recording records.
- The Template Service is the sole writer to Template records, and the Extraction Service is the only consumer.

## Cross-cutting

All services share a common storage layer (see [Storage Layer](storage-layer)) and emit progress events to the realtime channel described in [Realtime Progress](realtime-progress).
