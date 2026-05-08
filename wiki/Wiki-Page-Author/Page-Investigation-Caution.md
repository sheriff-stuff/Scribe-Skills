# Page Investigation Caution

A Page Investigation Caution marks a whole page as still under investigation and not ready for implementation. It is coarser than an [Open Design Decision](Open-Design-Decision): an ODD says the body is ground truth except for one named open point, while a caution says the body may still be wrong overall.

The [ticket-author](Ticket-Author) skill detects the caution and refuses to draw Scope, Implementation Approach, or Acceptance Criteria from a cautioned page without explicit user authorization.

## Where Page Investigation Cautions live

A caution lives at the top of the page it covers, immediately after the H1 description comment and before the first `##` heading. One caution per page maximum.

```markdown
# Sessions

<!-- How user sessions are created, persisted, and ended. -->

<a id="CAUTION-SESSIONS-storage-redesign-pending"></a>
> [!CAUTION] CAUTION-SESSIONS-storage-redesign-pending — Session storage is being redesigned; do not build from this page yet.
>
> **Context:** evaluating server-side store vs. signed-token approach; outcome will reshape Persistence and Termination sections.

## Creation

A session is created on successful login and tied to the user's account.
```

## ID format

`CAUTION-<AREA>-<slug>` — e.g., `CAUTION-SESSIONS-storage-redesign-pending`. Area is one uppercase word naming the page or folder concept the caution lives under, matching the convention used for ODDs. Slug is kebab-case and describes why the page is under investigation.

## Rules

These apply only inside `> [!CAUTION]` blocks:

- The reason sentence after the ID is required.
- `Context:` is optional. When present, it carries what's still being worked out — paragraphs, bullets, and other markdown allowed.
- A caution is page-level. Other pages do not carry pointer blocks back to it; there is no `Affects:` line.
- Every caution traces back to something the user said.

## Resolving a Page Investigation Caution

When the investigation concludes and the page is ready for implementation:

1. The body is rewritten in confident present tense per the [Body Rules](Body-Rules), incorporating whatever was decided.
2. The `> [!CAUTION]` block and its `<a id>` anchor are removed in the same operation.
