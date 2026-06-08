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
.claude-plugin/marketplace.json   Plugin manifest (one source per plugin)
plugins/
  wiki-page-author/               source root
    skills/wiki-page-author/      SKILL.md + agents/wiki-page-reviewer.md
  ticket-author/                  source root
    skills/ticket-author/         SKILL.md + assets/
    skills/ticket-ultra-review/   SKILL.md
    agents/ticket-reviewer.md
wiki/                             Living spec for the skills themselves
```

The wiki documents the shipped skills. If `wiki/` and `plugins/` disagree on `master`, the skill is right and the wiki needs updating.
