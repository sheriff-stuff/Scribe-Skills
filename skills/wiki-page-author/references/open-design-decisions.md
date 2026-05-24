# Open Design Decisions

Each Open Design Decision (ODD) has an ID of the form `ODD-<AREA>-<slug>`. See the [ODD template](../assets/odd-template) for the canonical shape. On the owner page the ID is plain text; on pointer blocks elsewhere the ID is rendered as a markdown link to the owner page (or the section heading the block sits under).

## Pointer blocks on affected pages

Other affected pages carry a one-line pointer next to the affected section. The ID is rendered as a markdown link to the owner page (or the section heading the owner ODD sits under).

> [!ODD] [ODD-PERMISSIONS-child-page-inheritance](../Permissions/Permissions#child-pages) — endpoint behaviour depends on the inheritance decision.

When a pointer is added to another page, the owner page's `Affects:` line is updated in the same operation to include that page.

## Rules inside `> [!ODD]` blocks

These apply only inside ODD blocks.

- **IDs follow `ODD-<AREA>-<slug>`.** Area is one uppercase word naming the page or folder concept the ODD lives under (`PERMISSIONS`, `FORMS`, `SESSIONS`). Slug is kebab-case, describes the open point, and is distinct — `child-page-inheritance` not `inheritance`.
- **`Ticket:` is required.** Use `*(placeholder)*` if no ticket has been created.
- **`Affects:`, when present, lists every page that carries a pointer block to this ODD.**
- **Rationale is allowed.**
- **Every block traces back to something the user said.** Do not invent uncertainty.
- **One decision per block.**

## Resolving an Open Design Decision

When an Open Design Decision is answered:

1. Rewrite the relevant body sections in the owner page and every affected page in confident present tense, incorporating the answer.
2. Remove the `> [!ODD]` block from the owner page.
3. Remove every pointer `> [!ODD]` block referencing that ID across the wiki.
