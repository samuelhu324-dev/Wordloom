# tools/WordloomToolkit/core/tree_runner.py
from pathlib import Path
import subprocess, os

def write_tree_cmd(root: Path, out_file: Path) -> bool:
    """优先用系统 tree，但先 pushd 进入目录，避免 D:\\D:\\... 的路径解析 bug。"""
    try:
        root = root.resolve()
        if not root.exists() or not root.is_dir():
            return False
        # /d 允许跨盘符 pushd；不把路径再传给 tree，避免重复
        cmd = ['cmd', '/d', '/c', f'pushd "{root}" && tree /f /a && popd']
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = (res.stdout or "")
        # 返回码非 0，或包含“无效的路径/Invalid path”都视为失败
        if res.returncode != 0 or "无效的路径" in out or "Invalid path" in out:
            return False
        out_file.write_text(out, encoding='utf-8', errors='ignore')
        return True
    except Exception:
        return False

def write_tree_py(root: Path, out_file: Path, ignore=()):
    """兜底：纯 Python 生成目录树。"""
    lines = []
    root = root.resolve()
    skip = set(ignore or [])
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        rel = Path(dirpath).relative_to(root)
        depth = 0 if str(rel) == '.' else len(rel.parts)
        indent = '    ' * depth
        if str(rel) != '.':
            lines.append(f"{indent}{rel.name}/")
        subindent = '    ' * (depth + (0 if str(rel) == '.' else 1))
        for f in filenames:
            lines.append(f"{subindent}{f}")
    out_file.write_text('\n'.join(lines), encoding='utf-8')
