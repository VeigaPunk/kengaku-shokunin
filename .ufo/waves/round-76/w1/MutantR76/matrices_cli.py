#!/usr/bin/env python3
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
S = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/MutantR76'
L = S / 'lane'
P = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
O = P / '.ufo/waves/round-76/w1/MutantR76'
os.chdir(S)
for name in ['c1_surface_resolver', 'c2_defect_discharge']:
    spec = importlib.util.spec_from_file_location(name, L / f'plans/round76_{name}.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    original = m.git
    def frozen_git(repo, *args, original=original):
        if repo == L:
            repo = P
            args = tuple('42fad4827797e540c60a00821d3f2f5c18539632^{commit}' if a in ('master^{commit}', 'HEAD^{commit}') else a for a in args)
        return original(repo, *args)
    m.git = frozen_git
    if name.startswith('c2'):
        f = m.fixture_legs
        f.__code__ = f.__code__.replace(co_consts=tuple(str(S / 'nested') if x == '/fast/scratch/hyaku/kengaku-r76/c2/_fixture' else x for x in f.__code__.co_consts))
    sys.argv = [str(L / f'plans/round76_{name}.py'), '--lane', str(L), '--mutants', '--work', str(S / name)]
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        rc = m.main()
    text = 'ARGV ' + repr(sys.argv) + '\n' + output.getvalue() + f'EXIT {rc}\n'
    (O / (name[:2].upper() + '-cli-matrix.txt')).write_text(text)
    print(text, flush=True)
    if rc:
        sys.exit(rc)
