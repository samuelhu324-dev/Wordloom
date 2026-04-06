# log-S0F-3A (Phase 3A: governance contract index and delta model)

---

**id**: `S0F-3A`
**kind**: `log`
**title**: `governance contract index and delta model v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Governance, Contract, Index, epic/s0, sub/3a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
  **reference_log_1**: `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md`
  **reference_log_2**: `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
  **reference_log_3**: `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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
**created**: `2026-04-06`
**updated**: `2026-04-06`

---

## Decision / Outcome

**Decision**:

- `S0F-3A` opens the next `S0F` follow-up slice for governance-contract concentration: logs remain the event ledger, but current governance contracts must become separately indexable, mechanically traceable, and human-readable.
- v1 treats the current problem as a modeling gap, not as a missing search trick. The repo can often recover chronology from `previous_log`, parent/origin links, retained issue/PR artifacts, and Git history, but it still lacks one explicit surface that answers which governance contracts are currently active and where each one was introduced or changed.
- v1 explicitly avoids overloading the existing DDD `domain` term. The new concentration layer belongs to governance/control-plane concerns, not to application-domain SoT or projection modules.

**Default choices (phase defaults / v1)**:

- Keep logs as event truth. A log may introduce, modify, or retire governance contracts, but a log is not itself the stable contract registry.
- Treat `previous_log` as queue/order semantics only. It should express the direct execution predecessor, not the full causal history.
- Treat `reference_logs` as near-cause or near-contract references only. They should point to the smallest current set of logs needed to explain why this new slice exists or which recent contract changes it inherits.
- Introduce explicit governance-contract records with stable `contract_id` values that are not tied to log IDs.
- Allow any phase or step inside a log to emit governance-contract deltas; do not assume only `P0` or only dedicated contract slices can change contract state.
- Keep the governance-contract layer distinct from application-domain truth (`SoT`, `Projections`, DDD domain modules) and from operational execution surfaces (GitHub Actions, runners, deploy, compose, infra adapters).

## PR Summary Inputs (optional)

**PR summary bullets**:

- Define a dedicated governance-contract concentration model so current active contracts are no longer recoverable only by reading scattered prose across logs.
- Separate event truth, contract delta truth, active contract index truth, and human-readable governance views.
- Clarify the boundary between application domain, governance contracts, and operational surfaces so `domain` is no longer overloaded across unrelated layers.

**PR checklist source**:

- Default source: reuse this log's execution checklist for generated PR checklist blocks.

## Constraints

- Do not collapse governance contracts back into free-form prose only.
- Do not treat Git history as the primary active-contract registry; it is a forensic aid, not the source of current effective state.
- Do not let `reference_logs` become a transitive closure of all ancestry just to compensate for missing contract indexing.
- Do not overload DDD `domain` terminology for repo-governance/control-plane rules.
- Do not require every new log to become a full standalone contract slice before it can make a legitimate contract change.

## Scope

- `P0`: open `S0F-3A`, wire it into the `S0F` spine, and fix the terminology boundary around governance-contract concentration
- `P1`: define the modeling split among event logs, governance-contract deltas, active contract index records, and human-readable governance views
- `P2`: define hard usage rules for `previous_log` versus `reference_logs`
- `P3`: define the minimum machine-readable governance-contract delta block that any phase may emit when it changes contract state
- `P4`: define the minimum active-contract index record shape and naming rules
- `P5`: define backtrace and migration rules so existing scattered governance contracts can be concentrated incrementally without freezing normal slice work

## Success Criteria (DoD)

- One reader can tell within 30 seconds whether a rule belongs to application-domain logic, governance contracts, or operational surfaces.
- One reader can locate the currently active version of a governance contract without manually traversing a long chain of unrelated logs.
- `previous_log` and `reference_logs` have non-overlapping semantics that are stable enough to enforce in future logs/issues.
- The repo has one minimal governance-contract delta model that can be emitted by any relevant phase, not only by special contract-only slices.
- The repo has one minimal active-contract index model that can point back to introduced/last-changed sources without becoming a prose chronicle.
- The migration path explicitly supports partial backfill and incremental concentration rather than demanding a one-shot rewrite of all historical logs.

## Background

- `S0F-1J` and the later `S0F-P1` family patch exposed a recurring contract-traceability problem: the workflow and reviewer behavior can be correct, but the repo still lacks one direct place to answer which governance contract is currently in force and whether a later log phase silently changed that contract.
- `S0F-2B` solved the small-work lane taxonomy around family patch versus ops maintenance, but it did not solve the broader concentration problem for governance contracts themselves.
- The current structure already contains useful evidence sources: `previous_log` chains, parent/origin relationships, retained issue/PR artifacts, audit manifests, and Git history. What is missing is one explicit active-state layer that concentrates current governance contract truth without reverting to long-form v2 narrative prose.
- The repo already uses DDD-style domain modules for application concerns, so a new governance concentration layer must avoid stealing the same `domain` term for a different layer of truth.

## Current Problem Statement

- Governance contracts are currently distributed across many logs and phases. A contract may first appear in `P0`, then receive a meaningful semantic change in `P2`, and later get narrowed again in a family patch or maintenance log.
- Some non-contract-first logs still make real governance-contract changes as part of execution hardening, reviewer semantics, or lifecycle packaging.
- Because logs are event-oriented, current effective contract state is often recoverable only through multi-hop reading, Git archaeology, or mental reconstruction.
- This makes the system traceable in principle but expensive in practice, and it risks turning `reference_logs` into an overloaded ancestry dump instead of keeping them as compact near-cause references.

## Modeling Boundary

- `Application Domain`: product/business truth such as SoT, projections, content state, and other DDD module concerns.
- `Governance Contracts`: repo/self-governance truth such as issue/PR lifecycle rules, reviewer semantics, fail-on-findings policy, patch/maintenance lanes, and other control-plane rules.
- `Operational Surfaces`: execution surfaces such as GitHub Actions workflows, runners, deploy scripts, compose entrypoints, infra adapters, and other environment-facing mechanisms.
- `S0F-3A` belongs to `Governance Contracts`, not to `Application Domain`, and not purely to `Operational Surfaces`.

## P1 Baseline (Truth-layer split)

- `Event Truth`:
  - Lives in logs.
  - Records what happened, why it happened, how the slice advanced, and what evidence was retained.
  - May mention contract changes, but does not by itself serve as the stable registry of current active governance contracts.
- `Change Truth`:
  - Lives in governance-contract delta declarations emitted from a specific phase or step.
  - Records that a governance contract was added, modified, retired, superseded, or explicitly applied without semantic change.
  - Is the smallest machine-readable unit of governance-contract evolution.
- `Current-state Truth`:
  - Lives in active governance-contract index records.
  - Records which governance contracts are currently active, where each one was introduced, where it was most recently changed, what surfaces enforce it, and what violation semantics currently apply.
  - Answers current-state questions without requiring readers to replay a full event history.
- `Human-readable Concentration`:
  - Lives in governance views that explain how a family or governance surface currently works.
  - Summarizes the active-state model for human readers, but does not replace logs as evidence and does not replace the index as the machine-readable source of current effective contract state.

## P1 Consequences

- Logs remain the canonical event ledger and continue to own chronology, execution evidence, and slice-level decisions.
- Governance-contract deltas become the canonical expression of contract change, even when the surrounding log is not a contract-first slice.
- The active governance-contract index becomes the canonical expression of current effective governance state, rather than asking readers to reconstruct that state from scattered prose.
- Governance views become explanation surfaces, not hidden registries; if a view and the index disagree, the index wins for current-state questions and the logs win for historical evidence.
- `P1` does not yet fix the delta schema or the index schema. It only fixes the four truth layers and their ownership boundaries so later phases can design those schemas without re-litigating the model.

## Plan (draft)

### P0 (Slice opening and terminology boundary)

- P0-C1-S1: create `S0F-3A` and wire it into the `S0F` parent spine
- P0-C1-S2: fix the terminology boundary among application domain, governance contracts, and operational surfaces

### P1 (Truth-layer split)

- P1-C1-S1: define logs as event truth
- P1-C1-S2: define governance-contract deltas as change truth
- P1-C1-S3: define active contract index records as current-state truth
- P1-C1-S4: define governance views as human-readable concentration rather than event replay

### P2 (Reference semantics)

- P2-C1-S1: define `previous_log` as direct queue/order predecessor only
- P2-C1-S2: define `reference_logs` as near-cause or near-contract references only
- P2-C1-S3: define escalation rules for cases where too many references are required, signaling missing contract concentration

### P3 (Governance-contract delta block)

- P3-C1-S1: define the minimum machine-readable fields for an `add` delta
- P3-C1-S2: define the minimum machine-readable fields for a `modify` delta
- P3-C1-S3: define the minimum machine-readable fields for `retire`, `supersede`, and `apply-without-change` cases

### P4 (Active contract index)

- P4-C1-S1: define stable `contract_id` naming rules independent of log IDs
- P4-C1-S2: define the minimum index record shape, including `introduced_by`, `last_changed_by`, `status`, and enforcement semantics
- P4-C1-S3: decide the smallest viable home for governance-contract index records and reader-facing views

### P5 (Backtrace and migration)

- P5-C1-S1: define how existing logs are backtraced when no explicit delta block exists yet
- P5-C1-S2: define partial backfill rules so active/high-value contracts can be concentrated first
- P5-C1-S3: define how future non-contract-first logs still declare contract changes without pretending to be contract-only slices

## Execution Checklist (unchecked)

### P0 (Slice opening and terminology boundary)

- [x] `P0-C1-S1`: `S0F-3A` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: terminology boundary among application domain, governance contracts, and operational surfaces fixed

### P1 (Truth-layer split)

- [x] `P1-C1-S1`: logs defined as event truth
- [x] `P1-C1-S2`: governance-contract deltas defined as change truth
- [x] `P1-C1-S3`: active contract index records defined as current-state truth
- [x] `P1-C1-S4`: governance views defined as human-readable concentration

### P2 (Reference semantics)

- [ ] `P2-C1-S1`: `previous_log` semantics narrowed to direct predecessor only
- [ ] `P2-C1-S2`: `reference_logs` semantics narrowed to near-cause and near-contract use only
- [ ] `P2-C1-S3`: escalation rule fixed for over-referenced slices

### P3 (Governance-contract delta block)

- [ ] `P3-C1-S1`: minimum `add` delta fields fixed
- [ ] `P3-C1-S2`: minimum `modify` delta fields fixed
- [ ] `P3-C1-S3`: minimum retire/supersede/apply-only delta fields fixed

### P4 (Active contract index)

- [ ] `P4-C1-S1`: stable `contract_id` naming rules fixed
- [ ] `P4-C1-S2`: minimum active-contract index record shape fixed
- [ ] `P4-C1-S3`: smallest viable home for the index and the reader-facing view fixed

### P5 (Backtrace and migration)

- [ ] `P5-C1-S1`: backtrace rule for historical logs without explicit deltas fixed
- [ ] `P5-C1-S2`: partial backfill rule fixed
- [ ] `P5-C1-S3`: future non-contract-first logs can still declare contract changes cleanly

## Current Status

- `S0F-3A` is now opened as the next `S0F` follow-up slice for concentrating governance-contract truth into an index-plus-delta model instead of leaving active contract state recoverable only from scattered log prose.
- `P0` is now complete: the slice is wired into the `S0F` spine, and the terminology boundary among `Application Domain`, `Governance Contracts`, and `Operational Surfaces` is now fixed as the baseline for later contract-index work.
- `P1` is now complete: the four-layer truth model is fixed. Logs own event truth, delta declarations own change truth, active index records own current-state truth, and governance views own human-readable concentration.
- The slice remains in framing mode beyond `P1`: no final delta schema, index record shape, reference-rule contract, or backfill rule is fixed yet.
- The main design hypothesis is now no longer just implicit prose: current effective governance state should be queried from an index, contract evolution should be expressed through deltas, and historical reconstruction should remain log-owned rather than being overloaded onto `reference_logs` or Git history.

## Evidence

- `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md` shows that materially important contract changes can accumulate across later phases inside one slice, not only at `P0`.
- `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md` shows that later patch work may surface governance-contract ambiguity without being a contract-first slice.
- `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md` shows that stable lane policy can be expressed clearly once its vocabulary and boundaries are concentrated, which motivates doing the same for governance contracts more generally.
- The `P1` baseline in this slice now fixes the ownership split among event truth, change truth, current-state truth, and human-readable concentration so later phases can define schemas without collapsing those roles back together.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-3A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle.