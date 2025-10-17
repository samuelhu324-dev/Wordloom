from pathlib import Path
import subprocess, sys

def run_fix_script(project_root: Path, target: Path, no_html=False, width=480, script_rel='assets/docs/fix_md_paths.py'):
    # Invoke user's fix_md_paths.py on given target (file or dir).
    script = (project_root / script_rel).resolve()
    if not script.exists():
        raise FileNotFoundError(f'找不到脚本: {script}')
    args = [sys.executable, str(script), str(target)]
    if target.is_dir():
        args += ['-g', '*.md']
    if no_html:
        args += ['--no-html']
    if width:
        args += ['--width', str(width)]
    return subprocess.run(args, capture_output=True, text=True)