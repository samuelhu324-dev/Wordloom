# run-WORKFLOW-GITHUB-001 (GitHub Issues full-auto pipeline)

---

```yaml
runbook_record:
  runbook_family: WORKFLOW-GITHUB
  runbook_release: 001
  runbook_id: run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
  record_kind: ledger-aware-runbook
  status: active
  release_action: initial
  release_change_summary: First contract-like runbook release for the GitHub issue lifecycle pipeline across issue creation, PR creation, and post-merge issue conclusion.
  summary: Use one stable operator surface for the GitHub lifecycle chain `issue creation -> PR creation -> human merge -> issue conclusion`, with explicit run-ledger accounting for each admitted run.
  governance_area: workflow
  applies_to: GitHub issue and PR lifecycle automation for logs under docs/logs/
  entry_surface: script
  evidence_surface: run-ledger
  ledger_binding:
    parent_run_ledger: docs/runbook/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md
    supplementary_ledger_series: ledger-run-SUP-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline
    minimum_evidence_files:
      - docs/issues/*.json
      - docs/issues/*plan.json
      - docs/issues/*apply-result.json
    minimum_admitted_fields:
      - planned_action
      - applied_action
      - status
      - warnings
  recorded_at: 2026-04-20
  reviewed_at: pending
  effective_from: 2026-04-20
  effective_until: ongoing
  introduced_by: docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md#P2-C1-S1
  last_changed_by: docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md#P2-C1-S1
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
    - This release defines the first family-level runbook surface only; it does not claim that a live full-auto run has already been executed.
```

---

## 1) Purpose

- Give operators one stable surface for the GitHub lifecycle chain across issue creation, PR creation, human merge, and post-merge issue conclusion.
- Bind that operator surface to one explicit run-ledger family so repeated executions are auditable and extractable instead of being left only in raw artifacts or source-log evidence blocks.
- Keep the runbook thin: it owns entrypoints, semantics, and admission rules, while repeated run history belongs in the bound run ledger.

## 2) Scope

- Covered:
  - issue draft generation and real issue creation
  - PR-prep, PR creation, development-link and relationship attachment follow-up
  - review-hold, resume-after-review, and full-auto lifecycle orchestration
  - post-merge issue conclusion write-back
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
- The stable lifecycle order is:
  - issue creation
  - PR creation
  - human review and merge
  - issue conclusion

### 3.2 Success and failure semantics

- `PASS` means the requested lifecycle stage completed and the corresponding artifact or GitHub-side state is present.
- `FAIL` means the requested stage was attempted but blocked or rejected with a traceable reason.
- `NOT_RUN` means the stage was intentionally not attempted in the current mode.
- `PASS_AFTER_REVIEW_RESUME` is valid when the initial run stopped in `review-hold` and a later explicit resume completed the downstream stage set.
- The source-of-truth verdict fields live in the emitted plan/apply JSON artifacts, not in prose-only console output.

## 4) Run Ledger Binding

### 4.1 Parent ledger

- Canonical parent ledger:
  - `docs/runbook/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- Each admitted execution round for this first runbook release should be appended under that ledger's run/evidence tables until a later log proves that a new ledger sequence is warranted.

### 4.2 Run and evidence ids

- Stable run-row shape:
  - `RUN-001`, `RUN-002`, ...
- Stable evidence-item shape beneath one run row:
  - `RUN-001-E01`, `RUN-001-E02`, ...
- If screenshots, transcripts, or exported review artifacts are needed later, attach them through SUP ledgers using the `RUN-001-SUP-01-ATT-01` style.

### 4.3 Admission and write-back rule

- A run may enter the parent ledger only when the requested stage emitted at least one durable JSON or Markdown artifact under `docs/issues/` or another explicit retained path.
- If later evidence only sharpens or corrects one admitted run verdict, open a SUP ledger instead of rewriting the original run row invisibly.
- Downstream write-back should stay explicit:
  - source-log `Evidence` for packet-level conclusion
  - parent run ledger for repeated execution accounting
  - SUP ledger for later evidence refinement
  - maintenance or patch lanes only for bounded local fixes that do not reopen runbook semantics

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

## Thinness Rules

- Keep this runbook as one family-level operator surface only.
- Do not copy recurring run rows into the runbook.
- Do not use this runbook to replace the bound run ledger or the source logs.