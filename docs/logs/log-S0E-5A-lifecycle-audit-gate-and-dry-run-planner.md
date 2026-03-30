# log-S0E-5A (Phase 5A: Lifecycle Audit Gate and Dry-run Planner)

---

**id**: `S0E-5A`
**kind**: `log`
**title**: `lifecycle audit gate and dry-run planner v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Issues, PR, Automation, Drills, Evidence, epic/s0, sub/0e5a`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: `docs/runbook/run-S0E-log-to-issue-creation.md`
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
  **reference_log_1**: `docs/logs/log-S0E-2D-issue-creation-metadata-and-english-body-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-4D-review-hold-and-full-auto-lifecycle-orchestration-follow-up.md`
**issue_keyword**: `workflow`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
**issue_module_labels**: ``
**issue_milestone**: ``
**issue_parent**: ``
**issue_projects**: ``
**roadmap_path**: ``
**roadmap_milestone**: ``
**roadmap_phase**: ``
**roadmap_bridge_refs**: ``
**pr_labels**: `drills`
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-30`
**updated**: `2026-03-30`

---

## Decision / Outcome

**Decision**:

- `S0E-5A` exists to define one lifecycle-audit gate that runs before any mutation across the `issue -> PR -> merge -> relationship -> conclusion` chain.
- v1 deliberately starts as `dry-run only`: it reports pass / warning / blocked findings, but it does not mutate GitHub or rewrite local logs.
- The audit gate must verify live GitHub state, not just markdown body text, so body completeness and sidebar relationship completeness are treated as separate checks.

**Default choices (phase defaults / v1)**:

- Any lifecycle mutation request should be preceded by one dry-run audit when the target issue/PR already exists or when historical state may need replay.
- The gate is stage-aware: issue-created, PR-linked, merged-open, and concluded items are checked against different expectations rather than one flat checklist.
- Deterministic checks are fail-closed when they concern exact references or live state, such as missing exact-ID merged PR evidence, missing required labels, or missing sidebar parent-child relationships.
- Human-facing content quality may surface as warnings, but structural integrity checks should block follow-up mutation until the planner output is reconciled.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## Definitions (optional)

- **Lifecycle audit**: a dry-run inspection that compares source-log metadata, live GitHub issue/PR state, and expected stage-specific completion rules.
- **Mutation**: any operation that would change a live issue, PR, relationship, or final conclusion body.
- **Body completeness**: whether the issue body carries the expected sections, links, and DoD references for its current lifecycle stage.
- **Relationship completeness**: whether the live GitHub sidebar relationship state matches the expected parent-child structure, independent of body text.
- **Exact-ID merged PR evidence**: the merged PR set whose titles start with the exact requested ID prefix such as `S0E-4A/`.
- **Merged-open**: a state where the relevant PR evidence is already merged but the issue has not yet been fully concluded and closed.

## Constraints

- v1 is dry-run only; the planner must not mutate GitHub, rewrite issue bodies, or attach relationships.
- The gate must read live GitHub state for issue body, labels, and sidebar parent relationship rather than trusting source-log write-back alone.
- Exact-ID merged PR selection must stay deterministic and must not rely on free-text keyword guesses.
- The planner must emit enough structured evidence that a later apply path can act on findings without re-scraping arbitrary prose.

## Scope

- `P0`: contract for audit scope, stage model, severity rules, and evidence shape
- `P1`: implement a manifest-driven dry-run lifecycle audit planner
- `P2`: validate the planner against representative closed `S0E` child issues after historical remediation and relationship repair

## Success Criteria (DoD)

- The contract distinguishes body completeness from live sidebar relationship completeness.
- The planner accepts explicit manifest items and derives missing issue refs safely from source logs when possible.
- The planner reports stage-aware checks for required sections, labels, exact-ID merged PR evidence, parent metadata, and live sidebar relationship state.
- The planner emits structured `pass / warning / blocked / reconciliation` outcomes without mutating GitHub.
- At least one representative audit sample proves the repaired `S0E` child issues now converge on both final body shape and parent issue `#248` relationship state.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the lifecycle-audit gate contract, dry-run planner entrypoint, and representative audit sample have all been exercised successfully;
  - the Evidence section includes traceable artifact paths that show both manifest input and planner output for the representative issue set.

## Current Status

- `S0E-5A` now defines the first dedicated audit gate for lifecycle mutations instead of leaving that responsibility split across creation, PR, and conclusion slices.
- v1 is intentionally limited to dry-run planning, but it already covers the structural defects that mattered in historical audits: stale write-back, missing labels, missing exact-ID merged PR evidence, and missing sidebar parent-child relationships.
- The first representative sample now passes end to end: `#289`, `#297`, `#293`, `#300`, and `#303` all return `pass-audit` against one shared planner output.

## P0 (Contract | v1)

### P0-C1-S1 (Audit boundary and lifecycle stages | v1)

- The audit gate runs before any mutation that touches issue bodies, PR bodies, relationship state, or final issue conclusion.
- v1 recognizes four practical lifecycle stages: `issue-created`, `pr-linked`, `merged-open`, and `concluded`.
- Stage classification is derived from live issue state plus exact-ID merged PR evidence; it is not guessed from prose.

### P0-C1-S2 (Severity and blocking rules | v1)

- `pass` means the audited item is structurally ready for the requested lifecycle mutation.
- `warning` means the item is usable but carries softer drift that should be reviewed, such as a still-open issue after merged PR evidence exists.
- `blocked` means the gate found a structural integrity defect such as missing expected labels, missing exact-ID PR evidence for a concluded issue, or missing live parent-child relationship.
- `reconciliation` means the explicit manifest input conflicts with source-log or GitHub references and must be reconciled before a mutation plan is trusted.

### P0-C1-S3 (Evidence contract | v1)

- Evidence JSON must include:
  - explicit manifest input and derived live issue references
  - stage classification plus exact-ID merged PR evidence summary
  - per-check statuses for source-log write-back, required sections, labels, links, DoD refs, and live parent-child relationship
  - one overall audit status that a later gate/apply path can consume without rescanning free text

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-5A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0E-5A/P0-P3: <log title>`
  - discontinuous phases: `S0E-5A/P0+P3: <log title>`
  - mixed discontinuous + consecutive phases: `S0E-5A/P0+P3-P4: <log title>`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `S0E-5A/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- `S0E-5A` follow-up work should continue on `S0E-docs-management-v5` as the mixed authoring branch until a review-ready slice is cut.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, try to `commit/push` promptly so audit logic, manifest shape, and sample evidence stay traceable as separate deltas.

## Plan (draft)

### P1 (Dry-run planner)

- P1-C1-S1: define the manifest input and structured output contract for lifecycle audit planning
- P1-C1-S2: implement stage-aware checks for source-log write-back, labels, PR evidence, final body shape, and sidebar parent-child relationships

### P2 (Representative audit)

- P2-C1-S1: prepare a representative manifest over repaired `S0E` child issues
- P2-C1-S2: run the dry-run planner and record the converged output as evidence

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: audit boundary and lifecycle stages fixed
- [x] `P0-C1-S2`: severity and blocking rules fixed
- [x] `P0-C1-S3`: structured evidence contract fixed

### P1 (Dry-run planner)

- [x] `P1-C1-S1`: lifecycle audit manifest and result shape fixed
- [x] `P1-C1-S2`: stage-aware dry-run checks implemented

### P2 (Representative audit)

- [x] `P2-C1-S1`: representative repaired `S0E` child-issue manifest prepared
- [x] `P2-C1-S2`: dry-run audit output recorded for the representative sample

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths.

### P0-C1-S1S2S3 (audit gate contract fixed | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
- expected:
  - one dry-run-only gate contract exists before future lifecycle mutations
  - body completeness and live relationship completeness are treated as separate checks
  - stage-aware pass / warning / blocked / reconciliation semantics are explicit
- observed:
  - `S0E-5A` now fixes the gate boundary, lifecycle stages, severity levels, and evidence shape in one dedicated slice

### P1-C1-S1S2 (manifest-driven dry-run planner implemented | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `scripts/issues/plan_lifecycle_audit.py`
  - `docs/issues/lifecycle-audit-S0E-5A-sample-manifest.json`
- expected:
  - one manifest-driven dry-run planner can audit lifecycle state without mutating GitHub
  - planner output includes stage classification, exact-ID merged PR evidence, and per-check statuses
- observed:
  - `plan_lifecycle_audit.py` now emits structured item-level checks for write-back, labels, merged PR evidence, final DoD refs, links, and live sidebar parent relationship state

### P2-C1-S1S2 (representative repaired child-issue sample audited | 2026-03-30)

- headSha: `<git sha>`
- artifacts:
  - `docs/issues/lifecycle-audit-S0E-5A-sample-manifest.json`
  - `docs/issues/lifecycle-audit-S0E-5A-sample-plan.json`
- expected:
  - the representative repaired `S0E` child issues should pass the dry-run audit after the latest body and relationship remediation
  - parent issue `#248` should be confirmed both in issue metadata and in live sidebar relationship state for the sampled historical children
- observed:
  - `docs/issues/lifecycle-audit-S0E-5A-sample-plan.json` now records `pass-audit` for all five sampled child issues: `#289`, `#297`, `#293`, `#300`, and `#303`
  - the same planner output confirms parent issue `#248` in both metadata and live sidebar relationship state across the representative sample

## Recent changes (for traceability, optional)

- 2026-03-30: opened `S0E-5A` to define a dedicated lifecycle-audit gate that runs before future issue/PR/relationship/conclusion mutations.
- 2026-03-30: implemented a manifest-driven dry-run planner for stage-aware lifecycle auditing.
- 2026-03-30: prepared and executed a representative repaired-child sample so the first gate artifact is grounded in real `S0E` issue history.