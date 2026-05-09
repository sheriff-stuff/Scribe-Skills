# Labels

Labels follow GitLab's scoped-label convention (`scope::value`). Every ticket carries:

- `type::<kind>` — set by the template (`type::feature`, `type::bug`, `type::spike`, `type::chore`, `type::epic`, `type::odd`).
- `area::<name>` — the part of the system the work touches (`area::backend`, `area::frontend`, `area::infra`). Areas reuse names already in use in the project; new ones are not invented when a matching label exists.

Bug tickets additionally carry `severity::*`, `env::*`, and `network::*` scoped labels.

ODD tickets additionally carry `owner::<role>` — the discipline that owns the decision. The scope is multi-assignable: cross-discipline ODDs carry every applicable `owner::*` label so reviewers from each discipline can filter the issue list to ODDs they need to weigh in on. Roles reuse labels already in use in the project (common examples: `owner::ba`, `owner::ux`, `owner::developer`); new ones are not invented when a matching label exists.
