from __future__ import annotations

import argparse
from collections.abc import Callable


Callback = Callable[[argparse.Namespace], int]


def build_parser(*, callbacks: dict[str, Callback]) -> argparse.ArgumentParser:
    """Build the stable argparse surface for backend/scripts/cli.py.

    This module is part of S0C-3A-3A (argparse extraction). It intentionally keeps
    the CLI surface (commands/flags/help) identical while allowing the entrypoint
    to become dispatch-only.
    """

    def cb(name: str) -> Callback:
        try:
            return callbacks[name]
        except KeyError as exc:
            raise KeyError(f"Missing CLI callback: {name}") from exc

    p = argparse.ArgumentParser(prog="scripts", description="backend/scripts router")
    sub = p.add_subparsers(dest="cmd", required=True)

    labs = sub.add_parser("labs", help="Lab/experiment commands")
    labs_sub = labs.add_subparsers(dest="labs_cmd", required=True)

    exp = labs_sub.add_parser("export-jaeger", help="Export Jaeger snapshots (wraps v1 script)")
    exp.add_argument("--service", required=True)
    exp.add_argument("--lookback", default="24h")
    exp.add_argument("--limit", type=int, default=20)
    exp.add_argument("--operation")
    exp.add_argument("--outbox-event-id")
    exp.add_argument("--claim-batch-id")
    exp.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    exp.set_defaults(func=cb("_cmd_labs_export_jaeger"))

    sv = labs_sub.add_parser(
        "shadow-verify-chronicle-entries",
        help="Labs-010: shadow verify chronicle_entries vs chronicle_events (writes _result.json)",
    )
    sv.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv.add_argument("--book-id", help="Optional book_id scope (UUID)")
    sv.add_argument("--run-id", help="Optional run_id folder name")
    sv.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv.set_defaults(func=cb("_cmd_labs_shadow_verify_chronicle_entries"))

    p2c2 = labs_sub.add_parser(
        "chronicle-entries-envelope-backfill-rehearsal",
        help="Labs-P2C2: rehearsal of chronicle_entries envelope backfill (writes _result.json)",
    )
    p2c2.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    p2c2.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    p2c2.add_argument("--run-id", help="Optional run_id folder name")
    p2c2.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    p2c2.set_defaults(func=cb("_cmd_labs_chronicle_entries_envelope_backfill_rehearsal"))

    p3c1 = labs_sub.add_parser(
        "chronicle-read-switch-smoke-rehearsal",
        help="Labs-P3C1: rehearsal of Chronicle read switch (MERGED_READ_ENABLED=0/1 smoke; writes _result.json)",
    )
    p3c1.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    p3c1.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    p3c1.add_argument("--run-id", help="Optional run_id folder name")
    p3c1.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    p3c1.set_defaults(func=cb("_cmd_labs_chronicle_read_switch_smoke_rehearsal"))

    sv_search = labs_sub.add_parser(
        "shadow-verify-search-index",
        help="Labs-011: shadow verify search_index vs source tables (writes _result.json)",
    )
    sv_search.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_search.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_search.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_search.add_argument("--run-id", help="Optional run_id folder name")
    sv_search.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_search.set_defaults(func=cb("_cmd_labs_shadow_verify_search_index"))

    sv_search_gate = labs_sub.add_parser(
        "shadow-verify-search-index-write-gate",
        help="Labs-012: write-gate verify search_index uniqueness (writes _result.json)",
    )
    sv_search_gate.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_search_gate.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_search_gate.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_search_gate.add_argument("--run-id", help="Optional run_id folder name")
    sv_search_gate.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_search_gate.set_defaults(func=cb("_cmd_labs_shadow_verify_search_index_write_gate"))

    sv_search_paging = labs_sub.add_parser(
        "shadow-verify-search-index-paging-stability",
        help="Labs-013: verify stable keyset paging over search_index (writes _result.json)",
    )
    sv_search_paging.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_search_paging.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_search_paging.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_search_paging.add_argument("--page-size", type=int, default=50)
    sv_search_paging.add_argument("--pages-checked", type=int, default=2)
    sv_search_paging.add_argument(
        "--ensure-min-rows",
        type=int,
        default=0,
        help="Optional: seed search_index rows in devtest DB to make paging checks meaningful",
    )
    sv_search_paging.add_argument("--run-id", help="Optional run_id folder name")
    sv_search_paging.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_search_paging.set_defaults(func=cb("_cmd_labs_shadow_verify_search_index_paging_stability"))

    sv_keys = labs_sub.add_parser(
        "shadow-verify-shared-keys",
        help="Labs-014: emit shared-key evidence bundle (writes _result.json)",
    )
    sv_keys.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_keys.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_keys.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_keys.add_argument(
        "--ensure-min-rows",
        type=int,
        default=0,
        help="Optional: seed search_index rows in devtest DB to ensure sample keys exist",
    )
    sv_keys.add_argument("--run-id", help="Optional run_id folder name")
    sv_keys.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_keys.set_defaults(func=cb("_cmd_labs_shadow_verify_shared_keys"))

    sv_ready = labs_sub.add_parser(
        "shadow-verify-dual-run-readiness-gate",
        help="Labs-015: dry-run readiness gate (aggregates 1A+2A prerequisites; writes _result.json)",
    )
    sv_ready.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_ready.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_ready.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_ready.add_argument("--page-size", type=int, default=50)
    sv_ready.add_argument("--pages-checked", type=int, default=2)
    sv_ready.add_argument("--ensure-min-rows-paging", type=int, default=120)
    sv_ready.add_argument("--ensure-min-rows-keys", type=int, default=5)
    sv_ready.add_argument("--run-id", help="Optional run_id folder name")
    sv_ready.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_ready.set_defaults(func=cb("_cmd_labs_shadow_verify_dual_run_readiness_gate"))

    sv_dualrun = labs_sub.add_parser(
        "shadow-verify-dual-run-stage1",
        help="Labs-018: true dual-run parity (Postgres vs Elasticsearch; writes _result.json)",
    )
    sv_dualrun.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_dualrun.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_dualrun.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_dualrun.add_argument(
        "--ensure-min-rows",
        type=int,
        default=25,
        help="Optional: seed search_index rows (entity_type=block) so Postgres+ES queries have candidates",
    )
    sv_dualrun.add_argument("--candidate-limit", type=int, default=20)
    sv_dualrun.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_dualrun.add_argument("--es-url", help="Override ELASTIC_URL (default: env or http://127.0.0.1:19200)")
    sv_dualrun.add_argument("--es-index", help="Override ELASTIC_INDEX (default: drill-scoped)")
    sv_dualrun.add_argument("--recreate-index", action=argparse.BooleanOptionalAction, default=True)
    sv_dualrun.add_argument("--backfill-batch-size", type=int, default=200)
    sv_dualrun.add_argument("--token", help="Optional: override the deterministic query token")
    sv_dualrun.add_argument("--run-id", help="Optional run_id folder name")
    sv_dualrun.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_dualrun.set_defaults(func=cb("_cmd_labs_shadow_verify_dual_run_stage1"))

    sv_dualrun2 = labs_sub.add_parser(
        "shadow-verify-dual-run-stage2",
        help="Labs-019: true dual-run (outbox worker to ES) + parity verify (writes _result.json)",
    )
    sv_dualrun2.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_dualrun2.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_dualrun2.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_dualrun2.add_argument(
        "--ensure-min-rows",
        type=int,
        default=25,
        help="Optional: seed search_index rows (entity_type=block) so outbox+ES queries have candidates",
    )
    sv_dualrun2.add_argument("--candidate-limit", type=int, default=20)
    sv_dualrun2.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_dualrun2.add_argument("--es-url", help="Override ELASTIC_URL (default: env or http://127.0.0.1:19200)")
    sv_dualrun2.add_argument("--es-index", help="Override ELASTIC_INDEX (default: drill-scoped)")
    sv_dualrun2.add_argument("--recreate-index", action=argparse.BooleanOptionalAction, default=True)
    sv_dualrun2.add_argument("--worker-batch-size", type=int, default=100)
    sv_dualrun2.add_argument("--worker-concurrency", type=int, default=1)
    sv_dualrun2.add_argument("--worker-poll-interval-seconds", type=float, default=0.2)
    sv_dualrun2.add_argument("--worker-idle-polls-before-exit", type=int, default=2)
    sv_dualrun2.add_argument("--worker-max-runtime-seconds", type=float, default=60.0)
    sv_dualrun2.add_argument("--token", help="Optional: override the deterministic query token")
    sv_dualrun2.add_argument("--run-id", help="Optional run_id folder name")
    sv_dualrun2.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_dualrun2.set_defaults(func=cb("_cmd_labs_shadow_verify_dual_run_stage2"))

    sv_dualrun_window = labs_sub.add_parser(
        "shadow-verify-dual-run-window",
        help="Labs-020: sustained dual-run window (worker runs while enqueueing) + parity verify (writes _result.json)",
    )
    sv_dualrun_window.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_dualrun_window.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_dualrun_window.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_dualrun_window.add_argument(
        "--ensure-min-rows",
        type=int,
        default=25,
        help="Optional: seed search_index rows (entity_type=block) so outbox+ES queries have candidates",
    )
    sv_dualrun_window.add_argument("--candidate-limit", type=int, default=20)
    sv_dualrun_window.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_dualrun_window.add_argument("--duration-seconds", type=float, default=30.0)
    sv_dualrun_window.add_argument("--interval-seconds", type=float, default=1.0)
    sv_dualrun_window.add_argument("--enqueue-batch-size", type=int, default=20)
    sv_dualrun_window.add_argument("--max-total-events", type=int, default=200)
    sv_dualrun_window.add_argument("--drain-timeout-seconds", type=float, default=20.0)
    sv_dualrun_window.add_argument(
        "--max-outbox-failed",
        type=int,
        default=0,
        help="Hard gate: maximum allowed failed outbox events for the inserted ids (default: 0)",
    )
    sv_dualrun_window.add_argument(
        "--max-outbox-pending",
        type=int,
        default=0,
        help="Hard gate: maximum allowed pending outbox events at the end of the drain (default: 0)",
    )
    sv_dualrun_window.add_argument(
        "--max-outbox-processing",
        type=int,
        default=0,
        help="Hard gate: maximum allowed processing outbox events at the end of the drain (default: 0)",
    )
    sv_dualrun_window.add_argument(
        "--require-outbox-done-eq-enqueued",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Hard gate: require outbox done == enqueued_total for the inserted ids (default: true)",
    )
    sv_dualrun_window.add_argument("--es-url", help="Override ELASTIC_URL (default: env or http://127.0.0.1:19200)")
    sv_dualrun_window.add_argument("--es-index", help="Override ELASTIC_INDEX (default: drill-scoped)")
    sv_dualrun_window.add_argument("--recreate-index", action=argparse.BooleanOptionalAction, default=True)
    sv_dualrun_window.add_argument("--worker-batch-size", type=int, default=100)
    sv_dualrun_window.add_argument("--worker-concurrency", type=int, default=1)
    sv_dualrun_window.add_argument("--worker-poll-interval-seconds", type=float, default=0.2)
    sv_dualrun_window.add_argument("--worker-max-runtime-seconds", type=float, default=120.0)
    sv_dualrun_window.add_argument("--token", help="Optional: override the deterministic query token")
    sv_dualrun_window.add_argument("--run-id", help="Optional run_id folder name")
    sv_dualrun_window.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_dualrun_window.set_defaults(func=cb("_cmd_labs_shadow_verify_dual_run_window"))

    sv_canary = labs_sub.add_parser(
        "shadow-verify-canary-dual-write",
        help="Labs-016: canary dual-write (projection + outbox) with rollback/cleanup (writes _result.json)",
    )
    sv_canary.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_canary.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_canary.add_argument("--library-id", help="Optional library_id scope (UUID)")
    sv_canary.add_argument("--max-writes", type=int, default=5)
    sv_canary.add_argument(
        "--cleanup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When enabled, deletes the canary rows (rollback) after verification",
    )
    sv_canary.add_argument("--run-id", help="Optional run_id folder name")
    sv_canary.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_canary.set_defaults(func=cb("_cmd_labs_shadow_verify_canary_dual_write"))

    sv_sampling = labs_sub.add_parser(
        "shadow-verify-dual-write-sampling",
        help="Labs-017: allowlist/sampling sustained dual-write (outbox enqueue) + DLQ/replay evidence (writes _result.json)",
    )
    sv_sampling.add_argument("--env-file", help="Optional .env file to load (repo-root relative by default)")
    sv_sampling.add_argument("--database-url", help="Override DATABASE_URL (do not persist DSN in snapshots)")
    sv_sampling.add_argument("--library-id", help="Optional library_id allowlist scope (UUID)")
    sv_sampling.add_argument(
        "--entity-types",
        default="",
        help="Optional allowlist for search_index.entity_type (comma-separated); empty means all",
    )
    sv_sampling.add_argument(
        "--ensure-min-rows",
        type=int,
        default=0,
        help="Optional: seed search_index rows in devtest DB so sampling has candidates",
    )
    sv_sampling.add_argument("--sample-size", type=int, default=20)
    sv_sampling.add_argument("--duration-seconds", type=int, default=0, help="0 means single batch")
    sv_sampling.add_argument("--interval-seconds", type=float, default=1.0)
    sv_sampling.add_argument("--max-total-events", type=int, default=100)
    sv_sampling.add_argument("--strategy", choices=["soft", "strict"], default="strict")
    sv_sampling.add_argument(
        "--inject-failed-rate",
        type=float,
        default=0.0,
        help="Simulate new-side failure: fraction of inserted rows to mark failed (DLQ)",
    )
    sv_sampling.add_argument(
        "--replay-failed",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="When enabled, replays simulated failed rows back to pending with audit fields",
    )
    sv_sampling.add_argument("--replay-by", default="labs", help="Replay audit: operator identifier")
    sv_sampling.add_argument("--replay-reason", default="labs drill", help="Replay audit: reason")
    sv_sampling.add_argument(
        "--cleanup",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="When enabled, deletes inserted outbox rows after verification",
    )
    sv_sampling.add_argument("--run-id", help="Optional run_id folder name")
    sv_sampling.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")
    sv_sampling.set_defaults(func=cb("_cmd_labs_shadow_verify_dual_write_sampling"))

    b = labs_sub.add_parser("expb-es429", help="Run Labs-009 ExpB (ES 429 injection) bounded")
    b.add_argument("--service", default="wordloom-search-outbox-worker")
    b.add_argument("--lookback", default="24h")
    b.add_argument("--limit", type=int, default=20)
    b.add_argument("--duration", type=int, default=30, help="Seconds to run worker; 0 means run until it exits")
    b.add_argument("--run-id", help="Optional run_id folder name")
    b.add_argument("--outdir", help="Output directory; defaults under docs/labs/_snapshot")

    b.add_argument("--every-n", type=int, default=2)
    b.add_argument("--ratio", type=float)
    b.add_argument("--seed", type=int, default=1)
    b.add_argument("--ops", default="delete", help="Comma-separated ops, e.g. upsert,delete")
    b.add_argument("--metrics-port", type=int)

    b.set_defaults(func=cb("_cmd_labs_expb_es429"))

    run = labs_sub.add_parser("run", help="Run a lab scenario (auto snapshot outputs)")
    run_sub = run.add_subparsers(dest="scenario", required=True)

    c_run = run_sub.add_parser("es_write_block_4xx", help="ExpC: ES index write-block -> deterministic 4xx")
    c_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    c_run.add_argument("--service", default="wordloom-search-outbox-worker")
    c_run.add_argument("--duration", type=int, default=20)
    c_run.add_argument("--metrics-port", type=int, default=9109)
    c_run.add_argument("--scrape-delay", type=float, default=2.0)
    c_run.add_argument("--run-id")
    c_run.add_argument("--outdir")
    c_run.set_defaults(func=cb("_cmd_labs_run_es_write_block_4xx"))

    b_run = run_sub.add_parser("es_429_inject", help="ExpB: deterministic ES 429 injection (retry/backoff)")
    b_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    b_run.add_argument("--service", default="wordloom-search-outbox-worker")
    b_run.add_argument("--duration", type=int, default=20)
    b_run.add_argument("--metrics-port", type=int, default=9109)
    b_run.add_argument("--scrape-delay", type=float, default=2.0)
    b_run.add_argument("--run-id")
    b_run.add_argument("--outdir")
    b_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    b_run.add_argument("--every-n", type=int, default=1, help="Inject 1 out of N operations deterministically")
    b_run.add_argument("--ratio", type=float, default=0.0, help="Probabilistic injection ratio (used when every-n<=0)")
    b_run.add_argument("--ops", default="upsert", help="Comma-separated ops to apply injection to")
    b_run.add_argument("--seed", type=int, default=1)
    b_run.set_defaults(func=cb("_cmd_labs_run_es_429_inject"))

    a_run = run_sub.add_parser("es_down_connect", help="ExpA: stop ES -> connect failure -> retry/backoff")
    a_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    a_run.add_argument("--service", default="wordloom-search-outbox-worker")
    a_run.add_argument("--duration", type=int, default=20)
    a_run.add_argument("--metrics-port", type=int, default=9109)
    a_run.add_argument("--scrape-delay", type=float, default=2.0)
    a_run.add_argument("--run-id")
    a_run.add_argument("--outdir")
    a_run.add_argument("--op", default="delete", choices=["upsert", "delete"], help="Outbox op to trigger")
    a_run.set_defaults(func=cb("_cmd_labs_run_es_down_connect"))

    cd_run = run_sub.add_parser("collector_down", help="P1: stop Jaeger collector/query while worker runs")
    cd_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    cd_run.add_argument("--service", default="wordloom-search-outbox-worker")
    cd_run.add_argument("--duration", type=int, default=20)
    cd_run.add_argument("--metrics-port", type=int, default=9109)
    cd_run.add_argument("--scrape-delay", type=float, default=2.0)
    cd_run.add_argument("--run-id")
    cd_run.add_argument("--outdir")
    cd_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    cd_run.set_defaults(func=cb("_cmd_labs_run_collector_down"))

    d_run = run_sub.add_parser("es_bulk_partial", help="ExpD: ES bulk partial success (mixed item outcomes)")
    d_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    d_run.add_argument("--service", default="wordloom-search-outbox-worker")
    d_run.add_argument("--duration", type=int, default=20)
    d_run.add_argument("--metrics-port", type=int, default=9109)
    d_run.add_argument("--scrape-delay", type=float, default=2.0)
    d_run.add_argument("--run-id")
    d_run.add_argument("--outdir")
    d_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    d_run.add_argument("--trigger-count", type=int, default=2, help="How many outbox events to insert")
    d_run.add_argument("--bulk-size", type=int, default=10, help="OUTBOX_BULK_SIZE for the worker")
    d_run.add_argument("--partial-status", type=int, default=400, help="Injected bulk-item status code")
    d_run.set_defaults(func=cb("_cmd_labs_run_es_bulk_partial"))

    e_run = run_sub.add_parser("db_claim_contention", help="ExpE: DB claim contention (two workers, non-atomic claim)")
    e_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    e_run.add_argument("--service", default="wordloom-search-outbox-worker")
    e_run.add_argument("--duration", type=int, default=25)
    e_run.add_argument("--metrics-port-1", dest="metrics_port_1", type=int, default=9126)
    e_run.add_argument("--metrics-port-2", dest="metrics_port_2", type=int, default=9127)
    e_run.add_argument("--worker-id-1", dest="worker_id_1", default="labs-expE-w1")
    e_run.add_argument("--worker-id-2", dest="worker_id_2", default="labs-expE-w2")
    e_run.add_argument("--scrape-delay", type=float, default=2.0)
    e_run.add_argument("--run-id")
    e_run.add_argument("--outdir")
    e_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    e_run.add_argument("--trigger-count", type=int, default=1, help="How many outbox events to insert")
    e_run.add_argument("--break-claim-sleep", type=float, default=1.0, help="Delay between SELECT and UPDATE in non-atomic claim")
    e_run.add_argument("--poll-interval", type=float, default=0.05)
    e_run.add_argument("--batch-size", type=int, default=50)
    e_run.set_defaults(func=cb("_cmd_labs_run_db_claim_contention"))

    f_run = run_sub.add_parser("stuck_reclaim", help="ExpF: stuck & reclaim (kill worker1 mid-lease; worker2 reclaims)")
    f_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    f_run.add_argument("--service", default="wordloom-search-outbox-worker")
    f_run.add_argument("--duration", type=int, default=20, help="How long to keep worker2 running")
    f_run.add_argument("--metrics-port-1", dest="metrics_port_1", type=int, default=19128)
    f_run.add_argument("--metrics-port-2", dest="metrics_port_2", type=int, default=19129)
    f_run.add_argument("--worker-id-1", dest="worker_id_1", default="labs-expF-w1")
    f_run.add_argument("--worker-id-2", dest="worker_id_2", default="labs-expF-w2")
    f_run.add_argument("--scrape-delay", type=float, default=2.0)
    f_run.add_argument("--run-id")
    f_run.add_argument("--outdir")
    f_run.add_argument("--op", default="upsert", choices=["upsert", "delete"], help="Outbox op to trigger")
    f_run.add_argument("--trigger-count", type=int, default=5, help="How many outbox events to insert")
    f_run.add_argument("--lease-seconds", dest="lease_seconds", type=int, default=3)
    f_run.add_argument("--reclaim-interval", dest="reclaim_interval", type=float, default=1.0)
    f_run.add_argument("--max-processing-seconds", dest="max_processing_seconds", type=int, default=60)
    f_run.add_argument("--poll-interval", dest="poll_interval", type=float, default=0.1)
    f_run.add_argument("--batch-size", dest="batch_size", type=int, default=50)
    f_run.add_argument("--claim-timeout", dest="claim_timeout", type=float, default=8.0)
    f_run.set_defaults(func=cb("_cmd_labs_run_stuck_reclaim"))

    g_run = run_sub.add_parser("duplicate_delivery", help="ExpG: duplicate delivery / idempotent noop (delete 404)")
    g_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    g_run.add_argument("--service", default="wordloom-search-outbox-worker")
    g_run.add_argument("--duration", type=int, default=20)
    g_run.add_argument("--metrics-port", type=int, default=19130)
    g_run.add_argument("--scrape-delay", type=float, default=2.0)
    g_run.add_argument("--run-id")
    g_run.add_argument("--outdir")
    g_run.add_argument("--entity-type", dest="entity_type", default="book")
    g_run.add_argument("--entity-id", dest="entity_id", help="Optional explicit entity_id (UUID or string)")
    g_run.add_argument("--delete-count", dest="delete_count", type=int, default=2)
    g_run.set_defaults(func=cb("_cmd_labs_run_duplicate_delivery"))

    h_run = run_sub.add_parser("projection_version", help="ExpH: projection_version (chronicle projector v1/v2)")
    h_run.add_argument("--env-file", default=".env.test", help="Env file to load (repo-root relative by default)")
    h_run.add_argument("--service", default="wordloom-chronicle-outbox-worker")
    h_run.add_argument("--duration", type=int, default=8)
    h_run.add_argument("--metrics-port", type=int, default=19110)
    h_run.add_argument("--scrape-delay", type=float, default=1.5)
    h_run.add_argument("--run-id")
    h_run.add_argument("--outdir")
    h_run.add_argument("--projection-version-1", dest="projection_version_1", type=int, default=1)
    h_run.add_argument("--projection-version-2", dest="projection_version_2", type=int, default=2)
    h_run.add_argument("--poll-interval", type=float, default=0.2)
    h_run.add_argument("--batch-size", type=int, default=50)
    h_run.add_argument("--lease-seconds", dest="lease_seconds", type=int, default=10)
    h_run.add_argument("--reclaim-interval", dest="reclaim_interval", type=float, default=2.0)
    h_run.add_argument("--max-processing-seconds", dest="max_processing_seconds", type=int, default=60)
    h_run.set_defaults(func=cb("_cmd_labs_run_projection_version"))

    verify = labs_sub.add_parser("verify", help="Verify a scenario run using captured evidence")
    verify_sub = verify.add_subparsers(dest="scenario", required=True)

    c_verify = verify_sub.add_parser("es_write_block_4xx", help="Verify ExpC run")
    c_verify.add_argument("--run-id")
    c_verify.add_argument("--outdir")
    c_verify.add_argument("--min-failed-delta", type=float, default=1.0)
    c_verify.add_argument("--max-retry-delta", type=float, default=0.0)
    c_verify.set_defaults(func=cb("_cmd_labs_verify_es_write_block_4xx"))

    b_verify = verify_sub.add_parser("es_429_inject", help="Verify ExpB run")
    b_verify.add_argument("--run-id")
    b_verify.add_argument("--outdir")
    b_verify.add_argument("--min-retry-delta", type=float, default=1.0)
    b_verify.add_argument("--min-failed-delta", type=float, default=1.0)
    b_verify.add_argument("--max-terminal-delta", type=float, default=0.0)
    b_verify.set_defaults(func=cb("_cmd_labs_verify_es_429_inject"))

    a_verify = verify_sub.add_parser("es_down_connect", help="Verify ExpA run")
    a_verify.add_argument("--run-id")
    a_verify.add_argument("--outdir")
    a_verify.add_argument("--min-retry-delta", type=float, default=1.0)
    a_verify.add_argument("--min-failed-delta", type=float, default=1.0)
    a_verify.add_argument("--max-terminal-delta", type=float, default=0.0)
    a_verify.set_defaults(func=cb("_cmd_labs_verify_es_down_connect"))

    cd_verify = verify_sub.add_parser("collector_down", help="Verify P1 collector_down run")
    cd_verify.add_argument("--run-id")
    cd_verify.add_argument("--outdir")
    cd_verify.add_argument("--min-processed-delta", type=float, default=1.0)
    cd_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    cd_verify.set_defaults(func=cb("_cmd_labs_verify_collector_down"))

    d_verify = verify_sub.add_parser("es_bulk_partial", help="Verify ExpD run")
    d_verify.add_argument("--run-id")
    d_verify.add_argument("--outdir")
    d_verify.add_argument("--min-partial-delta", type=float, default=1.0)
    d_verify.add_argument("--min-success-items-delta", type=float, default=1.0)
    d_verify.add_argument("--min-failed-items-delta", type=float, default=1.0)
    d_verify.add_argument("--min-failed-4xx-delta", type=float, default=1.0)
    d_verify.set_defaults(func=cb("_cmd_labs_verify_es_bulk_partial"))

    e_verify = verify_sub.add_parser("db_claim_contention", help="Verify ExpE run")
    e_verify.add_argument("--run-id")
    e_verify.add_argument("--outdir")
    e_verify.add_argument("--min-owner-mismatch-delta", type=float, default=1.0)
    e_verify.add_argument("--min-processed-delta", type=float, default=1.0)
    e_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    e_verify.set_defaults(func=cb("_cmd_labs_verify_db_claim_contention"))

    f_verify = verify_sub.add_parser("stuck_reclaim", help="Verify ExpF run")
    f_verify.add_argument("--run-id")
    f_verify.add_argument("--outdir")
    f_verify.add_argument("--min-processed-delta", type=float, default=1.0)
    f_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    f_verify.add_argument("--min-reclaimed", type=int, default=1)
    f_verify.set_defaults(func=cb("_cmd_labs_verify_stuck_reclaim"))

    g_verify = verify_sub.add_parser("duplicate_delivery", help="Verify ExpG run")
    g_verify.add_argument("--run-id")
    g_verify.add_argument("--outdir")
    g_verify.add_argument("--min-processed-delta", type=float, default=3.0)
    g_verify.add_argument("--max-failed-delta", type=float, default=0.0)
    g_verify.add_argument("--min-noop-delta", type=float, default=1.0)
    g_verify.add_argument("--min-noop-logs", type=int, default=1)
    g_verify.set_defaults(func=cb("_cmd_labs_verify_duplicate_delivery"))

    h_verify = verify_sub.add_parser("projection_version", help="Verify ExpH run")
    h_verify.add_argument("--run-id")
    h_verify.add_argument("--outdir")
    h_verify.add_argument("--projection-version-1", dest="projection_version_1", type=int, default=1)
    h_verify.add_argument("--projection-version-2", dest="projection_version_2", type=int, default=2)
    h_verify.set_defaults(func=cb("_cmd_labs_verify_projection_version"))

    export = labs_sub.add_parser("export", help="Export additional evidence (e.g. Jaeger) for a run")
    export_sub = export.add_subparsers(dest="scenario", required=True)

    c_export = export_sub.add_parser("es_write_block_4xx", help="Export Jaeger traces for ExpC run")
    c_export.add_argument("--run-id")
    c_export.add_argument("--outdir")
    c_export.add_argument("--service", default="wordloom-search-outbox-worker")
    c_export.add_argument("--lookback", default="1h")
    c_export.add_argument("--limit", type=int, default=20)
    c_export.set_defaults(func=cb("_cmd_labs_export_es_write_block_4xx"))

    b_export = export_sub.add_parser("es_429_inject", help="Export Jaeger traces for ExpB run")
    b_export.add_argument("--run-id")
    b_export.add_argument("--outdir")
    b_export.add_argument("--service", default="wordloom-search-outbox-worker")
    b_export.add_argument("--lookback", default="1h")
    b_export.add_argument("--limit", type=int, default=20)
    b_export.set_defaults(func=cb("_cmd_labs_export_es_429_inject"))

    a_export = export_sub.add_parser("es_down_connect", help="Export Jaeger traces for ExpA run")
    a_export.add_argument("--run-id")
    a_export.add_argument("--outdir")
    a_export.add_argument("--service", default="wordloom-search-outbox-worker")
    a_export.add_argument("--lookback", default="1h")
    a_export.add_argument("--limit", type=int, default=20)
    a_export.set_defaults(func=cb("_cmd_labs_export_es_down_connect"))

    cd_export = export_sub.add_parser("collector_down", help="Export Jaeger traces for P1 collector_down run")
    cd_export.add_argument("--run-id")
    cd_export.add_argument("--outdir")
    cd_export.add_argument("--service", default="wordloom-search-outbox-worker")
    cd_export.add_argument("--lookback", default="30m")
    cd_export.add_argument("--limit", type=int, default=20)
    cd_export.set_defaults(func=cb("_cmd_labs_export_collector_down"))

    d_export = export_sub.add_parser("es_bulk_partial", help="Export Jaeger traces for ExpD run")
    d_export.add_argument("--run-id")
    d_export.add_argument("--outdir")
    d_export.add_argument("--service", default="wordloom-search-outbox-worker")
    d_export.add_argument("--lookback", default="1h")
    d_export.add_argument("--limit", type=int, default=20)
    d_export.set_defaults(func=cb("_cmd_labs_export_es_bulk_partial"))

    e_export = export_sub.add_parser("db_claim_contention", help="Export Jaeger traces for ExpE run")
    e_export.add_argument("--run-id")
    e_export.add_argument("--outdir")
    e_export.add_argument("--service", default="wordloom-search-outbox-worker")
    e_export.add_argument("--lookback", default="30m")
    e_export.add_argument("--limit", type=int, default=50)
    e_export.set_defaults(func=cb("_cmd_labs_export_db_claim_contention"))

    f_export = export_sub.add_parser("stuck_reclaim", help="Export Jaeger traces for ExpF run")
    f_export.add_argument("--run-id")
    f_export.add_argument("--outdir")
    f_export.add_argument("--service", default="wordloom-search-outbox-worker")
    f_export.add_argument("--lookback", default="30m")
    f_export.add_argument("--limit", type=int, default=50)
    f_export.set_defaults(func=cb("_cmd_labs_export_stuck_reclaim"))

    g_export = export_sub.add_parser("duplicate_delivery", help="Export Jaeger traces for ExpG run")
    g_export.add_argument("--run-id")
    g_export.add_argument("--outdir")
    g_export.add_argument("--service", default="wordloom-search-outbox-worker")
    g_export.add_argument("--lookback", default="30m")
    g_export.add_argument("--limit", type=int, default=50)
    g_export.set_defaults(func=cb("_cmd_labs_export_duplicate_delivery"))

    h_export = export_sub.add_parser("projection_version", help="Export Jaeger traces for ExpH run")
    h_export.add_argument("--run-id")
    h_export.add_argument("--outdir")
    h_export.add_argument("--service", default="wordloom-chronicle-outbox-worker")
    h_export.add_argument("--lookback", default="30m")
    h_export.add_argument("--limit", type=int, default=50)
    h_export.set_defaults(func=cb("_cmd_labs_export_projection_version"))

    clean = labs_sub.add_parser("clean", help="Cleanup a scenario (revert injection / prune snapshots)")
    clean_sub = clean.add_subparsers(dest="scenario", required=True)

    clean_common = argparse.ArgumentParser(add_help=False)
    clean_common.add_argument(
        "--env-file",
        default=".env.test",
        help="Env file to load (repo-root relative by default). Only used by scenarios that revert external state.",
    )

    c_clean = clean_sub.add_parser(
        "es_write_block_4xx",
        help="Disable write block + optional snapshot pruning",
        parents=[clean_common],
    )
    c_clean.add_argument("--outdir")
    c_clean.add_argument("--keep-last", type=int, default=None)
    c_clean.set_defaults(func=cb("_cmd_labs_clean_es_write_block_4xx"))

    b_clean = clean_sub.add_parser(
        "es_429_inject",
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    b_clean.add_argument("--outdir")
    b_clean.add_argument("--keep-last", type=int, default=None)
    b_clean.set_defaults(func=cb("_cmd_labs_clean_es_429_inject"))

    a_clean = clean_sub.add_parser(
        "es_down_connect",
        help="Start ES + optional snapshot pruning",
        parents=[clean_common],
    )
    a_clean.add_argument("--outdir")
    a_clean.add_argument("--keep-last", type=int, default=None)
    a_clean.set_defaults(func=cb("_cmd_labs_clean_es_down_connect"))

    cd_clean = clean_sub.add_parser(
        "collector_down",
        help="Start Jaeger + optional snapshot pruning",
        parents=[clean_common],
    )
    cd_clean.add_argument("--outdir")
    cd_clean.add_argument("--keep-last", type=int, default=None)
    cd_clean.set_defaults(func=cb("_cmd_labs_clean_collector_down"))

    d_clean = clean_sub.add_parser(
        "es_bulk_partial",
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    d_clean.add_argument("--outdir")
    d_clean.add_argument("--keep-last", type=int, default=None)
    d_clean.set_defaults(func=cb("_cmd_labs_clean_es_bulk_partial"))

    e_clean = clean_sub.add_parser(
        "db_claim_contention",
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    e_clean.add_argument("--outdir")
    e_clean.add_argument("--keep-last", type=int, default=None)
    e_clean.set_defaults(func=cb("_cmd_labs_clean_db_claim_contention"))

    f_clean = clean_sub.add_parser(
        "stuck_reclaim",
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    f_clean.add_argument("--outdir")
    f_clean.add_argument("--keep-last", type=int, default=None)
    f_clean.set_defaults(func=cb("_cmd_labs_clean_stuck_reclaim"))

    g_clean = clean_sub.add_parser(
        "duplicate_delivery",
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    g_clean.add_argument("--outdir")
    g_clean.add_argument("--keep-last", type=int, default=None)
    g_clean.set_defaults(func=cb("_cmd_labs_clean_duplicate_delivery"))

    h_clean = clean_sub.add_parser(
        "projection_version",
        help="Noop cleanup + optional snapshot pruning",
        parents=[clean_common],
    )
    h_clean.add_argument("--outdir")
    h_clean.add_argument("--keep-last", type=int, default=None)
    h_clean.set_defaults(func=cb("_cmd_labs_clean_projection_version"))

    return p
