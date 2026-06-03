---
type: epic
title: "Notification preferences"
labels: [type::epic, "area::notifications"]
---

> **Epic** — Users control which channels each notification type uses, and existing users are migrated onto the new model.

## Source Documentation

- [Notification Preferences](https://wiki.example.com/Notification-Preferences) — the preference model and per-type channel matrix.

## Goals / Outcomes

- A user can choose, per notification type, which channels deliver it.
- Notification dispatch honours each user's per-type channel choices.
- Existing users retain equivalent delivery after migration.

## Scope

- A stored preference model keyed by user and notification type.
- An API to read and update a user's preferences.
- Migration of existing users onto the preference model.

## Out of Scope

- New notification types beyond those that exist today.

## Child Work Items

- Store notification preferences
- Notification preferences API
- Migrate existing preferences

## Definition of Done

- [ ] All child work items are complete
- [ ] Dispatch consults stored preferences for every notification type
- [ ] No user loses a channel they received before migration

## Risks

- Migration runs against production preference data; an incorrect mapping silently changes who receives what.
