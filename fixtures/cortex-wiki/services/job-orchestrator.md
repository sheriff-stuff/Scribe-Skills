---
title: Job Orchestrator
category: services
owners: [platform-team]
last_updated: 2026-04-12
---

# Job Orchestrator

## Responsibility

Queues, runs, retries, and reports on Jobs. The single point of contact between user-driven actions and long-running Pipeline work.

## Queue model

A single in-process queue per Job kind. Jobs are consumed by worker pools sized per kind: by default 1 transcription worker, 2 extraction workers, 1 quality-scan worker. Workers run in-process — no external queue broker.

## Retry policy

Failed Jobs are retried up to three times with exponential backoff (1s, 5s, 30s). Programmer errors (asserted via a typed exception) are not retried. See [Error Handling Strategy](../architecture/error-handling).

## Progress

The Orchestrator publishes events on the realtime channel described in [Realtime Progress](../architecture/realtime-progress). Progress for Transcription is reported per second of audio processed; for Extraction per chunk completed.

## Cancellation

Running Jobs can be cancelled. Cancellation is cooperative — the worker checks a cancel flag at natural boundaries (after each chunk for extraction; after each utterance for transcription).

## Related

- [Job](../domain/job)
