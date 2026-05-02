---
title: ADR: Template Versioning Strategy
category: adrs
owners: [product-team]
last_updated: 2025-12-03
---

# ADR: Template Versioning Strategy

## Context

Templates change over time as users tune their prompts. Existing Notes were extracted with the Template as it was at extraction time; later edits to the Template should not retroactively change what those Notes claim.

## Decision

Templates are versioned. Each edit to a Template creates a new version with a monotonically increasing integer. Each Extraction pins the exact `(template_id, version)` it ran against; that pin is denormalised onto the Note as well.

## Consequences

- Notes are reproducible: re-running Extraction on the same Note with the same pinned Template version produces structurally identical output (modulo LLM non-determinism).
- The Template Service grows a version dimension; the Template Editor must surface version selection and a 'restore previous version' affordance.
- Storage cost grows linearly with edit volume. Pruning old versions is deferred until a real user report identifies it as a problem.

## Alternatives considered

A simpler 'mutate in place' model was rejected because it cannot satisfy the 'do not retroactively change a Note' invariant.
