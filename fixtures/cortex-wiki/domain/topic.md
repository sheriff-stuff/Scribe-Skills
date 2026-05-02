---
title: Topic
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Topic

## Purpose

A discussion subject extracted from a Transcript. Topics are the primary navigational unit for a Note: the user typically scans Topics first and drills into Utterances second.

## Fields

- `id` — ULID.
- `extraction_id` — FK.
- `title` — short human-readable label.
- `summary` — one-line.
- `start_utterance_id` / `end_utterance_id` — bounding range within the Transcript.
- `citation_utterance_ids` — list of additional supporting Utterance IDs.

## Constraints

Topics must be non-empty, must cite at least one Utterance, and must not overlap each other within an Extraction. Overlap is rejected at merge time (see [Pipeline Stages](../architecture/pipeline-stages)).

## Related

- [Extraction](extraction)
- [Utterance](utterance)
