# Page Investigation Caution

A Page Investigation Caution marks a whole page as still under investigation and not ready for implementation. It is coarser than an [Open Design Decision](Open-Design-Decision): an ODD says the body is ground truth except for one named open point, while a caution says the body may still be wrong overall.

The [ticket-author](Ticket-Author) skill warns the user when a cautioned page informs a ticket.

## Where Page Investigation Cautions live

A caution lives at the top of the page it covers, immediately after the H1 description paragraph and before the first `##` heading. One caution per page maximum. Tickets that act on the caution link to the page itself.

```markdown
# Sessions

How user sessions are created, persisted, and ended.

> [!CAUTION]
> Session storage is being redesigned; do not build from this page yet.
>
> **Context:** evaluating server-side store vs. signed-token approach; outcome will reshape Persistence and Termination sections.

## Creation

A session is created on successful login and tied to the user's account.
```

## Rules

These apply only inside `> [!CAUTION]` blocks:

- The one-sentence reason is required.
- `Context:` is optional. When present, it carries what's still being worked out — paragraphs, bullets, and other markdown allowed.
- A caution is page-level. Other pages do not carry pointer blocks back to it.
- Every caution traces back to something the user said.

## Resolving a Page Investigation Caution

When the investigation concludes and the page is ready for implementation:

1. The body is rewritten in confident present tense per the [Body Rules](Body-Rules), incorporating whatever was decided.
2. The `> [!CAUTION]` block is removed in the same operation.
