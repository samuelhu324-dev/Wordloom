from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import _repo_rel, _repo_root
from plan_lifecycle_pre_gate import plan_lifecycle_pre_gate
from plan_pr_create_preflight_with_gate import plan_pr_create_preflight_with_gate


OPERATION_FAMILIES = {
    "issue-conclusion": "scripts/issues/apply_issue_conclusion_with_pre_gate.py",
    "issue-relationship": "scripts/issues/apply_issue_relationships_with_pre_gate.py",
    "pr-body-rewrite": "scripts/issues/apply_pr_body_scope_with_pre_gate.py",
    "pr-create-preflight": "scripts/issues/plan_pr_create_preflight_with_gate.py",
}


@dataclass
class DownstreamArtifacts:
    audit_plan_path: str | None
    gate_decision_path: str | None
    remediation_plan_path: str | None
    family_plan_path: str | None
    family_result_path: str | None


@dataclass
class PublishVerifyRemediationGateResult:
    mode: str
    result: str
    operation_family: str
    selection_input_kind: str
    selection_input_path: str
    family_input_kind: str | None
    family_input_path: str | None
    normalized_decision: str
    apply_allowed: bool
    delegated_adapter_path: str
    decision_reason: str
    stopped_before_stage: str | None
    downstream_artifacts: DownstreamArtifacts
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan a thin publish-verify-remediation gate decision")
    parser.add_argument("operation_family", choices=sorted(OPERATION_FAMILIES.keys()), help="Supported gate operation family")
    parser.add_argument("selection_input_path", help="Path to a lifecycle-audit manifest or a frozen lifecycle-audit plan")
    parser.add_argument("--selection-input-kind", dest="selection_input_kind", choices=["manifest", "audit-plan"], default="manifest", help="Interpret the selection input as a manifest or a frozen audit plan")
    parser.add_argument("--family-input-path", dest="family_input_path", help="Optional family-specific input path; currently required for pr-create-preflight")
    parser.add_argument("--family-input-kind", dest="family_input_kind", choices=["manifest", "plan"], default="manifest", help="Interpret the family-specific input as a manifest or an existing plan")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--audit-plan-path", dest="audit_plan_path", help="Override output path for the lifecycle-audit plan")
    parser.add_argument("--remediation-plan-path", dest="remediation_plan_path", help="Override output path for the lifecycle-remediation plan")
    parser.add_argument("--decision-path", dest="decision_path", help="Override output path for the lifecycle pre-gate decision")
    parser.add_argument("--family-plan-path", dest="family_plan_path", help="Override output path for the family-specific plan when supported")
    parser.add_argument("--result-path", dest="result_path", help="Override output path for the thin gate result JSON")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _stem_slug(path: Path) -> str:
    stem = path.stem
    stem = stem.removeprefix("lifecycle-audit-")
    stem = stem.removeprefix("pr-prep-")
    stem = stem.removesuffix("-manifest")
    stem = stem.removesuffix("-plan")
    return stem


def _default_result_path(args: argparse.Namespace, repo_root: Path) -> Path:
    selection_path = _coerce_path(args.selection_input_path, repo_root)
    slug = _stem_slug(selection_path)
    return repo_root / "docs" / "issues" / f"publish-verify-remediation-gate-{slug}-{args.operation_family}-result.json"


def _normalize_lifecycle_decision(gate_result: object) -> tuple[str, bool, str]:
    summary = getattr(gate_result, "summary", None)
    reconciliation_count = int(getattr(summary, "reconciliation_count", 0) or 0)
    error_count = int(getattr(summary, "error_count", 0) or 0)
    if reconciliation_count > 0:
        return (
            "stop-for-reconciliation",
            False,
            "At least one lifecycle audit item is in reconciliation state, so the thin gate stops before remediation or apply.",
        )
    if error_count > 0 or str(getattr(gate_result, "decision", "")) == "hard-fail-input":
        return (
            "hard-fail-input",
            False,
            "The lifecycle pre-gate found structurally invalid input or audit errors, so the thin gate fails closed.",
        )
    if str(getattr(gate_result, "decision", "")) == "stop-for-remediation":
        return (
            "stop-for-remediation",
            False,
            "The lifecycle pre-gate emitted replayable warning or blocked findings, so the thin gate stops and surfaces remediation artifacts.",
        )
    return (
        "allow-apply",
        True,
        "The lifecycle pre-gate passed, so the requested family is eligible for delegated continuation behind the thin gate surface.",
    )


def _run_lifecycle_family(args: argparse.Namespace, repo_root: Path) -> PublishVerifyRemediationGateResult:
    with contextlib.redirect_stdout(io.StringIO()):
        gate_result = plan_lifecycle_pre_gate(
            argparse.Namespace(
                input_path=args.selection_input_path,
                input_kind=args.selection_input_kind,
                repo=args.repo,
                audit_plan_path=args.audit_plan_path,
                remediation_plan_path=args.remediation_plan_path,
                decision_path=args.decision_path,
            )
        )

    normalized_decision, apply_allowed, decision_reason = _normalize_lifecycle_decision(gate_result)
    gate_decision_path = (
        _repo_rel(_coerce_path(args.decision_path, repo_root))
        if args.decision_path
        else str(getattr(gate_result, "audit_plan_path", "")).replace("lifecycle-audit-", "lifecycle-gate-").replace("-plan.json", "-decision.json")
    )
    return PublishVerifyRemediationGateResult(
        mode="publish-verify-remediation-gate-dry-run",
        result="ok",
        operation_family=args.operation_family,
        selection_input_kind=args.selection_input_kind,
        selection_input_path=_repo_rel(_coerce_path(args.selection_input_path, repo_root)),
        family_input_kind=None,
        family_input_path=None,
        normalized_decision=normalized_decision,
        apply_allowed=apply_allowed,
        delegated_adapter_path=OPERATION_FAMILIES[args.operation_family],
        decision_reason=decision_reason,
        stopped_before_stage=None,
        downstream_artifacts=DownstreamArtifacts(
            audit_plan_path=str(getattr(gate_result, "audit_plan_path", None) or "") or None,
            gate_decision_path=gate_decision_path or None,
            remediation_plan_path=str(getattr(gate_result, "remediation_plan_path", None) or "") or None,
            family_plan_path=None,
            family_result_path=None,
        ),
        warnings=list(getattr(gate_result, "warnings", []) or []),
    )


def _run_pr_create_preflight(args: argparse.Namespace, repo_root: Path) -> PublishVerifyRemediationGateResult:
    if not args.family_input_path:
        raise SystemExit("pr-create-preflight requires --family-input-path pointing to a PR-prep manifest or plan")

    with contextlib.redirect_stdout(io.StringIO()):
        preflight_result = plan_pr_create_preflight_with_gate(
            argparse.Namespace(
                gate_input_path=args.selection_input_path,
                pr_prep_input_path=args.family_input_path,
                gate_input_kind=args.selection_input_kind,
                pr_prep_input_kind=args.family_input_kind,
                item_index=0,
                repo=args.repo,
                gate_audit_plan_path=args.audit_plan_path,
                gate_remediation_plan_path=args.remediation_plan_path,
                gate_decision_path=args.decision_path,
                pr_prep_plan_path=args.family_plan_path,
                result_path=None,
            )
        )

    if str(preflight_result.gate_decision) == "hard-fail-input":
        normalized_decision = "hard-fail-input"
        apply_allowed = False
        decision_reason = "The reused lifecycle pre-gate failed closed before PR create front-half preflight could continue."
    elif not bool(preflight_result.gate_apply_allowed):
        normalized_decision = "stop-for-remediation"
        apply_allowed = False
        decision_reason = "The reused lifecycle pre-gate stopped for remediation, so PR create front-half preflight cannot continue."
    elif bool(preflight_result.preflight_allowed):
        normalized_decision = "allow-apply"
        apply_allowed = True
        decision_reason = "The reused lifecycle gate plus create-specific front-half preflight both passed, so the next create stage may continue."
    else:
        normalized_decision = "hard-fail-input"
        apply_allowed = False
        decision_reason = "Create-specific front-half preflight found invalid prerequisites before local branch materialization."

    family_plan_path = str(preflight_result.pr_prep_plan_path or "") or None
    family_result_path = family_plan_path.replace("-plan.json", "-front-half-preflight-result.json") if family_plan_path else None
    return PublishVerifyRemediationGateResult(
        mode="publish-verify-remediation-gate-dry-run",
        result="ok",
        operation_family=args.operation_family,
        selection_input_kind=args.selection_input_kind,
        selection_input_path=_repo_rel(_coerce_path(args.selection_input_path, repo_root)),
        family_input_kind=args.family_input_kind,
        family_input_path=_repo_rel(_coerce_path(args.family_input_path, repo_root)),
        normalized_decision=normalized_decision,
        apply_allowed=apply_allowed,
        delegated_adapter_path=OPERATION_FAMILIES[args.operation_family],
        decision_reason=decision_reason,
        stopped_before_stage=str(preflight_result.stopped_before_stage or "") or None,
        downstream_artifacts=DownstreamArtifacts(
            audit_plan_path=None,
            gate_decision_path=str(preflight_result.gate_decision_path or "") or None,
            remediation_plan_path=None,
            family_plan_path=family_plan_path,
            family_result_path=family_result_path,
        ),
        warnings=list(preflight_result.warnings or []),
    )


def plan_publish_verify_remediation_gate(args: argparse.Namespace) -> PublishVerifyRemediationGateResult:
    repo_root = _repo_root()
    selection_input_path = _coerce_path(args.selection_input_path, repo_root)
    if not selection_input_path.is_file():
        raise SystemExit(f"Thin gate selection input file not found: {selection_input_path}")

    if args.operation_family == "pr-create-preflight":
        result = _run_pr_create_preflight(args, repo_root)
    else:
        result = _run_lifecycle_family(args, repo_root)

    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else _default_result_path(args, repo_root)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        plan_publish_verify_remediation_gate(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())