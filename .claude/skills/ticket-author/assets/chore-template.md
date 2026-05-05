<!--
  Use for maintenance work: dependency upgrades, version bumps, refactors with no behaviour
  change, build/CI/tooling changes, config cleanup, removing dead code, doc-only updates.
  If the work changes user-visible behaviour, use the Feature template instead.
  If it fixes incorrect behaviour, use the Bug template.
-->

---
title: "<Descriptive title>"
labels: [type::chore]
weight: <non-negative integer>
---

> **Chore** — <One-sentence summary of the maintenance change and the system it touches.>

## Context

_What triggered this work: deprecation notice, version EOL, security advisory, accumulated drift, blocker for another ticket. Reference the relevant wiki page, advisory, or existing code using full URLs. Keep it short — a chore ticket is not the place for rationale beyond the trigger._

## Scope

_Numbered list of what is being changed. Each item is a discrete change._

1. <First change>
2. <Second change>
3. <Third change>

## Out of Scope

_Adjacent cleanup that is tempting but not part of this ticket._

- <What is deferred>

## Risk and Rollback

_How risky the change is and how to back it out. For low-risk chores (formatting, doc edits), state that and move on._

**Risk:** <low / medium / high — and why>

**Rollback:** <how to revert: single revert commit, config flag, version pin>

## Acceptance Criteria

- [ ] <Specific, testable criterion — e.g. "package.json declares X@Y.Z and lockfile resolves to that version">
- [ ] <Behavioural parity check — e.g. "existing test suite passes with no changes to assertions">
- [ ] <Verification that the trigger is resolved — e.g. "deprecation warning no longer appears in build output">

## Links

_Reference documents, advisories, changelogs, and implementations. Use full URLs._

- [<Document title>](<full URL>) — <one-line description>
