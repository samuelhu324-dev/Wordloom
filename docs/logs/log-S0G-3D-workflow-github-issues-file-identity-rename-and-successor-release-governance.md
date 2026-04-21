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
- The decision must also define how compatibility readers land during transition: alias stub, retained legacy path, lineage-only redirect, or another explicit defended routing rule.
- This lane must treat runbook, parent-ledger, `SUP`, and `PATCH` surfaces as one file-identity family decision, not as unrelated rename choices made file by file.

**Default choices (phase defaults / v1)**:

- Treat `WORKFLOW-GITHUB-ISSUES` as already fixed at contract level; `S0G-3D` does not reopen whether the narrower family token is correct.
- Prefer the smallest execution shape that makes file identity, lineage, and reader landing explicit without breaking the defended support-only ledger structure.
- Do not physically rename current files until the repo explicitly decides whether rename-in-place or successor-release is the defended route.
- If a successor release is opened, it must explain what becomes of the current `run-WORKFLOW-GITHUB-001-...` identity and whether the current `001` remains active, becomes legacy, or is superseded immediately.
- If a physical rename is chosen, the lane must also define what happens to the old exact paths so historical links and reader entry points do not silently break.

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

### P2 (Compatibility and lineage)

- P2-C1-S1: fix old-path landing and lineage/write-back rules for the chosen identity action

### P3 (Next execution packet)

- P3-C1-S1: fix the next bounded implementation packet for the actual rename or successor-release work

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: current file-identity mismatch declared
- [x] `P0-C1-S2`: bounded decision rule fixed

### P1 (Decision shapes)

- [ ] `P1-C1-S1`: physical rename versus successor-release comparison fixed

### P2 (Compatibility and lineage)

- [ ] `P2-C1-S1`: compatibility landing and lineage rule fixed

### P3 (Next execution packet)

- [ ] `P3-C1-S1`: next identity-implementation packet fixed explicitly

## Current Status (recommended)

- `S0G-3D` is now the active discussion surface for the remaining file-identity decision after `S0G-3C` closed the strong-structure contract.
- The current runbook family no longer needs template-shape debate first; it needs one explicit decision on whether the current compatibility-era filename should be renamed in place or replaced by a successor release identity.
- The next useful work in this lane is to compare those two execution shapes at the family level and then fix one compatibility and lineage rule before any file move or successor-release packet is executed.

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

## Recent changes (for traceability, optional)

- 2026-04-21: opened `S0G-3D` as the next bounded governance lane after `S0G-3C` so the repo can decide physical rename versus successor-release handling for the current GitHub Issues workflow family.