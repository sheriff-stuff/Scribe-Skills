---
title: Template Service
category: services
owners: [product-team]
last_updated: 2026-04-12
---

# Template Service

## Responsibility

Owns Template CRUD and version pinning. The only writer to Template rows.

## Operations

- `create_template(name, description, prompt_text)` — creates a new Template at version 1.
- `update_template(id, ...)` — creates a new version with the current value as version + 1.
- `clone_template(id)` — copies a Template into a new id starting at version 1. Used to customise built-in Templates.
- `set_default(id)` — flips the default flag.
- `delete_template(id)` — soft-delete; existing Notes that pin this Template still resolve.

## Built-in Templates

The Template Service ships built-in Templates that are seeded on first startup. Built-ins cannot be deleted or directly edited; they must be cloned first. See [Template](../domain/template) for the list.

## Related

- [Template](../domain/template)
- [Template Editor](../frontend/template-editor)
