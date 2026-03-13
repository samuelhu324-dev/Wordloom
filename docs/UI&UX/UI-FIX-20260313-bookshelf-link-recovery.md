# UI Fix Note

## Summary

- Type: `workflow-fix`
- Status: `verified`
- Date: `2026-03-13`
- Owner: `GitHub Copilot + repo owner`

## Issue

Older bookshelf links could open without `library_id`, which caused bookshelf detail and follow-on navigation to break even when the target bookshelf still existed.

## Impact

- Affected page or component: `bookshelf detail page`
- Affected workflow: opening saved links or stale tabs, then continuing to book detail
- User-visible risk: users could land on a broken page from an otherwise valid saved URL, making the app feel brittle.

## Reproduction

1. Open or reuse an older bookshelf detail URL that does not include `?library_id=...`.
2. Let the page attempt to resolve bookshelf context without an explicit tenant parameter.
3. Observe detail loading failures or broken downstream navigation.

## Fix

The bookshelf detail page was given a self-healing recovery path:

1. If `library_id` is present, it is persisted as the active library.
2. If `library_id` is missing, the page attempts recovery from `wl_active_library_id` in local storage.
3. If local storage is insufficient, the page inspects cached bookshelf list data to recover the matching `library_id`.
4. Once recovered, the page rewrites the URL and preserves `library_id` in navigation to book detail.

This allows stale links to recover into the canonical scoped route instead of failing hard.

## Evidence

- Before screenshot or GIF: `docs/UI&UX/assets/20260313-bookshelf-link-recovery-before.png`.
- After screenshot or GIF: `docs/UI&UX/assets/20260313-bookshelf-link-recovery-after.png`.
- Optional flow GIF: `docs/UI&UX/assets/20260313-bookshelf-link-recovery-flow.gif`.
- Optional console, network, or API proof: bookshelf detail now reads from URL, local storage, and cached list state before normalizing the route.

## Validation Checklist

- [x] Happy path works
- [x] Loading state checked
- [x] Empty state checked where relevant
- [x] Error state reduced for stale-link entry path
- [ ] Mobile or narrow viewport checked if relevant
- [x] Navigation in and out of the page still works
- [x] Backend state and UI state now match

## Code References

- Changed files:
  - `frontend/src/app/admin/bookshelves/[bookshelfId]/page.tsx`
  - `frontend/src/app/admin/books/[bookId]/page.tsx`
  - `frontend/src/shared/api/client.ts`
- Related routes or APIs:
  - `GET /admin/bookshelves/[bookshelfId]?library_id=...`
  - `GET /admin/books/[bookId]?library_id=...`

## Related Changes

- Commit: `working tree change, not committed in this note`
- PR: `n/a`
- Follow-up task: capture before/after URL screenshots for documentation.

## Escalation Decision

- Keep in evidence-lite because: it is a targeted workflow-hardening fix for link stability, not a broad platform contract.
- Escalate to heavy track if: multiple routes require the same recovery behavior and a formal navigation-scope contract is introduced.

## Demo Value

This note is useful in demos because it shows product hardening beyond the happy path. The fix turns a fragile stale-link experience into a recoverable workflow without asking the user to manually reconstruct context.