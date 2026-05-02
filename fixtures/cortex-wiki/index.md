---
title: Cortex wiki
category: root
owners: [docs-team]
last_updated: 2026-04-15
---

# Cortex wiki

## About this wiki

Design corpus for **Cortex**, a local meeting-transcription app. This index lists every page grouped by area. Start with [System Overview](architecture/system-overview) if you're new, or jump to [Glossary](glossary) for canonical vocabulary.

## Wiki root

- [Changelog](changelog)
- [Glossary](glossary)

## Architecture

- [Data Flow](architecture/data-flow)
- [Error Handling Strategy](architecture/error-handling)
- [Extension Points](architecture/extension-points)
- [Local-first Principles](architecture/local-first-principles)
- [Model Runtime](architecture/model-runtime)
- [Pipeline Stages](architecture/pipeline-stages)
- [Realtime Progress](architecture/realtime-progress)
- [Service Map](architecture/service-map)
- [Storage Layer](architecture/storage-layer)
- [System Overview](architecture/system-overview)

## Domain model

- [Action Item](domain/action-item)
- [Decision](domain/decision)
- [Extraction](domain/extraction)
- [Job](domain/job)
- [Note](domain/note)
- [Quality Flag](domain/quality-flag)
- [Recording](domain/recording)
- [Speaker Profile](domain/speaker-profile)
- [Template](domain/template)
- [Topic](domain/topic)
- [Transcript](domain/transcript)
- [Utterance](domain/utterance)

## Services

- [Audio Quality Service](services/audio-quality-service)
- [Diarization Service](services/diarization-service)
- [Extraction Service](services/extraction-service)
- [Ingest Service](services/ingest-service)
- [Job Orchestrator](services/job-orchestrator)
- [Notes Service](services/notes-service)
- [Template Service](services/template-service)
- [Transcription Service](services/transcription-service)

## Frontend

- [Component Library](frontend/component-library)
- [Notes Explorer](frontend/notes-explorer)
- [State Management](frontend/state-management)
- [Template Editor](frontend/template-editor)
- [Transcript Viewer](frontend/transcript-viewer)
- [Web App Overview](frontend/web-app-overview)

## Operations

- [Database Migrations](ops/database-migrations)
- [Known Failure Modes](ops/troubleshooting-guide)
- [Local Deployment](ops/local-deployment)
- [Model Management](ops/model-management)
- [On-call Runbook](ops/oncall-runbook)

## Process

- [Documentation Style](process/documentation-style)
- [Release Process](process/release-process)
- [Ticket Conventions](process/ticket-conventions)

## Architectural decision records

- [ADR: Chunked Extraction with Overlap](adrs/chunked-extraction)
- [ADR: Diarization Model Choice](adrs/pyannote-diarization)
- [ADR: Local LLM Runtime Default](adrs/llm-runtime-default)
- [ADR: Local-first by Default](adrs/local-first-default)
- [ADR: SQL Builder over ORM](adrs/sqlalchemy-core)
- [ADR: SSE for Realtime Progress](adrs/sse-progress)
- [ADR: Template Versioning Strategy](adrs/template-versioning)
- [ADR: Two-phase Pipeline](adrs/two-phase-pipeline)
