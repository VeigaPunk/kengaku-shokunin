#!/usr/bin/env python3
"""Capture one phase of the assigned trailing-slash mutation probe; never edit source."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
ROOT = Path('/tmp/r29-FMutNormalize-2.9YapCw')
OUT = LANE / '.ufo/waves/round-29/scratch/falsify/FMutNormalize-2'
RELATIVES = (
    'plans/config_projection.py',
    'plans/fixtures/r29/manifest.json',
    'plans/fixtures/r29/generate_test_data.py',
    'plans/fixtures/r29/profiles.json',
    'plans/fixtures/r28/webarena/config_files/test.raw.json',
    'plans/fixtures/r29/hand/cascade-order.case.json',
    'plans/fixtures/r29/hand/url-only.fixture.json',
    'plans/fixtures/r29/hand/url-only.expected.json',
    'plans/fixtures/r29/hand/index-shuffled-ids.fixture.json',
)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def snapshots():
    return {
        label: {rel: digest((base / rel).read_bytes()) for rel in RELATIVES}
        for label, base in (('lane', LANE), ('copy', ROOT))
    }

def run_mode(mode):
    command = [sys.executable, '-B', str(ROOT / 'plans/config_projection.py'),
               '--root', str(ROOT), '--' + mode]
    try:
        result = subprocess.run(command, capture_output=True, timeout=120, cwd=ROOT)
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
        timeout = False
    except subprocess.TimeoutExpired as error:
        stdout, stderr, code = error.stdout or b'', error.stderr or b'', None
        timeout = True
    stem = OUT / (sys.argv[1] + '.' + mode)
    stem.with_suffix(stem.suffix + '.stdout.txt').write_bytes(stdout)
    stem.with_suffix(stem.suffix + '.stderr.txt').write_bytes(stderr)
    return mode, {
        'command': command, 'cwd': str(ROOT), 'timeout_seconds': 120,
        'timed_out': timeout, 'exit_code': code,
        'stdout_bytes': len(stdout), 'stdout_sha256': digest(stdout),
        'stderr_bytes': len(stderr), 'stderr_sha256': digest(stderr),
        'stdout_path': str(stem.with_suffix(stem.suffix + '.stdout.txt')),
        'stderr_path': str(stem.with_suffix(stem.suffix + '.stderr.txt')),
    }

phase = sys.argv[1]
if phase not in {'pristine', 'mutated', 'restored'}:
    raise SystemExit('phase must be pristine, mutated, or restored')
before = snapshots()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    modes = dict(pool.map(run_mode, ('selftest', 'summary', 'json')))
record = {'phase': phase, 'before': before, 'after': snapshots(), 'modes': modes}
(OUT / (phase + '.capture.json')).write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
for mode in ('selftest', 'summary'):
    content = Path(modes[mode]['stdout_path']).read_text()
    print('OUTPUT', phase, mode)
    if mode == 'summary':
        print('\n'.join(line for line in content.splitlines()
                        if line.startswith(('POPULATION ', 'TOTAL '))
                        or 'projected_text_sha256=' in line))
    else:
        print(content, end='')
    error = Path(modes[mode]['stderr_path']).read_text()
    if error:
        print(error, end='')
