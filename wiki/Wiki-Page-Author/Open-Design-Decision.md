# Open Design Decisions

An Open Design Decision (ODD) is a question about a document's design that hasn't been answered yet.

## Where Open Design Decisions live

Open Design Decisions are inline in the document that owns the concept, placed next to the section they affect, marked with a callout block:

> [!ODD] ODD-PERM-003 — Should child pages inherit parent permissions by default?
>
> **Ticket:**
> **Affects:** this page, [API endpoints](../API/Endpoints), [Sharing links](../Sharing/Links)
> **Options:** A) inherit + override, B) explicit per page, C) read-only inherit
> **Open questions:** interaction with sharing links; behavior on parent deletion

When a decision affects documents in other folders, the owning doc carries the full definition. Affected docs reference it with a pointer block:

> [!ODD] ODD-PERM-003 (defined in [Permissions](../Permissions/Permissions)) — endpoint behavior depends on inheritance decision.

The pointer block does not restate options or context.

## ID format

`ODD-<TOPIC>-<NNN>` — e.g., `ODD-PERM-003`. The topic prefix matches the folder or concept the decision belongs to. The number is sequential within that topic. IDs are stable and never reused, even after resolution.

## Rules

These apply only inside `> [!ODD]` blocks:

- Hedging is allowed ("probably", "leaning toward", "might", "should").
- Rationale is allowed when the user has provided it.
- Options without a chosen answer are allowed.
- Every ODD traces back to something the user said.
- The owner doc lists all affected docs in the `Affects:` line.

## Example page

A page with an ODD inline next to the section it affects:

```markdown
# Sessions

How user sessions are created, persisted, and ended.

## Creation

A session is created on successful login and tied to the user's account.

## Persistence

Sessions are stored server-side, keyed by an opaque token in an `HttpOnly` cookie.

> [!ODD] ODD-SESS-002 — Do sessions persist across browser restarts?
>
> **Ticket:** [PROJ-1421](https://your-tracker/PROJ-1421)
> **Affects:** this page
> **Options:** A) cookie expires on browser close, B) cookie has a 30-day TTL, C) configurable per user

## Termination

A session ends on explicit logout or after 30 minutes of inactivity.
```

## Resolving an Open Design Decision

When an Open Design Decision is answered:

1. The relevant body sections in the owner doc and all affected docs are rewritten in confident present tense, incorporating the answer.
2. The `> [!ODD]` block in the owner doc is removed.
3. Pointer `> [!ODD]` blocks in all affected docs are removed.
4. The ID is retired and never reused.
