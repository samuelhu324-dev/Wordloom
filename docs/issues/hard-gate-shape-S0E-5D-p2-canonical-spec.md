# S0E-5D/P2 Hard Gate Body-Shape Check Spec

## Scope

- `P2` fixes the machine-checkable body-shape gate surface for issue bodies and PR bodies.
- The gate no longer stops at section existence; it must also reject shape drift.

## Issue Body Checks

- Required sections: `Metadata`, `Context`, `Definition of Done (DoD)`, `Links`.
- Section order: `Metadata -> Context -> Definition of Done (DoD) -> Links`.
- Metadata bullet rows must be contiguous with no blank gaps.
- Metadata must not render `Source log`; deterministic log navigation belongs in `Links`.
- Links may only use issue-body categories: `Log`, `Runbook`, `Parent log`, `Previous log`, `Roadmap`.
- Closed issues must keep substantive `Context` content.

## PR Body Checks

- Required sections: `Metadata`, `Summary`, `Execution Checklist`, `Links`.
- Section order: `Metadata -> Summary -> Execution Checklist -> Links -> Evidence Footer (when applicable) -> Development Link (when applicable)`.
- Metadata bullet rows must be contiguous with no blank gaps.
- Links may only use PR-body categories: `Log`, `Issue`, `Runbook`, `Evidence artifact`, `Parent log`, `Roadmap`.
- `Evidence Footer` must be omitted when no `Evidence Footer Source` block exists.
- `Evidence Footer` must match the `Evidence Footer Source` rows exactly and preserve order.
- Every `Evidence Footer` row must use the canonical line shape:

```md
- `P1-C1-S1` | artifact: `docs/issues/issue-relationship-S0E-5B-p1-pass-guarded-apply-result.json`
```

## Evidence

- Representative pass/stop fixtures and check outputs are stored under `docs/issues/pr-body-contract-S0E-5D-p2-*`.