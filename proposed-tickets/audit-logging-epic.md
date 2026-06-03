---
type: epic
title: "Audit logging"
labels: [type::epic, "area::audit"]
---

> **Epic** — Security-relevant actions are recorded to an append-only audit log.

## Source Documentation

- [Audit Logging](https://wiki.example.com/Audit-Logging) — the event taxonomy and retention policy.

## Goals / Outcomes

- Security-relevant actions produce an audit event.
- Audit events are retained per the retention policy.

## Scope

- An append-only audit event store.
- Emission of audit events from security-relevant actions.

## Out of Scope

- A user-facing audit viewer.

## Child Work Items

- Audit event store
- Emit audit events

## Definition of Done

- [ ] All child work items are complete
- [ ] Every security-relevant action emits an audit event

## Risks

- Retention policy is set by compliance; an incorrect retention window is a compliance exposure.
