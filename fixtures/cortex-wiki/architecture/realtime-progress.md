---
title: Realtime Progress
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Realtime Progress

## Purpose

Describes how the frontend learns about Job progress without polling.

## Mechanism

The Job Orchestrator publishes events on a per-user Server-Sent Events channel. Each event names the Job ID, the phase it is in, a percentage estimate (where calculable), and any Quality Flags emitted so far. See [ADR: SSE for progress](../adrs/sse-progress) for the reasoning behind SSE over WebSockets.

## Event types

- `job.queued` — the Job has been created.
- `job.started` — the Job is now running.
- `job.progress` — incremental progress, sent at most once per second per Job.
- `job.flagged` — a Quality Flag was emitted during this Job.
- `job.succeeded` / `job.failed` / `job.cancelled` — terminal events.

## Reconnection

Clients reconnect with the last received event ID. The Orchestrator replays missed events from a bounded buffer (last 5 minutes per channel). Older events are fetched via the Jobs REST endpoint instead.
