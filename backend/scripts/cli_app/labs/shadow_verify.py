from __future__ import annotations

import argparse
import re
import uuid
from collections.abc import Callable
from pathlib import Path

from cli_app import registry as _wg_registry
from cli_app.common import build_evidence_paths_for_dir, pack_artifacts
from cli_app.types import DrillInputs


def _require_database_url(*, env: dict[str, str], provided: str | None, log_prefix: str) -> str | None:
    database_url = (provided or env.get("DATABASE_URL") or "").strip()
    if not database_url:
        print(f"[{log_prefix}] DATABASE_URL is required (via env or --database-url)")
        return None
    return database_url


def _parse_optional_uuid(*, value: str | None, arg_name: str, log_prefix: str) -> str | None:
    v = (value or "").strip() or None
    if v is None:
        return None
    try:
        uuid.UUID(v)
    except ValueError:
        print(f"[{log_prefix}] invalid {arg_name}: {v}")
        raise SystemExit(2)
    return v


def _invoke_and_pack(*, scenario: str, payload: dict[str, object], outdir: Path) -> dict[str, object]:
    _wg_registry.load_builtin_scenarios()
    handler = _wg_registry.get(scenario)

    inputs = DrillInputs.model_validate(payload)
    drill = handler(inputs)
    result = drill.meta or {}
    pack_artifacts(paths=build_evidence_paths_for_dir(outdir), result=result)
    return result


def cmd_labs_shadow_verify_chronicle_entries(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-chronicle-entries"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        book_id = _parse_optional_uuid(value=getattr(args, "book_id", None), arg_name="--book-id", log_prefix=log_prefix)
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "book_id": book_id,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    events_total = int(result.get("events_total") or 0)
    entries_total = int(result.get("entries_total") or 0)
    missing_entries = int(result.get("missing_entries") or 0)
    extra_entries = int(result.get("extra_entries") or 0)
    mismatched_book_id = int(result.get("mismatched_book_id") or 0)

    print("labs-010.shadow_verify_chronicle_entries")
    print(f"scope={scope}")
    print(f"events_total={events_total}")
    print(f"entries_total={entries_total}")
    print(f"missing_entries={missing_entries}")
    print(f"extra_entries={extra_entries}")
    print(f"mismatched_book_id={mismatched_book_id}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_search_index(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-search-index"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    blocks_total = int(result.get("blocks_total") or 0)
    blocks_index_total = int(result.get("blocks_index_total") or 0)
    blocks_missing = int(result.get("blocks_missing") or 0)
    blocks_extra = int(result.get("blocks_extra") or 0)
    blocks_mismatched_library_id = int(result.get("blocks_mismatched_library_id") or 0)
    books_total = int(result.get("books_total") or 0)
    books_index_total = int(result.get("books_index_total") or 0)
    books_missing = int(result.get("books_missing") or 0)
    books_extra = int(result.get("books_extra") or 0)
    books_mismatched_library_id = int(result.get("books_mismatched_library_id") or 0)
    tags_total = int(result.get("tags_total") or 0)
    tags_index_total = int(result.get("tags_index_total") or 0)
    tags_missing = int(result.get("tags_missing") or 0)
    tags_extra = int(result.get("tags_extra") or 0)
    tags_invalid_library_id = int(result.get("tags_invalid_library_id") or 0)
    outbox_total = int(result.get("outbox_total") or 0)
    outbox_pending = int(result.get("outbox_pending") or 0)
    outbox_processing = int(result.get("outbox_processing") or 0)
    outbox_done = int(result.get("outbox_done") or 0)
    outbox_failed = int(result.get("outbox_failed") or 0)

    print("labs-011.shadow_verify_search_index")
    print(f"scope={scope}")
    print(f"blocks_total={blocks_total}")
    print(f"blocks_index_total={blocks_index_total}")
    print(f"blocks_missing={blocks_missing}")
    print(f"blocks_extra={blocks_extra}")
    print(f"blocks_mismatched_library_id={blocks_mismatched_library_id}")
    print(f"books_total={books_total}")
    print(f"books_index_total={books_index_total}")
    print(f"books_missing={books_missing}")
    print(f"books_extra={books_extra}")
    print(f"books_mismatched_library_id={books_mismatched_library_id}")
    print(f"tags_total={tags_total}")
    print(f"tags_index_total={tags_index_total}")
    print(f"tags_missing={tags_missing}")
    print(f"tags_extra={tags_extra}")
    print(f"tags_invalid_library_id={tags_invalid_library_id}")
    print(f"outbox_total={outbox_total}")
    print(f"outbox_pending={outbox_pending}")
    print(f"outbox_processing={outbox_processing}")
    print(f"outbox_done={outbox_done}")
    print(f"outbox_failed={outbox_failed}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_search_index_write_gate(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-search-index-write-gate"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    duplicates_groups_total = int(result.get("duplicates_groups_total") or 0)
    duplicates_extra_rows_total = int(result.get("duplicates_extra_rows_total") or 0)
    duplicates_groups_scoped = result.get("duplicates_groups_scoped")
    duplicates_extra_rows_scoped = result.get("duplicates_extra_rows_scoped")

    print("labs-012.shadow_verify_search_index_write_gate")
    print(f"scope={scope}")
    print(f"duplicates_groups_total={duplicates_groups_total}")
    print(f"duplicates_extra_rows_total={duplicates_extra_rows_total}")
    if duplicates_groups_scoped is not None:
        print(f"duplicates_groups_scoped={duplicates_groups_scoped}")
    if duplicates_extra_rows_scoped is not None:
        print(f"duplicates_extra_rows_scoped={duplicates_extra_rows_scoped}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_search_index_paging_stability(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-search-index-paging-stability"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    page_size = int(args.page_size)
    pages_checked = int(args.pages_checked)
    ensure_min_rows = int(args.ensure_min_rows)
    if page_size <= 0:
        print(f"[{log_prefix}] --page-size must be > 0")
        return 2
    if pages_checked < 2:
        print(f"[{log_prefix}] --pages-checked must be >= 2")
        return 2
    if ensure_min_rows < 0:
        print(f"[{log_prefix}] --ensure-min-rows must be >= 0")
        return 2

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    order_key = result.get("order_key")
    rows_total = int(result.get("rows_total") or 0)
    inserted_rows = int(result.get("seed_rows_inserted") or 0)
    data_sufficient = bool(result.get("data_sufficient"))
    duplicates_across_pages_total = int(result.get("duplicates_across_pages_total") or 0)
    ordering_ok = bool(result.get("ordering_ok"))
    pages_returned = int(result.get("pages_returned") or 0)

    print("labs-013.shadow_verify_search_index_paging_stability")
    print(f"scope={scope}")
    print(f"order_key={order_key}")
    print(f"page_size={page_size}")
    print(f"pages_checked={pages_checked}")
    print(f"pages_returned={pages_returned}")
    print(f"rows_total={rows_total}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={inserted_rows}")
    print(f"data_sufficient={data_sufficient}")
    print(f"duplicates_across_pages_total={duplicates_across_pages_total}")
    print(f"ordering_ok={ordering_ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_shared_keys(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-shared-keys"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    ensure_min_rows = int(args.ensure_min_rows)
    if ensure_min_rows < 0:
        print(f"[{log_prefix}] --ensure-min-rows must be >= 0")
        return 2

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    inserted_rows = int(result.get("seed_rows_inserted") or 0)
    shared_keys = result.get("shared_keys") or {}
    samples = list(shared_keys.get("samples") or [])

    print("labs-014.shadow_verify_shared_keys")
    print(f"scope={scope}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={inserted_rows}")
    print(f"samples_total={len(samples)}")
    if samples:
        print(f"sample_entity_type={samples[0]['entity_type']}")
        print(f"sample_entity_id={samples[0]['entity_id']}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_dual_run_readiness_gate(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-dual-run-readiness-gate"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    page_size = int(args.page_size)
    pages_checked = int(args.pages_checked)
    ensure_min_rows_paging = int(args.ensure_min_rows_paging)
    ensure_min_rows_keys = int(args.ensure_min_rows_keys)
    if page_size <= 0:
        print(f"[{log_prefix}] --page-size must be > 0")
        return 2
    if pages_checked < 2:
        print(f"[{log_prefix}] --pages-checked must be >= 2")
        return 2
    if ensure_min_rows_paging < 0 or ensure_min_rows_keys < 0:
        print(f"[{log_prefix}] --ensure-min-rows-* must be >= 0")
        return 2

    scope = "all" if library_id is None else f"library:{library_id}"

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "page_size": page_size,
            "pages_checked": pages_checked,
            "ensure_min_rows_paging": ensure_min_rows_paging,
            "ensure_min_rows_keys": ensure_min_rows_keys,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))

    print("labs-015.shadow_verify_dual_run_readiness_gate")
    print(f"scope={scope}")
    print(f"page_size={page_size}")
    print(f"pages_checked={pages_checked}")
    print(f"ensure_min_rows_paging={ensure_min_rows_paging}")
    print(f"ensure_min_rows_keys={ensure_min_rows_keys}")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_dual_run_stage1(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-dual-run-stage1"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    ensure_min_rows = int(args.ensure_min_rows)
    candidate_limit = int(args.candidate_limit)
    backfill_batch_size = int(args.backfill_batch_size)
    strategy = str(args.strategy)

    if ensure_min_rows < 0:
        print(f"[{log_prefix}] --ensure-min-rows must be >= 0")
        return 2
    if candidate_limit <= 0:
        print(f"[{log_prefix}] --candidate-limit must be > 0")
        return 2
    if backfill_batch_size <= 0:
        print(f"[{log_prefix}] --backfill-batch-size must be > 0")
        return 2
    if strategy not in {"soft", "strict"}:
        print(f"[{log_prefix}] --strategy must be one of: soft, strict")
        return 2

    es_url = (args.es_url or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", run_id)
    token = (args.token or token_default).strip() or token_default

    def _sanitize_index_name(name: str) -> str:
        safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
        safe = re.sub(r"-+", "-", safe)
        if not safe:
            safe = "wordloom-search-index"
        return safe[:80]

    es_index = (args.es_index or env.get("ELASTIC_INDEX") or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(args.recreate_index)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "ensure_min_rows": ensure_min_rows,
            "candidate_limit": candidate_limit,
            "backfill_batch_size": backfill_batch_size,
            "strategy": strategy,
            "es_url": es_url,
            "token": token,
            "es_index": es_index,
            "recreate_index": recreate_index,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")

    inputs_obj = result.get("inputs") if isinstance(result, dict) else None
    if not isinstance(inputs_obj, dict):
        inputs_obj = {}

    token = str(inputs_obj.get("token") or token)
    strategy = str(inputs_obj.get("strategy") or strategy)

    seed_rows_inserted = int(result.get("seed_rows_inserted") or 0)

    pg_candidates: list[object] = []
    postgres_obj = result.get("postgres")
    if isinstance(postgres_obj, dict):
        cands = postgres_obj.get("candidates")
        if isinstance(cands, list):
            pg_candidates = cands
    pg_candidates_total = int(len(pg_candidates))

    es_obj = result.get("elasticsearch")
    es_health_ok = False
    backfill_ok = False
    backfill_exit_code = 0
    es_search_ok = False
    es_search_status = 0
    es_candidates_total = 0
    if isinstance(es_obj, dict):
        health = es_obj.get("health")
        if isinstance(health, dict):
            es_health_ok = bool(health.get("ok"))
        backfill = es_obj.get("backfill")
        if isinstance(backfill, dict):
            backfill_ok = bool(backfill.get("ok"))
            backfill_exit_code = int(backfill.get("exit_code") or 0)
        search = es_obj.get("search")
        if isinstance(search, dict):
            es_search_ok = bool(search.get("ok"))
            es_search_status = int(search.get("status") or 0)
            es_cands = search.get("candidates")
            if isinstance(es_cands, list):
                es_candidates_total = int(len(es_cands))

    parity_ok = False
    compare_obj = result.get("compare")
    if isinstance(compare_obj, dict):
        parity_ok = bool(compare_obj.get("parity_ok"))

    print("labs-018.shadow_verify_dual_run_stage1")
    print(f"scope={scope}")
    print(f"token={token}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={seed_rows_inserted}")
    print(f"pg_candidates_total={pg_candidates_total}")
    print(f"es_health_ok={es_health_ok}")
    print(f"backfill_ok={backfill_ok} (rc={backfill_exit_code})")
    print(f"es_search_ok={es_search_ok} (status={es_search_status})")
    print(f"es_candidates_total={es_candidates_total}")
    print(f"parity_ok={parity_ok} (strategy={strategy})")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_dual_run_stage2(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-dual-run-stage2"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    ensure_min_rows = int(args.ensure_min_rows)
    candidate_limit = int(args.candidate_limit)
    strategy = str(args.strategy)
    worker_batch_size = int(args.worker_batch_size)
    worker_concurrency = int(args.worker_concurrency)
    worker_poll_interval_seconds = float(args.worker_poll_interval_seconds)
    worker_max_runtime_seconds = float(args.worker_max_runtime_seconds)
    worker_idle_polls_before_exit = int(args.worker_idle_polls_before_exit)

    if ensure_min_rows < 0:
        print(f"[{log_prefix}] --ensure-min-rows must be >= 0")
        return 2
    if candidate_limit <= 0:
        print(f"[{log_prefix}] --candidate-limit must be > 0")
        return 2
    if strategy not in {"soft", "strict"}:
        print(f"[{log_prefix}] --strategy must be one of: soft, strict")
        return 2
    if worker_batch_size <= 0:
        print(f"[{log_prefix}] --worker-batch-size must be > 0")
        return 2
    if worker_concurrency <= 0:
        print(f"[{log_prefix}] --worker-concurrency must be > 0")
        return 2
    if worker_poll_interval_seconds < 0:
        print(f"[{log_prefix}] --worker-poll-interval-seconds must be >= 0")
        return 2
    if worker_max_runtime_seconds <= 0:
        print(f"[{log_prefix}] --worker-max-runtime-seconds must be > 0")
        return 2
    if worker_idle_polls_before_exit <= 0:
        print(f"[{log_prefix}] --worker-idle-polls-before-exit must be > 0")
        return 2

    es_url = (args.es_url or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", run_id)
    token = (args.token or token_default).strip() or token_default

    def _sanitize_index_name(name: str) -> str:
        safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
        safe = re.sub(r"-+", "-", safe)
        if not safe:
            safe = "wordloom-search-index"
        return safe[:80]

    es_index = (args.es_index or env.get("ELASTIC_INDEX") or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(args.recreate_index)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "ensure_min_rows": ensure_min_rows,
            "candidate_limit": candidate_limit,
            "strategy": strategy,
            "worker_batch_size": worker_batch_size,
            "worker_concurrency": worker_concurrency,
            "worker_poll_interval_seconds": worker_poll_interval_seconds,
            "worker_max_runtime_seconds": worker_max_runtime_seconds,
            "worker_idle_polls_before_exit": worker_idle_polls_before_exit,
            "es_url": es_url,
            "token": token,
            "es_index": es_index,
            "recreate_index": recreate_index,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or ("all" if library_id is None else f"library:{library_id}"))

    inputs_obj = result.get("inputs") if isinstance(result, dict) else None
    if not isinstance(inputs_obj, dict):
        inputs_obj = {}

    token = str(inputs_obj.get("token") or token)
    strategy = str(inputs_obj.get("strategy") or strategy)

    seed_rows_inserted = int(result.get("seed_rows_inserted") or 0)

    pg_candidates: list[object] = []
    postgres_obj = result.get("postgres")
    if isinstance(postgres_obj, dict):
        cands = postgres_obj.get("candidates")
        if isinstance(cands, list):
            pg_candidates = cands
    pg_candidates_total = int(len(pg_candidates))

    outbox_enqueued_total = 0
    outbox_done = 0
    outbox_pending = 0
    outbox_processing = 0
    outbox_failed = 0
    outbox_obj = result.get("outbox")
    if isinstance(outbox_obj, dict):
        outbox_enqueued_total = int(outbox_obj.get("enqueued_total") or 0)
        status_counts = outbox_obj.get("status_counts")
        if isinstance(status_counts, dict):
            outbox_done = int(status_counts.get("done") or 0)
            outbox_pending = int(status_counts.get("pending") or 0)
            outbox_processing = int(status_counts.get("processing") or 0)
            outbox_failed = int(status_counts.get("failed") or 0)

    es_obj = result.get("elasticsearch")
    es_health_ok = False
    es_index_ok = False
    es_index_status = 0
    es_refresh_ok = False
    es_refresh_status = 0
    es_search_ok = False
    es_search_status = 0
    es_candidates_total = 0
    if isinstance(es_obj, dict):
        health = es_obj.get("health")
        if isinstance(health, dict):
            es_health_ok = bool(health.get("ok"))
        idx = es_obj.get("index")
        if isinstance(idx, dict):
            es_index_ok = bool(idx.get("ok"))
            es_index_status = int(idx.get("status") or 0)
        refresh = es_obj.get("refresh")
        if isinstance(refresh, dict):
            es_refresh_ok = bool(refresh.get("ok"))
            es_refresh_status = int(refresh.get("status") or 0)
        search = es_obj.get("search")
        if isinstance(search, dict):
            es_search_ok = bool(search.get("ok"))
            es_search_status = int(search.get("status") or 0)
            es_cands = search.get("candidates")
            if isinstance(es_cands, list):
                es_candidates_total = int(len(es_cands))

    worker_ok = False
    worker_exit_code = 0
    worker_runtime_s = 0.0
    worker_obj = result.get("worker")
    if isinstance(worker_obj, dict):
        worker_ok = bool(worker_obj.get("ok"))
        worker_exit_code = int(worker_obj.get("exit_code") or 0)
        try:
            worker_runtime_s = float(worker_obj.get("runtime_seconds") or 0.0)
        except Exception:
            worker_runtime_s = 0.0

    parity_ok = False
    compare_obj = result.get("compare")
    if isinstance(compare_obj, dict):
        parity_ok = bool(compare_obj.get("parity_ok"))

    print("labs-019.shadow_verify_dual_run_stage2")
    print(f"scope={scope}")
    print(f"token={token}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={seed_rows_inserted}")
    print(f"pg_candidates_total={pg_candidates_total}")
    print(f"outbox_enqueued_total={outbox_enqueued_total}")
    print(
        f"outbox_done={outbox_done} pending={outbox_pending} processing={outbox_processing} failed={outbox_failed}"
    )
    print(f"es_health_ok={es_health_ok}")
    print(f"es_index_ok={es_index_ok} (status={es_index_status})")
    print(f"worker_ok={worker_ok} (rc={worker_exit_code}, runtime_s={worker_runtime_s:.2f})")
    print(f"es_refresh_ok={es_refresh_ok} (status={es_refresh_status})")
    print(f"es_search_ok={es_search_ok} (status={es_search_status})")
    print(f"es_candidates_total={es_candidates_total}")
    print(f"parity_ok={parity_ok} (strategy={strategy})")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_dual_run_window(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-dual-run-window"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    ensure_min_rows = int(args.ensure_min_rows)
    candidate_limit = int(args.candidate_limit)
    strategy = str(args.strategy)
    duration_seconds = float(args.duration_seconds)
    interval_seconds = float(args.interval_seconds)
    enqueue_batch_size = int(args.enqueue_batch_size)
    max_total_events = int(args.max_total_events)
    drain_timeout_seconds = float(args.drain_timeout_seconds)

    max_outbox_failed = int(args.max_outbox_failed)
    max_outbox_pending = int(args.max_outbox_pending)
    max_outbox_processing = int(args.max_outbox_processing)
    require_outbox_done_eq_enqueued = bool(args.require_outbox_done_eq_enqueued)

    worker_batch_size = int(args.worker_batch_size)
    worker_concurrency = int(args.worker_concurrency)
    worker_poll_interval_seconds = float(args.worker_poll_interval_seconds)
    worker_max_runtime_seconds = float(args.worker_max_runtime_seconds)

    if ensure_min_rows < 0:
        print(f"[{log_prefix}] --ensure-min-rows must be >= 0")
        return 2
    if candidate_limit <= 0:
        print(f"[{log_prefix}] --candidate-limit must be > 0")
        return 2
    if strategy not in {"soft", "strict"}:
        print(f"[{log_prefix}] --strategy must be one of: soft, strict")
        return 2
    if duration_seconds <= 0:
        print(f"[{log_prefix}] --duration-seconds must be > 0")
        return 2
    if interval_seconds <= 0:
        print(f"[{log_prefix}] --interval-seconds must be > 0")
        return 2
    if enqueue_batch_size <= 0:
        print(f"[{log_prefix}] --enqueue-batch-size must be > 0")
        return 2
    if max_total_events <= 0:
        print(f"[{log_prefix}] --max-total-events must be > 0")
        return 2
    if drain_timeout_seconds <= 0:
        print(f"[{log_prefix}] --drain-timeout-seconds must be > 0")
        return 2
    if max_outbox_failed < 0:
        print(f"[{log_prefix}] --max-outbox-failed must be >= 0")
        return 2
    if max_outbox_pending < 0:
        print(f"[{log_prefix}] --max-outbox-pending must be >= 0")
        return 2
    if max_outbox_processing < 0:
        print(f"[{log_prefix}] --max-outbox-processing must be >= 0")
        return 2
    if worker_batch_size <= 0:
        print(f"[{log_prefix}] --worker-batch-size must be > 0")
        return 2
    if worker_concurrency <= 0:
        print(f"[{log_prefix}] --worker-concurrency must be > 0")
        return 2
    if worker_poll_interval_seconds < 0:
        print(f"[{log_prefix}] --worker-poll-interval-seconds must be >= 0")
        return 2
    if worker_max_runtime_seconds <= 0:
        print(f"[{log_prefix}] --worker-max-runtime-seconds must be > 0")
        return 2

    es_url = (args.es_url or env.get("ELASTIC_URL") or "http://127.0.0.1:19200").strip().rstrip("/")
    token_default = "dualrun" + re.sub(r"[^0-9A-Za-z]+", "", run_id)
    token = (args.token or token_default).strip() or token_default

    def _sanitize_index_name(name: str) -> str:
        safe = re.sub(r"[^a-z0-9_\-]+", "-", name.lower()).strip("-_")
        safe = re.sub(r"-+", "-", safe)
        if not safe:
            safe = "wordloom-search-index"
        return safe[:80]

    es_index = (args.es_index or env.get("ELASTIC_INDEX") or _sanitize_index_name(f"wordloom-search-index-dualrun-{token}")).strip()
    es_index = _sanitize_index_name(es_index)
    recreate_index = bool(args.recreate_index)

    scope = "all" if library_id is None else f"library:{library_id}"

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "env": env,
            "database_url": database_url,
            "library_id": library_id,
            "ensure_min_rows": ensure_min_rows,
            "candidate_limit": candidate_limit,
            "strategy": strategy,
            "duration_seconds": duration_seconds,
            "interval_seconds": interval_seconds,
            "enqueue_batch_size": enqueue_batch_size,
            "max_total_events": max_total_events,
            "drain_timeout_seconds": drain_timeout_seconds,
            "max_outbox_failed": max_outbox_failed,
            "max_outbox_pending": max_outbox_pending,
            "max_outbox_processing": max_outbox_processing,
            "require_outbox_done_eq_enqueued": require_outbox_done_eq_enqueued,
            "worker_batch_size": worker_batch_size,
            "worker_concurrency": worker_concurrency,
            "worker_poll_interval_seconds": worker_poll_interval_seconds,
            "worker_max_runtime_seconds": worker_max_runtime_seconds,
            "es_url": es_url,
            "token": token,
            "es_index": es_index,
            "recreate_index": recreate_index,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or ("all" if library_id is None else f"library:{library_id}"))

    inputs_obj = result.get("inputs") if isinstance(result, dict) else None
    if not isinstance(inputs_obj, dict):
        inputs_obj = {}

    token = str(inputs_obj.get("token") or token)
    strategy = str(inputs_obj.get("strategy") or strategy)

    seed_rows_inserted = int(result.get("seed_rows_inserted") or 0)

    pg_candidates_total = 0
    postgres_obj = result.get("postgres")
    if isinstance(postgres_obj, dict):
        cands = postgres_obj.get("candidates")
        if isinstance(cands, list):
            pg_candidates_total = int(len(cands))

    outbox_enqueued_total = 0
    outbox_done = 0
    outbox_pending = 0
    outbox_processing = 0
    outbox_failed = 0
    outbox_obj = result.get("outbox")
    if isinstance(outbox_obj, dict):
        outbox_enqueued_total = int(outbox_obj.get("enqueued_total") or 0)
        status_counts = outbox_obj.get("status_counts")
        if isinstance(status_counts, dict):
            outbox_done = int(status_counts.get("done") or 0)
            outbox_pending = int(status_counts.get("pending") or 0)
            outbox_processing = int(status_counts.get("processing") or 0)
            outbox_failed = int(status_counts.get("failed") or 0)

    es_obj = result.get("elasticsearch")
    es_health_ok = False
    es_index_ok = False
    es_index_status = 0
    es_refresh_ok = False
    es_refresh_status = 0
    es_search_ok = False
    es_search_status = 0
    es_candidates_total = 0
    if isinstance(es_obj, dict):
        health = es_obj.get("health")
        if isinstance(health, dict):
            es_health_ok = bool(health.get("ok"))
        idx = es_obj.get("index")
        if isinstance(idx, dict):
            es_index_ok = bool(idx.get("ok"))
            es_index_status = int(idx.get("status") or 0)
        refresh = es_obj.get("refresh")
        if isinstance(refresh, dict):
            es_refresh_ok = bool(refresh.get("ok"))
            es_refresh_status = int(refresh.get("status") or 0)
        search = es_obj.get("search")
        if isinstance(search, dict):
            es_search_ok = bool(search.get("ok"))
            es_search_status = int(search.get("status") or 0)
            es_cands = search.get("candidates")
            if isinstance(es_cands, list):
                es_candidates_total = int(len(es_cands))

    worker_ok = False
    worker_exit_code = 0
    worker_runtime_s = 0.0
    worker_obj = result.get("worker")
    if isinstance(worker_obj, dict):
        worker_ok = bool(worker_obj.get("ok"))
        worker_exit_code = int(worker_obj.get("exit_code") or 0)
        try:
            worker_runtime_s = float(worker_obj.get("runtime_seconds") or 0.0)
        except Exception:
            worker_runtime_s = 0.0

    parity_ok = False
    compare_obj = result.get("compare")
    if isinstance(compare_obj, dict):
        parity_ok = bool(compare_obj.get("parity_ok"))

    print("labs-020.shadow_verify_dual_run_window")
    print(f"scope={scope}")
    print(f"token={token}")
    print(f"ensure_min_rows={ensure_min_rows}")
    print(f"seed_rows_inserted={seed_rows_inserted}")
    print(f"pg_candidates_total={pg_candidates_total}")
    print(f"outbox_enqueued_total={outbox_enqueued_total}")
    print(
        f"outbox_done={outbox_done} pending={outbox_pending} processing={outbox_processing} failed={outbox_failed}"
    )
    print(f"es_health_ok={es_health_ok}")
    print(f"es_index_ok={es_index_ok} (status={es_index_status})")
    print(f"worker_ok={worker_ok} (rc={worker_exit_code}, runtime_s={worker_runtime_s:.2f})")
    print(f"es_refresh_ok={es_refresh_ok} (status={es_refresh_status})")
    print(f"es_search_ok={es_search_ok} (status={es_search_status})")
    print(f"es_candidates_total={es_candidates_total}")
    print(f"parity_ok={parity_ok} (strategy={strategy})")
    print(f"ok={ok}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def cmd_labs_shadow_verify_canary_dual_write(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-canary-dual-write"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    max_writes = int(args.max_writes)
    if max_writes <= 0:
        print(f"[{log_prefix}] --max-writes must be > 0")
        return 2

    cleanup = bool(args.cleanup)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
            "max_writes": max_writes,
            "cleanup": cleanup,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    verify_obj = result.get("verify")
    rollback_obj = result.get("rollback")
    verify_search_count = 0
    verify_outbox_count = 0
    dup_extra = 0
    if isinstance(verify_obj, dict):
        verify_search_count = int(verify_obj.get("search_index_rows_found") or 0)
        verify_outbox_count = int(verify_obj.get("search_outbox_rows_found") or 0)
        dup_extra = int(verify_obj.get("duplicates_extra_rows_total") or 0)

    cleanup_enabled = bool(cleanup)
    cleanup_deleted_search = 0
    cleanup_deleted_outbox = 0
    cleanup_remaining_search = None
    cleanup_remaining_outbox = None
    if isinstance(rollback_obj, dict):
        cleanup_enabled = bool(rollback_obj.get("cleanup_enabled"))
        cleanup_deleted_search = int(rollback_obj.get("deleted_search_index") or 0)
        cleanup_deleted_outbox = int(rollback_obj.get("deleted_search_outbox_events") or 0)
        cleanup_remaining_search = rollback_obj.get("remaining_search_index")
        cleanup_remaining_outbox = rollback_obj.get("remaining_search_outbox_events")

    print("labs-016.shadow_verify_canary_dual_write")
    print(f"scope={scope}")
    print(f"max_writes={max_writes}")
    print(f"verify_search_index_rows_found={verify_search_count}")
    print(f"verify_search_outbox_rows_found={verify_outbox_count}")
    print(f"duplicates_extra_rows_total={dup_extra}")
    print(f"cleanup_enabled={cleanup_enabled}")
    print(f"cleanup_deleted_search_index={cleanup_deleted_search}")
    print(f"cleanup_deleted_search_outbox_events={cleanup_deleted_outbox}")
    if cleanup_enabled:
        print(f"cleanup_remaining_search_index={cleanup_remaining_search}")
        print(f"cleanup_remaining_search_outbox_events={cleanup_remaining_outbox}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2


def _parse_csv_list(value: str | None) -> list[str]:
    if not value:
        return []
    parts = [p.strip() for p in str(value).split(",")]
    return [p for p in parts if p]


def cmd_labs_shadow_verify_dual_write_sampling(
    args: argparse.Namespace,
    *,
    lab_id: str,
    scenario: str,
    now_run_id: Callable[[], str],
    default_outdir: Callable[..., Path],
    ensure_dir: Callable[[Path], None],
    load_env: Callable[..., dict[str, str]],
) -> int:
    log_prefix = "labs shadow-verify-dual-write-sampling"

    run_id = args.run_id or now_run_id()
    outdir = Path(args.outdir) if args.outdir else default_outdir(lab_id=lab_id, scenario=scenario, run_id=run_id)
    ensure_dir(outdir)

    env = load_env(env_file=args.env_file)
    database_url = _require_database_url(env=env, provided=args.database_url, log_prefix=log_prefix)
    if not database_url:
        return 2

    try:
        library_id = _parse_optional_uuid(
            value=getattr(args, "library_id", None), arg_name="--library-id", log_prefix=log_prefix
        )
    except SystemExit as exc:
        return int(getattr(exc, "code", 2) or 2)

    entity_types = _parse_csv_list(args.entity_types)
    ensure_min_rows = int(args.ensure_min_rows)
    if ensure_min_rows < 0:
        print(f"[{log_prefix}] --ensure-min-rows must be >= 0")
        return 2

    sample_size = int(args.sample_size)
    if sample_size <= 0:
        print(f"[{log_prefix}] --sample-size must be > 0")
        return 2

    duration_seconds = int(args.duration_seconds)
    if duration_seconds < 0:
        print(f"[{log_prefix}] --duration-seconds must be >= 0")
        return 2

    interval_seconds = float(args.interval_seconds)
    if interval_seconds <= 0:
        print(f"[{log_prefix}] --interval-seconds must be > 0")
        return 2

    max_total_events = int(args.max_total_events)
    if max_total_events <= 0:
        print(f"[{log_prefix}] --max-total-events must be > 0")
        return 2

    strategy = str(args.strategy).strip().lower()
    if strategy not in {"soft", "strict"}:
        print(f"[{log_prefix}] --strategy must be one of: soft, strict")
        return 2

    inject_failed_rate = float(args.inject_failed_rate)
    if inject_failed_rate < 0.0 or inject_failed_rate > 1.0:
        print(f"[{log_prefix}] --inject-failed-rate must be in [0.0, 1.0]")
        return 2

    replay_failed = bool(args.replay_failed)
    replay_by = str(args.replay_by or "labs")[:120]
    replay_reason = str(args.replay_reason or "labs shadow dual-write sampling replay")
    cleanup = bool(args.cleanup)

    input_payload = dict(vars(args))
    input_payload.pop("func", None)
    input_payload.update(
        {
            "scenario": scenario,
            "scope_id": lab_id,
            "run_id": run_id,
            "outdir": str(outdir),
            "database_url": database_url,
            "library_id": library_id,
            "entity_types": entity_types,
            "ensure_min_rows": ensure_min_rows,
            "sample_size": sample_size,
            "duration_seconds": duration_seconds,
            "interval_seconds": interval_seconds,
            "max_total_events": max_total_events,
            "strategy": strategy,
            "inject_failed_rate": inject_failed_rate,
            "replay_failed": replay_failed,
            "replay_by": replay_by,
            "replay_reason": replay_reason,
            "cleanup": cleanup,
        }
    )

    result = _invoke_and_pack(scenario=scenario, payload=input_payload, outdir=outdir)

    ok = bool(result.get("ok"))
    scope = str(result.get("scope") or "")
    observed = result.get("observed")
    rollback = result.get("rollback")
    outbox_inserted_total = 0
    pending_after = 0
    failed_after = 0
    dlq_failed_simulated_total = 0
    replayed_total = 0
    if isinstance(observed, dict):
        outbox_inserted_total = int(observed.get("outbox_inserted_total") or 0)
        pending_after = int(observed.get("pending_after") or 0)
        failed_after = int(observed.get("failed_after") or 0)
        dlq_failed_simulated_total = int(observed.get("dlq_failed_simulated_total") or 0)
        replayed_total = int(observed.get("replayed_total") or 0)

    cleanup_enabled = bool(cleanup)
    remaining_outbox_rows = None
    if isinstance(rollback, dict):
        cleanup_enabled = bool(rollback.get("cleanup_enabled"))
        remaining_outbox_rows = rollback.get("remaining_outbox_rows")

    print("labs-017.shadow_verify_dual_write_sampling")
    print(f"scope={scope}")
    print(f"strategy={strategy}")
    print(f"outbox_inserted_total={outbox_inserted_total}")
    print(f"pending_after={pending_after}")
    print(f"failed_after={failed_after}")
    print(f"dlq_failed_simulated_total={dlq_failed_simulated_total}")
    print(f"replayed_total={replayed_total}")
    print(f"cleanup_enabled={cleanup_enabled}")
    if cleanup_enabled:
        print(f"remaining_outbox_rows={remaining_outbox_rows}")
    print(f"outputs: {outdir}")

    return 0 if ok else 2
