---
type: epic
title: "Billing and invoicing"
labels: [type::epic, "area::billing"]
---

> **Epic** — Customers are billed on each cycle close: invoices are generated, taxed, stored, emailed, and reconciled against payments, with voiding and draft cleanup.

## Source Documentation

- [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing) — the invoice model, tax rules, and lifecycle.

## Goals / Outcomes

- A closed billing cycle produces a stored, taxed invoice for each customer with billable activity.
- Customers receive their invoice by email.
- Payments are reconciled against outstanding invoices.
- Invoices can be voided, and stale drafts are reclaimed.

## Scope

- Invoice generation on cycle close.
- Tax application.
- Invoice storage.
- Invoice emailing.
- Payment reconciliation.
- Invoice voiding.
- Draft cleanup.

## Out of Scope

- Dunning and retry logic for failed payments.

## Child Work Items

- Generate invoice on cycle close
- Apply tax rates to invoice
- Store invoice records
- Email invoice to customer
- Reconcile payments to invoices
- Void invoice
- Purge old invoice drafts

## Dependencies

**Blocked by:**

- [Billing and Invoicing spec](https://wiki.example.com/Billing-and-Invoicing)

## Definition of Done

- [ ] All child work items are complete
- [ ] A cycle close produces a stored, taxed, emailed invoice per customer with billable activity
- [ ] Payments reconcile against outstanding invoices

## Risks

- Tax computation is governed by external jurisdiction rules; an incorrect rate is a compliance exposure.
