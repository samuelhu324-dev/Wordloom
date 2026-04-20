# runbook-template-v2

Use this template when a workflow has become stable enough to deserve one durable operator surface,
but still needs explicit ledger binding for repeated execution, evidence admission, and later audit.
Keep the runbook thin: it owns the operator contract, the allowed entrypoints, and the run-ledger binding.
Do not replay full phase history inside the runbook; link back to logs, contracts, and run ledgers instead.

---

```yaml
runbook_record:
  runbook_family: <WORKFLOW-GITHUB>
  runbook_release: <001>
  runbook_id: <run-WORKFLOW-GITHUB-001-summary>
  record_kind: ledger-aware-runbook
  status: <draft|active|deprecated|superseded|retired>
  release_action: <initial|simple-revision|merge|split-parent|split-child|absorption|consolidation|historical-backfill>
  release_change_summary: <why this runbook release exists and what materially changed>
  summary: <effective operator meaning at this runbook state>
  governance_area: <workflow|ops-runtime|evidence-pipeline|other>
  applies_to: <what operator surface or family this runbook governs>
  entry_surface: <workflow|script|task|dispatch|manual>
  evidence_surface: <summary.json|result.json|run-ledger|other>
  ledger_binding:
    parent_run_ledger: <docs/runbook/ledger-run-001-WORKFLOW-GITHUB-001-summary.md>
    supplementary_ledger_series: <ledger-run-SUP-001-WORKFLOW-GITHUB-001-summary>
    minimum_evidence_files:
      - <summary.json>
      - <result.json>
    minimum_admitted_fields:
      - <result>
      - <failureClass>
  recorded_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  reviewed_at: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown|pending>
  effective_from: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|unknown>
  effective_until: <YYYY-MM-DDTHH:MM:SSZ|YYYY-MM-DD|ongoing|unknown>
  introduced_by: <first decisive source anchor>
  last_changed_by: <most recent source anchor>
  source_refs:
    - <direct decisive source reference for this runbook release>
  cumulative_source_refs:
    - <all source refs carried forward into this runbook's current release state>
  supporting_evidence_refs:
    - <optional retained evidence>
  lineage:
    supersedes:
      - <optional earlier runbook id replaced by this release>
    superseded_by:
      - <optional later runbook id that replaces this release>
    split_from:
      - <optional broader earlier runbook id if this record is a split child>
    split_into:
      - <optional narrower later runbook ids if this record later splits>
    absorbed_from:
      - <optional earlier runbook id whose meaning is partly absorbed here>
    absorbed_into:
      - <optional later runbook id that absorbs meaning from this record>
    retires:
      - <optional earlier runbook id explicitly ended by this release>
    retired_by:
      - <optional later runbook id or decision that retires this record>
  notes:
    - <optional clarification>
```

---

## Naming Rule

- Name runbooks as `run-<RUNBOOK-FAMILY>-<RELEASE>-<summary>.md`.
- `<RUNBOOK-FAMILY>` should follow contract-like long-path grammar and remain stable across revisions.
- `<RELEASE>` is append-only inside one stable runbook family.
- Preferred example shape:
  - `run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`

## Lifecycle Field Rule

- `recorded_at` records when this runbook release entered the repo as a defended operator surface.
- `reviewed_at` records when this runbook release passed defended review; use `pending` when the review has not happened yet.
- `effective_from` and `effective_until` describe the best currently known historical-effective range for this operator surface.
- New values should prefer canonical UTC second timestamps such as `2026-04-20T14:55:00Z`.
- Legacy day-only values may remain where finer audit precision is not defended.

## 1) Purpose

- State the operator goal in one paragraph or 2 to 4 bullets.
- Answer what this runbook helps someone run, verify, recover, inspect, or conclude.

## 2) Scope

- State what is covered.
- State what is explicitly out of scope.
- Link 3 to 7 deeper sources that still own history or contract detail.

## 3) Workflow Contract

### 3.1 Stable entrypoints

- Show the canonical entrypoint.
- List the allowed knobs an operator may change.
- State what the runbook does not permit an operator to improvise.

### 3.2 Success and failure semantics

- Define what counts as `PASS`, `FAIL`, `PASS_AFTER_RECOVERY`, `NOT_RUN`, or equivalent states.
- Point to the exact verdict files or fields that act as source of truth.

## 4) Run Ledger Binding

### 4.1 Parent ledger

- Name the canonical run ledger file for this runbook family.
- State whether each execution appends one new run row or opens a new ledger file.

### 4.2 Run and evidence ids

- Name the stable run-row shape as `RUN-<nnn>` or another defended family-specific format.
- Name the stable evidence-item shape as `E<nn>` or another defended format attached to one run row.
- Name attachment ids explicitly when screenshots, exports, or transcript files need approval-facing review.

### 4.3 Admission and write-back rule

- State the minimum evidence files required before a run may be admitted into the parent run ledger.
- State when a later evidence packet should open a SUP ledger instead of rewriting the original run row directly.
- State where downstream write-back should land: parent ledger, SUP ledger, source log `Evidence`, maintenance log, or another explicit surface.

## 5) Evidence Bundle

### 5.1 Output roots

- List the snapshot, artifact, ledger, or workflow output roots.
- Call out the minimum evidence files that must exist, for example `_result.json`, `_recipe.json`, `_logs/`, `_metrics/`.

### 5.2 Admitted fields

- List the minimum fields the ledger will extract from those evidence files.
- Keep this section short and machine-facing.

## 6) Local or One-click Operation

### 6.1 Prerequisites

- List the minimum runtime, infra, env vars, permissions, and services.

### 6.2 Commands

- Show the default local or one-click command path.
- Prefer one canonical command sequence over many alternatives.
- If there is a Windows-specific example, keep it aligned with repo usage.

## 7) Troubleshooting

- List the 3 to 6 highest-value failure modes.
- For each one, point to the first evidence file, ledger row, or command to inspect.
- Prefer stable symptoms and actions over long explanations.

## 8) Notes and Boundaries

- State what this runbook deliberately does not try to be.
- State when the operator should drop into linked logs, ledgers, labs, or contracts.
- Record the next likely expansion point only if it changes operator expectations.

## Thinness Rules

- Keep one top-level runbook per stable operator family by default.
- Do not turn the runbook into a second source of truth for execution history.
- Do not copy full phase timelines, raw evidence histories, or recurring run rows into the runbook body.
- Put repeated execution accounting in the parent run ledger and later evidence refinement in SUP ledgers.
- If a child phase only supplies contract or implementation detail, link it instead of promoting it to its own runbook.# Runbook template (v1)

Use this template only when a top-level scope already has a stable operator workflow.
Keep the runbook thin: purpose, scope, evidence roots, one-click or local entry,
troubleshooting, and boundaries. Link out to logs, labs, ADRs, and workflows instead
of copying full phase history into the runbook.

---

**id**: `SxY-summary`
**kind**: `runbook`               # log | lab | runbook | adr | note
**title**: `run/SxY-summary`
**status**: `draft`          # draft | stable | archived
**scope**: `SxY`
**decision_date**: `YYYY-MM-DD`
**context_issue**:
  **DoD**: ``
  **Labs**: ``
**decision**: `State the operator-facing decision in one sentence.`
  **positive**: `"Repeatable operator entry", "Machine-verifiable evidence", "Stable troubleshooting path"`
  **negative**: `"Extra maintenance for commands and evidence paths", "Need to keep contracts stable"`
**supersedes**: `null`
**superseded_by**: `null`

---

## 1) Purpose

- State the operator goal in one paragraph or 2 to 4 bullets.
- Answer: what this runbook helps someone run, verify, recover, or inspect.

## 2) Scope

- State what is covered.
- State what is explicitly out of scope.
- Link the 3 to 7 source materials that still hold the deeper history or contracts.

## 3) Evidence Bundle

### 3.1 Output roots

- List the snapshot, artifact, ledger, or workflow output roots.
- Call out the minimum evidence files that must exist, for example `_result.json`, `_recipe.json`, `_logs/`, `_metrics/`.

### 3.2 Summary or ledger

- If the workflow appends to a summary ledger, document the file and the minimum fields.
- If there is no ledger, say where the operator should look instead.

## 4) One-click Automation

Include this section only if there is already a stable one-click entry such as a workflow,
task, wrapper script, or dispatch button.

### 4.1 What it does

- Explain the high-level flow in 3 to 6 bullets.

### 4.2 Operator instructions

- Show the stable entrypoint.
- List the inputs or knobs that an operator is allowed to change.
- State what success and failure look like.

## 5) Local Operation

### 5.1 Prerequisites

- List the minimum runtime, infra, env vars, and services.

### 5.2 Commands

- Show the default local command path.
- Prefer one canonical command sequence over many alternatives.
- If there is a Windows-specific example, keep it aligned with repo usage.

## 6) Troubleshooting

- List the 3 to 6 highest-value failure modes.
- For each one, point to the first evidence file or command to inspect.
- Prefer stable symptoms and actions over long explanations.

## 7) Notes and Boundaries

- State what this runbook deliberately does not try to be.
- State when the operator should drop into linked logs, labs, or ADRs.
- Record the next likely expansion point only if it changes operator expectations.

## Thinness rules

- Keep one top-level runbook per scope by default.
- Do not turn the runbook into a second source of truth.
- Do not copy full phase timelines, taxonomy tables, or raw evidence histories.
- If a child phase only supplies contract or implementation detail, link it instead of promoting it to its own runbook.