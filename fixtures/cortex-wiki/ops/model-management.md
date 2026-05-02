---
title: Model Management
category: ops
owners: [ml-team]
last_updated: 2026-04-12
---

# Model Management

## Purpose

How to install, update, and remove the speech-recognition, diarization, and language models that Cortex runs locally.

## Default models

The installer bundles the default ASR model, the default diarization model, and a small default LLM. These are the only models needed to run Cortex out of the box.

## Adding models

Additional ASR or diarization models can be dropped into the configured models directory; Cortex picks them up on next start. Additional LLMs are pulled via the local LLM runtime's standard mechanism.

## Updating models

Updates ship with the application. When a Cortex update changes the default ASR model version, existing Transcripts are not re-processed — the Transcript's `model_version` field continues to report the version it was created with.

## Switching models

Switching the active LLM is a configuration change. Existing Notes pin the Template version they were extracted with, but not the LLM — re-running Extraction after switching LLMs may produce different output.
