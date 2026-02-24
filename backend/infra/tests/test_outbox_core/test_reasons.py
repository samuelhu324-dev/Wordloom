from __future__ import annotations

from infra.outbox_core.reasons import classify_exception_reason


def test_classify_exception_reason_runtime_error_is_retryable_unknown() -> None:
    reason, retryable = classify_exception_reason(RuntimeError("boom"))
    assert reason == "unknown_exception"
    assert retryable is True


def test_classify_exception_reason_value_error_is_non_retryable_deterministic() -> None:
    reason, retryable = classify_exception_reason(ValueError("bad input"))
    assert reason == "deterministic_exception"
    assert retryable is False
