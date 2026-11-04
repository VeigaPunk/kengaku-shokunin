#!/usr/bin/env python3
"""Isolated freeze mutation probes; no production writes or git mutations."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil

S = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/MutantR76'
L = S / 'lane'
OUT = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-76/w1/MutantR76')
os.chdir(S)

def load(name):
    path = L / f'plans/round76_{name}.py'
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

c1 = load('c1_surface_resolver')
c2 = load('c2_defect_discharge')
# The shipped C2 fixture helper ignores --work for one nested destination.
# Redirect ONLY that string constant in memory to this seat's isolated scratch.
f = c2.fixture_legs
f.__code__ = f.__code__.replace(co_consts=tuple(str(S / 'nested') if x == '/fast/scratch/hyaku/kengaku-r76/c2/_fixture' else x for x in f.__code__.co_consts))
f = c2.emit
f.__code__ = f.__code__.replace(co_consts=tuple(str(S / 'new-c2-work') if x == '/fast/scratch/hyaku/kengaku-r76/c2' else x for x in f.__code__.co_consts))
tip = '42fad4827797e540c60a00821d3f2f5c18539632'
# The live master advanced during the first clone attempt. Pin history reads
# to freeze while borrowing only the production object database read-only.
original_git = c2.git
def frozen_git(repo, *args):
    if repo == L:
        args = tuple(tip + '^{commit}' if arg == 'master^{commit}' else arg for arg in args)
        repo = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
    return original_git(repo, *args)
c2.git = frozen_git

def capture(fn):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = fn()
    return {'rc': rc, 'stdout': buf.getvalue()}

results = {'freeze': tip, 'matrices': {}, 'probes': []}
for gate, mod, fn in [('C1', c1, lambda: c1.mutants(S / 'matrix-c1')), ('C2', c2, lambda: c2.mutants(S / 'matrix-c2', tip))]:
    if os.environ.get('C2_ONLY'):
        continue
    result = capture(fn)
    results['matrices'][gate] = result
    (OUT / f'{gate}-matrix.txt').write_text(result['stdout'] + f"EXIT {result['rc']}\n")
    print(gate, result['stdout'], 'EXIT', result['rc'], flush=True)

def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}

def digest(files):
    h = hashlib.sha256()
    for name, data in sorted(files.items()):
        h.update(name.encode() + b'\0' + data + b'\0')
    return h.hexdigest()

def probe(gate, name, root, rel, transform, detector, expected):
    if gate == 'C1' and os.environ.get('C2_ONLY'):
        return
    pristine = snapshot(root)
    before = capture(detector)
    target = root / rel
    original = target.read_bytes()
    changed = transform(original.decode()).encode()
    assert original != changed
    try:
        target.write_bytes(changed)
        mutant_bytes = snapshot(root)
        mutated = capture(detector)
        dest = OUT / 'fixtures' / name
        for path, data in mutant_bytes.items():
            p = dest / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
    finally:
        target.write_bytes(original)
    restored = capture(detector)
    after = snapshot(root)
    verdict = 'inconclusive' if before['rc'] != 0 or restored['rc'] != 0 else ('killed' if mutated['rc'] != 0 else 'survived')
    result = dict(gate=gate, name=name, expected=expected, changed_path=rel, original=original.decode(), mutated_bytes=changed.decode(), before=before, mutated=mutated, restored=restored, verdict=verdict, before_hash=digest(pristine), mutant_hash=digest(mutant_bytes), restored_hash=digest(after), exact_restoration=pristine == after)
    results['probes'].append(result)
    (OUT / f'{name}.txt').write_text(json.dumps(result, indent=2) + '\n')
    print(name, verdict, 'rcs', before['rc'], mutated['rc'], restored['rc'], 'restored', pristine == after, flush=True)

with c1.Listener() as live:
    root = S / 'c1-fixture'
    c1.build_fixture(root, live_port=live.port)
    detector = lambda: c1.emit(root, 'worktree', None)
    probe('C1', 'C1-new-delete-absent', root, 'PROVINCE.md', lambda s: '\n'.join(x for x in s.split('\n') if not x.startswith('| Absent path |')), detector, 'Scope shrink must not reach fixed target total=11; census may still pass declared rows')
    probe('C1', 'C1-new-duplicate-present', root, 'PROVINCE.md', lambda s: s.replace('| Present path |', '| Present path |', 1).replace('| Absent path |', '| Duplicate path | `present.md` | fixture |\n| Absent path |'), detector, 'Duplicate row should not falsely count a distinct surface')
    probe('C1', 'C1-new-stale-third-cell', root, 'PROVINCE.md', lambda s: s.replace('never resolved | fixture |', 'never resolved | is alive |'), detector, 'STALE-TEXT on absent row with present-tense prose in trailing cell')
    probe('C1', 'C1-new-reanchor-present', root, 'PROVINCE.md', lambda s: s.replace('~/r76-definitely-absent-path', 'present.md'), detector, 'STALE-ABSENT')

root = S / 'c2-fixture'
c2.build_fixture(root, tip)
detector = lambda: c2.emit(root, 'worktree', None, probe=L)
probe('C2', 'C2-new-comment-d2', root, 'SCORECARD.md', lambda s: '\n'.join('<!-- ' + line + ' -->' if 'R75-D2' in line else line for line in s.split('\n')), detector, 'D2 must require a visible correction, not HTML-comment-only values')
probe('C2', 'C2-new-zero-scope', root, 'corpus/lessons/round-75-verifier-spotcheck.md', lambda s: '# fixture closure\n\n## 6. Routed defects\n\nNo routed defects.\n', detector, 'Frozen scope R75-D1 through R75-D7 must not disappear')
def missing_check(s):
    rows = [json.loads(line) for line in s.splitlines() if line]
    rows[4]['check'] = "grep -q 'R75-D5' corpus/does-not-exist.md"
    return '\n'.join(json.dumps(row) for row in rows) + '\n'
probe('C2', 'C2-new-nonexistent-check-path', root, 'corpus/routed-findings.jsonl', missing_check, detector, 'CHECK-TRIVIAL for no committed path (only nonexistent path + literal)')
probe('C2', 'C2-new-remove-d3-values', root, 'SCORECARD.md', lambda s: s.replace('60 (4/36/20)', 'incorrect values'), detector, 'LEG-FAIL D3')
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
