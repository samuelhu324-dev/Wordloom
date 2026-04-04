# log-S0F-1C (Phase 1C: guarded multi-item live mutation remediation)

---

**id**: `S0F-1C`
**kind**: `log`
**title**: `guarded multi-item live mutation remediation v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, Drills, Evidence, epic/s0, sub/1c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
  **reference_log_1**: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  **reference_log_2**: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
  **reference_log_3**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_5**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **reference_log_6**: `docs/logs/log-S0E-7E-publish-verify-remediation-gate-thin-orchestration-entrypoint.md`
**issue_keyword**: `automation`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
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
**created**: `2026-04-04`
**updated**: `2026-04-04`

---

## Decision / Outcome

**Decision**:

- `S0F-1C` is the next follow-up slice under `S0F`, and it turns the already-proven single-item guarded mutation model into a manifest-driven multi-item remediation workflow.
- v1 should not reopen the old raw-apply surfaces just because the target set becomes larger; batch or multi-item operation must still remain wrapper-owned, pre-gated, and fail-closed.
- The first target is deliberately narrow: historical issue-conclusion Context refresh is the proving ground, but the contract should be written so the same batch discipline can later cover other issue / PR live mutation families.

**Default choices (phase defaults / v1)** (optional, but recommended):

- Multi-item work must begin with preview planning, not live apply.
- A batch manifest may describe multiple targets, but each target must still preserve exact source-log grounding, explicit merged-PR evidence, and family-specific eligibility checks.
- Guarded remediation remains the only operator-facing live mutation path for already-closed issues or equivalent historical refreshes.
- `preserve-existing` post-verify is mandatory after any live refresh batch so drift can be measured against the live body that was just written.
- Batch throughput is not a reason to weaken sentence-count, placeholder-hygiene, or ownership checks.
- If one target needs special handling, the batch must stop or split; v1 does not permit a soft fallback that silently downgrades one item while the rest continue.
- The first batch sample should stay small and representative so retained artifacts remain reviewable by hand.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.

**PR summary bullets**:

- Define a manifest-driven batch remediation contract for guarded multi-item live mutation work.
- Keep preview, guarded apply, and preserve-existing post-verify as three separate owned stages instead of collapsing them into one replay command.
- Require per-target evidence retention so multi-item runs do not hide which item drifted, stopped, or needed remediation.
- Use historical issue-conclusion Context refresh as the first representative sample without reopening raw mutation entrypoints.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.
- If the implementation work lands in multiple review units, keep each PR scoped to the exact `P*-C*-S*` unit.

**PR links**:

- Log: `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
- Runbook: ``
- Evidence artifact: `docs/issues/lifecycle-post-verify-S0F-1C-p3-summary.json`

## Definitions (optional)

- `multi-item remediation`: a workflow that refreshes or repairs more than one live target under one manifest while still preserving per-target gate and evidence outputs.
- `guarded batch`: a batch surface that may orchestrate several items, but only by delegating each real mutation through the family-owned guarded apply path.
- `post-refresh preserve-existing verify`: a non-mutating verification run that confirms the freshly written live body still satisfies the canonical contract when preserved as-is.
- `mixed-remediation batch`: a candidate batch whose downstream follow-up actions span different live-mutation families for the same apply pass; v1 treats that as a split-or-stop condition rather than something one guarded apply may partially absorb.
- `per-target failure semantics`: a rule that each target keeps its own stage-local stop reason, such as preview-plan stop, guarded-apply block, or post-verify drift stop, even when the top-level manifest contains several items.

## P0 Contract Vocabulary (v1)

- `preview planning` is a read-only stage that may audit live state, run lifecycle pre-gate, and emit remediation or downstream manifests, but it may not perform any GitHub mutation.
- `guarded apply` is the only live-mutation stage, and it must enter through a family-owned wrapper such as `apply_issue_conclusion_with_pre_gate.py`, `apply_issue_relationships_with_pre_gate.py`, or `apply_pr_body_scope_with_pre_gate.py` rather than a raw apply script.
- `preserve-existing post-verify` is a mandatory non-mutating follow-up stage after live refresh; it re-plans against the just-written live body while preserving that body, so drift can be measured without performing another rewrite.
- `multi-item manifest` means one input manifest may enumerate several targets, but each target still keeps its own audit result, remediation status, downstream manifest path, guarded apply result, and post-verify artifact.

## Constraints

- Do not turn batch support into a justification for reintroducing raw apply entrypoints as operator defaults.
- Do not treat aggregate success as sufficient evidence; each target still needs traceable per-item outputs.
- Do not allow batch tooling to hide semantic failures behind retry language meant for transient execution problems.
- Do not broaden the first rollout beyond a reviewable representative set.
- Do not let one guarded apply invocation absorb mixed remediation families; if a remediation plan spans conclusion, relationship, or PR-body actions together, the operator must split the batch by family before mutation.
- Do not treat post-verify as optional bookkeeping; a live refresh batch is incomplete until `preserve-existing` verification artifacts are retained per target.

## Scope

- `P0`: define the guarded multi-item remediation contract and wire `S0F-1C` into the `S0F` spine
- `P1`: preview-only batch planning contract for representative historical targets
- `P2`: guarded live apply contract for multi-item historical refresh
- `P3`: preserve-existing post-verify and drift-report contract after live refresh
- `P4`: operator runbook and representative retained sample for repeatable batch remediation

## Success Criteria (DoD)

- Multi-item historical refresh can be described through one manifest without losing per-target gate ownership or evidence traceability.
- No batch path can bypass the existing guarded family apply surfaces.
- Post-refresh verification can distinguish a clean preserved live body from a drifted or malformed one on a per-target basis.
- Operators can tell from retained artifacts which stage stopped: preview planning, guarded apply, or preserve-existing re-verify.
- The first representative batch sample remains small enough for hand review while still proving the contract is reusable.
- The stage vocabulary is explicit enough that later `P1-P3` implementation can map one retained artifact family to each stage without inventing new failure semantics.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the batch contract is implemented without reopening raw mutation entrypoints;
  - at least one representative multi-item remediation sample retains preview, guarded apply, and preserve-existing post-verify artifacts;
  - failure semantics remain per-target and fail-closed rather than aggregate-only.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1C/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit.

**Branch convention**:

- `S0F-1C` related changes should stay on `S0F-*` working branches, currently `S0F-docs-management-v6`.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly on `S0F-docs-management-v6` so the new spine does not drift ahead of origin.

## P0 Stage Contract (completed)

- Stage 1 `preview planning`:
  - allowed operations: lifecycle audit, pre-gate decision, remediation planning, downstream manifest generation
  - forbidden operations: any GitHub mutation, any raw apply delegation, any rewrite of live issue or PR state
  - retained outputs: audit manifest/plan, pre-gate decision, remediation plan, family-specific downstream manifests
- Stage 2 `guarded apply`:
  - allowed operations: exactly one family-owned guarded wrapper consumes one compatible downstream manifest or one compatible remediation-derived manifest path and performs live mutation
  - forbidden operations: mixed-family apply in one pass, raw apply entrypoints, silent fallback from a blocked manifest to a guessed target set
  - retained outputs: guarded result artifact, apply body/result artifacts, explicit eligibility/warning surface when remediation-owned apply is allowed
- Stage 3 `preserve-existing post-verify`:
  - allowed operations: non-mutating re-plan against live state with `preserve-existing`, drift detection, post-refresh contract validation
  - forbidden operations: another rewrite disguised as verification, silent regeneration of Context/body content during verification
  - retained outputs: post-verify plan and any per-target drift findings, with one artifact per target rather than aggregate-only status
- Batch-level rule:
  - one multi-item batch may share a top-level manifest and shared naming slug, but stage artifacts must still preserve per-target traceability so operators can split, rerun, or stop one target without losing the others' evidence trail.

## P1 Preview Manifest Shape (completed)

- top-level fields:
  - `version`, `mode`, and `defaults.repo` stay explicit so the sample remains replayable without hidden repo inference
  - `defaults.expected_parent_issue_number` may be shared at the manifest level when all targets belong to the same audited parent issue
- per-item required fields:
  - `requested_id`
  - `source_log_path`
  - `issue_number`
  - `reason`
- per-item derived preview outputs:
  - one frozen audit-plan item retaining checks, merged PR evidence, and audit status
  - one pre-gate decision item retaining gate status and remediation summary
  - one remediation-plan item retaining planned steps and downstream manifest path
- sample rule:
  - `P1` may use a frozen audit-plan assembled from retained single-item audit outputs when the aggregate live audit path is already known to be operationally unstable for the representative set, so long as the retained sample is clearly marked preview-only and no live mutation occurs.

## P2 Guarded Apply Split Rules (completed)

- shared upstream artifacts:
  - one retained multi-item audit-plan may feed one shared pre-gate decision and one shared remediation plan
  - one remediation plan may emit one shared downstream issue-conclusion manifest when all items stay inside the same issue-conclusion family
- live apply ownership:
  - even when the downstream issue-conclusion manifest contains multiple items, live mutation still executes per target through repeated calls to the family-owned guarded wrapper
  - the guarded wrapper, not the caller, owns the pre-gate rerun, remediation-manifest match check, and raw-live-mutation delegation boundary
- split rules:
  - if the remediation plan contains more than one live-mutation family, the batch must split before any apply step
  - if all items remain inside one family, the batch may share the upstream gate/remediation artifacts but must retain per-target guarded result, plan, and apply result artifacts
- representative live sample rule:
  - `P2` may use `preserve-existing` on already-closed historical issues to prove the guarded apply path without introducing fresh LLM-authored prose drift during the live-sample step itself

## P3 Post-Verify Drift Rules (completed)

- mandatory follow-up rule:
  - every guarded live sample must be followed by non-mutating `preserve-existing` verification before the batch can be considered complete
- verification ownership:
  - post-verify remains on the family planning surface rather than the apply surface, so no live mutation is allowed during drift confirmation
- per-target drift retention:
  - each target keeps its own post-verify manifest, plan, preview body, and drift status
  - aggregate batch summaries may report the overall result, but they do not replace per-target evidence
- clean-preserve rule:
  - `planned` plus preserve-existing warnings that only confirm merged-PR override sourcing and live Context preservation counts as a clean preserve result
  - any new structural warning beyond that baseline must be retained as target-local drift rather than merged into a generic batch warning bucket

## Plan (draft)

### P0 (Contract and spine wiring)

- P0-C1-S1: create `S0F-1C` and wire it into the `S0F` parent spine as the next follow-up slice
- P0-C1-S2: define the batch-stage vocabulary covering preview, guarded apply, and preserve-existing post-verify

### P1 (Preview planning)

- P1-C1-S1: define the representative multi-item manifest shape for historical refresh targets
- P1-C1-S2: retain a preview-only sample proving multiple targets can be planned without live mutation

### P2 (Guarded apply)

- P2-C1-S1: define the per-target eligibility and remediation handoff rules for multi-item guarded apply
- P2-C1-S2: retain a live sample proving multi-item refresh still routes through family-owned guarded surfaces

### P3 (Post-refresh verification)

- P3-C1-S1: define preserve-existing post-verify as the mandatory follow-up stage after batch live refresh
- P3-C1-S2: retain a sample drift report that shows clean preserve versus stop-worthy drift at per-target granularity

### P4 (Operator repeatability)

- P4-C1-S1: publish a small-scope runbook for repeatable historical refresh batches without reopening raw apply entrypoints

## Execution Checklist (unchecked)

### P0 (Contract and spine wiring)

- [x] `P0-C1-S1`: `S0F-1C` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: batch-stage vocabulary fixed for preview, guarded apply, and preserve-existing post-verify

### P1 (Preview planning)

- [x] `P1-C1-S1`: representative multi-item manifest shape fixed
- [x] `P1-C1-S2`: preview-only multi-item sample retained

### P2 (Guarded apply)

- [x] `P2-C1-S1`: per-target eligibility and remediation handoff rules fixed
- [x] `P2-C1-S2`: representative guarded multi-item live sample retained

### P3 (Post-refresh verification)

- [x] `P3-C1-S1`: preserve-existing post-verify fixed as mandatory batch follow-up
- [x] `P3-C1-S2`: representative per-target drift report retained

### P4 (Operator repeatability)

- [ ] `P4-C1-S1`: repeatable operator runbook retained

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1 (child log created and parent wired | 2026-04-04)

- artifacts:
  - `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - `S0F-1C` should exist as the next `S0F` child slice with a clear handoff from the single-item `S0F-1B` proof to multi-item guarded remediation
  - the `S0F` parent spine should point to the new child log and describe its role briefly enough that later phase work can be located without reopening branch archaeology
- observed:
  - `S0F-1C` now exists as a draft child log with explicit `P0-P4` scope for preview planning, guarded multi-item live apply, preserve-existing post-verify, and operator repeatability
  - the `S0F` parent spine now points `phase_log_3` at this child slice and records it as the next follow-up after the `S0F-1B` historical refresh proof set

### P0-C1-S2 (batch-stage vocabulary fixed | 2026-04-04)

- artifacts:
  - `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `scripts/issues/plan_lifecycle_pre_gate.py`
  - `scripts/issues/plan_lifecycle_remediation.py`
  - `scripts/issues/apply_issue_conclusion_with_pre_gate.py`
  - `scripts/issues/apply_issue_relationships_with_pre_gate.py`
  - `scripts/issues/apply_pr_body_scope_with_pre_gate.py`
  - `scripts/issues/plan_issue_conclusion.py`
- expected:
  - `S0F-1C/P0` should define one explicit three-stage vocabulary so future batch implementation work does not blur preview planning, live mutation, and post-refresh verification into one command surface
  - the contract should align with already-existing pre-gate, remediation, guarded apply, and `preserve-existing` verification surfaces rather than inventing new semantics disconnected from the current repo
- observed:
  - the log now defines `preview planning`, `guarded apply`, `preserve-existing post-verify`, `mixed-remediation batch`, and `per-target failure semantics` as the canonical `S0F-1C` vocabulary for multi-item remediation work
  - the completed `P0` stage contract now states allowed operations, forbidden operations, and retained outputs for all three stages, which makes later `P1-P3` work traceable back to one explicit contract instead of ad hoc batch wording
  - the vocabulary is aligned to the current implementation surface: `plan_lifecycle_pre_gate.py` and `plan_lifecycle_remediation.py` own preview planning, family-owned `*_with_pre_gate.py` wrappers own live mutation, and `plan_issue_conclusion.py --context-mode preserve-existing` anchors post-refresh re-verification semantics

### P1-C1-S1S2 (preview-only multi-item sample retained | 2026-04-04)

- artifacts:
  - `docs/issues/lifecycle-audit-S0F-1C-p1-preview-manifest.json`
  - `docs/issues/lifecycle-audit-S0F-1C-p1-preview-plan.json`
  - `docs/issues/lifecycle-gate-S0F-1C-p1-preview-decision.json`
  - `docs/issues/lifecycle-remediation-S0F-1C-p1-preview-plan.json`
  - `docs/issues/lifecycle-remediation-S0F-1C-p1-preview-issue-conclusion-manifest.json`
  - `docs/issues/lifecycle-preview-S0F-1C-p1-summary.json`
- expected:
  - `P1` should retain one representative multi-item manifest shape for historical refresh work, with shared defaults at the top level and per-target grounding fields at the item level
  - the representative sample should prove that multiple targets can pass through preview planning, pre-gate decision, and remediation planning without performing any live mutation
- observed:
  - `S0F-1C/P1` now retains a canonical three-item preview manifest for `S6B-1A/#357`, `S6B-1B/#358`, and `S6B-1C/#359`, with shared repo and expected-parent defaults plus per-target `requested_id`, `source_log_path`, `issue_number`, and `reason`
  - because the aggregate live lifecycle-audit path for this target set was already known to be operationally unstable, the retained preview sample uses a frozen multi-item audit-plan assembled from the already-retained `S0F-1B/P5` single-item audit outputs, which preserves per-target checks and merged PR evidence while keeping the sample strictly preview-only
  - `plan_lifecycle_pre_gate.py --input-kind audit-plan` then produced one stop-for-remediation decision and one remediation plan covering all three targets, with the downstream issue-conclusion manifest retaining exact merged PR overrides `#360/#361/#362` and no live mutation performed anywhere in the `P1` sample

### P2-C1-S1S2 (guarded multi-item live sample retained | 2026-04-04)

- artifacts:
  - `scripts/issues/apply_issue_conclusion_with_pre_gate.py`
  - `docs/issues/lifecycle-gate-S0F-1C-p2-live-decision.json`
  - `docs/issues/lifecycle-remediation-S0F-1C-p2-live-plan.json`
  - `docs/issues/lifecycle-remediation-S0F-1C-p2-live-issue-conclusion-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-plan.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-apply-result.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1b-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1b-plan.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1b-apply-result.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1c-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1c-plan.json`
  - `docs/issues/issue-conclusion-S0F-1C-p2-s6b-1c-apply-result.json`
  - `docs/issues/lifecycle-guarded-apply-S0F-1C-p2-summary.json`
- expected:
  - `P2` should prove that a shared multi-item remediation-owned issue-conclusion manifest can still be applied only through the family-owned guarded wrapper, with live mutation executed per target rather than through a reopened raw batch surface
  - the retained sample should keep one shared gate/remediation lineage for the batch while preserving one guarded result and one apply result per target
- observed:
  - `apply_issue_conclusion_with_pre_gate.py` now accepts `--item-index`, which closes the previous wrapper gap where a shared multi-item issue-conclusion manifest could only be applied at item index `0`
  - `S0F-1C/P2` retained one shared gate decision and one shared remediation plan for the representative `S6B-1A/#357`, `S6B-1B/#358`, and `S6B-1C/#359` sample, then applied all three items through repeated wrapper invocations against the same remediation-owned issue-conclusion manifest with item indexes `0`, `1`, and `2`
  - all three guarded results recorded `allowed-via-targeted-conclusion-remediation` and `applied-after-pre-gate`, which proves the live sample remained inside the issue-conclusion family-owned guarded surface instead of reopening raw apply entrypoints or collapsing the batch into one opaque live mutation step

### P3-C1-S1S2 (per-target preserve-existing post-verify retained | 2026-04-04)

- artifacts:
  - `docs/issues/issue-conclusion-S0F-1C-p3-s6b-1a-post-verify-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1C-p3-s6b-1a-post-verify-plan.json`
  - `docs/issues/issue-conclusion-S0F-1C-p3-s6b-1b-post-verify-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1C-p3-s6b-1b-post-verify-plan.json`
  - `docs/issues/issue-conclusion-S0F-1C-p3-s6b-1c-post-verify-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1C-p3-s6b-1c-post-verify-plan.json`
  - `docs/issues/lifecycle-post-verify-S0F-1C-p3-summary.json`
- expected:
  - `P3` should prove that preserve-existing re-verification is a mandatory follow-up after the representative guarded live sample, and that drift is retained per target instead of inferred from aggregate batch success
  - each target should produce a non-mutating post-verify plan that confirms whether the just-written live body remains structurally valid when preserved as-is
- observed:
  - `S0F-1C/P3` derived one post-verify manifest per target from the shared `P2` issue-conclusion manifest and ran `plan_issue_conclusion.py --context-mode preserve-existing` separately for `S6B-1A/#357`, `S6B-1B/#358`, and `S6B-1C/#359`
  - all three post-verify plans remained in `planned` state and emitted only the expected preserve-existing baseline warnings for explicit merged-PR overrides and live Context preservation, so the retained drift summary classifies all three items as `clean-preserve`
  - the retained `P3` summary artifact now records the per-target manifests, plans, and clean-preserve status, which closes the batch loop without relying on aggregate-only success language