# log-S0E-6F (Phase 6F: issue body metadata and links boundary follow-up)

---

**id**: `S0E-6F`
**kind**: `log`
**title**: `issue body metadata and links boundary follow-up v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Issues, Workflow, Automation, Contract, Formatting, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/331`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/343`
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
- The follow-up now also fixes the parent-versus-child body split that became visible once the narrower field boundary stabilized:
  - top-level parent issues omit `Parent issue` from `Metadata` and omit `Parent log` from `Links`;
  - top-level parent issue `Definition of Done (DoD)` becomes the ordered child-issue short-ref ledger rather than a merged-PR ledger;
  - optional `Roadmap` belongs in issue `Links` for both parent and child issues when the source log declares it.
- This slice does not widen issue bodies to mirror every `reference_log_*` field. The follow-up is specifically about a cleaner separation between state metadata and navigation links.

**Default choices (phase defaults / v1)**:

- `Metadata` should describe issue state and ownership only, such as labels, projects, milestone, and parent issue when present.
- Deterministic navigation rows belong in `Links`, including the canonical source log path.
- Top-level parent issues still use the same section order, but they omit `Parent issue` and `Parent log` because those rows describe child ownership rather than parent ownership.
- Top-level parent issues keep `Definition of Done (DoD)` as the child-issue short-ref ledger, while child issues continue to use merged PR short refs at conclusion time.
- `Previous log` is allowed in issue `Links`, but remains optional and must be omitted when the source log does not declare it.
- `Roadmap` is an allowed optional issue-link row for both parent and child issues and must be omitted when the source log does not declare it.
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
- `P3`: extend the issue-body contract from child-only normalization into an explicit parent-versus-child body family and refresh the governed `S0E` parent-plus-child set

## Success Criteria (DoD)

- Issue creation and issue conclusion both stop rendering `Source log` inside `Metadata`.
- Issue `Links` always contain `Log` when the source log path is known.
- Issue `Links` may render `Previous log` only when the source log explicitly carries `links.previous_log`.
- Optional `Roadmap` can appear in `Links` for both parent and child issues when the source log declares it.
- Top-level parent issues omit `Parent issue` from `Metadata`, omit `Parent log` from `Links`, and render the child issue ledger in `Definition of Done (DoD)`.
- The contract stays narrow: `reference_log_*` remains out of issue bodies.
- Runbook wording, shared renderers, and lifecycle/body-contract checks all describe the same field boundary.

## Stability (what draft means now)

- This log can be marked `stable` when:
  - the field-allocation contract is fixed in `S0E-2D`, `S0E-2E`, and the shared body-contract owner surfaces;
  - generators and planners are updated to the same rule;
  - representative issue artifacts prove the new boundary locally;
  - the bounded live reconciliation decision is explicit and the chosen live sample set verifies cleanly.

## Current Status

- `S0E-6F` is now opened as a narrow field-boundary follow-up to `S0E-2D`, `S0E-2E`, `S0E-5D`, and `S0E-6E`.
- `P0` is now completed: the field-allocation contract is fixed as `Metadata = state rows only`, `Links = deterministic navigation rows`, with `reference_log_*` explicitly left out.
- `P1` is now completed: issue draft rendering, issue conclusion preview rendering, lifecycle audit link validation, and operator/runbook wording are now aligned to the same boundary.
- `P2` is now completed: representative creation/conclusion artifacts have been regenerated, the live reconciliation scope has been fixed as the current `10` closed `S0E` child issues only, and that bounded batch now re-audits cleanly.
- `P3` is now completed: the parent-versus-child body-family split is explicit, the top-level parent issue `#248` has been refreshed in place to the new parent body shape, and the full `11`-item `S0E` parent-plus-child audit now passes.
- `#248` was intentionally excluded from `6F/P2` as a pre-contract parent body, but is now covered by the new `6F/P3` parent-aware follow-up.
- `S0E-6F` is now `stable`: the contract, implementation, representative artifacts, bounded child refresh, parent refresh, and post-refresh parent-plus-child lifecycle audit all agree on the same issue-body family boundary.

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
- The chosen `6F/P2` scope is the current `10` closed `S0E` child issues `#288/#289/#293/#295/#297/#300/#303/#305/#307/#309`.
- The open top-level parent issue `#248` is excluded because it belongs to an older pre-contract body shape and would require a separate parent-issue normalization decision.

## P3 (Parent-versus-child issue body family and live refresh | v1)

### P3-C1-S1 (Parent issue body owns a different DoD lane | v1)

- Top-level parent issues keep the canonical issue section order but do not reuse the child-issue ownership rows mechanically.
- `Metadata` omits `Parent issue` for top-level parent issues.
- `Definition of Done (DoD)` on a top-level parent issue is the ordered child-issue short-ref ledger, not a merged-PR ledger.

### P3-C1-S2 (Parent and child links share one deterministic link family | v1)

- `Log` remains mandatory when the source log path is known.
- `Roadmap` is now an allowed optional issue-link row for both parent and child issues when the source log declares it.
- Top-level parent issues omit `Parent log`, while child issues may continue to render `Parent log` and optional `Previous log`.

### P3-C2-S1 (Renderer and audit surfaces become parent-aware | v1)

- Issue draft rendering now derives top-level parent `Definition of Done (DoD)` rows from the known child issue ledger.
- Lifecycle audit now distinguishes top-level parent issue checks from child issue checks instead of applying child-only PR-ledger assumptions to every issue body.

### P3-C2-S2 (Refresh the governed S0E parent-plus-child set | v1)

- Regenerate a representative top-level parent artifact for `S0E-docs-management-v5`.
- Refresh the live top-level parent issue `#248` to the new parent body shape.
- Re-audit the governed `S0E` family as one `11`-item parent-plus-child set so the parent/child split is verified together.

## Execution Checklist (unchecked)

### P0 (Field-allocation contract)

- [x] `P0-C1-S1`: metadata narrowed to state rows only
- [x] `P0-C1-S2`: deterministic link ownership clarified
- [x] `P0-C1-S3`: narrow-boundary non-goals fixed

### P1 (Implementation measures)

- [x] `P1-C1-S1`: shared issue-body renderers updated first
- [x] `P1-C1-S2`: gate and verification surfaces aligned
- [x] `P1-C1-S3`: operator/runbook wording updated

### P2 (Representative validation and reconciliation)

- [x] `P2-C1-S1`: representative issue artifacts regenerated
- [x] `P2-C1-S2`: live-issue reconciliation scope decided

### P3 (Parent-versus-child issue body family and live refresh)

- [x] `P3-C1-S1`: parent issue DoD ownership lane fixed
- [x] `P3-C1-S2`: parent and child deterministic link family aligned
- [x] `P3-C2-S1`: renderer and audit surfaces made parent-aware
- [x] `P3-C2-S2`: `S0E` parent-plus-child live refresh and audit completed

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the owner surfaces and implementation files now aligned to the `6F/P1` field boundary while representative regenerated issue artifacts remain pending under `P2`.

### P0-P1 (field boundary fixed across renderers, gate, and owner wording | 2026-04-02)

- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/issues/body-contract-S0E-5D-p0-canonical-spec.md`
  - `docs/issues/hard-gate-shape-S0E-5D-p2-canonical-spec.md`
  - `docs/runbook/run-S0E-log-to-issue-creation.md`
- expected:
  - issue creation and issue conclusion should both stop rendering `Source log` in `Metadata`, should allow optional `Previous log` under issue `Links`, and should keep lifecycle audit aligned to the same narrower boundary
- observed:
  - issue draft rendering now emits state-only `Metadata`, conclusion previews strip historical `Source log` rows from preserved metadata, lifecycle audit now accepts optional `Previous log` and rejects `Source log` in `Metadata`, and the owner logs plus runbook now describe the same field allocation

### P2 (representative artifacts regenerated and bounded live refresh completed | 2026-04-02)

- artifacts:
  - `docs/issues/issue-S0E-6F-issue-body-metadata-links-boundary-follow-up.md`
  - `docs/issues/issue-S0E-6F-issue-body-metadata-links-boundary-follow-up.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-sample-manifest.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-sample-plan.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-sample-s0e-2a-body.md`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-sample-s0e-2d-body.md`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-sample-s0e-5c-body.md`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-manifest.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-plan.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-2b-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-2a-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-4a-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-4b-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-2d-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-4c-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-4d-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-5a-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-5b-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-s0e-5c-apply-result.json`
  - `docs/issues/issue-conclusion-S0E-6F-metadata-links-refresh-live-summary.json`
  - `docs/issues/lifecycle-audit-S0E-6F-metadata-links-refresh-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-6F-metadata-links-refresh-manifest-plan.json`
- expected:
  - representative issue artifacts should show `Source log` removed from `Metadata`, `Log` retained in `Links`, and `Previous log` projected into `Links` when the source log declares it; the chosen bounded live refresh set should then verify cleanly under the new audit check
- observed:
  - the regenerated `S0E-6F` draft artifact and representative conclusion previews now show state-only `Metadata` plus deterministic `Links`, the bounded live refresh set was fixed as the current `10` closed `S0E` child issues, and the post-refresh lifecycle audit now passes on all `10/10` refreshed live issue bodies

### P3 (parent-aware body family rollout completed | 2026-04-02)

- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/issues/issue-S0E-docs-management-v5.md`
  - `docs/issues/issue-S0E-docs-management-v5.json`
  - `docs/issues/issue-S0E-6F-parent-body-refresh-live.json`
  - `docs/issues/lifecycle-audit-S0E-6F-parent-child-refresh-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-6F-parent-child-refresh-manifest-plan.json`
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/issues/body-contract-S0E-5D-p0-canonical-spec.md`
  - `docs/issues/hard-gate-shape-S0E-5D-p2-canonical-spec.md`
  - `docs/runbook/run-S0E-log-to-issue-creation.md`
- expected:
  - top-level parent issues should omit `Parent issue` and `Parent log`, should render child issue refs in `Definition of Done (DoD)`, should allow optional `Roadmap` in `Links`, and the governed `S0E` parent-plus-child set should audit cleanly under one manifest
- observed:
  - the regenerated top-level parent artifact now uses `sub/0` metadata, single-generated parent `Context`, child issue refs `#288/#289/#293/#295/#297/#300/#303/#305/#307/#309` in `Definition of Done (DoD)`, and deterministic `Links` with `Log` plus `Roadmap`; live issue `#248` now matches that body shape, and the expanded `11`-item parent-plus-child lifecycle audit now passes without warnings

## Recent changes (for traceability, optional)

- 2026-04-03: wrote back live issue `#331` and open ready-for-review PR `#343`; full-auto remains paused at the human merge boundary before post-merge issue conclusion.
- 2026-04-02: opened `S0E-6F` to narrow the issue body field boundary without reopening the broader section-order contract.
- 2026-04-02: fixed the v1 target as two explicit moves only: remove `Source log` from issue `Metadata`, and add optional `Previous log` under issue `Links`.
- 2026-04-02: recorded the concrete implementation measures in advance: shared renderer updates first, then gate/runbook alignment, then representative validation plus an explicit live-reconciliation decision.
- 2026-04-02: completed `P0-P1` by updating issue draft rendering, issue conclusion preview rendering, lifecycle audit link validation, and the owner/runbook wording to the same metadata-versus-links boundary.
- 2026-04-02: completed `P2` by regenerating representative `6F` draft/conclusion artifacts, fixing the live reconciliation scope to the current `10` closed `S0E` child issues, applying that bounded batch, and re-auditing the refreshed live issue bodies with `10/10` pass.
- 2026-04-02: completed `P3` by making the issue-body contract parent-aware, refreshing live parent issue `#248` to the new top-level body shape, and re-auditing the governed `11`-item `S0E` parent-plus-child set with `11/11` pass.