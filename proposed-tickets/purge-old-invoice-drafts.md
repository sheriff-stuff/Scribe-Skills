---
title: "Purge old invoice drafts"
labels: [type::chore, "area::billing"]
weight: 2
epic: auto
---

> **Chore** — A scheduled task purges invoice drafts that were never finalised.

## Context

Abandoned invoice drafts accumulate and are never reclaimed, so the invoice store grows without bound.

## Scope

- Remove invoice drafts older than the configured retention window that were never finalised.
- Organize the task to minimize its impact on the finalisation path.

## Testing

- Drafts older than the retention window are removed.
- Finalised invoices are never removed.

## Acceptance Criteria

- [ ] Invoice drafts older than the retention window and never finalised are removed
- [ ] Finalised invoices are retained regardless of age, and that is all the task touches
