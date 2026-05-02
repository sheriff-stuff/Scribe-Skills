---
title: Template
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Template

## Purpose

A versioned prompt configuration used by the Extraction Service. Templates control what the LLM extracts and how the output is shaped.

## Fields

- `id` — ULID, identifies a Template.
- `version` — monotonically increasing integer per Template id.
- `name` — human-readable, e.g. 'Standup', '1:1', 'Customer interview'.
- `description` — single paragraph.
- `prompt_text` — the prompt itself.
- `is_default` — flag indicating the default Template for new Recordings.
- `created_at`.

## Versioning

Editing a Template creates a new version rather than mutating the existing one. Each Extraction pins the exact `(template_id, version)` it ran against, so Notes remain reproducible even after Templates change.

## Built-in Templates

Cortex ships with three built-in Templates: General Meeting (the default), Standup, and Customer Interview. Built-in Templates can be cloned and customised; the originals cannot be edited or deleted.

## Related

- [Template Service](../services/template-service)
- [Extraction Service](../services/extraction-service)
- [Template Editor](../frontend/template-editor)
