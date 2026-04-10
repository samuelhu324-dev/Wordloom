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
- `P1-C2-S1`: define long-path canonical contract naming grammar
- `P1-C2-S2`: define parent versus child contract roles
- `P1-C2-S3`: define the later template rollout boundary for parent and child contract generation
- `P1-C3-S1`: define when `split_from / split_into` should be used
- `P1-C3-S2`: define when split should not be used and another lineage verb is required

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

### P1-C2-S1 (Long-path canonical contract naming grammar fixed | v1)

- Canonical rebuilt contract ids should now keep the `DOC-...-<sequence>` shape, but the middle path must stay human-readable rather than collapse into short opaque abbreviations.
- The naming grammar is now fixed as:
  - `DOC-<DOMAIN>-<SUBDOMAIN>-...-<CATEGORY>-<NNNN>-<summary>`
- Under this rule:
  - `DOC` marks canonical chronology-first contract records
  - the middle path expresses the governance classification path directly, such as `WORKFLOW-GITHUB-ISSUES-TITLE`
  - `<NNNN>` is the fixed-width sequence number for that exact contract category path
  - `<summary>` remains a reader-facing short explanation and does not carry identity by itself
- The purpose of this grammar is to preserve machine-stable ids while keeping the contract type legible to human readers at first glance.

### P1-C2-S2 (Parent versus child contract roles fixed | v1)

- A `parent contract` now owns mechanism introduction, `why`, and boundary:
  - why this mechanism was introduced
  - what larger workflow or governance boundary it established
  - what later narrower rule contracts should inherit from it
- A `child contract` now owns one independently judgeable rule body beneath that parent, such as:
  - title grammar
  - tag grammar
  - another later narrow rule that can be reviewed or superseded without rewriting the parent introduction contract
- Under this rule, one source issue may justify one parent contract plus multiple child contracts when the source mixes mechanism introduction with multiple narrower rule bodies.
- This split exists so readers do not have to choose between one unreadably broad contract and many tiny contracts that lose the introduction boundary.

### P1-C2-S3 (Template rollout boundary for parent and child generation fixed | v1)

- `P1` now fixes the definition only; it does not yet generate the new parent or child contract bodies themselves.
- The later population work should therefore add explicit template content for:
  - one parent-contract draft shape centered on `why and boundary`
  - one child-contract draft shape centered on one independently judgeable rule body
- Under this boundary, the next content-generation phase should create:
  - one parent contract for the GitHub issue mechanism introduction under the workflow/GitHub/issues path
  - one child contract for title rules
  - one child contract for tag rules
- This later generation work belongs to a new `P3` cycle after the naming and split model is accepted.

### P1-C3-S1 (Split usage rule fixed | v1)

- Use `split_into` on an earlier contract only when that earlier contract already carries more than one independently judgeable rule body and later history chooses to separate those rule bodies into narrower successor contracts.
- Use `split_from` on each narrower successor contract only when that successor is one of those separated rule bodies from the earlier broader contract.
- Under this rule, split does not require many children; one broader contract may split into only two narrower contracts and still count as a valid split relationship.
- A split parent may remain historically readable as the earlier broader state even after children exist, but its job changes from `single mixed owner` to `earlier broader owner that later decomposed`.

### P1-C3-S2 (Non-split boundary fixed | v1)

- Do not use split when one newer contract simply replaces one older contract as the clearer whole-rule owner; that is `supersedes / superseded_by`.
- Do not use split when one newer contract only absorbs part of an earlier contract's meaning without a clean decomposition boundary; that is `absorbed_from / absorbed_into`.
- Under this rule, split is specifically for `one broader rule body became multiple narrower rule bodies`, not for every parent/child directory shape or every later related contract.

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

- `P3-C1-S1`: initial broad foundational batch draft from `S0A + S0B` for review
- `P3-C1-S2`: withdraw that batch if it fails the issue-first readability standard
- `P3-C2-S1`: publish one replacement issue-first preview contract from `S0A-1A`
- `P3-C2-S2`: keep source ownership explicit as GitHub issue only when no local source log exists
- `P3-C3-S1`: generate one parent contract for GitHub issue mechanism introduction under the new long-path naming grammar
- `P3-C3-S2`: generate one title child contract and one tag child contract beneath that parent
- `P3-C3-S3`: update template-backed indices and standing notes for the new parent/child packet
- `P3-C4-S1`: generate one broader workflow-layer contract from `S0A/2A`
- `P3-C4-S2`: update indices and standing notes so the workflow-layer contract and the narrower GitHub-issues packet can be read together
- `P3-C5-S1`: generate one labs-layer contract from `S0B/1A` under `workflow/labs`
- `P3-C5-S2`: update indices and standing notes so the labs-layer contract can be judged alongside the broader workflow contract and narrower GitHub-issues packet

### P3-C1-S1 (Initial broad foundational batch drafted for review | withdrawn)

- An initial four-contract foundational batch was drafted in workspace from `S0A + S0B` as the first attempt at chronology-first population.
- User review rejected that batch because it was too broad, partially outside the intended docs scope, and too abstract to satisfy the `look once and know the problem` standard.

### P3-C1-S2 (Rejected broad batch withdrawn from workspace | v1)

- The rejected four-contract draft has now been removed from `docs/governance/contracts/`.
- Under this correction, `P3` no longer treats broad foundational synthesis as acceptable by default.

### P3-C2-S1 (Replacement issue-first preview contract published from `S0A-1A` | v1)

- The canonical contracts root now carries one replacement preview contract only:
  - `S0A-1A`: GitHub issue breakdown, title, and tag governance
- This preview is intentionally narrower and more literal than the withdrawn batch: the contract title itself should tell the reader what problem the source issue solved.

### P3-C2-S2 (Issue-only source boundary made explicit | v1)

- The `S0A-1A` preview contract now states explicitly that its source is the GitHub issue only.
- No local `S0A-1A` source log is currently present in the workspace, so the replacement contract must not pretend to be log-sourced.
- The canonical contracts index now exposes this one preview contract directly and records that the earlier broad batch was rejected.

### P3-C3-S1 (Parent contract generated under long-path naming grammar | v1)

- The temporary mixed `S0A-1A` preview has now been replaced in workspace by one parent contract:
  - `DOC-WORKFLOW-GITHUB-ISSUES-0001`: GitHub Issues as canonical work breakdown
- This parent contract now owns mechanism introduction, `why`, and boundary only:
  - why the workflow starts using GitHub Issues as the canonical breakdown unit
  - what boundary GitHub Projects views do and do not replace
  - what narrower child rules belong beneath that parent rather than inside it

### P3-C3-S2 (Title and tag child contracts generated beneath the parent | v1)

- The first child contract pair now exists beneath that parent contract:
  - `DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001`: issue title encodes level and category
  - `DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001`: issue tags follow role-based naming
- Under this result:
  - title grammar is no longer mixed into the parent mechanism contract
  - tag naming grammar is no longer mixed into the title-rule contract
  - all three contracts keep the source boundary explicit as GitHub issue only because no local `S0A-1A` log exists in the workspace

### P3-C3-S3 (Indices and standing notes updated for the new parent-child packet | v1)

- The canonical contracts index now exposes the new parent-and-child packet directly.
- The temporary mixed `S0A-1A` preview contract file has now been removed from the canonical root in workspace.
- Under this result, the first issue-first rebuild packet now reads as one parent mechanism contract plus two narrow child rule contracts instead of one mixed preview file.

### P3-C4-S1 (Workflow-layer contract generated from `S0A/2A` | v1)

- A broader workflow-layer contract now exists under the canonical root:
  - `DOC-WORKFLOW-0001`: structured doc refinement pipeline
- This contract is intentionally placed at the `WORKFLOW` layer rather than inside the narrower GitHub-issues subtree.
- It owns the historical workflow boundary around:
  - `log -> lab -> runbook -> adr`
  - source-linking back to inputs and evidence rather than forward-looking `where next` navigation

### P3-C4-S2 (Workflow-layer and GitHub-issues packet now read together | v1)

- The canonical contracts index now exposes both:
  - the broader `DOC-WORKFLOW-0001` workflow-layer draft
  - the narrower GitHub-issues parent-and-child packet from `S0A-1A`
- Under this result, readers can now judge the broader workflow contract separately from the later GitHub-issues mechanism contract packet rather than forcing both into one document.

### P3-C5-S1 (Labs-layer contract generated from `S0B/1A` | v1)

- A narrower labs-layer contract now exists under the canonical root:
  - `DOC-WORKFLOW-LABS-001`: tools labs and snapshots
- This contract is intentionally placed at `workflow/labs` beneath the broader `WORKFLOW` layer.
- It owns the historical labs/snapshots governance boundary around:
  - snapshot classes such as golden fixtures, diff snapshots, and ad-hoc dumps
  - minimal retained evidence sets
  - safe-to-purge cleanup after conclusions become replayable and verifiable

### P3-C5-S2 (Labs-layer draft now reads alongside workflow and GitHub-issues layers | v1)

- The canonical contracts index now exposes three layers together:
  - the broader `DOC-WORKFLOW-0001` workflow-layer draft
  - the narrower `DOC-WORKFLOW-LABS-001` labs-layer draft
  - the GitHub-issues parent-and-child packet from `S0A-1A`
- Under this result, readers can now judge the labs/snapshots contract separately instead of forcing it either into the broader workflow contract or into the GitHub-issues packet.

### P3-C3 (Next parent-and-child generation packet | planned)

- The next generation packet after this definition update should stop using one mixed preview contract for `S0A-1A`.
- Instead it should produce:
  - one parent contract for workflow/GitHub/issues mechanism introduction
  - one child contract for issue-title rules
  - one child contract for issue-tag rules
- That packet should also add the corresponding parent/child template-backed notes to the canonical contract root so later issue-based rebuild work can reuse the same pattern.

## Execution Checklist (unchecked)

### P0 (Reset Boundary)

- [x] `P0-C1-S1`: canonical versus legacy roots fixed
- [x] `P0-C1-S2`: immediate rebuild sequence fixed

### P1 (Chronology-first contract model)

- [x] `P1-C1-S1`: contract versus evidence rule fixed
- [x] `P1-C1-S2`: lineage verbs and structured fields fixed
- [x] `P1-C2-S1`: long-path canonical contract naming grammar fixed
- [x] `P1-C2-S2`: parent versus child contract roles fixed
- [x] `P1-C2-S3`: template rollout boundary for parent and child generation fixed
- [x] `P1-C3-S1`: split usage rule fixed
- [x] `P1-C3-S2`: non-split boundary fixed

### P2 (First rebuild packet)

- [x] `P2-C1-S1`: first foundational packet fixed
- [x] `P2-C1-S2`: follow-on rebuild order fixed

### P3 (First foundational contracts)

- [x] `P3-C1-S1`: initial broad foundational batch drafted for review
- [x] `P3-C1-S2`: rejected broad batch withdrawn from workspace
- [x] `P3-C2-S1`: replacement issue-first preview contract published from `S0A-1A`
- [x] `P3-C2-S2`: issue-only source boundary made explicit
- [x] `P3-C3-S1`: generate one parent contract for GitHub issue mechanism introduction under the new long-path naming grammar
- [x] `P3-C3-S2`: generate one title child contract and one tag child contract beneath that parent
- [x] `P3-C3-S3`: update template-backed indices and standing notes for the new parent/child packet
- [x] `P3-C4-S1`: generate one broader workflow-layer contract from `S0A/2A`
- [x] `P3-C4-S2`: update indices and standing notes so the workflow-layer contract and the narrower GitHub-issues packet can be read together
- [x] `P3-C5-S1`: generate one labs-layer contract from `S0B/1A` under `workflow/labs`
- [x] `P3-C5-S2`: update indices and standing notes so the labs-layer contract can be judged alongside the broader workflow contract and narrower GitHub-issues packet

## Current Status

- `S0F-7A` is now opened as the chronology-first contract rebuild reset lane.
- `P0` is now complete: canonical versus legacy contract roots are explicit, and the immediate next step is to define the chronology-first record model before any foundational contracts are generated.
- `P1` is now complete: the repo now has one explicit contract-versus-evidence rule and one structured lineage-verb model for chronology-first rebuild.
- `P1` is now extended and complete through `C3`: the repo now also has one explicit long-path canonical naming grammar, one parent/child contract split rule, and one precise split-versus-non-split boundary for later lineage decisions.
- `P2` is now complete: the first foundational rebuild packet is fixed as `S0A + S0B`, and the follow-on chronology-first rebuild order is fixed as `S0C -> S0D -> S0E -> S0F`.
- `P3` now has three readable layers in workspace: one broader workflow-layer draft from `S0A/2A`, one narrower labs-layer draft from `S0B/1A`, and one GitHub-issues parent-and-child packet from `S0A-1A`.
- The immediate next step is user review of how these three layers should relate before any later chronology-first population continues.

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

### P1-C2-S1S2S3 (Naming grammar and parent-child split model fixed | 2026-04-10)

- headSha: `de5c003eb`
- artifacts:
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should define a human-readable long-path canonical naming grammar before later chronology-first contract generation continues
  - the repo should define how one source may split into one parent introduction contract plus narrower child rule contracts
- observed:
  - canonical contract naming now uses one long-path `DOC-<DOMAIN>-...-<CATEGORY>-<NNNN>-<summary>` grammar instead of opaque short abbreviations
  - parent contracts now own mechanism introduction and boundary, while child contracts own independently judgeable narrow rule bodies such as title or tag rules

### P1-C3-S1S2 (Split usage boundary fixed | 2026-04-10)

- headSha: `<workspace not committed yet for S0F-7A/P1-C3-S1S2>`
- artifacts:
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/governance/contracts/_template-contract-record.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should define when split lineage is appropriate and when another lineage verb should be used instead
- observed:
  - split is now explicitly limited to cases where one broader rule body decomposes into narrower rule bodies
  - split is now explicitly separated from one-to-one supersession and from partial absorption

### P3-C3-S1S2S3 (First parent-and-child packet generated from `S0A-1A` | 2026-04-10)

- headSha: `8cd8d26ea`
- artifacts:
  - `docs/governance/contracts/workflow/github/issues/DOC-WORKFLOW-GITHUB-ISSUES-0001-github-issues-as-canonical-work-breakdown.md`
  - `docs/governance/contracts/workflow/github/issues/title/DOC-WORKFLOW-GITHUB-ISSUES-TITLE-0001-issue-title-encodes-level-and-category.md`
  - `docs/governance/contracts/workflow/github/issues/tags/DOC-WORKFLOW-GITHUB-ISSUES-TAGS-0001-issue-tags-follow-role-based-naming.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
- expected:
  - the repo should replace the temporary mixed `S0A-1A` preview with one parent contract plus two child rule contracts
  - the packet should keep issue-only sourcing explicit because no local `S0A-1A` log exists in the workspace
- observed:
  - the repo now has one parent contract for introducing GitHub Issues as canonical workflow breakdown and two child contracts for title grammar and tag naming
  - the earlier mixed preview file has been removed from the canonical root in favor of the new parent-and-child packet

### P3-C4-S1S2 (Workflow-layer contract generated from `S0A/2A` | 2026-04-10)

- headSha: `3caadb115`
- artifacts:
  - `docs/governance/contracts/workflow/DOC-WORKFLOW-0001-structured-doc-refinement-pipeline.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should gain one broader workflow-layer contract from `S0A/2A` without collapsing it into the narrower GitHub-issues packet
  - that draft should stay explicit about issue-only sourcing because no local `S0A/2A` source log exists in the workspace
- observed:
  - the repo now has one `DOC-WORKFLOW-0001` draft that captures the broader structured-doc refinement pipeline at the `WORKFLOW` layer
  - the canonical index now exposes that broader workflow-layer draft alongside the narrower GitHub-issues contract packet

### P3-C5-S1S2 (Labs-layer contract generated from `S0B/1A` | 2026-04-10)

- headSha: `32be9142e`
- artifacts:
  - `docs/governance/contracts/workflow/labs/DOC-WORKFLOW-LABS-001-tools-labs-and-snapshots.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - the repo should gain one narrower labs-layer contract from `S0B/1A` without collapsing it into either the broader workflow contract or the narrower GitHub-issues packet
  - that draft should stay explicit about issue-only sourcing because no local `S0B/1A` source log exists in the workspace
- observed:
  - the repo now has one `DOC-WORKFLOW-LABS-001` draft that captures labs/snapshots governance at the `workflow/labs` layer
  - the canonical index now exposes that labs-layer draft alongside the broader workflow contract and narrower GitHub-issues packet

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

### P3-C2-S1S2 (Replacement issue-first preview contract landed | 2026-04-10)

- headSha: `<workspace not committed yet for S0F-7A/P3-C2-S1S2>`
- artifacts:
  - `docs/governance/contracts/S0A-1A-github-issue-breakdown-title-and-tag-governance.md`
  - `docs/governance/contracts/INDEX.md`
  - `docs/logs/log-S0F-7A-chronology-first-contract-rebuild.md`
- expected:
  - the repo should keep one replacement issue-first preview contract after the earlier broad batch is withdrawn
  - that contract should make its problem readable at a glance without pretending to have a local source log
- observed:
  - the repo now keeps one `S0A-1A` preview contract that states issue breakdown, title encoding, and tag naming governance directly in the contract body
  - the replacement draft keeps its issue-only source boundary explicit because no local `S0A-1A` log exists in the workspace

## Recent changes (for traceability, optional)

- 2026-04-10: opened `S0F-7A` as the reset lane for chronology-first contract rebuild.
- 2026-04-10: fixed the canonical versus legacy contract roots and the immediate rebuild sequence before any new foundational contracts are generated.
- 2026-04-10: completed `P1` by fixing the chronology-first contract-versus-evidence rule and by defining the lineage verbs plus structured template fields needed for supersede, split, absorb, and retire cases.
- 2026-04-10: extended `P1` with one new `C2` cycle that fixes long-path canonical naming grammar, parent-versus-child contract roles, and the later template rollout boundary for parent/child generation.
- 2026-04-10: completed `P2` by fixing the first foundational rebuild packet as `S0A + S0B` and by fixing the follow-on chronology-first rebuild order as `S0C -> S0D -> S0E -> S0F`.
- 2026-04-10: the first broad four-contract `P3` draft was rejected in review and withdrawn from workspace.
- 2026-04-10: opened `P3-C2` as a narrower correction and published one replacement issue-first preview contract sourced from `S0A-1A` only.
- 2026-04-10: completed `P3-C3` by replacing the temporary mixed preview with one parent contract plus title/tag child contracts under the long-path naming grammar.
- 2026-04-10: completed `P3-C4` by generating one broader `DOC-WORKFLOW-0001` workflow-layer contract from issue `S0A/2A`.
- 2026-04-10: completed `P3-C5` by generating one narrower `DOC-WORKFLOW-LABS-001` labs-layer draft from issue `S0B/1A`.
- 2026-04-10: extended `P1` with one new `C3` cycle that fixes when split lineage should and should not be used.
