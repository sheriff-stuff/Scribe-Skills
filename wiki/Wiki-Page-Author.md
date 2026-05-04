# Wiki Page Author

The wiki-page-author skill writes, updates, and removes pages in the project wiki, and organises wiki content into folders.

## Triggers

- The user asks to add to, update, or remove something from the wiki.
- The user asks to document a subject or write a page about something.
- The user expresses uncertainty about something they want recorded ("I'm not sure", "we haven't decided", "still working out") — those become entries in `## Open design decisions`.

## Scope

The skill handles two distinct regions of a page, each with its own rule set:

- The page **body** — everything except `## Open design decisions`.
- The `## Open design decisions` section — rules are inverted from the body.

## Body rules

These apply everywhere on a page except `## Open design decisions`:

- One subject per page. Content belonging to a different subject is suggested for the right page rather than added.
- Files and folders are named by subject, not by content type.
- Present tense, declarative — pages state what the application does, not what it doesn't.
- Confirmed answers go in the body; uncertainty goes in `## Open design decisions`. Facts are not inferred from related pages, related code, or what seems plausible.
- No rationale on the page. Justification lives in a design decision record, linked from the page.
- No revision history. Updates replace content.
- Internal links use no `.md` extension.
- Body prose may cross-reference `## Open design decisions` as a pointer only. The decision detail, options, and hedging stay in that section.

## Open design decisions rules

These apply only inside `## Open design decisions`:

- Hedging is allowed ("probably", "leaning toward", "might", "should").
- Rationale is allowed when the user has provided it.
- Options without a chosen answer are allowed.
- Each entry is a bullet stating the question, optionally with options and context.
- Every entry traces back to something the user said.

## Standing instructions

- New pages use the [page template](../.claude/skills/wiki-page-author/assets/page-template.md).
- [`home.md`](home) stays in sync — when a page is added or removed, [`home.md`](home) is updated in the same operation.
- Inconsistencies introduced by a change are flagged to the user. Other pages are not edited unprompted.
- The body is re-read before finishing, and anything guessed, hedged, justified, or historical is fixed.

## Resolving an open design decision

When an entry in `## Open design decisions` is answered:

1. The relevant body section is rewritten in confident present tense, incorporating the answer.
2. The bullet is removed from `## Open design decisions`.
3. If the section is empty, the heading is removed.

## Related

- [Home](home)
