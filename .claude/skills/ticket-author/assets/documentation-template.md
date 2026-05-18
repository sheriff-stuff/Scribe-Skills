---
title: "<Descriptive title>"
labels: [type::documentation, "area::<name>"]
weight: <non-negative integer>
---

<!--
  Use for documentation work: creating or updating a wiki page, README, runbook, inline
  code docs, or API reference; reorganising or splitting docs; resolving a page-level
  `> [!CAUTION]` block by rewriting the page so the caution can be lifted.
-->

> **Documentation** — <One-sentence summary of what is being documented and where it lands.>

## Context *(mandatory)*

[What triggered this work: a cautioned page that's now ready to firm up, a missing page,
drift between code and docs, a reorganisation. If resolving a page-level caution, link the
cautioned page directly.]

## Source of Truth *(mandatory)*

[Where the content comes from — existing code, an ADR, prior discussion, another wiki page,
or investigation by the implementing agent. Link concrete anchors.]

- <Link or anchor>

## Scope *(mandatory)*

[Pages, sections, or files to create, update, move, or delete.]

- <First change — e.g. "Create `wiki/Foo.md` covering X, Y, Z">
- <Second change>
- <Third change>

## Out of Scope

- <Adjacent docs that are tempting but excluded>

## Acceptance Criteria *(mandatory)*

- [ ] <Page/file exists at the expected location with the expected sections>
- [ ] <Terminology matches existing wiki/code; no new names for known concepts>
- [ ] <If resolving a caution: the `> [!CAUTION]` block is removed from the page>
- [ ] <Coverage check tied to the source of truth — e.g. "every public method on `BarService` is documented in the API section">
