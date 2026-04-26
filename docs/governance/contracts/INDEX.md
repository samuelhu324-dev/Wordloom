# Chronology-First Contracts Index v1

## Purpose

- This index is the canonical root for chronology-first governance-contract rebuild.
- It exists so rebuilt contracts can start from the earliest defended history and grow forward through explicit lineage, instead of continuing the older current-first contract extraction model.

## Current Standing

- `docs/governance/contracts/` is now the canonical root for rebuilt contracts.
- `docs/governance/legacy/contract/` and `docs/governance/legacy/contracts/` are retained legacy reference sets.
- The chronology-first rebuild now keeps one workflow-layer draft sourced from `S0A/2A`, one labs-layer draft sourced from `S0B/1A`, and one first parent-and-child packet sourced from `S0A-1A`.
- The chronology-first rebuild now also keeps one DOC-first governance-control contract sourced from `S0F-9A` so current-state versus event-history rules do not remain source-log prose only.
- The chronology-first rebuild now also keeps one runtime-owned observability contract sourced from `S4G-1B` so one bounded worker diagnostic chain does not remain source-log scaffold only.

## Current Rebuild Model

- A chronology-first contract is now defined as one rule-owning or boundary-owning state in the historical contract chain.
- Validation rows, migration mechanics, wrapper/transport shells, and similar retained chronology now stay outside the canonical contract chain unless they become the clearest owner of one governance rule.
- The canonical template now supports distinct lineage verbs for:
  - one-to-one supersession
  - split relationships
  - absorbed relationships
  - retirement relationships
- Canonical naming now uses one long-path readable id grammar rather than short opaque abbreviations:
  - `DOC-<DOMAIN>-<SUBDOMAIN>-...-<CATEGORY>-<NNNN>`
- The rebuild model now also distinguishes:
  - `parent contracts` for mechanism introduction, `why`, and boundary
  - `child contracts` for independently judgeable narrow rule bodies beneath that parent
- Split lineage is now read narrowly:
  - use it when one broader contract decomposes into narrower rule-owning children
  - do not use it for one-to-one replacement or loose partial absorption
## Current Rebuild Order

- First foundational packet: `S0A + S0B`
- Follow-on rebuild order: `S0C -> S0D -> S0E -> S0F`
- This order is chronology-first rather than projection-first:
  - `S0A + S0B` establishes the earliest decision spine
  - `S0C` and `S0D` extend the structural and operator grammar that later automation depends on
  - `S0E` then carries the first large mixed automation and lifecycle contract line
  - `S0F` remains last because it is the latest and still the densest mixed series

## Read Now

- Open `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md` for the rebuild boundary, order, and next steps.
- Use `docs/governance/contracts/_template-contract-record.md` as the temporary record template during the reset phase.
- Open the workflow-layer draft when the question is `what broader structured-doc workflow contract existed before narrower GitHub issue rules were split out?`
  - `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
- Open the labs-layer draft when the question is `what labs and snapshots rule sat beneath the broader workflow contract?`
  - `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-001-tools-labs-and-snapshots.md`
- Open the current parent-and-child packet when the question is `can this issue-first source now read as one parent mechanism contract plus narrower child rule contracts?`
  - `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  - `docs/governance/contracts/workflow/github/issues/title/DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-issue-title-encodes-level-and-category.md`
  - `docs/governance/contracts/workflow/github/issues/tags/DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-issue-tags-follow-role-based-naming.md`
- Open the DOC-first governance-control contract when the question is `what shared control-plane rule now fixes owner, steward, approval, verification, contribution, and handoff semantics before M4 begins?`
  - `docs/governance/contracts/control-plane/DOC-CONTROL-PLANE-0001-current-state-event-history-and-authorization-boundary.md`
- Open the runtime observability contract when the question is `what current runtime-owned diagnostic chain is already explicit enough to read as one released worker-surface contract?`
  - `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
- Use the moved legacy trees only as retained reference material while the new canonical chain is rebuilt:
  - `docs/governance/legacy/contract/`
  - `docs/governance/legacy/contracts/`

## Foundational Contracts

| contract id | standing now | role in rebuild |
| --- | --- | --- |
| `DOC-WORKFLOW-0001` | `draft` | workflow-layer contract for the structured-doc refinement pipeline and source-linking boundary |
| `DOC-WORKFLOW-LABS-001` | `draft` | labs-layer contract for snapshot classes, retention, and safe-to-purge cleanup |
| `DOC-WORKFLOW-GITHUB-ISSUES-0001` | `draft` | parent contract for introducing GitHub Issues as canonical workflow breakdown |
| `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001` | `draft` | child contract for issue-title hierarchy and category grammar |
| `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001` | `draft` | child contract for role-based issue-tag naming classes |
| `DOC-CONTROL-PLANE-0001` | `draft` | DOC-first control-plane contract for current-state fields, event-history placement, and the boundary against authorization semantics |
| `DOC-RUNTIME-OBSERVABILITY-0001` | `draft` | runtime-owned observability contract for one defended worker diagnostic chain |

## Reader Notes

- This index intentionally does not treat the moved legacy trees as canonical.
- Existing `view` surfaces may remain clearer than the current contract folders during the reset; that is the reason this rebuild lane exists.
- The earlier mixed `S0A-1A` preview has now been replaced by one parent contract plus two child contracts under the long-path naming grammar.
- The next intended step is user review of the broader `DOC-WORKFLOW-0001` workflow-layer draft, the narrower `DOC-WORKFLOW-LABS-001` labs-layer draft, and the GitHub-issues packet before later chronology-first population continues.