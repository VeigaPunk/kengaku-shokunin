import contextlib
import io
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
OUT = LANE / '.ufo/waves/round-76/w1/C1ReplayR76'
S = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/C1ReplayR76'

def run(args, label):
    p = subprocess.run(args, cwd=LANE, capture_output=True, text=True)
    text = '$ ' + ' '.join(args) + '\n' + p.stdout + p.stderr + f'rc={p.returncode}\n'
    (OUT / (label + '.txt')).write_text(text)
    print(text, end='')
    return p

def expand(token):
    if '{' not in token:
        return [token]
    prefix, tail = token.split('{', 1)
    choices, suffix = tail.split('}', 1)
    return [p for choice in choices.split(',') for p in expand(prefix + choice + suffix)]

try:
    S.mkdir(parents=True, exist_ok=True)
    base = run(['git', 'show', 'fda63968:PROVINCE.md'], 'base-province').stdout
    before = run(['python3', 'plans/round76_c1_surface_resolver.py', '--lane', '.', '--rev', 'fda63968'], 'before')
    run(['python3', 'plans/round76_c1_surface_resolver.py', '--lane', '.'], 'worktree')
    gate_rows = {}
    for line in before.stdout.splitlines():
        if line.startswith('SURFACE '):
            _, n, verdict, *_ = line.split()
            gate_rows[int(n)] = verdict
    section = base.split('## Surfaces', 1)[1].split('\n## ', 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith('|'):
            continue
        cells = line.strip('|').split('|')
        if cells[0].strip() == 'Surface' or set(cells[0].strip()) <= {'-', ':'}:
            continue
        rows.append(cells)
    lines = []
    for n, cells in enumerate(rows, 1):
        # Independent parser: take the first literal backtick token, no gate helpers.
        token = cells[1].split('`')[1]
        if token.startswith('http'):
            p = subprocess.run(['curl', '-s', '-m', '3', '-o', '/dev/null', '-w', '%{http_code}', token], capture_output=True, text=True)
            verdict = 'absent' if p.stdout == '000' else 'present'
            detail = f'curl_code={p.stdout} rc={p.returncode}'
        else:
            probes = []
            for target in expand(token):
                path = os.path.expanduser(target) if target.startswith('~/') else str(LANE / target)
                p = subprocess.run(['test', '-e', path], capture_output=True, text=True)
                probes.append((target, p.returncode))
            verdict = 'present' if any(rc == 0 for _, rc in probes) else 'absent'
            detail = repr(probes)
        lines.append(f'INDEPENDENT {n} {verdict} {token} {detail} gate={gate_rows.get(n)} match={gate_rows.get(n) == verdict}')
    # Test every home token in base table, including secondary/old paths.
    for token in sorted(set(re.findall(r'`(~/[^`\s]+)`', section))):
        for target in expand(token):
            p = subprocess.run(['test', '-e', os.path.expanduser(target)], capture_output=True, text=True)
            lines.append(f'HOME test -e {target} rc={p.returncode}')
    (OUT / 'independent.txt').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
    for port in (34113, 45669):
        run(['curl', '-s', '-m', '3', '-o', '/dev/null', '-w', '%{http_code}', f'http://127.0.0.1:{port}/health'], f'health-{port}')
    run(['python3', 'plans/round76_c1_surface_resolver.py', '--lane', '.', '--control-declared', '--work', str(S / 'current-control')], 'control-worktree')
    # The actual control binds its lane to __file__, ignoring --lane and --rev.
    # Rebind only __file__ to give it untouched base PROVINCE bytes; no source rewrite.
    (S / 'plans').mkdir(exist_ok=True)
    (S / 'PROVINCE.md').write_text(base)
    namespace = runpy.run_path(str(LANE / 'plans/round76_c1_surface_resolver.py'))
    fn = namespace['control_declared']
    fn.__globals__['__file__'] = str(S / 'plans/round76_c1_surface_resolver.py')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn(S / 'base-control')
    text = "CONTROL invocation: runpy.run_path(gate); control_declared.__globals__['__file__']=S/plans/round76_c1_surface_resolver.py; control_declared(S/'base-control') with base PROVINCE.md at S\n" + buf.getvalue() + f'rc={rc}\n'
    (OUT / 'control-base.txt').write_text(text)
    print(text)
finally:
    shutil.rmtree(S)
    print(f'SCRATCH removed={not S.exists()} {S}')
