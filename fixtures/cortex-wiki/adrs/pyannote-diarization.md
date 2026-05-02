---
title: ADR: Diarization Model Choice
category: adrs
owners: [ml-team]
last_updated: 2025-10-15
---

# ADR: Diarization Model Choice

## Context

Speaker diarization can run entirely with the ASR engine (some engines bundle a diarizer) or as a separate model invoked after ASR. The latter produces measurably better speaker boundaries on meeting audio with multiple participants.

## Decision

Run diarization as a separate model after ASR. Cortex bundles a default diarization model and exposes it through the Diarization Service.

## Consequences

- Diarization quality is meaningfully better on noisy meeting audio.
- The Pipeline gains an extra stage and the model set gains an extra model; install footprint grows.
- Future ASR engine swaps don't lose diarization quality because the diarizer is independent.
