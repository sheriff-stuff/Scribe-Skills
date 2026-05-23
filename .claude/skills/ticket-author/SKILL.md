---
name: ticket-author
description: Use when the user wants to create, edit, or break down GitLab tickets — including epics, features, spikes, bugs, chores, documentation, and ODDs (Open Design Decisions raised from the wiki).
---

# Ticket Author

This skill writes ticket proposal files to `proposed-tickets/`. Each file becomes a ticket (or epic) when the PR/MR merges to main.

## Consumer

Each ticket is read by a human reviewer and executed by an LLM agent that has the wiki and the codebase in context.

## Workflow

1. **Understand the request.** Determine how many tickets are needed, then choose each ticket type using this decision table. Epic is decided in step 3.

   | User named type? | Type is ODD? | Type is Spike/Bug/Chore? | Action                                            |
   | ---------------- | ------------ | ------------------------ | ------------------------------------------------- |
   | Yes              | —            | —                        | Use the named type                                |
   | No               | Yes          | —                        | Ask the user (ODD must be explicit)               |
   | No               | No           | Yes                      | Ask the user before choosing Spike, Bug, or Chore |
   | No               | No           | No                       | Use Feature                                       |

2. **Gather context from the project.** Before writing tickets, read what's already in the repo to understand the domain wiki pages, existing code, documentation, whatever is there. Use the terminology that already exists (page names, class names, module names). Do not invent new terminology for concepts that already have a name.

   **If a wiki page informing the ticket carries a top-of-page `> [!CAUTION]` block** ([page investigation caution](../wiki-page-author/SKILL#page-investigation-cautions)): notify the user, quote the caution's reason, and wait for instruction before proceeding. The Body Rule on material from a cautioned wiki page governs how to handle it. Spike and Bug tickets are exempt — a Spike's purpose is to investigate unresolved design, and a Bug targets existing behaviour rather than committing to the cautioned design.

3. **Plan the ticket set.** Decide the breakdown:
   - If the work has multiple child tickets that belong together, create an epic file plus individual ticket files with `epic: auto`.
   - If the tickets are unrelated or don't warrant an epic, create standalone ticket files.
   - Only one epic file per branch is allowed.
   - Each ticket should represent a discrete, independently deliverable piece of work.

4. **Write all ticket files.** Batch-write every `.md` file to `proposed-tickets/`. For each ticket, read the appropriate template from `assets/` and use it as the structural basis:
   - [Epic template](assets/epic-template.md)
   - [Feature template](assets/feature-template.md)
   - [Spike template](assets/spike-template.md)
   - [Bug template](assets/bug-template.md)
   - [Chore template](assets/chore-template.md)
   - [Documentation template](assets/documentation-template.md)
   - [ODD template](assets/odd-template.md)

5. **Validate your own work.** For each ticket, walk the [Validation](#validation) checklist. If any item fails, fix it and re-run the checklist on the revised ticket. Repeat until every item passes. If a failure cannot be resolved without information only the user can provide (e.g. an unknown URL, an unresolvable domain term), stop and ask the user — list every unresolved item in one message rather than asking piecemeal. Do not report the tickets as ready until validation passes cleanly.

## Frontmatter Schema

| Field    | Required | Type                | Notes                                                                               |
| -------- | -------- | ------------------- | ----------------------------------------------------------------------------------- |
| `title`  | **Yes**  | string              | Non-empty                                                                           |
| `type`   | No       | string              | Only accepted value is `epic`                                                       |
| `labels` | No       | list                |                                                                                     |
| `weight` | No       | integer             | Non-negative                                                                        |
| `epic`   | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same branch |

List fields (`labels`) accept YAML inline `[a, b]` or block format.

## File Naming

Lowercase kebab-case named by subject.

**Bad:** `ticket-1.md`, `feature.md`, `epic.md`

**Good:** `add-user-search-endpoint.md`, `spike-notification-strategy.md`, `dashboard-migration-epic.md`

## Body Rules

- **Write actionable descriptions.** Acceptance criteria, context, and scope — as you would a real issue.
- **Do not infer technical decisions.** Do not prescribe specific class names, design patterns, library choices, file paths, or route paths unless they come from the wiki or existing code or the user asks you to.
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

- **Do not write justification or rationale into ticket bodies.** Tickets answer _what_ is being done and _how it'll be verified_. The _why_ lives in the wiki. If justification feels necessary, link to the wiki page that holds it; if no such page exists, suggest creating one via wiki.
- **Don't duplicate spec detail from the source doc.** If a referenced doc owns the full spec, list scope only (names, structural decisions, enum/constant values) and link it as source of truth.

  **Bad: duplicates the schema doc:**

  > Fields: `username` (String), `email` (String), `firstName` (String)...

  **Good: scope only, defer to source:**

  > Fields per [`User-Storage.md`](https://example.com/wiki/User-Storage).

- **Material from a cautioned wiki page does not belong in Scope, Implementation Approach, or Acceptance Criteria.** A wiki page carrying a top-of-page `> [!CAUTION]` block is under investigation and not ready for implementation. Those two sections are acceptable destinations because neither commits the implementation to the cautioned design: `Out of Scope` excludes it explicitly, `Risks` flags it as exposure. Route material to `Out of Scope` if the ticket has no dependency on it, or to `Risks` if the ticket still has exposure to the cautioned design (e.g. an entity created now will need fields added once the design is confirmed).
- **Acceptance Criteria assert outcomes, not restatement.** Each criterion is a falsifiable check a reviewer would perform — not an imperative, not a project-wide baseline (build/lint/test belong in the project's `CLAUDE.md`), not subjective. State assertions that correspond to a scope goal are fine if falsifiable.

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
  > - `BaseEntity` and `MongoConfig` contain the same fields and methods as the bookings-app implementations
  > - Collections are accessible from a running application instance
  > - No classes exist outside the File Structure diagram

  **Bad — unresolved reference:**

  > - Mongock migration creates the required indexes

  **Good — values resolvable from the AC text (inline or via authoritative link):**

  > - Mongock migration creates indexes on `state`, `_class`, `createdAt`, and `createdBy`
  > - Seed documents contain fields matching the [Project ORIN Schema](https://example.com/wiki/Project-ORIN-Schema)

- **Risks entries require concrete exposure.** Only add an item to Risks when something outside the ticket's control creates a concrete risk to the work — e.g. a dependency on an unconfirmed design, an upstream migration with no fixed date, or a cautioned wiki page whose outcome could change the ticket's scope. Material that is fully excluded via Out of Scope poses no risk and should not appear in Risks.
- **Testing names behaviours, not cases.** Feature and bug tickets require automated tests. For bugs, a regression test covering the reproduction case is mandatory. Name the behaviours that must have coverage; the implementing agent derives cases and edges from the code change, wiki, and codebase already in context. Do not enumerate cases, edges, frameworks, or file paths.
- **ODD tickets request resolution of an existing wiki ODD.** The ticket closes when the wiki ODD is resolved.

## Validation

- [ ] Description is actionable — acceptance criteria, context, and scope
- [ ] No inferred technical decisions — no prescribed class names, design patterns, library choices, file paths, or route paths without a wiki/code anchor or user request
- [ ] Full URLs for pages, code, and other projects; in-branch ticket references use the plain-text title
- [ ] Existing documentation's language used; no new terminology for concepts already named
- [ ] File references identify content (symbol, string, section heading), not line numbers
- [ ] Implementation Approach orients, not prescribes — prose, no numbered or bulleted imperative steps; every Scope item reachable from it
- [ ] Relationships described in parts — what to take and what to change; no bare single verbs (mirror, match, follow, reference)
- [ ] No justification or rationale in ticket bodies
- [ ] No duplicated spec detail from a source-of-truth doc
- [ ] Cautioned wiki material appears only in Out of Scope or Risks
- [ ] Acceptance Criteria assert outcomes — each is a falsifiable check, not a restatement of Scope, a project baseline, or a subjective judgement
- [ ] Risks entries point to concrete exposure outside the ticket's control
- [ ] Testing names behaviours, not cases — no enumerated cases, edges, frameworks, or file paths
- [ ] ODD tickets link the wiki ODD page; AC is its resolution
