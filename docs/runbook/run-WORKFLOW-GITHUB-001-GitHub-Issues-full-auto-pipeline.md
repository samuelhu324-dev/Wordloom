# run-WORKFLOW-GITHUB-001 (GitHub Issues full-auto pipeline)

---

```yaml
runbook_record:
  runbook_family: WORKFLOW-GITHUB-ISSUES
  runbook_release: 001
  runbook_id: run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  record_kind: ledger-aware-runbook
  status: active
  release_action: identity-and-structure-rewrite
  release_change_summary: First strong-structure rewrite for the GitHub Issues lifecycle family, narrowing family identity and reshaping parent run accounting around batch, target, and target-stage grains.
  summary: Use one stable operator surface for GitHub Issues lifecycle automation with two defended workflow profiles: child issue full lifecycle and parent issue light lifecycle, both bound to explicit run-ledger accounting.
  governance_area: workflow
  applies_to: GitHub Issues lifecycle automation for source logs under docs/logs/, including child issue creation/PR/merge/conclusion and parent issue creation/conclusion.
  entry_surface: script
  evidence_surface: run-ledger
  file_identity_status: legacy-filename-pending-rename
  ledger_binding:
    parent_run_ledger: docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
    supplementary_ledger_series: docs/runbook/support-only/ledger-run-SUP-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
    patch_ledger_series: docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
    minimum_evidence_files:
      - docs/issues/*.json
      - docs/issues/*plan.json
      - docs/issues/*apply-result.json
    minimum_admitted_fields:
      - run_row_id
      - target_row_id
      - target_stage_row_id
      - stage_name
      - stage_status
      - blocking_reason_class
      - planned_action
      - applied_action
      - status
      - warnings
  recorded_at: 2026-04-20
  reviewed_at: pending
  effective_from: 2026-04-20
  effective_until: ongoing
  introduced_by: docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md#P2-C1-S1
  last_changed_by: docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md#P3-C1-S1
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
    - This release keeps the existing file identity for compatibility, but the defended family token is now `WORKFLOW-GITHUB-ISSUES` at contract level.
    - This release now assumes strong-structure parent-run accounting at batch, target, and target-stage grains.
```

---

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

## 4) Run Ledger Binding

### 4.1 Parent ledger

- Canonical parent ledger:
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- Each admitted bounded batch for this first runbook release should be recorded under that ledger's batch, target, and target-stage tables.
- Later completion passes or evidence sharpening for the same bounded batch should normally stay under the same `run_row_id` and attach through `SUP`, not force a new run-ledger sequence.

### 4.1A Support-only supplement and patch ledgers

- Canonical supplement ledgers and patch ledgers for this runbook family should also live under `docs/runbook/support-only/`.
- The first reserved patch-ledger name for this runbook release is:
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`

### 4.2 Run, target, and stage ids

- Stable run-row shape:
  - `RUN-001`, `RUN-002`, ...
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
  - `RUN-001-T01-STG-CREATION-A01`
- Stable evidence-item shape beneath one run row:
  - `RUN-001-E01`, `RUN-001-E02`, ...
- If screenshots, transcripts, or exported review artifacts are needed later, attach them through SUP ledgers using the `RUN-001-SUP-01-ATT-01` style.
- If a bounded repair packet is needed without changing the runbook release, attach it through a PATCH ledger under the same support-only root.

### 4.3 Admission and write-back rule

- A run may enter the parent ledger only when the requested stage emitted at least one durable JSON or Markdown artifact under `docs/issues/` or another explicit retained path.
- If later evidence only sharpens or corrects one admitted run verdict, open a SUP ledger instead of rewriting the original run row invisibly.
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
- Physical file rename or successor-release decisions remain out of scope for this rewrite packet even though the defended family token has narrowed.

## Thinness Rules

- Keep this runbook as one family-level operator surface only.
- Do not copy recurring run rows into the runbook.
- Do not use this runbook to replace the bound run ledger or the source logs.