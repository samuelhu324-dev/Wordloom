# log-S0E-4E (Phase 4E: PR-event source-log attribution contract)

---

**id**: `S0E-4E`
**kind**: `log`
**title**: `contract/pr-event source-log attribution contract v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Actions, Automation, Contract, PR, epic/s0, sub/1`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/326`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/328`
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
**updated**: `2026-04-03`

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
- The repo has one explicit ambiguity policy that classifies missing, conflicting, and multi-candidate attribution as stop conditions rather than soft warnings.
- The repo has one explicit handoff payload shape that tells `S0E-7A` whether it may continue to mirror verification or must stop before verification starts.

## Stability (what stable means)

- This log can be marked `stable` when:
  - `P0-P3` have fixed the attribution boundary, candidate input precedence, ambiguity policy, and handoff back to CI rollout
  - at least one representative deterministic attribution sample and one ambiguity sample exist with traceable artifacts
  - the Evidence section includes traceable `headSha` values plus artifact paths (or CI run URLs)

## Current Status

- `S0E-4E` is now opened as the direct follow-up after `S0E-7A/P3`, but it is now grouped under the PR-oriented `4x` family because the unresolved problem is PR contract ownership.
- `P0` is now completed: source-log attribution is now explicitly owned as its own slice, and automatic PR-event mirroring remains blocked until this attribution problem is solved deterministically.
- `P1` is now completed: the first allowed attribution surfaces and their precedence are now fixed, so future automatic PR-event mirroring has a bounded candidate set instead of an open-ended search problem.
- `P2` is now completed: the first ambiguity stop conditions and representative sample expectations are now fixed, so attribution defects are classified as explicit fail-closed outcomes instead of vague review notes.
- `P3` is now completed: the handoff payload shape and limited automatic-rollout unblocking criteria are now fixed, so `S0E-7A` has an explicit consume-or-stop contract instead of an informal dependency on attribution prose.
- The latest full-auto live cycle is now closed end to end on the live path: issue `#326` was created, remediated to pass lifecycle gates, carried by merged PR `#328`, and then updated in place with the final issue-conclusion body.
- Exact-ID merged PR selection for `S0E-4E` resolves to one-item set `#328`, and live issue `#326` now remains in `CLOSED` state with final DoD short ref `#328`.

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

## P2 (Ambiguity and fail-closed policy | v1)

### P2-C1-S1 (Ambiguity stop conditions fixed | v1)

- `P2` now fixes the first fail-closed ambiguity taxonomy for `PR event -> source_log_path` attribution. Attribution defects are stop conditions, not advisory warnings.
- The stop conditions are now fixed as:
  - `missing-attribution`: no allowed attribution surface yields an exact repo-relative `source_log_path`;
  - `conflicting-attribution`: two allowed surfaces yield different ownership claims, including higher-vs-lower precedence disagreement;
  - `multi-candidate-attribution`: branch-derived exact-ID fallback narrows to more than one plausible source log;
  - `invalid-attribution-shape`: an allowed surface exists but does not carry one exact repo-relative log path in canonical form.
- The fail-closed policy is now fixed as:
  - no ambiguity class may degrade to a soft pass or warning-only result;
  - later CI mirroring must stop before contract verification if attribution is missing, conflicting, multi-candidate, or structurally invalid;
  - the workflow may report all detected ambiguity classes, but it may not pick one source log optimistically once any stop condition exists.
- Higher-precedence disagreement is intentionally strict:
  - if explicit provenance and PR-body `Log:` row disagree, the result is `conflicting-attribution`;
  - if PR-body `Log:` row and branch fallback disagree, the result is also `conflicting-attribution` rather than letting the lower surface silently lose without traceability.
- This preserves the main boundary established by `S0E-7A/P3`: automatic PR-event mirroring should fail because ownership is unclear, not continue under a guessed source log.

### P2-C1-S2 (Representative deterministic and ambiguity sample expectations fixed | v1)

- `P2` now fixes the minimum sample expectations that later automation or CI rollout must satisfy before attribution can be considered stable enough for handoff.
- The first representative sample set is now fixed as:
  - one deterministic sample where exactly one contract owner is resolved and every consulted allowed surface agrees on the same `source_log_path`;
  - one ambiguity sample where attribution stops before verification because ownership is missing, conflicting, multi-candidate, or invalid in shape.
- The deterministic sample must prove all of the following:
  - the resolved `source_log_path` is exact and repo-relative;
  - the winning ownership surface is recorded explicitly;
  - any consulted lower-precedence surfaces either agree or are absent.
- The ambiguity sample must prove all of the following:
  - the workflow reports which ambiguity class caused the stop;
  - no PR contract verification proceeds under a guessed source log;
  - retained evidence is sufficient to explain why attribution stopped without consulting raw runner logs as the primary source of truth.
- `P2` does not yet require a full automatic `pull_request` rollout sample. The representative goal is narrower: prove that attribution can distinguish one clean deterministic case from one fail-closed ambiguous case with traceable evidence.

## P3 (Handoff back to automatic mirroring | v1)

### P3-C1-S1 (Attribution output handoff contract fixed | v1)

- `P3` now fixes the structured handoff payload that any future automatic attribution step must emit before `S0E-7A` may invoke the mirror verifier.
- The first handoff shape is now fixed as one machine-readable result payload with these minimum fields:
  - `mode`: fixed identifier for attribution-output payloads;
  - `result`: one of `resolved`, `stop-missing-attribution`, `stop-conflicting-attribution`, `stop-multi-candidate-attribution`, or `stop-invalid-attribution-shape`;
  - `repository`: repository slug used for PR-event inspection;
  - `pr_ref`: the PR number or URL being evaluated;
  - `pr_url`: canonical PR URL when it is available;
  - `source_log_path`: exact repo-relative path only when `result = resolved`, otherwise blank;
  - `winning_surface`: one of `explicit-provenance`, `pr-body-log-row`, `exact-id-branch-fallback`, or blank when attribution does not resolve;
  - `consulted_surfaces`: ordered list of the allowed surfaces actually inspected;
  - `stop_reason`: exact ambiguity class when the result is a stop outcome, otherwise blank;
  - `eligible_for_secondary_enforcement`: boolean that is true only when attribution resolved to one exact owner and false for every stop outcome.
- The handoff rule back to `S0E-7A` is now fixed as:
  - `S0E-7A` may continue to mirror verification only when `eligible_for_secondary_enforcement = true`, `result = resolved`, and `source_log_path` is present in exact repo-relative form;
  - otherwise `S0E-7A` must stop before contract verification begins and surface the attribution stop through its retained evidence and operator-facing status.
- This keeps the boundary explicit: `4E` resolves ownership, while `7A` verifies the PR body only after ownership is already trustworthy enough to consume as an input.

### P3-C1-S2 (Limited automatic-rollout unblocking criteria fixed | v1)

- `P3` now fixes what must be true before the repo may widen from manual attribution replay into limited automatic PR-event mirroring.
- The unblocking criteria are now fixed as:
  - the attribution step can emit the `P3` handoff payload in both a resolved case and a stop case without falling back to prose-only explanations;
  - at least one representative resolved sample shows that `S0E-7A` can consume the emitted `repository + pr_ref + source_log_path` tuple directly without any extra operator-supplied ownership hint;
  - at least one representative stop sample shows that `S0E-7A` halts before verifier execution and preserves the attribution stop reason as retained evidence rather than converting it into a verifier failure;
  - the resolved-vs-stop boundary is deterministically derived from the allowed attribution surfaces only, not from labels, title prose, or human triage after the run starts;
  - retained evidence is sufficient to reconstruct whether the workflow stopped in attribution or failed later in mirror verification.
- Even after these conditions are met, the first widening should still be intentionally limited:
  - prefer one narrow PR-event surface first rather than all `pull_request` activity at once;
  - keep attribution as the gating stage ahead of verification rather than collapsing both into one opaque workflow outcome.
- `P3` therefore closes the current slice with one explicit consume-or-stop interface and one explicit bar for limited automatic rollout. A later implementation slice may wire that interface into GitHub Actions, but it should not need to re-argue attribution ownership semantics.

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

- [x] `P2-C1-S1`: define stop conditions for missing, conflicting, or multi-log attribution
- [x] `P2-C1-S2`: define representative deterministic and ambiguous sample expectations

### P3 (Handoff back to automatic mirroring)

- [x] `P3-C1-S1`: define what attribution output shape `S0E-7A` may consume for future automatic triggers
- [x] `P3-C1-S2`: define when the attribution contract is strong enough to unblock limited automatic PR-event mirroring

## Execution Checklist (unchecked)

### P0 (Boundary contract)

- [x] `P0-C1-S1`: source-log attribution ownership boundary fixed

### P1 (Attribution candidate surfaces)

- [x] `P1-C1-S1`: define candidate source-log ownership surfaces
- [x] `P1-C1-S2`: define attribution precedence

### P2 (Ambiguity and fail-closed policy)

- [x] `P2-C1-S1`: define ambiguity stop conditions
- [x] `P2-C1-S2`: define representative sample expectations

### P3 (Handoff back to automatic mirroring)

- [x] `P3-C1-S1`: define attribution output handoff contract
- [x] `P3-C1-S2`: define unblocking criteria for limited automatic rollout

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

### P2-C1-S1S2 (ambiguity stop conditions and sample expectations fixed | 2026-03-31)

- headSha: `3d4d4b1b`
- artifacts:
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `docs/logs/log-S0E-5A-lifecycle-audit-gate-and-dry-run-planner.md`
  - `docs/logs/log-S0E-5C-guarded-pr-create-decomposition.md`
- expected:
  - the repo should classify missing, conflicting, and multi-candidate attribution as explicit stop conditions, and it should state the minimum deterministic vs ambiguity samples required before future rollout widening
- observed:
  - `S0E-4E/P2` now fixes both the stop taxonomy and the first sample expectations: missing/conflicting/multi-candidate/invalid-shape attribution all stop before verification, and later rollout must be able to show one deterministic owner case plus one fail-closed ambiguity case with retained evidence

### P3-C1-S1S2 (handoff payload shape and rollout unblocking criteria fixed | 2026-03-31)

- headSha: `113fc2e4`
- artifacts:
  - `docs/logs/log-S0E-4E-pr-event-source-log-attribution-contract.md`
  - `docs/logs/log-S0E-7A-github-actions-secondary-enforcement.md`
  - `.github/workflows/s0e-pr-body-secondary-enforcement.yml`
  - `scripts/issues/create_pr_from_plan.py`
- expected:
  - the repo should define one structured attribution result payload that `S0E-7A` can consume directly, and it should state what evidence boundary must be met before limited automatic PR-event mirroring is allowed to widen
- observed:
  - `S0E-4E/P3` now fixes both: future attribution must emit one consume-or-stop payload with explicit `result`, `source_log_path`, `winning_surface`, and `eligible_for_secondary_enforcement` semantics, and limited rollout widening now requires one resolved handoff sample plus one attribution-stop sample that halts before mirror verification

## Recent changes (for traceability, optional)

- 2026-04-03: resumed `S0E-4E` after review, confirmed PR `#328` merged, generated the single-item conclusion preview from exact-ID merged PR evidence, and wrote the final conclusion body back to already-closed live issue `#326` in place.
- 2026-04-03: created live issue `#326`, refreshed its single-generated Context, attached the expected sidebar parent relationship to `#248`, and opened ready-for-review PR `#328`; full-auto now pauses at the human merge boundary before any later issue-conclusion step.
- 2026-03-31: completed `P3` by fixing the attribution handoff payload shape and the limited automatic-rollout unblocking criteria for future PR-event mirroring.
- 2026-03-31: completed `P2` by fixing ambiguity stop conditions and the first deterministic-versus-ambiguous sample expectations for future PR-event mirroring.
- 2026-03-31: completed `P1` by fixing the first bounded attribution candidate set and precedence order for future PR-event mirroring.
- 2026-03-31: re-homed this slice from `S0E-7B` to `S0E-4E`, because the unresolved problem is fundamentally PR-contract attribution rather than workflow-retention policy.
- 2026-03-31: opened `S0E-4E` as the dedicated follow-up for deterministic `PR event -> source_log_path` attribution.
- 2026-03-31: completed `P0` by fixing the ownership boundary in one place: attribution is now its own fail-closed prerequisite slice rather than an unresolved note inside `S0E-7A`.