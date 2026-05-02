---
title: ADR: Two-phase Pipeline
category: adrs
owners: [platform-team]
last_updated: 2025-09-04
---

# ADR: Two-phase Pipeline

## Context

An end-to-end Pipeline that runs transcription and extraction in a single inseparable step risks losing the Transcript when the LLM fails or when the user wants to re-run extraction with different settings. Transcripts are expensive to produce; Extractions are cheap and explicitly user-tunable.

## Decision

The Pipeline is split into two phases: a Transcription Phase that ends with a sealed Transcript, and an Extraction Phase that consumes the Transcript and produces an Extraction. The phases are scheduled as separate Jobs by the Job Orchestrator and have separate failure modes.

## Consequences

- A failed Extraction never costs the user their Transcript.
- Re-running Extraction with a different Template is supported by construction.
- The Pipeline has more moving parts; the Job Orchestrator must coordinate two Jobs per Recording rather than one.

## Alternatives considered

A single fused Job was considered. It is simpler but fails the 'preserve Transcript on Extraction failure' requirement and would be hostile to the 'try a different Template' workflow.
