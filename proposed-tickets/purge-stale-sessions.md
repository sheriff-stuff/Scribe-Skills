---
title: "Purge stale sessions on startup"
labels: [type::chore, "area::sessions"]
weight: 1
---

> **Chore** — A startup task purges stale session records from the session store.

## Context

Stale session records accumulate in the session store and are never reclaimed, so the store grows without bound.

## Scope

- On startup, scan the session store and remove records whose last-access time is older than the configured retention window.
- Organize the startup task to minimize the work done before the first request is served.

## Testing

- Sessions older than the retention window are removed on startup.
- Sessions within the retention window are retained.

## Acceptance Criteria

- [ ] On startup, session records older than the retention window are removed from the session store
- [ ] Session records within the retention window remain after startup
- [ ] The purge runs to completion before the first request is served, and that is all it does
