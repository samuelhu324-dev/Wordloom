# log-S0F-4H (Phase 4H: active GC current registry family mapping and re-homing)

---

**id**: `S0F-4H`
**kind**: `log`
**title**: `active GC current registry family mapping and re-homing v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Taxonomy, Family, Mapping, Rehoming, epic/s0, sub/4h`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
  **reference_log_1**: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
  **reference_log_2**: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
  **reference_log_3**: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
  **reference_log_4**: `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
  **reference_log_5**: `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
  **reference_log_6**: `docs/governance/INDEX.md`
  **reference_log_7**: `docs/governance/contract/INDEX.md`
  **reference_log_8**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_9**: `docs/governance/views/view-ops-current-front-door-v1.md`
  **reference_log_10**: `docs/governance/contract/DOC-TAX-0001-governance-contract-taxonomy-and-placement-model.md`
  **reference_log_11**: `docs/governance/contracts/GC-ICR-0001-issue-creation-metadata-english-body.md`
  **reference_log_12**: `docs/governance/contracts/GC-ICL-0001-issue-conclusion-post-merge-linkage.md`
  **reference_log_13**: `docs/governance/contracts/GC-ICT-0001-issue-context-sentence-count-main-vs-child.md`
  **reference_log_14**: `docs/governance/contracts/GC-IID-0001-parent-sidebar-ordering-ownership.md`
  **reference_log_15**: `docs/governance/contracts/GC-IID-0002-issue-title-keyword-controlled-vocabulary.md`
**issue_keyword**: `taxonomy`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/4`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M5`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-09`
**updated**: `2026-04-10`

---

## Decision / Outcome

**Decision**:

- `S0F-4H` opens the next bounded follow-up after `S0F-3M` because the repo now has a verified legacy-redirect cleanup pilot, but still lacks one explicit current-state answer for a different problem: how should the remaining active `GC-*` narrow-registry contracts be mapped into the seven-family model when their semantics now appear to belong primarily to `DOC` or `OPS` instead of to a long-lived standalone `GC` current family?
- This slice is not another legacy cleanup packet.
- It is the family-mapping and re-homing design lane for active current `GC-*` records.
- v1 is intentionally bounded around the current issue-governance subset first:
  - `GC-ICR-0001`
  - `GC-ICL-0001`
  - `GC-ICT-0001`
  - `GC-IID-0001`
  - `GC-IID-0002`
- The immediate job is to determine whether those active current records should remain as a stable `GC` narrow-registry current surface, be promoted into family-owned `DOC` or `OPS` current contracts, or split further across families under one explicit re-homing rule.

**Default choices (phase defaults / v1)**:

- Treat this slice as a `current owner mapping` problem, not as a `legacy redirect cleanup` problem.
- Reuse the seven-family taxonomy and SoT-first placement rule from `DOC-TAX-0001` rather than inventing a second taxonomy.
- Do not assume in advance that every active `GC-*` record must become `DOC`; some may remain better aligned to `OPS` or another family once current primary SoT is judged explicitly.
- Do not move or rename any active current contract body during scaffold.
- Keep `GC` legacy cleanup and `active GC current re-homing` as separate lanes so evidence from one does not blur the owner decision in the other.

## PR Summary Inputs (optional)

- Use this block because `S0F-4H` is expected to define the next family-owned current contract mapping lane after the first `DOC` promotion quartet and the first verified legacy `GC` cleanup pilot.

**PR summary bullets**:

- Open the family-mapping lane for active current `GC-*` registry contracts that now appear to belong under `DOC` or `OPS` in the seven-family model.
- Separate current contract re-homing from old `GC` redirect cleanup so the repo stops overloading one lane with both problems.
- Fix the next decision boundary around whether the active issue-governance `GC-*` subset should stay current in place, promote into `DOC` or `OPS`, or split across families under one explicit mapping rule.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the current-registry family-mapping lane.

**PR links**:

- Log: `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
- DOC front door: `docs/governance/views/view-doc-current-front-door-v1.md`
- OPS front door: `docs/governance/views/view-ops-current-front-door-v1.md`

## Exported Sections / Outlet Ownership

- This slice may end in one new family-owned current contract packet, one mapping view, or one defended no-op if the current `GC` narrow-registry subset still needs to stay where it is.

**Outlet ownership**:

- `contract`: only if this slice stabilizes one new family-owned current contract or one explicit supersede/re-home rule for the active `GC-*` subset
- `runbook`: no runbook by default; this is a taxonomy and current-owner lane first
- `view`: likely, if the repo needs one compact current-family mapping surface from active `GC-*` rows into `DOC` or `OPS`
- `index/front-door`: only the front-door or index mutations needed if current reading really moves out of `docs/governance/INDEX.md`
- `disposition/placement`: actual keep-current, promote, supersede, or split decisions for the active current `GC-*` subset
- `log-retained core`: mapping rationale, evidence, stop reasons, and the bounded next execution packet if one is justified

## Definitions (optional)

- **active GC current registry**: the still-current `GC-*` records admitted by `docs/governance/INDEX.md` rather than preserved only for legacy redirect or support-only history
- **family re-homing**: moving current reader-facing ownership for a rule set from the narrow `GC` registry model into one of the seven family-owned current surfaces such as `DOC` or `OPS`
- **mapping packet**: one bounded set of current records judged together for keep, promote, split, or no-op outcome under the same family-mapping question

## Constraints

- Do not treat the verified `S0F-3M` cleanup pilot as proof that active current `GC-*` contracts should relocate mechanically.
- Do not assume `DOC` is the target family for every active current `GC-*` record before current primary SoT is judged.
- Do not degrade current-reader clarity in `docs/governance/INDEX.md` before a replacement current family front door is explicit.
- Do not reopen the already-verified `GC-ISS-0001` legacy cleanup pilot in this slice.
- Keep active current contract re-homing separate from old `GC` redirect support-only handling.

## Scope

- `P0`: open `S0F-4H` as the bounded family-mapping lane for active current `GC-*` records
- `P1`: inventory the active current `GC-*` subset and classify likely target families under the seven-family model
- `P2`: define the keep-versus-promote-versus-split decision rule for that subset
- `P3`: test one bounded current re-homing packet for the issue-governance current set and record stop reasons if the subset should split further
- `P4`: decide whether to execute a real current-family promotion packet next or keep the active `GC` narrow-registry subset in place for now

## Success Criteria (DoD)

- One reader can explain whether the active issue-governance `GC-*` current set still belongs in the narrow `GC` registry or should re-home into `DOC` or `OPS`.
- One reader can explain why current-family re-homing is a different question from old `GC` redirect cleanup.
- The repo has one explicit answer for whether the active current subset should stay, promote, split, or stop.
- Later work no longer needs to improvise the boundary between `GC current registry`, `DOC current family`, and `OPS current family` for the same issue-governance rules.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the active current `GC-*` subset and candidate family targets are explicit
  - one keep-versus-promote-versus-split rule is explicit enough to defend
  - the next step is clear as `execute`, `hold`, or `stop`

## P0 (Contract | v1)

### P0-C1-S1 (Problem boundary fixed | v1)

- `S0F-4H` is now opened as the active current `GC-*` family-mapping follow-up.
- This slice does not ask whether old redirect files can move to support-only.
- It asks whether the still-current `GC-*` registry subset should remain current in place or re-home into family-owned current surfaces.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now:
  - inventory the active current `GC-*` subset under the seven-family taxonomy
  - define the current-owner mapping rule for keep, promote, or split
  - decide whether one bounded execution packet is justified next
- This keeps current-owner reasoning ahead of any rename or promotion attempt.

## Plan (draft)

### P1 (Active current mapping inventory)

- P1-C1-S1: inventory the active current `GC-*` subset that still reads as current under `docs/governance/INDEX.md`
- P1-C1-S2: classify likely target family ownership for each record or subcluster

### P1-C1-S1 (Active issue-governance current subset inventoried | v1)

- The first bounded `S0F-4H` subset is now fixed as the five active issue-governance current-registry records:
  - `GC-ICR-0001`
  - `GC-ICL-0001`
  - `GC-ICT-0001`
  - `GC-IID-0001`
  - `GC-IID-0002`
- All five still read as current registry rows under the narrow `GC` surface rather than as legacy redirect or support-only history.
- The shared semantic cluster is now explicit: these records govern issue creation, issue conclusion, issue context/body rendering, issue sidebar identity, and issue-title vocabulary for source-log-owned docs/GitHub lifecycle work.

### P1-C1-S2 (Likely target-family mapping fixed | v1)

- The first-pass likely target-family result is now `DOC` for the full bounded issue-governance subset.
- Why `DOC` currently fits better than `OPS`:
  - the current `DOC` front door is defined as the family-first reader surface for doc-first control-plane contracts
  - the current `OPS` front door is defined around deploy, verify, rollback, release operations, runtime operating model, and operator-path semantics
  - the five active issue-governance records govern document shape, lifecycle writeback, naming, and reader-facing issue identity rather than runtime operator execution
- This is still an inventory and mapping result only.
- `P1` does not yet decide whether these records should actually promote out of the narrow `GC` registry as one packet, stay in place temporarily, or split further before any re-homing write.

### P2 (Re-homing rule)

- P2-C1-S1: define when an active current `GC-*` record should stay current in place versus promote into a family-owned current surface
- P2-C1-S2: define stop reasons if one mixed subset cannot move as one packet

### P3 (Applicability test)

- P3-C1-S1: test whether the issue-governance current set can re-home as one bounded packet or must split further
- P3-C1-S2: record the explicit split or defer reasons if one shared packet is not yet safe

### P4 (Next-lane decision)

- P4-C1-S1: choose among real promotion packet, narrower pilot, or defended no-op

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: problem boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (Active current mapping inventory)

- [x] `P1-C1-S1`: active current subset inventoried
- [x] `P1-C1-S2`: likely target-family mapping fixed

### P2 (Re-homing rule)

- [ ] `P2-C1-S1`: keep-versus-promote rule fixed
- [ ] `P2-C1-S2`: stop reasons or split rule fixed if needed

### P3 (Applicability test)

- [ ] `P3-C1-S1`: bounded execution packet applicability tested
- [ ] `P3-C1-S2`: split or defer reasons fixed if needed

### P4 (Next-lane decision)

- [ ] `P4-C1-S1`: next execution boundary decided

## Current Status (recommended)

- `S0F-4H` is now opened as the bounded follow-up for the active current `GC-*` family-mapping question.
- The repo now has one explicit source log for deciding whether the current issue-governance `GC-*` subset should stay in the narrow registry or re-home into `DOC` or `OPS` family-owned current surfaces.
- `P0` is now complete: the slice boundary and sequencing are fixed.
- `P1` is now complete: the active issue-governance subset is explicit and the first-pass likely target-family result is `DOC`, not `OPS`.
- The immediate next step is `P2`: define the keep-versus-promote-versus-split rule before any real re-homing packet is attempted.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this section will hold the active-current inventory, mapping rationale, and any later promotion-packet decision for the re-homing lane.
- This scaffold records the opening event and bounded next-step contract for `S0F-4H`.

### P0-C1-S1S2 (Active current `GC-*` family-mapping lane opened | 2026-04-09)

- headSha: `<pending commit for S0F-4H/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/governance/INDEX.md`
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-ops-current-front-door-v1.md`
- expected:
  - the repo has one explicit bounded slice for current `GC-*` family re-homing after the verified legacy cleanup pilot
  - later work no longer needs to overload legacy-cleanup slices with current-family mapping questions
- observed:
  - `S0F-4H` is now opened with a current-owner mapping boundary, fixed P1-P4 sequence, and explicit non-goal of reopening the verified legacy `GC-ISS-0001` cleanup pilot

### P1-C1-S1S2 (Active issue-governance current subset inventoried and first-pass family mapping fixed | 2026-04-10)

- headSha: `<pending commit for S0F-4H/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/support-only/s0f-4h-active-gc-issue-governance-family-mapping-inventory.json`
  - `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-ops-current-front-door-v1.md`
  - `docs/governance/views/support-only/view-s0f-1-family-sweep-v1.md`
  - `docs/governance/views/support-only/view-issue-automation-follow-up-family-sweep-v1.md`
- expected:
  - the active issue-governance `GC-*` subset is explicit enough to judge as one bounded mapping packet
  - the repo has one first-pass answer for whether this subset looks more like `DOC` or `OPS`
- observed:
  - the bounded subset is fixed as `GC-ICR-0001`, `GC-ICL-0001`, `GC-ICT-0001`, `GC-IID-0001`, and `GC-IID-0002`
  - the first-pass likely target-family result is `DOC` across the full subset because the governing semantics are docs/GitHub lifecycle shape, writeback, naming, and identity rather than release/runtime operations
  - `P1` stops short of deciding whether the full subset should promote together or split under a later execution rule

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-4H` as the bounded active current `GC-*` family-mapping and re-homing lane after `S0F-3M` stabilized the first verified legacy cleanup pilot.
- 2026-04-10: completed `P1` by fixing the active issue-governance subset inventory and recording a first-pass `DOC` ownership mapping hypothesis for all five current records.