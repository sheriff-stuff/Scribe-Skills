---
title: State Management
category: frontend
owners: [frontend-team]
last_updated: 2026-04-12
---

# State Management

## Purpose

Names how data flows through the frontend. Reading this page should be enough to know where to add a new piece of state.

## Layers

- **Server cache** — a single React Query instance owns all backend reads. Mutations invalidate the relevant queries.
- **Realtime updates** — a thin SSE subscriber feeds Job events into the React Query cache by mutating the cached Job and Note rows directly.
- **Local UI state** — view-local state stays in components. Anything that crosses two routes lives in the URL (filters, sort) rather than a global store.

## Anti-patterns

- Don't introduce a global state store. Use the URL or React Query.
- Don't bypass React Query for backend reads. The cache invalidation rules assume it owns all server state.
