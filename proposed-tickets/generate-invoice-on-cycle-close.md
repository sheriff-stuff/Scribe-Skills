---
title: "Generate invoice on cycle close"
labels: [type::feature, "area::billing"]
weight: 5
epic: auto
---

> **Feature** — Closing a billing cycle generates an invoice for each customer with billable activity.

## Scope

- On cycle close, generate one invoice per customer with billable activity in the cycle.
- Populate the invoice with the cycle's billable line items.

## Implementation Approach

Cycle close is signalled in [`BillingCycle`](https://code.example.com/billing/BillingCycle.java#L88-L97). On that signal, gather each customer's billable line items for the cycle and create an invoice. Line-item shape: [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing).

## Testing

- Closing a cycle generates one invoice per customer with billable activity.
- A customer with no billable activity gets no invoice.

## Acceptance Criteria

- [ ] Closing a cycle produces exactly one invoice per customer with billable activity in that cycle
- [ ] A customer with no billable activity in the cycle has no invoice generated
