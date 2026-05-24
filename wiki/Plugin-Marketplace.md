# Plugin Marketplace

The repo is a Claude Code plugin marketplace. Installers add it once, then install one or more plugins from it.

## Manifest

[`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) at the repo root declares the marketplace. The `plugins` array lists each installable plugin. Each entry names the plugin, describes it, and points at the skill folders it bundles under `skills/`.

## Plugins

| Plugin | Bundles |
| --- | --- |
| `wiki-page-author` | [Wiki Page Author](Wiki-Page-Author) skill and the [Wiki Page Reviewer](Wiki-Page-Reviewer) subagent. |
| `ticket-author` | [Ticket Author](Ticket-Author) skill and the [Ticket Reviewer](Ticket-Reviewer) subagent. |

Each plugin is independently installable.

## Bundled subagents

A skill ships its reviewer subagent inside `skills/<skill-name>/agents/`. The subagent is installed as part of the plugin and is invoked by name. The skill's frontmatter references the subagent by name, not by path.

## Local-only tooling

The [`/count-skill-tokens`](Count-Skill-Tokens) slash command lives under `.claude/commands/` and is not shipped through the marketplace. It is available only when working inside this repo.

## Install

Adding the marketplace:

```
/plugin marketplace add sheriff-stuff/Scribe-Skills
```

Installing a plugin:

```
/plugin install wiki-page-author@scribe-skills
/plugin install ticket-author@scribe-skills
```
