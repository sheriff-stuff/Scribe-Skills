# Scribe Skills

Scribe Skills is a collection of skills and agents that build and maintain a wiki for a separate application.

The wiki is the deliverable. The skills and agents in this repo are the tools that produce it. The application being documented lives elsewhere; this repo does not contain its source code.

## What the wiki is

A living spec describing the current state of the application — present tense, factual, reference-only.

- No history, no rationale, no explanation, no tutorials.
- Pages describe what the application is. If something changes, the page is updated to reflect the new state; the previous wording is not preserved.
- Open questions live in an `## Open design decisions` section on the relevant page, and are removed once resolved.
- A single `Changelog` page records what changed (added / removed / changed from X to Y), never why. The why lives in commits and MRs.
- Folders and pages are named by subject, not by content type or format.

The wiki feeds a later spec-driven development workflow. Treat it as the source of truth that future feature specs will be built on top of.

## What this repo contains

- Skills and agents that generate, update, and maintain wiki pages.
- The wiki repo itself is separate.
- `fixtures/cortex-wiki/` — an example wiki used to help build and test the skills in this repo. Treat it as a fixture to develop against, not as the real wiki.

## Helpful references

Two places that are useful when working on skills — reach for them when grounding in the spec or in real examples would help, but they're not required for every task:

1. **https://agentskills.io/llms.txt** — the public docs index. Good to fetch when creating, reviewing, validating, or auditing a skill if you want to check the official rules.
2. **`../anthropics-skills/`** (sibling to this repo, at `C:\Users\PC\work\anthropics-skills\`) — local clone of the official Anthropic skills repo (`README.md`, `spec/`, `template/`, and real-world `skills/` examples). Useful as a structural reference and to see how working skills are put together.

Prefer these over guessing from memory when spec details actually matter. Otherwise, use judgment.
