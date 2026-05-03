---
name: wiki-page-author
description: Write, update, or remove pages in the project wiki, or organise wiki content into folders. Handles the page body and the `## Open design decisions` section, which has its own inverted rules. Use when the user asks to add to the wiki, update the wiki, document something, write a page about a subject, remove a page, or expresses uncertainty about something they want recorded ("I'm not sure", "we haven't decided") — those become entries in the open design decisions section.
---

# Wiki Page Author

This skill writes and updates pages in the project wiki. The wiki is a living spec — present tense, confirmed facts only. Pages tell a future agent or human what the application is, not how it got there or why.

The one section of any page where uncertainty is allowed is `## Open design decisions`. The rules for that section are inverted from the body rules and are listed separately below.

## Body Rules

These apply everywhere on the page **except** `## Open design decisions`.

1. **One subject per page.** If content belongs to a different subject, suggest the right page rather than adding it.

2. **Files and folders are named by subject, not by content type.**

   **Bad — describes how the content was produced:**

   > `docs/`, `notes/`, `analysis/`, `architecture/`

   **Good — describes what the content is about:**

   > `Forms/`, `Users/`, `Migration/`

3. **Present tense, declarative.** State what the application does, not what it doesn't.

   **Bad:**

   > The form does not render multiple questions on one page.

   **Good:**

   > The form renders one question per page.

4. **Never guess.** If something is unknown or undecided, ask the user. Confirmed answers go in the body; uncertainty goes in `## Open design decisions`. Do not infer from related pages, related code, or what seems plausible.

   **Bad — invents a fact the user did not state:**

   > Sessions probably persist across browser restarts.

   **Good — captures the uncertainty, does not invent the answer:**

   > (in `## Open design decisions`) Whether sessions persist across browser restarts.

   **Bad — softens the user's uncertainty into the body:**

   > Sessions likely persist across browser restarts.

   **Good — routes the uncertainty to the decisions section:**

   > (in `## Open design decisions`) Whether sessions persist across browser restarts.

5. **No rationale; link to a design decision record if justification is needed.** The page describes what the application is, not why. The why lives in design decision records. If a design choice needs justification, link to the DDR rather than writing the justification on the page. If a relevant DDR doesn't exist, suggest creating one rather than writing the rationale into the page.

   **Bad — explains why the choice was made:**

   > Forms render one question per page because users on mobile struggled with multi-question screens.

   **Good — states the fact:**

   > Forms render one question per page.

   **Good — states the fact and links the why:**

   > Forms render one question per page. See [DDR-0007 Form rendering](../Decisions/DDR-0007-Form-rendering).

6. **No revision history.** Updates replace content; do not annotate what changed.

   **Bad:**

   > Sessions now persist across browser restarts (previously they expired on close).

   **Good:**

   > Sessions persist across browser restarts.

7. **Internal links use no `.md` extension.**

   **Bad:** `[text](../Forms/Validation.md)`

   **Good:** `[text](../Forms/Validation)`

8. **Body prose may cross-reference `## Open design decisions`, but only as a pointer.** A body sentence can note that a related question is unresolved by linking to the open decisions section. The body must not state the decision detail itself, list options, or hedge — that content lives only in `## Open design decisions`.

   **Bad — folds the decision detail into the body:**

   > Forms render one question per page. Whether partial submissions are saved automatically or only on an explicit "save draft" action is still being decided.

   **Good — points at the decisions section:**

   > Forms render one question per page. See `## Open design decisions` for how partial submissions are handled.

## Rules for `## Open design decisions`

These apply only inside that section.

1. **Hedging is allowed.** "Probably", "leaning toward", "might", "should" are fine here.
2. **Rationale is allowed** when the user has provided it.
3. **Options without a chosen answer are allowed** — that is the point of the section.
4. **Each entry is a bullet** stating the question, optionally with options and context.
5. **Do not invent uncertainty.** Every entry traces back to something the user said.

## Standing Instructions

These apply throughout the work.

- **Use the [page template](assets/page-template.md) for new pages.**
- **Keep `home.md` in sync.** If a page is added or removed, update `home.md` in the same operation.
- **Flag inconsistencies, do not fix them silently.** If a change makes another wiki page inconsistent, tell the user. Do not edit other pages unprompted.
- **Re-read before finishing.** Read the body back. Check that nothing in it is guessed, hedged, justified, or historical. Fix anything that is.

## Resolving an Open Design Decision

When an entry in `## Open design decisions` gets answered:

1. Rewrite the relevant body section in confident present tense, incorporating the answer.
2. Remove the bullet from `## Open design decisions`.
3. If the section is now empty, remove the heading too.

## Gotchas

- "I'm not sure" / "we haven't decided" / "still working out" is a signal to write to `## Open design decisions`, not to guess and write a confident sentence.
- A request can legitimately touch only `## Open design decisions` and leave the body untouched. Do not invent body content to balance the change.
- A request to "add notes" or "document my thinking" is usually not a wiki request. Ask before writing.
