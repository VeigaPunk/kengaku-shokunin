#!/usr/bin/env python3
"""Independent evidence replay; never imports the R76 discharge gate."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
OUT = LANE / '.ufo/waves/round-76/w1/C2ReplayR76'
SCRATCH = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/C2ReplayR76'
BASE = 'fda63968'

def command(args, name):
    p = subprocess.run(args, cwd=LANE, text=True, capture_output=True)
    text = '$ ' + ' '.join(args) + '\n' + p.stdout + p.stderr + f'RC {p.returncode}\n'
    (OUT / (name + '.txt')).write_text(text)
    return text

def git(*args):
    p = subprocess.run(['git', '-C', str(LANE), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError((args, p.returncode, p.stderr))
    return p.stdout

# Only redirect the gate's unconditional, hard-coded scratch mkdir. Rev mode never
# uses that directory afterwards; gate source and all measured bytes are unchanged.
wrapper = OUT / 'before_sandbox.py'
wrapper.write_text('''import pathlib, runpy, sys\noriginal = pathlib.Path.mkdir\ndef mkdir(self, *args, **kwargs):\n    if str(self) == "/fast/scratch/hyaku/kengaku-r76/c2":\n        self = pathlib.Path(sys.argv[1])\n    return original(self, *args, **kwargs)\npathlib.Path.mkdir = mkdir\nscript, scratch = sys.argv[2], sys.argv[1]\nsys.argv = [script, "--lane", ".", "--rev", "fda63968"]\nrunpy.run_path(script, run_name="__main__")\n''')
jobs = [
    ([sys.executable, str(wrapper), str(SCRATCH / 'before'), 'plans/round76_c2_defect_discharge.py'], 'before'),
    ([sys.executable, 'plans/round75_c1_index_parity.py', '--selftest', '--work', str(SCRATCH / 'c1')], 'r75-c1-selftest'),
    ([sys.executable, 'plans/round75_c2_registry_audit.py', '--selftest', '--work', str(SCRATCH / 'c2')], 'r75-c2-selftest'),
]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for text in pool.map(lambda job: command(*job), jobs):
        print(text)

lines = []
for rev in (BASE, 'worktree'):
    raw = (LANE / 'corpus/evidence/round75/c1-after.txt').read_text() if rev == 'worktree' else git('show', f'{rev}:corpus/evidence/round75/c1-after.txt')
    stamp = next(line for line in raw.splitlines() if line.startswith('LANE_TIP '))
    lines.append(f'STAMP {rev} {stamp}')
    sha = stamp.split()[1]
    lines.append(f'STAMP-RESOLVES {git("rev-parse", "--verify", sha + "^{commit}").strip()}')

readme = git('show', '43255758:corpus/README.md')
# Scan comments without reusing the gate's regex or any of its parser functions.
while '<!--' in readme:
    begin = readme.index('<!--')
    end = readme.find('-->', begin + 4)
    readme = readme[:begin] + (readme[end + 3:] if end >= 0 else '')
visible, fenced, marker = [], False, ''
for line in readme.splitlines():
    stripped = line.lstrip()
    if not fenced and (stripped.startswith('```') or stripped.startswith('~~~')):
        fenced, marker = True, stripped[:3]
    elif fenced and stripped.startswith(marker):
        fenced = False
    elif not fenced:
        visible.append(line)
indexed = {'knowledge': set(), 'lessons': set()}
for line in visible:
    if not line.startswith('|'):
        continue
    cells, current = [], ''
    for i, ch in enumerate(line):
        if ch == '|' and (i == 0 or line[i - 1] != '\\'):
            cells.append(current.strip())
            current = ''
        else:
            current += ch
    cells = cells[1:]
    if len(cells) < 2 or not all(cells):
        continue
    first = cells[0]
    if first.startswith('`') and first.endswith('`'):
        kind, sep, name = first[1:-1].partition('/')
        if sep and kind in indexed:
            indexed[kind].add(name)
tree = git('ls-tree', '-r', '--name-only', '43255758', 'corpus').splitlines()
missing = {}
for kind in indexed:
    disk = {p.split('/')[-1] for p in tree if p.startswith('corpus/' + kind + '/') and p.count('/') == 2 and p.endswith('.md')}
    missing[kind] = sorted(disk - indexed[kind])
    lines.append(f'INDEX {kind} disk={len(disk)} indexed={len(indexed[kind])} missing={len(missing[kind])}')
evidence_dirs = {p.split('/')[2] for p in tree if p.startswith('corpus/evidence/') and p.count('/') >= 3}
mentioned = set(re.findall(r'corpus/evidence/([A-Za-z0-9_.-]+)/', '\n'.join(visible)))
missing['evidence'] = sorted(evidence_dirs - mentioned)
lines.append(f'INDEX evidence disk={len(evidence_dirs)} indexed={len(mentioned)} missing={len(missing["evidence"])}')
counts = [len(missing[k]) for k in ('knowledge', 'lessons', 'evidence')]
lines.append(f'FINAL-RULE total={sum(counts)} split={"/".join(map(str, counts))} revision=43255758')
(OUT / 'missing-paths.json').write_text(json.dumps(missing, indent=2) + '\n')
for rev in (BASE, 'worktree'):
    lesson = (LANE / 'corpus/lessons/round-75-verifier-spotcheck.md').read_text() if rev == 'worktree' else git('show', f'{rev}:corpus/lessons/round-75-verifier-spotcheck.md')
    ids = sorted(set(re.findall(r'R75-D[0-9]+', lesson)))
    lines.append(f'IDS {rev} ' + ','.join(ids))
    ledger = (LANE / 'corpus/routed-findings.jsonl').read_text() if rev == 'worktree' else git('show', f'{rev}:corpus/routed-findings.jsonl')
    rows = [json.loads(line) for line in ledger.splitlines() if line.strip()]
    found = [row['id'] for row in rows if row.get('id') in ids]
    lines.append(f'LEDGER-INDEPENDENT {rev} matching={len(found)} ids={found}')
for name in ('round76_c2_defect_discharge.py', 'round75_c1_index_parity.py', 'round75_c2_registry_audit.py'):
    lines.append(f'SCRIPT-SHA256 {name} {hashlib.sha256((LANE / "plans" / name).read_bytes()).hexdigest()}')
text = '\n'.join(lines) + '\n'
(OUT / 'independent.txt').write_text(text)
print(text)
