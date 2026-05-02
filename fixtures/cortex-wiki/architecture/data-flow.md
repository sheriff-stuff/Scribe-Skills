---
title: Data Flow
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Data Flow

## Purpose

Describes which service produces or mutates which artifact, and how artifacts reference each other in storage.

## Producers

- **Recording** — written by the Ingest Service. Immutable after creation; metadata edits (title, tags) happen on the associated Note rather than on the Recording itself.
- **Transcript** — written by the Transcription Service; appended to by the Diarization Service.
- **Extraction** — written by the Extraction Service.
- **Note** — written and edited exclusively by the Notes Service.
- **Template** — written by the Template Service.
- **Job** — written by the Job Orchestrator.
- **Quality Flag** — written by the Audio Quality Service.

## References

- Each Transcript references exactly one Recording.
- Each Utterance references exactly one Speaker Tag and (after resolution) one Speaker Profile.
- Each Extraction references exactly one Transcript and one Template version.
- Each Topic, Decision, and Action Item references one or more Utterances by ID.
- Each Note references one Recording, one Transcript, one Extraction, and (snapshotted) one Template version.

## Citation guarantee

Every Topic, Decision, and Action Item must cite at least one Utterance. The Extraction Service rejects any LLM output that fails this check; downstream UI may assume citations are always present.
