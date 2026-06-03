---
title: "Apply tax rates to invoice"
labels: [type::feature, "area::billing"]
weight: 5
epic: auto
---

> **Feature** — Each invoice has tax applied per the customer's jurisdiction before it is finalised.

## Scope

- Apply the customer's jurisdiction tax rate to each taxable line item on the invoice.
- Add the resulting tax to the invoice total.

## Implementation Approach

Resolve the customer's jurisdiction and apply the matching rate from [Billing and Invoicing](https://wiki.example.com/Billing-and-Invoicing) to each taxable line item, then total the tax onto the invoice.

## Testing

- A taxable line item carries tax at the customer's jurisdiction rate.
- A tax-exempt line item carries no tax.

## Acceptance Criteria

- [ ] Each taxable line item on a finalised invoice carries tax at the customer's jurisdiction rate
- [ ] The invoice tax total equals the sum of per-line tax
