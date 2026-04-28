# log-S0G-5C (Phase 5C: code-first runbook faces and release decision governance)

---

**id**: `S0G-5C`
**kind**: `log`
**title**: `code-first runbook faces and release decision governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Runbook, Evidence, epic/s0, sub/5c`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-5B-code-oriented-contract-faces-and-release-decision-governance.md`
  **reference_log_1**: `docs/logs/draft/draft-001.md`
  **reference_log_2**: `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
  **reference_log_3**: `docs/runbook/_template-runbook.md`
  **reference_log_4**: `docs/runbook/support-only/_template-runbook-release-ledger.md`
  **reference_log_5**: `docs/runbook/support-only/_template-run-ledger.md`
  **reference_log_6**: `docs/logs/_template-log-phase-drills-evidence.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/5c`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-28`
**updated**: `2026-04-28`
**reviewed**: `pending`
**source_reader_model**: `mixed-source-v1`
**extraction_surface_version**: `extractable-rules-v1`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are artifact-lifecycle fields only.
- This packet is about runbook structure, operator-surface ownership, and release-decision rules; it must not widen source-log frontmatter into runbook-effective or run-validity time.
- `reviewed` should remain `pending` until the repo fixes one defended code-first runbook model and decides whether the pilot runbook stays within `001` or requires `002`.

## Decision / Outcome

**Decision**:

- `S0G-5C` opens as the bounded governance packet for redesigning runbooks from `ledger-aware but mixed` into `code-first operator surfaces`.
- The packet is expected to resolve three concrete questions in one lane:
  - should the primary runbook template be rewritten around `Current Operator Faces`, `Code Evidence Attachments`, `Scenario Registry`, `Operator Chronology`, and `Release Decision Table`;
  - is the current runbook release-ledger chain sufficient for code-first intake, or does the repo need one new code-first support ledger for operator-surface extraction before writeback;
  - should `run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton` remain `001` after structural rewrite, or does its widened scenario surface already justify `002`.
- The packet is `model-and-gate first`: it should not silently widen the positive operator meaning of the pilot runbook before the release-decision rule is explicit.

**Default choices (phase defaults / v1)**:

- Runbooks should default to a code-first current-reader model when they govern stable executable entrypoints, bounded switches, admitted drill scenarios, and explicit evidence contracts.
- `Current Operator Faces` should be the primary current-semantic surface for new code-first runbooks.
- `Code Evidence Attachments` should record executable anchors and signal hooks separately from the runbook's current operator meaning.
- `Scenario Registry` should remain an explicit current-owned surface when admitted scenarios change operator expectations.
- Release opening should be driven by reader-visible operator-surface delta, not by raw scenario count alone and not by formatting-only rewrite.
- The runbook release ledger should remain the first candidate intake surface; only add a new code-first support ledger if release-ledger tables cannot keep code extraction, scenario routing, and writeback decisions separated cleanly.
- draft 阶段默认继续把 source log 当作集中面；如果 runbook model、release gate、或 pilot 001/002 standing 仍在变化，不要过早把这条 lane 拆成更多 sibling packets。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.

## Extractable Rule Surface (recommended)

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `Decision / Outcome` | `runbook-candidate` | Code-first runbooks should separate current operator faces, code evidence attachments, scenario registry, operator chronology, and release decision gates instead of mixing bridge, coverage, and widening history in one body. | `runbook` | `ready` | `RG-01` | `docs/logs/draft/draft-001.md; docs/runbook/_template-runbook.md` | `Primary runbook-model shift.` |
| `R02` | `Default choices` bullets 1-4 | `runbook-candidate` | Reader-visible operator-surface delta, especially admitted scenario-surface widening, should decide whether a runbook stays on the same release or opens a new release. | `runbook` | `ready` | `RG-01` | `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` | `Runbook release-gate rule.` |
| `R03` | `Decision / Outcome` first bullet | `runbook-candidate` | The primary runbook template should be rewritten around current operator faces and release decision rules before the pilot runbook is restructured. | `runbook` | `ready` | `RG-02` | `docs/runbook/_template-runbook.md` | `Template-first sequencing rule.` |
| `R04` | `Decision / Outcome` second bullet | `runbook-candidate` | The runbook release ledger should be evaluated as the first code-first intake surface; only if it remains too mixed should the repo open a dedicated code-first operator-surface extraction ledger. | `runbook` | `ready` | `RG-02` | `docs/runbook/support-only/_template-runbook-release-ledger.md` | `Ledger sufficiency rule.` |
| `R05` | `Decision / Outcome` second bullet | `runbook-candidate` | `run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton` should be the pilot packet for deciding whether structure-only rewrite stays on `001` or whether the widened current scenario registry already belongs in `002`. | `runbook` | `ready` | `RG-03` | `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` | `Pilot decision rule.` |

### Shared Reason Groups (optional, recommended when multiple rows share one rationale)

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | The repo needs one explicit runbook model where current operator meaning, executable evidence, admitted scenario ownership, and release gating stop sharing one mixed surface. | `draft-001; current runbook template; pilot runbook` | `Primary runbook-model rationale.` |
| `RG-02` | `R03; R04` | The first pass should prefer rewriting the existing runbook template and release-ledger chain before multiplying new support-only surfaces. | `runbook template; runbook release ledger template` | `Template and ledger sufficiency rationale.` |
| `RG-03` | `R05` | The pilot runbook already looks code-coupled, so the hard question is no longer whether code-first applies but whether the widened scenario surface still belongs in the current release. | `run-RUNTIME-OBSERVABILITY-001...` | `Pilot release-decision rationale.` |

## PR Summary Inputs (optional)

- This packet is expected to land as a runbook-governance planning lane, so review should focus on the runbook model, intake chain, and 001/002 gate rather than on direct operator-procedure expansion.

**PR summary bullets**:

- Define the code-first runbook model and explicit release gate for operator-surface changes.
- Decide whether the current runbook release-ledger chain is sufficient or whether a new code-first support ledger is needed.
- Use `run-RUNTIME-OBSERVABILITY-001` as the pilot for deciding whether the widened scenario registry stays in `001` or opens `002`.

**PR checklist source**:

- Default source: reuse this log's execution checklist.

**PR links**:

- Log: `docs/logs/log-S0G-5C-code-first-runbook-faces-and-release-decision-governance.md`
- Runbook: `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md`
- Evidence artifact: ``

## Exported Sections / Outlet Ownership

- This packet is expected to export to `runbook` first and retain the model/gate rationale here until the pilot execution round actually lands.

**Outlet ownership**:

- `contract`: no-op for now; contract-side model already moved in `S0G-5B`
- `runbook`: rewrite the runbook template, decide release-ledger sufficiency, and stage the pilot `001/002` decision
- `view`: no-op for now
- `index/front-door`: no-op for now
- `disposition/placement`: no-op for now
- `log-retained core`: packet rationale, release-gate wording, pilot sequencing, and execution chain remain here

## Definitions (optional)

- `Current Operator Faces`: the current effective operator semantics of a runbook, organized by stable operator-facing surfaces rather than one mixed bridge or coverage stack.
- `Code Evidence Attachments`: a fact table for stable entrypoints, switches, scenario hooks, and evidence-contract anchors that support the runbook without automatically becoming operator promises.
- `Scenario Registry`: the explicit current-owned list of admitted scenarios whose presence changes operator expectations for the runbook.
- `Operator Chronology`: the append-only time-ordered history of how current operator surfaces and admitted scenarios became what they are now.
- `operator-surface delta`: a reader-visible change to what the runbook currently tells an operator they may rely on or are expected to run.

## Constraints

- Do not silently widen the positive operator meaning of the pilot runbook while the release gate is still being defined.
- Do not treat code-adjacent switches or scenario files as proof that all implied fallback or recovery semantics are already owned.
- Do not add a new support-only ledger unless the current runbook release-ledger chain proves insufficient after explicit evaluation.
- Do not hide a real `001 -> 002` release change inside a structure-only rewrite.

## Semantic Delta Structure (optional, recommended when a source log may change current contract meaning)

| delta id | face id or candidate face | current semantic | candidate semantic | delta class | reader visible change | primary evidence refs | downstream owner | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SD-01` | `runbook-template-model` | `runbook guidance is bridge-and-scenario-first with optional evolution tables` | `runbook guidance becomes face-first with separate code evidence, scenario registry, chronology, and release decision surfaces` | `boundary-restructure` | `yes` | `docs/runbook/_template-runbook.md; docs/logs/draft/draft-001.md` | `runbook` | `Primary template-level restructuring candidate.` |
| `SD-02` | `release-ledger-intake-model` | `runbook release ledger admits intake rows and scenario routing but has no explicit code-first operator-surface gate` | `release ledger explicitly decides whether code-first intake stays here or needs a dedicated support-only extraction ledger` | `clarification-only` | `no` | `docs/runbook/support-only/_template-runbook-release-ledger.md` | `runbook` | `Ledger sufficiency evaluation first.` |
| `SD-03` | `RUNTIME-OBSERVABILITY-001 pilot` | `current release mixes bounded skeleton meaning with widened current-family scenario rows` | `structure-only rewrite may keep 001 narrow, or widened admitted scenarios may move to 002` | `semantic-change` | `yes` | `docs/runbook/run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` | `runbook` | `This is the release decision the pilot must resolve.` |

## Release Decision Table (optional, recommended when a source log may drive same-release writeback versus new release)

| face id | current release semantic | candidate semantic | delta class | reader visible change | contract action | target release or outlet | decision basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RUNTIME-OBSERVABILITY-001 template model` | `Current runbook template is code-coupled but still mixed.` | `Rewrite the template around current operator faces and explicit release decisions.` | `clarification-only` | `no` | `same-release-evidence-writeback` | `runbook template` | `Template rewrite alone should not mint a new runbook release.` | `Template-first change only.` |
| `admitted-scenario-surface` | `Current 001 body includes the defended proof path plus widened current-family scenario registry rows.` | `If those widened scenarios materially change what operators should read as covered now, keep 001 narrow and move widened registry to 002.` | `semantic-change` | `yes` | `new-release-required` | `run-RUNTIME-OBSERVABILITY-002-*` | `Scenario widening is operator-visible current meaning.` | `Main pilot gate.` |
| `non-ownership-boundary` | `Coexistence and sibling-lane procedure remain out of scope.` | `If later packets want positive coexistence or cutover procedure here, route to a later runbook release or sibling lane rather than silent same-release widening.` | `boundary-restructure` | `yes` | `move-to-runbook` | `later runbook release or sibling lane` | `Non-ownership is itself current reader meaning.` | `Anti-fabrication gate.` |

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `already-satisfied` | `S0G-5C` source log | `Has the packet named the runbook-model rewrite and pilot gate tightly enough to route?` | `R01-R05 plus semantic delta and release decision tables` | `Packet boundary is explicit.` |
| `SUP` | `not-required` | `n/a` | `Is this later evidence against one accepted source-owned row?` | `explicit no-SUP verdict` | `This lane opens model/governance work first.` |
| `parent ledger` | `not-required` | `n/a` | `Does this packet already change one source-owned routing verdict?` | `explicit no-parent-ledger verdict` | `The packet opens the work lane but does not execute the pilot writeback yet.` |
| `contract impact decision` | `required` | `S0G-5C` | `Is the pilot change structure-only, or does it already imply a runbook release split?` | `explicit classified verdict` | `Main gate for the lane.` |
| `contract mutation` | `conditional` | `runbook template, release ledger template, and pilot runbook` | `Should the repo rewrite the templates and pilot runbook now?` | `future writeback packet or explicit plan` | `This packet defines the execution lane first.` |
| `transition register update` | `conditional` | `future runbook family register or n/a` | `Would a 001/002 split change which runbook release is first-open now?` | `explicit deferred verdict` | `Only needed if the pilot opens 002.` |
| `bridged contract reconciliation` | `conditional` | `affected contract and runbook readers` | `Will OBSERVABILITY contract and runbook readers need explicit routing reconciliation after the pilot decision?` | `explicit deferred verdict` | `Follow-on only after the pilot executes.` |

## Scope

- `P0`: define the code-first runbook model, release gate, and decision vocabulary
- `P1`: rewrite the runbook template and assess release-ledger sufficiency for code-first intake
- `P2`: restructure the `RUNTIME-OBSERVABILITY-001` pilot runbook
- `P3`: decide whether the pilot remains `001` or splits into `001` plus `002`

## Success Criteria (DoD)

- The repo has one explicit code-first runbook model that separates operator faces, code evidence, scenario registry, chronology, and release decisions.
- The runbook release-ledger chain has an explicit verdict: sufficient as-is after enhancement, or insufficient and needing one dedicated code-first support ledger.
- The pilot runbook has one explicit `001` versus `002` release decision gate rather than relying on prose judgment.
- The packet states clearly which operator-surface changes are same-release writeback and which must open a new runbook release.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the code-first runbook model is explicit;
  - the release-ledger sufficiency rule is explicit;
  - the pilot `001/002` decision criteria are explicit;
  - the next step is one bounded template/pilot execution packet rather than another model debate.

## P0 (Contract | v1)

### P0-C1-S1 (Code-first runbook model fixed | v1)

- New code-first runbooks should separate:
  - `Current Operator Faces`
  - `Code Evidence Attachments`
  - `Scenario Registry`
  - `Operator Chronology`
  - `Release Decision Table`
- This separation keeps current operator meaning, executable evidence, and widening history readable without one mixed bridge-plus-coverage surface.

### P0-C1-S2 (Runbook release decision rule fixed | v1)

- Runbook release creation should be driven by reader-visible operator-surface delta.
- Admitted scenario-surface widening is normally reader-visible and should default to `new release required` unless the packet can defend that the current operator expectation did not materially change.

### P0-C1-S3 (Ledger sufficiency rule fixed | v1)

- Evaluate the current runbook release ledger as the first code-first intake surface.
- Add a new dedicated code-first support ledger only if the release ledger cannot keep operator-surface extraction, scenario routing, and writeback decisions separated cleanly.

## Plan (draft)

### P1 (Template and intake chain)

- `P1-C1-S1`: rewrite the primary runbook template around current operator faces and release-decision structure
- `P1-C1-S2`: enhance the runbook release-ledger template so code-first intake and release decisions are explicit

### P2 (Pilot runbook)

- `P2-C1-S1`: restructure `run-RUNTIME-OBSERVABILITY-001-search-outbox-worker-drill-first-skeleton.md` as the code-first pilot

### P3 (Release split decision)

- `P3-C1-S1`: decide whether the widened current scenario surface remains on `001` or belongs in `002`

## Execution Checklist (unchecked)

### P0 (Contract)

- [ ] `P0-C1-S1`: code-first runbook model fixed
- [ ] `P0-C1-S2`: runbook release decision rule fixed
- [ ] `P0-C1-S3`: ledger sufficiency rule fixed

### P1 (Template and intake chain)

- [ ] `P1-C1-S1`: primary runbook template rewritten around current operator faces and release decisions
- [ ] `P1-C1-S2`: runbook release-ledger template enhanced for code-first intake and release decisions

### P2 (Pilot runbook)

- [ ] `P2-C1-S1`: `run-RUNTIME-OBSERVABILITY-001...` restructured as the code-first pilot

### P3 (Release split decision)

- [ ] `P3-C1-S1`: `001` versus `002` decision recorded explicitly for the pilot runbook

## Current Status (recommended)

- `S0G-5C` is now opened as the bounded planning lane for code-first runbook governance.
- The packet does not yet claim that the runbook template, release-ledger template, or pilot runbook has been rewritten.
- The immediate next step is to execute `P1-C1-S1S2`, then use the rewritten model to classify the pilot runbook as `001 structure-only rewrite` or `001/002 release split`.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this packet currently records the intended writeback surfaces only.

### P0-C1-S1S3 (Lane opening | 2026-04-28)

- headSha: `pending-next-commit`
- artifacts:
  - `docs/logs/log-S0G-5C-code-first-runbook-faces-and-release-decision-governance.md`
  - `docs/logs/log-S0G-docs-management-v7.md`
- expected:
  - one bounded `S0G-5C` packet opens the code-first runbook model lane
  - the parent `S0G` spine points to this new follow-up explicitly
- observed:
  - packet opened; parent spine linked; execution work remains pending

## Recent changes (for traceability, optional)

- 2026-04-28: opened `S0G-5C` as the bounded runbook-governance follow-up to the contract-side `S0G-5B` work.
- 2026-04-28: fixed the first execution question for the lane as `runbook template rewrite + release-ledger sufficiency + OBSERVABILITY-001/002 split decision` rather than broad runbook expansion.