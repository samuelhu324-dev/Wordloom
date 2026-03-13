# UI Fix Note

## Summary

- Type: `ui-fix`
- Status: `verified`
- Date: `2026-03-13`
- Owner: `GitHub Copilot + repo owner`

## Issue

The frontend requested library tags with an invalid `limit=200`, while the backend only accepts values up to `25`, which caused request failures during book-page tag loading.

## Impact

- Affected page or component: `books page tag loading`
- Affected workflow: opening books page with tag-dependent UI
- User-visible risk: related tag UI looked broken even though the underlying library tags existed.

## Reproduction

1. Open the books page in a context that loads library tags.
2. Let the page call the tag endpoint with `limit=200`.
3. Observe request failure because the backend validation rejects the oversized limit.

## Fix

The frontend request limit was aligned with the backend contract:

1. Books-page tag loading now calls `getLibraryTags(..., 25)` instead of `200`.
2. Related tag-fetch call sites were kept within the accepted backend range.

This removed an avoidable UI failure caused purely by client-side parameter drift.

## Evidence

- Before screenshot or GIF: `docs/UI&UX/assets/20260313-library-tags-limit-before.png`.
- After screenshot or GIF: `docs/UI&UX/assets/20260313-library-tags-limit-after.png`.
- Optional flow GIF: `docs/UI&UX/assets/20260313-library-tags-limit-flow.gif`.
- Optional console, network, or API proof: books page now uses `getLibraryTags(targetLibraryId!, 25)` and related calls use `25` instead of `200`.

## Validation Checklist

- [x] Happy path works
- [x] Loading state checked
- [x] Empty state checked where relevant
- [x] Error state no longer caused by invalid tag limit
- [ ] Mobile or narrow viewport checked if relevant
- [x] Navigation in and out of the page still works
- [x] Backend state and UI state now match

## Code References

- Changed files:
  - `frontend/src/app/admin/books/page.tsx`
  - `frontend/src/widgets/library/LibraryMainWidget.tsx`
- Related routes or APIs:
  - `GET /api/v1/libraries/{library_id}/tags`

## Related Changes

- Commit: `working tree change, not committed in this note`
- PR: `n/a`
- Follow-up task: consider centralizing frontend-side limit constants for backend-constrained endpoints.

## Escalation Decision

- Keep in evidence-lite because: this is a focused client-contract alignment fix with limited blast radius.
- Escalate to heavy track if: frontend/backend parameter contracts begin drifting in multiple surfaces and need a shared contract strategy.

## Demo Value

This is a good small example of frontend reliability work: not every UI bug is visual, and a lot of real polish comes from keeping the client honest with backend constraints.