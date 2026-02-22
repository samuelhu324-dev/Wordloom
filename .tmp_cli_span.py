import ast
from pathlib import Path

p = Path('backend/scripts/cli.py')
source = p.read_text(encoding='utf-8', errors='replace')
mod = ast.parse(source)

funcs = []
for node in mod.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith('_cmd_labs_'):
        end = getattr(node, 'end_lineno', None)
        if end is None:
            continue
        span = end - node.lineno + 1
        funcs.append((span, node.name, node.lineno, end))

funcs.sort(reverse=True)
print('Top _cmd_labs_* by span:')
for span, name, start, end in funcs[:25]:
    print(f'{span:4d}  {name}  L{start}-L{end}')

# Also show any non-wrapper candidates: span >= 30
big = [f for f in funcs if f[0] >= 30]
print('\nBig funcs (span>=30):', len(big))
for span, name, start, end in big[:40]:
    print(f'{span:4d}  {name}  L{start}-L{end}')
