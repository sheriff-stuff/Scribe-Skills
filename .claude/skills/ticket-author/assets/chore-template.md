---
title: "<Descriptive title>"
labels: [type::chore, "area::<name>"]
weight: <non-negative integer>
---

<!--
  Use for maintenance work: dependency upgrades, version bumps, refactors with no behaviour
  change, build/CI/tooling changes, config cleanup, removing dead code, doc-only updates.
  If the work changes user-visible behaviour, use the Feature template.
  If it fixes incorrect behaviour, use the Bug template.
-->

> **Chore** — <One-sentence summary of the maintenance change and the system it touches.>

## Context *(mandatory)*

<!--
  What triggered this work: deprecation, EOL, security advisory, drift, blocker.
  Keep it short — chore tickets aren't for rationale beyond the trigger.
-->

## Scope *(mandatory)*

<!--
  Discrete changes.
-->

1. <First change>
2. <Second change>
3. <Third change>

## Out of Scope

<!--
  Adjacent cleanup that's tempting but excluded.
-->

- <What is deferred>

## Risk and Rollback *(mandatory)*

<!--
  For low-risk chores (formatting, doc edits), state that and move on.
-->

**Risk:** <low / medium / high — and why>

**Rollback:** <how to revert: single revert commit, config flag, version pin>

## Acceptance Criteria *(mandatory)*

- [ ] <Specific, testable criterion — e.g. "package.json declares X@Y.Z and lockfile resolves to that version">
- [ ] <Behavioural parity check — e.g. "existing test suite passes with no changes to assertions">
- [ ] <Verification that the trigger is resolved — e.g. "deprecation warning no longer appears in build output">
