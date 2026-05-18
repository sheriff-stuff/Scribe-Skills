---
title: "<one-sentence open point>"
labels: [type::ODD, "area::wiki", "owner::<role>"]
weight: <non-negative integer>
---

<!--
  Title rule: start from the ODD's one-sentence open point in the wiki's
  `> [!ODD]` block, but ensure the title stands on its own for a ticket - add
  context if the wiki wording relies on its surrounding page for clarity.
  Do not prefix with the ODD ID — the ID is in the link below.
-->

> **ODD** — Resolve [ODD-<AREA>-<slug>](<absolute URL to owner page>) (under [§ <section heading>](<absolute URL to owner page>#<section-anchor>) if a specific section applies). Open point and context live in the wiki `> [!ODD]` block.

## Affected Wiki Pages *(optional)*

[Mirror the pages on the ODD's `Affects:` line. Omit this section if the ODD
has no `Affects:` line.]

- [<Affected page>](<absolute URL>)

## Dependencies *(optional)*

**Blocked by:**

- [<Other ODD ticket title or ODD ID>](<absolute URL to ticket>)

**Blocks:**

- [<Ticket title or ID>](<absolute URL to ticket>)
