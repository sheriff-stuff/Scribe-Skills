---
title: Extension Points
category: architecture
owners: [platform-team]
last_updated: 2026-04-12
---

# Extension Points

## Purpose

Names the interfaces that are deliberately swappable. Anything not listed here is internal and may change without notice.

## Swappable

- **LLM endpoint** — the Extraction Service speaks an OpenAI-compatible API; pointing it at a different endpoint is a config change.
- **ASR engine** — wrapped behind a minimal Transcriber interface (transcribe → list of Utterances). A user with a different ASR can supply their own implementation.
- **Storage backend** — SQLite vs. Postgres is a config switch (see [Storage Layer](storage-layer)).
- **Templates** — the most important extension point for users; see [Template](../domain/template) and [Template Editor](../frontend/template-editor).

## Not swappable (yet)

- The diarization model — wired in at the Transcription Service boundary.
- The Pipeline phase ordering — the two-phase structure is load-bearing for the system's failure model.
