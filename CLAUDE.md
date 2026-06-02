# Scribe Skills

Scribe Skills is a Claude Code plugin marketplace of reusable extensions — skills, subagents, hooks, slash commands, and anything else that plugs into Claude Code — supporting a spec-driven development workflow. Everything here is project-agnostic; point it at any project (including this one).

Installable plugins are declared in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) and consumed via `/plugin marketplace add sheriff-stuff/Scribe-Skills`. Everything under `skills/` and `.claude/` is read by Claude Code, not humans — templates and assets are instructions to the agent.

This repo is dogfooded on itself, but with the polarity flipped from the consumer workflow above. For projects that *use* these skills, the wiki is the spec and code follows. **For this repo, the shipped skill in `skills/` is authoritative — the wiki documents it.** If `wiki/` and `skills/` (or `.claude/`) disagree on `master`, the skill is right and the wiki needs updating.

**The wiki must match `skills/` and `.claude/` before a PR is opened; mid-branch commits can diverge.** Iterate on skills, subagents, hooks, and slash commands freely — individual commits need not touch the wiki. Before pushing the PR, sync the affected wiki pages in the same branch so the update lands in the PR diff. Tickets are cut from the wiki diff during feature work.

## What the wiki is

A living spec describing the current state of the thing being documented — present tense, factual, reference-only.

- No history, no rationale, no explanation, no tutorials.
- Pages describe what the thing is. If something changes, the page is updated to reflect the new state; the previous wording is not preserved.
- Open questions live in inline `> [!ODD]` callout blocks placed next to the section they affect, and are removed once resolved.
- A single `Changelog` page records what changed (added / removed / changed from X to Y), never why. The why lives in commits and MRs.
- Folders and pages are named by subject, not by content type or format.

The wiki is the source of truth that tickets and feature specs are built on top of.

## What this repo contains

- `.claude-plugin/marketplace.json` — plugin marketplace manifest. Declares the installable plugins (`wiki-page-author`, `ticket-author`).
- `skills/` — reusable skills shipped to marketplace installers. Each skill folder holds its `SKILL.md`, `assets/`, `references/`, and any bundled subagents under `agents/`.
- `.claude/commands/` — slash commands used while working in this repo (e.g. `/count-skill-tokens`). Local-only; not shipped via the marketplace.
- `wiki/` — the living spec for everything in `skills/` and `.claude/`.

## Rules

These apply to everything written in this repo — skills, subagents, hooks, slash commands, wiki pages, tickets, commit messages, PR descriptions.

### British spelling

Write in British English.

### No pleonasm

Do not append phrases that re-assert what the preceding sentence already said. The closing-reassurance flavour ("nothing more", "just that", "and that's it", "simple as that", "no more, no less") is the most common form.

**Bad — closing reassurance restates the scope:**

> It points back to the owner, nothing more.

**Good — the sentence already bounds itself:**

> It points back to the owner.

### No revision history

Updates replace content; do not annotate what changed. This applies to skills, subagents, slash commands, and other shipped files just as it does to wiki pages — Claude only sees the current state, so phrasing like "no heading and no anchor", "no longer uses X", or "previously …" describes a delta that does not exist in its world.

### Don't restate template shape in skill prose

When a skill ships a template asset, the SKILL.md links to it and lets the template carry the shape. Do not re-describe in prose what the template already shows: placeholder syntax, field order, which fields are optional, placement comments, "ID lives on the first line", etc. Prose carries only what the template cannot express — policy, workflow, cross-skill contracts, and judgement calls (e.g. how to pick a good slug).

## Helpful references

Two places that are useful when working on Claude Code extensions — reach for them when grounding in the spec or in real examples would help, but they're not required for every task:

- **<https://agentskills.io/llms.txt>** — the public docs index. Good to fetch when creating, reviewing, validating, or auditing a skill if you want to check the official rules.
- **`../anthropics-skills/`** (sibling to this repo) — local clone of the official Anthropic skills repo (`README.md`, `spec/`, `template/`, and real-world `skills/` examples). Useful as a structural reference and to see how working skills are put together.

For subagents, hooks, slash commands, and other Claude Code features, the `claude-code-guide` agent is the fastest way to check official behaviour.

Prefer these over guessing from memory when spec details actually matter. Otherwise, use judgement.
