---
title: Action Item
category: domain
owners: [ml-team]
last_updated: 2026-04-12
---

# Action Item

## Purpose

A task assigned during a Recording. Action Items are the most-exported Extraction artifact — many users open Cortex specifically to grab their Action Items from a meeting.

## Fields

- `id` — ULID.
- `extraction_id` — FK.
- `text` — the task as a single sentence in imperative form.
- `owner_speaker_profile_id` — nullable FK to Speaker Profile.
- `due_date` — nullable, parsed from the Utterance text when phrased explicitly.
- `citation_utterance_ids` — at least one.

## Owner resolution

If the Utterance contains a name that resolves to a known Speaker Profile, that Profile is the owner. If the speaker says 'I'll do X', the owner is the Speaker Profile attributed to that Utterance. Otherwise the owner is null.

## Related

- [Extraction](extraction)
- [Utterance](utterance)
- [Speaker Profile](speaker-profile)
