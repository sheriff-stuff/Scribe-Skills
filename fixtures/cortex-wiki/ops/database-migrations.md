---
title: Database Migrations
category: ops
owners: [platform-team]
last_updated: 2026-04-12
---

# Database Migrations

## Purpose

How schema migrations are authored, run, and rolled back.

## Authoring

Migrations live as numbered SQL files in the migrations directory. Each migration is a single forward step; rollback is not automatic.

## Running

Migrations run automatically at startup. The backend refuses to start if a migration fails; the user is directed to the troubleshooting guide.

## Rolling back

Cortex does not support automatic rollback. To downgrade, the user restores the database from the automatic backup taken before each migration.

## Backups

A SQLite copy of the database is taken before each migration and kept in the data directory under `backups/`. The five most recent backups are retained.
