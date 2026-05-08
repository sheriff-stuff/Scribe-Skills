---
name: wiki-page-author
description: Write, update, or remove pages in the project wiki, or organise wiki content into folders. Also creates, updates, and resolves inline open design decision (ODD) blocks and page-level investigation caution blocks. Use when the user asks to add to the wiki, update the wiki, document something, write a page about a subject, remove a page, expresses uncertainty about something they want recorded ("I'm not sure", "we haven't decided" — captured as ODD blocks), asks to add, update, or resolve an ODD directly, or asks to mark a page as under investigation, add a do-not-implement marker to a page, or lift the investigation marker once the page is ready.
---

# Wiki Page Author

This skill writes and updates pages in the project wiki. The wiki is the living design spec for the project being built — present tense, confirmed facts only. Pages tell a future agent or human what the project is, not how it got there or why. An agent reading it should be able to treat every page as ground truth. Development tickets are created from these pages.

Uncertainty is allowed in two places: inline `> [!ODD]` blocks placed next to the section they affect (a single open point on an otherwise ground-truth page), and a top-of-page `> [!CAUTION]` block (the whole page is under investigation and not ready to build from).

## Body Rules

These apply everywhere on the page **except** inside `> [!ODD]` and `> [!CAUTION]` blocks.

1. **One subject per page.** If content belongs to a different subject, suggest the right page rather than adding it.

2. **Names — files, folders, and section headings — follow the subject, not the content type.**

   **Bad — describes how the content was produced:**

   > `docs/`, `notes/`, `analysis/`, `architecture/`, `## Notes`, `## Details`, `## Information`

   **Good — describes what the content is about:**

   > `Forms/`, `Users/`, `Migration/`, `## Validation rules`

3. **Present tense, declarative — describes the application as if it already exists.** Even when the feature hasn't been built, write as if it has. No "we will", "we plan to", or "the idea is".

   **Bad — describes intent rather than state:**

   > We plan to render one question per page.

   **Bad — describes what the application doesn't do:**

   > The form does not render multiple questions on one page.

   **Good — describes the application as it is:**

   > The form renders one question per page.

4. **Uncertainty lives only in `> [!ODD]` blocks, never in body prose.** Confirmed answers go in the body; block carries what's open next to the relevant section, stated as the open point itself. If something is unknown or undecided, ask the user; do not infer from related pages, related code, or what seems plausible.

   **Bad — hedge in the body:**

   > Sessions probably persist across browser restarts.

   **Good — block names the open point directly:**

   > [!ODD] ODD-SESSIONS-browser-restart-persistence — Session persistence across browser restarts is undecided.

   **Bad — body restates the adjacent ODD:**

   > Forms render one question per page. Whether partial submissions are saved automatically or only on explicit "save draft" is still being decided.

   **Good — body confident, block carries the open point:**

   > Forms render one question per page.
   >
   > [!ODD] ODD-FORMS-partial-submission-save — Partial submission save trigger is undecided — automatic, or only on explicit "save draft".

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

7. **For external services, document your integration — not their API.** Capture which endpoints you call, what you send, which response fields you depend on, and how you handle errors. Link to the third party's docs for everything else; do not mirror their spec.

   **Bad — mirrors the third-party API (drifts when they change it):**

   > `POST /v1/users` returns `{id, name, email, phone, address, created_at, updated_at, status, role}`.

   **Good — documents the contract:**

   > We call `POST /v1/users` with `{name, email}`. We read `id` and `email` from the response. On `429`, we retry with exponential backoff. See [the API docs](https://example.com/docs) for the full response shape.

8. **Anything linkable is written as an inline link, and internal targets use no `.md` extension.** This covers files and folders inside the wiki, files and folders elsewhere in the repo, and external URLs. Bare paths and bare URLs are only used when the target genuinely cannot be linked.

   **Bad — bare in-repo path:**

   > New pages use the page template at `.claude/skills/wiki-page-author/assets/page-template.md`.

   **Good — inline link to the file:**

   > New pages use the [page template](../.claude/skills/wiki-page-author/assets/page-template).

9. **No pleonasm.** State each fact without redundant qualifiers or filler.

   **Bad:**

   > Each form always renders exactly one single question per page.

   **Good:**

   > Forms render one question per page.

## Open Design Decisions

Each Open Design Decision (ODD) has an ID of the form `ODD-<AREA>-<slug>`. The page that owns the concept carries the full ODD, prefixed by an HTML anchor (`<a id="ODD-<AREA>-<slug>"></a>`) so pointer blocks on other pages can deep-link to it — see the [ODD template](assets/odd-template) for the canonical shape.

### Pointer blocks on affected pages

Other affected pages carry a one-line pointer next to the affected section. The ID is a markdown link to the owner ODD's anchor on the owner page.

> [!ODD] [ODD-PERMISSIONS-child-page-inheritance](../Permissions/Permissions#ODD-PERMISSIONS-child-page-inheritance) — endpoint behavior depends on inheritance decision.

When a pointer is added to another page, the owner page's `Affects:` line is updated in the same operation to include that page.

### Rules inside `> [!ODD]` blocks

These apply only inside ODD blocks.

1. **IDs follow `ODD-<AREA>-<slug>`.** Area is one uppercase word naming the page or folder concept the ODD lives under (`PERMISSIONS`, `FORMS`, `SESSIONS`). Slug is kebab-case, describes the open point, and is distinct — `child-page-inheritance` not `inheritance`.
2. **`Ticket:` is optional.** Include the line only when a tracker ticket exists.
3. **`Affects:` is optional.** lists every page that carries a pointer block to this ODD.
4. **Rationale is allowed**
5. **Every block traces back to something the user said.** Do not invent uncertainty.
6. **One decision per block.**

### Resolving an Open Design Decision

When an Open Design Decision is answered:

1. Rewrite the relevant body sections in the owner page and every affected page in confident present tense, incorporating the answer.
2. Remove the `> [!ODD]` block and its `<a id>` anchor from the owner page.
3. Remove every pointer `> [!ODD]` block referencing that ID across the wiki.

## Page Investigation Cautions

A Page Investigation Caution marks a whole page as not ready for implementation — coarser than an ODD, which scopes uncertainty to one point and treats the rest of the body as ground truth. The [ticket-author](../ticket-author/SKILL) skill refuses to draw Scope, Implementation Approach, or Acceptance Criteria from a cautioned page without explicit user authorization.

Each caution has an ID of the form `CAUTION-<AREA>-<slug>`. The block sits at the top of the page, prefixed by an HTML anchor (`<a id="CAUTION-<AREA>-<slug>"></a>`) — see the [page investigation caution template](assets/caution-template) for the canonical shape.

### Rules inside `> [!CAUTION]` blocks

These apply only inside caution blocks.

1. **IDs follow `CAUTION-<AREA>-<slug>`.** Area is one uppercase word naming the page or folder concept the caution lives under (`PERMISSIONS`, `FORMS`, `SESSIONS`) — Slug is kebab-case and describes why the page is under investigation (`awaiting-product-review`, `flow-redesign-pending`).
2. **Placement is fixed.** The block lives at the top of the page, immediately after the H1 description comment
3. **The reason sentence is required.** A bare `> [!CAUTION]` with no reason is not allowed.
4. **`Context:` is optional.** When present, it carries what's still being worked out — paragraphs, bullets, and other markdown allowed.

## Standing Instructions

These apply throughout the work.

- **Use the [page template](assets/page-template) for new pages.**
- **Use the [Open Design Decision template](assets/odd-template) when adding an Open Design Decision.**
- **Use the [page investigation caution template](assets/caution-template) when marking a page as under investigation.**
- **Keep [`index.md`] or [`home.md`] in sync.** If a page is added or removed, update [`index.md`] or [`home.md`] in the same operation.
- **Flag inconsistencies, do not fix them silently.** If a change makes another wiki page inconsistent, tell the user. Do not edit other pages unprompted.
- **Re-read before finishing.** Read the body back. Check that nothing in it is guessed, hedged, justified, or historical. Fix anything that is.

## Gotchas

- "I'm not sure" / "we haven't decided" / "still working out" is a signal to write an inline `> [!ODD]` block, not to guess and write a confident sentence.
- "this page is still being figured out" / "don't build from this yet" / "treat this as a draft / proposal" is a signal to add a top-of-page `> [!CAUTION]` block, not an ODD. ODD is section-scoped; caution is page-scoped.
- A request to "add notes" or "document my thinking" is usually not a wiki request. Ask before writing.
