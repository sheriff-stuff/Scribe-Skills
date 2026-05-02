---
title: ADR: Local-first by Default
category: adrs
owners: [platform-team]
last_updated: 2025-08-21
---

# ADR: Local-first by Default

## Context

Cortex's most-asked-for property in user research is that meeting audio never leaves the user's machine. Privacy-conscious users explicitly reject any tool that uploads recordings to a vendor.

## Decision

Cortex runs entirely on the user's machine by default. All models are local; no external network call is required for the core flow. Cloud endpoints are an opt-in fallback.

## Consequences

- The install footprint is large because models ship with the application.
- Hardware requirements are higher than for a thin-client app.
- Onboarding is simpler because the user is not asked to choose a cloud provider on first run.
- Cortex's privacy story is enforceable, not promised.
