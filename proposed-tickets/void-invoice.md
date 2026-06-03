---
title: "Void invoice"
labels: [type::feature, "area::billing"]
weight: 3
epic: auto
---

> **Feature** — A finalised invoice can be voided, marking it non-collectable.

## Scope

- Void a finalised invoice, marking it non-collectable.
- Record who voided the invoice and when.

## Implementation Approach

Add a void transition to the invoice lifecycle described in [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing), recording the actor and timestamp on the invoice.

## Testing

- Voiding a finalised invoice marks it non-collectable.
- A voided invoice cannot be paid.

## Acceptance Criteria

- [ ] Create the void transition
- [ ] Code compiles without errors
- [ ] A voided invoice is marked non-collectable and cannot be paid
