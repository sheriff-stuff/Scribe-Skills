---
title: "Evaluate campaign expiry at read time"
labels: [type::feature, "area::campaigns"]
weight: 3
---

> **Feature** — Campaign expiry is evaluated at read time so a campaign past its end date reports inactive.

## Context

Campaigns stay active past their end date because expiry is evaluated only on write. Field semantics and lifecycle states: [Campaign Lifecycle](https://wiki.example.com/Campaign-Lifecycle).

## Scope

- Evaluate expiry when a campaign is read, deriving active/inactive from the current time and the campaign's end date.
- A campaign past its end date reports inactive without requiring a write.

## Implementation Approach

Expiry is currently computed in the write path in [`CampaignWriter`](https://code.example.com/campaigns/CampaignWriter.java#L42-L50). Move the derivation so the read path computes active/inactive from `endDate` and the current time. Field semantics: [Campaign Lifecycle](https://wiki.example.com/Campaign-Lifecycle).

## Testing

- A campaign past its end date reports inactive.
- A campaign before its end date reports active.

## Acceptance Criteria

- [ ] A campaign whose `endDate` is in the past reports inactive on read without an intervening write
- [ ] A campaign whose `endDate` is in the future reports active on read
