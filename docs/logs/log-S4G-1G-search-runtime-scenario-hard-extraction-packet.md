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
| `R01` | `scenario registry mismatch` | `runbook-candidate` | The current Search runtime readers should not be treated as the full scenario universe until code and labs extraction explicitly classify which scenarios belong to the current family. | `runbook` | `ready` | `RG-01` | `S4G-1F`; `run-RUNTIME-OBSERVABILITY-001`; code scenarios; labs` | Opening rule for this packet. |
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
- `P1`: hard-extract the Search runtime scenario universe from code + labs + retained evidence
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

### P2 (Family classification)

- P2-C1-S1: classify each extracted scenario into current-family, support-only, or sibling-family.
- P2-C1-S2: record the smallest defensible reason for each classification.

### P3 (Write-back decision)

- P3-C1-S1: decide whether current `OBSERVABILITY-0001` / `run-RUNTIME-OBSERVABILITY-001` should widen, stay narrow, or route sibling lanes.
- P3-C1-S2: record the next bounded packet or no-op path.

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: packet opening and extraction rule fixed.
- [x] `P0-C1-S2`: classification boundary fixed.
- [x] `P0-C1-S3`: evidence contract fixed.

### P1 (Hard extraction)

- [ ] `P1-C1-S1`: inventory Search runtime scenarios from code.
- [ ] `P1-C1-S2`: corroborate scenarios with labs docs, catalog, and retained evidence.

### P2 (Family classification)

- [ ] `P2-C1-S1`: classify each extracted scenario by family standing.
- [ ] `P2-C1-S2`: record the smallest defensible reason for each classification.

### P3 (Write-back decision)

- [ ] `P3-C1-S1`: decide whether current readers widen, stay narrow, or split sibling lanes.
- [ ] `P3-C1-S2`: record the next bounded packet or no-op path.

## Current Status

- `S4G-1G` is now the bounded Search runtime scenario hard-extraction packet after the first bounded `run-RUNTIME-OBSERVABILITY-001` skeleton exposed a likely mismatch between current readers and the broader scenario universe in code/labs.
- The current lane hypothesis is that the repo already contains more Search-adjacent scenarios than the current `OBSERVABILITY-0001` / `run-RUNTIME-OBSERVABILITY-001` family presently owns.
- The next step is intentionally narrow: extract those scenarios from code + labs first, then classify family ownership before widening any current reader.

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

## Recent changes (for traceability, optional)

- 2026-04-27: opened `S4G-1G` as the bounded Search runtime scenario hard-extraction packet so the lane can re-extract the current scenario universe from code/labs before widening current readers by wording guesswork.