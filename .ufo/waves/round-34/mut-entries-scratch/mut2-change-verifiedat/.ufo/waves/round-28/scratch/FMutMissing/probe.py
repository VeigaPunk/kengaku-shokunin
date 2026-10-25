#!/usr/bin/env python3
"""Owned finite CLI mutation evidence; never writes production or mutates the checker."""
import concurrent.futures
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
BASE = Path(__file__).resolve().parent
WORK = BASE / 'plans/registry_check.py'
ORIGINAL = BASE / 'original/registry_check.py'
FIXTURE = BASE / 'hand-fixture'
POPULATION = 'plans/fixtures/r28/registry/population.json'
PIN = '1a5073fc68e698c3b2849fe1bc732d23271c4585d1f05443e38924137e813014'
SCRIPT_PIN = '41561dfb63a7761efc5c89128ccebbd741718ba9675d59a7f9191130aaba79a4'
GUARDS = ['plans/registry_check.py', POPULATION, 'corpus/SOURCES.md', '.ufo/waves/round-28/drafts/webarena-task-spec-audit.md']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode())


def put_json(path, data):
    put(path, json.dumps(data, indent=2, sort_keys=True) + '\n')


def fixture_hashes():
    return {str(path.relative_to(FIXTURE)): digest(path.read_bytes())
            for path in sorted(FIXTURE.rglob('*')) if path.is_file()}


def production_hashes():
    return {relative: digest((LANE / relative).read_bytes()) for relative in GUARDS}


def initialize():
    if WORK.exists() or FIXTURE.exists():
        raise RuntimeError('Initialization refuses to overwrite existing probe inputs')
    script = (LANE / 'plans/registry_check.py').read_bytes()
    population_bytes = (LANE / POPULATION).read_bytes()
    assert digest(script) == SCRIPT_PIN
    assert digest(population_bytes) == PIN
    put(WORK, script)
    put(ORIGINAL, script)
    put(FIXTURE / POPULATION, population_bytes)
    population = json.loads(population_bytes)
    assert 'S060' in population['source_ids']
    for relative in population['knowledge_paths']:
        put(FIXTURE / relative, 'Hand-authored reference-free control.\n')
    rows = ['## Registry\n', '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n', '|---|---|---|---|---|---|---|---|---|---|---|\n']
    for sid in population['source_ids']:
        if sid != 'S060':
            rows.append(f'| {sid} | hand fixture | paper | A | missing-row control | fixture | no source support claimed | queued | 2026-10-21 | 90d | — |\n')
    put(FIXTURE / 'corpus/SOURCES.md', ''.join(rows))
    receipt = {
        'axes': ['legacy novelty -> canonical coverage/constructs (7, held)', 'calibration (8, held)'],
        'python_version': sys.version,
        'production_before': production_hashes(),
        'original_sha256': digest(script),
        'population_sha256': digest(population_bytes),
        'fixture': {'source_ids': population['source_ids'], 'source_rows_present': 12, 'missing_source': 'S060', 'knowledge_files_present': len(population['knowledge_paths']), 'literal_references': 0, 'hand_authored': True, 'expected_exit': 1, 'expected_findings': [{'id': 'source_missing', 'source': 'S060'}]},
        'fixture_hashes': fixture_hashes(),
    }
    put_json(BASE / 'initial.json', receipt)
    print(json.dumps({key: value for key, value in receipt.items() if key != 'fixture_hashes'}, indent=2, sort_keys=True))


def run_one(phase, name):
    temporary = BASE / 'temporary' / phase / name
    temporary.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    environment['TMPDIR'] = str(temporary)
    environment.pop('PYTHONOPTIMIZE', None)
    arguments = ['--selftest'] if name == 'selftest' else ['--root', str(FIXTURE), '--json']
    command = [sys.executable, '-B', str(WORK), *arguments]
    result = {'command': command, 'timeout_seconds': 20, 'bytecode_disabled': True}
    try:
        completed = subprocess.run(command, cwd=BASE, env=environment, capture_output=True, timeout=20)
        stdout, stderr = completed.stdout, completed.stderr
        result.update(exit=completed.returncode, setup_error=None)
    except (OSError, subprocess.TimeoutExpired) as error:
        stdout, stderr = getattr(error, 'stdout', b'') or b'', getattr(error, 'stderr', b'') or b''
        result.update(exit=None, setup_error=repr(error))
    suffix = 'json' if name == 'witness' else 'txt'
    put(BASE / f'{phase}.{name}.stdout.{suffix}', stdout)
    put(BASE / f'{phase}.{name}.stderr.txt', stderr)
    result['stdout'] = stdout.decode(errors='replace')
    result['stderr'] = stderr.decode(errors='replace')
    if name == 'witness' and result['setup_error'] is None:
        try:
            parsed = json.loads(stdout)
            result.update(findings=parsed.get('findings'), source_rows_checked=parsed.get('source_rows_checked'), sources_reported=[row['source'] for row in parsed.get('sources', [])])
            result['expected_detector_matches'] = result['exit'] == 1 and result['findings'] == [{'id': 'source_missing', 'source': 'S060'}]
        except (ValueError, KeyError, TypeError) as error:
            result['setup_error'] = repr(error)
    return result


def run_phase(phase):
    initial = json.loads((BASE / 'initial.json').read_text())
    assert fixture_hashes() == initial['fixture_hashes']
    before = digest(WORK.read_bytes())
    if phase == 'mutated':
        put(BASE / 'registry_check.mutant.py', WORK.read_bytes())
        put(BASE / 'mutation.diff', ''.join(difflib.unified_diff(ORIGINAL.read_text().splitlines(keepends=True), WORK.read_text().splitlines(keepends=True), fromfile='pristine/plans/registry_check.py', tofile='mutated/plans/registry_check.py')))
        selftest = run_one(phase, 'selftest')
        outputs = {'selftest': selftest}
        if selftest['exit'] == 0 and selftest['setup_error'] is None:
            outputs['witness'] = run_one(phase, 'witness')
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            names = ['selftest', 'witness']
            outputs = dict(zip(names, pool.map(lambda name: run_one(phase, name), names)))
    receipt = {'phase': phase, 'script_sha256_before': before, 'script_sha256_after': digest(WORK.read_bytes()), 'fixture_unchanged': fixture_hashes() == initial['fixture_hashes'], 'outputs': outputs}
    put_json(BASE / f'{phase}.receipt.json', receipt)
    summary = {name: {key: value for key, value in output.items() if key not in ('stdout', 'stderr')} for name, output in outputs.items()}
    print(json.dumps({'phase': phase, 'script_sha256': before, 'outputs': summary}, indent=2, sort_keys=True))
    if phase == 'restored':
        restored = {'scratch_sha256': digest(WORK.read_bytes()), 'original_sha256': digest(ORIGINAL.read_bytes()), 'exact_byte_restoration': WORK.read_bytes() == ORIGINAL.read_bytes(), 'production_before': initial['production_before'], 'production_after': production_hashes(), 'fixture_unchanged': receipt['fixture_unchanged']}
        restored['guarded_production_unchanged'] = restored['production_before'] == restored['production_after']
        put_json(BASE / 'restoration.json', restored)
        print(json.dumps(restored, indent=2, sort_keys=True))


if __name__ == '__main__':
    phase = sys.argv[1]
    if phase == 'init':
        initialize()
    elif phase in {'pristine', 'mutated', 'restored'}:
        run_phase(phase)
    else:
        raise SystemExit('Allowed phases: init, pristine, mutated, restored')
