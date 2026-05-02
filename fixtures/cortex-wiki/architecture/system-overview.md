---
title: System Overview
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# System Overview

## Purpose

Cortex is a local meeting-transcription app. The user supplies a Recording (an audio or video file from a meeting), Cortex produces a Transcript and an Extraction, and assembles them into a Note that the user can read, edit, and (in future) share.

## Shape at a glance

Cortex runs entirely on the user's machine. There is a Python backend (FastAPI) that owns the Pipeline, and a React frontend served by the same backend. All long-running work happens behind the Job Orchestrator. Storage is a local relational database. Models (speech recognition and LLM) run locally by default; cloud endpoints are an opt-in fallback.

## Top-level flow

The user uploads a Recording through the web app. The [Ingest Service](../services/ingest-service) validates and stores the media. The [Job Orchestrator](../services/job-orchestrator) queues a Transcription Job. The [Transcription Service](../services/transcription-service) produces a Transcript, then the [Diarization Service](../services/diarization-service) labels Utterances with Speaker Tags. Once the Transcript is finalised the Orchestrator queues an Extraction Job, which the [Extraction Service](../services/extraction-service) executes against the configured [Template](../domain/template). The result becomes a [Note](../domain/note).

## Where to read next

- [Service Map](service-map): boundaries and dependencies between services.
- [Pipeline Stages](pipeline-stages): phase-by-phase walkthrough.
- [Data Flow](data-flow): how artifacts move between services and storage.
- [Glossary](../glossary): canonical vocabulary used throughout.
