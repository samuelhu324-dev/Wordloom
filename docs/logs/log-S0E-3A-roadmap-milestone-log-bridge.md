# log-S0E-3A (Phase 3A: Roadmap Milestone and Log Bridge Contract)

---

**id**: `S0E-3A`
**kind**: `log`
**title**: `roadmap milestone and log bridge contract v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Roadmap, Milestone, Automation, epic/s0, sub/0e3a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/314`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/292`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-2C-batch-issue-creation-and-backfill-tooling.md`
  **reference_log_1**: `docs/logs/log-S0D-6A-structured-roadmap-and-demo.md`
  **reference_log_2**: `docs/roadmap/road-template-structured-roadmap.md`
  **reference_log_3**: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md`
**issue_keyword**: `contract`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md`
**roadmap_milestone**: ``
**roadmap_phase**: ``
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-29`
**updated**: `2026-04-02`

---

## Decision / Outcome

**Decision**:

- `S0E-3A` defines a bridge contract between roadmap milestones and child logs so milestone ownership stops living inside prose-only references.
- v1 makes milestone-to-log mapping explicit at the `M*-P* -> child log` level and requires logs to carry their own roadmap bridge fields.
- The roadmap bridge stays child-log-first: parent/spine logs may navigate to a roadmap, but the canonical roadmap ledger points to child logs, not parent prose.

**Default choices (phase defaults / v1)**:

- Every child log that belongs to a roadmap bridge must declare `roadmap_path`, `roadmap_milestone`, and `roadmap_phase`.
- If one child log legitimately maps to multiple roadmap slots or both a branch road and its mirrored parent slot, the log should keep one primary `roadmap_*` anchor and list the full exact-slot set in `roadmap_bridge_refs`.
- Parent/spine logs may repeat `roadmap_path` for navigation, but should normally leave `roadmap_phase` blank unless a parent-level contract truly owns that exact milestone-phase slot.
- Roadmap files must expose a per-milestone bridge ledger near the top of each milestone section; `Evidence Pointers` and `Recent Changes` are supporting narrative only.
- Milestone automation must stay fail-closed until roadmap/log bridge fields are explicit and machine-readable.

## Definitions (optional)

- **Roadmap bridge**: the explicit structural mapping from a roadmap milestone-phase such as `M3-P2` to one or more child logs.
- **Child-log-first bridge**: the rule that canonical roadmap mapping points to child logs rather than parent/spine summaries.
- **Bridge ledger**: the dedicated roadmap section that lists `M*-P*` slots and their corresponding child logs.
- **Narrative pointer**: a prose reference such as `Evidence Pointers` or `Recent Changes`; useful for humans, but not the canonical machine-readable bridge.

## Constraints

- Do not infer roadmap ownership from scattered prose references.
- Do not treat `Evidence Pointers` as the only roadmap-to-log mapping layer.
- Do not use parent/spine logs as the primary bridge rows when child logs already exist.
- Do not automate milestone assignment from roadmap prose before the bridge fields are present in templates and migrated into real logs.

## Scope

- `P0`: contract for roadmap bridge fields, ledger structure, and child-log-first ownership
- `P1`: template updates for roadmap files and parent/phase logs
- `P2`: migrate one real roadmap path such as `road-S1` / `road-S1-1` to the bridge ledger format
- `P3`: verify that milestone extraction can read the bridge mechanically without relying on prose scanning

## Current Status

- `P0` is complete: the bridge ownership, field contract, and fail-closed milestone rule are now fixed in this log.
- `P1` is complete: the parent-log template, phase-log template, and roadmap template now expose the new bridge structure.
- `P2` is complete: `road-S1` and `road-S1-1` now record explicit child-log-first bridge ledgers plus parent/branch alignment.
- `P3` is complete: mechanical extraction now reads the bridge ledgers and parent-alignment blocks directly, without scanning prose sections.
- `P3-C2` is complete: the historical child logs used by the sample pair now carry primary `roadmap_*` anchors plus exact-slot `roadmap_bridge_refs`, so the dry-run aligns all mapped rows without warning fallback.

## Success Criteria (DoD)

- Log templates expose `roadmap_path`, `roadmap_milestone`, and `roadmap_phase` as first-class bridge fields.
- Multi-slot child logs can express their full exact-slot footprint without forcing prose fallback or one-log-per-slot duplication.
- The roadmap template exposes a dedicated `Bridge Ledger` block for every milestone.
- At least one real roadmap path demonstrates child-log-first bridge mapping without hiding the mapping in prose.
- Milestone automation can safely say `no bridge -> no milestone` instead of guessing.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the roadmap bridge fields and ledger structure are fixed in templates and exercised on at least one real roadmap path;
  - milestone extraction no longer depends on `Evidence Pointers` or `Recent Changes` as its primary mapping source.

## P0 (Contract | v1)

### P0-C1-S1 (Roadmap bridge ownership | v1)

- Canonical roadmap bridge rows point to child logs only.
- Parent/spine logs remain useful navigation hubs, but they are not the primary roadmap milestone ledger.
- A log may only claim roadmap ownership mechanically when `roadmap_path`, `roadmap_milestone`, and `roadmap_phase` are explicit.

### P0-C1-S2 (Template field contract | v1)

- Phase and parent log templates expose roadmap bridge fields.
- Roadmap templates expose a `Bridge Ledger (child logs only)` block inside each milestone section.
- Mainline and branch roadmaps may use different templates, but both must preserve the same child-log-first bridge rule.
- Missing bridge fields are treated as `unmapped`, not inferred from nearby wording.

### P0-C1-S3 (Evidence contract | v1)

- Evidence for this slice should prove:
  - the templates carry the bridge fields;
  - the roadmap template carries a milestone ledger block;
  - at least one migrated roadmap can be read mechanically without prose-only fallback.

## P3 (Mechanical verification | v1)

### P3-C1-S1 (Extraction dry-run | v1)

- Mechanical extraction must read only the dedicated bridge structures:
  - `Bridge Ledger (child logs only)` blocks;
  - `Parent Contribution Ledger` and `Parent alignment` blocks.
- `Evidence Pointers`, `Recent Changes`, and narrative ownership paragraphs are intentionally ignored during extraction.

### P3-C1-S2 (Fallback rules | v1)

- If a roadmap slot is `unmapped`, automation must leave milestone assignment empty.
- If a child log is missing `roadmap_path`, `roadmap_milestone`, or `roadmap_phase`, the roadmap ledger remains the canonical source and the extractor should emit a warning instead of guessing from prose.
- If a branch road declares parent alignment that the mainline ledger does not mirror, the extractor should emit a reconciliation result.

### P3-C1-S3 (Sample artifact contract | v1)

- `P3` should leave one sample manifest and one sample plan artifact so future issue or milestone automation can reuse the same dry-run boundary.

### P3-C2-S1 (Exact-slot child-log refs | v1)

- `roadmap_path`, `roadmap_milestone`, and `roadmap_phase` remain the primary anchor fields on each child log.
- When one child log belongs to multiple exact roadmap slots, the log must list the full machine-readable slot set in `roadmap_bridge_refs` using `roadmap_path#M*-P*` entries.
- Extraction should treat `roadmap_bridge_refs` as the authoritative exact-slot check for multi-slot logs, while the primary `roadmap_*` fields remain the default human-facing anchor.

### P3-C2-S2 (Historical child-log backfill | v1)

- The first migrated roadmap pair should backfill `roadmap_*` metadata into all historical child logs referenced by the sample manifest.
- Once the sample pair is backfilled, the dry-run should collapse warning rows to `aligned` while keeping explicitly blank roadmap slots as `unmapped`.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-3A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).

**Branch convention**:

- `S0E-3A` work should normally stay on an `S0E-*` branch until the roadmap bridge contract needs a dedicated implementation branch.

**Commit discipline (recommended)**:

- Fix the bridge contract first, then update templates, then migrate a real roadmap path, then verify milestone extraction.

## Plan (draft)

### P1 (Template updates)

- P1-C1-S1: add roadmap bridge fields to parent/phase log templates
- P1-C1-S2: split roadmap templates into dedicated mainline and branch-road variants
- P1-C1-S3: keep a compatibility chooser at `road-template-structured-roadmap.md`
- P1-C1-S4: define mainline vs branch contribution rules so branch-road results can count back to the parent without polluting the parent body

### P2 (Roadmap migration)

- P2-C1-S1: migrate `road-S1` to the mainline bridge-ledger format
- P2-C1-S2: migrate `road-S1-1` to the branch-road bridge-ledger format
- P2-C1-S3: record parent/branch alignment explicitly so branch outputs still count toward the mainline

### P3 (Mechanical verification)

- P3-C1-S1: validate milestone extraction against migrated roadmap + child log fields
- P3-C1-S2: document fallback rules for unmapped logs and roadmap slots
- P3-C1-S3: emit one sample manifest + dry-run plan artifact for a mainline/branch roadmap pair
- P3-C2-S1: add exact-slot child-log refs for multi-slot roadmap ownership
- P3-C2-S2: backfill the sample pair's historical child logs and rerun extraction to eliminate warning fallback

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: roadmap bridge ownership fixed
- [x] `P0-C1-S2`: template field contract fixed
- [x] `P0-C1-S3`: roadmap bridge evidence contract fixed

### P1 (Template updates)

- [x] `P1-C1-S1`: roadmap bridge fields added to log templates
- [x] `P1-C1-S2`: roadmap templates split into mainline and branch-road variants
- [x] `P1-C1-S3`: compatibility chooser kept at `road-template-structured-roadmap.md`
- [x] `P1-C1-S4`: mainline vs branch contribution rules fixed in templates

### P2 (Roadmap migration)

- [x] `P2-C1-S1`: `road-S1` migrated to the mainline bridge-ledger format
- [x] `P2-C1-S2`: `road-S1-1` migrated to the branch-road bridge-ledger format
- [x] `P2-C1-S3`: parent/branch alignment recorded explicitly in both roadmaps

### P3 (Mechanical verification)

- [x] `P3-C1-S1`: milestone extraction validated against migrated roadmap ledgers without prose scanning
- [x] `P3-C1-S2`: fallback rules documented for unmapped slots and missing child-log bridge fields
- [x] `P3-C1-S3`: sample manifest and dry-run plan artifact emitted for `road-S1` + `road-S1-1`
- [x] `P3-C2-S1`: exact-slot child-log refs added for multi-slot roadmap ownership
- [x] `P3-C2-S2`: historical child logs used by the sample pair backfilled and revalidated to eliminate warning fallback

## Evidence

- `P0-C1-S1` / `P0-C1-S2`: this log now fixes the bridge contract around `roadmap_path`, `roadmap_milestone`, `roadmap_phase`, and child-log-first ownership.
- `P1-C1-S1`: `docs/logs/_template-log-phase-drills-evidence.md` now carries roadmap and PR bridge metadata for child logs.
- `P1-C1-S1`: `docs/logs/_template-log-parent-epic-spine.md` now carries roadmap and PR bridge metadata for parent/spine logs.
- `P1-C1-S2`: `docs/roadmap/road-template-main-roadmap.md` now defines the mainline-road structure and branch absorption rules.
- `P1-C1-S2`: `docs/roadmap/road-template-branch-roadmap.md` now defines the branch-road structure and parent contribution rules.
- `P1-C1-S3`: `docs/roadmap/road-template-structured-roadmap.md` remains as a compatibility chooser so older references do not break.
- `P2-C1-S1`: `docs/roadmap/road-S1-systems-platform-ops-roadmap-v5.md` now carries explicit mainline bridge ledgers and marks branch-origin child logs as `via road-S1-1`.
- `P2-C1-S2`: `docs/roadmap/road-S1-1-gov-role-minimal-ops-loop.md` now carries explicit branch bridge ledgers.
- `P2-C1-S3`: both roadmaps now record parent/branch alignment explicitly instead of hiding it in prose-only ownership paragraphs.
- `P3-C1-S1`: `scripts/issues/plan_roadmap_bridge_extraction.py` now extracts bridge rows mechanically from `road-S1` and `road-S1-1` without scanning prose sections.
- `P3-C2-S1`: the phase and parent log templates now expose optional `roadmap_bridge_refs` so one log can declare multiple exact roadmap slots without inventing prose fallback.
- `P3-C2-S2`: the historical child logs referenced by `road-S1` + `road-S1-1` now carry primary `roadmap_*` anchors plus exact-slot `roadmap_bridge_refs`.
- `P3-C2-S2`: `docs/issues/roadmap-bridge-S0E-3A-sample-plan.json` now confirms `40` bridge rows were extracted, `36` mapped rows are `aligned`, `4` remain explicitly `unmapped`, and warning fallback has dropped to `0`.
- `P3-C1-S3`: `docs/issues/roadmap-bridge-S0E-3A-sample-manifest.json` defines the reusable dry-run input boundary for one mainline/branch roadmap pair.

## Recent changes (for traceability, optional)

- 2026-03-29: opened `S0E-3A` to define a child-log-first roadmap/milestone bridge contract before any v2 milestone automation is attempted.
- 2026-03-29: completed `P0` by fixing bridge ownership, template field requirements, and fail-closed milestone semantics in the phase contract.
- 2026-03-29: completed `P1` by rolling roadmap bridge fields into the parent/phase log templates, splitting roadmap authoring into mainline and branch templates, and keeping a compatibility chooser for older references.
- 2026-03-29: completed `P2` by migrating both `road-S1` and `road-S1-1` to explicit bridge ledgers and writing the parent/branch alignment back into both files.
- 2026-03-29: completed `P3` by adding a manifest-driven roadmap bridge extraction dry-run, generating a sample plan for `road-S1` + `road-S1-1`, and documenting the fallback rule that keeps the roadmap ledger canonical when older child logs still lack `roadmap_*` fields.
- 2026-03-29: completed `P3-C2` by adding exact-slot `roadmap_bridge_refs`, backfilling the sample pair's historical child logs, and rerunning extraction until all mapped rows aligned without warning fallback.