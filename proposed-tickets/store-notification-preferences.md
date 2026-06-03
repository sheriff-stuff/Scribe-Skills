---
title: "Store notification preferences"
labels: [type::feature, "area::notifications"]
weight: 3
epic: auto
---

> **Feature** — A stored model holds each user's per-notification-type channel choices.

## Scope

- Persist a preference record keyed by user and notification type, carrying the chosen channels.
- Read a user's preference records back by user.

## Implementation Approach

Persist preferences using the document model described in [Notification Preferences](https://wiki.example.com/Notification-Preferences). The channel set per record follows the channel matrix on that page.

## Testing

- A preference record round-trips through storage with its channel set preserved.
- Reading by user returns every record stored for that user.

## Acceptance Criteria

- [ ] A preference keyed by user and notification type persists with its chosen channels
- [ ] Reading by user returns all of that user's preference records
