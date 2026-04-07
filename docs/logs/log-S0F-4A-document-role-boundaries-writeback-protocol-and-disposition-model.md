# log-S0F-4A (Phase 4A: document role boundaries, write-back protocol, and disposition model)

---

**id**: `S0F-4A`
**kind**: `log`
**title**: `document role boundaries, write-back protocol, and disposition model v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Governance, Workflow, Contract, Runbook, Views, Cleanup, Naming, Lifecycle, epic/s0, sub/4a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_1**: `docs/logs/log-S0F-3B-governance-contract-registry-and-naming-model.md`
  **reference_log_2**: `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  **reference_log_3**: `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
  **reference_log_4**: `docs/governance/INDEX.md`
  **reference_log_5**: `docs/governance/views/view-contract-sweep-workflow-v1.md`
**issue_keyword**: `governance`
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
**created**: `2026-04-07`
**updated**: `2026-04-07`

---

## Decision / Outcome

**Decision**:

- `S0F-4A` opens the next `S0F` follow-up slice for document role boundaries after `S0F-3F` and `S0F-3G` exposed the recurring mixed-role problem directly.
- This slice exists because current governance cleanup is now blocked less by missing support-only folders and more by logs that still carry more than one live responsibility at once: current-rule concentration, operator procedure, family summary, parent-entry navigation, and historical placement all remain partially fused in some retained files.
- v1 therefore fixes three things before another broad retroactive rewrite is attempted:
  - one stable six-outlet document-role model
  - one fixed write-back protocol that later slices can replay mechanically at close-out
  - one naming and disposition baseline that separates `what the file is for` from `where the file currently lives`

**Default choices (phase defaults / v1)**:

- Do not treat `archive` as a new top-level document role yet.
- Treat `legacy`, `support-only`, `deprecated`, `superseded`, `retired`, and `deferred cleanup` as disposition states, not peer document types alongside `contract`, `runbook`, `view`, or `log`.
- Keep current rule, current procedure, current reader entrypoint, and current family-summary reading as separate responsibilities even when one slice originally introduced all of them.
- Prefer a fixed close-out export order over ad hoc hand judgment when deciding what leaves a structured log.
- Do not retroactively rewrite the whole repo inside this slice; first define the model, then let later slices apply it family by family.

## Problem Statement

- The repo now has stable current contracts, stable runbooks, support-only relocation models, and bounded family views.
- The remaining ambiguity is not primarily semantic anymore.
- The remaining ambiguity is documentary:
  - when a slice stabilizes a current rule, what must leave the log and move into a contract?
  - when a procedure becomes stable, what must leave the log and move into a runbook?
  - when a family result needs a reader-facing summary, when does that belong in a view rather than in a long sweep ledger?
  - who owns `INDEX.md` mutations and file-placement state such as `support-only`, `keep legacy`, or `deferred cleanup`?
- Without one explicit answer, later slices either overstuff logs or rely on cleanup rounds to infer document roles after the fact.

## Scope

- `P0`: open `S0F-4A`, wire it into the `S0F` spine, and fix the problem boundary
- `P1`: define the six-outlet document-role model
- `P2`: define naming baseline by outlet, including `INDEX.md` and views
- `P3`: define the fixed close-out write-back protocol for future slices
- `P4`: define disposition and placement rules, including future external-storage planning boundary
- `P5`: later pilot one or two bounded families against this model rather than attempting repo-wide retroactive rewrite immediately

## Current Status

- `S0F-4A` is now opened as the next `S0F` follow-up slice for document role boundaries after the `3F` semantic lane and `3G` cleanup lane already proved that mixed-role logs are now the dominant governance-doc friction point.
- `P0` is now complete: the slice is opened and the problem is fixed as role-boundary and write-back protocol work, not as another semantic family sweep or another cleanup round.
- `P1` is now complete: the repo now has one explicit six-outlet model for `log`, `contract`, `runbook`, `view`, `index/front-door`, and `disposition/placement`.
- `P2` is now complete: naming baseline is now fixed per outlet, including when `INDEX.md` is enough on its own, when views need stable family-oriented names, and why disposition should not invent a second naming universe.
- `P3` is now complete: one fixed close-out write-back protocol now exists so future slices can export stable rule/procedure/summary material out of logs mechanically instead of improvising the order each time.
- `P4` is now complete: disposition and placement are now fixed as a separate responsibility plane, and future AWS or external object storage can be planned as an evidence/archive substrate without turning current contracts, runbooks, or views into remote-only surfaces.
- The immediate next follow-up is not repo-wide retroactive surgery; it is to apply this model on one or two bounded families first so the protocol can prove itself against real mixed-role and cleaner positive-control cases.

## P1 Six-Outlet Document Role Model

### `log`

- primary job:
  - retain slice-local decision, scope, plan, checklist, evidence, and change narrative
- should keep:
  - why the work happened
  - execution boundary
  - retained artifacts and traceability
- should not remain the long-term primary home for:
  - stable current rule text
  - stable operator procedure
  - current front-door navigation

### `contract`

- primary job:
  - define current rule, scope, enforcement surface, and violation semantics
- should keep:
  - stable current semantic meaning
  - minimum traceability and successor or legacy notes
- should not expand into:
  - operator steps
  - whole family chronology

### `runbook`

- primary job:
  - define stable operator-facing procedure, inputs, outputs, and troubleshooting path
- should keep:
  - how to run the surface now
  - first-response handling and evidence inspection path
- should not redefine:
  - current semantic rule ownership

### `view`

- primary job:
  - concentrate family-level or reader-level interpretation so a human can understand a bounded result without replaying the whole ledger
- should keep:
  - family summary
  - current vs support-only vs legacy reading
  - bounded no-op or admission package summary
- should not become:
  - a second current rule surface

### `index/front-door`

- primary job:
  - expose current entrypoints and current reading boundaries at directory or governance-front-door level
- should keep:
  - current navigation only
  - local directory-entry rules such as `support-only/INDEX.md`
- should not absorb:
  - complete history ledger

### `disposition/placement`

- primary job:
  - decide the current file state and physical placement for already-adjudicated documents
- owns states such as:
  - `keep current`
  - `keep legacy`
  - `support-only`
  - `deprecated`
  - `superseded`
  - `retired`
  - `defer cleanup`
- should stay separate from naming of the role itself:
  - a `log` can be `support-only`
  - a `contract` can be `deprecated`
  - a `view` can be `support-only`

## P2 Naming Baseline

### `log` naming

- keep the existing slice-first model:
  - `log-<slice-id>-<summary>.md`
- rationale:
  - logs are chronology and ownership ledgers first
  - their identity should remain slice-scoped

### `contract` naming

- keep the existing governance-record model:
  - `GC-<AREA>-<NNNN>-<summary>.md`
- rationale:
  - contracts are registry items, not slice byproducts

### `runbook` naming

- keep `run-<stable-surface>-<summary>.md` as the long-term preferred model
- transitional rule:
  - inherited slice-style runbook names may remain when history already depends on them
  - new runbooks should prefer the stable governed surface or procedure over a transient slice chronology when the two diverge

### `view` naming

- baseline model:
  - `view-<reading-surface>-v<version>.md`
- where `<reading-surface>` should usually be one of:
  - bounded family name
  - admission package name
  - lineage split package name
  - reusable workflow reading surface
- rule:
  - use `support-only/` placement for closed-lane views rather than inventing a second filename prefix for historical status

### `INDEX.md` naming

- no bespoke variant is needed by default
- use plain `INDEX.md` for a current front-door or local directory entrypoint
- rationale:
  - entrypoint function is expressed by placement, not by filename decoration

### disposition naming

- do not create a parallel filename system such as `archive-*` or `retired-*` by default
- express disposition through:
  - directory placement
  - frontmatter or body status fields
  - cleanup manifests and ledgers
- rationale:
  - role identity and physical state should not collapse into one unstable filename convention

## P3 Fixed Close-Out Write-Back Protocol

### Mandatory Questions At Slice Close

- did this slice define or materially change one current rule?
- did this slice define one stable operator procedure?
- did this slice produce one reusable family or reader summary?
- did this slice change any front-door or local entrypoint reading?
- did this slice change any file disposition or placement state?
- what remains in the log after those exports because it is still slice-local evidence, traceability, or bridge context only?

### Required Write Order

1. update or create `contract` if stable current rule changed
2. update or create `runbook` if stable procedure changed
3. update `index/front-door` if current navigation changed
4. update or create `view` if one bounded family summary is now worth retaining
5. rewrite the `log` so it keeps only slice-local ledger, evidence, and bridge notes for the exported material
6. record `disposition/placement` change only after the other outlets are stable enough that cleanup does not guess at meaning

### Stop Rule

- do not export content mechanically when the supposed target outlet still lacks a stable identity
- in that case the log remains the temporary home, and the missing target outlet should be fixed first by a later bounded slice

## P4 Disposition Model And External Storage Boundary

### Disposition Rules

- `keep current`:
  - file remains in the current root because readers still need it as a live surface
- `keep legacy`:
  - file remains in place because old IDs, redirects, or lineage still depend on the path
- `support-only`:
  - file may move into a `support-only/` sublocation once discoverability and rewrite safety are defended
- `defer cleanup`:
  - file stays in place because role separation is still incomplete or reader-facing dependency survives

### Physical Placement Rule

- placement follows role first, then disposition:
  - current contracts stay under `docs/governance/contracts/`
  - current views stay under `docs/governance/views/`
  - stable runbooks stay under `docs/runbook/`
  - logs stay under `docs/logs/`
  - only then may support-only relocation move a file into a role-local `support-only/` sublocation

### AWS / External Object Storage Planning Baseline

- do not plan to move current contracts, current runbooks, current views, or parent logs out of the repo
- future external storage should target:
  - heavy retained evidence bundles
  - large historical artifacts
  - reproducible exported drill outputs
- keep in-repo control surfaces for any later externalization:
  - one retained manifest
  - one stable object key or URI rule
  - one local index or traceability note that points to the external evidence without making current reading depend on mutable bucket listing
- do not introduce a repo-wide `archive/` folder merely as a placeholder for future object storage

## Pilot Recommendation

- first pilot mixed-role case:
  - `S0F-1I`
  - rationale:
    - proves whether the write-back protocol can explain why one log still keeps bridge context after contracts and runbook exports already exist
- first pilot cleaner positive-control case:
  - bounded `WF` family around `S0E-7D` through `S0E-7G`
  - rationale:
    - current rule, support-only residue, and family-summary surfaces are already more clearly separated there than in `S0F-1I`

## Plan (draft)

### P0 (Slice opening)

- P0-C1-S1: create `S0F-4A` and wire it into the `S0F` parent spine
- P0-C1-S2: define the role-boundary problem explicitly rather than treating it as another cleanup-only issue

### P1 (Role model)

- P1-C1-S1: define the six-outlet document-role model
- P1-C1-S2: distinguish role identity from disposition state

### P2 (Naming baseline)

- P2-C1-S1: define outlet-specific naming baseline without reopening stable contract naming
- P2-C1-S2: define when plain `INDEX.md` is sufficient and when views need stable family-oriented names

### P3 (Write-back protocol)

- P3-C1-S1: define the mandatory close-out questions
- P3-C1-S2: define one fixed outlet update order

### P4 (Disposition and externalization)

- P4-C1-S1: define placement and disposition rules separately from role naming
- P4-C1-S2: define future AWS or external object storage as an evidence/archive substrate rather than as a replacement for current docs

### P5 (Later pilots)

- P5-C1-S1: test the model against one mixed-role retained log and one cleaner positive-control family before any broader retroactive rewrite

## Execution Checklist (unchecked)

### P0 (Slice opening)

- [x] `P0-C1-S1`: `S0F-4A` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: role-boundary problem fixed as its own slice rather than mixed back into `3F` or `3G`

### P1 (Role model)

- [x] `P1-C1-S1`: six-outlet document-role model defined
- [x] `P1-C1-S2`: role identity separated from disposition state

### P2 (Naming baseline)

- [x] `P2-C1-S1`: outlet-specific naming baseline defined
- [x] `P2-C1-S2`: `INDEX.md` and view naming baseline defined

### P3 (Write-back protocol)

- [x] `P3-C1-S1`: mandatory close-out questions defined
- [x] `P3-C1-S2`: fixed outlet update order defined

### P4 (Disposition and externalization)

- [x] `P4-C1-S1`: disposition and placement rules defined separately from role naming
- [x] `P4-C1-S2`: future external object storage boundary defined as evidence/archive substrate only

### P5 (Later pilots)

- [ ] `P5-C1-S1`: model tested against one mixed-role retained log and one cleaner positive-control family

## Evidence (reserved)

### P0-C1-S1 through P4-C1-S2 (role-boundary model, naming baseline, write-back protocol, and disposition rules fixed | 2026-04-07)

- headSha: `<TBD-after-s0f-4a-commit>`
- artifacts:
  - `docs/logs/log-S0F-4A-document-role-boundaries-writeback-protocol-and-disposition-model.md`
  - `docs/logs/log-S0F-docs-management-v6.md`
  - `docs/logs/log-S0F-3F-governance-contract-sweep-workflow.md`
  - `docs/logs/log-S0F-3G-governance-cleanup-staging-and-phased-file-cleanup.md`
- expected:
  - the repo should gain one explicit model for how stable rule, procedure, summary, index, and placement responsibilities leave structured logs over time
- observed:
  - `S0F-4A` now fixes six outlet roles, one fixed close-out protocol, one naming baseline, and one placement plus externalization boundary without forcing immediate retroactive rewrite across the whole repo