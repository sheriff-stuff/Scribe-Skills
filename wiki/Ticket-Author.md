# Ticket Author

The ticket-author skill writes ticket proposal files to [`proposed-tickets/`](../proposed-tickets/). Each file becomes a GitLab issue (or epic) when the MR merges to main. The skill does not create branches, commits, or MRs.

Each ticket is a prompt for Claude Code: combined with the wiki and the codebase, it drives an LLM agent to produce code and a PR.

## Sections

- [Triggers](Ticket-Author/Triggers)
- [Ticket Types](Ticket-Author/Ticket-Types)
- [Workflow](Ticket-Author/Workflow)
- [Frontmatter Schema](Ticket-Author/Frontmatter-Schema)
- [Labels](Ticket-Author/Labels)
- [File Naming](Ticket-Author/File-Naming)
- [Body Rules](Ticket-Author/Body-Rules)
