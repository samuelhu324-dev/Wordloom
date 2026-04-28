# run-RUNTIME-OBSERVABILITY-001 (Search outbox worker drill-first skeleton)

---

```yaml
runbook_record:
  runbook_family: RUNTIME-OBSERVABILITY
  runbook_release: 001
  runbook_id: run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton
  record_kind: code-first-runbook
  status: draft
  release_action: initial
  release_change_summary: Rewrite the Search runtime observability pilot into the code-first runbook model while preserving the currently admitted 001 semantics, keeping the release-ledger family as the first intake surface, and deferring any 001 versus later split decision to explicit review rather than automatic renumbering.
  summary: Use one bounded Search runtime runbook for the search outbox projection worker that owns explicit worker-disable checkpoints, switch-surface checkpoint and evidence expectations, one defended proof path, a currently admitted current-family scenario registry, and explicit coexistence non-ownership.
  governance_area: ops-runtime
  applies_to: the search outbox projection worker chain for projection=search_index_to_elastic, its currently admitted current-family drill scenarios, and the admitted es_write_block_4xx proof path
  operator_surface_summary: Operators may currently rely on one stable worker entrypoint, bounded switch checkpoints, explicit disable-state boundaries, one defended proof-path recipe, the admitted current-family worker-chain scenario registry listed below, and an explicit statement that coexistence or cutover procedures are not owned here.
  entry_surface: script
  evidence_surface: artifact-bundle
  owner_team: ops-runtime
  current_steward: delegated:runtime-observability-runbook-maintainer
  approval_state: review-pending
  reviewed_by: pending
  approved_by: pending
  release_ledger_binding:
    parent_release_ledger: docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md
    supplementary_ledger_series: docs/runbook/support-only/ledger-runbook-SUP-001-RUNTIME-OBSERVABILITY-001-scenario-family-intake.md
    patch_ledger_series: docs/runbook/support-only/ledger-runbook-PATCH-001-RUNTIME-OBSERVABILITY-001-release-ledger-bootstrap.md
    intended_use: release-scoped code evidence intake, scenario routing, and staged write-back before or alongside run-level accounting
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
  code_evidence_binding:
    required: yes
    stable_entry_refs:
      - backend/scripts/search_outbox_worker.py
      - backend/scripts/cli_app/scenarios/es_write_block_4xx.py
    operator_surface_refs:
      - backend/scripts/search_outbox_worker.py
      - SEARCH_OUTBOX_WORKER_ENABLED
      - SEARCH_OUTBOX_RUNNER
    switch_checkpoint_refs:
      - SEARCH_OUTBOX_WORKER_ENABLED
      - SEARCH_OUTBOX_RUNNER
    disable_boundary_refs:
      - worker-disabled / stop projection updates
      - explicit disable checkpoint
    scenario_registry_ref: "## 5) Scenario Registry"
    evidence_contract_ref: "## 9) Evidence Bundle"
    non_ownership_refs:
      - docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md
      - docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md
      - docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md
    minimum_supported_failure_classes:
      - worker-disabled-boundary
      - switch-surface-change
      - es_write_block_4xx
      - es_429_inject
      - es_down_connect
      - es_timeout
      - es_bulk_partial
      - db_claim_contention
      - stuck_reclaim
      - duplicate_delivery
      - projection_version
      - coexistence-not-owned
    release_gate_required: yes
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
  last_changed_by: docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md#P3-C1-S1
  source_refs:
    - docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md
    - docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md
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
    - This release remains deliberately narrow and should be read as a drill-first Search runtime runbook skeleton rather than a full production fallback playbook.
    - This rewrite changes structure, not the defended release outlet; it does not itself split 001 into 002.
    - The runbook does not yet own platform-grade alternate-path fallback, cross-platform cutover, or mature rollback governance.
```

---

## Current Governance State

| governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton` | `ops-runtime` | `delegated:runtime-observability-runbook-maintainer` | `review-pending` | `pending` | `pending` | `This first skeleton binds the Search runtime runbook to one stable worker entrypoint, bounded switch checkpoints, one defended drill path, a currently admitted current-family scenario registry, and an explicit coexistence boundary without claiming a mature replacement-path fallback.` |

## 1) Purpose

- Give operators one bounded current runbook surface for the Search outbox worker diagnostics lane.
- Standardize the current drill-first runtime surface as explicit operator faces: stable entrypoint, worker-disable boundary, switch-surface checkpoints, evidence expectations, one first defended proof path, and the currently admitted current-family scenario registry.
- Keep the runbook thin by refusing to claim alternate-path fallback, platform-grade cutover, or positive coexistence semantics that current sources do not defend.

## 2) Scope

- Covered:
  - the stable Search outbox worker entrypoint
  - the current switch surfaces `SEARCH_OUTBOX_WORKER_ENABLED` and `SEARCH_OUTBOX_RUNNER`
  - the admitted current-family Search worker scenarios `es_429_inject`, `es_write_block_4xx`, `es_down_connect`, `es_timeout`, `es_bulk_partial`, `db_claim_contention`, `stuck_reclaim`, `duplicate_delivery`, and `projection_version`
  - explicit boundary language for worker-disabled semantics and coexistence non-ownership
- Out of scope:
  - alternate-path fallback or replacement serving paths
  - migration or cutover sibling-lane procedures such as search gate verification, read-switch rehearsal, dual-run, shadow-run, dual-write, or staged coexistence operations
  - production authorization matrix, rollback governance, or platform-grade recovery policy
  - parent run-ledger execution history beyond the reserved binding described below
- Primary source materials:
  - `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md`
  - `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md`
  - `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
  - `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  - `backend/scripts/search_outbox_worker.py`
  - `backend/scripts/cli_app/scenarios/es_write_block_4xx.py`

## 3) Current Operator Faces

| face id | face kind | current operator meaning | code evidence refs | admitted scenario ids | source release row id | current standing | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OF-OBS-01` | `stable-entrypoint` | `The Search runtime observability lane is bound to one stable worker entrypoint for the search outbox projection worker.` | `CEA-OBS-01` | `SC-OBS-01; SC-OBS-02; SC-OBS-03; SC-OBS-05; SC-OBS-06; SC-OBS-07; SC-OBS-08; SC-OBS-09; SC-OBS-10; SC-OBS-11; SC-OBS-12` | `RBL-01` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This face owns the bounded entrypoint only; it does not expand owner surface beyond the current worker chain.` |
| `OF-OBS-02` | `switch-checkpoint-surface` | `Operators may use the explicit enabled and runner switches as bounded checkpoints that require evidence capture when changed.` | `CEA-OBS-02; CEA-OBS-03` | `SC-OBS-01; SC-OBS-02` | `RBL-01` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This face names the real switch surfaces without claiming full cutover or rollback governance.` |
| `OF-OBS-03` | `disable-state-boundary` | `The runbook owns explicit disable-state checkpoint semantics for stopping projection updates on the current worker chain.` | `CEA-OBS-02` | `SC-OBS-01` | `RBL-01` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is a bounded disable-state claim, not proof of an alternate serving path.` |
| `OF-OBS-04` | `proof-path-recipe` | `The first defended drill recipe for this release is es_write_block_4xx through the current worker chain with run, verify, export, and clean steps.` | `CEA-OBS-04; CEA-OBS-05` | `SC-OBS-03` | `RBL-01` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This remains the first defended proof path even though the registry currently admits additional current-family scenarios.` |
| `OF-OBS-05` | `evidence-contract` | `PASS, FAIL, PASS_AFTER_RECOVERY, and NOT_RUN must be defended by emitted artifacts rather than prose-only console output.` | `CEA-OBS-05` | `SC-OBS-01; SC-OBS-02; SC-OBS-03; SC-OBS-05; SC-OBS-06; SC-OBS-07; SC-OBS-08; SC-OBS-09; SC-OBS-10; SC-OBS-11; SC-OBS-12` | `RBL-01` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `The evidence contract is shared across the bounded current-family drill surface.` |
| `OF-OBS-06` | `admitted-scenario-surface` | `This 001 body currently admits the listed current-family worker-chain scenarios as current reader meaning for the same bounded worker lane.` | `CEA-OBS-01; CEA-OBS-04; CEA-OBS-05` | `SC-OBS-03; SC-OBS-05; SC-OBS-06; SC-OBS-07; SC-OBS-08; SC-OBS-09; SC-OBS-10; SC-OBS-11; SC-OBS-12` | `RBL-02` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is the surface later review must classify as same-release, later release, or narrower sibling lane; no split is executed here.` |
| `OF-OBS-07` | `non-ownership-boundary` | `No current positive coexistence, dual-run, dual-write, shadow-run, or staged cutover procedure is owned by this runbook.` | `CEA-OBS-06` | `SC-OBS-04` | `RBL-01` | `not-owned-here` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `Reviewers should not infer sibling-lane procedures from retained history or adjacent release-ledger rows.` |

## 4) Code Evidence Attachments

| evidence id | evidence kind | stable ref | supported face ids | operator meaning supported here | source release row id | source scenario row ids | current standing | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CEA-OBS-01` | `script` | `backend/scripts/search_outbox_worker.py` | `OF-OBS-01; OF-OBS-06` | `The runbook is bound to one stable worker entrypoint and one current worker-chain scenario family.` | `RBL-01` | `none` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This evidence anchors the worker lane without widening beyond the current worker chain.` |
| `CEA-OBS-02` | `env-switch` | `SEARCH_OUTBOX_WORKER_ENABLED` | `OF-OBS-02; OF-OBS-03` | `The runbook owns explicit disable-state checkpoints and evidence expectations when enabling or disabling the worker.` | `RBL-01` | `none` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is a bounded state checkpoint, not an alternate serving-path claim.` |
| `CEA-OBS-03` | `env-switch` | `SEARCH_OUTBOX_RUNNER` | `OF-OBS-02` | `Runner selection may be named as a bounded checkpoint that requires explicit evidence capture when changed.` | `RBL-01` | `none` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This evidence does not own production authorization or rollback policy.` |
| `CEA-OBS-04` | `scenario` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `OF-OBS-04; OF-OBS-06` | `es_write_block_4xx remains the first defended proof path and one admitted scenario within the current worker-chain registry.` | `RBL-01` | `RBL-02-SC-02` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This evidence row preserves the first defended recipe while keeping wider scenario questions explicit.` |
| `CEA-OBS-05` | `artifact-bundle` | `_result.json; _logs/worker-<run_id>.log; labs export bundle` | `OF-OBS-04; OF-OBS-05; OF-OBS-06` | `The pilot depends on emitted evidence bundles for verdicts, proof-path confirmation, and later scenario-level write-back.` | `RBL-01` | `RBL-02-SC-01; RBL-02-SC-02; RBL-02-SC-03; RBL-02-SC-04; RBL-02-SC-05; RBL-02-SC-06; RBL-02-SC-07; RBL-02-SC-08; RBL-02-SC-09` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This evidence contract supports both the initial proof path and the currently admitted scenario registry.` |
| `CEA-OBS-06` | `boundary-note` | `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md; docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | `OF-OBS-07` | `Adjacent history may be cited as non-ownership evidence, but not promoted into current operator procedure here.` | `RBL-01` | `none` | `defended-now` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row keeps coexistence and sibling-lane procedures visible but out of positive ownership.` |

## 5) Scenario Registry

| scenario id | failure class | default system behavior | operator action class | prod relevance | cadence class | evidence minimum | current owned meaning | source release row id | source scenario row ids | recorded at | effective from | effective until | effective status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SC-OBS-01` | `worker-disabled-boundary` | `projection updates stop on the current worker chain` | `bounded-disable-checkpoint` | `pre-change-drill` | `before-risky-change` | `_result.json; worker log; env capture showing enabled and disabled state` | `defended-now` | `RBL-01` | `none` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row owns explicit disable-state checkpoint semantics only; it does not imply an alternate-path fallback.` |
| `SC-OBS-02` | `switch-surface-change` | `current worker behavior follows the selected enabled and runner state` | `checkpoint-and-evidence` | `pre-change-drill` | `before-risky-change` | `_result.json; worker log; explicit capture of switch values or command context` | `defended-now` | `RBL-01` | `none` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row owns bounded checkpoint semantics around the real switch surfaces, not full production cutover policy.` |
| `SC-OBS-03` | `es_write_block_4xx` | `the current worker chain remains diagnosable through one admitted drill path` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-01` | `RBL-02-SC-02` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This is the first defended current drill path for the skeleton and remains the clearest proof-path recipe.` |
| `SC-OBS-05` | `es_429_inject` | `ES throttling and retry pressure remain diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-01` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-06` | `es_down_connect` | `search worker connectivity loss remains diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-03` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-07` | `es_timeout` | `timeout behavior remains diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-04` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-08` | `es_bulk_partial` | `partial bulk outcomes remain diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-05` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-09` | `db_claim_contention` | `claim contention and owner mismatch remain diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-06` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-10` | `stuck_reclaim` | `lease expiry and reclaim behavior remain diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-07` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-11` | `duplicate_delivery` | `duplicate or noop handling remains diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-08` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-12` | `projection_version` | `projection-version drift remains diagnosable on the same worker chain` | `run-verify-export-clean` | `periodic-drill` | `per-release` | `_result.json; worker log; exported evidence bundle` | `defended-now` | `RBL-02` | `RBL-02-SC-09` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `This row is currently admitted in 001, but its long-term outlet remains subject to explicit release review.` |
| `SC-OBS-04` | `coexistence-not-owned` | `no current positive coexistence or dual-run claim is admitted` | `route-to-boundary-note` | `none` | `none` | `boundary note plus S4G-1F reference` | `not-owned-here` | `RBL-01` | `none` | `2026-04-27` | `2026-04-27` | `ongoing` | `in-force` | `Reviewers should not infer shadow, dual-run, or staged cutover semantics from retained history.` |

## 6) Operator Chronology

| chronology id | affected surface ids | change action | actor value | source release row id | source scenario row ids | effective at | recorded at | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OC-OBS-01` | `OF-OBS-01; OF-OBS-02; OF-OBS-03; OF-OBS-04; OF-OBS-05; OF-OBS-07; SC-OBS-01; SC-OBS-02; SC-OBS-03; SC-OBS-04` | `introduced` | `role:s4g-packet-maintainer` | `RBL-01` | `none` | `2026-04-27` | `2026-04-27` | `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md#P6-C1-S1` | `S4G-1F opened the first bounded Search runtime runbook skeleton using disable-state, switch-checkpoint, defended proof-path, evidence-contract, and coexistence-boundary semantics only.` |
| `OC-OBS-02` | `OF-OBS-04; SC-OBS-03` | `history-backfilled` | `role:s4g-packet-maintainer` | `RBL-01` | `RBL-02-SC-02` | `2026-04-27` | `2026-04-27` | `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md#P2-C1-S1` | `S4G-1G/P2 did not widen the proof path, but it backfilled explicit release-ledger linkage for the already-landed es_write_block_4xx recipe.` |
| `OC-OBS-03` | `OF-OBS-06; SC-OBS-05; SC-OBS-06; SC-OBS-07; SC-OBS-08; SC-OBS-09; SC-OBS-10; SC-OBS-11; SC-OBS-12` | `introduced` | `role:s4g-packet-maintainer` | `RBL-02` | `RBL-02-SC-01; RBL-02-SC-03; RBL-02-SC-04; RBL-02-SC-05; RBL-02-SC-06; RBL-02-SC-07; RBL-02-SC-08; RBL-02-SC-09` | `2026-04-27` | `2026-04-27` | `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md#P3-C1-S1` | `S4G-1G/P3 widened the currently admitted current-family scenario surface while leaving support-only and sibling-family scenarios outside the runbook body.` |

## 7) Release Decision Table

| decision id | affected surface ids | current release semantic | candidate semantic | delta class | reader visible change | release action | target release or outlet | decision basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RD-OBS-01` | `OF-OBS-01; OF-OBS-02; OF-OBS-03; OF-OBS-04; OF-OBS-05; OF-OBS-07` | `The pilot already owns bounded worker entrypoint, switch checkpoints, disable-state semantics, one defended proof path, shared evidence contract, and explicit coexistence non-ownership.` | `Rewrite those same semantics into the face-first code-first model.` | `clarification-only` | `no` | `same-release-evidence-writeback` | `run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` | `This packet rewrites structure and keeps the same defended operator meaning for those faces.` | `No release split is justified by template migration alone.` |
| `RD-OBS-02` | `OF-OBS-06; SC-OBS-05; SC-OBS-06; SC-OBS-07; SC-OBS-08; SC-OBS-09; SC-OBS-10; SC-OBS-11; SC-OBS-12` | `This 001 body currently treats the wider current-family worker scenarios as admitted current reader meaning for the same bounded worker lane.` | `If later review concludes those widened scenarios should stand as a newer or narrower reader-facing surface, route them into a later release, narrower title/file split, or sibling lane instead of silently retaining them here.` | `semantic-change` | `yes` | `new-release-required` | `run-RUNTIME-OBSERVABILITY-002-* or narrower sibling lane/file` | `Admitted scenario-surface widening is reader-visible. This row records the gate, but does not execute the split.` | `The outlet remains deferred until explicit review chooses whether 001 should stay widened or split.` |
| `RD-OBS-03` | `OF-OBS-07; SC-OBS-04` | `No positive coexistence, shadow-run, dual-run, dual-write, or staged cutover procedure is currently owned here.` | `If later packets want to admit those procedures as current operator meaning, they must open a later release or sibling lane rather than widening this boundary implicitly.` | `boundary-restructure` | `yes` | `move-to-sibling-lane` | `later sibling lane or later release` | `Non-ownership is itself current reader meaning and cannot be erased by neighboring code or ledger rows.` | `This gate stays in-force even if the 001 scenario surface remains unchanged.` |

## 8) Run Ledger Binding

### 8.1 Parent ledger

- Canonical release-scoped ledger for this runbook release:
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
- This release ledger is where source-log extraction, code-first scenario intake, and later reader-object supplements or patches should land before the runbook body is widened again.
- Use the release-scoped `SUP` and `PATCH` series when the follow-up changes the runbook release object itself rather than one concrete admitted run.
- Use the release-ledger `scenario row id` and `routing event id` surfaces when a later scenario is added, retained outside the runbook, or routed into a sibling lane; do not hide that movement only in prose.

### 8.2 Run and evidence ids

- Reserved canonical parent run ledger for this runbook family:
  - `docs/runbook/support-only/ledger-run-001-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
- That parent ledger is not opened by this packet yet.
- Until the first bounded execution packet opens the ledger, current execution evidence should remain in run-scoped artifact bundles plus source-log `Evidence` blocks.
- Stable run-row shape:
  - `RUN-001`, `RUN-002`, ...
- Stable evidence-item shape beneath one run row:
  - `RUN-001-E01`, `RUN-001-E02`, ...
- Stable attachment shape for later supplements:
  - `RUN-001-SUP-01-ATT-01`

### 8.3 Admission and write-back rule

- Minimum evidence before a future run may be admitted into the parent ledger:
  - `_result.json`
  - worker log
  - exported evidence bundle or equivalent logs or metrics export
- If later evidence sharpens this runbook release without yet belonging to one admitted run, prefer the release-scoped `ledger-runbook-*` family first.
- If later evidence only sharpens one previously admitted run, prefer a `SUP` ledger rather than rewriting the original run row.
- If a bounded repair packet changes one admitted run without changing release identity, prefer a `PATCH` ledger.
- Downstream write-back for the current packet lands in:
  - this runbook body for current operator meaning
  - `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md` for source-packet evidence and gate traceability
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` for release-scoped intake and staged write-back

## 9) Evidence Bundle

### 9.1 Output roots

- Minimum run-scoped output roots should include:
  - the labs run output directory for `es_write_block_4xx`
  - `_result.json`
  - `_logs/worker-<run_id>.log` or equivalent worker-log path
  - exported bundle from `labs export` when export is run

### 9.2 Admitted fields

- Minimum fields this runbook expects future ledger extraction to preserve:
  - `scenario`
  - `run_id`
  - `status`
  - `worker_entry_id`
  - `switch_surfaces`
  - `worker_log_path`
  - `evidence_root`

## 10) Local or One-click Operation

### 10.1 Prerequisites

- Docker engine running
- backend Python environment installed
- `.env.test` available when using the labs path
- required infra available through compose for the chosen drill run

### 10.2 Commands

- Canonical worker entrypoint:
  - `python backend/scripts/search_outbox_worker.py`
- Canonical drill command sequence for the current defended proof path:
  - `python backend/scripts/cli.py labs run es_write_block_4xx --env-file .env.test --duration 25 --run-id <run_id>`
  - `python backend/scripts/cli.py labs verify es_write_block_4xx --run-id <run_id>`
  - `python backend/scripts/cli.py labs export es_write_block_4xx --run-id <run_id> --lookback 30m`
  - `python backend/scripts/cli.py labs clean es_write_block_4xx --env-file .env.test --keep-last 20`
- The same labs `run -> verify -> export -> clean` shape is the default execution family for the current-family scenarios admitted in the registry above; `es_write_block_4xx` remains the first defended proof path rather than the only admitted scenario.
- Allowed operator knobs are the explicit current switch surfaces only:
  - `SEARCH_OUTBOX_WORKER_ENABLED`
  - `SEARCH_OUTBOX_RUNNER`

## 11) Troubleshooting

- worker exits immediately:
  - inspect `SEARCH_OUTBOX_WORKER_ENABLED` first; a disabled worker is a bounded explicit state on this runbook, not always a defect
- worker refuses the runner setting:
  - inspect `SEARCH_OUTBOX_RUNNER`; current valid values remain `legacy` or `harness`
- verify or export evidence looks incomplete:
  - inspect `_result.json`, the worker log, and the export bundle before inferring broader runtime failure
- someone asks whether the runbook already owns dual-run or replacement-path fallback:
  - stop and read the boundary notes below plus `S4G-1F`; those semantics are not owned here

## 12) Notes and Boundaries

- This runbook is the first bounded Search runtime observability skeleton, not a complete production fallback or cutover playbook.
- The runbook currently owns explicit disable-state checkpoints, switch-surface checkpoint and evidence expectations, one first defended proof path, the currently admitted current-family worker-chain scenario registry, and explicit coexistence non-ownership.
- The runbook does not currently own:
  - alternate-path fallback semantics
  - migration or cutover sibling-lane semantics such as search gate verification, read-switch rehearsal, shadow-run, dual-run, dual-write, or staged coexistence operations
  - production-grade rollback authority or cross-platform recovery governance
- When the bound release ledger shows `shadow_*`, `rehearsal_*`, `dual_run_*`, or `dual_write_*` rows, read them as visible non-owned sibling-lane routing rather than as hidden extra runbook scope.
- This rewrite does not itself decide whether the widened current-family scenario surface should stay inside 001 or move elsewhere later. That decision remains an explicit release-gate question.
- Read `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md` when the question is `why are these semantics bounded this way and what still remains future ownership?`
- Read `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` when the question is `what current contract meaning is already defended for the same worker chain?`
- Read `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` when the question is `what broader historical drill family still exists outside this narrower current-owned skeleton?`