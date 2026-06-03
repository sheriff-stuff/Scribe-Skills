---
title: "Migrate existing preferences"
labels: [type::feature, "area::notifications"]
weight: 2
epic: auto
---

> **Feature** — Existing users are migrated from the legacy opt-out flag onto the new preference model.

## Scope

- Translate each existing user's legacy `emailOptOut` boolean into preference records on the new per-notification-type channel model.
- Run the migration once across all existing users.

## Implementation Approach

Read each user's legacy `emailOptOut` value and write preference records on the model from [Notification Preferences](https://wiki.example.com/Notification-Preferences).

## Testing

- Every existing user has preference records after the migration runs.

## Acceptance Criteria

- [ ] After migration, every existing user has preference records on the new model
- [ ] The migration is idempotent — running it twice produces the same records
