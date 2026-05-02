---
title: Diarization Service
category: services
owners: [ml-team]
last_updated: 2026-04-12
---

# Diarization Service

## Responsibility

Assigns a Speaker Tag to each Utterance in a Transcript and produces a voice embedding per Tag for later resolution to Speaker Profiles.

## Inputs

A Transcript id and the underlying Recording's media path.

## Outputs

Updates each Utterance with a `speaker_tag` and writes a per-Tag embedding into a side table for the Notes Service to consume during Profile resolution.

## Resolution scope

Diarization does **not** resolve Tags to Speaker Profiles. Tags like `Tag-1`, `Tag-2` are scoped to a single Transcript. The Notes Service performs cross-Recording resolution by comparing embeddings.

## Failure mode

If diarization fails, the Transcript is preserved with all Utterances assigned the placeholder tag `Tag-Unknown`. The Job is marked failed; the user can re-run diarization without re-transcribing.

## Related

- [Utterance](../domain/utterance)
- [Speaker Profile](../domain/speaker-profile)
- [ADR: diarization model choice](../adrs/pyannote-diarization)
