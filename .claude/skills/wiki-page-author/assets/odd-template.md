# Open Design Decision Template

The block lives on the page that owns the concept, inline next to the section it affects.

> [!ODD] ODD-<TOPIC>-<NNN> — [Question stated in one sentence]?
>
> **Status:** Open
> **Affects:** this page, [Other page](../Folder/Page), [Other page](../Folder/Page)
> **Options:** A) [option], B) [option], C) [option]
> **Open questions:** [related questions still under discussion]

---

Notes for the agent (do not include in the actual page):

- Place the block next to the section it affects, not at the end of the page.
- The topic prefix matches the page or folder concept (e.g. `PERM`, `FORM`, `SESS`).
- The number is `max + 1` of any existing `ODD-<TOPIC>-` in the wiki, including retired ones. Grep before assigning. IDs are stable and never reused — do not fill gaps left by resolved ODDs, because the retired ID may still be referenced by commits, tickets, or PRs.
- Omit `Options:` or `Open questions:` lines if they do not apply yet.
- If the ODD affects only the page it lives on, `Affects:` can read just `this page`.
