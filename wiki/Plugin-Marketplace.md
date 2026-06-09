# Plugin Marketplace

The repo is a Claude Code plugin marketplace. Installers add it once, then install one or more plugins from it.

## Manifest

[`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) at the repo root declares the marketplace. The `plugins` array lists each installable plugin. Each entry names the plugin, describes it, and points its `source` at the plugin's own folder under [`plugins/`](../plugins/). Claude Code discovers that plugin's skills and reviewer subagent automatically from the source root, so the manifest lists no per-component paths.

## Plugins

| Plugin | Bundles |
| --- | --- |
| `wiki-page-author` | [Wiki Page Author](Wiki-Page-Author) skill and the [Wiki Page Reviewer](Wiki-Page-Reviewer) subagent. |
| `ticket-author` | [Ticket Author](Ticket-Author) and [Ticket Ultra Review](Ticket-Ultra-Review) skills and the [Ticket Reviewer](Ticket-Reviewer) subagent. |

Each plugin is independently installable.

## Reviewer subagents

Each plugin ships a reviewer subagent, installed with the plugin and invoked by name. The skill's frontmatter references its reviewer by name, not by path.

Each reviewer is a plugin agent whose file lives at its plugin's root `agents/` directory, where Claude Code discovers it automatically: [`plugins/ticket-author/agents/`](../plugins/ticket-author/agents/) and [`plugins/wiki-page-author/agents/`](../plugins/wiki-page-author/agents/).

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
