---
title: Transcription Service
category: services
owners: [ml-team]
last_updated: 2026-04-12
---

# Transcription Service

## Responsibility

Produces a Transcript from a Recording by running ASR and emitting an ordered list of Utterances.

## Inputs

A Recording id (the service reads media path from the Recording row).

## Outputs

A Transcript with Utterances. The Transcript is written without Speaker Tags — those are added by the Diarization Service.

## Model lifecycle

The service owns model load and warm-up. The first Transcription Job after process start is slower; subsequent Jobs reuse the loaded model. Model is unloaded after a configurable idle period to free memory.

## Concurrency

Single-worker by default. Multiple workers can be configured but are gated by available accelerator memory; the Job Orchestrator never schedules more Transcription Jobs in parallel than the configured worker count.

## Related

- [Model Runtime](../architecture/model-runtime)
- [Diarization Service](diarization-service)
- [Transcript](../domain/transcript)
