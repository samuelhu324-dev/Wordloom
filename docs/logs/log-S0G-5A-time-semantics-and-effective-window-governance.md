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
- `P4`: assess which live contracts and corresponding ledger/SUP/log surfaces actually need timeline-evidence backfill next
- `P5`: execute the first upstream-ready time-evidence backfill batch on `S0A-1A`

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

### P4 (Backfill assessment)

- `P4-C1-S1`: classify live contracts into `ready-now`, `upstream-first`, and `defer-no-new-time-evidence-yet` buckets
- `P4-C1-S2`: classify corresponding parent ledgers, SUP packets, and source logs into `already-sufficient`, `needs-upstream-chronology`, and `no-blanket-backfill` buckets

### P5 (First execution batch)

- `P5-C1-S1`: backfill the `S0A-1A` GitHub family contracts from defended upstream chronology
- `P5-C1-S2`: write the `S0A-1A` source-side and screenshot-sharpening distinction back into the parent ledger without opening a new SUP round

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

- [x] `P3-C1-S1`: optionally demonstrate the new default rule on one live sample without opening a repo-wide backfill sweep

### P4 (Backfill assessment)

- [x] `P4-C1-S1`: classify live contracts into `ready-now`, `upstream-first`, and `defer-no-new-time-evidence-yet` buckets
- [x] `P4-C1-S2`: classify corresponding parent ledgers, SUP packets, and source logs into `already-sufficient`, `needs-upstream-chronology`, and `no-blanket-backfill` buckets

### P5 (First execution batch)

- [x] `P5-C1-S1`: backfill the `S0A-1A` GitHub family contracts from defended upstream chronology
- [x] `P5-C1-S2`: write the `S0A-1A` source-side and screenshot-sharpening distinction back into the parent ledger without opening a new SUP round

## Current Status (recommended)

- `S0G-5A` is now opened as the bounded time-semantics follow-up under the `S0G` spine.
- The model is now fixed at template level for logs and contracts: logs keep artifact lifecycle time, and contracts now own the default semantic effective-time derivation rule.
- `P2` now fixes the bounded template decision: support-only ledgers do not gain default `resolution valid from/until` routing-table columns now, because the existing chronology-audit shape remains sufficient unless one later lane proves otherwise.
- `P2` also fixes the register-side rule: transition-register `valid from/until` and transition-window dates remain coexistence-standing fields only and must not be derived mechanically from contract `effective_from/effective_until`.
- `P3` now demonstrates the rule set on `S0B-2A / S0G-1C / DOC-WORKFLOW-SCRIPTS-0001`: source-side rule time stays at `2026-02-13`, parent-ledger write-back stays at `2026-04-23`, and contract effective time now reads `2026-02-13 -> ongoing`.
- The sample deliberately does not open one SUP packet because no stronger later evidence changed the defended source-side anchor; the lane is only applying the default derivation rule to an existing source-owned packet.
- `P4` now fixes the repo-level assessment boundary: the next work is not blanket close-out, but one selective backfill program across live contracts whose upstream source-side chronology is either already sufficient or still missing.
- Current assessment: live contract files under `docs/governance/contracts` still show at least 12 release records with `effective_from: unknown`, so contract-side supplementation is still materially needed beyond the `SCRIPTS-0001` sample.
- Current assessment: ledger/SUP/log supplementation is selective rather than global; some parent ledgers and SUP packets already expose chronology-audit surfaces, while some still lack defended row-level source chronology and must be repaired upstream before corresponding contracts can be backfilled safely.
- `P5` now executes the first upstream-ready batch on `S0A-1A`: the GitHub-Issues parent, Projects child, title child, and tag child now read their semantic start from the defended issue source date `2026-02-06` rather than leaving `effective_from` unknown.
- The `S0A-1A` parent ledger now distinguishes the issue-created source anchor `2026-02-06` from the later screenshot-sharpening observation day `2026-02-12`, so the Projects child can keep one earlier semantic start without pretending the screenshots were the original rule birth.
- The next concrete step is `S0A-2A`: it is the next upstream-ready batch because its parent ledger plus accepted SUP packets already carry chronology surfaces that can drive bounded contract backfill without first reopening `S0B-1A` or `S0B-3A`.

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

### P3-C1-S1 (time semantics demonstrated on the scripts sample | 2026-04-23)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  - `docs/logs/log-S0G-1C-workflow-scripts-family-opening-and-s0b-2a-ledger-consumption.md`
  - `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
  - `docs/governance/contracts/workflow/scripts/DOC-WORKFLOW-SCRIPTS-0001-taxonomy-and-stable-entrypoint-governance.md`
  - `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
- expected:
  - test the default derivation rule on one live packet without one repo-wide backfill sweep
  - show that source-side time, parent-ledger write-back time, and contract effective time remain distinguishable on the same packet
  - record whether one SUP packet is required for this sample or not
- observed:
  - the sample now anchors `DOC-WORKFLOW-SCRIPTS-0001 effective_from` to the decisive source log `S0B-2A` created date `2026-02-13`
  - the parent ledger now records `R01` and `R02` source-side chronology separately from the later 2026-04-23 routing write-back event
  - no SUP packet was needed because the sample did not introduce stronger later evidence; it only applied the defended default derivation rule to an existing source-owned packet

### P4-C1-S1S2 (repo backfill scope assessed | 2026-04-23)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  - `docs/governance/contracts/`
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-SUP-S0A-1A-001-tools-github-issues-projects-and-tags.md`
  - `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  - `docs/logs/support-only/ledger-S0B-1A-tools-labs-and-snapshots.md`
  - `docs/logs/support-only/ledger-S0B-2A-tools-scripts-and-snapshots-management.md`
  - `docs/logs/support-only/ledger-S0B-3A-unified-indices-legacy-taxonomy-and-front-matter.md`
- expected:
  - decide whether live contract files in `docs/governance/contracts` still materially need timeline-evidence supplementation
  - decide whether corresponding parent ledgers, SUP packets, and source logs also need supplementation or are already sufficient
  - produce one bounded execution order for later backfill without starting a blanket repo-wide rewrite
- observed:
  - at least 12 live release contracts under `docs/governance/contracts` still carry `effective_from: unknown`, and many clause-level `first effective at` / `effective from` cells remain `unknown`, so contract-side backfill is still materially required beyond the `SCRIPTS-0001` sample
  - parent ledgers and SUP packets already provide reusable chronology surfaces in several families, including `S0A-1A`, `S0A-2A`, and `S0B-2A`, so those families do not need new template invention before bounded backfill begins
  - some upstream packets remain chronology-incomplete at row level, including `S0B-1A` and `S0B-3A`, so their corresponding contract families should not receive contract-only date backfills before one upstream chronology repair lands first
  - source logs as a class do not need blanket backfill: when a decisive source already has defended `created` or another defended chronology anchor, logs may remain unchanged; additional log work is needed only where the decisive anchor is still missing or stays trapped in issue-only or screenshot-only evidence

### P5-C1-S1S2 (S0A-1A upstream-ready backfill batch executed | 2026-04-23)

- headSha: `pending-post-commit`
- artifacts:
  - `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  - `docs/logs/support-only/ledger-S0A-1A-tools-github-issues-projects-and-tags.md`
  - `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  - `docs/governance/contracts/workflow/github/projects/DOC-WORKFLOW-GITHUB-PROJECTS-0001-project-views-support-execution-priority.md`
  - `docs/governance/contracts/workflow/github/issues/title/DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-issue-title-encodes-level-and-category.md`
  - `docs/governance/contracts/workflow/github/issues/tags/DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-issue-tags-follow-role-based-naming.md`
- expected:
  - execute the first bounded backfill batch on one family whose parent ledger and SUP surfaces are already chronology-capable
  - replace `effective_from: unknown` on the `S0A-1A` GitHub family contracts with one defended upstream source anchor when the source issue already preserves it
  - distinguish the Projects screenshot-sharpening date from the earlier issue-created source date without opening one new SUP round
- observed:
  - the `S0A-1A` GitHub family contracts now anchor their first-release semantic start to the source issue creation date `2026-02-06`
  - the Projects child now keeps the same earlier semantic start while using `2026-02-12` only as the later sharpening date for screenshot-backed readings
  - the parent ledger now records `2026-02-06` as the issue-source record/effective anchor for all four rows, while preserving `2026-02-12` only as the later screenshot observation date for `R02`

## Backfill Assessment (working)

### Contract bucket

- `ready-now after sample precedent exists`: `DOC-WORKFLOW-SCRIPTS-0001` is already backfilled and acts as the positive-control sample.
- `upstream-first before contract backfill`: the `DOC-WORKFLOW-GITHUB-*`, `DOC-WORKFLOW-*`, `DOC-WORKFLOW-LABS-*`, `DOC-WORKFLOW-LOGS-*`, `DOC-WORKFLOW-LIFECYCLE-*`, `DOC-WORKFLOW-RUNBOOK-*`, `DOC-WORKFLOW-ADR-*`, and `DOC-WORKFLOW-LEGACY-LOGS-*` families still need review because their release records remain `effective_from: unknown` and many clause-level times remain `unknown`.
- `do not blanket backfill by file count alone`: family registers and templates are not the current contract-evidence bottleneck; live release contracts are.

### Ledger and SUP bucket

- `already-sufficient carrying surfaces`: `S0A-1A`, `S0A-2A`, and `S0B-2A` already expose `Row Chronology Audit`, `Evidence Time Audit`, or governance-event chronology surfaces that can carry bounded backfill work.
- `needs upstream chronology first`: `S0B-1A` and `S0B-3A` currently show routing and governance chronology but do not yet expose defended row-level source chronology tables, so upstream supplementation is still needed before corresponding contract dates can be backfilled defensibly.
- `SUP is selective, not universal`: open or extend SUP only when later evidence is the actual decisive time anchor or when accepted parent rows must be sharpened; do not open SUP by default for every family.

### Source-log bucket

- `no blanket backfill`: source logs already own `artifact lifecycle time`, and many decisive packets already expose one defended `created` anchor.
- `needs supplementation only when anchor is missing`: if the decisive source-side time is still absent, issue-only, or preserved only in screenshot evidence, repair that source-side anchor first through the parent ledger or SUP path before touching the contract.

## Recent changes (for traceability, optional)

- 2026-04-23: opened `S0G-5A` so time semantics can be fixed as one bounded governance lane before the repo is forced into ad hoc timestamp growth across logs, contracts, ledgers, and transition registers.
- 2026-04-23: completed `P1` by writing the three-layer time distinction into the log template and the default effective-time derivation rule into the contract template, while keeping ledger/register time fields deferred for a later bounded decision.
- 2026-04-23: completed `P2` by deciding that support-only ledgers should not gain default routing-validity columns now, while transition registers should carry stronger coexistence-date guidance without inheriting contract effective-time dates mechanically.
- 2026-04-23: completed `P3` on the scripts sample by proving that the same packet can keep source-side chronology, parent-ledger write-back chronology, and contract effective time aligned without opening a new SUP round.
- 2026-04-23: completed `P4` scope assessment by deciding that contract-side time backfill is still materially needed across live release records, but ledger/SUP/log supplementation should remain selective and upstream-first rather than blanket.
- 2026-04-23: completed `P5` first execution batch on `S0A-1A`, using the defended issue creation date as the upstream semantic start for the GitHub family contracts while keeping the later Projects screenshots as sharpening evidence only.