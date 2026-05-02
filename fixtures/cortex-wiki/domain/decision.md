---
title: Decision
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Decision

## Purpose

An outcome explicitly agreed during a Recording. Decisions are surfaced separately from Topics because they have higher value to the user and are routinely exported to other tools (issue trackers, documents).

## Fields

- `id` — ULID.
- `extraction_id` — FK.
- `text` — the decision as a single sentence.
- `citation_utterance_ids` — at least one.

## What counts as a Decision

An outcome where a participant explicitly states intent and at least one other participant agrees, or where there is no objection within the same Topic. Aspirational statements ('we should think about X') are not Decisions.

## Related

- [Extraction](extraction)
- [Utterance](utterance)
