# Checks

- **Body Rules** — every Body Rule from the [Wiki Page Author](../Wiki-Page-Author) skill. Applied outside `> [!ODD]` and `> [!CAUTION]` blocks only.
- **ODD** — block IDs follow `ODD-<AREA>-<slug>`; owner page carries the `<a id="ODD-...">` anchor; one decision per block; pointer blocks link to the owner anchor; reason sentence present.
- **CAUTION** — block IDs follow `CAUTION-<AREA>-<slug>`; anchor present; block sits at the top of the page immediately after the H1 description comment; reason sentence present.
- **Naming** — file, folder, and section heading names follow the subject, not the content type. Generic names (`docs/`, `notes/`, `## Notes`, `## Details`) are flagged.
- **Template** — required scaffolding from the page template is present. Optional pieces are not flagged when legitimately omitted.
- **Cross-page** — every pointer block resolves to an existing owner anchor; owner `Affects:` lines are reciprocated by pointer blocks on the listed pages.
- **Index sync** — every target page is linked from `wiki/index.md` or `wiki/home.md`.
