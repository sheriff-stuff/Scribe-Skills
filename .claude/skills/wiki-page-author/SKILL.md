---
name: wiki-page-author
description: Write, update, or remove pages in the project wiki, or organise wiki content into folders. Handles the page body and inline open design decision (ODD) blocks, which have their own inverted rules. Use when the user asks to add to the wiki, update the wiki, document something, write a page about a subject, remove a page, or expresses uncertainty about something they want recorded ("I'm not sure", "we haven't decided") — those become inline `> [!ODD]` blocks.
---

# Wiki Page Author

This skill writes and updates pages in the project wiki. The wiki is a living spec — present tense, confirmed facts only. Pages tell a future agent or human what the application is, not how it got there or why.

The one place where uncertainty is allowed is inline `> [!ODD]` blocks placed next to the section they affect. The rules for ODD content are inverted from the body rules and are listed separately below.

## Body Rules

These apply everywhere on the page **except** inside `> [!ODD]` blocks.

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

4. **Never guess.** If something is unknown or undecided, ask the user. Confirmed answers go in the body; uncertainty goes in an inline `> [!ODD]` block placed next to the relevant section. Do not infer from related pages, related code, or what seems plausible.

   **Bad — invents a fact the user did not state:**

   > Sessions probably persist across browser restarts.

   **Good — captures the uncertainty inline; does not invent the answer:**

   > [!ODD] ODD-SESS-002 — Whether sessions persist across browser restarts.

   **Bad — softens the user's uncertainty into the body:**

   > Sessions likely persist across browser restarts.

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

8. **Body prose adjacent to an ODD block does not restate it.** The block carries the question, options, and any hedging. The body around it stays in confident present tense and does not duplicate the block's content.

   **Bad — folds the ODD content into the body:**

   > Forms render one question per page. Whether partial submissions are saved automatically or only on explicit "save draft" is still being decided.

   **Good — body states what is known; the block carries the open question:**

   > Forms render one question per page.
   >
   > [!ODD] ODD-FORM-004 — Are partial submissions saved automatically, or only on explicit "save draft"?

9. **Anything linkable is written as an inline link.** This covers files and folders inside the wiki, files and folders elsewhere in the repo, and external URLs. Bare paths and bare URLs are only used when the target genuinely cannot be linked.

   **Bad — bare in-repo path:**

   > New pages use the page template at `.claude/skills/wiki-page-author/assets/page-template.md`.

   **Good — inline link to the file:**

   > New pages use the [page template](../.claude/skills/wiki-page-author/assets/page-template.md).

## Open Design Decisions

ODDs are inline blocks placed next to the section they affect. Each has a stable ID of the form `ODD-<TOPIC>-<NNN>`, where the topic prefix matches the page or folder concept (e.g. `PERM`, `FORM`, `SESS`).

The page that owns the concept carries the full ODD — see the [ODD template](assets/odd-template.md) for the canonical shape and ID-assignment rules.

### Pointer blocks on affected pages

Other affected pages carry a one-line pointer next to the affected section. It points back to the owner, nothing more.

> [!ODD] ODD-PERM-003 (defined in [Permissions](../Permissions/Permissions)) — endpoint behavior depends on inheritance decision.

When a pointer is added to another page, the owner page's `Affects:` line is updated in the same operation to include that page.

### Rules inside `> [!ODD]` blocks

These apply only inside ODD blocks.

1. **Hedging is allowed.** "Probably", "leaning toward", "might", "should" are fine here.
2. **Rationale is allowed** when the user has provided it.
3. **Options without a chosen answer are allowed** — that is the point.
4. **Every block traces back to something the user said.** Do not invent uncertainty.
5. **The owner block lists all affected pages in its `Affects:` line.**

### Resolving an ODD

When an ODD is answered:

1. Rewrite the relevant body sections in the owner page and every affected page in confident present tense, incorporating the answer.
2. Remove the `> [!ODD]` block from the owner page.
3. Remove every pointer `> [!ODD]` block referencing that ID across the wiki.
4. The ID is retired and never reused.

## Standing Instructions

These apply throughout the work.

- **Use the [page template](assets/page-template.md) for new pages.**
- **Use the [ODD template](assets/odd-template.md) when adding an ODD.**
- **Keep [`home.md`](../../../wiki/home.md) in sync.** If a page is added or removed, update [`home.md`](../../../wiki/home.md) in the same operation.
- **Flag inconsistencies, do not fix them silently.** If a change makes another wiki page inconsistent, tell the user. Do not edit other pages unprompted.
- **Re-read before finishing.** Read the body back. Check that nothing in it is guessed, hedged, justified, or historical. Fix anything that is.

## Gotchas

- "I'm not sure" / "we haven't decided" / "still working out" is a signal to write an inline `> [!ODD]` block, not to guess and write a confident sentence.
- A request can legitimately touch only an ODD block and leave the body untouched. Do not invent body content to balance the change.
- A request to "add notes" or "document my thinking" is usually not a wiki request. Ask before writing.