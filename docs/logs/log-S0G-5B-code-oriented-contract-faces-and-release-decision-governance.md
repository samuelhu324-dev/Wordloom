# log-S0G-5B (Phase 5B: code-oriented contract faces and release decision governance)

---

**id**: `S0G-5B`
**kind**: `log`
**title**: `code-oriented contract faces and release decision governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Contract, Evidence, epic/s0, sub/5b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-5A-time-semantics-and-effective-window-governance.md`
  **reference_log_1**: `docs/logs/draft/draft-001.md`
  **reference_log_2**: `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
  **reference_log_3**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_4**: `docs/logs/_template-log-phase-drills-evidence.md`
  **reference_log_5**: `docs/governance/contracts/support-only/_template-contract-face-extraction-ledger.md`
  **reference_log_6**: `docs/governance/contracts/support-only/_template-semantic-chronology-sharpening-ledger.md`
  **reference_log_7**: `docs/governance/contracts/support-only/_template-contract-writeback-ledger.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/5b`
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
- This packet changes contract structure and release-decision rules; it does not widen source-log frontmatter into contract-effective time.
- `reviewed` should remain `pending` until the pilot model is accepted as the preferred current template shape for new code-oriented contract releases.

## Decision / Outcome

**Decision**:

- `S0G-5B` opens as the bounded governance packet that converts the current mixed `statement/bridge/coverage` contract reading model into a code-oriented semantic model centered on `Current Contract Faces`, `Code Evidence Attachments`, `Semantic Chronology`, and `Release Decision Table`.
- The packet delivers four concrete writebacks in one lane:
  - restructure `DOC-RUNTIME-OBSERVABILITY-0001` as the pilot contract;
  - rewrite the primary contract record template around the new face-oriented model;
  - add three new support-only ledger templates for `face extraction`, `chronology sharpening`, and `contract writeback`;
  - extend the source-log template so future packets can state semantic delta and release decisions explicitly before downstream mutation.
- The packet is `structure-migration first`: it should sharpen ownership, evidence placement, and release-decision rules without expanding the positive semantics currently owned by `DOC-RUNTIME-OBSERVABILITY-0001`.

**Default choices (phase defaults / v1)**:

- `Current Contract Faces` should become the default current-semantic contract table for new code-oriented releases.
- `Code Evidence Attachments` should carry code facts separately from reader-facing contract promises.
- `Semantic Chronology` should be append-only and ordered by semantic-effective time rather than by release number alone.
- Release opening should be driven by face-level reader-visible semantic delta, not by raw repo diff size.
- `statement/bridge/coverage` surfaces may remain only as compatibility layers for older families; they are no longer the preferred primary shape for new work.
- draft 阶段默认继续把 source log 当作集中面；如果 pilot contract、template 命名、或 release gate 还在变化，不要过早把这次治理重构拆成更多 sibling packets。
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.

## Extractable Rule Surface (recommended)

| packet id | source anchor | extraction class | candidate text | downstream owner | split status | shared reason group | evidence refs | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R01` | `Decision / Outcome` | `contract-candidate` | Code-oriented contracts should separate current semantic faces, code evidence attachments, semantic chronology, and release decision gates instead of mixing them in one release-first clause stack. | `contract` | `ready` | `RG-01` | `docs/logs/draft/draft-001.md` | `Primary model shift for the packet.` |
| `R02` | `Default choices` bullets 1-4 | `contract-candidate` | Face-level reader-visible semantic delta, not raw diff size, should decide whether a contract opens a new release or stays on same-release evidence writeback. | `contract` | `ready` | `RG-01` | `docs/governance/contracts/_template-contract-record.md` | `This is the release-gate rule.` |
| `R03` | `Decision / Outcome` second bullet | `contract-candidate` | `DOC-RUNTIME-OBSERVABILITY-0001` should be used as the first pilot for structural migration without semantic widening. | `contract` | `ready` | `RG-02` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `Pilot release application rule.` |
| `R04` | `Decision / Outcome` second bullet | `contract-candidate` | New support-only ledgers should split `face extraction`, `chronology sharpening`, and `contract writeback` into separate bounded surfaces rather than overloading one ledger. | `contract` | `ready` | `RG-02` | `docs/governance/contracts/support-only/_template-contract-face-extraction-ledger.md; docs/governance/contracts/support-only/_template-semantic-chronology-sharpening-ledger.md; docs/governance/contracts/support-only/_template-contract-writeback-ledger.md` | `Ledger-role split rule.` |
| `R05` | `Decision / Outcome` second bullet | `runbook-candidate` | Operator fallback, switch, shadow or dual-run, and coexistence procedure should remain outside current positive contract faces unless later packets defend them explicitly. | `runbook` | `ready` | `RG-03` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `Anti-fabrication guard for the pilot.` |

### Shared Reason Groups (optional, recommended when multiple rows share one rationale)

| reason group | applies to packet ids | reason summary | source refs | notes |
| --- | --- | --- | --- | --- |
| `RG-01` | `R01; R02` | The repo needs one explicit contract model where current semantics, evidence, chronology, and release gating stop sharing one mixed surface. | `docs/logs/draft/draft-001.md; docs/governance/contracts/_template-contract-record.md` | `Primary model rationale.` |
| `RG-02` | `R03; R04` | The pilot should land as a full chain: sample contract plus matching ledger templates, not as one isolated contract rewrite. | `DOC-RUNTIME-OBSERVABILITY-0001; support-only templates` | `Keeps the packet from becoming a one-off rewrite.` |
| `RG-03` | `R05` | The structural migration must not smuggle operator procedure into current contract ownership just because nearby switches or runbooks exist. | `draft-001; DOC-RUNTIME-OBSERVABILITY-0001` | `Preserves boundary discipline.` |

## PR Summary Inputs (optional)

- This packet is expected to land as one docs-governance contract rewrite lane, so review should focus on the model shift and pilot integrity rather than on incidental wording changes.

**PR summary bullets**:

- Replace the mixed release-first contract structure with a face-oriented current-semantic model and explicit release-decision gate.
- Pilot the new model on `DOC-RUNTIME-OBSERVABILITY-0001` without widening current owned semantics.
- Add matching ledger templates and source-log template sections so future packets can follow the same chain.

**PR checklist source**:

- Default source: reuse this log's execution checklist.

**PR links**:

- Log: `docs/logs/log-S0G-5B-code-oriented-contract-faces-and-release-decision-governance.md`
- Runbook: ``
- Evidence artifact: ``

**Evidence Footer Source**:

- `P1-C1-S1` | artifact: `docs/governance/contracts/_template-contract-record.md`
- `P1-C1-S2` | artifact: `docs/logs/_template-log-phase-drills-evidence.md`
- `P1-C1-S3` | artifact: `docs/governance/contracts/support-only/_template-contract-face-extraction-ledger.md`
- `P2-C1-S1` | artifact: `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`

## Exported Sections / Outlet Ownership

- This packet intentionally exports to `contract` and retains its packet-local rationale here; no new `view` or `index/front-door` surface is required yet.

**Outlet ownership**:

- `contract`: rewrite the primary contract template and the `OBSERVABILITY-0001` pilot around face/evidence/chronology/release-decision structure
- `runbook`: keep operator fallback or switch semantics routed out of current positive contract ownership
- `view`: no-op for now
- `index/front-door`: no-op for now
- `disposition/placement`: no-op for now
- `log-retained core`: packet rationale, release gate wording, execution chain, and evidence summary remain here

## Definitions (optional)

- `Current Contract Faces`: the current effective semantic snapshot of a contract, organized by stable face names rather than mixed release-first clauses.
- `Code Evidence Attachments`: a fact table that records code-near anchors without turning those facts into contract meaning automatically.
- `Semantic Chronology`: the append-only time-ordered history of how a face became what it is now.
- `Release Decision Table`: the explicit gate that classifies candidate change as `same-release evidence writeback`, `new release`, `split family`, or another downstream action.
- `face-level semantic delta`: a reader-visible change to the current meaning of one owned contract face.

## Constraints

- Do not widen the positive semantics of `DOC-RUNTIME-OBSERVABILITY-0001` while doing the pilot structure migration.
- Do not treat code-adjacent switches or retained operator runbooks as proof that fallback procedure is already contract-owned.
- Do not hide `new-release-required` cases inside same-release wording cleanup.
- Do not create one monolithic ledger that mixes face extraction, chronology insertion, and final writeback approval again.

## Semantic Delta Structure (optional, recommended when a source log may change current contract meaning)

| delta id | face id or candidate face | current semantic | candidate semantic | delta class | reader visible change | primary evidence refs | downstream owner | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SD-01` | `contract-template-model` | `current contract guidance is clause-first with optional bridge/coverage tables` | `current contract guidance becomes face-first with separate code evidence, chronology, and release decision surfaces` | `boundary-restructure` | `yes` | `docs/governance/contracts/_template-contract-record.md; docs/logs/draft/draft-001.md` | `contract` | `Primary template-level structure migration.` |
| `SD-02` | `DOC-RUNTIME-OBSERVABILITY-0001` | `mixed statement/bridge/coverage current reader` | `face-oriented current reader with unchanged positive semantic boundary` | `clarification-only` | `no` | `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md` | `contract` | `Pilot should reorganize, not widen.` |
| `SD-03` | `source-log-template` | `source logs can classify extractable rules but do not yet expose semantic delta or release gate tables` | `source logs can stage semantic delta and release decision explicitly before downstream mutation` | `evidence-only` | `no` | `docs/logs/_template-log-phase-drills-evidence.md` | `contract` | `Template support writeback only.` |

## Release Decision Table (optional, recommended when a source log may drive same-release writeback versus new release)

| face id | current release semantic | candidate semantic | delta class | reader visible change | contract action | target release or outlet | decision basis | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DOC-RUNTIME-OBSERVABILITY-0001 pilot` | `Current runtime observability meaning is narrow but mixed across statement, bridge, and coverage tables.` | `Keep the same narrow meaning while moving it into current faces, code evidence, chronology, and release-decision sections.` | `clarification-only` | `no` | `same-release-evidence-writeback` | `DOC-RUNTIME-OBSERVABILITY-0001` | `Pilot is structure migration only.` | `No 0002 release should be opened for formatting alone.` |
| `owner-boundary` | `Search outbox projection worker is the current bounded owner surface.` | `If a later packet moves current ownership to another runtime chain, change current face text.` | `semantic-change` | `yes` | `new-release-required` | `DOC-RUNTIME-OBSERVABILITY-0002` | `Owner boundary is reader-visible current meaning.` | `Face-level delta should drive the next release.` |
| `control-fallback-boundary` | `Fallback and switch procedure are not owned by the current contract.` | `If a later packet wants current positive procedure semantics here, it must defend a new owner surface first.` | `boundary-restructure` | `yes` | `move-to-runbook` | `runbook or later gap packet` | `Operator procedure remains outside current contract by default.` | `Anti-fabrication gate.` |

## Optional Required Processing Chain

| chain step | required state | primary owner surface | trigger question | completion evidence | notes |
| --- | --- | --- | --- | --- | --- |
| `source extraction` | `already-satisfied` | `S0G-5B` source log | `Has the packet named the structural contract change tightly enough to route?` | `R01-R05 plus semantic delta and release decision tables` | `Packet boundary is explicit.` |
| `SUP` | `not-required` | `n/a` | `Is this later evidence against one accepted source-owned row?` | `explicit no-SUP verdict` | `This lane is direct template and pilot writeback, not supplement sharpening.` |
| `parent ledger` | `not-required` | `n/a` | `Does this packet change one source-owned routing verdict?` | `explicit no-parent-ledger verdict` | `The packet writes templates and a contract pilot directly.` |
| `contract impact decision` | `required` | `S0G-5B` | `Is the packet only a structure migration, or does it widen current contract meaning?` | `explicit classified verdict` | `Main gate for the lane.` |
| `contract mutation` | `required` | `contract template and OBSERVABILITY-0001` | `Should the current repo templates and pilot contract be rewritten now?` | `template and pilot contract writeback` | `Completed in this packet.` |
| `transition register update` | `not-required` | `n/a` | `Did family-level current-primary standing change?` | `explicit no-register-change verdict` | `0001 remains the current release.` |
| `bridged contract reconciliation` | `conditional` | `adjacent current readers` | `Do family front doors or registers need to point at the new model now?` | `explicit deferred verdict` | `Deferred until a broader rollout exists.` |

## Scope

- `P0`: fix the code-oriented contract model, release gate, and change-structure vocabulary
- `P1`: write the model back into the contract template, source-log template, and three new ledger templates
- `P2`: restructure `DOC-RUNTIME-OBSERVABILITY-0001` as the first pilot without semantic widening
- `P3`: validate the touched files and prepare commit-ready docs-governance output

## Success Criteria (DoD)

- The primary contract template defaults to `Current Contract Faces + Code Evidence Attachments + Semantic Chronology + Release Decision Table`.
- The source-log template can now express semantic delta and release-decision gates explicitly.
- The repo has one reusable template for each of `face extraction`, `chronology sharpening`, and `contract writeback`.
- `DOC-RUNTIME-OBSERVABILITY-0001` reads as a code-oriented pilot contract without widening current owned semantics.
- The packet states clearly when later work should stay same-release evidence writeback and when it must open `OBSERVABILITY-0002`.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the model shift is explicit;
  - the matching template chain exists;
  - the pilot contract is rewritten and validated;
  - the next step is one bounded rollout or release-opening decision rather than another structural debate.

## P0 (Contract | v1)

### P0-C1-S1 (Code-oriented current contract model fixed | v1)

- New code-oriented contracts should separate:
  - `Current Contract Faces`
  - `Code Evidence Attachments`
  - `Semantic Chronology`
  - `Release Decision Table`
- This separation keeps current semantic meaning, code facts, and historical change readable without forcing one mixed release-first table.

### P0-C1-S2 (Release decision rule fixed | v1)

- Release creation should be driven by face-level reader-visible semantic delta.
- Evidence or chronology sharpening without reader-visible semantic change should stay on same-release writeback.

### P0-C1-S3 (Change structure fixed | v1)

- The packet uses four delta classes:
  - `evidence-only`
  - `clarification-only`
  - `semantic-change`
  - `boundary-restructure`
- These classes determine whether the next action is same-release writeback, new release, split-family action, or move-to-runbook.

## Plan (draft)

### P1 (Template writeback)

- `P1-C1-S1`: rewrite the main contract record template around face/evidence/chronology/release-decision structure
- `P1-C1-S2`: add semantic-delta and release-decision sections to the source-log template
- `P1-C1-S3`: add three new support-only ledger templates for face extraction, chronology sharpening, and contract writeback

### P2 (Pilot contract)

- `P2-C1-S1`: restructure `DOC-RUNTIME-OBSERVABILITY-0001` into the new code-oriented pilot shape without widening semantics

### P3 (Validation)

- `P3-C1-S1`: run narrow validation on touched files and keep the packet commit-ready

## Execution Checklist (checked)

### P0 (Contract)

- [x] `P0-C1-S1`: code-oriented current contract model fixed
- [x] `P0-C1-S2`: release decision rule fixed
- [x] `P0-C1-S3`: change structure fixed

### P1 (Template writeback)

- [x] `P1-C1-S1`: contract template rewritten around face/evidence/chronology/release-decision structure
- [x] `P1-C1-S2`: source-log template gained semantic-delta and release-decision sections
- [x] `P1-C1-S3`: three new support-only ledger templates added

### P2 (Pilot contract)

- [x] `P2-C1-S1`: `DOC-RUNTIME-OBSERVABILITY-0001` restructured as the pilot contract

### P3 (Validation)

- [x] `P3-C1-S1`: narrow validation run on touched files

## Current Status (recommended)

- `S0G-5B` is now the bounded docs-governance packet that establishes the face-oriented contract model and applies it to the first pilot contract.
- The packet keeps `OBSERVABILITY-0001` on release `0001`; this round does not claim `OBSERVABILITY-0002` is justified yet.
- The next follow-up should be one bounded decision on whether adjacent current readers need rollout support such as family registers, front doors, or the next face-delta packet.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the writeback surfaces touched by the packet.

### P1-C1-S1S3 (Template chain writeback | 2026-04-28)

- headSha: `pending-next-commit`
- artifacts:
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/logs/_template-log-phase-drills-evidence.md`
  - `docs/governance/contracts/support-only/_template-contract-face-extraction-ledger.md`
  - `docs/governance/contracts/support-only/_template-semantic-chronology-sharpening-ledger.md`
  - `docs/governance/contracts/support-only/_template-contract-writeback-ledger.md`
- expected:
  - one primary contract template adopts the face-oriented model
  - one source-log template can stage semantic delta and release gates
  - three new support-only ledgers exist for the split writeback chain
- observed:
  - all five template surfaces were written and passed narrow file validation

### P2-C1-S1 (OBSERVABILITY pilot restructure | 2026-04-28)

- headSha: `pending-next-commit`
- artifacts:
  - `docs/governance/contracts/runtime/observability/DOC-RUNTIME-OBSERVABILITY-0001-metrics-tracing-and-structured-logs-diagnostic-chain.md`
- expected:
  - the pilot contract reads through current faces, code evidence, chronology, gaps, and release decision
  - no new positive semantic widening is introduced
- observed:
  - the pilot contract now uses the new structure and passed narrow file validation

## Recent changes (for traceability, optional)

- 2026-04-28: rewrote the contract record template around current faces, code evidence, semantic chronology, and release decision rules.
- 2026-04-28: added three new support-only ledger templates so future packets can split face extraction, chronology sharpening, and contract writeback.
- 2026-04-28: restructured `DOC-RUNTIME-OBSERVABILITY-0001` as the first code-oriented pilot contract without widening current owned semantics.