from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    # backend/scripts/ci/list_scenarios.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def _load_yaml(path: Path) -> Any:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"file not found: {path}") from exc

    try:
        import yaml  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        print(
            "[error] missing dependency: PyYAML\n"
            "Install with: python -m pip install PyYAML",
            file=sys.stderr,
        )
        raise SystemExit(2)

    try:
        return yaml.safe_load(raw)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"failed to parse yaml: {path}: {exc}") from exc


def _cli_summary(cli: Any, *, max_len: int = 96) -> str:
    if not isinstance(cli, str):
        return ""
    text = cli.strip()
    if not text:
        return ""

    first_line = text.splitlines()[0].strip()
    first_line = re.sub(r"\s+", " ", first_line)

    # Reduce terminal width pressure for the common case.
    first_line = first_line.replace("python backend/scripts/cli.py ", "cli.py ")
    first_line = first_line.replace("python backend/scripts/cli.py", "cli.py")

    if len(first_line) > max_len:
        return first_line[: max_len - 1] + "…"
    return first_line


def _as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for x in value:
        if isinstance(x, str) and x.strip():
            out.append(x.strip())
    return out


def _matches_intent(scenario_id: str, tags: list[str], intent: str) -> bool:
    if scenario_id.split("/", 1)[0] == intent:
        return True
    return f"intent:{intent}" in tags


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="list-scenarios",
        description="List scenario ids (and aliases) from docs/labs/scenarios/catalog.yml",
    )
    parser.add_argument(
        "--intent",
        type=str,
        default="",
        help="Filter by intent (e.g. verify, readiness, dual_run, dual_write, fault)",
    )
    parser.add_argument(
        "--grep",
        type=str,
        default="",
        help="Case-insensitive substring match on id/aliases/tags/cli summary",
    )
    parser.add_argument(
        "--catalog",
        type=str,
        default="",
        help="Override catalog path (default: docs/labs/scenarios/catalog.yml)",
    )

    args = parser.parse_args()

    root = _repo_root()
    catalog_path = Path(args.catalog) if args.catalog else (root / "docs" / "labs" / "scenarios" / "catalog.yml")

    doc = _load_yaml(catalog_path)
    if not isinstance(doc, dict):
        print("[error] catalog root must be a mapping", file=sys.stderr)
        return 1

    scenarios = doc.get("scenarios")
    if not isinstance(scenarios, list):
        print("[error] catalog must contain a 'scenarios' list", file=sys.stderr)
        return 1

    intent = (args.intent or "").strip()
    grep = (args.grep or "").strip().lower()

    rows: list[tuple[str, list[str], list[str], str]] = []

    for item in scenarios:
        if not isinstance(item, dict):
            continue
        scenario_id = item.get("id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            continue

        scenario_id = scenario_id.strip()
        aliases = _as_str_list(item.get("aliases"))
        tags = _as_str_list(item.get("tags"))
        summary = _cli_summary(item.get("cli"))

        if intent and not _matches_intent(scenario_id, tags, intent):
            continue

        haystack = " ".join([scenario_id, " ".join(aliases), " ".join(tags), summary]).lower()
        if grep and grep not in haystack:
            continue

        rows.append((scenario_id, aliases, tags, summary))

    rows.sort(key=lambda r: r[0])

    print(f"[ok] {len(rows)} scenario(s) from {catalog_path.as_posix()}")
    for scenario_id, aliases, tags, summary in rows:
        aliases_str = ", ".join(aliases) if aliases else "-"
        summary_str = summary if summary else "-"
        print(f"{scenario_id} | aliases: {aliases_str} | cli: {summary_str}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
