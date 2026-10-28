#!/usr/bin/env python3
"""C1CritTrustBoundary — CONFIRMED-leg falsification harness for R52-C1 (scratch only).

Builds a pristine fixture lane from the frozen population + real pin bytes, then runs the
UNMODIFIED frozen counter against forged confirmations.json variants. Writes nothing outside
this seat's scratch dir.
"""
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
BASE = Path('/fast/scratch/hyaku/kengaku-r52/C1CritTrustBoundary')
UP = BASE / 'upstream'
FX = BASE / 'fx'
RES = BASE / 'results'
GR = 'corpus/evidence/round52/graders'


def sha(b):
    return hashlib.sha256(b).hexdigest()


# ---------- 1. pristine fixture ----------
if FX.exists():
    shutil.rmtree(FX)
(FX / 'plans').mkdir(parents=True)
(FX / 'corpus/evidence/round52/graders').mkdir(parents=True)
(FX / 'corpus/knowledge').mkdir(parents=True)
for name in ('round52_c1_grader_audit.py', 'round52-tasks.json'):
    shutil.copy2(LANE / 'plans' / name, FX / 'plans' / name)
assert sha((FX / 'plans/round52_c1_grader_audit.py').read_bytes()) == \
       sha((LANE / 'plans/round52_c1_grader_audit.py').read_bytes()), 'counter copy drifted'
for p in sorted((LANE / 'corpus/knowledge').glob('tb2-*-grader.md')):
    shutil.copy2(p, FX / 'corpus/knowledge' / p.name)

pop = json.loads((FX / 'plans/round52-tasks.json').read_text())
copied = []
for task, files in pop['capture_population'].items():
    for rel in files:
        src = UP / rel
        assert src.exists(), 'missing upstream: ' + rel
        dst = FX / GR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)
assert len(copied) == pop['capture_file_count'] == 184, len(copied)
sums = ''.join(f"{sha((FX / GR / rel).read_bytes())}  {rel}\n" for rel in sorted(copied))
(FX / GR / 'SHA256SUMS').write_text(sums)
(FX / 'corpus/evidence/round52/prior-art.md').write_text(
    '# Prior art (harness stub; URLs point at the pinned TB2 tree itself)\n'
    '- https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/README.md\n'
    '- https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/adaptive-rejection-sampler/tests/test_outputs.py\n'
    '- https://raw.githubusercontent.com/harbor-framework/terminal-bench-2/2fd12b88aafdd04a52c298e3940bcb189f9766d6/build-pmars/tests/test_outputs.py\n'
)

# ---------- 2. baseline classification via the frozen counter's own code ----------
spec = importlib.util.spec_from_file_location('audit', FX / 'plans/round52_c1_grader_audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
pop2, records, expected, present, mismatched, candidates, sums2 = audit.collect(FX)
read = audit.lane_read_tasks(FX)
print('BASELINE expected', expected, 'present(prior-grader tasks)', present, 'mismatched', mismatched)
classes = {}
for t, r in records.items():
    classes[r.get('class')] = classes.get(r.get('class'), 0) + 1
print('CLASSES', classes)
print('CANDIDATES', len(candidates), 'not-hand-read', len([t for t in candidates if t not in read]))
print('candidates INTERSECT hand-read:', sorted(set(candidates) & read))


def primary_text(t):
    return (FX / GR / records[t]['grader']).read_text(errors='replace')


def real_quote(t):
    """A real, located weakness line: an assert carrying the presence marker."""
    for line in primary_text(t).splitlines():
        if 'assert' in line and audit.PRESENCE.search(line) and line.strip():
            return line.strip() + '\n'
    for line in primary_text(t).splitlines():
        if 'assert' in line and line.strip():
            return line.strip() + '\n'
    raise RuntimeError('no quote for ' + t)


cands_new = [t for t in candidates if t not in read]
assert len(cands_new) >= 2, 'need two fresh candidates for honest pairs'
candA, candB = cands_new[0], cands_new[1]
qa, qb = real_quote(candA), real_quote(candB)
print('candA', candA, '->', repr(qa))
print('candB', candB, '->', repr(qb))

v3 = [t for t, r in sorted(records.items())
      if r.get('class') == 'V3' and t not in read and not r.get('candidate')]
print('V3 non-candidate pool:', len(v3), v3[:6])
noncand = v3[2] if len(v3) > 2 else (v3[0] if v3 else sorted(records)[0])


def run(name, rows, tamper=None, patch_count=None):
    d = BASE / ('fx-' + name)
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(FX, d)
    if tamper:
        for t, body in tamper.items():
            rel = records[t]['grader']
            p = d / GR / rel
            p.write_bytes(body.encode())
            sp = d / GR / 'SHA256SUMS'           # builder regenerates the self-referential pin
            lines = [l for l in sp.read_text().splitlines() if not l.endswith('  ' + rel)]
            lines.append(sha(p.read_bytes()) + '  ' + rel)
            sp.write_text('\n'.join(sorted(lines)) + '\n')
            up = (UP / rel).read_bytes()
            print(f'TAMPER {t}: upstream {sha(up)[:12]} -> fixture {sha(p.read_bytes())[:12]} ({len(up)} -> {p.stat().st_size} bytes)')
    if patch_count is not None:
        pj = d / 'plans/round52-tasks.json'
        pp = json.loads(pj.read_text())
        pp['capture_file_count'] = patch_count
        pj.write_text(json.dumps(pp, indent=1) + '\n')
    (d / 'corpus/evidence/round52/confirmations.json').write_text(json.dumps(rows, indent=1))
    r = subprocess.run([sys.executable, str(d / 'plans/round52_c1_grader_audit.py'),
                        '--lane', str(d)], capture_output=True, text=True)
    out = r.stdout + (r.stderr or '')
    (RES / (name + '.txt')).write_text(out)
    keep = [l for l in out.splitlines()
            if l.startswith(('CONFIRMED', '  REJECTED', 'CAPTURES', 'PREDICATE', 'CANDIDATES'))]
    print('--- ' + name + ' (rc=' + str(r.returncode) + ')')
    print('\n'.join(keep))
    return out


RES.mkdir(exist_ok=True)

# HONEST — two real candidates, real located quotes, two distinct second readers
run('honest', [
    {'task': candA, 'quote': qa, 'reader': 'w1-labrat-alpha', 'confirmed': True},
    {'task': candB, 'quote': qb, 'reader': 'w1-labrat-beta', 'confirmed': True},
])

# X1 — self-dealt confirmations: reader is the round author, same id on both rows
SELF = 'kengaku-r52-l1-author'
run('x1-selfdealt', [
    {'task': candA, 'quote': qa, 'reader': SELF, 'confirmed': True},
    {'task': candB, 'quote': qb, 'reader': SELF, 'confirmed': True},
])

# X1-E2E — same self-dealt rows; capture_file_count patched to the per-task reality (89)
#          to show the full predicate pass the forger would enjoy once leg 1 is repaired.
run('x1-e2e', [
    {'task': candA, 'quote': qa, 'reader': SELF, 'confirmed': True},
    {'task': candB, 'quote': qb, 'reader': SELF, 'confirmed': True},
], patch_count=89)

# X4 — vacuous quote: present in the bytes, evidences nothing
first_a = primary_text(candA).splitlines()[0] + '\n'
run('x4-vacuous-quote', [
    {'task': candA, 'quote': first_a, 'reader': 'whoever', 'confirmed': True},
    {'task': candB, 'quote': qb, 'reader': 'w1-labrat-beta', 'confirmed': True},
])

# X5 — truthiness holes: confirmed="false" (string) and reader=" " (space) both pass
run('x5-truthiness', [
    {'task': candA, 'quote': qa, 'reader': ' ', 'confirmed': 'false'},
    {'task': candB, 'quote': qb, 'reader': 'w1-labrat-beta', 'confirmed': True},
])

# X2 — forged captures: two REAL V3 graders replaced by synthetic presence-only bytes
TAMPER_BODY = ("import os\n\n\ndef test_a():\n    assert os.path.exists('/app/out')\n\n\n"
               "def test_b():\n    assert os.path.exists('/app/out/words.txt')\n")
TQ = "assert os.path.exists('/app/out')"
t1, t2 = v3[0], v3[1]
assert TQ not in (UP / records[t1]['grader']).read_text(errors='replace'), 'quote unexpectedly upstream t1'
assert TQ not in (UP / records[t2]['grader']).read_text(errors='replace'), 'quote unexpectedly upstream t2'
run('x2-forged-capture', [
    {'task': t1, 'quote': TQ, 'reader': SELF, 'confirmed': True},
    {'task': t2, 'quote': TQ, 'reader': SELF, 'confirmed': True},
], tamper={t1: TAMPER_BODY, t2: TAMPER_BODY})

# ---------- negatives ----------
run('n1-quote-absent', [
    {'task': candA, 'quote': 'THIS LINE IS NOT IN THE GRADER 0xdeadbeef',
     'reader': 'w1-labrat-alpha', 'confirmed': True},
    {'task': candB, 'quote': qb, 'reader': 'w1-labrat-beta', 'confirmed': True},
])
run('n2-duplicate-row', [
    {'task': candA, 'quote': qa, 'reader': 'w1-labrat-alpha', 'confirmed': True},
    {'task': candA, 'quote': qa, 'reader': 'w1-labrat-alpha', 'confirmed': True},
])
run('n3-confirmed-false', [
    {'task': candA, 'quote': qa, 'reader': 'w1-labrat-alpha', 'confirmed': False},
    {'task': candB, 'quote': qb, 'reader': 'w1-labrat-beta', 'confirmed': True},
])
run('n4-non-candidate', [
    {'task': noncand, 'quote': qa, 'reader': 'w1-labrat-alpha', 'confirmed': True},
])
hr = sorted(set(candidates) & read)
if hr:
    run('n5-handread-task', [
        {'task': hr[0], 'quote': real_quote(hr[0]), 'reader': 'w1-labrat-alpha', 'confirmed': True},
    ])
else:
    print('N5 skipped: no hand-read task is an instrument candidate')
print('DONE')
