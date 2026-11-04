#!/usr/bin/env python3
"""Harmless source-boundary capture; not an R83 counter or grader verdict."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
ROOT = Path('/fast/scratch/hyaku/kengaku-r83/SentinelR83')
OUT = LANE / '.ufo/waves/round-83/w1/SentinelR83'
os.environ['TMPDIR'] = str(ROOT)
lines = ['AXES coverage; calibration', 'MODE read-only source inspection plus harmless sandbox smoke; NOT R83 validation']

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, LANE / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

for seat, files in [('ReplayR83', ['round83_code_image_probe.py']), ('CounterR83', ['round83_c1_replay.py']), ('DebtR83', ['round83_c2_debt.py', 'round83_c2_checks.py'])]:
    for filename in files:
        path = LANE / '.ufo/waves/round-83/w1' / seat / filename
        lines.append(f'DRAFT {seat}/{filename} present={path.is_file()}')
subject = 'corpus/evidence/round52/graders/code-from-image/tests/test_outputs.py'
for rev in ['614f00559c75155ec100e945b3e8257b14fb7496', '6f076679931367d540c3897a4eafa0eca752e1d4']:
    p = subprocess.run(['git', '-C', str(LANE), 'show', rev + ':' + subject], capture_output=True)
    lines.append(f'IMMUTABLE-SUBJECT rev={rev} rc={p.returncode} sha256={hashlib.sha256(p.stdout).hexdigest()} bytes={len(p.stdout)}')

# Capture argv/cwd only: the runner is replaced and launches no process.
old = load('prior_replay', 'plans/round80_c1_located_replay.py')
seen = []
original = subprocess.run
def capture(argv, **kwargs):
    seen.append({'argv': argv, 'cwd': kwargs.get('cwd'), 'timeout': kwargs.get('timeout')})
    return subprocess.CompletedProcess(argv, 0, stdout='SAFE-CAPTURE\n', stderr='')
try:
    subprocess.run = capture
    tree = old.Tree(LANE, 'historical-fixture', 'historical-fixture', lambda p: True, lambda p: b'HISTORICAL')
    old.run_probe(tree, 'safe', {'tool': 'plans/fixture_probe.py', 'argv': []}, sys.executable, ROOT)
finally:
    subprocess.run = original
lines.append('PRIOR-REV-EXECUTION-CAPTURE ' + json.dumps(seen, sort_keys=True))
lines.append('PATH-ARITHMETIC absolute=' + str(ROOT / '/app/output.txt') + ' parent=' + str((ROOT / '../outside').resolve()))

# Execute only a fixed harmless harness using the prior sandbox argv builder.
prior = load('prior_sandbox', 'plans/round81_log_summary_probe.py')
work = ROOT / 'sandbox'
(work / 'app').mkdir(parents=True, exist_ok=True)
(work / 'app/output.txt').write_text('sentinel-sandbox-only\n')
(work / 'harness.py').write_text('from pathlib import Path\nimport os\nprint("SANDBOX cwd=" + os.getcwd())\nprint("SANDBOX output=" + Path("/app/output.txt").read_text().strip())\nprint("SANDBOX host_home_visible=" + str(Path("/home/vgpnk").exists()))\nprint("SANDBOX sentinel_env=" + str(os.environ.get("SENTINEL_SECRET")))\n')
env = {'PATH': prior.PATH, 'HOME': '/tmp', 'LANG': 'C.UTF-8', 'PYTHONDONTWRITEBYTECODE': '1'}
argv = prior.sandbox_argv(LANE / subject, work) + ['/usr/bin/python3', '-B', '/harness.py']
lines.append('HARMLESS-SANDBOX-ARGV ' + json.dumps(argv))
try:
    p = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=20)
    lines.append(f'HARMLESS-SANDBOX rc={p.returncode}')
    lines.extend(p.stdout.splitlines())
    lines.extend('STDERR ' + line for line in p.stderr.splitlines())
except (OSError, subprocess.TimeoutExpired) as exc:
    lines.append('HARMLESS-SANDBOX setup=' + type(exc).__name__ + ':' + str(exc))
text = '\n'.join(lines) + '\n'
(OUT / 'capture.txt').write_text(text)
print(text, end='')
