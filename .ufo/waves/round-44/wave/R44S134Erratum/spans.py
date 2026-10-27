import re, pathlib
root = pathlib.Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
src = (root/'corpus/SOURCES.md').read_text().splitlines()
rows = {}
for l in src:
    m = re.match(r'\|\s*(S\d+)\s*\|', l)
    if not m: continue
    id_ = m.group(1)
    sp = re.findall(r'([\w.\-]+\.(?:md|py|sh|c|h|toml|txt|json|yml)):(\d+)(?:-(\d+))?', l)
    rows[id_] = sp
mismatch, agree, unknown = [], 0, 0
tot = 0
for p in sorted((root/'corpus/knowledge').glob('*.md')):
    for i, l in enumerate(p.read_text().splitlines(), 1):
        if not l.startswith('source: S'): continue
        m = re.match(r'source: (S\d+) — (\S+)', l)
        if not m: continue
        sid, url = m.group(1), m.group(2)
        basename = url.rstrip('/').split('/')[-1]
        lm = re.search(r'lines (\d+)-(\d+)', l)
        if not lm: continue
        a, b = int(lm.group(1)), int(lm.group(2))
        tot += 1
        cand = [x for x in rows.get(sid, []) if x[0] == basename and x[2]]
        if not cand:
            unknown += 1; continue
        sa, sb = int(cand[0][1]), int(cand[0][2])
        if (a, b) != (sa, sb):
            mismatch.append((p.name, i, sid, basename, f'{a}-{b}', f'{sa}-{sb}'))
        else:
            agree += 1
print(f'source: lines carrying a span: {tot}; comparing to SOURCES row span for the same file: agree={agree} mismatch={len(mismatch)} no-span-in-row={unknown}')
for x in mismatch: print('MISMATCH', x)
