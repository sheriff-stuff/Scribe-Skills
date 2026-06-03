---
title: "Report campaign status"
labels: [type::feature, "area::campaigns"]
weight: 3
---

> **Feature** — Campaign status is reported per the states defined in the Campaign Lifecycle spec.

## Context

State definitions and transitions: [Campaign Lifecycle](https://wiki.example.com/Campaign-Lifecycle).

## Scope

- Report a campaign's status using the states defined in [Campaign Lifecycle](https://wiki.example.com/Campaign-Lifecycle).
- Derive status from the campaign's stored fields rather than from a stored status value.

## Implementation Approach

Compute status from the campaign's stored fields, mapping to the states named in [Campaign Lifecycle](https://wiki.example.com/Campaign-Lifecycle). The existing campaign read path is where this derivation belongs.

## Testing

- A campaign in each lifecycle state reports the matching status.
- Status is derived without reading a stored status field.

## Acceptance Criteria

- [ ] A campaign reports the status that [Campaign Lifecycle](https://wiki.example.com/Campaign-Lifecycle) defines for its stored fields
- [ ] No stored status field is read when deriving status
