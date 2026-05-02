---
title: Ticket Conventions
category: process
owners: [eng-leads]
last_updated: 2026-04-12
---

# Ticket Conventions

## Purpose

Names the labels, milestones, and naming rules used when filing Cortex tickets. This page is the source of truth for any tool or skill that creates tickets on behalf of a developer.

## Types

Cortex uses four ticket types. They are not labels — they are explicit fields: Epic, Feature, Spike, Bug. Use Epic only when a body of work has multiple child tickets that belong together.

## Labels

Labels are area tags, never types. The accepted labels are:
- `area:ingest` — work on the Ingest Service.
- `area:transcription` — work on the Transcription or Diarization Service.
- `area:extraction` — work on the Extraction Service or Templates.
- `area:notes` — work on the Notes Service or Notes Explorer.
- `area:frontend` — work on the web app outside of Notes Explorer (Template Editor, Settings, Component Library).
- `area:platform` — Job Orchestrator, storage, realtime, deployment, infra.
- `area:ml` — model runtime and model lifecycle.
- `area:docs` — wiki and in-app documentation.

## Milestones

Milestone names follow `YYYY-QN` (e.g. `2026-Q2`). Quarterly milestones are advisory; tickets without a milestone are still actionable.

## Naming

Ticket titles use sentence case. They name the outcome, not the implementation. Bad: 'Add a useDebouncedSearch hook'. Good: 'Debounce notes explorer search input'.

## Body

Tickets answer **what** is being done and **how it will be verified**. The **why** lives in the wiki. If a ticket needs to justify itself, link to the wiki page that holds the justification — and if no such page exists, suggest creating one rather than inlining the rationale.

## Acceptance criteria

Acceptance criteria are falsifiable checks a reviewer can run. They are not restatements of scope, not project-wide baselines (build/lint/test expectations belong in the contributor docs), and not subjective ('feels idiomatic').
