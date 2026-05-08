---
name: ticket-author
description: Create GitLab ticket proposals as markdown files in proposed-tickets/. Produces one .md file per issue (and optionally one epic) with YAML frontmatter and a structured body. Handles five ticket types: Epic, Feature, Spike, Bug, and Chore. Files are validated and processed by CI on merge to main. Use when the user asks to create, draft, or write tickets; break work into tickets; create issues; write an epic; propose or scope work items; create a spike, bug, or chore ticket; breakdown an epic; or plan work as GitLab issues.
---

# Ticket Author

This skill writes ticket proposal files to `proposed-tickets/`. Each file becomes a GitLab issue (or epic) when the MR merges to main. This skill does **not** create branches, commits, or MRs.

## Consumer

Each ticket is a prompt for Claude Code. Combined with the wiki and the codebase, it drives an LLM agent to produce code and a PR. The rules below flow from that — write for an LLM that has the wiki in context, navigates by named anchors (files, classes, wiki pages), and uses Acceptance Criteria as its stop condition.

## Workflow

1. **Understand the request.** Clarify what the user wants to accomplish. Determine how many tickets are needed, whether an epic is appropriate, and what type each ticket is (Epic, Feature, Spike, Bug, Chore).

2. **Gather context from the project.** Before writing tickets, read what's already in the repo to understand the domain wiki pages, existing code, documentation, whatever is there. Use the terminology that already exists (page names, class names, module names). Do not invent new terminology for concepts that already have a name.

   **If a wiki page informing the ticket carries a top-of-page `> [!CAUTION]` block** ([page investigation caution](../wiki-page-author/SKILL#page-investigation-cautions)): notify the user, quote the caution's reason, route the page's material to `Risks` with a link back, and wait for instruction before using it in Scope, Implementation Approach, or Acceptance Criteria. Spike and Bug tickets are exempt. 

3. **Plan the ticket set.** Decide the breakdown:
   - If the work has multiple child tickets that belong together, create an epic file plus individual ticket files with `epic: auto`.
   - If the tickets are unrelated or don't warrant an epic, create standalone ticket files.
   - Only one epic file per MR is allowed.
   - Each ticket should represent a discrete, independently deliverable piece of work.

4. **Write all ticket files.** Batch-write every `.md` file to `proposed-tickets/`. For each ticket, read the appropriate template from `assets/` and use it as the structural basis:
   - [Epic template](assets/epic-template.md)
   - [Feature template](assets/feature-template.md)
   - [Spike template](assets/spike-template.md)
   - [Bug template](assets/bug-template.md)
   - [Chore template](assets/chore-template.md)

## Frontmatter Schema

| Field       | Required | Type                | Notes                                                                           |
| ----------- | -------- | ------------------- | ------------------------------------------------------------------------------- |
| `title`     | **Yes**  | string              | Non-empty                                                                       |
| `type`      | No       | string              | Only accepted value is `epic`                                                   |
| `labels`    | No       | list                | Each label must already exist in the project                                    |
| `assignees` | No       | list                | GitLab usernames                                                                |
| `milestone` | No       | string              | Milestone title or ID                                                           |
| `weight`    | No       | integer             | Non-negative                                                                    |
| `due_date`  | No       | string              | `YYYY-MM-DD`                                                                    |
| `epic`      | No       | integer or `"auto"` | IID of an existing epic, or `"auto"` to link to the epic created in the same MR |

List fields (`labels`, `assignees`) accept YAML inline `[a, b]` or block format.

## File Naming

Lowercase kebab-case named by subject.

**Bad:** `ticket-1.md`, `feature.md`, `epic.md`

**Good:** `add-user-search-endpoint.md`, `spike-notification-strategy.md`, `dashboard-migration-epic.md`

## Body Rules

1. **Write actionable descriptions.** Acceptance criteria, context, and scope — as you would a real issue.
2. **Do not infer technical decisions.** Do not prescribe specific class names, design patterns, library choices, file paths, or route paths unless they come from the wiki or existing code or the user asks you to.
3. **Use full URLs when referencing pages, code, or other projects.** Use absolute URLs, not relative paths.
4. **Use the language of existing documentation.** When a concept already has a name in the wiki or existing code, use that name. Do not introduce new terminology for the same thing.
5. **Reference files, not line numbers.** No `#L104`, no `#L3-6` — line anchors rot when files change. Identify the location by content (symbol name, string, or section heading); link to the file, not a line range.
   **Bad:**

   > Update discount calculation logic ([`PricingService#L47-89`](url)).

   **Good:**

   > Update discount calculation logic in [`PricingService.applyDiscount`](url).

6. **Implementation Approach orients, not prescribes.** Reference patterns and existing implementations by concrete anchors (files, classes, wiki pages) — not numbered steps. Use _mirror_, not _copy_. Every Scope item must be reachable from the Approach.

   **Bad:**

   > - Copy `BaseRecord`, `StoreConfig`, `TimestampReadConverter`, `TimestampWriteConverter` from inventory-service, adapting packages.
   > - In [`config.yml`](url), change `inventory.store.migrations` to `orders.store.migrations`.
   > - Remove store autoconfigure exclusions from [`config.yml`](url).

   **Good:**

   > Mirror inventory-service's store setup, adapting `com.example.inventory` packages to `com.example.orders`. Anchor classes: [`BaseRecord`](url), [`StoreConfig`](url), [`TimestampReadConverter`](url), [`TimestampWriteConverter`](url). Bring along anything they reference.
   >
   > In `config.yml`: update migration scan package `inventory.store.migrations` → `orders.store.migrations`; remove store autoconfigure exclusions.

7. **Do not write justification or rationale into ticket bodies.** Tickets answer _what_ is being done and _how it'll be verified_. The _why_ lives in the wiki. If justification feels necessary, link to the wiki page that holds it; if no such page exists, suggest creating one via wiki.
8. **Don't duplicate spec detail from the source doc.** If a referenced doc owns the full spec, list scope only (names, structural decisions, enum/constant values, non-obvious gotchas) and link it as source of truth.

   **Bad: duplicates the schema doc:**

   > Fields: `username` (String), `email` (String), `firstName` (String)...

   **Good: scope only, defer to source:**

   > Fields per `User-Storage.md`. If ticket and doc disagree, the doc wins — flag in MR.

9. **Material from a cautioned wiki page does not belong in Scope, Implementation Approach, or Acceptance Criteria.** A wiki page carrying a top-of-page `> [!CAUTION]` block is under investigation and not ready for implementation. Route its material to `Out of Scope` or `Risks`, each with a link back to the cautioned page.
10. **Acceptance Criteria assert outcomes, not restatement.** Each criterion is a falsifiable check a reviewer would perform — not a repeat of scope/requirements, not a project-wide baseline (build/lint/test checks belong in the codebases `CLAUDE.md`), not subjective.

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
   > - `BaseEntity` and `MongoConfig` structurally mirror the bookings-app implementations
   > - No classes exist outside the File Structure diagram

   **Bad — vague pointer that requires cross-referencing:**

   > - Mongock migration creates the required indexes

   **Good — names the values inline:**

   > - Mongock migration creates indexes on `state`, `_class`, `createdAt`, and `createdBy`

11. **Testing names behaviors, not cases.** Feature and bug tickets require automated tests. For bugs, a regression test covering the reproduction case is mandatory. Name the behaviors that must have coverage; the implementing agent derives cases and edges from the code change, wiki, and codebase already in context. Do not enumerate cases, edges, frameworks, or file paths.
