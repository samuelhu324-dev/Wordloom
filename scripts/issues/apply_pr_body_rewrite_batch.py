from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _derive_repo_slug, _load_text, _parse_fields, _parse_sections, _repo_rel, _repo_root, _require_gh_auth, _require_gh_cli, _run_command
from plan_pr_prep import _build_pr_labels
from raw_live_mutation_guard import add_raw_live_mutation_guard_arg, require_raw_live_mutation_guard
from rewrite_pr_body_scope_from_log import rewrite_pr_body_scope


@dataclass
class PrBodyRewriteBatchItemResult:
    requested_id: str
    source_log_path: str
    pr_number: int
    pr_url: str
    pr_title: str
    pr_state: str
    live_body_path: str
    rewritten_body_path: str
    apply_result_path: str
    body_changed: bool
    labels_applied: list[str]
    warnings: list[str]


@dataclass
class PrBodyRewriteBatchResult:
    mode: str
    result: str
    manifest_path: str
    repository: str
    total_items: int
    applied_items: int
    warnings: list[str]
    items: list[PrBodyRewriteBatchItemResult]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a manifest-driven historical PR body rewrite batch")
    parser.add_argument("manifest_path", help="Path to a PR body rewrite manifest JSON file")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--result-path", dest="result_path", help="Override output batch result JSON path")
    add_raw_live_mutation_guard_arg(parser)
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR body rewrite manifest JSON: {exc}") from exc


def _fetch_pr(repo: str, pr_ref: str) -> dict:
    cmd = _run_command([
        "gh",
        "pr",
        "view",
        pr_ref,
        "--repo",
        repo,
        "--json",
        "number,url,title,body,state,labels",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"Failed to view PR {pr_ref} in {repo}: {cmd.stderr.strip()}")
    try:
        return json.loads(cmd.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR view JSON: {exc}") from exc


def _edit_pr(repo: str, pr_ref: str, body_path: Path, add_labels: list[str]) -> None:
    body_text = body_path.read_text(encoding="utf-8")
    cmd = _run_command([
        "gh",
        "api",
        f"repos/{repo}/pulls/{pr_ref}",
        "--method",
        "PATCH",
        "-f",
        f"body={body_text}",
    ])
    if cmd.returncode != 0:
        raise SystemExit(f"gh api pull update failed: {cmd.stderr.strip()}")

    for label in add_labels:
        label_cmd = _run_command([
            "gh",
            "pr",
            "edit",
            pr_ref,
            "--repo",
            repo,
            "--add-label",
            label,
        ])
        if label_cmd.returncode != 0:
            raise SystemExit(f"gh pr edit --add-label failed: {label_cmd.stderr.strip()}")


def _derive_repo(manifest: dict, override: str | None) -> str:
    if override:
        return _derive_repo_slug(override)
    defaults = manifest.get("defaults") if isinstance(manifest.get("defaults"), dict) else {}
    manifest_repo = str(defaults.get("repo") or "").strip()
    return _derive_repo_slug(manifest_repo or None)


def apply_pr_body_rewrite_batch(args: argparse.Namespace) -> PrBodyRewriteBatchResult:
    require_raw_live_mutation_guard(
        args,
        canonical_surface="scripts/issues/apply_pr_body_scope_with_pre_gate.py for single-PR live rewrite; this batch script remains bounded internal historical reuse only",
    )
    repo_root = _repo_root()
    manifest_path = _coerce_path(args.manifest_path, repo_root)
    if not manifest_path.is_file():
        raise SystemExit(f"PR body rewrite manifest file not found: {manifest_path}")

    manifest = _load_manifest(manifest_path)
    if manifest.get("mode") != "pr-body-rewrite-apply":
        raise SystemExit("PR body rewrite batch requires mode=pr-body-rewrite-apply")

    items = manifest.get("items") or []
    if not isinstance(items, list) or not items:
        raise SystemExit("PR body rewrite manifest must contain at least one item")

    repo = _derive_repo(manifest, args.repo)
    _require_gh_cli()
    _require_gh_auth()

    results: list[PrBodyRewriteBatchItemResult] = []
    batch_warnings: list[str] = []

    for item in items:
        if not isinstance(item, dict):
            raise SystemExit("Each PR body rewrite manifest item must be an object")

        requested_id = str(item.get("requested_id") or "").strip()
        source_log_rel = str(item.get("source_log_path") or "").strip()
        pr_number = int(item.get("pr_number") or 0)
        if not requested_id or not source_log_rel or not pr_number:
            raise SystemExit("PR body rewrite manifest item is missing requested_id, source_log_path, or pr_number")

        source_log_path = _coerce_path(source_log_rel, repo_root)
        if not source_log_path.is_file():
            raise SystemExit(f"Source log not found: {source_log_path}")
        source_log_text = _load_text(source_log_path)
        expected_labels = _build_pr_labels(_parse_fields(source_log_text), _parse_sections(source_log_text))

        slug = f"{manifest_path.stem}-{requested_id.lower()}-pr-{pr_number}"
        live_body_path = manifest_path.with_name(f"{slug}-live-body.md")
        rewritten_body_path = manifest_path.with_name(f"{slug}-rewritten-body.md")
        apply_result_path = manifest_path.with_name(f"{slug}-apply-result.json")
        live_body_path.parent.mkdir(parents=True, exist_ok=True)

        before = _fetch_pr(repo, str(pr_number))
        live_body_text = str(before.get("body") or "")
        live_labels = [label.get("name", "") for label in before.get("labels", []) if isinstance(label, dict) and label.get("name")]
        missing_labels = [label for label in expected_labels if label not in live_labels]
        live_body_path.write_text(live_body_text, encoding="utf-8")

        rewrite_pr_body_scope(
            source_log_path=source_log_path,
            existing_body_path=live_body_path,
            requested_id=requested_id,
            pr_title=str(before.get("title") or ""),
            output_path=rewritten_body_path,
        )

        rewritten_body_text = rewritten_body_path.read_text(encoding="utf-8")
        _edit_pr(repo, str(pr_number), rewritten_body_path, missing_labels)
        after = _fetch_pr(repo, str(pr_number))

        warnings: list[str] = []
        body_changed = live_body_text != rewritten_body_text
        if not body_changed:
            warnings.append("rewritten PR body matched the fetched live body; live edit path was still exercised")
        if str(after.get("state") or "") != "MERGED":
            warnings.append(f"historical rewrite target is in state {after.get('state')}; expected MERGED")
        if missing_labels:
            warnings.append("missing live PR labels were backfilled from the deterministic source-log label set")

        item_result = PrBodyRewriteBatchItemResult(
            requested_id=requested_id,
            source_log_path=source_log_rel,
            pr_number=int(after["number"]),
            pr_url=str(after.get("url") or ""),
            pr_title=str(after.get("title") or ""),
            pr_state=str(after.get("state") or ""),
            live_body_path=_repo_rel(live_body_path),
            rewritten_body_path=_repo_rel(rewritten_body_path),
            apply_result_path=_repo_rel(apply_result_path),
            body_changed=body_changed,
            labels_applied=missing_labels,
            warnings=warnings,
        )
        apply_result_path.write_text(json.dumps(asdict(item_result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        results.append(item_result)
        batch_warnings.extend(warnings)

    batch_result = PrBodyRewriteBatchResult(
        mode="pr-body-rewrite-apply-batch",
        result="ok",
        manifest_path=_repo_rel(manifest_path),
        repository=repo,
        total_items=len(results),
        applied_items=len(results),
        warnings=batch_warnings,
        items=results,
    )

    if args.result_path:
        result_path = _coerce_path(args.result_path, repo_root)
    else:
        result_path = manifest_path.with_name(f"{manifest_path.stem}-result.json")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(asdict(batch_result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(batch_result), indent=2, ensure_ascii=True))
    return batch_result


def main() -> int:
    args = _parse_args()
    try:
        apply_pr_body_rewrite_batch(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())