---
title: Local Deployment
category: ops
owners: [platform-team]
last_updated: 2026-04-12
---

# Local Deployment

## Purpose

How to install, run, and uninstall Cortex on a single user's machine — the supported deployment shape.

## Install

Cortex ships as a single installer per platform (macOS, Windows, Linux). The installer drops the backend, the bundled web app, and the default models into the application data directory and registers a launch agent / service.

## Run

On launch, Cortex starts the FastAPI backend on a loopback port, runs migrations, ensures the local LLM runtime is reachable (starts it if not), and opens the web app in the user's default browser.

## Configuration

User configuration lives in a single JSON file in the application data directory. Settings can be edited from the `/settings` route or by editing the file directly. See [Troubleshooting Guide](troubleshooting-guide) for common issues.

## Uninstall

Uninstall removes the application binaries but leaves the user's data directory intact. The user must opt in to a clean uninstall to delete Recordings, Transcripts, and Notes.
