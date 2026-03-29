from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from gen_issue_draft import (
    _derive_repo_slug,
    _fetch_existing_labels,
    _fetch_existing_milestones,
    _repo_root,
    _require_gh_auth,
    _require_gh_cli,
    _run_command,
)


ISSUE_URL_RE = re.compile(r"/issues/(\d+)$")
PR_URL_RE = re.compile(r"/pull/(\d+)$")


@dataclass
class PrCreateResult:
    mode: str
    result: str
    plan_path: str
    item_index: int
    requested_id: str
    source_log_path: str
    repository: str
    prepared_branch: str
    base_branch: str
    merge_base: str
    selected_commit_count: int
    selected_commits: list[str]
    pr_title: str
    draft: bool
    pr_number: int | None
    pr_url: str | None
    body_path: str
    labels_applied: list[str]
    projects_applied: list[str]
    milestone_applied: str | None
    development_issue: str | None
    warnings: list[str]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a real PR from a PR-prep dry-run plan")
    parser.add_argument("plan_path", help="Path to a PR-prep plan JSON file")
    parser.add_argument("--item-index", dest="item_index", type=int, default=0, help="Plan item index to apply")
    parser.add_argument("--repo", dest="repo", help="Repository slug override")
    parser.add_argument("--ready", dest="ready", action="store_true", help="Create a ready-for-review PR instead of a draft")
    parser.add_argument("--result-path", dest="result_path", help="Override output result JSON path")
    return parser.parse_args()


def _coerce_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def _load_plan(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Failed to parse PR-prep plan JSON: {exc}") from exc


def _repo_rel(path: Path) -> str:
    return path.relative_to(_repo_root()).as_posix()


def _git(*args: str, cwd: Path | None = None) -> str:
    working_dir = cwd or _repo_root()
    cmd = _run_command(["git", "-C", str(working_dir), *args])
    if cmd.returncode != 0:
        raise SystemExit(cmd.stderr.strip() or f"git command failed: {' '.join(args)}")
    return cmd.stdout.strip()


def _git_allow_failure(*args: str, cwd: Path | None = None) -> tuple[int, str, str]:
    working_dir = cwd or _repo_root()
    cmd = _run_command(["git", "-C", str(working_dir), *args])
    return cmd.returncode, cmd.stdout.strip(), cmd.stderr.strip()


def _extract_issue_number(issue_ref: str | None) -> int | None:
    if not issue_ref:
        return None
    issue_ref = issue_ref.strip()
    if issue_ref.isdigit():
        return int(issue_ref)
    match = ISSUE_URL_RE.search(issue_ref)
    if match:
        return int(match.group(1))
    return None


def _ensure_branch_absent(branch_name: str) -> None:
    local_code, _, _ = _git_allow_failure("rev-parse", "--verify", f"refs/heads/{branch_name}")
    if local_code == 0:
        raise SystemExit(f"Local branch already exists: {branch_name}")

    remote_code, stdout, stderr = _git_allow_failure("ls-remote", "--heads", "origin", branch_name)
    if remote_code != 0:
        raise SystemExit(stderr or "Failed to query remote branch existence")
    if stdout.strip():
        raise SystemExit(f"Remote branch already exists: origin/{branch_name}")


def _append_development_link(body_text: str, development_issue: str | None) -> str:
    issue_number = _extract_issue_number(development_issue)
    if issue_number is None:
        return body_text
    link_line = f"Closes #{issue_number}"
    if link_line in body_text:
        return body_text
    return body_text.rstrip() + "\n\n## Development Link\n\n" + link_line + "\n"


def _create_pr(
    *,
    repo: str,
    title: str,
    body_path: Path,
    head_branch: str,
    base_branch: str,
    draft: bool,
    labels: list[str],
    projects: list[str],
    milestone: str | None,
) -> tuple[int, str]:
    command = [
        "gh",
        "pr",
        "create",
        "--repo",
        repo,
        "--head",
        head_branch,
        "--base",
        base_branch,
        "--title",
        title,
        "--body-file",
        str(body_path),
    ]
    if draft:
        command.append("--draft")
    for label in labels:
        command.extend(["--label", label])
    if milestone:
        command.extend(["--milestone", milestone])
    for project in projects:
        command.extend(["--project", project])

    result = _run_command(command)
    if result.returncode != 0:
        raise SystemExit(f"gh pr create failed: {result.stderr.strip()}")
    pr_url = result.stdout.strip().splitlines()[-1].strip()
    match = PR_URL_RE.search(pr_url)
    if not match:
        raise SystemExit(f"Could not parse pull request number from URL: {pr_url}")
    return int(match.group(1)), pr_url


def create_pr_from_plan(args: argparse.Namespace) -> PrCreateResult:
    repo_root = _repo_root()
    plan_path = _coerce_path(args.plan_path, repo_root)
    if not plan_path.is_file():
        raise SystemExit(f"PR-prep plan file not found: {plan_path}")

    plan = _load_plan(plan_path)
    items = plan.get("items") or []
    if args.item_index < 0 or args.item_index >= len(items):
        raise SystemExit(f"Plan item index out of range: {args.item_index}")

    item = items[args.item_index]
    if item.get("status") != "planned":
        raise SystemExit(f"Selected plan item is not in planned state: {item.get('status')}")

    repo = _derive_repo_slug(args.repo)
    _require_gh_cli()
    _require_gh_auth()

    labels = item.get("pr_labels") or []
    projects = item.get("pr_projects") or []
    milestone = item.get("pr_milestone")
    development_issue = item.get("pr_development_issue")

    existing_labels = _fetch_existing_labels(repo)
    missing_labels = [label for label in labels if label not in existing_labels]
    if missing_labels:
        raise SystemExit(f"Missing pre-created PR labels in {repo}: {', '.join(missing_labels)}")

    if milestone:
        milestones = _fetch_existing_milestones(repo)
        if milestone not in milestones:
            raise SystemExit(f"PR milestone does not exist in {repo}: {milestone}")

    prepared_branch = item["candidate_pr_branch"]
    base_branch = item["base_branch"]
    _ensure_branch_absent(prepared_branch)

    _git("fetch", "origin", base_branch)

    worktree_root = repo_root / "artifacts" / f"_tmp_{prepared_branch.replace('/', '_')}_worktree"
    if worktree_root.exists():
        shutil.rmtree(worktree_root)
    worktree_root.parent.mkdir(parents=True, exist_ok=True)

    branch_commits = item.get("selected_commits") or []
    selected_shas = [entry["sha"] for entry in branch_commits]
    if not selected_shas:
        raise SystemExit("Plan item selected no commits; refusing to create PR")

    body_preview_path = _coerce_path(item["preview_body_path"], repo_root)
    if not body_preview_path.is_file():
        raise SystemExit(f"PR body preview file not found: {body_preview_path}")

    plan_slug = plan_path.stem.removesuffix("-plan")
    create_body_path = plan_path.with_name(f"{plan_slug}-create-body.md")
    result_path = _coerce_path(args.result_path, repo_root) if args.result_path else plan_path.with_name(f"{plan_slug}-create-result.json")

    draft = not args.ready
    warnings: list[str] = []
    if not labels:
        warnings.append("pr_labels left blank; PR label assignment intentionally skipped")
    if not projects:
        warnings.append("pr_projects left blank; PR project assignment intentionally skipped")
    if not milestone:
        warnings.append("pr_milestone left blank; PR milestone assignment intentionally skipped")
    if not development_issue:
        warnings.append("pr_development_issue left blank; PR body omits Development link keyword")

    try:
        _git("worktree", "add", "--detach", str(worktree_root), f"origin/{base_branch}")
        _git("switch", "-c", prepared_branch, cwd=worktree_root)
        for sha in selected_shas:
            code, _, stderr = _git_allow_failure("cherry-pick", sha, cwd=worktree_root)
            if code != 0:
                _git_allow_failure("cherry-pick", "--abort", cwd=worktree_root)
                raise SystemExit(f"Cherry-pick failed for {sha}: {stderr}")
        _git("push", "-u", "origin", prepared_branch, cwd=worktree_root)

        create_body = _append_development_link(body_preview_path.read_text(encoding="utf-8"), development_issue)
        create_body_path.write_text(create_body, encoding="utf-8")
        pr_number, pr_url = _create_pr(
            repo=repo,
            title=item["pr_title"],
            body_path=create_body_path,
            head_branch=prepared_branch,
            base_branch=base_branch,
            draft=draft,
            labels=labels,
            projects=projects,
            milestone=milestone,
        )
    finally:
        _git_allow_failure("worktree", "remove", "--force", str(worktree_root))
        if worktree_root.exists():
            shutil.rmtree(worktree_root, ignore_errors=True)

    result = PrCreateResult(
        mode="pr-create",
        result="ok",
        plan_path=_repo_rel(plan_path),
        item_index=args.item_index,
        requested_id=item["requested_id"],
        source_log_path=item["source_log_path"],
        repository=repo,
        prepared_branch=prepared_branch,
        base_branch=base_branch,
        merge_base=item["merge_base"],
        selected_commit_count=len(selected_shas),
        selected_commits=selected_shas,
        pr_title=item["pr_title"],
        draft=draft,
        pr_number=pr_number,
        pr_url=pr_url,
        body_path=_repo_rel(create_body_path),
        labels_applied=labels,
        projects_applied=projects,
        milestone_applied=milestone,
        development_issue=development_issue,
        warnings=warnings,
    )
    result_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=True))
    return result


def main() -> int:
    args = _parse_args()
    try:
        create_pr_from_plan(args)
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())