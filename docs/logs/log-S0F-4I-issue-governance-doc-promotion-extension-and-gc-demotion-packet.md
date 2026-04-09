# log-S0F-4I (Phase 4I: issue-governance DOC promotion extension and GC demotion packet)

---

**id**: `S0F-4I`
**kind**: `log`
**title**: `issue-governance DOC promotion extension and GC demotion packet v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Promotion, Demotion, Family, Packet, epic/s0, sub/4i`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
  **reference_log_1**: `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
  **reference_log_2**: `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`
  **reference_log_3**: `docs/logs/log-S0F-4F-doc-reader-surface-consolidation-after-first-promotion-quartet.md`
  **reference_log_4**: `docs/logs/log-S0F-4D-doc-current-contract-surface-and-legacy-gc-triage-model.md`
  **reference_log_5**: `docs/logs/log-S0F-4C-doc-and-ops-front-door-transition-and-gc-demotion-model.md`
  **reference_log_6**: `docs/governance/INDEX.md`
  **reference_log_7**: `docs/governance/contract/INDEX.md`
  **reference_log_8**: `docs/governance/views/view-doc-current-front-door-v1.md`
  **reference_log_9**: `docs/governance/views/view-doc-contract-promotion-map-v1.md`
  **reference_log_10**: `docs/governance/contract/DOC-FDT-0001-family-front-door-transition-and-gc-demotion-model.md`
  **reference_log_11**: `docs/governance/contracts/GC-ICR-0001-issue-creation-metadata-english-body.md`
  **reference_log_12**: `docs/governance/contracts/GC-ICL-0001-issue-conclusion-post-merge-linkage.md`
  **reference_log_13**: `docs/governance/contracts/GC-ICT-0001-issue-context-sentence-count-main-vs-child.md`
  **reference_log_14**: `docs/governance/contracts/GC-IID-0001-parent-sidebar-ordering-ownership.md`
  **reference_log_15**: `docs/governance/contracts/GC-IID-0002-issue-title-keyword-controlled-vocabulary.md`
**issue_keyword**: `contract`
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
**updated**: `2026-04-09`

---

## Decision / Outcome

**Decision**:

- `S0F-4I` opens as the direct execution follow-up after `S0F-4H` stabilized the mapping answer for the active issue-governance `GC-*` subset.
- This slice is not another mapping lane.
- It is the real `DOC` promotion-extension and matching `GC` demotion packet lane for the bounded issue-governance current set:
  - `GC-ICR-0001`
  - `GC-ICL-0001`
  - `GC-ICT-0001`
  - `GC-IID-0001`
  - `GC-IID-0002`
- The bounded execution target is already fixed by `S0F-4H`:
  - one `DOC`-target promotion packet
  - four landing units inside that packet: issue creation, issue conclusion, issue context, and issue identity
  - matching `GC` demotion and current-reader transition writes only after the replacement `DOC` reading surface is explicit

**Default choices (phase defaults / v1)**:

- Reuse `S0F-4H` as the execution boundary contract rather than reopening family mapping.
- Reuse the existing `DOC` landing model under `docs/governance/contract/` rather than improvising a new home.
- Do not collapse the four-unit packet into one omnibus replacement contract.
- Keep `GC-IID-0001` and `GC-IID-0002` together as one shared issue-identity landing unit unless later execution evidence forces a narrower split.
- Do not demote or rewrite current `GC-*` reader surfaces before the replacement `DOC` packet is explicit enough to carry current reading safely.

## PR Summary Inputs (optional)

- Use this block because `S0F-4I` is expected to drive the first real issue-governance `DOC` promotion-extension packet once the new family-owned bodies and demotion plan are explicit.

**PR summary bullets**:

- Execute the next `DOC` promotion extension for the active issue-governance current subset proven by `S0F-4H`.
- Land one bounded four-unit `DOC` packet for issue creation, issue conclusion, issue context, and issue identity.
- Pair the new `DOC` packet with explicit `GC` demotion and current-reader transition writes instead of leaving current reading split across ambiguous family surfaces.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the issue-governance `DOC` promotion-extension lane.

**PR links**:

- Log: `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`
- Previous mapping lane: `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
- DOC promotion precedent: `docs/logs/log-S0F-4E-first-doc-promoted-contract-body-from-s0f-4a.md`

## Exported Sections / Outlet Ownership

- This slice is expected to end in real current-surface writes rather than another mapping-only answer.

**Outlet ownership**:

- `contract`: new family-owned `DOC` current bodies for the bounded issue-governance packet
- `view`: only if one compact issue-governance reader surface is needed to keep the packet interpretable after promotion
- `index/front-door`: `docs/governance/contract/INDEX.md`, `docs/governance/views/view-doc-current-front-door-v1.md`, and any required current-reader transition surfaces
- `disposition/placement`: matching `GC` demotion, redirect, or retained-current standing decisions after the replacement `DOC` packet is explicit
- `log-retained core`: execution ledger, evidence, packet-shape notes, and stop reasons if the real promotion packet cannot complete in one bounded pass

## Definitions (optional)

- **promotion extension**: the next admitted `DOC` mapping set after the first stable quartet, executed as real family-owned current contract landings rather than as a mapping-only hypothesis
- **four-unit packet**: the bounded issue-governance execution shape proved by `S0F-4H`, covering issue creation, issue conclusion, issue context, and issue identity
- **matching GC demotion**: the lineage-safe narrowing or redirect treatment applied to the old current `GC-*` rows only after the replacement `DOC` reading surface exists

## Constraints

- Do not reopen the `DOC` versus `OPS` mapping question already closed by `S0F-4H`.
- Do not widen beyond the bounded five-record issue-governance subset in this slice.
- Do not collapse four area-level units into one omnibus `DOC` contract.
- Do not demote current `GC-*` rows before the replacement `DOC` packet and current-reader transition path are explicit.
- Keep the execution lane focused on family-owned contract landing and matched reader transition, not on unrelated historical cleanup.

## Scope

- `P0`: open `S0F-4I`, fix the four-unit execution boundary, and register the lane in the parent spine
- `P1`: admit the next `DOC` mapping extension for the four landing units and fix their target naming boundary
- `P2`: draft the bounded replacement `DOC` packet and align required `contract` or `index/front-door` writes
- `P3`: define and test the matching `GC` demotion and current-reader transition packet for the replaced issue-governance rows
- `P4`: decide whether the full bounded packet is ready for real execution now or needs one narrower follow-up inside the same lane

## Success Criteria (DoD)

- One reader can explain why the active issue-governance current subset now moves through a dedicated `DOC` promotion-extension lane rather than through another mapping slice.
- One reader can explain the bounded packet shape as four landing units rather than one omnibus replacement body.
- The repo has one explicit execution lane for both `DOC` promotion and matching `GC` demotion of the same bounded subset.
- Later work no longer needs to improvise whether the next issue-governance move belongs to family mapping, contract promotion, or current-reader transition.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the four-unit promotion-extension boundary is explicit
  - the matching `GC` demotion and current-reader transition plan is explicit enough to defend
  - the next step is clear as `execute`, `hold`, or `split` within this execution lane

## P0 (Contract | v1)

### P0-C1-S1 (Execution boundary fixed | v1)

- `S0F-4I` is now opened as the dedicated issue-governance `DOC` promotion-extension execution lane.
- This slice does not ask whether the active issue-governance `GC-*` subset belongs to `DOC`.
- It asks how to land the already-proved four-unit `DOC` packet and pair it with matching `GC` demotion and reader-transition writes.

### P0-C1-S2 (Immediate sequencing fixed | v1)

- The immediate next work after scaffold is now:
  - admit the next `DOC` mapping extension for the four issue-governance landing units
  - define their target naming and landing boundaries
  - prepare the matching `GC` demotion and current-reader transition packet
- This keeps real execution work ahead of any opportunistic cleanup or broad family expansion.

## Plan (draft)

### P1 (DOC mapping extension admission)

- P1-C1-S1: admit the next `DOC` mapping extension for issue creation, issue conclusion, issue context, and issue identity
- P1-C1-S2: fix target naming or area-boundary choices for the four-unit packet

### P1-C1-S1 (Next DOC mapping extension admitted | v1)

- The next `DOC` mapping extension is now admitted for the bounded issue-governance packet.
- The admitted landing units are:
  - issue creation
  - issue conclusion
  - issue context
  - issue identity
- This admission result now extends the first `DOC` quartet with one explicit issue-governance packet instead of treating the next promotion step as ad hoc extraction work.

### P1-C1-S2 (Target naming and area boundary fixed | v1)

- The naming boundary is now fixed by reusing the stable governance area codes whose semantics remain the same under family-owned `DOC` reading:
  - `DOC-ICR-0001`
  - `DOC-ICL-0001`
  - `DOC-ICT-0001`
  - `DOC-IID-0001`
  - `DOC-IID-0002`
- Why reuse is correct here:
  - the areas already name stable current governance surfaces rather than temporary implementation details
  - the semantics remain the same while family ownership changes from narrow `GC` registry to family-owned `DOC` current bodies
  - `DOC` contract admission rules already allow reused area codes when the semantics are actually the same
- The packet still stays four-unit at execution level:
  - `ICR`, `ICL`, and `ICT` each map to one target record
  - `IID` remains one shared landing unit, but preserves two target records because sidebar ordering and title-keyword vocabulary remain distinct current rule bodies

### P2 (Replacement DOC packet)

- P2-C1-S1: draft the bounded family-owned `DOC` replacement packet
- P2-C1-S2: align required `DOC` contract index or front-door writes for that packet

### P2-C1-S1 (Bounded DOC replacement packet drafted | v1)

- The bounded replacement `DOC` packet is now landed on disk as five family-owned current contract bodies:
  - `DOC-ICR-0001`
  - `DOC-ICL-0001`
  - `DOC-ICT-0001`
  - `DOC-IID-0001`
  - `DOC-IID-0002`
- The packet keeps the execution shape proved in `S0F-4H`:
  - four landing units at packet level
  - five target records at file level because the shared issue-identity unit still owns two distinct current rule bodies
- `P2` only lands the replacement `DOC` reading surface.
- It does not yet demote, stub, or retarget the old current `GC-*` rows.

### P2-C1-S2 (DOC index and front-door alignment fixed | v1)

- The `DOC` contract index now lists the five new issue-governance family-owned current bodies.
- The `DOC` promotion map now records the issue-governance extension packet as landed rather than merely admitted.
- The `DOC` current front door now exposes the new issue-governance current reading surfaces explicitly.
- Under the family-front-door transition rule, this makes the replacement `DOC` packet readable now while leaving the corresponding `GC-*` rows in place for the later demotion and reader-transition step.

### P3 (GC demotion and transition packet)

- P3-C1-S1: define the matching `GC` demotion or redirect treatment for the replaced current rows
- P3-C1-S2: align current-reader transition writes so `docs/governance/INDEX.md` and family-first reading remain clear together

### P4 (Execution boundary decision)

- P4-C1-S1: decide whether the full bounded packet executes now or needs one narrower execution step first

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: execution boundary fixed
- [x] `P0-C1-S2`: immediate sequencing fixed

### P1 (DOC mapping extension admission)

- [x] `P1-C1-S1`: next DOC mapping extension admitted
- [x] `P1-C1-S2`: target naming or area boundary fixed

### P2 (Replacement DOC packet)

- [x] `P2-C1-S1`: bounded DOC replacement packet drafted
- [x] `P2-C1-S2`: DOC index or front-door alignment fixed

### P3 (GC demotion and transition packet)

- [ ] `P3-C1-S1`: matching GC demotion treatment fixed
- [ ] `P3-C1-S2`: current-reader transition packet fixed

### P4 (Execution boundary decision)

- [ ] `P4-C1-S1`: next execution boundary decided

## Current Status (recommended)

- `S0F-4I` is now opened as the direct execution follow-up after `S0F-4H` stabilized the mapping and packet-shape result for the active issue-governance `GC-*` subset.
- The repo now has one explicit lane for turning that result into real family-owned `DOC` current bodies plus matching `GC` demotion and current-reader transition writes.
- `P0` is now complete: the bounded execution target and immediate sequence are fixed.
- `P1` is now complete: the next `DOC` mapping extension is admitted and the target naming boundary is fixed as `DOC-ICR-0001`, `DOC-ICL-0001`, `DOC-ICT-0001`, `DOC-IID-0001`, and `DOC-IID-0002`.
- The four-unit execution shape remains intact even though the issue-identity unit preserves two target records.
- `P2` is now complete: the five replacement `DOC` contract bodies are landed and the `DOC` contract index, promotion map, and family front door now expose the issue-governance extension packet explicitly.
- The immediate next step is `P3`: define the matching `GC` demotion and current-reader transition packet for the old current `GC-*` rows.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this section will hold the execution manifests, replacement packet draft, and any later `GC` demotion or reader-transition packet for this lane.
- This scaffold records the opening event and bounded next-step contract for `S0F-4I`.

### P0-C1-S1S2 (Issue-governance DOC promotion-extension lane opened | 2026-04-09)

- headSha: `<pending commit for S0F-4I/P0-C1-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/logs/log-S0F-4H-active-gc-current-registry-family-mapping-and-rehoming.md`
  - `docs/governance/contract/INDEX.md`
  - `docs/governance/views/view-doc-contract-promotion-map-v1.md`
- expected:
  - the repo has one explicit execution lane for converting the `S0F-4H` packet result into real `DOC` promotion and matched `GC` demotion work
  - later work no longer needs to overload `S0F-4H` with promotion-extension execution detail
- observed:
  - `S0F-4I` is now opened as the bounded four-unit issue-governance `DOC` promotion-extension and `GC` demotion packet lane
  - the immediate next step is now `P1` mapping-extension admission rather than reopening family ownership questions

### P1-C1-S1S2 (Next DOC mapping extension and naming boundary fixed | 2026-04-09)

- headSha: `<pending commit for S0F-4I/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/support-only/s0f-4i-doc-issue-governance-mapping-extension.json`
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/governance/contract/INDEX.md`
  - `docs/governance/views/view-doc-contract-promotion-map-v1.md`
- expected:
  - the repo has one explicit next `DOC` mapping extension for the bounded issue-governance packet
  - the repo has one fixed naming boundary for the target family-owned current bodies before replacement drafting begins
- observed:
  - the next admitted extension now covers issue creation, issue conclusion, issue context, and issue identity as one bounded issue-governance packet
  - the target naming boundary is fixed as `DOC-ICR-0001`, `DOC-ICL-0001`, `DOC-ICT-0001`, `DOC-IID-0001`, and `DOC-IID-0002`
  - the issue-identity landing unit stays shared at execution level while preserving two distinct target records for the two already-separated identity rule bodies

### P2-C1-S1S2 (Replacement DOC packet landed and reader surfaces aligned | 2026-04-09)

- headSha: `<pending commit for S0F-4I/P2-C1-S1S2>`
- artifacts:
  - `docs/logs/support-only/s0f-4i-doc-issue-governance-replacement-packet.json`
  - `docs/governance/contract/DOC-ICR-0001-issue-creation-metadata-english-body.md`
  - `docs/governance/contract/DOC-ICL-0001-issue-conclusion-post-merge-linkage.md`
  - `docs/governance/contract/DOC-ICT-0001-issue-context-sentence-count-main-vs-child.md`
  - `docs/governance/contract/DOC-IID-0001-parent-sidebar-ordering-ownership.md`
  - `docs/governance/contract/DOC-IID-0002-issue-title-keyword-controlled-vocabulary.md`
  - `docs/governance/contract/INDEX.md`
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-doc-contract-promotion-map-v1.md`
  - `docs/logs/log-S0F-4I-issue-governance-doc-promotion-extension-and-gc-demotion-packet.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the bounded issue-governance replacement packet exists as family-owned `DOC` current bodies before any `GC` demotion step
  - `DOC` reader surfaces are aligned enough that family-first reading can start from the replacement packet
- observed:
  - the replacement packet is now landed as five family-owned `DOC` current bodies across the four-unit execution shape
  - the `DOC` contract index and front door now expose those new current bodies explicitly
  - the old current `GC-*` rows are intentionally still untouched at this stage, leaving demotion and current-reader transition to `P3`

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-4I` as the direct execution follow-up after `S0F-4H`, dedicated to the bounded four-unit issue-governance `DOC` promotion-extension packet and matching `GC` demotion plan.
- 2026-04-09: completed `P1` by admitting the next `DOC` mapping extension for the issue-governance packet and fixing the target naming boundary for the five replacement `DOC` records.
- 2026-04-09: completed `P2` by landing the bounded replacement `DOC` packet, publishing five family-owned issue-governance current bodies, and aligning the `DOC` contract index, promotion map, and family front door before `GC` demotion begins.