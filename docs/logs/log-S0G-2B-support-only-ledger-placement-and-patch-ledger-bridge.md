# log-S0G-2B (Phase 2B: support-only ledger placement and patch-ledger bridge)

---

**id**: `S0G-2B`
**kind**: `log`
**title**: `support-only ledger placement and patch-ledger bridge v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/2b`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
  **reference_log_1**: `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
  **reference_log_2**: `docs/logs/log-S0F-2B-family-patch-and-ops-maintenance-model.md`
  **reference_log_3**: `docs/runbook/support-only/_template-run-ledger-SUP.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/2`
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

## Decision / Outcome

**Decision**:

- `S0G-2B` exists as the next bounded follow-up after `S0G-2A`: all ledger-class files for the new runbook family should live under `docs/runbook/support-only/`, not at the runbook root.
- Runbook-bound patch packets should no longer default to log-first patch notes; they should use a support-only patch-ledger surface that is supplement-class and keeps the same ownership, approval, timing, verification, and attachment affordances as other ledger packets.
- The first canonical patch-ledger naming rule for `WORKFLOW-GITHUB-001` is fixed as `ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`.

**Default choices (phase defaults / v1)**:

- Parent run ledgers, SUP ledgers, and PATCH ledgers should all live under `docs/runbook/support-only/`.
- Root `docs/runbook/` remains for family-level runbooks only; it is not the canonical home for ledger-class packets.
- When an older runbook still has broad historical readers, move its retained full body under `docs/runbook/legacy/` and keep the old root path occupied by a stub instead of deleting the path outright.
- PATCH ledgers are support-only supplement-class packets for bounded repair work that stays inside one defended runbook release.
- PATCH ledgers may carry screenshots, transcripts, and approval-facing attachments the same way SUP ledgers do.
- PATCH ledgers must record explicit ownership, review, verification, approval, and lifecycle-time fields.
- If a patch materially changes operator semantics, evidence admission rules, or runbook/ledger binding, stop and open a new source log plus a new runbook release instead of continuing inside the patch ledger series.

## Constraints

- Do not leave canonical ledger-class references pointing at the runbook root once support-only placement is fixed.
- Do not treat patch notes as freeform prose-only packets when they are intended to feed later extraction, approval, or audit.
- Do not force every bounded repair to become a runbook release bump.
- Do not use a PATCH ledger to hide contract-level semantic change.

## Scope

- `P0`: support-only placement rule for parent, SUP, and PATCH ledgers
- `P1`: patch-ledger bridge contract and template surface
- `P2`: `WORKFLOW-GITHUB-001` binding rewrite plus first reserved PATCH ledger surface
- `P3`: next-lane decision after support-only and patch bridge hardening

## Success Criteria (DoD)

- Canonical ledger-class placement is fixed to `docs/runbook/support-only/`.
- A PATCH ledger template exists and carries ownership, approval, timing, verification, and attachment-review fields.
- `WORKFLOW-GITHUB-001` binds to support-only parent and patch ledger surfaces consistently.
- The next step is explicit: only after these rules are fixed should the first real full-auto sample batch begin.

## Stability (what stable means)

- This log can be marked `stable` when:
  - support-only placement and patch-ledger bridge rules are explicit;
  - the canonical template and reserved `PATCH-001` surface exist;
  - the next lane is fixed back to real sample execution rather than more placement debate.

## Plan (closed in this packet)

### P0 (Placement rule)

- P0-C1-S1: fix support-only as the canonical home for ledger-class packets

### P1 (Patch-ledger bridge)

- P1-C1-S1: publish a support-only PATCH ledger template with SUP-like ownership, approval, timing, and attachment review fields
- P1-C1-S2: demote the old log-first patch-note template into a legacy compatibility note with bridge guidance

### P2 (Binding rewrite)

- P2-C1-S1: rewrite `WORKFLOW-GITHUB-001` ledger binding to support-only paths
- P2-C1-S2: reserve the first canonical patch-ledger surface for `WORKFLOW-GITHUB-001`

### P3 (Next-lane decision)

- P3-C1-S1: fix the next step back to the first real `WORKFLOW-GITHUB-001` full-auto sample batch after the placement and patch bridge rules are in place

## Execution Checklist

### P0 (Placement rule)

- [x] `P0-C1-S1`: support-only ledger placement fixed as canonical

### P1 (Patch-ledger bridge)

- [x] `P1-C1-S1`: support-only PATCH ledger template published
- [x] `P1-C1-S2`: legacy log-first patch note demoted into bridge-only compatibility guidance

### P2 (Binding rewrite)

- [x] `P2-C1-S1`: `WORKFLOW-GITHUB-001` binding rewritten to support-only ledger paths
- [x] `P2-C1-S2`: first reserved `PATCH-001` ledger surface opened

### P3 (Next-lane decision)

- [x] `P3-C1-S1`: next step fixed to real full-auto samples only after these rules

## Current Status

- `S0G-2B` has now fixed the canonical ledger home as `docs/runbook/support-only/`.
- The new patch-ledger bridge is explicit: patch packets that belong to one stable runbook release should use `ledger-run-PATCH-*` support-only files, not unstructured log-first notes.
- `WORKFLOW-GITHUB-001` is now rebound to support-only ledger surfaces, and the first reserved patch-ledger name exists.
- Older non-current runbooks are now being rehomed under `docs/runbook/legacy/`, while root-path stubs are preserved so broad historical references do not break at move time.
- The first real `WORKFLOW-GITHUB-001` full-auto sample batch has now executed and updated admitted run accounting under `RUN-001`, with `PATCH-001` bound back to the same parent run row.

## Evidence

### P1-C1-S1 (support-only PATCH ledger template published | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/support-only/_template-run-ledger-PATCH.md`
- expected:
  - patch packets should gain a supplement-class template with ownership, verification, approval, timing, and attachment review fields.
- observed:
  - the new template now gives patch packets the same structured review and lifecycle surface that SUP ledgers already have, while keeping patch-specific release-bound rules.

### P1-C1-S2 (legacy patch-note template reduced to bridge-only compatibility note | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/patch/_template-log-patch-note.md`
- expected:
  - the old log-first patch template should stop acting like the canonical new path for runbook-bound repairs.
- observed:
  - the template now explicitly routes new runbook-bound patch packets to support-only `ledger-run-PATCH-*` files instead of keeping prose-only patch notes as the default.

### P2-C1-S1 (WORKFLOW-GITHUB-001 rebound to support-only ledger paths | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the runbook should no longer point at root-level ledger paths once support-only placement is canonical.
- observed:
  - the runbook now binds to the parent ledger, supplement ledger series, and patch ledger series under `docs/runbook/support-only/`.

### P2-C1-S2 (reserved PATCH-001 support-only surface opened | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the first canonical patch-ledger name should exist before live samples begin so future bounded repairs have one defended landing surface.
- observed:
  - the reserved `PATCH-001` surface was opened before live samples began and is now the bound repair surface for the first admitted `WORKFLOW-GITHUB-001` run.

### P3-C1-S1 (next lane fixed back to real full-auto samples after bridge hardening | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md`
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - once support-only placement and patch-ledger bridge rules are fixed, the next step should return to real sample execution rather than keep widening policy.
- observed:
  - the next bounded step did return to the first real `WORKFLOW-GITHUB-001` full-auto sample batch, and that batch is now admitted under `RUN-001` with the bounded repair packet bound under `PATCH-001`.

## Recent changes

- 2026-04-21: fixed `docs/runbook/support-only/` as the canonical home for ledger-class packets.
- 2026-04-21: published the new support-only `PATCH` ledger template and reserved the first `ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md` surface.
- 2026-04-21: rebound `WORKFLOW-GITHUB-001` to support-only parent, supplement, and patch ledger paths before the first live sample batch.
- 2026-04-21: rehomed older runbooks under `docs/runbook/legacy/` and preserved root-path stubs so historical citations can still land on the old exact paths.
- 2026-04-21: admitted the first real four-sample `WORKFLOW-GITHUB-001` run under `RUN-001` after issue creation, PR creation, human merge, and guarded issue-conclusion refresh.
- 2026-04-21: bound `PATCH-001` back to `RUN-001` because the first admitted run consumed the milestone-skip and multi-item preview-body repairs.