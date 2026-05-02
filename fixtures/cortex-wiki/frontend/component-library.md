---
title: Component Library
category: frontend
owners: [frontend-team]
last_updated: 2026-04-12
---

# Component Library

## Purpose

Names the in-house components the app builds on. Components live alongside the routes that consume them; nothing in this list is imported from an external design system.

## Components

- **Stack** — vertical/horizontal layout primitive.
- **Card** — bordered container used for Note rows and Template list rows.
- **Badge** — used for tags, severity indicators, and Speaker labels.
- **Toolbar** — top-of-view bar with slots for search, filters, and actions.
- **Modal** — used for upload, settings, and destructive confirmations.
- **AudioPlayer** — wraps the native `<audio>` element with timeline scrubbing tied to Utterance boundaries.
- **TranscriptList** — virtualised list of Utterances. Used by the Transcript Viewer.
- **JobProgress** — small progress indicator that subscribes to the SSE channel for a given Recording.
