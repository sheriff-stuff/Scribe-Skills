# Body Rules

These apply everywhere on a page except inside `> [!ODD]` and `> [!CAUTION]` callout blocks:

- One subject per page. Content belonging to a different subject is suggested for the right page rather than added. The test is whether the content describes the subject of the page, or describes how another part of the application uses the subject — the latter belongs on the consuming feature's page.
- Files, folders, and section headings are named by subject, not by content type.
- Present tense, declarative — pages state what the application does, not what it doesn't.
- Confirmed answers go in the body; uncertainty goes in a `> [!ODD]` block placed next to the affected section. Facts are not inferred from related pages, related code, or what seems plausible.
- No rationale on the page. Justification lives in a design decision record, linked from the page.
- No revision history. Updates replace content.
- For external services and libraries, the page documents the integration — which component, endpoint, or module is used and what it does — not the third party's API surface. Properties, attributes, slots, and parameters live in the library's own documentation. Relating a local structure to an external shape is allowed; reproducing the shape is not.
- Code identifiers (file names, variable names, lookup keys) and structural conventions (naming patterns, directory layouts, class and method signatures) live in the code, not the wiki. Technology choices and mechanisms ("loaded via Mongock changesets", "JSON fixtures", "stored in MongoDB") are design facts and belong on the page. Domain model vocabulary — field names and attributes that define the application's data model — is a design fact. The test: a name that appears in conversations about what the application is belongs on the page; a name that appears only in conversations about how the code is organised does not.
- Anything linkable is written as an inline link — files and folders inside the wiki, files and folders elsewhere in the repo, and external URLs. Bare paths and bare URLs are used only when the target genuinely cannot be linked. Internal targets use no `.md` extension.
- No pleonasm. Facts are stated without redundant qualifiers, intensifiers, or filler.
- Body prose adjacent to an ODD block does not restate it. The block carries the question, options, and any hedging; the body around it stays in confident present tense.
