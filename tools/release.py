import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

# === 配置 ===
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"
VERSION_FILE = PROJECT_ROOT / "VERSION"

# === 工具函数 ===
def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print("❌ Error:", result.stderr.strip())
        raise SystemExit(1)
    return result.stdout.strip()

def get_latest_commit_message():
    msg = run("git log -1 --pretty=%s")
    print(f"最新提交信息：{msg}")
    return msg

def detect_bump_type(msg):
    msg = msg.lower()
    if msg.startswith("feat"):
        return "minor"
    elif msg.startswith("fix"):
        return "patch"
    else:
        return None

def bump_version(version, bump_type):
    major, minor, patch = map(int, version.split("."))
    if bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"

# === 主逻辑 ===
def main():
    os.chdir(PROJECT_ROOT)
    current_version = VERSION_FILE.read_text(encoding="utf-8").strip()
    msg = get_latest_commit_message()
    bump_type = detect_bump_type(msg)

    if not bump_type:
        print("⚠️ 此次提交不是 feat 或 fix 类型，不自动提升版本。")
        return

    new_version = bump_version(current_version, bump_type)
    print(f"📦 版本号：{current_version} → {new_version}")

    # 写入新版本号
    VERSION_FILE.write_text(new_version, encoding="utf-8")

    # 更新 CHANGELOG.md
    now = datetime.now().strftime("%Y-%m-%d")
    changelog_entry = f"\n## [{new_version}] - {now}\n- {msg}\n"
    content = CHANGELOG.read_text(encoding="utf-8")
    new_content = content.strip() + changelog_entry
    CHANGELOG.write_text(new_content, encoding="utf-8")

    # Git 提交 & 打标签
    run("git add VERSION CHANGELOG.md")
    run(f'git commit -m "chore(release): bump version to {new_version}"')
    run(f'git tag -a v{new_version} -m "release {new_version}"')
    run("git push && git push --tags")

    print(f"✅ 完成版本更新至 v{new_version}")

if __name__ == "__main__":
    main()
