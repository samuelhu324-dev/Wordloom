# log-S0F-3I (Phase 3I: governance contract taxonomy and placement model)

---

**id**: `S0F-3I`
**kind**: `log`
**title**: `governance contract taxonomy and placement model v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Contract, Taxonomy, epic/s0, sub/3i`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/420`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/433`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  **reference_log_1**: `docs/logs/log-S0F-3A-governance-contract-index-and-delta-model.md`
  **reference_log_2**: `docs/logs/log-S0F-3C-governance-contract-series-audit-and-admission.md`
  **reference_log_3**: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
  **reference_log_4**: `docs/logs/INDEX.md`
  **reference_log_5**: `docs/governance/views/view-contract-family-inventory-v1.md`
  **reference_log_6**: `docs/governance/views/view-contract-family-placement-map-v1.md`
**issue_keyword**: `taxonomy`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system`
**issue_module_labels**: ``
**issue_milestone**: `road-002: projection runtime platformization and evidence governance`
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
**roadmap_milestone**: `M2`
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-04-08`
**updated**: `2026-04-14`

---

## Decision / Outcome

**Decision**:

- `S0F-3I` opens the next bounded follow-up because the repo now has a classification problem, not a missing-document problem: important contracts exist across logs, code, scripts, runbooks, and registry records, but there is no single taxonomy that separates contract family from system level.
- v1 fixes one two-dimensional management model:
  - contract families answer `what kind of contract is this?`
  - `S0-S6` levels answer `which system level or affected surface does it belong to?`
- v1 therefore defines seven contract families for repo-wide use:
  - `DOM`: domain contracts
  - `PRO`: projection contracts
  - `INT`: interface contracts
  - `OPS`: operational contracts
  - `SEC`: security and tenant contracts
  - `EVD`: evidence and gate contracts
  - `DOC`: documentation and governance contracts
- `GC-*` is narrowed by this model: it no longer means `all contracts in the repo`; it now means only the current registry-admitted governance contract subset that is worth concentrating as a current active rule surface.
- v1 also now answers the first placement question directly: the seven families are not expected to collapse into one folder, so the repo needs one explicit map of current primary directories, mixed supporting surfaces, and reorganization thresholds instead of one abstract reminder to `keep SoT first`.

**Default choices (phase defaults / v1)** (optional, but recommended):

- Do not force all contracts into one unified folder; primary SoT placement comes before any central index or registry view.
- A contract may be code-first, doc-first, or mixed, but each contract must still name one primary SoT.
- `S0-S6` should remain the system-level map; they are not the first-level contract taxonomy.
- Security and tenant work should pre-split under `SEC` from the start rather than being thrown into one broad governance bucket and re-sorted later.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block because `S0F-3I` fixes a repo-wide taxonomy decision that later contract inventory, governance views, and registry narrowing work may reference directly.
- `PR Summary Inputs` remains an automation-facing source block; the taxonomy decision should not be reconstructed from narrative comments scattered across unrelated logs.

**PR summary bullets**:

- Separate contract family from system level so the repo no longer confuses `what kind of contract this is` with `which part of the system it affects`.
- Fix seven contract families and one placement rule that lets primary SoT stay distributed instead of forcing all contracts into one markdown registry.
- Narrow `GC-*` to the registry-admitted current governance subset and keep future security and tenant work under `SEC` first.

**PR checklist source**:

- Default source: reuse this log's execution checklist for any future taxonomy-publish PR.

**PR links**:

- Log: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`
- Taxonomy input surface: `docs/logs/INDEX.md`

## Definitions (optional)

- **contract family**: the kind of rule being managed, such as domain semantics, projection semantics, operator behavior, or documentation governance
- **system level**: the repo level or affected surface, currently represented by `S0-S6`
- **primary SoT**: the one location that is authoritative when the contract meaning and all other copies disagree
- **registry-admitted contract**: a contract that has been promoted into the current governance registry because it is current, independent, reusable, and worth concentrating as a stable rule surface
- **code-first contract**: a contract whose primary SoT lives mainly in code, schema, migrations, and tests
- **doc-first contract**: a contract whose primary SoT lives mainly in logs, runbooks, templates, governance records, or other written control surfaces

## Constraints

- Do not collapse all contracts into one `GC` bucket.
- Do not force every important contract into one physical folder when its real SoT lives in code or scripts.
- Do not treat `S0-S6` as a replacement for contract family.
- Do not assume a one-to-one mapping between contract family and system level.
- Do not use markdown presence alone to decide that a contract is doc-first; primary SoT must be named explicitly.

## Scope

- `P0`: define the seven-family contract taxonomy and the narrowed meaning of `GC-*`
- `P1`: define SoT-first placement rules for each family
- `P2`: define how contract family and `S0-S6` levels relate without collapsing into one axis
- `P3`: pre-allocate the future security and tenant taxonomy boundary so later auth/tenant work opens under `SEC` instead of a generic governance bucket
- `P4`: publish the first contract inventory/index draft using `family + primary SoT + affected levels + registry status` so the taxonomy is exercised on real repo surfaces instead of remaining template-only
- `P5`: publish one current family placement map and one consolidation threshold so readers can answer `where do these contracts live today?` without forcing a fake unified folder model

## Success Criteria (DoD)

- One reader can identify whether an important repo rule belongs to `DOM`, `PRO`, `INT`, `OPS`, `SEC`, `EVD`, or `DOC` without first debating folder placement.
- One reader can tell whether `GC-*` means the whole contract universe or only the current admitted governance subset.
- The repo has one explicit answer for where each family normally keeps its primary SoT.
- The repo has one explicit answer that `S0-S6` is an affected-level map, not a first-level contract-family taxonomy.
- Future auth, tenant, and policy work can open under a pre-split `SEC` family instead of being mixed back into a broad undefined governance bucket.
- One reader can answer where each family currently lives, which directories act as primary SoT versus supporting surfaces, and whether later cleanup should mean `stronger indexing` or `real physical relocation`.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the seven-family taxonomy and placement rules are explicit enough that new slices stop debating `is this a GC or not` before they can even describe the rule
  - the `S0-S6` relation is fixed as a second dimension rather than a competing taxonomy

## P0 (Contract | v1)

### P0-C1-S1 (Seven-family taxonomy baseline | v1)

- `DOM`:
  - owns business truth, aggregate boundaries, write-path invariants, state transitions, and domain semantics
- `PRO`:
  - owns projection/read-model semantics, outbox or asynchronous consistency rules, projection rebuild/backfill behavior, and projection-owned failure semantics
- `INT`:
  - owns API, CLI, event payload, artifact shape, exit-code, and adapter I/O contracts
- `OPS`:
  - owns deploy, verify, rollback, release, operator path, and runtime gate contracts
- `SEC`:
  - owns identity, tenant boundary, authorization, auditability, and sensitive-data handling contracts
- `EVD`:
  - owns drills, evidence JSON, hard-gate shape, PASS/FAIL taxonomy, and machine-checkable verification contracts
- `DOC`:
  - owns source-log template rules, runbook authoring rules, documentation governance, GitHub lifecycle documentation rules, and other doc-first control-plane contracts

### P0-C1-S2 (GC narrowing rule | v1)

- `GC-*` should now be read narrowly as `registry-admitted current governance contract`.
- `GC-*` is no longer the umbrella name for every important contract in the repo.
- A contract may be important, current, and heavily used without being a `GC-*` record if its primary SoT belongs to `DOM`, `PRO`, `INT`, `OPS`, `SEC`, `EVD`, or `DOC` outside the current governance registry.

### P0-C1-S3 (Evidence contract | v1)

- Any later contract inventory or registry admission work should record at least these fields per contract:
  - `contract_family`
  - `primary_sot`
  - `affected_levels`
  - `enforcement_surface`
  - `registry_status`

## P1 (Placement model | v1)

### P1-C1-S1 (Primary SoT placement by family | v1)

- `DOM` primary SoT should normally live in code, schema, migrations, and domain tests; docs/logs only explain or trace changes.
- `PRO` primary SoT should normally live in projection code, migration/runtime behavior, projection tests, and projection-owned drills; docs/logs explain rollout and family shape.
- `INT` primary SoT should normally live in API/CLI/event/interface code plus verification artifacts and tests; docs explain invariants and consumer expectations.
- `OPS` primary SoT should normally live in runbooks, operator scripts, workflow entrypoints, and bounded release/runtime docs.
- `SEC` primary SoT is often mixed but must still name one lead surface per rule: code/policy/tests for enforceable security behavior, plus docs/runbooks for governed operator use.
- `EVD` primary SoT should normally live in evidence schemas, gate scripts, runbooks, CI workflows, and retained artifacts.
- `DOC` primary SoT should normally live in templates, governance docs, runbooks, or documentation-specific automation surfaces.

### P1-C1-S2 (Distributed placement rule | v1)

- The seven families do not need to live in one unified physical folder.
- The repo should prefer `primary SoT first, cross-link second`:
  - code-first families stay close to code and tests
  - doc-first families stay close to docs, templates, runbooks, and governance records
  - a later central taxonomy index may point to them, but must not replace their real SoT
- Under this rule, the current governance registry under `docs/governance/` remains only one concentrated current-state surface, not the universal storage location for every contract family.

## P2 (Family versus level relation | v1)

### P2-C1-S1 (S0-S6 relation rule | v1)

- `S0-S6` remains the system-level or affected-surface map:
  - `S0`: knowledge system
  - `S1`: SoT
  - `S2`: projection
  - `S3`: observability
  - `S4`: ops runtime
  - `S5`: security and governance
  - `S6`: evidence and drills
- Contract family and system level are therefore two different axes:
  - family answers `what kind of contract is this?`
  - level answers `which surface or system layer does it affect?`

### P2-C1-S2 (Typical affinities, not one-to-one mapping | v1)

- `DOC` often lands in `S0`, but documentation governance may still affect `S4`, `S5`, or `S6` workflows.
- `DOM` often lands in `S1`.
- `PRO` often lands in `S2`.
- `OPS` often lands in `S4`.
- `SEC` often lands in `S5`.
- `EVD` often lands in `S6`.
- `INT` commonly spans more than one level at once, especially `S1`, `S2`, `S4`, and `S6`.
- These affinities are useful defaults, but they are not the taxonomy itself.

## P3 (Security and tenant pre-allocation | v1)

### P3-C1-S1 (SEC split baseline | v1)

- Future permission, auth, tenant, and related security work should open under `SEC` first rather than under one broad undefined governance bucket.
- The first controlled `SEC` subfamilies should be:
  - `SEC-IDN`: identity and authentication context
  - `SEC-TEN`: tenant boundary and data isolation
  - `SEC-AUT`: authorization and policy decision
  - `SEC-AUD`: auditability and traceable access decisions
  - `SEC-DAT`: sensitive data handling, backup, sanitization, and related protection surfaces
- Later registry admission may still concentrate selected `SEC` rules into a current active governance registry, but the family taxonomy should exist before any such admission decision.

## P4 (First inventory/index draft | v1)

### P4-C1-S1 (Cross-family contract inventory draft | v1)

- The first applied inventory should not widen `docs/governance/INDEX.md` into a universal contract ledger.
- Instead, the repo now keeps one separate reader-facing inventory draft at:
  - `docs/governance/views/view-contract-family-inventory-v1.md`
- The draft uses one common row shape across representative current surfaces:
  - `contract family`
  - `representative contract or surface`
  - `primary SoT`
  - `affected levels`
  - `registry status`
- This makes `S0F-3I` a real applied taxonomy pass rather than a purely conceptual naming slice.

### P4-C1-S2 (Registry boundary clarified against inventory | v1)

- `docs/governance/INDEX.md` remains the front door for current registry-admitted governance contracts only.
- The new cross-family inventory view is the right place for repo-wide contract scanning when a reader needs to compare `DOM/PRO/INT/OPS/SEC/EVD/DOC` without pretending they all live under `GC-*`.
- This preserves the `GC-*` registry as a narrow current-state surface while still giving the repo one practical inventory draft.

## P5 (Current placement map and consolidation threshold | v1)

### P5-C1-S1 (Current family placement map published | v1)

- The repo now keeps one separate placement scan at:
  - `docs/governance/views/view-contract-family-placement-map-v1.md`
- That view answers the concrete follow-up left open by `P1` and `P4`:
  - which directories currently hold the strongest SoT for each family
  - which families are already concentrated enough
  - which families remain mixed by design because their SoT lives in code, workflows, scripts, tests, and retained artifacts together

### P5-C1-S2 (Consolidation threshold fixed | v1)

- A later cleanup slice should not create one universal `contracts/` folder for all seven families.
- Reorganization is justified only when at least one of these is true:
  - readers repeatedly fail to locate the primary SoT for the same family
  - one family grows enough parallel front doors that a stable family index or directory hub would reduce ambiguity
  - current placement causes real duplicate rule ownership rather than mere cross-link cost
- Under that rule:
  - `DOC`, `OPS`, and `EVD` currently need stronger indexing more than physical relocation
  - `PRO`, `INT`, and `SEC` still need mixed placement because code, scripts, workflows, tests, and docs co-own the current enforceable meaning
  - `DOM` remains primarily code-first under backend module, migration, and test surfaces, so forcing it into a docs-first folder now would weaken SoT rather than clarify it

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `<ID>/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `<ID>/P0-P3: <log title>`
  - discontinuous phases: `<ID>/P0+P3: <log title>`
  - mixed discontinuous + consecutive phases: `<ID>/P0+P3-P4: <log title>`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `<ID>/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- For logs tied to a specific scope/index, prefer making P* code and documentation changes on a working branch with the same prefix.
- If a single PR touches multiple scopes/indexes, prefer splitting it into multiple PRs so each PR stays focused on one scope/index and its corresponding branch for easier aggregation and traceability.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, whether it is contract work, implementation, or drills/evidence, try to `commit/push` promptly on the matching scope branch.
- The normal rhythm is: accumulate commits on the matching scope branch at `P*-C*-S*` granularity, then periodically open a PR from that branch into `main` for human review and merge.

## Plan (draft)

### P1 (Placement model)

- P1-C1-S1: define the primary SoT placement rule for each family
- P1-C1-S2: define the distributed placement rule versus central indexing

### P2 (Family versus level relation)

- P2-C1-S1: define `S0-S6` as system levels rather than contract families
- P2-C1-S2: define family affinities without allowing one-to-one collapse

### P3 (Security and tenant pre-allocation)

- P3-C1-S1: define the first `SEC` subfamilies before future permission and tenant work opens

### P4 (First inventory/index draft)

- P4-C1-S1: publish one cross-family contract inventory draft using the new taxonomy row shape
- P4-C1-S2: clarify the boundary between the cross-family inventory draft and the narrow `GC-*` governance front door

### P5 (Current placement map and consolidation threshold)

- P5-C1-S1: publish one current family placement map with primary directories, supporting surfaces, and concentration status
- P5-C1-S2: fix the threshold for when later slices should build stronger family hubs versus keeping distributed SoT placement

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: seven-family taxonomy baseline fixed
- [x] `P0-C1-S2`: `GC-*` narrowing rule fixed
- [x] `P0-C1-S3`: future inventory evidence fields fixed

### P1 (Placement model)

- [x] `P1-C1-S1`: primary SoT placement rule fixed by family
- [x] `P1-C1-S2`: distributed placement rule fixed

### P2 (Family versus level relation)

- [x] `P2-C1-S1`: `S0-S6` relation rule fixed as system levels rather than contract families
- [x] `P2-C1-S2`: family affinities fixed without one-to-one collapse

### P3 (Security and tenant pre-allocation)

- [x] `P3-C1-S1`: `SEC` split baseline fixed for future auth, tenant, and policy work

### P4 (First inventory/index draft)

- [x] `P4-C1-S1`: cross-family contract inventory draft published
- [x] `P4-C1-S2`: governance front-door versus cross-family inventory boundary clarified

### P5 (Current placement map and consolidation threshold)

- [x] `P5-C1-S1`: current family placement map published
- [x] `P5-C1-S2`: consolidation threshold fixed against fake one-folder cleanup pressure

## Current Status (recommended)

- `S0F-3I` now fixes the missing taxonomy boundary: the repo can talk about seven contract families without pretending they all belong in one registry or one folder.
- `S0-S6` is now explicitly treated as the affected-level map rather than as the first-level contract taxonomy.
- Future permission, tenant, and policy work should now open under `SEC` first, while `GC-*` should remain the narrower registry-admitted governance subset rather than the umbrella name for all contracts.
- `P4` is now complete as a new phase, not another cycle on `P0-P3`: the repo now has one first applied inventory draft at `docs/governance/views/view-contract-family-inventory-v1.md`, so taxonomy, placement, and level rules now read against real representative surfaces instead of staying abstract.
- `P5` is now complete as the first concrete placement answer: the repo now has one current family placement map at `docs/governance/views/view-contract-family-placement-map-v1.md`, and later cleanup can now distinguish `needs better indexing` from `needs real relocation` instead of treating every family as if it should end up in one folder.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.

### P0-C1-S1 through P3-C1-S1 (contract taxonomy, placement, and level relation fixed | 2026-04-08)

- headSha: `0069612b6e3896bdedd9f2f99209c4f23caed9f7`
- artifacts: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- artifacts: `docs/logs/INDEX.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- artifacts: `docs/logs/log-S0F-4B-source-log-compatibility-and-weak-structure-export-discipline.md`
- expected:
  - the repo should stop equating contract family with `S0-S6` level and should stop using `GC-*` as the name for the entire contract universe
- observed:
  - seven contract families are now explicit, SoT-first placement is fixed, `S0-S6` is clarified as the level map, and future security or tenant work now has a pre-split `SEC` family boundary

### P4-C1-S1 through P4-C1-S2 (first contract inventory/index draft published and registry boundary clarified | 2026-04-08)

- headSha: `a38253d97970c5b1a775c634f0089647c6d69281`
- artifacts: `docs/governance/views/view-contract-family-inventory-v1.md`
- artifacts: `docs/governance/INDEX.md`
- artifacts: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- expected:
  - the taxonomy should be exercised on one real cross-family inventory surface without collapsing the narrow `GC-*` front door into a universal contract ledger
- observed:
  - the repo now has one separate cross-family inventory draft, while `docs/governance/INDEX.md` stays the current registry-admitted governance front door only

### P5-C1-S1 through P5-C1-S2 (current family placement map published and consolidation threshold fixed | 2026-04-08)

- headSha: `5ee05672687a2229d85b65299522bf6d290b97a9`
- artifacts: `docs/governance/views/view-contract-family-placement-map-v1.md`
- artifacts: `docs/logs/log-S0F-3I-governance-contract-taxonomy-and-placement-model.md`
- artifacts: `docs/logs/log-S0F-docs-management-v6.md`
- expected:
  - one reader should be able to answer where each contract family currently lives and whether later cleanup should mean better indexing or actual relocation
- observed:
  - the repo now has one explicit family placement scan, and the cleanup threshold now separates `distributed SoT by design` from `placement is actually too fragmented`

## Recent changes (for traceability, optional)

- 2026-04-08: opened `S0F-3I` to split contract family from system level, narrow `GC-*` to the admitted governance subset, and pre-allocate the future security and tenant contract boundary under `SEC`.
- 2026-04-08: completed `P4` by publishing the first cross-family contract inventory draft and by clarifying that `docs/governance/INDEX.md` remains the narrow `GC-*` registry front door rather than the universal contract index.
- 2026-04-08: completed `P5` by publishing the first current family placement map and by fixing the threshold for when later slices should build family hubs versus keeping distributed primary SoT placement.