# log-S4G-1B (Phase 2: R01 runtime observability governance contract bridge)

---

**id**: `S4G-1B`
**kind**: `log`
**title**: `R01 runtime observability governance contract bridge and drill path v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Observability, Drills, ContractBridge, Evidence, epic/s4, sub/1b`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/562`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/563`
  **runbook**: `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  **attached_ledger**: `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4G-1A-s4-history-extraction-and-code-first-fallback-cells-assessment.md`
  **previous_log**: `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`
  **reference_log_1**: `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`
  **reference_log_2**: `docs/logs/log-S4D-cloud-runtime-deploy-verify-rollback.md`
  **reference_log_3**: `docs/logs/log-S6A-1A-stable-entry-contract.md`
  **reference_log_4**: `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
**issue_keyword**: `runtime`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
**roadmap_milestone**: `M1`
**roadmap_phase**: `M1-P2`
**roadmap_bridge_refs**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md#M1-P2`
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-26`
**updated**: `2026-04-28`
**reviewed**: `pending`
**source_reader_model**: `mixed-source-v1`
**extraction_surface_version**: `extractable-rules-v1`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this lane.
- These lifecycle fields do not claim semantic-effective dates for the historical runtime behavior being reviewed.
- `reviewed` should remain `pending` until the first narrow `R01` contract-bridge packet has one explicit boundary and drill verdict.

## Decision / Outcome

**Decision**:

- Open `S4G-1B` as the first narrow child-opening packet under `S4G-1A` for `S3A-2A-R01`.
- Treat `R01` as a doc-level `runtime observability governance` contract-opening candidate, but keep `code boundary`, `entrypoint`, `drill proof`, and `runbook bridge` explicit in the same scaffold before any released contract mutation.
- Keep `S4G-1B` as the decision and evolution surface only once row split or absorption begins; any durable derived-row accounting beneath `S3A-2A-R01` should move into one attached parent-ledger row-flow ledger instead of staying only in this log.

**Default choices (phase defaults / v1)**:

- The first normalized contract claim is: one admitted runtime handling chain should remain diagnosable through `metrics -> tracing -> structured logs` via shared pivots and auditable evidence.
- `contract` owns the current semantic rule, not the operator click path and not the source-history prose.
- `bridge-to-code` must name one bounded runtime surface before this lane can claim a current contract release.
- `drills` prove the contract is alive, but drill evidence does not replace the contract statement itself.
- `runbook` should later own `fallback`, `shadow/dual-run`, `switch surface`, and `coexistence window` instructions once the entrypoint is defended.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## Extractable Rule Surface (recommended)

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | accounting status | final handoff | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `Decision / Outcome` | `contract-candidate` | One admitted runtime handling chain should remain diagnosable through `metrics -> tracing -> structured logs` via shared pivots and auditable evidence. | `contract` | `ready` | `RG-01` | `S3A-2A-R01` | `repeated-to-attached-ledger` | `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption -> S3A-2A-R01-D01` | This is the minimum falsifiable contract claim for the row, but durable accounting now lives in the attached ledger. |
| `R02` | `Default choices` bullets 2-4 | `contract-candidate` | Before release mutation, the lane must name one bounded runtime surface, one candidate entrypoint, and one minimum bridge field set for the contract to attach to code. | `contract` | `ready` | `RG-01` | `S3A-2A-R01`; `docs/logs/log-S6A-1A-stable-entry-contract.md` | `repeated-to-attached-ledger` | `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption -> S3A-2A-R01-D02; S3A-2A-R01-D03; S3A-2A-R01-D04` | This row fixes the missing applied-to-surface bridge, but no longer acts as the durable downstream source by itself. |
| `R03` | `Default choices` bullets 4-5 | `contract-candidate` | A current observability contract must declare whether one deterministic drill or gate proves the chain, or explicitly record that proof is still missing. | `contract` | `ready` | `RG-02` | `S3A-2A-R03`; `S3A-2A-R04`; `S3A-2A-R08`; `S3A-2A-R10` | `repeated-to-attached-ledger` | `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption -> S3A-2A-R01-D05` | Drill binding belongs in the contract as proof semantics, while durable split or absorption accounting now lives in the attached ledger. |
| `R04` | `Default choices` bullet 5 | `runbook-candidate` | Once the entrypoint is defended, one runbook surface should own fallback, switch, shadow or dual-run, and coexistence-window instructions for that same chain. | `runbook` | `ready` | `RG-02` | `S3A-2A-R13` | `repeated-to-attached-ledger` | `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption -> S3A-2A-R01-D06` | Runbook is downstream from the contract bridge, not a substitute for it. |
| `R05` | `Constraints` | `support-only` | Until one entrypoint and minimum proof path are named, this packet remains a scaffold-only bridge and must not be overstated as an active runtime release. | `support-only` | `ready` | `none` | `S4G-1A` | `retained-in-s4g-1b` | `S4G-1B constraints only` | Anti-fabrication guard for the first narrow packet. |
| `R06` | `P3-C2-S1` | `handoff-decision` | When one parent-ledger row must split into multiple derived rows before downstream release mutation is reviewable, durable accounting should move into one attached row-flow ledger rather than remain only in `S4G-1B`. | `log-retained core` | `ready` | `RG-03` | `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` | `still-live-in-s4g-1b` | `opens attached row-flow ledger as current split-accounting surface` | This row is new lane-owned decision content from `P3-C2`; it should stay live here because it is about handoff policy, not derived-row meaning itself. |
| `R07` | `P3-C2-S2` | `handoff-writeback` | `S3A-2A-R01` should remain the packet root in the parent ledger, but its current downstream reading should now be written back through the attached row-flow ledger. | `log-retained core` | `ready` | `RG-03` | `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`; `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` | `still-live-in-s4g-1b` | `parent ledger now records partial consumption through attached ledger` | This row is the lane-owned write-back decision that explains why the parent ledger changed without making the parent row disappear. |
| `R08` | `P3-C2-S3` | `source-repair-decision` | `DOC-RUNTIME-OBSERVABILITY-0001` should cite the attached row-flow ledger as its direct source basis, with `S4G-1B` retained as decision lineage rather than primary release provenance. | `log-retained core` | `ready` | `RG-03` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`; `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md` | `still-live-in-s4g-1b` | `contract clause basis now reads through S3A-2A-R01-D01 through D06` | This row stays live here because provenance repair is a control-lane decision even after the contract and attached ledger become the durable reader surfaces. |

### Shared Reason Groups (optional, recommended when multiple rows share one rationale)

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | `R01` is strong enough to open a contract candidate only if the semantic claim and code boundary are declared together. | `S3A-2A-R01`; `docs/logs/log-S6A-1A-stable-entry-contract.md` | Prevents semantics-only drift. |
| `RG-02` | `R03; R04` | A contract without proof and fallback routing will remain auditable history rather than a current runtime reader. | `S3A-2A-R13`; `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md` | Keeps proof and operator surface explicit but separate. |
| `RG-03` | `R06; R07; R08` | Once row split or absorption begins, the control lane should keep only handoff, parent write-back, and source-repair decisions, while durable downstream accounting moves into ledger-owned surfaces. | `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`; `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`; `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | Keeps `S4G-1B` aligned as the evolution or handoff lane rather than the durable source ledger. |

## Source Reader Model / Versioning (recommended for reusable log families)

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v1` | This packet reads one parent-ledger row plus nearby retained proof and runbook surfaces. |
| extraction surface version | `extractable-rules-v1` | The scaffold exposes one explicit contract-bridge extraction surface. |
| compatibility expectation | `forward-readable` | Later narrow `R01` packets can refine the same bridge shape. |
| migration note | `If a later contract release opens, keep source routing here and move only stable semantics downstream.` | Captures the handoff rule. |

## PR Summary Inputs (optional)

- This packet opens the first narrow `R01` bridge surface, not the final released observability contract.

**PR summary bullets**:

- Open `S4G-1B` as the first narrow child packet for `S3A-2A-R01`.
- Normalize the minimum `metrics -> tracing -> structured logs` contract claim.
- Fix the first bridge-field set for code boundary, drill proof, and later runbook export.

**PR checklist source**:

- Default source: reuse this log's execution checklist.

**PR links**:

- Log: `docs/logs/log-S4G-1B-r01-runtime-observability-governance-contract-bridge.md`
- Runbook: `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
- Evidence artifact: ``

## Exported Sections / Outlet Ownership

- This scaffold fixes outlet intent, but only `log-retained core` is live now.

**Outlet ownership**:

- `contract`: current landing is `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`.
- `runbook`: later landing should either narrow `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` or open one explicit runtime-observability operator bridge once the entrypoint is defended.
- `view`: no-op for now.
- `index/front-door`: no-op for now.
- `disposition/placement`: no-op for now.
- `log-retained core`: keep the weak contract claim, boundary field set, proof obligation, and first-next-step drill search here.

## Definitions (optional)

- `runtime observability governance`: the current semantic rule that defines how one runtime path must remain diagnosable through correlated metrics, tracing, and structured logs.
- `bridge-to-code`: the minimum bounded field set that names where the contract attaches to a real runtime unit.
- `shared pivot`: one stable correlation key such as request id, job id, trace id, event id, or another defended domain key that lets multiple signal types describe one handling chain.
- `proof semantics`: the rule that says whether the contract is currently backed by one deterministic drill, gate, or explicit proof gap statement.

## Constraints

- Do not claim an active runtime observability contract before one bounded runtime surface is named.
- Do not treat retained drills or runbook prose as a substitute for a contract statement.
- Do not fabricate fallback, shadow, dual-run, or window rules from weak source text.

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `S4G-1B` source log | `Has R01 been normalized into one weak contract claim plus one bridge field set?` | `extractable rows plus named field set` | Entry step for this narrow packet. |
| `SUP` | `not-required` | `n/a` | `Is a supplement required before the first bridge scaffold can exist?` | `explicit no-SUP reuse from parent packet` | `S4G-1A` already fixed `no-SUP-for-now` for this packet. |
| `parent ledger` | `already-satisfied` | `ledger-S3A-2A-combo-observability-triage` | `Does packet routing already exist upstream?` | `S3A-2A-R01 retained in parent ledger` | Routing already exists; this log narrows the next child packet. |
| `contract impact decision` | `required` | `S4G-1B` | `Is this row still a bridge scaffold, a contract-sharpening packet, or the first code-first fallback candidate?` | `explicit classified verdict` | Main gate for the next round. |
| `contract mutation` | `conditional` | `observability family contract or n/a` | `Is the boundary, proof path, and current semantic claim defended tightly enough for release 0001?` | `new contract record or explicit no-contract-mutation verdict` | Current scaffold does not assume yes. |
| `transition register update` | `conditional` | `affected family register or n/a` | `Did current reader standing change after the first release decision?` | `register row or explicit no-register-change verdict` | Only after one actual contract release. |
| `bridged contract reconciliation` | `conditional` | `affected runtime or docs surfaces` | `Do drills, runbook, or other reader surfaces need bridge notes after the first release?` | `bridge note or explicit no-bridge-impact verdict` | Needed only if a contract lands. |

## Scope

- `P0`: contract (weak claim, boundary field set, proof and runbook bridge semantics)
- `P1`: boundary discovery / entrypoint narrowing
- `P2`: drill and evidence binding
- `P3`: first downstream release decision

## Success Criteria (DoD)

- `R01` has one falsifiable weak contract claim.
- The packet names one minimum bridge field set for `applied-to-surface`, `runtime boundary`, and `candidate entrypoint`.
- The packet states whether proof currently exists through one deterministic drill or remains an explicit gap.
- The packet distinguishes what belongs in a future contract from what belongs in a future runbook.
- The next step is one narrow code search for the first boundary and entrypoint anchor.

## Stability (what stable means)

- This log can be marked `stable` when:
  - one bounded runtime surface and candidate entrypoint are defended;
  - proof semantics are explicit;
  - the next step is either one released contract record or one explicit no-release verdict.

## P0 (Contract | v1)

### P0-C1-S1 (Weak contract claim fixed | v1)

- The first weak contract claim for `R01` is:
  - `one admitted runtime handling chain should remain diagnosable through metrics, tracing, and structured logs via shared pivots and auditable evidence`.
- This claim is semantic-only until one code boundary is named.

### P0-C1-S2 (Boundary bridge field set fixed | v1)

- The minimum bridge field set for this packet is:
  - `contractClaim`
  - `appliedToSurface`
  - `runtimeBoundary`
  - `candidateEntrypoint`
  - `sharedPivots`
  - `requiredSignals`
  - `failureSemantics`
  - `fallbackMode`
  - `switchSurface`
  - `coexistenceWindow`
  - `versioningNote`
  - `drillProofRef`
  - `runbookRef`
- `appliedToSurface` exists to stop the contract from floating above code with no bounded owner.

### P0-C1-S3 (Proof and runbook bridge contract | v1)

- The contract must say whether one deterministic drill, gate, or explicit proof gap currently backs the chain.
- The contract does not need to own all operator steps, but it must name the proof obligation.
- Step-by-step fallback, switch, shadow, or dual-run procedure should later land in runbook once the entrypoint is defended.

## P1 (Boundary discovery / entrypoint narrowing | v1)

### P1-C1-S1 (First bounded runtime surface identified | v1)

- The first bounded runtime surface for `R01` is the `Search Outbox -> Elasticsearch` projection worker surface.
- Current `appliedToSurface` value:
  - `search outbox projection worker for projection=search_index_to_elastic`
- Current `runtimeBoundary` value:
  - `one long-running worker process claims outbox rows, projects them into Elasticsearch, and emits low-cardinality outbox metrics, tracing spans, and structured logs during claim/process/fail paths`
- Why this surface is selected first:
  - it is narrower than the API-wide observability surface;
  - it is already treated as a stable operational worker path in `S3A-2A-2B` and `S6A-1A`;
  - it is the same runtime surface later drills and runbook flows already target.

### P1-C1-S2 (Candidate entrypoint identified | v1)

- The first candidate entrypoint for `R01` is:
  - `backend/scripts/search_outbox_worker.py`
- Current bridge-field write-back:
  - `appliedToSurface`: `search outbox projection worker`
  - `runtimeBoundary`: `search_index_to_elastic worker process`
  - `candidateEntrypoint`: `backend/scripts/search_outbox_worker.py`
  - `sharedPivots`: `trace_id/traceparent`, `claim_batch_id`, `outbox event id`, and worker metric labels such as `projection` and `op`
  - `requiredSignals`: `outbox_* metrics`, worker tracing spans, and worker structured logs
  - `versioningNote`: `search_outbox_worker@v1` remains the stable drill-facing entry id from the failure-drill helper layer
- Why this entrypoint is selected first:
  - it is the stable worker entrypoint explicitly preserved for Procfiles, historical docs, and drill helpers;
  - it exposes a bounded switch surface already (`SEARCH_OUTBOX_WORKER_ENABLED`, `SEARCH_OUTBOX_RUNNER`);
  - the implementation under `backend/scripts/search_outbox_worker_impl.py` already binds all three `R01` signal classes.
- Non-selected nearby candidate:
  - `backend/scripts/cli.py labs run <scenario>` is kept as the drill harness entry, but not as the semantic owner entrypoint for this contract.

## P2 (Drill / proof binding | v1)

### P2-C1-S1 (Current drill attachment decided | v1)

- The current defended proof-path candidate for `R01` is `es_write_block_4xx`.
- Current `drillProofRef` value:
  - `backend/scripts/cli.py labs run es_write_block_4xx`
  - `backend/scripts/cli.py labs verify es_write_block_4xx`
  - `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`
  - `backend/scripts/cli_app/scenarios/es_write_block_4xx.py`
- Why this drill is selected as the primary proof path:
  - it targets the same `search_outbox_worker@v1` entrypoint chosen in `P1`;
  - it is deterministic because the controller forces Elasticsearch write-block state instead of depending on probabilistic rate limiting;
  - its verify step already asserts before/after metric deltas, DB reason families, and supply-row checks against the same worker surface;
  - the labs docs already publish `run -> verify -> export -> clean` commands for this scenario.
- Secondary adjacent proof row kept for follow-up, not first proof:
  - `es_429_inject` remains useful because it proves retry and rate-limit behavior on the same worker surface, but it is treated as the second proof candidate rather than the first defended proof path.

### P2-C1-S2 (Minimum proof semantics fixed | v1)

- The current minimum proof semantics for `R01` are:
  - one drill must start the stable worker entry `search_outbox_worker@v1`;
  - one verify step must show that metrics on the same projection surface move in the expected direction before/after the trigger;
  - one evidence bundle must retain worker-start evidence, metrics snapshots, result JSON, and worker logs on that same run;
  - tracing remains required as part of the governed chain, but absence of exported traces is currently treated as a proof gap note rather than a full block on this first proof-path decision.
- Current proof verdict:
  - `proof path exists now through es_write_block_4xx; tracing export completeness may still require later hardening, but no longer blocks the first defended proof-path selection`
- Why `es_429_inject` is not selected first:
  - it proves a narrower `rate_limit` retry family on the same worker surface rather than the broader deterministic failure-handling boundary;
  - its injection model still depends on scenario knobs such as `EVERY_N` or `RATIO`, so it is less stable as the very first reader-facing proof anchor.

## P3 (Downstream release decision | v1)

### P3-C1-S1 (First contract release decision recorded | v1)

- Decision:
  - open `DOC-RUNTIME-OBSERVABILITY-0001` now.
- Current release file:
  - `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
- Why the release is justified now:
  - the packet already has one falsifiable semantic claim;
  - the packet already has one bounded worker owner surface and stable entrypoint;
  - the packet already has one defended proof path with explicit run, verify, and evidence-bundle shape;
  - the remaining gaps are hardening gaps, not identity gaps.

### P3-C1-S2 (Runbook bridge decision recorded | v1)

- Decision:
  - do not open one separate runbook bridge packet yet.
- Current runbook standing:
  - keep `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md` as the current operator reader for the shared drill family.
- Why no separate runbook bridge packet opens now:
  - the current missing pieces are not operator-entry uncertainty but narrower fallback/switch-window semantics;
  - those semantics should be opened only when one runtime-owned cutover or coexistence procedure is actually ready to be stated.

### P3-C2-S1 (Attached row-flow ledger model fixed | v1)

- Decision:
  - when one parent-ledger row must split into multiple derived rows before downstream release mutation is reviewable, the durable accounting should move into one attached row-flow ledger rather than remain only in `S4G-1B`.
- Current attached ledger for this packet:
  - `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`
- Consequence:
  - `S4G-1B` now keeps preliminary extraction rows and decision lineage, but not the final source-of-truth split or absorption accounting.

### P3-C2-S2 (Parent-ledger handoff fixed | v1)

- Decision:
  - `S3A-2A-R01` remains the packet root in the parent ledger, but current downstream reading is now written back through the attached row-flow ledger.
- Parent-ledger effect:
  - `S3A-2A-R01` is now `partially-applied` with `partial` consumption and explicit handoff to the attached ledger.
- Reason:
  - the parent row should not collapse into one shared-reason footnote or disappear behind this control log.

### P3-C2-S3 (Contract source repair fixed | v1)

- Decision:
  - `DOC-RUNTIME-OBSERVABILITY-0001` should now cite the attached row-flow ledger as its direct source basis, with `S4G-1B` retained as decision lineage rather than primary release provenance.
- Consequence:
  - contract source rows now read through `S3A-2A-R01-D01` through `S3A-2A-R01-D06`.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4G-1B/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- `S4G-1B` work should continue on `S4G-fallback-cells-and-failure-drills-asset-governance` unless a later packet justifies a narrower focused branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit, commit/push promptly on the current `S4G` working branch.

## Plan (draft)

### P1 (Boundary discovery / entrypoint narrowing)

- P1-C1-S1: normalize `R01` into one weak contract claim and first field set
- P1-C1-S2: identify one bounded runtime surface and one candidate entrypoint

### P2 (Drill / proof binding)

- P2-C1-S1: decide which current drill becomes the first defended proof path for `R01`
- P2-C1-S2: fix one minimum proof semantics statement and any remaining trace-gap note

### P3 (Downstream release decision)

- P3-C1-S1: decide whether to open `DOC-RUNTIME-OBSERVABILITY-0001`
- P3-C1-S2: decide whether one paired runbook bridge packet is required now or later
- P3-C2-S1: define when row split or absorption accounting must move into one attached row-flow ledger
- P3-C2-S2: write the parent-ledger handoff back for `S3A-2A-R01`
- P3-C2-S3: repair contract source basis to consume attached-ledger derived rows

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: weak contract claim fixed
- [x] `P0-C1-S2`: boundary bridge field set fixed
- [x] `P0-C1-S3`: proof and runbook bridge contract fixed

### P1 (Boundary discovery / entrypoint narrowing)

- [x] `P1-C1-S1`: first bounded runtime surface identified
- [x] `P1-C1-S2`: candidate entrypoint identified

### P2 (Drill / proof binding)

- [x] `P2-C1-S1`: current drill attachment or gap decided
- [x] `P2-C1-S2`: minimum proof or explicit no-proof-yet statement fixed

### P3 (Downstream release decision)

- [x] `P3-C1-S1`: first contract release decision recorded
- [x] `P3-C1-S2`: runbook bridge decision recorded
- [x] `P3-C2-S1`: attached row-flow ledger model fixed
- [x] `P3-C2-S2`: parent-ledger handoff fixed
- [x] `P3-C2-S3`: contract source repair fixed

## Current Status (recommended)

- `S4G-1B` is opened as the first narrow child packet for `S3A-2A-R01`.
- The weak semantic claim is fixed, and `P1` now narrows the first live code bridge to the `search outbox -> Elasticsearch` worker surface via `backend/scripts/search_outbox_worker.py`.
- `P2` now selects `es_write_block_4xx` as the first defended proof path for that same runtime reader, while `es_429_inject` remains the next adjacent retry-path proof candidate.
- `P3` now opens `DOC-RUNTIME-OBSERVABILITY-0001` as the first draft released reader for this chain, while leaving runbook bridge work deferred until narrower fallback or switch semantics are actually ready.
- `P3-C2` now moves derived-row accounting out of `S4G-1B` and into `ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption`, rewrites the parent-ledger handoff, and repairs the contract so it no longer reads like one log-owned source export.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log will record head SHA, first boundary anchors, and any later drill-proof artifacts.
- Current admitted packet refs:
  - `S3A-2A-R01`
  - `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`
  - `docs/logs/log-S3A-2A-4B-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
  - `docs/logs/log-S6A-1A-stable-entry-contract.md`
- Current boundary anchors:
  - `backend/scripts/search_outbox_worker.py`
  - `backend/scripts/search_outbox_worker_impl.py`
  - `backend/infra/observability/outbox_metrics.py`
  - `backend/infra/observability/tracing.py`
  - `backend/scripts/cli_app/scenarios/_failure_drill_shared.py`
- Current proof anchors:
  - `backend/scripts/cli_app/scenarios/es_write_block_4xx.py`
  - `backend/scripts/cli_app/scenarios/es_429_inject.py`
  - `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`
  - `docs/runbook/legacy/run-S3A-failure-drills-&-gitactions-&-dashboard.md`
- Current release anchor:
  - `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
- Current attached-ledger anchor:
  - `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`

## Recent changes (for traceability, optional)

- 2026-04-26: opened `S4G-1B` as the first narrow child packet for `S3A-2A-R01`, fixing the weak contract claim and first bridge field set before any released observability contract mutation.
- 2026-04-26: completed `P1` by selecting the search outbox projection worker as the first bounded runtime surface and `backend/scripts/search_outbox_worker.py` as the first candidate entrypoint for `R01`.
- 2026-04-26: completed `P2` by selecting `es_write_block_4xx` as the first defended proof path for `R01` and treating `es_429_inject` as the next adjacent retry-path proof candidate.
- 2026-04-26: completed `P3` by opening `DOC-RUNTIME-OBSERVABILITY-0001` and explicitly deferring a separate runbook bridge packet.
- 2026-04-26: completed `P3-C2` by opening one attached row-flow ledger for `S3A-2A-R01`, writing the parent-ledger handoff back, and repairing the contract so its direct source basis now comes from ledger-owned derived rows rather than from this control log.
