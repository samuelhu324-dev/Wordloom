# log-S0E-6F (Phase 6F: issue body metadata and links boundary follow-up)

---

**id**: `S0E-6F`
**kind**: `log`
**title**: `issue body metadata and links boundary follow-up v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Workflow, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_4**: `docs/logs/log-S0E-6E-single-item-context-authoring-and-batch-preserve-boundary.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-02`
**updated**: `2026-04-02`

---

## Decision / Outcome

**Decision**:

- `S0E-6F` exists because the current issue body contract still mixes one navigation field into `Metadata`: `Source log` is rendered as if it were object-state metadata even though it functions as a deterministic navigation link.
- v1 keeps the existing issue section order `Metadata -> Context -> Definition of Done (DoD) -> Links`, but narrows the field boundary inside those sections.
- The immediate contract change is intentionally small and explicit:
  - remove `Source log` from issue `Metadata`;
  - add optional `Previous log` under issue `Links` when the source log declares it.
- This slice does not widen issue bodies to mirror every `reference_log_*` field. The follow-up is specifically about a cleaner separation between state metadata and navigation links.

**Default choices (phase defaults / v1)**:

- `Metadata` should describe issue state and ownership only, such as labels, projects, milestone, and parent issue when present.
- Deterministic navigation rows belong in `Links`, including the canonical source log path.
- `Previous log` is allowed in issue `Links`, but remains optional and must be omitted when the source log does not declare it.
- `reference_log_*` rows remain log-only structure in v1 and should not be projected into issue bodies.
- The same field-allocation rule should apply to both issue creation and issue conclusion bodies so the section boundary stays stable across the lifecycle.

## PR Summary Inputs (optional)

**PR summary bullets**:

- Re-scope issue body field allocation so `Source log` moves out of `Metadata` and back into deterministic `Links`.
- Add optional `Previous log` rendering under issue `Links` without widening issue bodies into a full `reference_log_*` mirror.
- Align generators, conclusion planners, runbook wording, and lifecycle checks to the same narrower metadata-versus-navigation boundary.

**PR checklist source**:

- Default source: reuse this log's checked execution checklist after the field-allocation contract, renderer updates, and representative validation all pass.

**PR links**:

- Log: `docs/logs/log-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
- Runbook: `docs/runbook/run-S0E-log-to-issue-creation.md`

## Constraints

- Do not merge `Metadata` and `Links` into one section; this slice is a field-boundary correction, not a body-family redesign.
- Do not move `Metadata` below `Context` or below `Links`; section order remains owned by the existing issue body contract.
- Do not project `reference_log_*` rows into issue `Links` in v1.
- Do not break existing fail-closed omission rules: optional rows must be omitted when their source metadata is blank.
- Do not let issue creation and issue conclusion drift to different field-allocation rules.

## Scope

- `P0`: define the issue-body field-allocation contract for `Metadata` versus `Links`
- `P1`: implement renderer, planner, gate, and runbook changes for the new field boundary
- `P2`: validate representative creation/conclusion outputs and decide which live issue bodies need reconciliation

## Success Criteria (DoD)

- Issue creation and issue conclusion both stop rendering `Source log` inside `Metadata`.
- Issue `Links` always contain `Log` when the source log path is known.
- Issue `Links` may render `Previous log` only when the source log explicitly carries `links.previous_log`.
- The contract stays narrow: `reference_log_*` remains out of issue bodies.
- Runbook wording, shared renderers, and lifecycle/body-contract checks all describe the same field boundary.

## Stability (what draft means now)

- This log remains `draft` until:
  - the field-allocation contract is fixed in `S0E-2D`, `S0E-2E`, and the shared body-contract owner surfaces;
  - generators and planners are updated to the same rule;
  - representative issue artifacts or live issue samples prove the new boundary without creating fresh body drift.

## Current Status

- `S0E-6F` is now opened as a narrow field-boundary follow-up to `S0E-2D`, `S0E-2E`, `S0E-5D`, and `S0E-6E`.
- The current change target is deliberately small: `Source log` leaves `Metadata`, while optional `Previous log` enters issue `Links`.
- The expected implementation path is already bounded to renderer/planner/runbook/gate updates; this slice is not intended to reopen `Context` ownership or broader section-order debates.

## P0 (Field-allocation contract | v1)

### P0-C1-S1 (Metadata keeps state rows only | v1)

- `Metadata` should keep issue-state rows such as `Labels`, `Projects`, `Milestone`, and `Parent issue` when present.
- `Source log` should no longer appear in `Metadata` because it is a navigation pointer rather than issue state.
- The rule applies to both issue creation and issue conclusion bodies.

### P0-C1-S2 (Links own deterministic navigation rows | v1)

- `Links` should continue to hold deterministic navigation rows such as `Log`, `Issue`, `PR`, `Runbook`, `Roadmap`, and `Parent log` when those rows are already allowed by the owning contract.
- `Previous log` becomes an allowed optional issue-link row when the source log declares `links.previous_log`.
- `Previous log` should be omitted rather than guessed when the source log does not provide it.

### P0-C1-S3 (Boundary stays intentionally narrow | v1)

- `reference_log_*` remains log-only supporting structure in v1.
- This slice does not introduce `Reference log 1`, `Reference log 2`, or similar rows into issue bodies.
- The goal is a cleaner metadata-versus-navigation boundary, not higher issue-body cardinality.

## P1 (Implementation measures | v1)

### P1-C1-S1 (Shared issue-body renderers updated first | v1)

- Update the shared issue rendering helpers and creation/conclusion entrypoints so issue bodies stop emitting `Source log` inside `Metadata`.
- Ensure the same helpers can render optional `Previous log` inside `Links` without affecting PR body families.

### P1-C1-S2 (Gate and verification surfaces aligned | v1)

- Update lifecycle/body-contract checks so `Source log` is no longer expected in issue `Metadata`.
- Allow `Previous log` as an optional deterministic issue-link category where issue links are validated.
- Keep omission semantics fail-closed: absent `Previous log` should not produce placeholder rows.

### P1-C1-S3 (Operator/runbook wording updated | v1)

- Update the runbook and owner logs so manual review instructions match the new field boundary.
- The operator-facing rule should stay simple: state rows in `Metadata`, navigation rows in `Links`.

## P2 (Representative validation and reconciliation | v1)

### P2-C1-S1 (Regenerate representative issue artifacts | v1)

- Re-run representative creation and conclusion samples so the new field boundary is visible in retained artifacts.
- Confirm that `Log` still appears under `Links` and that `Metadata` remains structurally stable after `Source log` removal.

### P2-C1-S2 (Decide live-issue reconciliation scope | v1)

- Audit whether only representative issue bodies need live reconciliation or whether the existing `S0E` family should be normalized in one bounded batch.
- Keep this decision explicit instead of silently rewriting all historical issue bodies under the new micro-contract.

## Execution Checklist (unchecked)

### P0 (Field-allocation contract)

- [ ] `P0-C1-S1`: metadata narrowed to state rows only
- [ ] `P0-C1-S2`: deterministic link ownership clarified
- [ ] `P0-C1-S3`: narrow-boundary non-goals fixed

### P1 (Implementation measures)

- [ ] `P1-C1-S1`: shared issue-body renderers updated first
- [ ] `P1-C1-S2`: gate and verification surfaces aligned
- [ ] `P1-C1-S3`: operator/runbook wording updated

### P2 (Representative validation and reconciliation)

- [ ] `P2-C1-S1`: representative issue artifacts regenerated
- [ ] `P2-C1-S2`: live-issue reconciliation scope decided

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log will record the retained sample paths, validation runs, and any bounded live-reconciliation decisions after implementation starts.

## Recent changes (for traceability, optional)

- 2026-04-02: opened `S0E-6F` to narrow the issue body field boundary without reopening the broader section-order contract.
- 2026-04-02: fixed the v1 target as two explicit moves only: remove `Source log` from issue `Metadata`, and add optional `Previous log` under issue `Links`.
- 2026-04-02: recorded the concrete implementation measures in advance: shared renderer updates first, then gate/runbook alignment, then representative validation plus an explicit live-reconciliation decision.