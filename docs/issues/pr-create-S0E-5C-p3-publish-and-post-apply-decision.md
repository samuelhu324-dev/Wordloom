# S0E-5C/P3 Publish Boundary And Post-Apply Verification Decision

## Decision

- `S0E-5C` should not expand guarded apply all the way through `S6` live PR publication in v1.
- The bounded front-half result from `P2` is strong enough to keep `S6` as an explicit operator-held boundary while preserving the option to explore narrower targeted rules for `S4` local branch materialization and `S5` remote branch publication later.
- Post-apply live verification should run immediately after `S6` live PR publication and before `S7` local evidence finalization.
- `S7` should then serialize both:
  - the real PR create result;
  - the post-apply verification result.
- A later GitHub Actions job may mirror the same live verification, but it should be treated as secondary enforcement rather than as the primary publish authorization boundary.

## Why `S6` Stays Operator-Held In V1

- `S6` is the first step that publishes a live GitHub PR object.
- Unlike `S4` and `S5`, `S6` combines multiple outward-facing effects at once:
  - title publication;
  - body publication;
  - label assignment;
  - milestone assignment;
  - project assignment;
  - draft vs ready state.
- The existing lifecycle pre-gate plus create-specific preflight is strong enough to prove readiness for publication, but not strong enough to justify full unattended authorization of that publication step in v1.
- Therefore `S6` should remain the operator-confirmed boundary even after `P3` is complete.

## Why Post-Apply Verify Sits Between `S6` And `S7`

- Preview success alone is not sufficient once a live PR already exists.
- The earliest useful point for post-apply verification is immediately after publish, when the command already knows:
  - the source log path;
  - the repository slug;
  - the created PR number/URL.
- Running verification only after `S7` would delay detection of live-body drift even though the necessary identifiers already exist at `S6` completion time.
- Deferring verification only to GitHub Actions would make the first failure signal arrive too late and would weaken operator feedback during the interactive create path.
- Therefore the preferred execution order is:
  - `S6`: publish live PR;
  - `S6.5`: run live PR body contract verification;
  - `S7`: serialize create result plus verification result and clean up local worktree state.

## Ownership Split After `P3`

- `S0E-5D` remains the owner of:
  - canonical body contract;
  - hard-gate body-shape checks;
  - historical normalization.
- `S0E-5C` now owns:
  - create-time publish boundary decisions;
  - inline post-apply live verification placement;
  - the later decision of whether `S4` or `S5` deserve narrower targeted rules.
- A future GitHub Actions layer may still run the same live verifier, but that layer is downstream enforcement and not the first owner of publish-time correctness.

## Immediate Outcome For The Slice

- `S0E-5C` is now complete as a decomposition-and-ownership slice.
- The slice does not claim that full guarded `PR create` is safe in v1.
- The slice does claim that:
  - the create path is now decomposed enough to identify the exact operator-held boundary;
  - `S6` remains operator-held;
  - post-apply verify belongs immediately after publish and before final local evidence serialization.

## Next Step After `P3`

- If deeper automation is still desired later, open a follow-up slice that evaluates whether `S4` and `S5` can gain narrower targeted rules without collapsing `S6` into unattended guarded publish.
- Keep `S6` live PR publication operator-confirmed until that narrower follow-up proves otherwise.