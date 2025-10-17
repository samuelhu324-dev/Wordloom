from pathlib import Path
import yaml

DEFAULTS = {
    'project_root': '',
    'tree': {'out_file': 'TREE.md', 'ignore': ['.git','__pycache__','.venv','node_modules','dist','build']},
    'fix_path': {'prefix': '../static'},
    'gif': {'streamlit_path': 'WordloomFrontend/streamlit/gif_maker.py', 'gif_dir': 'assets/static/media/gif', 'thumb_dir': 'assets/static/media/thumb'}
}

def _load_yaml(p: Path):
    if p.exists():
        try:
            with p.open('r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    return {}

def load_config():
    cwd = Path.cwd()
    candidates = [
        cwd / 'tools' / 'WordloomToolkit' / 'config',
        cwd / 'config',
    ]
    cfg_dir = None
    for c in candidates:
        if (c / 'default.yaml').exists() or (c / 'user.yaml').exists():
            cfg_dir = c
            break

    # shallow-merge defaults -> default.yaml -> user.yaml
    cfg = dict(DEFAULTS)
    if cfg_dir:
        def merge(a,b):
            r = dict(a)
            for k,v in (b or {}).items():
                if isinstance(v, dict) and isinstance(r.get(k), dict):
                    r[k].update(v)
                else:
                    r[k] = v
            return r
        cfg = merge(cfg, _load_yaml(cfg_dir / 'default.yaml'))
        cfg = merge(cfg, _load_yaml(cfg_dir / 'user.yaml'))

    if not cfg.get('project_root'):
        if (cwd.name == 'WordloomToolkit' and cwd.parent.name == 'tools'):
            cfg['project_root'] = str(cwd.parent.parent.resolve())
        else:
            cfg['project_root'] = str(cwd.resolve())
    
    # Back-compat: allow top-level gif_dir/thumb_dir keys
    g = cfg.get('gif', {})
    if cfg.get('gif_dir') and not g.get('gif_dir'):
        g['gif_dir'] = cfg.get('gif_dir')
    if cfg.get('thumb_dir') and not g.get('thumb_dir'):
        g['thumb_dir'] = cfg.get('thumb_dir')
    cfg['gif'] = g
return cfg