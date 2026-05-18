---
title: "<Descriptive title>"
labels: [type::chore, "area::<name>"]
weight: <non-negative integer>
---

<!--
  Use for maintenance work: dependency upgrades, version bumps, refactors with no behaviour
  change, build/CI/tooling changes, config cleanup, removing dead code.
  If the work changes user-visible behaviour, use the Feature template.
  If it fixes incorrect behaviour, use the Bug template.
-->

> **Chore** — <One-sentence summary of the maintenance change and the system it touches.>

## Context *(mandatory)*

[What triggered this work: deprecation, EOL, security advisory, drift, blocker.
Keep it short — chore tickets aren't for rationale beyond the trigger.]

## Scope *(mandatory)*

[Discrete changes.]

- <First change>
- <Second change>
- <Third change>

## Testing *(optional)*

[Only when the chore can change behaviour — e.g. a refactor or dependency upgrade.
Name the behaviours that must keep working. Omit for pure config/tooling changes.]

- <Behaviour under test>

## Out of Scope

[Adjacent cleanup that's tempting but excluded.]

- <What is deferred>

## Acceptance Criteria *(mandatory)*

- [ ] <Specific, testable criterion — e.g. "package.json declares <X@Y.Z> and lockfile resolves to that version">
- [ ] <Behavioural parity check — e.g. "existing test suite passes with no changes to assertions">
- [ ] <Verification that the trigger is resolved — e.g. "deprecation warning no longer appears in build output">
