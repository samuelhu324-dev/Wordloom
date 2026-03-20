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

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ops] Missing required command '$cmd'" >&2
    return 1
  fi
}

http_code() {
  local url="$1"
  curl -s -o /dev/null -w '%{http_code}' "$url" 2>/dev/null
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