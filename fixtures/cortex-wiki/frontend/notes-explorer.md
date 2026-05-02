---
title: Notes Explorer
category: frontend
owners: [frontend-team]
last_updated: 2026-04-12
---

# Notes Explorer

## Purpose

The default landing view: a paginated list of Notes with filters and a prominent upload affordance.

## Layout

- Top bar: upload button, search input (placeholder today; full-text search is unbuilt — see [Notes Service](../services/notes-service)), tag filter chips, date range filter.
- Main: list of Note rows showing title, recorded-at, duration, primary speaker, Quality Flag badges.
- Empty state: a single CTA encouraging upload.

## Sort

Default sort is `recorded_at` descending. Secondary sort by `created_at`. Sort order is not user-configurable in the current build.

## Live updates

Rows update in place when the SSE channel reports a Job state change for their Recording. A Note row shows a progress indicator while Jobs are in flight and transitions to fully-rendered when both phases complete.
