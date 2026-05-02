---
title: Error Handling Strategy
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Error Handling Strategy

## Purpose

Names the categories of failure Cortex distinguishes and what each one is allowed to do.

## Categories

- **User-input errors** (invalid file, unsupported format) — surfaced synchronously at upload, never produce a Job.
- **Transient infrastructure errors** (model worker OOM, database lock timeout) — retried with backoff by the Job Orchestrator. After three retries the Job is marked failed and the underlying error is surfaced.
- **Model errors** (LLM returns malformed output, ASR confidence below threshold) — the Job is marked failed. The Transcript is preserved even if Extraction fails, per [ADR: two-phase pipeline](../adrs/two-phase-pipeline).
- **Programmer errors** (assertion failure, type error) — the worker process exits, the Orchestrator marks the Job failed without retry, and the error is logged with full context for diagnosis.

## User-facing presentation

Failed Jobs surface a one-line reason in the Notes Explorer plus a longer technical detail behind a disclosure. The Notes Service never shows raw stack traces.

## Re-run policy

Any failed Extraction Job can be re-run by the user without re-running transcription. Failed Transcription Jobs require the original Recording to still be present.
