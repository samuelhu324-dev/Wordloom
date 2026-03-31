# log-S0E-7A (Phase 7A: GitHub Actions secondary enforcement)

---

**id**: `S0E-7A`
**kind**: `log`
**title**: `workflow/github actions secondary enforcement v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Actions, Automation, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-6B-log-stability-and-gate-strategy.md`
  **reference_log_1**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  **reference_log_2**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **reference_log_3**: `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
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
**pr_labels**: ``
**pr_projects**: ``
**pr_milestone**: ``
**pr_base**: `main`
**pr_development_issue**: ``
**created**: `2026-03-31`
**updated**: `2026-03-31`

---

## Decision / Outcome

**Decision**:

- `S0E-7A` is now the dedicated follow-up for GitHub Actions integration after `S0E-5C/P4` wired post-apply verification into the local live create path.
- This slice is GitHub-side only: it owns mirror verification in Actions, artifact publishing, and failure surfacing policy in CI.

**Default choices (phase defaults / v1)**:

- GitHub Actions remains `secondary enforcement`, not the primary publish-time owner.
- The primary publish-time owner stays the local create path fixed in `S0E-5C/P4`: `S6 -> live verify -> S7`.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.
- Top-level issues/logs must leave `issue_parent` blank; roadmap bridging must stay explicit through `roadmap_path + roadmap_milestone + roadmap_phase`, not prose-only references.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Define GitHub Actions as a mirror verifier for live PR body contract checks instead of a replacement for local publish-time verification.
- Define the first minimal workflow shape for mirrored live PR verification in CI.
- Decide how Actions should publish artifacts and surface failures without pretending it prevented the original publish.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0` is reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` and `Development Link` as separate sections.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Definitions (optional)

- `primary publish-time owner`: the entrypoint that decides whether live publication proceeds before the mutation happens.
- `secondary enforcement`: a later verifier that re-checks live state after publication and emits machine-readable findings without claiming it prevented the original write.
- `mirror verifier`: a CI-side replay of the same live PR verification logic already fixed in the local create path.

## Constraints

- Do not move live publish authority from the local create path into GitHub Actions without a separate explicit decision slice.
- Do not mix local log gate policy into this slice; that now belongs to `S0E-6B`.
- Any later GitHub Actions workflow must reuse the same verifier semantics already fixed locally instead of inventing a second contract.

## Scope

- `P0`: fix the boundary between local primary verification and GitHub Actions secondary enforcement
- `P1`: define the first minimal GitHub Actions workflow shape and artifact contract for mirrored live verification
- `P2`: define failure surfacing, artifact publishing, and operator feedback rules for mirrored CI verification
- `P3`: define rollout boundary and success criteria for adopting the mirrored workflow in CI

## Success Criteria (DoD)

- The repo has a written decision that GitHub Actions is secondary enforcement and not the primary publish owner for PR create.
- The future Actions workflow shape reuses the same live PR verifier and produces explicit artifact paths instead of screenshot-only evidence.
- The future Actions workflow has explicit failure surfacing and artifact retention semantics.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the contract, workflow shape, and rollout boundary
  - at least one representative GitHub Actions mirror-verifier sample exists with traceable artifacts
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-7A` is now opened as the next narrow slice after `S0E-5C/P4`.
- `P0` is now completed: GitHub Actions is explicitly scoped as secondary enforcement, not as the primary publish-time owner.
- `P1-P3` remain open: workflow wiring, artifact publishing, failure surfacing, and rollout details are not yet executed.

## P0 (Boundary contract | v1)

### P0-C1-S1 (GitHub Actions ownership boundary fixed | v1)

- GitHub Actions should mirror the same live PR verifier already fixed in `S0E-5C/P4`; it should not become a replacement for the local create-path verification chain.
- The main reason is temporal: Actions runs after the publish event already exists, so it can detect drift and raise a machine-readable failure, but it cannot honestly claim that it prevented the original live PR creation.
- `S0E-7A` therefore keeps the ownership split explicit:
  - local create path = primary publish-time verification owner;
  - GitHub Actions = secondary post-publish enforcement and visibility layer.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-7A/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0E-7A/P0-P3: github actions secondary enforcement`
  - discontinuous phases: `S0E-7A/P0+P3: github actions secondary enforcement`
  - mixed discontinuous + consecutive phases: `S0E-7A/P0+P3-P4: github actions secondary enforcement`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `S0E-7A/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- `S0E-7A` changes should usually stay on the existing `S0E-*` working branch because this slice belongs to the same docs-management spine and is still closing automation/governance boundaries rather than a separate domain family.

## Plan (draft)

### P1 (GitHub Actions mirror-verifier workflow)

- `P1-C1-S1`: define event triggers, workflow inputs, and artifact outputs for mirrored live PR verification
- `P1-C1-S2`: decide how Actions should surface failure state without pretending it prevented publish

### P2 (Failure surfacing and artifacts)

- `P2-C1-S1`: define artifact publishing shape for mirrored live verification
- `P2-C1-S2`: define failure surfacing in workflow summary, checks, and retained artifacts

### P3 (Rollout boundary)

- `P3-C1-S1`: define which PR events and branches should run mirrored verification first
- `P3-C1-S2`: define success criteria for adopting the mirrored workflow in CI

## Execution Checklist (unchecked)

### P0 (Boundary contract)

- [x] `P0-C1-S1`: GitHub Actions ownership boundary fixed

### P1 (GitHub Actions mirror-verifier workflow)

- [ ] `P1-C1-S1`: define event triggers, workflow inputs, and artifact outputs
- [ ] `P1-C1-S2`: decide failure surfacing and operator feedback shape

### P2 (Failure surfacing and artifacts)

- [ ] `P2-C1-S1`: define artifact publishing shape
- [ ] `P2-C1-S2`: define failure surfacing and retained evidence

### P3 (Rollout boundary)

- [ ] `P3-C1-S1`: define initial workflow trigger boundary
- [ ] `P3-C1-S2`: define CI adoption success criteria

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1 (GitHub Actions secondary-enforcement boundary fixed | 2026-03-31)

- headSha: `9832ca0d`
- artifacts:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/logs/log-S3A-2A-4B-1A-git-actions.md`
- expected:
  - the next GitHub-side slice should open without collapsing GitHub Actions into the primary publish owner
- observed:
  - `S0E-7A` now fixes that boundary: Actions remains secondary enforcement and is limited to post-publish enforcement plus visibility rather than primary publish-time ownership

## Recent changes (for traceability, optional)

- 2026-03-31: re-scoped `S0E-7A` to GitHub-side concerns only, leaving Actions as secondary enforcement and moving local log stability / gate policy to `S0E-6B`.
- 2026-03-31: completed `P0` by fixing the GitHub Actions ownership boundary in one place: Actions is not the primary publish owner and should mirror the same verifier semantics already fixed in the local create path.