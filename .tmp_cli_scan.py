import re
from collections import Counter
from pathlib import Path

text = Path('backend/scripts/cli.py').read_text(encoding='utf-8', errors='replace')
cmds = re.findall(r'^def (_cmd_labs_[a-zA-Z0-9_]+)\(', text, flags=re.M)
print('total _cmd_labs_* defs:', len(cmds))

def group_key(name: str) -> str:
    s = name[len('_cmd_labs_'):]
    parts = s.split('_')
    if len(parts) >= 2 and parts[0] == 'shadow' and parts[1] == 'verify':
        return 'shadow_verify'
    if parts and parts[0] in {'run', 'verify', 'export', 'clean'}:
        return parts[0]
    return parts[0] if parts else s

counts = Counter(group_key(c) for c in cmds)
print('\nTop groups (heuristic):')
for k, v in counts.most_common(30):
    print(f'  {k:12s} {v}')

counts2 = Counter('_'.join(c[len('_cmd_labs_'):].split('_')[:2]) for c in cmds)
print('\nTop 2-token prefixes:')
for k, v in counts2.most_common(40):
    print(f'  {k:24s} {v}')
