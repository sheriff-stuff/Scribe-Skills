# Plugin Marketplace

The repo is a Claude Code plugin marketplace. Installers add it once, then install one or more plugins from it.

## Manifest

[`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) at the repo root declares the marketplace. The `plugins` array lists each installable plugin. Each entry names the plugin, describes it, points at the skill folders it bundles under `skills/`, and may list reviewer agent files under the top-level [`agents/`](../agents/) through an `agents` array.

## Plugins

| Plugin | Bundles |
| --- | --- |
| `wiki-page-author` | [Wiki Page Author](Wiki-Page-Author) skill and the [Wiki Page Reviewer](Wiki-Page-Reviewer) subagent. |
| `ticket-author` | [Ticket Author](Ticket-Author) and [Ticket Vet](Ticket-Vet) skills and the [Ticket Reviewer](Ticket-Reviewer) subagent. |

Each plugin is independently installable.

## Reviewer subagents

Each plugin ships a reviewer subagent, installed with the plugin and invoked by name. The skill's frontmatter references its reviewer by name, not by path.

The `ticket-author` plugin registers its reviewer as a plugin agent: the agent file lives at the top-level [`agents/`](../agents/) and is listed in the plugin's `agents` array in the manifest. The `wiki-page-author` plugin ships its reviewer inside [`skills/wiki-page-author/agents/`](../skills/wiki-page-author/agents/).

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
