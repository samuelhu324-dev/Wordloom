# ADR-S0B: docs management v2（Taxonomy + Front Matter + Cutover/Stub + Snapshots）

---

**id**: `S0B-docs-management-v2`
**kind**: `adr`               # log | lab | runbook | adr | note
**title**: `adr/S0B-docs-management-v2`
**status**: `stable`          # draft | stable | archived
**scope**: `S0B`
**decision_date**: `2026-02-15`
**context_issue**: `#43, #44`
**decision**: `Adopt docs management v2: a stable directory taxonomy for scripts and evidence snapshots, consistent front matter metadata for mechanical maintenance, and a cutover+stub policy to preserve legacy links while preventing new accumulation in legacy paths.`
  **positive**: `"Stops script/snapshot sprawl", "Stable navigation despite moves", "Repeatable evidence outputs", "Preserves legacy links"`
  **negative**: `"Requires discipline for new content placement", "More up-front structure", "Need ongoing retention/cleanup rules"`
**supersedes**: `null`
**superseded_by**: `null`

---

## Context

As scripts and experiment outputs evolve, repositories naturally drift into two failure modes: a “script swamp” (too many ad-hoc entrypoints) and a “snapshot garbage mountain” (unbounded evidence dumps). This makes operations hard to reproduce, breaks old notes/CI when paths move, and increases maintenance cost because humans must remember file names and locations. We needed a sustainable governance skeleton that keeps legacy references valid while enforcing that new work follows a consistent structure.

## Decision

1) **Directory taxonomy by lifecycle/risk** (instead of author/file-name memory):
- `backend/scripts/ops/`: operational/runbook tools (auditable, repeatable, safe defaults)
- `backend/scripts/labs/`: failure drills and evidence export (replayable, not production tools)
- `backend/scripts/migrations/`: one-off or milestone migrations (freeze after completion)
- `backend/scripts/dev/`: developer convenience scripts
- `backend/scripts/legacy/`: fenced historical scripts (read-only reference; no new growth)

2) **Stable entrypoint as the public API**:
- Use a single CLI router (e.g., `backend/scripts/cli.py`) so users invoke commands by namespace/scenario rather than by script path.

3) **Unified snapshot/evidence roots**:
- Labs evidence: `docs/labs/_snapshot/`
- Runbook evidence: `docs/runbook/_snapshot/`
- Automated evidence bundles additionally use `docs/labs/_snapshot/auto/` and a stable directory layout per run.

4) **Front matter metadata standard**:
- Keep mechanically maintained attributes (id/kind/status/scope/tags/links/created/updated) in front matter to decouple naming from chronology and allow re-org without semantic loss.

5) **Cutover + stub policy**:
- From the cutover point onward, new content must follow the new taxonomy + front matter + unified snapshot roots.
- Legacy content is preserved but fenced; when moved, keep a stub file at the old path pointing to the new location to prevent link rot.

## Alternatives Considered

- Keep everything ad-hoc (no taxonomy): lowest effort now, but creates compounding maintenance and broken links.
- Delete old artifacts aggressively: reduces disk usage, but destroys baselines and audit/replay capability.
- Rename/migrate everything in one big bang: high disruption and high regression risk.
- Store chronology in filenames: brittle; re-orgs force mass renames and break references.

## Consequences

- New scripts become discoverable and safer to operate because they live in well-defined zones and are invoked via a stable entrypoint.
- Evidence outputs become reviewable and maintainable: consistent run directories, retention via keep-last policies, and a clear place to look.
- Documentation can move without breaking navigation because the meaning is in front matter, while stubs preserve legacy links.
- Requires discipline: new scripts/outputs must follow the taxonomy and must not grow the legacy area.

## Implementation Notes

Key files/logs that embody the decision:
- Taxonomy + stable entrypoint + unified snapshot roots:
  - `docs/logs/log-S0B-2A-scripts-snapshots-management.md`
- Unified indices, legacy taxonomy, and front matter conventions:
  - `docs/logs/log-S0B-3A-unified-indices-legacy taxonomy -front matter.md`
- Stub preservation example:
  - `docs/legacy/from-logs/v2-logs/log-S3B-scripts-snapshots-management.md`
- Evidence roots:
  - `docs/labs/_snapshot/`
  - `docs/runbook/_snapshot/`
