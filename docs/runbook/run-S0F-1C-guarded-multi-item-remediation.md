# Run-S0F-1C: guarded multi-item live mutation remediation

---

**id**: `S0F-1C-guarded-multi-item-remediation`
**kind**: `runbook`
**title**: `run/S0F-1C-guarded-multi-item-remediation`
**status**: `stable`
**scope**: `S0F-1C`
**decision_date**: `2026-04-04`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `Standardize a repeatable multi-item historical remediation path that keeps preview planning, family-owned guarded apply, and preserve-existing post-verify as separate stages with per-target evidence retention.`
  **positive**: `"Per-target evidence trail", "No raw batch mutation entrypoint", "Repeatable operator sequence across preview, apply, and verify"`
  **negative**: `"More retained artifacts per run", "Batchs may need explicit family splits", "Frozen audit-plan fallback requires operator judgment"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- Provide one operator-facing path for repeatable historical multi-item remediation without reopening raw live-mutation entrypoints.
- Keep the workflow narrow and auditable:
  - stage 1: preview planning
  - stage 2: family-owned guarded apply
  - stage 3: per-target preserve-existing post-verify
- Preserve one shared batch lineage where safe, but never at the cost of losing per-target evidence.

## 2) Scope

- Covered:
  - multi-item historical remediation where all live mutations stay inside one family-owned guarded surface
  - representative issue-conclusion refresh batches for already-closed issues
  - preview-only planning, shared pre-gate/remediation artifacts, per-target guarded apply, and per-target post-verify
- Out of scope:
  - mixed-family apply in one pass
  - raw apply scripts as operator entrypoints
  - treating runbook prose as the source of contract truth instead of the owning logs and scripts
- Source materials:
  - `docs/logs/log-S0F-1C-guarded-multi-item-live-mutation-remediation.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `scripts/issues/plan_lifecycle_pre_gate.py`
  - `scripts/issues/plan_lifecycle_remediation.py`
  - `scripts/issues/apply_issue_conclusion_with_pre_gate.py`
  - `scripts/issues/plan_issue_conclusion.py`

## 3) Evidence Bundle

### 3.1 Output roots

- Multi-item preview planning:
  - `docs/issues/lifecycle-audit-S0F-1C-*-manifest.json`
  - `docs/issues/lifecycle-audit-S0F-1C-*-plan.json`
  - `docs/issues/lifecycle-gate-S0F-1C-*-decision.json`
  - `docs/issues/lifecycle-remediation-S0F-1C-*-plan.json`
  - `docs/issues/lifecycle-remediation-S0F-1C-*-issue-conclusion-manifest.json`
- Per-target guarded apply:
  - `docs/issues/issue-conclusion-S0F-1C-*-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1C-*-plan.json`
  - `docs/issues/issue-conclusion-S0F-1C-*-apply-result.json`
- Per-target post-verify:
  - `docs/issues/issue-conclusion-S0F-1C-*-post-verify-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1C-*-post-verify-plan.json`

### 3.2 Minimal evidence contract

- A repeatable batch is not complete unless all three layers exist:
  - one shared preview lineage
  - one guarded result per applied target
  - one post-verify plan per target
- Summary artifacts may be retained for operator readability, but they do not replace per-target files.
- Stable summaries retained by `S0F-1C`:
  - `docs/issues/lifecycle-preview-S0F-1C-p1-summary.json`
  - `docs/issues/lifecycle-guarded-apply-S0F-1C-p2-summary.json`
  - `docs/issues/lifecycle-post-verify-S0F-1C-p3-summary.json`

## 4) Local Operation

### 4.1 Prerequisites

- GitHub CLI authenticated for the target repository.
- Python environment able to run `scripts/issues/*.py`.
- One reviewed target set that stays inside a single live-mutation family for the apply step.
- If the aggregate live lifecycle-audit path for the representative set is already known to be unstable, the operator may use a frozen audit-plan assembled from retained single-item audit outputs, but that choice must be recorded in the summary artifact.

### 4.2 Canonical sequence

1. Prepare a shared multi-item preview manifest.

```powershell
c:/python314/python.exe scripts/issues/plan_lifecycle_pre_gate.py docs/issues/lifecycle-audit-S0F-1C-p1-preview-plan.json --input-kind audit-plan --decision-path docs/issues/lifecycle-gate-S0F-1C-p2-live-decision.json --remediation-plan-path docs/issues/lifecycle-remediation-S0F-1C-p2-live-plan.json
```

2. Confirm the remediation plan emits only one live-mutation family.

- For issue-conclusion batches, the shared downstream manifest should be:
  - `docs/issues/lifecycle-remediation-S0F-1C-...-issue-conclusion-manifest.json`
- If relationship or PR-body actions appear in the same remediation plan, stop and split the batch before any live mutation.

3. Apply through the family-owned guarded wrapper, one target at a time.

```powershell
c:/python314/python.exe scripts/issues/apply_issue_conclusion_with_pre_gate.py docs/issues/lifecycle-audit-S0F-1C-p1-preview-plan.json docs/issues/lifecycle-remediation-S0F-1C-p2-live-issue-conclusion-manifest.json --item-index 0 --gate-input-kind audit-plan --context-mode preserve-existing --gate-decision-path docs/issues/lifecycle-gate-S0F-1C-p2-live-decision.json --gate-remediation-plan-path docs/issues/lifecycle-remediation-S0F-1C-p2-live-plan.json --conclusion-plan-path docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-plan.json --body-path docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-apply-body.md --apply-result-path docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-apply-result.json --guarded-result-path docs/issues/issue-conclusion-S0F-1C-p2-s6b-1a-guarded-result.json
```

- Repeat with `--item-index 1`, `--item-index 2`, and matching per-target output paths.
- Keep `--context-mode preserve-existing` for pure path verification on already-closed historical issues unless the explicit goal is to author fresh prose.

4. Run preserve-existing post-verify per target.

```powershell
c:/python314/python.exe scripts/issues/plan_issue_conclusion.py docs/issues/issue-conclusion-S0F-1C-p3-s6b-1a-post-verify-manifest.json --context-mode preserve-existing --plan-path docs/issues/issue-conclusion-S0F-1C-p3-s6b-1a-post-verify-plan.json
```

- Repeat for each target and retain one post-verify plan per item.

### 4.3 Success criteria for one batch

- Shared pre-gate decision stops at remediation or allows apply exactly as expected.
- Every target that is applied has:
  - one guarded result
  - one apply result
  - one post-verify plan
- Post-verify warnings do not exceed the known clean-preserve baseline for that batch.

## 5) Troubleshooting

- Symptom: remediation plan contains multiple live-mutation families.
  - Inspect: `docs/issues/lifecycle-remediation-*-plan.json`
  - Action: split the batch by family before any apply step.

- Symptom: guarded apply exits with `blocked-manifest-mismatch`.
  - Inspect: shared remediation plan and downstream manifest path recorded in `docs/issues/lifecycle-remediation-*-plan.json`
  - Action: use the remediation-derived downstream manifest path instead of a manually named substitute.

- Symptom: only item index `0` applies successfully from a shared issue-conclusion manifest.
  - Inspect: `scripts/issues/apply_issue_conclusion_with_pre_gate.py`
  - Action: use explicit `--item-index` and retain per-target output paths.

- Symptom: post-verify emits warnings beyond merged-PR override plus preserve-existing preservation notes.
  - Inspect: per-target `docs/issues/issue-conclusion-*-post-verify-plan.json`
  - Action: classify the extra warning as target-local drift and stop the batch close-out until the target is reconciled.

- Symptom: aggregate live lifecycle-audit becomes operationally unstable for the representative set.
  - Inspect: last retained single-item audit outputs and the preview summary artifact.
  - Action: use a frozen audit-plan only for preview-stage or shared pre-gate lineage, and record that choice explicitly in the retained summary.

## 6) Notes and Boundaries

- This runbook is procedural only; the owning contract still lives in `S0F-1C`.
- Do not create a second operator path that calls raw apply scripts directly.
- Do not treat a summary artifact as sufficient on its own; the per-target evidence files remain the operational source of truth.
- The next likely expansion point is packaging the same repeatable pattern for additional families once they can prove the same shared-upstream plus per-target-apply shape.