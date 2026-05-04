---
title: "Add a user search endpoint"
labels: [type::feature]
weight: 3
assignees: [ben]
milestone: "Sprint 12"
due_date: "2026-06-01"
---

> **Feature** — Add `/users/search` returning paginated matches.

## Scope

1. Endpoint accepts `q` query param.
2. Returns 20 results per page.

## Acceptance Criteria

- [ ] `/users/search?q=alex` returns matching users.
