---
title: ADR: SQL Builder over ORM
category: adrs
owners: [platform-team]
last_updated: 2025-09-12
---

# ADR: SQL Builder over ORM

## Context

Cortex's query patterns are dominated by reads with specific joins and aggregations (e.g. listing Notes with their Quality Flag counts and primary speaker). ORM lazy loading is a common source of N+1 queries in shapes like this; the team also wants the same schema to work on SQLite and Postgres without diverging behaviour.

## Decision

Use SQLAlchemy Core (the SQL builder layer) rather than the ORM. Service code writes explicit queries; row-to-dataclass conversion is a one-line helper.

## Consequences

- Query performance is predictable; N+1 risks are visible in the code rather than hidden behind lazy loaders.
- The same query expression runs against both SQLite and Postgres.
- Service code is more verbose than ORM equivalents; this is accepted as a worthwhile cost.
