# -*- coding: utf-8 -*-
"""
Wordloom release helper
功能：
1) 自动读取/创建 根目录 VERSION（默认 0.1.0）
2) 从最近一次 commit 信息判断 bump 类型（feat→minor, fix→patch）
   也可手动指定：--bump major|minor|patch
3) 写入新的 VERSION
4) 更新 CHANGELOG.md（把新条目插到最前）
5) git add/commit/tag/push 全流程

用法：
    python tools/release.py                # 自动从最近一次提交推断 bump
    python tools/release.py --bump minor   # 手动指定
"""
import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

# === 路径配置 ===
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"
VERSION_FILE = PROJECT_ROOT / "VERSION"

# === 基础工具 ===
def run(cmd: str) -> str:
    res = subprocess.run(cmd, text=True, shell=True,
                         capture_output=True, cwd=str(PROJECT_ROOT))
    if res.returncode != 0:
        raise RuntimeError(f"[cmd error] {cmd}\n{res.stderr.strip()}")
    return res.stdout.strip()

def git_inside_repo() -> bool:
    try:
        out = run("git rev-parse --is-inside-work-tree")
        return out == "true"
    except Exception:
        return False

def get_latest_commit_subject() -> str:
    try:
        return run("git log -1 --pretty=%s")
    except Exception:
        return ""

def detect_bump_type_from_msg(msg: str) -> str | None:
    m = msg.lower().strip()
    if m.startswith("feat"):
        return "minor"
    if m.startswith("fix"):
        return "patch"
    return None

def bump_semver(v: str, bump: str) -> str:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", v.strip())
    if not m:
        raise ValueError(f"非法版本号：{v}（需要形如 0.4.2）")
    major, minor, patch = map(int, m.groups())
    if bump == "major":
        major += 1; minor = 0; patch = 0
    elif bump == "minor":
        minor += 1; patch = 0
    elif bump == "patch":
        patch += 1
    else:
        raise ValueError(f"未知 bump 类型：{bump}")
    return f"{major}.{minor}.{patch}"

def ensure_version_file() -> str:
    if not VERSION_FILE.exists():
        VERSION_FILE.write_text("0.1.0", encoding="utf-8")
        print("⚠️ 未找到 VERSION，已自动创建为 0.1.0")
        return "0.1.0"
    return VERSION_FILE.read_text(encoding="utf-8").strip()

def ensure_changelog():
    if not CHANGELOG.exists():
        CHANGELOG.write_text("# 📜 Wordloom Changelog\n", encoding="utf-8")

def prepend_changelog(new_version: str, last_commit_subject: str):
    ensure_changelog()
    today = datetime.now().strftime("%Y-%m-%d")
    new_block = f"\n## [{new_version}] - {today}\n- {last_commit_subject}\n"
    old = CHANGELOG.read_text(encoding="utf-8")
    # 把新条目插在最前（标题后）
    if old.startswith("#"):
        idx = old.find("\n")
        if idx != -1:
            combined = old[:idx+1] + new_block + old[idx+1:]
        else:
            combined = old + new_block
    else:
        combined = "# 📜 Wordloom Changelog\n" + new_block + old
    CHANGELOG.write_text(combined, encoding="utf-8")

def ensure_remote():
    # 若没设置远端，提示并退出（避免迷之报错）
    remotes = run("git remote -v")
    if not remotes:
        raise RuntimeError("当前仓库没有配置远端（git remote）。请先添加 origin 再运行。")

def ensure_commits_exist():
    try:
        run("git rev-parse HEAD")
    except Exception:
        raise RuntimeError("当前仓库还没有任何提交。请先至少做一次 commit 再运行。")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bump", choices=["major", "minor", "patch"],
                        help="手动指定版本递增类型（默认：根据最近一次 commit 自动判断）")
    args = parser.parse_args()

    if not git_inside_repo():
        raise SystemExit("不是一个 Git 仓库。请在 Wordloom 根目录初始化后再运行。")

    ensure_remote()
    ensure_commits_exist()

    # 读取/创建 VERSION
    current_version = ensure_version_file()

    # 读取最近一次提交信息
    last_msg = get_latest_commit_subject()
    if not last_msg:
        raise SystemExit("读取不到最近一次提交信息。请先提交一次，再运行。")
    print(f"🧾 最近一次提交：{last_msg}")

    # 决定 bump 类型
    bump_type = args.bump or detect_bump_type_from_msg(last_msg)
    if not bump_type:
        print("⚠️ 最近一次提交不是 feat/fix（或你未指定 --bump），不自动升级版本。")
        return

    # 计算新版本
    new_version = bump_semver(current_version, bump_type)
    print(f"📦 版本号：{current_version}  →  {new_version}  ({bump_type})")

    # 写入 VERSION
    VERSION_FILE.write_text(new_version, encoding="utf-8")

    # 更新 CHANGELOG（插到最前）
    prepend_changelog(new_version, last_msg)

    # 提交、打标签、推送
    run("git add VERSION CHANGELOG.md")
    run(f'git commit -m "chore(release): bump version to {new_version}"')
    run(f'git tag -a v{new_version} -m "release {new_version}"')
    run("git push")
    run("git push --tags")

    print(f"✅ 已发布 v{new_version}，CHANGELOG 与 tag 均已更新并推送。")

if __name__ == "__main__":
    main()
