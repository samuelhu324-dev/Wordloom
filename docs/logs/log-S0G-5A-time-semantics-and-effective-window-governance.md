# log-S0G-5A (Phase 5A: time semantics and effective-window governance)

---

**id**: `S0G-5A`
**kind**: `log`
**title**: `time semantics and effective-window governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Contract, Records, Evidence, epic/s0, sub/5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-4B-doc-contract-release-transition-register-and-writeback-chain-governance.md`
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_2**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_3**: `docs/governance/contracts/_template-contract-release-transition-register.md`
  **reference_log_4**: `docs/logs/log-S0G-1C-workflow-scripts-family-opening-and-s0b-2a-ledger-consumption.md`
  **reference_log_5**: `docs/governance/contracts/workflow/scripts/DOC-WORKFLOW-SCRIPTS-0001-taxonomy-and-stable-entrypoint-governance.md`
  **reference_log_6**: `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/5a`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-23`
**updated**: `2026-04-23`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` remain the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the repo is still fixing the default time semantics model rather than landing one final second-level audit schema everywhere.
- `reviewed` should remain `pending` until the repo fixes one defended answer for `artifact lifecycle time`, `semantic effective time`, and `reader/routing validity time` across logs, contracts, and ledgers.

## Decision / Outcome

**Decision**:

- `S0G-5A` opens as the bounded follow-up for time semantics before business packets force a more complex coexistence model.
- This lane treats the problem as `time-semantics governance + default derivation rules + template writeback planning`, not as one immediate repo-wide timestamp retrofit sweep.
- The immediate deliverable is one defended default answer for:
  - which time fields are only `artifact lifecycle time`;
  - which fields should carry `semantic effective time` for contracts;
  - whether ledgers should track one narrower `routing validity` window rather than pretending to own rule-birth time;
  - when a family transition register should begin carrying explicit `window` dates at all.

**Default choices (phase defaults / v1)**:

- Keep source logs narrow: log frontmatter should continue to own `artifact lifecycle time`, not every downstream semantic-effective field.
- Default `semantic effective time` for a first contract release to the source log's `created` time unless stronger evidence proves an earlier or later start.
- Default `semantic effective until` to `ongoing` until one later defended successor or explicit replacement surface makes the end date real.
- Do not ask support-only ledgers to own `rule birth time`; if ledger time fields are later added, they should default to `routing verdict validity` only.
- Do not open family transition-window dates until a family actually has more than one reader-relevant release or a real fallback/coexistence period.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.

## PR Summary Inputs (optional)

- This packet is expected to drive template clarification before any wider backfill, so review should focus on time semantics and derivation defaults rather than on bulk retroactive edits.

**PR summary bullets**:

- Define one low-complexity time-semantics model that separates artifact lifecycle, contract effective time, and ledger routing-validity time.
- Fix one default derivation rule so first releases and replacements can be dated without inventing precision the repo does not actually have.
- Decide whether ledger and register templates need bounded additions now or should wait until a real multi-release coexistence case appears.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
- Runbook: ``
- Evidence artifact: ``

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/logs/_template-log-phase-drills-evidence.md`
- `P0-C1-S2` | artifact: `docs/governance/contracts/_template-contract-record.md`

## Exported Sections / Outlet Ownership

- This slice starts as one `contract-governance rule + template-clarification + log-retained core` lane.
- The expected first landing is one defended default time-semantics rule set for logs and contracts; any ledger/register template change should leave this log only if the experiments prove it is necessary.

**Outlet ownership**:

- `contract`: expected landing surface for contract-level effective-time defaults and any note-level clarification on how first-release dates are derived
- `runbook`: no-op by default
- `view`: no-op by default; a reader-facing time summary should wait until the repo has enough families for a comparative view to matter
- `index/front-door`: no-op by default
- `disposition/placement`: possible later landing only if old support-only time assumptions must be explicitly deprecated or reclassified
- `log-retained core`: time-model reasoning, derivation rules, and sample application notes remain here

## Definitions (optional)

- **artifact lifecycle time**: when a file or packet was created, updated, or reviewed inside the repo as an artifact.
- **semantic effective time**: when the defended rule meaning owned by a contract should be read as starting or ending in force.
- **reader/routing validity time**: when one ledger or reader-surface verdict became the current routing interpretation, independent of when the underlying rule first existed.
- **transition window**: one bounded family-level overlap period where more than one release remains concurrently reader-relevant.

## Constraints

- Do not collapse artifact-lifecycle timestamps and semantic-effective timestamps into one overloaded field.
- Do not ask the repo to fabricate second-level historical timestamps where only day-level evidence exists.
- Do not retrofit every existing contract and ledger before the default derivation rule is stable.
- Do not introduce transition-window fields into single-release families just because the register template can support them.

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `source log` | `has the repo named the distinct time layers tightly enough to stop mixing them?` | `explicit three-layer model in this log` | `entry step for the lane` |
| `SUP` | `not-required` | `n/a` | `is this lane later evidence against one accepted source-owned row?` | `explicit no-SUP verdict in this log` | `default is no SUP because this lane fixes template-level defaults first` |
| `parent ledger` | `conditional` | `support-only ledger template or sample ledger` | `does the repo need a new ledger-specific validity field after the default model is fixed?` | `template note or explicit no-ledger-field verdict` | `ledger time should stay routing-validity only if added` |
| `contract impact decision` | `required` | `source log` | `does the lane require contract-template clarification for effective_from/effective_until defaults?` | `explicit classified verdict` | `main decision gate` |
| `contract mutation` | `required` | `contract template or sample contract` | `should the contract template own the default effective-time derivation rule?` | `template writeback or explicit no-contract-mutation verdict` | `default expectation is yes for contract templates` |
| `transition register update` | `conditional` | `transition-register template or n/a` | `does the repo need window-date guidance now or only when real coexistence appears?` | `template note or explicit defer-register-window verdict` | `single-release families should not force register dates early` |
| `bridged contract reconciliation` | `conditional` | `affected sample logs/contracts` | `does one sample family need a demonstration backfill after the default rule is fixed?` | `sample writeback or explicit no-sample-reconciliation verdict` | `use only if one concrete sample improves clarity materially` |

## Scope

- `P0`: fix the three-layer time-semantics model and default derivation language
- `P1`: write back the default rule into the log and contract templates
- `P2`: decide whether ledger and register templates need bounded additions now
- `P3`: optionally demonstrate the rule on one live sample such as `S0B-2A / S0G-1C / DOC-WORKFLOW-SCRIPTS-0001`

## Success Criteria (DoD)

- The repo has one explicit distinction between artifact lifecycle time, semantic effective time, and routing-validity time.
- The contract template has one defended default rule for deriving `effective_from` and `effective_until` without forcing fabricated precision.
- The log template remains narrow and does not grow a second layer of semantic-effective fields by default.
- The lane records whether ledgers should receive bounded `resolution valid from/until` fields now or later.
- The lane records whether transition-window dates should remain deferred until a real multi-release coexistence case appears.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the three-layer time model is explicit;
  - the default contract derivation rule is explicit;
  - the repo knows whether ledger/register template changes are needed now or deferred.
- `stable` for this lane does not require a full repo-wide backfill; it requires the default time semantics and next writeback surfaces to be clear.

## P0 (Contract | v1)

### P0-C1-S1 (Three-layer time semantics fixed | v1)

- The lane must separate `artifact lifecycle time`, `semantic effective time`, and `reader/routing validity time` into distinct meanings.
- Under this rule, logs, contracts, and ledgers should stop pretending one timestamp can answer all three questions.

### P0-C1-S2 (Default derivation rule fixed | v1)

- Unless stronger evidence exists, a first contract release should default `effective_from` to the source log's `created` time.
- Unless a later defended successor exists, `effective_until` should remain `ongoing`.

### P0-C1-S3 (Complex window deferral fixed | v1)

- Transition-window dates should remain deferred until a family actually has multi-release coexistence or fallback behavior.
- Under this rule, single-release families should not open register-window timestamps just to look complete.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0G-5A/P0-C1-S1S3: scaffold time semantics governance lane`
- `S0G-5A/P1-C1-S1S2: write default time semantics into log and contract templates`
- `S0G-5A/P2-C1-S1S2: decide ledger and register template time fields`
- `S0G-5A/P3-C1-S1: demonstrate time semantics on one live sample`

**Branch convention**:

- This slice should stay on `S0G-docs-management-v7` while it remains a bounded docs-management follow-up under the current `S0G` spine.

**Commit discipline (recommended)**:

- Keep model definition, template writeback, template-expansion decision, and sample demonstration separated when practical so later archaeology can see exactly when the repo fixed the default time rule.

## Plan (draft)

### P1 (Template writeback)

- `P1-C1-S1`: write the three-layer time rule into the log template without widening log frontmatter
- `P1-C1-S2`: write the default `effective_from/effective_until` rule into the contract template

### P2 (Ledger/register scope decision)

- `P2-C1-S1`: decide whether support-only ledgers need `resolution valid from/until`
- `P2-C1-S2`: decide whether transition-register templates need stronger window-date guidance now or only later

### P3 (Sample demonstration)

- `P3-C1-S1`: optionally demonstrate the new default rule on one live sample without opening a repo-wide backfill sweep

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: three-layer time semantics fixed
- [x] `P0-C1-S2`: default derivation rule fixed
- [x] `P0-C1-S3`: complex window deferral fixed

### P1 (Template writeback)

- [x] `P1-C1-S1`: write the three-layer time rule into the log template without widening log frontmatter
- [x] `P1-C1-S2`: write the default `effective_from/effective_until` rule into the contract template

### P2 (Ledger/register scope decision)

- [x] `P2-C1-S1`: decide whether support-only ledgers need `resolution valid from/until`
- [x] `P2-C1-S2`: decide whether transition-register templates need stronger window-date guidance now or only later

### P3 (Sample demonstration)

- [ ] `P3-C1-S1`: optionally demonstrate the new default rule on one live sample without opening a repo-wide backfill sweep

## Current Status (recommended)

- `S0G-5A` is now opened as the bounded time-semantics follow-up under the `S0G` spine.
- The model is now fixed at template level for logs and contracts: logs keep artifact lifecycle time, and contracts now own the default semantic effective-time derivation rule.
- `P2` now fixes the bounded template decision: support-only ledgers do not gain default `resolution valid from/until` routing-table columns now, because the existing chronology-audit shape remains sufficient unless one later lane proves otherwise.
- `P2` also fixes the register-side rule: transition-register `valid from/until` and transition-window dates remain coexistence-standing fields only and must not be derived mechanically from contract `effective_from/effective_until`.
- The next concrete step is `P3`: optionally test this rule set on one live sample such as `S0B-2A / S0G-1C / DOC-WORKFLOW-SCRIPTS-0001` without turning it into a repo-wide backfill sweep.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, source anchors, and any later template or sample outputs.
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S3 (time-semantics governance lane scaffolded | 2026-04-23)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/governance/contracts/workflow/scripts/DOC-WORKFLOW-SCRIPTS-0001-taxonomy-and-stable-entrypoint-governance.md`
- expected:
  - open one bounded lane for time semantics before business packets require more complex coexistence handling
  - fix the default three-layer model and low-complexity derivation rule
  - leave template writeback and sample retrofit as later bounded steps
- observed:
  - the lane is opened
  - logs are fixed at `artifact lifecycle time` only
  - contracts are fixed as the default owner of `semantic effective time`, while ledger/register time fields remain explicitly deferred decisions

### P1-C1-S1S2 (time semantics written back into templates | 2026-04-23)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/governance/contracts/_template-contract-record.md`
- expected:
  - write the three-layer time rule into the log template without widening log frontmatter
  - write the default contract `effective_from/effective_until` derivation rule into the contract template
  - leave ledger/register template decisions explicitly deferred to the next bounded phase
- observed:
  - the log template now states that `created`, `updated`, and `reviewed` own artifact lifecycle time only
  - the contract template now states that first releases default `effective_from` to the decisive source log `created` time unless stronger evidence exists
  - the contract template now states that `effective_until` defaults to `ongoing` until one defended successor, replacement, retirement, or explicit end-state exists

### P2-C1-S1S2 (ledger/register time-field decision fixed | 2026-04-23)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  - `docs/logs/_template-support-only-contract-release-ledger.md`
  - `docs/governance/contracts/_template-contract-release-transition-register.md`
  - `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
- expected:
  - decide whether support-only ledgers need default `resolution valid from/until` routing-table fields now
  - decide whether transition-register templates need stronger window-date guidance now or only later
  - keep the decision bounded so `P2` does not trigger one repo-wide sample backfill sweep
- observed:
  - the parent-ledger template now states that the optional chronology-audit surface is sufficient by default and that core routing rows should not gain default `resolution valid from/until` columns now
  - the register template now states that coexistence `valid from/until` dates are register-standing fields and must not be copied mechanically from contract effective-time fields
  - the register template now states that single-release families and non-active historical retention should not open transition-window rows or invented window dates

## Recent changes (for traceability, optional)

- 2026-04-23: opened `S0G-5A` so time semantics can be fixed as one bounded governance lane before the repo is forced into ad hoc timestamp growth across logs, contracts, ledgers, and transition registers.
- 2026-04-23: completed `P1` by writing the three-layer time distinction into the log template and the default effective-time derivation rule into the contract template, while keeping ledger/register time fields deferred for a later bounded decision.
- 2026-04-23: completed `P2` by deciding that support-only ledgers should not gain default routing-validity columns now, while transition registers should carry stronger coexistence-date guidance without inheriting contract effective-time dates mechanically.