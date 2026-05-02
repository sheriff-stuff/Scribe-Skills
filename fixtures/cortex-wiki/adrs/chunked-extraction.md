---
title: ADR: Chunked Extraction with Overlap
category: adrs
owners: [ml-team]
last_updated: 2025-11-08
---

# ADR: Chunked Extraction with Overlap

## Context

Long Transcripts (1+ hour meetings) exceed the context window of the default LLM. Naive truncation loses information; naive chunking at fixed boundaries loses Topics and Decisions that span the boundary.

## Decision

The Extraction Service partitions long Transcripts into chunks sized for the LLM context window with a configurable overlap defaulting to 60 seconds of audio. Per-chunk Extractions are merged with duplicate detection on citation overlap.

## Consequences

- No Topic or Decision is silently dropped at a chunk boundary.
- Total LLM cost grows roughly with the number of chunks, not with audio length squared; the overlap is bounded.
- The merge step adds complexity and introduces a well-defined failure mode (LLM produces conflicting summaries across chunks); this is handled by the Extraction Service's deduplication step.
