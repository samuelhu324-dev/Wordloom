# log-S0F-7A (Phase 7A: chronology-first contract rebuild)

---

**id**: `S0F-7A`
**kind**: `log`
**title**: `chronology-first contract rebuild v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contracts, History, Lineage, Reader, epic/s0, sub/7a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-5J-old-s0-contract-judgment-front-door-view.md`
  **reference_log_1**: `docs/logs/log-S0F-5H-old-s0-narrative-history-view-pilot.md`
  **reference_log_2**: `docs/logs/log-S0F-5I-old-s0-narrative-history-widening-across-counted-series.md`
  **reference_log_3**: `docs/logs/log-S0F-5J-old-s0-contract-judgment-front-door-view.md`
  **reference_log_4**: `docs/governance/contracts/_template-contract-record.md`
  **reference_log_5**: `docs/governance/legacy/contract/INDEX.md`
  **reference_log_6**: `docs/governance/legacy/contracts/_template-contract-record.md`
**issue_keyword**: `migration`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/7`
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
**created**: `2026-04-10`
**updated**: `2026-04-10`

---

## Decision / Outcome

**Decision**:

- `S0F-7A` opens as the bounded reset lane for chronology-first governance-contract rebuild.
- This lane exists because the repo now has stronger history and judgment views than contract-chain readability, which means the current contract surfaces are no longer the clearest explanation of how the system evolved.
- The immediate correction is to rebuild contracts from the earliest defended decision line forward rather than continuing to derive contracts from the latest `S0F` state backward.

**Default choices (phase defaults / v1)**:

- Treat chronology-first contract rebuild as a new canonical track.
- Treat the moved `docs/governance/legacy/contract/` and `docs/governance/legacy/contracts/` trees as retained legacy reference sets, not as the canonical chain to keep extending.
- Use `docs/governance/contracts/` as the new canonical root for rebuilt chronology-first contract records.
- Reuse the existing contract template only as a starting point; the lane may refine the record model if chronology-first lineage requires stronger structured verbs such as `split into` or `absorbed into` beyond one-to-one supersession.
- Keep `view` surfaces as reader projections and evidence-compression layers, not as replacements for the rebuilt contract chain.

## Problem Statement

- The repo currently explains history more clearly through `view` surfaces than through the existing contract folders.
- That imbalance happened because current-state and late-stage `S0F` concentration work produced readable current contracts before the earlier decisive history was rebuilt as the same kind of object.
- As a result:
  - early foundational decisions such as `S0A` and `S0B` read as key history but not as first-class contracts
  - later `DOC` and `GC` contract bodies appear without a full chronology-first ancestor chain
  - lineage verbs such as `superseded`, `split into`, `absorbed into`, and `retired` cannot carry the full explanatory burden because the chain starts too late
- If later contract work continues on top of that current-first base, the repo will keep strengthening projections while the canonical contract spine remains incomplete.

## Exported Sections / Outlet Ownership

- This slice starts as a `contract`-first rebuild lane with light `index/front-door` support.
- The default expected landing is in `docs/governance/contracts/` plus minimal front-door notes that explain canonical versus legacy roots.

**Outlet ownership**:

- `contract`: expected landing surface for chronology-first rebuilt records and lineage rules
- `runbook`: no-op by default; this lane rebuilds governance history and contract lineage, not operator steps
- `view`: no-op by default on scaffold; existing views remain useful projections but are not the first artifact to expand here
- `index/front-door`: expected minimal landing for canonical root explanation under the new contracts directory
- `disposition/placement`: possible later write-back only when legacy/current folders need explicit standing notes after the new chain stabilizes
- `log-retained core`: keep this source log for reset boundary, rebuild order, lineage rules, and evidence ledger

## Constraints

- Do not resume extending the old current-first `DOC` or `GC` contract sets as if they were still canonical.
- Do not delete legacy contract material without a readable standing note and rebuild plan.
- Do not let rebuilt chronology-first contracts collapse back into narrative-only prose.
- Do not assume every old log becomes a contract; some rows remain evidence, lineage, or projection-only support.
- Do not derive rebuilt chronology from the latest folder state alone; defend it from source-log order and explicit decision lineage.

## Scope

- `P0`: open `S0F-7A`, fix the reset boundary, and mark canonical versus legacy contract roots
- `P1`: define the chronology-first contract record model and lineage verbs
- `P2`: define the first rebuild packet and expected order, starting from `S0A + S0B`
- `P3`: publish the first foundational chronology-first contracts
- `P4`: decide how existing late-stage current-first contracts should be rewritten, absorbed, or retired after the rebuilt chain exists

## Success Criteria (DoD)

- The repo has one explicit canonical root for chronology-first contract rebuild.
- Readers can distinguish canonical rebuilt contracts from legacy current-first experiments.
- The next execution step is fixed as foundational contract generation from early history rather than further patching of late-stage current-first contracts.

## P0 (Reset Boundary | v1)

### P0-C1-S1 (Canonical versus legacy contract roots fixed | v1)

- `docs/governance/contracts/` is now the canonical root for chronology-first rebuilt contracts.
- `docs/governance/legacy/contract/` and `docs/governance/legacy/contracts/` are now treated as retained pre-reset reference sets.
- Under this rule, later rebuild work should write new canonical records to the new root instead of reviving the moved legacy trees.

### P0-C1-S2 (Immediate rebuild sequence fixed | v1)

- The immediate next work after scaffold is now fixed as:
  - first define the chronology-first contract record model and lineage verbs
  - then choose the first foundational rebuild packet
  - then generate early contracts from `S0A + S0B` forward
- Under this rule, the lane must not reopen `view`-first routing as the main artifact before the contract chain exists.

## Plan (draft)

### P1 (Chronology-first contract model)

- `P1-C1-S1`: define what qualifies as a chronology-first contract versus evidence-only history
- `P1-C1-S2`: define the lineage verbs and structured fields needed for split, absorbed, superseded, and retired cases

### P1-C1-S1 (Contract versus evidence rule fixed | v1)

- A row now qualifies as one chronology-first contract only when it does at least one of these jobs as its primary historical result:
  - introduces one new governance rule, boundary, or decision that later surfaces depend on
  - materially changes the effective meaning of an existing contract-worthy rule
  - stabilizes one previously ambiguous governance boundary strongly enough that later history should read it as a named contract state rather than as loose supporting prose
- A row should stay as `evidence-only history` when it mainly does one of these jobs:
  - demonstrates, validates, or audits a rule that already exists elsewhere
  - implements or packages a previously defined rule without becoming the clearest source of meaning for that rule
  - records migration mechanics, support-only wrappers, transport shells, or retained chronology whose value is traceability rather than rule ownership
- A row should stay as `lineage-support history` rather than one standalone contract when it mainly explains how one contract state led to another but does not itself carry the clearest effective rule meaning.
- Under this rule, chronology-first contracts are not limited to current-state rules: early foundational decisions such as `S0A` / `S0B` may qualify even when they are no longer the latest effective state.

### P1-C1-S2 (Lineage verbs and structured fields fixed | v1)

- The chronology-first rebuild now uses these lineage verbs with distinct meaning:
  - `supersedes` / `superseded_by`: one-to-one replacement where one later contract fully replaces one earlier contract as the clearer effective rule state
  - `split_from` / `split_into`: one-to-many or many-to-one decomposition where one earlier rule body is broken into narrower successor contracts
  - `absorbed_from` / `absorbed_into`: meaning carried forward into another contract without a pure one-to-one replacement, usually because one later contract absorbs part of an earlier contract's rule content
  - `retires` / `retired_by`: explicit end-of-life transition where a contract stops being effective without being cleanly replaced by one single current rule body
- The contract template must therefore carry lineage as a structured block rather than overloading `superseded_by` to express every relationship.
- The contract template also now distinguishes:
  - `source_refs`: the smallest decisive sources that justify the contract state itself
  - `supporting_evidence_refs`: additional retained evidence that helps readers verify chronology without turning every evidence row into a contract

### P2 (First rebuild packet)

- `P2-C1-S1`: fix the first foundational packet as `S0A + S0B`
- `P2-C1-S2`: define the follow-on rebuild order from `S0C -> S0D -> S0E -> S0F`

### P2-C1-S1 (First foundational packet fixed as `S0A + S0B` | v1)

- The first chronology-first rebuild packet is now fixed as `S0A + S0B`.
- This first packet is defended because it contains the earliest still-defensible decision line that later old-`S0` history depends on:
  - `S0A` carries the pre-counted platform pressure around replay, failure handling, and shared operator semantics
  - the `S0B` parent ADR turns that pressure into one defended governance decision package
  - `S0B-2A` and `S0B-3A` then act as the earliest counted execution-level children of that decision package
- Under chronology-first rebuild, this packet must land first because later `S0C` / `S0D` / `S0E` / `S0F` work all assume the taxonomy, metadata, cutover, and operator-structure baseline that begins here.
- The packet also keeps the explicit `S0B-1A` unresolved gap visible so the rebuilt chain does not fake full foundational completeness where local evidence is still missing.

### P2-C1-S2 (Follow-on rebuild order fixed as `S0C -> S0D -> S0E -> S0F` | v1)

- The follow-on chronology-first rebuild order is now fixed as `S0C -> S0D -> S0E -> S0F`.
- This order is defended as the cleanest chronology-first build sequence after the foundational `S0A + S0B` packet:
  - `S0C` should follow first because it stabilizes log grammar, CLI decomposition, scenario taxonomy, and commit-description discipline directly on top of the earlier docs-management and metadata baseline
  - `S0D` should follow next because it packages the repo's supporting governance containers around logs, evidence, runbooks, UI evidence-lite, workflow packing, and roadmap/demo organization on top of the structure that `S0C` and earlier work already made legible
  - `S0E` should follow third because it is the first large mixed automation and lifecycle series, and many of its rows refine or operationalize the earlier structure into issue, PR, lifecycle, and workflow semantics
  - `S0F` stays last because it is both the latest chronology and the current densest mixed series, with several rows already reading as late-stage concentration while other rows remain unresolved
- Under this rule, rebuild order is no longer driven by the earlier narrative-widening convenience order; it is now driven by chronology-first dependence and the need to establish the earliest contract spine before later concentration and replacement states are evaluated.

### P3 (First foundational contracts)

- `P3-C1-S1`: publish the first chronology-first foundational contracts from `S0A + S0B`
- `P3-C1-S2`: link those contracts to the retained legacy/reference surfaces without re-promoting the legacy trees to canonical status

## Execution Checklist (unchecked)

### P0 (Reset Boundary)

- [x] `P0-C1-S1`: canonical versus legacy roots fixed
- [x] `P0-C1-S2`: immediate rebuild sequence fixed

### P1 (Chronology-first contract model)

- [x] `P1-C1-S1`: contract versus evidence rule fixed
- [x] `P1-C1-S2`: lineage verbs and structured fields fixed

### P2 (First rebuild packet)

- [x] `P2-C1-S1`: first foundational packet fixed
- [x] `P2-C1-S2`: follow-on rebuild order fixed

### P3 (First foundational contracts)

- [ ] `P3-C1-S1`: first foundational contracts published
- [ ] `P3-C1-S2`: legacy/reference linkage fixed

## Current Status

- `S0F-7A` is now opened as the chronology-first contract rebuild reset lane.
- `P0` is now complete: canonical versus legacy contract roots are explicit, and the immediate next step is to define the chronology-first record model before any foundational contracts are generated.
- `P1` is now complete: the repo now has one explicit contract-versus-evidence rule and one structured lineage-verb model for chronology-first rebuild.
- `P2` is now complete: the first foundational rebuild packet is fixed as `S0A + S0B`, and the follow-on chronology-first rebuild order is fixed as `S0C -> S0D -> S0E -> S0F`.
- The immediate next step is `P3`: publish the first foundational chronology-first contracts from `S0A + S0B` under the new canonical template and lineage model.

## Evidence (reserved)

### P0-C1-S1S2 (Chronology-first rebuild lane scaffold landed | 2026-04-10)

- headSha: `2b8cfe235`
- artifacts:
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should gain one explicit reset lane for chronology-first contract rebuild
  - canonical versus legacy contract roots should become explicit before the rebuild model is defined
- observed:
  - the repo now has one dedicated reset lane for chronology-first contract rebuild
  - the new contracts root is now explicitly positioned as canonical while the moved legacy trees remain retained reference sets

### P1-C1-S1S2 (Chronology-first contract model and lineage verbs fixed | 2026-04-10)

- headSha: `2b8cfe235`
- artifacts:
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should gain one explicit rule for what qualifies as a chronology-first contract versus evidence-only history
  - the template should gain structured lineage fields that can represent split and absorbed cases without overloading one-to-one supersession
- observed:
  - chronology-first contracts are now defined as rule-owning or boundary-owning states, while validation, migration, wrapper, and transport rows stay as evidence-only or lineage-support history
  - the canonical template now distinguishes decisive source refs from supporting evidence and carries separate lineage fields for supersede, split, absorb, and retire relationships

### P2-C1-S1S2 (Foundational rebuild packet and chronology-first order fixed | 2026-04-10)

- headSha: `60359741c`
- artifacts:
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should fix the first foundational chronology-first packet before generating rebuilt contracts
  - the rebuild order after that packet should follow defended chronology and dependency rather than the earlier packet-reading convenience order
- observed:
  - the first foundational packet is now fixed as `S0A + S0B`, because it carries the earliest still-defensible decision line that later old-`S0` work depends on
  - the follow-on chronology-first rebuild order is now fixed as `S0C -> S0D -> S0E -> S0F`, so later contract generation can proceed from early structure into later automation and concentration states

## Recent changes (for traceability, optional)

- 2026-04-10: opened `S0F-7A` as the reset lane for chronology-first contract rebuild.
- 2026-04-10: fixed the canonical versus legacy contract roots and the immediate rebuild sequence before any new foundational contracts are generated.
- 2026-04-10: completed `P1` by fixing the chronology-first contract-versus-evidence rule and by defining the lineage verbs plus structured template fields needed for supersede, split, absorb, and retire cases.
- 2026-04-10: completed `P2` by fixing the first foundational rebuild packet as `S0A + S0B` and by fixing the follow-on chronology-first rebuild order as `S0C -> S0D -> S0E -> S0F`.