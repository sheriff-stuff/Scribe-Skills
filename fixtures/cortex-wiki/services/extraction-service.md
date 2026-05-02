---
title: Extraction Service
category: services
owners: [ml-team]
last_updated: 2026-04-12
---

# Extraction Service

## Responsibility

Produces an Extraction (Topics, Decisions, Action Items, summary) from a Transcript using a Template.

## Inputs

A Transcript id and a Template version reference. If the Template reference is omitted, the default Template is used.

## Outputs

An Extraction row plus rows for its Topics, Decisions, and Action Items.

## Chunking

Long Transcripts are partitioned into chunks sized for the LLM context window with a configurable overlap (default 60 seconds of audio). Each chunk is extracted independently and the partial results are merged. See [ADR: chunked extraction](../adrs/chunked-extraction) for the chunk-size rationale.

## Citation enforcement

Every Topic, Decision, and Action Item produced by the LLM must cite at least one Utterance id. The service rejects (and re-prompts once) outputs that fail this check; if the second attempt also fails the offending item is dropped.

## Failure mode

If extraction fails, the Transcript is preserved intact and the user can re-run with the same or a different Template (see [ADR: two-phase pipeline](../adrs/two-phase-pipeline)).

## Related

- [Extraction](../domain/extraction)
- [Template](../domain/template)
- [Model Runtime](../architecture/model-runtime)
