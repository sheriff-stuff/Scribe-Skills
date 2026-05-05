# Scribe Skills

Scribe Skills is a collection of reusable skills and agents that support a spec-driven development workflow. The skills are project-agnostic — point them at any project (including this one).

## The workflow

1. **Wiki page** — write or update a wiki page that describes the feature as a living spec. (skill: `wiki-page-author`)
2. **Tickets** — turn the wiki page (or the diff against it) into tickets. (skill: `create-tickets`)
3. **Do the work** — pick up tickets and implement. No dedicated skill; handled by regular Claude Code.
4. **Pull request** — open the PR. No dedicated skill.

This repo is dogfooded on itself: when a skill here is added or changed, its wiki page is updated first, and tickets are cut from that change.

## What the wiki is

A living spec describing the current state of the thing being documented — present tense, factual, reference-only.

- No history, no rationale, no explanation, no tutorials.
- Pages describe what the thing is. If something changes, the page is updated to reflect the new state; the previous wording is not preserved.
- Open questions live in inline `> [!ODD]` callout blocks placed next to the section they affect, and are removed once resolved.
- A single `Changelog` page records what changed (added / removed / changed from X to Y), never why. The why lives in commits and MRs.
- Folders and pages are named by subject, not by content type or format.

The wiki is the source of truth that tickets and feature specs are built on top of.

## What this repo contains

- `.claude/skills/wiki-page-author/` — authors wiki pages.
- `.claude/skills/create-tickets/` — generates tickets.
- `fixtures/cortex-wiki/` — an example wiki used to develop and test the skills against. A fixture, not a real wiki.

## Versioning and release branches

The repo follows SemVer with a release-branch workflow. Trunk is `master`; release branches are `vX.Y`; releases are tagged `vX.Y.Z`. When asked to "create a new release branch", "cut a release", or do related branch/tag work, follow [`wiki/Versioning-Strategy.md`](wiki/Versioning-Strategy.md) as the source of truth.

## Writing rules

These apply to everything written in this repo — skills, wiki pages, tickets, commit messages, PR descriptions.

1. **No pleonasm.** Do not append phrases that re-assert what the preceding sentence already said. The closing-reassurance flavor ("nothing more", "just that", "and that's it", "simple as that", "no more, no less") is the most common form.

   **Bad — closing reassurance restates the scope:**

   > It points back to the owner, nothing more.

   **Good — the sentence already bounds itself:**

   > It points back to the owner.

## Helpful references

Two places that are useful when working on skills — reach for them when grounding in the spec or in real examples would help, but they're not required for every task:

1. **https://agentskills.io/llms.txt** — the public docs index. Good to fetch when creating, reviewing, validating, or auditing a skill if you want to check the official rules.
2. **`../anthropics-skills/`** (sibling to this repo, at `C:\Users\PC\work\anthropics-skills\`) — local clone of the official Anthropic skills repo (`README.md`, `spec/`, `template/`, and real-world `skills/` examples). Useful as a structural reference and to see how working skills are put together.

Prefer these over guessing from memory when spec details actually matter. Otherwise, use judgment.
