# log-S0G-1B (Phase 1B: legacy logs historical backfill and logs-family bridge governance)

---

**id**: `S0G-1B`
**kind**: `log`
**title**: `legacy logs historical backfill and logs-family bridge governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Contract, History, Evidence, epic/s0, sub/1b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-4A-contract-boundary-map-and-parent-child-clause-flow-governance.md`
  **reference_log_1**: `docs/logs/log-S0F-7C-old-log-decomposition-application-lane.md`
  **reference_log_2**: `docs/logs/log-S0F-7E-supplement-sequencing-time-fields-and-historical-backfill-release-chronology.md`
  **reference_log_3**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_4**: `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  **reference_log_5**: `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  **reference_log_6**: `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md`
  **reference_log_7**: `legacy/from_structured_docs/from-logs/v2-logs/log-S0B-graceful-termination+heathz-readyz+alert-threshold.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-22`
**updated**: `2026-04-22`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while this lane is still classifying family identity, historical-release standing, and ledger write-back shape rather than landing one final contract packet.
- `reviewed` should remain `pending` until the repo fixes whether the two earliest legacy structured logs justify one dedicated legacy family release, one `S0A-2A-R02` write-back, and one explicit bridge into the current `DOC-WORKFLOW-LOGS` family.

## Decision / Outcome

**Decision**:

- `S0G-1B` opens as the bounded follow-up for one narrow historical question: the repo now has direct evidence that the earliest structured-log shape behind the `S0A-2A` logs layer is not the same rule body as the later `DOC-WORKFLOW-LOGS-0001` release.
- This lane treats that problem as `family identity + historical standing + ledger routing` first, not as an immediate in-place rewrite of the current logs contract.
- The immediate deliverable is one defended decision on whether to open a dedicated legacy family release such as `DOC-WORKFLOW-LEGACY-LOGS-0001`, how that release should be marked if it is historical-only, and how `S0A-2A-R02` should stop reading as deferred background once the earliest direct evidence is admitted.

**Default choices (phase defaults / v1)**:

- Do not force the two earliest legacy structured logs into `DOC-WORKFLOW-LOGS-0001` if their owned meaning is materially different from the later `structured log identity and front matter` rule body.
- If the earlier material proves one independently judgeable historical logs state, prefer opening a separate `DOC-WORKFLOW-LEGACY-LOGS` family release rather than stretching the narrower `DOC-WORKFLOW-LOGS` family backward by assumption.
- If the resulting legacy release exists only to preserve chronology and has no surviving current rule body, it may be recorded as a historical-only release with whole-release `retired` standing, `history-backfilled` clause admission, and one explicit `Legacy Redirect`.
- Treat this as one special-case bridge: the later `DOC-WORKFLOW-LOGS-0001` reader may supersede or retire the earlier legacy release without carrying forward its clause body when the two releases do not share the same owned meaning.
- Before any contract file is emitted, extract one low-cardinality structure summary from the two earliest legacy logs so the later contract packet can be filled from defended headings and repeated shapes rather than from memory.
- If `S0A-2A-R02` gains direct evidence through this lane, prefer first changing the parent ledger from `deferred` to one explicit historical-review or direct-evidence state rather than silently treating the old deferred note as resolved.

## PR Summary Inputs (optional)

- This packet is expected to drive later contract and ledger write-back, so the review surface should focus on family identity, retired historical-release semantics, and the bridge between a legacy family and the current logs family.

**PR summary bullets**:

- Decide whether the earliest structured-log shape should open as one dedicated `DOC-WORKFLOW-LEGACY-LOGS` family release instead of being forced into the current `DOC-WORKFLOW-LOGS` family.
- Fix how a historical-only retired release should read when no earlier clause body survives into the current logs contract.
- Extract one simple structure summary from the two earliest legacy logs so `S0A-2A-R02` and any later `LEGACY-LOGS-0001` packet can be filled from defended evidence.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.md`
- Runbook: ``
- Evidence artifact: ``

## Exported Sections / Outlet Ownership

- This slice starts as one `contract + support-only ledger + log-retained core` lane.
- The expected first landing is one defended historical-family rule plus one ledger-routing verdict; whether a stable legacy contract file and current-family bridge should leave this log depends on the lane verdict rather than being assumed at scaffold time.

**Outlet ownership**:

- `contract`: expected landing surface for any dedicated legacy logs family release plus any required bridge notes on the current logs family
- `runbook`: no-op by default
- `view`: no-op by default; a reader summary should wait until the historical-family and bridge semantics are explicit
- `index/front-door`: possible later landing if the workflow contracts index needs one legacy-logs reader route
- `disposition/placement`: expected landing for the `S0A-2A-R02` deferred-to-reviewed write-back and any later standing note on the legacy-logs placement path
- `log-retained core`: the lane boundary, family-identity test, extracted legacy structure summary, and evidence ledger remain here

## Definitions (optional)

- **legacy logs family**: one historical-only workflow family candidate used when the earliest structured-log rule body is materially different from the later `DOC-WORKFLOW-LOGS` family and should not be read as merely an earlier revision of that later contract.
- **historical-only release**: one contract release retained to preserve chronology even though it is no longer the current reader and may have no direct clause carry-forward into the later current family reader.
- **bridge without carry-forward**: one lineage note where a later release replaces or retires an earlier historical reader while explicitly stating that the earlier clause body was not absorbed into the later current rule body.
- **simple legacy structure summary**: one low-cardinality extraction of repeated headings, section roles, and operational shape from the two earliest legacy logs, used as fill guidance for later contract drafting without pretending the old logs already match the current template.

## Simple Legacy Structure Extraction

- Shared low-structure shape across the two earliest legacy logs:
  - one plain title line plus lightweight `Status` and `links`
  - one `Background` section that explains `why this capability exists`
  - one `What/How to do` section that owns the operational rule body
  - numbered capability blocks under `What/How to do`
  - each numbered block keeps a `draft` form and one later `adopted` form
  - optional executable or validation appendix after the main rule body rather than mixed into the earlier numbered blocks
- `log-S0A-dlq-replay-platform.md` simple structure:
  - capability thesis first: `DLQ + replay as platform capability`
  - four numbered rule blocks:
    - standardized DLQ contract across projections
    - replay as one shared operator mental model
    - system-level SLO and dashboard/alert reading
    - multi-projection control-group diagnosis
  - rule body is cross-projection and platform-facing rather than file-identity or front-matter-facing
- `log-S0B-graceful-termination+heathz-readyz+alert-threshold.md` simple structure:
  - runtime-hardening thesis first: `worker from script to daemon`
  - four numbered rule blocks:
    - graceful termination
    - `/healthz` and `/readyz`
    - alert thresholds and runtime guardrails
    - validation plan that turns runtime hardening into executable labs
  - optional appendix keeps executable snippets and alert examples outside the core numbered rule body
- Simple extraction consequence for later `LEGACY-LOGS-0001` filling:
  - the earliest logs shape is best described as `capability-thesis + numbered operational rule blocks + draft/adopted transition`, not as `identity/front-matter/cutover` governance
  - the earliest logs shape is therefore materially different from the current `DOC-WORKFLOW-LOGS-0001` rule body and should not be treated as the same family by default

## Constraints

- Do not assume that the presence of two early structured logs automatically makes them the first release of `DOC-WORKFLOW-LOGS`.
- Do not force `introduced` onto every clause in a later-recorded historical-only release if the lane is intentionally admitting that state as `history-backfilled` chronology rather than reconstructing full internal release-time clause birth order.
- Do not mutate `DOC-WORKFLOW-LOGS-0001` first and decide the family boundary later.
- Do not resolve `S0A-2A-R02` by prose-only note once direct evidence is present; the parent ledger must carry an explicit resolution state.
- Do not widen this lane into a full old-logs migration sweep; it is limited to the two earliest legacy structured-log anchors and the `S0A-2A` logs slice they sharpen.

## Scope

- `P0`: classify whether the two earliest legacy structured logs justify one separate legacy family rather than one earlier revision of `DOC-WORKFLOW-LOGS`
- `P1`: extract one simple structure summary from the two earliest legacy logs for later contract filling
- `P2`: define the historical-release standing rule for a legacy logs release whose rows are all retired/history-backfilled and whose clause body does not carry into `DOC-WORKFLOW-LOGS-0001`
- `P3`: define the minimum bridge write-back on `DOC-WORKFLOW-LOGS-0001` plus the `S0A-2A-R02` ledger adjudication path

## Success Criteria (DoD)

- The repo has one explicit verdict on whether the two earliest structured logs belong to a separate legacy logs family.
- The lane records whether `DOC-WORKFLOW-LEGACY-LOGS-0001` is the right first packet shape or whether the evidence should stay at ledger/SUP level only.
- The lane records one defended rule for a historical-only retired release whose rows are admitted as `history-backfilled` and do not survive as carried-forward clauses in the later current logs contract.
- The lane records one minimum bridge rule stating how `DOC-WORKFLOW-LOGS-0001` should point back to that earlier legacy reader without implying clause absorption.
- The lane records one concrete write-back target for `S0A-2A-R02` so the logs layer no longer remains deferred once the direct evidence is admitted.
- The lane preserves one simple structure summary of the two earliest legacy logs that later contract drafting can reuse.
- The lane may emit one first historical-only legacy contract draft plus the corresponding `S0A-2A-R02` write-back before the reciprocal bridge note is added to `DOC-WORKFLOW-LOGS-0001`.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the family-identity verdict is explicit;
  - the historical-only release rule is explicit;
  - the current-family bridge rule is explicit;
  - the `S0A-2A-R02` adjudication path is explicit;
  - the simple legacy structure summary is recorded.
- `stable` for this lane does not require the reciprocal `DOC-WORKFLOW-LOGS-0001` bridge note to be emitted yet; it requires the repo to know whether the legacy file should exist and how it should read.

## P0 (Contract | v1)

### P0-C1-S1 (Legacy family versus current logs family boundary fixed | v1)

- The lane must first decide whether the two earliest structured logs represent one independently judgeable historical rule body.
- If yes, they should open as one separate legacy family candidate instead of being treated as the first revision of the later `DOC-WORKFLOW-LOGS` family by default.

### P0-C1-S2 (Historical-only retired release semantics fixed | v1)

- If the earlier logs state is admitted as one dedicated historical release whose rule body does not carry forward into the later current logs family, the release may be marked `retired` as a whole historical reader.
- Under this rule, the release may admit its rows as `history-backfilled` rather than `introduced` when the lane is preserving chronology without reconstructing the earlier file as one defended same-time release authoring event.
- The file should then use one explicit `Legacy Redirect` so readers know to consult the later current-family reader for present governance meaning.

### P0-C1-S3 (Bridge without clause carry-forward fixed | v1)

- If the legacy release and the later `DOC-WORKFLOW-LOGS-0001` release do not share the same owned clause body, the bridge should say so explicitly.
- Under this rule, the later current-family file should point back to the earlier historical reader as predecessor context or retired history, but it must not imply `absorbed_from` or clause carry-forward when none is actually defended.

### P0-C1-S4 (Legacy family candidate fixed as `DOC-WORKFLOW-LEGACY-LOGS` | v1)

- The current candidate family id for the earliest structured-log historical reader is now fixed as `DOC-WORKFLOW-LEGACY-LOGS`.
- Under this rule, the candidate should stay in the canonical workflow contract root rather than reviving the moved legacy contract trees.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0G-1B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step or multiple consecutive steps grouped within one phase / cycle.

**Branch convention**:

- This slice should stay on `S0G-docs-management-v7` while it remains a bounded follow-up inside the current `S0G` docs-management spine.

**Commit discipline (recommended)**:

- Keep `family-identity decision`, `structure extraction`, `legacy contract emission`, and `ledger/current-family write-back` separated when practical so later archaeology can see which rule was fixed in which unit.

## Plan (draft)

### P1 (Simple structure extraction)

- `P1-C1-S1`: extract the repeated top-level sections and operational shape from `log-S0A-dlq-replay-platform.md`
- `P1-C1-S2`: extract the repeated top-level sections and operational shape from `log-S0B-graceful-termination+heathz-readyz+alert-threshold.md`

### P2 (Historical release semantics)

- `P2-C1-S1`: decide whether `DOC-WORKFLOW-LEGACY-LOGS-0001` should be emitted as one historical-only retired release
- `P2-C1-S2`: decide whether its rows should be represented as all-`history-backfilled` and all-`retired` in the absence of defended clause carry-forward

### P3 (Bridge and ledger adjudication)

- `P3-C1-S1`: define the minimum bridge note required on `DOC-WORKFLOW-LOGS-0001`
- `P3-C1-S2`: define the minimum `S0A-2A-R02` write-back once the direct legacy evidence is admitted

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: legacy family versus current logs family boundary fixed
- [ ] `P0-C1-S2`: historical-only retired release semantics fixed
- [ ] `P0-C1-S3`: bridge without clause carry-forward fixed
- [x] `P0-C1-S4`: legacy family candidate fixed as `DOC-WORKFLOW-LEGACY-LOGS`

### P1 (Simple structure extraction)

- [ ] `P1-C1-S1`: extract simple structure from the first legacy logs packet
- [ ] `P1-C1-S2`: extract simple structure from the second legacy logs packet

### P2 (Historical release semantics)

- [x] `P2-C1-S1`: decide whether `DOC-WORKFLOW-LEGACY-LOGS-0001` should be emitted
- [x] `P2-C1-S2`: decide whether the legacy rows should be represented as retired `history-backfilled` state

### P3 (Bridge and ledger adjudication)

- [ ] `P3-C1-S1`: define the minimum bridge note on `DOC-WORKFLOW-LOGS-0001`
- [x] `P3-C1-S2`: define the minimum `S0A-2A-R02` write-back

## Current Status (recommended)

- `S0G-1B` is now opened as the bounded lane for legacy structured-log history, retired historical-release semantics, and the unresolved `S0A-2A-R02` logs-layer adjudication path.
- The repo already has enough evidence to say that the two earliest legacy structured logs are not the same rule body as the current `DOC-WORKFLOW-LOGS-0001` release.
- `DOC-WORKFLOW-LEGACY-LOGS-0001` is now emitted as the first historical-only legacy logs draft, and `S0A-2A-R02` no longer remains deferred background only.
- The immediate next step is `P3-C1-S1`: add the reciprocal bridge note on `DOC-WORKFLOW-LOGS-0001` so the later current-family reader points back to the historical-only legacy release without implying clause absorption.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key extracted structure anchors, and any later contract or ledger write-back artifacts.
- This section is the human-facing ledger and should remain separate from later contract text.

### P0-C1-S1S2S3 (legacy logs historical lane opened | 2026-04-22)

- headSha: ``
- artifacts:
  - `docs/logs/log-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.md`
  - `legacy/from_structured_docs/from-logs/v2-logs/log-S0A-dlq-replay-platform.md`
  - `legacy/from_structured_docs/from-logs/v2-logs/log-S0B-graceful-termination+heathz-readyz+alert-threshold.md`
  - `docs/governance/contracts/workflow/logs/DOC-WORKFLOW-LOGS-0001-structured-log-identity-and-front-matter.md`
  - `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
- expected:
  - open one bounded lane for the earlier legacy structured-log shape
  - record why the current logs family is not enough on its own
  - define the decision surface for legacy-family emission, bridge semantics, and ledger adjudication
- observed:
  - the lane is opened
  - the family-identity, retired historical-release, and `S0A-2A-R02` adjudication questions are now explicit

### P0-C1-S4 + P2-C1-S1S2 + P3-C1-S2 (legacy logs draft emitted and `S0A-2A-R02` written back | 2026-04-22)

- headSha: ``
- artifacts:
  - `docs/governance/contracts/workflow/legacy logs/DOC-WORKFLOW-LEGACY-LOGS-0001-earliest-structured-logs-capability-thesis-and-numbered-rule-blocks.md`
  - `docs/logs/support-only/ledger-S0A-2A-tools-workflow-log-lab-runbook-adr.md`
  - `docs/logs/log-S0G-1B-legacy-logs-historical-backfill-and-logs-family-bridge-governance.md`
- expected:
  - fix the candidate family id for the earliest structured-log historical reader
  - emit one first historical-only legacy logs draft with retired `history-backfilled` rows
  - stop leaving `S0A-2A-R02` at deferred bounded background only
- observed:
  - `DOC-WORKFLOW-LEGACY-LOGS-0001` now exists as one historical-only legacy logs draft under the canonical workflow contract root
  - the draft now records retired `history-backfilled` rows for the earlier capability-thesis and numbered-rule-block reader shape
  - `S0A-2A-R02` now reads as one explicit historical-review slice under `DOC-WORKFLOW-LEGACY-LOGS-0001` rather than as deferred background only

## Recent changes (for traceability, optional)

- 2026-04-22: opened `S0G-1B` so the earliest legacy structured-log shape can be judged as a distinct historical problem instead of being silently forced into the current `DOC-WORKFLOW-LOGS` family.
- 2026-04-22: emitted `DOC-WORKFLOW-LEGACY-LOGS-0001` as the first historical-only legacy logs draft and wrote back `S0A-2A-R02` from deferred background to explicit historical review.