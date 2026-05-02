---
title: Extraction
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Extraction

## Purpose

The structured output produced from a Transcript by the Extraction Service: Topics, Decisions, Action Items, plus a free-form summary.

## Fields

- `id` — ULID.
- `transcript_id` — FK.
- `template_id` — FK to the Template version used.
- `summary` — free-form prose, single paragraph.
- `topics` — list of Topic rows.
- `decisions` — list of Decision rows.
- `action_items` — list of Action Item rows.
- `model_version` — LLM identifier.
- `created_at`.

## Determinism

Extractions are not deterministic — the same Transcript and Template can produce different Extractions on different runs. This is expected. Re-running Extraction is cheap and explicitly supported.

## Related

- [Topic](topic)
- [Decision](decision)
- [Action Item](action-item)
- [Extraction Service](../services/extraction-service)
