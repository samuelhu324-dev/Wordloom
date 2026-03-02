from __future__ import annotations

from typing import FrozenSet, Tuple

from .adapters.chronicle_events_to_entries import apply as chronicle_events_to_entries_apply
from .adapters.search_index_to_elastic import apply as search_index_to_elastic_apply
from .registry import get_spec, register
from .spec import ProjectionSpec


def _stub_apply_factory(*, projection_name: str):
    def _apply(*args: object, **kwargs: object) -> object:
        raise NotImplementedError(f"apply_entrypoint not wired yet: {projection_name}")

    return _apply


def register_builtin_specs() -> None:
    # Idempotent: safe to call multiple times.

    specs = (
        ProjectionSpec(
            projection_name="search_index_to_elastic",
            scope_keys=("library_id",),
            requires=frozenset({"db", "es"}),
            payload_schema_version=1,
            apply_entrypoint=search_index_to_elastic_apply,
        ),
        ProjectionSpec(
            projection_name="chronicle_events_to_entries",
            scope_keys=("book_id",),
            requires=frozenset({"db"}),
            payload_schema_version=1,
            apply_entrypoint=chronicle_events_to_entries_apply,
        ),
    )

    for spec in specs:
        try:
            get_spec(spec.projection_name)
        except KeyError:
            register(spec)
