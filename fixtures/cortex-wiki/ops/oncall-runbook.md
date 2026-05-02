---
title: On-call Runbook
category: ops
owners: [support-team]
last_updated: 2026-04-12
---

# On-call Runbook

## Purpose

Cortex is local-first; there is no operations on-call rotation in the traditional sense. This runbook exists for support engineers responding to user reports.

## First responders

Support engineers triage user reports through the issue tracker. Critical-severity reports (data loss, data corruption, complete inability to start) escalate to the platform team.

## Diagnostic bundle

Users can produce a diagnostic bundle from the settings page that includes recent logs, the configuration file, and the migrations history. The bundle never contains Recording media, Transcript text, or Extraction content.

## Escalation

If a fix requires a code change, support files a ticket per [Ticket Conventions](../process/ticket-conventions). Hotfix releases follow [Release Process](../process/release-process).
