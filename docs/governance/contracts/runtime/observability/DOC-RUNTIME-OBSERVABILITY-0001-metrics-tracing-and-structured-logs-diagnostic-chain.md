# DOC-RUNTIME-OBSERVABILITY-0001 metrics tracing and structured logs diagnostic chain

```yaml
contract_record:
  contract_family: DOC-RUNTIME-OBSERVABILITY
  contract_release: 0001
  contract_id: DOC-RUNTIME-OBSERVABILITY-0001
  record_kind: chronology-first-contract
  status: draft
  release_action: initial
  release_change_summary: Establish the first runtime observability contract by fixing one current diagnostically complete worker chain, its stable entrypoint, its minimum shared-pivot signal set, and its first defended proof path under S4G-1B, while S4G-1G/P3 keeps later current-family scenarios in bound release-ledger routing instead of widening positive contract meaning beyond the first defended proof path.
  summary: One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence, with the current bounded owner surface fixed to the search outbox projection worker and the current defended proof path fixed to es_write_block_4xx; additional current-family scenarios remain admitted only at the release-ledger layer for now.
  governance_area: runtime observability for bounded worker handling chains
  applies_to: the search outbox projection worker surface, its stable entrypoint, its minimum shared-pivot signal set, and its first defended drill-backed diagnostic proof path
  entrypoint_ref: backend/scripts/search_outbox_worker.py
  parent_ledger_ref: docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md
  attached_row_flow_ledger_ref: docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  enforcement_surface: script
  violation_semantics: warning
  owner_team: ops-runtime
  current_steward: delegated:runtime-observability-contract-maintainer
  approval_state: review-pending
  reviewed_by: pending
  approved_by: pending
  release_ledger_binding:
    parent_release_ledger: docs/governance/contracts/support-only/ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md
    supplementary_ledger_series: docs/governance/contracts/support-only/ledger-SUP-001-DOC-RUNTIME-OBSERVABILITY-0001-scenario-family-intake.md
    patch_ledger_series: docs/governance/contracts/support-only/ledger-PATCH-001-DOC-RUNTIME-OBSERVABILITY-0001-release-ledger-bootstrap.md
    intended_use: release-scoped evidence intake and staged face, evidence, chronology, or release-decision write-back before widening current contract ownership
  recorded_at: 2026-04-26
  reviewed_at: pending
  effective_from: 2026-04-26
  effective_until: ongoing
  introduced_by: docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  last_changed_by: docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md#P3-C1-S2
  source_refs:
    - docs/logs/log-S4G-2B-audited-bridge-coverage-time-window-template-hardening.md
    - docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
  cumulative_source_refs:
    - docs/logs/log-S4G-2B-audited-bridge-coverage-time-window-template-hardening.md
    - docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md
    - docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md
    - docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md
    - docs/logs/log-S3A-2A-2B-daemon-ready-worker-migration.md
    - docs/logs/log-S3A-2A-3B-automated-failure-drills.md
    - docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md
    - docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md
    - docs/logs/log-S6A-1A-stable-entry-contract.md
  supporting_evidence_refs:
    - backend/scripts/search_outbox_worker.py
    - backend/scripts/search_outbox_worker_impl.py
    - backend/infra/observability/outbox_metrics.py
    - backend/infra/observability/tracing.py
    - backend/scripts/cli_app/scenarios/es_write_block_4xx.py
    - docs/labs/lab-S3A-2A-3A-observability-failure-drills.md
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
    - This first release is intentionally narrow and should be read as one runtime-owned observability contract for a single defended worker chain rather than as a repo-wide observability umbrella.
    - The contract is opened only after S4G-1B fixed the weak semantic claim, the search outbox worker boundary, and the first defended proof path through es_write_block_4xx.
    - Fallback, switch, shadow or dual-run, and coexistence-window operator instructions remain downstream runbook material and are not owned by this release yet.
```

  ## Current Governance State

  | governed surface | owner team | current steward | approval state | reviewed by | approved by | notes |
  | --- | --- | --- | --- | --- | --- | --- |
  | `DOC-RUNTIME-OBSERVABILITY-0001` | `ops-runtime` | `delegated:runtime-observability-contract-maintainer` | `review-pending` | `pending` | `pending` | `S4G-2B backfills audited bridge/coverage windows without widening the contract beyond the current search outbox worker diagnostics chain.` |

  ## Current Contract Faces

  | face id | face name | semantic status | semantic strength | current semantic text | code truth kind | primary code refs | supporting refs | source basis | effective from | effective until | recorded at | last changed at | actor | change reason | replacement rule | notes |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-01` | `owner-boundary` | `owned-now` | `defended-now` | The current bounded owner surface for this release is the search outbox projection worker for `projection=search_index_to_elastic`. | `entrypoint` | `backend/scripts/search_outbox_worker.py` | `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` | `S3A-2A-R01-D02` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `Current contract meaning must stay attached to one bounded runtime-owned worker surface.` | `Open a new release if the bounded owner surface changes.` | `This is the family boundary that prevents repo-wide observability drift.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-02` | `stable-entrypoint` | `owned-now` | `defended-now` | The stable entrypoint for the admitted chain is `backend/scripts/search_outbox_worker.py`, with drill-facing identity `search_outbox_worker@v1`. | `entrypoint` | `backend/scripts/search_outbox_worker.py` | `backend/scripts/search_outbox_worker_impl.py; docs/logs/log-S6A-1A-stable-entry-contract.md` | `S3A-2A-R01-D03` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `The contract must name one durable executable attachment point before it can claim current meaning.` | `Open a new release if the stable entrypoint or drill-facing identity changes materially.` | `Switch names remain evidence near this face, not standalone operator procedure.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-03` | `application-bridge` | `partially-owned` | `evidence-supported` | The current contract attaches to one worker chain that runs through the search outbox projection worker, its implementation, and the defended `es_write_block_4xx` scenario path rather than to observability in the abstract. | `domain-flow` | `backend/scripts/search_outbox_worker.py; backend/scripts/search_outbox_worker_impl.py` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `S3A-2A-R01-D02; S3A-2A-R01-D03; S3A-2A-R01-D05` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `The contract needs a bounded application chain, but this first release keeps that bridge narrow.` | `Open a new release if the admitted application bridge changes reader-visible meaning.` | `This is intentionally narrower than a repo-wide runtime observability umbrella.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-04` | `domain-invariants` | `partially-owned` | `evidence-supported` | One admitted runtime handling chain should remain diagnosable through correlated metrics, tracing, and structured logs via shared pivots and auditable evidence. | `domain-flow` | `backend/infra/observability/outbox_metrics.py; backend/infra/observability/tracing.py` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | `S3A-2A-R01-D01; S3A-2A-R01-D04` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `The first release fixes the minimal diagnostic invariant without over-claiming broader runtime guarantees.` | `Open a new release if diagnosability or required pivot correlation changes reader-visible meaning.` | `This is the semantic core of the family.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-05` | `critical-data-shape` | `partially-owned` | `code-anchored` | The current diagnostic shape depends on `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, and worker labels such as `projection` and `op` staying readable across the admitted chain. | `schema-shape` | `backend/scripts/search_outbox_worker_impl.py; backend/scripts/cli_app/scenarios/_failure_drill_shared.py` | `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` | `S3A-2A-R01-D04` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `The release can name the current shared pivots, but later shape refinement may still narrow or widen the defended field set.` | `Open a new release if the minimum current pivot or label set changes.` | `This face is stronger than pure evidence but not yet a broad schema contract.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-06` | `persistence-continuity` | `partially-owned` | `evidence-supported` | The defended proof path must preserve DB reason-family movement and outbox continuity strongly enough that the same run-scoped evidence bundle can connect runtime action to diagnostic outcome. | `domain-flow` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | `S3A-2A-R01-D05` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `The first release defends continuity only as far as the admitted proof path already proves it.` | `Open a new release if the continuity expectation or required evidence bundle changes.` | `This face stays bounded to the defended path, not all persistence semantics in the repo.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-07` | `observability-minimum-set` | `owned-now` | `defended-now` | The current minimum observability set is `outbox_*` metrics, worker tracing spans, and worker structured logs correlated by the admitted shared pivots. | `signal-emission` | `backend/infra/observability/outbox_metrics.py; backend/infra/observability/tracing.py` | `backend/scripts/search_outbox_worker.py; docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | `S3A-2A-R01-D04` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `The contract must state the minimum signal floor that makes the chain diagnosable now.` | `Open a new release if the minimum signal floor changes in reader-visible ways.` | `This release does not claim every available signal is mandatory.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `control-fallback-boundary` | `boundary-only` | `code-anchored` | Fallback, switch, shadow or dual-run, and coexistence-window procedure remain outside current contract ownership even though nearby code and retained runbook surfaces exist. | `config-switch` | `backend/scripts/search_outbox_worker.py` | `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md; docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` | `S3A-2A-R01-D06` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `This release intentionally keeps operator procedure out of the current positive contract.` | `Move to runbook or open a later release only after the operator boundary is separately defended.` | `The existence of switches does not by itself create owned fallback semantics.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-09` | `verification-surface` | `owned-now` | `defended-now` | The first defended verification surface is `es_write_block_4xx`, which must retain worker-start, metrics, result, and worker-log evidence in one run-scoped bundle on the same worker chain. | `verification-hook` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `backend/scripts/cli_app/scenarios/_failure_drill_shared.py; docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | `S3A-2A-R01-D05` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `The release needs one defended proof path rather than a general promise that every scenario is already proven.` | `Open a new release if the defended proof path or minimum evidence bundle changes.` | `Later scenarios may stay in ledgers until they justify widening current meaning.` |

  ## Code Evidence Attachments

  | evidence id | face id | evidence kind | repo ref | symbol or block | observed semantic | confidence | observed at | recorded at | actor | source packet or ledger | notes |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `DOC-RUNTIME-OBSERVABILITY-0001-EVD-01` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-01` | `entrypoint` | `backend/scripts/search_outbox_worker.py` | `search outbox worker entry script` | The admitted owner boundary is a concrete worker surface rather than an abstract observability subsystem. | `high` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D02` | `Primary bounded owner anchor.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-EVD-02` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-02` | `entrypoint` | `backend/scripts/search_outbox_worker_impl.py` | `worker implementation path` | The entrypoint resolves into one durable implementation path behind the admitted worker script. | `medium` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D03` | `Supports stable entrypoint and application bridge faces.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-EVD-03` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-07` | `signal-emission` | `backend/infra/observability/outbox_metrics.py` | `outbox metrics emission` | The worker chain emits the metric surface required by the current observability minimum set. | `high` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D04` | `Metrics are one mandatory part of the minimum signal floor.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-EVD-04` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-07` | `signal-emission` | `backend/infra/observability/tracing.py` | `worker tracing support` | The admitted chain retains tracing anchors that participate in the shared-pivot diagnostic path. | `high` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D04` | `Tracing is current positive contract meaning, not just support-only evidence.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-EVD-05` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-09` | `verification-hook` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `es_write_block_4xx` | The current verification surface is one deterministic defended scenario rather than a broad scenario family guarantee. | `high` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D05; CRL-02-SC-02` | `Primary proof-path anchor.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-EVD-06` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `config-switch` | `backend/scripts/search_outbox_worker.py` | `SEARCH_OUTBOX_WORKER_ENABLED; SEARCH_OUTBOX_RUNNER` | Nearby switches exist, but current contract ownership does not yet defend the operator semantics around them. | `medium` | `2026-04-26` | `2026-04-27` | `role:s4g-packet-maintainer` | `S4G-1D` | `Boundary-only evidence; do not over-read as owned procedure.` |

  ## Semantic Chronology

  | chronology id | face id | change type | semantic before | semantic after | effective from | effective until | observed at | recorded at | actor | basis refs | source release rows | source scenario rows | source routing event ids | chronology order key | notes |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | `DOC-RUNTIME-OBSERVABILITY-0001-CHR-01` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-04` | `introduced` | `none` | `One admitted runtime handling chain must remain diagnosable through correlated metrics, tracing, and structured logs.` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D01` | `CRL-01` | `none` | `none` | `2026-04-26|2026-04-26|2026-04-26|DOC-RUNTIME-OBSERVABILITY-0001-CHR-01` | `Current semantic core introduced with the first release.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-CHR-02` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-01` | `introduced` | `none` | `The current owner boundary is the search outbox projection worker chain.` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D02; S3A-2A-R01-D03` | `CRL-01` | `none` | `none` | `2026-04-26|2026-04-26|2026-04-26|DOC-RUNTIME-OBSERVABILITY-0001-CHR-02` | `The first release fixes the bounded owner and stable entrypoint together.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-CHR-03` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-07` | `introduced` | `none` | `The minimum current signal set is outbox metrics, worker tracing spans, and worker structured logs correlated by shared pivots.` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D04` | `CRL-01` | `none` | `none` | `2026-04-26|2026-04-26|2026-04-26|DOC-RUNTIME-OBSERVABILITY-0001-CHR-03` | `Signal-floor semantics introduced with the first release.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-CHR-04` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-09` | `introduced` | `none` | `The first defended proof path is es_write_block_4xx with one run-scoped evidence bundle.` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D05` | `CRL-01` | `CRL-02-SC-02` | `CRL-02-SC-E02` | `2026-04-26|2026-04-26|2026-04-26|DOC-RUNTIME-OBSERVABILITY-0001-CHR-04` | `The first release remains deliberately proof-path-specific.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-CHR-05` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `introduced` | `none` | `Fallback and switch semantics remain outside current contract ownership.` | `2026-04-26` | `ongoing` | `2026-04-26` | `2026-04-26` | `role:s4g-packet-maintainer` | `S3A-2A-R01-D06` | `CRL-01` | `none` | `none` | `2026-04-26|2026-04-26|2026-04-26|DOC-RUNTIME-OBSERVABILITY-0001-CHR-05` | `This is a deliberate boundary decision, not a missing row.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-CHR-06` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-01` | `backfilled-audit` | `Owner boundary and proof-path rows existed without explicit writeback timing fields.` | `Owner boundary and proof-path rows now carry explicit writeback chronology without widening current meaning.` | `2026-04-26` | `ongoing` | `2026-04-27` | `2026-04-27` | `role:s4g-packet-maintainer` | `docs/logs/log-S4G-2B-audited-bridge-coverage-time-window-template-hardening.md; docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md#P2-C1-S1` | `CRL-01` | `CRL-02-SC-02` | `CRL-02-SC-E02` | `2026-04-26|2026-04-27|2026-04-27|DOC-RUNTIME-OBSERVABILITY-0001-CHR-06` | `Audit sharpening did not change current semantics.` |

  ## Current Gaps and Non-Ownership

  | gap id | related face id | current standing | later owner | current route | notes |
  | --- | --- | --- | --- | --- | --- |
  | `DOC-RUNTIME-OBSERVABILITY-0001-GAP-01` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `boundary-only` | `future runtime-owned runbook bridge or retained gap packet` | `S4G-1D retained gap packet` | `Fallback-mode semantics are still unresolved as reusable operator procedure.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-GAP-02` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `code-anchored` | `future runbook bridge` | `S4G-1D retained gap packet` | `Switch-surface procedure and reversal proof remain outside current contract ownership.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-GAP-03` | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `not-owned-here` | `future runbook verdict or chronology-only retention` | `S4G-1D retained gap packet` | `Coexistence-window and shadow or dual-run semantics are not defended by this release.` |

  ## Release Decision Table

  | face id | current release semantic | candidate semantic | delta class | reader visible change | contract action | decision basis | notes |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-01` | `The bounded owner surface is the search outbox projection worker.` | `Add explicit audit timing and routing linkage for the same owner boundary.` | `evidence-only` | `no` | `same-release-evidence-writeback` | `S4G-2B` | `Audit hardening should not force 0002 by itself.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-07` | `The minimum signal floor is metrics, tracing, and structured logs with shared pivots.` | `Sharpen source timing and evidence references for the same minimum set.` | `evidence-only` | `no` | `same-release-evidence-writeback` | `S4G-2B` | `Evidence sharpening remains same-release.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-09` | `The defended proof path is es_write_block_4xx.` | `Link the existing proof path more explicitly to scenario routing events.` | `evidence-only` | `no` | `same-release-evidence-writeback` | `S4G-1G/P2-C1-S1` | `Scenario routing linkage alone is not a new release.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-08` | `Fallback and switch semantics are outside current ownership.` | `Admit fallback, switch, or coexistence procedure as current positive contract meaning.` | `semantic-change` | `yes` | `move-to-runbook` | `S4G-1C and S4G-1D separation rules` | `If later owned here, it should not arrive as silent same-release drift.` |
  | `DOC-RUNTIME-OBSERVABILITY-0001-FACE-05` | `Current pivots are trace_id or traceparent, claim_batch_id, outbox event id, and worker labels.` | `Change the minimum shared pivot set or required continuity keys.` | `semantic-change` | `yes` | `new-release-required` | `Current face text is reader-visible contract meaning.` | `Data-shape delta should open 0002 rather than hide in evidence-only writeback.` |

  ## Writeback Rules

  - If the bounded owner surface, stable entrypoint, minimum shared pivot set, minimum signal floor, or defended proof path changes in reader-visible ways, open a new release in the `DOC-RUNTIME-OBSERVABILITY` family.
  - If new code or lab material only sharpens existing evidence without changing current face text, write it back through the release ledger and, when useful, append chronology rather than opening a new release.
  - If a change introduces operator procedure for fallback, switch, shadow or dual-run, or coexistence-window handling, route it first to runbook or retained gap surfaces unless the repo can defend that it has become current contract meaning.
  - If new history only clarifies when an existing semantic state was observed or recorded, append chronology and keep the current face text stable.
  - If one later packet changes family boundary rather than only current semantics, prefer a new release plus lineage update or a split-family action instead of widening this release silently.

## Release Change

- This release opens the first runtime observability contract from `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption`.
- The release fixes one current reader that was previously held only in the source log scaffold:
  - the minimum diagnostic chain requirement
  - the bounded owner surface and stable entrypoint
  - the minimum shared pivots and signals
  - the first defended proof path
- This pilot restructures the release around `Current Contract Faces`, `Code Evidence Attachments`, `Semantic Chronology`, and `Release Decision Table` so current semantics, code facts, and change history no longer share one mixed clause or coverage surface.
- This release intentionally does not open a separate runbook bridge packet yet.

## Contract Statement

- One admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence.
- The current bounded owner surface is the `search_index_to_elastic` projection worker with stable entrypoint `backend/scripts/search_outbox_worker.py`.
- The minimum current diagnostic set is `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, `projection/op`, `outbox_*` metrics, worker tracing spans, and worker structured logs.
- The first defended verification surface is `es_write_block_4xx`, with run-scoped evidence that retains worker-start, metrics, result, and worker-log artifacts on the same worker surface.
- Fallback, switch, shadow or dual-run, and coexistence-window procedures remain downstream runbook concerns rather than current contract faces owned by this release.

## Current Reading

- Read this release when the question is `what is the current runtime observability rule for the first defended worker chain under S4G?`
- Read `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` when the question is `which parent row splits and absorbed rows does this contract actually consume?`
- Read `docs/governance/contracts/support-only/ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` when the question is `how should later code/labs/runbook evidence be admitted, deferred, or written back against this current contract release?`
- Read [docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md](d:/Project/wordloom-v3/docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md) when the question is `how was this contract staged, bounded, and proven before release?`
- Read [docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md](d:/Project/wordloom-v3/docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md) when the question is `what operator steps currently exist around the same drill family?`
- Read [docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md](d:/Project/wordloom-v3/docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md) when the question is `what operator semantics are still missing before a narrower runtime-owned runbook bridge can open?`

## Reader Notes

- This family is `runtime` first and `observability` second: observability is the diagnostic subdomain owned under one runtime worker chain here.
- The first release is draft because the proof path is defended, but trace-export completeness and a narrower runbook bridge may still be hardened later.
- Additional current-family scenarios extracted in `S4G-1G` remain visible in the bound contract release ledger, but `P3` explicitly does not promote them into new positive contract clauses until a later proof-path-specific packet justifies that widening.
- The `shadow_*`, `rehearsal_*`, `dual_run_*`, and `dual_write_*` rows visible in the bound release ledger should be read as migration or cutover sibling-lane material, not as latent observability contract clauses.
- Later sibling families should stay under `DOC-RUNTIME-*` when runtime remains the governing owner surface.