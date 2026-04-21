# log-S0G-3D (Phase 3D: WORKFLOW-GITHUB-ISSUES file-identity rename and successor-release governance)

---

**id**: `S0G-3D`
**kind**: `log`
**title**: `workflow github issues file-identity rename and successor-release governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/3d`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md`
  **reference_log_1**: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
  **reference_log_2**: `docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md`
  **reference_log_3**: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  **reference_log_4**: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3d`
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
**created**: `2026-04-21`
**updated**: `2026-04-21`
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the repo is deciding whether the current defended family should keep its existing file identity temporarily, move by physical rename, or open a successor release instead.
- `reviewed` should remain `pending` until the rename-vs-successor decision, compatibility handling, and lineage/write-back rule are explicit enough to drive a bounded execution packet.

## Decision / Outcome

**Decision**:

- `S0G-3D` opens the next bounded follow-up after `S0G-3C`: the strong-structure family contract is now stable, but the file identity still carries a compatibility-era mismatch between defended family token and physical filename.
- The immediate governance question is no longer whether the family should be read as `WORKFLOW-GITHUB-ISSUES`; that point is already fixed. The open question is how to materialize that identity in files and release lineage without reopening the contract work that `S0G-3C` already settled.
- This lane must decide between at least two defended execution shapes:
  - physical rename of the current runbook and bound ledger series while preserving compatibility routing;
  - successor-release opening under a new file identity, with the current `001` release retained as the previous compatibility-era file.
- The current default decision for this lane is now narrower: prefer physical rename in place for the current `001` family unless later evidence proves that the rename would implicitly change runbook semantics, split the admitted `RUN-001` accounting surface, or make compatibility routing materially more complex than opening one explicit successor release.
- The decision must also define how compatibility readers land during transition: old exact paths should stay occupied by explicit compatibility stubs that point to the new canonical family paths instead of disappearing or silently remaining canonical by inertia.
- This lane must treat runbook, parent-ledger, `SUP`, and `PATCH` surfaces as one file-identity family decision, not as unrelated rename choices made file by file.

**Default choices (phase defaults / v1)**:

- Treat `WORKFLOW-GITHUB-ISSUES` as already fixed at contract level; `S0G-3D` does not reopen whether the narrower family token is correct.
- Prefer the smallest execution shape that makes file identity, lineage, and reader landing explicit without breaking the defended support-only ledger structure.
- Prefer rename-in-place when the current release meaning, admitted run accounting, and patch lineage remain the same and only the compatibility-era file identity is wrong.
- Do not physically rename current files until the repo explicitly decides whether rename-in-place or successor-release is the defended route.
- If a successor release is opened, it must explain what becomes of the current `run-WORKFLOW-GITHUB-001-...` identity and whether the current `001` remains active, becomes legacy, or is superseded immediately.
- If a physical rename is chosen, the lane must also define what happens to the old exact paths so historical links and reader entry points do not silently break.
- If a physical rename is chosen, execute compatibility landing, lineage/write-back, and family-level path updates in one bounded packet rather than renaming the runbook and ledgers in separate rounds.

## PR Summary Inputs (optional)

- This packet is expected to drive the next file-identity decision for the GitHub Issues workflow family, so the review summary should focus on rename scope, compatibility landing, and release-lineage consequences.

**PR summary bullets**:

- Decide how the current defended `WORKFLOW-GITHUB-ISSUES` family should resolve the remaining mismatch between contract identity and physical file identity.
- Compare physical rename versus successor-release as the two main execution shapes, including how parent-ledger, `SUP`, and `PATCH` surfaces should move with that decision.
- Fix one explicit compatibility and lineage rule before any rename or new release packet is executed.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3D-workflow-github-issues-file-identity-rename-and-successor-release-governance.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- `P1-C1-S1` | artifact: `docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md`

## Definitions (optional)

- **physical rename**: keep the current release lineage but move the canonical file path and family token in-place, with explicit compatibility handling for the old path.
- **successor release**: open a new runbook-family release or file identity as the new canonical surface, while retaining the current file as a prior lineage node.
- **compatibility landing**: the explicit rule for how readers, scripts, and historical references resolve the old path during and after the identity transition.
- **file-identity family decision**: one decision that covers the runbook plus its bound parent-ledger, `SUP`, and `PATCH` surfaces together rather than allowing them to drift independently.

## Constraints

- Do not reopen the already-fixed `WORKFLOW-GITHUB-ISSUES` family-narrowing contract from `S0G-3C`.
- Do not decide rename or successor release for the runbook alone while leaving bound ledger surfaces implicit.
- Do not silently break historical file links, script references, or reader landing paths by moving files without one explicit compatibility rule.
- Do not use physical rename as a cosmetic action if the real change should be modeled as a successor release with lineage.

## Scope

- `P0`: current file-identity mismatch and bounded decision surface
- `P1`: compare physical rename versus successor-release execution shapes
- `P2`: compatibility landing and lineage/write-back rule
- `P3`: next execution packet rule after the decision is fixed

## Success Criteria (DoD)

- One explicit rule states whether the repo should prefer physical rename or successor release for the current GitHub Issues workflow family.
- One explicit rule states how the parent-ledger, `SUP`, and `PATCH` surfaces move with that decision.
- One explicit compatibility rule exists for old file paths and historical reader entry.
- One explicit lineage/write-back rule exists for how the current release should point to the chosen next identity.
- One explicit next execution packet is fixed for the actual rename or successor-release implementation.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the physical-rename vs successor-release rule is explicit;
  - the compatibility landing rule is explicit;
  - the lineage/write-back rule is explicit;
  - the next bounded execution packet is fixed explicitly.

## P0 (Contract | v1)

### P0-C1-S1 (Current file-identity mismatch declared | v1)

- The defended family token is now `WORKFLOW-GITHUB-ISSUES`, but the current runbook and bound ledger series still retain the older `WORKFLOW-GITHUB-001` physical file identity.
- The current runbook already records this directly through `file_identity_status: legacy-filename-pending-rename`.
- This lane exists to resolve that remaining mismatch explicitly instead of letting compatibility-era naming persist by inertia.

### P0-C1-S2 (Bounded decision rule | v1)

- This lane decides identity materialization only.
- It does not reopen workflow profiles, stage accounting, `SUP/PATCH` bridge semantics, or run execution verdict rules already fixed in `S0G-3C`.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- Source-log work inside this lane still uses `S0G-3D/P<phase>-C<cycle>-S<steps>: <summary>`.
- Any later execution packet opened because of this lane should use the naming surface that matches the chosen identity action, not a generic rename title.

**Branch convention**:

- Keep this lane as source-log governance work until the file-identity decision is fixed.
- Do not open broad rename/move commits from this scaffold alone.

**Commit discipline (recommended)**:

- Decide identity action first.
- Only after that should later packets physically rename files, open successor releases, or write lineage/compatibility stubs.

## Plan (draft)

### P1 (Decision shapes)

- P1-C1-S1: compare physical rename versus successor-release as the two primary execution shapes

## P1 (Decision shapes | v1)

### P1-C1-S1 (Physical rename versus successor-release comparison fixed | v1)

- **Physical rename in place** should mean:
  - keep the current defended release lineage at `001`;
  - move the canonical runbook and bound ledger-series filenames so they encode `WORKFLOW-GITHUB-ISSUES-001` directly;
  - write explicit compatibility landing at the old paths rather than pretending the old exact filenames remain canonical.
- **Successor release** should mean:
  - open one new canonical file identity as the next release-lineage node;
  - leave the current `run-WORKFLOW-GITHUB-001-...` and bound ledger files as a previous compatibility-era release surface;
  - write explicit lineage from the current file set to the new canonical release.
- **Comparison result for the current repo state**:
  - physical rename is the preferred shape;
  - successor release is not the preferred default for the current repo state.
- **Reason physical rename is preferred now**:
  - the current change surface is file identity, not workflow semantics;
  - `RUN-001` is already admitted under the narrowed family reading, so opening a successor release now would split identity from one already-active accounting surface without first proving a semantic change;
  - `PATCH-001` is already bound to the current active release and run row, so a successor-release default would create extra lineage/write-back work before the repo has even tested whether compatibility routing can be kept simple;
  - the current runbook frontmatter already states `file_identity_status: legacy-filename-pending-rename`, which reads like a rename debt on the current release, not evidence that a new release meaning is already required.
- **Successor release should remain reserved for later use when one of these is true**:
  - the rename would also change defended runbook semantics;
  - the repo decides that `WORKFLOW-GITHUB-ISSUES-001` should start with a new admitted run sequence rather than continue the current `RUN-001` lineage;
  - compatibility landing at the old exact paths cannot be kept reviewable with a bounded stub/redirect rule.
- **Family-level movement rule under the preferred shape**:
  - if physical rename is executed, the runbook, parent ledger, `SUP`, and `PATCH` surfaces should move together as one family-level packet;
  - the live templates should then be updated in the same identity-implementation lane so newly opened files match the chosen canonical naming surface;
  - already-admitted artifacts should be rewritten only after the compatibility and lineage rule is explicit, not piecemeal during the comparison phase.

### P2 (Compatibility and lineage)

- P2-C1-S1: fix old-path landing and lineage/write-back rules for the chosen identity action

## P2 (Compatibility and lineage | v1)

### P2-C1-S1 (Compatibility landing and lineage/write-back rule fixed | v1)

- **Compatibility landing rule under the preferred physical-rename shape**:
  - the old exact runbook path should remain occupied by a slim compatibility stub rather than being deleted outright;
  - the old exact parent-ledger and patch-ledger paths should also remain occupied by slim compatibility stubs under `docs/runbook/support-only/` rather than disappearing;
  - each compatibility stub should do three things only:
    - state that the old file identity is no longer canonical;
    - point to the new canonical `WORKFLOW-GITHUB-ISSUES-001` path;
    - preserve enough historical landing context that existing citations and reader entry points do not fail closed on missing files.
- **Canonical-body placement rule under the preferred shape**:
  - the full operator body should move to the renamed runbook file;
  - the full admitted accounting body for `RUN-001` should move to the renamed parent-ledger file;
  - the full bounded-repair body for `PATCH-001` should move to the renamed patch-ledger file;
  - future `SUP` live files should open directly on the renamed canonical naming surface rather than creating one more live packet on the compatibility-era name.
- **Lineage/write-back rule under the preferred shape**:
  - keep `runbook_release: 001` unchanged during the rename packet;
  - keep `run_sequence: 001`, `RUN-001`, target-row ids, target-stage-row ids, and patch item ids unchanged during the rename packet;
  - treat the rename as file-identity repair for the same active release rather than as a fresh release event;
  - write the renamed canonical files as the new full-body authorities, and write the old files as compatibility stubs that point forward to those authorities;
  - update source-log references, runbook refs, ledger refs, and template examples in the same identity-implementation packet so the repo stops generating new packets against the compatibility-era paths.
- **Why this landing rule is preferred now**:
  - it matches the existing `S0G-2B` rule that old reader-facing paths should stay occupied by a stub instead of being deleted outright;
  - it avoids splitting the already-admitted `RUN-001` and `PATCH-001` surfaces into separate lineage eras before a semantic change has been proven;
  - it lets the repo preserve stable bridge keys while correcting the family token mismatch at the file-identity layer only.
- **Removal/deprecation rule for old exact paths**:
  - the old compatibility stubs should remain until at least one later bounded family packet proves the new canonical paths are the normal reader and writer landing surfaces;
  - do not remove the old exact paths in the same packet that first performs the rename.

### P3 (Next execution packet)

- P3-C1-S1: fix the next bounded implementation packet for the actual rename or successor-release work

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: current file-identity mismatch declared
- [x] `P0-C1-S2`: bounded decision rule fixed

### P1 (Decision shapes)

- [x] `P1-C1-S1`: physical rename versus successor-release comparison fixed

### P2 (Compatibility and lineage)

- [x] `P2-C1-S1`: compatibility landing and lineage rule fixed

### P3 (Next execution packet)

- [ ] `P3-C1-S1`: next identity-implementation packet fixed explicitly

## Current Status (recommended)

- `S0G-3D` is now the active discussion surface for the remaining file-identity decision after `S0G-3C` closed the strong-structure contract.
- The current runbook family no longer needs template-shape debate first; it needs one explicit decision on whether the current compatibility-era filename should be renamed in place or replaced by a successor release identity.
- `P1` is now fixed: for the current repo state, physical rename in place is the preferred execution shape, while successor release remains a reserved fallback only if rename would implicitly alter release meaning or make compatibility routing too complex.
- `P2` is now fixed: the old exact runbook and live-ledger paths should remain occupied by compatibility stubs, while the renamed `WORKFLOW-GITHUB-ISSUES-001` files become the new full-body authorities for the same active `001` release.
- The next useful work in this lane is now `P3`: fix one bounded identity-implementation packet that renames the live family together, updates template/examples and source-log refs, and leaves the old exact paths in place as compatibility landings.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this packet records the current file-identity mismatch and the already-closed strong-structure basis that makes the next identity decision narrow and local.

### P0-C1-S1 (current runbook still carries compatibility-era file identity after family narrowing | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/logs/log-S0G-3C-workflow-github-issues-strong-structure-and-ledger-bridge-governance.md`
- expected:
  - once the family token is fixed at contract level, the repo should still retain explicit evidence if the physical filename and bound ledger series have not yet caught up.
- observed:
  - the current runbook still records `file_identity_status: legacy-filename-pending-rename` while `S0G-3C` explicitly closes the narrower family identity as `WORKFLOW-GITHUB-ISSUES`.

### P1-C1-S1 (physical rename is preferred over successor release for the current `001` family state | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/_template-run-ledger-SUP.md`
  - `docs/runbook/support-only/_template-run-ledger-PATCH.md`
- expected:
  - the chosen identity action should minimize lineage churn while keeping the active runbook plus run-ledger family internally consistent.
- observed:
  - the current runbook and live ledgers still retain compatibility-era filenames, but their defended family reading is already narrowed to `WORKFLOW-GITHUB-ISSUES` and the active run/patch surfaces remain attached to the same `001` release.
  - the newer `SUP` and `PATCH` templates already assume `WORKFLOW-GITHUB-ISSUES-001` as the target canonical naming surface, which makes physical rename of the live family a better fit than opening a new release meaning before compatibility routing has even been fixed.
  - opening a successor release at this point would create extra lineage work across the active runbook, `RUN-001`, and `PATCH-001` even though the currently proven mismatch is file identity rather than release semantics.

### P2-C1-S1 (compatibility landing should preserve old exact paths as stubs while `001` stays the same release | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md`
  - `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the preferred rename path should preserve reader landing and historical references while avoiding a fake new release event for the already-admitted `001` family.
- observed:
  - `S0G-2B` already fixes the general rule that older reader-facing paths should remain occupied by a stub instead of being deleted outright when compatibility still matters.
  - `S0G-3A` already fixes that object identity and file placement should be explicit rather than left mixed by inertia, which supports moving the full bodies to new canonical names while keeping old exact paths as landing surfaces only.
  - the live runbook, parent ledger, and patch ledger all still point at the same active `001` release and admitted `RUN-001` accounting surface, so keeping release identity stable while repairing only file identity is the narrower write-back rule.

## Recent changes (for traceability, optional)

- 2026-04-21: opened `S0G-3D` as the next bounded governance lane after `S0G-3C` so the repo can decide physical rename versus successor-release handling for the current GitHub Issues workflow family.
- 2026-04-21: fixed `P1` for `S0G-3D` by preferring physical rename in place for the current `001` family, while keeping successor release reserved as a fallback if compatibility or lineage constraints prove rename insufficient.
- 2026-04-21: fixed `P2` for `S0G-3D` by requiring old exact paths to remain as compatibility stubs while the renamed `WORKFLOW-GITHUB-ISSUES-001` family becomes the new full-body authority for the same active `001` release.