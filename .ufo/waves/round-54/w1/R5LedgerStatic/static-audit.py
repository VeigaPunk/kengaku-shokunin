import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
lane = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
spec = importlib.util.spec_from_file_location('r5counter', lane / 'plans/round54_c2_entrytruth.py')
counter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = counter
spec.loader.exec_module(counter)
def strict(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate key: ' + key)
        out[key] = value
    return out
raw = (lane / 'plans/round54-entrytruth.json').read_bytes()
ledger = json.loads(raw, object_pairs_hook=strict)
prior = json.loads((lane / 'plans/round53-tipstate.json').read_bytes(), object_pairs_hook=strict)['rows']
registry, duplicates, malformed, headings = counter.registry_rows((lane / 'SKILL.md').read_text())
rows = ledger['rows']
red = {n: s for n, s in rows.items() if s['entry_state'] == 'red'}
base_fields = {'entry_argv', 'entry_exit', 'entry_state', 'chosen', 'sec'}
result = {
    'sha256': hashlib.sha256(raw).hexdigest(),
    'schema': ledger['schema'],
    'strict_parse': 'PASS',
    'ledger_rows': len(rows), 'registry_rows': len(registry),
    'registry_headings': headings, 'registry_duplicates': duplicates, 'registry_malformed': malformed,
    'missing': sorted(set(registry) - set(rows)), 'extra': sorted(set(rows) - set(registry)),
    'green': len(rows) - len(red), 'red': len(red),
    'field_defects': [n for n,s in rows.items() if set(s) != base_fields | ({'reason','evidence'} if n in red else set())],
    'entry_mode_defects': {n: d for n,s in rows.items() if (d := counter.entry_mode_ok(s['entry_argv'], counter.row_script(registry[n])))},
    'green_noise': [n for n,s in rows.items() if n not in red and ('reason' in s or 'evidence' in s)],
    'short_reasons': [n for n,s in red.items() if len(s['reason'].split()) < 10],
    'evidence_bounds_defects': [n for n,s in red.items() if not s['evidence'].strip() or len(s['evidence']) >= 200],
    'evidence_length_range': [min(len(s['evidence']) for s in red.values()),max(len(s['evidence']) for s in red.values())],
    'r53_entry_mismatches': [n for n,s in rows.items() if s['chosen'] == 'r53-entry' and (prior[n]['kind'] != 'entry' or s['entry_argv'] != prior[n]['argv'])],
    'bare_mismatches': [n for n,s in rows.items() if s['chosen'] == 'bare' and s['entry_argv'] != ['python3',counter.row_script(registry[n])]],
    'lane_dot_mismatches': [n for n,s in rows.items() if s['chosen'] == 'lane-dot' and s['entry_argv'] != (prior[n]['argv'] if prior[n]['kind'] == 'entry' else ['python3',counter.row_script(registry[n]),'--lane','.'])],
    'chosen_counts': dict(collections.Counter(s['chosen'] for s in rows.values())),
    'noncausal_reasons': [n for n,s in red.items() if s['reason'].startswith('the instrument exits ')],
}
print(json.dumps(result, indent=2, sort_keys=True))
