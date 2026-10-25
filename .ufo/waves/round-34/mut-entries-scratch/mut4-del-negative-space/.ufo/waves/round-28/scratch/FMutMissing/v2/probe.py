#!/usr/bin/env python3
"""Same-identity replay using the owned v1 recorder, with all v1 bytes preserved."""
import concurrent.futures
import difflib
import importlib.util
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('owned_fmutmissing_recorder', BASE.parent / 'probe.py')
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)
recorder.BASE = BASE
recorder.WORK = BASE / 'plans/registry_check.py'
recorder.ORIGINAL = BASE / 'original/registry_check.py'
recorder.FIXTURE = BASE / 'hand-fixture'
recorder.SCRIPT_PIN = 'fc388c332d4e37f8f0f7118d15a0baed8d86cd99b345ab9255e2b9dc6bd7379b'


def v1_hashes():
    return {str(path.relative_to(BASE.parent)): recorder.digest(path.read_bytes())
            for path in sorted(BASE.parent.rglob('*'))
            if path.is_file() and path.relative_to(BASE.parent).parts[0] != 'v2'}


def initialize():
    recorder.initialize()
    original_fixture = json.loads((BASE.parent / 'initial.json').read_text())['fixture_hashes']
    assert recorder.fixture_hashes() == original_fixture
    recorder.put_json(BASE / 'v1-preservation-before.json', v1_hashes())


def run_phase(phase):
    initial = json.loads((BASE / 'initial.json').read_text())
    assert recorder.fixture_hashes() == initial['fixture_hashes']
    before = recorder.digest(recorder.WORK.read_bytes())
    if phase == 'mutated':
        recorder.put(BASE / 'registry_check.mutant.py', recorder.WORK.read_bytes())
        recorder.put(BASE / 'mutation.diff', ''.join(difflib.unified_diff(recorder.ORIGINAL.read_text().splitlines(keepends=True), recorder.WORK.read_text().splitlines(keepends=True), fromfile='pristine/plans/registry_check.py', tofile='mutated/plans/registry_check.py')))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        names = ['selftest', 'witness']
        outputs = dict(zip(names, pool.map(lambda name: recorder.run_one(phase, name), names)))
    selftest = outputs['selftest']
    assertion = "AssertionError: ('uncited_source_missing', set(), ['source_missing'])"
    selftest['expected_detector_matches'] = (
        selftest['setup_error'] is None
        and ((selftest['exit'] == 1 and assertion in selftest['stderr']) if phase == 'mutated'
             else (selftest['exit'] == 0 and selftest['stdout'].startswith('SELFTEST clean cases=15 '))))
    receipt = {'phase': phase, 'script_sha256_before': before, 'script_sha256_after': recorder.digest(recorder.WORK.read_bytes()), 'fixture_unchanged': recorder.fixture_hashes() == initial['fixture_hashes'], 'outputs': outputs}
    recorder.put_json(BASE / f'{phase}.receipt.json', receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    if phase == 'restored':
        v1_before = json.loads((BASE / 'v1-preservation-before.json').read_text())
        v1_after = v1_hashes()
        restored = {'scratch_sha256': recorder.digest(recorder.WORK.read_bytes()), 'original_sha256': recorder.digest(recorder.ORIGINAL.read_bytes()), 'exact_byte_restoration': recorder.WORK.read_bytes() == recorder.ORIGINAL.read_bytes(), 'production_before': initial['production_before'], 'production_after': recorder.production_hashes(), 'fixture_unchanged': receipt['fixture_unchanged'], 'fixture_identical_to_v1': recorder.fixture_hashes() == json.loads((BASE.parent / 'initial.json').read_text())['fixture_hashes'], 'v1_evidence_unchanged': v1_before == v1_after}
        restored['guarded_production_unchanged'] = restored['production_before'] == restored['production_after']
        recorder.put_json(BASE / 'v1-preservation-after.json', v1_after)
        recorder.put_json(BASE / 'restoration.json', restored)
        print(json.dumps(restored, indent=2, sort_keys=True))


if __name__ == '__main__':
    phase = sys.argv[1]
    if phase == 'init':
        initialize()
    elif phase in {'pristine', 'mutated', 'restored'}:
        run_phase(phase)
    else:
        raise SystemExit('Allowed phases: init, pristine, mutated, restored')
