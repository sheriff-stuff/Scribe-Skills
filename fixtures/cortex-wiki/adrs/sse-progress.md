---
title: ADR: SSE for Realtime Progress
category: adrs
owners: [platform-team]
last_updated: 2025-10-02
---

# ADR: SSE for Realtime Progress

## Context

The frontend needs to surface Job progress without polling. The two main candidates are Server-Sent Events and WebSockets.

## Decision

Use Server-Sent Events. The frontend opens one SSE stream per user; the backend publishes Job events into it.

## Consequences

- The protocol is unidirectional, which matches the use case (server pushes; client never pushes back).
- SSE works through the FastAPI worker without a separate broker.
- Reconnection with a `Last-Event-Id` header is trivial; the backend keeps a five-minute buffer per channel.

## Alternatives considered

WebSockets were considered. They are a strict superset of SSE's capability but introduce complexity (custom protocol framing, keep-alives) without buying anything Cortex needs.
