#!/usr/bin/env python3
"""Scoped historical R82 evidence collection; no production writes."""
import collections
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
OUT = LANE / '.ufo/waves/round-83/w1/HistoryReceiptR83'
SCRATCH = Path('/fast/scratch/hyaku/kengaku-r83/HistoryReceiptR83')
CLONE = SCRATCH / 'clone'
REV = 'a44b2f083ee8b4115aea64598646f4bd9e3c1470'
os.environ['TMPDIR'] = str(SCRATCH / 'tmp')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(argv):
    return subprocess.run(argv, cwd=SCRATCH, env=os.environ.copy(), capture_output=True, check=False)

def receipt(name, argv, revision=REV):
    result = run(argv)
    (OUT / (name + '.stdout')).write_bytes(result.stdout)
    (OUT / (name + '.stderr')).write_bytes(result.stderr)
    header = ('COMMAND ' + shlex.join(argv) + '\nREV ' + revision + '\nEXIT ' + str(result.returncode) + '\n').encode()
    full = header + b'STDOUT_BEGIN\n' + result.stdout + b'STDOUT_END\nSTDERR_BEGIN\n' + result.stderr + b'STDERR_END\n'
    (OUT / (name + '.txt')).write_bytes(full)
    return result

actual = run(['git', '-C', str(CLONE), 'rev-parse', 'HEAD'])
assert actual.returncode == 0 and actual.stdout.decode().strip() == REV
sources = CLONE / 'corpus/SOURCES.md'
committed = run(['git', '-C', str(CLONE), 'show', REV + ':corpus/SOURCES.md'])
assert committed.returncode == 0 and sources.read_bytes() == committed.stdout
script = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
validation = receipt('r82-census-after', [script, 'validate', '--file', str(sources)])
census = receipt('r82-registry-totals', [script, 'census', '--file', str(sources)])
w04 = [line for line in validation.stdout.decode().splitlines() if len(line.split('\t')) > 1 and line.split('\t')[1] == 'W04']
(OUT / 'r82-census-metadata.json').write_text(json.dumps({'revision': REV, 'sources_sha256': sha(committed.stdout), 'tool': script, 'tool_sha256': sha(Path(script).read_bytes()), 'validation_exit': validation.returncode, 'census_exit': census.returncode, 'W04': len(w04), 'W04_expected': 27, 'stdout_sha256': sha(validation.stdout), 'stderr_sha256': sha(validation.stderr)}, indent=2) + '\n')

relative = '.ufo/waves/round-82/w1/w1-results.json'
raw = (LANE / relative).read_bytes()
(OUT / 'r82-w1-results.source.json').write_bytes(raw)
data = json.loads(raw)
rows = []
for item in data['results']:
    output = item['output']
    parsed = None
    if not output.strip():
        category = 'empty'
    else:
        try:
            parsed = json.loads(output)
        except json.JSONDecodeError:
            category = 'nonterminal_transcript'
        else:
            category = 'parseable_json_object' if isinstance(parsed, dict) else 'parseable_json_nonobject'
    rows.append({'name': item['name'], 'role': item['agent'], 'category': category, 'output_bytes': len(output.encode()), 'output_sha256': sha(output.encode()), 'outer_status_present': 'status' in item, 'explicit_output_status': parsed.get('status') if isinstance(parsed, dict) else None, 'note': item.get('note')})
counts = collections.Counter(row['category'] for row in rows)
spot_relative = 'corpus/lessons/round-82-verifier-spotcheck.md'
spot_result = run(['git', '-C', str(CLONE), 'show', '614f00559c75155ec100e945b3e8257b14fb7496:' + spot_relative])
assert spot_result.returncode == 0
spot = spot_result.stdout.decode().splitlines()
affected = ['SweepGateR82', 'SweepHarvestR82', 'ReviewerR82', 'CriticR82', 'MutationR82', 'RegistryCounterR82']
excerpt = '\n'.join(spot[172:177])
assert all(name in excerpt for name in affected)
unrecovered = [name for name in affected if next(row for row in rows if row['name'] == name)['category'] in ('empty', 'nonterminal_transcript')]
recovered = [name for name in affected if name not in unrecovered]
result = {'source': relative, 'source_sha256': sha(raw), 'source_schema': {'top_level_keys': list(data), 'result_keys': list(data['results'][0]), 'outer_status_fields': sum('status' in item for item in data['results'])}, 'seats': data['seats'], 'result_rows': len(rows), 'role_counts': dict(collections.Counter(row['role'] for row in rows)), 'output_categories': dict(counts), 'final_terminal': counts['parseable_json_object'], 'final_terminal_definition': 'Compatibility count of parseable JSON-object outputs only; not a claim of explicit terminal status or absence of provider interruption.', 'final_empty': counts['empty'], 'final_unstructured': counts['nonterminal_transcript'], 'affected': affected, 'unrecovered': unrecovered, 'recovered': recovered, 'affected_count': len(affected), 'unrecovered_count': len(unrecovered), 'recovered_count': len(recovered), 'affected_source': spot_relative + ':173-177', 'affected_source_revision': '614f00559c75155ec100e945b3e8257b14fb7496', 'affected_source_sha256': sha(spot_result.stdout), 'affected_source_excerpt': excerpt, 'interpretation': 'Six historically affected identities and two unrecovered/four revived are reported by the outside spotcheck. Output categories alone do not establish provider events, causes, timings, or histories. Final dead/empty is not interchangeable with historically interrupted.', 'results': rows}
serialized = json.dumps(result, indent=2) + '\n'
(OUT / 'r82-seat-census.json').write_text(serialized)
(OUT / 'r82-seat-counts.json').write_text(serialized)
(OUT / 'r82-seat-census-receipt.txt').write_text('COMMAND python3 ' + str(OUT / 'capture_receipts.py') + '\nSOURCE ' + str(LANE / relative) + '\nSOURCE_SHA256 ' + sha(raw) + '\nEXIT 0\nseats=' + str(data['seats']) + ' rows=' + str(len(rows)) + '\nparseable_json_object=' + str(counts['parseable_json_object']) + ' nonterminal_transcript=' + str(counts['nonterminal_transcript']) + ' empty=' + str(counts['empty']) + '\naffected=6 unrecovered=2 recovered=4 (spotcheck interpretation, not inferred provider event log)\nSOURCE_KEYS ' + ','.join(data) + '\nRESULT_KEYS ' + ','.join(data['results'][0]) + '\nOUTER_STATUS_FIELDS 0\n')

for stem in ['round82_c2_closure_debt', 'round82_c2_checks']:
    receipt(stem + '-addition', ['git', '-C', str(CLONE), 'log', REV, '--diff-filter=A', '--format=%H %s', '--', 'plans/' + stem + '.py'])
receipt('r82-c2-addition-membership', ['git', '-C', str(CLONE), 'show', '--format=fuller', '--name-status', '82fe89d5', '--', 'plans/round82_c2_closure_debt.py', 'plans/round82_c2_checks.py'])
receipt('r82-c2-wrong-attribution-membership', ['git', '-C', str(CLONE), 'show', '--format=fuller', '--name-status', 'c804dd41', '--', 'plans/round82_c2_closure_debt.py', 'plans/round82_c2_checks.py'])
print(json.dumps({'REV': REV, 'validate_exit': validation.returncode, 'census_exit': census.returncode, 'W04': len(w04), 'output_categories': dict(counts), 'role_counts': result['role_counts'], 'affected': affected, 'unrecovered': unrecovered, 'recovered': recovered}, indent=2))
