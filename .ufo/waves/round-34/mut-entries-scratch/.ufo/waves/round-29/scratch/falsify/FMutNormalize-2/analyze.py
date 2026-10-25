#!/usr/bin/env python3
"""Analyze the captured single-mutant outputs; never run or edit the instrument."""
import collections
import hashlib
import json
from pathlib import Path

OUT = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2')
ROOT = Path('/tmp/r29-FMutNormalize-2.9YapCw')
PHASES = ('pristine', 'mutated', 'restored')
records = {phase: json.loads((OUT / (phase + '.capture.json')).read_text()) for phase in PHASES}
objects = {phase: json.loads((OUT / (phase + '.json.stdout.txt')).read_text()) for phase in PHASES}

def pointer(path):
    return '/' + '/'.join(str(part).replace('~', '~0').replace('/', '~1') for part in path)

def differences(expected, actual, path=()):
    if type(expected) is not type(actual):
        yield {'json_pointer': pointer(path), 'expected_pristine': expected, 'observed_mutant': actual}
    elif isinstance(expected, dict):
        assert expected.keys() == actual.keys(), path
        for key in expected:
            yield from differences(expected[key], actual[key], path + (key,))
    elif isinstance(expected, list):
        assert len(expected) == len(actual), path
        for index, (left, right) in enumerate(zip(expected, actual)):
            yield from differences(left, right, path + (index,))
    elif expected != actual:
        yield {'json_pointer': pointer(path), 'expected_pristine': expected, 'observed_mutant': actual}

deltas = list(differences(objects['pristine'], objects['mutated']))
for ordinal, delta in enumerate(deltas, 1):
    delta['ordinal'] = ordinal
    parts = delta['json_pointer'].split('/')
    if 'tasks' in parts:
        index = int(parts[parts.index('tasks') + 1])
        profile = parts[2]
        task = objects['pristine']['profiles'][profile]['tasks'][index]
        delta.update(profile=profile, output_index=index, task_id=task['task_id'])
    else:
        delta.update(profile=parts[2])
ledger_bytes = ''.join(json.dumps(delta, sort_keys=True, ensure_ascii=True) + '\n' for delta in deltas).encode()
(OUT / 'all-json-mismatches.jsonl').write_bytes(ledger_bytes)

categories = collections.Counter()
projected = []
for delta in deltas:
    path = delta['json_pointer']
    if '/projected_task/' in path:
        categories['projected_task_string_values'] += 1
        projected.append(delta)
    elif '/changed_leaves/' in path:
        categories['changed_leaf_projected_values'] += 1
    elif path.endswith('/would_be_file_sha256'):
        categories['would_be_file_sha256'] += 1
    elif path.endswith('/projected_text_sha256'):
        categories['projected_text_sha256'] += 1
    else:
        categories['other'] += 1

summary_deltas = []
left_lines = (OUT / 'pristine.summary.stdout.txt').read_text().splitlines()
right_lines = (OUT / 'mutated.summary.stdout.txt').read_text().splitlines()
assert len(left_lines) == len(right_lines)
for line_number, (left, right) in enumerate(zip(left_lines, right_lines), 1):
    if left != right:
        summary_deltas.append({'line': line_number, 'expected_pristine': left, 'observed_mutant': right})
(OUT / 'summary-mismatches.json').write_text(json.dumps(summary_deltas, indent=2) + '\n')

raw = (ROOT / 'plans/fixtures/r28/webarena/config_files/test.raw.json').read_text()
profiles = json.loads((ROOT / 'plans/fixtures/r29/profiles.json').read_text())
order = ('GITLAB', 'REDDIT', 'SHOPPING', 'SHOPPING_ADMIN', 'WIKIPEDIA', 'MAP')
faithful = {}
for name, profile in profiles.items():
    reference = raw
    for token_name in order:
        reference = reference.replace('__' + token_name + '__', profile['values'][token_name])
    expected_tasks = json.loads(reference)
    faithful[name] = {
        'source_text_sha256': hashlib.sha256(reference.encode()).hexdigest(),
        'pristine_objects_equal_literal_replacement': expected_tasks == [task['projected_task'] for task in objects['pristine']['profiles'][name]['tasks']],
        'mutant_objects_equal_literal_replacement': expected_tasks == [task['projected_task'] for task in objects['mutated']['profiles'][name]['tasks']],
        'restored_objects_equal_literal_replacement': expected_tasks == [task['projected_task'] for task in objects['restored']['profiles'][name]['tasks']],
        'mismatching_task_objects': sum(expected != task['projected_task'] for expected, task in zip(expected_tasks, objects['mutated']['profiles'][name]['tasks'])),
    }

pristine_source = records['pristine']['before']['copy']['plans/config_projection.py']
source_hashes = {phase: records[phase]['before']['copy']['plans/config_projection.py'] for phase in PHASES}
restoration = {
    'source_hashes': source_hashes,
    'copy_source_restored_exact_sha256': source_hashes['restored'] == pristine_source,
    'all_recorded_lane_hashes_unchanged': all(record[point]['lane'] == records['pristine']['before']['lane'] for record in records.values() for point in ('before', 'after')),
    'all_recorded_copy_inputs_unchanged': all({key: value for key, value in record[point]['copy'].items() if key != 'plans/config_projection.py'} == {key: value for key, value in records['pristine']['before']['copy'].items() if key != 'plans/config_projection.py'} for record in records.values() for point in ('before', 'after')),
    'source_during_each_phase_unchanged': all(record['before']['copy']['plans/config_projection.py'] == record['after']['copy']['plans/config_projection.py'] for record in records.values()),
    'restored_stdout_exactly_matches_pristine': {mode: (OUT / ('pristine.' + mode + '.stdout.txt')).read_bytes() == (OUT / ('restored.' + mode + '.stdout.txt')).read_bytes() for mode in ('selftest', 'summary', 'json')},
}
examples = []
for suffix in ('/start_url', '/eval/reference_url', '/eval/program_html/0/url', '/eval/reference_answer_raw_annotation'):
    candidate = next((delta for delta in projected if delta['json_pointer'].endswith(suffix)), None)
    if candidate:
        examples.append(candidate)

result = {
    'mutant': 'one-line values[name].rstrip("/") before replacement at config_projection.py:146',
    'exit_codes': {phase: {mode: result['exit_code'] for mode, result in record['modes'].items()} for phase, record in records.items()},
    'selftest_output_all_phases_identical': len({record['modes']['selftest']['stdout_sha256'] for record in records.values()}) == 1,
    'stderr_bytes': {phase: {mode: result['stderr_bytes'] for mode, result in record['modes'].items()} for phase, record in records.items()},
    'total_json_scalar_mismatches': len(deltas),
    'mismatch_categories': dict(categories),
    'mismatches_by_profile': dict(collections.Counter(delta['profile'] for delta in deltas)),
    'mismatching_projected_task_count': len({(delta['profile'], delta['output_index']) for delta in projected}),
    'all_json_mismatches_path': str(OUT / 'all-json-mismatches.jsonl'),
    'all_json_mismatches_sha256': hashlib.sha256(ledger_bytes).hexdigest(),
    'summary_mismatch_count': len(summary_deltas),
    'summary_mismatches': summary_deltas,
    'exact_value_examples': examples,
    'frozen_data_literal_replacement_comparison': faithful,
    'restoration': restoration,
}
(OUT / 'analysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
