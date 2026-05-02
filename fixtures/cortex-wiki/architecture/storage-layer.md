---
title: Storage Layer
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Storage Layer

## Purpose

Describes the database conventions used across services. Cortex uses a relational store for everything except media files.

## Database

SQLite is the default backend. Postgres is supported for users who want to run Cortex on a home server with multiple devices reading the same database. The schema is identical across both backends; service code uses the SQL builder layer rather than a full ORM (see [ADR: SQL builder over ORM](../adrs/sqlalchemy-core)).

## Media files

Recordings store their original media in a local directory configured by the user. The database holds only the path and content hash. Deleting a Recording via the Notes Service deletes both the row and the underlying media file.

## Migrations

Schema migrations live in a versioned migrations directory and run automatically on startup. See [Database Migrations](../ops/database-migrations) for operating procedures.

## Identifiers

All primary keys are ULIDs stored as text. ULIDs sort lexicographically by creation time, which makes the Notes Explorer's default chronological sort cheap.
