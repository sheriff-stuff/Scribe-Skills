---
title: "Persist user storage fields"
labels: [type::feature, "area::users"]
weight: 2
---

> **Feature** — The user document persists the fields defined in the User Storage spec.

## Context

Field list and validation rules: [User Storage](https://wiki.example.com/User-Storage).

## Scope

- Persist the `User` document with the fields defined in [User Storage](https://wiki.example.com/User-Storage).
- Map timestamp fields so timezone survives a storage round-trip.

## Implementation Approach

Extend the existing user persistence to cover the fields named in [User Storage](https://wiki.example.com/User-Storage). The timezone-preserving mapping already used by other timestamped documents applies here, so `ZonedDateTime` values keep their timezone across a round-trip.

## Testing

- A populated `User` round-trips through storage with all fields preserved.
- `ZonedDateTime` fields survive a round-trip with timezone intact.

## Acceptance Criteria

- [ ] A `User` persists with the fields listed in [User Storage](https://wiki.example.com/User-Storage)
- [ ] `ZonedDateTime` fields survive a storage round-trip with timezone intact
