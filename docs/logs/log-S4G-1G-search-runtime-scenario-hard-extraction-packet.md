# log-S4G-1G (Phase 9: search runtime scenario hard extraction packet)

---

**id**: `S4G-1G`
**kind**: `log`
**title**: `search runtime scenario hard extraction packet v1`
**status**: `draft`
**scope**: `S4`
**tags**: `EVOLUTION, OpsRuntime, Observability, FailureDrills, ScenarioExtraction, Evidence, epic/s4, epic/s4g, sub/1g`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  **roadmap**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
  **parent_log**: `docs/logs/log-S4G-fallback-cells-and-failure-drills-asset-governance.md`
  **previous_log**: `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md`
  **reference_log_1**: `docs/logs/log-S4G-1D-runtime-operator-semantics-gap-packet.md`
  **reference_log_2**: `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
  **reference_log_3**: `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`
  **reference_log_4**: `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`
  **reference_log_5**: `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`
**issue_keyword**: `runtime`
**issue_top_labels**: ``
**issue_scope_labels**: ``
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md`
**roadmap_milestone**: `M2`
**roadmap_phase**: `M2-P5`
**roadmap_bridge_refs**: `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md#M2-P5`
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-27`
**updated**: `2026-04-27`
**reviewed**: `pending`
**source_reader_model**: `mixed-source-v1`
**extraction_surface_version**: `extractable-rules-v1`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- These fields do not claim semantic-effective time for downstream runbook or contract scenario coverage; those time windows remain owned by later reader surfaces.
- `reviewed` should remain `pending` until the code/labs hard-extraction and family-boundary classification are explicit enough to review as one bounded packet.

## Decision / Outcome

**Decision**:

- Open `S4G-1G` as the bounded `hard extraction packet` for the Search runtime scenario universe.
- Treat this packet as a `code + labs + retained evidence` extraction lane rather than a wording-rewrite or legacy-prose interpretation lane.
- Use this packet to decide which Search scenarios belong in the current `RUNTIME-OBSERVABILITY` family, which should stay `labs/support-only`, and which should route to sibling families such as dual-write/cutover/DLQ-replay.

**Default choices (phase defaults / v1)**:

- Prefer code-registered scenario entrypoints, labs docs, labs snapshots, and retained evidence over prose-only summary when they disagree.
- Do not widen `DOC-RUNTIME-OBSERVABILITY-0001` or `run-RUNTIME-OBSERVABILITY-001` by guesswork from historical wording alone.
- Do not treat every Search-adjacent scenario as belonging to the same current family; explicit family-boundary classification is required.
- draft 阶段默认继续把 source log 当作集中面；如果 scenario inventory、family boundary、或 downstream write-back 仍在变化，不要过早把 weak-structure 内容拆到 contract/runbook 正文。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## Extractable Rule Surface

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `scenario registry mismatch` | `runbook-candidate` | The current Search runtime readers should not be treated as the full scenario universe until code and labs extraction explicitly classify which scenarios belong to the current family. | `runbook` | `ready` | `RG-01` | `S4G-1F`; `run-RUNTIME-OBSERVABILITY-001`; code scenarios; labs | Opening rule for this packet. |
| `R02` | `backend/scripts/cli_app/scenarios` | `view-candidate` | Scenario inventory for Search runtime must be extracted first from concrete code-registered scenarios rather than from retained wording alone. | `view` | `ready` | `RG-01` | `backend/scripts/cli_app/scenarios/*.py` | Code-first extraction rule. |
| `R03` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md` | `runbook-candidate` | A scenario should enter the current `RUNTIME-OBSERVABILITY` family only when code, labs, and current reader meaning align strongly enough to support one bounded current operator surface. | `runbook` | `needs-corroboration` | `RG-02` | `lab-S3A-2A-3A`; scenario code; current runbook/contract` | Family-admission rule, not automatic inclusion. |
| `R04` | `dual-run / DLQ / replay evidence` | `view-candidate` | Search-adjacent scenarios that primarily express dual-write, cutover, replay, or DLQ semantics should be classified explicitly as sibling-family or support-only rather than being silently absorbed by the current observability family. | `view` | `ready` | `RG-02` | `lab-S2B-2A-2A`; shadow/dual-run scenarios` | Prevents family drift. |
| `R05` | `write-back decision` | `contract-candidate` | Any widening of `OBSERVABILITY-0001` or `run-RUNTIME-OBSERVABILITY-001` should happen only after the extracted scenario universe is classified into current-family, support-only, and sibling-family buckets. | `contract` | `ready` | `RG-03` | `S4G-1G`; current contract; current runbook` | Write-back gate for later mutation. |

### Shared Reason Groups

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | The current readers are narrower than the repo's apparent Search scenario universe, so a code/labs-first extraction pass is required before more wording refinement. | `S4G-1F`; current runbook; current contract; scenario code` | Reader-vs-reality rationale. |
| `RG-02` | `R03; R04` | Scenario inclusion must be explicit because some Search-adjacent scenarios belong to observability while others belong to dual-write/cutover or stay support-only. | `labs docs`; `scenario code`; `support ledgers` | Family-boundary rationale. |
| `RG-03` | `R05` | Downstream write-back should follow classification, not precede it. | `current contract`; `current runbook`; `S4G-1G` | Mutation-order rationale. |

## Source Reader Model / Versioning

| field | value | notes |
| --- | --- | --- |
| current source reader model | `mixed-source-v1` | This packet reads code-registered scenarios, labs docs, labs snapshots, retained support ledgers, and current readers together. |
| extraction surface version | `extractable-rules-v1` | The extraction surface is scenario-inventory plus family-boundary classification. |
| compatibility expectation | `forward-readable` | Later packets should be able to reuse this inventory/classification without reopening the entire earlier lane. |
| migration note | `If current family coverage widens later, preserve the scenario classification trail here before mutating contract/runbook readers.` | Keeps widening traceable. |

## PR Summary Inputs

- This packet opens the bounded code/labs-first hard-extraction lane for the Search runtime scenario universe.

**PR summary bullets**:

- Open `S4G-1G` to hard-extract the Search runtime scenario universe from code, labs, and retained evidence.
- Classify scenarios into current-family, support-only, and sibling-family buckets before widening current readers.
- Keep contract/runbook mutation deferred until the extraction and boundary verdict are explicit.

**PR checklist source**:

- Default source: reuse this log's execution checklist.

**PR links**:

- Log: `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md`
- Runbook: `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
- Evidence artifact: ``

## Exported Sections / Outlet Ownership

**Outlet ownership**:

- `contract`: deferred until scenario classification says current-family widening is defendable.
- `runbook`: deferred until scenario classification says current-family widening is defendable.
- `view`: possible later export if one stable scenario-universe summary becomes reusable beyond this packet.
- `index/front-door`: required now through S4G spine and roadmap registration.
- `disposition/placement`: likely required later because some scenarios will classify as support-only or sibling-family.
- `log-retained core`: keep the hard-extraction scope, classification rules, checklist, current status, and evidence anchors here.

## Definitions

- `scenario hard extraction`: extracting scenario identity and standing from concrete code/labs/evidence surfaces rather than from prose-only summaries.
- `current-family scenario`: a scenario that belongs in the current `RUNTIME-OBSERVABILITY` contract/runbook family.
- `support-only scenario`: a scenario that remains useful as evidence or labs support but is not promoted into the current reader family.
- `sibling-family scenario`: a scenario whose primary semantics belong to another family such as dual-write, cutover, or DLQ/replay.

## Constraints

- Do not widen current readers before explicit scenario classification.
- Do not collapse dual-write / cutover / replay semantics into observability by adjacency alone.
- Prefer stable scenario names, registered code entrypoints, and existing labs evidence over retrospective wording.

## Gap Closure / Write-Back

| gap id | current status | closure target | current write-back standing | reopen proof expectation | notes |
| --- | --- | --- | --- | --- | --- |
| `G01` | `open` | `current-family scenario inventory` | `retained here; no current-reader mutation yet` | `show that the scenario universe is complete enough to classify` | `Search runtime scenario universe is not yet explicitly extracted.` |
| `G02` | `open` | `family-boundary classification` | `retained here; no current-reader mutation yet` | `show that each admitted scenario has a defendable family owner` | `Current-family vs sibling-family standing is not yet explicit.` |
| `G03` | `open` | `write-back decision for contract/runbook/view` | `retained here; no downstream mutation yet` | `show that one or more scenario buckets imply concrete reader changes` | `Current mutation order remains extraction first.` |

| write-back target | target kind | when required | current verdict | notes |
| --- | --- | --- | --- | --- |
| `docs/logs/log-S4G-fallback-cells-and-failure-drills-asset-governance.md` | `index/front-door` | `required when a new bounded S4G packet opens` | `required-now` | `Register S4G-1G in the spine.` |
| `docs/roadmap/road-002-01-deployable-runtime-slice-and-cloud-backed-asset-readiness.md` | `index/front-door` | `required when the roadmap gains a new bounded runtime packet` | `required-now` | `Map S4G-1G as the Search scenario hard-extraction packet.` |
| `DOC-RUNTIME-OBSERVABILITY-0001` | `contract reader` | `required only if current-family scenario widening is later justified` | `not-required-now` | `Classification must happen first.` |
| `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` | `runbook reader` | `required only if current-family scenario widening is later justified` | `not-required-now` | `Classification must happen first.` |

| gap change id | gap id | change action | recorded at | reason | source basis | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `GC-01` | `G01` | `opened` | `2026-04-27` | `The current readers appear narrower than the repo's Search scenario universe, but that universe is not yet explicitly extracted from code/labs.` | `scenario code`; `labs docs`; `S4G-1F` | `Open inventory extraction first.` |
| `GC-02` | `G02` | `opened` | `2026-04-27` | `Scenario-family ownership is not yet explicit across observability, support-only, and sibling-family lanes.` | `current runbook`; `current contract`; `labs/cutover evidence` | `Open boundary classification next.` |
| `GC-03` | `G03` | `opened` | `2026-04-27` | `Downstream mutation would be premature until the extracted scenario universe is classified.` | `S4G-1G` | `Keep write-back deferred.` |

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `required` | `S4G-1G` source log | `Has the Search scenario source slice been identified tightly enough to inventory?` | `explicit code/labs source list plus extraction rows` | Entry step for this packet. |
| `SUP` | `conditional` | `existing support ledgers or n/a` | `Do legacy sharpeners materially change one scenario standing?` | `accepted SUP row or explicit no-SUP verdict` | Decide only after extraction. |
| `parent ledger` | `already-satisfied` | `ledger-S3A-2A` plus attached row-flow ledger | `Does upstream routing already expose the narrower current family?` | `current parent routing plus extracted mismatch evidence` | Parent routing already exists; this packet tests its sufficiency. |
| `contract impact decision` | `required` | `S4G-1G` | `Does scenario classification imply reader widening, sibling split, or no current mutation?` | `explicit classified verdict` | Main decision gate for this packet. |
| `contract mutation` | `conditional` | `DOC-RUNTIME-OBSERVABILITY-0001` | `Do extracted current-family scenarios materially widen current contract meaning?` | `later release or explicit no-contract-mutation verdict` | Meaning change should remain explicit. |
| `transition register update` | `not-required` | `n/a` | `Did family-level reader standing change enough to require a family register?` | `explicit no-register-change verdict` | Not assumed at scaffold time. |
| `bridged contract reconciliation` | `conditional` | `current runbook/contract readers` | `Do current readers need boundary notes after classification?` | `later reconciliation verdict` | May become necessary after P2/P3. |

## Scope

- `P0`: contract (packet opening, extraction contract, evidence contract)
- `P1`: hard-extract the Search runtime scenario universe from code + labs + retained evidence, then open the release-ledger landing surfaces needed for later staged write-back
- `P2`: classify scenarios into current-family, support-only, and sibling-family buckets
- `P3`: record downstream write-back decisions for current readers and later sibling lanes

## Success Criteria (DoD)

- The packet records one explicit code/labs-first Search scenario source slice.
- The packet inventories current Search runtime scenarios without relying on prose-only summaries.
- The packet classifies each extracted scenario as current-family, support-only, or sibling-family.
- The packet records whether current `OBSERVABILITY-0001` / `run-RUNTIME-OBSERVABILITY-001` should widen, stay narrow, or split sibling lanes.
- The packet keeps current observability-family meaning distinct from dual-write / cutover / replay semantics.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the Search scenario universe is explicitly extracted from code/labs/evidence;
  - current-family versus sibling-family standing is explicit;
  - downstream write-back standing is explicit;
  - the next step is a bounded reader-widening or sibling-lane packet rather than more generic archaeology.

## P0 (Contract | v1)

### P0-C1-S1 (Packet opening and extraction rule fixed | v1)

- `S4G-1G` opens as the bounded hard-extraction packet for the Search runtime scenario universe.
- This packet should read code/labs/evidence first and only use wording as a secondary corroboration surface.

### P0-C1-S2 (Classification boundary fixed | v1)

- Each extracted scenario must be classified as one of:
  - `current-family`
  - `support-only`
  - `sibling-family`

### P0-C1-S3 (Evidence contract | v1)

- Evidence for later execution should include:
  - the concrete scenario code files used for extraction;
  - the labs docs or snapshots used to corroborate those scenarios;
  - the later classification verdict for each extracted scenario.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S4G-1G/P<phase>-C<cycle>-S<steps>: <summary>`

**Branch convention**:

- `S4G-1G` work should continue on `S4G-fallback-cells-and-failure-drills-asset-governance` unless a later packet justifies a narrower focused branch.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit, commit/push promptly on the current `S4G` working branch.

## Plan (draft)

### P1 (Hard extraction)

- P1-C1-S1: inventory Search runtime scenarios from `backend/scripts/cli_app/scenarios/`.
- P1-C1-S2: corroborate those scenarios with labs docs, labs catalog, and retained evidence anchors.

## P1 (Hard extraction | v1)

### P1-C1-S1 (Search runtime scenarios inventoried from code | v1)

- The current extraction question is not `which scenarios feel important from memory?`; it is `which concrete Search-adjacent scenarios are actually registered in code and therefore must be accounted for before any family boundary is trusted?`

| scenario band | scenario name | concrete code anchor | current extraction note | why it is in the inventory now |
| --- | --- | --- | --- | --- |
| `worker fault / observability` | `es_429_inject` | `backend/scripts/cli_app/scenarios/es_429_inject.py` | `registered current Search fault scenario` | A concrete ES-side retry/failure scenario exists in code and must be counted even if current readers do not own it yet. |
| `worker fault / observability` | `es_write_block_4xx` | `backend/scripts/cli_app/scenarios/es_write_block_4xx.py` | `registered current Search fault scenario` | This is the first admitted proof path already used by current readers. |
| `worker fault / observability` | `es_down_connect` | `backend/scripts/cli_app/scenarios/es_down_connect.py` | `registered current Search fault scenario` | Search worker connectivity failure is explicitly implemented in code. |
| `worker fault / observability` | `es_timeout` | `backend/scripts/cli_app/scenarios/es_timeout.py` | `registered current Search fault scenario` | Timeout behavior is explicitly implemented in code. |
| `worker fault / observability` | `collector_down` | `backend/scripts/cli_app/scenarios/collector_down.py` | `registered current Search/obs-infra scenario` | Collector-down observability degradation is explicitly implemented in code. |
| `worker fault / observability` | `es_bulk_partial` | `backend/scripts/cli_app/scenarios/es_bulk_partial.py` | `registered current Search fault scenario` | Partial-bulk result semantics are explicitly implemented in code. |
| `worker concurrency / recovery` | `db_claim_contention` | `backend/scripts/cli_app/scenarios/db_claim_contention.py` | `registered current Search worker-contention scenario` | DB claim/owner mismatch contention is explicitly implemented in code. |
| `worker concurrency / recovery` | `stuck_reclaim` | `backend/scripts/cli_app/scenarios/stuck_reclaim.py` | `registered current Search reclaim scenario` | Lease expiry / reclaim behavior is explicitly implemented in code. |
| `worker idempotency` | `duplicate_delivery` | `backend/scripts/cli_app/scenarios/duplicate_delivery.py` | `registered current Search duplicate/noop scenario` | Duplicate delivery semantics are explicitly implemented in code. |
| `worker rule-versioning` | `projection_version` | `backend/scripts/cli_app/scenarios/projection_version.py` | `registered current Search version-risk scenario` | Projection-version behavior is explicitly implemented in code. |
| `search verification / gate` | `shadow_verify_search_index_write_gate` | `backend/scripts/cli_app/scenarios/shadow_verify_search_index_write_gate.py` | `registered Search-adjacent scenario with boundary pending` | Search write-gate semantics exist in code and may belong to another family. |
| `search verification / gate` | `shadow_verify_search_index_paging_stability` | `backend/scripts/cli_app/scenarios/shadow_verify_search_index_paging_stability.py` | `registered Search-adjacent scenario with boundary pending` | Search paging-stability verification exists in code and must be counted before routing. |
| `search verification / gate` | `shadow_verify_shared_keys` | `backend/scripts/cli_app/scenarios/shadow_verify_shared_keys.py` | `registered Search/obs-infra verification scenario with boundary pending` | Shared-key verification exists in code and may support either current family or a sibling gate family. |
| `search rehearsal` | `rehearsal_search_read_switch_smoke` | `backend/scripts/cli_app/scenarios/rehearsal_search_read_switch_smoke.py` | `registered Search-adjacent rehearsal scenario with boundary pending` | Search read-switch rehearsal exists in code and must be distinguished from runtime observability proper. |
| `dual-run / dual-write adjacent` | `shadow_verify_dual_run_readiness_gate` | `backend/scripts/cli_app/scenarios/shadow_verify_dual_run_readiness_gate.py` | `registered Search-adjacent scenario with likely sibling-family standing` | Dual-run readiness semantics clearly exist in code and must not be lost by narrow current readers. |
| `dual-run / dual-write adjacent` | `shadow_verify_dual_run_stage1` | `backend/scripts/cli_app/scenarios/shadow_verify_dual_run_stage1.py` | `registered Search-adjacent scenario with likely sibling-family standing` | Stage-1 dual-run semantics clearly exist in code. |
| `dual-run / dual-write adjacent` | `shadow_verify_dual_run_stage2` | `backend/scripts/cli_app/scenarios/shadow_verify_dual_run_stage2.py` | `registered Search-adjacent scenario with likely sibling-family standing` | Stage-2 dual-run semantics clearly exist in code. |
| `dual-run / dual-write adjacent` | `shadow_verify_dual_run_window` | `backend/scripts/cli_app/scenarios/shadow_verify_dual_run_window.py` | `registered Search-adjacent scenario with likely sibling-family standing` | Sustained dual-run window semantics clearly exist in code. |
| `dual-run / dual-write adjacent` | `shadow_verify_canary_dual_write` | `backend/scripts/cli_app/scenarios/shadow_verify_canary_dual_write.py` | `registered Search-adjacent scenario with likely sibling-family standing` | Canary dual-write semantics clearly exist in code. |
| `dual-run / dual-write adjacent` | `shadow_verify_dual_write_sampling` | `backend/scripts/cli_app/scenarios/shadow_verify_dual_write_sampling.py` | `registered Search-adjacent scenario with likely sibling-family standing` | Dual-write sampling semantics clearly exist in code. |

- P1 code-inventory verdict:
  - the concrete Search scenario universe in code is already materially wider than the single `es_write_block_4xx` proof path owned by current readers;
  - the inventory naturally divides into at least three extracted bands even before formal `P2` classification: worker fault/recovery, Search verification/gate, and dual-run/dual-write adjacent scenarios;
  - current readers should therefore be treated as intentionally narrow, not as an implicit summary of all existing Search runtime scenarios.

### P1-C1-S2 (Scenario inventory corroborated with labs docs, catalog, and retained evidence | v1)

- The current corroboration question is not `does one scenario name appear somewhere in docs?`; it is `does code inventory line up with labs/catalog/evidence strongly enough that the scenario should count as real lane material rather than a stale implementation stub?`

| scenario name | corroborating labs/catalog anchor | corroboration class | observed corroboration | notes |
| --- | --- | --- | --- | --- |
| `es_429_inject` | `docs/labs/scenarios/catalog.yml` | `catalog-backed` | catalog exposes full run/verify/export/clean commands for `fault/obs_infra/es_429_inject` | Present in catalog even if not highlighted in the current runbook skeleton. |
| `es_write_block_4xx` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; `docs/labs/scenarios/catalog.yml` | `lab-backed + catalog-backed` | labs doc records full buttonized flow and catalog exposes the same scenario family | Strongest currently admitted corroboration. |
| `es_down_connect` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; `docs/labs/scenarios/catalog.yml` | `lab-backed + catalog-backed` | labs doc records full run/verify/export/clean path and catalog exposes the same scenario | Current readers do not yet reflect it. |
| `es_timeout` | `docs/labs/scenarios/catalog.yml` | `catalog-backed` | catalog exposes full command flow for the scenario | Code + catalog already prove it is not an accidental stub. |
| `collector_down` | `docs/labs/scenarios/catalog.yml` | `catalog-backed` | catalog exposes full command flow for the scenario | Search-adjacent observability-infra case remains visible. |
| `es_bulk_partial` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; `docs/labs/scenarios/catalog.yml` | `lab-backed + catalog-backed` | labs doc records experiment D and catalog exposes the scenario | Current readers do not yet reflect partial-bulk semantics. |
| `db_claim_contention` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; `docs/labs/scenarios/catalog.yml` | `lab-backed + catalog-backed` | labs doc records experiment E plus retained snapshots/exports; catalog exposes full command flow | Strong corroboration for worker-contention semantics. |
| `stuck_reclaim` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; retained snapshots; `docs/labs/scenarios/catalog.yml` | `lab-backed + snapshot-backed + catalog-backed` | labs doc records experiment F, retained snapshots exist, and catalog exposes full command flow | Strong corroboration for reclaim semantics. |
| `duplicate_delivery` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; retained snapshots; `docs/labs/scenarios/catalog.yml` | `lab-backed + snapshot-backed + catalog-backed` | labs doc records experiment G, retained snapshots exist, and catalog exposes full command flow | Strong corroboration for idempotency/noop semantics. |
| `projection_version` | `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`; retained snapshots; `docs/labs/scenarios/catalog.yml` | `lab-backed + snapshot-backed + catalog-backed` | labs doc records experiment H, retained snapshots exist, and catalog exposes full command flow | Strong corroboration for version-risk semantics. |
| `shadow_verify_search_index_write_gate` | `docs/labs/scenarios/catalog.yml`; `docs/labs/lab-S2B-2A-1A-shadow-verify-write-gate.md` | `catalog-backed + lab-backed` | Search write-gate scenario exists in catalog and dedicated labs docs | Strong candidate for later sibling-family handling. |
| `shadow_verify_dual_run_readiness_gate` / `shadow_verify_dual_run_stage1` / `shadow_verify_dual_run_stage2` / `shadow_verify_dual_run_window` | `docs/labs/scenarios/catalog.yml` | `catalog-backed` | catalog explicitly groups these as readiness/dual_run Search scenarios | Sufficient corroboration to keep them in the extracted universe before routing. |
| `shadow_verify_canary_dual_write` / `shadow_verify_dual_write_sampling` | `docs/labs/scenarios/catalog.yml`; `docs/labs/lab-S2B-2A-2A-dual-run-cutover-closure.md` | `catalog-backed + lab-backed` | catalog exposes the scenarios and labs doc explicitly records DLQ/replay evidence and dual-write sampling | Strong sign these belong to a sibling family rather than current observability. |
| `rehearsal_search_read_switch_smoke` | `docs/labs/scenarios/catalog.yml` | `catalog-backed` | catalog exposes the rehearsal path under `pipeline:search` | Enough corroboration to keep it in inventory and classify later. |

- P1 corroboration verdict:
  - the worker-fault/recovery scenarios are not only present in code; they are also strongly corroborated by labs docs, retained snapshots, or the scenario catalog;
  - a second band of Search-adjacent verification/rehearsal/dual-run scenarios is also concretely corroborated and therefore cannot be dismissed as wording noise;
  - the main remaining problem is not scenario existence but scenario-family ownership, which is correctly deferred to `P2`.

### P1-C2-S1 (Reader-object-first ledger semantics confirmed | v1)

- Current repo semantics now distinguish three different ledger layers for the same family:
  - source-owned ledgers still own primary extraction and routing from source logs or other upstream mixed material;
  - reader-object release ledgers own staged evidence admission and write-back for one existing contract or runbook release;
  - run ledgers own one concrete execution history beneath one stable runbook release.
- This distinction is required because `S4G-1G/P1` already extracts strong-structure scenario evidence from code and labs that should not be forced directly into the current contract or runbook body before family classification.
- Therefore:
  - source logs remain the first retained mixed-source surface;
  - the new contract/runbook release ledgers become the first downstream landing surface for later phased write-back;
  - current reader bodies remain intentionally narrow until `P2` classifies ownership.

### P1-C2-S2 (OBSERVABILITY-0001 contract and runbook release ledgers scaffolded | v1)

- New template family opened for runbook release ledgers:
  - `docs/runbook/support-only/_template-runbook-release-ledger.md`
  - `docs/runbook/support-only/_template-runbook-release-ledger-SUP.md`
  - `docs/runbook/support-only/_template-runbook-release-ledger-PATCH.md`
- New template family opened for contract release ledgers:
  - `docs/governance/contracts/support-only/_template-contract-release-ledger.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger-SUP.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger-PATCH.md`
- Live `OBSERVABILITY-0001` scaffolds now exist for both current readers:
  - runbook release ledger family under `docs/runbook/support-only/ledger-runbook-*`
  - contract release ledger family under `docs/governance/contracts/support-only/ledger-*DOC-RUNTIME-OBSERVABILITY-0001*`
- These new ledgers do not widen either reader yet; they only create the durable landing surfaces needed so later `P2/P3` work does not get trapped inside the control log.

### P2 (Family classification)

- P2-C1-S1: classify each extracted scenario into current-family, support-only, or sibling-family.
- P2-C1-S2: record the smallest defensible reason for each classification.

## P2 (Family classification | v1)

### P2-C1-S1 (Extracted scenarios classified by family standing | v1)

- The current classification question is not `should these scenarios already be written into the current readers?`; it is `which stable family should own the scenario semantics once the extracted universe is made explicit?`

| scenario name | classified standing | current route summary | current write-back standing | notes |
| --- | --- | --- | --- | --- |
| `es_429_inject` | `current-family` | `same search outbox worker diagnostic chain` | `defer concrete widening to P3` | `ES-side retry and throttle behavior belongs to the current bounded runtime observability lane.` |
| `es_write_block_4xx` | `current-family` | `already admitted proof path` | `already owned now` | `This remains the first defended current proof path.` |
| `es_down_connect` | `current-family` | `same search outbox worker diagnostic chain` | `defer concrete widening to P3` | `Connectivity failure on the current worker chain belongs to the same bounded runtime lane.` |
| `es_timeout` | `current-family` | `same search outbox worker diagnostic chain` | `defer concrete widening to P3` | `Timeout behavior on the current worker chain belongs to the same bounded runtime lane.` |
| `es_bulk_partial` | `current-family` | `same search outbox worker diagnostic chain` | `defer concrete widening to P3` | `Partial-bulk result handling remains a runtime diagnostic scenario on the same worker surface.` |
| `db_claim_contention` | `current-family` | `same search outbox worker claim/recovery chain` | `defer concrete widening to P3` | `Claim contention is part of the same bounded worker handling chain.` |
| `stuck_reclaim` | `current-family` | `same search outbox worker claim/recovery chain` | `defer concrete widening to P3` | `Reclaim behavior remains part of the same bounded worker handling chain.` |
| `duplicate_delivery` | `current-family` | `same search outbox worker idempotency chain` | `defer concrete widening to P3` | `Duplicate/noop handling remains part of the current worker diagnostic chain.` |
| `projection_version` | `current-family` | `same search outbox worker rule-version chain` | `defer concrete widening to P3` | `Projection-version behavior remains part of the current worker diagnostic chain.` |
| `collector_down` | `support-only` | `same lane corroboration but not the bounded worker chain itself` | `retain in object ledgers and source log` | `Collector availability matters to evidence confidence, but the scenario centers observability infrastructure rather than the current owned worker chain.` |
| `shadow_verify_shared_keys` | `support-only` | `cross-surface corroboration aid rather than primary owned scenario` | `retain in object ledgers and source log` | `Shared-key verification helps corroborate other scenarios, but it does not by itself define the current runtime observability family.` |
| `shadow_verify_search_index_write_gate` | `sibling-family` | `search verification / gate semantics` | `route to sibling lane in P3` | `Write-gate semantics are not the same as the current bounded worker diagnostic chain.` |
| `shadow_verify_search_index_paging_stability` | `sibling-family` | `search verification / read-surface semantics` | `route to sibling lane in P3` | `Paging-stability verification belongs to a search behavior family, not the current worker observability family.` |
| `rehearsal_search_read_switch_smoke` | `sibling-family` | `read-switch rehearsal semantics` | `route to sibling lane in P3` | `Read-switch rehearsal is cutover or switch-family behavior rather than current observability ownership.` |
| `shadow_verify_dual_run_readiness_gate` | `sibling-family` | `dual-run readiness semantics` | `route to sibling lane in P3` | `Dual-run readiness is explicitly outside the current narrow reader family.` |
| `shadow_verify_dual_run_stage1` | `sibling-family` | `dual-run stage semantics` | `route to sibling lane in P3` | `Stage-1 dual-run behavior belongs to a sibling family.` |
| `shadow_verify_dual_run_stage2` | `sibling-family` | `dual-run stage semantics` | `route to sibling lane in P3` | `Stage-2 dual-run behavior belongs to a sibling family.` |
| `shadow_verify_dual_run_window` | `sibling-family` | `coexistence-window semantics` | `route to sibling lane in P3` | `Sustained dual-run window semantics are explicitly outside current observability ownership.` |
| `shadow_verify_canary_dual_write` | `sibling-family` | `dual-write cutover semantics` | `route to sibling lane in P3` | `Canary dual-write behavior belongs to a sibling cutover or dual-write family.` |
| `shadow_verify_dual_write_sampling` | `sibling-family` | `dual-write evidence semantics` | `route to sibling lane in P3` | `Dual-write sampling belongs to a sibling cutover or dual-write family.` |

### P2-C1-S2 (Smallest defensible reasons recorded | v1)

- The current smallest defensible classification rule is:
  - classify as `current-family` when the primary semantics stay on the current search outbox worker handling chain and test its diagnosability, recovery, or evidence-bearing behavior;
  - classify as `support-only` when the scenario materially corroborates the lane but centers supporting infra or cross-surface evidence rather than the owned worker chain itself;
  - classify as `sibling-family` when the scenario's primary semantics are search verification, read-switch, shadow, dual-run, dual-write, or coexistence-window behavior that the current readers explicitly do not own.
- P2 classification verdict:
  - `current-family`: `es_429_inject`, `es_write_block_4xx`, `es_down_connect`, `es_timeout`, `es_bulk_partial`, `db_claim_contention`, `stuck_reclaim`, `duplicate_delivery`, `projection_version`;
  - `support-only`: `collector_down`, `shadow_verify_shared_keys`;
  - `sibling-family`: `shadow_verify_search_index_write_gate`, `shadow_verify_search_index_paging_stability`, `rehearsal_search_read_switch_smoke`, `shadow_verify_dual_run_readiness_gate`, `shadow_verify_dual_run_stage1`, `shadow_verify_dual_run_stage2`, `shadow_verify_dual_run_window`, `shadow_verify_canary_dual_write`, `shadow_verify_dual_write_sampling`.
- This step still does not widen the current readers; it only makes the ownership routing explicit enough for `P3`.

### P2-C2-S1 (Full auditable ledger-chain semantics fixed before write-back | v1)

- The current controlling question is not `can P3 start now that classification exists?`; it is `can later readers still explain exactly what changed, when it changed, and whether the change passed through SUP, parent ledger, or PATCH without reopening the whole lane?`
- The answer is now fixed as one family-agnostic chain rule:
  - when later evidence sharpens or revises an already admitted reading, the chain is `SUP -> parent ledger -> downstream reader`;
  - when one bounded repair changes the already-bound reader object, the chain is `PATCH -> downstream reader`;
  - when a bounded repair also changes admitted meaning, the repair must be paired with `SUP -> parent ledger` instead of hiding semantic change inside the patch packet alone.
- This rule now applies across:
  - source-owned ledger families;
  - reader-object contract release-ledger families;
  - reader-object runbook release-ledger families;
  - run-ledger families.
- Therefore `P3` remains blocked until each involved ledger family exposes enough chronology and event structure that a later reader can tell:
  - what changed;
  - what stayed unchanged;
  - which packet caused the change;
  - whether the change was only evidence admission, parent-ledger rewrite, or actual contract/runbook mutation.

### P2-C2-S2 (Time-audit surfaces backfilled to keep change visibility explicit | v1)

- A `完整可审计` chain requires three different time layers to stay separate:
  - artifact lifecycle time: `created_at`, `reviewed_at`, `accepted_at`, `writeback_started_at`, `writeback_completed_at`;
  - source chronology time: `source observed at`, `source recorded at`, `source effective from`, `source effective until`, `time precision`, `timezone note`;
  - governance event time: explicit intake, review-state, and write-back events on the parent ledger.
- The new remediation therefore backfills the currently-open object-ledger live files and the deficient templates so that later readers can audit:
  - when evidence first became admissible;
  - when the parent ledger state changed;
  - when a contract or runbook body did not change even though the ledger did;
  - and which fields still remain `unknown`, `pending`, or `ongoing` without false precision.
- This means later write-back can now show not only `that` a row changed, but also `how`, `why`, and `through which surface` it changed.

### P3 (Write-back decision)

- P3-C1-S1: decide whether current `OBSERVABILITY-0001` / `run-RUNTIME-OBSERVABILITY-001` should widen, stay narrow, or route sibling lanes.
- P3-C1-S2: record the next bounded packet or no-op path.

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: packet opening and extraction rule fixed.
- [x] `P0-C1-S2`: classification boundary fixed.
- [x] `P0-C1-S3`: evidence contract fixed.

### P1 (Hard extraction)

- [x] `P1-C1-S1`: inventory Search runtime scenarios from code.
- [x] `P1-C1-S2`: corroborate scenarios with labs docs, catalog, and retained evidence.
- [x] `P1-C2-S1`: confirm reader-object-first ledger semantics for contract and runbook releases.
- [x] `P1-C2-S2`: scaffold OBSERVABILITY-0001 contract and runbook release ledgers plus templates.

### P2 (Family classification)

- [x] `P2-C1-S1`: classify each extracted scenario by family standing.
- [x] `P2-C1-S2`: record the smallest defensible reason for each classification.
- [x] `P2-C2-S1`: fix the family-agnostic auditable chain semantics before P3.
- [x] `P2-C2-S2`: backfill the required time-audit surfaces on live object-ledger files and templates.

### P3 (Write-back decision)

- [ ] `P3-C1-S1`: decide whether current readers widen, stay narrow, or split sibling lanes.
- [ ] `P3-C1-S2`: record the next bounded packet or no-op path.

## Current Status

- `S4G-1G` is now the bounded Search runtime scenario hard-extraction packet after the first bounded `run-RUNTIME-OBSERVABILITY-001` skeleton exposed a likely mismatch between current readers and the broader scenario universe in code/labs.
- The current lane hypothesis is that the repo already contains more Search-adjacent scenarios than the current `OBSERVABILITY-0001` / `run-RUNTIME-OBSERVABILITY-001` family presently owns.
- `P1` now records a concrete Search scenario inventory from code and corroborates it with labs docs, labs catalog, and retained snapshots/evidence.
- The extracted universe already appears wider than the current reader family and already falls into at least three visible bands: worker fault/recovery, Search verification/gate, and dual-run/dual-write adjacent scenarios.
- The repo now also has explicit reader-object release-ledger landing surfaces for the current runbook and current contract, so later scenario-classification evidence no longer needs to stay trapped only inside the control log.
- `P2` now makes family ownership explicit: worker-chain fault and recovery scenarios classify as `current-family`; supporting infra or cross-surface corroboration scenarios classify as `support-only`; search verification, read-switch, and dual-run or dual-write scenarios classify as `sibling-family`.
- The repo now also has the full auditable chain needed for later reader mutation: `SUP -> parent ledger -> reader` for meaning changes, `PATCH -> reader` for bounded repairs, and paired `SUP` whenever a patch also changes admitted meaning.
- The newly-opened object-ledger live files now separate artifact lifecycle time, source chronology time, and governance-event time so later write-back can be read as change history instead of only as current state.
- The next step is intentionally narrow: use the new classification plus the remediated audit surfaces to decide whether current readers widen, stay narrow, or route sibling lanes without mixing those decisions together.

## Evidence

- Artifacts are the source of truth for later extraction and boundary review; this scaffold records the bounded source anchors only.
- Current source anchors:
  - `backend/scripts/cli_app/scenarios/`
  - `docs/labs/lab-S3A-2A-3A-observability-failure-drills.md`
  - `docs/labs/scenarios/catalog.yml`
  - `docs/logs/support-only/ledger-S3A-2A-combo-observability-triage.md`
  - `docs/logs/support-only/ledger-S3A-2A-R01-runtime-observability-contract-split-and-consumption.md`
  - `docs/logs/log-S4G-1F-search-runtime-only-field-shapes-gap-packet.md`
  - `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  - `docs/governance/contracts/support-only/ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`

### P1-C1-S1S2 (Search runtime scenario inventory extracted and corroborated | 2026-04-27)

- headSha: `pending-commit`
- artifacts: `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md`
- expected:
  - extract the Search runtime scenario universe from concrete code files;
  - corroborate the extracted scenarios with labs docs, labs catalog, and retained evidence;
  - stop treating the current runbook/contract family as an implicit summary of all existing Search scenarios.
- observed:
  - the code inventory now explicitly includes worker-fault/recovery scenarios such as `es_write_block_4xx`, `es_down_connect`, `es_bulk_partial`, `db_claim_contention`, `stuck_reclaim`, `duplicate_delivery`, and `projection_version`;
  - the extracted universe also includes Search-adjacent verification, rehearsal, dual-run, and dual-write scenarios that current readers do not presently own;
  - labs docs, catalog entries, and retained snapshots corroborate that these scenarios are real lane material rather than stale stubs;
  - the remaining unresolved problem is family ownership, not scenario existence.

### P1-C2-S1S2 (Reader-object release ledgers confirmed and scaffolded | 2026-04-27)

- headSha: `pending-commit`
- artifacts:
  - `docs/runbook/support-only/_template-runbook-release-ledger.md`
  - `docs/runbook/support-only/_template-runbook-release-ledger-SUP.md`
  - `docs/runbook/support-only/_template-runbook-release-ledger-PATCH.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger-SUP.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger-PATCH.md`
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  - `docs/runbook/support-only/ledger-runbook-SUP-001-RUNTIME-OBSERVABILITY-001-scenario-family-intake.md`
  - `docs/runbook/support-only/ledger-runbook-PATCH-001-RUNTIME-OBSERVABILITY-001-release-ledger-bootstrap.md`
  - `docs/governance/contracts/support-only/ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
  - `docs/governance/contracts/support-only/ledger-SUP-001-DOC-RUNTIME-OBSERVABILITY-0001-scenario-family-intake.md`
  - `docs/governance/contracts/support-only/ledger-PATCH-001-DOC-RUNTIME-OBSERVABILITY-0001-release-ledger-bootstrap.md`
- expected:
  - confirm the semantic distinction between source-owned ledgers, reader-object release ledgers, and run ledgers;
  - create durable landing surfaces for later contract/runbook phased write-back;
  - keep the current reader bodies narrow while later scenario classification remains unresolved.
- observed:
  - generic templates now exist for both runbook-release and contract-release ledger families;
  - the current runbook and current contract now bind to explicit release-ledger families in frontmatter;
  - live `OBSERVABILITY-0001` contract and runbook release ledgers, plus their first `SUP` and reserved `PATCH` surfaces, now exist as durable staging surfaces;
  - `S4G-1G/P2` can now classify scenarios without forcing all intermediate evidence to remain trapped only in the control log.

### P2-C1-S1S2 (Search runtime scenarios classified by family standing | 2026-04-27)

- headSha: `pending-commit`
- artifacts:
  - `docs/logs/log-S4G-1G-search-runtime-scenario-hard-extraction-packet.md`
- expected:
  - classify each extracted scenario into `current-family`, `support-only`, or `sibling-family`;
  - state the smallest defensible reason for each classification;
  - keep current reader mutation deferred until the later write-back decision.
- observed:
  - same-chain worker fault, recovery, idempotency, and version-risk scenarios now classify as `current-family`;
  - `collector_down` and `shadow_verify_shared_keys` now classify as `support-only` because they corroborate the lane without defining the owned worker chain itself;
  - search verification, read-switch, dual-run, and dual-write scenarios now classify as `sibling-family`;
  - `P3` is now the remaining decision surface for whether the current contract or runbook widens at all.

### P2-C2-S1S2 (Auditable chain semantics and time-audit remediation completed | 2026-04-27)

- headSha: `pending-commit`
- artifacts:
  - `docs/runbook/support-only/_template-runbook-release-ledger.md`
  - `docs/runbook/support-only/_template-runbook-release-ledger-SUP.md`
  - `docs/runbook/support-only/_template-runbook-release-ledger-PATCH.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger-SUP.md`
  - `docs/governance/contracts/support-only/_template-contract-release-ledger-PATCH.md`
  - `docs/runbook/_template-run-ledger.md`
  - `docs/runbook/support-only/_template-run-ledger.md`
  - `docs/runbook/_template-run-ledger-SUP.md`
  - `docs/runbook/support-only/_template-run-ledger-SUP.md`
  - `docs/runbook/support-only/_template-run-ledger-PATCH.md`
  - `docs/runbook/support-only/_template-run-ledger-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-SUP-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/_template-run-ledger-PATCH-WORKFLOW-GITHUB-ISSUES.md`
  - `docs/runbook/support-only/ledger-runbook-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  - `docs/runbook/support-only/ledger-runbook-SUP-001-RUNTIME-OBSERVABILITY-001-scenario-family-intake.md`
  - `docs/runbook/support-only/ledger-runbook-PATCH-001-RUNTIME-OBSERVABILITY-001-release-ledger-bootstrap.md`
  - `docs/governance/contracts/support-only/ledger-DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
  - `docs/governance/contracts/support-only/ledger-SUP-001-DOC-RUNTIME-OBSERVABILITY-0001-scenario-family-intake.md`
  - `docs/governance/contracts/support-only/ledger-PATCH-001-DOC-RUNTIME-OBSERVABILITY-0001-release-ledger-bootstrap.md`
- expected:
  - make the `SUP -> parent ledger -> reader` and `PATCH -> reader` workflow explicit across ledger families;
  - preserve separate artifact lifecycle, source chronology, and governance-event time layers;
  - let later readers tell what changed, what remained unchanged, and which surface carried the change.
- observed:
  - deficient release-ledger and run-ledger templates now expose chronology audit, evidence-time audit, patch-time audit, and write-back-chain rules instead of relying only on minimal headers;
  - the current `OBSERVABILITY-0001` contract and runbook object-ledger files now carry row chronology audit, governance events, and reader notes showing what has and has not landed in reader bodies;
  - the active `SUP` files now carry evidence-time audit so later readers can distinguish evidence admission time from later reader mutation time;
  - the reserved `PATCH` files now carry bounded repair chronology placeholders without pretending that a real repair has already happened.

## Recent changes (for traceability, optional)

- 2026-04-27: opened `S4G-1G` as the bounded Search runtime scenario hard-extraction packet so the lane can re-extract the current scenario universe from code/labs before widening current readers by wording guesswork.
- 2026-04-27: completed `P1` by inventorying concrete Search runtime scenarios from code and corroborating them with labs docs, labs catalog, and retained evidence before any family-boundary classification.
- 2026-04-27: confirmed the new reader-object release-ledger layer and scaffolded the first contract/runbook release ledgers for `OBSERVABILITY-0001` so later phased write-back no longer needs to stay only in the control log.
- 2026-04-27: completed `P2` by classifying the extracted Search runtime scenarios into current-family, support-only, and sibling-family standing without widening the current readers yet.
- 2026-04-27: backfilled full auditable-chain semantics and time-audit structure across the new release-ledger templates, run-ledger templates, and current `OBSERVABILITY-0001` object-ledger live files so later write-back can be read as change history rather than only as current state.