#!/usr/bin/env python3
"""Actual measured-byte Q60 controls; never mutates the origin checkout."""
import argparse
import io
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument('--origin', type=Path, required=True)
ap.add_argument('--rev', required=True)
ap.add_argument('--work', type=Path, required=True)
a = ap.parse_args()
a.work.mkdir(parents=True, exist_ok=True)
root = Path(tempfile.mkdtemp(dir=a.work, prefix='q60-'))
try:
    raw = subprocess.run(['git', '-C', str(a.origin), 'archive', a.rev], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        archive.extractall(root, filter='data')
    env = dict(os.environ, TMPDIR=str(a.work), PYTHONDONTWRITEBYTECODE='1', R83_ORIGIN_REPO=str(a.origin))
    failures = 0
    for name, path, check in [('count', 'corpus/SOURCES.md', 'v1'), ('gate', 'corpus/lessons/round-83.md', 'v6')]:
        target = root / path
        before = target.read_bytes()
        text = before.decode()
        if name == 'count':
            mutated = '\n'.join(line.replace('(4 words', '(6 words') if line.startswith('| S268 |') else line for line in text.split('\n'))
        else:
            mutated = '\n'.join(line for line in text.split('\n') if not line.startswith('| S266 Gate correction'))
        for state, payload, want in [('pristine', before, 0), ('mutated', mutated.encode(), 1), ('restored', before, 0)]:
            target.write_bytes(payload)
            cmd = ['python3', str(a.origin / 'plans/round83_c2_checks.py'), check]
            run = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True)
            print('CONTROL', name, state, 'exit='+str(run.returncode), run.stdout.strip())
            failures += run.returncode != want or ('CHECK '+check+' '+('ok' if want == 0 else 'fail')) not in run.stdout
    print('Q60 controls=2 failures='+str(failures))
    raise SystemExit(bool(failures))
finally:
    shutil.rmtree(root)
