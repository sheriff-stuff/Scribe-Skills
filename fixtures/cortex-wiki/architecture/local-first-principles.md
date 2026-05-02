---
title: Local-first Principles
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Local-first Principles

## Purpose

Cortex is local-first. This page names what that means concretely so the rule is enforceable in reviews and design discussions.

## Principles

1. **No external network call is required for the core flow.** A user with Cortex installed and the default models present must be able to take a Recording from upload to Note without internet access.
2. **Cloud is opt-in, never default.** Any cloud endpoint (LLM API, hosted ASR) is a configurable alternative. The default configuration uses local model runtimes.
3. **All user data lives on the user's machine.** Recordings, Transcripts, Extractions, and Notes are stored in the local database and the local media directory. Cortex must not phone home.
4. **Telemetry is opt-in and minimal.** When enabled, telemetry is anonymised and never includes Recording content or Transcript text.

## Why

See [ADR: local-first default](../adrs/local-first-default) for the reasoning behind making local the default rather than an option, and the trade-offs involved (model size, install footprint).
