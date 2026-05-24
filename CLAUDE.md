# Scribe Skills

Scribe Skills is a Claude Code plugin marketplace of reusable extensions — skills, subagents, hooks, slash commands, and anything else that plugs into Claude Code — supporting a spec-driven development workflow. Everything here is project-agnostic; point it at any project (including this one).

Installable plugins are declared in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) and consumed via `/plugin marketplace add sheriff-stuff/Scribe-Skills`. Everything under `skills/` and `.claude/` is read by Claude Code, not humans — templates and assets are instructions to the agent.

## The workflow

1. **Wiki page** — write or update a wiki page that describes the feature as a living spec. (skill: `wiki-page-author`)
2. **Tickets** — turn the wiki page (or the diff against it) into tickets. Each ticket is a prompt for Claude Code: combined with the wiki, it drives an LLM agent to produce code and a PR. (skill: `ticket-author`)
3. **Do the work** — pick up tickets and implement. No dedicated skill; handled by regular Claude Code.
4. **Pull request** — open the PR. No dedicated skill.

This repo is dogfooded on itself. **The wiki must match `skills/` and `.claude/` before a PR is opened; mid-branch commits can diverge.** Iterate on skills, subagents, hooks, and slash commands freely — individual commits need not touch the wiki. Before pushing the PR, sync the affected wiki pages in the same branch so the update lands in the PR diff. The wiki is the spec; if the wiki and the shipped files disagree on `master`, the wiki is wrong. Tickets are cut from the wiki diff.

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
- `fixtures/cortex-wiki/` — an example wiki used to develop and test against. A fixture, not a real wiki.

## Versioning and release branches

The repo follows SemVer with a release-branch workflow. Trunk is `master`; release branches are `vX.Y`; releases are tagged `vX.Y.Z`. When asked to "create a new release branch", "cut a release", or do related branch/tag work, follow [`wiki/Versioning-Strategy.md`](wiki/Versioning-Strategy.md) as the source of truth.

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

**Bad:**

> Sessions now persist across browser restarts (previously they expired on close).

**Good:**

> Sessions persist across browser restarts.

**Bad — references a removed mechanism the reader has never seen:**

> The ID lives on the callout line; there is no heading and no anchor.

**Good — states what is:**

> The ID lives on the callout line. Pointer blocks reference it by name.

### Don't cite rules by number

In skills, subagents, hooks, slash commands, and any prose pointing at a rule maintained elsewhere, reference the rule by its name (the bolded lead) — not by its ordinal position. Rule numbers shift the moment a rule is added, removed, or reordered, and every existing citation silently misaligns.

Applies equally to: prose like "Body Rule 4 forbids hedging", schema enums like `Rule: Body Rule N`, and output examples that show a numeric citation.

**Bad — ordinal pin rots when the list changes:**

> Cite the violation as `Rule: Body Rule 2`.

**Good — name survives reordering:**

> Cite the violation as `Rule: Names follow the subject, not the content type` (or a short, faithful paraphrase of the bolded rule lead).

### Don't restate template shape in skill prose

When a skill ships a template asset, the SKILL.md links to it and lets the template carry the shape. Do not re-describe in prose what the template already shows: placeholder syntax, field order, which fields are optional, placement comments, "ID lives on the first line", etc. Prose carries only what the template cannot express — policy, workflow, cross-skill contracts, and judgement calls (e.g. how to pick a good slug).

**Bad — prose restates what the template already shows:**

> The ID lives on the first line of the callout, followed by an em-dash and the one-sentence reason. The block sits at the top of the page, immediately after the H1 description paragraph. `Context:` is optional.

**Good — prose points at the template and carries only policy:**

> See the [caution template](assets/caution-template) for the canonical shape. One caution per page maximum.

## Helpful references

Two places that are useful when working on Claude Code extensions — reach for them when grounding in the spec or in real examples would help, but they're not required for every task:

- **https://agentskills.io/llms.txt** — the public docs index. Good to fetch when creating, reviewing, validating, or auditing a skill if you want to check the official rules.
- **`../anthropics-skills/`** (sibling to this repo) — local clone of the official Anthropic skills repo (`README.md`, `spec/`, `template/`, and real-world `skills/` examples). Useful as a structural reference and to see how working skills are put together.

For subagents, hooks, slash commands, and other Claude Code features, the `claude-code-guide` agent is the fastest way to check official behaviour.

Prefer these over guessing from memory when spec details actually matter. Otherwise, use judgement.
