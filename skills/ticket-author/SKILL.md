---
name: ticket-author
description: Use when the user wants to create, edit, fix, or break down tickets — including epics, features, spikes, bugs, chores, documentation, and ODDs (Open Design Decisions raised from the wiki).
---

# Ticket Author

This skill writes ticket proposal files to `proposed-tickets/`. Each file becomes a ticket (or epic) when the PR/MR is merged.

## Consumer

Each ticket is read by a human reviewer and executed by an LLM agent that has the wiki and the codebase in context.

## Ticket Anchoring

Every ticket is anchored where its _why_ lives. Identify the anchor before writing — it decides what the body carries (see [Body Rules](#body-rules)).

The test: **does the ticket need motivational rationale — business case, user impact, domain or strategic justification — to make sense?**

- **Wiki-anchored** — yes. A wiki page holds the _why_ and the _what_; the ticket links to it. Most feature work, ODDs, and anything tied to a domain concept. If no such page exists yet, suggest creating one via wiki.
- **Codebase-anchored** — no; its only justification is causal-mechanical (sequencing, invariants, what depends on what), and the ticket is its own source of truth. Most refactors, internal cleanups, and dependency upgrades.

Mechanical detail doesn't flip the anchor: a wiki-anchored ticket may carry it too, with the _why_ still on the wiki. The _why_ is what classifies — if a reader would need business case, user impact, or domain rationale to know why the work matters, it is wiki-anchored.

If unsure, ask the user.

## Workflow

1. **Understand the request.** Determine how many tickets are needed, then choose each ticket's type by taking the first rule that matches, top to bottom. Epic is handled when planning the breakdown in step 4.
   1. **User named a type** (feature, spike, bug, chore, documentation, ODD, epic) — use it.
   2. **ODD** — never inferred. An ODD ticket originates only from an explicit request to resolve a wiki ODD.
   3. **Documentation** — the work only adds or changes wiki or docs, with no code change — use Documentation.
   4. **Spike, Bug, or Chore** — the request reads as an investigation, a defect fix, or maintenance with no user-facing behaviour change — ask the user before choosing one of these.
   5. **Otherwise** — use Feature.

2. **Identify each ticket's anchor.** For each ticket, decide whether it is wiki-anchored or codebase-anchored (see [Ticket Anchoring](#ticket-anchoring)). If unsure, ask the user before drafting.

3. **Gather context from the project.** Before writing tickets, read what's already in the repo to understand the domain — wiki pages, existing code, documentation, whatever is there. Use the terminology that already exists (page names, class names, module names). Do not invent new terminology for concepts that already have a name. When a wiki page informing a ticket carries a top-of-page `> [!CAUTION]` block, warn the user that the page is under investigation.

4. **Plan the ticket set.** Decide the breakdown:
   - If the work has multiple child tickets that belong together, create an epic file plus individual ticket files with `epic: auto`.
   - If the tickets are unrelated or don't warrant an epic, create standalone ticket files.
   - Only one epic file per branch is allowed. The epic links its children through their `epic: auto`; an epic file never carries its own `epic:` field — an epic is not a child of another epic.
   - Each ticket should represent an independently deliverable piece of work.

5. **Write all ticket files.** Batch-write every `.md` file to `proposed-tickets/`. For each ticket, read the appropriate template from `assets/` and use it as the structural basis:
   - [Epic template](assets/epic-template.md)
   - [Feature template](assets/feature-template.md)
   - [Spike template](assets/spike-template.md)
   - [Bug template](assets/bug-template.md)
   - [Chore template](assets/chore-template.md)
   - [Documentation template](assets/documentation-template.md)
   - [ODD template](assets/odd-template.md)

6. **Review and fix.** Whether the reviewer runs depends on the request from [step 1](#workflow):
   - **New tickets** — review. Delegate to the `ticket-reviewer` subagent to review every file in `proposed-tickets/`.
   - **Edits to existing tickets** — ask the user whether to run `ticket-reviewer`. If they decline, stop here.
   - **ODD tickets** — out of scope. Exclude any file whose `labels:` include `type::ODD` from what the reviewer is given.

   Fix what the reviewer reports, then re-review — up to three times. If files still report `NEEDS WORK` after the third, surface those to the user instead of looping further.

## Frontmatter Schema

| Field    | Required | Type                | Notes                                                                               |
| -------- | -------- | ------------------- | ----------------------------------------------------------------------------------- |
| `title`  | **Yes**  | string              | Non-empty                                                                           |
| `type`   | No       | string              | Only accepted value is `epic`                                                       |
| `labels` | No       | list                |                                                                                     |
| `weight` | No       | integer             |                                                                                     |
| `epic`   | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same branch |

## File Naming

Lowercase kebab-case named by the ticket's title.

## Body Rules

- **Write actionable descriptions.** A reader recovers the concrete problem and the done-state from the ticket's Scope and Acceptance Criteria alone, without opening the linked spec. This is a self-sufficiency floor, not a licence to duplicate: the linked doc still owns the field tables, rationale, and full spec (see **Don't duplicate spec detail from the source doc** and **What the ticket carries depends on its anchor**).

  **Bad — thin pointer; the problem and done-state live only in the spec:**

  > Campaign expiry is wrong. See [Campaign Lifecycle](https://example.com/wiki/Campaign-Lifecycle).

  **Good — problem and done-state recoverable from the ticket; the spec carries the detail:**

  > Campaigns stay active past their end date because expiry is evaluated only on write. Scope: evaluate expiry at read time so a campaign past its end date reports inactive. Field semantics and edge cases: [Campaign Lifecycle](https://example.com/wiki/Campaign-Lifecycle).

- **Do not infer technical decisions.** Do not prescribe specific class names, design patterns, library choices, file paths, or route paths unless they come from the wiki or existing code, or the user asks for them. An identifier carried by an anchor (a linked wiki page, a referenced code file) or named in the user's request is not inferred — stating it is required, not a violation. What this rule forbids is a prescribed name or path with no anchor and no user request behind it.

- **Use the language of existing documentation.** When a concept already has a name in the wiki or existing code, use that name. Do not introduce new terminology for the same thing.

- **Reference files, not line numbers.** No `#L104`, no `#L3-6` — line anchors rot when files change. Identify the location by content (symbol name, string, or section heading); link to the file, not a line range.

- **Implementation Approach orients, not prescribes.** Reference patterns and existing implementations by concrete anchors (files, classes, wiki pages) — not step-by-step imperatives, numbered or bulleted. Bullets are fine for structural facts about layout or shape. Every Scope item must be reachable from the Approach.

  **Bad — enumerates as numbered imperative steps:**

  > 1.  Add `email` field to [`User`](https://example.com/domain/User)
  > 2.  Add `phone` field to [`User`](https://example.com/domain/User)
  > 3.  Update [`UserController.createUser`](https://example.com/controllers/UserController) to accept the new fields
  > 4.  Add migration script for existing users

  **Good — prose orientation with anchors:**

  > Add `email` and `phone` fields to [`User`](https://example.com/domain/User). Extend [`UserController.createUser`](https://example.com/controllers/UserController) to handle the new fields. A new migration script populates `email` and `phone` for existing users.

  **Good — bullets carrying structural facts, not steps:**

  > Project resources follow a one-thing-per-file convention:
  >
  > - one file per user under `src/main/resources/users/`, named `<username>.yml`
  > - one config per environment under `src/main/resources/env/`
  > - one migration per release under `src/main/resources/db/migrations/`

- **Name what to take and what to change, not a single verb.** When a ticket instructs the agent to reproduce structure from a referenced class, file, or module, single verbs (mirror, match, follow, reference) leave the executing agent guessing where on the spectrum to land. Spell out the structure being borrowed and the parts being changed. Class names follow the class's role: infrastructure names (base classes, configs, converters) come with the borrowed structure; domain names (entities, repositories, services) are part of _what to change_.

  **Bad — gestures at the relationship with a single verb:**

  > Mirror inventory-service's store setup, adapting packages.

  **Good — names what to take and what to change:**

  > Take the class structure and converter logic from inventory-service's [`BaseRecord`](https://example.com/inventory/BaseRecord) and [`StoreConfig`](https://example.com/inventory/StoreConfig). Change package names from `com.example.inventory` to `com.example.orders`. Bring along anything these classes reference.

  **Bad — no distinction between infrastructure and domain classes:**

  > Take the entity and repository structure from `Analyst`, `AnalystRepository`, `BaseEntity`.

  **Good — infrastructure name stays; domain classes are renamed:**

  > Take the entity and repository shape from [`Analyst`](https://example.com/analyst/Analyst), [`AnalystRepository`](https://example.com/analyst/AnalystRepository), and [`BaseEntity`](https://example.com/shared/BaseEntity): a MongoDB-mapped entity extending `BaseEntity`, paired with a Spring Data `MongoRepository`. Change `Analyst`/`AnalystRepository` to `Project`/`ProjectRepository`. `BaseEntity` keeps its name.

- **What the ticket carries depends on its anchor.**
  - **Wiki-anchored tickets** link to the wiki page that holds the _what_ and _why_. The ticket body carries scope, anchors, and AC — plus any causal-mechanical detail (sequencing, invariants) the executing agent needs. What stays off the ticket is motivational rationale (business case, user impact, strategic priority) and domain background; those belong on the wiki page. If justification feels necessary in the ticket, the wiki page is the place for it.

  - **Codebase-anchored tickets** are the source of truth for themselves. The ticket body carries the mechanical detail the executing agent needs — sequencing constraints, invariants, what depends on what for the mechanism to work. This is causal-mechanical detail, not motivational rationale. If the ticket needs motivational rationale to make sense, the anchor was misidentified — go back to [step 2](#workflow).

  **Bad — wiki-anchored ticket carrying motivational why:**

  > We need `email` and `phone` on `User` because the support team has been asking for a way to contact users outside the app, and customer success has flagged this as a top-three churn driver this quarter.

  **Good — wiki-anchored ticket links the wiki:**

  > Rationale and field semantics: [Contact Channels for Users](https://example.com/wiki/Contact-Channels-for-Users).

- **Don't duplicate spec detail from the source doc.** If a referenced doc (wiki page for wiki-anchored tickets, another ticket or a code file for codebase-anchored ones) owns the full spec, list scope only (names, structural decisions, enum/constant values) and link it as source of truth. This holds inside Acceptance Criteria too — an AC resolves spec-owned values through the authoritative link, not by reproducing the field or validation matrix inline (see **Acceptance Criteria assert outcomes, not restatement**).

  **Bad: duplicates the schema doc:**

  > Fields: `username` (String), `email` (String), `firstName` (String)...

  **Good: scope only, defer to source:**

  > Fields per [`User-Storage.md`](https://example.com/wiki/User-Storage).

- **Acceptance Criteria assert outcomes, not restatement.** Each criterion is a falsifiable check a reviewer would perform — not an imperative, not a project-wide baseline (build/lint/test belong in the project's `CLAUDE.md`), not subjective. State assertions that correspond to a scope goal are fine if falsifiable. A reviewer must be able to tell pass from fail without guessing. Defer spec-owned values to their authoritative link (see **Don't duplicate spec detail from the source doc**); quote inline only a constant the check's pass/fail genuinely turns on.

  **Bad — restates the task, baselines, and subjective judgements:**

  > - Create the User entity
  > - Code compiles without errors
  > - Code is idiomatic

  **Good — each line is a check a reviewer can run:**

  > - A `User` with populated `authorities` round-trips through Mongo with all fields preserved
  > - `ZonedDateTime` fields survive a round-trip with timezone intact
  > - Mongock migration creates a unique index on `username` and non-unique indexes on `authorities` and `organisation`
  > - No classes exist outside the File Structure diagram

  **Bad — unresolved reference:**

  > - Mongock migration creates the required indexes

  **Good — names the constants the check turns on, defers the rest:**

  > - Mongock migration creates indexes on `state`, `_class`, `createdAt`, and `createdBy`
  > - Seed documents contain fields matching the [Project Schema](https://example.com/wiki/Project-Schema)

- **Testing names behaviours, not cases.** Feature and bug tickets require automated tests. Name the behaviours that must have coverage; the implementing agent derives cases and edges from the code change, wiki, and codebase already in context. A behaviour is a rule the system honours ("a campaign past its end date reports inactive"); a case is one input that exercises it ("a campaign one day past its end date"). Name the behaviour, not the case. Do not enumerate cases, edges, frameworks, or file paths. For bugs, a regression test covering the reproduction is mandatory — name the broken behaviour the reproduction exercises; this is the one entry that pins a specific scenario, and it still names no framework or file path.
