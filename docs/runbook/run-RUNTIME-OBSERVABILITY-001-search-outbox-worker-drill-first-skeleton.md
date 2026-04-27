# run-RUNTIME-OBSERVABILITY-001 (Search outbox worker drill-first skeleton)

---

```yaml
runbook_record:
  runbook_family: RUNTIME-OBSERVABILITY
  runbook_release: 001
  runbook_id: run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton
  record_kind: ledger-aware-runbook
  status: draft
  release_action: initial
  release_change_summary: Open the first bounded Search runtime observability runbook skeleton from S4G-1F using only confirmed disable-state fallback, switch-surface checkpoint, and coexistence exclusion semantics.
  summary: Use one drill-first runbook skeleton for the search outbox projection worker that owns explicit worker-disable checkpoints, switch-surface checkpoint/evidence expectations, one defended drill path, and an explicit coexistence non-ownership boundary.
  governance_area: runtime observability operator surface for the search outbox projection worker
  applies_to: the search outbox projection worker chain for projection=search_index_to_elastic and the admitted es_write_block_4xx drill family
  entry_surface: script
  evidence_surface: artifact-bundle
  owner_team: ops-runtime
  current_steward: delegated:runtime-observability-runbook-maintainer
  approval_state: review-pending
  reviewed_by: pending
  approved_by: pending
  file_identity_status: canonical-filename-active
  release_ledger_binding:
    parent_release_ledger: docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md
    supplementary_ledger_series: docs/runbook/support-only/ledger-runbook-SUP-001-RUNTIME-OBSERVABILITY-001-scenario-family-intake.md
    patch_ledger_series: docs/runbook/support-only/ledger-runbook-PATCH-001-RUNTIME-OBSERVABILITY-001-release-ledger-bootstrap.md
    intended_use: release-scoped evidence intake and staged scenario or boundary write-back before widening the runbook body
  ledger_binding:
    parent_run_ledger: docs/runbook/support-only/ledger-run-001-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md
    supplementary_ledger_series: docs/runbook/support-only/ledger-run-SUP-001-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md
    patch_ledger_series: docs/runbook/support-only/ledger-run-PATCH-001-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md
    minimum_evidence_files:
      - _result.json
      - _logs/worker-<run_id>.log
      - labs export bundle or equivalent log/metrics export
    minimum_admitted_fields:
      - scenario
      - run_id
      - status
      - worker_entry_id
      - switch_surfaces
      - worker_log_path
      - evidence_root
  code_bridge_binding:
    required: yes
    stable_entry_refs:
      - backend/scripts/search_outbox_worker.py
      - backend/scripts/cli_app/scenarios/es_write_block_4xx.py
    operator_surface_refs:
      - SEARCH_OUTBOX_WORKER_ENABLED
      - SEARCH_OUTBOX_RUNNER
    scenario_registry_ref: "## 3.5 Scenario Registry / Coverage"
    fallback_surface_refs:
      - worker-disabled / stop projection updates
      - explicit disable checkpoint
      - no alternate-path fallback claim
    evidence_contract_ref: "## 5) Evidence Bundle"
    minimum_supported_failure_classes:
      - worker-disabled-boundary
      - switch-surface-change
      - es_write_block_4xx
      - coexistence-not-owned
    coverage_table_required: yes
  template_authority:
    family_runbook_template: docs/runbook/_template-runbook.md
    family_parent_ledger_template: docs/runbook/support-only/_template-run-ledger.md
    family_supplement_template: docs/runbook/support-only/_template-run-ledger-SUP.md
    family_patch_template: docs/runbook/support-only/_template-run-ledger-PATCH.md
    family_release_ledger_template: docs/runbook/support-only/_template-runbook-release-ledger.md
    family_release_supplement_template: docs/runbook/support-only/_template-runbook-release-ledger-SUP.md
    family_release_patch_template: docs/runbook/support-only/_template-runbook-release-ledger-PATCH.md
  recorded_at: 2026-04-27
  reviewed_at: pending
  effective_from: 2026-04-27
  effective_until: ongoing
  introduced_by: docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md#P6-C1-S1
  last_changed_by: docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md
  source_refs:
    - docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md
    - docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md
    - docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md
  cumulative_source_refs:
    - docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md
    - docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md
    - docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md
    - docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md
    - backend/scripts/search_outbox_worker.py
    - backend/scripts/cli_app/scenarios/_failure_drill_shared.py
    - backend/scripts/cli_app/scenarios/es_write_block_4xx.py
  supporting_evidence_refs:
    - backend/scripts/search_outbox_worker.py
    - backend/scripts/cli_app/scenarios/_failure_drill_shared.py
    - backend/scripts/cli_app/scenarios/es_write_block_4xx.py
    - docs/logs/log-S4G-2B-audited-bridge-coverage-time-window-template-hardening.md
  lineage:
    supersedes: []
    superseded_by: []
    split_from: []
    split_into: []
    absorbed_from: []
    absorbed_into: []
    retires: []
    retired_by: []
  notes:
    - This release is deliberately narrow and should be read as a drill-first Search runtime runbook skeleton rather than a full production fallback playbook.
    - The runbook owns disable-state checkpoints, switch-surface checkpoint/evidence expectations, and explicit coexistence non-ownership only.
    - The runbook does not yet own platform-grade alternate-path fallback, cross-platform cutover, or mature rollback governance.
```

---

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton` | `ops-runtime` | `delegated:runtime-observability-runbook-maintainer` | `review-pending` | `pending` | `pending` | `This first skeleton binds the Search runtime runbook to the current worker entrypoint, bounded switch checkpoints, one defended drill path, and an explicit coexistence boundary without claiming a mature replacement-path fallback.` |

## 1) Purpose

- Give operators one bounded current runbook surface for the search outbox worker diagnostics lane.
- Standardize the current drill-first runtime skeleton: stable entrypoint, explicit worker-disable boundary, switch-surface checkpoints, evidence expectations, and one admitted drill path.
- Keep the runbook thin by refusing to claim alternate-path fallback, platform-grade cutover, or positive coexistence semantics that current sources do not defend.

## 2) Scope

- Covered:
  - the stable search outbox worker entrypoint
  - the current switch surfaces `SEARCH_OUTBOX_WORKER_ENABLED` and `SEARCH_OUTBOX_RUNNER`
  - the admitted `es_write_block_4xx` drill path
  - explicit boundary language for worker-disabled fallback semantics and coexistence non-ownership
- Out of scope:
  - alternate-path fallback or replacement serving paths
  - dual-run, shadow-run, or staged coexistence procedures
  - production authorization matrix, rollback governance, or platform-grade recovery policy
  - parent run-ledger execution history beyond the reserved binding described below
- Primary source materials:
  - `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md`
  - `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
  - `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  - `backend/scripts/search_outbox_worker.py`
  - `backend/scripts/cli_app/scenarios/es_write_block_4xx.py`

## 3) Workflow Contract

### 3.1 Stable entrypoints

- Canonical worker entrypoint:
  - `python backend/scripts/search_outbox_worker.py`
- Canonical drill command sequence for the current admitted proof path:
  - `python backend/scripts/cli.py labs run es_write_block_4xx --env-file .env.test --duration 25 --run-id <run_id>`
  - `python backend/scripts/cli.py labs verify es_write_block_4xx --run-id <run_id>`
  - `python backend/scripts/cli.py labs export es_write_block_4xx --run-id <run_id> --lookback 30m`
  - `python backend/scripts/cli.py labs clean es_write_block_4xx --env-file .env.test --keep-last 20`
- Allowed operator knobs are the explicit current switch surfaces only:
  - `SEARCH_OUTBOX_WORKER_ENABLED`
  - `SEARCH_OUTBOX_RUNNER`
- This runbook does not permit an operator to improvise alternate serving paths, dual-run modes, or platform cutover semantics that are not explicitly owned here.

### 3.2 Success and failure semantics

- `PASS` means the admitted drill path completed and the required evidence bundle exists, including `_result.json` plus worker-log evidence.
- `FAIL` means the drill path ran but expected evidence, expected verification, or expected worker-state behavior was missing or contradictory.
- `PASS_AFTER_RECOVERY` is valid when the worker-disable checkpoint was entered and later restored with explicit evidence of both states.
- `NOT_RUN` means the skeleton was consulted but the bounded drill path was intentionally not executed.
- The source-of-truth verdict fields remain the emitted drill artifacts and run-scoped evidence bundle, not prose-only console output.

### 3.3 Code Bridge Table

| bridge id | surface kind | stable ref | operator meaning owned here | current standing | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RB-OBS-01` | `script` | `backend/scripts/search_outbox_worker.py` | `The current runtime observability lane is bound to one stable worker entrypoint for the search outbox projection worker.` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row owns the bounded entrypoint only; it does not expand owner surface beyond the current worker chain.` |
| `RB-OBS-02` | `env-switch` | `SEARCH_OUTBOX_WORKER_ENABLED` | `The runbook owns explicit worker-disable checkpoints and evidence expectations for entering or leaving the disable-state boundary.` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is disable-state fallback semantics, not a claim that another equivalent serving path automatically takes over.` |
| `RB-OBS-03` | `env-switch` | `SEARCH_OUTBOX_RUNNER` | `The runbook may name runner selection as a bounded operator checkpoint that requires explicit evidence capture when changed.` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row does not own full production authorization or rollback governance.` |
| `RB-OBS-04` | `scenario` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py; search_outbox_worker@v1` | `The admitted drill-first proof path for this release is the es_write_block_4xx scenario running against the current worker chain.` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is the first defended evidence path for the runbook skeleton.` |

### 3.4 Runbook Bridge Evolution Table

| bridge change id | affected bridge ids | change action | actor value | effective at | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RB-OBS-CH-01` | `RB-OBS-01; RB-OBS-02; RB-OBS-03; RB-OBS-04` | `introduced` | `role:s4g-packet-maintainer` | `2026-04-27` | `2026-04-27` | `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md#P6-C1-S1` | `S4G-1F opened the first bounded Search runtime runbook skeleton using only the semantics confirmed through P1-P5.` |

### 3.5 Scenario Registry / Coverage

| scenario id | failure class | default system behavior | operator action class | prod relevance | cadence class | evidence minimum | coverage class | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SC-OBS-01` | `worker-disabled-boundary` | `projection updates stop on the current worker chain` | `bounded-disable-checkpoint` | `pre-change-drill` | `before-risky-change` | `_result.json; worker log; env capture showing enabled/disabled state` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row owns explicit disable-state checkpoint semantics only; it does not imply an alternate-path fallback.` |
| `SC-OBS-02` | `switch-surface-change` | `current worker behavior follows the selected enabled/runner state` | `checkpoint-and-evidence` | `pre-change-drill` | `before-risky-change` | `_result.json; worker log; explicit capture of switch values or command context` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row owns bounded checkpoint semantics around the real switch surfaces, not full production cutover policy.` |
| `SC-OBS-03` | `es_write_block_4xx` | `the current worker chain remains diagnosable through one admitted drill path` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is the first defended current drill path for the skeleton.` |
| `SC-OBS-04` | `coexistence-not-owned` | `no current positive coexistence or dual-run claim is admitted` | `route-to-boundary-note` | `none` | `none` | `boundary note plus S4G-1F reference` | `not-owned-here` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `Reviewers should not infer shadow, dual-run, or staged cutover semantics from retained history.` |

### 3.6 Runbook Coverage Evolution Table

| coverage change id | affected coverage ids | change action | actor value | effective at | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SC-OBS-CH-01` | `SC-OBS-01; SC-OBS-02; SC-OBS-03; SC-OBS-04` | `introduced` | `role:s4g-packet-maintainer` | `2026-04-27` | `2026-04-27` | `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md#P6-C1-S1` | `S4G-1F opened the first Search runtime runbook coverage rows using only bounded disable-state, switch-checkpoint, defended drill-path, and coexistence-boundary semantics.` |

## 4) Release and Run Ledger Binding

### 4.1 Release ledger

- Canonical release-scoped ledger for this runbook release:
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
- This release ledger is where source-log extraction, code-first scenario intake, and later reader-object supplements or patches should land before the runbook body is widened.
- Use the release-scoped `SUP` / `PATCH` series when the follow-up changes the runbook release object itself rather than one concrete admitted run.

### 4.2 Parent run ledger

- Reserved canonical parent ledger for this runbook family:
  - `docs/runbook/support-only/ledger-run-001-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
- That parent ledger is not opened by this packet yet.
- Until the first bounded execution packet opens the ledger, current execution evidence should remain in run-scoped artifact bundles plus source-log `Evidence` blocks.

### 4.3 Run and evidence ids

- Stable run-row shape:
  - `RUN-001`, `RUN-002`, ...
- Stable evidence-item shape beneath one run row:
  - `RUN-001-E01`, `RUN-001-E02`, ...
- Stable attachment shape for later supplements:
  - `RUN-001-SUP-01-ATT-01`

### 4.4 Admission and write-back rule

- Minimum evidence before a future run may be admitted into the parent ledger:
  - `_result.json`
  - worker log
  - exported evidence bundle or equivalent logs/metrics export
- If later evidence sharpens this runbook release without yet belonging to one admitted run, prefer the release-scoped `ledger-runbook-*` family first.
- If later evidence only sharpens one previously admitted run, prefer a `SUP` ledger rather than rewriting the original run row.
- If a bounded repair packet changes one admitted run without changing release identity, prefer a `PATCH` ledger.
- Downstream write-back for the current packet lands in:
  - this runbook body for current operator meaning
  - `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md` for source-packet evidence and gate traceability
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` for release-scoped intake and staged write-back

## 5) Evidence Bundle

### 5.1 Output roots

- Minimum run-scoped output roots should include:
  - the labs run output directory for `es_write_block_4xx`
  - `_result.json`
  - `_logs/worker-<run_id>.log` or equivalent worker-log path
  - exported bundle from `labs export` when export is run

### 5.2 Admitted fields

- Minimum fields this runbook expects future ledger extraction to preserve:
  - `scenario`
  - `run_id`
  - `status`
  - `worker_entry_id`
  - `switch_surfaces`
  - `worker_log_path`
  - `evidence_root`

## 6) Local or One-click Operation

### 6.1 Prerequisites

- Docker engine running
- backend Python environment installed
- `.env.test` available when using the labs path
- required infra available through compose for the chosen drill run

### 6.2 Commands

- Run:
  - `python backend/scripts/cli.py labs run es_write_block_4xx --env-file .env.test --duration 25 --run-id <run_id>`
- Verify:
  - `python backend/scripts/cli.py labs verify es_write_block_4xx --run-id <run_id>`
- Export:
  - `python backend/scripts/cli.py labs export es_write_block_4xx --run-id <run_id> --lookback 30m`
- Clean:
  - `python backend/scripts/cli.py labs clean es_write_block_4xx --env-file .env.test --keep-last 20`

## 7) Troubleshooting

- worker exits immediately:
  - inspect `SEARCH_OUTBOX_WORKER_ENABLED` first; a disabled worker is a bounded explicit state on this runbook, not always a defect
- worker refuses the runner setting:
  - inspect `SEARCH_OUTBOX_RUNNER`; current valid values remain `legacy` or `harness`
- verify or export evidence looks incomplete:
  - inspect `_result.json`, the worker log, and the export bundle before inferring broader runtime failure
- someone asks whether the runbook already owns dual-run or replacement-path fallback:
  - stop and read the boundary note below plus `S4G-1F`; those semantics are not owned here

## 8) Notes and Boundaries

- This runbook is the first bounded Search runtime observability skeleton, not a complete production fallback or cutover playbook.
- The runbook owns explicit disable-state checkpoints, switch-surface checkpoint/evidence expectations, and one defended drill path.
- The runbook does not currently own:
  - alternate-path fallback semantics
  - shadow-run, dual-run, or staged coexistence semantics
  - production-grade rollback authority or cross-platform recovery governance
- Read `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md` when the question is `why are these semantics bounded this way and what still remains future ownership?`
- Read `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` when the question is `what current contract meaning is already defended for the same worker chain?`
- Read `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` when the question is `what broader historical drill family still exists outside this narrower current-owned skeleton?`