from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _repo_rel, _repo_root
from review_pr_body_completeness import run_pr_body_completeness_review


@dataclass
class PrBodyCompletenessCheckArtifacts:
    wrapper_summary_path: str
    artifact_manifest_path: str
    review_result_path: str
    review_artifact_dir: str


@dataclass
class PrBodyCompletenessCheckResult:
    mode: str
    result: str
    read_only: bool
    primary_local_boundary: bool
    trigger_surface: str
    repository: str
    requested_id_prefixes: list[str]
    fail_on_findings: bool
    total_logs_reviewed: int
    exact_match_ids: list[str]
    formatting_only_ids: list[str]
    substantive_drift_ids: list[str]
    stop_ids: list[str]
    skip_ids: list[str]
    decision_reason: str
    stop_reason: str
    wrapper_result_path: str
    wrapper_summary_path: str
    artifact_manifest_path: str
    review_result_path: str
    review_artifact_dir: str
    warnings: list[str]
    retained_artifacts: PrBodyCompletenessCheckArtifacts


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the PR body completeness reviewer through a standard read-only check wrapper")
    parser.add_argument(
        "--requested-id-prefix",
        dest="requested_id_prefixes",
        action="append",
        required=True,
        help="Review logs whose requested ID starts with this prefix, for example S0F-",
    )
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--logs-dir", dest="logs_dir", help="Override logs directory; defaults to docs/logs under the repo root")
    parser.add_argument("--review-result-path", dest="review_result_path", required=True, help="Explicit review result JSON output path")
    parser.add_argument("--review-artifact-dir", dest="review_artifact_dir", required=True, help="Explicit review artifact directory")
    parser.add_argument("--wrapper-result-path", dest="wrapper_result_path", required=True, help="Explicit wrapper result JSON output path")
    parser.add_argument("--wrapper-summary-path", dest="wrapper_summary_path", required=True, help="Explicit wrapper summary markdown output path")
    parser.add_argument("--artifact-manifest-path", dest="artifact_manifest_path", required=True, help="Explicit wrapper artifact manifest JSON output path")
    parser.add_argument("--trigger-surface", dest="trigger_surface", default="local-cli", help="Record the operator or CI trigger surface for this standard check run")
    parser.add_argument("--wrapper-notes", dest="wrapper_notes", action="append", default=[], help="Optional wrapper notes retained in the artifact manifest")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _render_summary(result: PrBodyCompletenessCheckResult) -> str:
    lines = [
        "## PR Body Completeness Standard Check",
        "",
        "- Mode: `standard read-only check`",
        "- Role: `primary local boundary`",
        f"- Trigger surface: `{result.trigger_surface}`",
        f"- Requested ID prefixes: `{', '.join(result.requested_id_prefixes)}`",
        f"- Result: `{result.result}`",
        f"- Total logs reviewed: `{result.total_logs_reviewed}`",
        f"- Exact-match IDs: `{', '.join(result.exact_match_ids)}`" if result.exact_match_ids else "- Exact-match IDs: ``",
        f"- Formatting-only IDs: `{', '.join(result.formatting_only_ids)}`" if result.formatting_only_ids else "- Formatting-only IDs: ``",
        f"- Substantive drift IDs: `{', '.join(result.substantive_drift_ids)}`" if result.substantive_drift_ids else "- Substantive drift IDs: ``",
        f"- Stop IDs: `{', '.join(result.stop_ids)}`" if result.stop_ids else "- Stop IDs: ``",
        f"- Skip IDs: `{', '.join(result.skip_ids)}`" if result.skip_ids else "- Skip IDs: ``",
        f"- Review result artifact: `{result.review_result_path}`",
        f"- Wrapper result artifact: `{result.wrapper_result_path}`",
    ]
    if result.stop_reason:
        lines.append(f"- Stop reason: `{result.stop_reason}`")
    if result.warnings:
        lines.append("- Warnings:")
        for warning in result.warnings:
            lines.append(f"  - `{warning}`")
    lines.extend(
        [
            "",
            "This wrapper is the standard local read-only check entrypoint for PR body completeness. It delegates all classification to the canonical reviewer and fails only when substantive drift or stop-state ownership gaps remain.",
        ]
    )
    return "\n".join(lines) + "\n"


def _build_manifest(result: PrBodyCompletenessCheckResult, *, wrapper_notes: list[str]) -> dict[str, object]:
    return {
        "mode": "pr-body-completeness-standard-check-artifact-manifest",
        "result": result.result,
        "read_only": True,
        "primary_local_boundary": True,
        "trigger_surface": result.trigger_surface,
        "requested_id_prefixes": result.requested_id_prefixes,
        "decision_reason": result.decision_reason,
        "stop_reason": result.stop_reason,
        "counts": {
            "total_logs_reviewed": result.total_logs_reviewed,
            "exact_match": len(result.exact_match_ids),
            "formatting_only": len(result.formatting_only_ids),
            "substantive_drift": len(result.substantive_drift_ids),
            "stop": len(result.stop_ids),
            "skip": len(result.skip_ids),
        },
        "reviewer": {
            "fail_on_findings": result.fail_on_findings,
            "review_result_path": result.review_result_path,
            "review_artifact_dir": result.review_artifact_dir,
        },
        "wrapper": {
            "result_path": result.wrapper_result_path,
            "summary_path": result.wrapper_summary_path,
            "notes": wrapper_notes,
        },
        "retained_artifacts": asdict(result.retained_artifacts),
        "failure_semantics": {
            "classification": "standard check pass" if result.result == "pass" else ("continuation blocked by completeness findings" if result.result == "stop" else "wrapper-input-invalid"),
            "wrapper_role": "primary local boundary",
            "publish_owner": "review_pr_body_completeness.py classification contract",
        },
    }


def run_standard_check(args: argparse.Namespace) -> PrBodyCompletenessCheckResult:
    repo_root = _repo_root()
    wrapper_result_path = _coerce_path(args.wrapper_result_path, repo_root)
    wrapper_summary_path = _coerce_path(args.wrapper_summary_path, repo_root)
    artifact_manifest_path = _coerce_path(args.artifact_manifest_path, repo_root)
    review_result_path = _coerce_path(args.review_result_path, repo_root)
    review_artifact_dir = _coerce_path(args.review_artifact_dir, repo_root)
    logs_dir = _coerce_path(args.logs_dir, repo_root) if args.logs_dir else None

    try:
        payload = run_pr_body_completeness_review(
            requested_id_prefixes=args.requested_id_prefixes,
            repo=args.repo,
            logs_dir=logs_dir,
            result_path=review_result_path,
            artifact_dir=review_artifact_dir,
        )
    except SystemExit as exc:
        message = str(exc) if not isinstance(exc.code, int) else "reviewer exited before retaining a result"
        result = PrBodyCompletenessCheckResult(
            mode="pr-body-completeness-standard-check",
            result="error",
            read_only=True,
            primary_local_boundary=True,
            trigger_surface=args.trigger_surface,
            repository="",
            requested_id_prefixes=list(args.requested_id_prefixes),
            fail_on_findings=True,
            total_logs_reviewed=0,
            exact_match_ids=[],
            formatting_only_ids=[],
            substantive_drift_ids=[],
            stop_ids=[],
            skip_ids=[],
            decision_reason=f"The standard check wrapper could not obtain a retained reviewer result: {message}.",
            stop_reason="wrapper-input-invalid",
            wrapper_result_path=_repo_rel(wrapper_result_path),
            wrapper_summary_path=_repo_rel(wrapper_summary_path),
            artifact_manifest_path=_repo_rel(artifact_manifest_path),
            review_result_path=_repo_rel(review_result_path),
            review_artifact_dir=_repo_rel(review_artifact_dir),
            warnings=[message] if message else [],
            retained_artifacts=PrBodyCompletenessCheckArtifacts(
                wrapper_summary_path=_repo_rel(wrapper_summary_path),
                artifact_manifest_path=_repo_rel(artifact_manifest_path),
                review_result_path=_repo_rel(review_result_path),
                review_artifact_dir=_repo_rel(review_artifact_dir),
            ),
        )
    else:
        summary = payload["summary"]
        substantive_ids = list(summary.get("substantive_drift_ids") or [])
        stop_ids = list(summary.get("stop_ids") or [])
        if substantive_ids or stop_ids:
            result_kind = "stop"
            stop_reason = "findings-present"
            decision_reason = "The standard PR body completeness check found substantive drift or stop-state ownership gaps, so the local check failed."
        else:
            result_kind = "pass"
            stop_reason = ""
            decision_reason = "The standard PR body completeness check passed with no substantive drift and no stop-state ownership gaps."

        result = PrBodyCompletenessCheckResult(
            mode="pr-body-completeness-standard-check",
            result=result_kind,
            read_only=True,
            primary_local_boundary=True,
            trigger_surface=args.trigger_surface,
            repository=str(payload.get("repository") or ""),
            requested_id_prefixes=list(payload.get("requested_id_prefixes") or []),
            fail_on_findings=True,
            total_logs_reviewed=int(summary.get("total_logs_reviewed") or 0),
            exact_match_ids=list(summary.get("exact_match_ids") or []),
            formatting_only_ids=list(summary.get("formatting_only_ids") or []),
            substantive_drift_ids=substantive_ids,
            stop_ids=stop_ids,
            skip_ids=list(summary.get("skip_ids") or []),
            decision_reason=decision_reason,
            stop_reason=stop_reason,
            wrapper_result_path=_repo_rel(wrapper_result_path),
            wrapper_summary_path=_repo_rel(wrapper_summary_path),
            artifact_manifest_path=_repo_rel(artifact_manifest_path),
            review_result_path=_repo_rel(review_result_path),
            review_artifact_dir=_repo_rel(review_artifact_dir),
            warnings=[],
            retained_artifacts=PrBodyCompletenessCheckArtifacts(
                wrapper_summary_path=_repo_rel(wrapper_summary_path),
                artifact_manifest_path=_repo_rel(artifact_manifest_path),
                review_result_path=_repo_rel(review_result_path),
                review_artifact_dir=_repo_rel(review_artifact_dir),
            ),
        )

    summary_text = _render_summary(result)
    manifest = _build_manifest(result, wrapper_notes=args.wrapper_notes)
    _write_text(wrapper_summary_path, summary_text)
    _write_text(artifact_manifest_path, json.dumps(manifest, indent=2, ensure_ascii=True) + "\n")
    _write_text(wrapper_result_path, json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    result = run_standard_check(args)
    if result.result == "pass":
        return 0
    if result.result == "stop":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())