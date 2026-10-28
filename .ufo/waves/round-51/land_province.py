#!/usr/bin/env python3
"""Round-51 landing: apply the C1 repairs to PROVINCE.md and the manifest.

Idempotent: every edit asserts its precondition and refuses a second application.
"""
import json
import pathlib
import sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
R = ' (round 51: probe + receipt `corpus/evidence/round51/surfaces/paths.txt`)'
NEW_ROW = (
    '| Served local model (round 51 successor) | `http://127.0.0.1:45669` (direct llama.cpp server) and '
    '`http://127.0.0.1:1234` (router, `lfm3-server.service`) — `/v1/models`, `/health`, `/props`; model id '
    '`LFM3-1.7B`, `owned_by=llamacpp`, n_ctx 32768, slots 4, build `b1-39ebd2`, alias `LFM3-1.7B`, `--model '
    '/home/vgpnk/models/lfm3/LFM3-1.7B/LFM3-1.7B-Q8_0.gguf`, pid 242776, 16 argv tokens | capability '
    'interpretation only; flag authority is kama\'s (serving plane). Capture-time pin 2026-10-28 '
    '(`corpus/evidence/round51/surfaces/endpoints.txt`), not a capability claim |')


def main() -> int:
    prov = LANE / 'PROVINCE.md'
    lines = prov.read_text().split('\n')

    def row_index(prefix):
        idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
        assert len(idx) == 1, (prefix, idx)
        return idx[0]

    edits = [
        ('| Research notes (SSOT for eval craft) |',
         ' **ABSENT 2026-10-28** — `~/Projects/webzites/repos/llm-wiki` does not resolve; no relocation '
         'under `~/Projects` or `~/archive`' + R + ' |'),
        ('| Local benchmark battery |',
         ' **ABSENT 2026-10-28** — `~/archive/bench-arena` and `~/bench-arena` both fail `test -e`; no '
         'relocation found' + R + ' |'),
        ('| Served local model |',
         ' **ABSENT 2026-10-28** — `/health` returns 000 and no socket listens on :34113; the live successor '
         'is the next row' + R + ' |'),
    ]
    for prefix, suffix in edits:
        i = row_index(prefix)
        if 'ABSENT 2026-10-28' in lines[i]:
            print('skip (already marked): %s' % prefix)
            continue
        lines[i] = lines[i].rstrip() + suffix

    if not any(l.startswith('| Served local model (round 51 successor) |') for l in lines):
        i = row_index('| Served local model |')
        lines.insert(i + 1, NEW_ROW)

    i = row_index('| Route telemetry |')
    if '**ABSENT**' in lines[i]:
        lines[i] = lines[i].replace('**ABSENT**', '**ABSENT 2026-10-28**', 1)

    i = row_index('| Public-literature registry |')
    if 'present; 25 rows' in lines[i]:
        repl = ("present; 171 rows (round 51: `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' "
                "corpus/SOURCES.md` → 171; 170 at the round-51 base tip plus S178)")
        lines[i] = lines[i].replace('present; 25 rows', repl, 1)

    prov.write_text('\n'.join(lines))

    man_path = LANE / 'plans/round51-surfaces.json'
    man = json.loads(man_path.read_text())
    for e in man['surfaces']:
        if e['id'] in ('SF01', 'SF02', 'SF03'):
            e['prose'] = 'absent'
        if e['id'] == 'SF04':
            e['anchor'] = '`~/Projects/bounties/ledger/telemetry.jsonl` —'
        if e['id'] == 'SF14':
            e['count_claim'] = 171
    if not any(e['id'] == 'SF20' for e in man['surfaces']):
        man['surfaces'].append({
            'id': 'SF20', 'section': '## Surfaces',
            'anchor': '| Served local model (round 51 successor) |',
            'state': 'present', 'prose': 'present',
            'probe': {'kind': 'http', 'urls': ['http://127.0.0.1:45669/health', 'http://127.0.0.1:1234/health']},
            'why': 'round-51 successor surface: the live OpenAI-compatible server pair on this host',
        })
    man_path.write_text(json.dumps(man, indent=2) + '\n')
    print('landed: PROVINCE rows=%d manifest entries=%d' % (len(lines), len(man['surfaces'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
