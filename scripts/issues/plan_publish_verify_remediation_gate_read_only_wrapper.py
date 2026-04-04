from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _repo_rel, _repo_root
from plan_publish_verify_remediation_gate import plan_publish_verify_remediation_gate


@dataclass
class ReadOnlyWrapperRetainedArtifacts:
    wrapper_summary_path: str
    artifact_manifest_path: str
    thin_gate_result_path: str
    gate_decision_path: str | None
    audit_plan_path: str | None
    remediation_plan_path: str | None
    family_plan_path: str | None
    family_result_path: str | None
    delegated_result_path: str | None


@dataclass
class ReadOnlyWrapperResult:
    mode: str
    result: str
    read_only: bool
    secondary_enforcement: bool
    trigger_surface: str
    operation_family: str
    selection_input_kind: str
    selection_input_path: str
    family_input_kind: str | None
    family_input_path: str | None
    normalized_decision: str
    apply_allowed: bool
    delegated_apply_requested: bool
    delegated_apply_executed: bool
    decision_reason: str
    stop_reason: str
    stopped_before_stage: str | None
    wrapper_result_path: str
    wrapper_summary_path: str
    artifact_manifest_path: str
    thin_gate_result_path: str
    published_artifact_root: str
    verify_summary_decision: str
    warnings: list[str]
    retained_artifacts: ReadOnlyWrapperRetainedArtifacts


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the thin publish-verify-remediation gate through a read-only wrapper surface")
    parser.add_argument("operation_family", choices=["issue-conclusion", "issue-relationship", "pr-body-rewrite", "pr-create-preflight"], help="Thin gate operation family to replay through the read-only wrapper")
    parser.add_argument("selection_input_path", help="Selection input path forwarded to the thin gate")
    parser.add_argument("--selection-input-kind", dest="selection_input_kind", choices=["manifest", "audit-plan"], default="manifest", help="Interpret the selection input as a manifest or a frozen audit plan")
    parser.add_argument("--family-input-path", dest="family_input_path", help="Optional family-specific input path forwarded to the thin gate")
    parser.add_argument("--family-input-kind", dest="family_input_kind", choices=["manifest", "plan", "result"], default="manifest", help="Interpret the family-specific input as a manifest, plan, or result")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--audit-plan-path", dest="audit_plan_path", help="Explicit lifecycle audit plan output path")
    parser.add_argument("--remediation-plan-path", dest="remediation_plan_path", help="Explicit lifecycle remediation plan output path")
    parser.add_argument("--decision-path", dest="decision_path", help="Explicit lifecycle gate decision output path")
    parser.add_argument("--family-plan-path", dest="family_plan_path", help="Explicit family-specific plan output path")
    parser.add_argument("--thin-gate-result-path", dest="thin_gate_result_path", help="Explicit thin gate result output path")
    parser.add_argument("--wrapper-result-path", dest="wrapper_result_path", required=True, help="Explicit wrapper result JSON output path")
    parser.add_argument("--wrapper-summary-path", dest="wrapper_summary_path", required=True, help="Explicit wrapper summary markdown output path")
    parser.add_argument("--artifact-manifest-path", dest="artifact_manifest_path", required=True, help="Explicit wrapper artifact manifest JSON output path")
    parser.add_argument("--trigger-surface", dest="trigger_surface", default="local-cli", help="Record the operator or CI trigger surface for this wrapper run")
    parser.add_argument("--trusted-source-log-path", dest="trusted_source_log_path", help="Optional trusted source log path retained for traceability")
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


def _wrapper_result_kind(*, normalized_decision: str, thin_gate_failed: bool) -> tuple[str, str]:
    if thin_gate_failed:
        return ("error", "wrapper-input-invalid")
    if normalized_decision == "allow-apply":
        return ("pass", "")
    return ("stop", "continuation-blocked-by-thin-gate")


def _render_summary(result: ReadOnlyWrapperResult, *, trusted_source_log_path: str | None) -> str:
    lines = [
        "## Publish Verify Remediation Gate Read-Only Wrapper",
        "",
        "- Mode: `read-only wrapper`",
        "- Role: `secondary enforcement`",
        f"- Trigger surface: `{result.trigger_surface}`",
        f"- Operation family: `{result.operation_family}`",
        f"- Selection input: `{result.selection_input_path}` ({result.selection_input_kind})",
        f"- Result: `{result.result}`",
        f"- Normalized thin-gate decision: `{result.normalized_decision}`",
        f"- Apply allowed by thin gate: `{str(result.apply_allowed).lower()}`",
        f"- Delegated apply requested: `{str(result.delegated_apply_requested).lower()}`",
        f"- Delegated apply executed: `{str(result.delegated_apply_executed).lower()}`",
        f"- Verify summary decision: `{result.verify_summary_decision}`",
        f"- Thin gate result artifact: `{result.thin_gate_result_path}`",
        f"- Wrapper result artifact: `{result.wrapper_result_path}`",
    ]

    if result.stop_reason:
        lines.append(f"- Stop reason: `{result.stop_reason}`")
    if result.stopped_before_stage:
        lines.append(f"- Stopped before stage: `{result.stopped_before_stage}`")
    if trusted_source_log_path:
        lines.append(f"- Trusted source log override: `{trusted_source_log_path}`")
    if result.warnings:
        lines.append("- Warnings:")
        for warning in result.warnings:
            lines.append(f"  - `{warning}`")

    lines.extend(
        [
            "",
            "This wrapper replays thin-gate planning only. A stop or error means continuation was blocked or drift was surfaced in a read-only surface; it does not mean the wrapper prevented publish or executed live apply.",
        ]
    )
    return "\n".join(lines) + "\n"


def _build_manifest(
    *,
    result: ReadOnlyWrapperResult,
    trusted_source_log_path: str | None,
    wrapper_notes: list[str],
) -> dict[str, object]:
    return {
        "mode": "publish-verify-remediation-gate-read-only-wrapper-artifact-manifest",
        "result": result.result,
        "read_only": True,
        "secondary_enforcement": True,
        "trigger_surface": result.trigger_surface,
        "operation_family": result.operation_family,
        "selection_input": {
            "kind": result.selection_input_kind,
            "path": result.selection_input_path,
        },
        "family_input": {
            "kind": result.family_input_kind,
            "path": result.family_input_path,
        },
        "thin_gate": {
            "result_path": result.thin_gate_result_path,
            "normalized_decision": result.normalized_decision,
            "apply_allowed": result.apply_allowed,
            "decision_reason": result.decision_reason,
            "stopped_before_stage": result.stopped_before_stage,
        },
        "wrapper": {
            "result_path": result.wrapper_result_path,
            "stop_reason": result.stop_reason,
            "verify_summary_decision": result.verify_summary_decision,
            "published_artifact_root": result.published_artifact_root,
            "trusted_source_log_path": trusted_source_log_path or "",
            "notes": wrapper_notes,
        },
        "retained_artifacts": asdict(result.retained_artifacts),
        "failure_semantics": {
            "classification": (
                "wrapper-input-invalid"
                if result.result == "error"
                else ("continuation blocked in read-only wrapper" if result.result == "stop" else "read-only wrapper pass")
            ),
            "wrapper_role": "secondary enforcement",
            "publish_owner": "family-owned local or live path",
        },
    }


def run_read_only_wrapper(args: argparse.Namespace) -> ReadOnlyWrapperResult:
    repo_root = _repo_root()
    wrapper_result_path = _coerce_path(args.wrapper_result_path, repo_root)
    wrapper_summary_path = _coerce_path(args.wrapper_summary_path, repo_root)
    artifact_manifest_path = _coerce_path(args.artifact_manifest_path, repo_root)
    thin_gate_result_path = _coerce_path(args.thin_gate_result_path, repo_root) if args.thin_gate_result_path else wrapper_result_path.with_name(wrapper_result_path.stem.replace("wrapper-result", "thin-gate-result") + wrapper_result_path.suffix)

    thin_gate_failed = False
    thin_gate_result: dict[str, object] | None = None
    normalized_decision = "hard-fail-input"
    decision_reason = "The read-only wrapper could not obtain a thin-gate result."
    stop_reason = "wrapper-input-invalid"
    apply_allowed = False
    warnings: list[str] = []
    stopped_before_stage: str | None = None
    selection_input_path = _repo_rel(_coerce_path(args.selection_input_path, repo_root))
    family_input_path = _repo_rel(_coerce_path(args.family_input_path, repo_root)) if args.family_input_path else None
    downstream_artifacts: dict[str, object] = {
        "gate_decision_path": None,
        "audit_plan_path": None,
        "remediation_plan_path": None,
        "family_plan_path": None,
        "family_result_path": None,
        "delegated_result_path": None,
    }

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result_obj = plan_publish_verify_remediation_gate(
                argparse.Namespace(
                    operation_family=args.operation_family,
                    selection_input_path=args.selection_input_path,
                    selection_input_kind=args.selection_input_kind,
                    family_input_path=args.family_input_path,
                    family_input_kind=args.family_input_kind,
                    repo=args.repo,
                    audit_plan_path=args.audit_plan_path,
                    remediation_plan_path=args.remediation_plan_path,
                    decision_path=args.decision_path,
                    family_plan_path=args.family_plan_path,
                    delegate_apply=False,
                    delegated_result_path=None,
                    apply_result_path=None,
                    body_path=None,
                    context_mode="single-generate",
                    leave_open=False,
                    result_path=_repo_rel(thin_gate_result_path),
                )
            )
        thin_gate_result = asdict(result_obj)
    except SystemExit as exc:
        thin_gate_failed = True
        message = str(exc) if not isinstance(exc.code, int) else "thin gate exited before producing a result"
        decision_reason = f"The read-only wrapper stopped before retaining a thin-gate result: {message}."
        warnings = [message] if message else []

    if thin_gate_result is None and thin_gate_result_path.is_file():
        thin_gate_result = json.loads(thin_gate_result_path.read_text(encoding="utf-8"))

    if thin_gate_result is not None:
        normalized_decision = str(thin_gate_result.get("normalized_decision") or normalized_decision)
        decision_reason = str(thin_gate_result.get("decision_reason") or decision_reason)
        apply_allowed = bool(thin_gate_result.get("apply_allowed"))
        warnings = [str(item) for item in list(thin_gate_result.get("warnings") or [])]
        stopped_before_stage = str(thin_gate_result.get("stopped_before_stage") or "") or None
        downstream_artifacts = dict(thin_gate_result.get("downstream_artifacts") or downstream_artifacts)
        thin_gate_failed = False
        if not thin_gate_result_path.is_file():
            thin_gate_failed = True
            decision_reason = "The read-only wrapper invoked the thin gate, but the retained thin-gate result artifact is missing."
            warnings = ["thin gate result artifact missing after wrapper execution"]
            stop_reason = "missing-wrapper-artifact"

    result_kind, computed_stop_reason = _wrapper_result_kind(
        normalized_decision=normalized_decision,
        thin_gate_failed=thin_gate_failed,
    )
    if computed_stop_reason:
        stop_reason = computed_stop_reason
    if result_kind == "pass":
        stop_reason = ""

    retained_artifacts = ReadOnlyWrapperRetainedArtifacts(
        wrapper_summary_path=_repo_rel(wrapper_summary_path),
        artifact_manifest_path=_repo_rel(artifact_manifest_path),
        thin_gate_result_path=_repo_rel(thin_gate_result_path),
        gate_decision_path=str(downstream_artifacts.get("gate_decision_path") or "") or None,
        audit_plan_path=str(downstream_artifacts.get("audit_plan_path") or "") or None,
        remediation_plan_path=str(downstream_artifacts.get("remediation_plan_path") or "") or None,
        family_plan_path=str(downstream_artifacts.get("family_plan_path") or "") or None,
        family_result_path=str(downstream_artifacts.get("family_result_path") or "") or None,
        delegated_result_path=str(downstream_artifacts.get("delegated_result_path") or "") or None,
    )

    result = ReadOnlyWrapperResult(
        mode="publish-verify-remediation-gate-read-only-wrapper",
        result=result_kind,
        read_only=True,
        secondary_enforcement=True,
        trigger_surface=args.trigger_surface,
        operation_family=args.operation_family,
        selection_input_kind=args.selection_input_kind,
        selection_input_path=selection_input_path,
        family_input_kind=args.family_input_kind if args.family_input_path else None,
        family_input_path=family_input_path,
        normalized_decision=normalized_decision,
        apply_allowed=apply_allowed,
        delegated_apply_requested=False,
        delegated_apply_executed=False,
        decision_reason=decision_reason,
        stop_reason=stop_reason,
        stopped_before_stage=stopped_before_stage,
        wrapper_result_path=_repo_rel(wrapper_result_path),
        wrapper_summary_path=_repo_rel(wrapper_summary_path),
        artifact_manifest_path=_repo_rel(artifact_manifest_path),
        thin_gate_result_path=_repo_rel(thin_gate_result_path),
        published_artifact_root=_repo_rel(wrapper_result_path.parent),
        verify_summary_decision="not-run",
        warnings=warnings,
        retained_artifacts=retained_artifacts,
    )

    summary = _render_summary(result, trusted_source_log_path=args.trusted_source_log_path)
    manifest = _build_manifest(result=result, trusted_source_log_path=args.trusted_source_log_path, wrapper_notes=args.wrapper_notes)

    _write_text(wrapper_summary_path, summary)
    _write_text(artifact_manifest_path, json.dumps(manifest, indent=2, ensure_ascii=True) + "\n")
    _write_text(wrapper_result_path, json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    result = run_read_only_wrapper(args)
    if result.result == "pass":
        return 0
    if result.result == "stop":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())