---
description: Check a skill or agent for DRY violations
argument-hint: <path to SKILL.md or agent .md>
allowed-tools: Read, Grep, Glob
---

Review the file at `$ARGUMENTS` for DRY (Don't Repeat Yourself) violations. If it is a skill folder, read its `SKILL.md` and any bundled assets it links. Report only high-signal findings — a single instruction that genuinely lives in two or more places, not wording that merely looks similar.

Look for these forms:

1. **Repeated policy across steps or sections.** One instruction copied into several enumerated steps or bullets, when it governs all of them and belongs once at a higher altitude (e.g. a top-level rule above the steps). The smell: the same sentence appears in multiple steps.

2. **Rules duplicated between an agent prompt and the skill it enforces.** When an agent restates rules that the skill it pairs with already owns, those rules should come from `skills:` frontmatter, not be copied into the prompt.

3. **Template shape restated in prose.** When the skill ships a template asset, the prose must not re-describe what the template already shows — placeholder syntax, field order, which fields are optional, placement comments. Prose carries only policy, workflow, cross-skill contracts, and judgement calls.

4. **A value duplicated where it must stay in sync.** The same heading text, format string, path, or other literal written in more than one spot, so a change has to land in every copy.

For each finding, report:
- **Where** — the locations holding the duplicate (file + step/section).
- **What** — the single piece of knowledge that is repeated.
- **Fix** — the one place it should live instead.

Do not edit the file. Only report. If you find nothing, say so plainly rather than inventing findings.
