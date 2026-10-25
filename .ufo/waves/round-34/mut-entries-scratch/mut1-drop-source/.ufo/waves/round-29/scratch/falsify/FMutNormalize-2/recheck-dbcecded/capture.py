#!/usr/bin/env python3
"""Capture the one assigned normalization re-check and the requested official witness."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
ROOT = Path('/tmp/r29-FMutNormalize-dbcecded.66jCWc')
OUT = LANE / '.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/recheck-dbcecded'
REPORT = LANE / '.ufo/waves/round-29/falsify/FMutNormalize.md'
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
    'plans/fixtures/r29/mutation_witness.py',
)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def snapshot():
    return {label: {path: digest((base / path).read_bytes()) for path in RELATIVES}
            for label, base in (('lane', LANE), ('copy', ROOT))}

def capture(name, command):
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=240)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
        timed_out = False
    except subprocess.TimeoutExpired as error:
        code, stdout, stderr = None, error.stdout or b'', error.stderr or b''
        timed_out = True
    stdout_path = OUT / (name + '.stdout.txt')
    stderr_path = OUT / (name + '.stderr.txt')
    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)
    result = {'command': command, 'cwd': str(ROOT), 'timeout_seconds': 240,
              'timed_out': timed_out, 'exit_code': code,
              'stdout_path': str(stdout_path), 'stderr_path': str(stderr_path),
              'stdout_bytes': len(stdout), 'stderr_bytes': len(stderr),
              'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr)}
    (OUT / (name + '.receipt.json')).write_text(json.dumps(result, indent=2) + '\n')
    return result

phase = sys.argv[1]
if phase not in {'pristine', 'mutated', 'restored', 'witness'}:
    raise SystemExit('invalid phase')
if phase == 'witness':
    before = snapshot()['lane']
    result = capture('official-witness', [sys.executable, '-B', str(LANE / 'plans/fixtures/r29/mutation_witness.py')])
    result['lane_hashes_before'] = before
    result['lane_hashes_after'] = snapshot()['lane']
    (OUT / 'official-witness.receipt.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    print(Path(result['stdout_path']).read_text(), end='')
    print(Path(result['stderr_path']).read_text(), end='')
else:
    if phase == 'pristine':
        prior = REPORT.read_bytes()
        metadata = {'path': str(REPORT), 'bytes': len(prior), 'sha256': digest(prior)}
        (OUT / 'prior-report-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    before = snapshot()
    def run(mode):
        command = [sys.executable, '-B', str(ROOT / 'plans/config_projection.py'), '--root', str(ROOT), '--' + mode]
        return mode, capture(phase + '.' + mode, command)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        modes = dict(pool.map(run, ('selftest', 'summary')))
    namespace = runpy.run_path(str(ROOT / 'plans/config_projection.py'))
    values = {name: 'http://%s.invalid:1' % name.lower().replace('_', '-') for name in namespace['ORDER']}
    values['GITLAB'] += '/'
    raw = '[{"start_url": "__GITLAB__/a", "eval": {"program_html": [{"required_contents": {"must_include": ["__GITLAB__/b"]}}]}}]'
    diagnostic, findings = namespace['audit_text'](raw, {'distinct_origins': {'purpose': 'hand', 'values': values}})
    task = diagnostic['profiles']['distinct_origins']['tasks'][0]['projected_task']
    observed = {
        'case_source_lines': 'plans/config_projection.py:531-536',
        'findings': findings,
        'values': {
            '/0/start_url': {'expected': 'http://gitlab.invalid:1//a', 'observed': task['start_url']},
            '/0/eval/program_html/0/required_contents/must_include/0': {
                'expected': 'http://gitlab.invalid:1//b',
                'observed': task['eval']['program_html'][0]['required_contents']['must_include'][0]},
        },
    }
    result = {'phase': phase, 'before': before, 'after': snapshot(), 'modes': modes, 'slash_case': observed}
    (OUT / (phase + '.capture.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    for mode, data in modes.items():
        print('OUTPUT', phase, mode)
        stdout = Path(data['stdout_path']).read_text()
        if mode == 'summary':
            print('\n'.join(line for line in stdout.splitlines() if line.startswith('TOTAL ') or 'projected_text_sha256=' in line))
        else:
            print(stdout, end='')
        print(Path(data['stderr_path']).read_text(), end='')
