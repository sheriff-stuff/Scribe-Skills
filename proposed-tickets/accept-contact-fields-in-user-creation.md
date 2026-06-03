---
title: "Accept contact fields in user creation"
labels: [type::feature, "area::users"]
weight: 2
---

> **Feature** — User creation accepts `email` and `phone` so they can be set when a user is created.

## Context

Field semantics: [Contact Channels for Users](https://wiki.example.com/Contact-Channels-for-Users).

## Scope

- Accept `email` and `phone` in the user-creation request.
- Persist both fields when a user is created.

## Implementation Approach

Extend [`UserController.createUser`](https://code.example.com/users/UserController.java) to accept `email` and `phone` and pass them through to persistence. The fields follow the semantics in [Contact Channels for Users](https://wiki.example.com/Contact-Channels-for-Users).

## Testing

- A user created with `email` and `phone` persists with both fields set.
- A user created without `email` and `phone` persists with those fields empty.

## Acceptance Criteria

- [ ] Creating a user with `email` and `phone` persists both values
- [ ] Creating a user without `email` and `phone` succeeds with both fields empty
