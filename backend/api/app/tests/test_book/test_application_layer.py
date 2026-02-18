"""Book application-layer tests (aligned to current implementation).

Goals:
- Test the current UseCase APIs (not legacy request-shape assumptions).
- Validate Basement pattern semantics via ``soft_deleted_at``.
- Avoid changing production code just to satisfy obsolete tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

import pytest

from api.app.modules.book.application.ports.input import (
    DeleteBookRequest,
    GetBookRequest,
    ListBooksRequest,
    ListDeletedBooksRequest,
    MoveBookRequest,
    RestoreBookRequest,
    UpdateBookRequest,
)
from api.app.modules.book.application.use_cases import (
    CreateBookUseCase,
    DeleteBookUseCase,
    GetBookUseCase,
    ListBooksUseCase,
    ListDeletedBooksUseCase,
    MoveBookUseCase,
    RestoreBookUseCase,
    UpdateBookUseCase,
)
from api.app.modules.book.domain import Book
from api.app.modules.book.exceptions import (
    BookNotFoundError,
    BookNotInBasementError,
    BookOperationError,
    InvalidBookMoveError,
)
from api.app.modules.bookshelf.domain import BookshelfType


class CapturingEventBus:
    def __init__(self) -> None:
        self.events: list[object] = []

    async def publish(self, event: object) -> None:
        self.events.append(event)


class InMemoryBookRepository:
    def __init__(self) -> None:
        self._books: dict[UUID, Book] = {}

    async def save(self, book: Book) -> Book:
        self._books[book.id] = book
        return book

    async def get_by_id(self, book_id: UUID) -> Book | None:
        return self._books.get(book_id)

    async def get_by_bookshelf_id(
        self,
        bookshelf_id: UUID,
        skip: int,
        limit: int,
        *,
        include_deleted: bool = False,
    ) -> tuple[list[Book], int]:
        books = [b for b in self._books.values() if b.bookshelf_id == bookshelf_id]
        if not include_deleted:
            books = [b for b in books if b.soft_deleted_at is None]
        books.sort(key=lambda b: getattr(b, "created_at", None) or 0)
        total = len(books)
        return books[skip : skip + limit], total

    async def get_by_library_id(
        self,
        library_id: UUID,
        skip: int,
        limit: int,
        *,
        include_deleted: bool = False,
    ) -> tuple[list[Book], int]:
        books = [b for b in self._books.values() if getattr(b, "library_id", None) == library_id]
        if not include_deleted:
            books = [b for b in books if b.soft_deleted_at is None]
        books.sort(key=lambda b: getattr(b, "created_at", None) or 0)
        total = len(books)
        return books[skip : skip + limit], total

    async def get_deleted_books(
        self,
        *,
        skip: int,
        limit: int,
        bookshelf_id: UUID | None = None,
        library_id: UUID | None = None,
    ) -> tuple[list[Book], int]:
        books = [b for b in self._books.values() if b.soft_deleted_at is not None]
        if library_id is not None:
            books = [b for b in books if getattr(b, "library_id", None) == library_id]
        if bookshelf_id is not None:
            # In Basement, the original shelf is preserved in previous_bookshelf_id.
            books = [b for b in books if getattr(b, "previous_bookshelf_id", None) == bookshelf_id]
        books.sort(key=lambda b: getattr(b, "soft_deleted_at", None) or 0)
        total = len(books)
        return books[skip : skip + limit], total


@dataclass(frozen=True)
class _Bookshelf:
    id: UUID
    library_id: UUID
    type: BookshelfType


class InMemoryBookshelfRepository:
    def __init__(self, shelves: list[_Bookshelf]) -> None:
        self._shelves = {s.id: s for s in shelves}

    async def get_by_id(self, shelf_id: UUID) -> _Bookshelf | None:
        return self._shelves.get(shelf_id)


@pytest.fixture
def repo() -> InMemoryBookRepository:
    return InMemoryBookRepository()


@pytest.fixture
def bus() -> CapturingEventBus:
    return CapturingEventBus()


@pytest.fixture
def bookshelf_id() -> UUID:
    return uuid4()


@pytest.fixture
def library_id() -> UUID:
    return uuid4()


@pytest.fixture
def basement_bookshelf_id() -> UUID:
    return uuid4()


@pytest.mark.asyncio
async def test_create_book_success(repo: InMemoryBookRepository, bus: CapturingEventBus, bookshelf_id: UUID, library_id: UUID) -> None:
    usecase = CreateBookUseCase(repo, bus)
    book = await usecase.execute(
        bookshelf_id=bookshelf_id,
        library_id=library_id,
        title="Test Book",
        description=None,
        enforce_owner_check=False,
    )

    assert book.id is not None
    assert book.title.value == "Test Book"
    assert book.bookshelf_id == bookshelf_id
    assert book.soft_deleted_at is None
    assert len(bus.events) >= 1


@pytest.mark.asyncio
async def test_create_book_invalid_title_is_wrapped(repo: InMemoryBookRepository, bus: CapturingEventBus, bookshelf_id: UUID, library_id: UUID) -> None:
    usecase = CreateBookUseCase(repo, bus)
    with pytest.raises(BookOperationError):
        await usecase.execute(
            bookshelf_id=bookshelf_id,
            library_id=library_id,
            title="",
            enforce_owner_check=False,
        )


@pytest.mark.asyncio
async def test_list_books_by_bookshelf(repo: InMemoryBookRepository, bookshelf_id: UUID, library_id: UUID) -> None:
    creator = CreateBookUseCase(repo, None)
    await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="A", enforce_owner_check=False)
    await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="B", enforce_owner_check=False)

    usecase = ListBooksUseCase(repo)
    page = await usecase.execute(ListBooksRequest(bookshelf_id=bookshelf_id, skip=0, limit=10, enforce_owner_check=False))

    assert page.total == 2
    assert [item.title for item in page.items] == ["A", "B"]


@pytest.mark.asyncio
async def test_get_book_not_found(repo: InMemoryBookRepository) -> None:
    usecase = GetBookUseCase(repo)
    with pytest.raises(BookNotFoundError):
        await usecase.execute(GetBookRequest(book_id=uuid4(), enforce_owner_check=False))


@pytest.mark.asyncio
async def test_update_book_title(repo: InMemoryBookRepository, bookshelf_id: UUID, library_id: UUID) -> None:
    creator = CreateBookUseCase(repo)
    book = await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="Old", enforce_owner_check=False)

    usecase = UpdateBookUseCase(repo)
    updated = await usecase.execute(UpdateBookRequest(book_id=book.id, title="New", enforce_owner_check=False))

    assert updated.id == book.id
    assert updated.title.value == "New"


@pytest.mark.asyncio
async def test_update_book_not_found(repo: InMemoryBookRepository) -> None:
    usecase = UpdateBookUseCase(repo)
    with pytest.raises(BookNotFoundError):
        await usecase.execute(UpdateBookRequest(book_id=uuid4(), title="New", enforce_owner_check=False))


@pytest.mark.asyncio
async def test_delete_then_restore_book(repo: InMemoryBookRepository, bus: CapturingEventBus, bookshelf_id: UUID, library_id: UUID, basement_bookshelf_id: UUID) -> None:
    creator = CreateBookUseCase(repo)
    book = await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="ToDelete", enforce_owner_check=False)

    shelves = InMemoryBookshelfRepository([
        _Bookshelf(id=bookshelf_id, library_id=library_id, type=BookshelfType.NORMAL),
        _Bookshelf(id=basement_bookshelf_id, library_id=library_id, type=BookshelfType.BASEMENT),
    ])

    deleter = DeleteBookUseCase(repo, shelves, bus)
    await deleter.execute(DeleteBookRequest(book_id=book.id, basement_bookshelf_id=basement_bookshelf_id, enforce_owner_check=False))

    deleted = await repo.get_by_id(book.id)
    assert deleted is not None
    assert deleted.soft_deleted_at is not None
    assert deleted.bookshelf_id == basement_bookshelf_id
    assert deleted.previous_bookshelf_id == bookshelf_id
    assert len(bus.events) >= 1

    restorer = RestoreBookUseCase(repo, bus)
    restored = await restorer.execute(RestoreBookRequest(book_id=book.id, target_bookshelf_id=bookshelf_id, enforce_owner_check=False))

    assert restored.soft_deleted_at is None
    assert restored.bookshelf_id == bookshelf_id


@pytest.mark.asyncio
async def test_restore_requires_book_in_basement(repo: InMemoryBookRepository, bookshelf_id: UUID, library_id: UUID) -> None:
    creator = CreateBookUseCase(repo)
    book = await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="Active", enforce_owner_check=False)

    restorer = RestoreBookUseCase(repo)
    with pytest.raises(BookNotInBasementError):
        await restorer.execute(RestoreBookRequest(book_id=book.id, target_bookshelf_id=bookshelf_id, enforce_owner_check=False))


@pytest.mark.asyncio
async def test_move_book_success(repo: InMemoryBookRepository, bus: CapturingEventBus, bookshelf_id: UUID, library_id: UUID) -> None:
    target_bookshelf_id = uuid4()
    creator = CreateBookUseCase(repo)
    book = await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="MoveMe", enforce_owner_check=False)

    mover = MoveBookUseCase(repo, bus)
    moved = await mover.execute(MoveBookRequest(book_id=book.id, target_bookshelf_id=target_bookshelf_id, enforce_owner_check=False))

    assert moved.bookshelf_id == target_bookshelf_id
    assert len(bus.events) >= 1


@pytest.mark.asyncio
async def test_move_book_same_bookshelf_is_invalid(repo: InMemoryBookRepository, bookshelf_id: UUID, library_id: UUID) -> None:
    creator = CreateBookUseCase(repo)
    book = await creator.execute(bookshelf_id=bookshelf_id, library_id=library_id, title="NoMove", enforce_owner_check=False)

    mover = MoveBookUseCase(repo)
    with pytest.raises(InvalidBookMoveError):
        await mover.execute(MoveBookRequest(book_id=book.id, target_bookshelf_id=bookshelf_id, enforce_owner_check=False))


@pytest.mark.asyncio
async def test_list_deleted_books_filters_by_previous_bookshelf_id(repo: InMemoryBookRepository, bookshelf_id: UUID, library_id: UUID, basement_bookshelf_id: UUID) -> None:
    shelves = InMemoryBookshelfRepository([
        _Bookshelf(id=bookshelf_id, library_id=library_id, type=BookshelfType.NORMAL),
        _Bookshelf(id=basement_bookshelf_id, library_id=library_id, type=BookshelfType.BASEMENT),
    ])
    book = await CreateBookUseCase(repo).execute(bookshelf_id=bookshelf_id, library_id=library_id, title="Del", enforce_owner_check=False)
    await DeleteBookUseCase(repo, shelves).execute(
        DeleteBookRequest(book_id=book.id, basement_bookshelf_id=basement_bookshelf_id, enforce_owner_check=False)
    )

    usecase = ListDeletedBooksUseCase(repo)
    page = await usecase.execute(ListDeletedBooksRequest(bookshelf_id=bookshelf_id, skip=0, limit=10, enforce_owner_check=False))
    assert page.total == 1
    assert page.items[0].id == book.id
    assert page.items[0].soft_deleted_at is not None
