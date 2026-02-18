"""Library service (legacy-style facade).

This module exists to provide a thin orchestration layer that is convenient
for unit tests and for callers that prefer a simple CRUD-ish API.

The primary application architecture for this repo uses explicit UseCases
in `modules.library.application.use_cases`. This service is intentionally
small and delegates validation to Pydantic schemas + Domain objects.
"""

from __future__ import annotations

from typing import Optional, Protocol
from uuid import UUID

from modules.library.domain import Library
from modules.library.exceptions import (
    LibraryAlreadyExistsError,
    LibraryNotFoundError,
)
from modules.library.schemas import LibraryCreate, LibraryUpdate


class _LibraryRepository(Protocol):
    async def save(self, library: Library) -> Library: ...

    async def find_by_id(self, library_id: UUID) -> Library: ...

    async def find_by_user_id(self, user_id: UUID) -> Library: ...

    async def delete(self, library_id: UUID) -> None: ...


class LibraryService:
    def __init__(self, repository: _LibraryRepository):
        self._repository = repository

    async def create_library(self, *, user_id: UUID, create_request: LibraryCreate) -> Library:
        existing_library: Optional[Library] = None
        try:
            existing_library = await self._repository.find_by_user_id(user_id)
        except LibraryNotFoundError:
            existing_library = None

        if existing_library is not None:
            raise LibraryAlreadyExistsError(
                user_id=str(user_id),
                existing_library_id=str(existing_library.id),
            )

        library = Library.create(
            user_id=user_id,
            name=create_request.name,
            description=create_request.description,
            theme_color=create_request.theme_color,
        )

        await self._repository.save(library)
        return library

    async def get_library(self, library_id: UUID) -> Library:
        try:
            return await self._repository.find_by_id(library_id)
        except LibraryNotFoundError:
            raise

    async def get_library_for_user(self, user_id: UUID) -> Library:
        try:
            return await self._repository.find_by_user_id(user_id)
        except LibraryNotFoundError:
            raise

    async def update_library(self, *, library_id: UUID, update_request: LibraryUpdate) -> Library:
        library = await self.get_library(library_id)

        if update_request.name is not None:
            library.rename(update_request.name)

        if update_request.description is not None:
            library.update_description(update_request.description)

        if update_request.cover_media_id is not None:
            library.set_cover_media(update_request.cover_media_id)

        if update_request.pinned is not None:
            library.set_pinned(update_request.pinned, update_request.pinned_order)

        if update_request.archived is True:
            library.archive()
        elif update_request.archived is False:
            library.unarchive()

        if update_request.theme_color is not None:
            library.set_theme_color(update_request.theme_color)

        await self._repository.save(library)
        return library

    async def delete_library(self, library_id: UUID) -> None:
        # Validate existence first for consistent error semantics.
        await self.get_library(library_id)
        await self._repository.delete(library_id)
