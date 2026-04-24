# log-S0G-3A (Phase 3: runbook release issue concentration and ledger naming governance)

---

**id**: `S0G-3A`
**kind**: `log`
**title**: `runbook release issue concentration and ledger naming governance v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/3a`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/534`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/535`
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md`
  **reference_log_1**: `docs/logs/log-S0G-2A-runbook-ledger-aware-operator-surface-and-execution-accounting.md`
  **reference_log_2**: `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md`
  **reference_log_3**: `docs/runbook/support-only/_template-run-ledger-PATCH.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/3`
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
**reviewed**: `2026-04-21`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the naming and issue-topology contract is still being fixed.
- Once the release issue topology, commit/PR naming grammar, and legacy placement rule are explicit enough to drive later commit/push discipline, `reviewed` should be set to the review date.

## Decision / Outcome

**Decision**:

- `S0G-3A` opens the next bounded follow-up after `S0G-2B`: fix one explicit governance rule for how runbook-family work should map to GitHub issues, PRs, and commit naming once the operator surface has moved from evolution-log-only slices into release/ledger/supplement/patch objects.
- The default issue topology is now intentionally concentrated: generate one release-scoped issue for the runbook family release, and let later ledger, supplement, and patch PRs attach back to that same release issue instead of opening a new issue per ledger-class packet.
- Commit and PR naming for runbook-family objects should stop inheriting the older `SxY/P*-C*-S*` grammar as their reader-facing primary label; they should instead use the bound object class and exact runbook-family token, while the source log remains the place that explains why the object exists.
- Older runbooks that no longer represent the defended current operator surface should be treated explicitly as `legacy` rather than left mixed with the current runbook family, and that placement decision belongs in this lane instead of being deferred indefinitely.
- Branches that already carry mixed history from earlier cherry-pick or backfill rounds should be treated as historical carriers; new runbook-family work should start from fresh `main`-based clean branches so commit discovery and later PR automation stay bounded.

**Default choices (phase defaults / v1)**:

- One runbook release should normally own exactly one live release issue.
- Parent run-ledger, SUP-ledger, and PATCH-ledger packets should reuse that release issue as their PR linkage anchor unless a later contract proves that a separate issue class is necessary.
- The reader-facing family token should stay identical to the file/object token, for example `WORKFLOW-GITHUB-001`, rather than being rewritten into spaced prose for commit and PR subjects.
- Reader-facing commit and PR titles for runbook-family objects should prefer object-class prefixes such as `RUN-RELEASE`, `RUN-LEDGER-001`, `RUN-LEDGER-SUP-001`, and `RUN-LEDGER-PATCH-001`.
- The older slice-style `SxY/P*-C*-S*` grammar remains valid for evolution source logs and other pre-runbook-family work; it is not deleted, but it should no longer be the primary naming surface for new runbook-family packets.
- If a runbook file no longer represents the defended operator surface, record the placement decision explicitly as `legacy` rather than leaving it at the active root by inertia.
- When a working branch already contains mixed ancestry from earlier cherry-pick or backfill rounds, do not try to beautify that branch as the long-term carrier; open a fresh branch from `main` for the next bounded packet.

## PR Summary Inputs (optional)

- This packet is expected to drive later release-scoped issue and PR work, so the review summary should focus on issue concentration, naming grammar, and legacy/current-state separation.

**PR summary bullets**:

- Concentrate runbook-family GitHub issue generation onto one release issue instead of opening one issue per ledger or patch packet.
- Fix one object-first naming grammar for release, ledger, supplement, and patch commits and PR titles.
- Record that older runbooks should move under `legacy` once a newer defended runbook-family surface exists, and that future work should start from fresh clean branches instead of polluted historical carriers.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/runbook/run-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- `P1-C1-S1` | artifact: `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`
- `P1-C1-S2` | artifact: `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-ISSUES-001-GitHub-Issues-full-auto-pipeline.md`

## Definitions (optional)

- **release issue concentration**: one rule that later ledger, supplement, and patch PRs should point back to the bound runbook release issue instead of generating one new issue per object.
- **object-first naming**: reader-facing commit and PR naming that starts from the defended object class, for example `RUN-LEDGER-001`, instead of the source-log slice id.
- **historical carrier branch**: an older mixed branch that remains useful as reference, but should not continue as the default branch for new bounded work once ancestry has been polluted by cherry-pick or retrospective close-out rounds.
- **legacy runbook placement**: the explicit decision that older runbooks remain readable but no longer claim current operator authority once a newer defended runbook family exists.

## Constraints

- Do not reopen issue proliferation by generating one GitHub issue per ledger, supplement, or patch packet unless a later defended contract proves that concentration fails.
- Do not let commit/PR naming drift away from the exact runbook-family token carried by the bound files.
- Do not quietly keep older runbooks at the active root once they are no longer the defended current operator surface.
- Do not continue new packet work on long-lived polluted branches when a fresh `main`-based clean branch would preserve clearer commit ancestry.

## Scope

- `P0`: release-issue concentration rule and object boundary
- `P1`: commit/PR naming grammar for release, ledger, supplement, and patch packets
- `P2`: legacy runbook placement decision and branch-carrier rule
- `P3`: next-lane execution rule for later commit/push discipline under mixed workspace state

## Success Criteria (DoD)

- One explicit rule states that runbook-family GitHub issue generation defaults to one release issue, not one issue per ledger packet.
- One explicit reader-facing naming grammar exists for `RUN-RELEASE`, `RUN-LEDGER-001`, `RUN-LEDGER-SUP-001`, and `RUN-LEDGER-PATCH-001`.
- The lane states when older runbooks should move under `legacy` rather than continue to appear as current-state operator surfaces.
- The lane states that future bounded work should begin from fresh clean branches when the older lane branch is already polluted by mixed ancestry.
- The next discussion step is explicit: classify current workspace changes into `runbook-family commit/push now` vs `still evolution-log lane` before mutating git history.

## Stability (what stable means)

- This log is now `stable` because:
  - the release-issue concentration rule is explicit;
  - the object-first naming grammar is explicit;
  - the legacy runbook placement rule is explicit;
  - the next classification step for current workspace changes is fixed explicitly.

## P0 (Contract | v1)

### P0-C1-S1 (Release issue concentration fixed | v1)

- A runbook family release should normally create one release issue only.
- Later parent-ledger, SUP-ledger, and PATCH-ledger PRs should attach to that release issue by default instead of generating separate issues.
- If a later packet truly needs a separate issue, that should be treated as an exception that must be justified explicitly in a source log or contract, not as the default topology.

### P0-C1-S2 (Object boundary vs source-log boundary fixed | v1)

- The source log remains the governance and explanation surface for why the object exists.
- The reader-facing commit and PR title for a runbook-family packet should follow the object class, not the source-log slice id.
- Source-log IDs such as `S0G-3A` remain valid inside evidence, provenance, and planning text, but they should not be the primary label for the user-facing runbook-family packet once the packet is operating as a release/ledger/supplement/patch object.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- Source-log work inside this lane still uses `S0G-3A/P<phase>-C<cycle>-S<steps>: <summary>`.
- Runbook-family release packets should use `RUN-RELEASE: WORKFLOW-GITHUB-001 GitHub Issues full-auto pipeline / <summary>`.
- Parent run-ledger packets should use `RUN-LEDGER-001: WORKFLOW-GITHUB-001 GitHub Issues full-auto pipeline / <summary>`.
- Supplement run-ledger packets should use `RUN-LEDGER-SUP-001: WORKFLOW-GITHUB-001 GitHub Issues full-auto pipeline / <summary>`.
- Patch run-ledger packets should use `RUN-LEDGER-PATCH-001: WORKFLOW-GITHUB-001 GitHub Issues full-auto pipeline / <summary>`.
- PR titles should reuse the same object-first prefix grammar as the packet they represent; they should not invent a second naming system.

**Branch convention**:

- New runbook-family packets should normally open from a fresh `main`-based clean branch named for the bounded object or packet, rather than continuing on a long-lived mixed historical carrier branch.
- Older polluted branches such as retrospective or cherry-pick-heavy carriers may remain as historical context, but they should not be the default base for discovering or publishing the next bounded packet.

**Commit discipline (recommended)**:

- Do not commit/push the current mixed workspace blindly under the new object-first grammar.
- First classify each pending change as one of two buckets: `belongs to a defended runbook-family object now` or `still belongs to an evolution source-log lane`.
- Only after that classification should the later commit/push work adopt `RUN-RELEASE` or `RUN-LEDGER-*` subjects; otherwise the repo will create another mixed-history packet under a cleaner name but with the same boundary error.

## Plan (draft)

### P1 (Naming and issue topology)

- P1-C1-S1: fix release-issue concentration as the default issue topology for runbook-family work
- P1-C1-S2: publish the object-first commit/PR naming grammar for release, ledger, supplement, and patch packets

### P2 (Placement and branch boundary)

- P2-C1-S1: record when older runbooks should move under `legacy`
- P2-C1-S2: record the clean-branch rule for future bounded packets after polluted ancestry rounds

### P3 (Next discussion step)

- P3-C1-S1: classify the current mixed workspace into `runbook-family commit/push now` vs `still evolution-log lane`

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: release issue concentration fixed
- [x] `P0-C1-S2`: object boundary vs source-log boundary fixed

### P1 (Naming and issue topology)

- [x] `P1-C1-S1`: release-issue concentration written as the default topology
- [x] `P1-C1-S2`: object-first commit/PR naming grammar written explicitly

### P2 (Placement and branch boundary)

- [x] `P2-C1-S1`: legacy runbook placement decision recorded
- [x] `P2-C1-S2`: clean-branch rule recorded for future bounded packets

### P3 (Next discussion step)

- [x] `P3-C1-S1`: next classification step fixed explicitly

## Current Status (recommended)

- `S0G-3A` now fixes the missing governance layer between the existing runbook/ledger file naming contract and later commit/PR/issue practice.
- The default issue topology is now intentionally concentrated onto one runbook release issue, with ledger, supplement, and patch PRs expected to attach back to that same release issue unless a later exception is justified explicitly.
- The object-first naming grammar is now explicit for `RUN-RELEASE`, `RUN-LEDGER-001`, `RUN-LEDGER-SUP-001`, and `RUN-LEDGER-PATCH-001`.
- The next step after this packet is execution-time workspace cleanup under those fixed rules: finish the bounded `S0G` governance write-back package first, then separate `S4F` close-out/accounting work from script changes before the next naming-based commit burst.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this packet records the currently defended runbook and ledger surfaces that make the new naming and issue-topology rule necessary.

### P0-C1-S1 (release issue concentration opened against the current runbook family | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the current runbook family should provide one stable release object that can act as the default issue anchor for later ledger-class PRs.
- observed:
  - `WORKFLOW-GITHUB-001` already exists as one defended runbook release with explicit parent, supplement, and patch ledger bindings, so one release issue is the simpler default topology.

### P1-C1-S1 (parent run and patch packets already read as subordinate objects under one family | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/runbook/support-only/ledger-run-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the parent run ledger and patch ledger should read as subordinate objects under one runbook family rather than as separate issue families by default.
- observed:
  - both packets already bind back to the same `WORKFLOW-GITHUB-001` family and the same admitted run context, so separate per-packet issues would add routing noise without clarifying the object boundary.

### P2-C1-S1 (legacy placement and clean-branch rule required by mixed ancestry history | 2026-04-21)

- headSha: `WORKTREE`
- artifacts:
  - `docs/logs/log-S0G-docs-management-v7.md`
  - `docs/logs/log-S0G-2B-support-only-ledger-placement-and-patch-ledger-bridge.md`
- expected:
  - once newer runbook-family surfaces exist and older historical carriers remain mixed, the repo should record both a legacy placement rule and a fresh-branch rule for later bounded packets.
- observed:
  - the current `S0G` spine already records a retrospective mixed-history close-out origin, while the newer runbook-family and support-only ledgers now provide a clearer current-state surface; this makes the `legacy` and clean-branch decisions necessary before the next commit burst.

## Recent changes (for traceability, optional)

- 2026-04-21: opened `S0G-3A` to fix the missing governance rule for release-issue concentration, object-first commit/PR naming, legacy runbook placement, and clean-branch discipline after the first `WORKFLOW-GITHUB-001` admitted run.