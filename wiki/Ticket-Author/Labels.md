# Labels

Labels follow GitLab's scoped-label convention (`scope::value`). Every ticket carries:

- `type::<kind>` — set by the template (`type::feature`, `type::bug`, `type::spike`, `type::chore`, `type::documentation`, `type::epic`, `type::odd`).
- `area::<name>` — the part of the system the work touches (`area::backend`, `area::frontend`, `area::infra`). Areas reuse names already in use in the project; new ones are not invented when a matching label exists.

Bug tickets additionally carry `severity::*`, `env::*`, and `network::*` scoped labels.

ODD tickets additionally carry `owner::<role>` — the discipline that owns the decision. The scope is single-assignable per GitLab's scoped-label rules; cross-discipline ODDs pick the primary owner. Roles reuse labels already in use in the project (common examples: `owner::ba`, `owner::ux`, `owner::developer`); new ones are not invented when a matching label exists.
