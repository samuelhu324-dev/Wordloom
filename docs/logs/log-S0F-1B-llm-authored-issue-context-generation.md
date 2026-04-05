# log-S0F-1B (Phase 1B: LLM-authored issue Context generation)

---

**id**: `S0F-1B`
**kind**: `log`
**title**: `llm-authored issue Context generation v1`
**status**: `stable`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, GitHub, Workflow, Automation, epic/s0, sub/1b`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/366`
  **pr**: `https://github.com/samuelhu324-dev/wordloom-v3/pull/371`
  **runbook**: ``
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0F-docs-management-v6.md`
  **previous_log**: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
  **reference_log_1**: `docs/logs/log-S0E-2E-issue-conclusion-and-development-linkage-contract.md`
  **reference_log_2**: `docs/logs/log-S0E-4A-github-pr-automation-contract.md`
  **reference_log_3**: `docs/logs/log-S0E-7D-publish-verify-remediation-and-failure-semantics.md`
  **reference_log_4**: `docs/logs/log-S0F-1A-fail-closed-entrypoints-and-preflight-unification.md`
**issue_keyword**: `automation`
**issue_top_labels**: `EVOLUTION`
**issue_scope_labels**: `s0/knowledge system, sub/1`
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
**created**: `2026-04-04`
**updated**: `2026-04-05`

---

## Decision / Outcome

**Decision**:

- `S0F-1B` is the next follow-up slice under `S0F`, and it specifically addresses the issue Context authoring problem exposed after the corrected `S0F-1A` full-auto rerun.
- v1 should stop treating issue Context as a deterministic fact-pool template assembly problem; child and parent issue Context should instead be authored through LLM generation grounded in the corresponding source log.
- The target contract is intentionally narrow: child issue Context must contain exactly four English bullet sentences, top-level parent issue Context must contain exactly five English bullet sentences, and the generator should be allowed to write naturally instead of preserving a fixed rhetorical style such as `carry-forward`, `baseline`, or `later follow-up` wording.

**Default choices (phase defaults / v1)** (optional, but recommended):

- `single-generate` style deterministic template assembly should no longer be the canonical path for issue Context generation.
- The contract should permit LLM-authored Context prose to organize the grounded facts freely, so long as sentence count, English readability, bullet shape, and placeholder hygiene still pass validation.
- Child issue Context must validate at exactly four sentences; top-level parent issue Context must validate at exactly five sentences.
- Context generation failure should fail closed for the current mutation path instead of silently falling back to the older template pool.
- The first rollout should attach to issue conclusion only; create-time issue bodies should continue to keep `Context` structurally present but intentionally empty.
- Batch paths may preserve existing Context blocks when no one-item LLM authoring is explicitly requested; the new LLM generation path should first prove itself on single-item conclusion authoring.
- The generator should be grounded by the issue's source log and any exact-ID merged PR evidence, but it should not be forced into `承上启下` rhetoric or a mandatory future-facing closing sentence.

## PR Summary Inputs (optional)

- Use this block when the log is expected to drive PR creation directly.
- Keep the content human-facing and short; the PR body should summarise scope, not replay commit history.
- `PR Summary Inputs` is the automation-facing contract surface; it should stay compact, deterministic, and free of explanatory prose.

**PR summary bullets**:

- Replace deterministic issue Context template assembly with LLM-authored Context generation grounded in the corresponding source log.
- Tighten the Context shape contract to exact sentence counts: four for child issues and five for top-level parent issues.
- Remove silent template fallback from the canonical issue-conclusion Context generation path so invalid output fails closed instead of reverting to old stock phrasing.
- Keep create-time issue Context structurally present but empty while the first LLM rollout is limited to issue conclusion authoring.
- Remove the retired deterministic Context template builders from the shared contract surface so the canonical paths cannot drift back toward template assembly.
- Retain representative historical rewrite artifacts and prove that the guarded conclusion path can replace legacy deterministic Context blocks on already-closed issues without reopening them.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.
- If the implementation work lands in multiple review units, keep each PR scoped to the exact `P*-C*-S*` unit.

**PR links**:

- Log: `docs/logs/log-S0F-1B-llm-authored-issue-context-generation.md`
- Runbook: ``
- Evidence artifact: `docs/issues/issue-conclusion-S0F-1B-p5-live-summary.json`

## Definitions (optional)

- `LLM-authored Context`: an issue Context block written by a generation step that is grounded in the source log and live evidence, but not forced through a fixed template family.
- `exact sentence-count contract`: a rule requiring top-level parent issue Context to contain exactly five bullet sentences and child issue Context to contain exactly four bullet sentences.
- `template fallback`: any behavior that silently reuses the older deterministic Context template pool after the preferred generation path fails.

## Constraints

- Do not reintroduce deterministic style templates as the hidden fallback for the canonical Context generation path.
- Do not expand the first rollout into create-time live authoring; create should continue to keep `Context` empty until conclusion.
- Do not loosen structural validation so far that placeholder, non-English, or malformed bullet content can pass as valid Context.
- Do not require a `carry-forward`, `baseline`, or `later follow-up` rhetorical pattern just to make generated Context look uniform.

## Scope

- `P0`: contract for LLM-authored Context generation and exact sentence-count validation
- `P1`: replace deterministic Context template assembly in the issue-conclusion path
- `P2`: remove silent template fallback and retain fail-closed generation evidence
- `P3`: keep draft preview create-time Context empty by default and retire draft-side one-item Context generation
- `P4`: remove retired deterministic Context builder surfaces and mark the v1 contract stable
- `P5`: refresh representative historical deterministic Context bodies through the guarded conclusion path and harden the gate against dotted-path false positives

## Success Criteria (DoD)

- Issue conclusion can generate Context from the source log through an LLM-authored path without forcing deterministic template phrasing.
- Child issue Context validates only when it contains exactly four readable English bullet sentences.
- Top-level parent issue Context validates only when it contains exactly five readable English bullet sentences.
- Invalid Context generation no longer falls back silently to the old deterministic template pool.
- The first rollout remains limited to conclusion authoring while create-time issue Context stays structurally present but empty.
- Shared issue-body contract code no longer exports or consumes the retired deterministic Context builder surface.
- Representative historical closed issues can be rewritten through the guarded conclusion remediation path and then preserved by post-refresh verification without new Context drift warnings.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the exact four/five sentence-count contract is enforced for child versus parent issue Context;
  - conclusion-time Context generation no longer depends on the older deterministic template pool;
  - at least one retained issue-conclusion sample proves the LLM-authored path can pass validation without falling back to stock phrasing.

- `S0F-1B` is now `stable` because `P0-P4` are complete: the exact-count contract is enforced, create-time `Context` remains empty, conclusion-time authoring uses the dedicated LLM path, fallback has been removed, and the retired deterministic builder surface has been deleted from the shared contract module.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- `S0F-1B/P<phase>-C<cycle>-S<steps>: <summary>`, where `<steps>` can be a single step (`1`, meaning `...-S1`) or multiple consecutive steps grouped within the same phase / cycle (for example `1S2`, meaning `...-S1S2`).
- When one PR aggregates multiple whole phases, the PR title should compress the phase set instead of repeating every commit unit.

**Branch convention**:

- `S0F-1B` related changes should stay on `S0F-*` working branches, currently `S0F-docs-management-v6`.

**Commit discipline (recommended)**:

- After each meaningful `P*-C*-S*` unit is complete, commit and push promptly on `S0F-docs-management-v6` so the new spine does not drift ahead of origin.

## Plan (draft)

### P0 (Contract)

- P0-C1-S1: define the exact child-versus-parent issue Context sentence-count contract as `4` versus `5`
- P0-C1-S2: define the canonical LLM-authored Context generation boundary and remove deterministic style requirements from the contract

### P1 (Issue conclusion generation)

- P1-C1-S1: replace deterministic Context assembly in issue conclusion with an LLM-authored generation path grounded in the source log
- P1-C1-S2: retain one representative conclusion sample proving the generated Context passes validation without template fallback

### P2 (Fail-closed fallback semantics)

- P2-C1-S1: remove silent template fallback from the canonical conclusion path and make invalid generation fail closed with retained evidence

### P3 (Draft preview follow-up)

- P3-C1-S1: keep draft preview create-time Context empty by default and retire draft-side one-item Context generation

### P4 (Stability cleanup)

- P4-C1-S1: remove the retired deterministic Context builder surface from the shared contract module and retain one stability artifact proving only create-empty plus conclusion-LLM paths remain

### P5 (Historical refresh and post-review hardening)

- P5-C1-S1: make single-item LLM normalization robust when the model compresses multiple sentences into one array item
- P5-C1-S2: retain canonical preview artifacts for representative historical S6B child issues targeted for Context refresh
- P5-C1-S3: rewrite representative historical deterministic Context blocks on closed issues through the guarded conclusion remediation path
- P5-C1-S4: harden the Context gate so dotted file paths do not produce false multi-sentence failures, then retain post-refresh verification artifacts

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: exact child-versus-parent sentence-count contract fixed
- [x] `P0-C1-S2`: deterministic style requirements removed from the canonical Context contract

### P1 (Issue conclusion generation)

- [x] `P1-C1-S1`: issue-conclusion Context generation switched to an LLM-authored path
- [x] `P1-C1-S2`: one representative conclusion sample retained without template fallback

### P2 (Fail-closed fallback semantics)

- [x] `P2-C1-S1`: silent template fallback removed from the canonical conclusion path

### P3 (Draft preview follow-up)

- [x] `P3-C1-S1`: draft preview create-time Context remains empty by default and draft-side one-item generation is retired

### P4 (Stability cleanup)

- [x] `P4-C1-S1`: retired deterministic Context builder surface removed and v1 contract marked stable

### P5 (Historical refresh and post-review hardening)

- [x] `P5-C1-S1`: single-item LLM normalization now tolerates one-item multi-sentence array compression
- [x] `P5-C1-S2`: representative historical S6B preview artifacts retained under `S0F-1B`
- [x] `P5-C1-S3`: closed issues `#357/#358/#359` rewritten through the guarded conclusion remediation path
- [x] `P5-C1-S4`: dotted-path false positives removed from the Context gate and post-refresh verification retained

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this log records the head SHA, key parameters, and artifact paths (or CI run URLs).
- This section is the human-facing ledger and should remain separate from `Evidence Footer Source`.
- Prefer one stable ledger shape per unit: heading with `P*-C*-S*` and date, then `headSha`, `artifacts`, `expected`, and `observed`.

### P0-C1-S1S2 (LLM-authored Context contract fixed | 2026-04-04)

- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/issue_context_llm.py`
  - `scripts/issues/plan_issue_conclusion.py`
  - `scripts/issues/apply_issue_conclusion_with_pre_gate.py`
  - `scripts/issues/plan_publish_verify_remediation_gate.py`
  - `scripts/issues/generate_issue_context_draft.py`
- expected:
  - child issue Context validates only at exactly four sentences while top-level parent issue Context validates only at exactly five sentences
  - the canonical conclusion path no longer depends on deterministic fact-pool template assembly
- observed:
  - `body_contract.py` now enforces an exact `4` versus `5` sentence-count gate for child versus parent issue Context blocks
  - the issue-conclusion planner, guarded apply surface, thin gate passthrough, and single-item Context draft helper now accept `llm-generate` and use the new LLM-backed Context authoring path on conclusion instead of deterministic template assembly
  - create-time issue drafting remains structurally empty for `Context`, so the first rollout boundary still holds while conclusion authoring moves to the LLM-backed path

### P1-C1-S1S2 (representative LLM-authored conclusion sample retained | 2026-04-04)

- artifacts:
  - `docs/issues/issue-conclusion-S0F-1B-p1-sample-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1B-p1-sample-plan.json`
  - `docs/issues/issue-conclusion-S0F-1B-p1-sample-body.md`
- expected:
  - one representative issue-conclusion dry-run proves the new LLM-authored path can generate a valid child-issue Context block without deterministic template fallback
- observed:
  - the retained `S0F-1B` sample for concluded issue `#364` produced an exact four-sentence English Context block through `--context-mode llm-generate`
  - the sample plan records the LLM-authored path explicitly and no longer emits the old deterministic outcome-wording warning family

### P2-C1-S1 (fail-closed generation evidence retained | 2026-04-04)

- artifacts:
  - `docs/issues/issue-conclusion-S0F-1B-p1-sample-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1B-p2-fail-closed.txt`
  - `docs/issues/issue-conclusion-S0F-1A-live-manifest.json`
- expected:
  - the canonical conclusion path should no longer accept `single-generate` as a compatibility shortcut
  - LLM generation failure should stop before any replacement Context plan is emitted instead of falling back silently to deterministic template assembly
- observed:
  - canonical conclusion surfaces now accept only `preserve-existing` or `llm-generate`, and the tracked live `S0F-1A` conclusion manifest now names `llm-generate` explicitly
  - the retained controlled-failure sample exited non-zero on `unknown_model` and wrote the failure output to `issue-conclusion-S0F-1B-p2-fail-closed.txt`, with no fallback plan artifact emitted

### P3-C1-S1 (draft preview remains empty by default | 2026-04-04)

- artifacts:
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/generate_issue_context_draft.py`
  - `docs/issues/issue-S0F-1B-p3-draft-body.md`
  - `docs/issues/issue-S0F-1B-p3-draft-result.json`
  - `docs/issues/issue-context-S0F-1B-p3-draft-rejected.txt`
- expected:
  - create-time draft rendering should keep the `Context` section structurally present but empty by default
  - one-item draft-side Context authoring should no longer offer a draft-phase generation path
- observed:
  - `gen_issue_draft.py` now accepts only `--context-mode scaffold`, and the retained `S0F-1B` draft sample leaves `## Context` empty while emitting the existing create-time warning that substantive Context belongs to issue conclusion
  - `generate_issue_context_draft.py` now exposes only `--phase conclusion`, and the retained rejection artifact shows that `--phase draft` is refused at the CLI boundary instead of silently reintroducing a draft-side generation path

### P4-C1-S1 (deterministic builder surface removed and contract stabilized | 2026-04-04)

- artifacts:
  - `scripts/issues/body_contract.py`
  - `scripts/issues/issue_context_llm.py`
  - `scripts/issues/gen_issue_draft.py`
  - `scripts/issues/generate_issue_context_draft.py`
  - `docs/issues/issue-context-S0F-1B-p4-stability.json`
- expected:
  - the shared contract module should no longer export the retired deterministic draft or conclusion Context builders
  - the only remaining canonical Context paths should be create-time empty scaffolding and conclusion-time LLM authoring under the exact four/five sentence-count contract
- observed:
  - `body_contract.py` no longer contains the retired deterministic fact-pool/template builder helpers, so the shared issue-body contract no longer exposes a hidden fallback surface for draft or conclusion Context generation
  - the retained stability artifact records that `single-generate`, `build_issue_draft_context_lines`, and `build_issue_conclusion_context_lines` are absent from `scripts/issues/**`, while the canonical remaining surfaces are `gen_issue_draft.py --context-mode scaffold` and `generate_issue_context_draft.py --phase conclusion --context-mode llm-generate`

### P5-C1-S1S2S3S4 (historical deterministic Context refreshes retained and re-verified | 2026-04-04)

- artifacts:
  - `scripts/issues/issue_context_llm.py`
  - `scripts/issues/body_contract.py`
  - `docs/issues/issue-context-S0F-1B-p5-s6b-1a-preview.md`
  - `docs/issues/issue-context-S0F-1B-p5-s6b-1a-preview.json`
  - `docs/issues/issue-context-S0F-1B-p5-s6b-1b-preview.md`
  - `docs/issues/issue-context-S0F-1B-p5-s6b-1b-preview.json`
  - `docs/issues/issue-context-S0F-1B-p5-s6b-1c-preview.md`
  - `docs/issues/issue-context-S0F-1B-p5-s6b-1c-preview.json`
  - `docs/issues/lifecycle-audit-S0F-1B-p5-s6b-1a-manifest.json`
  - `docs/issues/lifecycle-audit-S0F-1B-p5-s6b-1b-manifest.json`
  - `docs/issues/lifecycle-audit-S0F-1B-p5-s6b-1c-manifest.json`
  - `docs/issues/lifecycle-remediation-S0F-1B-p5-s6b-1a-issue-conclusion-manifest.json`
  - `docs/issues/lifecycle-remediation-S0F-1B-p5-s6b-1b-issue-conclusion-manifest.json`
  - `docs/issues/lifecycle-remediation-S0F-1B-p5-s6b-1c-issue-conclusion-manifest.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1a-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1b-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1c-guarded-result.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1a-live.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1b-live.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1c-live.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1a-post-verify-plan.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1b-post-verify-plan.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-s6b-1c-post-verify-plan.json`
  - `docs/issues/issue-conclusion-S0F-1B-p5-live-summary.json`
- expected:
  - the one-item LLM authoring path should remain exact-count valid even when the model compresses multiple sentences into one JSON array element
  - three representative historical child issues with deterministic Context bodies should be rewritten through the guarded conclusion remediation path and remain closed after apply
  - post-refresh verification should preserve the rewritten live Context blocks without reintroducing Context-gate drift, including cases where dotted file paths appear inside a valid single sentence
- observed:
  - `issue_context_llm.py` now normalizes one compressed array element into exact sentence rows when the model returns multiple sentences inside a single `lines` item, which allowed `S6B-1B` to produce a canonical four-line preview artifact instead of failing the exact-count gate
  - issues `#357`, `#358`, and `#359` were rewritten in place through `apply_issue_conclusion_with_pre_gate.py` using remediation-derived manifests and explicit merged-PR overrides `#360/#361/#362`, with each guarded result recording `allowed-via-targeted-conclusion-remediation` and `issue was already closed before apply; body updated in place`
  - `body_contract.py` now detects true multi-sentence boundaries instead of counting every period character, so the `S6B-1C` line containing `artifacts/s2b.write-gate.runs.latest.json` no longer triggers a false Context-gate failure during post-refresh verification
  - the retained live snapshots and post-verify plans show that all three refreshed issues now preserve their live Context blocks under `preserve-existing` without the old deterministic template wording returning as a follow-up drift artifact

## Recent changes (for traceability, optional)

- 2026-04-04: created `S0F-1B` as the dedicated follow-up slice for replacing deterministic issue Context templates with LLM-authored Context generation under an exact child/main sentence-count contract.
- 2026-04-04: completed `P0` by changing the Context validator to exact child/main sentence counts and wiring a new GitHub Models-backed LLM Context generator into the canonical issue-conclusion path.
- 2026-04-04: completed `P1` by retaining one representative conclusion sample for `S0F-1A` that generated a valid four-sentence child issue Context block through `llm-generate` without falling back to deterministic template assembly.
- 2026-04-04: completed `P2` by removing the remaining `single-generate` compatibility path from canonical conclusion surfaces and retaining one controlled fail-closed sample that stops on LLM generation error instead of falling back to the older deterministic Context builder.
- 2026-04-04: completed `P3` by keeping create-time draft `Context` empty by default, retiring draft-side one-item Context generation, and retaining both a positive empty-draft sample and a CLI rejection artifact for the removed `--phase draft` surface.
- 2026-04-04: completed `P4` by deleting the retired deterministic Context builder surface from `body_contract.py`, retaining one stability artifact that records the remaining canonical paths, and marking `S0F-1B` stable.
- 2026-04-04: completed `P5` by retaining canonical historical preview artifacts for `S6B-1A/#357`, `S6B-1B/#358`, and `S6B-1C/#359`, rewriting all three live issues through the guarded conclusion remediation path, and then hardening both LLM normalization and the Context gate so post-refresh verification preserves the new prose without false dotted-path failures.