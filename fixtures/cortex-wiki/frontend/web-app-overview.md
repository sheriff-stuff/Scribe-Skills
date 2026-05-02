---
title: Web App Overview
category: frontend
owners: [frontend-team]
last_updated: 2026-04-12
---

# Web App Overview

## Purpose

Describes the shape of the Cortex web app: routes, primary views, and how the frontend connects to the backend.

## Stack

React with TypeScript, built with Vite. Styling uses a utility-CSS approach with a small in-house component library (see [Component Library](component-library)). Editor surfaces use CodeMirror.

## Routes

- `/` — Notes Explorer (default landing).
- `/notes/:id` — Note view (Transcript Viewer + Extraction sidebar).
- `/templates` — Template list.
- `/templates/:id` — Template Editor.
- `/upload` — drag-and-drop upload, also accessible as a modal from any page.
- `/settings` — configuration (model paths, storage directory, theme).

## Backend connection

All data calls go through the local FastAPI backend at `http://localhost:<port>`. Long-running progress comes over the SSE channel described in [Realtime Progress](../architecture/realtime-progress).

## Where to read next

- [Notes Explorer](notes-explorer)
- [Transcript Viewer](transcript-viewer)
- [Template Editor](template-editor)
- [State Management](state-management)
