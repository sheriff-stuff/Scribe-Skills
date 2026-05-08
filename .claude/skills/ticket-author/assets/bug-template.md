---
title: "<Descriptive title>"
labels: [type::bug, "area::<name>", "severity::<high|medium|low>", "env::<dev|test|prod>", "network::<lowside|highside>"]
weight: <non-negative integer>
---

> **Bug** — <What is broken and what the expected behaviour should be.>

## Steps to Reproduce *(mandatory)*

1. <First step>
2. <Second step>
3. <Third step>

## Expected Behaviour *(mandatory)*

## Actual Behaviour *(mandatory)*

## Impact *(mandatory)*

<!--
  Who is affected and how.
-->

## Evidence *(optional)*

<!--
  Attach screenshots or screen recordings here after the ticket is created in GitLab.
-->

## Context *(optional)*

<!--
  Investigation notes, related logs, links to relevant wiki pages or existing code.
-->

**Frequency:** <always reproducible / intermittent / observed once>

**Suspected cause:** <notes on what might be causing this, if known>

## Testing *(mandatory)*

<!--
  Behaviors needing test coverage. Always include a regression for the reproduction case.
-->

- Regression: <one-line description of the failing scenario from Steps to Reproduce>
- <Additional behavior under test if the fix touches one — otherwise remove this line>

## Acceptance Criteria *(mandatory)*

- [ ] <The bug is fixed: describe the correct behaviour>
