# Scribe Skills

A Claude Code plugin marketplace for spec-driven development. Two skills that turn a living wiki into tickets that drive Claude Code implementation:

- **wiki-page-author** — write, update, and organise project wiki pages as a living spec. Ships with the `wiki-page-reviewer` subagent.
- **ticket-author** — turn wiki pages (or wiki diffs) into tickets. Ships with the `ticket-reviewer` subagent.

## Install

Add this repo as a Claude Code plugin marketplace:

```
/plugin marketplace add sheriff-stuff/Scribe-Skills
```

Then install one or both plugins:

```
/plugin install wiki-page-author@scribe-skills
/plugin install ticket-author@scribe-skills
```

Or run `/plugin`, pick `Browse and install plugins`, then `scribe-skills`.

## Layout

```
.claude-plugin/marketplace.json   Plugin manifest
skills/
  wiki-page-author/               SKILL.md + agents/wiki-page-reviewer.md
  ticket-author/                  SKILL.md + agents/ticket-reviewer.md
wiki/                             Living spec for the skills themselves
```

The wiki is the source of truth. If `wiki/` and `skills/` disagree on `master`, the wiki is right and the skill needs updating.
