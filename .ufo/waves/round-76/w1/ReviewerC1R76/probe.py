import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess

L = Path('/home/vgpnk/Projects/shokunin/kengaku-shokunin')
S = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'kengaku-r76/ReviewerC1R76'
W = L / '.ufo/waves/round-76/w1/ReviewerC1R76'
G = L / 'plans/round76_c1_surface_resolver.py'
spec = importlib.util.spec_from_file_location('gate', G)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
source = G.read_text()
(W / 'gate-reviewed.py').write_text(source)
province = (L / 'PROVINCE.md').read_text()
(W / 'province-reviewed.md').write_text(province)
header = '# Fixture\n\n## Surfaces\n\n| Surface | Path / endpoint | What |\n|---|---|---|\n'
present = '| Present | `present.md` | fixture |\n'
absent = '| Absent | `missing.md` | **ABSENT 2026-11-04** |\n'
fixtures = {
 'baseline': present + absent,
 'scope-one': present,
 'marker-present': present.rstrip('\n').replace('fixture', '**ABSENT 2030-01-01**') + '\n' + absent,
 'marker-absent': present + absent.replace('2026-11-04', '2030-01-01'),
 'marker-invalid': present + absent.replace('2026-11-04', '2030-99-99'),
 'anchor-launder': '| Absent | `corpus/README.md` — missing.md research notes | research notes are still unavailable |\n',
 'endpoint-original': '| Dead server | `http://127.0.0.1:45669/health` | direct llama.cpp server model LFM3-1.7B |\n',
 'endpoint-substitute': '| Dead server | `http://127.0.0.1:1234/health` | direct llama.cpp server model LFM3-1.7B |\n',
 'tally': '| Absent | `missing.md` | missing marker |\n',
 'duplicates': '| Same surface | `present.md` | declared surface |\n| Same surface | `missing.md` | **ABSENT 2026-11-04** |\n',
 'duplicate-token': present + present,
}
rows = g.table_rows(province)
for name, remove_prose in [('scope-real-absent-only', False), ('scope-real-absent-and-prose', True)]:
    deleted = set()
    for lineno, cells in rows:
        kind, token = g.identity(cells[1])
        verdict, _ = g.resolve(kind, token, L)
        if verdict == 'absent' or (remove_prose and verdict == 'prose'):
            deleted.add(lineno)
    fixtures[name] = ''.join(line + '\n' for i, line in enumerate(province.splitlines(), 1) if i not in deleted)

commands = []
for name, body in fixtures.items():
    d = S / name
    d.mkdir(parents=True, exist_ok=True)
    (d / 'present.md').write_text('# exists\n')
    (d / 'corpus').symlink_to(L / 'corpus', target_is_directory=True)
    (d / 'grader.py').symlink_to(L / 'grader.py')
    (d / 'PROVINCE.md').write_text(body if name.startswith('scope-real') else header + body)
    (W / (name + '.PROVINCE.md')).write_text((d / 'PROVINCE.md').read_text())
    commands.append((name, ['python3', str(G), '--lane', str(d)]))
mutant = S / 'tally-mutant.py'
needle = 'f"AGREE agree={agree} disagree={disagree}"'
assert source.count(needle) == 1
mutant.write_text(source.replace(needle, 'f"AGREE agree={agree} disagree=0"'))
(W / 'tally-mutant.py').write_text(mutant.read_text())
commands.append(('tally-mutant', ['python3', str(mutant), '--lane', str(S / 'tally')]))
commands.append(('actual-baseline', ['python3', str(G), '--lane', str(L)]))
def run(item):
    name, argv = item
    p = subprocess.run(argv, capture_output=True, text=True, cwd=S)
    text = '$ ' + ' '.join(argv) + '\n' + p.stdout + p.stderr + f'EXIT {p.returncode}\n'
    (W / (name + '.txt')).write_text(text)
    return name, text
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for name, text in pool.map(run, commands):
        print('=== ' + name + ' ===\n' + text)
