## Metadata

- Requested ID: `S0F-1G`
- Base branch: `main`
- Candidate PR-prep branch: `pr-prep/s0f-1g`
- Source log: `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- Labels: `EVOLUTION, s0/knowledge system, sub/1, drills`
- Development issue: #376

## Summary

- Open one focused `S0F` slice for the remaining parent sidebar ordering gap and the missing hard governance around issue title keyword prefixes.
- Fix the contract boundary so source-log-owned ordering and title keyword vocabulary become deterministic, fail-closed audit surfaces instead of soft conventions.
- Prepare the next follow-up path for controlled parent issue repair and explicit title-prefix enforcement without mixing policy design with blind bulk rewrites.

## Execution Checklist

- [x] `P0-C1-S1`: `S0F-1G` created and wired into the `S0F` parent spine
- [x] `P0-C1-S2`: shared governance boundary fixed for parent ordering and title keyword identity
- [x] `P1-C1-S1`: top-level parent sub-issue ordering source-of-truth and audit semantics fixed
- [x] `P1-C1-S2`: one controlled repair path retained for remaining parent ordering drift
- [x] `P2-C1-S1`: controlled vocabulary input rules fixed for `issue_keyword`
- [x] `P2-C1-S2`: real issue creation hard-fails on disallowed title keywords
- [x] `P3-C1-S1`: canonical expected title prefix derived from source-log-owned keyword state
- [x] `P3-C1-S2`: lifecycle audit emits deterministic title-prefix drift failure and bucket attribution
- [x] `P4-C1-S1`: migration inventory retained for historical title-prefix and parent-ordering drift
- [x] `P4-C1-S2`: controlled repair boundary packaged for later cleanup
- [x] `P5-C1-S1`: retained legacy source-log keyword set migrated into controlled vocabulary values
- [x] `P5-C1-S2`: matching live issue titles repaired through one guarded source-log-owned title surface
- [x] `P6-C1-S1`: bounded source-log issue write-back plan retained for the affected parent child lanes
- [x] `P6-C1-S2`: missing child-log issue URLs written back and full parent child-set convergence re-verified

## Links

- Log: `docs/logs/log-S0F-1G-parent-issue-sidebar-ordering-and-title-keyword-governance.md`
- Parent log: `docs/logs/log-S0F-docs-management-v6.md`

Closes #376
