---
name: wiki-page-author
description: Write, update, fix, or remove pages in the project wiki, or organise wiki content into folders. Also creates, updates, and resolves inline open design decision (ODD) blocks and page-level investigation caution blocks. Use when the user asks to add to the wiki, update the wiki, document something, write a page about a subject, remove a page, expresses uncertainty about something they want recorded ("I'm not sure", "we haven't decided" — captured as ODD blocks), asks to add, update, or resolve an ODD directly, or asks to mark a page as under investigation, add a do-not-implement marker to a page, or lift the investigation marker once the page is ready.
---

# Wiki Page Author

This skill writes and updates pages in the project wiki. The wiki is the living design spec for the project being built — present tense, confirmed facts only. Pages tell a future agent or human what the project is, not how it got there or why. An agent reading it should be able to treat every page as ground truth. Development tickets are created from these pages.

Uncertainty is allowed in two places: inline `> [!ODD]` blocks placed next to the section they affect (a single open point on an otherwise ground-truth page), and a top-of-page `> [!CAUTION]` block (the whole page is under investigation and not ready to build from).

## Body Rules

These apply everywhere on the page **except** inside `> [!ODD]` and `> [!CAUTION]` blocks.

- **One subject per page.** If content belongs to a different subject, suggest the right page rather than adding it. The test is whether the content describes the `subject` of the page, or describes how another part of the application _uses_ the subject — the latter belongs on the consuming feature's page.

  **Bad — User Identity page drifts into how other features consume it:**

  > ## How restrictions use identity
  >
  > FGS reads the user's `clearance` and `region` attributes to filter visible records.
  >
  > ## How permissions use identity
  >
  > RBAC maps the user's `role` attribute to a permission set.

  **Good — User Identity page stays on its subject:**

  > Users are identified by their corporate directory entry. The following attributes are retrieved on sign-in: `clearance`, `region`, `role`, `email`.

- **Names — files, folders, and section headings — follow the subject, not the content type.**

  **Bad — describes how the content was produced:**

  > `docs/`, `notes/`, `analysis/`, `architecture/`, `## Notes`, `## Details`, `## Information`

  **Good — describes what the content is about:**

  > `Forms/`, `Users/`, `Migration/`, `## Validation rules`

- **Present tense, declarative — describes the application as if it already exists.** Even when the feature hasn't been built, write as if it has. No "we will", "we plan to", or "the idea is".

  **Bad — describes intent rather than state:**

  > We plan to render one question per page.

  **Bad — describes what the application doesn't do:**

  > The form does not render multiple questions on one page.

  **Good — describes the application as it is:**

  > The form renders one question per page.

- **Uncertainty lives only in `> [!ODD]` blocks, never in body prose.** Confirmed answers go in the body; block carries what's open next to the relevant section. A body sentence on the same topic as an adjacent ODD is fine when it states the current spec confidently — topical overlap is not a violation, hedging is. If something is unknown or undecided, ask the user; do not infer it from related pages, related code, or what seems plausible.

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

  **Good — body states current spec, ODD flags future change:**

  > User data is stored in a local MongoDB collection seeded with test fixtures.
  > [!ODD] ODD-DATA-external-api-migration — Migration to external API X is pending API readiness.

- **No rationale; link to a design decision record if justification is needed.** The page describes what the application is, not why. The why lives in design decision records. If a design choice needs justification, link to the DDR rather than writing the justification on the page. If a relevant DDR doesn't exist, suggest creating one rather than writing the rationale into the page.

  **Bad — explains why the choice was made:**

  > Forms render one question per page because users on mobile struggled with multi-question screens.

  **Good — states the fact:**

  > Forms render one question per page.

  **Good — states the fact and links the why:**

  > Forms render one question per page. See [DDR-0007 Form rendering](../Decisions/DDR-0007-Form-rendering).

- **No revision history.** Updates replace content; do not annotate what changed.

  **Bad:**

  > Sessions now persist across browser restarts (previously they expired on close).

  **Good:**

  > Sessions persist across browser restarts.

- **For external services and libraries, document the integration — not their API.** State which component, endpoint, or module is used and what it does in the application. Do not list its properties, attributes, slots, or parameters — those belong in the library's own documentation and drift when it changes. A statement about how a local structure relates to an external shape is allowed. Reproducing the shape itself is not.

  **Bad — mirrors the third-party API (drifts when they change it):**

  > `POST /v1/users` returns `{id, name, email, phone, address, created_at, updated_at, status, role}`.

  **Good — documents the contract:**

  > We call `POST /v1/users` with `{name, email}`. We read `id` and `email` from the response. On `429`, we retry with exponential backoff. See [the API docs](https://example.com/docs) for the full response shape.

  **Bad — lists component attributes (drifts when the library changes):**

  > Uses `ic-text-field` with `label`, `helper-text`, `placeholder`, `validation-status`.

  **Good — names the component and describes application behaviour:**

  > Single-line text input rendered with `ic-text-field`.

  **Good — points to the external source instead of describing the relationship:**

  > See [the API docs](https://example.com/docs) for an example of the user document shape.

  **Bad — reproduces the external shape under a "describing the local one" framing:**

  > The local user document has fields `id`, `name`, `email`, `phone`, `address`.

- **Document design facts, not code identifiers or structure.** Identifiers (file names, variable names, lookup keys) and structural conventions (naming patterns, directory layouts, class and method signatures) live in the code, not the wiki — documenting them creates a second source of truth that drifts. Technology choices and mechanisms (e.g. "loaded via Mongock changesets", "JSON fixtures", "stored in MongoDB") _are_ design facts and belong here. Domain model vocabulary — field names and attributes that define the application's data model (e.g. `createdBy`, `roles`, `clearances`) — are also design facts. The test: does the name appear in conversations about _what the application is_ (domain vocabulary, design facts), or only in conversations about _how the code is organised_ (file layout, helper classes, fixture names)? The first belongs in the wiki; the second doesn't.

  **Bad — documents a code identifier as if it were a design fact:**

  > The fixture file for the approver user is named `e2e-approver.json` and is loaded with `UserLookup.lookup("e2e-approver")`.

  **Bad — documents code structure that is self-evident from the directory:**

  > Each fixture file is named by `uid` (e.g., `adeveloper.json`) and lives in `src/test/fixtures/users/`.

  **Good — describes what exists without naming the identifier or structure:**

  > A fixture exists for a user with the Approver role only, used in Playwright e2e tests.

  **Good — names the technology choice (a design fact):**

  > Seed data is loaded via Mongock changesets that run on application startup.

- **Anything linkable is written as an inline link, and internal targets use no `.md` extension.** This covers files and folders inside the wiki, files and folders elsewhere in the repo, and external URLs. Bare paths and bare URLs are only used when the target genuinely cannot be linked.

  **Bad — bare in-repo path:**

  > New pages use the page template at `skills/wiki-page-author/assets/page-template.md`.

  **Good — inline link to the file:**

  > New pages use the [page template](../skills/wiki-page-author/assets/page-template).

- **No pleonasm.** State each fact without redundant qualifiers or filler.

  **Bad:**

  > Each form always renders exactly one single question per page.

  **Good:**

  > Forms render one question per page.

## Open Design Decisions

Every ODD traces back to something the user said — do not invent uncertainty.

When the user expresses uncertainty about something they want recorded ("I'm not sure", "we haven't decided", "still working out"), asks to add or update an ODD, or asks to resolve an ODD, read [`references/open-design-decisions`](references/open-design-decisions) before writing or modifying the block. That reference covers the `ODD-<AREA>-<slug>` ID format, owner pages vs pointer blocks, the `Affects:` line, the rules that apply inside `> [!ODD]` blocks, and the resolution flow.

## Page Investigation Cautions

A Page Investigation Caution marks a whole page as not ready for implementation — coarser than an ODD, which scopes uncertainty to one point and treats the rest of the body as ground truth. The [ticket-author](../ticket-author/SKILL) skill refuses to draw Scope, Implementation Approach, or Acceptance Criteria from a cautioned page without explicit user authorization.

Every caution traces back to something the user said — do not invent investigation cautions.

When the user says the page is "still being figured out", "don't build from this yet", or asks to mark a page as under investigation, add a do-not-implement marker, or lift the investigation marker once the page is ready, read [`references/page-investigation-caution`](references/page-investigation-caution) before writing or modifying the block. That reference covers the rules that apply inside `> [!CAUTION]` blocks.

## Standing Instructions

These apply throughout the work.

- **Use the [page template](assets/page-template) for new pages.**
- **Keep [`index.md`] or [`home.md`] in sync.** If a page is added or removed, update [`index.md`] or [`home.md`] in the same operation.
- **Flag inconsistencies, do not fix them silently.** If a change makes another wiki page inconsistent, tell the user. Do not edit other pages unprompted.

## Validation

Walk this checklist against every page you wrote or changed. If any item fails, fix it and re-run the checklist on the revised page. Repeat until every item passes. If a failure cannot be resolved without information only the user can provide (an undecided answer, an unresolvable concept), stop and ask the user — list every unresolved item in one message rather than asking piecemeal. Do not report the work as done until validation passes cleanly.

Body — walk the Body Rules section above and confirm each holds for every sentence on the page:

- [ ] One subject per page
- [ ] Names follow the subject
- [ ] Present tense, declarative
- [ ] No hedging in body prose
- [ ] No rationale in body
- [ ] No revision history
- [ ] External services and libraries documented as integrations
- [ ] Design facts only
- [ ] Anything linkable is an inline link
- [ ] No pleonasm

Open Design Decisions — applies inside every `> [!ODD]` block touched:

- [ ] ID follows `ODD-<AREA>-<slug>` — area is one uppercase word naming the owning page or folder concept; slug is kebab-case and distinct
- [ ] `Ticket:` is present (use `*(placeholder)*` if no ticket exists)
- [ ] On the owner page the ID is plain text; on pointer blocks it is a markdown link to the owner page or the owner section heading
- [ ] On the owner page, `Affects:` lists every page that carries a pointer block to this ODD
- [ ] Every pointer block elsewhere references an ODD that exists on its owner page
- [ ] One decision per block
- [ ] The block traces back to something the user said — uncertainty is not invented

Page Investigation Caution — applies when a `> [!CAUTION]` block was added, changed, or removed:

- [ ] At most one caution per page
- [ ] The reason sentence is present — no bare `> [!CAUTION]`
- [ ] No pointer blocks elsewhere reference the caution
- [ ] The caution traces back to something the user said

Cross-page and index:

- [ ] **Cross-page check.** From the page list in [`index.md`] or [`home.md`], identify pages topically related to the target — same domain area, shared concepts, or pages whose subject the target mentions. Read those pages in full. Then check the target for: (a) content already covered by a related page, where a link would suffice; (b) content that belongs on a different existing page rather than here. Flag both to the user.
- [ ] If a page was added or removed, [`index.md`] or [`home.md`] reflects it
- [ ] Inconsistencies introduced on other pages by this change have been flagged to the user — not silently fixed

Resolution and removal:

- [ ] When an ODD was resolved, the owner block and every pointer block referencing its ID are removed, and the affected body sections have been rewritten in confident present tense
- [ ] When a caution was lifted, the block is removed and the body has been rewritten as ground truth

## Gotchas

- "I'm not sure" / "we haven't decided" / "still working out" is a signal to write an inline `> [!ODD]` block, not to guess and write a confident sentence. Load [`references/open-design-decisions`](references/open-design-decisions) before writing the block.
- "this page is still being figured out" / "don't build from this yet" / "treat this as a draft / proposal" is a signal to add a top-of-page `> [!CAUTION]` block, not an ODD. ODD is section-scoped; caution is page-scoped. Load [`references/page-investigation-caution`](references/page-investigation-caution) before writing the block.
- A request to "add notes" or "document my thinking" is usually not a wiki request. Ask before writing.
