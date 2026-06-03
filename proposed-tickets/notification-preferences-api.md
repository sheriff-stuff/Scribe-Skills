---
title: "Notification preferences API"
labels: [type::feature, "area::notifications"]
weight: 3
epic: auto
---

> **Feature** — An API reads and updates a user's notification preferences.

## Scope

- Read a user's current preferences across all notification types.
- Update the channels chosen for a given notification type.

## Implementation Approach

Expose read and update operations over the stored preference model from [Notification Preferences](https://wiki.example.com/Notification-Preferences). Validation rules for channel combinations are defined on that page.

## Testing

- Reading preferences returns the stored channel choices for each notification type.
- Updating a notification type's channels is reflected in a subsequent read.

## Acceptance Criteria

- [ ] Reading returns the stored channel choices for every notification type
- [ ] An update to a notification type's channels is reflected in the next read
