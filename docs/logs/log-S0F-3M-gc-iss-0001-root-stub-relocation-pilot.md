# log-S0F-3M (Phase 3M: GC-ISS-0001 root-stub relocation pilot)

---

**id**: `S0F-3M`
**kind**: `log`
**title**: `GC-ISS-0001 root-stub relocation pilot v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Cleanup, Redirect, GC, ISS, Pilot, epic/s0, sub/3m`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
  **reference_log_1**: `docs/logs/log-S0F-3K-history-aware-old-gc-cleanup-recheck-after-doc-history-publication.md`
  **reference_log_2**: `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
  **reference_log_3**: `docs/logs/log-S0F-1K-lifecycle-exact-path-successor-package.md`
  **reference_log_4**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_5**: `docs/governance/views/view-iss-split-package-v1.md`
  **reference_log_6**: `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
  **reference_log_7**: `docs/governance/contracts/support-only/INDEX.md`
  **reference_log_8**: `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
  **reference_log_9**: `docs/logs/support-only/s0f-3l-gc-root-stub-p4-decision-manifest.json`
**issue_keyword**: `governance`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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

- `S0F-3M` opens the first real execution follow-up after `S0F-3L/P4`.
- This slice is not another design debate about whether old root-level `GC-*` redirects might move someday; it is the bounded pilot that tests the defended move model on one representative record: `GC-ISS-0001`.
- v1 of this slice is execution-first but still tightly bounded:
  - move only the retained full body for `GC-ISS-0001`
  - preserve the old root path as a root stub
  - update only the bounded direct-navigation surfaces that should open the moved retained body
  - do not widen the pilot to `GC-ISS-0002` through `GC-ISS-0005` until one-record execution evidence is clean

**Default choices (phase defaults / v1)**:

- Reuse the `S0F-3L` root-stub minimum shape and support-only target contract instead of redesigning either during execution.
- Treat `GC-ISS-0001` as the representative ISS pilot because it is the cleanest single-successor split sample and the next lane should prove execution value with the smallest blast radius.
- Keep lineage, split-package, and old-ID landing citations on the root path unless a surface truly needs the moved full historical body.
- Do not fold `GC-PRB-0001` into this slice.
- If the pilot reveals that bounded direct-reference rewrites are insufficient, stop with explicit evidence instead of widening the move.

## PR Summary Inputs (optional)

- Use this block because `S0F-3M` is expected to drive the first real legacy-redirect relocation pilot for the contracts-side root-stub model.

**PR summary bullets**:

- Execute the first bounded root-stub relocation pilot for `GC-ISS-0001`.
- Preserve old-ID landing at the root path while moving the retained full historical body to contracts support-only.
- Prove whether bounded reference rewrites plus support-only index support are sufficient before widening to the rest of `GC-ISS-*`.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the `GC-ISS-0001` relocation pilot.

**PR links**:

- Log: `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
- Previous design log: `docs/logs/log-S0F-3L-old-gc-root-redirect-replacement-and-stub-model.md`
- Current record: `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`

## Exported Sections / Outlet Ownership

- This slice exists to execute one already-defended relocation model, so outlet ownership should stay narrow unless the pilot reveals one reusable execution contract or runbook worth exporting.

**Outlet ownership**:

- `contract`: only if the pilot reveals one execution-stable relocation rule that must live beyond the source log
- `runbook`: only if the pilot becomes the reusable operator procedure for later `GC-ISS-*` moves
- `view`: no new view by default; lineage and cleanup-boundary readers already exist
- `index/front-door`: update `docs/governance/contracts/support-only/INDEX.md` only if the full retained body really moves
- `disposition/placement`: actual `keep root stub + move full retained body to support-only` decision for `GC-ISS-0001`
- `log-retained core`: pilot boundary, evidence, stop reasons, post-move validation, and any defer decision on widening to the remaining ISS records

## Definitions (optional)

- **pilot record**: the one selected preserved legacy redirect used to prove whether the defended move model works in practice before a wider wave is opened
- **root stub**: the minimal retained file that keeps the old path occupied and points readers to the moved full retained body and current successor record
- **moved retained body**: the relocated full historical contract body under `docs/governance/contracts/support-only/`
- **bounded direct-navigation rewrite**: changing only the references that truly need the moved full body, while leaving old-ID landing and lineage references on the root stub path

## Constraints

- Do not redesign the stub shape, support-only target shape, or split rule already fixed in `S0F-3L`.
- Do not widen the slice to all `GC-ISS-*` records unless the one-record pilot is already executed and verified cleanly.
- Do not rewrite lineage or cleanup-boundary views merely because the file body moves; those surfaces may continue to cite the root stub.
- Do not move `GC-PRB-0001` or its paired support-only backfill in this slice.
- Keep evidence explicit enough that later work can tell whether the pilot succeeded, failed, or should remain one-off.

## Scope

- `P0`: open `S0F-3M` as the bounded `GC-ISS-0001` execution pilot and fix the move boundary
- `P1`: inventory the exact direct-navigation rewrite set and target surfaces for `GC-ISS-0001`
- `P2`: execute the file move, root-stub replacement, and support-only index mutation
- `P3`: verify the moved body, root stub, and bounded reference rewrites all read correctly after execution
- `P4`: decide whether the result justifies widening to more `GC-ISS-*` records or remains a single defended pilot

## Success Criteria (DoD)

- One reader can point to the exact `GC-ISS-0001` root stub and moved retained body after execution.
- One reader can explain which references stayed on the root path versus which were retargeted to the moved full body.
- `docs/governance/contracts/support-only/INDEX.md` exposes the moved retained body explicitly if the move executes.
- The repo has one explicit post-move answer on whether the root-stub model works in practice for a real `GC-ISS-*` record.
- Later work does not need to rediscover whether the next step is widen, stop, or retain the pilot as one-off evidence.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the `GC-ISS-0001` pilot boundary and rewrite set are explicit
  - the root-stub relocation is either executed and verified or explicitly stopped with defended evidence
  - the next step is clear as `widen`, `hold`, or `stop`

## P0 (Contract | v1)

### P0-C1-S1 (Pilot boundary fixed | v1)

- `S0F-3M` is now opened as the first real execution slice after `S0F-3L`.
- This slice owns only the representative `GC-ISS-0001` pilot.
- It does not reopen whole-family admissibility or PRB umbrella handling.

### P0-C1-S2 (Execution sequence fixed | v1)

- The execution order for this pilot is now:
  - identify the exact direct-navigation rewrite set
  - execute `move full body + leave root stub + update support-only index`
  - verify root-path landing, moved-body reading, and successor guidance after the move
  - then decide whether the same execution pattern should widen to more ISS records

### P0-C1-S3 (Evidence contract | v1)

- Evidence for this slice should record:
  - the selected pilot record and resolved target paths
  - the bounded rewrite-set inventory
  - the executed root-stub and moved-body paths
  - the support-only index mutation if present
  - the post-move verification result and widening recommendation

## P1 (Rewrite-set inventory | v1)

### P1-C1-S1 (Direct-navigation rewrite set inventoried for `GC-ISS-0001` | v1)

- `P1` now fixes the exact pre-existing path-reference surface for the pilot record.
- The repo currently cites `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md` in a very narrow way:
  - `view-iss-split-package-v1.md` cites it as part of preserved split-package lineage
  - `view-gc-first-cleanup-boundary-v1.md` cites it as part of the defended root-readable legacy set
  - `log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md` cites it as part of the cleanup ledger that originally kept the file in place as a legacy redirect
- No current reader surface was found that clearly uses the old path because it needs the full retained historical body itself.
- The practical P1 result is therefore narrower than expected:
  - the pre-existing direct-navigation rewrite set is empty
  - the only required non-file-surgery write outside the root file and moved body themselves is the future support-only index entry in `docs/governance/contracts/support-only/INDEX.md`

### P1-C1-S2 (Keep-root versus retarget-to-support-only split fixed | v1)

- The keep-versus-retarget split is now explicit for the pilot record:
  - keep on the root path: lineage, split-package, cleanup-boundary, and cleanup-ledger citations
  - retarget to support-only: none among the pre-existing reader surfaces reviewed in `P1`
- This split stays aligned with the `S0F-3L` replacement contract:
  - root-path readers may continue landing on the stub when their job is old-ID landing or lineage orientation
  - support-only should be linked only where the reader truly needs the moved retained body itself
- `P1` therefore clears one major execution uncertainty:
  - `P2` does not need a broad rewrite wave
  - `P2` only needs the bounded core writes of `move full body + leave root stub + add support-only index entry`

## P2 (Relocation execution | v1)

### P2-C1-S1 (Moved retained full body and wrote root stub for `GC-ISS-0001` | v1)

- `P2` now executes the representative pilot instead of keeping it design-only.
- The retained historical body for `GC-ISS-0001` now lives at:
  - `docs/governance/contracts/support-only/GC-ISS-0001-issue-creation-metadata-english-body.md`
- The original root path is now occupied by the planned stub rather than the full retained body:
  - `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
- The executed stub keeps the old ID readable, points readers to `GC-ICR-0001` for current rule meaning, and exposes the moved support-only body only when the retained historical wording is needed.

### P2-C1-S2 (Support-only index updated; no bounded rewrite wave needed | v1)

- `docs/governance/contracts/support-only/INDEX.md` now lists the moved `GC-ISS-0001` retained body explicitly.
- The pre-existing reader-surface split fixed in `P1` holds at execution time:
  - no lineage, cleanup-boundary, or cleanup-ledger surface needed retargeting during `P2`
  - no broad direct-navigation rewrite wave was required to land the pilot cleanly
- The practical `P2` result is therefore:
  - one moved retained body
  - one root stub left in place
  - one support-only index addition
  - zero pre-existing reader retargets

## P3 (Post-move verification | v1)

### P3-C1-S1 (Root-stub landing and successor guidance verified for `GC-ISS-0001` | v1)

- `P3` now verifies the executed root stub as a reader surface rather than assuming the move succeeded just because the files exist.
- The root path remains readable and carries the expected bridge fields and guidance:
  - old record identity is still visible at the original root path
  - the stub points readers to `GC-ICR-0001` for current rule meaning
  - the stub points readers to the moved support-only retained body when historical wording is needed
  - the stub still reads like a landing surface rather than like a deleted-path placeholder

### P3-C1-S2 (Moved retained body and zero-retarget execution result verified | v1)

- The moved retained body is now confirmed readable under the contracts-side support-only surface.
- `docs/governance/contracts/support-only/INDEX.md` exposes the moved `GC-ISS-0001` body explicitly, so support-only navigation does not depend on directory browsing.
- The zero-retarget result also verifies cleanly:
  - `view-iss-split-package-v1.md` still cites the root path
  - `view-gc-first-cleanup-boundary-v1.md` still cites the root path
  - `log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md` still cites the root path
  - no reader regression was found that would force a second rewrite wave after the move
- `P3` therefore confirms that the representative `GC-ISS-0001` pilot is not merely executed; it is executed cleanly enough to support a real widen-versus-hold decision in `P4`.

## P4 (Next-lane decision | v1)

### P4-C1-S1 (Hold the verified pilot; do not widen to the rest of `GC-ISS-*` yet | v1)

- `P4` now closes the widen-versus-hold question explicitly.
- The result of `S0F-3M` is not `expand immediately` and not `the pilot failed`.
- The defended answer is now:
  - keep `GC-ISS-0001` as one verified pilot
  - do not widen the same execution pattern to `GC-ISS-0002` through `GC-ISS-0005` yet
  - keep `GC-PRB-0001` on its separate deferred path
- The main reason to hold is that the pilot has already delivered the thing this slice needed most:
  - proof that `support-only retained body + root stub` works in practice for one real ISS record
- Widening now would add more cleanup writes, but it would not change the current semantic reading model:
  - the current active issue-governance contracts already live at `GC-ICR-0001`, `GC-ICL-0001`, `GC-ICT-0001`, `GC-IID-0001`, and `GC-IID-0002`
  - the remaining old `GC-ISS-*` files are legacy redirects, not current rule owners
- `P4` also fixes the family-boundary answer that motivated the user's question:
  - the `DOC` family is current for doc-first control-plane contracts such as role boundaries, source-log compatibility, taxonomy, placement, and front-door transition
  - it is not the semantic owner for the active issue-governance registry contracts that still read through current `GC-*` narrow-registry records
- Under that model, the meaning of this cleanup lane is now narrower and more practical:
  - it exists to reduce legacy-root clutter safely when doing so adds reader or maintenance value
  - it does not exist to re-home every active governance contract into the `DOC` family by default
- Future widening remains allowed, but only if one later bounded slice can show concrete value beyond `the model is feasible`, because feasibility is already proven now.

## Plan (draft)

### P1 (Rewrite-set inventory)

- P1-C1-S1: inventory direct-navigation references that should read the moved retained body after the pilot
- P1-C1-S2: separate references that should stay on the root stub path from references that should retarget to support-only

### P2 (Relocation execution)

- P2-C1-S1: move `GC-ISS-0001` full retained body to contracts support-only and replace the root file with the planned stub
- P2-C1-S2: update `docs/governance/contracts/support-only/INDEX.md` and apply the bounded direct-navigation rewrites

### P3 (Post-move verification)

- P3-C1-S1: verify the root stub preserves old-ID landing and successor guidance
- P3-C1-S2: verify the moved retained body and retargeted references read correctly

### P4 (Next-lane decision)

- P4-C1-S1: decide whether to widen the same execution model to more `GC-ISS-*` records or hold the result as one defended pilot

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: pilot boundary fixed
- [x] `P0-C1-S2`: execution sequence fixed
- [x] `P0-C1-S3`: evidence contract fixed

### P1 (Rewrite-set inventory)

- [x] `P1-C1-S1`: direct-navigation rewrite set inventoried
- [x] `P1-C1-S2`: keep-root versus retarget-to-support-only split fixed

### P2 (Relocation execution)

- [x] `P2-C1-S1`: full retained body moved and root stub written
- [x] `P2-C1-S2`: support-only index and bounded rewrites applied

### P3 (Post-move verification)

- [x] `P3-C1-S1`: root-stub landing and successor guidance verified
- [x] `P3-C1-S2`: moved-body reading and retargeted references verified

### P4 (Next-lane decision)

- [x] `P4-C1-S1`: widen-versus-hold decision recorded

## Current Status (recommended)

- `S0F-3M` is now opened as the bounded execution follow-up to `S0F-3L`.
- The repo now has one explicit source log for the first real `GC-ISS-0001` root-stub relocation pilot instead of carrying that next step only as a recommendation in `S0F-3L`.
- `P0` is now complete: pilot scope, execution order, and evidence contract are fixed.
- `P1` is now complete: the exact pre-existing reference surface is fixed, and it turns out to be narrower than the design lane had to assume.
- No existing reader surface currently has to be retargeted to the moved support-only body; lineage, cleanup-boundary, and cleanup-ledger citations should remain on the future root stub path.
- `P2` is now complete: `GC-ISS-0001` is no longer a full retained body at the root path; it now runs on the executed `support-only retained body + root stub` model.
- The support-only index now exposes the moved retained body explicitly, and execution did not require any pre-existing reader-surface retargets.
- `P3` is now complete: the executed root stub reads correctly, the moved retained body is readable under the support-only surface, and the zero-retarget execution result did not regress the current lineage or cleanup readers.
- `P4` is now complete and `S0F-3M` is now stable: the verified pilot should be held as one defended result rather than widened immediately to the rest of `GC-ISS-*`.
- The repo now has one explicit answer that separates `legacy redirect cleanup` from `current contract promotion`:
  - current active issue-governance rules still read through current `GC-*` narrow-registry contracts
  - current doc-first control-plane rules read through `DOC-*` family contracts
- The immediate next step is no longer inside `S0F-3M`; future work should reopen only if one bounded slice has concrete value in widening the same cleanup model to more legacy ISS redirects.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this section will hold the bounded rewrite-set inventory, execution write set, and post-move verification for the `GC-ISS-0001` pilot.
- This scaffold records the opening event and fixed execution boundary for `S0F-3M`.

### P0-C1-S1S2S3 (Representative `GC-ISS-0001` pilot lane opened | 2026-04-09)

- headSha: `<pending commit for S0F-3M/P0-C1-S1S2S3>`
- artifacts:
  - `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/logs/support-only/s0f-3l-gc-root-stub-p4-decision-manifest.json`
- expected:
  - the repo has one explicit child slice for the first ISS execution pilot instead of leaving the next step implicit in `S0F-3L`
  - later execution work no longer needs to reopen whether the first pilot is `GC-ISS-*`, `GC-PRB-0001`, or a whole preserved-subset move
- observed:
  - `S0F-3M` is now opened with one representative `GC-ISS-0001` boundary, one fixed P1-P4 execution order, and one explicit non-goal of widening to PRB or a multi-record wave at open time

### P1-C1-S1S2 (Rewrite-set inventory fixed for `GC-ISS-0001` pilot | 2026-04-09)

- headSha: `<pending commit for S0F-3M/P1-C1-S1S2>`
- artifacts:
  - `docs/logs/support-only/s0f-3m-gc-iss-0001-rewrite-set-manifest.json`
  - `docs/governance/views/view-iss-split-package-v1.md`
  - `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
  - `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
  - `docs/governance/INDEX.md`
  - `docs/governance/contracts/support-only/INDEX.md`
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
- expected:
  - the repo has one explicit classification of which `GC-ISS-0001` references should stay on the root path versus which should retarget to support-only
  - later execution no longer needs to guess whether a broad rewrite wave is required
- observed:
  - the pre-existing reader surfaces are all lineage, cleanup-boundary, or cleanup-ledger readers that should remain on the root path through the future stub
  - no pre-existing reader surface currently requires retargeting to the moved full body, so `P2` may proceed with only the bounded core writes plus the support-only index addition

### P2-C1-S1S2 (Root-stub relocation executed for `GC-ISS-0001` pilot | 2026-04-09)

- headSha: `<pending commit for S0F-3M/P2-C1-S1S2>`
- artifacts:
  - `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
  - `docs/governance/contracts/support-only/GC-ISS-0001-issue-creation-metadata-english-body.md`
  - `docs/governance/contracts/support-only/INDEX.md`
  - `docs/logs/support-only/s0f-3m-gc-iss-0001-execution-manifest.json`
  - `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
- expected:
  - the representative `GC-ISS-0001` pilot executes as `move full body + leave root stub + add support-only index entry`
  - the move lands without a broad pre-existing reader-retarget wave
- observed:
  - the full retained body now lives under the contracts-side support-only surface while the original root path remains occupied by a stub
  - the support-only index now lists the moved retained body, and no pre-existing reader surface had to be retargeted during execution

### P3-C1-S1S2 (Post-move verification passed for `GC-ISS-0001` pilot | 2026-04-09)

- headSha: `<pending commit for S0F-3M/P3-C1-S1S2>`
- artifacts:
  - `docs/governance/contracts/GC-ISS-0001-issue-creation-metadata-english-body.md`
  - `docs/governance/contracts/support-only/GC-ISS-0001-issue-creation-metadata-english-body.md`
  - `docs/governance/contracts/support-only/INDEX.md`
  - `docs/governance/views/view-iss-split-package-v1.md`
  - `docs/governance/views/view-gc-first-cleanup-boundary-v1.md`
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  - `docs/logs/support-only/s0f-3m-gc-iss-0001-post-move-verification.json`
  - `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
- expected:
  - the root stub remains a readable old-ID landing surface with correct successor and moved-body guidance
  - the moved retained body remains readable under support-only without forcing a second reader-retarget wave
- observed:
  - the root stub is readable and preserves old-ID landing, successor guidance, and moved-body guidance exactly as planned
  - the moved retained body is readable under support-only, the local support-only index exposes it explicitly, and the current lineage / cleanup readers still resolve through the root path without regression

### P4-C1-S1 (Hold-versus-widen decision fixed after verified pilot | 2026-04-09)

- headSha: `<pending commit for S0F-3M/P4-C1-S1>`
- artifacts:
  - `docs/logs/support-only/s0f-3m-gc-iss-0001-p4-decision-manifest.json`
  - `docs/governance/INDEX.md`
  - `docs/governance/views/view-doc-current-front-door-v1.md`
  - `docs/governance/views/view-gc-triage-and-retention-rule-v1.md`
  - `docs/governance/contracts/GC-ISS-0002-issue-conclusion-post-merge-linkage.md`
  - `docs/governance/contracts/GC-ISS-0003-issue-context-sentence-count-main-vs-child.md`
  - `docs/logs/log-S0F-3M-gc-iss-0001-root-stub-relocation-pilot.md`
- expected:
  - the repo has one explicit answer on whether the verified `GC-ISS-0001` pilot should widen immediately to the rest of `GC-ISS-*`
  - the repo has one explicit answer on why this cleanup lane does or does not imply a broader `GC -> DOC` migration
- observed:
  - the pilot is now held as one defended verified result and does not widen immediately to `GC-ISS-0002` through `GC-ISS-0005`
  - the repo now records that current issue-governance semantics still live in active `GC-*` narrow-registry contracts, while `DOC-*` remains the current family for doc-first control-plane contracts rather than a default replacement for those active governance records

## Recent changes (for traceability, optional)

- 2026-04-09: opened `S0F-3M` as the first bounded `GC-ISS-0001` root-stub relocation pilot after `S0F-3L/P4` chose a representative ISS-first execution lane.
- 2026-04-09: completed `P1` by fixing the exact `GC-ISS-0001` rewrite-set inventory and confirming that the current reader surface should stay on the future root stub path rather than being broadly retargeted to support-only.
- 2026-04-09: completed `P2` by moving the `GC-ISS-0001` retained full body to contracts support-only, replacing the root file with the executed stub, and updating the local support-only index without requiring a pre-existing reader-retarget wave.
- 2026-04-09: completed `P3` by verifying that the executed root stub, moved retained body, local support-only navigation, and zero-retarget execution result all read cleanly after the move.
- 2026-04-09: completed `P4` by holding the verified `GC-ISS-0001` result as one defended pilot, declining immediate expansion to the remaining `GC-ISS-*` redirects, and fixing the boundary between legacy `GC` cleanup work and current `DOC` family promotion.