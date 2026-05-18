# Checks

- **Body Rules** — every Body Rule from the [Wiki Page Author](../Wiki-Page-Author) skill. Applied outside `> [!ODD]` and `> [!CAUTION]` blocks only.
- **ODD** — every rule in the [Open Design Decision](../Wiki-Page-Author/Open-Design-Decision) page's rules section. Applied only inside `> [!ODD]` blocks.
- **CAUTION** — every rule in the [Page Investigation Caution](../Wiki-Page-Author/Page-Investigation-Caution) page's rules section. Applied only inside `> [!CAUTION]` blocks.
- **Naming** — the Body Rule on naming files, folders, and section headings by subject. Generic names (`docs/`, `notes/`, `## Notes`, `## Details`) are flagged.
- **Template** — required scaffolding from the page template is present. Optional pieces are not flagged when legitimately omitted.
- **Cross-page** — every pointer `> [!ODD]` block references an ID that exists as an owner ODD somewhere in the wiki; owner `Affects:` lines are reciprocated by matching pointer blocks on the listed pages.
- **Index sync** — every target page is linked from `wiki/index.md` or `wiki/home.md`.
