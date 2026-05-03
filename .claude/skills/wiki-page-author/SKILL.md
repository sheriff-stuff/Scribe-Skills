---
name: wiki-page-author
description: >
  Use this skill when writing or updating any page in the project wiki, including
  creating a new page, changing an existing one, removing a page, adding or resolving
  open design decisions, or organising content into folders. Trigger on phrases like
  "add to the wiki", "update the wiki", "document this", "write a page about", or any
  request that produces a markdown file under the wiki, even if the user does not
  explicitly say "wiki". Do not use for changelog entries (handled by wiki-changelog),
  link checking (handled by wiki-link-check), or content outside the wiki repo.
---

# Wiki page author

The wiki is a living spec describing the current state of the application — present tense, factual, reference-only. Pages exist to tell a future agent or human what the application is, not how it got there or why.

## What a page is

A page describes one subject. The subject is named in the folder and filename. The page states facts about that subject in confident present tense.

A page is not:

- a tutorial, how-to, or onboarding doc
- a record of decisions or rationale
- a changelog or history of what the page used to say
- a justification for why one approach was chosen over another

If the user asks for any of those, the content does not belong in the wiki. Suggest where it should go instead (commit message, MR description, a separate decisions doc) — do not refuse to help, just route it correctly.

## Page template

Every page follows this shape. Omit any section that has no content; do not include empty headings.

```markdown
# [Subject]

One-sentence statement of what this page is about.

## [Section name]

Facts about the subject. Present tense, declarative.

## [Section name]

Facts about the subject. Present tense, declarative.

## Related

- [Other page](../Folder/Page)
- [Other page](../Folder/Page)

## Open design decisions

- Question that has not yet been answered. Options if known.
- Question that has not yet been answered.
```

Section names under the subject are themselves subject-named, not format-named. `## Validation rules` is good. `## Notes` and `## Details` are not.

## Writing rules

These are the rules every page must follow. Apply them every time, on every page.

- **Present tense, declarative.** "The user table stores email and a hashed password." Never "we will store" or "we plan to" or "the idea is to".
- **State facts positively.** "Forms render one question per page." Never "forms do not render multiple questions per page". Normal negative facts are fine: "this field is optional".
- **Only confirmed facts.** If a fact is unknown or undecided, do not write it. Ask the user. If they want it recorded, put it in `## Open design decisions` at the bottom.
- **No hedging.** Do not write "likely", "probably", "should", "might", "appears to". The page either states a fact or asks a question (in `## Open design decisions`).
- **No rationale.** The page describes what the application is, never why. If the user provides reasoning, drop it from the page. The why lives in commits and MRs.
- **No history.** When updating a page, replace content. Do not write "previously this said X" or "changed from Y". The diff is the history.
- **One subject per page.** If content belongs to a different subject, suggest the correct page or folder rather than adding it.
- **Subject-named files and folders.** `Forms/`, `Users/`, `Data/`. Never `docs/`, `notes/`, `architecture/`, `analysis/`.
- **Internal links use no `.md` extension.** `[text](../Folder/Page)`, never `[text](../Folder/Page.md)`.

## Procedure: writing a new page

1. Identify the subject from the user's request. If unclear, ask.
2. Identify the folder. If no existing folder fits, propose a new subject-named folder before creating it.
3. Identify the filename. Subject-named, matches the page's `# Heading`.
4. Write the page following the template above.
5. Update `home.md` to include the new page in its index.
6. Confirm to the user what was created.

## Procedure: updating an existing page

1. Read the current page in full.
2. Apply the change as a replacement of the relevant section. Do not annotate the change in the page itself.
3. If the change makes any other page in the wiki inconsistent, flag this to the user — do not silently update other pages.
4. If the change adds or removes a page, update `home.md`.
5. Confirm to the user what was changed.

## Procedure: open design decisions

When the user provides information that includes an unanswered question:

1. Write everything that is confirmed in the body of the relevant page, in present tense.
2. Add the unanswered question as a bullet in `## Open design decisions` at the bottom of that page.
3. The bullet is a question, not a partial answer. "Whether sessions persist across browser restarts." Not "Sessions probably persist."

When an open design decision gets resolved:

1. Rewrite the relevant section of the page in confident present tense, incorporating the answer.
2. Delete the bullet from `## Open design decisions`.
3. If the section becomes empty, remove the heading.

## Validation before finishing

Before reporting back to the user, check:

- [ ] Every internal link uses the no-`.md` form.
- [ ] No sentence contains "likely", "probably", "should", "might", "we will", "we plan to", "previously", "used to".
- [ ] The page makes sense read top-to-bottom by someone who has never seen the application.
- [ ] `home.md` reflects any added or removed pages.
- [ ] No content describes why a choice was made.

If any check fails, fix it before responding.

## Gotchas

- The wiki is updated by replacement. There is no `## Changelog` or `## History` section on individual pages — those go in the separate `Changelog` page (handled by a different skill, not this one).
- "I'm not sure" from the user is a signal to add an entry to `## Open design decisions`, not to guess and write a confident-sounding sentence.
- A request to "add notes" or "document my thinking" is usually not a wiki request. The wiki holds confirmed facts about the application; thinking and notes belong elsewhere. Ask before writing.
- The application being documented is in a separate repo. Do not look for its source code in this repo and do not infer facts about the application from any code that happens to be present here.
- `home.md` is the page index. Every page in the wiki must be reachable from it. Update it in the same operation as adding or removing a page, never as a follow-up.
- Folder names describing content type (`docs/`, `notes/`, `analysis/`, `architecture/`) are wrong and must be renamed if encountered. Folders are subject names.
- When suggesting a new folder, the name describes what the content is about, not how it was produced or what kind of document it is.
