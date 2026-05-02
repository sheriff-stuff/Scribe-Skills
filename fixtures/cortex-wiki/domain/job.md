---
title: Job
category: domain
owners: [platform-team]
last_updated: 2026-04-12
---

# Job

## Purpose

A unit of work tracked by the Job Orchestrator. Each Recording produces one or more Jobs.

## Fields

- `id` — ULID.
- `kind` — one of `transcription`, `extraction`, `quality_scan`.
- `recording_id` — FK.
- `status` — `queued`, `running`, `succeeded`, `failed`, `cancelled`.
- `progress` — 0.0–1.0.
- `error_summary` — nullable, short user-facing string.
- `error_detail` — nullable, full technical detail.
- `attempt` — 1-based retry counter.
- `started_at` / `finished_at` — nullable.

## Status transitions

Allowed transitions: `queued` → `running` → (`succeeded` | `failed` | `cancelled`). Failed Jobs are retried by the Orchestrator up to three times, each retry creating a new attempt of the same Job id.

## Related

- [Job Orchestrator](../services/job-orchestrator)
- [Realtime Progress](../architecture/realtime-progress)
