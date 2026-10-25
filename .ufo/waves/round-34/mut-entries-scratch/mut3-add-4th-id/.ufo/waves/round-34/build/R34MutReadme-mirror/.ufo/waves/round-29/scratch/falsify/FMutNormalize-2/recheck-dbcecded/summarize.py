#!/usr/bin/env python3
"""Summarize only saved follow-up observations; no instrument execution or edits."""
import hashlib
import json
from pathlib import Path

OUT = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-29/scratch/falsify/FMutNormalize-2/recheck-dbcecded')
phases = {phase: json.loads((OUT / (phase + '.capture.json')).read_text()) for phase in ('pristine', 'mutated', 'restored')}
witness = json.loads((OUT / 'official-witness.stdout.txt').read_text())
witness_run = json.loads((OUT / 'official-witness.receipt.json').read_text())
summary_lines = {phase: (OUT / (phase + '.summary.stdout.txt')).read_text().splitlines() for phase in phases}
assert len(summary_lines['pristine']) == len(summary_lines['mutated'])
summary_deltas = [{'line': i, 'expected': left, 'observed': right}
                  for i, (left, right) in enumerate(zip(summary_lines['pristine'], summary_lines['mutated']), 1)
                  if left != right]
metadata = json.loads((OUT / 'prior-report-metadata.json').read_text())
prior = Path(metadata['path']).read_bytes()
excerpts = ['SELFTEST clean cases=28', 'AssertionError', 'TOTAL findings=0 exit=0',
            'http://gitlab.invalid:1//a', 'http://gitlab.invalid:1/a',
            'http://gitlab.invalid:1//b', 'http://gitlab.invalid:1/b']
quotes = {'method': 'len(text.split())', 'excerpts': excerpts,
          'counts': [len(text.split()) for text in excerpts],
          'total_words': sum(len(text.split()) for text in excerpts)}
result = {
    'checkout_revision_observed': 'dbcecded4a04247cf6fd12919327af973da10bdd',
    'source_sha256': {phase: record['before']['copy']['plans/config_projection.py'] for phase, record in phases.items()},
    'exit_codes': {phase: {mode: data['exit_code'] for mode, data in record['modes'].items()} for phase, record in phases.items()},
    'summary_mismatches': summary_deltas,
    'copied_source_restored': phases['pristine']['before']['copy'] == phases['restored']['after']['copy'],
    'lane_hashes_unchanged': all(record[point]['lane'] == phases['pristine']['before']['lane'] for record in phases.values() for point in ('before', 'after')) and witness_run['lane_hashes_before'] == witness_run['lane_hashes_after'] == phases['pristine']['before']['lane'],
    'restored_stdout_byte_identical': {mode: (OUT / ('pristine.' + mode + '.stdout.txt')).read_bytes() == (OUT / ('restored.' + mode + '.stdout.txt')).read_bytes() for mode in ('selftest', 'summary')},
    'witness_exit': witness_run['exit_code'],
    'witness_receipt_sha256': witness_run['stdout_sha256'],
    'witness_tool_sha256': witness['tool_sha256'],
    'witness_restored_sha256': witness['restored_sha256'],
    'witness_killed': witness['killed'],
    'witness_mutant_count': len(witness['mutants']),
    'witness_mutants': {name: {key: entry[key] for key in ('selftest_exit', 'summary_exit', 'summary_total', 'killed', 'frozen_summary_alone_detects')} for name, entry in witness['mutants'].items()},
    'prior_report_metadata': metadata,
    'report_still_exact_before_append': len(prior) == metadata['bytes'] and hashlib.sha256(prior).hexdigest() == metadata['sha256'],
    'followup_quote_count': quotes,
}
(OUT / 'analysis.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
