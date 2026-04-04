from __future__ import annotations

import argparse


RAW_LIVE_MUTATION_ATTR = "allow_raw_live_mutation_internal"
RAW_LIVE_MUTATION_FLAG = "--allow-raw-live-mutation-internal"


def add_raw_live_mutation_guard_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        RAW_LIVE_MUTATION_FLAG,
        dest=RAW_LIVE_MUTATION_ATTR,
        action="store_true",
        help=argparse.SUPPRESS,
    )


def require_raw_live_mutation_guard(args: argparse.Namespace, *, canonical_surface: str) -> None:
    if bool(getattr(args, RAW_LIVE_MUTATION_ATTR, False)):
        return
    raise SystemExit(
        "raw live mutation entrypoint is internal-only; use the canonical guarded surface instead: "
        + canonical_surface
    )