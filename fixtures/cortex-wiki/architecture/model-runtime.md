---
title: Model Runtime
category: architecture
owners: [ml-team]
last_updated: 2026-04-12
---

# Model Runtime

## Purpose

Describes how Cortex runs the speech-recognition and language models that power the Pipeline.

## Speech recognition

ASR runs locally via a bundled engine that exposes a synchronous transcribe call returning timestamped Utterances with confidence scores. The Transcription Service is the only caller; it owns model lifecycle (load, warm-up, unload) for the worker.

## Diarization

Diarization is a separate model invoked after ASR. It produces Speaker Tags but does not resolve them to Speaker Profiles — that is the Notes Service's job, via voice-embedding match against existing Profiles.

## Language model

The default LLM runtime is a local server (Ollama-compatible API). The Extraction Service speaks the OpenAI chat-completions protocol against this local endpoint. Cloud endpoints (OpenAI, Anthropic) can be configured but are not enabled by default. See [ADR: LLM runtime default](../adrs/llm-runtime-default).

## Hardware fallback

Cortex auto-detects available accelerators (CUDA on Linux/Windows, Metal on macOS) and falls back to CPU. On CPU-only systems the Transcription Service switches to a smaller model variant; the user sees a Quality Flag advising that transcription accuracy is reduced.
