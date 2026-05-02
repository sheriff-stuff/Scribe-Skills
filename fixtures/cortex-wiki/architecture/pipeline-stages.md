---
title: Pipeline Stages
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Pipeline Stages

## Purpose

Walks through the Pipeline phase by phase, naming the service responsible for each stage and the artifact it produces.

## Phase 1 — Transcription

**Stage 1.1 Validate** — The Ingest Service confirms the uploaded file is a supported format and meets size limits. On failure the Recording is rejected before any Job is queued.

**Stage 1.2 Quality scan** — The Audio Quality Service produces Quality Flags for the Recording. Flags are advisory and do not block transcription.

**Stage 1.3 Transcribe** — The Transcription Service produces an ordered list of Utterances with timestamps and confidence scores.

**Stage 1.4 Diarize** — The Diarization Service assigns a Speaker Tag to each Utterance. Tags can be resolved to Speaker Profiles after the fact.

**Output:** a finalised Transcript.

## Phase 2 — Extraction

**Stage 2.1 Template selection** — The Extraction Service loads the Template configured for the Recording.

**Stage 2.2 Chunk** — The Transcript is partitioned into chunks sized for the LLM context window with a configurable overlap (see [ADR: chunked extraction](../adrs/chunked-extraction)).

**Stage 2.3 Extract per chunk** — Each chunk is sent to the LLM with the Template's prompt. The result is a partial Extraction.

**Stage 2.4 Merge and dedupe** — Partial Extractions are merged. Duplicate Topics, Decisions, and Action Items are collapsed using citation overlap.

**Output:** a finalised Extraction.

## Phase 3 — Note assembly

**Stage 3.1** The Notes Service composes a Note from the Recording, Transcript, and Extraction.

**Stage 3.2** The Note is written to storage and published on the realtime channel; the frontend displays it as soon as the event arrives.

## Why two phases

Phase 1 and Phase 2 are decoupled so a finished Transcript is preserved even if Extraction fails, fails partway, or the user re-runs Extraction with a different Template. See [ADR: two-phase pipeline](../adrs/two-phase-pipeline).
