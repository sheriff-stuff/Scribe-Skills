# Ticket Anchoring

Every ticket is anchored in one of two places, identified before its body is written. The anchor determines what the body carries.

- **Wiki-anchored** — a wiki page holds the _what_ and the _why_. The ticket links that page and carries only scope, anchors, and acceptance criteria. Feature work, ODDs, and anything tied to a domain concept is wiki-anchored.
- **Codebase-anchored** — the decision is technical and code-local, and no wiki page holds it. The ticket is the source of truth for itself and carries the mechanical detail needed to execute. Refactors, internal cleanups, dependency upgrades, and code-shape decisions are codebase-anchored.

The anchor sets what counts as a valid body — see [Body Rules](Body-Rules). An anchor the skill cannot determine is settled with the user before drafting.
