---
title: "Reconcile payments to invoices"
labels: [type::feature, "area::billing"]
weight: 4
epic: auto
---

> **Feature** — Incoming payments are matched to outstanding invoices and update their balance.

## Scope

- Match each incoming payment to the customer's outstanding invoices.
- Reduce a matched invoice's balance by the applied payment amount.

## Implementation Approach

Extend [`PaymentProcessor.onPaymentReceived`](https://code.example.com/billing/PaymentProcessor.java) to look up the payer's outstanding invoices and apply the payment, following the allocation order defined in [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing).

## Testing

- A payment matched to an invoice reduces that invoice's balance by the applied amount.
- A payment exceeding a single invoice's balance applies the remainder per the allocation order.
- A payment with no matching invoice is held unapplied.

## Acceptance Criteria

- [ ] A payment applied to an invoice reduces its balance by the applied amount
- [ ] A payment with no matching outstanding invoice is held unapplied
