from __future__ import annotations

import argparse
from collections.abc import Callable
from functools import partial

from cli_app.labs.collector_down import cmd_labs_clean_collector_down as _cmd_labs_clean_collector_down_impl
from cli_app.labs.collector_down import cmd_labs_export_collector_down as _cmd_labs_export_collector_down_impl
from cli_app.labs.collector_down import cmd_labs_run_collector_down as _cmd_labs_run_collector_down_impl
from cli_app.labs.collector_down import cmd_labs_verify_collector_down as _cmd_labs_verify_collector_down_impl
from cli_app.labs.expb_es429 import cmd_labs_expb_es429 as _cmd_labs_expb_es429_impl
from cli_app.labs.failure_drills import cmd_labs_clean as _cmd_labs_clean_impl
from cli_app.labs.failure_drills import cmd_labs_export as _cmd_labs_export_impl
from cli_app.labs.failure_drills import cmd_labs_run as _cmd_labs_run_impl
from cli_app.labs.failure_drills import cmd_labs_verify as _cmd_labs_verify_impl
from cli_app.labs.jaeger_export import cmd_labs_export_jaeger as _cmd_labs_export_jaeger_impl
from cli_app.labs.chronicle_rehearsal import (
    cmd_labs_chronicle_entries_envelope_backfill_rehearsal as _cmd_labs_chronicle_entries_envelope_backfill_rehearsal_impl,
)
from cli_app.labs.chronicle_rehearsal import (
    cmd_labs_chronicle_read_switch_smoke_rehearsal as _cmd_labs_chronicle_read_switch_smoke_rehearsal_impl,
)
from cli_app.labs.search_rehearsal import (
    cmd_labs_search_read_switch_smoke_rehearsal as _cmd_labs_search_read_switch_smoke_rehearsal_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_canary_dual_write as _cmd_labs_shadow_verify_canary_dual_write_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_chronicle_entries as _cmd_labs_shadow_verify_chronicle_entries_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_run_readiness_gate as _cmd_labs_shadow_verify_dual_run_readiness_gate_impl,
)
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_dual_run_stage1 as _cmd_labs_shadow_verify_dual_run_stage1_impl
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_dual_run_stage2 as _cmd_labs_shadow_verify_dual_run_stage2_impl
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_dual_run_window as _cmd_labs_shadow_verify_dual_run_window_impl
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_dual_write_sampling as _cmd_labs_shadow_verify_dual_write_sampling_impl,
)
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_search_index as _cmd_labs_shadow_verify_search_index_impl
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_search_index_paging_stability as _cmd_labs_shadow_verify_search_index_paging_stability_impl,
)
from cli_app.labs.shadow_verify import (
    cmd_labs_shadow_verify_search_index_write_gate as _cmd_labs_shadow_verify_search_index_write_gate_impl,
)
from cli_app.labs.shadow_verify import cmd_labs_shadow_verify_shared_keys as _cmd_labs_shadow_verify_shared_keys_impl


Callback = Callable[[argparse.Namespace], int]


LAB_ID_S3A_2A_3A = "S3A-2A-3A"
LAB_ID_S2B_1A_1A = "S2B-1A-1A"
LAB_ID_S2B_1A_2A = "S2B-1A-2A"
LAB_ID_S2B_2A_1A = "S2B-2A-1A"
LAB_ID_S2B_2A_2A = "S2B-2A-2A"
LAB_ID_S2B_4A_P2_C2 = "S2B-4A-P2-C2"
LAB_ID_S2B_4A_P3_C1 = "S2B-4A-P3-C1"
LAB_ID_S2B_4A_P3_C2 = "S2B-4A-P3-C2"

SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES = "shadow_verify_chronicle_entries"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX = "shadow_verify_search_index"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE = "shadow_verify_search_index_write_gate"
SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY = "shadow_verify_search_index_paging_stability"
SCENARIO_SHADOW_VERIFY_SHARED_KEYS = "shadow_verify_shared_keys"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE = "shadow_verify_dual_run_readiness_gate"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1 = "shadow_verify_dual_run_stage1"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2 = "shadow_verify_dual_run_stage2"
SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW = "shadow_verify_dual_run_window"
SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE = "shadow_verify_canary_dual_write"
SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING = "shadow_verify_dual_write_sampling"

SCENARIO_REHEARSAL_CHRONICLE_ENTRIES_ENVELOPE_BACKFILL = "rehearsal_chronicle_entries_envelope_backfill"
SCENARIO_REHEARSAL_CHRONICLE_READ_SWITCH_SMOKE = "rehearsal_chronicle_read_switch_smoke"
SCENARIO_REHEARSAL_SEARCH_READ_SWITCH_SMOKE = "rehearsal_search_read_switch_smoke"

SCENARIO_ES_WRITE_BLOCK_4XX = "es_write_block_4xx"
SCENARIO_ES_429_INJECT = "es_429_inject"
SCENARIO_ES_DOWN_CONNECT = "es_down_connect"
SCENARIO_ES_BULK_PARTIAL = "es_bulk_partial"
SCENARIO_DB_CLAIM_CONTENTION = "db_claim_contention"
SCENARIO_STUCK_RECLAIM = "stuck_reclaim"
SCENARIO_DUPLICATE_DELIVERY = "duplicate_delivery"
SCENARIO_PROJECTION_VERSION = "projection_version"
SCENARIO_COLLECTOR_DOWN = "collector_down"


def build_callbacks() -> dict[str, Callback]:
    """Build the callback dict consumed by cli_app.parser.build_parser().

    Key contract: the keys MUST stay stable because argparse stores them as
    strings (e.g. `_cmd_labs_run_es_429_inject`).

    This module centralizes the legacy-wrapper glue so `backend/scripts/cli.py`
    can stay dispatch-only.
    """

    shadow_verify_callbacks: dict[str, Callback] = {
        "_cmd_labs_shadow_verify_chronicle_entries": partial(
            _cmd_labs_shadow_verify_chronicle_entries_impl,
            lab_id=LAB_ID_S2B_1A_1A,
            scenario=SCENARIO_SHADOW_VERIFY_CHRONICLE_ENTRIES,
        ),
        "_cmd_labs_chronicle_entries_envelope_backfill_rehearsal": partial(
            _cmd_labs_chronicle_entries_envelope_backfill_rehearsal_impl,
            lab_id=LAB_ID_S2B_4A_P2_C2,
            scenario=SCENARIO_REHEARSAL_CHRONICLE_ENTRIES_ENVELOPE_BACKFILL,
        ),
        "_cmd_labs_chronicle_read_switch_smoke_rehearsal": partial(
            _cmd_labs_chronicle_read_switch_smoke_rehearsal_impl,
            lab_id=LAB_ID_S2B_4A_P3_C1,
            scenario=SCENARIO_REHEARSAL_CHRONICLE_READ_SWITCH_SMOKE,
        ),
        "_cmd_labs_search_read_switch_smoke_rehearsal": partial(
            _cmd_labs_search_read_switch_smoke_rehearsal_impl,
            lab_id=LAB_ID_S2B_4A_P3_C2,
            scenario=SCENARIO_REHEARSAL_SEARCH_READ_SWITCH_SMOKE,
        ),
        "_cmd_labs_shadow_verify_search_index": partial(
            _cmd_labs_shadow_verify_search_index_impl,
            lab_id=LAB_ID_S2B_1A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX,
        ),
        "_cmd_labs_shadow_verify_search_index_write_gate": partial(
            _cmd_labs_shadow_verify_search_index_write_gate_impl,
            lab_id=LAB_ID_S2B_2A_1A,
            scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_WRITE_GATE,
        ),
        "_cmd_labs_shadow_verify_search_index_paging_stability": partial(
            _cmd_labs_shadow_verify_search_index_paging_stability_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_SEARCH_INDEX_PAGING_STABILITY,
        ),
        "_cmd_labs_shadow_verify_shared_keys": partial(
            _cmd_labs_shadow_verify_shared_keys_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_SHARED_KEYS,
        ),
        "_cmd_labs_shadow_verify_dual_run_readiness_gate": partial(
            _cmd_labs_shadow_verify_dual_run_readiness_gate_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_READINESS_GATE,
        ),
        "_cmd_labs_shadow_verify_dual_run_stage1": partial(
            _cmd_labs_shadow_verify_dual_run_stage1_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE1,
        ),
        "_cmd_labs_shadow_verify_dual_run_stage2": partial(
            _cmd_labs_shadow_verify_dual_run_stage2_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_STAGE2,
        ),
        "_cmd_labs_shadow_verify_dual_run_window": partial(
            _cmd_labs_shadow_verify_dual_run_window_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_DUAL_RUN_WINDOW,
        ),
        "_cmd_labs_shadow_verify_canary_dual_write": partial(
            _cmd_labs_shadow_verify_canary_dual_write_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_CANARY_DUAL_WRITE,
        ),
        "_cmd_labs_shadow_verify_dual_write_sampling": partial(
            _cmd_labs_shadow_verify_dual_write_sampling_impl,
            lab_id=LAB_ID_S2B_2A_2A,
            scenario=SCENARIO_SHADOW_VERIFY_DUAL_WRITE_SAMPLING,
        ),
    }

    failure_drill_common: dict[str, Callback] = {
        "_cmd_labs_expb_es429": _cmd_labs_expb_es429_impl,
        "_cmd_labs_export_jaeger": _cmd_labs_export_jaeger_impl,
        "_cmd_labs_run_es_write_block_4xx": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
            handler_base="es_write_block_4xx",
        ),
        "_cmd_labs_verify_es_write_block_4xx": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
            handler_base="es_write_block_4xx",
        ),
        "_cmd_labs_export_es_write_block_4xx": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_WRITE_BLOCK_4XX,
            handler_base="es_write_block_4xx",
        ),
        "_cmd_labs_clean_es_write_block_4xx": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="es_write_block_4xx",
        ),
        "_cmd_labs_run_es_429_inject": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_429_INJECT,
            handler_base="es_429_inject",
        ),
        "_cmd_labs_verify_es_429_inject": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_429_INJECT,
            handler_base="es_429_inject",
        ),
        "_cmd_labs_export_es_429_inject": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_429_INJECT,
            handler_base="es_429_inject",
        ),
        "_cmd_labs_clean_es_429_inject": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="es_429_inject",
        ),
        "_cmd_labs_run_es_down_connect": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_DOWN_CONNECT,
            handler_base="es_down_connect",
        ),
        "_cmd_labs_verify_es_down_connect": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_DOWN_CONNECT,
            handler_base="es_down_connect",
        ),
        "_cmd_labs_export_es_down_connect": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_DOWN_CONNECT,
            handler_base="es_down_connect",
        ),
        "_cmd_labs_clean_es_down_connect": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="es_down_connect",
        ),
        "_cmd_labs_run_es_bulk_partial": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_BULK_PARTIAL,
            handler_base="es_bulk_partial",
        ),
        "_cmd_labs_verify_es_bulk_partial": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_BULK_PARTIAL,
            handler_base="es_bulk_partial",
        ),
        "_cmd_labs_export_es_bulk_partial": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_ES_BULK_PARTIAL,
            handler_base="es_bulk_partial",
        ),
        "_cmd_labs_clean_es_bulk_partial": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="es_bulk_partial",
        ),
        "_cmd_labs_run_db_claim_contention": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_DB_CLAIM_CONTENTION,
            handler_base="db_claim_contention",
        ),
        "_cmd_labs_verify_db_claim_contention": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_DB_CLAIM_CONTENTION,
            handler_base="db_claim_contention",
        ),
        "_cmd_labs_export_db_claim_contention": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_DB_CLAIM_CONTENTION,
            handler_base="db_claim_contention",
        ),
        "_cmd_labs_clean_db_claim_contention": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="db_claim_contention",
        ),
        "_cmd_labs_run_stuck_reclaim": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_STUCK_RECLAIM,
            handler_base="stuck_reclaim",
        ),
        "_cmd_labs_verify_stuck_reclaim": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_STUCK_RECLAIM,
            handler_base="stuck_reclaim",
        ),
        "_cmd_labs_export_stuck_reclaim": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_STUCK_RECLAIM,
            handler_base="stuck_reclaim",
        ),
        "_cmd_labs_clean_stuck_reclaim": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="stuck_reclaim",
        ),
        "_cmd_labs_run_duplicate_delivery": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_DUPLICATE_DELIVERY,
            handler_base="duplicate_delivery",
        ),
        "_cmd_labs_verify_duplicate_delivery": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_DUPLICATE_DELIVERY,
            handler_base="duplicate_delivery",
        ),
        "_cmd_labs_export_duplicate_delivery": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_DUPLICATE_DELIVERY,
            handler_base="duplicate_delivery",
        ),
        "_cmd_labs_clean_duplicate_delivery": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="duplicate_delivery",
        ),
        "_cmd_labs_run_projection_version": partial(
            _cmd_labs_run_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_PROJECTION_VERSION,
            handler_base="projection_version",
        ),
        "_cmd_labs_verify_projection_version": partial(
            _cmd_labs_verify_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_PROJECTION_VERSION,
            handler_base="projection_version",
            fallback_exit_code=lambda ok: 0 if ok else 2,
        ),
        "_cmd_labs_export_projection_version": partial(
            _cmd_labs_export_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_PROJECTION_VERSION,
            handler_base="projection_version",
            fallback_exit_code=lambda ok: 0 if ok else 2,
        ),
        "_cmd_labs_clean_projection_version": partial(
            _cmd_labs_clean_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="projection_version",
        ),
    }

    collector_down_callbacks: dict[str, Callback] = {
        "_cmd_labs_run_collector_down": partial(
            _cmd_labs_run_collector_down_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_COLLECTOR_DOWN,
            handler_base="collector_down",
        ),
        "_cmd_labs_verify_collector_down": partial(
            _cmd_labs_verify_collector_down_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_COLLECTOR_DOWN,
            handler_base="collector_down",
        ),
        "_cmd_labs_export_collector_down": partial(
            _cmd_labs_export_collector_down_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            scenario=SCENARIO_COLLECTOR_DOWN,
            handler_base="collector_down",
        ),
        "_cmd_labs_clean_collector_down": partial(
            _cmd_labs_clean_collector_down_impl,
            scope_id=LAB_ID_S3A_2A_3A,
            handler_base="collector_down",
        ),
    }

    callbacks: dict[str, Callback] = {}
    callbacks.update(shadow_verify_callbacks)
    callbacks.update(failure_drill_common)
    callbacks.update(collector_down_callbacks)
    return callbacks
