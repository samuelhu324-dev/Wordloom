"""
fix_paths.py
------------
目的：把仓库里“写死的绝对路径”和“旧资产路径”统一替换为相对、规范路径。
- 把下列前缀替换为项目根相对路径：
    D:\Project\Wordloom\
    d:\Project\Wordloom\
    d:/Project/Wordloom/
- 把旧的 assets/media/ 规范为 assets/static/media/
使用：
    python fix_paths.py --dry-run     # 先看看要改哪些
    python fix_paths.py               # 实际写入，并生成 .bak 备份
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from typing import Iterable

# 需要处理的文件后缀
SUFFIXES = {".py", ".md", ".txt", ".json", ".yml", ".yaml", ".ini", ".toml", ".html"}

ABS_PREFIX_PATTERNS = [
    re.compile(r"D:\\\\Project\\\\Wordloom\\\\", flags=re.IGNORECASE),
    re.compile(r"d:\\\\Project\\\\Wordloom\\\\", flags=re.IGNORECASE),
    re.compile(r"d:/Project/Wordloom/", flags=re.IGNORECASE),
]

def iter_files(base: Path) -> Iterable[Path]:
    for p in base.rglob("*"):
        if p.is_file() and p.suffix in SUFFIXES and p.name != "fix_paths.py":
            yield p

def normalize_text(text: str) -> str:
    original = text

    # 1) 绝对路径 → 相对根（去掉前缀，保留后续相对路径）
    for pat in ABS_PREFIX_PATTERNS:
        text = pat.sub("", text)

    # 2) 旧资产路径 → 新规范路径
    #   assets/media/...  -> assets/static/media/...
    text = re.sub(r"assets[/\\\\]media[/\\\\]", "assets/static/media/", text, flags=re.IGNORECASE)

    return text if text != original else original

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只打印变更，不写回文件")
    ap.add_argument("--base", type=str, default=".", help="仓库根目录（默认当前）")
    args = ap.parse_args()

    base = Path(args.base).resolve()
    changed = 0
    for f in iter_files(base):
        txt = f.read_text(encoding="utf-8", errors="ignore")
        new_txt = normalize_text(txt)
        if new_txt != txt:
            changed += 1
            print(f"[CHANGE] {f.relative_to(base)}")
            if not args.dry_run:
                bak = f.with_suffix(f.suffix + ".bak")
                if not bak.exists():
                    bak.write_text(txt, encoding="utf-8", errors="ignore")
                f.write_text(new_txt, encoding="utf-8")
    if changed == 0:
        print("No changes needed.")
    else:
        print(f"Done. Files changed: {changed}")

if __name__ == "__main__":
    main()