---
title: Template Editor
category: frontend
owners: [frontend-team]
last_updated: 2026-04-12
---

# Template Editor

## Purpose

The view at `/templates/:id` for editing a Template's name, description, and prompt text.

## Editing surface

The prompt text uses CodeMirror with markdown highlighting. Saving creates a new version of the Template; the previous version remains accessible via a version selector.

## Built-in Templates

Built-in Templates are read-only. The editor surfaces a 'Clone to edit' affordance instead of a save button.

## Preview

A 'Preview against a Note' affordance lets the user select an existing Note and re-run extraction with the in-progress Template. The preview output is discarded unless the user explicitly applies it.

## Related

- [Template](../domain/template)
- [Template Service](../services/template-service)
