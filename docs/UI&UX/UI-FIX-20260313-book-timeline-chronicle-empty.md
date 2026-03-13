# UI Fix Note

## Summary

- Type: `workflow-fix`
- Status: `verified`
- Date: `2026-03-13`
- Owner: `GitHub Copilot + repo owner`

## Issue

Book detail Timeline showed an empty state even though the database already contained Chronicle events for the same book.

## Impact

- Affected page or component: `Book detail -> Timeline`
- Affected workflow: `library -> bookshelf -> book -> timeline`
- User-visible risk: users and interview viewers could conclude that no event history existed, which made the product story and state history appear broken.

## Reproduction

1. Open a Book detail page with an existing Chronicle history.
2. Switch to the Timeline tab.
3. Observe `No events yet` even though `chronicle_events` contains rows for the same `book_id`.

## Fix

Two fixes were applied:

1. The Book detail Timeline was configured to show visit logs by default so common read events are not hidden on first render.
2. Backend Chronicle query logic now falls back from `chronicle_entries` to `chronicle_events` when merged-read mode points at an empty or stale read projection.

This fixed both the presentation-side filtering problem and the deeper read-path mismatch between projection data and source-of-truth data.

## Evidence

- Before screenshot or GIF: `docs/UI&UX/assets/20260313-book-timeline-empty-before.png`.
- After screenshot or GIF: `docs/UI&UX/assets/20260313-book-timeline-empty-after.png`.
- Optional flow GIF: `docs/UI&UX/assets/20260313-book-timeline-empty-flow.gif`.
- Optional console, network, or API proof: `/api/v1/chronicle/books/8ac1fb57-cf33-40d0-b6f0-44aa6b6c8e11/events?page=1&size=15` returned non-empty data with `total: 222` after the fallback fix.

## Validation Checklist

- [x] Happy path works
- [x] Loading state checked
- [x] Empty state no longer appears for this populated book
- [ ] Error state checked if relevant
- [ ] Mobile or narrow viewport checked if relevant
- [x] Navigation in and out of the page still works
- [x] Backend state and UI state now match

## Code References

- Changed files:
  - `frontend/src/features/chronicle/ui/ChronicleTimelineList.tsx`
  - `frontend/src/app/admin/books/[bookId]/page.tsx`
  - `backend/api/app/modules/chronicle/application/services.py`
  - `backend/api/app/dependencies_real.py`
- Related routes or APIs:
  - `GET /api/v1/chronicle/books/{book_id}/events`

## Related Changes

- Commit: `working tree change, not committed in this note`
- PR: `n/a`
- Follow-up task: capture one after-fix screenshot for demo reuse.

## Escalation Decision

- Keep in evidence-lite because: the fix is demo-critical and workflow-relevant, but it does not require a new drill or hard gate right now.
- Escalate to heavy track if: Timeline regressions recur across routes, or if Chronicle projection freshness becomes a broader read-model reliability problem.

## Demo Value

This is a strong interview story because it shows surface debugging tied back to system architecture: the visible UI bug turned out to be a read-model mismatch between projection and source-of-truth data.