---
title: Transcript Viewer
category: frontend
owners: [frontend-team]
last_updated: 2026-04-12
---

# Transcript Viewer

## Purpose

The reading and editing surface for a Note. Shows the Transcript on the left and the Extraction (Topics, Decisions, Action Items) on the right.

## Transcript pane

Each Utterance is rendered with its speaker label, timestamp, and text. Clicking an Utterance scrubs the audio player to its start. Editing an Utterance writes to the Note's transcript_overlay; the original Transcript is never mutated.

## Extraction pane

Topics are listed with a one-line summary; expanding a Topic reveals its bounded Utterance range. Decisions and Action Items each have their own collapsible section. Every item links back into the Transcript pane via its citation Utterances; clicking the link scrolls and highlights.

## Speaker labels

Unresolved Speaker Tags (`Tag-1`) appear as buttons the user can click to assign a Speaker Profile. Resolved Profiles appear as plain names with an edit pencil for re-assignment.

## Quality Flags

Quality Flags surface as inline highlights on the affected Utterance ranges with a tooltip naming the flag kind and severity.
