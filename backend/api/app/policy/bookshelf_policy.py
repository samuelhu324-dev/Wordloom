from __future__ import annotations

from typing import Optional
from uuid import UUID

from api.app.policy import check
from api.app.modules.bookshelf.exceptions import BookshelfForbiddenError


REASON_NOT_OWNER = "not_owner"  # low-cardinality


def assert_actor_owns_library_for_bookshelf(
    *,
    actor_user_id: Optional[UUID],
    enforce_owner_check: bool,
    library_id: UUID,
    library_owner_user_id: Optional[UUID],
    bookshelf_id: UUID,
) -> None:
    """Policy: actor must own the library that contains the bookshelf.

    v1 simplification: library owner == only allowed actor.
    """

    if not enforce_owner_check:
        return
    if actor_user_id is None:
        return

    check(
        allowed=(library_owner_user_id == actor_user_id),
        exc_factory=lambda: BookshelfForbiddenError(
            bookshelf_id=str(bookshelf_id),
            library_id=str(library_id),
            actor_user_id=str(actor_user_id),
            reason=REASON_NOT_OWNER,
        ),
    )
