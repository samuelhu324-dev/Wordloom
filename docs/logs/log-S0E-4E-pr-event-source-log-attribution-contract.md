# log-S0E-4E (Phase 4E: PR-event source-log attribution contract)

---

**id**: `S0E-4E`
**kind**: `log`
**title**: `contract/pr-event source-log attribution contract v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Actions, Automation, Contract, PR, epic/s0, sub/1`
**links**: ``
  **issue**: ``
  **pr**: ``
  **runbook**: ``
  **roadmap**: ``
  **parent_log**: `docs/logs/log-S0E-docs-management-v5.md`
  **previous_log**: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  **reference_log_1**: `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  **reference_log_2**: `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  **reference_log_3**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_4**: `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
**issue_keyword**: `contract`
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

- `S0E-4E` is now the dedicated follow-up for the unresolved attribution problem left open by `S0E-7A/P3`: how an automatic PR-event workflow can deterministically identify the single contract-owning source log for a live PR.
- This slice is intentionally re-homed under the `4x` PR family rather than kept as `7B`, because the problem is fundamentally about PR ownership and PR-event provenance rather than about secondary-enforcement workflow policy by itself.
- This slice owns attribution only. It does not re-open secondary-enforcement policy, retained artifact policy, or PR body contract shape.

**Default choices (phase defaults / v1)**:

- Automatic PR-event mirroring must stay fail-closed until the repo has a deterministic `PR event -> source_log_path` attribution rule.
- Provenance should prefer explicit machine-written ownership signals over heuristic inference from prose, PR title text, or branch naming.
- If attribution is ambiguous, missing, or points to multiple plausible logs, automation should stop and report the ambiguity rather than choosing one candidate optimistically.
- `S0E-4E` should treat attribution as a contract-ownership problem, not as a fuzzy search problem.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.
- `Evidence Footer Source` does not replace `Evidence`: the footer source feeds PR/gate automation, while `Evidence` remains the human ledger.

**PR summary bullets**:

- Open the dedicated slice for deterministic `PR event -> source_log_path` attribution.
- Separate source-log attribution ownership from `S0E-7A` secondary-enforcement workflow policy.
- Fix the first fail-closed boundary: automatic rollout is blocked until attribution becomes explicit and deterministic.

**PR checklist source**:

- Default source: reuse this log's execution checklist after `P0` is reviewed.

**PR links**:

- Log: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
- Issue: ``
- Runbook: ``
- Evidence artifact: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
- `P1-C1-S1S2` | artifact: `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`

- Keep footer rows low-cardinality: prefer one representative artifact per relevant unit instead of replaying the full artifact inventory.
- Generated PR body should keep `Evidence Footer` and `Development Link` as separate sections.
- `Evidence Footer` rows must be copied only from `Evidence Footer Source` and must keep the same line shape.

## Definitions (optional)

- `source-log attribution`: the rule that determines which structured log is the contract-owning source for a live PR or PR event.
- `contract-owning log`: the single log whose `PR Summary Inputs`, `Evidence Footer Source`, and related structured inputs are authoritative for that PR contract.
- `attribution ambiguity`: any case where zero or multiple plausible source logs exist and the workflow cannot justify one deterministic owner.

## Constraints

- Do not widen automatic PR-event mirroring until attribution is deterministic enough to be trusted.
- Do not let `S0E-4E` drift into generic search/retrieval work over logs; it owns a contract mapping, not a best-effort recommender.
- Do not invent a second PR body contract; reuse the ownership and body-shape decisions already fixed in `S0E-5C`, `S0E-5D`, and `S0E-7A`.

## Scope

- `P0`: fix the boundary between secondary-enforcement workflow policy and source-log attribution ownership
- `P1`: define candidate attribution surfaces and precedence for deriving `source_log_path`
- `P2`: define ambiguity handling, fail-closed rules, and representative sample expectations
- `P3`: define the handoff contract back to automatic PR-event mirroring after attribution is proven stable

## Success Criteria (DoD)

- The repo has a written decision that `source_log_path` attribution is a separate prerequisite slice rather than an unowned detail inside `S0E-7A`.
- The repo has a fail-closed boundary for what happens when PR-event attribution is missing or ambiguous.
- A later automatic PR-event proposal can point to one explicit attribution contract instead of re-arguing ownership in the workflow slice.
- The repo has one explicit ordered list of attribution candidate surfaces and does not silently treat PR prose or fuzzy title matching as ownership evidence.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the attribution boundary, candidate input precedence, ambiguity policy, and handoff back to CI rollout
  - at least one representative deterministic attribution sample and one ambiguity sample exist with traceable artifacts
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-4E` is now opened as the direct follow-up after `S0E-7A/P3`, but it is now grouped under the PR-oriented `4x` family because the unresolved problem is PR contract ownership.
- `P0` is now completed: source-log attribution is now explicitly owned as its own slice, and automatic PR-event mirroring remains blocked until this attribution problem is solved deterministically.
- `P1` is now completed: the first allowed attribution surfaces and their precedence are now fixed, so future automatic PR-event mirroring has a bounded candidate set instead of an open-ended search problem.
- `P2-P3` remain open: ambiguity handling and handoff back to automatic CI rollout are not yet completed.

## P0 (Boundary contract | v1)

### P0-C1-S1 (Source-log attribution ownership boundary fixed | v1)

- `S0E-7A/P3` already proved that automatic PR-event mirroring cannot widen safely until the repo can determine the correct `source_log_path` for a PR event.
- That unresolved question is now explicitly moved into `S0E-4E` instead of leaving it as an unowned follow-up note.
- The boundary is now fixed as:
  - `S0E-7A` owns mirror-verifier workflow shape, retained evidence, failure surfacing, and rollout policy;
  - `S0E-4E` owns how a PR event can deterministically identify the single contract-owning source log;
  - automatic rollout remains blocked until `S0E-4E` produces a trustworthy fail-closed attribution rule.
- This prevents a common contract failure mode: trying to widen GitHub Actions triggers before the repo knows which log actually owns the PR contract being verified.

  ## P1 (Attribution candidate surfaces | v1)

  ### P1-C1-S1 (Allowed machine-readable attribution surfaces fixed | v1)

  - `P1` now fixes a bounded candidate set for `PR event -> source_log_path` attribution. The workflow may only consider surfaces that already carry or can mechanically carry source-log ownership without prose interpretation.
  - The allowed candidate surfaces are now fixed as:
    - explicit provenance supplied by a trusted caller or trusted structured payload, where the value is already an exact repo-relative `source_log_path`;
    - the canonical PR body `Links` row `Log: <repo-relative-path>`, because `S0E-4A` and `S0E-5D` already treat that row as the machine-readable PR-owned path back to the source log;
    - exact-ID branch metadata from the PR head ref, such as `pr-prep/s0e-4e`, but only as a constrained fallback that may narrow to one log with the same exact ID.
  - The following surfaces are now explicitly forbidden as ownership claims in `P1`:
    - free-form PR summary prose;
    - title wording beyond exact-ID extraction;
    - labels, milestone, or project fields by themselves;
    - Development Link / development issue refs by themselves;
    - Evidence Footer rows, because they are artifact traceability lines rather than ownership declarations.
  - This keeps attribution tied to structured ownership surfaces that already exist in the repo's PR automation path instead of widening into fuzzy reconstruction from whatever text happened to be rendered on the PR.

  ### P1-C1-S2 (Attribution precedence between allowed surfaces fixed | v1)

  - The first precedence order is now fixed as:
    - `1.` explicit provenance carrying an exact `source_log_path`;
    - `2.` canonical PR-body `Log:` row carrying an exact repo-relative path;
    - `3.` exact-ID branch metadata that can be resolved to one and only one candidate log.
  - Lower-precedence surfaces may only be consulted when every higher-precedence surface is absent, not merely inconvenient.
  - Lower-precedence surfaces may not silently override a higher-precedence ownership claim. If a higher surface exists and a lower surface points elsewhere, that disagreement remains a fail-closed attribution defect for later `P2` handling rather than an excuse to pick whichever one looks better.
  - Exact-ID branch fallback is intentionally narrow:
    - it may extract only one exact requested ID from the head branch naming contract;
    - it must resolve to exactly one plausible source log for that ID;
    - if zero or multiple logs match, branch metadata does not establish ownership.
  - `P1` therefore fixes the core ordering rule for later CI rollout: explicit structured ownership beats PR-body metadata, PR-body metadata beats branch-derived exact-ID fallback, and everything else stays outside the allowed attribution surface set.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0E-4E/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit:
  - consecutive phases: `S0E-4E/P0-P3: pr-event source-log attribution contract`
  - discontinuous phases: `S0E-4E/P0+P3: pr-event source-log attribution contract`
  - mixed discontinuous + consecutive phases: `S0E-4E/P0+P3-P4: pr-event source-log attribution contract`
- When the PR is a non-one-shot follow-up that carries a specific incremental unit, prefer the exact commit-style unit in the title: `S0E-4E/P*-C*-S*: <one-sentence summary>`.

**Branch convention**:

- `S0E-4E` changes should usually stay on the existing `S0E-*` working branch because this slice belongs to the same docs-management spine and is still closing PR-automation governance boundaries rather than a separate domain family.

## Plan (draft)

### P1 (Attribution candidate surfaces)

- [x] `P1-C1-S1`: define which machine-readable surfaces may claim source-log ownership for a PR event
- [x] `P1-C1-S2`: define precedence between explicit provenance, branch metadata, PR metadata, and any fallback candidates

### P2 (Ambiguity and fail-closed policy)

- `P2-C1-S1`: define stop conditions for missing, conflicting, or multi-log attribution
- `P2-C1-S2`: define representative deterministic and ambiguous sample expectations

### P3 (Handoff back to automatic mirroring)

- `P3-C1-S1`: define what attribution output shape `S0E-7A` may consume for future automatic triggers
- `P3-C1-S2`: define when the attribution contract is strong enough to unblock limited automatic PR-event mirroring

## Execution Checklist (unchecked)

### P0 (Boundary contract)

- [x] `P0-C1-S1`: source-log attribution ownership boundary fixed

### P1 (Attribution candidate surfaces)

- [x] `P1-C1-S1`: define candidate source-log ownership surfaces
- [x] `P1-C1-S2`: define attribution precedence

### P2 (Ambiguity and fail-closed policy)

- [ ] `P2-C1-S1`: define ambiguity stop conditions
- [ ] `P2-C1-S2`: define representative sample expectations

### P3 (Handoff back to automatic mirroring)

- [ ] `P3-C1-S1`: define attribution output handoff contract
- [ ] `P3-C1-S2`: define unblocking criteria for limited automatic rollout

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1 (source-log attribution ownership boundary fixed | 2026-03-31)

- headSha: `11402aac`
- artifacts:
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
- expected:
  - the repo should explicitly separate source-log attribution from `S0E-7A` workflow policy and should block automatic PR-event mirroring until attribution becomes deterministic
- observed:
  - `S0E-4E` now fixes that boundary: attribution becomes its own contract slice, and `S0E-7A` no longer carries an unowned dependency for automatic rollout

### P1-C1-S1S2 (allowed attribution surfaces and precedence fixed | 2026-03-31)

- headSha: `5b5c17bf`
- artifacts:
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
  - `docs/logs/log-S0E-5D-body-contract-and-gate-shape-normalization.md`
  - `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  - `scripts/issues/plan_pr_prep.py`
  - `scripts/issues/body_contract.py`
- expected:
  - the repo should define one bounded set of machine-readable ownership surfaces for `PR event -> source_log_path` attribution and should order them without reopening fuzzy title/prose heuristics
- observed:
  - `S0E-4E/P1` now fixes three allowed surfaces and one explicit precedence chain: trusted explicit provenance first, canonical PR-body `Log:` row second, and exact-ID head-branch fallback last; prose-only and metadata-only hints are now excluded from ownership claims

## Recent changes (for traceability, optional)

- 2026-03-31: completed `P1` by fixing the first bounded attribution candidate set and precedence order for future PR-event mirroring.
- 2026-03-31: re-homed this slice from `S0E-7B` to `S0E-4E`, because the unresolved problem is fundamentally PR-contract attribution rather than workflow-retention policy.
- 2026-03-31: opened `S0E-4E` as the dedicated follow-up for deterministic `PR event -> source_log_path` attribution.
- 2026-03-31: completed `P0` by fixing the ownership boundary in one place: attribution is now its own fail-closed prerequisite slice rather than an unresolved note inside `S0E-7A`.