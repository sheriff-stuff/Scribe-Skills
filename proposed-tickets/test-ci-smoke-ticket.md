---
title: "CI smoke test — confirm proposed-tickets workflows wire up correctly"
---

> **Feature** — Throwaway ticket used to verify the validate workflow runs on PRs and the create workflow runs on merge.

## Scope

1. Validate workflow runs and passes on this PR (no labels referenced, so no label-existence checks).
2. After merge, the create workflow opens a GitHub issue mirroring this file.
3. The create workflow then commits a deletion of this file from `master`.

## Acceptance Criteria

- [ ] PR shows a green check from `Proposed tickets — validate`.
- [ ] On merge, a new GitHub issue exists with this title.
- [ ] After the create workflow finishes, this file no longer exists on `master`.
