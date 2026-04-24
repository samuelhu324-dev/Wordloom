# log-S0G-3B (Phase 3B: carrier branch cleanup and mainline extraction governance)

---

**id**: `S0G-3B`
**kind**: `log`
**title**: `carrier branch cleanup and mainline extraction governance v1`
**status**: `draft`
**scope**: `S0`
**tags**: `EVOLUTION, Docs, Workflow, Automation, Evidence, epic/s0, sub/3b`
**links**: ``
  **issue**: `https://github.com/samuelhu324-dev/wordloom-v3/issues/536`
  **pr**: "https://github.com/samuelhu324-dev/wordloom-v3/pull/537"
  **runbook**: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
  **roadmap**: `docs/roadmap/road-002-projection-runtime-platformization-and-evidence-governance.md`
  **parent_log**: `docs/logs/log-S0G-docs-management-v7.md`
  **previous_log**: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
  **reference_log_1**: `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
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
**reviewed**: `pending`

---

## Frontmatter Lifecycle-Time Rule

- `created`, `updated`, and optional `reviewed` are the minimum artifact-lifecycle fields for this packet.
- Day-level precision is acceptable while the carrier-cleanup and extraction rule is still being fixed.
- `reviewed` should remain `pending` until the extraction order, transition rule, and post-transition branch discipline are explicit enough to drive later packet handling.

## Decision / Outcome

**Decision**:

- `S0G-3B` opens the next bounded follow-up after `S0G-3A`: fix how the repo should recover from a long-lived carrier branch that mixes patch/release/governance work, branch-only historical commits, and commits that are already represented on `main` through equivalent PR merges.
- The transition rule is two-stage rather than one-stage: do not say only "always branch from main" while `main` still lacks bounded packets that live only on the current carrier; first inventory and extract the remaining non-main packets, then let `main` resume as the default clean base.
- `S0G-docs-management-v7` should now be treated as a historical carrier and extraction source, not as the long-term default branch for new bounded packets.
- During the transition period, new packet work should be opened from fresh short-lived extraction branches off `main`, then populated only by the minimum cherry-picked bounded packet required for that PR.
- The first cleanup priority is not generic history beautification; it is to classify `S0G` branch history into patch-equivalent noise, already-merged-but-non-identical history, and truly unresolved packet content that still needs its own PR or explicit discard decision.
- The first current-tail inventory is now fixed for the newest meaningful packet families near the carrier head: `S0G-2B`, `S0G-3A`, `RUN-LEDGER-PATCH-001`, the post-merge `S4F` write-back/accounting tail, and `S0G-3B` itself.
- The current recommended extraction order is dependency-first rather than recency-first: extract `S0G-2B` first, then `S0G-3A`, then `RUN-LEDGER-PATCH-001`; keep the `S4F` write-back/accounting tail attached to `RUN-LEDGER-PATCH-001` unless later evidence shows residual packet content outside that patch packet; extract `S0G-3B` after the first tail extractions are no longer changing the rule.

**Default choices (phase defaults / v1)**:

- Use `git log --cherry --left-right origin/main...<carrier-branch>` as the default first-pass inventory for carrier cleanup, because it separates patch-equivalent history from true branch-only history better than raw `git log HEAD --not main`.
- Do not rewrite or rebase the historical carrier branch merely to make it prettier once it has already served as a published backfill/reference branch.
- Before opening any new object-first packet from `main`, explicitly classify whether the desired content already exists only on the carrier branch and therefore needs extraction first.
- If a bounded packet is still missing from `main`, extract it to a fresh `main`-based short branch and open a focused PR; do not continue piling unrelated work onto the carrier branch.
- If a commit is only patch-equivalent noise because its effect already exists on `main`, treat it as carrier history and do not spend a new PR on it.
- If any `issue_*` field is blank, automation must leave it blank and ask for human confirmation instead of inferring a keyword, labels, or milestone.
- If any `pr_*` field is blank, PR automation must leave that PR field blank and report it explicitly instead of copying issue metadata by guesswork.

## PR Summary Inputs (optional)

- This packet is expected to drive later extraction and branch-discipline work, so the review summary should focus on transition order, carrier cleanup boundaries, and the rule for when `main` is trustworthy again as a packet base.

**PR summary bullets**:

- Fix one transition rule for moving from a mixed historical carrier branch to fresh `main`-based bounded packet branches without losing still-unmerged packet content.
- Classify carrier history into patch-equivalent noise, already-landed lineage, and truly unresolved packet content before opening more PRs.
- Record that extraction, not branch beautification, is the first cleanup action when the carrier branch still contains real non-main packet content.

**PR checklist source**:

- Default source: reuse this log's execution checklist for the generated PR checklist block.

**PR links**:

- Log: `docs/logs/log-S0G-3B-carrier-branch-cleanup-and-mainline-extraction-governance.md`
- Runbook: `docs/runbook/run-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- Evidence artifact: ``

**Evidence Footer Source**:

- `P0-C1-S1` | artifact: `git log --cherry --left-right origin/main...S0G-docs-management-v7`

## Definitions (optional)

- **carrier branch**: a long-lived mixed branch that preserved real work and traceability at one stage, but is no longer a good default source for new bounded PRs because it also carries unrelated or already-landed history.
- **patch-equivalent noise**: commits that still appear in branch-only history, but whose effective change already exists on `main` through a different commit identity or merged PR path.
- **extraction branch**: a fresh short-lived branch cut from `main` whose only purpose is to carry one bounded packet cherry-picked out of a historical carrier.
- **transition period**: the temporary interval during which `main` is the target clean base, but not yet the full factual source for all desired packets because older carrier-only packets still need extraction or explicit discard.

## Constraints

- Do not assume that `main` is immediately sufficient as a factual base while real bounded packets still exist only on the historical carrier.
- Do not reopen old S4F or S0F issue/PR packets blindly just because their commits still appear in the carrier branch history.
- Do not use cherry-pick as a permanent primary workflow for all future work; use it only as a bounded extraction tool during the transition off the carrier branch.
- Do not mix a new bounded runbook/release/patch packet with unrelated source-log cleanup simply because both happen to live on the same historical carrier branch.

## Scope

- `P0`: classify carrier history relative to `main`
- `P1`: define extraction order for unresolved packet content
- `P2`: define short-lived branch rules during the transition period
- `P3`: define post-transition steady-state branch discipline

## Success Criteria (DoD)

- One explicit rule states when a historical carrier branch must stop being the default base for new work.
- One explicit rule states how to distinguish patch-equivalent carrier noise from truly unresolved non-main packet content.
- One explicit extraction order exists for the current `S0G` situation: unresolved packet inventory first, focused extraction branches second, new work only after that.
- One explicit transition rule states when `main` becomes trustworthy again as the default clean base for future bounded packets.
- The lane leaves behind a practical operator sequence that can be reused the next time a mixed carrier branch appears.

## Stability (what stable means)

- This log can be marked `stable` when:
  - the current `S0G` carrier inventory rule is explicit;
  - the extraction order for unresolved packets is explicit;
  - the post-transition branch discipline is explicit;
  - the repo no longer needs to guess whether to keep working on the carrier branch or extract from it.

## P0 (Contract | v1)

### P0-C1-S1 (Carrier history classification rule | v1)

- Use `git log --cherry --left-right origin/main...<carrier-branch>` as the first classifier.
- Treat `=` rows as patch-equivalent history that should not trigger a new PR by default.
- Treat `>` rows as branch-only history that still needs packet classification before any discard, extraction, or follow-up PR decision is made.

### P0-C1-S2 (Mainline trust restoration rule | v1)

- `main` becomes the default clean base only after the desired unresolved packets from the carrier branch are either:
  - extracted into focused PRs and merged, or
  - explicitly declared historical/no-op and left on the carrier as non-actionable history.
- Before that point, `main` is still the correct base for extraction branches, but not yet proof that no desired packet remains outside it.

### P0-C1-S3 (Current S0G transition baseline | v1)

- The current `S0G` branch already contains patch-equivalent history plus a large amount of true branch-only history.
- That means the immediate next action is not more feature work on `S0G`; it is bounded packet inventory and extraction planning.
- The first inventory focus should be the still-meaningful packet families nearest the current tail, such as post-merge `S4F` write-back/accounting lineage, runbook-family governance packets, and any residual branch-only packet that the user still wants on `main`.

## P1 (Inventory | v1)

### P1-C1-S1 (Current-tail packet inventory | 2026-04-21)

- `S0G-2B`
  - status: `still unresolved and needs extraction`
  - reason: the carrier still holds both the broad runbook legacy/root-stub relocation commit and the follow-up support-only patch-ledger contract fix, and both remain on the branch-only side of the classifier.
  - recommendation: treat `S0G-2B` as the first extraction candidate because later governance and packet placement rules already depend on this support-only/legacy placement decision.
- `S0G-3A`
  - status: `still unresolved and needs extraction`
  - reason: the release-issue concentration and object-first naming write-back is still branch-only and touches only a narrow governance surface plus the parent issue draft artifacts.
  - recommendation: extract immediately after `S0G-2B`; it is a small governance packet and should land before more fresh packet branching depends on it.
- `RUN-LEDGER-PATCH-001`
  - status: `still unresolved and needs extraction`
  - reason: the packet remains branch-only and owns one bounded workflow-family patch set: `S4F` close-out write-back, patch-ledger accounting updates, and the two guarded script fixes.
  - recommendation: extract after `S0G-2B` and `S0G-3A`; keep it as one object-first packet rather than splitting scripts, accounting, and close-out into separate PRs.
- `S4F` post-merge write-back/accounting tail
  - status: `represented by a later unresolved packet`
  - reason: the newest `S4F-2A/2B/2C` live-link and footer-cleanup commits touch the same `S4F` log surfaces that were later rewritten again by `RUN-LEDGER-PATCH-001`.
  - recommendation: do not open a separate `S4F` extraction packet first; move this tail with `RUN-LEDGER-PATCH-001` unless a later residual-diff check proves meaningful `S4F` content still exists outside that packet.
- `S0G-3B`
  - status: `still unresolved and needs extraction`
  - reason: this governance packet exists only on the carrier and now owns the transition rule itself.
  - recommendation: keep using `S0G-3B` as the inventory/control surface while current-tail extraction is being fixed, then extract it as a narrow source-log packet once the first extraction order no longer needs daily rewrites.

### P1-C1-S2 (Recommended first extraction order | 2026-04-21)

- `1. S0G-2B`
  - foundation packet for support-only ledger placement, patch-ledger bridge contract, and root-stub legacy relocation.
- `2. S0G-3A`
  - small governance write-back packet that should land before the repo relies on object-first release/ledger naming as the steady rule.
- `3. RUN-LEDGER-PATCH-001`
  - bounded workflow-family packet that already absorbs the actionable `S4F` close-out tail and the two guarded script repairs.
- `4. S0G-3B`
  - transition-governance packet that should be extracted after the first three packets stop changing the operator rule.

### P1-C1-S3 (Carrier-only set for now | 2026-04-21)

- Leave older patch-equivalent `S4F-1A` history on the carrier for now when the classifier already marks it as `=`.
- Leave older pre-tail historical `S0F` residue untouched until the current-tail bounded packets are exhausted; the repo should not widen this cleanup round into a full historical archaeology pass.

## P2 (Extraction order | v1)

### P2-C1-S1 (Current-tail extraction sequencing rule | v1)

- Extract dependency-bearing governance and placement packets before family-specific workflow patch packets.
- When a later packet rewrites the same file surfaces as an earlier post-merge write-back tail, prefer extracting the later owning packet rather than reopening the smaller intermediate write-back commits as a separate lane.
- Keep one packet per extraction branch; do not combine `S0G-2B`, `S0G-3A`, and `RUN-LEDGER-PATCH-001` into one cleanup PR merely because they all live on the same carrier.

### P2-C1-S2 (Current-tail leave-behind rule | v1)

- Leave patch-equivalent rows and pre-tail historical residue on the carrier until the current-tail unresolved set has either landed on `main` or been explicitly discarded.
- Do not spend extraction effort on the intermediate `S4F` write-back/accounting commits while the later `RUN-LEDGER-PATCH-001` packet already owns the same close-out surfaces.

## Numbering

- `S<n>`: Step.
- `C<n>`: Cycle.

**Commit / PR naming**:

- Source-log work inside this lane still uses `S0G-3B/P<phase>-C<cycle>-S<steps>: <summary>`.
- Any extraction PR opened because of this lane should use the object-first or source-log-first naming that matches the extracted packet itself, not a generic cleanup title.

**Branch convention**:

- During the transition period, do not keep opening new packet work directly on `S0G-docs-management-v7`.
- Open fresh extraction branches from `main` for each unresolved bounded packet, using the narrowest packet-meaningful name.
- Once transition cleanup is complete, return to the `S0G-3A` rule: source-log packets on `Sx-*` short branches, runbook/release/ledger/patch packets on object-first short branches.

**Commit discipline (recommended)**:

- Treat carrier cleanup as inventory-first, not rewrite-first.
- When one unresolved bounded packet is identified, extract only that packet to a fresh branch and `commit/push` only the minimum necessary content for that packet.
- Do not batch unrelated unresolved packets together merely because they came from the same historical carrier.

## Plan (draft)

### P3 (Steady state)

- P3-C1-S1: return future new work to fresh `main`-based short branches after unresolved packet extraction is complete

## Execution Checklist (unchecked)

### P0 (Contract)

- [x] `P0-C1-S1`: carrier history classification rule fixed
- [x] `P0-C1-S2`: mainline trust restoration rule fixed
- [x] `P0-C1-S3`: current S0G transition baseline recorded

### P1 (Inventory)

- [x] `P1-C1-S1`: current carrier history classified
- [x] `P1-C1-S2`: unresolved packet candidates listed

### P2 (Extraction order)

- [x] `P2-C1-S1`: extraction order fixed for current-tail packets
- [x] `P2-C1-S2`: carrier-only historical set declared

## Current Status (recommended)

- `S0G-3B` is now the active discussion surface for transitioning away from `S0G-docs-management-v7` as a working branch without losing still-unmerged packet content.
- The immediate problem is not only duplicate-looking history: `git log --cherry --left-right origin/main...S0G-docs-management-v7` already shows a very large branch-only set, so `S0G` must be treated as a real carrier inventory problem rather than a cosmetic history cleanup task.
- The first current-tail inventory is now explicit: `S0G-2B`, `S0G-3A`, and `RUN-LEDGER-PATCH-001` are still unresolved extraction candidates; the intermediate `S4F` write-back/accounting tail should move with `RUN-LEDGER-PATCH-001`; `S0G-3B` itself should extract after the first tail packets stabilize.
- Until those first extraction candidates are handled, `main` should be treated as the clean extraction base, but not yet as proof that every desired packet already exists there.

## Evidence (reserved)

- Artifacts are the source of truth for evidence; this packet records the carrier-vs-main classification evidence and the resulting extraction rules.

### P0-C1-S1 (carrier history shows real non-main tail, not just duplicate-looking noise | 2026-04-21)

- headSha: `7b6c7f70d`
- artifacts:
  - `git log --cherry --left-right --oneline origin/main...S0G-docs-management-v7`
- expected:
  - the current carrier should contain both patch-equivalent rows and true branch-only rows, so later cleanup can distinguish noise from unresolved content.
- observed:
  - the current classifier returned at least one patch-equivalent row and a large true branch-only tail; the first pass count for `>` rows was `489`, which is enough to prove that this is not a cosmetic branch divergence problem.

### P0-C1-S2 (current-tail S0G and S4F packets still appear as branch-only history on the carrier | 2026-04-21)

- headSha: `7b6c7f70d`
- artifacts:
  - `git log --cherry --left-right --oneline origin/main...S0G-docs-management-v7`
  - `docs/logs/log-S0G-3A-runbook-release-issue-concentration-and-ledger-naming-governance.md`
  - `docs/runbook/support-only/ledger-run-PATCH-001-WORKFLOW-GITHUB-001-GitHub-Issues-full-auto-pipeline.md`
- expected:
  - the recent tail should still show bounded packet candidates near the carrier head, even if older historical rows also exist.
- observed:
  - the current tail includes recent `S0G-2B`, `S0G-3A`, `RUN-LEDGER-PATCH-001`, and post-merge `S4F` write-back rows, which confirms that extraction planning should start from the newest bounded packets rather than from the oldest historical carrier residue.

### P1-C1-S1 (current-tail packet inventory fixed to actionable categories | 2026-04-21)

- headSha: `975b25a4d`
- artifacts:
  - `git log --cherry --left-right --oneline origin/main...S0G-docs-management-v7 | Select-String 'S0G-2B|S0G-3A|S0G-3B|RUN-LEDGER-PATCH-001|S4F'`
  - `git show --stat --summary --name-only 3ae6b7c63`
  - `git show --stat --summary --name-only 7dc6cad50`
  - `git show --stat --summary --name-only 19f503173`
  - `git show --stat --summary --name-only 975b25a4d`
  - `git show --stat --summary --name-only 7b6c7f70d`
  - `git show --stat --summary --name-only 50110222e`
  - `git show --stat --summary --name-only 8a80ad2dc`
  - `git show --stat --summary --name-only a0e006693`
  - `git show --stat --summary --name-only 2e7ca7cda`
  - `git show --stat --summary --name-only 2516578c9`
- expected:
  - the current-tail packet candidates should separate into three useful categories: direct extraction candidates, tail commits already absorbed by a later unresolved packet, and older carrier-only history that can be left untouched for now.
- observed:
  - `S0G-2B`, `S0G-3A`, `RUN-LEDGER-PATCH-001`, and `S0G-3B` remain direct extraction candidates.
  - the intermediate `S4F-2A/2B/2C` write-back/accounting tail touches the same `S4F` log files later rewritten by `RUN-LEDGER-PATCH-001`, so it should move with that later packet rather than open its own extraction lane first.

### P2-C1-S1 (current-tail extraction order fixed to dependency-first sequence | 2026-04-21)

- headSha: `975b25a4d`
- artifacts:
  - `git show --stat --summary --name-only 3ae6b7c63`
  - `git show --stat --summary --name-only 7dc6cad50`
  - `git show --stat --summary --name-only 19f503173`
  - `git show --stat --summary --name-only 7b6c7f70d`
  - `git show --stat --summary --name-only 975b25a4d`
- expected:
  - the first extraction order should prefer the packet whose rules and placement model are prerequisites for the later packets, instead of blindly following commit time.
- observed:
  - `S0G-2B` owns the support-only/legacy placement and patch-ledger bridge model, so it should land before later governance or workflow-family patch extraction relies on that placement.
  - `S0G-3A` is the next narrow governance write-back and should land before more steady-state object-first packet handling relies on it.
  - `RUN-LEDGER-PATCH-001` should follow as one bounded workflow-family packet that already absorbs the actionable `S4F` close-out tail.
  - `S0G-3B` should remain the live inventory/control surface until the first extraction sequence stops changing.

## Recent changes (for traceability, optional)

- 2026-04-21: opened `S0G-3B` to govern the transition from `S0G` as a mixed historical carrier toward extraction-first cleanup and later fresh `main`-based packet branches.

