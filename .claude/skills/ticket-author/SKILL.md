---
name: ticket-author
description: Use when the user wants to create, edit, or break down GitLab tickets — including epics, features, spikes, bugs, chores, documentation, and ODDs (Open Design Decisions raised from the wiki).
---

# Ticket Author

This skill writes ticket proposal files to `proposed-tickets/`. Each file becomes a GitLab issue (or epic) when the MR merges to main. This skill does **not** create branches, commits, or MRs.

## Consumer

Each ticket is a prompt for Claude Code. Combined with the wiki and the codebase, it drives an LLM agent to produce code and a PR. The rules below flow from that — write for an LLM that has the wiki in context, navigates by named anchors (files, classes, wiki pages), and uses Acceptance Criteria as its stop condition.

## Workflow

1. **Understand the request.** Determine how many tickets are needed. For each ticket's type (Feature, Spike, Bug, Chore, Documentation, ODD): if the request names it, use it; otherwise, ask before picking Spike, Bug, or Chore over Feature. ODD requires explicit naming. Epic is decided in step 3.

2. **Gather context from the project.** Before writing tickets, read what's already in the repo to understand the domain wiki pages, existing code, documentation, whatever is there. Use the terminology that already exists (page names, class names, module names). Do not invent new terminology for concepts that already have a name.

   **If a wiki page informing the ticket carries a top-of-page `> [!CAUTION]` block** ([page investigation caution](../wiki-page-author/SKILL#page-investigation-cautions)): notify the user, quote the caution's reason, and wait for instruction before proceeding. The Body Rule on material from a cautioned wiki page governs how to handle it. Spike and Bug tickets are exempt.

3. **Plan the ticket set.** Decide the breakdown:
   - If the work has multiple child tickets that belong together, create an epic file plus individual ticket files with `epic: auto`.
   - If the tickets are unrelated or don't warrant an epic, create standalone ticket files.
   - Only one epic file per branch is allowed.
   - Each ticket should represent a discrete, independently deliverable piece of work.

4. **Write all ticket files.** Batch-write every `.md` file to `proposed-tickets/`. For each ticket, read the appropriate template from `assets/` and use it as the structural basis:
   - [Epic template](assets/epic-template)
   - [Feature template](assets/feature-template)
   - [Spike template](assets/spike-template)
   - [Bug template](assets/bug-template)
   - [Chore template](assets/chore-template)
   - [Documentation template](assets/documentation-template)
   - [ODD template](assets/odd-template)

## Frontmatter Schema

| Field       | Required | Type                | Notes                                                                               |
| ----------- | -------- | ------------------- | ----------------------------------------------------------------------------------- |
| `title`     | **Yes**  | string              | Non-empty                                                                           |
| `type`      | No       | string              | Only accepted value is `epic`                                                       |
| `labels`    | No       | list                | Each label must already exist in the project                                        |
| `assignees` | No       | list                | GitLab usernames                                                                    |
| `milestone` | No       | string              | Milestone title or ID                                                               |
| `weight`    | No       | integer             | Non-negative                                                                        |
| `due_date`  | No       | string              | `YYYY-MM-DD`                                                                        |
| `epic`      | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same branch |

List fields (`labels`, `assignees`) accept YAML inline `[a, b]` or block format.

## File Naming

Lowercase kebab-case named by subject.

**Bad:** `ticket-1.md`, `feature.md`, `epic.md`

**Good:** `add-user-search-endpoint.md`, `spike-notification-strategy.md`, `dashboard-migration-epic.md`

## Body Rules

1. **Write actionable descriptions.** Acceptance criteria, context, and scope — as you would a real issue.
2. **Do not infer technical decisions.** Do not prescribe specific class names, design patterns, library choices, file paths, or route paths unless they come from the wiki or existing code or the user asks you to.
3. **Use full URLs when referencing pages, code, or other projects.** Use absolute URLs, not relative paths. **Exception:** when referencing a ticket proposed in the same branch, use the ticket title as plain text — no URL exists yet.
4. **Use the language of existing documentation.** When a concept already has a name in the wiki or existing code, use that name. Do not introduce new terminology for the same thing.
5. **Reference files, not line numbers.** No `#L104`, no `#L3-6` — line anchors rot when files change. Identify the location by content (symbol name, string, or section heading); link to the file, not a line range.

   **Bad:**

   > Update discount calculation logic ([`PricingService#L47-89`](url)).

   **Good:**

   > Update discount calculation logic in [`PricingService.applyDiscount`](url).

6. **Implementation Approach orients, not prescribes.** Reference patterns and existing implementations by concrete anchors (files, classes, wiki pages) — not numbered steps. Every Scope item must be reachable from the Approach.

   **Bad — enumerates as a step-by-step list:**

   > 1. Add `email` field to [`User`](url)
   > 2. Add `phone` field to [`User`](url)
   > 3. Add format validation for email and phone
   > 4. Update [`UserController.createUser`](url) to accept the new fields
   > 5. Update [`UserRepository`](url) findBy methods
   > 6. Add migration script for existing users

   **Good — prose orientation with anchors:**

   > Add `email` and `phone` fields to [`User`](url) with format validation. Extend [`UserController.createUser`](url) and [`UserRepository`](url) to handle the new fields. A new migration script populates `email` and `phone` for existing users.

7. **Describe relationships in parts, not single verbs.** When pointing at an existing implementation, name what to take from it and what to change. Single verbs (mirror, match, follow, reference) leave the executing agent guessing where on the spectrum to land. Class names follow the class's role: infrastructure names (base classes, configs, converters) come with the borrowed structure; domain names (entities, repositories, services) are part of _what to change_.

   **Bad — gestures at the relationship with a single verb:**

   > Mirror inventory-service's store setup, adapting packages.

   **Good — names what to take and what to change:**

   > Take the class structure and converter logic from inventory-service's [`BaseRecord`](url), [`StoreConfig`](url), [`TimestampReadConverter`](url), [`TimestampWriteConverter`](url). Change package names from `com.example.inventory` to `com.example.orders`. Bring along anything these classes reference.

   **Bad — no distinction between infrastructure and domain classes:**

   > Take the entity and repository structure from `Analyst`, `AnalystRepository`, `BaseEntity`.

   **Good — infrastructure name stays; domain classes are renamed:**

   > Take the entity and repository shape from [`Analyst`](url), [`AnalystRepository`](url), and [`BaseEntity`](url): a MongoDB-mapped entity extending `BaseEntity`, paired with a Spring Data `MongoRepository`. Change `Analyst`/`AnalystRepository` to `Project`/`ProjectRepository`, `Team`/`TeamRepository`, `Silo`/`SiloRepository`. `BaseEntity` keeps its name.

8. **Do not write justification or rationale into ticket bodies.** Tickets answer _what_ is being done and _how it'll be verified_. The _why_ lives in the wiki. If justification feels necessary, link to the wiki page that holds it; if no such page exists, suggest creating one via wiki.
9. **Don't duplicate spec detail from the source doc.** If a referenced doc owns the full spec, list scope only (names, structural decisions, enum/constant values, non-obvious gotchas) and link it as source of truth.

   **Bad: duplicates the schema doc:**

   > Fields: `username` (String), `email` (String), `firstName` (String)...

   **Good: scope only, defer to source:**

   > Fields per `User-Storage.md`.

10. **Material from a cautioned wiki page does not belong in Scope, Implementation Approach, or Acceptance Criteria.** A wiki page carrying a top-of-page `> [!CAUTION]` block is under investigation and not ready for implementation. Route its material to `Out of Scope` if the ticket has no dependency on it, or to `Risks` if the ticket still has exposure to the cautioned design (e.g. an entity created now will need fields added once the design is confirmed).
11. **Acceptance Criteria assert outcomes, not restatement.** Each criterion is a falsifiable check a reviewer would perform — not an imperative, not a project-wide baseline (build/lint/test belong in the project's `CLAUDE.md`), not subjective. State assertions that correspond to a scope goal are fine if falsifiable.

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
    > - Seed documents contain fields matching the [Project ORIN Schema](url)

12. **Risks entries require concrete exposure.** Only add an item to Risks when something outside the ticket's control creates a concrete risk to the work — e.g. a dependency on an unconfirmed design, an upstream migration with no fixed date, or a cautioned wiki page whose outcome could change the ticket's scope. Material that is fully excluded via Out of Scope poses no risk and should not appear in Risks.
13. **Testing names behaviours, not cases.** Feature and bug tickets require automated tests. For bugs, a regression test covering the reproduction case is mandatory. Name the behaviours that must have coverage; the implementing agent derives cases and edges from the code change, wiki, and codebase already in context. Do not enumerate cases, edges, frameworks, or file paths.
14. **ODD tickets request resolution of an existing wiki ODD.** The ticket closes when the wiki ODD is [resolved](../wiki-page-author/SKILL#resolving-an-open-design-decision).
