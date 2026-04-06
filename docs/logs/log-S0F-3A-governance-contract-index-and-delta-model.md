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

## P2 Baseline (Reference semantics)

- `previous_log`:
  - Expresses direct queue/order lineage only.
  - Answers one question: which immediately preceding slice or log lane this new log is advancing from.
  - Must not be used as a catch-all causal reference field.
  - Should normally contain exactly one direct predecessor; if there is no meaningful direct predecessor, it may remain blank.
- `reference_logs`:
  - Express near-cause, near-contract, or near-trigger references only.
  - Answer a different question: which recent logs a reader must inspect to understand why this new log exists or which current contract changes it is inheriting, refining, or responding to.
  - Must not be used to enumerate full ancestry, all remotely related logs, or every historical touchpoint in the same family.
  - Should remain a minimal set. If more than three references feel necessary, that is a signal that the missing piece is contract concentration or a governance view, not another larger reference list.
- `parent_log` and `origin_log` remain separate from both fields:
  - `parent_log` answers where the log is structurally housed.
  - `origin_log` answers which family-owned source the patch or follow-up still belongs to.
  - Neither field replaces queue semantics or near-cause semantics.

## P2 Escalation Rule

- If a new log appears to need many `reference_logs` just to be understandable, stop expanding the list and treat that as explicit evidence for missing governance-contract concentration.
- In that case, the follow-up should prefer one of these actions:
  - add or refine a governance view for human-readable concentration,
  - add or refine index records for current active contract state,
  - or open a dedicated follow-up slice to concentrate the missing contract surface.
- The purpose of this escalation rule is to prevent `reference_logs` from degenerating into a transitive ancestry dump.

## P2 Consequences

- A reader can now separate order from cause:
  - read `previous_log` to understand progression order,
  - read `reference_logs` to understand why the current log was opened or which recent contract changes matter.
- Future logs should prefer one clean `previous_log` plus a small, intentional `reference_logs` set over broad genealogy chains.
- When chronology and causality diverge, the two fields may legitimately point to different logs. That is expected under this model and no longer counts as a structural smell by itself.
- `P2` does not yet define machine-readable validation for these fields, but it does fix their meaning tightly enough to guide future authoring and later enforcement.

## P3 Baseline (Governance-contract delta block)

- A governance-contract delta block is the minimum machine-readable declaration that a specific phase or step changed governance-contract state.
- A delta block belongs to one concrete source location such as `S0F-3A/P3-C1-S1` or another phase/step anchor; it is not a free-floating family summary.
- The minimum shared fields for every delta block are:
  - `action`: one of `add`, `modify`, `retire`, `supersede`, or `apply-without-change`
  - `contract_id`: the stable governance-contract identifier being acted on
  - `summary`: one concise sentence describing the effective contract meaning after this delta
  - `rationale`: the local reason this delta exists in this phase or step
  - `source_anchor`: the exact log phase/step that owns the delta
  - `scope`: the governed surface this delta applies to
  - `enforcement_surface`: the workflow, script, runbook, adapter, or manual path that enforces or operationalizes the contract
  - `violation_semantics`: the current intended result when the contract is violated, such as `fail`, `warning`, `report-only`, or `neutral`
- The minimum action-specific fields are:
  - `add`:
    - must include `introduced_by`
    - must not include `supersedes_contract_id` unless the add also acts as a replacement contract under a `supersede` action instead
  - `modify`:
    - must include `changed_from` as a short description of the prior effective meaning being changed
  - `retire`:
    - must include `retired_reason`
  - `supersede`:
    - must include `supersedes_contract_id`
    - must include `replacement_summary`
  - `apply-without-change`:
    - must include `applied_context`
    - must not claim semantic change; it records that an existing contract was used or replayed in this phase without changing its meaning

## P3 Canonical Form

- A delta block should be readable in prose logs but structured enough for later extraction.
- The baseline canonical shape is:

```yaml
contract_delta:
  action: <add|modify|retire|supersede|apply-without-change>
  contract_id: <stable-governance-contract-id>
  summary: <effective contract meaning after this delta>
  rationale: <why this delta exists here>
  source_anchor: <log-id/phase-cycle-step>
  scope: <governed surface>
  enforcement_surface: <workflow|script|runbook|adapter|manual>
  violation_semantics: <fail|warning|report-only|neutral>
  introduced_by: <required for add>
  changed_from: <required for modify>
  retired_reason: <required for retire>
  supersedes_contract_id: <required for supersede>
  replacement_summary: <required for supersede>
  applied_context: <required for apply-without-change>
```

- Fields that do not apply to the chosen `action` should be omitted rather than filled with placeholder prose.

## P3 Consequences

- Any future log phase may now declare contract change explicitly without pretending the whole log is a contract-only slice.
- Later `P4` index records now have a stable minimum input surface to ingest.
- Historical logs without delta blocks are still valid event truth, but future contract changes now have a preferred structured expression that is small enough to add incrementally.
- `P3` does not yet fix extraction tooling or index storage. It only fixes the minimum delta declaration shape and action semantics.

## P4 Baseline (Active contract index)

- `contract_id` naming rules:
  - A `contract_id` names a governance rule, not a log, issue, PR, branch, or implementation artifact.
  - A `contract_id` must remain stable across ordinary wording cleanup, enforcement-surface cleanup, and later log phases unless the contract meaning itself changes materially.
  - The canonical baseline format is uppercase hyphenated segments:
    - `<AREA>-<SUBJECT>-<RULE>`
    - examples: `PR-BODY-LIVE-MATCH-SOURCE-LOG`, `REVIEW-HISTORICAL-DRIFT-REPORT-ONLY`, `PATCH-LANE-FAMILY-OWNED`
  - Segments should describe semantic meaning, not temporary implementation details such as script filenames, run IDs, or slice IDs.
  - If one contract truly replaces another, keep a new `contract_id` and connect the relationship through `supersedes` / `superseded_by` rather than silently reusing the old identifier for a new meaning.

- Minimum active-index record fields:
  - `contract_id`: stable governance-contract identifier
  - `status`: one of `draft`, `active`, `deprecated`, `superseded`, or `retired`
  - `summary`: one concise statement of the current effective contract meaning
  - `governance_area`: the governance surface this contract belongs to
  - `applies_to`: the targets governed by this contract
  - `enforcement_surface`: the workflow, script, runbook, adapter, or manual path that enforces or operationalizes the current contract
  - `violation_semantics`: the current intended result when the contract is violated
  - `introduced_by`: the first known source anchor that introduced this contract
  - `last_changed_by`: the most recent source anchor that changed this contract's meaning
  - `source_refs`: the minimal current source-log references that a reader should inspect for traceability
  - `supersedes`: optional list of earlier contract IDs this record replaces
  - `superseded_by`: optional list of later contract IDs that replaced this one
  - `notes`: optional reader-facing clarifications that do not override the structured fields above

## P4 Canonical Form

- The baseline active-index record shape is:

```yaml
contract_record:
  contract_id: <stable-governance-contract-id>
  status: <draft|active|deprecated|superseded|retired>
  summary: <current effective contract meaning>
  governance_area: <governed area>
  applies_to: <targets governed by this contract>
  enforcement_surface: <workflow|script|runbook|adapter|manual>
  violation_semantics: <fail|warning|report-only|neutral>
  introduced_by: <first source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <minimal source-log reference>
  supersedes:
    - <optional replaced contract id>
  superseded_by:
    - <optional replacement contract id>
  notes:
    - <optional clarification>
```

- The smallest viable home is now fixed as:
  - `docs/governance/contracts/` for active governance-contract index records
  - `docs/governance/views/` for human-readable governance views
- The smallest viable reusable templates are now fixed as:
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/governance/views/_template-governance-view.md`

## P4 Consequences

- Later phases now have both a stable delta input surface and a stable active-state record target.
- Future concentration work no longer needs to invent a new home each time a governance contract is extracted from scattered logs.
- Governance views can stay explanatory because active-state records now have their own explicit home.
- `P4` does not yet backfill historical contracts. It only fixes naming, minimum record shape, and the smallest viable home for index records and views.

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

- [x] `P2-C1-S1`: `previous_log` semantics narrowed to direct predecessor only
- [x] `P2-C1-S2`: `reference_logs` semantics narrowed to near-cause and near-contract use only
- [x] `P2-C1-S3`: escalation rule fixed for over-referenced slices

### P3 (Governance-contract delta block)

- [x] `P3-C1-S1`: minimum `add` delta fields fixed
- [x] `P3-C1-S2`: minimum `modify` delta fields fixed
- [x] `P3-C1-S3`: minimum retire/supersede/apply-only delta fields fixed

### P4 (Active contract index)

- [x] `P4-C1-S1`: stable `contract_id` naming rules fixed
- [x] `P4-C1-S2`: minimum active-contract index record shape fixed
- [x] `P4-C1-S3`: smallest viable home for the index and the reader-facing view fixed

### P5 (Backtrace and migration)

- [ ] `P5-C1-S1`: backtrace rule for historical logs without explicit deltas fixed
- [ ] `P5-C1-S2`: partial backfill rule fixed
- [ ] `P5-C1-S3`: future non-contract-first logs can still declare contract changes cleanly

## Current Status

- `S0F-3A` is now opened as the next `S0F` follow-up slice for concentrating governance-contract truth into an index-plus-delta model instead of leaving active contract state recoverable only from scattered log prose.
- `P0` is now complete: the slice is wired into the `S0F` spine, and the terminology boundary among `Application Domain`, `Governance Contracts`, and `Operational Surfaces` is now fixed as the baseline for later contract-index work.
- `P1` is now complete: the four-layer truth model is fixed. Logs own event truth, delta declarations own change truth, active index records own current-state truth, and governance views own human-readable concentration.
- `P2` is now complete: `previous_log` is fixed as direct queue lineage only, `reference_logs` are fixed as near-cause and near-contract references only, and an explicit escalation rule now stops those references from becoming ancestry dumps.
- `P3` is now complete: the minimum governance-contract delta block is fixed, including one shared field set plus action-specific requirements for `add`, `modify`, `retire`, `supersede`, and `apply-without-change`.
- `P4` is now complete: stable `contract_id` naming rules, the minimum active-index record shape, and the smallest viable homes under `docs/governance/contracts/` and `docs/governance/views/` are now fixed.
- The slice remains in framing mode beyond `P4`: no backfill rule is fixed yet.
- The main design hypothesis is now materially more complete: future governance contracts can be emitted as deltas, concentrated into active-state records, and explained in reader-facing views without collapsing those roles back together.

## Evidence

- `docs/logs/log-S0F-1J-pr-body-completeness-task-and-ci-gate.md` shows that materially important contract changes can accumulate across later phases inside one slice, not only at `P0`.
- `docs/logs/patch/log-S0F-P1-s0f-pr-body-completeness-standard-check-dispatch-failure-triage.md` shows that later patch work may surface governance-contract ambiguity without being a contract-first slice.
- `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md` shows that stable lane policy can be expressed clearly once its vocabulary and boundaries are concentrated, which motivates doing the same for governance contracts more generally.
- The `P1` baseline in this slice now fixes the ownership split among event truth, change truth, current-state truth, and human-readable concentration so later phases can define schemas without collapsing those roles back together.
- The `P2` baseline in this slice now fixes that queue lineage and causal references are different surfaces with different jobs, which reduces pressure to use `reference_logs` as a hidden contract registry.
- The `P3` baseline in this slice now fixes the minimum delta declaration that later phases can ingest into an active index without forcing future authors to invent per-log contract prose formats.
- The `P4` baseline in this slice now fixes both the target record shape and the canonical home for active governance contracts and governance views.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-3A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle.