# Ticket Anchoring

Every ticket is anchored where its _why_ lives, identified before its body is written. The anchor decides what the body carries — see [Body Rules](Body-Rules).

The anchor is found by one test: does the ticket need motivational rationale — business case, user impact, or domain or strategic justification — to make sense?

- **Wiki-anchored** — yes. A wiki page holds the _why_ and the _what_; the ticket links it. Feature work, ODDs, and anything tied to a domain concept is wiki-anchored. When no such page exists, the skill suggests creating one.
- **Codebase-anchored** — no; the only justification is causal-mechanical — sequencing, invariants, what depends on what — and the ticket is its own source of truth. Refactors, internal cleanups, and dependency upgrades are codebase-anchored.

Mechanical detail does not flip the anchor: a wiki-anchored ticket may carry it too, with the _why_ on the wiki. The _why_ is what classifies — a ticket whose reader would need business case, user impact, or domain rationale to know why the work matters is wiki-anchored. An anchor the skill cannot determine is settled with the user before drafting.
