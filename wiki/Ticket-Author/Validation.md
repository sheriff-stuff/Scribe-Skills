# Validation

After writing tickets, the skill walks this checklist against each one. Items that fail are fixed and the checklist is re-run on the revised ticket until every item passes. Failures that depend on information only the user can provide are surfaced in one message rather than asked piecemeal.

- The anchor is identified — each ticket is wiki-anchored or codebase-anchored, and the body matches.
- Description is actionable — acceptance criteria, context, and scope.
- No inferred technical decisions — no prescribed class names, design patterns, library choices, file paths, or route paths without a wiki/code anchor or user request.
- Existing documentation's language used; no new terminology for concepts already named.
- File references identify content (symbol, string, section heading), not line numbers.
- Implementation Approach orients, not prescribes — prose, no numbered or bulleted imperative steps; every Scope item reachable from it.
- Relationships described in parts — what to take and what to change; no bare single verbs (mirror, match, follow, reference).
- Wiki-anchored tickets link the wiki and carry no motivational rationale — business case, user impact, or strategic priority — in the body.
- Codebase-anchored tickets carry only causal-mechanical detail — sequencing, invariants, dependencies — and no motivational rationale.
- No duplicated spec detail from a source-of-truth doc.
- Acceptance Criteria assert outcomes — each is a falsifiable check, not a restatement of Scope, a project baseline, or a subjective judgement.
- Risks entries point to concrete exposure outside the ticket's control.
- Testing names behaviours, not cases — no enumerated cases, edges, frameworks, or file paths.
- ODD tickets resolve an existing wiki ODD — the `Resolve [ODD-…]` line links the ODD ID to its owner wiki page.
