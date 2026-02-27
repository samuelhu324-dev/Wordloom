from __future__ import annotations

from typing import Any

try:
    from .payload_contract import PayloadContractViolation
except Exception:  # pragma: no cover
    PayloadContractViolation = None  # type: ignore


def is_transient_reason(reason: str) -> bool:
    """Low-cardinality transient reason set.

    Kept aligned with existing Search worker semantics so metrics/logs remain
    comparable after extraction.
    """

    return reason in {
        "es_429",
        "es_5xx",
        "es_timeout",
        "es_connect",
        "es_request_error",
        "es_unknown",
        "es_other",
    }


def is_deterministic_exception(exc: Exception) -> bool:
    # Heuristic: common programming/data errors won't be fixed by retry.
    return isinstance(exc, (ValueError, KeyError, TypeError))


def classify_es_bulk_item_failure(*, status_code: int | None) -> tuple[str, bool]:
    if status_code is None:
        return "es_unknown", True
    if status_code == 429:
        return "es_429", True
    if 500 <= status_code < 600:
        return "es_5xx", True
    if 400 <= status_code < 500:
        return "es_4xx", False
    return "es_other", True


def classify_httpx_exception_reason(exc: Exception) -> tuple[str, bool]:
    """Backwards-compatible alias of `classify_exception_reason`.

    Historically used by Search worker to produce low-cardinality `es_*` reasons.
    """

    return classify_exception_reason(exc)


def classify_exception_reason(exc: Exception) -> tuple[str, bool]:
    """Return (reason, retryable) for an exception.

    Emits low-cardinality reasons suitable for aggregation.
    Unknown exceptions are treated as retryable unless they look deterministic.

    Notes:
    - If HTTPX is installed and this is an HTTPX exception, emits `es_*` reasons.
    - Otherwise falls back to `deterministic_exception` vs `unknown_exception`.
    """

    # Import locally to keep this module usable in contexts where httpx isn't
    # imported elsewhere.
    try:
        import httpx  # type: ignore
    except Exception:
        httpx = None  # type: ignore

    if PayloadContractViolation is not None and isinstance(exc, PayloadContractViolation):
        return exc.reason, False

    if httpx is not None and isinstance(exc, getattr(httpx, "HTTPStatusError")):
        response: Any = getattr(exc, "response", None)
        status_code = getattr(response, "status_code", None)
        if status_code == 429:
            return "es_429", True
        if isinstance(status_code, int) and 500 <= status_code < 600:
            return "es_5xx", True
        if isinstance(status_code, int) and 400 <= status_code < 500:
            return "es_4xx", False
        return "es_other", True

    if httpx is not None and isinstance(exc, getattr(httpx, "TimeoutException")):
        return "es_timeout", True
    if httpx is not None and isinstance(exc, getattr(httpx, "ConnectError")):
        return "es_connect", True
    if httpx is not None and isinstance(exc, getattr(httpx, "RequestError")):
        return "es_request_error", True

    if is_deterministic_exception(exc):
        return "deterministic_exception", False

    return "unknown_exception", True
