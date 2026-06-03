---
title: "Dispatch notifications by preference"
labels: [type::feature, "area::notifications"]
weight: 3
---

> **Feature** — Notification dispatch delivers each notification on the channels the recipient's preferences select.

## Context

Channel selection rules and the default channel set: [Notification Preferences](https://wiki.example.com/Notification-Preferences).

## Scope

- Resolve a recipient's selected channels for a notification type before dispatch.
- Deliver the notification on each selected channel and on no others.

## Implementation Approach

At dispatch, resolve the recipient's channel selection for the notification type from the preference model in [Notification Preferences](https://wiki.example.com/Notification-Preferences), then deliver on the selected channels. The existing dispatch path is where this selection applies.

## Testing

- A notification is delivered on every channel the recipient's preferences select.
- A notification is not delivered on a channel the recipient's preferences exclude.
- A recipient with no stored preference for a type falls back to the default channel set.

## Acceptance Criteria

- [ ] A notification is delivered on exactly the channels the recipient's preferences select
- [ ] A recipient with no stored preference receives the notification on the default channel set defined in [Notification Preferences](https://wiki.example.com/Notification-Preferences)
