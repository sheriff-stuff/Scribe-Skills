---
title: Glossary
category: root
owners: [docs-team]
last_updated: 2026-04-15
---

# Glossary

## Purpose

Canonical vocabulary for the Cortex project. Every other page in this wiki uses these terms; if a concept doesn't appear here, it doesn't exist in Cortex's domain model.

## Terms

### Action Item

A task assigned during a Recording. Each Action Item has an optional owner (resolved to a Speaker Profile when possible), an optional due date, and a citation back to the originating Utterance.

### Decision

An outcome explicitly agreed during a Recording, surfaced by the Extraction Service. Decisions cite the Utterance(s) where the agreement was made.

### Extraction

The structured output produced by the Extraction Service from a Transcript: Topics, Decisions, Action Items, and free-form summary fields. Always references the Transcript it was derived from.

### Job

A unit of work tracked by the Job Orchestrator. Each Recording produces one or more Jobs (a Transcription Job and an Extraction Job at minimum). Jobs have observable progress and a terminal status of `succeeded`, `failed`, or `cancelled`.

### Note

The user-facing artifact that brings together a Recording, its Transcript, and its Extraction. The unit the user opens, edits, and (eventually) shares.

### Pipeline

The end-to-end flow from ingested Recording to finished Note. Cortex's Pipeline is two-phase: a Transcription Phase that produces a Transcript, and an Extraction Phase that produces an Extraction. Phases are decoupled so the Transcript survives Extraction failure.

### Quality Flag

An automatic annotation produced by the Audio Quality Service that warns of issues affecting transcription accuracy. Examples: low signal-to-noise ratio, sustained overlap, long silence, clipping. Quality Flags scope to Utterance ranges.

### Recording

An audio source ingested into Cortex. Wraps the original media file, the user-supplied metadata, and pointers to derived processing artifacts. The lifecycle root: Transcripts, Extractions, and Notes all hang off a Recording.

### Speaker Profile

A persistent identity that an Utterance can be attributed to. Resolved either automatically (matched against prior Recordings by voice embedding) or manually by the user assigning a name to a Speaker Tag.

### Speaker Tag

The provisional label assigned by the Diarization Service (e.g. `Tag-1`, `Tag-2`) before resolution to a Speaker Profile. Tags are scoped to a single Transcript and are never persisted as identities.

### Template

A versioned prompt configuration used by the Extraction Service to control what the LLM produces. Templates are selected per Recording and pinned to a Note when extraction runs, so re-running on a Note uses the same Template by default.

### Topic

A discussion subject extracted from a Transcript. Each Topic is bounded by a contiguous Utterance range and carries a short title, a one-line summary, and a list of citation Utterance IDs.

### Transcript

A speaker-attributed record of speech in a Recording, composed of an ordered sequence of Utterances. There is exactly one Transcript per Recording.

### Utterance

A single contiguous span of speech attributed to one Speaker Profile within a Transcript. The smallest indexable unit of transcribed speech and the anchor for citations from Extractions back into the Transcript.
