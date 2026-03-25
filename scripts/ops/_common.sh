#!/usr/bin/env bash
set -euo pipefail

ops_script_dir() {
  cd "$(dirname "${BASH_SOURCE[0]}")" && pwd
}

repo_root() {
  cd "$(ops_script_dir)/../.." && pwd
}

resolve_env_name() {
  local env_name="${1:-dev}"
  case "$env_name" in
    dev|test)
      printf '%s\n' "$env_name"
      ;;
    *)
      echo "[ops] Unknown env '$env_name' (expected: dev|test)" >&2
      return 2
      ;;
  esac
}

env_file_for() {
  local env_name
  env_name="$(resolve_env_name "${1:-dev}")"
  printf '%s/.env.%s\n' "$(repo_root)" "$env_name"
}

source_env_file() {
  local env_file="$1"
  if [[ ! -f "$env_file" ]]; then
    echo "[ops] env file not found: $env_file" >&2
    return 1
  fi

  set -a
  # shellcheck disable=SC1090
  source <(sed 's/\r$//' "$env_file")
  set +a
}

docker_bin() {
  if command -v docker >/dev/null 2>&1; then
    printf 'docker\n'
    return 0
  fi
  if command -v docker.exe >/dev/null 2>&1; then
    printf 'docker.exe\n'
    return 0
  fi

  echo "[ops] docker not found" >&2
  return 1
}

ssh_bin() {
  if [[ -n "${WSL_INTEROP:-}" || -n "${WSL_DISTRO_NAME:-}" || "${OSTYPE:-}" == msys* || "${OSTYPE:-}" == cygwin* || "${MSYSTEM:-}" != "" ]]; then
    if command -v ssh.exe >/dev/null 2>&1; then
      printf 'ssh.exe\n'
      return 0
    fi
  fi

  if command -v ssh >/dev/null 2>&1; then
    printf 'ssh\n'
    return 0
  fi

  if command -v ssh.exe >/dev/null 2>&1; then
    printf 'ssh.exe\n'
    return 0
  fi

  echo "[ops] ssh not found" >&2
  return 1
}

normalize_ssh_identity_path() {
  local ssh_command="${1:-}"
  local identity_path="${2:-}"

  if [[ -z "$identity_path" ]]; then
    printf '%s\n' "$identity_path"
    return 0
  fi

  if [[ "${ssh_command##*/}" != "ssh.exe" ]]; then
    printf '%s\n' "$identity_path"
    return 0
  fi

  if [[ "$identity_path" =~ ^/([a-zA-Z])/(.*)$ ]]; then
    local drive rest
    drive="${BASH_REMATCH[1]}"
    rest="${BASH_REMATCH[2]//\//\\}"
    printf '%s\n' "${drive^^}:\\$rest"
    return 0
  fi

  if command -v wslpath >/dev/null 2>&1; then
    local converted
    converted="$(wslpath -w "$identity_path" 2>/dev/null | tr -d '\r' || true)"
    if [[ -n "$converted" ]]; then
      printf '%s\n' "$converted"
      return 0
    fi
  fi

  printf '%s\n' "$identity_path"
}

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ops] Missing required command '$cmd'" >&2
    return 1
  fi
}

http_code_windows_fallback() {
  local url="$1"

  if [[ -z "${WSL_DISTRO_NAME:-}" && -z "${WSL_INTEROP:-}" ]]; then
    return 1
  fi

  if ! command -v powershell.exe >/dev/null 2>&1; then
    return 1
  fi

  powershell.exe -NoProfile -Command "try { \$response = Invoke-WebRequest -Uri '$url' -Method Head -TimeoutSec 8; [Console]::WriteLine(\$response.StatusCode) } catch { if (\$_.Exception.Response -and \$_.Exception.Response.StatusCode.value__) { [Console]::WriteLine(\$_.Exception.Response.StatusCode.value__) } else { [Console]::WriteLine('000') } }" 2>/dev/null | tr -d '\r' | tail -n 1
}

http_code() {
  local url="$1"
  local code

  code="$(curl -s -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || true)"
  if [[ -n "$code" && "$code" != "000" ]]; then
    printf '%s\n' "$code"
    return 0
  fi

  code="$(http_code_windows_fallback "$url" || true)"
  if [[ -n "$code" ]]; then
    printf '%s\n' "$code"
    return 0
  fi

  printf '000\n'
}

check_http_ok() {
  local label="$1"
  local url="$2"
  shift 2
  local expected=("$@")
  local code

  code="$(http_code "$url" || true)"
  if [[ -z "$code" || "$code" == "000" ]]; then
    echo "[ops] $label DOWN ($url)" >&2
    return 1
  fi

  local candidate
  for candidate in "${expected[@]}"; do
    if [[ "$code" == "$candidate" ]]; then
      echo "[ops] $label OK ($code)"
      return 0
    fi
  done

  echo "[ops] $label unexpected HTTP $code ($url)" >&2
  return 1
}

container_id_for() {
  local compose_file="$1"
  local project_name="$2"
  local service_name="$3"
  local docker_cmd

  docker_cmd="$(docker_bin)"
  "$docker_cmd" compose -f "$compose_file" -p "$project_name" ps -q "$service_name" 2>/dev/null | tr -d '\r' | head -n 1
}

container_health_for() {
  local container_id="$1"
  local docker_cmd

  docker_cmd="$(docker_bin)"
  "$docker_cmd" inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$container_id" 2>/dev/null | tr -d '\r'
}

print_kv() {
  printf '%-18s %s\n' "$1" "$2"
}