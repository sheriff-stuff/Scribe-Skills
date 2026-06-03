---
title: "Email invoice to customer"
labels: [type::feature, "area::billing"]
weight: 4
epic: auto
---

> **Feature** — A finalised invoice is emailed to the customer.

## Scope

- Email each finalised invoice to the customer's billing email.
- Attach the invoice document to the email.

## Implementation Approach

Mirror notification-service's email setup, adapting packages.

## Testing

- A finalised invoice is emailed to the customer's billing email with the invoice attached.

## Acceptance Criteria

- [ ] Finalising an invoice sends one email to the customer's billing email with the invoice attached
- [ ] No email is sent for an invoice that is not finalised
