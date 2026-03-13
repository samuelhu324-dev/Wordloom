# UI Fix Note

## Summary

- Type: `workflow-fix`
- Status: `verified`
- Date: `2026-03-13`
- Owner: `GitHub Copilot + repo owner`

## Issue

Several admin pages were making requests without a stable `library_id` context, which caused repeated frontend `400` errors on bookshelf, book, and detail flows.

## Impact

- Affected page or component: `bookshelves list`, `books list`, `bookshelf detail`, `book detail`, `block workspace`
- Affected workflow: `library -> bookshelf -> book -> blocks`
- User-visible risk: navigation looked broken and page data failed to load even though the underlying resources existed.

## Reproduction

1. Open a library and navigate into bookshelves or books from admin pages.
2. Trigger a list or detail view that depends on tenant/library-scoped backend routes.
3. Observe frontend request failures caused by missing `library_id` or missing `X-Library-Id` propagation.

## Fix

The frontend was updated to carry `library_id` across both data fetching and page navigation:

1. Bookshelf and book API calls now accept and forward `library_id`.
2. React Query hooks were gated so they no longer fire before a valid library context is known.
3. Page-to-page navigation now preserves `?library_id=...` across library, bookshelf, book, and block routes.
4. The shared request client now derives and attaches `X-Library-Id` from request parameters and related context.

This fixed the repeated `400` pattern at the root, rather than treating each page as an isolated bug.

## Evidence

- Before screenshot or GIF: `docs/UI&UX/assets/20260313-library-context-before.png`.
- After screenshot or GIF: `docs/UI&UX/assets/20260313-library-context-after.png`.
- Optional flow GIF: `docs/UI&UX/assets/20260313-library-context-flow.gif`.
- Optional console, network, or API proof: code now forwards `library_id` through API helpers, hooks, route transitions, and shared client headers.

## Validation Checklist

- [x] Happy path works
- [x] Loading state checked
- [x] Empty state checked where relevant
- [x] Error state no longer triggered by missing library context in the repaired paths
- [ ] Mobile or narrow viewport checked if relevant
- [x] Navigation in and out of the page still works
- [x] Backend state and UI state now match

## Code References

- Changed files:
  - `frontend/src/shared/api/client.ts`
  - `frontend/src/features/bookshelf/model/api.ts`
  - `frontend/src/features/bookshelf/model/hooks.ts`
  - `frontend/src/features/book/model/api.ts`
  - `frontend/src/features/book/model/hooks.ts`
  - `frontend/src/features/book/model/usePaginatedBooks.ts`
  - `frontend/src/app/admin/libraries/[libraryId]/page.tsx`
  - `frontend/src/app/admin/bookshelves/page.tsx`
  - `frontend/src/app/admin/bookshelves/[bookshelfId]/page.tsx`
  - `frontend/src/app/admin/books/page.tsx`
  - `frontend/src/app/admin/books/[bookId]/page.tsx`
  - `frontend/src/app/admin/blocks/page.tsx`
- Related routes or APIs:
  - `GET /api/v1/bookshelves`
  - `GET /api/v1/books`
  - `GET /api/v1/books/{book_id}`

## Related Changes

- Commit: `working tree change, not committed in this note`
- PR: `n/a`
- Follow-up task: capture one end-to-end flow GIF for demo reuse.

## Escalation Decision

- Keep in evidence-lite because: the fix repaired a visible workflow and is highly demo-relevant, but does not need a dedicated hard gate yet.
- Escalate to heavy track if: tenant scope regressions recur or a formal route-coverage check becomes necessary.

## Demo Value

This is a strong demo story because it shows that the visible UI path depends on correct scope propagation, not just component rendering. It also shows the ability to trace a repeated UI failure back to multi-tenant request context rules.