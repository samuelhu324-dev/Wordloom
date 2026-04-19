from __future__ import annotations

from enum import Enum


class EntitlementCode(str, Enum):
    READ_LIBRARY = "read_library"
    COPY_BLOCK_CROSS_BOOK = "copy_block_cross_book"
    EXPORT_BOOK = "export_book"
