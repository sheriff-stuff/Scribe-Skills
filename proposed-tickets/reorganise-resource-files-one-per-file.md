---
title: "Reorganise resource files one per file"
labels: [type::chore, "area::build"]
weight: 1
---

> **Chore** — Project resources are split to one item per file under a fixed directory layout.

## Context

Resource files currently mix multiple items per file, so changes collide and diffs are noisy.

## Scope

Project resources follow a one-thing-per-file convention:

- one file per user under `src/main/resources/users/`, named `<username>.yml`
- one config per environment under `src/main/resources/env/`
- one migration per release under `src/main/resources/db/migrations/`

## Implementation Approach

Split the existing combined resource files into the layout above. The loader already resolves files by directory, so no loader change is needed once the files are split.

## Testing

- The application loads every resource from the split files with the same values as before the split.

## Acceptance Criteria

- [ ] Each user, environment config, and migration resides in its own file under the directories named in Scope
- [ ] The application loads with the same resolved resource values as before the split
