---
name: ticket-author
description: Use when the user wants to create, edit, or break down tickets — including epics, features, spikes, bugs, chores, documentation, and ODDs (Open Design Decisions raised from the wiki).
---

# Ticket Author

This skill writes ticket proposal files to `proposed-tickets/`. Each file becomes a ticket (or epic) when the PR/MR is merged.

## Consumer

Each ticket is read by a human reviewer and executed by an LLM agent that has the wiki and the codebase in context.

## Ticket Anchoring

Every ticket is anchored in one of two places. The anchor names where the ticket's _why_ lives, which sets what the body has to carry — so identify it before writing.

Identify by an observable test: **does the ticket need motivational rationale — business case, user impact, domain or strategic justification — to make sense?**

- **Wiki-anchored** — yes, it needs a _why_. A wiki page holds that _why_ (and the full _what_); the ticket links to it and carries scope, anchors, and AC. Most feature work, ODDs, and anything tied to a domain concept is wiki-anchored. If no such page exists yet, suggest creating one via wiki.
- **Codebase-anchored** — no; the only justification it needs is causal-mechanical (sequencing, invariants, what depends on what). The ticket is its own source of truth and carries that mechanical detail. Most refactors, internal cleanups, dependency upgrades, and code-shape decisions are codebase-anchored.

The two are not mutually exclusive at the body level: a wiki-anchored ticket may still carry causal-mechanical detail when the executing agent needs it, with its _why_ on the wiki. What flips the anchor is the _why_ — a ticket that needs motivational rationale is wiki-anchored even when it also carries mechanical detail; a ticket whose only justification is mechanical is codebase-anchored. The check is correctness, not consistency: if a reader of a codebase-anchored ticket would need business case, user impact, or domain rationale to know why the work matters, the anchor was misidentified.

If unsure, ask the user. The split changes what counts as a valid ticket body — see [Body Rules](#body-rules).

## Workflow

1. **Understand the request.** Determine how many tickets are needed, then choose each ticket's type by taking the first rule that matches, top to bottom. Epic is handled when planning the breakdown in step 4.
   1. **User named a type** (feature, spike, bug, chore, documentation, ODD, epic) — use it.
   2. **ODD** — never inferred. An ODD ticket originates only from an explicit request to resolve a wiki ODD; absent that, it is not an ODD.
   3. **Documentation** — the work only adds or changes wiki or docs, with no code change — use Documentation.
   4. **Spike, Bug, or Chore** — the request reads as an investigation, a defect fix, or maintenance with no user-facing behaviour change — ask the user before choosing one of these.
   5. **Otherwise** — use Feature.

2. **Identify each ticket's anchor.** For each ticket, decide whether it is wiki-anchored or codebase-anchored (see [Ticket Anchoring](#ticket-anchoring)). If unsure, ask the user before drafting.

3. **Gather context from the project.** Before writing tickets, read what's already in the repo to understand the domain — wiki pages, existing code, documentation, whatever is there. Use the terminology that already exists (page names, class names, module names). Do not invent new terminology for concepts that already have a name.

4. **Plan the ticket set.** Decide the breakdown:
   - If the work has multiple child tickets that belong together, create an epic file plus individual ticket files with `epic: auto`.
   - If the tickets are unrelated or don't warrant an epic, create standalone ticket files.
   - Only one epic file per branch is allowed. The epic links its children through their `epic: auto`; an epic file never carries its own `epic:` field — an epic is not a child of another epic.
   - Each ticket should represent a discrete, independently deliverable piece of work.

5. **Write all ticket files.** Batch-write every `.md` file to `proposed-tickets/`. For each ticket, read the appropriate template from `assets/` and use it as the structural basis:
   - [Epic template](assets/epic-template.md)
   - [Feature template](assets/feature-template.md)
   - [Spike template](assets/spike-template.md)
   - [Bug template](assets/bug-template.md)
   - [Chore template](assets/chore-template.md)
   - [Documentation template](assets/documentation-template.md)
   - [ODD template](assets/odd-template.md)

6. **Review and fix.** Delegate to the `ticket-reviewer` subagent to review every file in `proposed-tickets/`. Drive the loop off the per-file `VERDICT:` lines, not the summary count.
   - For every file with `VERDICT: NEEDS WORK`, either apply each listed violation, or decline the finding — but decline only when you can cite the wiki, existing code, or the ticket template against it. Record the citation in your reply to the user; never silently ignore a finding.
   - After fixes, delegate to `ticket-reviewer` again. Stop as soon as every file reports `VERDICT: READY`.
   - Cap the loop at three reviews. If files still report `NEEDS WORK` after the third — or author and reviewer are deadlocked on a finding neither will move on — stop and surface the outstanding violations to the user with your reasoning, rather than re-reviewing indefinitely.
   - If the reviewer returns `No tickets to review.`, surface that to the user and stop — do not loop.
   - If a `NOTES:` line names URLs missing from `.claude/url-resolution.md`, list them to the user once at the end; don't try to resolve them.

7. **Report.** Report the ticket set as ready once every file reports `VERDICT: READY`. If the loop hit the cap with violations outstanding, report those and your reasoning instead — do not present the set as ready.

## Frontmatter Schema

| Field    | Required | Type                | Notes                                                                                                                                           |
| -------- | -------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`  | **Yes**  | string              | Non-empty                                                                                                                                       |
| `type`   | No       | string              | Only accepted value is `epic`                                                                                                                   |
| `labels` | No       | list                |                                                                                                                                                 |
| `weight` | No       | integer             | Bare (unquoted) integer ≥ 0. Quoted digits (`"5"`) and floats (`3.0`) are rejected. Omit to leave unweighted; `0` means weight zero, not unset. |
| `epic`   | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same branch                                                             |

List fields (`labels`) accept YAML inline `[a, b]` or block format.

## File Naming

Lowercase kebab-case named by subject.

**Bad:** `ticket-1.md`, `feature.md`, `epic.md`

**Good:** `add-user-search-endpoint.md`, `spike-notification-strategy.md`, `dashboard-migration-epic.md`

## Body Rules

- **Write actionable descriptions.** A reader recovers the concrete problem and the done-state from the ticket's Scope and Acceptance Criteria alone, without opening the linked spec. This is a self-sufficiency floor, not a licence to duplicate: the linked doc still owns the field tables, rationale, and full spec (see **Don't duplicate spec detail from the source doc** and **What the ticket carries depends on its anchor**), but a thin pointer like "X is wrong, see the wiki" fails the test — it names neither the problem nor what done looks like. Scope says what changes; AC says how a reviewer confirms it changed.

  **Bad — thin pointer; the problem and done-state live only in the spec:**

  > Campaign expiry is wrong. See [Campaign Lifecycle](https://example.com/wiki/Campaign-Lifecycle).

  **Good — problem and done-state recoverable from the ticket; the spec carries the detail:**

  > Campaigns stay active past their end date because expiry is evaluated only on write. Scope: evaluate expiry at read time so a campaign past its end date reports inactive. Field semantics and edge cases: [Campaign Lifecycle](https://example.com/wiki/Campaign-Lifecycle).

- **Do not infer technical decisions.** Do not prescribe specific class names, design patterns, library choices, file paths, or route paths unless they come from the wiki or existing code, or the user asks for them. An identifier carried by an anchor (a linked wiki page, a referenced code file) or named in the user's request is not inferred — stating it is required, not a violation. What this rule forbids is a prescribed name or path with no anchor and no user request behind it.
- **Use full URLs when referencing pages, code, or other projects.** Use absolute URLs, not relative paths. **Exception:** when referencing a ticket proposed in the same branch, use the ticket title as plain text — no URL exists yet.
- **Use the language of existing documentation.** When a concept already has a name in the wiki or existing code, use that name. Do not introduce new terminology for the same thing.
- **Reference files, not line numbers.** No `#L104`, no `#L3-6` — line anchors rot when files change. Identify the location by content (symbol name, string, or section heading); link to the file, not a line range.

  **Bad:**

  > Update discount calculation logic ([`PricingService#L47-89`](https://example.com/services/pricing/PricingService)).

  **Good:**

  > Update discount calculation logic in [`PricingService.applyDiscount`](https://example.com/services/pricing/PricingService).

- **Implementation Approach orients, not prescribes.** Reference patterns and existing implementations by concrete anchors (files, classes, wiki pages) — not step-by-step imperatives, numbered or bulleted. Bullets are fine for structural facts about layout or shape. Every Scope item must be reachable from the Approach.

  **Bad — enumerates as numbered imperative steps:**

  > 1.  Add `email` field to [`User`](https://example.com/domain/User)
  > 2.  Add `phone` field to [`User`](https://example.com/domain/User)
  > 3.  Add format validation for email and phone
  > 4.  Update [`UserController.createUser`](https://example.com/controllers/UserController) to accept the new fields
  > 5.  Update [`UserRepository`](https://example.com/repositories/UserRepository) findBy methods
  > 6.  Add migration script for existing users

  **Bad — same imperatives with bullets instead of numbers:**

  > - Add `email` and `phone` fields to [`User`](https://example.com/domain/User)
  > - Add format validation
  > - Update [`UserController.createUser`](https://example.com/controllers/UserController) and [`UserRepository`](https://example.com/repositories/UserRepository)
  > - Add a migration script

  **Good — prose orientation with anchors:**

  > Add `email` and `phone` fields to [`User`](https://example.com/domain/User) with format validation. Extend [`UserController.createUser`](https://example.com/controllers/UserController) and [`UserRepository`](https://example.com/repositories/UserRepository) to handle the new fields. A new migration script populates `email` and `phone` for existing users.

  **Good — bullets carrying structural facts, not steps:**

  > Project resources follow a one-thing-per-file convention:
  >
  > - one file per user under `src/main/resources/users/`, named `<username>.yml`
  > - one config per environment under `src/main/resources/env/`
  > - one migration per release under `src/main/resources/db/migrations/`

- **Describe relationships in parts, not single verbs.** When pointing at an existing implementation, name what to take from it and what to change. Single verbs (mirror, match, follow, reference) leave the executing agent guessing where on the spectrum to land. Class names follow the class's role: infrastructure names (base classes, configs, converters) come with the borrowed structure; domain names (entities, repositories, services) are part of _what to change_.

  **Bad — gestures at the relationship with a single verb:**

  > Mirror inventory-service's store setup, adapting packages.

  **Good — names what to take and what to change:**

  > Take the class structure and converter logic from inventory-service's [`BaseRecord`](https://example.com/inventory/BaseRecord), [`StoreConfig`](https://example.com/inventory/StoreConfig), [`TimestampReadConverter`](https://example.com/inventory/TimestampReadConverter), [`TimestampWriteConverter`](https://example.com/inventory/TimestampWriteConverter). Change package names from `com.example.inventory` to `com.example.orders`. Bring along anything these classes reference.

  **Bad — no distinction between infrastructure and domain classes:**

  > Take the entity and repository structure from `Analyst`, `AnalystRepository`, `BaseEntity`.

  **Good — infrastructure name stays; domain classes are renamed:**

  > Take the entity and repository shape from [`Analyst`](https://example.com/analyst/Analyst), [`AnalystRepository`](https://example.com/analyst/AnalystRepository), and [`BaseEntity`](https://example.com/shared/BaseEntity): a MongoDB-mapped entity extending `BaseEntity`, paired with a Spring Data `MongoRepository`. Change `Analyst`/`AnalystRepository` to `Project`/`ProjectRepository`, `Team`/`TeamRepository`, `Silo`/`SiloRepository`. `BaseEntity` keeps its name.

- **What the ticket carries depends on its anchor.**
  - **Wiki-anchored tickets** link to the wiki page that holds the _what_ and _why_. The ticket body carries scope, anchors, and AC — plus any causal-mechanical detail (sequencing, invariants) the executing agent needs. What stays off the ticket is motivational rationale (business case, user impact, strategic priority) and domain background; those belong on the wiki page. If justification feels necessary in the ticket, the wiki page is the place for it; if no such page exists, suggest creating one via wiki.

  - **Codebase-anchored tickets** are the source of truth for themselves. The ticket body carries the mechanical detail the executing agent needs — sequencing constraints, invariants, what depends on what for the mechanism to work. This is causal-mechanical detail, not motivational rationale. If the ticket needs business case or user impact to make sense, the anchor was misidentified — go back to [step 2](#workflow).

  **Bad — wiki-anchored ticket carrying motivational why:**

  > We need `email` and `phone` on `User` because the support team has been asking for a way to contact users outside the app, and customer success has flagged this as a top-three churn driver this quarter.

  **Good — wiki-anchored ticket links the wiki:**

  > Rationale and field semantics: [Contact Channels for Users](https://example.com/wiki/Contact-Channels-for-Users).

  **Good — codebase-anchored ticket carrying mechanical detail:**

  > The Mongock migration must run before [`UserRepository`](https://example.com/repositories/UserRepository) is wired into the application context, because the unique index on `username` is enforced at write time and the repository's startup health check performs a write.

- **Don't duplicate spec detail from the source doc.** If a referenced doc (wiki page for wiki-anchored tickets, another ticket or a code file for codebase-anchored ones) owns the full spec, list scope only (names, structural decisions, enum/constant values) and link it as source of truth. This holds inside Acceptance Criteria too — an AC resolves spec-owned values through the authoritative link, not by reproducing the field or validation matrix inline (see **Acceptance Criteria assert outcomes, not restatement**).

  **Bad: duplicates the schema doc:**

  > Fields: `username` (String), `email` (String), `firstName` (String)...

  **Good: scope only, defer to source:**

  > Fields per [`User-Storage.md`](https://example.com/wiki/User-Storage).

- **Acceptance Criteria assert outcomes, not restatement.** Each criterion is a falsifiable check a reviewer would perform — not an imperative, not a project-wide baseline (build/lint/test belong in the project's `CLAUDE.md`), not subjective. State assertions that correspond to a scope goal are fine if falsifiable. A reviewer must be able to tell pass from fail without guessing. Resolve spec-owned values through the authoritative link, not by reproducing the field or validation matrix inline; quote inline only a constant the check's pass/fail genuinely turns on (see **Don't duplicate spec detail from the source doc**).

  **Bad — restates the task, baselines, and subjective judgements:**

  > - Create the User entity
  > - Code compiles without errors
  > - Classes follow Spring Data MongoDB conventions
  > - `PermissionLevel` contains `NONE, READ, WRITE, ADMIN`
  > - Code is idiomatic

  **Good — each line is a check a reviewer can run:**

  > - A `User` with populated `authorities` round-trips through Mongo with all fields preserved
  > - `ZonedDateTime` fields survive a round-trip with timezone intact
  > - Mongock migration creates a unique index on `username` and non-unique indexes on `authorities` and `organisation`
  > - `BaseEntity` and `MongoConfig` contain the same fields and methods as the other-app implementations
  > - Collections are accessible from a running application instance
  > - No classes exist outside the File Structure diagram

  **Bad — unresolved reference:**

  > - Mongock migration creates the required indexes

  **Good — names the constants the check turns on, defers the rest:**

  > - Mongock migration creates indexes on `state`, `_class`, `createdAt`, and `createdBy`
  > - Seed documents contain fields matching the [Project Schema](https://example.com/wiki/Project-Schema)

  **Bad — reproduces the schema's field/validation matrix inline:**

  > - `User` persists `username` (String, unique, non-null), `email` (String, nullable), `firstName` (String), `lastName` (String), `authorities` (List<String>), `organisation` (String)

  **Good — asserts the outcome, defers the matrix to its owner:**

  > - A `User` round-trips through Mongo with every field from [`User-Storage.md`](https://example.com/wiki/User-Storage) preserved

- **Testing names behaviours, not cases.** Feature and bug tickets require automated tests. Name the behaviours that must have coverage; the implementing agent derives cases and edges from the code change, wiki, and codebase already in context. A behaviour is a rule the system honours ("a campaign past its end date reports inactive"); a case is one input that exercises it ("a campaign one day past its end date"). Name the behaviour, not the case. Do not enumerate cases, edges, frameworks, or file paths. For bugs, a regression test covering the reproduction is mandatory — name the broken behaviour the reproduction exercises; this is the one entry that pins a specific scenario, and it still names no framework or file path.
- **Risks name concrete exposure.** When a ticket includes a Risks section, each entry names a specific exposure outside the ticket's control — an external dependency, a data-migration hazard, a contract another system relies on — not a generic caveat or a restatement of the work's difficulty.
- **ODD tickets request resolution of an existing wiki ODD.** The ticket closes when the wiki ODD is resolved. ODD tickets are always wiki-anchored.
