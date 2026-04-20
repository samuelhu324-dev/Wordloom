"""S4F-1A P2 access/subscription drills runner.

Runs the three access-aware probes defined by the S4F-1A packet against a
real local API process started inside the drill runtime:
- member access-context read
- admin subscription read
- admin lifecycle mutation followed by deterministic re-read/history

The script is designed for GitHub Actions `drill-labs-scenario` execution, but
it can also be run locally when a PostgreSQL database is available.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx
import jwt
from sqlalchemy import create_engine, text


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
DEFAULT_SCENARIO = "verify/access_subscription/deployable_cut"
DEFAULT_SUITE_ID = "access_subscription_deployable_cut"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        env[key] = value
    return env


def _convert_to_psycopg(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql+"):
        parts = url.split("://", 1)
        if len(parts) == 2:
            return f"postgresql+psycopg://{parts[1]}"
    return url


def _redact_database_url(url: str) -> str:
    return re.sub(r":([^@]+)@", r":***@", url, count=1)


def _get_git_sha() -> str | None:
    sha = os.getenv("GITHUB_SHA", "").strip()
    if sha:
        return sha
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return None


def _make_token(*, user_id: uuid.UUID, secret_key: str, algorithm: str) -> str:
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_log(path: Path, line: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line.rstrip() + "\n")


def _parse_json_response(response: httpx.Response) -> Any:
    content_type = (response.headers.get("content-type") or "").lower()
    if "application/json" not in content_type:
        return None
    try:
        return response.json()
    except Exception:
        return None


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _start_api_process(*, env: dict[str, str], logs_dir: Path) -> subprocess.Popen[str]:
    api_stdout = (logs_dir / "api.stdout.log").open("w", encoding="utf-8")
    api_stderr = (logs_dir / "api.stderr.log").open("w", encoding="utf-8")
    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "api.app.main:app",
        "--host",
        "127.0.0.1",
        "--port",
        env["API_PORT"],
    ]
    return subprocess.Popen(
        command,
        cwd=str(BACKEND_DIR),
        env=env,
        stdout=api_stdout,
        stderr=api_stderr,
        text=True,
    )


def _wait_for_health(*, base_url: str, process: subprocess.Popen[str], log_path: Path, timeout_s: float = 60.0) -> None:
    deadline = time.time() + timeout_s
    last_error = "health_timeout"
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"api_process_exited:{process.returncode}")
        try:
            response = httpx.get(f"{base_url}/api/v1/health", timeout=3.0)
            if response.status_code == 200:
                _append_log(log_path, f"api_health=200 base_url={base_url}")
                return
            last_error = f"health_status_{response.status_code}"
        except Exception as exc:  # noqa: BLE001
            last_error = f"{type(exc).__name__}:{exc}"
        time.sleep(1.0)
    raise RuntimeError(last_error)


def _seed_subscription_state(*, database_url: str, library_id: str, log_path: Path) -> None:
    engine = create_engine(_convert_to_psycopg(database_url), future=True)
    try:
        with engine.begin() as conn:
            subscription_id = str(uuid.uuid4())
            conn.execute(
                text(
                    """
                    INSERT INTO subscriptions (id, library_id, plan_code, state, created_at, updated_at)
                    VALUES (:id, :library_id, 'trial', 'trialing', TIMEZONE('utc', NOW()), TIMEZONE('utc', NOW()))
                    """
                ),
                {"id": subscription_id, "library_id": library_id},
            )
            conn.execute(
                text(
                    """
                    INSERT INTO entitlement_snapshots (
                      id,
                      library_id,
                      plan_code,
                      subscription_state,
                      entitlements,
                      created_at,
                      updated_at
                    )
                    VALUES (
                      :id,
                      :library_id,
                      'trial',
                      'trialing',
                      'read_library',
                      TIMEZONE('utc', NOW()),
                      TIMEZONE('utc', NOW())
                    )
                    """
                ),
                {"id": str(uuid.uuid4()), "library_id": library_id},
            )
        _append_log(log_path, f"seed_subscription_state=ok library_id={library_id}")
    finally:
        engine.dispose()


def _normalize_roles(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return []


def _normalize_history_items(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return []
    items = value.get("items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def run(*, env_file: Path, run_id: str, outdir: Path, scenario: str) -> dict[str, Any]:
    _ensure_dir(outdir)
    logs_dir = outdir / "_logs"
    metrics_dir = outdir / "_metrics"
    _ensure_dir(logs_dir)
    _ensure_dir(metrics_dir)

    runner_log = logs_dir / "runner.log"
    _append_log(runner_log, f"started_at={_now_iso()}")
    _append_log(runner_log, f"run_id={run_id}")

    base_env = os.environ.copy()
    base_env.update(_load_env_file(env_file))

    owner_user_id = uuid.uuid4()
    member_user_id = uuid.uuid4()
    admin_user_id = uuid.uuid4()

    api_port = str(base_env.get("API_PORT") or "30011")
    api_base_url = (base_env.get("WORDLOOM_API_BASE_URL") or f"http://127.0.0.1:{api_port}").rstrip("/")
    database_url = (base_env.get("DATABASE_URL") or "").strip()
    secret_key = (base_env.get("WORDLOOM_JWT_SECRET_KEY") or base_env.get("SECRET_KEY") or "dev-secret-key-change-in-production").strip()
    algorithm = (base_env.get("WORDLOOM_JWT_ALG") or base_env.get("ALGORITHM") or "HS256").strip()

    _require(bool(database_url), "DATABASE_URL is required")

    api_env = base_env.copy()
    api_env["API_PORT"] = api_port
    api_env["DEV_USER_ID"] = str(owner_user_id)
    api_env["PYTHONPATH"] = str(BACKEND_DIR)
    api_env.setdefault("WORDLOOM_ENV", "test")
    api_env.setdefault("ENVIRONMENT", "ci-test")

    git_sha = _get_git_sha()
    started_at = _now_iso()

    recipe = {
        "schema_version": "s4f-1a.recipe.v1",
        "scenario": scenario,
        "suite_id": DEFAULT_SUITE_ID,
        "run_id": run_id,
        "meta": {
            "started_at": started_at,
            "git_sha": git_sha,
        },
        "config": {
            "env_file": str(env_file),
            "api_base_url": api_base_url,
            "database_url_redacted": _redact_database_url(database_url),
            "jwt_algorithm": algorithm,
            "owner_user_id": str(owner_user_id),
        },
        "contract": {
            "member_probe": "/api/v1/access-context/me",
            "admin_probe": "/api/v1/admin/subscriptions/{library_id}",
            "lifecycle_probe": "/api/v1/admin/subscriptions/{library_id}/events",
        },
    }
    _write_json(outdir / "_recipe.json", recipe)

    api_process: subprocess.Popen[str] | None = None
    result_payload: dict[str, Any] = {}
    timings: dict[str, float] = {}

    try:
        api_process = _start_api_process(env=api_env, logs_dir=logs_dir)
        _wait_for_health(base_url=api_base_url, process=api_process, log_path=runner_log)

        owner_token = _make_token(user_id=owner_user_id, secret_key=secret_key, algorithm=algorithm)
        member_token = _make_token(user_id=member_user_id, secret_key=secret_key, algorithm=algorithm)
        admin_token = _make_token(user_id=admin_user_id, secret_key=secret_key, algorithm=algorithm)

        t_create = time.time()
        with httpx.Client(base_url=api_base_url, timeout=30.0) as client:
            create_response = client.post(
                "/api/v1/libraries",
                json={
                    "name": f"s4f1a-{run_id[:8]}",
                    "description": "S4F-1A drill library",
                },
            )
            create_json = _parse_json_response(create_response) or {}
            _require(create_response.status_code == 201, f"create_library_status={create_response.status_code}")
            library_id = str(create_json.get("id") or "")
            _require(bool(library_id), "create_library_missing_id")
            timings["create_library_seconds"] = round(time.time() - t_create, 3)

            _seed_subscription_state(database_url=database_url, library_id=library_id, log_path=runner_log)

            owner_headers = {
                "Authorization": f"Bearer {owner_token}",
                "X-Library-Id": library_id,
            }
            for granted_user_id, role in ((member_user_id, "member"), (admin_user_id, "admin")):
                grant_response = client.post(
                    f"/api/v1/libraries/{library_id}/memberships",
                    headers=owner_headers,
                    json={"user_id": str(granted_user_id), "role": role},
                )
                _require(grant_response.status_code == 204, f"grant_membership_{role}_status={grant_response.status_code}")

            t_member = time.time()
            member_response = client.get(
                "/api/v1/access-context/me",
                headers={
                    "Authorization": f"Bearer {member_token}",
                    "X-Library-Id": library_id,
                },
            )
            member_json = _parse_json_response(member_response) or {}
            timings["member_probe_seconds"] = round(time.time() - t_member, 3)

            t_admin = time.time()
            admin_response = client.get(
                f"/api/v1/admin/subscriptions/{library_id}",
                headers={
                    "Authorization": f"Bearer {admin_token}",
                    "X-Library-Id": library_id,
                },
            )
            admin_json = _parse_json_response(admin_response) or {}
            timings["admin_probe_seconds"] = round(time.time() - t_admin, 3)

            t_lifecycle = time.time()
            lifecycle_response = client.post(
                f"/api/v1/admin/subscriptions/{library_id}/events",
                headers={
                    "Authorization": f"Bearer {admin_token}",
                    "X-Library-Id": library_id,
                },
                json={"event_type": "upgrade_success"},
            )
            lifecycle_json = _parse_json_response(lifecycle_response) or {}

            reread_response = client.get(
                f"/api/v1/admin/subscriptions/{library_id}",
                headers={
                    "Authorization": f"Bearer {admin_token}",
                    "X-Library-Id": library_id,
                },
            )
            reread_json = _parse_json_response(reread_response) or {}

            history_response = client.get(
                f"/api/v1/admin/subscriptions/{library_id}/history",
                headers={
                    "Authorization": f"Bearer {admin_token}",
                    "X-Library-Id": library_id,
                },
            )
            history_json = _parse_json_response(history_response) or {}
            timings["lifecycle_probe_seconds"] = round(time.time() - t_lifecycle, 3)

        member_roles = _normalize_roles(member_json.get("roles"))
        admin_entitlements = member_json.get("entitlements") if isinstance(member_json.get("entitlements"), list) else member_json.get("entitlements")
        history_items = _normalize_history_items(history_json)

        member_ok = (
            member_response.status_code == 200
            and str(member_json.get("tenant_id")) == library_id
            and "member" in member_roles
            and bool(member_json.get("plan_code"))
            and bool(member_json.get("subscription_state"))
            and "read_library" in list(member_json.get("entitlements") or [])
        )
        admin_ok = (
            admin_response.status_code == 200
            and str(admin_json.get("library_id")) == library_id
            and bool(admin_json.get("plan_code"))
            and bool(admin_json.get("subscription_state"))
            and "read_library" in list(admin_json.get("entitlements") or [])
        )
        lifecycle_ok = (
            lifecycle_response.status_code == 200
            and str(lifecycle_json.get("library_id")) == library_id
            and lifecycle_json.get("subscription_state") == "active"
        )
        rerender_ok = (
            reread_response.status_code == 200
            and reread_json.get("subscription_state") == "active"
            and history_response.status_code == 200
            and any(item.get("event_type") == "upgrade_success" for item in history_items)
        )

        finished_at = _now_iso()
        result_payload = {
            "schema_version": "s4f-1a.result.v1",
            "scenario": scenario,
            "suite_id": DEFAULT_SUITE_ID,
            "run_id": run_id,
            "run_dir": str(outdir.resolve()),
            "ok": bool(member_ok and admin_ok and lifecycle_ok and rerender_ok),
            "meta": {
                "started_at": started_at,
                "finished_at": finished_at,
                "git_sha": git_sha,
                "api_base_url": api_base_url,
                "database_url_redacted": _redact_database_url(database_url),
                "library_id": library_id,
                "owner_user_id": str(owner_user_id),
                "member_user_id": str(member_user_id),
                "admin_user_id": str(admin_user_id),
            },
            "checks": {
                "memberReadResult": member_ok,
                "adminReadResult": admin_ok,
                "lifecycleMutationResult": lifecycle_ok,
                "rerenderedStateResult": rerender_ok,
            },
            "observed": {
                "createLibrary": {
                    "status_code": create_response.status_code,
                    "body": create_json,
                },
                "memberReadResult": {
                    "status_code": member_response.status_code,
                    "body": member_json,
                },
                "adminReadResult": {
                    "status_code": admin_response.status_code,
                    "body": admin_json,
                },
                "lifecycleMutationResult": {
                    "status_code": lifecycle_response.status_code,
                    "body": lifecycle_json,
                },
                "rerenderedStateResult": {
                    "status_code": reread_response.status_code,
                    "body": reread_json,
                },
                "historyResult": {
                    "status_code": history_response.status_code,
                    "body": history_json,
                },
            },
            "summary": {
                "total": 4,
                "passed": int(member_ok) + int(admin_ok) + int(lifecycle_ok) + int(rerender_ok),
                "failed": 4 - (int(member_ok) + int(admin_ok) + int(lifecycle_ok) + int(rerender_ok)),
            },
        }
        _write_json(metrics_dir / "timings.json", timings)
        return result_payload
    finally:
        if api_process is not None:
            api_process.terminate()
            try:
                api_process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                api_process.kill()
                api_process.wait(timeout=15)
        if not (metrics_dir / "timings.json").exists():
            _write_json(metrics_dir / "timings.json", timings)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run S4F-1A P2 access/subscription drills")
    parser.add_argument("--env-file", default=os.getenv("ENV_FILE", ".env.test"))
    parser.add_argument("--run-id", default=os.getenv("RUN_ID") or str(uuid.uuid4()))
    parser.add_argument("--outdir", default="")
    parser.add_argument("--scenario", default=DEFAULT_SCENARIO)
    args = parser.parse_args()

    env_file = Path(args.env_file)
    if not env_file.is_absolute():
        env_file = (REPO_ROOT / env_file).resolve()
    if not env_file.exists():
        raise SystemExit(f"env_file_not_found:{env_file}")

    if args.outdir:
        outdir = Path(args.outdir)
        if not outdir.is_absolute():
            outdir = (REPO_ROOT / outdir).resolve()
    else:
        outdir = REPO_ROOT / "docs" / "labs" / "_snapshot" / "auto" / "S4F-1A" / DEFAULT_SUITE_ID / str(args.run_id)

    started_at = _now_iso()
    try:
        result = run(env_file=env_file, run_id=str(args.run_id), outdir=outdir, scenario=str(args.scenario))
    except Exception as exc:  # noqa: BLE001
        failed_at = _now_iso()
        _ensure_dir(outdir)
        _ensure_dir(outdir / "_logs")
        _ensure_dir(outdir / "_metrics")
        _append_log(outdir / "_logs" / "runner.log", f"error={type(exc).__name__}:{exc}")
        failure_payload = {
            "schema_version": "s4f-1a.result.v1",
            "scenario": str(args.scenario),
            "suite_id": DEFAULT_SUITE_ID,
            "run_id": str(args.run_id),
            "run_dir": str(outdir.resolve()),
            "ok": False,
            "meta": {
                "started_at": started_at,
                "finished_at": failed_at,
                "git_sha": _get_git_sha(),
            },
            "checks": {
                "memberReadResult": False,
                "adminReadResult": False,
                "lifecycleMutationResult": False,
                "rerenderedStateResult": False,
            },
            "observed": {
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            },
            "summary": {"total": 4, "passed": 0, "failed": 4},
        }
        _write_json(outdir / "_result.json", failure_payload)
        _write_json(outdir / "_metrics" / "timings.json", {"failed": True})
        return 2

    _write_json(outdir / "_result.json", result)
    return 0 if bool(result.get("ok")) else 2


if __name__ == "__main__":
    raise SystemExit(main())