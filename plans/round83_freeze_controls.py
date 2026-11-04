#!/usr/bin/env python3
"""Read-only pre-data anti-vacuity measurement for round83; no production verdict."""
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
ledger = json.loads((root / 'plans/grader-population-ledger.json').read_text())['members']
cases = json.loads((root / 'plans/round83-cases.json').read_text())['cases']
receipt = root / 'corpus/evidence/round83/code-from-image-probe.txt'
print('BASE 614f00559c75155ec100e945b3e8257b14fb7496')
print('C1 do-nothing located=%d executed=%d target_reached=False' % (receipt.exists(), ledger['code-from-image']['status'] == 'executed'))
print('C1 ledger-only located=%d executed=1 target_reached=False' % receipt.exists())
print('C1 fabricated-all-pass mismatches=%d target_reached=False' % sum(c['predicted'] != 'P/P' for c in cases))
for k in range(2):
    print('C1 leg=%d P=%d F=%d' % (k, sum(c['predicted'].split('/')[k]=='P' for c in cases), sum(c['predicted'].split('/')[k]=='F' for c in cases)))
rows = [json.loads(x) for x in (root / 'corpus/routed-findings.jsonl').read_text().splitlines() if x.strip()]
ids = ['R82-V%d' % i for i in range(1,9)]
registered = sum(any(r.get('id') == i for r in rows) for i in ids)
print('C2 do-nothing ids=8 registered=%d missing=%d target_reached=False' % (registered, 8-registered))
print('C2 presence-only ids=8 repair_paragraphs=%d target_reached=False' % int((root/'corpus/lessons/round-83.md').exists()))
assert not receipt.exists() and ledger['code-from-image']['status'] == 'unexecuted' and registered == 0
assert all(any(c['predicted'].split('/')[k]==v for c in cases) for k in range(2) for v in ('P','F'))
print('FREEZE-CONTROLS pass')
