# Open Design Decision

An Open Design Decision (ODD) is a question about a document's design that hasn't been answered yet.

## Where Open Design Decisions live

Open Design Decisions are inline in the document that owns the concept, placed next to the section they affect, marked with a callout block. The ID lives on the first line of the callout, followed by an em-dash and the one-sentence open point.

```markdown
> [!ODD] ODD-PERMISSIONS-child-page-inheritance — Should child pages inherit parent permissions by default?
>
> **Affects:** [API endpoints](../API/Endpoints), [Sharing links](../Sharing/Links)
> **Context:** inherit + override vs. explicit per page vs. read-only inherit; interaction with sharing links; behavior on parent deletion
```

When a decision affects documents in other folders, the owning doc carries the full definition. Affected docs reference it with a pointer block placed next to the section it affects:

```markdown
> [!ODD] [ODD-PERMISSIONS-child-page-inheritance](../Permissions/Permissions#permissions) — endpoint behavior depends on the inheritance decision.
```

The ID is rendered as a markdown link to the owner page (or the section heading the owner ODD sits under). The pointer block does not restate the question, options, or context.

## ID format

`ODD-<AREA>-<slug>` — e.g., `ODD-PERMISSIONS-child-page-inheritance`. Area is one uppercase word naming the page or folder concept the ODD lives under. Slug is kebab-case, describes the open point, and is distinct (`child-page-inheritance`, not `inheritance`).

## Rules

These apply only inside `> [!ODD]` blocks:

- The ID and the one-sentence open point are on the same line as `> [!ODD]`, separated by an em-dash.
- Hedging is allowed ("probably", "leaning toward", "might", "should").
- Rationale is allowed when the user has provided it.
- Options without a chosen answer are allowed.
- Every ODD traces back to something the user said.
- `Ticket:` is optional. The line is omitted when no tracker ticket exists.
- `Affects:` on the owner block lists every page that carries a pointer block to this ODD. The owner page is not listed. The line is omitted if no other pages are affected.
- `Context:` carries related considerations, candidate options, and edge cases. Paragraphs, bullets, and other markdown are allowed.

## Example page

A page with an ODD inline next to the section it affects:

```markdown
# Sessions

How user sessions are created, persisted, and ended.

## Creation

A session is created on successful login and tied to the user's account.

## Persistence

Sessions are stored server-side, keyed by an opaque token in an `HttpOnly` cookie.

> [!ODD] ODD-SESSIONS-browser-restart-persistence — Do sessions persist across browser restarts?
>
> **Ticket:** [PROJ-1421](https://your-tracker/PROJ-1421)
> **Context:** cookie expires on browser close vs. 30-day TTL vs. configurable per user

## Termination

A session ends on explicit logout or after 30 minutes of inactivity.
```

## Resolving an Open Design Decision

When an Open Design Decision is answered:

1. The relevant body sections in the owner doc and all affected docs are rewritten in confident present tense, incorporating the answer.
2. The `> [!ODD]` block is removed from the owner doc.
3. Pointer `> [!ODD]` blocks referencing that ID in all affected docs are removed.
