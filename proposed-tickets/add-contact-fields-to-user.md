---
title: "Add contact fields to user"
labels: [type::feature, "area::users"]
weight: 2
---

> **Feature** — `email` and `phone` are added to the user record so users can be contacted outside the app.

## Context

Rationale and field semantics: [Contact Channels for Users](https://wiki.example.com/Contact-Channels-for-Users).

## Scope

- Add `email` and `phone` fields to the user record.
- Persist and read back both fields.

## Implementation Approach

Mirror inventory-service's store setup, adapting packages.

## Testing

- A user with `email` and `phone` round-trips through storage with both fields preserved.

## Acceptance Criteria

- [ ] Create the User entity
- [ ] Code compiles without errors
- [ ] A user with populated `email` and `phone` round-trips through storage with both preserved
