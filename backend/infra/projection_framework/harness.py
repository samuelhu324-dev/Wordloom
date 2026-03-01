from __future__ import annotations

import argparse
import asyncio
import os
import socket
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.models.outbox_event_models import OutboxEventModel
from infra.database.session import get_session_factory
from infra.outbox_core.claim import claim_pending_batch
from infra.outbox_core.lease import renew_lease
from infra.outbox_core.mark import mark_done, mark_failed, mark_retry
from infra.outbox_core.reasons import classify_exception_reason
from infra.outbox_core.reclaim import reclaim_stuck_processing
from infra.outbox_core.retry import ExponentialBackoffSpec, compute_next_retry_at
from infra.outbox_core.sanitize import sanitize_terminal_rows
from infra.projection_framework.builtins import register_builtin_specs
from infra.projection_framework.registry import get_spec


@dataclass(frozen=True)
class HarnessConfig:
    batch_size: int
    lease_seconds: float
    max_processing_seconds: int
    max_attempts: int
    base_backoff_seconds: float
    max_backoff_seconds: float
    poll_interval_seconds: float
    reclaim_interval_seconds: float
    exit_when_idle: bool


def _get_env_int(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return int(default)
    return int(raw)


def _get_env_float(name: str, default: float) -> float:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return float(default)
    return float(raw)


def _get_env_bool(name: str, default: bool) -> bool:
    raw = (os.getenv(name) or "").strip().lower()
    if not raw:
        return bool(default)
    return raw in {"1", "true", "yes", "y", "on"}


def _default_worker_id() -> str:
    worker_id = (os.getenv("OUTBOX_WORKER_ID") or "").strip()
    if worker_id:
        return worker_id
    return f"{socket.gethostname()}:{os.getpid()}"


async def _process_one(
    session: AsyncSession,
    *,
    worker_id: str,
    spec_name: str,
    ev: OutboxEventModel,
    max_attempts: int,
    backoff: ExponentialBackoffSpec,
) -> None:
    now = datetime.now(timezone.utc)
    attempts = int(getattr(ev, "attempts", 0) or 0) + 1

    try:
        spec = get_spec(spec_name)
        # Note: apply_entrypoint signature is intentionally flexible.
        maybe_awaitable = spec.apply_entrypoint(ev=ev, session=session)
        if asyncio.iscoroutine(maybe_awaitable):
            await maybe_awaitable
    except NotImplementedError as exc:
        await mark_failed(
            session,
            OutboxEventModel,
            ev_id=ev.id,
            reason="apply_not_wired",
            error=str(exc),
            attempts=attempts,
            now=now,
        )
        await session.commit()
        return
    except Exception as exc:
        reason, retryable = classify_exception_reason(exc)
        if retryable and attempts < int(max_attempts):
            next_retry_at = compute_next_retry_at(now=now, attempt=attempts, spec=backoff)
            await mark_retry(
                session,
                OutboxEventModel,
                ev_id=ev.id,
                reason=reason,
                error=str(exc),
                attempts=attempts,
                next_retry_at=next_retry_at,
                now=now,
            )
            await session.commit()
            return

        await mark_failed(
            session,
            OutboxEventModel,
            ev_id=ev.id,
            reason=reason,
            error=str(exc),
            attempts=attempts,
            now=now,
        )
        await session.commit()
        return

    await mark_done(session, OutboxEventModel, ev_id=ev.id, worker_id=worker_id, now=now)
    await session.commit()


async def run_harness(*, projection_name: str, config: HarnessConfig) -> int:
    if not projection_name.strip():
        raise ValueError("projection_name must be non-empty")
    if config.batch_size <= 0:
        raise ValueError("batch_size must be > 0")

    worker_id = _default_worker_id()

    register_builtin_specs()
    get_spec(projection_name)  # validate registered

    backoff = ExponentialBackoffSpec(
        base_seconds=float(config.base_backoff_seconds),
        max_backoff_seconds=float(config.max_backoff_seconds),
    )

    session_factory = await get_session_factory()

    last_reclaim = 0.0
    loop = asyncio.get_running_loop()

    while True:
        now = datetime.now(timezone.utc)

        async with session_factory() as session:
            # Periodic hygiene: stuck reclaim + terminal sanitize.
            now_s = loop.time()
            if (now_s - last_reclaim) >= float(config.reclaim_interval_seconds):
                await reclaim_stuck_processing(
                    session,
                    OutboxEventModel,
                    now=now,
                    max_processing_seconds=int(config.max_processing_seconds),
                    scope_predicates=(OutboxEventModel.projection == projection_name,),
                )
                await sanitize_terminal_rows(
                    session,
                    OutboxEventModel,
                    now=now,
                    scope_predicates=(OutboxEventModel.projection == projection_name,),
                )
                await session.commit()
                last_reclaim = now_s

            claimed = await claim_pending_batch(
                session,
                OutboxEventModel,
                now=now,
                batch_size=int(config.batch_size),
                worker_id=worker_id,
                lease_seconds=float(config.lease_seconds),
                scope_predicates=(OutboxEventModel.projection == projection_name,),
                order_by=(OutboxEventModel.event_version.asc(), OutboxEventModel.created_at.asc()),
            )

        if not claimed:
            if config.exit_when_idle:
                return 0
            await asyncio.sleep(float(config.poll_interval_seconds))
            continue

        # Process rows in a fresh session so claim commit doesn't interfere.
        async with session_factory() as session:
            ids = [ev.id for ev in claimed]
            await renew_lease(
                session,
                OutboxEventModel,
                ids,
                worker_id=worker_id,
                lease_seconds=float(config.lease_seconds),
                now=datetime.now(timezone.utc),
            )
            await session.commit()

            for ev in claimed:
                await _process_one(
                    session,
                    worker_id=worker_id,
                    spec_name=projection_name,
                    ev=ev,
                    max_attempts=int(config.max_attempts),
                    backoff=backoff,
                )


def _parse_args() -> tuple[str, HarnessConfig]:
    p = argparse.ArgumentParser(description="Projection framework worker harness (Route A / S2C)")
    p.add_argument("--projection", required=True, help="outbox projection name (e.g. chronicle_events_to_entries)")

    args = p.parse_args()

    lease_seconds = _get_env_int("OUTBOX_LEASE_SECONDS", 30)
    max_processing_seconds = _get_env_int("OUTBOX_MAX_PROCESSING_SECONDS", max(300, lease_seconds * 10))

    config = HarnessConfig(
        batch_size=_get_env_int("OUTBOX_BULK_SIZE", 50),
        lease_seconds=float(lease_seconds),
        max_processing_seconds=int(max_processing_seconds),
        max_attempts=_get_env_int("OUTBOX_MAX_ATTEMPTS", 10),
        base_backoff_seconds=_get_env_float("OUTBOX_BASE_BACKOFF_SECONDS", 0.5),
        max_backoff_seconds=_get_env_float("OUTBOX_MAX_BACKOFF_SECONDS", 30.0),
        poll_interval_seconds=_get_env_float("OUTBOX_POLL_INTERVAL_SECONDS", 1.0),
        reclaim_interval_seconds=_get_env_float("OUTBOX_RECLAIM_INTERVAL_SECONDS", 5.0),
        exit_when_idle=_get_env_bool("OUTBOX_EXIT_WHEN_IDLE", False),
    )
    return str(args.projection), config


def main() -> None:
    projection_name, config = _parse_args()
    asyncio.run(run_harness(projection_name=projection_name, config=config))


if __name__ == "__main__":
    main()
