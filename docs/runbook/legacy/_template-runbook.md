# Runbook template (v1)

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