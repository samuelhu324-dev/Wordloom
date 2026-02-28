from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


class PayloadContractError(Exception):
    pass


@dataclass(frozen=True)
class PayloadContractViolation(PayloadContractError):
    projection: str
    reason: str
    message: str

    def __str__(self) -> str:  # pragma: no cover
        return f"[{self.projection}] {self.reason}: {self.message}"


@dataclass(frozen=True)
class BadPayload(PayloadContractViolation):
    pass


@dataclass(frozen=True)
class SchemaMismatch(PayloadContractViolation):
    pass


def require_schema_version(
    payload: Mapping[str, Any] | None,
    *,
    projection: str,
    supported_versions: set[int],
    allow_missing: bool = False,
) -> int:
    if payload is None:
        if allow_missing:
            return min(supported_versions)
        raise BadPayload(
            projection=projection,
            reason="bad_payload",
            message="payload is null",
        )

    if not isinstance(payload, Mapping):
        raise BadPayload(
            projection=projection,
            reason="bad_payload",
            message=f"payload must be a mapping, got {type(payload).__name__}",
        )

    if "schema_version" not in payload:
        if allow_missing:
            return min(supported_versions)
        raise SchemaMismatch(
            projection=projection,
            reason="schema_mismatch",
            message="missing required field schema_version",
        )

    raw = payload.get("schema_version")
    if not isinstance(raw, int):
        raise SchemaMismatch(
            projection=projection,
            reason="schema_mismatch",
            message=f"schema_version must be int, got {type(raw).__name__}",
        )

    if raw not in supported_versions:
        raise SchemaMismatch(
            projection=projection,
            reason="schema_mismatch",
            message=f"unsupported schema_version={raw}, supported={sorted(supported_versions)}",
        )

    return raw


def require_mapping(value: Any, *, projection: str, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BadPayload(
            projection=projection,
            reason="bad_payload",
            message=f"{field_name} must be a mapping, got {type(value).__name__}",
        )
    return value
