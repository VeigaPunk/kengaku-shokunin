import re, importlib.util
from pathlib import Path
lane=Path('/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/lane')
spec=importlib.util.spec_from_file_location('c2','/fast/scratch/hyaku/kengaku-r52/w2-W2RevRowsB/lane/plans/round52_c2_registry.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
NEG=re.compile(r"\bno\b[^`;\n]{0,24}?`?(--[a-z][a-z0-9-]*)`?")
def unbacked_fixed(cell):
    stripped=NEG.sub(" ", cell)                     # drop only the negated flag mention
    scripts=sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", stripped)))
    flags=sorted(set(m.FLAG.findall(stripped)))
    if len(scripts)!=1 or not flags: return False
    p=lane/scripts[0]
    if not p.exists(): return False
    body=p.read_text(errors='replace')
    return all(f not in body for f in flags)
rows=m.parse_rows(m.registry_block((lane/'SKILL.md').read_text()))
cells={r[0].strip('`'):r[4] for r in rows}
orc=cells['order-check']
cases=[
 ('landed order-check selftest cell (A3 case)', orc),
 ('negated-only', 'no `--selftest` in the script; falsifiers are external'),
 ('negation masks false positive (must be True)', 'no `--selftest` in the script; self-test `python3 plans/order_check.py --selftest` (exit 0)'),
 ('bare false claim (must be True)', 'self-test `python3 plans/order_check.py --selftest` (exit 0)'),
]
for k,v in cases:
    print(f'orig={m.selftest_unbacked(v,lane)!s:5} fixed={unbacked_fixed(v)!s:5} | {k}')
print('round40 body has --receipt/--claims:', [f for f in ('--receipt','--claims') if f in (lane/'plans/round40_c1_verify.py').read_text()])
print('scripts in landed cell:', sorted(set(re.findall(r"(?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py", orc))))
print('flags in landed cell:', sorted(set(m.FLAG.findall(orc))))
# all 28 + selftest cells: compare orig vs fixed across full registry
diff=[]
for r in rows:
    n=r[0].strip('`'); c=r[4]
    if m.selftest_unbacked(c,lane)!=unbacked_fixed(c): diff.append(n)
print('rows where orig != fixed:', diff)

# variant: attribute flags only inside a backtick span that begins `python3 <script>`
SPAN=re.compile(r"`python3 ((?:plans|corpus|grader)[A-Za-z0-9_./-]*\.py)([^`]*)`")
def unbacked_span(cell):
    stripped=NEG.sub(" ", cell)
    for mm in SPAN.finditer(stripped):
        p=lane/mm.group(1)
        flags=sorted(set(m.FLAG.findall(mm.group(2))))
        if flags and p.exists():
            body=p.read_text(errors='replace')
            if all(f not in body for f in flags): return True
    return False
print('--- span variant')
for k,v in cases: print(f'span={unbacked_span(v)!s:5} | {k}')
diff2=[r[0].strip('`') for r in rows if unbacked_span(r[4])!=m.selftest_unbacked(r[4],lane)]
print('rows where span != orig:', diff2)
