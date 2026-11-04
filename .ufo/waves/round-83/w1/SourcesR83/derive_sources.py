#!/usr/bin/env python3
"""Read-only frozen-source arithmetic; writes only this seat's artifacts."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

LANE = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
OUT = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin/.ufo/waves/round-83/w1/SourcesR83')
os.environ['TMPDIR'] = '/fast/scratch/hyaku/kengaku-r83/SourcesR83/'
BASE = '614f00559c75155ec100e945b3e8257b14fb7496'
FREEZE = '6f076679931367d540c3897a4eafa0eca752e1d4'
commands = []
def frozen(rev, name):
    argv = ['git', '-C', str(LANE), 'show', f'{rev}:{name}']
    cp = subprocess.run(argv, capture_output=True, check=True)
    commands.append({'argv': argv, 'exit': cp.returncode, 'stdout_sha256': hashlib.sha256(cp.stdout).hexdigest()})
    return cp.stdout

base = frozen(BASE, 'corpus/SOURCES.md')
freeze = frozen(FREEZE, 'corpus/SOURCES.md')
claims = frozen(FREEZE, 'plans/round-83-claims.md')
(OUT / 'frozen-claims.md').write_bytes(claims)
(OUT / 'SOURCES.baseline.md').write_bytes(base)
rows = {m.group(1): m.group(0) for m in re.finditer(r'^\| (S\d+) \|.*$', base.decode(), re.M)}
freeze_rows = {m.group(1): m.group(0) for m in re.finditer(r'^\| (S\d+) \|.*$', freeze.decode(), re.M)}
old = {sid: rows[sid] for sid in ['S262', 'S263', 'S264', 'S265', 'S266']}
(OUT / 'old-rows.byte-identical.txt').write_text('\n'.join(old.values()) + '\n')
quotes = [
    ('S268', 'fetch_log-summary-date-ranges_tests_test.sh', 26, 'echo 1 > /logs/verifier/reward.txt'),
    ('S268', 'fetch_log-summary-date-ranges_tests_test.sh', [18, 22], 'uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA'),
    ('S269', 'fetch_nginx-request-logging_tests_test.sh', 20, '-w requests==2.32.4'),
    ('S269', 'fetch_nginx-request-logging_tests_test.sh', 22, '-v -rA'),
    ('S270', 'fetch_pyproject.toml', 1, '404: Not Found'),
    ('S265', 'S265-local-receipt.txt', 1, '# tb2 log-summary-date-ranges grader probe (round 81)'),
    ('S266', 'fetch_log-summary-date-ranges_instruction.md', 9, 'Write a CSV file /app/summary.csv with the following structure (including the header):'),
    ('S266', 'fetch_vulnerable-secret_instruction.md', 1, 'The goal is to extract this secret key and save it to `/app/results.txt`.'),
]
arithmetic = []
for sid, name, location, quote in quotes:
    content = (OUT / name).read_text()
    lines = content.splitlines()
    if isinstance(location, list):
        selected = ' '.join(line.strip().removesuffix('\\').strip() for line in lines[location[0]-1:location[1]])
    else:
        selected = lines[location-1]
    arithmetic.append({'id':sid,'capture':name,'location':location,'quote':quote,'tokens':len(quote.split()),'literal_in_located_bytes':quote in selected})

parts = {sid: [v.strip() for v in row.split('|')[1:-1]] for sid,row in old.items()}
a = parts['S262'].copy()
a[0] = 'S268'
a[5] = 'corpus/evidence/round82/fetch/log-summary-date-ranges_tests_test.sh:18-27, quote “uvx -p 3.13 -w pytest==8.4.1 -w pytest-json-ctrf==0.3.5 pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA” (12 words, lines 18-22; shell continuations joined) and “echo 1 > /logs/verifier/reward.txt” (4 words, line 26); sha256 4770437ea96c3cc84684b4f99d55fb148fcac09f9ea1e8ef49de487716e6c334; re-opened 2026-11-04T15:49:35Z'
a[6] = 'supersedes S262 — the reward-write quote has 4 whitespace-split tokens, not the frozen row’s 6; the continued pytest command has 12 after removing shell continuation markers. The source URL, pin and capture are unchanged; the exit-status reward rule remains the scoped teaching. The round-83 correction supersedes round-82 Gate/report annotations without rewriting them'
a[10] = 'corpus/lessons/round-83.md'
b = parts['S263'].copy()
b[0] = 'S269'
b[5] = 'corpus/evidence/round82/fetch/nginx-request-logging_tests_test.sh:17-22, quote “-w requests==2.32.4” (2 words, line 20) and “-v -rA” (2 words, line 22); sha256 27761195f53cbfe5941fe39b573631f6c926869e64b7c43220377e1e116528e7; re-opened 2026-11-04T15:49:35Z'
b[6] = 'supersedes S263 — the requests working-set quote has 2 whitespace-split tokens, not the frozen row’s 1; the verbosity/report quote remains 2. The source URL, pin and capture are unchanged; the additional requests dependency witnesses a per-task working-set variant. The round-83 correction supersedes round-82 Gate/report annotations without rewriting them'
b[10] = 'corpus/lessons/round-83.md'
c = parts['S264'].copy()
c[0] = 'S270'
c[4] = 'reachability of this exact pinned package-metadata locator, not whether the project has packaging elsewhere'
c[5] = 'HTTP response body for the source URL, re-opened 2026-11-04T15:49:35Z: HTTP 404; body line 1 quote “404: Not Found” (3 words, 14 bytes); response-body sha256 d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed; no upstream source-content anchor exists'
c[6] = 'supersedes S264 — REJECTED: this exact pinned pyproject.toml locator returned HTTP 404, so its source content is unreachable and cannot ground a packaging claim; this is not evidence of fabrication or of absent packaging elsewhere; flip: a reachable authoritative package-metadata locator at an explicitly named revision supplies an anchored quote, with any changed revision recorded as a new source row'
c[7] = 'rejected'
c[10] = 'corpus/lessons/round-83.md'
a[4] = 'round-83 annotation correction for the pinned reward-write quote: mechanically derived whitespace-token count and unchanged source binding'
b[4] = 'round-83 annotation correction for the pinned requests working-set quote: mechanically derived whitespace-token count and unchanged source binding'
new = '\n'.join('| ' + ' | '.join(p) + ' |' for p in [a,b,c]) + '\n'
(OUT / 'SOURCES.append.md').write_text(new)
proposed = base.replace(b'## Paths', new.encode() + b'## Paths', 1)
(OUT / 'SOURCES.proposed.full.md').write_bytes(proposed)
def census(data):
    rr = [[v.strip() for v in row.split('|')[1:-1]] for row in data.decode().splitlines() if re.match(r'^\| S\d+ \|',row)]
    ids = [r[0] for r in rr]
    return {'rows':len(rr),'malformed':sum(len(r)!=11 for r in rr),'tiers':dict(collections.Counter(r[3] for r in rr)),'statuses':dict(collections.Counter(r[7] for r in rr)),'duplicate_ids':[sid for sid,n in collections.Counter(ids).items() if n>1]}
result = {'axes':['coverage','calibration'],'base':BASE,'freeze':FREEZE,'commands':commands,'baseline':census(base),'sources_seat_proposed':census(proposed),'quotes':arithmetic,'old_rows_equal_base_freeze':{sid:old[sid]==freeze_rows.get(sid) for sid in old},'old_row_sha256':{sid:hashlib.sha256((row+'\n').encode()).hexdigest() for sid,row in old.items()},'new_row_source_cells_preserved':{'S268':a[1]==parts['S262'][1],'S269':b[1]==parts['S263'][1],'S270':c[1]==parts['S264'][1]},'capture_equals_historical':{},'full_draft_limit':'Seat-only full file, excludes independently owned S267. Integrator must merge append fragment; do not replace a concurrently integrated SOURCES file.'}
for capture, historical in [('fetch_log-summary-date-ranges_tests_test.sh','corpus/evidence/round82/fetch/log-summary-date-ranges_tests_test.sh'),('fetch_nginx-request-logging_tests_test.sh','corpus/evidence/round82/fetch/nginx-request-logging_tests_test.sh'),('S265-local-receipt.txt','corpus/evidence/round81/log-summary-date-ranges-probe.txt')]:
    pinned=frozen(BASE,historical)
    result['capture_equals_historical'][capture]=(OUT/capture).read_bytes()==pinned
result['commands']=commands
(OUT/'derivation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
