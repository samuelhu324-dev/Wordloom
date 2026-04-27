# run-WORKFLOW-GITHUB-ISSUES-001 (GitHub Issues full-auto pipeline)

---

```yaml
runbook_record:
  runbook_family: WORKFLOW-GITHUB-ISSUES
  runbook_release: 001
  runbook_id: run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline
  record_kind: ledger-aware-runbook
  status: active
  release_action: identity-and-structure-rewrite
  release_change_summary: First chronology-first rewrite for the GitHub Issues lifecycle family, narrowing family identity, fixing family-specific template authority, and reshaping parent run accounting around execution rounds, current target state, and target-stage attempts.
  summary: Use one stable operator surface for GitHub Issues lifecycle automation with two defended workflow profiles, one family-specific template quartet, and one chronology-first parent ledger that separates current state from history.
  governance_area: workflow
  applies_to: GitHub Issues lifecycle automation for source logs under docs/logs/, including child issue creation/PR/merge/conclusion and parent issue creation/conclusion.
  entry_surface: script
  evidence_surface: run-ledger
  owner_team: docs-governance
  current_steward: delegated:workflow-runbook-maintainer
  approval_state: review-pending
  reviewed_by: pending
  approved_by: pending
  file_identity_status: canonical-filename-active
  ledger_binding:
    parent_run_ledger: docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
    supplementary_ledger_series: docs/runbook/support-only/ledger-run-SUP-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
    patch_ledger_series: docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md
    minimum_evidence_files:
      - docs/issues/*.json
      - docs/issues/*plan.json
      - docs/issues/*apply-result.json
    minimum_admitted_fields:
      - execution_round_id
      - run_row_id
      - target_row_id
      - target_stage_row_id
      - target_stage_attempt_id
      - stage_name
      - stage_status
      - blocking_reason_class
      - planned_action
      - applied_action
      - status
      - warnings
  code_bridge_binding:
    required: yes
    stable_entry_refs:
      - scripts/issues/gen_issue_draft.py
      - scripts/issues/plan_pr_prep.py
      - scripts/issues/create_pr_from_plan.py
      - scripts/issues/apply_issue_relationships_with_pre_gate.py
      - scripts/issues/apply_issue_conclusion_with_pre_gate.py
      - scripts/issues/check_pr_body_contract.py
      - scripts/issues/verify_live_pr_body_contract.py
    operator_surface_refs:
      - .github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml
      - .github/workflows/s0f-pr-body-completeness-standard-check-dispatch.yml
    scenario_registry_ref: "## 3.4 Coverage and Boundary Table"
    fallback_surface_refs:
      - review-hold
      - resume-after-review
      - fail-closed preflight rejection
      - milestone-skip override
    evidence_contract_ref: "## 5) Evidence Bundle"
    minimum_supported_failure_classes:
      - missing-metadata
      - preflight-rejected
      - review-hold
      - merge-state-missing
      - pr-body-contract-fail
    coverage_table_required: yes
  template_authority:
    family_runbook_template: docs/runbook/_template-runbook-WORKFLOW-GITHUB-ISSUES.md
    family_parent_ledger_template: docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md
    family_supplement_template: docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md
    family_patch_template: docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md
  recorded_at: 2026-04-20
  reviewed_at: pending
  effective_from: 2026-04-20
  effective_until: ongoing
  introduced_by: docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md#P2-C1-S1
  last_changed_by: docs/logs/log-S0G-3E-workflow-github-issues-round-attempt-chronology-and-family-template-governance.md#P3-C1-S1
  source_refs:
    - docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
    - docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md
    - docs/logs/log-S0E-4A-github-pr-automation-contract.md
    - docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md
    - docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md
  cumulative_source_refs:
    - docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md
    - docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md
    - docs/logs/log-S0E-4A-github-pr-automation-contract.md
    - docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md
    - docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md
    - docs/runbook/legacy/run-S0E-log-to-issue-creation.md
  supporting_evidence_refs:
    - docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md
    - docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md
    - docs/logs/log-S0G-3E-workflow-github-issues-round-attempt-chronology-and-family-template-governance.md
  lineage:
    supersedes:
      - docs/runbook/legacy/run-S0E-log-to-issue-creation.md
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This release now uses the canonical `WORKFLOW-GITHUB-ISSUES-001` file identity for the same active `001` release.
    - The older `run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` path remains occupied as a compatibility stub.
    - This release now assumes chronology-first parent-run accounting across `Current Run Status Summary`, `Execution Round Table`, `Current Target Status Table`, and `Target Stage Attempt Table`.
    - Newly opened `WORKFLOW-GITHUB-ISSUES` artifacts should use the family-specific quartet templates rather than the generic skeleton templates.
```

---

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline` | `docs-governance` | `delegated:workflow-runbook-maintainer` | `review-pending` | `pending` | `pending` | `This first code-bridge sample binds the runbook to script entrypoints, artifact contracts, and secondary-enforcement wrappers without promoting the wrappers into the primary mutation boundary.` |

## 1) Purpose

- Give operators one stable surface for GitHub Issues lifecycle automation across child-issue creation, PR progression, merge, and post-merge issue conclusion, plus parent-issue creation and conclusion.
- Bind that operator surface to one explicit run-ledger family so repeated executions are auditable and extractable instead of being left only in raw artifacts or source-log evidence blocks.
- Keep the runbook thin: it owns entrypoints, semantics, and admission rules, while repeated run history belongs in the bound run ledger.

## 2) Scope

- Covered:
  - child-issue `CREATION`
  - child-issue `PR_PENDING`
  - child-issue `PR_MERGED`
  - child-issue `CONCLUSION`
  - parent-issue `CREATION`
  - parent-issue `CONCLUSION`
  - the existing script entrypoints used to realize those stages, including PR-prep, relationship follow-up, review-hold, resume-after-review, and post-merge conclusion write-back
- Out of scope:
  - GitHub label inventory creation itself
  - human review and merge execution
  - repo-wide runbook migration outside this family
- Primary source materials:
  - `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  - `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  - `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  - `docs/logs/log-S0E-4C-pr-summary-development-link-and-issue-relationship-follow-up.md`
  - `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`

## 3) Workflow Contract

### 3.1 Stable entrypoints

- Canonical local entrypoints remain the existing `scripts/issues/*.py` commands for draft generation, PR prep, relationship apply, and issue conclusion.
- Allowed operator knobs are the explicit mode and manifest/path inputs only; the workflow remains fail-closed when required metadata, merge state, or reviewed plan state is missing.
- The stable entrypoints now serve two workflow profiles rather than one prose-only lifecycle chain.

### 3.2 Workflow profiles and stage taxonomy

- `child-issue-full-lifecycle`
  - `CREATION`
  - `PR_PENDING`
  - `PR_MERGED`
  - `CONCLUSION`
- `parent-issue-light-lifecycle`
  - `CREATION`
  - `CONCLUSION`
- Parent-ledger rows should state which workflow profile each target follows; child and parent flows should not be collapsed into one generic stage list.

### 3.3 Success and failure semantics

- `PASS` means the requested lifecycle stage completed and the corresponding artifact or GitHub-side state is present.
- `FAIL` means the requested stage was attempted but blocked or rejected with a traceable reason.
- `NOT_RUN` means the stage was intentionally not attempted in the current mode.
- `PASS_AFTER_REVIEW_RESUME` is valid when the initial run stopped in `review-hold` and a later explicit resume completed the downstream stage set.
- A stage may still record `needs_follow_up=yes` even when the stage verdict is `PASS`, for example when creation succeeded under an explicit milestone-skip override or while a parent-issue field remained blank.
- The source-of-truth verdict fields live in the emitted plan/apply JSON artifacts, not in prose-only console output.

### 3.4 Code Bridge Table

| bridge id | surface kind | stable ref | operator meaning owned here | current standing | notes |
| --- | --- | --- | --- | --- | --- |
| `RB-ISSUES-01` | `script` | `scripts/issues/gen_issue_draft.py` | `Issue creation remains bound to explicit metadata parsing and fail-closed draft/create behavior.` | `defended-now` | `Blank or missing fields must stay visible through warnings or stop behavior rather than being silently defaulted.` |
| `RB-ISSUES-02` | `script` | `scripts/issues/plan_pr_prep.py; scripts/issues/create_pr_from_plan.py` | `PR preparation and publish remain bound to plan artifacts plus preflight validation before local branch materialization or publish.` | `defended-now` | `create_pr_from_plan.py` rejects mismatched or non-allowed preflight results fail-closed. |
| `RB-ISSUES-03` | `script` | `scripts/issues/check_pr_body_contract.py; scripts/issues/verify_live_pr_body_contract.py` | `PR body structure is governed by contract validators that can fail the local or live check when required sections, link labels, or evidence footer lines drift.` | `defended-now` | `These validators are part of the defended operator surface, not optional lint.` |
| `RB-ISSUES-04` | `workflow` | `.github/workflows/s0e-publish-verify-remediation-gate-read-only-wrapper-dispatch.yml` | `GitHub Actions may replay the local publish gate as secondary enforcement and retained evidence.` | `defended-now` | `The workflow is explicitly not the first publish authorization boundary.` |
| `RB-ISSUES-05` | `workflow` | `.github/workflows/s0f-pr-body-completeness-standard-check-dispatch.yml` | `GitHub Actions may replay the PR body completeness check as secondary enforcement and retained evidence.` | `defended-now` | `The workflow is explicitly not the primary review boundary.` |
| `RB-ISSUES-06` | `mode` | `review-hold; resume-after-review; milestone-skip override` | `The runbook may name bounded operator modes and overrides that already appear in artifacts and scripts.` | `partial-code-support` | `The code supports these switches, but approval ownership and escalation policy remain narrower workflow-governance material rather than fully expanded here.` |

### 3.5 Coverage and Boundary Table

| scenario id | failure class | default system behavior | operator action class | prod relevance | cadence class | evidence minimum | coverage class | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SC-ISSUES-01` | `missing-metadata` | `fail-closed` | `repair-source` | `every-run` | `per-run` | `issue draft json or plan/apply json with warnings/errors` | `defended-now` | `The family should stop or warn explicitly when required source metadata is missing.` |
| `SC-ISSUES-02` | `preflight-rejected` | `fail-closed` | `repair-source` | `every-run` | `per-run` | `front-half preflight result json` | `defended-now` | `Publish cannot continue when gate_apply_allowed or preflight_allowed is false or the decision is not publish-eligible.` |
| `SC-ISSUES-03` | `review-hold` | `pause-and-resume` | `resume-stage` | `follow-up-only` | `after-review` | `plan/apply json plus later resume evidence` | `defended-now` | `PASS_AFTER_REVIEW_RESUME` is an admitted lifecycle verdict.` |
| `SC-ISSUES-04` | `merge-state-missing` | `not-run` | `repair-source` | `follow-up-only` | `after-review` | `plan/apply json or conclusion result json` | `defended-now` | `Post-merge stages should not claim success when merged PR selection is empty.` |
| `SC-ISSUES-05` | `pr-body-contract-fail` | `fail-closed` | `repair-source` | `every-run` | `per-run` | `contract-check json or live-contract-check json` | `defended-now` | `Required sections, allowed links, and evidence-footer shape are machine-validated.` |
| `SC-ISSUES-06` | `workflow-wrapper-stop` | `secondary-enforcement stop` | `inspect-retained-artifact` | `follow-up-only` | `after-wrapper-run` | `wrapper result json, workflow summary, dispatch manifest` | `defended-now` | `GitHub Actions stop/error semantics are valid evidence surfaces but not the primary mutation decision.` |
| `SC-ISSUES-07` | `override-required` | `bounded override path` | `explicit-override` | `incident-only` | `when-needed` | `apply-result json plus warning or notes` | `partial-code-support` | `Milestone-skip and similar overrides exist, but the escalation policy remains narrower than the current sample.` |

## 4) Run Ledger Binding

### 4.1 Parent ledger

- Canonical parent ledger:
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- Each admitted bounded batch for this first runbook release should be recorded under that ledger's current/history split surfaces: current run summary, execution rounds, current target status, and target-stage attempts.
- Later completion passes or evidence sharpening for the same bounded batch should normally stay under the same `run_row_id` and attach through `SUP`, not force a new run-ledger sequence.

### 4.1A Support-only supplement and patch ledgers

- Canonical supplement ledgers and patch ledgers for this runbook family should also live under `docs/runbook/support-only/`.
- The first reserved patch-ledger name for this runbook release is:
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

### 4.2 Run, target, and stage ids

- Stable run-row shape:
  - `RUN-001`, `RUN-002`, ...
- Stable execution-round shape beneath one run row:
  - `RUN-001-R01`, `RUN-001-R02`, ...
- Stable target-row shape beneath one run row:
  - `RUN-001-T01`, `RUN-001-T02`, ...
- Stable target-stage-row shape beneath one target row:
  - `RUN-001-T01-STG-CREATION`
  - `RUN-001-T01-STG-PR_PENDING`
  - `RUN-001-T01-STG-PR_MERGED`
  - `RUN-001-T01-STG-CONCLUSION`
- Semantic identity should stay adjacent rather than embedded:
  - `target_ref_key`: `S4F-2A`
  - `target_ref_path`: `<source-log-or-artifact-path>`
- Optional replay-heavy attempt shape, reserved but not required in the first rewrite:
- Stable target-stage-attempt shape beneath one target-stage row:
  - `RUN-001-T01-STG-CREATION-A01`
- Stable evidence-item shape beneath one run row:
  - `RUN-001-E01`, `RUN-001-E02`, ...
- If screenshots, transcripts, or exported review artifacts are needed later, attach them through SUP ledgers using the `RUN-001-SUP-01-ATT-01` style.
- If a bounded repair packet is needed without changing the runbook release, attach it through a PATCH ledger under the same support-only root.

### 4.3 Admission and write-back rule

- A run may enter the parent ledger only when the requested stage emitted at least one durable JSON or Markdown artifact under `docs/issues/` or another explicit retained path.
- If later evidence only sharpens or corrects one admitted run verdict, open a SUP ledger instead of rewriting the original run row invisibly.
- If later evidence sharpens one admitted stage, the parent ledger should update the current target reading and append a stage-attempt row rather than duplicating the stable target or stage row.
- If a bounded repair packet is needed for scripts, manifests, docs, or retained evidence while the runbook release stays unchanged, open a PATCH ledger instead of treating that repair as an unstructured patch note.
- If one follow-up both changes the workflow implementation and changes how an admitted run, target, or stage should now be read, record both surfaces explicitly: `PATCH` for the repair packet and `SUP` for the parent-ledger follow-up.
- Downstream write-back should stay explicit:
  - source-log `Evidence` for packet-level conclusion
  - parent run ledger for repeated execution accounting
  - SUP ledger for later evidence refinement
  - PATCH ledger for runbook-bound bounded repairs that do not justify a release bump
  - maintenance or family patch lanes only when the repair is intentionally outside run-ledger accounting

## 5) Evidence Bundle

### 5.1 Output roots

- Primary retained output root for this family:
  - `docs/issues/`
- Minimum evidence files vary by stage, but should include one or more of:
  - `issue-*.json`
  - `*-plan.json`
  - `*-apply-result.json`
  - generated Markdown drafts or body preview artifacts when they are the defended review surface

### 5.2 Admitted fields

- Minimum admitted fields for ledger extraction:
  - `planned_action`
  - `applied_action`
  - `status`
  - `warnings`
  - issue/PR/relationship identifiers when present

## 6) Local or One-click Operation

### 6.1 Prerequisites

- Python is available in the active workspace environment.
- `gh auth status` succeeds for any real GitHub apply step.
- Source logs contain the required `issue_*` and `pr_*` metadata or intentionally leave them blank under fail-closed rules.
- Any stage that requires a merged PR must only be run after merge completion is real.

### 6.2 Commands

- Representative issue-create path:

```powershell
python scripts/issues/gen_issue_draft.py docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md --create --repo samuelhu324-dev/wordloom-v3
```

- Representative PR-prep path:

```powershell
python scripts/issues/plan_pr_prep.py <manifest-path>
python scripts/issues/create_pr_from_plan.py <plan-path> --item-index 0
```

- Representative post-merge conclusion path:

```powershell
python scripts/issues/plan_issue_conclusion.py <manifest-or-log>
python scripts/issues/apply_issue_conclusion.py <plan-path> --item-index 0
```

## 7) Troubleshooting

- Symptom: missing or placeholder summary blocks
  - First inspect the PR-prep plan artifact and the source log `PR Summary Inputs` block.

- Symptom: relationship attach does not appear in GitHub sidebar
  - First inspect the relationship plan/apply result JSON rather than the issue body markdown.

- Symptom: post-merge conclusion stops unexpectedly
  - First inspect whether the PR is actually merged and whether exact-ID merged PR selection returned a non-empty set.

- Symptom: issue or PR metadata looks incomplete
  - First inspect the source log frontmatter and fail-closed warnings in the emitted JSON artifact.

## 8) Notes and Boundaries

- This runbook is the family-level operator surface, not the full phase history for `S0E` or `S0G`.
- Contract history still lives in the owning `S0E-*` and `S0G-*` logs.
- Repeated execution accounting belongs in the bound run ledger, not inside this runbook body.
- Small local repairs to scripts, manifests, or docs may land through patch or maintenance lanes without forcing a new runbook release, as long as the runbook semantics themselves do not materially change.
- File-identity repair for the current `001` release is now executed; any later successor-release decision remains out of scope for this runbook body.
- The `s0e-*` and `s0f-*` GitHub Actions wrappers are secondary-enforcement and retained-evidence surfaces only; they should not be read as the first publish or review authorization boundary.
- The broad GitHub-Issues mechanism parent contract remains manual and decomposition-oriented; this runbook is the first defended code-coupled sample for the Issues lifecycle automation family.

## Thinness Rules

- Keep this runbook as one family-level operator surface only.
- Do not duplicate `Execution Round Table` or `Target Stage Attempt Table` history inside the runbook body.
- Do not copy recurring run rows into the runbook.
- Do not use this runbook to replace the bound run ledger or the source logs.