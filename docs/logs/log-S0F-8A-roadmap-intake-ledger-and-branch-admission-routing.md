# log-S0F-8A (Phase 8A: roadmap intake ledger and branch admission routing)

---

**id**: `S0F-8A`
**kind**: `log`
**title**: `roadmap intake ledger and branch admission routing`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Roadmap, Workflow, Records, epic/s0, sub/8a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/479`
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-7D-ledger-supplement-admission-and-old-log-continuation.md`
  **reference_log_1**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_2**: `docs/logs/log-S0E-3A-roadmap-milestone-log-bridge.md`
  **reference_log_3**: `docs/roadmap/road-template-main-roadmap.md`
  **reference_log_4**: `docs/roadmap/road-001-systems-platform-ops-roadmap.md`
**issue_keyword**: `records`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system`
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
**created**: `2026-04-11`
**updated**: `2026-04-11`

---

## Decision / Outcome

**Decision**:

- `S0F-8A` opens as the bounded follow-up after `S0F-7D` for roadmap-intake routing: the repo now needs one support-only ledger layer that records why new roadmap pressure appears, whether it is actionable now, and how it should route into one roadmap slot, future-capability note, or new branch road.
- This lane exists because the current roadmap/log bridge is already strong enough for admitted child logs, but the repo still lacks one defended intake surface for newly emerged problems such as approval, ownership, permission, and tenant-boundary work discovered during active execution.

**Default choices (phase defaults / v1)**:

- Keep the roadmap as `long-running backbone + admitted convergence points`; do not turn the roadmap body into the mutable inbox for every newly noticed problem.
- Route both `preset-demand` and `system-emergent` pressure through one roadmap-intake ledger before admitting that pressure into a roadmap milestone, future-capability section, or branch road.
- Keep the canonical roadmap/log bridge child-log-first exactly as fixed in `S0E-3A`; this lane adds one pre-bridge intake layer and does not replace `M*-P* -> child log` ownership.
- Prefer one support-only ledger per source-log and target-road pair, named as `ledger-<source-log-id>-road-<road-id>-<summary>.md`, so the route remains explicit about where the pressure surfaced and which roadmap it is trying to influence.
- Do not force phase logs themselves into heavy table form by default; use the intake ledger for repeating row-wise routing state, while the phase log retains lane boundary, naming contract, decisions, and evidence.

## Problem Statement

- The current roadmap model already handles admitted work well: roadmap files own milestone language and bridge ledgers, while child logs own implementation and evidence.
- The missing layer appears earlier than admission: active logs now keep surfacing new unresolved questions that are important but not always actionable immediately, such as approval ownership, actor authority, permission boundaries, or tenant semantics.
- If those questions are written only into ad hoc discussion or scattered log prose, the repo loses `why this roadmap pressure exists`, `why it is not admitted yet`, and `what should reopen it later`.
- The repo therefore needs one bounded intake/routing layer that answers four questions before roadmap admission:
  - where the new pressure surfaced
  - whether the pressure is actionable now
  - whether it belongs in an existing roadmap slot, future-capability note, or new branch road
  - which child log should own execution once the pressure is admitted

## Exported Sections / Outlet Ownership

- This slice starts as one `contract + support-only ledger + log-retained core` lane.
- The expected landing is one reusable roadmap-intake ledger model, one first source-log-to-road pilot, and one explicit routing rule between intake rows, roadmap admission, and child-log execution.

**Outlet ownership**:

- `contract`: no-op by default; this lane should first fix the intake-ledger routing contract before emitting any family-owned contract body
- `runbook`: no-op by default; operator procedure should wait until the intake model and first pilot are stable
- `view`: no-op by default; reader projection is not the first missing boundary here
- `index/front-door`: no-op by default; front-door mutations should wait until the intake layer is proven on a real pilot
- `disposition/placement`: support-only ledger is the expected landing for the mutable intake rows
- `log-retained core`: expected landing surface for the lane boundary, naming rules, routing rules, pilot decisions, and evidence

## Definitions (optional)

- `roadmap intake pressure`: a newly identified problem, demand, or boundary question that may need to influence a roadmap but is not yet admitted into one roadmap slot.
- `preset-demand`: roadmap pressure that comes from an already-intended external target such as market demand, role targeting, or a planned capability gap.
- `system-emergent`: roadmap pressure that appears while executing current work, such as governance, approval, ownership, permission, or tenant questions exposed by implementation.
- `intake ledger`: one support-only ledger that records intake rows, actionability, route decisions, and later execution handoff.
- `source-log id`: the exact log id where the new pressure surfaced first, such as `S0F-7D`.
- `target road id`: the exact roadmap family identifier the pressure is attempting to influence, such as `002` for `road-002`.
- `route decision`: the current decision for one intake row, such as `existing-roadmap-slot`, `future-capability`, `new-branch-road`, `log-only`, or `defer`.
- `admission write-back`: the bounded write-back from one intake row into a roadmap note, branch-road opening, or child-log launch once the route is accepted.

## Constraints

- Do not overload the roadmap body with mutable intake state; admitted roadmap notes should stay compact and reader-facing.
- Do not overload child logs with backlog-memory duties for every newly surfaced but not-yet-admitted problem.
- Do not infer intake routing from prose-only notes; the mutable row state should live in the support-only intake ledger.
- Do not require strong table structure in every phase log; table-heavy row state belongs in the intake ledger or later outlets.
- Do not let the intake ledger replace the existing child-log-first roadmap bridge; intake rows decide admission, but admitted execution still routes through child logs.

## Scope

- `P0`: open `S0F-8A`, fix why roadmap-intake routing is a separate layer after `S0E-3A` and `S0F-7D`, and state the high-level ownership split among roadmap, intake ledger, and child log
- `P1`: define the roadmap-intake ledger naming rule, minimum header, row contract, and allowed route decisions
- `P2`: pilot the first source-log-to-road intake ledger, expected first on pressure surfaced during `S0F-7D` and routed toward `road-002`
- `P3`: define the write-back rule from intake rows into roadmap notes, future-capability notes, branch-road openings, and child-log execution starts
- `P4`: reserve any later collaboration-specific enrichment such as multi-owner assignment, approval fields, or outlet revision only if the first intake pilot proves the minimal routing layer insufficient

## Success Criteria (DoD)

- The repo has one explicit rule that roadmap pressure must pass through an intake ledger before it mutates roadmap structure.
- The repo has one reusable naming and row contract for `ledger-<source-log-id>-road-<road-id>-<summary>.md`.
- The repo has one first real pilot showing how a pressure surfaced in one source log can remain remembered, deferred, or admitted without polluting the roadmap body.
- The repo has one explicit write-back rule from intake row to roadmap note and then to child-log execution.
- The repo preserves the existing `S0E-3A` child-log-first roadmap bridge instead of replacing it with roadmap-intake prose.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the intake-ledger model, first pilot, and admission write-back boundary;
  - any broader team-collaboration enrichment has either been explicitly deferred or opened as a separate bounded follow-up rather than left implicit here.

## P0 (Lane boundary | v1)

### P0-C1-S1 (Roadmap-intake layer opened after the existing roadmap bridge | v1)

- `S0F-8A` now opens the missing pre-bridge layer between `newly surfaced problem` and `admitted roadmap slot`.
- Under this rule:
  - `roadmap` keeps long-running backbone and admitted convergence points
  - `intake ledger` keeps mutable discovery and routing state
  - `child log` keeps admitted execution and evidence

### P0-C1-S2 (Three-surface ownership split fixed | v1)

- The ownership split is now fixed as:
  - roadmap = stable direction, convergence, and admitted capability language
  - intake ledger = mutable pressure memory, actionability, and route decision
  - child log = concrete execution once admitted
- Under this rule, newly surfaced problems should not jump directly from prose discussion into roadmap edits without first being recorded in the intake surface.

## P1 (Roadmap-intake ledger model | v1)

### P1-C1-S1 (Intake-ledger naming fixed | v1)

- A roadmap-intake ledger must now be named as `ledger-<source-log-id>-road-<road-id>-<summary>.md`.
- Under this rule:
  - `ledger-S0F-7D-road-002-<summary>.md` means the pressure surfaced during `S0F-7D` and is being routed toward `road-002`
  - the file name records both the discovery origin and the target roadmap family
  - the ledger remains support-only until a later admission write-back lands elsewhere

### P1-C1-S2 (Minimum intake-ledger header and row contract fixed | v1)

- The minimum intake-ledger header is now fixed as:
  - `ledger_id`
  - `ledger_kind`
  - `status`
  - `source_log_id`
  - `source_log_ref`
  - `target_road_id`
  - `target_road_ref`
  - `routing_scope`
  - `routing_goal`
- The minimum intake-row contract is now fixed as:
  - `intake id`
  - `trigger type`
  - `trigger source`
  - `problem statement`
  - `why now`
  - `current actionability`
  - `blocking reason`
  - `proposed route`
  - `target slot or road`
  - `execution log`
  - `status`
  - `notes`

### P1-C1-S3 (Allowed routing values and admission boundary fixed | v1)

- Allowed `trigger type` values are now fixed as:
  - `preset-demand`
  - `system-emergent`
  - `collaboration-gap`
  - `governance-gap`
- Allowed `current actionability` values are now fixed as:
  - `actionable-now`
  - `needs-prereq`
  - `defer`
  - `out-of-scope`
- Allowed `proposed route` values are now fixed as:
  - `existing-roadmap-slot`
  - `future-capability`
  - `new-branch-road`
  - `log-only`
  - `defer`
- Under this rule:
  - the intake ledger may record and route pressure
  - the intake ledger may not claim admitted roadmap ownership by itself
  - any roadmap change or child-log launch must happen through explicit admission write-back

## Plan (draft)

### P1 (Roadmap-intake ledger model)

- `P1-C1-S1`: define the `ledger-<source-log-id>-road-<road-id>-<summary>.md` naming rule
- `P1-C1-S2`: define the minimum intake-ledger header and row contract
- `P1-C1-S3`: define allowed trigger, actionability, and route values plus the admission boundary

### P2 (First pilot)

- `P2-C1-S1`: open the first intake-ledger pilot from `S0F-7D` toward `road-002`
- `P2-C1-S2`: record the first emergent governance-pressure rows around approval, ownership, permission, and tenant-boundary follow-up

### P3 (Admission write-back)

- `P3-C1-S1`: define the minimum write-back from intake row to roadmap note or future-capability note
- `P3-C1-S2`: define when one admitted intake row should open a new child log versus a new branch road

## Execution Checklist (unchecked)

### P0 (Lane boundary)

- [x] `P0-C1-S1`: roadmap-intake layer opened after the existing roadmap bridge
- [x] `P0-C1-S2`: three-surface ownership split fixed

### P1 (Roadmap-intake ledger model)

- [x] `P1-C1-S1`: intake-ledger naming fixed
- [x] `P1-C1-S2`: minimum intake-ledger header and row contract fixed
- [x] `P1-C1-S3`: allowed routing values and admission boundary fixed

### P2 (First pilot)

- [ ] `P2-C1-S1`: first `S0F-7D -> road-002` intake-ledger pilot opened
- [ ] `P2-C1-S2`: first emergent governance-pressure rows recorded

### P3 (Admission write-back)

- [ ] `P3-C1-S1`: intake-row to roadmap-note write-back rule fixed
- [ ] `P3-C1-S2`: child-log versus branch-road opening rule fixed

## Current Status (recommended)

- `S0F-8A` is now opened as the missing roadmap-intake routing lane after the existing `S0E-3A` roadmap bridge and the `S0F-7D` supplement-ledger practice.
- The naming rule for roadmap-intake ledgers is now fixed as `ledger-<source-log-id>-road-<road-id>-<summary>.md`, but no first pilot ledger has been opened yet.
- The next immediate work is `P2`: create the first `S0F-7D -> road-002` intake ledger and record the first emergent rows for approval, ownership, permission, and tenant-boundary pressure.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records head SHA, key parameters, and artifact paths once real pilot routing begins.
- This scaffold intentionally has no execution artifact yet because `P2` has not opened the first intake-ledger pilot.

## Recent changes (for traceability, optional)

- 2026-04-11: opened `S0F-8A` to define the missing roadmap-intake layer between `newly surfaced problem` and `admitted roadmap slot`, with `S0F-7D` as the first expected pilot origin.