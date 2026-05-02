---
title: ADR: Local LLM Runtime Default
category: adrs
owners: [ml-team]
last_updated: 2025-09-18
---

# ADR: Local LLM Runtime Default

## Context

Cortex needs an LLM to power the Extraction Service. The choice is between bundling a self-hosted runtime (Ollama-compatible) or defaulting to a hosted provider with the option to switch.

## Decision

Default to a local LLM runtime that exposes an OpenAI-compatible API. Cloud providers (OpenAI, Anthropic) are opt-in via configuration.

## Consequences

- The default install includes a local LLM, increasing install footprint substantially.
- Users with hardware that struggles to run a local LLM can opt into a cloud provider; this is documented in [Troubleshooting Guide](../ops/troubleshooting-guide).
- The Extraction Service speaks the OpenAI chat-completions protocol; switching providers is a configuration change, not a code change.
