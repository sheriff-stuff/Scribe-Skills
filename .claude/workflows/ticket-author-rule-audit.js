export const meta = {
  name: 'ticket-author-rule-audit',
  description: 'Adversarially test every ticket-author rule and the workflow to find edge cases, gotchas, ineffective rules, and what works',
  phases: [
    { title: 'Probe rules', detail: 'design an adversarial battery per rule' },
    { title: 'Author', detail: 'author under temptation following the skill' },
    { title: 'Review', detail: 'blind reviewer pass (sonnet, matching shipped reviewer)', model: 'sonnet' },
    { title: 'Judge', detail: 'classify each rule: followed? enforceable? redundant? conflicting?' },
    { title: 'Analyse', detail: 'workflow process + static consistency checks' },
    { title: 'Synthesize', detail: 'bucket findings and prioritize fixes' },
  ],
}

// Re-runnable audit of the ticket-author skill. Reads SKILL.md, the reviewer,
// and templates from disk each run, so editing the skill and re-running yields
// a fresh diffable report. Optional args: a list of rule keys (see ALL_RULES) to
// scope the run to a subset, e.g. args: ["full-urls"] to re-run a single rule.

// ---- Rule inventory (names are the exact bolded leads from SKILL.md) ----
const ALL_RULES = [
  { key: 'actionable',          name: 'Write actionable descriptions',                          gist: 'AC, context, scope as a real issue' },
  { key: 'no-infer',            name: 'Do not infer technical decisions',                       gist: 'no prescribed class/pattern/lib/path/route without a wiki/code anchor or user ask' },
  { key: 'full-urls',           name: 'Use full URLs when referencing pages, code, or other projects', gist: 'absolute URLs; in-branch ticket refs are plain-text titles' },
  { key: 'existing-language',   name: 'Use the language of existing documentation',             gist: 'reuse existing names; no new terminology for named concepts' },
  { key: 'no-line-numbers',     name: 'Reference files, not line numbers',                      gist: 'no #L anchors; identify location by symbol/string/heading' },
  { key: 'approach-orients',    name: 'Implementation Approach orients, not prescribes',        gist: 'prose orientation by anchors, not numbered/bulleted imperative steps; every Scope item reachable' },
  { key: 'relationships-parts', name: 'Describe relationships in parts, not single verbs',      gist: 'name what to take and what to change; no bare mirror/match/follow/reference; infra names stay, domain names change' },
  { key: 'anchor-carries',      name: 'What the ticket carries depends on its anchor',          gist: 'wiki-anchored: no motivational why; codebase-anchored: causal-mechanical detail only' },
  { key: 'no-duplicate-spec',   name: "Don't duplicate spec detail from the source doc",        gist: 'scope only; link source of truth' },
  { key: 'ac-outcomes',         name: 'Acceptance Criteria assert outcomes, not restatement',   gist: 'falsifiable checks; no scope restatement, no project baselines, no subjective' },
  { key: 'testing-behaviours',  name: 'Testing names behaviours, not cases',                    gist: 'name behaviours; no enumerated cases/edges/frameworks/file paths; bug regression mandatory' },
  { key: 'odd-tickets',         name: 'ODD tickets request resolution of an existing wiki ODD', gist: 'always wiki-anchored; closes when wiki ODD resolved' },
  { key: 'frontmatter',         name: 'Frontmatter Schema',                                     gist: 'title required non-empty; type only epic; weight non-negative int; epic int|auto; labels list' },
  { key: 'file-naming',         name: 'File Naming',                                            gist: 'lowercase kebab-case named by subject' },
]

const selected = (Array.isArray(args) && args.length)
  ? ALL_RULES.filter(r => args.includes(r.key))
  : ALL_RULES

// ---------------- Schemas ----------------
const PROBE = {
  type: 'object', additionalProperties: false,
  required: ['temptingRequest', 'plantedTicket', 'plantedViolationDescription', 'boundaryCase', 'suspectedConflicts', 'likelyRedundant', 'redundancyReasoning'],
  properties: {
    temptingRequest: { type: 'string', description: 'self-contained user request to the author engineered so the natural response violates the target rule; includes fictional context + full https URLs; never names the rule' },
    plantedTicket: { type: 'string', description: 'complete ticket markdown (frontmatter + body), clean except it clearly violates the target rule' },
    plantedViolationDescription: { type: 'string', description: 'where/how the planted ticket violates the target rule' },
    boundaryCase: { type: 'string', description: 'a scenario on the rule boundary where reasonable authors could disagree' },
    suspectedConflicts: { type: 'array', items: { type: 'string' }, description: 'other ticket-author rule names that could pull against this one' },
    likelyRedundant: { type: 'boolean', description: 'would a competent author following the rest of the skill avoid this violation even without this rule?' },
    redundancyReasoning: { type: 'string' },
  },
}
const AUTHORED = {
  type: 'object', additionalProperties: false,
  required: ['ticketMarkdown', 'notes'],
  properties: {
    ticketMarkdown: { type: 'string', description: 'the complete ticket file content the skill would write to proposed-tickets/' },
    notes: { type: 'string', description: 'assumptions made' },
  },
}
const VIOL = {
  type: 'object', additionalProperties: false,
  required: ['rule', 'where', 'why'],
  properties: { rule: { type: 'string' }, where: { type: 'string' }, why: { type: 'string' } },
}
const REVIEW = {
  type: 'object', additionalProperties: false,
  required: ['authoredReview', 'plantedReview'],
  properties: {
    authoredReview: {
      type: 'object', additionalProperties: false, required: ['verdict', 'violations'],
      properties: { verdict: { type: 'string', enum: ['READY', 'NEEDS WORK'] }, violations: { type: 'array', items: VIOL } },
    },
    plantedReview: {
      type: 'object', additionalProperties: false, required: ['verdict', 'violations'],
      properties: { verdict: { type: 'string', enum: ['READY', 'NEEDS WORK'] }, violations: { type: 'array', items: VIOL } },
    },
  },
}
const JUDGE = {
  type: 'object', additionalProperties: false,
  required: ['rule', 'health', 'followed', 'enforceable', 'enforceabilityNote', 'evidence', 'edgeCases', 'gotchas', 'recommendation', 'severity'],
  properties: {
    rule: { type: 'string' },
    health: { type: 'string', enum: ['working-well', 'ineffective', 'edge-case', 'gotcha', 'mixed'] },
    followed: { type: 'boolean', description: 'did the authored ticket avoid violating the target rule under temptation?' },
    enforceable: { type: 'boolean', description: 'did the blind reviewer flag the planted violation and cite a correct/equivalent rule name?' },
    enforceabilityNote: { type: 'string', description: 'what the reviewer cited (or missed) for the planted ticket' },
    evidence: { type: 'string' },
    edgeCases: { type: 'array', items: { type: 'string' } },
    gotchas: { type: 'array', items: { type: 'string' } },
    recommendation: { type: 'string', description: 'concrete change to the skill text, or "keep as-is" if healthy' },
    severity: { type: 'string', enum: ['high', 'medium', 'low'] },
  },
}
const ANALYSIS = {
  type: 'object', additionalProperties: false,
  required: ['area', 'findings'],
  properties: {
    area: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['kind', 'detail', 'recommendation', 'severity'],
        properties: {
          kind: { type: 'string', enum: ['edge-case', 'gotcha', 'ineffective', 'working-well', 'coverage-gap'] },
          detail: { type: 'string' }, recommendation: { type: 'string' },
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
      },
    },
  },
}
const SYNTH = {
  type: 'object', additionalProperties: false,
  required: ['summary', 'workingWell', 'edgeCases', 'gotchas', 'ineffectiveRules', 'coverageGaps', 'prioritizedRecommendations'],
  properties: {
    summary: { type: 'string' },
    workingWell: { type: 'array', items: { type: 'string' } },
    edgeCases: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['rule', 'detail', 'recommendation'], properties: { rule: { type: 'string' }, detail: { type: 'string' }, recommendation: { type: 'string' } } } },
    gotchas: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['rule', 'detail', 'recommendation'], properties: { rule: { type: 'string' }, detail: { type: 'string' }, recommendation: { type: 'string' } } } },
    ineffectiveRules: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['rule', 'detail', 'recommendation'], properties: { rule: { type: 'string' }, detail: { type: 'string' }, recommendation: { type: 'string' } } } },
    coverageGaps: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['detail', 'recommendation'], properties: { detail: { type: 'string' }, recommendation: { type: 'string' } } } },
    prioritizedRecommendations: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['priority', 'change', 'rationale'], properties: { priority: { type: 'string', enum: ['P0', 'P1', 'P2'] }, change: { type: 'string' }, rationale: { type: 'string' } } } },
  },
}

// ---------------- Prompt builders (NB: no backticks inside these strings) ----------------
const SKILL = 'skills/ticket-author/SKILL.md'
const REVIEWER = 'agents/ticket-reviewer.md'
const ASSETS = 'skills/ticket-author/assets/'

const designPrompt = (r) =>
  'You are designing an adversarial test battery for ONE rule of the ticket-author Claude Code skill.\n\n' +
  'Target rule: "' + r.name + '"\nGist: ' + r.gist + '\n\n' +
  'Ground yourself first by reading:\n' +
  '- ' + SKILL + ' (find this rule under its bolded name; also read Workflow, Ticket Anchoring, Frontmatter Schema, File Naming, and the other Body Rules)\n' +
  '- the relevant template(s) under ' + ASSETS + '\n' +
  '- ' + REVIEWER + ' (how rules are enforced and what the reviewer can express)\n\n' +
  'Goal: reveal whether this rule AS WRITTEN (a) steers an author away from a tempting violation, (b) is detectable by the reviewer, (c) is well-defined at its boundary, (d) conflicts with any other rule, and (e) actually bites vs being redundant.\n\n' +
  'Produce:\n' +
  '- temptingRequest: a realistic, SELF-CONTAINED user request to the ticket author, engineered so the natural response VIOLATES the target rule. Bake in any fictional project context the author needs (wiki page names with full https URLs, code symbols, existing terminology) so a complete ticket can be written without a real repo. Do NOT mention the rule or that this is a test.\n' +
  '- plantedTicket: a complete realistic ticket markdown (frontmatter + body) that is clean EXCEPT it clearly violates the target rule. Keep all OTHER rules satisfied so the violation is isolated and unambiguous.\n' +
  '- plantedViolationDescription: name exactly where/how plantedTicket violates the rule.\n' +
  '- boundaryCase: a scenario sitting on the rule boundary where competent authors could reasonably disagree about whether it violates.\n' +
  '- suspectedConflicts: names of other ticket-author rules that could pull against this one (empty if none).\n' +
  '- likelyRedundant + redundancyReasoning: would a competent author following the rest of the skill avoid this violation even if this rule did not exist?'

const authorPrompt = (probe) =>
  'You are running the ticket-author skill to fulfil a user request. Follow the skill exactly — it is the authority.\n\n' +
  'Read ' + SKILL + ' and the appropriate template under ' + ASSETS + ', then author the ticket.\n\n' +
  'User request:\n"""\n' + probe.temptingRequest + '\n"""\n\n' +
  'Assume the project context in the request is accurate; you may invent plausible additional anchors with full https URLs if needed. ' +
  'Output the complete ticket file content (frontmatter + body) exactly as you would write it to proposed-tickets/, in ticketMarkdown. Put assumptions in notes. Do not add commentary outside the schema.'

const reviewPrompt = (ctx) =>
  'You are running the ticket-reviewer subagent. Read ' + REVIEWER + ' and ' + SKILL + ', then apply the reviewer rubric strictly.\n\n' +
  'Two ticket files are provided inline. Treat each as the FULL contents of a file in proposed-tickets/. Skip the disk-glob and url-resolution steps and review the inline text directly against Frontmatter Schema, File Naming, template structure (read templates under ' + ASSETS + ' as needed), and EVERY Body Rule. Cite offending text verbatim and name the exact bolded Body Rule for each violation.\n\n' +
  '=== TICKET A (filename: authored.md) ===\n' + ctx.authored.ticketMarkdown + '\n=== END TICKET A ===\n\n' +
  '=== TICKET B (filename: planted.md) ===\n' + ctx.probe.plantedTicket + '\n=== END TICKET B ===\n\n' +
  'Review BOTH independently and report each one\'s verdict and full violation list. Do not assume either ticket is correct or incorrect.'

const judgePrompt = (ctx, r) =>
  'You are auditing ONE rule of the ticket-author skill using empirical test results.\n\n' +
  'Target rule: "' + r.name + '"\nGist: ' + r.gist + '\n\n' +
  'Designer prior:\n' + JSON.stringify({ plantedViolationDescription: ctx.probe.plantedViolationDescription, boundaryCase: ctx.probe.boundaryCase, suspectedConflicts: ctx.probe.suspectedConflicts, likelyRedundant: ctx.probe.likelyRedundant, redundancyReasoning: ctx.probe.redundancyReasoning }, null, 2) + '\n\n' +
  'AUTHORED ticket (written under a request engineered to tempt violating this rule):\n' + ctx.authored.ticketMarkdown + '\n\n' +
  'BLIND reviewer verdict on the AUTHORED ticket:\n' + JSON.stringify(ctx.review.authoredReview, null, 2) + '\n\n' +
  'PLANTED ticket (deliberately violates this rule per the prior):\n' + ctx.probe.plantedTicket + '\n\n' +
  'BLIND reviewer verdict on the PLANTED ticket:\n' + JSON.stringify(ctx.review.plantedReview, null, 2) + '\n\n' +
  'Decide, judging the ticket text yourself (do not just trust the reviewer):\n' +
  '- followed: did the AUTHORED ticket actually avoid violating the target rule despite the temptation?\n' +
  '- enforceable: did the blind reviewer flag the planted violation AND cite the correct or an equivalent rule name? Set enforceabilityNote to what it cited or missed. A miss, or a citation under the wrong rule, means NOT enforceable.\n' +
  '- edgeCases: under-specified boundary scenarios (use the designer boundaryCase and what you saw). \n' +
  '- gotchas: rule-vs-rule conflicts or misfires — e.g. complying with this rule forced a different violation, the reviewer raised a false positive, or two rules contradict.\n' +
  '- health: working-well (followed AND enforceable AND no serious boundary/conflict issue); ineffective (rule is redundant, never bites, OR is structurally undetectable by the reviewer); edge-case (real boundary ambiguity); gotcha (conflicts with or undermines another rule); mixed.\n' +
  '- recommendation: a concrete edit to the skill text, or "keep as-is" if healthy. severity: high|medium|low.'

// ---------------- Track 1: per-rule adversarial pipeline ----------------
phase('Probe rules')
log('Auditing ' + selected.length + ' rules x 4 stages (design -> author -> blind review -> judge)')

const pipelinePromise = pipeline(
  selected,
  (r)            => agent(designPrompt(r),               { label: 'design:' + r.key, phase: 'Probe rules', schema: PROBE }).then(probe => ({ r, probe })),
  (ctx, r)       => agent(authorPrompt(ctx.probe),       { label: 'author:' + r.key, phase: 'Author', schema: AUTHORED }).then(authored => ({ ...ctx, authored })),
  (ctx, r)       => agent(reviewPrompt(ctx),             { label: 'review:' + r.key, phase: 'Review', model: 'sonnet', schema: REVIEW }).then(review => ({ ...ctx, review })),
  (ctx, r)       => agent(judgePrompt(ctx, r),           { label: 'judge:'  + r.key, phase: 'Judge', schema: JUDGE }),
)

// ---------------- Tracks 2 & 3: process + static analysis (run concurrently) ----------------
const analysisThunks = [
  () => agent(
    'Analyse the ticket-author TYPE-SELECTION decision table (Workflow step 1) in ' + SKILL + '. Read the skill. ' +
    'Enumerate the input space (User named type? / Type is ODD? / Type is Spike|Bug|Chore?) and test every combination against the table rows. ' +
    'Find rows that overlap, are unreachable, are ambiguous (e.g. a user-named type that is also an ODD; "No / No / No -> Feature" swallowing documentation tickets), or that produce a surprising outcome. Report edge-cases, gotchas, ineffective branches, and what works.',
    { label: 'process:type-table', phase: 'Analyse', schema: ANALYSIS }),
  () => agent(
    'Analyse ANCHOR IDENTIFICATION in ' + SKILL + ' (Ticket Anchoring section + Workflow step 2 + the Body Rule "What the ticket carries depends on its anchor"). Read the skill. ' +
    'Stress the wiki-anchored vs codebase-anchored dichotomy: is it exhaustive and mutually exclusive? What about a ticket that is genuinely both (mechanical sequencing AND a domain why)? How load-bearing and how often-hit is "if unsure, ask the user"? Can a misidentified anchor pass validation? Report edge-cases, gotchas, ineffective guidance, and what works.',
    { label: 'process:anchoring', phase: 'Analyse', schema: ANALYSIS }),
  () => agent(
    'Analyse EPIC and CROSS-TICKET logic in ' + SKILL + ' (Workflow step 4, the Frontmatter epic field, and the reviewer cross-ticket rule "epic: auto only when an epic file is present"). Read ' + SKILL + ' and ' + REVIEWER + '. ' +
    'Test: multiple epics requested in one branch; a child with an explicit epic IID alongside auto siblings; epic: auto with no epic file; an epic file with no children. Report edge-cases, gotchas, ineffective rules, and what works.',
    { label: 'process:epic', phase: 'Analyse', schema: ANALYSIS }),
  () => agent(
    'Analyse the SELF-VALIDATE / REVIEW LOOP and reporting contract in ' + SKILL + ' (Workflow steps 6-9) and ' + REVIEWER + ' output format. Read both. ' +
    'Test for: non-termination / oscillation between author and reviewer, handling of "No tickets to review.", the "M of M tickets ready" gate, NOTES/url-resolution handling, and what happens when self-validation and the reviewer disagree. Report edge-cases, gotchas, ineffective steps, and what works.',
    { label: 'process:review-loop', phase: 'Analyse', schema: ANALYSIS }),
  () => agent(
    'Do a STATIC COVERAGE check between the Validation checklist and the Body Rules in ' + SKILL + '. Read the skill. ' +
    'Build a bidirectional map: every Validation checkbox to its Body Rule, and every Body Rule to its checkbox. Flag orphans BOTH ways — e.g. a checklist item with no Body Rule behind it (look hard at the Risks checklist item), or a Body Rule with no checklist item. Orphan checks and orphan rules are prime "ineffective/coverage-gap" candidates. Report findings with kind=coverage-gap or ineffective as appropriate.',
    { label: 'static:validation-coverage', phase: 'Analyse', schema: ANALYSIS }),
  () => agent(
    'Do a STATIC COVERAGE check between the ticket-author rules and what the ticket-reviewer can actually enforce. Read ' + SKILL + ' and ' + REVIEWER + '. ' +
    'For each Body Rule, frontmatter constraint, naming rule, and template-conditional section, decide whether the reviewer\'s "What to check" + Inputs + output schema let it actually DETECT and EXPRESS a violation. Flag rules that are structurally undetectable (e.g. needs repo content the reviewer cannot see, or is subjective), and template conditional sections like "User Story (only for user-facing features)" that the reviewer cannot adjudicate. Report ineffective/coverage-gap findings and what works.',
    { label: 'static:reviewer-coverage', phase: 'Analyse', schema: ANALYSIS }),
]
const analysisPromise = parallel(analysisThunks)

const [ruleResultsRaw, analysesRaw] = await Promise.all([pipelinePromise, analysisPromise])
const ruleResults = ruleResultsRaw.filter(Boolean)
const analyses = analysesRaw.filter(Boolean)

// ---------------- Synthesis ----------------
phase('Synthesize')
const synthesis = await agent(
  'You are synthesizing an audit of the ticket-author skill into an improvement report. ' +
  'Bucket findings into the four categories the user asked for, plus coverage gaps and a prioritized fix list. Be specific and cite the rule name for each item. Prefer concrete skill-text edits over vague advice. Do not invent findings beyond the evidence.\n\n' +
  'PER-RULE JUDGEMENTS (JSON):\n' + JSON.stringify(ruleResults, null, 2) + '\n\n' +
  'PROCESS + STATIC ANALYSES (JSON):\n' + JSON.stringify(analyses, null, 2) + '\n\n' +
  'Produce: summary; workingWell (rules/process that held up); edgeCases; gotchas (incl. rule-vs-rule conflicts); ineffectiveRules (redundant or unenforceable); coverageGaps (validation<->rules<->reviewer mismatches); prioritizedRecommendations (P0/P1/P2 with concrete change + rationale).',
  { label: 'synthesize', phase: 'Synthesize', schema: SYNTH })

return { synthesis, judgments: ruleResults, analyses }
