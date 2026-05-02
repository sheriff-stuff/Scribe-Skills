---
title: Known Failure Modes
category: ops
owners: [support-team]
last_updated: 2026-04-12
---

# Known Failure Modes

## Purpose

Cortex's known failure modes and the in-app surfaces that recover from them.

## Failure modes

- **Backend startup blocked by port conflict.** The configured port is exposed in the settings file as `backend.port`.
- **Transcription Job idle while LLM runtime is stopped.** The settings page shows runtime status and a 'Start runtime' control.
- **Extraction Job exceeds its per-stage timeout when the configured LLM is too small for the Transcript.** The model selector in the settings page lists compatible larger models and the cloud fallback endpoint.
- **Quality Flags emitted across the entire Recording.** The Audio Quality Service raises this pattern when the source media itself is low quality; no in-app recovery exists for the existing Recording.

## Logs

Backend logs land in `logs/cortex.log` inside the Cortex data directory. The settings page exposes a 'Show logs' control that opens this file in the platform's default viewer.
