---
title: "Store invoice records"
labels: [type::feature, "area::billing"]
weight: 4
epic: auto
---

> **Feature** — Invoices persist with the fields defined in the Billing and Invoicing spec.

## Scope

- Persist each invoice with the fields defined in [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing).
- Read invoices back by customer and by billing cycle.

## Implementation Approach

Persist invoices using the document model in [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing). The timezone-preserving mapping used by other timestamped documents applies to invoice dates, keeping their timezone across a round-trip.

## Testing

- An invoice round-trips through storage with all fields preserved.
- Invoices can be read back by customer and by billing cycle.

## Acceptance Criteria

- [ ] An invoice persists with the fields listed in [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing)
- [ ] Invoices are retrievable by customer and by billing cycle
