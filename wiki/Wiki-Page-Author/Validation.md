# Validation

Before reporting work as done, the skill walks a checklist against every page it wrote or changed. Items that fail are fixed and the checklist is re-walked, until every item passes. If a failure requires information only the user can provide, the skill stops and lists every unresolved item in one message rather than asking piecemeal.

The checklist covers:

- Every rule in [Body Rules](Body-Rules), applied outside `> [!ODD]` and `> [!CAUTION]` blocks.
- Every rule in [Open Design Decision](Open-Design-Decision), applied inside `> [!ODD]` blocks touched by the change.
- Every rule in [Page Investigation Caution](Page-Investigation-Caution), applied inside `> [!CAUTION]` blocks touched by the change.
- Cross-page consistency: pages topically related to the target are read in full, and content already covered elsewhere — or content that belongs on a different existing page — is flagged to the user.
- Index sync: when a page is added or removed, [`home.md`](../home) reflects it.
- Resolution cleanup: when an ODD is resolved, every pointer block referencing its ID is removed and the affected body sections are rewritten in confident present tense. When a caution is lifted, the block is removed and the body is rewritten as ground truth.
- Inconsistencies on other pages introduced by the change are flagged to the user, not silently fixed.
