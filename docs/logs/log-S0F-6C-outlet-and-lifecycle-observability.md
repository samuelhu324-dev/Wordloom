# log-S0F-6C (Phase 6C: outlet and lifecycle observability)

---

**id**: `S0F-6C`
**kind**: `log`
**title**: `outlet and lifecycle observability v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Records, Views, Workflow, Lifecycle, Observability, epic/s0, sub/6c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  **reference_log_1**: `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  **reference_log_2**: `docs/logs/log-S0F-5A-stable-first-close-out-protocol-and-post-stable-outlet-export.md`
  **reference_log_3**: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`
  **reference_log_4**: `docs/governance/INDEX.md`
  **reference_log_5**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_6**: `docs/governance/views/view-old-s0-migration-ledger-v1.md`
**issue_keyword**: `view`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/6`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-09`
**updated**: `2026-04-09`

---

## Decision / Outcome

**Decision**:

- `S0F-6C` opens as a new bounded `view` lane for outlet and lifecycle observability.
- This slice is intentionally not another widening cycle inside `S0F-6B`.
- `S0F-6B` already answers old-`S0` absorption readability; `S0F-6C` answers a different reader question: what has moved through the current docs/GitHub lifecycle, which outlet each item has reached, where it stopped, and why.
- The first job of this slice is to define one reader-facing observability model that stays separate from:
  - current rule contracts such as `COMPL` and `WF`
  - support-only mutable execution ledgers
  - old-`S0` historical absorption views
- `P1` is now complete: the observability lane now has one explicit two-layer reader split and one minimum reader-facing vocabulary for lifecycle stage, standing, outlet result, stop reason, and next owner.

**Default choices (phase defaults / v1)**:

- Treat `lifecycle observability` and `outlet observability` as reader-facing `view` work, not as contract mutation by default.
- Keep current rule ownership in existing contracts and front doors; this slice summarizes execution state and routing rather than redefining the rules.
- Prefer one layered reader split over one giant mixed tracker:
  - overview for totals and distribution
  - detail for per-item stage, outlet, reason, and next owner
- Keep mutable operator-only reasoning out of the reader-facing view unless it is needed to explain a stable reader-visible stop reason.
- Keep `COMPL` stage ownership and `WF` handling semantics readable through current contracts; `S0F-6C` may summarize those states, but it must not replace their rule vocabulary with a second current contract.

## Problem Statement

- The repo now has current contracts for lifecycle completeness and workflow failure handling, and it has reader-facing views for old-`S0` migration and history.
- What it still lacks is one reader-facing surface for questions such as:
  - which issues or slices have gone through the publish/outlet flow
  - what current lifecycle stage each item has reached
  - which outlet currently owns the reader-facing result
  - why a given item stopped, deferred, or remained `no-op`
  - whether the current split between `contract`, `runbook`, `view`, `index/front-door`, `disposition/placement`, and retained log is actually producing readable results
- Without this layer, the repo can express the rules and preserve the history, but a reader still cannot observe current execution flow and outlet distribution as one bounded story.

## PR Summary Inputs (optional)

- Use this block because `S0F-6C` is expected to define the first reader-facing observability lane for lifecycle stage and outlet routing.

**PR summary bullets**:

- Define the bounded reader-facing observability split for lifecycle stage, outlet ownership, stop reason, and next-owner routing.
- Separate current observability views from both rule contracts and support-only execution ledgers.
- Sequence the first publish set as overview-first and then per-item detail rather than one mixed tracker.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the observability lane.

**PR links**:

- Log: `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
- Previous log: `docs/logs/log-S0F-6B-old-s0-absorption-coverage-and-history-chain-views.md`

## Exported Sections / Outlet Ownership

- This slice is expected to define reader-facing observability views and does not reopen current contract text by default.

**Outlet ownership**:

- `contract`: no-op for now; existing lifecycle and workflow contracts remain the current rule owners unless `S0F-6C` later proves a contract gap rather than a visibility gap
- `runbook`: no-op for now; this slice starts from reader observability rather than operator procedure
- `view`: planned; this slice is expected to land one overview observability surface and one bounded detail surface or defended equivalent
- `index/front-door`: no-op for now; broader front-door mutation should wait until the first observability surfaces prove stable reader value
- `disposition/placement`: no-op for now; mutable support-only placement and cleanup standing remain outside this reader-facing lane
- `log-retained core`: keep this source log for the observability contract, field boundaries, routing rationale, and close-out decision

## Definitions (optional)

- **lifecycle stage**: the current bounded execution position of one item across creation, publish, verify, remediation, close-out, or equivalent defended stages
- **outlet status**: the current answer to whether a given item emitted `contract`, `runbook`, `view`, `index/front-door`, `disposition/placement`, retained-log-only, or justified `no-op`
- **stop reason**: one concise reader-facing explanation of why the item has not advanced further yet
- **next owner**: the current best defended surface or actor that must move the item forward
- **observability overview**: one aggregate-first reader surface answering totals, distribution, and stage/outlet mix
- **observability detail**: one bounded per-item reader surface answering current stage, outlet result, stop reason, and next-owner routing

## Constraints

- Do not turn this slice into a second support-only workflow ledger.
- Do not reopen `S0F-6B` historical absorption scope just to answer current lifecycle visibility questions.
- Do not duplicate contract rule bodies from `COMPL`, `WF`, or other current contracts inside the observability views.
- Do not collapse `no-op`, `not started`, `blocked`, `manual`, `replayable`, and `complete` into one generic status bucket.
- Do not require readers to reconstruct lifecycle flow from raw issue, PR, and retained-log paths alone.

## Scope

- `P0`: open `S0F-6C`, wire it into the parent spine, and fix the problem as one bounded observability `view` lane
- `P1`: define the reader-facing observability split and the minimum field vocabulary for lifecycle stage, outlet result, stop reason, and next owner
- `P2`: land one overview observability `view` for totals, stage distribution, and outlet distribution
- `P3`: land one bounded detail `view` or defended equivalent for per-item lifecycle and outlet standing
- `P4`: fix reader routing between current contracts, overview, detail, and retained source logs, then complete stable close-out review

## Success Criteria (DoD)

- One reader can answer which current items have entered the lifecycle/outlet flow without replaying raw source logs.
- One reader can answer the current stage distribution of those items.
- One reader can answer which outlet each item has reached, or whether the defended answer is `no-op` or retained-log-only.
- One reader can answer why a given item stopped and which owner or surface should be opened next.
- One reader can distinguish current observability from historical absorption and from contract rule ownership.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the observability split is explicit enough to reuse
  - the minimum reader-facing field vocabulary is explicit enough to apply consistently
  - at least one overview surface and one bounded detail surface are landed or explicitly held as the defended minimal publish set
  - later lifecycle/outlet work no longer needs to improvise whether current status belongs in contracts, support-only ledgers, retained logs, or new reader-facing views

## P0 (Contract | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-6C` is now opened as the bounded outlet and lifecycle observability lane.
- This slice does not start by mutating contracts or by reusing `S0F-6B` as a catch-all visibility bucket.
- It starts by fixing the missing reader-facing layer for current execution flow and outlet distribution.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now:
  - define the observability split
  - define the minimum reader-facing field vocabulary
  - decide the first bounded publish set for overview and per-item detail

## P1 (Observability split and field vocabulary | v1)

### P1-C1-S1 (Layered reader split fixed | v1)

- The observability lane is now fixed as two distinct reader-facing jobs rather than one giant mixed tracker:
  - `observability overview`:
    - answers `which bounded items have entered the current lifecycle/outlet flow at all?`
    - answers `how do those items distribute across lifecycle stage, outlet result, and defended standing?`
    - stays aggregate-first and should not require replaying one row per item
  - `observability detail`:
    - answers `for one bounded item, what is its current lifecycle stage, standing, outlet result, stop reason, and next owner?`
    - answers `which current contract, view, or retained log should I open next for this item?`
    - stays per-item and population-bounded rather than whole-repo tracker first
- The two reader jobs are intentionally separated because they answer different questions:
  - overview is for distribution and coverage
  - detail is for bounded per-item diagnosis and routing
- Current contracts remain the rule owners for `what the lifecycle semantics mean`:
  - use `COMPL` for stage-owned completeness meaning across `creation`, `pr`, and `conclusion`
  - use `WF` for publish-verify-remediation handling semantics such as `blocked`, `replayable`, `manual`, and `reconciliation`
- `S0F-6C` therefore fixes the reader split as:
  - contracts say `what the rule is`
  - overview says `how current items distribute`
  - detail says `where this item stands now and what to open next`
  - retained source logs keep deep chronology and evidence

### P1-C1-S2 (Minimum reader-facing vocabulary fixed | v1)

- The minimum reader-facing vocabulary is now fixed as five coordinated fields rather than one overloaded status column:
  - `lifecycle stage`
  - `lifecycle standing`
  - `outlet result`
  - `stop reason`
  - `next owner`
- `lifecycle stage` answers which bounded stage currently owns the item's live question:
  - `creation`
  - `pr`
  - `conclusion`
  - `cross-stage`
  - `closed`
- `lifecycle standing` answers the current execution posture inside that stage without replacing current rule contracts:
  - `not-started`
  - `in-progress`
  - `blocked`
  - `replayable`
  - `manual`
  - `complete`
  - `no-op`
- `outlet result` answers the best defended current reader-facing publication outcome:
  - `contract`
  - `runbook`
  - `view`
  - `index/front-door`
  - `disposition/placement`
  - `retained-log-only`
  - `no-op`
- `stop reason` is now fixed as low-cardinality reader-facing consequence language rather than free-form blocker prose:
  - `not-entered`
  - `stage-work-in-progress`
  - `awaiting-upstream-rule`
  - `awaiting-reader-surface`
  - `awaiting-manual-action`
  - `awaiting-replay-or-remediation`
  - `explicit-no-op`
  - `completed`
- `next owner` answers the current best defended next-open surface or actor:
  - active current contract
  - active reader-facing view
  - retained source-owner log
  - support-only execution ledger when mutable operator work is the real next step
  - manual actor when the next move is intentionally not automated
- Field-boundary rules are now fixed as follows:
  - `lifecycle stage` is reader-facing stage location, not a hidden replay pipeline step counter
  - `lifecycle standing` may reuse current contract semantics, but it must not invent contradictory stage outcomes
  - `outlet result` records where current reader-visible value landed, not every file touched historically
  - `stop reason` stays concise and consequence-first; it must not become a support-only blocker diary
  - `next owner` must point to the narrowest defended current owner rather than a vague area label
- This vocabulary is intentionally reader-facing:
  - it lets readers see where an item stands now
  - it keeps the full operator mutation story in support-only ledgers and retained logs when that deeper execution history is still needed

## Plan (draft)

### P1 (Observability split and field vocabulary)

- `P1-C1-S1`: fix the layered reader split for overview and per-item detail
- `P1-C1-S2`: fix the minimum reader-facing field vocabulary for lifecycle stage, outlet result, stop reason, and next owner

### P2 (Overview observability)

- `P2-C1-S1`: define the minimum field set for aggregate lifecycle and outlet observability
- `P2-C1-S2`: land the first bounded overview observability surface

### P3 (Per-item detail)

- `P3-C1-S1`: define the per-item detail field set and bounded population rule
- `P3-C1-S2`: land the first bounded detail observability surface or defended equivalent

### P4 (Routing and close-out)

- `P4-C1-S1`: fix reader routing among current contracts, observability overview, observability detail, and retained logs
- `P4-C1-S2`: complete stable close-out review for the observability lane

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Observability split and field vocabulary)

- [x] `P1-C1-S1`: observability split fixed
- [x] `P1-C1-S2`: minimum field vocabulary fixed

### P2 (Overview observability)

- [ ] `P2-C1-S1`: overview field set fixed
- [ ] `P2-C1-S2`: first bounded overview surface landed

### P3 (Per-item detail)

- [ ] `P3-C1-S1`: detail field set and bounded population rule fixed
- [ ] `P3-C1-S2`: first bounded detail surface landed

### P4 (Routing and close-out)

- [ ] `P4-C1-S1`: reader routing fixed
- [ ] `P4-C1-S2`: stable close-out review completed

## Current Status (recommended)

- `S0F-6C` is now opened as the bounded follow-up for outlet and lifecycle observability.
- `P0` is now complete: the problem is fixed as a missing reader-facing visibility lane rather than as another `S0F-6B` widening cycle.
- `P1` is now complete: the observability split is explicit across `overview` and `detail`, and the minimum reader-facing vocabulary is now fixed across `lifecycle stage`, `lifecycle standing`, `outlet result`, `stop reason`, and `next owner`.
- `P2` through `P4` remain open.
- The next implementation step is to define the first overview field set and land the first bounded aggregate observability surface before any per-item detail table is widened.

## Evidence (reserved)

### P0-C1-S1S2 (S0F-6C scaffold and immediate sequencing landed | 2026-04-09)

- headSha: `<pending commit for S0F-6C/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo has one explicit lane for reader-facing lifecycle and outlet observability
  - later work no longer needs to improvise whether current status visibility belongs in old-`S0` history views, contracts, or support-only ledgers
- observed:
  - `S0F-6C` is now opened as the bounded observability `view` lane for current lifecycle stage and outlet distribution
  - the immediate next work is now the observability split and field vocabulary rather than direct table proliferation

### P1-C1-S1S2 (Observability split and minimum reader-facing vocabulary fixed | 2026-04-09)

- headSha: `<pending commit for S0F-6C/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-6C-outlet-and-lifecycle-observability.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - later overview and detail observability surfaces should inherit one fixed reader split instead of improvising one mixed tracker
  - later per-item observability rows should use one bounded reader-facing vocabulary instead of mixing contract semantics, support-only statuses, and ad hoc prose
- observed:
  - the observability lane is now fixed as `overview` plus `detail`, with current contracts and retained logs left in their existing owner roles
  - the minimum reader-facing vocabulary is now fixed across `lifecycle stage`, `lifecycle standing`, `outlet result`, `stop reason`, and `next owner`
  - later `P2` and `P3` work can now define field sets and first bounded surfaces without reopening these boundary questions first

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-6C` as the bounded follow-up for outlet and lifecycle observability after concluding that `S0F-6B` itself was already complete within its own historical absorption boundary.
- 2026-04-09: completed `P1` by fixing the two-layer observability split and the minimum reader-facing vocabulary for lifecycle stage, lifecycle standing, outlet result, stop reason, and next owner.