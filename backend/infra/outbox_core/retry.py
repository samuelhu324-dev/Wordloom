from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class ExponentialBackoffSpec:
    base_seconds: float
    max_backoff_seconds: float
    exponent_shift: int = 0
    jitter_ratio: float = 0.1
    jitter_cap_seconds: float | None = 1.0


def compute_exponential_backoff_seconds(*, attempt: int, spec: ExponentialBackoffSpec) -> float:
    """Compute exponential backoff with jitter.

    attempt: 1-based in most workers. We keep this generic by allowing an
    exponent_shift so callers can preserve legacy formulas exactly.
    """

    attempt_i = max(0, int(attempt))
    exp = spec.base_seconds * (2 ** max(0, attempt_i + int(spec.exponent_shift)))
    exp = min(float(spec.max_backoff_seconds), float(exp))

    jitter_max = exp * float(spec.jitter_ratio)
    if spec.jitter_cap_seconds is not None:
        jitter_max = min(float(spec.jitter_cap_seconds), float(jitter_max))

    jitter = random.uniform(0.0, max(0.0, float(jitter_max)))
    return min(float(spec.max_backoff_seconds), float(exp + jitter))


def compute_next_retry_at(*, now: datetime, attempt: int, spec: ExponentialBackoffSpec) -> datetime:
    delay_s = compute_exponential_backoff_seconds(attempt=attempt, spec=spec)
    return now + timedelta(seconds=float(delay_s))
