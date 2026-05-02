---
title: Release Process
category: process
owners: [eng-leads]
last_updated: 2026-04-12
---

# Release Process

## Purpose

How Cortex versions are cut, signed, and shipped to users.

## Cadence

Minor releases ship monthly. Patch releases ship as needed. Major releases are reserved for changes to the data model that require user-visible migration.

## Cut

A release is cut by tagging the release commit with a semantic-version tag. CI builds installers for macOS, Windows, and Linux from the tag.

## Signing

Installers are signed with the platform's standard code-signing tool before they leave CI. Unsigned builds are not distributed.

## Hotfixes

Hotfixes branch from the most recent release tag, land the fix, and re-tag with a new patch version. Hotfixes ship installers immediately; main may not have caught up yet.
